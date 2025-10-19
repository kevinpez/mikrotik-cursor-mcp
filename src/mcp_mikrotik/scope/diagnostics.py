from typing import Optional
from ..connector import execute_mikrotik_command
from ..api_fallback import api_fallback_execute
from ..logger import app_logger

def mikrotik_ping(
    address: str,
    count: Optional[int] = 4,
    size: Optional[int] = None,
    interval: Optional[str] = None,
    src_address: Optional[str] = None,
    interface: Optional[str] = None
) -> str:
    """Ping a host from the MikroTik router"""
    app_logger.info(f"Pinging: {address}")
    
    cmd = f"/ping {address}"
    
    if count:
        cmd += f" count={count}"
    if size:
        cmd += f" size={size}"
    if interval:
        cmd += f" interval={interval}"
    if src_address:
        cmd += f" src-address={src_address}"
    if interface:
        cmd += f' interface="{interface}"'
    
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return f"Unable to ping {address}."
    
    return f"PING RESULTS ({address}):\n\n{result}"

def mikrotik_traceroute(
    address: str,
    src_address: Optional[str] = None,
    interface: Optional[str] = None,
    max_hops: Optional[int] = None
) -> str:
    """Traceroute to a host from the MikroTik router"""
    app_logger.info(f"Traceroute to: {address}")
    
    cmd = f"/tool traceroute {address}"
    
    if src_address:
        cmd += f" src-address={src_address}"
    if interface:
        cmd += f' interface="{interface}"'
    if max_hops:
        cmd += f" max-hops={max_hops}"
    
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return f"Unable to traceroute to {address}."
    
    return f"TRACEROUTE ({address}):\n\n{result}"

def mikrotik_bandwidth_test(
    address: str,
    duration: Optional[int] = 10,
    direction: Optional[str] = "both",
    protocol: Optional[str] = "tcp",
    local_tx_speed: Optional[str] = None,
    remote_tx_speed: Optional[str] = None
) -> str:
    """Run bandwidth test to another MikroTik"""
    app_logger.info(f"Bandwidth test to: {address}")
    
    cmd = f"/tool bandwidth-test {address}"
    
    if duration:
        cmd += f" duration={duration}s"
    if direction:
        cmd += f" direction={direction}"
    if protocol:
        cmd += f" protocol={protocol}"
    if local_tx_speed:
        cmd += f" local-tx-speed={local_tx_speed}"
    if remote_tx_speed:
        cmd += f" remote-tx-speed={remote_tx_speed}"
    
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return f"Unable to run bandwidth test to {address}."
    
    return f"BANDWIDTH TEST ({address}):\n\n{result}"

def mikrotik_dns_lookup(hostname: str, server: Optional[str] = None) -> str:
    """Perform DNS lookup"""
    app_logger.info(f"DNS lookup: {hostname}")
    
    try:
        # Use API for DNS lookup (more reliable)
        params = {"name": hostname}
        if server:
            params["server"] = server
        
        result = api_fallback_execute("/tool/dns-lookup", params)
        
        if not result or result.strip() == "":
            return f"DNS lookup not available or unable to resolve {hostname}."
        
        return f"DNS LOOKUP ({hostname}):\n\n{result}"
        
    except Exception as e:
        # Fallback to simple ping as dns-lookup tool may not be available
        app_logger.warning(f"DNS lookup failed, trying ping: {e}")
        try:
            ping_cmd = f'/ping {hostname} count=1'
            ping_result = execute_mikrotik_command(ping_cmd)
            if ping_result and "timeout" not in ping_result.lower():
                return f"DNS RESOLUTION ({hostname}):\n\nHost is reachable (DNS tool not available)\n{ping_result}"
            else:
                return f"Unable to resolve {hostname}"
        except:
            return f"DNS lookup not available: {str(e)}"

def mikrotik_check_connection(
    address: str,
    port: Optional[int] = None,
    protocol: Optional[str] = "tcp"
) -> str:
    """Check if a port is reachable"""
    app_logger.info(f"Checking connection: {address}:{port}")
    
    if port:
        # Use tool/fetch to test TCP connectivity
        # Note: dst-path uses a simple filename without special chars
        cmd = f"/tool fetch url=tcp://{address}:{port} mode=tcp check-certificate=no dst-path=conn-test.txt"
    else:
        # Just ping if no port specified
        cmd = f"/ping {address} count=1"
    
    result = execute_mikrotik_command(cmd)
    
    if not result:
        return f"Unable to check connection to {address}."
    
    # Check if connection was successful
    if port:
        if "status: finished" in result.lower():
            return f"CONNECTION CHECK ({address}:{port}):\n\n✅ Port {port} is REACHABLE (Connection successful)\n\n{result}"
        elif "failed" in result.lower() or "timeout" in result.lower() or "could not" in result.lower() or "connect" in result.lower():
            return f"CONNECTION CHECK ({address}:{port}):\n\n❌ Port {port} is NOT REACHABLE (Connection failed)\n\n{result}"
        else:
            return f"CONNECTION CHECK ({address}:{port}):\n\n⚠️ Status unclear\n\n{result}"
    
    return f"CONNECTION CHECK ({address}):\n\n{result}"

def mikrotik_get_arp_table(
    interface: Optional[str] = None,
    address: Optional[str] = None
) -> str:
    """Get ARP table"""
    app_logger.info(f"Getting ARP table: interface={interface}, address={address}")
    
    cmd = "/ip arp print"
    
    filters = []
    if interface:
        filters.append(f'interface="{interface}"')
    if address:
        filters.append(f'address={address}')
    
    if filters:
        cmd += " where " + " and ".join(filters)
    
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return "No ARP entries found."
    
    return f"ARP TABLE:\n\n{result}"

def mikrotik_get_neighbors() -> str:
    """Get neighboring MikroTik devices (MAC discovery)"""
    app_logger.info("Getting neighbors via discovery")
    
    cmd = "/ip neighbor print"
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return "No neighbors discovered."
    
    return f"NEIGHBORS:\n\n{result}"

