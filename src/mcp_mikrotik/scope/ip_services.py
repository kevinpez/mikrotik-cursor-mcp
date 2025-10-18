"""
MikroTik IP Services Management
Manage IP services (SSH, Winbox, API, etc.) and their access controls
"""
from typing import Dict, Any, List, Optional
from ..connector import execute_mikrotik_command
from ..api_fallback import api_fallback_execute
from ..logger import app_logger


def mikrotik_list_ip_services(test_args: Dict[str, Any] = None) -> str:
    """List all IP services and their current configuration."""
    app_logger.info("Listing IP services")
    try:
        result = execute_mikrotik_command('/ip service print')
        app_logger.info("Successfully listed IP services")
        return result
    except Exception as e:
        error_msg = f"Failed to list IP services: {str(e)}"
        app_logger.error(error_msg)
        return error_msg


def mikrotik_get_ip_service(service_name: str, test_args: Dict[str, Any] = None) -> str:
    """Get configuration for a specific IP service."""
    app_logger.info(f"Getting IP service configuration for: {service_name}")
    try:
        result = execute_mikrotik_command(f'/ip service print where name={service_name}')
        app_logger.info(f"Successfully retrieved service {service_name}")
        return result
    except Exception as e:
        error_msg = f"Failed to get IP service {service_name}: {str(e)}"
        app_logger.error(error_msg)
        return error_msg


def mikrotik_set_service_address(service_name: str, address: str, test_args: Dict[str, Any] = None) -> str:
    """
    Set the 'Available From' address for an IP service.
    
    Args:
        service_name: Name of the service (ssh, winbox, api, telnet, ftp, etc.)
        address: IP address or network (e.g., "192.168.88.0/24" or "0.0.0.0/0")
    """
    app_logger.info(f"Setting service {service_name} address to: {address}")
    try:
        result = execute_mikrotik_command(f'/ip service set {service_name} address={address}')
        app_logger.info(f"Successfully set service {service_name} address to {address}")
        return f"SUCCESS: Service {service_name} address set to {address}\n\nResult: {result}"
    except Exception as e:
        error_msg = f"Failed to set service {service_name} address: {str(e)}"
        app_logger.error(error_msg)
        return error_msg


def mikrotik_enable_ip_service(service_name: str, test_args: Dict[str, Any] = None) -> str:
    """Enable an IP service."""
    app_logger.info(f"Enabling IP service: {service_name}")
    try:
        result = execute_mikrotik_command(f'/ip service set {service_name} disabled=no')
        app_logger.info(f"Successfully enabled service {service_name}")
        return f"SUCCESS: Service {service_name} enabled\n\nResult: {result}"
    except Exception as e:
        error_msg = f"Failed to enable service {service_name}: {str(e)}"
        app_logger.error(error_msg)
        return error_msg


def mikrotik_disable_ip_service(service_name: str, test_args: Dict[str, Any] = None) -> str:
    """Disable an IP service."""
    app_logger.info(f"Disabling IP service: {service_name}")
    try:
        result = execute_mikrotik_command(f'/ip service set {service_name} disabled=yes')
        app_logger.info(f"Successfully disabled service {service_name}")
        return f"SUCCESS: Service {service_name} disabled\n\nResult: {result}"
    except Exception as e:
        error_msg = f"Failed to disable service {service_name}: {str(e)}"
        app_logger.error(error_msg)
        return error_msg


def mikrotik_set_service_port(service_name: str, port: int, test_args: Dict[str, Any] = None) -> str:
    """Set the port for an IP service."""
    app_logger.info(f"Setting service {service_name} port to: {port}")
    try:
        result = execute_mikrotik_command(f'/ip service set {service_name} port={port}')
        app_logger.info(f"Successfully set service {service_name} port to {port}")
        return f"SUCCESS: Service {service_name} port set to {port}\n\nResult: {result}"
    except Exception as e:
        error_msg = f"Failed to set service {service_name} port: {str(e)}"
        app_logger.error(error_msg)
        return error_msg


def mikrotik_configure_secure_services(local_network: str = "192.168.88.0/24", test_args: Dict[str, Any] = None) -> str:
    """
    Configure secure IP services - restrict to local network only.
    
    Args:
        local_network: Local network to allow access from (default: 192.168.88.0/24)
    """
    app_logger.info(f"Configuring secure IP services for network: {local_network}")
    
    # Services to secure (restrict to local network)
    secure_services = ['ssh', 'winbox', 'api']
    
    # Services to disable entirely
    disable_services = ['telnet', 'ftp']
    
    results = []
    
    try:
        # Secure services - restrict to local network
        for service in secure_services:
            app_logger.info(f"Securing service: {service}")
            result = execute_mikrotik_command(f'/ip service set {service} address={local_network}')
            results.append(f"✓ {service}: Restricted to {local_network}")
        
        # Disable insecure services
        for service in disable_services:
            app_logger.info(f"Disabling service: {service}")
            result = execute_mikrotik_command(f'/ip service set {service} disabled=yes')
            results.append(f"✓ {service}: Disabled")
        
        app_logger.info("Successfully configured secure IP services")
        return f"""SUCCESS: IP Services Security Configuration Complete

Services Restricted to {local_network}:
{chr(10).join(results[:3])}

Services Disabled:
{chr(10).join(results[3:])}

Your MikroTik router is now secured with proper service access controls!"""
        
    except Exception as e:
        error_msg = f"Failed to configure secure services: {str(e)}"
        app_logger.error(error_msg)
        return error_msg


def mikrotik_restore_default_services(test_args: Dict[str, Any] = None) -> str:
    """Restore IP services to default configuration (allow from anywhere)."""
    app_logger.info("Restoring IP services to default configuration")
    
    # Services to restore to default (allow from anywhere)
    default_services = ['ssh', 'winbox', 'api']
    
    results = []
    
    try:
        for service in default_services:
            app_logger.info(f"Restoring service: {service}")
            result = execute_mikrotik_command(f'/ip service set {service} address=0.0.0.0/0')
            results.append(f"✓ {service}: Restored to default (allow from anywhere)")
        
        app_logger.info("Successfully restored default IP services")
        return f"""SUCCESS: IP Services Restored to Default

Services Restored:
{chr(10).join(results)}

WARNING: Services are now accessible from anywhere. Consider using secure configuration for production environments."""
        
    except Exception as e:
        error_msg = f"Failed to restore default services: {str(e)}"
        app_logger.error(error_msg)
        return error_msg


def mikrotik_get_service_status(test_args: Dict[str, Any] = None) -> str:
    """Get status summary of all IP services."""
    app_logger.info("Getting IP services status summary")
    try:
        result = execute_mikrotik_command('/ip service print')
        
        # Parse the result to create a summary
        lines = result.strip().split('\n')
        services = []
        
        for line in lines:
            if line.strip() and not line.startswith('Flags:') and not line.startswith('Columns:'):
                # Parse service information
                parts = line.split()
                if len(parts) >= 4:
                    name = parts[1] if len(parts) > 1 else "unknown"
                    port = parts[2] if len(parts) > 2 else "unknown"
                    address = parts[3] if len(parts) > 3 else "unknown"
                    disabled = "X" in parts[0] if parts else False
                    
                    status = "DISABLED" if disabled else "ENABLED"
                    services.append(f"  {name}: Port {port}, Address: {address}, Status: {status}")
        
        app_logger.info("Successfully retrieved IP services status")
        return f"""IP Services Status Summary:

{chr(10).join(services) if services else "No services found"}

Legend:
- Address 0.0.0.0/0 = Accessible from anywhere
- Address 192.168.88.0/24 = Restricted to local network
- Status DISABLED = Service is disabled"""
        
    except Exception as e:
        error_msg = f"Failed to get service status: {str(e)}"
        app_logger.error(error_msg)
        return error_msg


def mikrotik_create_service_backup(test_args: Dict[str, Any] = None) -> str:
    """Create a backup of current IP services configuration."""
    app_logger.info("Creating IP services configuration backup")
    try:
        result = execute_mikrotik_command('/ip service export')
        app_logger.info("Successfully created IP services backup")
        return f"""SUCCESS: IP Services Configuration Backup

Backup Configuration:
{result}

You can restore this configuration later if needed."""
        
    except Exception as e:
        error_msg = f"Failed to create service backup: {str(e)}"
        app_logger.error(error_msg)
        return error_msg
