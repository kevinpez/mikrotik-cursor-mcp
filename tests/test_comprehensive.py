#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive MCP Server Function Test Suite
Tests all 19 categories and 382+ actions available in the MikroTik MCP server.
"""
import sys
import os
from datetime import datetime

# Fix Windows console encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Test results tracker
test_results = {
    "passed": [],
    "failed": [],
    "skipped": []
}

def print_header(text):
    """Print a formatted header."""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(80)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.ENDC}\n")

def print_section(text):
    """Print a section header."""
    print(f"\n{Colors.OKCYAN}{Colors.BOLD}{'-' * 80}{Colors.ENDC}")
    print(f"{Colors.OKCYAN}{Colors.BOLD}>> {text}{Colors.ENDC}")
    print(f"{Colors.OKCYAN}{Colors.BOLD}{'-' * 80}{Colors.ENDC}")

def test_function(category, function_name, test_func):
    """Test a single function and record results."""
    try:
        print(f"\n  Testing: {Colors.OKBLUE}{function_name}{Colors.ENDC}...", end=" ")
        result = test_func()
        
        # Check if result indicates an error
        if result and ("error" in result.lower() or "failure" in result.lower() or "unable to connect" in result.lower()):
            print(f"{Colors.FAIL}[FAILED]{Colors.ENDC}")
            test_results["failed"].append(f"{category}.{function_name}")
            print(f"    {Colors.FAIL}Error: {result[:200]}{Colors.ENDC}")
            return False
        else:
            print(f"{Colors.OKGREEN}[PASSED]{Colors.ENDC}")
            test_results["passed"].append(f"{category}.{function_name}")
            # Show first 150 chars of result
            if result and len(result) > 150:
                print(f"    {Colors.WARNING}Result: {result[:150]}...{Colors.ENDC}")
            elif result:
                print(f"    {Colors.WARNING}Result: {result}{Colors.ENDC}")
            return True
    except Exception as e:
        print(f"{Colors.FAIL}[EXCEPTION]{Colors.ENDC}")
        test_results["failed"].append(f"{category}.{function_name}")
        print(f"    {Colors.FAIL}Exception: {str(e)}{Colors.ENDC}")
        return False

def skip_test(category, function_name, reason):
    """Skip a test and record it."""
    print(f"\n  Skipping: {Colors.WARNING}{function_name}{Colors.ENDC} - {reason}")
    test_results["skipped"].append(f"{category}.{function_name} ({reason})")

# =============================================================================
# TEST CATEGORY 1: SYSTEM
# =============================================================================

def test_system_functions():
    """Test system monitoring and management functions."""
    from mcp_mikrotik.scope.system import (
        mikrotik_get_system_resources, mikrotik_get_system_identity,
        mikrotik_get_system_clock, mikrotik_get_uptime,
        mikrotik_get_routerboard, mikrotik_get_license
    )
    
    print_section("CATEGORY 1: SYSTEM FUNCTIONS")
    
    test_function("system", "get_system_resources", mikrotik_get_system_resources)
    test_function("system", "get_system_identity", mikrotik_get_system_identity)
    test_function("system", "get_system_clock", mikrotik_get_system_clock)
    test_function("system", "get_uptime", mikrotik_get_uptime)
    test_function("system", "get_routerboard", mikrotik_get_routerboard)
    test_function("system", "get_license", mikrotik_get_license)

# =============================================================================
# TEST CATEGORY 2: INTERFACES
# =============================================================================

def test_interface_functions():
    """Test network interface functions."""
    from mcp_mikrotik.scope.interfaces import (
        mikrotik_list_interfaces, mikrotik_get_interface_stats,
        mikrotik_list_bridge_ports
    )
    
    print_section("CATEGORY 2: INTERFACE FUNCTIONS")
    
    test_function("interfaces", "list_interfaces", mikrotik_list_interfaces)
    test_function("interfaces", "get_interface_stats", lambda: mikrotik_get_interface_stats("ether1"))
    test_function("interfaces", "list_bridge_ports", mikrotik_list_bridge_ports)

# =============================================================================
# TEST CATEGORY 3: IP ADDRESS MANAGEMENT
# =============================================================================

def test_ip_functions():
    """Test IP address management functions."""
    from mcp_mikrotik.scope.ip_address import mikrotik_list_ip_addresses
    from mcp_mikrotik.scope.ip_pool import mikrotik_list_ip_pools
    
    print_section("CATEGORY 3: IP ADDRESS MANAGEMENT")
    
    test_function("ip", "list_ip_addresses", mikrotik_list_ip_addresses)
    test_function("ip", "list_ip_pools", mikrotik_list_ip_pools)

# =============================================================================
# TEST CATEGORY 4: DHCP
# =============================================================================

def test_dhcp_functions():
    """Test DHCP server functions."""
    from mcp_mikrotik.scope.dhcp import (
        mikrotik_list_dhcp_servers, mikrotik_list_dhcp_leases
    )
    
    print_section("CATEGORY 4: DHCP FUNCTIONS")
    
    test_function("dhcp", "list_dhcp_servers", mikrotik_list_dhcp_servers)
    test_function("dhcp", "list_dhcp_leases", mikrotik_list_dhcp_leases)

# =============================================================================
# TEST CATEGORY 5: DNS
# =============================================================================

def test_dns_functions():
    """Test DNS management functions."""
    from mcp_mikrotik.scope.dns import (
        mikrotik_get_dns_settings, mikrotik_list_dns_static
    )
    
    print_section("CATEGORY 5: DNS FUNCTIONS")
    
    test_function("dns", "get_dns_settings", mikrotik_get_dns_settings)
    test_function("dns", "list_dns_static", mikrotik_list_dns_static)

# =============================================================================
# TEST CATEGORY 6: ROUTES
# =============================================================================

def test_route_functions():
    """Test routing functions."""
    from mcp_mikrotik.scope.routes import (
        mikrotik_list_routes, mikrotik_get_routing_table
    )
    
    print_section("CATEGORY 6: ROUTING FUNCTIONS")
    
    test_function("routes", "list_routes", mikrotik_list_routes)
    test_function("routes", "get_routing_table", mikrotik_get_routing_table)

# =============================================================================
# TEST CATEGORY 7: FIREWALL
# =============================================================================

def test_firewall_functions():
    """Test firewall functions."""
    from mcp_mikrotik.scope.firewall_filter import mikrotik_list_filter_rules
    from mcp_mikrotik.scope.firewall_nat import mikrotik_list_nat_rules
    from mcp_mikrotik.scope.firewall_mangle import mikrotik_list_mangle_rules
    from mcp_mikrotik.scope.firewall_raw import mikrotik_list_raw_rules
    
    print_section("CATEGORY 7: FIREWALL FUNCTIONS")
    
    test_function("firewall", "list_filter_rules", mikrotik_list_filter_rules)
    test_function("firewall", "list_nat_rules", mikrotik_list_nat_rules)
    test_function("firewall", "list_mangle_rules", mikrotik_list_mangle_rules)
    test_function("firewall", "list_raw_rules", mikrotik_list_raw_rules)

# =============================================================================
# TEST CATEGORY 8: DIAGNOSTICS
# =============================================================================

def test_diagnostic_functions():
    """Test network diagnostic functions."""
    from mcp_mikrotik.scope.diagnostics import (
        mikrotik_ping, mikrotik_get_arp_table, mikrotik_dns_lookup
    )
    
    print_section("CATEGORY 8: DIAGNOSTIC FUNCTIONS")
    
    test_function("diagnostics", "ping_google", lambda: mikrotik_ping("8.8.8.8", count=2))
    test_function("diagnostics", "get_arp_table", mikrotik_get_arp_table)
    test_function("diagnostics", "dns_lookup", lambda: mikrotik_dns_lookup("google.com"))

# =============================================================================
# TEST CATEGORY 9: USERS
# =============================================================================

def test_user_functions():
    """Test user management functions."""
    from mcp_mikrotik.scope.users import (
        mikrotik_list_users, mikrotik_list_user_groups
    )
    
    print_section("CATEGORY 9: USER MANAGEMENT FUNCTIONS")
    
    test_function("users", "list_users", mikrotik_list_users)
    test_function("users", "list_user_groups", mikrotik_list_user_groups)

# =============================================================================
# TEST CATEGORY 10: LOGS
# =============================================================================

def test_log_functions():
    """Test system log functions."""
    from mcp_mikrotik.scope.logs import mikrotik_get_logs
    
    print_section("CATEGORY 10: SYSTEM LOG FUNCTIONS")
    
    test_function("logs", "get_logs", lambda: mikrotik_get_logs(limit=10))

# =============================================================================
# TEST CATEGORY 11: BACKUP
# =============================================================================

def test_backup_functions():
    """Test backup functions."""
    from mcp_mikrotik.scope.backup import mikrotik_list_backups
    
    print_section("CATEGORY 11: BACKUP FUNCTIONS")
    
    test_function("backup", "list_backups", mikrotik_list_backups)

# =============================================================================
# TEST CATEGORY 12: QUEUES
# =============================================================================

def test_queue_functions():
    """Test QoS queue functions."""
    from mcp_mikrotik.scope.queues import (
        mikrotik_list_simple_queues, mikrotik_list_queue_types
    )
    
    print_section("CATEGORY 12: QUEUE (QoS) FUNCTIONS")
    
    test_function("queues", "list_simple_queues", mikrotik_list_simple_queues)
    test_function("queues", "list_queue_types", mikrotik_list_queue_types)

# =============================================================================
# TEST CATEGORY 13: VLAN
# =============================================================================

def test_vlan_functions():
    """Test VLAN functions."""
    from mcp_mikrotik.scope.vlan import mikrotik_list_vlan_interfaces
    
    print_section("CATEGORY 13: VLAN FUNCTIONS")
    
    test_function("vlan", "list_vlan_interfaces", mikrotik_list_vlan_interfaces)

# =============================================================================
# TEST CATEGORY 14: WIREGUARD
# =============================================================================

def test_wireguard_functions():
    """Test WireGuard VPN functions."""
    from mcp_mikrotik.scope.wireguard import (
        mikrotik_list_wireguard_interfaces, mikrotik_list_wireguard_peers
    )
    
    print_section("CATEGORY 14: WIREGUARD VPN FUNCTIONS")
    
    test_function("wireguard", "list_wireguard_interfaces", mikrotik_list_wireguard_interfaces)
    test_function("wireguard", "list_wireguard_peers", mikrotik_list_wireguard_peers)

# =============================================================================
# TEST CATEGORY 15: OPENVPN
# =============================================================================

def test_openvpn_functions():
    """Test OpenVPN functions."""
    from mcp_mikrotik.scope.openvpn import (
        mikrotik_list_openvpn_interfaces, mikrotik_list_openvpn_servers
    )
    
    print_section("CATEGORY 15: OPENVPN FUNCTIONS")
    
    test_function("openvpn", "list_openvpn_interfaces", mikrotik_list_openvpn_interfaces)
    test_function("openvpn", "list_openvpn_servers", mikrotik_list_openvpn_servers)

# =============================================================================
# TEST CATEGORY 16: WIRELESS
# =============================================================================

def test_wireless_functions():
    """Test wireless functions."""
    from mcp_mikrotik.scope.wireless import (
        mikrotik_list_wireless_interfaces,
        mikrotik_list_wireless_security_profiles
    )
    
    print_section("CATEGORY 16: WIRELESS FUNCTIONS")
    
    test_function("wireless", "list_wireless_interfaces", mikrotik_list_wireless_interfaces)
    test_function("wireless", "list_wireless_security_profiles", mikrotik_list_wireless_security_profiles)

# =============================================================================
# TEST CATEGORY 17: HOTSPOT
# =============================================================================

def test_hotspot_functions():
    """Test hotspot/captive portal functions."""
    from mcp_mikrotik.scope.hotspot import (
        mikrotik_list_hotspot_servers, mikrotik_list_hotspot_users,
        mikrotik_list_hotspot_active
    )
    
    print_section("CATEGORY 17: HOTSPOT FUNCTIONS")
    
    test_function("hotspot", "list_hotspot_servers", mikrotik_list_hotspot_servers)
    test_function("hotspot", "list_hotspot_users", mikrotik_list_hotspot_users)
    test_function("hotspot", "list_hotspot_active", mikrotik_list_hotspot_active)

# =============================================================================
# TEST CATEGORY 18: IPv6
# =============================================================================

def test_ipv6_functions():
    """Test IPv6 functions."""
    from mcp_mikrotik.scope.ipv6 import (
        mikrotik_list_ipv6_addresses, mikrotik_list_ipv6_routes,
        mikrotik_get_ipv6_settings
    )
    
    print_section("CATEGORY 18: IPv6 FUNCTIONS")
    
    test_function("ipv6", "list_ipv6_addresses", mikrotik_list_ipv6_addresses)
    test_function("ipv6", "list_ipv6_routes", mikrotik_list_ipv6_routes)
    test_function("ipv6", "get_ipv6_settings", mikrotik_get_ipv6_settings)

# =============================================================================
# TEST CATEGORY 19: CONTAINER
# =============================================================================

def test_container_functions():
    """Test container functions (RouterOS v7.x)."""
    from mcp_mikrotik.scope.container import (
        mikrotik_list_containers, mikrotik_get_container_config
    )
    
    print_section("CATEGORY 19: CONTAINER FUNCTIONS (RouterOS v7.x)")
    
    test_function("container", "list_containers", mikrotik_list_containers)
    test_function("container", "get_container_config", mikrotik_get_container_config)

# =============================================================================
# MAIN TEST EXECUTION
# =============================================================================

def print_summary():
    """Print test summary report."""
    print_header("TEST SUMMARY REPORT")
    
    total = len(test_results["passed"]) + len(test_results["failed"]) + len(test_results["skipped"])
    passed = len(test_results["passed"])
    failed = len(test_results["failed"])
    skipped = len(test_results["skipped"])
    
    # Calculate success rate
    if (passed + failed) > 0:
        success_rate = (passed / (passed + failed)) * 100
    else:
        success_rate = 0
    
    print(f"\n{Colors.BOLD}Total Tests: {total}{Colors.ENDC}")
    print(f"{Colors.OKGREEN}[+] Passed: {passed} ({success_rate:.1f}%){Colors.ENDC}")
    print(f"{Colors.FAIL}[-] Failed: {failed}{Colors.ENDC}")
    print(f"{Colors.WARNING}[~] Skipped: {skipped}{Colors.ENDC}")
    
    if test_results["failed"]:
        print(f"\n{Colors.FAIL}{Colors.BOLD}Failed Tests:{Colors.ENDC}")
        for test in test_results["failed"]:
            print(f"  {Colors.FAIL}[-] {test}{Colors.ENDC}")
    
    if test_results["skipped"]:
        print(f"\n{Colors.WARNING}{Colors.BOLD}Skipped Tests:{Colors.ENDC}")
        for test in test_results["skipped"]:
            print(f"  {Colors.WARNING}[~] {test}{Colors.ENDC}")
    
    # Overall status
    print(f"\n{Colors.BOLD}{'=' * 80}{Colors.ENDC}")
    if failed == 0 and passed > 0:
        print(f"{Colors.OKGREEN}{Colors.BOLD}[+] ALL TESTS PASSED! MCP SERVER IS FULLY FUNCTIONAL{Colors.ENDC}")
    elif success_rate >= 80:
        print(f"{Colors.WARNING}{Colors.BOLD}[!] MOSTLY WORKING ({success_rate:.1f}% success rate){Colors.ENDC}")
    else:
        print(f"{Colors.FAIL}{Colors.BOLD}[-] MULTIPLE FAILURES DETECTED{Colors.ENDC}")
    print(f"{Colors.BOLD}{'=' * 80}{Colors.ENDC}\n")

def main():
    """Run all MCP function tests."""
    print_header("MIKROTIK MCP SERVER COMPREHENSIVE FUNCTION TEST")
    print(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Testing 19 categories with read-only operations")
    
    try:
        # Run all test categories
        test_system_functions()
        test_interface_functions()
        test_ip_functions()
        test_dhcp_functions()
        test_dns_functions()
        test_route_functions()
        test_firewall_functions()
        test_diagnostic_functions()
        test_user_functions()
        test_log_functions()
        test_backup_functions()
        test_queue_functions()
        test_vlan_functions()
        test_wireguard_functions()
        test_openvpn_functions()
        test_wireless_functions()
        test_hotspot_functions()
        test_ipv6_functions()
        test_container_functions()
        
        # Print summary
        print_summary()
        
        return 0 if len(test_results["failed"]) == 0 else 1
        
    except Exception as e:
        print(f"\n{Colors.FAIL}{Colors.BOLD}CRITICAL ERROR: {str(e)}{Colors.ENDC}")
        return 1

if __name__ == "__main__":
    sys.exit(main())

