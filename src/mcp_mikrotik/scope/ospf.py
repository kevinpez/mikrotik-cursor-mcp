"""
OSPF (Open Shortest Path First) management for MikroTik RouterOS.
For dynamic routing in enterprise networks.
"""
from typing import Optional
from ..connector import execute_mikrotik_command
from ..logger import app_logger


def mikrotik_create_ospf_instance(
    name: str = "default",
    router_id: Optional[str] = None,
    redistribute_connected: bool = False,
    redistribute_static: bool = False,
    comment: Optional[str] = None
) -> str:
    """Create OSPF routing instance."""
    app_logger.info(f"Creating OSPF instance: {name}")
    
    cmd = f'/routing ospf instance add name={name}'
    
    if router_id:
        cmd += f' router-id={router_id}'
    cmd += f' redistribute-connected={"yes" if redistribute_connected else "no"}'
    cmd += f' redistribute-static={"yes" if redistribute_static else "no"}'
    
    if comment:
        cmd += f' comment="{comment}"'
    
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to create OSPF instance: {result}"
    
    return f"OSPF instance '{name}' created successfully."


def mikrotik_add_ospf_network(
    network: str,
    area: str = "backbone",
    instance: str = "default",
    comment: Optional[str] = None
) -> str:
    """Add network to OSPF."""
    app_logger.info(f"Adding OSPF network: {network}")
    
    cmd = f'/routing ospf network add network={network} area={area}'
    
    if comment:
        cmd += f' comment="{comment}"'
    
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to add OSPF network: {result}"
    
    return f"OSPF network '{network}' added to area '{area}'."


def mikrotik_add_ospf_interface(
    interface: str,
    network_type: str = "broadcast",
    cost: int = 10,
    priority: int = 1,
    comment: Optional[str] = None
) -> str:
    """Configure OSPF on interface."""
    app_logger.info(f"Adding OSPF interface: {interface}")
    
    cmd = f'/routing ospf interface add interface={interface} network-type={network_type} cost={cost} priority={priority}'
    
    if comment:
        cmd += f' comment="{comment}"'
    
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to add OSPF interface: {result}"
    
    return f"OSPF enabled on interface '{interface}'."


def mikrotik_list_ospf_neighbors() -> str:
    """List OSPF neighbors. READ-ONLY - safe."""
    app_logger.info("Listing OSPF neighbors")
    
    cmd = "/routing ospf neighbor print detail"
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return "No OSPF neighbors found."
    
    return f"OSPF NEIGHBORS:\n\n{result}"


def mikrotik_list_ospf_routes() -> str:
    """View OSPF routes. READ-ONLY - safe."""
    app_logger.info("Listing OSPF routes")
    
    cmd = "/routing ospf route print"
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return "No OSPF routes found."
    
    return f"OSPF ROUTES:\n\n{result}"


def mikrotik_get_ospf_status(instance: str = "default") -> str:
    """Get OSPF instance status. READ-ONLY - safe."""
    app_logger.info(f"Getting OSPF status: {instance}")
    
    cmd = f'/routing ospf instance print detail where name={instance}'
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return f"OSPF instance '{instance}' not found."
    
    return f"OSPF STATUS ({instance}):\n\n{result}"


def mikrotik_create_ospf_area(
    name: str,
    area_id: str,
    instance: str = "default",
    area_type: str = "default",
    comment: Optional[str] = None
) -> str:
    """Configure OSPF area."""
    app_logger.info(f"Creating OSPF area: {name}")
    
    cmd = f'/routing ospf area add name={name} area-id={area_id} instance={instance} type={area_type}'
    
    if comment:
        cmd += f' comment="{comment}"'
    
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to create OSPF area: {result}"
    
    return f"OSPF area '{name}' (ID: {area_id}) created successfully."

