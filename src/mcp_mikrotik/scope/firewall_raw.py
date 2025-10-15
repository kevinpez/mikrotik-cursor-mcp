"""
Firewall RAW rule management for MikroTik RouterOS.
RAW rules bypass connection tracking for performance optimization.
"""
from typing import Optional
from ..connector import execute_mikrotik_command
from ..logger import app_logger


def mikrotik_list_raw_rules(
    chain_filter: Optional[str] = None,
    disabled_only: bool = False
) -> str:
    """
    List firewall RAW rules.
    READ-ONLY operation - safe to run.
    
    Args:
        chain_filter: Filter by chain (prerouting, output)
        disabled_only: Show only disabled rules
    """
    app_logger.info(f"Listing RAW rules: chain={chain_filter}")
    
    cmd = "/ip firewall raw print detail"
    
    filters = []
    if chain_filter:
        filters.append(f'chain={chain_filter}')
    if disabled_only:
        filters.append("disabled=yes")
    
    if filters:
        cmd += " where " + " and ".join(filters)
    
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return "No RAW firewall rules found."
    
    return f"FIREWALL RAW RULES:\n\n{result}"


def mikrotik_create_raw_rule(
    chain: str,
    raw_action: str,
    src_address: Optional[str] = None,
    dst_address: Optional[str] = None,
    protocol: Optional[str] = None,
    src_port: Optional[str] = None,
    dst_port: Optional[str] = None,
    in_interface: Optional[str] = None,
    out_interface: Optional[str] = None,
    comment: Optional[str] = None
) -> str:
    """
    Create a firewall RAW rule.
    
    ⚠️ RAW rules affect connection tracking - use carefully!
    Common use: bypass connection tracking for high-traffic servers
    
    Args:
        chain: RAW chain (prerouting, output)
        raw_action: Action (accept, drop, notrack)
        src_address: Source IP
        dst_address: Destination IP
        protocol: Protocol
        src_port: Source port
        dst_port: Destination port
        in_interface: Input interface
        out_interface: Output interface
        comment: Optional comment
    """
    app_logger.info(f"Creating RAW rule: chain={chain}, action={raw_action}")
    
    # Validate chain
    valid_chains = ["prerouting", "output"]
    if chain not in valid_chains:
        return f"Error: Invalid RAW chain '{chain}'. Must be one of: {', '.join(valid_chains)}"
    
    # Build command
    cmd = f'/ip firewall raw add chain={chain} action={raw_action}'
    
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
    if comment:
        cmd += f' comment="{comment}"'
    
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to create RAW rule: {result}"
    
    return f"RAW firewall rule created successfully in chain '{chain}'."


def mikrotik_remove_raw_rule(rule_id: str) -> str:
    """
    Remove a firewall RAW rule.
    
    ⚠️ Ensure rule is not critical!
    """
    app_logger.info(f"Removing RAW rule: {rule_id}")
    
    cmd = f'/ip firewall raw remove {rule_id}'
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to remove RAW rule: {result}"
    
    return f"RAW rule {rule_id} removed successfully."

