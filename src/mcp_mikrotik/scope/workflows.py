"""
High-level workflow helpers for common MikroTik operations.
These functions combine multiple MCP tools to accomplish complex tasks in one call.
"""
from typing import Optional, Dict
from ..logger import app_logger
from .wireguard import (
    mikrotik_create_wireguard_interface,
    mikrotik_add_wireguard_peer,
    mikrotik_list_wireguard_peers
)
from .ip_address import mikrotik_add_ip_address
from .diagnostics import mikrotik_ping


def mikrotik_setup_vpn_client(
    vpn_name: str,
    local_vpn_ip: str,
    remote_vpn_ip: str,
    remote_endpoint: str,
    remote_endpoint_port: int,
    remote_public_key: str,
    local_private_key: str,
    preshared_key: Optional[str] = None,
    persistent_keepalive: str = "25s",
    mtu: int = 1420
) -> str:
    """
    Complete VPN client setup in one command.
    Creates interface, assigns IP, adds peer, and tests connectivity.
    
    Args:
        vpn_name: Name for the WireGuard interface (e.g., 'wireguard-aws')
        local_vpn_ip: This router's VPN IP with CIDR (e.g., '10.13.13.2/24')
        remote_vpn_ip: Remote server's VPN IP (e.g., '10.13.13.1')
        remote_endpoint: Remote server's public IP or hostname
        remote_endpoint_port: Remote server's WireGuard port
        remote_public_key: Remote server's public key
        local_private_key: This router's private key
        preshared_key: Optional preshared key for extra security
        persistent_keepalive: Keepalive interval (default: '25s')
        mtu: MTU size (default: 1420)
    
    Returns:
        Status report of the complete setup
    """
    app_logger.info(f"Setting up complete VPN client: {vpn_name}")
    
    results = []
    
    # Step 1: Create interface
    app_logger.info("Step 1: Creating WireGuard interface...")
    result = mikrotik_create_wireguard_interface(
        name=vpn_name,
        listen_port=51820,
        private_key=local_private_key,
        mtu=mtu,
        comment=f"VPN to {remote_endpoint}"
    )
    results.append(f"✅ Interface: {result}")
    
    # Step 2: Add IP address
    app_logger.info("Step 2: Adding VPN IP address...")
    result = mikrotik_add_ip_address(
        address=local_vpn_ip,
        interface=vpn_name,
        comment=f"{vpn_name} VPN IP"
    )
    results.append(f"✅ IP Address: {result}")
    
    # Step 3: Add peer
    app_logger.info("Step 3: Adding VPN peer...")
    result = mikrotik_add_wireguard_peer(
        interface=vpn_name,
        public_key=remote_public_key,
        endpoint_address=remote_endpoint,
        endpoint_port=remote_endpoint_port,
        allowed_address=f"{remote_vpn_ip}/32",
        preshared_key=preshared_key,
        persistent_keepalive=persistent_keepalive,
        comment=f"VPN Server at {remote_endpoint}"
    )
    results.append(f"✅ Peer: {result}")
    
    # Step 4: Verify peer configuration
    app_logger.info("Step 4: Verifying peer configuration...")
    result = mikrotik_list_wireguard_peers(interface=vpn_name)
    results.append(f"✅ Peer Status:\n{result}")
    
    # Step 5: Test connectivity
    app_logger.info("Step 5: Testing connectivity...")
    import time
    time.sleep(3)  # Give the connection a moment to establish
    
    result = mikrotik_ping(address=remote_vpn_ip, count=4)
    results.append(f"✅ Connectivity Test:\n{result}")
    
    # Generate summary
    summary = f"""
VPN CLIENT SETUP COMPLETE: {vpn_name}
{'='*60}

Configuration Summary:
- Interface: {vpn_name}
- Local VPN IP: {local_vpn_ip}
- Remote VPN IP: {remote_vpn_ip}
- Remote Endpoint: {remote_endpoint}:{remote_endpoint_port}
- MTU: {mtu}
- Preshared Key: {'Yes' if preshared_key else 'No'}
- Persistent Keepalive: {persistent_keepalive}

Setup Results:
{'='*60}
{chr(10).join(results)}

Next Steps:
- Check peer status: mikrotik_wireguard(action="list_wireguard_peers", interface="{vpn_name}")
- Add firewall rules if needed
- Configure routing as required
"""
    
    return summary


def mikrotik_get_vpn_status(interface: str) -> str:
    """
    Get comprehensive VPN status including interface, peer, and connectivity.
    
    Args:
        interface: WireGuard interface name
    
    Returns:
        Complete VPN status report
    """
    app_logger.info(f"Getting VPN status for: {interface}")
    
    from .wireguard import mikrotik_get_wireguard_interface
    from .ip_address import mikrotik_list_ip_addresses
    
    results = []
    
    # Get interface status
    result = mikrotik_get_wireguard_interface(interface)
    results.append(f"Interface Status:\n{result}")
    
    # Get IP addresses
    result = mikrotik_list_ip_addresses(interface=interface)
    results.append(f"\nIP Addresses:\n{result}")
    
    # Get peer status
    result = mikrotik_list_wireguard_peers(interface=interface)
    results.append(f"\nPeer Status:\n{result}")
    
    return "\n".join(results)

