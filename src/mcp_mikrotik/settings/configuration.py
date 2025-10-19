import os
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

DEFAULT_MIKROTIK_HOST = "192.168.88.1"  
DEFAULT_MIKROTIK_USER = "admin"        
DEFAULT_MIKROTIK_PASS = ""    

mikrotik_config = {
    "host": os.getenv("MIKROTIK_HOST", DEFAULT_MIKROTIK_HOST),
    "username": os.getenv("MIKROTIK_USERNAME", DEFAULT_MIKROTIK_USER),
    "password": os.getenv("MIKROTIK_PASSWORD", DEFAULT_MIKROTIK_PASS),
    "port": int(os.getenv("MIKROTIK_PORT", "22")),
    # Optional SSH key authentication
    "ssh_key_path": os.getenv("MIKROTIK_SSH_KEY"),
    "ssh_key_passphrase": os.getenv("MIKROTIK_SSH_KEY_PASSPHRASE"),
    # Host key policy and known hosts
    "strict_host_key_checking": os.getenv("MIKROTIK_STRICT_HOST_KEY_CHECKING", "false").lower() == "true",
    "known_hosts_path": os.getenv("MIKROTIK_KNOWN_HOSTS"),
    # Timeouts (seconds)
    "connect_timeout": int(os.getenv("MIKROTIK_CONNECT_TIMEOUT", "10")),
    "command_timeout": int(os.getenv("MIKROTIK_CMD_TIMEOUT", "30")),
    # Safety settings
    "safety_mode": os.getenv("MIKROTIK_SAFETY_MODE", "true").lower() == "true",
}

def validate_config():
    """Validate the MikroTik configuration and return any issues."""
    issues = []
    
    # Check for missing credentials
    if not mikrotik_config.get("password") and not mikrotik_config.get("ssh_key_path"):
        issues.append("No authentication method configured. Set either MIKROTIK_PASSWORD or MIKROTIK_SSH_KEY")
    
    # Check for invalid port
    if not (1 <= mikrotik_config.get("port", 22) <= 65535):
        issues.append(f"Invalid port number: {mikrotik_config.get('port', 22)}")
    
    # Check for invalid timeouts
    if mikrotik_config.get("connect_timeout", 10) <= 0:
        issues.append(f"Invalid connect timeout: {mikrotik_config.get('connect_timeout', 10)}")
    
    if mikrotik_config.get("command_timeout", 30) <= 0:
        issues.append(f"Invalid command timeout: {mikrotik_config.get('command_timeout', 30)}")
    
    return issues

def get_config_summary():
    """Get a summary of the current configuration (without sensitive data)."""
    return {
        "host": mikrotik_config.get("host"),
        "username": mikrotik_config.get("username"),
        "port": mikrotik_config.get("port"),
        "authentication_method": "SSH Key" if mikrotik_config.get("ssh_key_path") else "Password" if mikrotik_config.get("password") else "None",
        "strict_host_key_checking": mikrotik_config.get("strict_host_key_checking"),
        "connect_timeout": mikrotik_config.get("connect_timeout"),
        "command_timeout": mikrotik_config.get("command_timeout"),
        "safety_mode": mikrotik_config.get("safety_mode"),
    }

def set_safety_mode(enabled: bool):
    """Set safety mode at runtime."""
    mikrotik_config["safety_mode"] = enabled
    return mikrotik_config["safety_mode"]

def get_safety_mode():
    """Get current safety mode status."""
    return mikrotik_config.get("safety_mode", True)