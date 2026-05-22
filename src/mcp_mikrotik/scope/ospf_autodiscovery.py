"""
OSPF auto-discovery helpers for MikroTik RouterOS.
"""

from __future__ import annotations

import hashlib
import ipaddress
from typing import Optional

from ..connector import execute_mikrotik_command
from ..logger import app_logger
from .ospf import (
    mikrotik_add_ospf_interface,
    mikrotik_add_ospf_network,
    mikrotik_create_ospf_area,
    mikrotik_create_ospf_instance,
)


def _has_routeros_error(result: str) -> bool:
    return any(
        token in result.lower()
        for token in ("failure:", "error", "bad command", "syntax error")
    )


def _site_index(site_id: str) -> int:
    digest = hashlib.sha256(site_id.encode("utf-8")).digest()
    return int.from_bytes(digest[:4], "big") % 254 + 1


def _calculate_assignment(site_id: str, base_subnet: str) -> dict[str, str]:
    try:
        network = ipaddress.ip_network(base_subnet, strict=False)
    except ValueError as exc:
        raise ValueError(f"Invalid base_subnet '{base_subnet}': {exc}") from exc

    if network.version != 4:
        raise ValueError(
            "OSPF auto-discovery currently supports IPv4 base subnets only."
        )

    index = _site_index(site_id)
    if network.prefixlen <= 24:
        subnet_count = 2 ** (24 - network.prefixlen)
        offset = ((index - 1) % subnet_count) * 256
        assigned_subnet = ipaddress.ip_network(
            (int(network.network_address) + offset, 24)
        )
    else:
        assigned_subnet = network

    router_id = f"100.100.{(index - 1) // 254}.{index}"
    return {
        "site_id": site_id,
        "subnet": str(assigned_subnet),
        "router_id": router_id,
        "router_id_network": f"{router_id}/32",
    }


def _format_section(title: str, body: str) -> str:
    body = body.strip() if body else ""
    return f"{title}:\n{body or 'No output returned.'}"


def mikrotik_scan_mikrotik_neighbors() -> str:
    """Scan for MikroTik neighbors using MNDP. READ-ONLY."""
    app_logger.info("Scanning MikroTik neighbors")

    result = execute_mikrotik_command("/ip neighbor print detail")
    if not result or result.strip() == "":
        return "No MikroTik neighbors discovered."

    return f"MIKROTIK NEIGHBORS:\n\n{result}"


def mikrotik_get_ospf_assignments() -> str:
    """Return OSPF instance, area, network, and interface state. READ-ONLY."""
    app_logger.info("Getting OSPF auto-discovery assignments")

    commands = [
        ("OSPF INSTANCES", "/routing ospf instance print detail"),
        ("OSPF AREAS", "/routing ospf area print detail"),
        ("OSPF NETWORKS", "/routing ospf network print detail"),
        ("OSPF INTERFACES", "/routing ospf interface print detail"),
    ]
    sections = []
    for title, command in commands:
        sections.append(_format_section(title, execute_mikrotik_command(command)))

    return "OSPF AUTO-DISCOVERY ASSIGNMENTS:\n\n" + "\n\n".join(sections)


def mikrotik_auto_assign_ospf_subnet(
    site_id: str,
    base_subnet: str = "192.168.100.0/24",
) -> str:
    """Generate a deterministic subnet and router ID assignment for a site."""
    app_logger.info(f"Assigning OSPF subnet for site_id={site_id}")

    try:
        assignment = _calculate_assignment(site_id, base_subnet)
    except ValueError as exc:
        return f"Error: {exc}"

    return (
        "OSPF AUTO-DISCOVERY ASSIGNMENT:\n\n"
        f"site_id: {assignment['site_id']}\n"
        f"subnet: {assignment['subnet']}\n"
        f"router_id: {assignment['router_id']}\n"
        f"router_id_network: {assignment['router_id_network']}"
    )


def mikrotik_auto_configure_ospf_instance(
    instance_name: str = "auto-ospf",
    router_id: Optional[str] = None,
    comment: str = "Auto-OSPF Instance",
) -> str:
    """Configure an OSPF instance using the existing OSPF helper."""
    return mikrotik_create_ospf_instance(
        name=instance_name,
        router_id=router_id,
        redistribute_connected=True,
        redistribute_static=False,
        comment=comment,
    )


def mikrotik_auto_configure_ospf_area(
    area_name: str = "backbone",
    instance_name: str = "auto-ospf",
    area_id: str = "0.0.0.0",
    comment: str = "Backbone Area",
) -> str:
    """Configure an OSPF area using the existing OSPF helper."""
    return mikrotik_create_ospf_area(
        name=area_name,
        area_id=area_id,
        instance=instance_name,
        comment=comment,
    )


def mikrotik_auto_configure_ospf_networks(
    subnet: str,
    router_id: str,
    area_name: str = "backbone",
    instance_name: str = "auto-ospf",
) -> str:
    """Advertise the assigned site subnet and router ID host route in OSPF."""
    app_logger.info(
        f"Configuring OSPF networks: subnet={subnet}, router_id={router_id}"
    )

    subnet_result = mikrotik_add_ospf_network(
        subnet, area=area_name, instance=instance_name
    )
    router_id_result = mikrotik_add_ospf_network(
        router_id, area=area_name, instance=instance_name
    )

    return "\n\n".join(
        [
            _format_section("OSPF SUBNET NETWORK", subnet_result),
            _format_section("OSPF ROUTER-ID NETWORK", router_id_result),
        ]
    )


def mikrotik_auto_configure_ospf_interfaces(
    management_interface: str = "ether1",
    area_name: str = "backbone",
    instance_name: str = "auto-ospf",
) -> str:
    """Configure OSPF on the management interface."""
    return mikrotik_add_ospf_interface(
        interface=management_interface,
        comment=f"Auto-OSPF interface for {instance_name}/{area_name}",
    )


def mikrotik_enable_ospf_instance(instance_name: str = "auto-ospf") -> str:
    """Enable an OSPF instance."""
    app_logger.info(f"Enabling OSPF instance: {instance_name}")

    result = execute_mikrotik_command(
        f'/routing ospf instance enable [find name="{instance_name}"]'
    )
    if _has_routeros_error(result):
        result = execute_mikrotik_command(
            f'/routing ospf instance set [find name="{instance_name}"] disabled=no'
        )

    if _has_routeros_error(result):
        return f"Failed to enable OSPF instance '{instance_name}': {result}"

    details = execute_mikrotik_command(
        f'/routing ospf instance print detail where name="{instance_name}"'
    )
    return f"OSPF instance '{instance_name}' enabled successfully.\n\n{details}"


def mikrotik_auto_discovery_ospf_complete(
    site_id: str,
    management_interface: str = "ether1",
    instance_name: str = "auto-ospf",
    area_name: str = "backbone",
) -> str:
    """Run the full OSPF auto-discovery configuration workflow for a site."""
    app_logger.info(f"Running complete OSPF auto-discovery for site_id={site_id}")

    assignment = _calculate_assignment(site_id, "192.168.100.0/24")
    steps = [
        _format_section(
            "ASSIGNMENT",
            mikrotik_auto_assign_ospf_subnet(site_id, "192.168.100.0/24"),
        ),
        _format_section(
            "INSTANCE",
            mikrotik_auto_configure_ospf_instance(
                instance_name=instance_name,
                router_id=assignment["router_id"],
            ),
        ),
        _format_section(
            "AREA",
            mikrotik_auto_configure_ospf_area(
                area_name=area_name,
                instance_name=instance_name,
            ),
        ),
        _format_section(
            "NETWORKS",
            mikrotik_auto_configure_ospf_networks(
                subnet=assignment["subnet"],
                router_id=assignment["router_id_network"],
                area_name=area_name,
                instance_name=instance_name,
            ),
        ),
        _format_section(
            "INTERFACE",
            mikrotik_auto_configure_ospf_interfaces(
                management_interface=management_interface,
                area_name=area_name,
                instance_name=instance_name,
            ),
        ),
        _format_section("ENABLE", mikrotik_enable_ospf_instance(instance_name)),
    ]

    return "OSPF AUTO-DISCOVERY COMPLETE:\n\n" + "\n\n".join(steps)


def mikrotik_get_ospf_auto_discovery_status() -> str:
    """Return OSPF auto-discovery status. READ-ONLY."""
    app_logger.info("Getting OSPF auto-discovery status")

    return "\n\n".join(
        [
            mikrotik_get_ospf_assignments(),
            _format_section(
                "MIKROTIK NEIGHBORS",
                execute_mikrotik_command("/ip neighbor print detail"),
            ),
        ]
    )
