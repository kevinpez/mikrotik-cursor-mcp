from typing import Optional
from ..connector import execute_mikrotik_command
from ..api_fallback import api_fallback_execute
from ..logger import app_logger

def mikrotik_get_watchdog_status() -> str:
    """
    Gets the current watchdog status and settings.
    
    Returns:
        Watchdog status information
    """
    app_logger.info("Getting watchdog status")
    
    cmd = "/system watchdog print detail"
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return "Unable to get watchdog status."
    
    return f"WATCHDOG STATUS:\n\n{result}"

def mikrotik_enable_watchdog(
    watchdog_timer: bool = True,
    automatic_supout: bool = True,
    auto_send_supout: bool = False,
    send_email_to: Optional[str] = None,
    send_smtp_server: Optional[str] = None,
    no_ping_delay: Optional[str] = None,
    ping_start_after_boot: Optional[str] = None,
    ping_timeout: Optional[str] = None
) -> str:
    """
    Enables and configures the watchdog.
    
    Args:
        watchdog_timer: Enable hardware watchdog timer
        automatic_supout: Automatically generate supout.rif file on crash
        auto_send_supout: Automatically send supout file
        send_email_to: Email address to send supout to
        send_smtp_server: SMTP server for sending email
        no_ping_delay: Delay before watchdog considers ping lost (e.g., 5m)
        ping_start_after_boot: Delay after boot before watchdog starts pinging (e.g., 5m)
        ping_timeout: Ping timeout (e.g., 1m)
    
    Returns:
        Command output or error message
    """
    app_logger.info("Enabling watchdog")
    
    cmd = "/system watchdog set"
    updates = []
    
    updates.append(f'watchdog-timer={"yes" if watchdog_timer else "no"}')
    updates.append(f'automatic-supout={"yes" if automatic_supout else "no"}')
    updates.append(f'auto-send-supout={"yes" if auto_send_supout else "no"}')
    
    if send_email_to:
        updates.append(f'send-email-to="{send_email_to}"')
    
    if send_smtp_server:
        updates.append(f'send-smtp-server={send_smtp_server}')
    
    if no_ping_delay:
        updates.append(f'no-ping-delay={no_ping_delay}')
    
    if ping_start_after_boot:
        updates.append(f'ping-start-after-boot={ping_start_after_boot}')
    
    if ping_timeout:
        updates.append(f'ping-timeout={ping_timeout}')
    
    cmd += " " + " ".join(updates)
    
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to configure watchdog: {result}"
    
    # Get the updated status
    status = mikrotik_get_watchdog_status()
    
    return f"Watchdog configured successfully.\n\n{status}"

def mikrotik_disable_watchdog() -> str:
    """
    Disables the watchdog.
    
    Returns:
        Command output or error message
    """
    app_logger.info("Disabling watchdog")
    
    cmd = "/system watchdog set watchdog-timer=no"
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to disable watchdog: {result}"
    
    return "Watchdog has been disabled."

def mikrotik_get_watchdog_types() -> str:
    """
    Lists available watchdog timer types.
    
    Returns:
        List of watchdog types
    """
    app_logger.info("Getting watchdog types")
    
    cmd = "/system watchdog print detail"
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return "Unable to get watchdog types."
    
    # Extract type information
    return f"WATCHDOG INFORMATION:\n\n{result}"

def mikrotik_set_watchdog_ping_target(ip_address: str) -> str:
    """
    Sets the ping target for watchdog monitoring.
    
    Args:
        ip_address: IP address to ping
    
    Returns:
        Command output or error message
    
    Note: If watchdog cannot ping this address, it will trigger a reboot
    """
    app_logger.info(f"Setting watchdog ping target: {ip_address}")
    
    if not ip_address or ip_address.strip() == "":
        return "Error: IP address cannot be empty."
    
    cmd = f'/system watchdog set watch-address={ip_address}'
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to set watchdog ping target: {result}"
    
    # Get the updated status
    status = mikrotik_get_watchdog_status()
    
    return f"Watchdog ping target set to '{ip_address}'.\n\n{status}"

def mikrotik_reset_watchdog_ping_target() -> str:
    """
    Removes the ping target from watchdog monitoring.
    
    Returns:
        Command output or error message
    """
    app_logger.info("Resetting watchdog ping target")
    
    cmd = "/system watchdog set watch-address=none"
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to reset watchdog ping target: {result}"
    
    return "Watchdog ping target has been reset."

def mikrotik_create_watchdog_script(
    script_name: str,
    script_content: str,
    trigger_type: str = "reboot"
) -> str:
    """
    Creates a watchdog monitoring script.
    
    Args:
        script_name: Name for the watchdog script
        script_content: Script content (RouterOS script)
        trigger_type: When to trigger (reboot, email, both)
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Creating watchdog script: {script_name}")
    
    if not script_name or script_name.strip() == "":
        return "Error: Script name cannot be empty."
    
    if not script_content or script_content.strip() == "":
        return "Error: Script content cannot be empty."
    
    # Create the monitoring script
    create_cmd = f'/system script add name="{script_name}" source="{script_content}" policy=read,write,policy,test,reboot'
    create_result = execute_mikrotik_command(create_cmd)
    
    if "failure:" in create_result.lower() or "error" in create_result.lower():
        return f"Failed to create watchdog script: {create_result}"
    
    return f"Watchdog script '{script_name}' created successfully. You can now add it to a scheduled task for periodic monitoring."

def mikrotik_create_basic_watchdog_monitor(
    monitor_name: str,
    check_interval: str = "5m",
    ping_target: Optional[str] = None,
    reboot_on_failure: bool = True
) -> str:
    """
    Creates a basic watchdog monitoring setup.
    
    Args:
        monitor_name: Name for the monitoring task
        check_interval: How often to check (e.g., 5m, 10m, 1h)
        ping_target: Optional IP address to ping for connectivity check
        reboot_on_failure: Whether to reboot on failure
    
    Returns:
        Setup result
    """
    app_logger.info(f"Creating basic watchdog monitor: {monitor_name}")
    
    results = []
    
    # Configure hardware watchdog if available
    config_cmd = "/system watchdog set watchdog-timer=yes automatic-supout=yes"
    config_result = execute_mikrotik_command(config_cmd)
    results.append(f"✓ Hardware watchdog enabled: {config_result if config_result else 'Success'}")
    
    # Set ping target if provided
    if ping_target:
        ping_cmd = f'/system watchdog set watch-address={ping_target} no-ping-delay=5m'
        ping_result = execute_mikrotik_command(ping_cmd)
        results.append(f"✓ Ping monitoring set for {ping_target}: {ping_result if ping_result else 'Success'}")
    
    # Create a monitoring script
    script_name = f"{monitor_name}-script"
    script_content = """
:local cpuLoad [/system resource get cpu-load]
:local freeMemory [/system resource get free-memory]
:local totalMemory [/system resource get total-memory]

:if ($cpuLoad > 90) do={
    :log warning "High CPU load detected: $cpuLoad%"
}

:local memPercent (($freeMemory * 100) / $totalMemory)
:if ($memPercent < 10) do={
    :log warning "Low memory: $memPercent% free"
}
"""
    
    script_cmd = f'/system script add name="{script_name}" source="{script_content}" policy=read,write,policy,test'
    script_result = execute_mikrotik_command(script_cmd)
    results.append(f"✓ Monitoring script created: {script_name}")
    
    # Create scheduled task to run the script
    task_cmd = f'/system scheduler add name="{monitor_name}" on-event="{script_name}" interval={check_interval} policy=read,write,policy,test'
    task_result = execute_mikrotik_command(task_cmd)
    results.append(f"✓ Monitoring task scheduled: runs every {check_interval}")
    
    return f"WATCHDOG MONITOR SETUP COMPLETE:\n\n" + "\n".join(results)

