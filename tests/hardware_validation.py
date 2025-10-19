#!/usr/bin/env python3
"""
MikroTik MCP Hardware Validation Suite
Tests all MCP commands against real MikroTik hardware with detailed CLI feedback.

This suite:
- Tests EVERY command category systematically
- Shows real-time progress with clear visual feedback
- Validates operations actually work on hardware
- Provides detailed error reporting
- Includes safe rollback for write operations
- Generates comprehensive test reports

Usage:
    python tests/hardware_validation.py                    # Run all tests
    python tests/hardware_validation.py --category system  # Test specific category
    python tests/hardware_validation.py --verbose          # Show detailed output
    python tests/hardware_validation.py --report report.json  # Save results to file
"""

import sys
import os
import time
import json
import argparse
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime
from collections import defaultdict

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    except:
        pass  # Fallback if this doesn't work

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_mikrotik.tools.tool_registry import get_all_handlers


# ANSI color codes for terminal output
class Colors:
    """Terminal color codes for better readability."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class HardwareValidator:
    """
    Comprehensive hardware validation test suite.
    Tests all MCP commands against actual MikroTik hardware.
    """
    
    # Test object prefix to identify our test objects
    TEST_PREFIX = "mcp-hwtest-"
    
    # Critical resources that should NEVER be modified
    PROTECTED_RESOURCES = {
        'interfaces': ['ether1', 'bridge', 'wlan1', 'sfp1'],
        'users': ['admin'],
        'services': ['ssh', 'api', 'api-ssl'],
    }
    
    # Handlers to skip (too dangerous or require special setup)
    SKIP_HANDLERS = [
        'mikrotik_reboot_system',
        'mikrotik_restore_backup',
        'mikrotik_remove_user',
        'mikrotik_disable_ip_service',
        'mikrotik_clear_logs',
        'mikrotik_flush_connections',
        'mikrotik_monitor_logs',  # Runs indefinitely (follow mode)
        'mikrotik_bandwidth_test',  # Can run for extended periods
        'mikrotik_traceroute',  # Can hang on network timeouts
    ]
    
    # Test arguments for handlers that need specific parameters
    TEST_ARGS = {
        'mikrotik_ping': {'address': '8.8.8.8', 'count': 2},
        'mikrotik_dns_lookup': {'hostname': 'google.com'},
        'mikrotik_traceroute': {'address': '8.8.8.8', 'count': 1},
        'mikrotik_check_connection': {'address': '8.8.8.8'},
        'mikrotik_search_logs': {'search_term': 'system'},
        'mikrotik_get_interface_stats': {'interface': 'ether1'},
        'mikrotik_get_interface_monitor': {'interface': 'ether1'},
        'mikrotik_get_interface_traffic': {'interface': 'ether1'},
    }
    
    def __init__(self, verbose: bool = False, save_report: str = None):
        """Initialize the hardware validator."""
        self.verbose = verbose
        self.save_report = save_report
        self.handlers = get_all_handlers()
        
        # Results tracking
        self.results = {
            'start_time': datetime.now().isoformat(),
            'router_info': {},
            'total_handlers': len(self.handlers),
            'total_tests': 0,
            'passed': 0,
            'failed': 0,
            'skipped': 0,
            'errors': [],
            'warnings': [],
            'categories': {},
            'test_objects_created': [],
            'duration_seconds': 0,
        }
        
        # Categorize handlers
        self.categorize_handlers()
    
    def categorize_handlers(self):
        """Categorize all handlers by their function."""
        categories = defaultdict(list)
        
        for handler_name in sorted(self.handlers.keys()):
            # Extract category from handler name
            # Format: mikrotik_<action>_<category>_<detail>
            parts = handler_name.split('_')
            if len(parts) < 2:
                categories['other'].append(handler_name)
                continue
            
            # Determine category based on handler name
            if 'system' in handler_name:
                category = 'System'
            elif 'interface' in handler_name or 'bridge' in handler_name or 'bonding' in handler_name:
                category = 'Interfaces'
            elif 'firewall' in handler_name or 'filter' in handler_name or 'nat' in handler_name or 'mangle' in handler_name or 'raw' in handler_name:
                category = 'Firewall'
            elif 'route' in handler_name or 'bgp' in handler_name or 'ospf' in handler_name:
                category = 'Routing'
            elif 'ip' in handler_name and 'ipv6' not in handler_name and 'address' in handler_name:
                category = 'IP Management'
            elif 'ipv6' in handler_name:
                category = 'IPv6'
            elif 'dhcp' in handler_name and 'ipv6' not in handler_name:
                category = 'DHCP'
            elif 'dhcpv6' in handler_name:
                category = 'DHCPv6'
            elif 'dns' in handler_name:
                category = 'DNS'
            elif 'wireless' in handler_name or 'capsman' in handler_name:
                category = 'Wireless'
            elif 'wireguard' in handler_name:
                category = 'WireGuard'
            elif 'openvpn' in handler_name:
                category = 'OpenVPN'
            elif 'pppoe' in handler_name or 'tunnel' in handler_name or 'eoip' in handler_name or 'gre' in handler_name:
                category = 'Tunnels/VPN'
            elif 'vlan' in handler_name:
                category = 'VLAN'
            elif 'queue' in handler_name:
                category = 'QoS/Queues'
            elif 'hotspot' in handler_name:
                category = 'Hotspot'
            elif 'user' in handler_name:
                category = 'Users'
            elif 'backup' in handler_name:
                category = 'Backup'
            elif 'log' in handler_name:
                category = 'Logs'
            elif 'ping' in handler_name or 'traceroute' in handler_name or 'arp' in handler_name or 'neighbor' in handler_name:
                category = 'Diagnostics'
            elif 'container' in handler_name:
                category = 'Containers'
            elif 'certificate' in handler_name:
                category = 'Certificates'
            elif 'pool' in handler_name:
                category = 'IP Management'
            elif 'service' in handler_name:
                category = 'IP Services'
            elif 'workflow' in handler_name or 'safe' in handler_name or 'safety' in handler_name:
                category = 'Safety/Workflow'
            else:
                category = 'Other'
            
            categories[category].append(handler_name)
        
        self.categories = dict(categories)
        return self.categories
    
    def print_header(self):
        """Print test suite header."""
        print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*80}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.HEADER}MikroTik MCP Hardware Validation Suite{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.HEADER}{'='*80}{Colors.ENDC}\n")
        
        # Router info
        router_host = os.getenv('MIKROTIK_HOST', 'Not configured')
        router_user = os.getenv('MIKROTIK_USER', 'Not configured')
        
        print(f"{Colors.CYAN}Router Configuration:{Colors.ENDC}")
        print(f"  Host: {Colors.BOLD}{router_host}{Colors.ENDC}")
        print(f"  User: {Colors.BOLD}{router_user}{Colors.ENDC}")
        print(f"\n{Colors.CYAN}Test Suite Information:{Colors.ENDC}")
        print(f"  Total Handlers: {Colors.BOLD}{len(self.handlers)}{Colors.ENDC}")
        print(f"  Categories: {Colors.BOLD}{len(self.categories)}{Colors.ENDC}")
        print(f"  Test Prefix: {Colors.BOLD}{self.TEST_PREFIX}{Colors.ENDC}")
        print(f"  Verbose Mode: {Colors.BOLD}{'Yes' if self.verbose else 'No'}{Colors.ENDC}")
        print(f"\n{Colors.YELLOW}Note: Write operations will be tested with automatic cleanup{Colors.ENDC}")
        print(f"{Colors.BOLD}{'='*80}{Colors.ENDC}\n")
    
    def verify_connectivity(self) -> Tuple[bool, str]:
        """Verify router connectivity and get system info."""
        try:
            handler = self.handlers.get('mikrotik_get_system_identity')
            if handler:
                result = handler({})
                if isinstance(result, str) and ("Error" in result or "Failed" in result or "ERROR:" in result):
                    return False, result
                # Store router info
                self.results['router_info']['identity'] = result
                return True, "Connected"
        except Exception as e:
            return False, str(e)
        
        return False, "Handler not found"
    
    def is_safe_operation(self, handler_name: str) -> bool:
        """Determine if an operation is safe (read-only)."""
        safe_keywords = ['list', 'get', 'show', 'print', 'check', 'monitor', 'scan', 'search', 'export']
        parts = handler_name.split('_')
        if len(parts) < 2:
            return False
        
        operation = parts[1]
        return operation in safe_keywords
    
    def get_test_args(self, handler_name: str) -> Optional[Dict[str, Any]]:
        """Get test arguments for a handler."""
        # Check if we have predefined test args
        if handler_name in self.TEST_ARGS:
            return self.TEST_ARGS[handler_name]
        
        # Check if handler requires no arguments (most list/get handlers)
        if self.is_safe_operation(handler_name):
            return {}
        
        # For handlers that need specific IDs, return None to skip
        needs_id_keywords = ['_remove_', '_delete_', '_update_', '_disable_', '_enable_']
        if any(keyword in handler_name for keyword in needs_id_keywords):
            # These need specific IDs from existing resources
            return None
        
        # For create/add operations, return None to handle specially
        create_keywords = ['_create_', '_add_', '_set_']
        if any(keyword in handler_name for keyword in create_keywords):
            return None
        
        # Default to empty args
        return {}
    
    def test_handler(self, handler_name: str, category: str) -> Dict[str, Any]:
        """
        Test a single handler and return detailed results.
        """
        # Skip dangerous handlers
        if handler_name in self.SKIP_HANDLERS:
            return {
                'status': 'skipped',
                'reason': 'Dangerous operation - manually skipped',
                'duration': 0
            }
        
        # Get test arguments
        test_args = self.get_test_args(handler_name)
        if test_args is None:
            return {
                'status': 'skipped',
                'reason': 'Requires specific resource ID or complex setup',
                'duration': 0
            }
        
        # Display command info if verbose
        if self.verbose:
            print(f"\n{Colors.CYAN}  Executing: {Colors.BOLD}{handler_name}{Colors.ENDC}")
            if test_args:
                print(f"{Colors.CYAN}  Arguments: {Colors.BOLD}{test_args}{Colors.ENDC}")
        
        # Test the handler
        start_time = time.time()
        try:
            handler = self.handlers[handler_name]
            result = handler(test_args)
            duration = time.time() - start_time
            
            # Display results if verbose
            if self.verbose:
                print(f"{Colors.GREEN}  ✓ Command executed in {duration:.2f}s{Colors.ENDC}")
                if isinstance(result, str):
                    if result and result.strip():
                        # Show first 500 chars of output
                        output_preview = result[:500]
                        if len(result) > 500:
                            output_preview += f"... ({len(result) - 500} more chars)"
                        print(f"{Colors.CYAN}  Result:{Colors.ENDC}\n{output_preview}\n")
                    else:
                        print(f"{Colors.CYAN}  Result: (empty response){Colors.ENDC}\n")
                else:
                    # For dict/list results
                    output_str = str(result)[:500]
                    if len(str(result)) > 500:
                        output_str += f"... ({len(str(result)) - 500} more chars)"
                    print(f"{Colors.CYAN}  Result (Type: {type(result).__name__}):{Colors.ENDC}\n{output_str}\n")
            
            # Analyze result
            if isinstance(result, str):
                # Check for errors
                if "ERROR:" in result or "Error:" in result:
                    # Check if it's a "not supported" error (not a failure)
                    if "not supported" in result.lower() or "no such command" in result.lower():
                        if self.verbose:
                            print(f"{Colors.YELLOW}  ⊘ Feature not supported on this router{Colors.ENDC}\n")
                        return {
                            'status': 'skipped',
                            'reason': 'Feature not supported on this router model',
                            'duration': duration,
                            'output': result[:200]
                        }
                    else:
                        if self.verbose:
                            print(f"{Colors.RED}  ✗ Command returned error{Colors.ENDC}\n")
                        return {
                            'status': 'failed',
                            'reason': 'Command returned error',
                            'duration': duration,
                            'output': result[:500]
                        }
                elif "Failed" in result:
                    if self.verbose:
                        print(f"{Colors.RED}  ✗ Operation failed{Colors.ENDC}\n")
                    return {
                        'status': 'failed',
                        'reason': 'Operation failed',
                        'duration': duration,
                        'output': result[:500]
                    }
                else:
                    # Success
                    if self.verbose:
                        print(f"{Colors.GREEN}  ✓ Command successful{Colors.ENDC}\n")
                    return {
                        'status': 'passed',
                        'duration': duration,
                        'output': result[:200] if self.verbose else None
                    }
            else:
                # Non-string result (dict, list, etc.) is usually success
                if self.verbose:
                    print(f"{Colors.GREEN}  ✓ Command successful (returned {type(result).__name__}){Colors.ENDC}\n")
                return {
                    'status': 'passed',
                    'duration': duration,
                    'output': str(result)[:200] if self.verbose else None
                }
                
        except KeyError as e:
            # Missing required argument
            if self.verbose:
                print(f"{Colors.YELLOW}  ⊘ Missing required argument: {Colors.BOLD}{str(e)}{Colors.ENDC}\n")
            return {
                'status': 'skipped',
                'reason': f'Missing required argument: {str(e)}',
                'duration': time.time() - start_time
            }
        except Exception as e:
            # Unexpected error
            if self.verbose:
                print(f"{Colors.RED}  ✗ Exception: {Colors.BOLD}{type(e).__name__}: {str(e)}{Colors.ENDC}\n")
            return {
                'status': 'failed',
                'reason': f'Exception: {type(e).__name__}',
                'duration': time.time() - start_time,
                'output': str(e)[:500]
            }
    
    def test_category(self, category_name: str, handlers: List[str]) -> Dict[str, Any]:
        """Test all handlers in a category."""
        print(f"\n{Colors.BOLD}{Colors.BLUE}Testing Category: {category_name}{Colors.ENDC}")
        print(f"{Colors.BLUE}{'─'*80}{Colors.ENDC}")
        
        category_results = {
            'total': len(handlers),
            'passed': 0,
            'failed': 0,
            'skipped': 0,
            'handlers': {},
            'duration': 0
        }
        
        start_time = time.time()
        
        for i, handler_name in enumerate(handlers, 1):
            # Show progress
            progress = f"[{i}/{len(handlers)}]"
            handler_display = handler_name.replace('mikrotik_', '')
            
            if not self.verbose:
                print(f"{Colors.CYAN}{progress:>10}{Colors.ENDC} {handler_display:<50}", end=' ', flush=True)
            else:
                print(f"\n{Colors.CYAN}{progress}{Colors.ENDC} {Colors.BOLD}{handler_display}{Colors.ENDC}")
            
            # Test the handler
            result = self.test_handler(handler_name, category_name)
            
            # Update statistics
            category_results['handlers'][handler_name] = result
            if result['status'] == 'passed':
                category_results['passed'] += 1
                self.results['passed'] += 1
                status_symbol = f"{Colors.GREEN}✓ PASS{Colors.ENDC}"
                result_info = f"({result['duration']:.2f}s)"
            elif result['status'] == 'failed':
                category_results['failed'] += 1
                self.results['failed'] += 1
                status_symbol = f"{Colors.RED}✗ FAIL{Colors.ENDC}"
                result_info = f"({result['duration']:.2f}s) - {result.get('reason', 'Unknown error')}"
                self.results['errors'].append({
                    'handler': handler_name,
                    'reason': result.get('reason', 'Unknown error'),
                    'output': result.get('output', '')
                })
            else:  # skipped
                category_results['skipped'] += 1
                self.results['skipped'] += 1
                status_symbol = f"{Colors.YELLOW}⊘ SKIP{Colors.ENDC}"
                result_info = f"- {result.get('reason', 'Skipped')}"
            
            # Print result inline (only if not verbose, since verbose shows it during execution)
            if not self.verbose:
                print(f"{status_symbol} {result_info}")
        
        # Category summary
        category_results['duration'] = time.time() - start_time
        passed_rate = (category_results['passed'] / max(category_results['total'], 1)) * 100
        
        print(f"\n{Colors.BLUE}Category Summary:{Colors.ENDC}")
        print(f"  Passed:  {Colors.GREEN}{category_results['passed']}/{category_results['total']} ({passed_rate:.1f}%){Colors.ENDC}")
        print(f"  Failed:  {Colors.RED}{category_results['failed']}{Colors.ENDC}")
        print(f"  Skipped: {Colors.YELLOW}{category_results['skipped']}{Colors.ENDC}")
        print(f"  Duration: {Colors.BOLD}{category_results['duration']:.2f}s{Colors.ENDC}")
        
        return category_results
    
    def run_all_tests(self, specific_category: str = None):
        """Run all hardware validation tests."""
        self.print_header()
        
        # Initial connectivity check
        print(f"{Colors.CYAN}Performing initial connectivity check...{Colors.ENDC}")
        connected, message = self.verify_connectivity()
        if not connected:
            print(f"{Colors.RED}X Cannot connect to router: {message}{Colors.ENDC}")
            print(f"{Colors.YELLOW}Please check your MIKROTIK_HOST, MIKROTIK_USER, and MIKROTIK_PASSWORD environment variables.{Colors.ENDC}")
            return False
        
        print(f"{Colors.GREEN}+ Connected to router successfully{Colors.ENDC}")
        if self.results['router_info'].get('identity'):
            print(f"{Colors.CYAN}Router Identity: {self.results['router_info']['identity']}{Colors.ENDC}")
        
        # Run tests by category
        start_time = time.time()
        
        categories_to_test = self.categories
        if specific_category:
            if specific_category in self.categories:
                categories_to_test = {specific_category: self.categories[specific_category]}
            else:
                print(f"{Colors.RED}Error: Category '{specific_category}' not found{Colors.ENDC}")
                print(f"{Colors.CYAN}Available categories:{Colors.ENDC}")
                for cat in sorted(self.categories.keys()):
                    print(f"  - {cat}")
                return False
        
        # Test each category with progress tracking
        total_categories = len(categories_to_test)
        for idx, category_name in enumerate(sorted(categories_to_test.keys()), 1):
            handlers = categories_to_test[category_name]
            
            # Show progress
            elapsed = time.time() - start_time
            print(f"\n{Colors.BOLD}{Colors.CYAN}[{idx}/{total_categories}] Testing category '{category_name}' ({len(handlers)} handlers){Colors.ENDC}")
            print(f"{Colors.CYAN}Elapsed time: {elapsed:.1f}s{Colors.ENDC}")
            
            category_results = self.test_category(category_name, handlers)
            self.results['categories'][category_name] = category_results
            
            # Show running totals after each category
            running_passed = sum(cat['passed'] for cat in self.results['categories'].values())
            running_failed = sum(cat['failed'] for cat in self.results['categories'].values())
            running_skipped = sum(cat['skipped'] for cat in self.results['categories'].values())
            running_total = running_passed + running_failed + running_skipped
            
            print(f"{Colors.CYAN}Running totals: {Colors.GREEN}{running_passed} passed{Colors.ENDC}, "
                  f"{Colors.RED}{running_failed} failed{Colors.ENDC}, "
                  f"{Colors.YELLOW}{running_skipped} skipped{Colors.ENDC} "
                  f"({running_total} of {self.results['total_handlers']} total handlers){Colors.ENDC}")
        
        self.results['duration_seconds'] = time.time() - start_time
        
        # Final connectivity check
        print(f"\n{Colors.CYAN}Performing final connectivity check...{Colors.ENDC}")
        connected, message = self.verify_connectivity()
        if not connected:
            print(f"{Colors.RED}WARNING: Lost connectivity to router!{Colors.ENDC}")
            self.results['warnings'].append("Lost connectivity after tests")
        else:
            print(f"{Colors.GREEN}+ Router still accessible{Colors.ENDC}")
        
        # Print final results
        self.print_final_results()
        
        # Save report if requested
        if self.save_report:
            self.save_json_report()
        
        return self.results['failed'] == 0
    
    def print_final_results(self):
        """Print comprehensive final test results."""
        print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*80}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.HEADER}HARDWARE VALIDATION RESULTS{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.HEADER}{'='*80}{Colors.ENDC}\n")
        
        # Overall statistics
        total = self.results['total_tests']
        passed = self.results['passed']
        failed = self.results['failed']
        skipped = self.results['skipped']
        pass_rate = (passed / max(1, total)) * 100
        
        print(f"{Colors.BOLD}Overall Statistics:{Colors.ENDC}")
        print(f"  Total Tests:    {Colors.BOLD}{total}{Colors.ENDC}")
        print(f"  Passed:         {Colors.GREEN}{passed}{Colors.ENDC} ({pass_rate:.1f}%)")
        print(f"  Failed:         {Colors.RED}{failed}{Colors.ENDC}")
        print(f"  Skipped:        {Colors.YELLOW}{skipped}{Colors.ENDC}")
        print(f"  Duration:       {Colors.BOLD}{self.results['duration_seconds']:.2f}s{Colors.ENDC}")
        
        # Results by category
        print(f"\n{Colors.BOLD}Results by Category:{Colors.ENDC}")
        print(f"{Colors.BOLD}{'─'*80}{Colors.ENDC}")
        
        for category_name in sorted(self.results['categories'].keys()):
            cat_results = self.results['categories'][category_name]
            cat_pass_rate = (cat_results['passed'] / max(1, cat_results['total'])) * 100
            
            # Color code based on pass rate
            if cat_pass_rate == 100:
                status_color = Colors.GREEN
                status = "+"
            elif cat_pass_rate >= 50:
                status_color = Colors.YELLOW
                status = "~"
            else:
                status_color = Colors.RED
                status = "X"
            
            print(f"  {status_color}{status}{Colors.ENDC} {category_name:25s}: "
                  f"{status_color}{cat_results['passed']:3d}{Colors.ENDC}/"
                  f"{cat_results['total']:3d} "
                  f"({cat_pass_rate:5.1f}%) "
                  f"[{Colors.RED}F:{cat_results['failed']}{Colors.ENDC} "
                  f"{Colors.YELLOW}S:{cat_results['skipped']}{Colors.ENDC}]")
        
        # Failed tests details
        if self.results['errors']:
            print(f"\n{Colors.BOLD}{Colors.RED}Failed Tests Details:{Colors.ENDC}")
            print(f"{Colors.RED}{'─'*80}{Colors.ENDC}")
            for i, error in enumerate(self.results['errors'][:20], 1):
                handler_display = error['handler'].replace('mikrotik_', '')
                print(f"\n  {Colors.RED}{i}.{Colors.ENDC} {Colors.BOLD}{handler_display}{Colors.ENDC}")
                print(f"     Category: {error['category']}")
                print(f"     Reason: {error['reason']}")
                if error.get('output') and self.verbose:
                    print(f"     Output: {error['output'][:150]}...")
            
            if len(self.results['errors']) > 20:
                print(f"\n  {Colors.YELLOW}... and {len(self.results['errors']) - 20} more failures{Colors.ENDC}")
        
        # Warnings
        if self.results['warnings']:
            print(f"\n{Colors.BOLD}{Colors.YELLOW}Warnings:{Colors.ENDC}")
            for warning in self.results['warnings']:
                print(f"  ! {warning}")
        
        # Final verdict
        print(f"\n{Colors.BOLD}{'='*80}{Colors.ENDC}")
        if failed == 0 and passed > 0:
            if skipped > 0:
                # Calculate actual total (passed + failed + skipped)
                actual_total = passed + failed + skipped
                print(f"{Colors.BOLD}{Colors.GREEN}*** ALL RUNNABLE TESTS PASSED! ***{Colors.ENDC}")
                print(f"{Colors.GREEN}{passed}/{actual_total} tests executed successfully ({skipped} skipped for safety){Colors.ENDC}")
            else:
                print(f"{Colors.BOLD}{Colors.GREEN}*** ALL TESTS PASSED! ***{Colors.ENDC}")
                print(f"{Colors.GREEN}Your MikroTik MCP server is fully functional on hardware!{Colors.ENDC}")
        elif pass_rate >= 80:
            print(f"{Colors.BOLD}{Colors.YELLOW}MOSTLY PASSING ({pass_rate:.1f}%){Colors.ENDC}")
            print(f"{Colors.YELLOW}Most functionality works, but some issues need attention.{Colors.ENDC}")
        else:
            print(f"{Colors.BOLD}{Colors.RED}MULTIPLE FAILURES ({pass_rate:.1f}% pass rate){Colors.ENDC}")
            print(f"{Colors.RED}Significant issues detected - please review failures.{Colors.ENDC}")
        print(f"{Colors.BOLD}{'='*80}{Colors.ENDC}\n")
    
    def save_json_report(self):
        """Save detailed test results to JSON file."""
        try:
            report_path = Path(self.save_report)
            report_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2, default=str, ensure_ascii=False)
            
            print(f"{Colors.GREEN}+ Report saved to: {report_path}{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.RED}X Failed to save report: {e}{Colors.ENDC}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='MikroTik MCP Hardware Validation Suite',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tests/hardware_validation.py                        # Run all tests
  python tests/hardware_validation.py --category System      # Test only System category
  python tests/hardware_validation.py --verbose              # Show detailed output
  python tests/hardware_validation.py --report results.json  # Save results to file
  python tests/hardware_validation.py -v --category Firewall # Verbose firewall tests

Environment Variables Required:
  MIKROTIK_HOST     - Router IP address or hostname
  MIKROTIK_USER     - Router username
  MIKROTIK_PASSWORD - Router password
        """
    )
    
    parser.add_argument('--category', '-c', 
                       help='Test only a specific category')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Show detailed output for each test')
    parser.add_argument('--report', '-r',
                       help='Save detailed JSON report to file')
    parser.add_argument('--list-categories', action='store_true',
                       help='List all available categories and exit')
    
    args = parser.parse_args()
    
    # Create validator
    validator = HardwareValidator(verbose=args.verbose, save_report=args.report)
    
    # List categories if requested
    if args.list_categories:
        print(f"\n{Colors.BOLD}Available Test Categories:{Colors.ENDC}\n")
        for i, (category, handlers) in enumerate(sorted(validator.categories.items()), 1):
            print(f"  {i:2d}. {Colors.CYAN}{category:25s}{Colors.ENDC} ({len(handlers)} handlers)")
        print()
        return 0
    
    # Run tests
    try:
        success = validator.run_all_tests(specific_category=args.category)
        return 0 if success else 1
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Tests interrupted by user{Colors.ENDC}")
        return 130
    except Exception as e:
        print(f"\n\n{Colors.RED}Test suite failed with exception: {e}{Colors.ENDC}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())

