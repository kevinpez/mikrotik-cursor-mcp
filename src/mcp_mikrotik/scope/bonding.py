"""
Bonding (link aggregation) management for MikroTik RouterOS.
"""
from typing import Optional
from ..connector import execute_mikrotik_command
from ..api_fallback import api_fallback_execute
from ..logger import app_logger


def mikrotik_list_bonding_interfaces(name_filter: Optional[str] = None) -> str:
    """List bonding interfaces. READ-ONLY - safe."""
    app_logger.info(f"Listing bonding interfaces: name={name_filter}")
    
    cmd = "/interface bonding print detail"
    
    if name_filter:
        cmd += f' where name~"{name_filter}"'
    
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return "No bonding interfaces found."
    
    return f"BONDING INTERFACES:\n\n{result}"


def mikrotik_create_bonding_interface(
    name: str,
    mode: str = "802.3ad",
    slaves: Optional[str] = None,
    mtu: int = 1500,
    comment: Optional[str] = None
) -> str:
    """
    Create bonding interface (link aggregation).
    
    Args:
        name: Bonding interface name
        mode: Bonding mode (balance-rr, active-backup, balance-xor, broadcast, 802.3ad, balance-tlb, balance-alb)
        slaves: Comma-separated list of slave interfaces (e.g., 'ether1,ether2')
        mtu: MTU size
        comment: Optional comment
    """
    app_logger.info(f"Creating bonding interface: {name}")
    
    cmd = f'/interface bonding add name={name} mode={mode} mtu={mtu}'
    
    if slaves:
        cmd += f' slaves={slaves}'
    if comment:
        cmd += f' comment="{comment}"'
    
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to create bonding interface: {result}"
    
    return f"Bonding interface '{name}' created successfully."


def mikrotik_add_bonding_slave(bonding_interface: str, slave_interface: str) -> str:
    """Add interface to bonding group."""
    app_logger.info(f"Adding {slave_interface} to bonding {bonding_interface}")
    
    # Get current slaves
    cmd = f'/interface bonding set [find name={bonding_interface}] slaves=[get [find name={bonding_interface}] slaves],{slave_interface}'
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to add slave: {result}"
    
    return f"Interface '{slave_interface}' added to bonding '{bonding_interface}'."


def mikrotik_remove_bonding_interface(name: str) -> str:
    """Remove bonding interface."""
    app_logger.info(f"Removing bonding interface: {name}")
    
    cmd = f'/interface bonding remove [find name={name}]'
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to remove bonding interface: {result}"
    
    return f"Bonding interface '{name}' removed successfully."

