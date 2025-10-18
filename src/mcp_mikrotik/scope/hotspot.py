"""
Hotspot (captive portal) management for MikroTik RouterOS.
For guest WiFi and public network access control.
"""
from typing import Optional
from ..connector import execute_mikrotik_command
from ..api_fallback import api_fallback_execute
from ..logger import app_logger


def mikrotik_list_hotspot_servers(name_filter: Optional[str] = None) -> str:
    """List hotspot servers. READ-ONLY - safe."""
    app_logger.info(f"Listing hotspot servers: name={name_filter}")
    
    cmd = "/ip hotspot print detail"
    
    if name_filter:
        cmd += f' where name~"{name_filter}"'
    
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return "No hotspot servers found."
    
    return f"HOTSPOT SERVERS:\n\n{result}"


def mikrotik_create_hotspot_server(
    name: str,
    interface: str,
    address_pool: str,
    profile: str = "default",
    comment: Optional[str] = None
) -> str:
    """Create hotspot server on an interface."""
    app_logger.info(f"Creating hotspot server: {name}")
    
    cmd = f'/ip hotspot add name={name} interface={interface} address-pool={address_pool} profile={profile}'
    
    if comment:
        cmd += f' comment="{comment}"'
    
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to create hotspot server: {result}"
    
    return f"Hotspot server '{name}' created successfully."


def mikrotik_remove_hotspot_server(name: str) -> str:
    """Remove hotspot server."""
    app_logger.info(f"Removing hotspot server: {name}")
    
    cmd = f'/ip hotspot remove [find name={name}]'
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to remove hotspot server: {result}"
    
    return f"Hotspot server '{name}' removed successfully."


def mikrotik_list_hotspot_users(server_filter: Optional[str] = None) -> str:
    """List hotspot users. READ-ONLY - safe."""
    app_logger.info(f"Listing hotspot users: server={server_filter}")
    
    cmd = "/ip hotspot user print detail"
    
    if server_filter:
        cmd += f' where server={server_filter}'
    
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return "No hotspot users found."
    
    return f"HOTSPOT USERS:\n\n{result}"


def mikrotik_create_hotspot_user(
    name: str,
    password: str,
    server: str = "all",
    profile: str = "default",
    limit_uptime: Optional[str] = None,
    comment: Optional[str] = None
) -> str:
    """Create hotspot user."""
    app_logger.info(f"Creating hotspot user: {name}")
    
    cmd = f'/ip hotspot user add name={name} password={password} server={server} profile={profile}'
    
    if limit_uptime:
        cmd += f' limit-uptime={limit_uptime}'
    if comment:
        cmd += f' comment="{comment}"'
    
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to create hotspot user: {result}"
    
    return f"Hotspot user '{name}' created successfully."


def mikrotik_list_hotspot_active() -> str:
    """List active hotspot sessions. READ-ONLY - safe."""
    app_logger.info("Listing active hotspot sessions")
    
    cmd = "/ip hotspot active print detail"
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return "No active hotspot sessions."
    
    return f"ACTIVE HOTSPOT SESSIONS:\n\n{result}"


def mikrotik_list_hotspot_profiles() -> str:
    """List hotspot profiles. READ-ONLY - safe."""
    app_logger.info("Listing hotspot profiles")
    
    cmd = "/ip hotspot profile print detail"
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return "No hotspot profiles found."
    
    return f"HOTSPOT PROFILES:\n\n{result}"


def mikrotik_create_hotspot_profile(
    name: str,
    rate_limit: Optional[str] = None,
    session_timeout: Optional[str] = None,
    idle_timeout: Optional[str] = None,
    shared_users: int = 1,
    comment: Optional[str] = None
) -> str:
    """Create hotspot profile with bandwidth/time limits."""
    app_logger.info(f"Creating hotspot profile: {name}")
    
    cmd = f'/ip hotspot profile add name={name} shared-users={shared_users}'
    
    if rate_limit:
        cmd += f' rate-limit={rate_limit}'
    if session_timeout:
        cmd += f' session-timeout={session_timeout}'
    if idle_timeout:
        cmd += f' idle-timeout={idle_timeout}'
    if comment:
        cmd += f' comment="{comment}"'
    
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to create hotspot profile: {result}"
    
    return f"Hotspot profile '{name}' created successfully."


def mikrotik_list_walled_garden() -> str:
    """List walled garden entries (sites accessible without login). READ-ONLY - safe."""
    app_logger.info("Listing walled garden")
    
    cmd = "/ip hotspot walled-garden print detail"
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return "No walled garden entries found."
    
    return f"WALLED GARDEN:\n\n{result}"


def mikrotik_add_walled_garden(
    dst_host: str,
    comment: Optional[str] = None
) -> str:
    """Add site to walled garden (accessible without hotspot login)."""
    app_logger.info(f"Adding walled garden entry: {dst_host}")
    
    cmd = f'/ip hotspot walled-garden add dst-host={dst_host}'
    
    if comment:
        cmd += f' comment="{comment}"'
    
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to add walled garden entry: {result}"
    
    return f"Walled garden entry for '{dst_host}' added successfully."

