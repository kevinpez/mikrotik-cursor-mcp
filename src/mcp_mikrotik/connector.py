import os
from .logger import app_logger
from .connection_manager import get_connection_manager
from .settings.configuration import mikrotik_config


def execute_mikrotik_command(command: str) -> str:
    """
    Execute a MikroTik command via SSH and return the output.
    Uses connection pooling for better performance.
    Handles RouterOS-specific errors gracefully.
    """
    app_logger.info(f"Executing MikroTik command: {command}")
    
    connection_manager = get_connection_manager()
    
    try:
        with connection_manager.get_connection_context() as ssh_client:
            stdin, stdout, stderr = ssh_client.exec_command(
                command,
                timeout=mikrotik_config.get("command_timeout", 30)
            )
            
            output = stdout.read().decode('utf-8')
            error = stderr.read().decode('utf-8')
            
            # Handle RouterOS-specific errors
            if error and not output:
                app_logger.warning(f"Command error: {error}")
                return error
            
            # Check for RouterOS unimplemented errors in output
            if "Oops, unhandled type" in output or "unimplemented" in output.lower():
                app_logger.warning(f"RouterOS command not supported: {command}")
                return f"ERROR: Command not supported on this router model\n\nCommand: {command}\n\nThis command is not implemented or supported on your RouterOS version/router model.\n\nTry using a different approach or check if the required package is installed."
            
            # Check for other RouterOS error patterns
            if "bad command name" in output.lower() or "syntax error" in output.lower():
                app_logger.warning(f"RouterOS syntax error: {command}")
                return f"ERROR: Invalid command syntax\n\nCommand: {command}\n\nError: {output.strip()}"
            
            # Check for permission errors
            if "access denied" in output.lower() or "permission denied" in output.lower():
                app_logger.warning(f"Permission denied: {command}")
                return f"ERROR: Permission denied\n\nCommand: {command}\n\nYou don't have sufficient privileges to execute this command.\n\nError: {output.strip()}"
            
            app_logger.debug(f"Command result length: {len(output)} chars")
            return output
            
    except Exception as e:
        error_msg = f"Error executing command: {str(e)}"
        app_logger.error(error_msg)
        return error_msg
