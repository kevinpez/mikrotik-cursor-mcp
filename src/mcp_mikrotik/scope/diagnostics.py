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
    
    # Limit max_hops for safety (prevent very long traces)
    if max_hops and max_hops > 15:
        max_hops = 15
    elif not max_hops:
        max_hops = 10  # Reasonable default
    
    cmd = f"/tool traceroute {address}"
    
    if src_address:
        cmd += f" src-address={src_address}"
    if interface:
        cmd += f' interface="{interface}"'
    if max_hops:
        cmd += f" max-hops={max_hops}"
    
    try:
        result = execute_mikrotik_command(cmd)
        
        if not result or result.strip() == "":
            return f"Unable to traceroute to {address}. This may be due to network restrictions or the target being unreachable."
        
        return f"TRACEROUTE ({address}, max-hops={max_hops}):\n\n{result}"
        
    except Exception as e:
        app_logger.error(f"Traceroute failed: {e}")
        return f"Traceroute to {address} failed: {str(e)}"

def mikrotik_bandwidth_test(
    address: Optional[str] = None,
    duration: Optional[int] = 10,
    direction: Optional[str] = "both",
    protocol: Optional[str] = "tcp",
    local_tx_speed: Optional[str] = None,
    remote_tx_speed: Optional[str] = None
) -> str:
    """Run bandwidth test to another MikroTik or local interface"""
    app_logger.info(f"Bandwidth test to: {address or 'auto-detect'}")
    
    # Limit duration for safety (max 30 seconds for testing)
    if duration and duration > 30:
        duration = 30
    elif not duration:
        duration = 5  # Very short default for testing
    
    # If no address specified, try to find a suitable target
    if not address:
        # Try to get the default gateway first
        try:
            gateway_cmd = "/ip route print where dst-address=0.0.0.0/0"
            gateway_result = execute_mikrotik_command(gateway_cmd)
            if gateway_result and "gateway" in gateway_result:
                # Extract gateway IP from the result
                lines = gateway_result.split('\n')
                for line in lines:
                    if "gateway" in line and "0.0.0.0/0" in line:
                        parts = line.split()
                        for i, part in enumerate(parts):
                            if part == "gateway" and i + 1 < len(parts):
                                address = parts[i + 1]
                                break
                        if address:
                            break
        except:
            pass
        
        # If still no address, use a common test target that might work
        if not address:
            address = "127.0.0.1"  # Localhost test
    
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
    
    try:
        result = execute_mikrotik_command(cmd)
        
        if not result or result.strip() == "":
            return f"Unable to run bandwidth test to {address}. This may be because the target doesn't support bandwidth testing or is not reachable."
        
        # Check for common error patterns
        if "failed" in result.lower() or "error" in result.lower() or "timeout" in result.lower() or "unimplemented" in result.lower():
            return f"Bandwidth test to {address} failed or is not supported. This is common when testing against non-MikroTik devices or servers that don't support bandwidth testing.\n\nResult: {result}"
        
        return f"BANDWIDTH TEST ({address}, {duration}s):\n\n{result}"
        
    except Exception as e:
        app_logger.error(f"Bandwidth test failed: {e}")
        error_msg = str(e)
        if "unimplemented" in error_msg.lower() or "type 3" in error_msg.lower():
            return f"Bandwidth test to {address} is not supported by this RouterOS version or the target device.\n\nNote: Bandwidth testing typically only works between MikroTik devices with compatible RouterOS versions."
        return f"Bandwidth test to {address} failed: {error_msg}\n\nNote: Bandwidth testing typically only works between MikroTik devices or with servers that support the bandwidth test protocol."

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

