from typing import Optional
from ..connector import execute_mikrotik_command
from ..logger import app_logger
from ..settings.configuration import validate_config, get_config_summary

def mikrotik_get_system_resources() -> str:
    """Get system resource usage (CPU, RAM, uptime, etc.)"""
    app_logger.info("Getting system resources")
    
    cmd = "/system resource print"
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return "Unable to retrieve system resources."
    
    return f"SYSTEM RESOURCES:\n\n{result}"

def mikrotik_get_system_health() -> str:
    """Get system health (temperature, voltage, etc.)"""
    app_logger.info("Getting system health")
    
    cmd = "/system health print"
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "" or "no such item" in result.lower():
        return "System health monitoring not available on this device."
    
    return f"SYSTEM HEALTH:\n\n{result}"

def mikrotik_get_system_identity() -> str:
    """Get system identity/name"""
    app_logger.info("Getting system identity")
    
    cmd = "/system identity print"
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return "Unable to retrieve system identity."
    
    return f"SYSTEM IDENTITY:\n\n{result}"

def mikrotik_set_system_identity(name: str) -> str:
    """Set system identity/name"""
    app_logger.info(f"Setting system identity to: {name}")
    
    cmd = f'/system identity set name="{name}"'
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to set identity: {result}"
    
    verify_cmd = "/system identity print"
    verify_result = execute_mikrotik_command(verify_cmd)
    
    return f"System identity updated:\n\n{verify_result}"

def mikrotik_get_system_clock() -> str:
    """Get system clock settings"""
    app_logger.info("Getting system clock")
    
    cmd = "/system clock print"
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return "Unable to retrieve system clock."
    
    return f"SYSTEM CLOCK:\n\n{result}"

def mikrotik_get_ntp_client() -> str:
    """Get NTP client configuration"""
    app_logger.info("Getting NTP client configuration")
    
    cmd = "/system ntp client print"
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return "Unable to retrieve NTP client configuration."
    
    return f"NTP CLIENT:\n\n{result}"

def mikrotik_set_ntp_client(
    enabled: bool = True,
    servers: Optional[str] = None,
    mode: Optional[str] = None
) -> str:
    """Configure NTP client"""
    app_logger.info(f"Setting NTP client: enabled={enabled}, servers={servers}")
    
    cmd = "/system ntp client set"
    
    if enabled:
        cmd += " enabled=yes"
    else:
        cmd += " enabled=no"
    
    if servers:
        cmd += f' servers="{servers}"'
    
    if mode:
        cmd += f' mode={mode}'
    
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to configure NTP: {result}"
    
    verify_cmd = "/system ntp client print"
    verify_result = execute_mikrotik_command(verify_cmd)
    
    return f"NTP client configured:\n\n{verify_result}"

def mikrotik_reboot_system(confirm: bool = False) -> str:
    """Reboot the MikroTik device (requires confirmation)"""
    app_logger.info(f"Reboot requested: confirm={confirm}")
    
    if not confirm:
        return "Reboot requires confirmation. Set confirm=True to proceed."
    
    app_logger.warning("REBOOTING MIKROTIK DEVICE!")
    cmd = "/system reboot"
    result = execute_mikrotik_command(cmd)
    
    return "Reboot command sent. Device will restart shortly."

def mikrotik_get_routerboard() -> str:
    """Get RouterBOARD hardware information"""
    app_logger.info("Getting RouterBOARD info")
    
    cmd = "/system routerboard print"
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "" or "no such item" in result.lower():
        return "RouterBOARD information not available (possibly CHR or x86)."
    
    return f"ROUTERBOARD INFO:\n\n{result}"

def mikrotik_get_license() -> str:
    """Get RouterOS license information"""
    app_logger.info("Getting license info")
    
    cmd = "/system license print"
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return "Unable to retrieve license information."
    
    return f"LICENSE INFO:\n\n{result}"

def mikrotik_get_uptime() -> str:
    """Get system uptime"""
    app_logger.info("Getting system uptime")
    
    cmd = "/system resource print"
    result = execute_mikrotik_command(cmd)
    
    if not result:
        return "Unable to retrieve uptime."
    
    # Extract just the uptime line
    lines = result.split('\n')
    for line in lines:
        if 'uptime:' in line.lower():
            return f"SYSTEM UPTIME:\n\n{line.strip()}"
    
    return f"SYSTEM INFO:\n\n{result}"

def mikrotik_validate_configuration() -> str:
    """Validate the MikroTik MCP server configuration."""
    app_logger.info("Validating configuration")
    
    issues = validate_config()
    
    if not issues:
        return "✅ CONFIGURATION VALID\n\nAll configuration settings are valid and properly configured."
    
    result = "❌ CONFIGURATION ISSUES FOUND:\n\n"
    for i, issue in enumerate(issues, 1):
        result += f"{i}. {issue}\n"
    
    result += "\nPlease fix these issues before using the MCP server."
    return result

def mikrotik_get_configuration_summary() -> str:
    """Get a summary of the current configuration (without sensitive data)."""
    app_logger.info("Getting configuration summary")
    
    summary = get_config_summary()
    
    result = "📋 CONFIGURATION SUMMARY:\n\n"
    for key, value in summary.items():
        result += f"{key.replace('_', ' ').title()}: {value}\n"
    
    return result

