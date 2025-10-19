"""
MikroTik Safe Mode implementation.
Provides access to RouterOS's built-in safe mode functionality with automatic rollback.
"""
from typing import Optional
from ..connector import execute_mikrotik_command
from ..api_fallback import api_fallback_execute
from ..logger import app_logger


def mikrotik_enter_safe_mode(timeout_minutes: Optional[int] = None) -> str:
    """
    Enter MikroTik Safe Mode.
    
    In Safe Mode, all changes are temporary and will be automatically reverted
    if the connection is lost or after the timeout period (default 10 minutes).
    Changes are only made permanent when Safe Mode is explicitly exited.
    
    Args:
        timeout_minutes: Optional timeout in minutes (default: 10 minutes)
        
    Returns:
        Status message about Safe Mode activation
    """
    app_logger.info("Entering MikroTik Safe Mode")
    
    try:
        # Try to enter safe mode using the command
        command = "/system safe-mode"
        
        if timeout_minutes:
            command += f" generic-timeout={timeout_minutes}m"
        
        result = execute_mikrotik_command(command)
        
        # Check if the result contains an error message
        if "ERROR:" in result or "bad command name" in result.lower() or "no such command" in result.lower() or "bad command name safe-mode" in result.lower():
            app_logger.info("Safe Mode is not available via API/SSH - this is a terminal-only feature")
            return f"INFO: SAFE MODE NOT AVAILABLE VIA API/SSH\n\nSafe Mode is a terminal-only feature in RouterOS and cannot be accessed via API or SSH commands.\n\nTo use Safe Mode:\n1. Connect directly to the router console\n2. Press Ctrl+X to enter Safe Mode\n3. Make your configuration changes\n4. Press Ctrl+X again to exit and make changes permanent\n\nThis is a limitation of RouterOS, not the MCP server."
        elif "safe mode" in result.lower() or "entered" in result.lower():
            app_logger.info("Successfully entered Safe Mode")
            return f"SUCCESS: SAFE MODE ACTIVATED\n\nSafe Mode is now active. All configuration changes will be temporary until Safe Mode is exited.\n\nTimeout: {timeout_minutes or 10} minutes\n\nTo make changes permanent, use the exit safe mode command.\n\nResult: {result}"
        else:
            app_logger.warning(f"Safe Mode activation may have failed: {result}")
            return f"WARNING: Safe Mode activation result: {result}"
            
    except Exception as e:
        error_msg = f"Failed to enter Safe Mode: {str(e)}"
        app_logger.error(error_msg)
        return error_msg


def mikrotik_exit_safe_mode() -> str:
    """
    Exit MikroTik Safe Mode and make all changes permanent.
    
    This command makes all temporary changes made during Safe Mode permanent.
    Use this command when you're satisfied with your configuration changes.
    
    Returns:
        Status message about Safe Mode deactivation
    """
    app_logger.info("Exiting MikroTik Safe Mode")
    
    try:
        # Exit safe mode - this makes all changes permanent
        command = "/system safe-mode"
        result = execute_mikrotik_command(command)
        
        # Check if the result contains an error message
        if "ERROR:" in result or "bad command name" in result.lower() or "no such command" in result.lower() or "bad command name safe-mode" in result.lower():
            app_logger.info("Safe Mode is not available via API/SSH - this is a terminal-only feature")
            return f"INFO: SAFE MODE NOT AVAILABLE VIA API/SSH\n\nSafe Mode is a terminal-only feature in RouterOS and cannot be accessed via API or SSH commands.\n\nTo exit Safe Mode:\n1. Connect directly to the router console\n2. Press Ctrl+X to exit Safe Mode and make changes permanent\n\nThis is a limitation of RouterOS, not the MCP server."
        elif "safe mode" in result.lower() or "exited" in result.lower():
            app_logger.info("Successfully exited Safe Mode - changes are now permanent")
            return f"✅ SAFE MODE DEACTIVATED\n\nSafe Mode has been exited. All configuration changes made during Safe Mode are now permanent.\n\nResult: {result}"
        else:
            app_logger.warning(f"Safe Mode deactivation may have failed: {result}")
            return f"⚠️ Safe Mode deactivation result: {result}"
            
    except Exception as e:
        error_msg = f"Failed to exit Safe Mode: {str(e)}"
        app_logger.error(error_msg)
        return error_msg


def mikrotik_get_safe_mode_status() -> str:
    """
    Get the current Safe Mode status.
    
    Returns:
        Current Safe Mode status and configuration
    """
    app_logger.info("Getting Safe Mode status")
    
    try:
        # Get safe mode status
        command = "/system safe-mode print"
        result = execute_mikrotik_command(command)
        
        # Check if the result contains an error message
        if "ERROR:" in result or "bad command name" in result.lower() or "no such command" in result.lower() or "bad command name safe-mode" in result.lower():
            app_logger.info("Safe Mode is not available via API/SSH - this is a terminal-only feature")
            return f"INFO: SAFE MODE NOT AVAILABLE VIA API/SSH\n\nSafe Mode is a terminal-only feature in RouterOS and cannot be accessed via API or SSH commands.\n\nSafe Mode status can only be checked by connecting directly to the router console.\n\nThis is a limitation of RouterOS, not the MCP server."
        else:
            app_logger.info("Retrieved Safe Mode status")
            return f"📊 SAFE MODE STATUS\n\n{result}"
        
    except Exception as e:
        error_msg = f"Failed to get Safe Mode status: {str(e)}"
        app_logger.error(error_msg)
        return error_msg


def mikrotik_set_safe_mode_timeout(timeout_minutes: int) -> str:
    """
    Set the Safe Mode timeout period.
    
    This sets how long the router will wait before automatically reverting
    changes if Safe Mode is not explicitly exited.
    
    Args:
        timeout_minutes: Timeout period in minutes (1-60)
        
    Returns:
        Status message about timeout configuration
    """
    app_logger.info(f"Setting Safe Mode timeout to {timeout_minutes} minutes")
    
    if not (1 <= timeout_minutes <= 60):
        return "❌ ERROR: Timeout must be between 1 and 60 minutes"
    
    try:
        # Set the generic timeout for safe mode
        command = f"/system safe-mode set generic-timeout={timeout_minutes}m"
        result = execute_mikrotik_command(command)
        
        # Check if the result contains an error message
        if "ERROR:" in result or "bad command name" in result.lower() or "no such command" in result.lower() or "bad command name safe-mode" in result.lower():
            app_logger.info("Safe Mode is not available via API/SSH - this is a terminal-only feature")
            return f"INFO: SAFE MODE NOT AVAILABLE VIA API/SSH\n\nSafe Mode is a terminal-only feature in RouterOS and cannot be accessed via API or SSH commands.\n\nSafe Mode timeout cannot be set remotely. This must be done by connecting directly to the router console.\n\nThis is a limitation of RouterOS, not the MCP server."
        else:
            app_logger.info(f"Safe Mode timeout set to {timeout_minutes} minutes")
            return f"✅ SAFE MODE TIMEOUT SET\n\nSafe Mode timeout has been set to {timeout_minutes} minutes.\n\nThis means that if Safe Mode is not explicitly exited, changes will be automatically reverted after {timeout_minutes} minutes.\n\nResult: {result}"
        
    except Exception as e:
        error_msg = f"Failed to set Safe Mode timeout: {str(e)}"
        app_logger.error(error_msg)
        return error_msg


def mikrotik_force_exit_safe_mode() -> str:
    """
    Force exit Safe Mode (emergency use).
    
    This command forces an immediate exit from Safe Mode, making all changes permanent.
    Use this only in emergency situations when normal exit is not possible.
    
    Returns:
        Status message about forced Safe Mode exit
    """
    app_logger.warning("Force exiting Safe Mode - this makes all changes permanent immediately")
    
    try:
        # Force exit safe mode
        command = "/system safe-mode force-exit"
        result = execute_mikrotik_command(command)
        
        # Check if the result contains an error message
        if "ERROR:" in result or "bad command name" in result.lower() or "no such command" in result.lower() or "bad command name safe-mode" in result.lower():
            app_logger.info("Safe Mode is not available via API/SSH - this is a terminal-only feature")
            return f"INFO: SAFE MODE NOT AVAILABLE VIA API/SSH\n\nSafe Mode is a terminal-only feature in RouterOS and cannot be accessed via API or SSH commands.\n\nTo force exit Safe Mode:\n1. Connect directly to the router console\n2. Press Ctrl+X to force exit Safe Mode\n\nThis is a limitation of RouterOS, not the MCP server."
        else:
            app_logger.warning("Force exited Safe Mode - all changes are now permanent")
            return f"🚨 FORCE EXIT SAFE MODE\n\nSafe Mode has been force exited. All configuration changes are now permanent.\n\n⚠️ WARNING: This action cannot be undone.\n\nResult: {result}"
        
    except Exception as e:
        error_msg = f"Failed to force exit Safe Mode: {str(e)}"
        app_logger.error(error_msg)
        return error_msg


def mikrotik_get_safe_mode_history() -> str:
    """
    Get Safe Mode change history.
    
    Returns the history of changes made during the current Safe Mode session.
    Safe Mode maintains a history of up to 100 recent actions.
    
    Returns:
        History of changes made in Safe Mode
    """
    app_logger.info("Getting Safe Mode change history")
    
    try:
        # Get safe mode history (this might not be available in all RouterOS versions)
        command = "/system safe-mode history print"
        result = execute_mikrotik_command(command)
        
        # Check if the result contains an error message
        if "ERROR:" in result or "bad command name" in result.lower() or "no such command" in result.lower() or "bad command name safe-mode" in result.lower():
            app_logger.info("Safe Mode is not available via API/SSH - this is a terminal-only feature")
            return f"INFO: SAFE MODE NOT AVAILABLE VIA API/SSH\n\nSafe Mode is a terminal-only feature in RouterOS and cannot be accessed via API or SSH commands.\n\nSafe Mode history can only be viewed by connecting directly to the router console.\n\nThis is a limitation of RouterOS, not the MCP server."
        else:
            app_logger.info("Retrieved Safe Mode history")
            return f"📋 SAFE MODE HISTORY\n\n{result}"
        
    except Exception as e:
        # If history command is not available, provide alternative information
        app_logger.info("Safe Mode history command not available, getting general status")
        try:
            command = "/system safe-mode print"
            result = execute_mikrotik_command(command)
            return f"📋 SAFE MODE STATUS (History not available)\n\nSafe Mode history is not available in this RouterOS version.\n\nCurrent status:\n{result}"
        except Exception as e2:
            error_msg = f"Failed to get Safe Mode information: {str(e2)}"
            app_logger.error(error_msg)
            return error_msg


def mikrotik_create_safe_mode_backup() -> str:
    """
    Create a backup before entering Safe Mode.
    
    This is a best practice - create a backup before making changes in Safe Mode
    so you have a known good configuration to restore if needed.
    
    Returns:
        Status message about backup creation
    """
    app_logger.info("Creating backup before Safe Mode operations")
    
    try:
        # Create a backup with timestamp
        import time
        timestamp = int(time.time())
        backup_name = f"pre-safe-mode-{timestamp}"
        
        command = f"/system backup save name={backup_name}"
        result = execute_mikrotik_command(command)
        
        app_logger.info(f"Created backup: {backup_name}")
        return f"💾 BACKUP CREATED\n\nBackup created successfully: {backup_name}\n\nThis backup was created before Safe Mode operations. You can restore from this backup if needed.\n\nResult: {result}"
        
    except Exception as e:
        error_msg = f"Failed to create backup: {str(e)}"
        app_logger.error(error_msg)
        return error_msg
