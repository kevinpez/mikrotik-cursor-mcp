import os
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

DEFAULT_MIKROTIK_HOST = "127.0.0.1"  
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
}
