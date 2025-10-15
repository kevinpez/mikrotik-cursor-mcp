"""
WireGuard VPN management functions for MikroTik RouterOS.
Supports interface creation, peer management, and configuration.
"""
from typing import Optional
from ..connector import execute_mikrotik_command
from ..logger import app_logger
from .validators import validate_wireguard_key, validate_port, validate_interface_name, validate_ip_address


def mikrotik_list_wireguard_interfaces(
    name_filter: Optional[str] = None,
    disabled_only: bool = False
) -> str:
    """List all WireGuard interfaces"""
    app_logger.info(f"Listing WireGuard interfaces: name={name_filter}")
    
    cmd = "/interface wireguard print detail"
    
    filters = []
    if name_filter:
        filters.append(f'name~"{name_filter}"')
    if disabled_only:
        filters.append("disabled=yes")
    
    if filters:
        cmd += " where " + " and ".join(filters)
    
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return "No WireGuard interfaces found."
    
    return f"WIREGUARD INTERFACES:\n\n{result}"


def mikrotik_create_wireguard_interface(
    name: str,
    listen_port: int = 51820,
    private_key: Optional[str] = None,
    mtu: int = 1420,
    comment: Optional[str] = None
) -> str:
    """Create a new WireGuard interface"""
    app_logger.info(f"Creating WireGuard interface: {name}")
    
    # Validate inputs
    is_valid, error_msg = validate_interface_name(name)
    if not is_valid:
        return f"Validation Error: {error_msg}"
    
    is_valid, error_msg = validate_port(listen_port)
    if not is_valid:
        return f"Validation Error: {error_msg}"
    
    if private_key:
        is_valid, error_msg = validate_wireguard_key(private_key)
        if not is_valid:
            return f"Validation Error (private_key): {error_msg}"
    
    if not 1280 <= mtu <= 9000:
        return f"Validation Error: MTU {mtu} out of range. Use 1280-9000 (recommended: 1420)"
    
    # Build the command
    cmd_parts = [
        f'/interface wireguard add',
        f'name="{name}"',
        f'listen-port={listen_port}',
        f'mtu={mtu}'
    ]
    
    if private_key:
        cmd_parts.append(f'private-key="{private_key}"')
    
    if comment:
        cmd_parts.append(f'comment="{comment}"')
    
    cmd = " ".join(cmd_parts)
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to create WireGuard interface: {result}"
    
    return f"WireGuard interface '{name}' created successfully.\nNote: If no private-key was provided, RouterOS generated one automatically."


def mikrotik_remove_wireguard_interface(name: str) -> str:
    """Remove a WireGuard interface"""
    app_logger.info(f"Removing WireGuard interface: {name}")
    
    cmd = f'/interface wireguard remove "{name}"'
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to remove WireGuard interface: {result}"
    
    return f"WireGuard interface '{name}' removed successfully."


def mikrotik_update_wireguard_interface(
    name: str,
    listen_port: Optional[int] = None,
    mtu: Optional[int] = None,
    private_key: Optional[str] = None,
    disabled: Optional[bool] = None,
    comment: Optional[str] = None
) -> str:
    """Update WireGuard interface settings"""
    app_logger.info(f"Updating WireGuard interface: {name}")
    
    cmd_parts = [f'/interface wireguard set [find name="{name}"]']
    
    if listen_port is not None:
        cmd_parts.append(f'listen-port={listen_port}')
    if mtu is not None:
        cmd_parts.append(f'mtu={mtu}')
    if private_key is not None:
        cmd_parts.append(f'private-key="{private_key}"')
    if disabled is not None:
        cmd_parts.append(f'disabled={"yes" if disabled else "no"}')
    if comment is not None:
        cmd_parts.append(f'comment="{comment}"')
    
    if len(cmd_parts) == 1:
        return "No updates specified."
    
    cmd = " ".join(cmd_parts)
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to update WireGuard interface: {result}"
    
    return f"WireGuard interface '{name}' updated successfully."


def mikrotik_get_wireguard_interface(name: str) -> str:
    """Get detailed information about a specific WireGuard interface"""
    app_logger.info(f"Getting WireGuard interface info: {name}")
    
    cmd = f'/interface wireguard print detail where name="{name}"'
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return f"WireGuard interface '{name}' not found."
    
    return f"WIREGUARD INTERFACE ({name}):\n\n{result}"


def mikrotik_list_wireguard_peers(
    interface: Optional[str] = None,
    endpoint_filter: Optional[str] = None
) -> str:
    """List WireGuard peers"""
    app_logger.info(f"Listing WireGuard peers: interface={interface}")
    
    cmd = "/interface wireguard peers print detail"
    
    filters = []
    if interface:
        filters.append(f'interface="{interface}"')
    if endpoint_filter:
        filters.append(f'endpoint-address~"{endpoint_filter}"')
    
    if filters:
        cmd += " where " + " and ".join(filters)
    
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return "No WireGuard peers found."
    
    return f"WIREGUARD PEERS:\n\n{result}"


def mikrotik_add_wireguard_peer(
    interface: str,
    public_key: str,
    endpoint_address: Optional[str] = None,
    endpoint_port: Optional[int] = None,
    allowed_address: Optional[str] = None,
    preshared_key: Optional[str] = None,
    persistent_keepalive: Optional[str] = None,
    comment: Optional[str] = None
) -> str:
    """Add a WireGuard peer to an interface"""
    app_logger.info(f"Adding WireGuard peer to interface: {interface}")
    
    # Validate public key
    is_valid, error_msg = validate_wireguard_key(public_key)
    if not is_valid:
        return f"Validation Error (public_key): {error_msg}"
    
    # Validate preshared key if provided
    if preshared_key:
        is_valid, error_msg = validate_wireguard_key(preshared_key)
        if not is_valid:
            return f"Validation Error (preshared_key): {error_msg}"
    
    # Validate endpoint port if provided
    if endpoint_port is not None:
        is_valid, error_msg = validate_port(endpoint_port)
        if not is_valid:
            return f"Validation Error (endpoint_port): {error_msg}"
    
    # Validate allowed address if provided
    if allowed_address:
        is_valid, error_msg = validate_ip_address(allowed_address)
        if not is_valid:
            return f"Validation Error (allowed_address): {error_msg}"
    
    cmd_parts = [
        '/interface wireguard peers add',
        f'interface="{interface}"',
        f'public-key="{public_key}"'
    ]
    
    if endpoint_address:
        cmd_parts.append(f'endpoint-address={endpoint_address}')
    if endpoint_port is not None:
        cmd_parts.append(f'endpoint-port={endpoint_port}')
    if allowed_address:
        cmd_parts.append(f'allowed-address={allowed_address}')
    if preshared_key:
        cmd_parts.append(f'preshared-key="{preshared_key}"')
    if persistent_keepalive:
        cmd_parts.append(f'persistent-keepalive={persistent_keepalive}')
    if comment:
        cmd_parts.append(f'comment="{comment}"')
    
    cmd = " ".join(cmd_parts)
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to add WireGuard peer: {result}"
    
    return f"WireGuard peer added successfully to interface '{interface}'."


def mikrotik_remove_wireguard_peer(
    interface: str,
    public_key: Optional[str] = None,
    peer_id: Optional[str] = None
) -> str:
    """Remove a WireGuard peer"""
    app_logger.info(f"Removing WireGuard peer from interface: {interface}")
    
    if peer_id:
        # Remove by ID
        cmd = f'/interface wireguard peers remove {peer_id}'
    elif public_key:
        # Remove by public key
        cmd = f'/interface wireguard peers remove [find interface="{interface}" public-key="{public_key}"]'
    else:
        return "Either peer_id or public_key must be provided."
    
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to remove WireGuard peer: {result}"
    
    return f"WireGuard peer removed successfully from interface '{interface}'."


def mikrotik_update_wireguard_peer(
    interface: str,
    public_key: str,
    endpoint_address: Optional[str] = None,
    endpoint_port: Optional[int] = None,
    allowed_address: Optional[str] = None,
    preshared_key: Optional[str] = None,
    persistent_keepalive: Optional[str] = None,
    disabled: Optional[bool] = None,
    comment: Optional[str] = None
) -> str:
    """Update WireGuard peer settings"""
    app_logger.info(f"Updating WireGuard peer on interface: {interface}")
    
    cmd_parts = [f'/interface wireguard peers set [find interface="{interface}" public-key="{public_key}"]']
    
    if endpoint_address is not None:
        cmd_parts.append(f'endpoint-address={endpoint_address}')
    if endpoint_port is not None:
        cmd_parts.append(f'endpoint-port={endpoint_port}')
    if allowed_address is not None:
        cmd_parts.append(f'allowed-address={allowed_address}')
    if preshared_key is not None:
        cmd_parts.append(f'preshared-key="{preshared_key}"')
    if persistent_keepalive is not None:
        cmd_parts.append(f'persistent-keepalive={persistent_keepalive}')
    if disabled is not None:
        cmd_parts.append(f'disabled={"yes" if disabled else "no"}')
    if comment is not None:
        cmd_parts.append(f'comment="{comment}"')
    
    if len(cmd_parts) == 1:
        return "No updates specified."
    
    cmd = " ".join(cmd_parts)
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to update WireGuard peer: {result}"
    
    return f"WireGuard peer updated successfully on interface '{interface}'."


def mikrotik_enable_wireguard_interface(name: str) -> str:
    """Enable a WireGuard interface"""
    app_logger.info(f"Enabling WireGuard interface: {name}")
    
    cmd = f'/interface wireguard enable "{name}"'
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to enable WireGuard interface: {result}"
    
    return f"WireGuard interface '{name}' enabled successfully."


def mikrotik_disable_wireguard_interface(name: str) -> str:
    """Disable a WireGuard interface"""
    app_logger.info(f"Disabling WireGuard interface: {name}")
    
    cmd = f'/interface wireguard disable "{name}"'
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to disable WireGuard interface: {result}"
    
    return f"WireGuard interface '{name}' disabled successfully."

