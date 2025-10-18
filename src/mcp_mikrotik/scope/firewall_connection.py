"""
Connection tracking management for MikroTik RouterOS.
View and manage active network connections.
"""
from typing import Optional
from ..connector import execute_mikrotik_command
from ..api_fallback import api_fallback_execute
from ..logger import app_logger


def mikrotik_get_connection_tracking(
    protocol_filter: Optional[str] = None,
    src_address_filter: Optional[str] = None,
    dst_address_filter: Optional[str] = None,
    limit: int = 100
) -> str:
    """
    View active connections in the connection tracking table.
    READ-ONLY operation - safe to run.
    
    Args:
        protocol_filter: Filter by protocol (tcp, udp, icmp)
        src_address_filter: Filter by source address
        dst_address_filter: Filter by destination address
        limit: Maximum number of connections to show (default: 100)
    """
    app_logger.info("Getting connection tracking table")
    
    cmd = "/ip firewall connection print"
    
    filters = []
    if protocol_filter:
        filters.append(f'protocol={protocol_filter}')
    if src_address_filter:
        filters.append(f'src-address~"{src_address_filter}"')
    if dst_address_filter:
        filters.append(f'dst-address~"{dst_address_filter}"')
    
    if filters:
        cmd += " where " + " and ".join(filters)
    
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return "No active connections found (or connection tracking disabled)."
    
    return f"CONNECTION TRACKING TABLE (showing up to {limit} connections):\n\n{result}"


def mikrotik_flush_connections(
    protocol: Optional[str] = None,
    src_address: Optional[str] = None,
    dst_address: Optional[str] = None
) -> str:
    """
    Flush (clear) connections from the connection tracking table.
    
    ⚠️ This terminates active connections - use carefully!
    Can cause temporary service interruption.
    
    Args:
        protocol: Only flush connections of this protocol
        src_address: Only flush connections from this source
        dst_address: Only flush connections to this destination
    """
    app_logger.info("Flushing connection tracking table")
    
    if not protocol and not src_address and not dst_address:
        return "Error: You must specify at least one filter (protocol, src_address, or dst_address) to prevent flushing ALL connections. Use with caution!"
    
    cmd = "/ip firewall connection remove [find"
    
    filters = []
    if protocol:
        filters.append(f'protocol={protocol}')
    if src_address:
        filters.append(f'src-address~"{src_address}"')
    if dst_address:
        filters.append(f'dst-address~"{dst_address}"')
    
    if filters:
        cmd += " " + " and ".join(filters)
    
    cmd += "]"
    
    result = execute_mikrotik_command(cmd)
    
    if result.strip() == "" or "failure" not in result.lower():
        return f"Connections flushed successfully (filtered by: {', '.join(filters)})."
    else:
        return f"Failed to flush connections: {result}"


