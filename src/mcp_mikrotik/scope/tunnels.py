"""
Tunnel interface management for MikroTik RouterOS (EoIP, GRE, IPIP, VXLAN).
"""
from typing import Optional
from ..connector import execute_mikrotik_command
from ..logger import app_logger


def mikrotik_list_eoip_tunnels(name_filter: Optional[str] = None) -> str:
    """List EoIP tunnel interfaces. READ-ONLY - safe."""
    app_logger.info(f"Listing EoIP tunnels: name={name_filter}")
    
    cmd = "/interface eoip print detail"
    
    if name_filter:
        cmd += f' where name~"{name_filter}"'
    
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return "No EoIP tunnels found."
    
    return f"EOIP TUNNELS:\n\n{result}"


def mikrotik_create_eoip_tunnel(
    name: str,
    remote_address: str,
    tunnel_id: int,
    local_address: Optional[str] = None,
    mtu: int = 1500,
    comment: Optional[str] = None
) -> str:
    """Create EoIP (Ethernet over IP) tunnel."""
    app_logger.info(f"Creating EoIP tunnel: {name}")
    
    cmd = f'/interface eoip add name={name} remote-address={remote_address} tunnel-id={tunnel_id} mtu={mtu}'
    
    if local_address:
        cmd += f' local-address={local_address}'
    if comment:
        cmd += f' comment="{comment}"'
    
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to create EoIP tunnel: {result}"
    
    return f"EoIP tunnel '{name}' created successfully."


def mikrotik_remove_eoip_tunnel(name: str) -> str:
    """Remove EoIP tunnel."""
    app_logger.info(f"Removing EoIP tunnel: {name}")
    
    cmd = f'/interface eoip remove [find name={name}]'
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to remove EoIP tunnel: {result}"
    
    return f"EoIP tunnel '{name}' removed successfully."


def mikrotik_list_gre_tunnels(name_filter: Optional[str] = None) -> str:
    """List GRE tunnel interfaces. READ-ONLY - safe."""
    app_logger.info(f"Listing GRE tunnels: name={name_filter}")
    
    cmd = "/interface gre print detail"
    
    if name_filter:
        cmd += f' where name~"{name_filter}"'
    
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return "No GRE tunnels found."
    
    return f"GRE TUNNELS:\n\n{result}"


def mikrotik_create_gre_tunnel(
    name: str,
    remote_address: str,
    local_address: Optional[str] = None,
    mtu: int = 1476,
    comment: Optional[str] = None
) -> str:
    """Create GRE (Generic Routing Encapsulation) tunnel."""
    app_logger.info(f"Creating GRE tunnel: {name}")
    
    cmd = f'/interface gre add name={name} remote-address={remote_address} mtu={mtu}'
    
    if local_address:
        cmd += f' local-address={local_address}'
    if comment:
        cmd += f' comment="{comment}"'
    
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to create GRE tunnel: {result}"
    
    return f"GRE tunnel '{name}' created successfully."


def mikrotik_remove_gre_tunnel(name: str) -> str:
    """Remove GRE tunnel."""
    app_logger.info(f"Removing GRE tunnel: {name}")
    
    cmd = f'/interface gre remove [find name={name}]'
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to remove GRE tunnel: {result}"
    
    return f"GRE tunnel '{name}' removed successfully."


def mikrotik_list_tunnels() -> str:
    """List all tunnel types (EoIP, GRE). READ-ONLY - safe."""
    app_logger.info("Listing all tunnels")
    
    results = []
    
    # Get EoIP tunnels
    eoip = mikrotik_list_eoip_tunnels()
    results.append(f"=== EoIP TUNNELS ===\n{eoip}")
    
    # Get GRE tunnels
    gre = mikrotik_list_gre_tunnels()
    results.append(f"\n=== GRE TUNNELS ===\n{gre}")
    
    return "\n".join(results)

