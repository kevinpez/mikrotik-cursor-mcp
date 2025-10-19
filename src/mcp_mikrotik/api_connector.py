"""
MikroTik RouterOS API connector.
Provides reliable API-based communication with MikroTik devices.
Enhanced with retry logic, caching, and performance metrics.
"""

import os
import time
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from routeros_api import connect
from .logger import app_logger
from .settings.configuration import mikrotik_config


class MikroTikApiConnector:
    """RouterOS API connector with error handling and connection management."""
    
    def __init__(self):
        self.api = None
        self.connected = False
        self.retry_attempts = 3
        self.retry_delay = 1  # seconds
        self.cache = {}
        self.cache_ttl = 300  # 5 minutes
        self.metrics = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'total_retry_attempts': 0,
            'api_response_times': []
        }
    
    def connect(self, retry: bool = True) -> bool:
        """Connect to RouterOS API with retry logic."""
        attempts = self.retry_attempts if retry else 1
        
        for attempt in range(1, attempts + 1):
            try:
                if attempt > 1:
                    delay = self.retry_delay * (2 ** (attempt - 2))  # Exponential backoff
                    app_logger.info(f"Retrying connection (attempt {attempt}/{attempts}) after {delay}s delay")
                    time.sleep(delay)
                    self.metrics['total_retry_attempts'] += 1
                
                app_logger.info(f"Connecting to RouterOS API at {mikrotik_config['host']}")
                
                # Get configuration values with defaults
                api_port = mikrotik_config.get('api_port', 8728)
                api_timeout = mikrotik_config.get('api_timeout', 30)
                
                self.api = connect(
                    mikrotik_config['host'],
                    username=mikrotik_config['username'],
                    password=mikrotik_config['password'],
                    port=api_port,
                    plaintext_login=True
                )
                
                # Test connection
                identity = self.api.get_resource('/system/identity').get()
                self.connected = True
                app_logger.info(f"Successfully connected to RouterOS API on attempt {attempt}")
                return True
                
            except Exception as e:
                app_logger.warning(f"Connection attempt {attempt} failed: {str(e)}")
                if attempt == attempts:
                    app_logger.error(f"Failed to connect to RouterOS API after {attempts} attempts")
                    self.connected = False
                    return False
        
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
    
    def execute_command(self, path: str, command: str = "print", use_cache: bool = True, **kwargs) -> List[Dict[str, Any]]:
        """
        Execute a RouterOS API command with caching and metrics.
        
        Args:
            path: API path (e.g., '/ip/route', '/system/identity')
            command: API command ('print', 'add', 'set', 'remove', etc.)
            use_cache: Whether to use caching for read operations
            **kwargs: Additional parameters
        
        Returns:
            List of result dictionaries
        """
        start_time = time.time()
        self.metrics['total_requests'] += 1
        
        # Check cache for read-only operations
        if command == "print" and use_cache and not kwargs:
            cache_key = f"{path}:{command}"
            cached_result = self._get_from_cache(cache_key)
            if cached_result is not None:
                self.metrics['cache_hits'] += 1
                app_logger.debug(f"Cache hit for {cache_key}")
                return cached_result
            self.metrics['cache_misses'] += 1
        
        # Ensure connection with automatic retry
        if not self.connected:
            if not self.connect(retry=True):
                self.metrics['failed_requests'] += 1
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
            
            # Cache read-only results
            if command == "print" and use_cache and not kwargs:
                cache_key = f"{path}:{command}"
                self._add_to_cache(cache_key, result)
            
            # Track metrics
            execution_time = time.time() - start_time
            self.metrics['api_response_times'].append(execution_time)
            self.metrics['successful_requests'] += 1
            
            app_logger.debug(f"API Result: {result} (took {execution_time:.2f}s)")
            return result
            
        except Exception as e:
            self.metrics['failed_requests'] += 1
            app_logger.error(f"API command failed: {str(e)}")
            
            # Try to reconnect if connection was lost
            if "connection" in str(e).lower():
                app_logger.info("Connection lost, attempting to reconnect...")
                self.connected = False
                if self.connect(retry=True):
                    app_logger.info("Reconnected successfully, retrying command...")
                    return self.execute_command(path, command, use_cache=False, **kwargs)
            
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
    
    def _get_from_cache(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired."""
        if key in self.cache:
            cached_data, timestamp = self.cache[key]
            if datetime.now() - timestamp < timedelta(seconds=self.cache_ttl):
                return cached_data
            else:
                # Remove expired entry
                del self.cache[key]
        return None
    
    def _add_to_cache(self, key: str, value: Any):
        """Add value to cache with timestamp."""
        self.cache[key] = (value, datetime.now())
    
    def clear_cache(self):
        """Clear all cached data."""
        self.cache.clear()
        app_logger.info("API cache cleared")
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get performance metrics."""
        metrics = self.metrics.copy()
        
        # Calculate average response time
        if metrics['api_response_times']:
            metrics['avg_response_time'] = sum(metrics['api_response_times']) / len(metrics['api_response_times'])
            metrics['min_response_time'] = min(metrics['api_response_times'])
            metrics['max_response_time'] = max(metrics['api_response_times'])
        else:
            metrics['avg_response_time'] = 0
            metrics['min_response_time'] = 0
            metrics['max_response_time'] = 0
        
        # Calculate success rate
        if metrics['total_requests'] > 0:
            metrics['success_rate'] = (metrics['successful_requests'] / metrics['total_requests']) * 100
            metrics['cache_hit_rate'] = (metrics['cache_hits'] / (metrics['cache_hits'] + metrics['cache_misses'])) * 100 if (metrics['cache_hits'] + metrics['cache_misses']) > 0 else 0
        else:
            metrics['success_rate'] = 0
            metrics['cache_hit_rate'] = 0
        
        # Remove raw response times array (too verbose)
        metrics['response_time_samples'] = len(metrics['api_response_times'])
        del metrics['api_response_times']
        
        return metrics
    
    def reset_metrics(self):
        """Reset performance metrics."""
        self.metrics = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'total_retry_attempts': 0,
            'api_response_times': []
        }
        app_logger.info("API metrics reset")


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


def get_api_metrics() -> Dict[str, Any]:
    """Get API performance metrics."""
    connector = get_api_connector()
    return connector.get_metrics()


def clear_api_cache():
    """Clear API response cache."""
    connector = get_api_connector()
    connector.clear_cache()


def reset_api_metrics():
    """Reset API performance metrics."""
    connector = get_api_connector()
    connector.reset_metrics()
