#!/usr/bin/env python3
"""
Simple integration tests for MikroTik Cursor MCP server.
Tests against a real MikroTik router (no Docker required).

This is much simpler than the Docker-based tests and tests against
your actual router configuration.
"""

import sys
import os
import time
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from mcp_mikrotik.tools.tool_registry import get_all_handlers
from mcp_mikrotik.settings.configuration import mikrotik_config


class SimpleIntegrationTester:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.handlers = get_all_handlers()
        self.results = {
            'total_tests': 0,
            'passed': 0,
            'failed': 0,
            'errors': [],
            'start_time': time.time()
        }
        
        # Set dry-run mode for safety
        os.environ['MIKROTIK_DRY_RUN'] = 'true'
    
    def log(self, message: str, level: str = "INFO"):
        """Log message with timestamp."""
        timestamp = time.strftime("%H:%M:%S")
        if self.verbose or level == "ERROR":
            print(f"[{timestamp}] {level}: {message}")
    
    def test_tool(self, tool_name: str, test_args: dict = None) -> tuple[bool, str]:
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
    
    def run_integration_tests(self):
        """Run simple integration tests against real router."""
        self.log("Starting Simple Integration Tests")
        
        # Test basic connectivity and core features
        integration_tests = [
            # System Information
            ("mikrotik_get_system_identity", {}),
            ("mikrotik_get_system_resources", {}),
            ("mikrotik_get_uptime", {}),
            
            # Network Configuration
            ("mikrotik_list_interfaces", {}),
            ("mikrotik_list_ip_addresses", {}),
            ("mikrotik_get_dns_settings", {}),
            
            # Services
            ("mikrotik_list_dhcp_servers", {}),
            ("mikrotik_list_dhcp_leases", {}),
            
            # Firewall
            ("mikrotik_list_filter_rules", {}),
            ("mikrotik_list_nat_rules", {}),
            
            # Users
            ("mikrotik_list_users", {}),
            
            # Diagnostics
            ("mikrotik_ping", {"address": "8.8.8.8", "count": "1"}),
            
            # Logs
            ("mikrotik_get_logs", {}),
        ]
        
        self.log(f"Testing {len(integration_tests)} integration features...")
        self.log(f"Router: {mikrotik_config.get('host', 'unknown')}")
        self.log(f"User: {mikrotik_config.get('username', 'unknown')}")
        self.log(f"Mode: Dry-run (safe)")
        
        for tool_name, test_args in integration_tests:
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
        print("Simple Integration Test Results")
        print("="*60)
        
        print(f"Test Duration: {duration:.2f} seconds")
        print(f"Total Tests: {self.results['total_tests']}")
        print(f"Passed: {self.results['passed']} ({self.results['passed']/max(self.results['total_tests'], 1)*100:.1f}%)")
        print(f"Failed: {self.results['failed']} ({self.results['failed']/max(self.results['total_tests'], 1)*100:.1f}%)")
        
        if self.results['failed'] == 0:
            print("\n*** ALL INTEGRATION TESTS PASSED! ***")
            print("Your MikroTik router is fully accessible and functional!")
        else:
            print(f"\nWARNING: {self.results['failed']} INTEGRATION TESTS FAILED")
            print("\nFailed tests:")
            for error in self.results['errors']:
                print(f"  - {error}")
        
        print("\n" + "="*60)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Simple integration tests for MikroTik MCP")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    print("MikroTik Cursor MCP - Simple Integration Tests")
    print("=" * 50)
    print("Testing against your actual MikroTik router")
    print("Mode: Dry-run (safe - no changes will be made)")
    print(f"Verbose: {args.verbose}")
    print()
    
    # Initialize tester
    tester = SimpleIntegrationTester(verbose=args.verbose)
    
    try:
        # Run tests
        tester.run_integration_tests()
        
        # Print summary
        tester.print_summary()
        
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
