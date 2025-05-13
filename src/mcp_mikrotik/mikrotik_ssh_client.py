import paramiko
from .logger import app_logger

class MikroTikSSHClient:
    """SSH client for MikroTik devices."""
    
    def __init__(self, host: str, username: str, password: str, port: int = 22):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.client = None
        self.channel = None
    
    def connect(self):
        """Establish SSH connection to MikroTik device."""
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(
                hostname=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                look_for_keys=False,
                allow_agent=False
            )
            # Use the exec_command method instead of shell for MikroTik
            return True
        except Exception as e:
            app_logger.error(f"Failed to connect to MikroTik: {e}")
            return False
    
    def execute_command(self, command: str) -> str:
        """Execute a command on MikroTik device using exec_command."""
        if not self.client:
            raise Exception("Not connected to MikroTik device")
        
        try:
            # Use exec_command for better compatibility with MikroTik
            stdin, stdout, stderr = self.client.exec_command(command)
            
            # Read the output
            output = stdout.read().decode('utf-8')
            error = stderr.read().decode('utf-8')
            
            if error and not output:
                return error
            
            return output
        except Exception as e:
            app_logger.error(f"Error executing command: {e}")
            raise
    
    def disconnect(self):
        """Close SSH connection."""
        if self.client:
            self.client.close()
