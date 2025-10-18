#!/usr/bin/env python3
"""
Core functionality test for MikroTik Cursor MCP server.
Tests the most essential features that users will commonly use.

This is a lightweight test that verifies basic connectivity and core operations.
"""

import sys
import os
import time
import json
from pathlib import Path
from typing import Dict, List, Any

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from mcp_mikrotik.tools.tool_registry import get_all_handlers
from mcp_mikrotik.settings.configuration import mikrotik_config
from mcp_mikrotik.logger import app_logger


class CoreTester:
    def __init__(self, verbose: bool = False, dry_run: bool = True):
        self.verbose = verbose
        self.dry_run = dry_run
        self.handlers = get_all_handlers()
        self.results = {
            'total_tests': 0,
            'passed': 0,
            'failed': 0,
            'errors': [],
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
    
    def test_tool(self, tool_name: str, test_args: Dict[str, Any] = None) -> tuple[bool, str]:
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
    
    def run_core_tests(self):
        """Run the core functionality tests."""
        self.log("Starting Core Functionality Tests")
        
        # Define core tests - essential features only
        core_tests = [
            # System Information (essential)
            ("mikrotik_get_system_identity", {}),
            ("mikrotik_get_system_resources", {}),
            ("mikrotik_get_uptime", {}),
            
            # Network Interfaces (essential)
            ("mikrotik_list_interfaces", {}),
            ("mikrotik_list_ip_addresses", {}),
            
            # Basic Connectivity (essential)
            ("mikrotik_ping", {"address": "8.8.8.8", "count": "1"}),
            
            # DHCP (commonly used)
            ("mikrotik_list_dhcp_servers", {}),
            ("mikrotik_list_dhcp_leases", {}),
            
            # DNS (essential)
            ("mikrotik_get_dns_settings", {}),
            
            # Firewall (essential)
            ("mikrotik_list_filter_rules", {}),
            ("mikrotik_list_nat_rules", {}),
            
            # Routing (essential)
            ("mikrotik_get_routing_table", {}),
            
            # Users (essential)
            ("mikrotik_list_users", {}),
            
            # Logs (essential)
            ("mikrotik_get_logs", {}),
        ]
        
        self.log(f"Testing {len(core_tests)} core features...")
        self.log(f"Router: {mikrotik_config.get('host', 'unknown')}")
        self.log(f"User: {mikrotik_config.get('username', 'unknown')}")
        self.log(f"Dry-run mode: {'ON' if os.environ.get('MIKROTIK_DRY_RUN') == 'true' else 'OFF'}")
        
        for tool_name, test_args in core_tests:
            self.results['total_tests'] += 1
            
            if self.verbose:
                self.log(f"Testing {tool_name}...")
            
            success, error = self.test_tool(tool_name, test_args)
            
            if success:
                self.results['passed'] += 1
                if self.verbose:
                    self.log(f"  PASSED: {tool_name}")
            else:
                self.results['failed'] += 1
                error_msg = f"{tool_name}: {error}"
                self.results['errors'].append(error_msg)
                self.log(f"  FAILED: {tool_name} - {error}", "ERROR")
    
    def print_summary(self):
        """Print test summary."""
        duration = time.time() - self.results['start_time']
        
        print("\n" + "="*60)
        print("MikroTik Cursor MCP - Core Functionality Test Results")
        print("="*60)
        
        print(f"Test Duration: {duration:.2f} seconds")
        print(f"Total Tests: {self.results['total_tests']}")
        print(f"Passed: {self.results['passed']} ({self.results['passed']/max(self.results['total_tests'], 1)*100:.1f}%)")
        print(f"Failed: {self.results['failed']} ({self.results['failed']/max(self.results['total_tests'], 1)*100:.1f}%)")
        
        if self.results['failed'] == 0:
            print("\n*** ALL CORE TESTS PASSED! ***")
            print("Your MikroTik Cursor MCP server is working perfectly!")
        else:
            print(f"\nWARNING: {self.results['failed']} CORE TESTS FAILED")
            print("\nFailed tests:")
            for error in self.results['errors']:
                print(f"  - {error}")
        
        print("\n" + "="*60)
    
    def save_report(self, filename: str = "core_test_report.json"):
        """Save detailed test report to JSON file."""
        report = {
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
            'test_type': 'core',
            'dry_run': self.dry_run,
            'verbose': self.verbose,
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
            'errors': self.results['errors']
        }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.log(f"Core test report saved to: {filename}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Test core MikroTik Cursor MCP functionality")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Test in dry-run mode (default)")
    parser.add_argument("--live", action="store_true", help="Run live tests (will make changes)")
    parser.add_argument("--save-report", action="store_true", help="Save detailed JSON report")
    
    args = parser.parse_args()
    
    # Determine dry-run mode
    dry_run = not args.live if args.live else args.dry_run
    
    print("MikroTik Cursor MCP - Core Functionality Test")
    print("=" * 50)
    print(f"Mode: {'Dry-run (safe)' if dry_run else 'Live (will make changes)'}")
    print(f"Verbose: {args.verbose}")
    print()
    
    # Initialize tester
    tester = CoreTester(verbose=args.verbose, dry_run=dry_run)
    
    try:
        # Run tests
        tester.run_core_tests()
        
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
