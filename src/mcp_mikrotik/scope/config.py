import json
from typing import Optional

def mikrotik_config_set(host: Optional[str] = None, username: Optional[str] = None, 
                       password: Optional[str] = None, port: Optional[int] = None) -> str:
    """
    Updates MikroTik connection configuration.
    
    Args:
        host: MikroTik device IP/hostname
        username: SSH username
        password: SSH password
        port: SSH port
    
    Returns:
        Updated configuration summary
    """
    global mikrotik_config
    
    if host:
        mikrotik_config["host"] = host
    if username:
        mikrotik_config["username"] = username
    if password:
        mikrotik_config["password"] = password
    if port:
        mikrotik_config["port"] = port
    
    # Don't show password in the output
    safe_config = mikrotik_config.copy()
    safe_config["password"] = "***hidden***"
    
    return f"Configuration updated:\n{json.dumps(safe_config, indent=2)}"

def mikrotik_config_get() -> str:
    """
    Shows current MikroTik connection configuration.
    
    Returns:
        Current configuration (with password hidden)
    """
    # Don't show password in the output
    safe_config = mikrotik_config.copy()
    safe_config["password"] = "***hidden***"
    
    return f"Current configuration:\n{json.dumps(safe_config, indent=2)}"
