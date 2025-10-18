"""
API Fallback Utility
Provides functions that try API first, then fall back to SSH if API fails.
"""

from typing import Any, Dict, List, Optional
from .logger import app_logger
from .connector import execute_mikrotik_command


def api_fallback_execute(api_path: str, api_command: str = "print", ssh_command: Optional[str] = None, **kwargs) -> str:
    """
    Execute a command using API first, fall back to SSH if API fails.
    
    Args:
        api_path: API path (e.g., '/system/identity', '/ip/route')
        api_command: API command ('print', 'add', 'set', 'remove', etc.)
        ssh_command: SSH command to use as fallback (if None, will be generated)
        **kwargs: Additional parameters for the command
    
    Returns:
        Command result as string
    """
    try:
        from .api_connector import execute_api_command
        
        # Try API first
        app_logger.debug(f"Trying API: {api_path}/{api_command} with args: {kwargs}")
        result = execute_api_command(api_path, api_command, **kwargs)
        
        # Check if API result indicates an error
        if isinstance(result, str) and ("ERROR:" in result or "Failed" in result):
            raise Exception(f"API returned error: {result}")
        
        app_logger.debug("API execution successful")
        return result
        
    except Exception as api_error:
        app_logger.warning(f"API failed, falling back to SSH: {str(api_error)}")
        
        # Generate SSH command if not provided
        if ssh_command is None:
            ssh_command = _generate_ssh_command(api_path, api_command, **kwargs)
        
        try:
            # Fall back to SSH
            app_logger.debug(f"Executing SSH fallback: {ssh_command}")
            result = execute_mikrotik_command(ssh_command)
            app_logger.debug("SSH fallback successful")
            return result
            
        except Exception as ssh_error:
            app_logger.error(f"Both API and SSH failed. API: {str(api_error)}, SSH: {str(ssh_error)}")
            return f"ERROR: Both API and SSH failed. API error: {str(api_error)}, SSH error: {str(ssh_error)}"


def _generate_ssh_command(api_path: str, api_command: str, **kwargs) -> str:
    """
    Generate SSH command from API path and parameters.
    
    Args:
        api_path: API path (e.g., '/system/identity', '/ip/route')
        api_command: API command ('print', 'add', 'set', 'remove', etc.)
        **kwargs: Additional parameters
    
    Returns:
        Generated SSH command string
    """
    # Convert API path to SSH command
    ssh_path = api_path.replace('/', '/')
    
    # Handle different commands
    if api_command == "print":
        return f"{ssh_path} print"
    elif api_command == "add":
        params = []
        for key, value in kwargs.items():
            if value is not None:
                if isinstance(value, bool):
                    params.append(f"{key}={str(value).lower()}")
                elif isinstance(value, str):
                    params.append(f'{key}="{value}"')
                else:
                    params.append(f"{key}={value}")
        return f"{ssh_path} add {' '.join(params)}"
    elif api_command == "set":
        # Extract ID from kwargs if present
        item_id = kwargs.get('id', kwargs.get('.id', '*1'))
        params = []
        for key, value in kwargs.items():
            if key not in ['id', '.id'] and value is not None:
                if isinstance(value, bool):
                    params.append(f"{key}={str(value).lower()}")
                elif isinstance(value, str):
                    params.append(f'{key}="{value}"')
                else:
                    params.append(f"{key}={value}")
        return f"{ssh_path} set {item_id} {' '.join(params)}"
    elif api_command == "remove":
        item_id = kwargs.get('id', kwargs.get('.id', '*1'))
        return f"{ssh_path} remove {item_id}"
    else:
        # For other commands, try to construct a reasonable SSH command
        params = []
        for key, value in kwargs.items():
            if value is not None:
                if isinstance(value, str):
                    params.append(f'{key}="{value}"')
                else:
                    params.append(f"{key}={value}")
        return f"{ssh_path} {api_command} {' '.join(params)}"


def api_fallback_list(api_path: str, ssh_command: Optional[str] = None, **filters) -> str:
    """
    List resources using API first, fall back to SSH.
    
    Args:
        api_path: API path (e.g., '/system/identity', '/ip/route')
        ssh_command: SSH command to use as fallback
        **filters: Filter parameters
    
    Returns:
        List of resources as formatted string
    """
    return api_fallback_execute(api_path, "print", ssh_command, **filters)


def api_fallback_add(api_path: str, ssh_command: Optional[str] = None, **properties) -> str:
    """
    Add a resource using API first, fall back to SSH.
    
    Args:
        api_path: API path (e.g., '/ip/route', '/ip/firewall/filter')
        ssh_command: SSH command to use as fallback
        **properties: Resource properties
    
    Returns:
        Addition result as string
    """
    return api_fallback_execute(api_path, "add", ssh_command, **properties)


def api_fallback_set(api_path: str, item_id: str, ssh_command: Optional[str] = None, **properties) -> str:
    """
    Update a resource using API first, fall back to SSH.
    
    Args:
        api_path: API path (e.g., '/ip/route', '/ip/firewall/filter')
        item_id: ID of the item to update
        ssh_command: SSH command to use as fallback
        **properties: Updated properties
    
    Returns:
        Update result as string
    """
    return api_fallback_execute(api_path, "set", ssh_command, id=item_id, **properties)


def api_fallback_remove(api_path: str, item_id: str, ssh_command: Optional[str] = None) -> str:
    """
    Remove a resource using API first, fall back to SSH.
    
    Args:
        api_path: API path (e.g., '/ip/route', '/ip/firewall/filter')
        item_id: ID of the item to remove
        ssh_command: SSH command to use as fallback
    
    Returns:
        Removal result as string
    """
    return api_fallback_execute(api_path, "remove", ssh_command, id=item_id)


def api_fallback_get(api_path: str, item_id: str, ssh_command: Optional[str] = None) -> str:
    """
    Get a specific resource using API first, fall back to SSH.
    
    Args:
        api_path: API path (e.g., '/ip/route', '/ip/firewall/filter')
        item_id: ID of the item to get
        ssh_command: SSH command to use as fallback
    
    Returns:
        Resource details as string
    """
    return api_fallback_execute(api_path, "print", ssh_command, id=item_id)
