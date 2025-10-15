from .logger import app_logger
from .connection_manager import get_connection_manager
from .settings.configuration import mikrotik_config


def execute_mikrotik_command(command: str) -> str:
    """
    Execute a MikroTik command via SSH and return the output.
    Uses connection pooling for better performance.
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
            
            if error and not output:
                app_logger.warning(f"Command error: {error}")
                return error
            
            app_logger.debug(f"Command result length: {len(output)} chars")
            return output
            
    except Exception as e:
        error_msg = f"Error executing command: {str(e)}"
        app_logger.error(error_msg)
        return error_msg
