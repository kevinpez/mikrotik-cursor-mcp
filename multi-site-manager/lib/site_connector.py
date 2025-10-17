"""
Enhanced Site Connector - Manages connections to multiple MikroTik sites
with concurrency controls, circuit breakers, and failure isolation.
"""
import yaml
import time
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import sys

# Import MCP modules
try:
    from mcp_mikrotik.mikrotik_ssh_client import MikroTikSSHClient
    from mcp_mikrotik.connector import execute_mikrotik_command
    from mcp_mikrotik.connection_manager import get_connection_manager
    from .concurrency_manager import ConcurrencyManager, get_concurrency_manager
except ImportError:
    print("Error: MCP modules not found. Make sure you're running from the correct directory.")
    sys.exit(1)


class SiteConnector:
    """Enhanced site connector with concurrency controls and failure isolation."""
    
    def __init__(self, config_file='sites.yaml', max_concurrent: int = 10):
        """
        Initialize site connector.
        
        Args:
            config_file: Path to sites configuration file
            max_concurrent: Maximum concurrent operations
        """
        self.config_file = Path(config_file)
        self.sites = self._load_config()
        self.connections = {}  # Cache of active connections
        self.concurrency_manager = get_concurrency_manager()
        self.logger = logging.getLogger(__name__)
    
    def _load_config(self):
        """Load sites configuration from YAML file."""
        if not self.config_file.exists():
            raise FileNotFoundError(
                f"Configuration file '{self.config_file}' not found. "
                "Copy sites.yaml.example to sites.yaml and configure your sites."
            )
        
        with open(self.config_file, 'r') as f:
            config = yaml.safe_load(f)
        
        return config.get('sites', {})
    
    def _save_config(self):
        """Save sites configuration to YAML file."""
        config = {'sites': self.sites}
        with open(self.config_file, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
    
    def get_sites(self, site_id=None):
        """
        Get site(s) configuration.
        
        Args:
            site_id: Specific site ID, or None for all sites
            
        Returns:
            dict: Site configuration(s)
        """
        if site_id:
            return {site_id: self.sites.get(site_id)} if site_id in self.sites else {}
        return self.sites
    
    def get_site(self, site_id):
        """Get specific site configuration."""
        return self.sites.get(site_id)
    
    def add_site(self, site_id, site_data):
        """
        Add a new site to configuration.
        
        Args:
            site_id: Unique site identifier
            site_data: Site configuration dictionary
        """
        self.sites[site_id] = site_data
        self._save_config()
    
    def remove_site(self, site_id):
        """Remove a site from configuration."""
        if site_id in self.sites:
            del self.sites[site_id]
            self._save_config()
    
    def update_site(self, site_id, updates):
        """Update site configuration."""
        if site_id in self.sites:
            self.sites[site_id].update(updates)
            self._save_config()
    
    def check_connection(self, site_id):
        """
        Check if connection to site is possible.
        
        Args:
            site_id: Site to check
            
        Returns:
            dict: Connection status with details
        """
        site = self.get_site(site_id)
        if not site:
            return {
                'connected': False,
                'error': f"Site '{site_id}' not found"
            }
        
        try:
            # Try to connect and get identity
            import os
            import importlib
            from mcp_mikrotik.settings import configuration
            
            # Set environment variables
            os.environ['MIKROTIK_HOST'] = site['host']
            os.environ['MIKROTIK_USERNAME'] = site['username']
            os.environ['MIKROTIK_PASSWORD'] = site.get('password', '')
            os.environ['MIKROTIK_PORT'] = str(site.get('ssh_port', 22))
            
            # Reload configuration to pick up new environment variables
            importlib.reload(configuration)
            
            # Use MCP connector
            result = execute_mikrotik_command('/system identity print')
            
            return {
                'connected': True,
                'last_check': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'details': result.strip()
            }
        
        except Exception as e:
            return {
                'connected': False,
                'error': str(e),
                'last_check': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
    
    def test_new_site(self, host, username, password, port=22):
        """
        Test connection to a new site before adding it.
        
        Args:
            host: Router IP/hostname
            username: SSH username
            password: SSH password
            port: SSH port
            
        Returns:
            dict: Test results
        """
        try:
            import os
            import importlib
            from mcp_mikrotik.settings import configuration
            
            # Set environment variables
            os.environ['MIKROTIK_HOST'] = host
            os.environ['MIKROTIK_USERNAME'] = username
            os.environ['MIKROTIK_PASSWORD'] = password
            os.environ['MIKROTIK_PORT'] = str(port)
            
            # Reload configuration to pick up new environment variables
            importlib.reload(configuration)
            
            # Try to connect
            result = execute_mikrotik_command('/system identity print')
            
            return {
                'success': True,
                'identity': result.strip()
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def execute_command(self, site_id, command):
        """
        Execute command on a specific site.
        
        Args:
            site_id: Site to execute on
            command: RouterOS command to execute
            
        Returns:
            dict: Execution results
        """
        site = self.get_site(site_id)
        if not site:
            return {
                'success': False,
                'error': f"Site '{site_id}' not found"
            }
        
        try:
            # Set environment for this site
            import os
            import importlib
            from mcp_mikrotik.settings import configuration
            
            # Set environment variables
            os.environ['MIKROTIK_HOST'] = site['host']
            os.environ['MIKROTIK_USERNAME'] = site['username']
            os.environ['MIKROTIK_PASSWORD'] = site.get('password', '')
            os.environ['MIKROTIK_PORT'] = str(site.get('ssh_port', 22))
            
            # Reload configuration to pick up new environment variables
            importlib.reload(configuration)
            
            # Execute command
            result = execute_mikrotik_command(command)
            
            return {
                'success': True,
                'output': result,
                'site_id': site_id,
                'timestamp': datetime.now().isoformat()
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'site_id': site_id,
                'timestamp': datetime.now().isoformat()
            }
    
    def get_site_groups(self):
        """Get defined site groups from config."""
        with open(self.config_file, 'r') as f:
            config = yaml.safe_load(f)
        return config.get('groups', {})
    
    def get_sites_by_tag(self, tag):
        """Get all sites with a specific tag."""
        return {
            site_id: site_data
            for site_id, site_data in self.sites.items()
            if tag in site_data.get('tags', [])
        }
    
    def get_sites_by_priority(self, priority):
        """Get all sites with a specific priority."""
        return {
            site_id: site_data
            for site_id, site_data in self.sites.items()
            if site_data.get('priority') == priority
        }
    
    def execute_bulk_commands(self, commands: List[Tuple[str, str]], 
                            max_concurrent: int = None) -> Dict[str, Any]:
        """
        Execute commands across multiple sites with concurrency controls.
        
        Args:
            commands: List of (site_id, command) tuples
            max_concurrent: Maximum concurrent operations
            
        Returns:
            Dictionary with results per site
        """
        operations = []
        
        for site_id, command in commands:
            def create_operation(site_id=site_id, command=command):
                return self._execute_single_command(site_id, command)
            
            operations.append((site_id, create_operation))
        
        return self.concurrency_manager.execute_bulk_operations(operations, max_concurrent)
    
    def _execute_single_command(self, site_id: str, command: str) -> Any:
        """Execute a single command on a site (for use with concurrency manager)."""
        site = self.get_site(site_id)
        if not site:
            raise ValueError(f"Site '{site_id}' not found")
        
        # Set environment for this site
        import os
        import importlib
        from mcp_mikrotik.settings import configuration
        
        # Set environment variables
        os.environ['MIKROTIK_HOST'] = site['host']
        os.environ['MIKROTIK_USERNAME'] = site['username']
        os.environ['MIKROTIK_PASSWORD'] = site.get('password', '')
        os.environ['MIKROTIK_PORT'] = str(site.get('ssh_port', 22))
        
        # Reload configuration to pick up new environment variables
        importlib.reload(configuration)
        
        # Execute command
        return execute_mikrotik_command(command)
    
    def health_check_all_sites(self) -> Dict[str, Dict[str, Any]]:
        """
        Perform health check on all sites concurrently.
        
        Returns:
            Dictionary with health status per site
        """
        commands = [(site_id, '/system resource print') for site_id in self.sites.keys()]
        results = self.execute_bulk_commands(commands)
        
        health_status = {}
        for site_id, result in results.items():
            if result['success']:
                # Parse resource information
                resource_info = self._parse_resource_output(result['result'])
                health_status[site_id] = {
                    'status': 'healthy',
                    'last_check': datetime.now().isoformat(),
                    'resources': resource_info
                }
            else:
                health_status[site_id] = {
                    'status': 'unhealthy',
                    'last_check': datetime.now().isoformat(),
                    'error': result['result']
                }
        
        return health_status
    
    def _parse_resource_output(self, output: str) -> Dict[str, Any]:
        """Parse RouterOS resource output into structured data."""
        resources = {}
        lines = output.strip().split('\n')
        
        for line in lines:
            if '=' in line:
                try:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Convert numeric values
                    if value.isdigit():
                        resources[key] = int(value)
                    elif value.replace('.', '').isdigit():
                        resources[key] = float(value)
                    else:
                        resources[key] = value
                except ValueError:
                    continue
        
        return resources
    
    def get_site_health(self, site_id: str) -> Dict[str, Any]:
        """Get detailed health information for a specific site."""
        return self.concurrency_manager.get_site_health(site_id)
    
    def get_all_sites_health(self) -> Dict[str, Dict[str, Any]]:
        """Get health information for all sites."""
        return self.concurrency_manager.get_all_sites_health()
    
    def get_concurrency_statistics(self) -> Dict[str, Any]:
        """Get concurrency manager statistics."""
        return self.concurrency_manager.get_statistics()
    
    def reset_site_circuit_breaker(self, site_id: str):
        """Reset circuit breaker for a specific site."""
        self.concurrency_manager.reset_circuit_breaker(site_id)
        self.logger.info(f"Circuit breaker reset for site: {site_id}")
    
    def reset_all_circuit_breakers(self):
        """Reset all circuit breakers."""
        self.concurrency_manager.reset_all_circuit_breakers()
        self.logger.info("All circuit breakers reset")
    
    def execute_with_retry(self, site_id: str, command: str, max_retries: int = 3) -> Tuple[bool, Any]:
        """
        Execute command with retry logic and circuit breaker.
        
        Args:
            site_id: Site to execute on
            command: RouterOS command
            max_retries: Maximum retry attempts
            
        Returns:
            Tuple of (success, result)
        """
        def operation():
            return self._execute_single_command(site_id, command)
        
        return self.concurrency_manager.execute_with_retry(site_id, operation, max_retries)
    
    def create_backup_all_sites(self, backup_name: str = None) -> Dict[str, Any]:
        """
        Create backups on all sites concurrently.
        
        Args:
            backup_name: Name for the backup (default: timestamp)
            
        Returns:
            Dictionary with backup results per site
        """
        if not backup_name:
            backup_name = f"bulk-backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        commands = [(site_id, f'/backup save name={backup_name}') for site_id in self.sites.keys()]
        return self.execute_bulk_commands(commands)
    
    def get_backups_all_sites(self) -> Dict[str, Any]:
        """Get backup information from all sites."""
        commands = [(site_id, '/backup print') for site_id in self.sites.keys()]
        return self.execute_bulk_commands(commands)
    
    def deploy_firewall_rule(self, rule_command: str, target_sites: List[str] = None) -> Dict[str, Any]:
        """
        Deploy a firewall rule to multiple sites.
        
        Args:
            rule_command: RouterOS firewall rule command
            target_sites: List of site IDs (default: all sites)
            
        Returns:
            Dictionary with deployment results
        """
        if target_sites is None:
            target_sites = list(self.sites.keys())
        
        commands = [(site_id, rule_command) for site_id in target_sites]
        return self.execute_bulk_commands(commands)
    
    def update_dns_servers(self, dns_servers: str, target_sites: List[str] = None) -> Dict[str, Any]:
        """
        Update DNS servers on multiple sites.
        
        Args:
            dns_servers: Comma-separated DNS server list
            target_sites: List of site IDs (default: all sites)
            
        Returns:
            Dictionary with update results
        """
        if target_sites is None:
            target_sites = list(self.sites.keys())
        
        command = f'/ip dns set servers={dns_servers}'
        commands = [(site_id, command) for site_id in target_sites]
        return self.execute_bulk_commands(commands)
    
    def shutdown(self):
        """Shutdown the site connector and cleanup resources."""
        self.concurrency_manager.shutdown()
        self.logger.info("Site connector shutdown complete")

