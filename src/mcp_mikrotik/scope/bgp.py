"""
BGP (Border Gateway Protocol) management for MikroTik RouterOS.
For enterprise routing, multi-homing, and internet peering.
"""
from typing import Optional
from ..connector import execute_mikrotik_command
from ..logger import app_logger


def mikrotik_create_bgp_instance(
    name: str,
    as_number: int,
    router_id: str,
    redistribute_connected: bool = False,
    redistribute_static: bool = False,
    comment: Optional[str] = None
) -> str:
    """Create BGP routing instance."""
    app_logger.info(f"Creating BGP instance: {name} (AS {as_number})")
    
    cmd = f'/routing bgp instance add name={name} as={as_number} router-id={router_id}'
    cmd += f' redistribute-connected={"yes" if redistribute_connected else "no"}'
    cmd += f' redistribute-static={"yes" if redistribute_static else "no"}'
    
    if comment:
        cmd += f' comment="{comment}"'
    
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to create BGP instance: {result}"
    
    return f"BGP instance '{name}' created successfully (AS {as_number})."


def mikrotik_add_bgp_peer(
    name: str,
    instance: str,
    remote_address: str,
    remote_as: int,
    multihop: bool = False,
    route_reflect: bool = False,
    comment: Optional[str] = None
) -> str:
    """Add BGP peer/neighbor."""
    app_logger.info(f"Adding BGP peer: {name} to {remote_address}")
    
    cmd = f'/routing bgp peer add name={name} instance={instance} remote-address={remote_address} remote-as={remote_as}'
    cmd += f' multihop={"yes" if multihop else "no"}'
    cmd += f' route-reflect={"yes" if route_reflect else "no"}'
    
    if comment:
        cmd += f' comment="{comment}"'
    
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to add BGP peer: {result}"
    
    return f"BGP peer '{name}' added successfully."


def mikrotik_list_bgp_peers(instance_filter: Optional[str] = None) -> str:
    """List BGP peers and their status. READ-ONLY - safe."""
    app_logger.info(f"Listing BGP peers: instance={instance_filter}")
    
    cmd = "/routing bgp peer print detail"
    
    if instance_filter:
        cmd += f' where instance={instance_filter}'
    
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return "No BGP peers configured."
    
    return f"BGP PEERS:\n\n{result}"


def mikrotik_add_bgp_network(
    instance: str,
    network: str,
    synchronize: bool = False,
    comment: Optional[str] = None
) -> str:
    """Advertise network via BGP."""
    app_logger.info(f"Adding BGP network: {network}")
    
    cmd = f'/routing bgp network add instance={instance} network={network}'
    cmd += f' synchronize={"yes" if synchronize else "no"}'
    
    if comment:
        cmd += f' comment="{comment}"'
    
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to add BGP network: {result}"
    
    return f"BGP network '{network}' added successfully."


def mikrotik_list_bgp_networks(instance_filter: Optional[str] = None) -> str:
    """List BGP advertised networks. READ-ONLY - safe."""
    app_logger.info("Listing BGP networks")
    
    cmd = "/routing bgp network print detail"
    
    if instance_filter:
        cmd += f' where instance={instance_filter}'
    
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return "No BGP networks configured."
    
    return f"BGP NETWORKS:\n\n{result}"


def mikrotik_list_bgp_routes() -> str:
    """View BGP routing table. READ-ONLY - safe."""
    app_logger.info("Listing BGP routes")
    
    cmd = "/routing bgp route print"
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return "No BGP routes in routing table."
    
    return f"BGP ROUTING TABLE:\n\n{result}"


def mikrotik_get_bgp_status(instance: Optional[str] = None) -> str:
    """Get BGP instance status. READ-ONLY - safe."""
    app_logger.info(f"Getting BGP status: instance={instance}")
    
    if instance:
        cmd = f'/routing bgp instance print detail where name={instance}'
    else:
        cmd = "/routing bgp instance print detail"
    
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return "No BGP instances configured."
    
    return f"BGP STATUS:\n\n{result}"


def mikrotik_clear_bgp_session(peer: str) -> str:
    """Reset BGP session (soft reset)."""
    app_logger.info(f"Clearing BGP session: {peer}")
    
    cmd = f'/routing bgp peer reset [find name={peer}]'
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to reset BGP session: {result}"
    
    return f"BGP session for peer '{peer}' reset successfully."

