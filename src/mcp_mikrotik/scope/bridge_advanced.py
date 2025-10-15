from typing import Optional
from ..connector import execute_mikrotik_command
from ..logger import app_logger

def mikrotik_list_bridges(
    name_filter: Optional[str] = None,
    disabled_only: bool = False
) -> str:
    """
    Lists bridge interfaces on MikroTik device.
    
    Args:
        name_filter: Filter by bridge name
        disabled_only: Show only disabled bridges
    
    Returns:
        List of bridge interfaces
    """
    app_logger.info(f"Listing bridges: name_filter={name_filter}")
    
    cmd = "/interface bridge print detail"
    
    filters = []
    if name_filter:
        filters.append(f'name~"{name_filter}"')
    if disabled_only:
        filters.append("disabled=yes")
    
    if filters:
        cmd += " where " + " ".join(filters)
    
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return "No bridges found matching the criteria."
    
    return f"BRIDGES:\n\n{result}"

def mikrotik_create_bridge(
    name: str,
    vlan_filtering: bool = False,
    protocol_mode: str = "rstp",
    priority: int = 32768,
    igmp_snooping: bool = False,
    mtu: int = 1500,
    comment: Optional[str] = None,
    disabled: bool = False
) -> str:
    """
    Creates a bridge interface with advanced options.
    
    Args:
        name: Name for the bridge
        vlan_filtering: Enable VLAN filtering
        protocol_mode: STP protocol (none, rstp, stp, mstp)
        priority: Bridge priority (0-65535)
        igmp_snooping: Enable IGMP snooping
        mtu: Maximum Transmission Unit
        comment: Optional comment
        disabled: Whether to disable after creation
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Creating bridge: name={name}")
    
    if not name or name.strip() == "":
        return "Error: Bridge name cannot be empty."
    
    valid_protocols = ["none", "rstp", "stp", "mstp"]
    if protocol_mode not in valid_protocols:
        return f"Error: Invalid protocol mode '{protocol_mode}'. Must be one of: {', '.join(valid_protocols)}"
    
    cmd = f'/interface bridge add name="{name}"'
    cmd += f' vlan-filtering={"yes" if vlan_filtering else "no"}'
    cmd += f' protocol-mode={protocol_mode}'
    cmd += f' priority={priority}'
    cmd += f' igmp-snooping={"yes" if igmp_snooping else "no"}'
    cmd += f' mtu={mtu}'
    
    if comment:
        cmd += f' comment="{comment}"'
    
    if disabled:
        cmd += " disabled=yes"
    
    result = execute_mikrotik_command(cmd)
    
    if result.strip() and ("*" in result or result.strip().isdigit()):
        bridge_id = result.strip()
        details_cmd = f"/interface bridge print detail where .id={bridge_id}"
        details = execute_mikrotik_command(details_cmd)
        return f"Bridge created successfully:\n\n{details}"
    else:
        return f"Failed to create bridge: {result}" if result else "Bridge creation completed."

def mikrotik_update_bridge(
    bridge_id: str,
    vlan_filtering: Optional[bool] = None,
    protocol_mode: Optional[str] = None,
    priority: Optional[int] = None,
    igmp_snooping: Optional[bool] = None,
    comment: Optional[str] = None,
    disabled: Optional[bool] = None
) -> str:
    """
    Updates an existing bridge interface.
    
    Args:
        bridge_id: ID or name of the bridge
        vlan_filtering: Enable/disable VLAN filtering
        protocol_mode: Change STP protocol
        priority: New bridge priority
        igmp_snooping: Enable/disable IGMP snooping
        comment: New comment
        disabled: Enable/disable the bridge
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Updating bridge: bridge_id={bridge_id}")
    
    cmd = f"/interface bridge set {bridge_id}"
    updates = []
    
    if vlan_filtering is not None:
        updates.append(f'vlan-filtering={"yes" if vlan_filtering else "no"}')
    
    if protocol_mode:
        valid_protocols = ["none", "rstp", "stp", "mstp"]
        if protocol_mode not in valid_protocols:
            return f"Error: Invalid protocol mode. Must be one of: {', '.join(valid_protocols)}"
        updates.append(f'protocol-mode={protocol_mode}')
    
    if priority is not None:
        updates.append(f'priority={priority}')
    
    if igmp_snooping is not None:
        updates.append(f'igmp-snooping={"yes" if igmp_snooping else "no"}')
    
    if comment is not None:
        updates.append(f'comment="{comment}"')
    
    if disabled is not None:
        updates.append(f'disabled={"yes" if disabled else "no"}')
    
    if not updates:
        return "No updates specified."
    
    cmd += " " + " ".join(updates)
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to update bridge: {result}"
    
    details_cmd = f"/interface bridge print detail where .id={bridge_id}"
    details = execute_mikrotik_command(details_cmd)
    return f"Bridge updated successfully:\n\n{details}"

def mikrotik_list_bridge_vlans(
    bridge_filter: Optional[str] = None,
    vlan_ids: Optional[str] = None
) -> str:
    """
    Lists VLAN configurations on bridges.
    
    Args:
        bridge_filter: Filter by bridge name
        vlan_ids: Filter by VLAN IDs
    
    Returns:
        List of bridge VLAN configurations
    """
    app_logger.info(f"Listing bridge VLANs: bridge={bridge_filter}")
    
    cmd = "/interface bridge vlan print detail"
    
    filters = []
    if bridge_filter:
        filters.append(f'bridge~"{bridge_filter}"')
    if vlan_ids:
        filters.append(f'vlan-ids~"{vlan_ids}"')
    
    if filters:
        cmd += " where " + " ".join(filters)
    
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return "No bridge VLAN configurations found."
    
    return f"BRIDGE VLANS:\n\n{result}"

def mikrotik_add_bridge_vlan(
    bridge: str,
    vlan_ids: str,
    tagged: str,
    untagged: Optional[str] = None,
    comment: Optional[str] = None
) -> str:
    """
    Adds VLAN configuration to a bridge.
    
    Args:
        bridge: Bridge name
        vlan_ids: VLAN IDs (e.g., "10" or "10-20")
        tagged: Tagged ports (comma-separated)
        untagged: Untagged ports (comma-separated)
        comment: Optional comment
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Adding bridge VLAN: bridge={bridge}, vlan_ids={vlan_ids}")
    
    cmd = f'/interface bridge vlan add bridge="{bridge}" vlan-ids={vlan_ids} tagged="{tagged}"'
    
    if untagged:
        cmd += f' untagged="{untagged}"'
    
    if comment:
        cmd += f' comment="{comment}"'
    
    result = execute_mikrotik_command(cmd)
    
    if result.strip() and ("*" in result or result.strip().isdigit()):
        return f"Bridge VLAN configuration added successfully."
    else:
        return f"Failed to add bridge VLAN: {result}" if result else "Bridge VLAN added."

def mikrotik_remove_bridge_vlan(vlan_id: str) -> str:
    """
    Removes a VLAN configuration from a bridge.
    
    Args:
        vlan_id: ID of the VLAN configuration to remove
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Removing bridge VLAN: vlan_id={vlan_id}")
    
    cmd = f"/interface bridge vlan remove {vlan_id}"
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to remove bridge VLAN: {result}"
    
    return f"Bridge VLAN configuration removed successfully."

def mikrotik_set_bridge_port_vlan(
    port: str,
    bridge: str,
    pvid: int = 1,
    frame_types: str = "admit-all",
    ingress_filtering: bool = False
) -> str:
    """
    Configures VLAN settings for a bridge port.
    
    Args:
        port: Port interface name
        bridge: Bridge name
        pvid: Port VLAN ID (default VLAN)
        frame_types: Frame types to accept (admit-all, admit-only-vlan-tagged, admit-only-untagged-and-priority-tagged)
        ingress_filtering: Enable ingress filtering
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Setting bridge port VLAN: port={port}, pvid={pvid}")
    
    valid_frame_types = ["admit-all", "admit-only-vlan-tagged", "admit-only-untagged-and-priority-tagged"]
    if frame_types not in valid_frame_types:
        return f"Error: Invalid frame_types. Must be one of: {', '.join(valid_frame_types)}"
    
    # Find the port in bridge ports
    find_cmd = f'/interface bridge port print where interface="{port}" and bridge="{bridge}"'
    find_result = execute_mikrotik_command(find_cmd)
    
    if not find_result or find_result.strip() == "":
        return f"Bridge port not found: {port} on bridge {bridge}"
    
    # Update the port
    cmd = f'/interface bridge port set [find interface="{port}" and bridge="{bridge}"]'
    cmd += f' pvid={pvid}'
    cmd += f' frame-types={frame_types}'
    cmd += f' ingress-filtering={"yes" if ingress_filtering else "no"}'
    
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to update bridge port VLAN settings: {result}"
    
    return f"Bridge port VLAN settings updated for {port}."

def mikrotik_enable_bridge_vlan_filtering(bridge_name: str) -> str:
    """
    Enables VLAN filtering on a bridge.
    
    Args:
        bridge_name: Name of the bridge
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Enabling VLAN filtering on bridge: {bridge_name}")
    
    return mikrotik_update_bridge(bridge_name, vlan_filtering=True)

def mikrotik_disable_bridge_vlan_filtering(bridge_name: str) -> str:
    """
    Disables VLAN filtering on a bridge.
    
    Args:
        bridge_name: Name of the bridge
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Disabling VLAN filtering on bridge: {bridge_name}")
    
    return mikrotik_update_bridge(bridge_name, vlan_filtering=False)

def mikrotik_get_bridge_settings(bridge_id: str) -> str:
    """
    Gets detailed settings for a specific bridge.
    
    Args:
        bridge_id: ID or name of the bridge
    
    Returns:
        Detailed bridge settings
    """
    app_logger.info(f"Getting bridge settings: bridge_id={bridge_id}")
    
    cmd = f'/interface bridge print detail where (.id={bridge_id} or name="{bridge_id}")'
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return f"Bridge '{bridge_id}' not found."
    
    return f"BRIDGE SETTINGS:\n\n{result}"

def mikrotik_set_bridge_protocol(
    bridge_id: str,
    protocol_mode: str,
    priority: Optional[int] = None
) -> str:
    """
    Sets the spanning tree protocol for a bridge.
    
    Args:
        bridge_id: ID or name of the bridge
        protocol_mode: Protocol mode (none, rstp, stp, mstp)
        priority: Bridge priority (0-65535)
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Setting bridge protocol: bridge_id={bridge_id}, protocol={protocol_mode}")
    
    valid_protocols = ["none", "rstp", "stp", "mstp"]
    if protocol_mode not in valid_protocols:
        return f"Error: Invalid protocol mode. Must be one of: {', '.join(valid_protocols)}"
    
    return mikrotik_update_bridge(bridge_id, protocol_mode=protocol_mode, priority=priority)

def mikrotik_enable_igmp_snooping(bridge_id: str) -> str:
    """
    Enables IGMP snooping on a bridge.
    
    Args:
        bridge_id: ID or name of the bridge
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Enabling IGMP snooping on bridge: {bridge_id}")
    
    return mikrotik_update_bridge(bridge_id, igmp_snooping=True)

def mikrotik_disable_igmp_snooping(bridge_id: str) -> str:
    """
    Disables IGMP snooping on a bridge.
    
    Args:
        bridge_id: ID or name of the bridge
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Disabling IGMP snooping on bridge: {bridge_id}")
    
    return mikrotik_update_bridge(bridge_id, igmp_snooping=False)

def mikrotik_create_vlan_aware_bridge(
    name: str,
    ports: list,
    vlan_config: list,
    protocol_mode: str = "rstp"
) -> str:
    """
    Creates a complete VLAN-aware bridge setup.
    
    Args:
        name: Bridge name
        ports: List of port interfaces
        vlan_config: List of VLAN configurations [{"vlan_id": 10, "tagged": ["ether1"], "untagged": ["ether2"]}]
        protocol_mode: STP protocol mode
    
    Returns:
        Setup result
    """
    app_logger.info(f"Creating VLAN-aware bridge: {name}")
    
    results = []
    
    # Create bridge with VLAN filtering
    bridge_result = mikrotik_create_bridge(
        name=name,
        vlan_filtering=True,
        protocol_mode=protocol_mode,
        comment=f"VLAN-aware bridge {name}"
    )
    results.append(f"✓ Bridge created: {name}")
    
    # Add ports to bridge
    for port in ports:
        add_port_cmd = f'/interface bridge port add bridge="{name}" interface="{port}"'
        execute_mikrotik_command(add_port_cmd)
        results.append(f"✓ Port added: {port}")
    
    # Configure VLANs
    for vlan in vlan_config:
        vlan_id = vlan.get("vlan_id")
        tagged = ",".join(vlan.get("tagged", []))
        untagged = ",".join(vlan.get("untagged", []))
        
        if tagged or untagged:
            mikrotik_add_bridge_vlan(
                bridge=name,
                vlan_ids=str(vlan_id),
                tagged=tagged,
                untagged=untagged if untagged else None
            )
            results.append(f"✓ VLAN {vlan_id} configured")
    
    return "VLAN-AWARE BRIDGE SETUP:\n\n" + "\n".join(results)

