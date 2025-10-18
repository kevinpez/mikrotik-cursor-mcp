from typing import Optional

from ..connector import execute_mikrotik_command
from ..api_fallback import api_fallback_execute
from ..logger import app_logger


# ============================================================================
# DHCPv6 SERVER
# ============================================================================

def mikrotik_list_dhcpv6_servers() -> str:
    """
    Lists all DHCPv6 servers.
    
    Returns:
        List of DHCPv6 servers
    """
    app_logger.info("Listing DHCPv6 servers")
    
    cmd = "/ipv6 dhcp-server print"
    result = execute_mikrotik_command(cmd)
    
    return f"DHCPv6 SERVERS:\n\n{result}"


def mikrotik_create_dhcpv6_server(
        name: str,
        interface: str,
        address_pool: str,
        lease_time: str = "1d",
        disabled: bool = False
) -> str:
    """
    Creates a DHCPv6 server.
    
    Args:
        name: Server name
        interface: Interface to run server on
        address_pool: IPv6 pool name
        lease_time: Lease time (e.g., "1d", "12h")
        disabled: Disable the server
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Creating DHCPv6 server: {name}")
    
    cmd = f"/ipv6 dhcp-server add name={name} interface={interface} address-pool={address_pool} lease-time={lease_time}"
    
    if disabled:
        cmd += " disabled=yes"
    
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to create DHCPv6 server: {result}"
    
    return f"DHCPv6 server '{name}' created successfully."


def mikrotik_remove_dhcpv6_server(name: str) -> str:
    """
    Removes a DHCPv6 server.
    
    Args:
        name: Server name
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Removing DHCPv6 server: {name}")
    
    cmd = f'/ipv6 dhcp-server remove [find name="{name}"]'
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to remove DHCPv6 server: {result}"
    
    return f"DHCPv6 server '{name}' removed successfully."


def mikrotik_get_dhcpv6_server(name: str) -> str:
    """
    Gets detailed information about a DHCPv6 server.
    
    Args:
        name: Server name
    
    Returns:
        Server details
    """
    app_logger.info(f"Getting DHCPv6 server: {name}")
    
    cmd = f'/ipv6 dhcp-server print detail where name="{name}"'
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return f"DHCPv6 server '{name}' not found."
    
    return f"DHCPv6 SERVER DETAILS:\n\n{result}"


# ============================================================================
# DHCPv6 LEASES
# ============================================================================

def mikrotik_list_dhcpv6_leases() -> str:
    """
    Lists all DHCPv6 leases.
    
    Returns:
        List of DHCPv6 leases
    """
    app_logger.info("Listing DHCPv6 leases")
    
    cmd = "/ipv6 dhcp-server binding print"
    result = execute_mikrotik_command(cmd)
    
    return f"DHCPv6 LEASES:\n\n{result}"


def mikrotik_create_dhcpv6_static_lease(
        address: str,
        duid: str,
        server: Optional[str] = None,
        comment: Optional[str] = None
) -> str:
    """
    Creates a DHCPv6 static lease.
    
    Args:
        address: IPv6 address to assign
        duid: Client DUID (DHCP Unique Identifier)
        server: DHCPv6 server name
        comment: Optional comment
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Creating DHCPv6 static lease for DUID: {duid}")
    
    cmd = f'/ipv6 dhcp-server binding add address="{address}" duid="{duid}"'
    
    if server:
        cmd += f" server={server}"
    if comment:
        cmd += f' comment="{comment}"'
    
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to create DHCPv6 static lease: {result}"
    
    return f"DHCPv6 static lease for '{duid}' created successfully."


def mikrotik_remove_dhcpv6_lease(lease_id: str) -> str:
    """
    Removes a DHCPv6 lease.
    
    Args:
        lease_id: Lease ID
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Removing DHCPv6 lease: {lease_id}")
    
    cmd = f"/ipv6 dhcp-server binding remove {lease_id}"
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to remove DHCPv6 lease: {result}"
    
    return f"DHCPv6 lease '{lease_id}' removed successfully."


# ============================================================================
# DHCPv6 CLIENT
# ============================================================================

def mikrotik_list_dhcpv6_clients() -> str:
    """
    Lists all DHCPv6 clients.
    
    Returns:
        List of DHCPv6 clients
    """
    app_logger.info("Listing DHCPv6 clients")
    
    cmd = "/ipv6 dhcp-client print"
    result = execute_mikrotik_command(cmd)
    
    return f"DHCPv6 CLIENTS:\n\n{result}"


def mikrotik_create_dhcpv6_client(
        interface: str,
        pool_name: Optional[str] = None,
        pool_prefix_length: int = 64,
        add_default_route: bool = True,
        request: str = "address",
        disabled: bool = False
) -> str:
    """
    Creates a DHCPv6 client.
    
    Args:
        interface: Interface to run client on
        pool_name: Pool name for prefix delegation
        pool_prefix_length: Prefix length to request
        add_default_route: Add default route
        request: What to request (address, prefix, address,prefix)
        disabled: Disable the client
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Creating DHCPv6 client on interface: {interface}")
    
    cmd = f"/ipv6 dhcp-client add interface={interface} request={request}"
    cmd += f' add-default-route={"yes" if add_default_route else "no"}'
    
    if pool_name:
        cmd += f" pool-name={pool_name} pool-prefix-length={pool_prefix_length}"
    
    if disabled:
        cmd += " disabled=yes"
    
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to create DHCPv6 client: {result}"
    
    return f"DHCPv6 client on interface '{interface}' created successfully."


def mikrotik_remove_dhcpv6_client(interface: str) -> str:
    """
    Removes a DHCPv6 client.
    
    Args:
        interface: Interface name
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Removing DHCPv6 client from interface: {interface}")
    
    cmd = f'/ipv6 dhcp-client remove [find interface="{interface}"]'
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to remove DHCPv6 client: {result}"
    
    return f"DHCPv6 client on interface '{interface}' removed successfully."


def mikrotik_get_dhcpv6_client(interface: str) -> str:
    """
    Gets detailed information about a DHCPv6 client.
    
    Args:
        interface: Interface name
    
    Returns:
        Client details
    """
    app_logger.info(f"Getting DHCPv6 client on interface: {interface}")
    
    cmd = f'/ipv6 dhcp-client print detail where interface="{interface}"'
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return f"DHCPv6 client on interface '{interface}' not found."
    
    return f"DHCPv6 CLIENT DETAILS:\n\n{result}"


# ============================================================================
# DHCPv6 SERVER OPTIONS
# ============================================================================

def mikrotik_list_dhcpv6_options() -> str:
    """
    Lists DHCPv6 server options.
    
    Returns:
        List of DHCPv6 options
    """
    app_logger.info("Listing DHCPv6 options")
    
    cmd = "/ipv6 dhcp-server option print"
    result = execute_mikrotik_command(cmd)
    
    return f"DHCPv6 OPTIONS:\n\n{result}"


def mikrotik_create_dhcpv6_option(
        name: str,
        code: int,
        value: str
) -> str:
    """
    Creates a DHCPv6 server option.
    
    Args:
        name: Option name
        code: Option code
        value: Option value (hex format)
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Creating DHCPv6 option: {name}")
    
    cmd = f'/ipv6 dhcp-server option add name={name} code={code} value="{value}"'
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to create DHCPv6 option: {result}"
    
    return f"DHCPv6 option '{name}' created successfully."


def mikrotik_remove_dhcpv6_option(name: str) -> str:
    """
    Removes a DHCPv6 server option.
    
    Args:
        name: Option name
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Removing DHCPv6 option: {name}")
    
    cmd = f'/ipv6 dhcp-server option remove [find name="{name}"]'
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to remove DHCPv6 option: {result}"
    
    return f"DHCPv6 option '{name}' removed successfully."


# ============================================================================
# DHCPv6 RELAY - NEW in v4.8.0
# ============================================================================

def mikrotik_configure_dhcpv6_relay(
    interface: str,
    dhcp_server: str,
    name: Optional[str] = None,
    disabled: bool = False
) -> str:
    """
    Configures DHCPv6 relay agent on an interface.
    
    Args:
        interface: Interface to run relay on
        dhcp_server: IPv6 address of DHCPv6 server
        name: Optional name for the relay configuration
        disabled: Whether to disable the relay after creation
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Configuring DHCPv6 relay on {interface} to server {dhcp_server}")
    
    if not interface or interface.strip() == "":
        return "Error: Interface cannot be empty."
    
    if not dhcp_server or dhcp_server.strip() == "":
        return "Error: DHCPv6 server address cannot be empty."
    
    # Build command
    cmd = f'/ipv6 dhcp-relay add interface="{interface}" dhcp-server={dhcp_server}'
    
    if name:
        cmd += f' name="{name}"'
    
    if disabled:
        cmd += " disabled=yes"
    
    result = execute_mikrotik_command(cmd)
    
    if result.strip() and ("*" in result or result.strip().isdigit()):
        relay_id = result.strip()
        details_cmd = f"/ipv6 dhcp-relay print detail where .id={relay_id}"
        details = execute_mikrotik_command(details_cmd)
        
        if details.strip():
            return f"DHCPv6 relay configured successfully:\n\n{details}"
        else:
            return f"DHCPv6 relay configured with ID: {result}"
    else:
        return f"Failed to configure DHCPv6 relay: {result}" if result else "DHCPv6 relay configured."

def mikrotik_list_dhcpv6_relays(
    interface_filter: Optional[str] = None,
    disabled_only: bool = False
) -> str:
    """
    Lists DHCPv6 relay configurations.
    
    Args:
        interface_filter: Filter by interface name
        disabled_only: Show only disabled relays
    
    Returns:
        List of DHCPv6 relay configurations
    """
    app_logger.info(f"Listing DHCPv6 relays: interface_filter={interface_filter}")
    
    cmd = "/ipv6 dhcp-relay print detail"
    
    filters = []
    if interface_filter:
        filters.append(f'interface~"{interface_filter}"')
    if disabled_only:
        filters.append("disabled=yes")
    
    if filters:
        cmd += " where " + " ".join(filters)
    
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "" or result.strip() == "no such item":
        return "No DHCPv6 relay configurations found."
    
    return f"DHCPv6 RELAYS:\n\n{result}"
