#!/usr/bin/env python3
"""
Integration test runner for MikroTik Cursor MCP server.
Runs integration tests against your actual MikroTik router.

Simple and straightforward - no Docker complexity required.
"""

import sys
import os
import time
import subprocess
import argparse
from pathlib import Path


def run_simple_integration_test() -> int:
    """Run the simple integration test."""
    test_file = "tests/integration/test_simple_integration.py"
    
    if not Path(test_file).exists():
        print(f"Error: Integration test file {test_file} not found!")
        return 1
    
    print(f"\n{'='*60}")
    print("Running Simple Integration Tests...")
    print(f"{'='*60}")
    
    cmd = [sys.executable, test_file]
    return subprocess.call(cmd)


def main():
    parser = argparse.ArgumentParser(
        description="Integration test runner for MikroTik Cursor MCP server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tests/integration/test_integration_runner.py          # Run simple integration tests
  python tests/integration/test_integration_runner.py --verbose # Run with verbose output
        """
    )
    
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    start_time = time.time()
    
    print("MikroTik Cursor MCP - Integration Test Runner")
    print("=" * 50)
    print("Testing against your actual MikroTik router")
    print("Mode: Dry-run (safe - no changes will be made)")
    print(f"Verbose: {args.verbose}")
    print()
    
    try:
        # Run simple integration test
        exit_code = run_simple_integration_test()
        
        # Print final summary
        duration = time.time() - start_time
        print(f"\n{'='*60}")
        print("INTEGRATION TEST SUMMARY")
        print(f"{'='*60}")
        print(f"Total Duration: {duration:.2f} seconds")
        
        if exit_code == 0:
            print("[PASS] Integration tests passed successfully!")
        else:
            print("[FAIL] Integration tests failed!")
        
        print(f"{'='*60}")
        
        return exit_code
        
    except KeyboardInterrupt:
        print("\n\nIntegration tests interrupted by user")
        return 130
    except Exception as e:
        print(f"\n\nIntegration test runner failed with exception: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())