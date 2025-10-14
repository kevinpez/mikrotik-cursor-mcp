from typing import Optional
from ..connector import execute_mikrotik_command
from ..logger import app_logger

def mikrotik_list_interfaces(
    name_filter: Optional[str] = None,
    type_filter: Optional[str] = None,
    running_only: bool = False,
    disabled_only: bool = False
) -> str:
    """List network interfaces"""
    app_logger.info(f"Listing interfaces: name={name_filter}, type={type_filter}")
    
    cmd = "/interface print"
    
    filters = []
    if name_filter:
        filters.append(f'name~"{name_filter}"')
    if type_filter:
        filters.append(f'type="{type_filter}"')
    if running_only:
        filters.append("running=yes")
    if disabled_only:
        filters.append("disabled=yes")
    
    if filters:
        cmd += " where " + " and ".join(filters)
    
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return "No interfaces found matching the criteria."
    
    return f"INTERFACES:\n\n{result}"

def mikrotik_get_interface_stats(interface_name: str) -> str:
    """Get traffic statistics for a specific interface"""
    app_logger.info(f"Getting interface stats: {interface_name}")
    
    cmd = f'/interface print stats where name="{interface_name}"'
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return f"Interface '{interface_name}' not found."
    
    return f"INTERFACE STATISTICS ({interface_name}):\n\n{result}"

def mikrotik_enable_interface(interface_name: str) -> str:
    """Enable a network interface"""
    app_logger.info(f"Enabling interface: {interface_name}")
    
    cmd = f'/interface enable "{interface_name}"'
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to enable interface: {result}"
    
    return f"Interface '{interface_name}' enabled successfully."

def mikrotik_disable_interface(interface_name: str) -> str:
    """Disable a network interface"""
    app_logger.info(f"Disabling interface: {interface_name}")
    
    cmd = f'/interface disable "{interface_name}"'
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to disable interface: {result}"
    
    return f"Interface '{interface_name}' disabled successfully."

def mikrotik_get_interface_monitor(interface_name: str) -> str:
    """Monitor interface in real-time (single snapshot)"""
    app_logger.info(f"Monitoring interface: {interface_name}")
    
    cmd = f'/interface monitor-traffic "{interface_name}" once'
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return f"Unable to monitor interface '{interface_name}'."
    
    return f"INTERFACE MONITOR ({interface_name}):\n\n{result}"

def mikrotik_list_bridge_ports(bridge_name: Optional[str] = None) -> str:
    """List bridge ports"""
    app_logger.info(f"Listing bridge ports: bridge={bridge_name}")
    
    cmd = "/interface bridge port print"
    
    if bridge_name:
        cmd += f' where bridge="{bridge_name}"'
    
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return "No bridge ports found."
    
    return f"BRIDGE PORTS:\n\n{result}"

def mikrotik_add_bridge_port(bridge: str, interface: str) -> str:
    """Add an interface to a bridge"""
    app_logger.info(f"Adding {interface} to bridge {bridge}")
    
    cmd = f'/interface bridge port add bridge="{bridge}" interface="{interface}"'
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to add bridge port: {result}"
    
    return f"Interface '{interface}' added to bridge '{bridge}' successfully."

def mikrotik_remove_bridge_port(interface: str) -> str:
    """Remove an interface from its bridge"""
    app_logger.info(f"Removing {interface} from bridge")
    
    # First find the port entry
    find_cmd = f'/interface bridge port print terse where interface="{interface}"'
    find_result = execute_mikrotik_command(find_cmd)
    
    if not find_result.strip() or "no such item" in find_result.lower():
        return f"Interface '{interface}' is not a bridge port."
    
    # Remove by interface name
    cmd = f'/interface bridge port remove [find where interface="{interface}"]'
    result = execute_mikrotik_command(cmd)
    
    if result.strip() == "" or "failure" not in result.lower():
        return f"Interface '{interface}' removed from bridge successfully."
    else:
        return f"Failed to remove bridge port: {result}"

def mikrotik_get_interface_traffic(interface_name: str) -> str:
    """Get current traffic for an interface"""
    app_logger.info(f"Getting traffic for: {interface_name}")
    
    cmd = f'/interface print stats where name="{interface_name}"'
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return f"Interface '{interface_name}' not found."
    
    return f"TRAFFIC STATS ({interface_name}):\n\n{result}"

