"""
OpenVPN management functions for MikroTik RouterOS.
Supports OpenVPN client and server configuration.
"""
from typing import Optional
from ..connector import execute_mikrotik_command
from ..logger import app_logger


def mikrotik_list_openvpn_interfaces(
    name_filter: Optional[str] = None,
    disabled_only: bool = False
) -> str:
    """
    List all OpenVPN interfaces (both client and server).
    This is a READ-ONLY operation - safe to run on live router.
    """
    app_logger.info(f"Listing OpenVPN interfaces: name={name_filter}")
    
    cmd = "/interface ovpn-client print detail"
    
    filters = []
    if name_filter:
        filters.append(f'name~"{name_filter}"')
    if disabled_only:
        filters.append("disabled=yes")
    
    if filters:
        cmd += " where " + " and ".join(filters)
    
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return "No OpenVPN client interfaces found."
    
    return f"OPENVPN CLIENT INTERFACES:\n\n{result}"


def mikrotik_list_openvpn_servers(
    name_filter: Optional[str] = None
) -> str:
    """
    List OpenVPN servers configured on the router.
    This is a READ-ONLY operation - safe to run on live router.
    """
    app_logger.info(f"Listing OpenVPN servers: name={name_filter}")
    
    cmd = "/interface ovpn-server print detail"
    
    if name_filter:
        cmd += f' where name~"{name_filter}"'
    
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return "No OpenVPN server interfaces found."
    
    return f"OPENVPN SERVER INTERFACES:\n\n{result}"


def mikrotik_get_openvpn_server_status() -> str:
    """
    Get OpenVPN server status and configuration.
    This is a READ-ONLY operation - safe to run on live router.
    """
    app_logger.info("Getting OpenVPN server status")
    
    cmd = "/ppp profile print detail where name~\"ovpn\""
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return "OpenVPN server not configured or no profiles found."
    
    return f"OPENVPN SERVER STATUS:\n\n{result}"


def mikrotik_create_openvpn_client(
    name: str,
    connect_to: str,
    port: int = 1194,
    user: Optional[str] = None,
    password: Optional[str] = None,
    certificate: Optional[str] = None,
    auth: str = "sha1",
    cipher: str = "aes128",
    mode: str = "ip",
    comment: Optional[str] = None
) -> str:
    """
    Create an OpenVPN client interface.
    
    ⚠️ This creates a new interface - test on non-critical setup first!
    
    Args:
        name: Interface name (e.g., 'ovpn-client-aws')
        connect_to: Server IP or hostname
        port: OpenVPN port (default: 1194)
        user: Username for authentication
        password: Password for authentication
        certificate: Certificate name (for cert-based auth)
        auth: Authentication method (sha1, sha256, sha512)
        cipher: Encryption cipher (aes128, aes192, aes256, blowfish128)
        mode: Connection mode ('ip' or 'ethernet')
        comment: Optional comment
    """
    app_logger.info(f"Creating OpenVPN client: {name}")
    
    # Build command - RouterOS OVPN client syntax (simplified)
    # Start with minimal required parameters
    cmd = f'/interface ovpn-client add name={name} connect-to={connect_to}'
    
    # Add optional parameters
    if port != 1194:
        cmd += f' port={port}'
    if mode != "ip":
        cmd += f' mode={mode}'
    if auth != "sha1":
        cmd += f' auth={auth}'
    if cipher != "aes128":
        cmd += f' cipher={cipher}'
    if user:
        cmd += f' user={user}'
    if password:
        cmd += f' password={password}'
    if certificate:
        cmd += f' certificate={certificate}'
    if comment:
        cmd += f' comment="{comment}"'
    
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to create OpenVPN client: {result}"
    
    return f"OpenVPN client '{name}' created successfully.\nUse list_openvpn_interfaces to verify."


def mikrotik_remove_openvpn_interface(name: str) -> str:
    """
    Remove an OpenVPN interface.
    
    ⚠️ This removes configuration - ensure it's not critical!
    """
    app_logger.info(f"Removing OpenVPN interface: {name}")
    
    cmd = f'/interface ovpn-client remove [find name="{name}"]'
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to remove OpenVPN interface: {result}"
    
    return f"OpenVPN interface '{name}' removed successfully."


def mikrotik_update_openvpn_client(
    name: str,
    connect_to: Optional[str] = None,
    port: Optional[int] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    disabled: Optional[bool] = None,
    comment: Optional[str] = None
) -> str:
    """
    Update OpenVPN client settings.
    
    ⚠️ Changes may disconnect active VPN - use with caution!
    """
    app_logger.info(f"Updating OpenVPN client: {name}")
    
    cmd_parts = [f'/interface ovpn-client set [find name="{name}"]']
    
    if connect_to:
        cmd_parts.append(f'connect-to={connect_to}')
    if port is not None:
        cmd_parts.append(f'port={port}')
    if user:
        cmd_parts.append(f'user="{user}"')
    if password:
        cmd_parts.append(f'password="{password}"')
    if disabled is not None:
        cmd_parts.append(f'disabled={"yes" if disabled else "no"}')
    if comment:
        cmd_parts.append(f'comment="{comment}"')
    
    if len(cmd_parts) == 1:
        return "No updates specified."
    
    cmd = " ".join(cmd_parts)
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to update OpenVPN client: {result}"
    
    return f"OpenVPN client '{name}' updated successfully."


def mikrotik_get_openvpn_status(name: str) -> str:
    """
    Get detailed status of an OpenVPN interface.
    This is a READ-ONLY operation - safe to run on live router.
    """
    app_logger.info(f"Getting OpenVPN status for: {name}")
    
    cmd = f'/interface ovpn-client print detail where name="{name}"'
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return f"OpenVPN interface '{name}' not found."
    
    return f"OPENVPN STATUS ({name}):\n\n{result}"


def mikrotik_enable_openvpn_client(name: str) -> str:
    """
    Enable an OpenVPN client interface.
    
    ⚠️ This will attempt to connect - ensure server is ready!
    """
    app_logger.info(f"Enabling OpenVPN client: {name}")
    
    cmd = f'/interface ovpn-client enable [find name="{name}"]'
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to enable OpenVPN client: {result}"
    
    return f"OpenVPN client '{name}' enabled successfully."


def mikrotik_disable_openvpn_client(name: str) -> str:
    """
    Disable an OpenVPN client interface.
    
    This is safe - just disables the interface without deleting it.
    """
    app_logger.info(f"Disabling OpenVPN client: {name}")
    
    cmd = f'/interface ovpn-client disable [find name="{name}"]'
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to disable OpenVPN client: {result}"
    
    return f"OpenVPN client '{name}' disabled successfully."

