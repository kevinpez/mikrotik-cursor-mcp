"""
MikroTik connection manager with pooling and health checks.
Provides efficient connection reuse and automatic reconnection.
"""
import time
import threading
from typing import Optional, Dict, Any
from contextlib import contextmanager
import paramiko
import socket
from .logger import app_logger
from .settings.configuration import mikrotik_config


class MikroTikConnectionManager:
    """
    Manages SSH connections to MikroTik devices with pooling and health checks.
    """
    
    def __init__(self, max_idle_time: int = 300, health_check_interval: int = 60):
        """
        Initialize connection manager.
        
        Args:
            max_idle_time: Maximum idle time before closing connection (seconds)
            health_check_interval: How often to check connection health (seconds)
        """
        self._connection: Optional[paramiko.SSHClient] = None
        self._last_used: Optional[float] = None
        self._lock = threading.Lock()
        self._max_idle_time = max_idle_time
        self._health_check_interval = health_check_interval
        self._last_health_check = 0
        self._is_healthy = False
        
    def _create_connection(self) -> paramiko.SSHClient:
        """Create a new SSH connection."""
        app_logger.debug("Creating new SSH connection to MikroTik")
        
        client = paramiko.SSHClient()
        # Host key policy
        if mikrotik_config.get("strict_host_key_checking"):
            client.set_missing_host_key_policy(paramiko.RejectPolicy())
            if mikrotik_config.get("known_hosts_path"):
                try:
                    client.load_host_keys(mikrotik_config["known_hosts_path"])
                except Exception as e:
                    app_logger.warning(f"Failed to load known hosts: {e}")
        else:
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        try:
            # Prepare auth options
            ssh_key = mikrotik_config.get("ssh_key_path")
            ssh_key_pass = mikrotik_config.get("ssh_key_passphrase")
            use_key = bool(ssh_key) and not mikrotik_config.get("password")

            client.connect(
                hostname=mikrotik_config["host"],
                port=mikrotik_config["port"],
                username=mikrotik_config["username"],
                password=mikrotik_config.get("password") if not use_key else None,
                key_filename=ssh_key if use_key else None,
                passphrase=ssh_key_pass if use_key and ssh_key_pass else None,
                look_for_keys=not use_key,
                allow_agent=not use_key,
                timeout=mikrotik_config.get("connect_timeout", 10)
            )
            # Enable TCP keepalive on transport
            try:
                transport = client.get_transport()
                if transport:
                    transport.set_keepalive(30)
            except Exception:
                pass
            app_logger.info(f"Successfully connected to {mikrotik_config['host']}")
            return client
        except paramiko.AuthenticationException:
            app_logger.error("Authentication failed - check credentials")
            raise
        except paramiko.SSHException as e:
            app_logger.error(f"SSH error: {str(e)}")
            raise
        except (socket.timeout, TimeoutError):
            app_logger.error("Connection timeout - check network connectivity")
            raise
        except Exception as e:
            app_logger.error(f"Unexpected connection error: {str(e)}")
            raise
    
    def _is_stale(self) -> bool:
        """Check if connection is stale and should be recreated."""
        if not self._connection or not self._last_used:
            return True
        
        idle_time = time.time() - self._last_used
        if idle_time > self._max_idle_time:
            app_logger.debug(f"Connection stale after {idle_time:.1f}s idle time")
            return True
        
        # Check if connection is still alive
        if not self._connection.get_transport() or not self._connection.get_transport().is_active():
            app_logger.debug("SSH transport is not active")
            return True
        
        return False
    
    def _health_check(self) -> bool:
        """Perform a health check on the connection."""
        if not self._connection:
            return False
        
        try:
            # Simple command to test connection
            stdin, stdout, stderr = self._connection.exec_command('/system identity print', timeout=5)
            result = stdout.read().decode('utf-8')
            if result and ("name=" in result or "name:" in result):
                app_logger.debug("Connection health check passed")
                return True
            else:
                app_logger.warning("Connection health check failed - no valid response")
                return False
        except Exception as e:
            app_logger.warning(f"Connection health check failed: {str(e)}")
            return False
    
    def get_connection(self) -> paramiko.SSHClient:
        """Get a healthy SSH connection, creating one if necessary."""
        with self._lock:
            current_time = time.time()
            
            # Check if we need a health check
            if (self._connection and 
                current_time - self._last_health_check > self._health_check_interval):
                if not self._health_check():
                    app_logger.info("Health check failed, recreating connection")
                    self._close_connection()
                self._last_health_check = current_time
            
            # Create new connection if needed
            if self._is_stale():
                self._close_connection()
                self._connection = self._create_connection()
                self._is_healthy = True
                self._last_health_check = current_time
            
            self._last_used = current_time
            return self._connection
    
    def _close_connection(self):
        """Close the current connection."""
        if self._connection:
            try:
                self._connection.close()
                app_logger.debug("SSH connection closed")
            except Exception as e:
                app_logger.warning(f"Error closing connection: {str(e)}")
            finally:
                self._connection = None
                self._is_healthy = False
    
    def close(self):
        """Close the connection manager and cleanup resources."""
        with self._lock:
            self._close_connection()
    
    @contextmanager
    def get_connection_context(self):
        """Context manager for getting a connection."""
        connection = self.get_connection()
        try:
            yield connection
        except Exception as e:
            app_logger.error(f"Connection error: {str(e)}")
            # Mark connection as unhealthy for next health check
            self._is_healthy = False
            raise


# Global connection manager instance
_connection_manager: Optional[MikroTikConnectionManager] = None


def get_connection_manager() -> MikroTikConnectionManager:
    """Get the global connection manager instance."""
    global _connection_manager
    if _connection_manager is None:
        _connection_manager = MikroTikConnectionManager()
    return _connection_manager


def cleanup_connections():
    """Cleanup all connections (call on shutdown)."""
    global _connection_manager
    if _connection_manager:
        _connection_manager.close()
        _connection_manager = None
