"""
OSPF (Open Shortest Path First) management for MikroTik RouterOS.
For dynamic routing in enterprise networks.
"""
from typing import Optional
from ..connector import execute_mikrotik_command
from ..api_fallback import api_fallback_execute
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


# ============================================================================
# OSPF AUTHENTICATION - NEW in v4.8.0
# ============================================================================

def mikrotik_configure_ospf_authentication(
    interface: str,
    auth_type: str,
    auth_key: str,
    auth_key_id: int = 1,
    comment: Optional[str] = None
) -> str:
    """
    Configures OSPF authentication on an interface.
    
    Args:
        interface: Interface name or OSPF interface ID
        auth_type: Authentication type (simple, md5, none)
        auth_key: Authentication key/password
        auth_key_id: Key ID for MD5 authentication (1-255)
        comment: Optional comment
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Configuring OSPF authentication on {interface}: type={auth_type}")
    
    valid_auth_types = ["simple", "md5", "none"]
    if auth_type not in valid_auth_types:
        return f"Error: Invalid auth_type '{auth_type}'. Must be one of: {', '.join(valid_auth_types)}"
    
    if auth_type != "none" and (not auth_key or auth_key.strip() == ""):
        return "Error: Authentication key is required for simple and MD5 authentication."
    
    if not 1 <= auth_key_id <= 255:
        return "Error: Auth key ID must be between 1 and 255."
    
    # Find the OSPF interface
    find_cmd = f'/routing ospf interface print where interface="{interface}"'
    find_result = execute_mikrotik_command(find_cmd)
    
    if not find_result or find_result.strip() == "":
        return f"OSPF interface '{interface}' not found. Please configure OSPF on the interface first."
    
    # Configure authentication
    cmd = f'/routing ospf interface set [find interface="{interface}"]'
    cmd += f' authentication={auth_type}'
    
    if auth_type == "md5":
        cmd += f' authentication-key="{auth_key}" authentication-key-id={auth_key_id}'
    elif auth_type == "simple":
        cmd += f' authentication-key="{auth_key}"'
    
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to configure OSPF authentication: {result}"
    
    # Get the updated configuration
    details_cmd = f'/routing ospf interface print detail where interface="{interface}"'
    details = execute_mikrotik_command(details_cmd)
    
    return f"OSPF authentication configured successfully on '{interface}':\n\n{details}"

def mikrotik_list_ospf_auth_keys(interface_filter: Optional[str] = None) -> str:
    """
    Lists OSPF authentication configurations.
    
    Args:
        interface_filter: Filter by interface name
    
    Returns:
        List of OSPF interfaces with authentication settings
    """
    app_logger.info(f"Listing OSPF authentication: interface_filter={interface_filter}")
    
    cmd = "/routing ospf interface print detail"
    
    if interface_filter:
        cmd += f' where interface~"{interface_filter}"'
    
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return "No OSPF interfaces found."
    
    # Filter to show only interfaces with authentication
    lines = result.split('\n')
    auth_interfaces = []
    current_interface = []
    
    for line in lines:
        if line.strip() and not line.startswith(' '):
            if current_interface:
                interface_text = '\n'.join(current_interface)
                if 'authentication=' in interface_text and 'authentication=none' not in interface_text:
                    auth_interfaces.append(interface_text)
            current_interface = [line]
        elif current_interface:
            current_interface.append(line)
    
    # Check last interface
    if current_interface:
        interface_text = '\n'.join(current_interface)
        if 'authentication=' in interface_text and 'authentication=none' not in interface_text:
            auth_interfaces.append(interface_text)
    
    if not auth_interfaces:
        return "No OSPF interfaces with authentication configured."
    
    return f"OSPF AUTHENTICATION CONFIGURATIONS:\n\n" + "\n\n".join(auth_interfaces)


