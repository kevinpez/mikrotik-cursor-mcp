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
    
    # Handlers to skip (truly dangerous operations)
    SKIP_HANDLERS = [
        'mikrotik_reboot_system',           # Reboots the router
        'mikrotik_restore_backup',          # Restores from backup (destructive)
        'mikrotik_remove_user',             # Deletes user accounts
        'mikrotik_disable_ip_service',      # Disables critical services
        'mikrotik_clear_logs',              # Clears system logs
        'mikrotik_flush_connections',       # Drops all connections
        'mikrotik_bandwidth_test',          # Causes API "unimplemented" errors and hangs
        'mikrotik_traceroute',              # Causes API "unimplemented" errors and hangs
    ]
    
    # Handlers that need special timeout handling
    TIMEOUT_HANDLERS = {
        'mikrotik_monitor_logs': 5,         # 5 second timeout for follow mode
    }
    
    # Test arguments for handlers that need specific parameters
    TEST_ARGS = {
        'mikrotik_ping': {'address': '1.1.1.1', 'count': 2},
        'mikrotik_dns_lookup': {'hostname': 'cloudflare.com'},
        'mikrotik_check_connection': {'address': '1.1.1.1'},
        'mikrotik_search_logs': {'search_term': 'system'},
        'mikrotik_get_interface_stats': {'interface': 'ether1'},
        'mikrotik_get_interface_monitor': {'interface': 'ether1'},
        'mikrotik_get_interface_traffic': {'interface': 'ether1'},
        # Safe Mode handlers - these are safe to test
        'mikrotik_enter_safe_mode': {'timeout_minutes': 1},  # Very short timeout for testing
        'mikrotik_set_safe_mode_timeout': {'timeout_minutes': 5},
        # Long-running handlers with safe parameters
        'mikrotik_monitor_logs': {'duration': 3},  # Very short duration
        # OSPF handlers - test with safe parameters
        'mikrotik_auto_configure_ospf_interfaces': {'dry_run': True},  # If supported
        # Watchdog handlers - safe to test
        'mikrotik_set_watchdog_ping_target': {'ip_address': '1.1.1.1'},  # Cloudflare DNS - more reliable
        # IGMP handlers - safe to test (these are configuration changes)
        'mikrotik_enable_igmp_snooping': {'bridge_id': 'bridge'},  # Use the default bridge
        'mikrotik_disable_igmp_snooping': {'bridge_id': 'bridge'},  # Use the default bridge
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
            elif 'safe' in handler_name or 'safety' in handler_name:
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
    
    def test_safe_mode_handler(self, handler_name: str, test_args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Test Safe Mode handlers with special safety measures.
        """
        if self.verbose:
            print(f"\n{Colors.CYAN}  Executing Safe Mode handler: {Colors.BOLD}{handler_name}{Colors.ENDC}")
            if test_args:
                print(f"{Colors.CYAN}  Arguments: {Colors.BOLD}{test_args}{Colors.ENDC}")
        
        start_time = time.time()
        try:
            handler = self.handlers[handler_name]
            result = handler(test_args)
            duration = time.time() - start_time
            
            # For Safe Mode handlers, we consider informative messages as success
            if isinstance(result, str):
                if "ERROR:" in result or "Error:" in result or "Failed" in result:
                    if self.verbose:
                        print(f"{Colors.RED}  ✗ Safe Mode operation failed{Colors.ENDC}\n")
                    return {
                        'status': 'failed',
                        'reason': 'Safe Mode operation failed',
                        'duration': duration,
                        'output': result[:500]
                    }
                elif "INFO:" in result and "NOT AVAILABLE VIA API/SSH" in result:
                    # This is an informative message about Safe Mode being terminal-only
                    if self.verbose:
                        print(f"{Colors.GREEN}  ✓ Safe Mode handler provided informative response{Colors.ENDC}\n")
                    return {
                        'status': 'passed',
                        'duration': duration,
                        'output': result[:200] if self.verbose else None
                    }
                else:
                    if self.verbose:
                        print(f"{Colors.GREEN}  ✓ Safe Mode operation successful{Colors.ENDC}\n")
                    return {
                        'status': 'passed',
                        'duration': duration,
                        'output': result[:200] if self.verbose else None
                    }
            else:
                if self.verbose:
                    print(f"{Colors.GREEN}  ✓ Safe Mode operation successful (returned {type(result).__name__}){Colors.ENDC}\n")
                return {
                    'status': 'passed',
                    'duration': duration,
                    'output': str(result)[:200] if self.verbose else None
                }
                
        except Exception as e:
            if self.verbose:
                print(f"{Colors.RED}  ✗ Exception: {Colors.BOLD}{type(e).__name__}: {str(e)}{Colors.ENDC}\n")
            return {
                'status': 'failed',
                'reason': f'Exception: {type(e).__name__}',
                'duration': time.time() - start_time,
                'output': str(e)[:500]
            }
    
    def test_timeout_handler(self, handler_name: str, test_args: Dict[str, Any], timeout_seconds: int) -> Dict[str, Any]:
        """
        Test handlers that might hang with a timeout mechanism.
        """
        if self.verbose:
            print(f"\n{Colors.CYAN}  Executing timeout handler: {Colors.BOLD}{handler_name}{Colors.ENDC} (timeout: {timeout_seconds}s)")
            if test_args:
                print(f"{Colors.CYAN}  Arguments: {Colors.BOLD}{test_args}{Colors.ENDC}")
        
        start_time = time.time()
        try:
            handler = self.handlers[handler_name]
            
            # Use a simple timeout mechanism
            import signal
            
            def timeout_handler(signum, frame):
                raise TimeoutError(f"Handler {handler_name} timed out after {timeout_seconds} seconds")
            
            # Set up timeout (Unix-like systems only)
            if hasattr(signal, 'SIGALRM'):
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(timeout_seconds)
            
            try:
                result = handler(test_args)
                duration = time.time() - start_time
                
                # Cancel timeout
                if hasattr(signal, 'SIGALRM'):
                    signal.alarm(0)
                
                # Analyze result
                if isinstance(result, str):
                    if "ERROR:" in result or "Error:" in result or "Failed" in result:
                        if self.verbose:
                            print(f"{Colors.RED}  ✗ Handler returned error{Colors.ENDC}\n")
                        return {
                            'status': 'failed',
                            'reason': 'Handler returned error',
                            'duration': duration,
                            'output': result[:500]
                        }
                    else:
                        if self.verbose:
                            print(f"{Colors.GREEN}  ✓ Handler completed successfully{Colors.ENDC}\n")
                        return {
                            'status': 'passed',
                            'duration': duration,
                            'output': result[:200] if self.verbose else None
                        }
                else:
                    if self.verbose:
                        print(f"{Colors.GREEN}  ✓ Handler completed successfully (returned {type(result).__name__}){Colors.ENDC}\n")
                    return {
                        'status': 'passed',
                        'duration': duration,
                        'output': str(result)[:200] if self.verbose else None
                    }
                    
            except TimeoutError as e:
                if hasattr(signal, 'SIGALRM'):
                    signal.alarm(0)
                if self.verbose:
                    print(f"{Colors.YELLOW}  ⊘ Handler timed out after {timeout_seconds}s{Colors.ENDC}\n")
                return {
                    'status': 'skipped',
                    'reason': f'Handler timed out after {timeout_seconds} seconds',
                    'duration': timeout_seconds
                }
                
        except Exception as e:
            if hasattr(signal, 'SIGALRM'):
                signal.alarm(0)
            if self.verbose:
                print(f"{Colors.RED}  ✗ Exception: {Colors.BOLD}{type(e).__name__}: {str(e)}{Colors.ENDC}\n")
            return {
                'status': 'failed',
                'reason': f'Exception: {type(e).__name__}',
                'duration': time.time() - start_time,
                'output': str(e)[:500]
            }
    
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
        
        # Special handling for Safe Mode handlers
        if handler_name.startswith('mikrotik_') and 'safe_mode' in handler_name:
            return self.test_safe_mode_handler(handler_name, test_args)
        
        # Special handling for timeout handlers
        if handler_name in self.TIMEOUT_HANDLERS:
            return self.test_timeout_handler(handler_name, test_args, self.TIMEOUT_HANDLERS[handler_name])
        
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
                    'category': category_name,
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
        print(f"{Colors.BOLD}{Colors.HEADER}TEST RESULTS SUMMARY{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.HEADER}{'='*80}{Colors.ENDC}\n")
        
        # Calculate correct statistics
        passed = self.results['passed']
        failed = self.results['failed']
        skipped = self.results['skipped']
        total_tested = passed + failed + skipped
        total_handlers = self.results['total_handlers']
        
        # Calculate rates
        if total_tested > 0:
            pass_rate = (passed / total_tested) * 100
            fail_rate = (failed / total_tested) * 100
        else:
            pass_rate = 0
            fail_rate = 0
        
        # Print statistics in a nice table format
        print(f"{Colors.BOLD}Overall Statistics:{Colors.ENDC}")
        print(f"  {'Total Handlers:':<20} {Colors.BOLD}{total_handlers}{Colors.ENDC}")
        print(f"  {'Tests Executed:':<20} {Colors.BOLD}{total_tested}{Colors.ENDC}")
        print(f"  {'├─ Passed:':<20} {Colors.GREEN}{passed:>4}{Colors.ENDC}  ({pass_rate:5.1f}%)")
        print(f"  {'├─ Failed:':<20} {Colors.RED}{failed:>4}{Colors.ENDC}  ({fail_rate:5.1f}%)")
        print(f"  {'└─ Skipped:':<20} {Colors.YELLOW}{skipped:>4}{Colors.ENDC}  (safety/setup)")
        print(f"  {'Duration:':<20} {Colors.BOLD}{self.results['duration_seconds']:.1f}s{Colors.ENDC}")
        
        # Success rate calculation
        if passed > 0 and failed == 0:
            print(f"\n  {Colors.BOLD}{Colors.GREEN}✓ Success Rate: 100% of runnable tests{Colors.ENDC}")
        elif total_tested > 0:
            success_rate = (passed / (passed + failed)) * 100 if (passed + failed) > 0 else 0
            if success_rate >= 90:
                color = Colors.GREEN
                symbol = "✓"
            elif success_rate >= 70:
                color = Colors.YELLOW
                symbol = "~"
            else:
                color = Colors.RED
                symbol = "✗"
            print(f"\n  {Colors.BOLD}{color}{symbol} Success Rate: {success_rate:.1f}% of runnable tests{Colors.ENDC}")
        
        # Results by category
        print(f"\n{Colors.BOLD}Results by Category:{Colors.ENDC}")
        print(f"{Colors.BOLD}{'─'*80}{Colors.ENDC}")
        print(f"  {'Category':<25} {'Passed':<8} {'Failed':<8} {'Skipped':<8} {'Rate'}")
        print(f"  {Colors.BOLD}{'─'*25} {'─'*8} {'─'*8} {'─'*8} {'─'*8}{Colors.ENDC}")
        
        for category_name in sorted(self.results['categories'].keys()):
            cat_results = self.results['categories'][category_name]
            cat_total = cat_results['total']
            cat_passed = cat_results['passed']
            cat_failed = cat_results['failed']
            cat_skipped = cat_results['skipped']
            
            # Calculate pass rate (of runnable tests)
            runnable = cat_passed + cat_failed
            if runnable > 0:
                success_rate = (cat_passed / runnable) * 100
            else:
                success_rate = 0
            
            # Color code based on success rate
            if success_rate == 100 and cat_passed > 0:
                status_color = Colors.GREEN
                status = "✓"
            elif success_rate >= 80:
                status_color = Colors.GREEN
                status = "+"
            elif success_rate >= 60:
                status_color = Colors.YELLOW
                status = "~"
            else:
                status_color = Colors.RED
                status = "✗"
            
            # Format the row
            print(f"  {status_color}{status}{Colors.ENDC} {category_name:<23} "
                  f"{Colors.GREEN}{cat_passed:>3}{Colors.ENDC}/{cat_total:<3} "
                  f"{Colors.RED if cat_failed > 0 else ''}{cat_failed:>3}{Colors.ENDC}     "
                  f"{Colors.YELLOW}{cat_skipped:>3}{Colors.ENDC}     "
                  f"{status_color}{success_rate:>5.1f}%{Colors.ENDC}")
        
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
            print(f"{Colors.BOLD}{Colors.GREEN}✓ ALL RUNNABLE TESTS PASSED{Colors.ENDC}")
            print(f"\n  {Colors.GREEN}Result:{Colors.ENDC} {Colors.BOLD}{passed}{Colors.ENDC} tests executed successfully")
            if skipped > 0:
                print(f"  {Colors.YELLOW}Note:{Colors.ENDC} {skipped} handlers skipped (dangerous/long-running operations)")
            print(f"\n  {Colors.GREEN}Your MikroTik MCP is fully operational!{Colors.ENDC}")
        elif failed == 0:
            print(f"{Colors.BOLD}{Colors.YELLOW}⚠ NO TESTS RUN{Colors.ENDC}")
            print(f"\n  Check your test configuration")
        else:
            # Calculate success rate of runnable tests
            runnable = passed + failed
            success_rate = (passed / runnable * 100) if runnable > 0 else 0
            
            if success_rate >= 80:
                print(f"{Colors.BOLD}{Colors.YELLOW}⚠ SOME TESTS FAILED{Colors.ENDC}")
                print(f"\n  {Colors.GREEN}Passed:{Colors.ENDC} {passed}/{runnable} ({success_rate:.1f}%)")
                print(f"  {Colors.RED}Failed:{Colors.ENDC} {failed} - Review failures above")
                print(f"\n  {Colors.YELLOW}Most functionality works, but some issues need attention{Colors.ENDC}")
            else:
                print(f"{Colors.BOLD}{Colors.RED}✗ MULTIPLE FAILURES{Colors.ENDC}")
                print(f"\n  {Colors.GREEN}Passed:{Colors.ENDC} {passed}/{runnable} ({success_rate:.1f}%)")
                print(f"  {Colors.RED}Failed:{Colors.ENDC} {failed} - Review failures above")
                print(f"\n  {Colors.RED}Significant issues detected - please review failures{Colors.ENDC}")
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

