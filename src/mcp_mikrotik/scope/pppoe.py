"""
PPPoE client and server management for MikroTik RouterOS.
"""
from typing import Optional
from ..connector import execute_mikrotik_command
from ..api_fallback import api_fallback_execute
from ..logger import app_logger


def mikrotik_list_pppoe_clients(
    name_filter: Optional[str] = None,
    disabled_only: bool = False
) -> str:
    """List PPPoE client interfaces. READ-ONLY - safe."""
    app_logger.info(f"Listing PPPoE clients: name={name_filter}")
    
    cmd = "/interface pppoe-client print detail"
    
    filters = []
    if name_filter:
        filters.append(f'name~"{name_filter}"')
    if disabled_only:
        filters.append("disabled=yes")
    
    if filters:
        cmd += " where " + " and ".join(filters)
    
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return "No PPPoE client interfaces found."
    
    return f"PPPOE CLIENT INTERFACES:\n\n{result}"


def mikrotik_create_pppoe_client(
    name: str,
    interface: str,
    user: str,
    password: str,
    add_default_route: bool = True,
    use_peer_dns: bool = True,
    comment: Optional[str] = None
) -> str:
    """Create PPPoE client interface (for ISP connections)."""
    app_logger.info(f"Creating PPPoE client: {name}")
    
    cmd = f'/interface pppoe-client add name={name} interface={interface} user={user} password={password}'
    cmd += f' add-default-route={"yes" if add_default_route else "no"}'
    cmd += f' use-peer-dns={"yes" if use_peer_dns else "no"}'
    
    if comment:
        cmd += f' comment="{comment}"'
    
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to create PPPoE client: {result}"
    
    return f"PPPoE client '{name}' created successfully."


def mikrotik_remove_pppoe_client(name: str) -> str:
    """Remove PPPoE client interface."""
    app_logger.info(f"Removing PPPoE client: {name}")
    
    cmd = f'/interface pppoe-client remove [find name={name}]'
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to remove PPPoE client: {result}"
    
    return f"PPPoE client '{name}' removed successfully."


def mikrotik_get_pppoe_status(name: str) -> str:
    """Get PPPoE client status. READ-ONLY - safe."""
    app_logger.info(f"Getting PPPoE status: {name}")
    
    cmd = f'/interface pppoe-client print detail where name={name}'
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return f"PPPoE client '{name}' not found."
    
    return f"PPPOE STATUS ({name}):\n\n{result}"


def mikrotik_list_pppoe_servers() -> str:
    """List PPPoE servers. READ-ONLY - safe."""
    app_logger.info("Listing PPPoE servers")
    
    cmd = "/interface pppoe-server server print detail"
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return "No PPPoE servers configured."
    
    return f"PPPOE SERVERS:\n\n{result}"

