"""
MikroTik RouterOS API connector.
Provides reliable API-based communication with MikroTik devices.
"""

import os
from typing import Dict, Any, List, Optional
from routeros_api import connect
from .logger import app_logger
from .settings.configuration import mikrotik_config


class MikroTikApiConnector:
    """RouterOS API connector with error handling and connection management."""
    
    def __init__(self):
        self.api = None
        self.connected = False
    
    def connect(self) -> bool:
        """Connect to RouterOS API."""
        try:
            app_logger.info(f"Connecting to RouterOS API at {mikrotik_config['host']}")
            
            self.api = connect(
                mikrotik_config['host'],
                username=mikrotik_config['username'],
                password=mikrotik_config['password'],
                port=8728,  # Default API port
                plaintext_login=True
            )
            
            # Test connection
            identity = self.api.get_resource('/system/identity').get()
            self.connected = True
            app_logger.info("Successfully connected to RouterOS API")
            return True
            
        except Exception as e:
            app_logger.error(f"Failed to connect to RouterOS API: {str(e)}")
            self.connected = False
            return False
    
    def disconnect(self):
        """Disconnect from RouterOS API."""
        if self.api:
            try:
                # API connection closes automatically
                app_logger.info("Disconnected from RouterOS API")
            except Exception as e:
                app_logger.warning(f"Error disconnecting from API: {str(e)}")
            finally:
                self.api = None
                self.connected = False
    
    def execute_command(self, path: str, command: str = "print", **kwargs) -> List[Dict[str, Any]]:
        """
        Execute a RouterOS API command.
        
        Args:
            path: API path (e.g., '/ip/route', '/system/identity')
            command: API command ('print', 'add', 'set', 'remove', etc.)
            **kwargs: Additional parameters
        
        Returns:
            List of result dictionaries
        """
        if not self.connected:
            if not self.connect():
                raise Exception("Not connected to RouterOS API")
        
        try:
            app_logger.debug(f"API Command: {path}/{command} {kwargs}")
            
            # Get the resource
            resource = self.api.get_resource(path)
            
            # Execute the command
            if command == "print":
                result = resource.get()
            elif command == "add":
                result = resource.add(**kwargs)
            elif command == "set":
                result = resource.set(**kwargs)
            elif command == "remove":
                result = resource.remove(**kwargs)
            else:
                # For other commands, use call method
                result = resource.call(command, **kwargs)
            
            app_logger.debug(f"API Result: {result}")
            return result
            
        except Exception as e:
            app_logger.error(f"API command failed: {str(e)}")
            raise
    
    def execute_simple_command(self, path: str, command: str = "print", **kwargs) -> str:
        """
        Execute a simple API command and return formatted string result.
        """
        try:
            result = self.execute_command(path, command, **kwargs)
            
            if not result:
                return "No results returned"
            
            # Format the result for display
            if isinstance(result, list):
                if len(result) == 1:
                    # Single result
                    return self._format_single_result(result[0])
                else:
                    # Multiple results
                    return self._format_multiple_results(result)
            else:
                return str(result)
                
        except Exception as e:
            return f"ERROR: {str(e)}"
    
    def _format_single_result(self, result: Dict[str, Any]) -> str:
        """Format a single result dictionary."""
        lines = []
        for key, value in result.items():
            lines.append(f"{key}: {value}")
        return "\n".join(lines)
    
    def _format_multiple_results(self, results: List[Dict[str, Any]]) -> str:
        """Format multiple result dictionaries."""
        if not results:
            return "No results"
        
        lines = []
        lines.append(f"Found {len(results)} results:")
        lines.append("")
        
        for i, result in enumerate(results, 1):
            lines.append(f"Result {i}:")
            for key, value in result.items():
                lines.append(f"  {key}: {value}")
            lines.append("")
        
        return "\n".join(lines)


# Global API connector instance
_api_connector: Optional[MikroTikApiConnector] = None


def get_api_connector() -> MikroTikApiConnector:
    """Get the global API connector instance."""
    global _api_connector
    if _api_connector is None:
        _api_connector = MikroTikApiConnector()
    return _api_connector


def execute_api_command(path: str, command: str = "print", **kwargs) -> str:
    """
    Execute a RouterOS API command using the global connector.
    
    Args:
        path: API path (e.g., '/ip/route', '/system/identity')
        command: API command ('print', 'add', 'set', 'remove', etc.)
        **kwargs: Additional parameters
    
    Returns:
        Formatted string result
    """
    connector = get_api_connector()
    return connector.execute_simple_command(path, command, **kwargs)


def cleanup_api_connections():
    """Cleanup API connections (call on shutdown)."""
    global _api_connector
    if _api_connector:
        _api_connector.disconnect()
        _api_connector = None
