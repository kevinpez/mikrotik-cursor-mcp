"""
Bulk Operations - Execute operations across multiple sites
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from .site_connector import SiteConnector


class BulkOperations:
    """Handle bulk operations across multiple sites."""
    
    def __init__(self, max_workers=5):
        """
        Initialize bulk operations handler.
        
        Args:
            max_workers: Maximum concurrent operations
        """
        self.connector = SiteConnector()
        self.max_workers = max_workers
    
    def execute_all(self, command):
        """
        Execute command on all sites.
        
        Args:
            command: RouterOS command to execute
            
        Returns:
            dict: Results from all sites
        """
        sites = self.connector.get_sites()
        return self.execute_sites(command, list(sites.keys()))
    
    def execute_sites(self, command, site_ids):
        """
        Execute command on specific sites.
        
        Args:
            command: RouterOS command to execute
            site_ids: List of site IDs
            
        Returns:
            dict: Results from specified sites
        """
        results = {}
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_site = {
                executor.submit(self.connector.execute_command, site_id, command): site_id
                for site_id in site_ids
            }
            
            # Collect results
            for future in as_completed(future_to_site):
                site_id = future_to_site[future]
                try:
                    results[site_id] = future.result()
                except Exception as e:
                    results[site_id] = {
                        'success': False,
                        'error': str(e)
                    }
        
        return results
    
    def execute_group(self, command, group_name):
        """
        Execute command on a site group.
        
        Args:
            command: RouterOS command to execute
            group_name: Name of site group
            
        Returns:
            dict: Results from group sites
        """
        groups = self.connector.get_site_groups()
        
        if group_name not in groups:
            return {
                'error': f"Group '{group_name}' not found",
                'available_groups': list(groups.keys())
            }
        
        site_ids = groups[group_name]
        return self.execute_sites(command, site_ids)
    
    def execute_by_tag(self, command, tag):
        """
        Execute command on all sites with a specific tag.
        
        Args:
            command: RouterOS command to execute
            tag: Site tag
            
        Returns:
            dict: Results from tagged sites
        """
        sites = self.connector.get_sites_by_tag(tag)
        
        if not sites:
            return {
                'error': f"No sites found with tag '{tag}'"
            }
        
        return self.execute_sites(command, list(sites.keys()))
    
    def deploy_firewall_rule(self, rule_config, site_ids=None):
        """
        Deploy firewall rule to multiple sites.
        
        Args:
            rule_config: Firewall rule configuration
            site_ids: List of site IDs or None for all
            
        Returns:
            dict: Deployment results
        """
        # Build firewall command
        cmd = self._build_firewall_command(rule_config)
        
        if site_ids:
            return self.execute_sites(cmd, site_ids)
        else:
            return self.execute_all(cmd)
    
    def deploy_user(self, user_config, site_ids=None):
        """
        Deploy user configuration to multiple sites.
        
        Args:
            user_config: User configuration
            site_ids: List of site IDs or None for all
            
        Returns:
            dict: Deployment results
        """
        name = user_config.get('name')
        group = user_config.get('group', 'full')
        password = user_config.get('password')
        
        cmd = f'/user add name={name} group={group} password={password}'
        
        if site_ids:
            return self.execute_sites(cmd, site_ids)
        else:
            return self.execute_all(cmd)
    
    def update_user_password(self, username, password, site_ids=None):
        """
        Update user password across sites.
        
        Args:
            username: Username to update
            password: New password
            site_ids: List of site IDs or None for all
            
        Returns:
            dict: Update results
        """
        cmd = f'/user set [find name={username}] password={password}'
        
        if site_ids:
            return self.execute_sites(cmd, site_ids)
        else:
            return self.execute_all(cmd)
    
    def get_configuration(self, path, site_ids=None):
        """
        Get configuration from multiple sites.
        
        Args:
            path: Configuration path (e.g., /ip address)
            site_ids: List of site IDs or None for all
            
        Returns:
            dict: Configuration from each site
        """
        cmd = f'{path} print'
        
        if site_ids:
            return self.execute_sites(cmd, site_ids)
        else:
            return self.execute_all(cmd)
    
    def compare_configurations(self, path, site_ids):
        """
        Compare configurations across sites.
        
        Args:
            path: Configuration path
            site_ids: List of site IDs to compare
            
        Returns:
            dict: Comparison results
        """
        configs = self.get_configuration(path, site_ids)
        
        # Simple comparison - check if all outputs are identical
        outputs = [c['output'] for c in configs.values() if c.get('success')]
        
        if not outputs:
            return {'error': 'No successful outputs to compare'}
        
        all_same = all(output == outputs[0] for output in outputs)
        
        return {
            'identical': all_same,
            'sites_compared': len(site_ids),
            'configs': configs
        }
    
    def _build_firewall_command(self, rule_config):
        """Build firewall rule command from configuration."""
        chain = rule_config.get('chain', 'input')
        action = rule_config.get('action', 'accept')
        
        cmd = f'/ip firewall filter add chain={chain} action={action}'
        
        # Add optional parameters
        if 'src-address' in rule_config:
            cmd += f' src-address={rule_config["src-address"]}'
        if 'dst-address' in rule_config:
            cmd += f' dst-address={rule_config["dst-address"]}'
        if 'protocol' in rule_config:
            cmd += f' protocol={rule_config["protocol"]}'
        if 'dst-port' in rule_config:
            cmd += f' dst-port={rule_config["dst-port"]}'
        if 'comment' in rule_config:
            cmd += f' comment="{rule_config["comment"]}"'
        
        return cmd
    
    def synchronize_users(self, template_site_id, target_site_ids):
        """
        Synchronize users from template site to target sites.
        
        Args:
            template_site_id: Source site for users
            target_site_ids: Sites to sync to
            
        Returns:
            dict: Synchronization results
        """
        # Get users from template site
        users_result = self.connector.execute_command(template_site_id, '/user print')
        
        if not users_result['success']:
            return {
                'error': f"Failed to get users from template: {users_result.get('error')}"
            }
        
        # Parse users (simplified - in production would parse properly)
        # For now, just return the command that would be executed
        
        return {
            'template_site': template_site_id,
            'target_sites': target_site_ids,
            'note': 'User synchronization prepared. Would sync users from template to targets.'
        }

