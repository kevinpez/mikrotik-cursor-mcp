from typing import Optional

from ..connector import execute_mikrotik_command
from ..api_fallback import api_fallback_execute
from ..logger import app_logger


# ============================================================================
# IPv6 FIREWALL FILTER RULES
# ============================================================================

def mikrotik_list_ipv6_filter_rules() -> str:
    """
    Lists all IPv6 firewall filter rules.
    
    Returns:
        List of IPv6 filter rules
    """
    app_logger.info("Listing IPv6 firewall filter rules")
    
    cmd = "/ipv6 firewall filter print"
    result = execute_mikrotik_command(cmd)
    
    return f"IPv6 FIREWALL FILTER RULES:\n\n{result}"


def mikrotik_create_ipv6_filter_rule(
        chain: str,
        rule_action: str,
        protocol: Optional[str] = None,
        src_address: Optional[str] = None,
        dst_address: Optional[str] = None,
        src_port: Optional[str] = None,
        dst_port: Optional[str] = None,
        in_interface: Optional[str] = None,
        out_interface: Optional[str] = None,
        connection_state: Optional[str] = None,
        disabled: bool = False,
        comment: Optional[str] = None
) -> str:
    """
    Creates an IPv6 firewall filter rule.
    
    Args:
        chain: Chain name (input, forward, output)
        rule_action: Action to take (accept, drop, reject, etc.)
        protocol: Protocol (tcp, udp, icmpv6, etc.)
        src_address: Source IPv6 address
        dst_address: Destination IPv6 address
        src_port: Source port
        dst_port: Destination port
        in_interface: Input interface
        out_interface: Output interface
        connection_state: Connection state (established, related, new, invalid)
        disabled: Disable the rule
        comment: Optional comment
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Creating IPv6 firewall filter rule in chain: {chain}")
    
    cmd = f"/ipv6 firewall filter add chain={chain} action={rule_action}"
    
    if protocol:
        cmd += f" protocol={protocol}"
    if src_address:
        cmd += f' src-address="{src_address}"'
    if dst_address:
        cmd += f' dst-address="{dst_address}"'
    if src_port:
        cmd += f" src-port={src_port}"
    if dst_port:
        cmd += f" dst-port={dst_port}"
    if in_interface:
        cmd += f" in-interface={in_interface}"
    if out_interface:
        cmd += f" out-interface={out_interface}"
    if connection_state:
        cmd += f" connection-state={connection_state}"
    if disabled:
        cmd += " disabled=yes"
    if comment:
        cmd += f' comment="{comment}"'
    
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to create IPv6 firewall rule: {result}"
    
    return f"IPv6 firewall rule created in chain '{chain}' successfully."


def mikrotik_remove_ipv6_filter_rule(rule_id: str) -> str:
    """
    Removes an IPv6 firewall filter rule.
    
    Args:
        rule_id: Rule ID or number
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Removing IPv6 firewall filter rule: {rule_id}")
    
    cmd = f"/ipv6 firewall filter remove {rule_id}"
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to remove IPv6 firewall rule: {result}"
    
    return f"IPv6 firewall rule '{rule_id}' removed successfully."


# ============================================================================
# IPv6 FIREWALL NAT (NAT66)
# ============================================================================

def mikrotik_list_ipv6_nat_rules() -> str:
    """
    Lists all IPv6 NAT rules (NAT66).
    
    Returns:
        List of IPv6 NAT rules
    """
    app_logger.info("Listing IPv6 NAT rules")
    
    cmd = "/ipv6 firewall nat print"
    result = execute_mikrotik_command(cmd)
    
    return f"IPv6 NAT RULES:\n\n{result}"


def mikrotik_create_ipv6_nat_rule(
        chain: str,
        action: str,
        src_address: Optional[str] = None,
        dst_address: Optional[str] = None,
        out_interface: Optional[str] = None,
        to_addresses: Optional[str] = None,
        comment: Optional[str] = None
) -> str:
    """
    Creates an IPv6 NAT rule.
    
    Args:
        chain: Chain name (srcnat, dstnat)
        action: Action (src-nat, dst-nat, masquerade)
        src_address: Source IPv6 address
        dst_address: Destination IPv6 address
        out_interface: Output interface
        to_addresses: Translation address
        comment: Optional comment
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Creating IPv6 NAT rule in chain: {chain}")
    
    cmd = f"/ipv6 firewall nat add chain={chain} action={action}"
    
    if src_address:
        cmd += f' src-address="{src_address}"'
    if dst_address:
        cmd += f' dst-address="{dst_address}"'
    if out_interface:
        cmd += f" out-interface={out_interface}"
    if to_addresses:
        cmd += f' to-addresses="{to_addresses}"'
    if comment:
        cmd += f' comment="{comment}"'
    
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to create IPv6 NAT rule: {result}"
    
    return f"IPv6 NAT rule created in chain '{chain}' successfully."


def mikrotik_remove_ipv6_nat_rule(rule_id: str) -> str:
    """
    Removes an IPv6 NAT rule.
    
    Args:
        rule_id: Rule ID or number
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Removing IPv6 NAT rule: {rule_id}")
    
    cmd = f"/ipv6 firewall nat remove {rule_id}"
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to remove IPv6 NAT rule: {result}"
    
    return f"IPv6 NAT rule '{rule_id}' removed successfully."


# ============================================================================
# IPv6 FIREWALL ADDRESS LISTS
# ============================================================================

def mikrotik_list_ipv6_address_lists(list_name: Optional[str] = None) -> str:
    """
    Lists IPv6 firewall address lists.
    
    Args:
        list_name: Filter by list name
    
    Returns:
        List of IPv6 address list entries
    """
    app_logger.info("Listing IPv6 firewall address lists")
    
    cmd = "/ipv6 firewall address-list print"
    
    if list_name:
        cmd += f' where list="{list_name}"'
    
    result = execute_mikrotik_command(cmd)
    
    return f"IPv6 ADDRESS LISTS:\n\n{result}"


def mikrotik_add_ipv6_address_list(
        list_name: str,
        address: str,
        timeout: Optional[str] = None,
        comment: Optional[str] = None
) -> str:
    """
    Adds an IPv6 address to a firewall address list.
    
    Args:
        list_name: Name of the address list
        address: IPv6 address to add
        timeout: Optional timeout for dynamic entries
        comment: Optional comment
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Adding {address} to IPv6 address list: {list_name}")
    
    cmd = f'/ipv6 firewall address-list add list={list_name} address="{address}"'
    
    if timeout:
        cmd += f" timeout={timeout}"
    if comment:
        cmd += f' comment="{comment}"'
    
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to add address to list: {result}"
    
    return f"IPv6 address '{address}' added to list '{list_name}' successfully."


def mikrotik_remove_ipv6_address_list_entry(entry_id: str) -> str:
    """
    Removes an IPv6 address from a firewall address list.
    
    Args:
        entry_id: Entry ID to remove
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Removing IPv6 address list entry: {entry_id}")
    
    cmd = f"/ipv6 firewall address-list remove {entry_id}"
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to remove address list entry: {result}"
    
    return f"IPv6 address list entry '{entry_id}' removed successfully."


# ============================================================================
# IPv6 FIREWALL MANGLE
# ============================================================================

def mikrotik_list_ipv6_mangle_rules() -> str:
    """
    Lists all IPv6 firewall mangle rules.
    
    Returns:
        List of IPv6 mangle rules
    """
    app_logger.info("Listing IPv6 firewall mangle rules")
    
    cmd = "/ipv6 firewall mangle print"
    result = execute_mikrotik_command(cmd)
    
    return f"IPv6 MANGLE RULES:\n\n{result}"


def mikrotik_create_ipv6_mangle_rule(
        chain: str,
        action: str,
        protocol: Optional[str] = None,
        src_address: Optional[str] = None,
        dst_address: Optional[str] = None,
        new_routing_mark: Optional[str] = None,
        passthrough: bool = True,
        comment: Optional[str] = None
) -> str:
    """
    Creates an IPv6 firewall mangle rule.
    
    Args:
        chain: Chain name (prerouting, postrouting, input, output, forward)
        action: Action (mark-routing, mark-packet, change-ttl, etc.)
        protocol: Protocol
        src_address: Source IPv6 address
        dst_address: Destination IPv6 address
        new_routing_mark: New routing mark name
        passthrough: Enable passthrough
        comment: Optional comment
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Creating IPv6 mangle rule in chain: {chain}")
    
    cmd = f"/ipv6 firewall mangle add chain={chain} action={action}"
    
    if protocol:
        cmd += f" protocol={protocol}"
    if src_address:
        cmd += f' src-address="{src_address}"'
    if dst_address:
        cmd += f' dst-address="{dst_address}"'
    if new_routing_mark:
        cmd += f" new-routing-mark={new_routing_mark}"
    cmd += f' passthrough={"yes" if passthrough else "no"}'
    if comment:
        cmd += f' comment="{comment}"'
    
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to create IPv6 mangle rule: {result}"
    
    return f"IPv6 mangle rule created in chain '{chain}' successfully."


def mikrotik_remove_ipv6_mangle_rule(rule_id: str) -> str:
    """
    Removes an IPv6 firewall mangle rule.
    
    Args:
        rule_id: Rule ID or number
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Removing IPv6 mangle rule: {rule_id}")
    
    cmd = f"/ipv6 firewall mangle remove {rule_id}"
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to remove IPv6 mangle rule: {result}"
    
    return f"IPv6 mangle rule '{rule_id}' removed successfully."

