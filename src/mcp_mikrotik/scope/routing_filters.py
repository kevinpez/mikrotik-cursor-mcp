"""
Routing filter management for MikroTik RouterOS.
For BGP/OSPF route filtering and policy-based routing.
"""
from typing import Optional
from ..connector import execute_mikrotik_command
from ..logger import app_logger


def mikrotik_create_route_filter(
    chain: str,
    prefix: str,
    prefix_length: Optional[str] = None,
    action: str = "accept",
    comment: Optional[str] = None
) -> str:
    """Create route filter rule."""
    app_logger.info(f"Creating route filter: chain={chain}, prefix={prefix}")
    
    cmd = f'/routing filter add chain={chain} prefix={prefix} action={action}'
    
    if prefix_length:
        cmd += f' prefix-length={prefix_length}'
    if comment:
        cmd += f' comment="{comment}"'
    
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to create route filter: {result}"
    
    return f"Route filter created in chain '{chain}'."


def mikrotik_list_route_filters(chain_filter: Optional[str] = None) -> str:
    """List route filters. READ-ONLY - safe."""
    app_logger.info(f"Listing route filters: chain={chain_filter}")
    
    cmd = "/routing filter print detail"
    
    if chain_filter:
        cmd += f' where chain={chain_filter}'
    
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return "No route filters found."
    
    return f"ROUTE FILTERS:\n\n{result}"

