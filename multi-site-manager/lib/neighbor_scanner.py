#!/usr/bin/env python3
"""
MikroTik Network Neighbor Scanner
Discovers MikroTik devices on the network and populates site configuration
"""

import os
import sys
import yaml
import logging
import ipaddress
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import concurrent.futures
import threading

# Add parent directory to path to import MCP modules
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir / 'src'))

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, TaskID
from rich import box

console = Console()

class MikroTikNeighborScanner:
    """Scanner to discover MikroTik devices on the network using neighbor discovery."""
    
    def __init__(self, config_file='sites.yaml', max_workers=20):
        """
        Initialize the neighbor scanner.
        
        Args:
            config_file: Path to sites configuration file
            max_workers: Maximum concurrent scan workers
        """
        self.config_file = Path(config_file)
        self.max_workers = max_workers
        self.logger = self._setup_logging()
        self.discovered_devices = []
        self.scan_results = {}
        
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for the scanner."""
        logger = logging.getLogger('neighbor_scanner')
        logger.setLevel(logging.INFO)
        
        # Create file handler
        handler = logging.FileHandler('neighbor_scan.log')
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def scan_from_router(self, router_host: str, username: str, password: str, 
                        port: int = 22) -> Dict[str, Any]:
        """
        Scan for MikroTik neighbors using an existing router.
        
        Args:
            router_host: IP/hostname of the router to scan from
            username: SSH username
            password: SSH password
            port: SSH port
            
        Returns:
            Dictionary with scan results
        """
        console.print(f"\n[bold cyan]Starting neighbor scan from {router_host}...[/bold cyan]\n")
        
        try:
            # Set environment variables for MCP connection
            os.environ['MIKROTIK_HOST'] = router_host
            os.environ['MIKROTIK_USERNAME'] = username
            os.environ['MIKROTIK_PASSWORD'] = password
            os.environ['MIKROTIK_PORT'] = str(port)
            os.environ['MIKROTIK_DRY_RUN'] = 'false'
            
            # Import and reload configuration
            import importlib
            from mcp_mikrotik.settings import configuration
            importlib.reload(configuration)
            
            # Import MCP tools
            from mcp_mikrotik.connector import execute_mikrotik_command
            
            # Get neighbor information
            neighbors = self._get_neighbors(execute_mikrotik_command)
            
            # Get ARP table for additional discovery
            arp_entries = self._get_arp_table(execute_mikrotik_command)
            
            # Get interface information
            interfaces = self._get_interfaces(execute_mikrotik_command)
            
            # Combine and analyze results
            discovered_devices = self._analyze_discoveries(neighbors, arp_entries, interfaces)
            
            scan_result = {
                'timestamp': datetime.now().isoformat(),
                'source_router': router_host,
                'neighbors_found': len(neighbors),
                'arp_entries': len(arp_entries),
                'interfaces': len(interfaces),
                'mikrotik_devices': discovered_devices,
                'total_discovered': len(discovered_devices)
            }
            
            self.logger.info(f"Scan completed from {router_host}: {len(discovered_devices)} MikroTik devices found")
            return scan_result
            
        except Exception as e:
            self.logger.error(f"Error scanning from {router_host}: {e}")
            return {
                'timestamp': datetime.now().isoformat(),
                'source_router': router_host,
                'error': str(e),
                'mikrotik_devices': [],
                'total_discovered': 0
            }
    
    def _get_neighbors(self, execute_command) -> List[Dict[str, Any]]:
        """Get neighbor discovery information."""
        try:
            # Try different neighbor discovery commands
            neighbor_commands = [
                '/ip neighbor print detail',
                '/ip neighbor discovery print detail',
                '/interface bridge host print detail'
            ]
            
            neighbors = []
            for cmd in neighbor_commands:
                try:
                    result = execute_command(cmd)
                    if result and 'no such command' not in result.lower():
                        neighbors.extend(self._parse_neighbor_output(result))
                        break
                except Exception:
                    continue
            
            return neighbors
            
        except Exception as e:
            self.logger.warning(f"Could not get neighbor information: {e}")
            return []
    
    def _get_arp_table(self, execute_command) -> List[Dict[str, Any]]:
        """Get ARP table entries."""
        try:
            result = execute_command('/ip arp print detail')
            return self._parse_arp_output(result)
        except Exception as e:
            self.logger.warning(f"Could not get ARP table: {e}")
            return []
    
    def _get_interfaces(self, execute_command) -> List[Dict[str, Any]]:
        """Get interface information."""
        try:
            result = execute_command('/interface print detail')
            return self._parse_interface_output(result)
        except Exception as e:
            self.logger.warning(f"Could not get interface information: {e}")
            return []
    
    def _parse_neighbor_output(self, output: str) -> List[Dict[str, Any]]:
        """Parse neighbor discovery output."""
        neighbors = []
        lines = output.strip().split('\n')
        
        current_neighbor = {}
        for line in lines:
            # Don't strip the line yet - we need to check for leading spaces
            original_line = line
            line = line.strip('\r')  # Only remove carriage returns
            
            if not line.strip():  # Empty line
                if current_neighbor:
                    neighbors.append(current_neighbor)
                    current_neighbor = {}
                continue
            
            # Handle RouterOS output format with numbered entries
            # Check for lines starting with digit (0, 1, 2, etc.) or space+digit
            if (line.startswith(('0 ', '1 ', '2 ', '3 ', '4 ', '5 ', '6 ', '7 ', '8 ', '9 ')) or
                line.startswith((' 0 ', ' 1 ', ' 2 ', ' 3 ', ' 4 ', ' 5 ', ' 6 ', ' 7 ', ' 8 ', ' 9 '))):
                if current_neighbor:
                    neighbors.append(current_neighbor)
                current_neighbor = {}
                # Parse the line with key=value pairs
                self._parse_key_value_line(line, current_neighbor)
            elif line.startswith('   ') and current_neighbor:
                # Continue parsing key=value pairs from continuation lines
                self._parse_key_value_line(line, current_neighbor)
        
        if current_neighbor:
            neighbors.append(current_neighbor)
        
        return neighbors
    
    def _parse_key_value_line(self, line: str, neighbor_dict: Dict[str, Any]):
        """Parse a line containing key=value pairs."""
        # Split by spaces but handle quoted values
        parts = []
        current_part = ""
        in_quotes = False
        
        for char in line:
            if char == '"' and not in_quotes:
                in_quotes = True
                current_part += char
            elif char == '"' and in_quotes:
                in_quotes = False
                current_part += char
            elif char == ' ' and not in_quotes:
                if current_part:
                    parts.append(current_part)
                    current_part = ""
            else:
                current_part += char
        
        if current_part:
            parts.append(current_part)
        
        # Parse key=value pairs
        for part in parts:
            if '=' in part:
                key, value = part.split('=', 1)
                key = key.strip()
                value = value.strip().strip('"')  # Remove quotes
                neighbor_dict[key] = value
    
    def _parse_arp_output(self, output: str) -> List[Dict[str, Any]]:
        """Parse ARP table output."""
        arp_entries = []
        lines = output.strip().split('\n')
        
        current_entry = {}
        for line in lines:
            line = line.strip()
            if not line:
                if current_entry:
                    arp_entries.append(current_entry)
                    current_entry = {}
                continue
            
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                current_entry[key] = value
        
        if current_entry:
            arp_entries.append(current_entry)
        
        return arp_entries
    
    def _parse_interface_output(self, output: str) -> List[Dict[str, Any]]:
        """Parse interface output."""
        interfaces = []
        lines = output.strip().split('\n')
        
        current_interface = {}
        for line in lines:
            line = line.strip()
            if not line:
                if current_interface:
                    interfaces.append(current_interface)
                    current_interface = {}
                continue
            
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                current_interface[key] = value
        
        if current_interface:
            interfaces.append(current_interface)
        
        return interfaces
    
    def _analyze_discoveries(self, neighbors: List[Dict], arp_entries: List[Dict], 
                           interfaces: List[Dict]) -> List[Dict[str, Any]]:
        """Analyze discovered devices to identify MikroTik devices."""
        mikrotik_devices = []
        
        # Check neighbors for MikroTik devices
        for neighbor in neighbors:
            if self._is_mikrotik_device(neighbor):
                device_info = self._extract_device_info(neighbor, 'neighbor')
                if device_info:
                    mikrotik_devices.append(device_info)
        
        # Check ARP entries for potential MikroTik devices
        for arp_entry in arp_entries:
            if self._is_mikrotik_device(arp_entry):
                device_info = self._extract_device_info(arp_entry, 'arp')
                if device_info and not self._device_exists(mikrotik_devices, device_info['ip']):
                    mikrotik_devices.append(device_info)
        
        # Check interfaces for connected devices
        for interface in interfaces:
            if self._is_mikrotik_device(interface):
                device_info = self._extract_device_info(interface, 'interface')
                if device_info and not self._device_exists(mikrotik_devices, device_info.get('ip', '')):
                    mikrotik_devices.append(device_info)
        
        return mikrotik_devices
    
    def _is_mikrotik_device(self, device_data: Dict[str, Any]) -> bool:
        """Check if device data indicates a MikroTik device."""
        # Check for MikroTik-specific indicators
        mikrotik_indicators = [
            'mikrotik', 'routeros', 'routerboard', 'rb', 'ccr', 'cr', 'hex', 'hap',
            'platform', 'version', 'board', 'software-id'
        ]
        
        # Convert all values to lowercase for comparison
        all_values = ' '.join(str(v).lower() for v in device_data.values())
        
        for indicator in mikrotik_indicators:
            if indicator in all_values:
                return True
        
        # Check for specific MikroTik fields
        mikrotik_fields = ['platform', 'version', 'board', 'software-id', 'identity']
        for field in mikrotik_fields:
            if field in device_data:
                value = str(device_data[field]).lower()
                if any(indicator in value for indicator in ['mikrotik', 'routeros', 'rb']):
                    return True
        
        # Check for MikroTik MAC address patterns
        mac_addresses = []
        for key, value in device_data.items():
            if 'mac' in key.lower() and isinstance(value, str):
                mac_addresses.append(value)
        
        for mac in mac_addresses:
            if self._is_mikrotik_mac(mac):
                return True
        
        return False
    
    def _is_mikrotik_mac(self, mac: str) -> bool:
        """Check if MAC address belongs to MikroTik."""
        # Known MikroTik OUI prefixes
        mikrotik_ouis = [
            '00:0C:42',  # MikroTik
            '4C:5E:0C',  # MikroTik
            '48:8F:5A',  # MikroTik
            'D4:CA:6D',  # MikroTik
            'E4:8D:8C',  # MikroTik
        ]
        
        mac = mac.upper().replace('-', ':').replace('.', ':')
        
        for oui in mikrotik_ouis:
            if mac.startswith(oui):
                return True
        
        return False
    
    def _extract_device_info(self, device_data: Dict[str, Any], source: str) -> Optional[Dict[str, Any]]:
        """Extract device information from discovery data."""
        device_info = {
            'source': source,
            'discovered_at': datetime.now().isoformat()
        }
        
        # Extract IP address
        ip_address = None
        for key, value in device_data.items():
            if 'address' in key.lower() and isinstance(value, str):
                try:
                    # Validate IP address
                    ipaddress.ip_address(value)
                    ip_address = value
                    break
                except ValueError:
                    continue
        
        if not ip_address:
            return None
        
        device_info['ip'] = ip_address
        
        # Extract MAC address
        mac_address = None
        for key, value in device_data.items():
            if 'mac' in key.lower() and isinstance(value, str):
                mac_address = value
                break
        
        if mac_address:
            device_info['mac'] = mac_address
        
        # Extract identity/name
        identity = None
        for key, value in device_data.items():
            if any(term in key.lower() for term in ['identity', 'name', 'description']):
                identity = value
                break
        
        if identity:
            device_info['identity'] = identity
        
        # Extract interface information
        interface = None
        for key, value in device_data.items():
            if 'interface' in key.lower():
                interface = value
                break
        
        if interface:
            device_info['interface'] = interface
        
        return device_info
    
    def _device_exists(self, devices: List[Dict], ip: str) -> bool:
        """Check if device with IP already exists in list."""
        return any(device.get('ip') == ip for device in devices)
    
    def populate_site_config(self, discovered_devices: List[Dict[str, Any]], 
                           default_username: str = 'admin', 
                           default_password: str = None) -> Dict[str, Any]:
        """
        Populate site configuration with discovered devices.
        
        Args:
            discovered_devices: List of discovered MikroTik devices
            default_username: Default username for new sites
            default_password: Default password for new sites
            
        Returns:
            Dictionary with population results
        """
        console.print(f"\n[bold cyan]Populating site configuration with {len(discovered_devices)} devices...[/bold cyan]\n")
        
        # Load existing configuration
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                config = yaml.safe_load(f)
        else:
            config = {'sites': {}}
        
        existing_sites = config.get('sites', {})
        added_sites = []
        skipped_sites = []
        
        for device in discovered_devices:
            ip = device['ip']
            
            # Check if site already exists
            site_exists = any(site_data.get('host') == ip for site_data in existing_sites.values())
            
            if site_exists:
                skipped_sites.append(ip)
                continue
            
            # Generate site ID
            site_id = self._generate_site_id(device)
            
            # Create site configuration
            site_config = {
                'name': device.get('identity', f'MikroTik Device {ip}'),
                'host': ip,
                'username': default_username,
                'password': default_password or 'changeme',
                'ssh_port': 22,
                'location': f'Discovered via {device["source"]}',
                'priority': 'medium',
                'tags': ['discovered', 'auto-populated'],
                'notes': f'Auto-discovered on {device["discovered_at"]}',
                'discovery_info': {
                    'source': device['source'],
                    'discovered_at': device['discovered_at'],
                    'mac_address': device.get('mac'),
                    'interface': device.get('interface')
                }
            }
            
            # Add to configuration
            existing_sites[site_id] = site_config
            added_sites.append({
                'site_id': site_id,
                'ip': ip,
                'name': site_config['name']
            })
        
        # Save updated configuration
        config['sites'] = existing_sites
        with open(self.config_file, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)
        
        result = {
            'timestamp': datetime.now().isoformat(),
            'total_discovered': len(discovered_devices),
            'added_sites': len(added_sites),
            'skipped_sites': len(skipped_sites),
            'added_sites_list': added_sites,
            'skipped_sites_list': skipped_sites
        }
        
        self.logger.info(f"Site population completed: {len(added_sites)} sites added, {len(skipped_sites)} skipped")
        return result
    
    def _generate_site_id(self, device: Dict[str, Any]) -> str:
        """Generate a unique site ID for the device."""
        ip = device['ip']
        identity = device.get('identity', '')
        
        # Use identity if available and clean
        if identity and len(identity) < 20:
            site_id = identity.lower().replace(' ', '-').replace('_', '-')
            # Remove special characters
            site_id = ''.join(c for c in site_id if c.isalnum() or c == '-')
        else:
            # Use IP-based ID
            site_id = f"mikrotik-{ip.replace('.', '-')}"
        
        return site_id
    
    def display_scan_results(self, scan_result: Dict[str, Any]):
        """Display scan results in a formatted table."""
        console.print(f"\n[bold green]Scan Results from {scan_result['source_router']}[/bold green]\n")
        
        if 'error' in scan_result:
            console.print(f"[red]Error: {scan_result['error']}[/red]")
            return
        
        # Summary table
        summary_table = Table(title="Scan Summary", box=box.ROUNDED)
        summary_table.add_column("Metric", style="cyan")
        summary_table.add_column("Count", style="white")
        
        summary_table.add_row("Neighbors Found", str(scan_result['neighbors_found']))
        summary_table.add_row("ARP Entries", str(scan_result['arp_entries']))
        summary_table.add_row("Interfaces", str(scan_result['interfaces']))
        summary_table.add_row("MikroTik Devices", str(scan_result['total_discovered']))
        
        console.print(summary_table)
        
        # Devices table
        if scan_result['mikrotik_devices']:
            devices_table = Table(title="Discovered MikroTik Devices", box=box.ROUNDED)
            devices_table.add_column("IP Address", style="cyan")
            devices_table.add_column("Identity", style="white")
            devices_table.add_column("MAC Address", style="yellow")
            devices_table.add_column("Source", style="green")
            devices_table.add_column("Interface", style="dim")
            
            for device in scan_result['mikrotik_devices']:
                devices_table.add_row(
                    device['ip'],
                    device.get('identity', 'Unknown'),
                    device.get('mac', 'Unknown'),
                    device['source'],
                    device.get('interface', 'Unknown')
                )
            
            console.print(devices_table)
        else:
            console.print("[yellow]No MikroTik devices discovered[/yellow]")
    
    def display_population_results(self, population_result: Dict[str, Any]):
        """Display population results in a formatted table."""
        console.print(f"\n[bold green]Site Population Results[/bold green]\n")
        
        # Summary table
        summary_table = Table(title="Population Summary", box=box.ROUNDED)
        summary_table.add_column("Metric", style="cyan")
        summary_table.add_column("Count", style="white")
        
        summary_table.add_row("Total Discovered", str(population_result['total_discovered']))
        summary_table.add_row("Sites Added", str(population_result['added_sites']))
        summary_table.add_row("Sites Skipped", str(population_result['skipped_sites']))
        
        console.print(summary_table)
        
        # Added sites table
        if population_result['added_sites_list']:
            added_table = Table(title="Added Sites", box=box.ROUNDED)
            added_table.add_column("Site ID", style="cyan")
            added_table.add_column("IP Address", style="white")
            added_table.add_column("Name", style="yellow")
            
            for site in population_result['added_sites_list']:
                added_table.add_row(
                    site['site_id'],
                    site['ip'],
                    site['name']
                )
            
            console.print(added_table)
        
        # Skipped sites
        if population_result['skipped_sites_list']:
            console.print(f"\n[yellow]Skipped sites (already exist): {', '.join(population_result['skipped_sites_list'])}[/yellow]")

def main():
    """Main function for neighbor scanner."""
    console.print("[bold cyan]MikroTik Network Neighbor Scanner[/bold cyan]")
    console.print("=" * 50)
    
    # Get router connection details
    router_host = input("Enter router IP/hostname: ").strip()
    username = input("Enter username (default: admin): ").strip() or "admin"
    password = input("Enter password: ").strip()
    
    if not router_host or not password:
        console.print("[red]Router host and password are required[/red]")
        return 1
    
    # Initialize scanner
    scanner = MikroTikNeighborScanner()
    
    try:
        # Perform scan
        scan_result = scanner.scan_from_router(router_host, username, password)
        
        # Display results
        scanner.display_scan_results(scan_result)
        
        if scan_result['mikrotik_devices']:
            # Ask if user wants to populate site config
            populate = input("\nDo you want to populate the site configuration? (y/N): ").strip().lower()
            
            if populate in ['y', 'yes']:
                default_password = input("Enter default password for discovered devices (or press Enter for 'changeme'): ").strip()
                
                population_result = scanner.populate_site_config(
                    scan_result['mikrotik_devices'],
                    username,
                    default_password or 'changeme'
                )
                
                scanner.display_population_results(population_result)
        
        return 0
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        return 1

if __name__ == '__main__':
    sys.exit(main())
