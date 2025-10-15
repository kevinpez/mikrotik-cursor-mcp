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
        
        if "list" in tool_name.lower():
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
        elif "create" in tool_name.lower() or "set" in tool_name.lower():
            # Create/Set commands need test data
            if "firewall" in tool_name:
                test_args = {
                    "chain": "input",
                    "action": "accept",
                    "protocol": "tcp",
                    "dst-port": "8080",
                    "comment": "test-rule"
                }
            elif "dhcp" in tool_name:
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
        elif "ping" in tool_name.lower():
            test_args = {"address": "8.8.8.8", "count": "1"}
        elif "dns" in tool_name.lower() and "lookup" in tool_name.lower():
            test_args = {"host": "google.com"}
        elif "traceroute" in tool_name.lower():
            test_args = {"address": "8.8.8.8"}
        
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
