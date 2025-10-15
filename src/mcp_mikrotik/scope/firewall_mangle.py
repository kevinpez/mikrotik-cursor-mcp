"""
Firewall Mangle rule management for MikroTik RouterOS.
Mangle rules are used for packet marking, TTL modification, and policy-based routing.
"""
from typing import Optional
from ..connector import execute_mikrotik_command
from ..logger import app_logger


def mikrotik_list_mangle_rules(
    chain_filter: Optional[str] = None,
    action_filter: Optional[str] = None,
    disabled_only: bool = False
) -> str:
    """
    List firewall mangle rules.
    READ-ONLY operation - safe to run.
    
    Args:
        chain_filter: Filter by chain (prerouting, postrouting, input, output, forward)
        action_filter: Filter by action type
        disabled_only: Show only disabled rules
    """
    app_logger.info(f"Listing mangle rules: chain={chain_filter}")
    
    cmd = "/ip firewall mangle print detail"
    
    filters = []
    if chain_filter:
        filters.append(f'chain={chain_filter}')
    if action_filter:
        filters.append(f'action~"{action_filter}"')
    if disabled_only:
        filters.append("disabled=yes")
    
    if filters:
        cmd += " where " + " and ".join(filters)
    
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return "No mangle rules found."
    
    return f"FIREWALL MANGLE RULES:\n\n{result}"


def mikrotik_create_mangle_rule(
    chain: str,
    mangle_action: str,
    src_address: Optional[str] = None,
    dst_address: Optional[str] = None,
    protocol: Optional[str] = None,
    src_port: Optional[str] = None,
    dst_port: Optional[str] = None,
    in_interface: Optional[str] = None,
    out_interface: Optional[str] = None,
    new_packet_mark: Optional[str] = None,
    new_connection_mark: Optional[str] = None,
    new_routing_mark: Optional[str] = None,
    passthrough: bool = True,
    comment: Optional[str] = None
) -> str:
    """
    Create a firewall mangle rule.
    
    ⚠️ Test on non-critical traffic first!
    
    Args:
        chain: Mangle chain (prerouting, postrouting, input, output, forward)
        mangle_action: Action (mark-packet, mark-connection, mark-routing, change-ttl, etc.)
        src_address: Source IP address
        dst_address: Destination IP address
        protocol: Protocol (tcp, udp, icmp, etc.)
        src_port: Source port
        dst_port: Destination port
        in_interface: Input interface
        out_interface: Output interface
        new_packet_mark: Packet mark to set
        new_connection_mark: Connection mark to set
        new_routing_mark: Routing mark to set
        passthrough: Whether to continue processing (default: True)
        comment: Optional comment
    """
    app_logger.info(f"Creating mangle rule: chain={chain}, action={mangle_action}")
    
    # Validate chain
    valid_chains = ["prerouting", "postrouting", "input", "output", "forward"]
    if chain not in valid_chains:
        return f"Error: Invalid chain '{chain}'. Must be one of: {', '.join(valid_chains)}"
    
    # Build command
    cmd = f'/ip firewall mangle add chain={chain} action={mangle_action}'
    
    # Add matching criteria
    if src_address:
        cmd += f' src-address={src_address}'
    if dst_address:
        cmd += f' dst-address={dst_address}'
    if protocol:
        cmd += f' protocol={protocol}'
    if src_port:
        cmd += f' src-port={src_port}'
    if dst_port:
        cmd += f' dst-port={dst_port}'
    if in_interface:
        cmd += f' in-interface={in_interface}'
    if out_interface:
        cmd += f' out-interface={out_interface}'
    
    # Add action-specific parameters
    if new_packet_mark:
        cmd += f' new-packet-mark={new_packet_mark}'
    if new_connection_mark:
        cmd += f' new-connection-mark={new_connection_mark}'
    if new_routing_mark:
        cmd += f' new-routing-mark={new_routing_mark}'
    
    # Add passthrough
    cmd += f' passthrough={"yes" if passthrough else "no"}'
    
    if comment:
        cmd += f' comment="{comment}"'
    
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to create mangle rule: {result}"
    
    return f"Mangle rule created successfully in chain '{chain}'."


def mikrotik_remove_mangle_rule(rule_id: str) -> str:
    """
    Remove a firewall mangle rule.
    
    ⚠️ Ensure rule is not critical for traffic flow!
    """
    app_logger.info(f"Removing mangle rule: {rule_id}")
    
    cmd = f'/ip firewall mangle remove {rule_id}'
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to remove mangle rule: {result}"
    
    return f"Mangle rule {rule_id} removed successfully."


def mikrotik_update_mangle_rule(
    rule_id: str,
    mangle_action: Optional[str] = None,
    new_packet_mark: Optional[str] = None,
    new_connection_mark: Optional[str] = None,
    new_routing_mark: Optional[str] = None,
    disabled: Optional[bool] = None,
    comment: Optional[str] = None
) -> str:
    """
    Update firewall mangle rule.
    
    ⚠️ Changes may affect traffic routing!
    """
    app_logger.info(f"Updating mangle rule: {rule_id}")
    
    cmd = f'/ip firewall mangle set {rule_id}'
    
    if mangle_action:
        cmd += f' action={mangle_action}'
    if new_packet_mark:
        cmd += f' new-packet-mark={new_packet_mark}'
    if new_connection_mark:
        cmd += f' new-connection-mark={new_connection_mark}'
    if new_routing_mark:
        cmd += f' new-routing-mark={new_routing_mark}'
    if disabled is not None:
        cmd += f' disabled={"yes" if disabled else "no"}'
    if comment:
        cmd += f' comment="{comment}"'
    
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to update mangle rule: {result}"
    
    return f"Mangle rule {rule_id} updated successfully."


def mikrotik_create_routing_mark(
    name: str,
    src_address: Optional[str] = None,
    dst_address: Optional[str] = None,
    in_interface: Optional[str] = None,
    comment: Optional[str] = None
) -> str:
    """
    Create a routing mark for policy-based routing.
    This is a helper that creates a mangle rule with mark-routing action.
    
    ⚠️ Policy routing changes how traffic is routed!
    """
    app_logger.info(f"Creating routing mark: {name}")
    
    return mikrotik_create_mangle_rule(
        chain="prerouting",
        mangle_action="mark-routing",
        src_address=src_address,
        dst_address=dst_address,
        in_interface=in_interface,
        new_routing_mark=name,
        passthrough=True,
        comment=comment or f"Routing mark: {name}"
    )


def mikrotik_list_routing_marks() -> str:
    """
    List all routing marks (mangle rules with mark-routing action).
    READ-ONLY operation - safe to run.
    """
    app_logger.info("Listing routing marks")
    
    return mikrotik_list_mangle_rules(action_filter="mark-routing")

