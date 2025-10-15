"""
Site Connector - Manages connections to multiple MikroTik sites
"""
import yaml
from pathlib import Path
from datetime import datetime
import sys

# Import MCP modules
try:
    from mcp_mikrotik.mikrotik_ssh_client import MikroTikSSHClient
    from mcp_mikrotik.connector import execute_mikrotik_command
    from mcp_mikrotik.connection_manager import get_connection_manager
except ImportError:
    print("Error: MCP modules not found. Make sure you're running from the correct directory.")
    sys.exit(1)


class SiteConnector:
    """Manages connections and configurations for multiple sites."""
    
    def __init__(self, config_file='sites.yaml'):
        """
        Initialize site connector.
        
        Args:
            config_file: Path to sites configuration file
        """
        self.config_file = Path(config_file)
        self.sites = self._load_config()
        self.connections = {}  # Cache of active connections
    
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
            os.environ['MIKROTIK_HOST'] = site['host']
            os.environ['MIKROTIK_USERNAME'] = site['username']
            os.environ['MIKROTIK_PASSWORD'] = site.get('password', '')
            os.environ['MIKROTIK_PORT'] = str(site.get('ssh_port', 22))
            
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
            os.environ['MIKROTIK_HOST'] = host
            os.environ['MIKROTIK_USERNAME'] = username
            os.environ['MIKROTIK_PASSWORD'] = password
            os.environ['MIKROTIK_PORT'] = str(port)
            
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
            os.environ['MIKROTIK_HOST'] = site['host']
            os.environ['MIKROTIK_USERNAME'] = site['username']
            os.environ['MIKROTIK_PASSWORD'] = site.get('password', '')
            os.environ['MIKROTIK_PORT'] = str(site.get('ssh_port', 22))
            
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

