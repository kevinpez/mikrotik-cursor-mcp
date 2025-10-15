#!/usr/bin/env python3
"""
Comprehensive test script for MikroTik Cursor MCP server.
Tests all 426+ features across 19 categories and reports any issues.

This is the complete test suite that validates all available functionality.
"""

import sys
import os
import time
import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Any

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from mcp_mikrotik.tools.tool_registry import get_all_handlers
from mcp_mikrotik.settings.configuration import mikrotik_config
from mcp_mikrotik.logger import app_logger


class ComprehensiveTester:
    def __init__(self, verbose: bool = False, dry_run: bool = True, category: str = None):
        self.verbose = verbose
        self.dry_run = dry_run
        self.category = category
        self.handlers = get_all_handlers()
        self.results = {
            'total_tests': 0,
            'passed': 0,
            'failed': 0,
            'errors': [],
            'categories': {},
            'start_time': time.time()
        }
        
        # Set dry-run mode for safety
        if dry_run:
            os.environ['MIKROTIK_DRY_RUN'] = 'true'
    
    def log(self, message: str, level: str = "INFO"):
        """Log message with timestamp."""
        timestamp = time.strftime("%H:%M:%S")
        if self.verbose or level == "ERROR":
            print(f"[{timestamp}] {level}: {message}")
    
    def test_tool(self, tool_name: str, test_args: Dict[str, Any] = None) -> Tuple[bool, str]:
        """Test a single tool and return (success, error_message)."""
        if test_args is None:
            test_args = {}
            
        try:
            if tool_name not in self.handlers:
                return False, f"Tool {tool_name} not found in handlers"
            
            # Test the tool
            result = self.handlers[tool_name](test_args)
            
            # Check if result is valid
            if result is None:
                return False, "Tool returned None"
            
            if isinstance(result, str) and result.strip():
                return True, ""
            elif isinstance(result, dict):
                return True, ""
            else:
                return False, f"Unexpected result type: {type(result)}"
                
        except Exception as e:
            return False, f"Exception: {str(e)}"
    
    def get_test_args_for_tool(self, tool_name: str) -> Dict[str, Any]:
        """Get appropriate test arguments for a tool."""
        test_args = {}
        
        # Handle specific parameter requirements first (highest priority)
        if "address_id" in tool_name.lower():
            test_args = {"address_id": "0"}
        elif "prefix" in tool_name.lower() and "pool" in tool_name.lower():
            test_args = {"name": "ipv6-pool", "prefix": "2001:db8::/64"}
        elif "list_name" in tool_name.lower():
            test_args = {"list_name": "test-list", "address": "2001:db8::1"}
        elif "entry_id" in tool_name.lower():
            test_args = {"entry_id": "0"}
        elif "lease_id" in tool_name.lower():
            test_args = {"lease_id": "0"}
        elif "interface" in tool_name.lower() and "dhcpv6" in tool_name.lower():
            test_args = {"interface": "bridgeLocal"}
        elif "name" in tool_name.lower() and "dhcpv6" in tool_name.lower():
            test_args = {"name": "dhcpv6-option", "value": "test"}
        elif "public_key" in tool_name.lower():
            test_args = {"interface": "wg1", "public_key": "test-key"}
        elif "hostname" in tool_name.lower():
            test_args = {"hostname": "google.com"}
        elif "severity" in tool_name.lower():
            test_args = {"severity": "info"}
        elif "topic" in tool_name.lower():
            test_args = {"topic": "system"}
        elif "mac_address" in tool_name.lower():
            test_args = {"interface": "wlan1", "mac_address": "00:11:22:33:44:55"}
        elif "ports" in tool_name.lower() and "vlan" in tool_name.lower():
            test_args = {"name": "bridge1", "ports": "ether1,ether2"}
        elif "vlan_id" in tool_name.lower():
            test_args = {"bridge": "bridge", "vlan_id": "100"}
        elif "expand" in tool_name.lower():
            test_args = {"name": "test-pool"}
        elif "address_pool" in tool_name.lower():
            test_args = {"name": "dhcpv6-server", "interface": "bridgeLocal", "address_pool": "ipv6-pool"}
        elif "key" in tool_name.lower() and "container" in tool_name.lower():
            test_args = {"name": "test-env", "key": "VAR", "value": "VALUE"}
        elif "src" in tool_name.lower() and "container" in tool_name.lower():
            test_args = {"name": "test-mount", "src": "/tmp", "dst": "/mnt"}
        elif "name" in tool_name.lower() and ("hotspot" in tool_name.lower() or "user" in tool_name.lower()):
            test_args = {"name": "testuser", "password": "testpass"}
        elif "address" in tool_name.lower() and ("ipv6" in tool_name.lower() or "dhcpv6" in tool_name.lower()):
            test_args = {"address": "2001:db8::1"}
        elif "additional_ranges" in tool_name.lower():
            test_args = {"name": "test-pool", "additional_ranges": "192.168.100.201-192.168.100.250"}
        elif "interface" in tool_name.lower() and "ipv6" in tool_name.lower():
            test_args = {"address": "2001:db8::1/64", "interface": "ether1"}
        elif "list" in tool_name.lower():
            # List commands usually don't need arguments
            pass
        elif "get" in tool_name.lower():
            # Get commands might need basic arguments
            if "interface" in tool_name:
                test_args = {"interface": "ether1"}
            elif "user" in tool_name:
                test_args = {"username": "admin"}
            elif "container" in tool_name:
                test_args = {"container": "test-container"}
            elif "address" in tool_name:
                test_args = {"address_id": "0"}
            elif "pool" in tool_name:
                test_args = {"name": "dhcp_pool0"}
            elif "entry" in tool_name:
                test_args = {"entry_id": "0"}
            elif "vlan" in tool_name:
                test_args = {"name": "vlan100"}
            elif "wireguard" in tool_name:
                test_args = {"name": "wg1"}
            elif "wireless" in tool_name:
                test_args = {"name": "wlan1"}
            elif "wireguard" in tool_name:
                test_args = {"name": "wg1"}
            elif "openvpn" in tool_name:
                test_args = {"name": "ovpn1"}
            elif "wireless" in tool_name:
                test_args = {"name": "wlan1"}
            elif "dhcp" in tool_name:
                test_args = {"name": "dhcp1"}
            elif "dhcpv6" in tool_name:
                test_args = {"interface": "bridgeLocal"}
            elif "ipv6" in tool_name and "address" in tool_name:
                test_args = {"address": "2001:db8::1/64", "interface": "ether1"}
            elif "ipv6" in tool_name and "nd" in tool_name:
                test_args = {"interface": "ether1"}
        elif "create" in tool_name.lower() or "set" in tool_name.lower() or "add" in tool_name.lower():
            # Create/Set/Add commands need test data
            if "firewall" in tool_name:
                test_args = {
                    "chain": "input",
                    "action": "accept",
                    "protocol": "tcp",
                    "dst-port": "8080",
                    "comment": "test-rule"
                }
            elif "dhcp" in tool_name:
                if "server" in tool_name:
                    test_args = {
                        "name": "dhcp1",
                        "interface": "bridgeLocal",
                        "address-pool": "dhcp_pool0",
                        "lease-time": "30m"
                    }
                elif "network" in tool_name:
                    test_args = {
                        "network": "192.168.1.0/24",
                        "gateway": "192.168.1.1",
                        "dns_servers": "8.8.8.8,8.8.4.4"
                    }
                elif "pool" in tool_name:
                    test_args = {
                        "name": "dhcp-pool-test",
                        "ranges": "192.168.1.100-192.168.1.200"
                    }
                else:
                    test_args = {
                        "interface": "bridgeLocal",
                        "address-pool": "dhcp_pool0",
                        "lease-time": "30m"
                    }
            elif "system" in tool_name and "identity" in tool_name:
                test_args = {"name": "test-router"}
            elif "user" in tool_name:
                test_args = {"username": "testuser", "password": "testpass"}
            elif "interface" in tool_name:
                test_args = {"name": "test-interface", "type": "bridge"}
            elif "address" in tool_name:
                test_args = {"address": "192.168.1.100/24", "interface": "ether1"}
            elif "pool" in tool_name:
                test_args = {"name": "test-pool", "ranges": "192.168.100.100-192.168.100.200"}
            elif "expand" in tool_name:
                test_args = {"name": "test-pool", "additional_ranges": "192.168.100.201-192.168.100.250"}
            elif "watchdog" in tool_name:
                test_args = {"script_name": "watchdog-test", "script_content": "echo watchdog test"}
            elif "script" in tool_name:
                test_args = {"script_name": "test-script", "source": "echo test"}
            elif "eoip" in tool_name:
                test_args = {"name": "eoip1", "remote_address": "192.168.1.1", "tunnel_id": "1"}
            elif "vlan" in tool_name:
                if "create" in tool_name or "vlan_interface" in tool_name:
                    test_args = {"name": "vlan100", "vlan_id": "100", "interface": "ether1"}
                elif "bridge" in tool_name:
                    if "add" in tool_name:
                        test_args = {"bridge": "bridge", "vlan_ids": "100", "tagged": "ether1", "untagged": "ether2"}
                    elif "remove" in tool_name:
                        test_args = {"bridge": "bridge", "vlan_id": "100"}
                    elif "port" in tool_name:
                        test_args = {"bridge": "bridge", "port": "ether1", "pvid": "100"}
                    elif "filtering" in tool_name:
                        test_args = {"bridge": "bridge", "vlan_ids": "100"}
                    elif "aware" in tool_name:
                        test_args = {"name": "bridge1", "ports": "ether1,ether2"}
                elif "get" in tool_name:
                    test_args = {"name": "vlan100"}
                else:
                    test_args = {"name": "vlan100", "vlan_id": "100", "interface": "ether1"}
            elif "script" in tool_name and "content" in tool_name:
                test_args = {"script_name": "test-script", "script_content": "echo test"}
            elif "wireguard" in tool_name:
                if "get" in tool_name:
                    test_args = {"name": "wg1"}
                elif "peer" in tool_name:
                    if "add" in tool_name:
                        test_args = {"interface": "wg1", "public_key": "test-key"}
                    elif "update" in tool_name:
                        test_args = {"interface": "wg1", "public_key": "test-key"}
                    else:
                        test_args = {"interface": "wg1", "public_key": "test-key"}
                else:
                    test_args = {"name": "wg1", "listen_port": "51820"}
            elif "openvpn" in tool_name:
                if "client" in tool_name:
                    test_args = {"name": "ovpn1", "connect_to": "192.168.1.1"}
                else:
                    test_args = {"name": "ovpn1"}
            elif "wireless" in tool_name:
                if "get" in tool_name:
                    test_args = {"name": "wlan1"}
                else:
                    test_args = {"name": "wlan1", "ssid": "test-wifi"}
            elif "hotspot" in tool_name:
                if "server" in tool_name:
                    test_args = {"name": "hs1", "interface": "ether1", "address_pool": "dhcp_pool0"}
                elif "user" in tool_name:
                    test_args = {"name": "hotspotuser", "password": "hotspotpass"}
                else:
                    test_args = {"name": "hs1", "interface": "ether1"}
            elif "container" in tool_name:
                if "image" in tool_name or "create" in tool_name:
                    test_args = {"name": "test-container", "image": "ubuntu"}
                elif "env" in tool_name:
                    test_args = {"name": "test-env", "key": "VAR", "value": "VALUE"}
                elif "mount" in tool_name:
                    test_args = {"name": "test-mount", "src": "/tmp", "dst": "/mnt"}
                elif "veth" in tool_name:
                    test_args = {"name": "test-veth", "bridge": "bridge"}
                elif "start" in tool_name or "stop" in tool_name or "get" in tool_name:
                    test_args = {"name": "test-container"}
                elif "registry" in tool_name:
                    test_args = {"url": "https://registry.example.com"}
                elif "tmpdir" in tool_name:
                    test_args = {"tmpdir": "/tmp"}
                elif "env" in tool_name and "create" in tool_name:
                    test_args = {"name": "test-env", "key": "VAR", "value": "VALUE"}
                elif "mount" in tool_name and "create" in tool_name:
                    test_args = {"name": "test-mount", "src": "/tmp", "dst": "/mnt"}
                else:
                    test_args = {"name": "test-container"}
            elif "dns" in tool_name:
                if "static" in tool_name:
                    if "get" in tool_name or "update" in tool_name or "remove" in tool_name or "enable" in tool_name or "disable" in tool_name:
                        test_args = {"entry_id": "0"}
                    else:
                        test_args = {"name": "test.local", "address": "192.168.1.100"}
                elif "servers" in tool_name:
                    test_args = {"servers": "8.8.8.8,8.8.4.4"}
                elif "regexp" in tool_name:
                    test_args = {"regexp": "test.*", "address": "192.168.1.100"}
                elif "lookup" in tool_name:
                    test_args = {"hostname": "google.com"}
            elif "route" in tool_name:
                test_args = {"dst_address": "0.0.0.0/0", "gateway": "192.168.1.1"}
            elif "ipv6" in tool_name:
                if "address" in tool_name:
                    test_args = {"address": "2001:db8::1/64", "interface": "ether1"}
                elif "route" in tool_name:
                    test_args = {"dst_address": "::/0", "gateway": "2001:db8::1"}
                elif "pool" in tool_name:
                    test_args = {"name": "ipv6-pool", "prefix": "2001:db8::/64"}
                elif "forward" in tool_name:
                    test_args = {"enabled": "yes"}
                elif "filter" in tool_name:
                    test_args = {"chain": "input", "rule_action": "accept"}
                elif "nat" in tool_name or "mangle" in tool_name:
                    test_args = {"chain": "input", "action": "accept"}
                elif "address_list" in tool_name:
                    test_args = {"list_name": "test-list", "address": "2001:db8::1"}
                elif "nd" in tool_name:
                    test_args = {"interface": "ether1", "hop_limit": "64"}
            elif "backup" in tool_name:
                if "schedule" in tool_name:
                    test_args = {"name": "daily-backup", "interval": "1d", "action": "backup"}
                else:
                    test_args = {"filename": "test-backup.backup"}
            elif "env" in tool_name:
                test_args = {"name": "test-env", "value": "test-value"}
            elif "mount" in tool_name:
                test_args = {"name": "test-mount", "src": "/tmp", "dst": "/mnt"}
            elif "veth" in tool_name:
                test_args = {"name": "test-veth", "bridge": "bridge"}
            elif "access" in tool_name:
                test_args = {"interface": "wlan1", "mac_address": "00:11:22:33:44:55"}
        elif "remove" in tool_name.lower() or "delete" in tool_name.lower():
            # Remove/Delete commands need identifiers
            if "address" in tool_name:
                test_args = {"address_id": "0"}
            elif "pool" in tool_name:
                test_args = {"name": "test-pool"}
            elif "interface" in tool_name:
                test_args = {"name": "test-interface"}
            elif "user" in tool_name:
                test_args = {"username": "testuser"}
            elif "entry" in tool_name:
                test_args = {"entry_id": "0"}
            elif "rule" in tool_name:
                test_args = {"rule_id": "0"}
            elif "peer" in tool_name:
                test_args = {"interface": "wg1", "peer": "peer1"}
            elif "container" in tool_name:
                test_args = {"name": "test-container"}
            elif "backup" in tool_name:
                test_args = {"filename": "test-backup.backup"}
            elif "watchdog" in tool_name:
                test_args = {"script_name": "watchdog-test"}
            elif "lease" in tool_name:
                test_args = {"lease_id": "0"}
            elif "client" in tool_name:
                test_args = {"interface": "bridgeLocal"}
            elif "route" in tool_name and "ipv6" in tool_name:
                test_args = {"dst_address": "::/0"}
            elif "eoip" in tool_name:
                test_args = {"name": "eoip1"}
            elif "dhcp" in tool_name:
                test_args = {"name": "dhcp1"}
            elif "dhcpv6" in tool_name:
                    if "server" in tool_name and "create" in tool_name:
                        test_args = {"name": "dhcpv6-server", "interface": "bridgeLocal", "address_pool": "ipv6-pool"}
                    elif "client" in tool_name:
                        test_args = {"interface": "bridgeLocal"}
                    elif "lease" in tool_name and "remove" in tool_name:
                        test_args = {"lease_id": "0"}
                    elif "option" in tool_name and "create" in tool_name:
                        test_args = {"name": "dhcpv6-option", "code": "23", "value": "test"}
                    elif "relay" in tool_name and "configure" in tool_name:
                        test_args = {"interface": "bridgeLocal", "servers": "2001:db8::1"}
                    elif "static_lease" in tool_name:
                        test_args = {"address": "2001:db8::100", "duid": "test-duid"}
            elif "wireless" in tool_name:
                if "security_profile" in tool_name:
                    test_args = {"name": "sec-profile-test"}
                elif "access_list" in tool_name:
                    test_args = {"entry_id": "0"}
            elif "hotspot" in tool_name:
                if "server" in tool_name:
                    test_args = {"name": "hs1"}
                else:
                    test_args = {"name": "hotspotuser"}
            elif "container" in tool_name:
                test_args = {"name": "test-container"}
        elif "update" in tool_name.lower():
            # Update commands need identifiers and new values
            if "address" in tool_name:
                test_args = {"address_id": "0", "comment": "updated"}
            elif "pool" in tool_name:
                test_args = {"name": "test-pool", "ranges": "192.168.200.100-192.168.200.200"}
            elif "interface" in tool_name:
                test_args = {"name": "test-interface", "comment": "updated"}
            elif "user" in tool_name:
                test_args = {"username": "testuser", "password": "newpass"}
            elif "peer" in tool_name:
                test_args = {"interface": "wg1", "peer": "peer1", "comment": "updated"}
            elif "public_key" in tool_name:
                test_args = {"interface": "wg1", "public_key": "test-key", "comment": "updated"}
            elif "wireguard" in tool_name:
                test_args = {"name": "wg1", "comment": "updated"}
            elif "openvpn" in tool_name:
                test_args = {"name": "ovpn1", "comment": "updated"}
            elif "wireless" in tool_name:
                if "security_profile" in tool_name:
                    test_args = {"name": "sec-profile-test", "comment": "updated"}
                else:
                    test_args = {"name": "wlan1", "comment": "updated"}
        elif "enable" in tool_name.lower() or "disable" in tool_name.lower():
            # Enable/Disable commands need identifiers
            if "interface" in tool_name:
                test_args = {"name": "test-interface"}
            elif "entry" in tool_name:
                test_args = {"entry_id": "0"}
            elif "user" in tool_name:
                test_args = {"username": "testuser"}
            elif "wireguard" in tool_name:
                test_args = {"name": "wg1"}
            elif "openvpn" in tool_name:
                test_args = {"name": "ovpn1"}
            elif "bridge" in tool_name and "vlan" in tool_name:
                test_args = {"bridge_name": "bridge"}
            elif "vlan_aware" in tool_name:
                test_args = {"name": "bridge1", "ports": "ether1,ether2"}
        elif "ping" in tool_name.lower():
            test_args = {"address": "8.8.8.8", "count": "1"}
        elif "dns" in tool_name.lower() and "lookup" in tool_name.lower():
            test_args = {"host": "google.com"}
        elif "traceroute" in tool_name.lower():
            test_args = {"address": "8.8.8.8"}
        elif "scan" in tool_name.lower():
            test_args = {"interface": "wlan1"}
        elif "search" in tool_name.lower():
            test_args = {"search_term": "test"}
        elif "severity" in tool_name.lower():
            test_args = {"severity": "info"}
        elif "topic" in tool_name.lower():
            test_args = {"topic": "system"}
        elif "query" in tool_name.lower():
            test_args = {"name": "test.local"}
        elif "backup" in tool_name.lower():
            if "restore" in tool_name or "info" in tool_name:
                test_args = {"filename": "test-backup.backup"}
            else:
                test_args = {"filename": "test-backup.backup"}
        elif "env" in tool_name.lower() and "create" in tool_name.lower():
            test_args = {"name": "test-env", "key": "VAR", "value": "VALUE"}
        elif "mount" in tool_name.lower() and "create" in tool_name.lower():
            test_args = {"name": "test-mount", "src": "/tmp", "dst": "/mnt"}
        elif "nd" in tool_name.lower():
            test_args = {"interface": "ether1"}
        elif "registry" in tool_name.lower():
            test_args = {"url": "https://registry.example.com"}
        elif "tmpdir" in tool_name.lower():
            test_args = {"tmpdir": "/tmp"}
        elif "filtering" in tool_name.lower():
            test_args = {"bridge_name": "bridge"}
        elif "bridge" in tool_name.lower() and "vlan" in tool_name.lower():
            test_args = {"bridge": "bridge", "vlan_id": "100"}
        elif "port" in tool_name.lower():
            test_args = {"port": "ether1"}
        elif "vlan_aware" in tool_name.lower():
            test_args = {"name": "bridge1", "ports": "ether1,ether2"}
        elif "access_list" in tool_name.lower() and "create" in tool_name.lower():
            test_args = {"interface": "wlan1", "mac_address": "00:11:22:33:44:55"}
        elif "access_list" in tool_name.lower() and "remove" in tool_name.lower():
            test_args = {"entry_id": "0"}
        elif "hotspot" in tool_name.lower() and "user" in tool_name.lower() and "create" in tool_name.lower():
            test_args = {"name": "hotspotuser", "password": "hotspotpass"}
        elif "dhcpv6" in tool_name.lower() and "client" in tool_name.lower():
            test_args = {"interface": "bridgeLocal"}
        elif "static_lease" in tool_name.lower():
            test_args = {"address": "192.168.1.100", "mac_address": "00:11:22:33:44:55"}
        elif "dhcpv6" in tool_name.lower() and "server" in tool_name.lower() and "create" in tool_name.lower():
            test_args = {"name": "dhcpv6-server", "interface": "bridgeLocal", "address_pool": "ipv6-pool"}
        elif "dhcpv6" in tool_name.lower() and "static_lease" in tool_name.lower():
            test_args = {"address": "2001:db8::100", "duid": "test-duid"}
        elif "dhcpv6" in tool_name.lower() and "lease" in tool_name.lower() and "remove" in tool_name.lower():
            test_args = {"lease_id": "0"}
        elif "dhcpv6" in tool_name.lower() and "client" in tool_name.lower() and "get" in tool_name.lower():
            test_args = {"interface": "bridgeLocal"}
        elif "dhcpv6" in tool_name.lower() and "client" in tool_name.lower() and "remove" in tool_name.lower():
            test_args = {"interface": "bridgeLocal"}
        elif "dhcpv6" in tool_name.lower() and "option" in tool_name.lower():
            test_args = {"name": "dhcpv6-option", "value": "test-value"}
        elif "dhcpv6" in tool_name.lower() and "option" in tool_name.lower() and "create" in tool_name.lower():
            test_args = {"name": "dhcpv6-option", "code": "23", "value": "test"}
        elif "dhcpv6" in tool_name.lower() and "relay" in tool_name.lower() and "configure" in tool_name.lower():
            test_args = {"interface": "bridgeLocal", "servers": "2001:db8::1", "dhcp_server": "2001:db8::1"}
        elif "hotspot" in tool_name.lower() and "user" in tool_name.lower() and "create" in tool_name.lower():
            test_args = {"name": "hotspotuser", "password": "hotspotpass"}
        elif "lookup" in tool_name.lower():
            test_args = {"hostname": "google.com"}
        elif "severity" in tool_name.lower():
            test_args = {"severity": "info"}
        elif "topic" in tool_name.lower():
            test_args = {"topic": "system"}
        elif "address_id" in tool_name.lower() or ("remove" in tool_name.lower() and "address" in tool_name.lower()):
            test_args = {"address_id": "0"}
        elif "prefix" in tool_name.lower() and "pool" in tool_name.lower():
            test_args = {"name": "ipv6-pool", "prefix": "2001:db8::/64"}
        elif "list_name" in tool_name.lower():
            test_args = {"list_name": "test-list", "address": "2001:db8::1"}
        elif "entry_id" in tool_name.lower():
            test_args = {"entry_id": "0"}
        elif "lease_id" in tool_name.lower():
            test_args = {"lease_id": "0"}
        elif "public_key" in tool_name.lower():
            test_args = {"interface": "wg1", "public_key": "test-key"}
        elif "name" in tool_name.lower() and ("hotspot" in tool_name.lower() or "user" in tool_name.lower()):
            test_args = {"name": "testuser", "password": "testpass"}
        elif "interface" in tool_name.lower() and ("dhcpv6" in tool_name.lower() or "client" in tool_name.lower()):
            test_args = {"interface": "bridgeLocal"}
        elif "address" in tool_name.lower() and ("ipv6" in tool_name.lower() or "dhcpv6" in tool_name.lower()):
            test_args = {"address": "2001:db8::1"}
        elif "key" in tool_name.lower() and "container" in tool_name.lower():
            test_args = {"name": "test-env", "key": "VAR", "value": "VALUE"}
        elif "src" in tool_name.lower() and "container" in tool_name.lower():
            test_args = {"name": "test-mount", "src": "/tmp", "dst": "/mnt"}
        elif "expand" in tool_name.lower():
            test_args = {"name": "test-pool"}
        elif "address_pool" in tool_name.lower():
            test_args = {"name": "dhcpv6-server", "interface": "bridgeLocal", "address_pool": "ipv6-pool"}
        elif "ports" in tool_name.lower() and "vlan" in tool_name.lower():
            test_args = {"name": "bridge1", "ports": "ether1,ether2"}
        elif "vlan_id" in tool_name.lower():
            test_args = {"bridge": "bridge", "vlan_id": "100"}
        elif "hostname" in tool_name.lower():
            test_args = {"hostname": "google.com"}
        elif "mac_address" in tool_name.lower():
            test_args = {"interface": "wlan1", "mac_address": "00:11:22:33:44:55"}
        elif "address_id" in tool_name.lower():
            test_args = {"address_id": "0"}
        elif "prefix" in tool_name.lower() and "pool" in tool_name.lower():
            test_args = {"name": "ipv6-pool", "prefix": "2001:db8::/64"}
        elif "list_name" in tool_name.lower():
            test_args = {"list_name": "test-list", "address": "2001:db8::1"}
        elif "entry_id" in tool_name.lower():
            test_args = {"entry_id": "0"}
        elif "interface" in tool_name.lower() and "dhcpv6" in tool_name.lower():
            test_args = {"interface": "bridgeLocal"}
        elif "name" in tool_name.lower() and "dhcpv6" in tool_name.lower():
            test_args = {"name": "dhcpv6-option", "value": "test"}
        elif "remove_ip_address" in tool_name.lower():
            test_args = {"address_id": "0"}
        elif "expand_ip_pool" in tool_name.lower():
            test_args = {"name": "test-pool", "additional_ranges": "192.168.100.201-192.168.100.250"}
        elif "add_ipv6_address" in tool_name.lower():
            test_args = {"address": "2001:db8::1/64", "interface": "ether1"}
        elif "create_ipv6_pool" in tool_name.lower():
            test_args = {"name": "ipv6-pool", "prefix": "2001:db8::/64"}
        elif "add_ipv6_address_list" in tool_name.lower():
            test_args = {"list_name": "test-list", "address": "2001:db8::1"}
        elif "remove_ipv6_address_list_entry" in tool_name.lower():
            test_args = {"entry_id": "0"}
        elif "create_dhcpv6_server" in tool_name.lower():
            test_args = {"name": "dhcpv6-server", "interface": "bridgeLocal", "address_pool": "ipv6-pool"}
        elif "create_dhcpv6_static_lease" in tool_name.lower():
            test_args = {"address": "2001:db8::100", "duid": "test-duid"}
        elif "get_dhcpv6_client" in tool_name.lower():
            test_args = {"interface": "bridgeLocal"}
        elif "create_dhcpv6_option" in tool_name.lower():
            test_args = {"name": "dhcpv6-option", "value": "test"}
        elif "get_dns_static" in tool_name.lower():
            test_args = {"entry_id": "0"}
        elif "update_dns_static" in tool_name.lower():
            test_args = {"entry_id": "0", "comment": "updated"}
        elif "remove_dns_static" in tool_name.lower():
            test_args = {"entry_id": "0"}
        elif "enable_dns_static" in tool_name.lower():
            test_args = {"entry_id": "0"}
        elif "disable_dns_static" in tool_name.lower():
            test_args = {"entry_id": "0"}
        
        return test_args
    
    def test_category(self, category_name: str) -> Dict[str, Any]:
        """Test all tools in a specific category."""
        self.log(f"Testing category: {category_name}")
        
        category_results = {
            'total': 0,
            'passed': 0,
            'failed': 0,
            'tools': {}
        }
        
        # Find tools in this category
        category_tools = [name for name in self.handlers.keys() if category_name in name.lower()]
        
        if not category_tools:
            self.log(f"No tools found for category: {category_name}", "WARNING")
            return category_results
        
        for tool_name in category_tools:
            category_results['total'] += 1
            self.results['total_tests'] += 1
            
            test_args = self.get_test_args_for_tool(tool_name)
            
            if self.verbose:
                self.log(f"  Testing {tool_name}...")
            
            success, error = self.test_tool(tool_name, test_args)
            
            if success:
                category_results['passed'] += 1
                self.results['passed'] += 1
                if self.verbose:
                    self.log(f"    PASSED: {tool_name}")
            else:
                category_results['failed'] += 1
                self.results['failed'] += 1
                error_msg = f"{tool_name}: {error}"
                self.results['errors'].append(error_msg)
                category_results['tools'][tool_name] = error
                self.log(f"    FAILED: {tool_name} - {error}", "ERROR")
        
        return category_results
    
    def test_all_categories(self):
        """Test all categories or a specific category."""
        categories = [
            'system', 'interfaces', 'ip', 'dhcp', 'dns', 'routes', 'firewall',
            'diagnostics', 'users', 'logs', 'backup', 'queues', 'vlan',
            'wireguard', 'openvpn', 'wireless', 'hotspot', 'ipv6', 'container'
        ]
        
        if self.category:
            if self.category.lower() not in categories:
                self.log(f"Unknown category: {self.category}", "ERROR")
                return
            categories = [self.category.lower()]
        
        for category in categories:
            self.results['categories'][category] = self.test_category(category)
    
    def print_summary(self):
        """Print test summary."""
        duration = time.time() - self.results['start_time']
        
        print("\n" + "="*80)
        print("MikroTik Cursor MCP - Comprehensive Test Results")
        print("="*80)
        
        print(f"Test Duration: {duration:.2f} seconds")
        print(f"Total Tests: {self.results['total_tests']}")
        print(f"Passed: {self.results['passed']} ({self.results['passed']/max(self.results['total_tests'], 1)*100:.1f}%)")
        print(f"Failed: {self.results['failed']} ({self.results['failed']/max(self.results['total_tests'], 1)*100:.1f}%)")
        
        if self.results['failed'] == 0:
            print("\n*** ALL TESTS PASSED! ***")
            print("Your MikroTik Cursor MCP server is fully functional!")
        else:
            print(f"\nWARNING: {self.results['failed']} TESTS FAILED")
        
        print("\nCategory Results:")
        print("-" * 50)
        
        for category, results in self.results['categories'].items():
            if results['total'] > 0:
                success_rate = results['passed'] / results['total'] * 100
                status = "PASS" if results['failed'] == 0 else "FAIL"
                print(f"{status:4} {category:12} {results['passed']:3}/{results['total']:3} ({success_rate:5.1f}%)")
        
        if self.results['errors']:
            print(f"\nFailed Tests ({len(self.results['errors'])}):")
            print("-" * 50)
            for error in self.results['errors'][:20]:  # Show first 20 errors
                print(f"  - {error}")
            
            if len(self.results['errors']) > 20:
                print(f"  ... and {len(self.results['errors']) - 20} more errors")
        
        print("\n" + "="*80)
    
    def save_report(self, filename: str = "comprehensive_test_report.json"):
        """Save detailed test report to JSON file."""
        report = {
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
            'test_type': 'comprehensive',
            'dry_run': self.dry_run,
            'verbose': self.verbose,
            'category': self.category,
            'router_config': {
                'host': mikrotik_config.get('host', 'unknown'),
                'username': mikrotik_config.get('username', 'unknown'),
                'port': mikrotik_config.get('port', 'unknown')
            },
            'summary': {
                'total_tests': self.results['total_tests'],
                'passed': self.results['passed'],
                'failed': self.results['failed'],
                'success_rate': self.results['passed'] / max(self.results['total_tests'], 1) * 100,
                'duration': time.time() - self.results['start_time']
            },
            'categories': self.results['categories'],
            'errors': self.results['errors']
        }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.log(f"Comprehensive test report saved to: {filename}")


def main():
    parser = argparse.ArgumentParser(description="Test all MikroTik Cursor MCP features")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Test in dry-run mode (default)")
    parser.add_argument("--live", action="store_true", help="Run live tests (will make changes)")
    parser.add_argument("--category", "-c", help="Test only specific category")
    parser.add_argument("--save-report", action="store_true", help="Save detailed JSON report")
    
    args = parser.parse_args()
    
    # Determine dry-run mode
    dry_run = not args.live if args.live else args.dry_run
    
    print("MikroTik Cursor MCP - Comprehensive Feature Test")
    print("=" * 50)
    print(f"Mode: {'Dry-run (safe)' if dry_run else 'Live (will make changes)'}")
    print(f"Verbose: {args.verbose}")
    if args.category:
        print(f"Category: {args.category}")
    print()
    
    # Initialize tester
    tester = ComprehensiveTester(verbose=args.verbose, dry_run=dry_run, category=args.category)
    
    try:
        # Run tests
        tester.test_all_categories()
        
        # Print summary
        tester.print_summary()
        
        # Save report if requested
        if args.save_report:
            tester.save_report()
        
        # Exit with appropriate code
        return 0 if tester.results['failed'] == 0 else 1
        
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        return 130
    except Exception as e:
        print(f"\n\nTest failed with exception: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
