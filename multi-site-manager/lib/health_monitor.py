"""
Health Monitor - Monitors health and performance of sites
"""
from datetime import datetime
import re
from .site_connector import SiteConnector


class HealthMonitor:
    """Monitors health metrics for all sites."""
    
    def __init__(self):
        """Initialize health monitor."""
        self.connector = SiteConnector()
    
    def check_site(self, site_id):
        """
        Perform comprehensive health check on a site.
        
        Args:
            site_id: Site to check
            
        Returns:
            dict: Health metrics
        """
        site = self.connector.get_site(site_id)
        if not site:
            return {'error': f"Site '{site_id}' not found"}
        
        health_data = {
            'site_id': site_id,
            'timestamp': datetime.now().isoformat(),
            'checks_performed': []
        }
        
        # Check 1: System Resources
        try:
            resources = self._check_resources(site_id)
            health_data.update(resources)
            health_data['checks_performed'].append('resources')
        except Exception as e:
            health_data['resource_error'] = str(e)
        
        # Check 2: Interfaces
        try:
            interfaces = self._check_interfaces(site_id)
            health_data.update(interfaces)
            health_data['checks_performed'].append('interfaces')
        except Exception as e:
            health_data['interface_error'] = str(e)
        
        # Check 3: DHCP Leases
        try:
            dhcp = self._check_dhcp(site_id)
            health_data.update(dhcp)
            health_data['checks_performed'].append('dhcp')
        except Exception as e:
            health_data['dhcp_error'] = str(e)
        
        # Check 4: Firewall
        try:
            firewall = self._check_firewall(site_id)
            health_data.update(firewall)
            health_data['checks_performed'].append('firewall')
        except Exception as e:
            health_data['firewall_error'] = str(e)
        
        # Calculate overall health score
        health_data['health_score'] = self._calculate_health_score(health_data)
        
        return health_data
    
    def check_all_sites(self):
        """
        Check health of all sites.
        
        Returns:
            dict: Health data for all sites
        """
        results = {}
        sites = self.connector.get_sites()
        
        for site_id in sites.keys():
            results[site_id] = self.check_site(site_id)
        
        return results
    
    def _check_resources(self, site_id):
        """Check system resources (CPU, memory, uptime)."""
        result = self.connector.execute_command(site_id, '/system resource print')
        
        if not result['success']:
            raise Exception(result.get('error', 'Unknown error'))
        
        output = result['output']
        
        # Parse output
        data = {}
        
        # Extract uptime
        uptime_match = re.search(r'uptime:\s*(.+?)(?:\n|$)', output)
        if uptime_match:
            data['uptime'] = uptime_match.group(1).strip()
        
        # Extract CPU load
        cpu_match = re.search(r'cpu-load:\s*(\d+)%', output)
        if cpu_match:
            data['cpu_load'] = int(cpu_match.group(1))
        
        # Extract memory
        free_mem_match = re.search(r'free-memory:\s*([\d.]+)(\w+)', output)
        total_mem_match = re.search(r'total-memory:\s*([\d.]+)(\w+)', output)
        
        if free_mem_match and total_mem_match:
            free_mem = float(free_mem_match.group(1))
            total_mem = float(total_mem_match.group(1))
            
            # Convert to same units (assume MiB if unit matches)
            used_mem = total_mem - free_mem
            data['memory_free'] = f"{free_mem}{free_mem_match.group(2)}"
            data['memory_total'] = f"{total_mem}{total_mem_match.group(2)}"
            data['memory_used'] = f"{used_mem:.1f}{total_mem_match.group(2)}"
            data['memory_percent'] = int((used_mem / total_mem) * 100)
        
        # Extract version
        version_match = re.search(r'version:\s*(.+?)(?:\n|$)', output)
        if version_match:
            data['version'] = version_match.group(1).strip()
        
        return data
    
    def _check_interfaces(self, site_id):
        """Check interface status."""
        result = self.connector.execute_command(site_id, '/interface print')
        
        if not result['success']:
            raise Exception(result.get('error', 'Unknown error'))
        
        output = result['output']
        
        # Count interfaces
        lines = output.strip().split('\n')
        total_interfaces = 0
        running_interfaces = 0
        
        for line in lines:
            # Skip header lines
            if line.startswith('Flags:') or line.startswith('Columns:') or line.startswith('#'):
                continue
            
            # Check if line has interface data
            if line.strip():
                total_interfaces += 1
                if 'R' in line[:5]:  # R flag indicates RUNNING
                    running_interfaces += 1
        
        return {
            'total_interfaces': total_interfaces,
            'interfaces_up': running_interfaces,
            'interfaces_down': total_interfaces - running_interfaces
        }
    
    def _check_dhcp(self, site_id):
        """Check DHCP lease count."""
        result = self.connector.execute_command(site_id, '/ip dhcp-server lease print count-only')
        
        if not result['success']:
            raise Exception(result.get('error', 'Unknown error'))
        
        try:
            lease_count = int(result['output'].strip())
        except ValueError:
            lease_count = 0
        
        return {
            'dhcp_leases': lease_count
        }
    
    def _check_firewall(self, site_id):
        """Check firewall rule count."""
        result = self.connector.execute_command(site_id, '/ip firewall filter print count-only')
        
        if not result['success']:
            raise Exception(result.get('error', 'Unknown error'))
        
        try:
            rule_count = int(result['output'].strip())
        except ValueError:
            rule_count = 0
        
        return {
            'firewall_rules': rule_count
        }
    
    def _calculate_health_score(self, health_data):
        """
        Calculate overall health score (0-100).
        
        Args:
            health_data: Health metrics
            
        Returns:
            int: Health score
        """
        score = 100
        
        # Deduct points for high CPU
        cpu = health_data.get('cpu_load', 0)
        if isinstance(cpu, (int, float)) and cpu > 90:
            score -= 30
        elif isinstance(cpu, (int, float)) and cpu > 80:
            score -= 20
        elif isinstance(cpu, (int, float)) and cpu > 70:
            score -= 10
        
        # Deduct points for high memory
        mem = health_data.get('memory_percent', 0)
        if isinstance(mem, (int, float)) and mem > 95:
            score -= 30
        elif isinstance(mem, (int, float)) and mem > 90:
            score -= 20
        elif isinstance(mem, (int, float)) and mem > 80:
            score -= 10
        
        # Deduct points for interfaces down
        interfaces_down = health_data.get('interfaces_down', 0)
        if isinstance(interfaces_down, (int, float)) and interfaces_down > 0:
            score -= (interfaces_down * 5)
        
        # Bonus points for successful checks
        checks = len(health_data.get('checks_performed', []))
        if checks >= 4:
            score += 5
        
        # Ensure score is in valid range
        return max(0, min(100, score))
    
    def get_alerts(self, health_data):
        """
        Generate alerts based on health data.
        
        Args:
            health_data: Health metrics
            
        Returns:
            list: Alert messages
        """
        alerts = []
        
        # CPU alerts
        cpu = health_data.get('cpu_load', 0)
        if isinstance(cpu, (int, float)) and cpu > 90:
            alerts.append(f"CRITICAL: CPU load is {cpu}% (>90%)")
        elif isinstance(cpu, (int, float)) and cpu > 80:
            alerts.append(f"WARNING: CPU load is {cpu}% (>80%)")
        
        # Memory alerts
        mem = health_data.get('memory_percent', 0)
        if isinstance(mem, (int, float)) and mem > 95:
            alerts.append(f"CRITICAL: Memory usage is {mem}% (>95%)")
        elif isinstance(mem, (int, float)) and mem > 90:
            alerts.append(f"WARNING: Memory usage is {mem}% (>90%)")
        
        # Interface alerts
        interfaces_down = health_data.get('interfaces_down', 0)
        if isinstance(interfaces_down, (int, float)) and interfaces_down > 0:
            alerts.append(f"WARNING: {interfaces_down} interface(s) down")
        
        # General errors
        if 'error' in health_data:
            alerts.append(f"ERROR: {health_data['error']}")
        
        return alerts
    
    def generate_report(self, site_id=None):
        """
        Generate comprehensive health report.
        
        Args:
            site_id: Specific site or None for all
            
        Returns:
            str: Formatted health report
        """
        if site_id:
            health_data = {site_id: self.check_site(site_id)}
        else:
            health_data = self.check_all_sites()
        
        report_lines = [
            "=" * 80,
            "MULTI-SITE HEALTH REPORT",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "=" * 80,
            ""
        ]
        
        for sid, data in health_data.items():
            report_lines.append(f"\nSite: {sid}")
            report_lines.append("-" * 40)
            
            if 'error' in data:
                report_lines.append(f"ERROR: {data['error']}")
                continue
            
            report_lines.append(f"Health Score: {data.get('health_score', 'N/A')}/100")
            report_lines.append(f"CPU Load: {data.get('cpu_load', 'N/A')}%")
            report_lines.append(f"Memory: {data.get('memory_percent', 'N/A')}% used")
            report_lines.append(f"Uptime: {data.get('uptime', 'N/A')}")
            report_lines.append(f"Interfaces: {data.get('interfaces_up', 0)}/{data.get('total_interfaces', 0)} up")
            report_lines.append(f"DHCP Leases: {data.get('dhcp_leases', 'N/A')}")
            report_lines.append(f"Firewall Rules: {data.get('firewall_rules', 'N/A')}")
            
            # Add alerts
            alerts = self.get_alerts(data)
            if alerts:
                report_lines.append("\nAlerts:")
                for alert in alerts:
                    report_lines.append(f"  - {alert}")
        
        report_lines.append("\n" + "=" * 80)
        
        return "\n".join(report_lines)

