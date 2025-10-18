from typing import Optional

from ..connector import execute_mikrotik_command
from ..api_fallback import api_fallback_execute
from ..logger import app_logger


# ============================================================================
# IPv6 ADDRESS MANAGEMENT
# ============================================================================

def mikrotik_list_ipv6_addresses(interface: Optional[str] = None) -> str:
    """
    Lists IPv6 addresses on MikroTik device.
    
    Args:
        interface: Filter by interface name
    
    Returns:
        List of IPv6 addresses
    """
    app_logger.info(f"Listing IPv6 addresses for interface: {interface}")
    
    cmd = "/ipv6 address print"
    
    if interface:
        cmd += f' where interface="{interface}"'
    
    result = execute_mikrotik_command(cmd)
    
    return f"IPv6 ADDRESSES:\n\n{result}"


def mikrotik_add_ipv6_address(
        address: str,
        interface: str,
        advertise: bool = True,
        eui_64: bool = False,
        no_dad: bool = False,
        comment: Optional[str] = None
) -> str:
    """
    Adds an IPv6 address to an interface.
    
    Args:
        address: IPv6 address with prefix (e.g., "2001:db8::1/64")
        interface: Interface name
        advertise: Advertise this prefix
        eui_64: Generate address using EUI-64
        no_dad: Disable Duplicate Address Detection
        comment: Optional comment
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Adding IPv6 address: {address} to {interface}")
    
    cmd = f'/ipv6 address add address="{address}" interface={interface}'
    cmd += f' advertise={"yes" if advertise else "no"}'
    cmd += f' eui-64={"yes" if eui_64 else "no"}'
    cmd += f' no-dad={"yes" if no_dad else "no"}'
    
    if comment:
        cmd += f' comment="{comment}"'
    
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to add IPv6 address: {result}"
    
    return f"IPv6 address '{address}' added to interface '{interface}' successfully."


def mikrotik_remove_ipv6_address(address: str) -> str:
    """
    Removes an IPv6 address.
    
    Args:
        address: IPv6 address to remove (can be partial match)
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Removing IPv6 address: {address}")
    
    cmd = f'/ipv6 address remove [find address~"{address}"]'
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to remove IPv6 address: {result}"
    
    return f"IPv6 address '{address}' removed successfully."


def mikrotik_get_ipv6_address(address: str) -> str:
    """
    Gets detailed information about an IPv6 address.
    
    Args:
        address: IPv6 address to query
    
    Returns:
        Address details
    """
    app_logger.info(f"Getting IPv6 address details: {address}")
    
    cmd = f'/ipv6 address print detail where address~"{address}"'
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return f"IPv6 address '{address}' not found."
    
    return f"IPv6 ADDRESS DETAILS:\n\n{result}"


# ============================================================================
# IPv6 ROUTE MANAGEMENT
# ============================================================================

def mikrotik_list_ipv6_routes(dst_address: Optional[str] = None) -> str:
    """
    Lists IPv6 routes.
    
    Args:
        dst_address: Filter by destination address
    
    Returns:
        List of IPv6 routes
    """
    app_logger.info("Listing IPv6 routes")
    
    cmd = "/ipv6 route print"
    
    if dst_address:
        cmd += f' where dst-address~"{dst_address}"'
    
    result = execute_mikrotik_command(cmd)
    
    return f"IPv6 ROUTES:\n\n{result}"


def mikrotik_add_ipv6_route(
        dst_address: str,
        gateway: Optional[str] = None,
        interface: Optional[str] = None,
        distance: int = 1,
        comment: Optional[str] = None
) -> str:
    """
    Adds an IPv6 route.
    
    Args:
        dst_address: Destination address/prefix
        gateway: Gateway IPv6 address
        interface: Interface name (for link-local gateways)
        distance: Administrative distance
        comment: Optional comment
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Adding IPv6 route to {dst_address}")
    
    cmd = f'/ipv6 route add dst-address="{dst_address}"'
    
    if gateway:
        cmd += f' gateway="{gateway}"'
    if interface:
        cmd += f'%{interface}'
    
    cmd += f" distance={distance}"
    
    if comment:
        cmd += f' comment="{comment}"'
    
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to add IPv6 route: {result}"
    
    return f"IPv6 route to '{dst_address}' added successfully."


def mikrotik_remove_ipv6_route(dst_address: str) -> str:
    """
    Removes an IPv6 route.
    
    Args:
        dst_address: Destination address to remove
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Removing IPv6 route: {dst_address}")
    
    cmd = f'/ipv6 route remove [find dst-address~"{dst_address}"]'
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to remove IPv6 route: {result}"
    
    return f"IPv6 route '{dst_address}' removed successfully."


# ============================================================================
# IPv6 NEIGHBOR DISCOVERY
# ============================================================================

def mikrotik_list_ipv6_neighbors() -> str:
    """
    Lists IPv6 neighbor discovery table.
    
    Returns:
        List of IPv6 neighbors
    """
    app_logger.info("Listing IPv6 neighbors")
    
    cmd = "/ipv6 neighbor print"
    result = execute_mikrotik_command(cmd)
    
    return f"IPv6 NEIGHBORS:\n\n{result}"


def mikrotik_get_ipv6_nd_settings(interface: str) -> str:
    """
    Gets IPv6 Neighbor Discovery settings for an interface.
    
    Args:
        interface: Interface name
    
    Returns:
        ND settings
    """
    app_logger.info(f"Getting IPv6 ND settings for {interface}")
    
    cmd = f'/ipv6 nd print detail where interface="{interface}"'
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return f"No IPv6 ND settings found for interface '{interface}'."
    
    return f"IPv6 ND SETTINGS:\n\n{result}"


def mikrotik_set_ipv6_nd(
        interface: str,
        ra_interval: Optional[str] = None,
        ra_lifetime: Optional[str] = None,
        hop_limit: Optional[int] = None,
        advertise_mac_address: Optional[bool] = None,
        advertise_dns: Optional[bool] = None
) -> str:
    """
    Configures IPv6 Neighbor Discovery on an interface.
    
    Args:
        interface: Interface name
        ra_interval: Router Advertisement interval
        ra_lifetime: Router lifetime
        hop_limit: Hop limit
        advertise_mac_address: Advertise MAC address
        advertise_dns: Advertise DNS servers
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Configuring IPv6 ND on {interface}")
    
    # Check if ND entry exists
    check_cmd = f'/ipv6 nd print count-only where interface="{interface}"'
    count = execute_mikrotik_command(check_cmd)
    
    if count.strip() == "0":
        # Add new entry
        cmd = f'/ipv6 nd add interface={interface}'
    else:
        # Update existing entry
        cmd = f'/ipv6 nd set [find interface="{interface}"]'
    
    if ra_interval:
        cmd += f" ra-interval={ra_interval}"
    if ra_lifetime:
        cmd += f" ra-lifetime={ra_lifetime}"
    if hop_limit is not None:
        cmd += f" hop-limit={hop_limit}"
    if advertise_mac_address is not None:
        cmd += f' advertise-mac-address={"yes" if advertise_mac_address else "no"}'
    if advertise_dns is not None:
        cmd += f' advertise-dns={"yes" if advertise_dns else "no"}'
    
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to configure IPv6 ND: {result}"
    
    return f"IPv6 ND configured on interface '{interface}' successfully."


# ============================================================================
# IPv6 POOL MANAGEMENT
# ============================================================================

def mikrotik_list_ipv6_pools() -> str:
    """
    Lists IPv6 address pools.
    
    Returns:
        List of IPv6 pools
    """
    app_logger.info("Listing IPv6 pools")
    
    cmd = "/ipv6 pool print"
    result = execute_mikrotik_command(cmd)
    
    return f"IPv6 POOLS:\n\n{result}"


def mikrotik_create_ipv6_pool(
        name: str,
        prefix: str,
        prefix_length: int = 64,
        comment: Optional[str] = None
) -> str:
    """
    Creates an IPv6 address pool.
    
    Args:
        name: Pool name
        prefix: IPv6 prefix
        prefix_length: Prefix length to delegate
        comment: Optional comment
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Creating IPv6 pool: {name}")
    
    cmd = f'/ipv6 pool add name={name} prefix="{prefix}" prefix-length={prefix_length}'
    
    if comment:
        cmd += f' comment="{comment}"'
    
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to create IPv6 pool: {result}"
    
    return f"IPv6 pool '{name}' created successfully."


def mikrotik_remove_ipv6_pool(name: str) -> str:
    """
    Removes an IPv6 pool.
    
    Args:
        name: Pool name
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Removing IPv6 pool: {name}")
    
    cmd = f'/ipv6 pool remove [find name="{name}"]'
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to remove IPv6 pool: {result}"
    
    return f"IPv6 pool '{name}' removed successfully."


# ============================================================================
# IPv6 SETTINGS
# ============================================================================

def mikrotik_get_ipv6_settings() -> str:
    """
    Gets global IPv6 settings.
    
    Returns:
        IPv6 settings
    """
    app_logger.info("Getting IPv6 settings")
    
    cmd = "/ipv6 settings print"
    result = execute_mikrotik_command(cmd)
    
    return f"IPv6 SETTINGS:\n\n{result}"


def mikrotik_set_ipv6_forward(enabled: bool) -> str:
    """
    Enables or disables IPv6 forwarding.
    
    Args:
        enabled: Enable IPv6 forwarding
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Setting IPv6 forwarding: {enabled}")
    
    cmd = f'/ipv6 settings set forward={"yes" if enabled else "no"}'
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to set IPv6 forwarding: {result}"
    
    return f"IPv6 forwarding {'enabled' if enabled else 'disabled'} successfully."

