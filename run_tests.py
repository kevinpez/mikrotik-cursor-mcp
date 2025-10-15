#!/usr/bin/env python3
"""
Unified test runner for MikroTik Cursor MCP server.
Provides easy access to both core and comprehensive tests.

Usage:
    python run_tests.py core          # Run core functionality tests
    python run_tests.py comprehensive # Run all feature tests
    python run_tests.py all           # Run both core and comprehensive
    python run_tests.py --help        # Show detailed help
"""

import sys
import os
import time
import subprocess
import argparse
from pathlib import Path


def run_test(test_type: str, args: list = None) -> int:
    """Run a specific test type and return exit code."""
    if args is None:
        args = []
    
    test_file = f"test_{test_type}.py"
    
    if not Path(test_file).exists():
        print(f"Error: Test file {test_file} not found!")
        return 1
    
    print(f"\n{'='*60}")
    print(f"Running {test_type.upper()} tests...")
    print(f"{'='*60}")
    
    cmd = [sys.executable, test_file] + args
    return subprocess.call(cmd)


def main():
    parser = argparse.ArgumentParser(
        description="Unified test runner for MikroTik Cursor MCP server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_tests.py core                    # Run core tests (default)
  python run_tests.py comprehensive           # Run all feature tests
  python run_tests.py all                     # Run both core and comprehensive
  python run_tests.py core --verbose          # Run core tests with verbose output
  python run_tests.py comprehensive --live    # Run comprehensive tests in live mode
  python run_tests.py core --save-report      # Run core tests and save report
        """
    )
    
    parser.add_argument(
        "test_type",
        choices=["core", "comprehensive", "all"],
        default="core",
        nargs="?",
        help="Type of test to run (default: core)"
    )
    
    # Test-specific arguments
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Test in dry-run mode (default)")
    parser.add_argument("--live", action="store_true", help="Run live tests (will make changes)")
    parser.add_argument("--category", "-c", help="Test only specific category (comprehensive only)")
    parser.add_argument("--save-report", action="store_true", help="Save detailed JSON report")
    
    args = parser.parse_args()
    
    # Build common arguments
    common_args = []
    if args.verbose:
        common_args.append("--verbose")
    if args.live:
        common_args.append("--live")
    elif args.dry_run:
        common_args.append("--dry-run")
    if args.save_report:
        common_args.append("--save-report")
    
    # Build comprehensive-specific arguments
    comprehensive_args = common_args.copy()
    if args.category:
        comprehensive_args.extend(["--category", args.category])
    
    start_time = time.time()
    exit_codes = []
    
    print("MikroTik Cursor MCP - Unified Test Runner")
    print("=" * 50)
    print(f"Test Type: {args.test_type}")
    print(f"Verbose: {args.verbose}")
    print(f"Mode: {'Live (will make changes)' if args.live else 'Dry-run (safe)'}")
    if args.category:
        print(f"Category: {args.category}")
    print(f"Save Report: {args.save_report}")
    print()
    
    try:
        if args.test_type == "core":
            exit_code = run_test("core", common_args)
            exit_codes.append(exit_code)
            
        elif args.test_type == "comprehensive":
            exit_code = run_test("comprehensive", comprehensive_args)
            exit_codes.append(exit_code)
            
        elif args.test_type == "all":
            # Run core tests first
            print("Phase 1: Core Functionality Tests")
            exit_code = run_test("core", common_args)
            exit_codes.append(exit_code)
            
            if exit_code == 0:
                print("\nPhase 2: Comprehensive Feature Tests")
                exit_code = run_test("comprehensive", comprehensive_args)
                exit_codes.append(exit_code)
            else:
                print("\nSkipping comprehensive tests due to core test failures")
                exit_codes.append(1)
        
        # Print final summary
        duration = time.time() - start_time
        print(f"\n{'='*60}")
        print("FINAL SUMMARY")
        print(f"{'='*60}")
        print(f"Total Duration: {duration:.2f} seconds")
        
        if len(exit_codes) == 1:
            if exit_codes[0] == 0:
                print("[PASS] All tests passed successfully!")
            else:
                print("[FAIL] Tests failed!")
        else:
            core_result = "[PASS]" if exit_codes[0] == 0 else "[FAIL]"
            comp_result = "[PASS]" if exit_codes[1] == 0 else "[FAIL]"
            print(f"Core Tests: {core_result}")
            print(f"Comprehensive Tests: {comp_result}")
            
            if all(code == 0 for code in exit_codes):
                print("[SUCCESS] All test phases passed successfully!")
            else:
                print("[WARNING] Some test phases failed!")
        
        print(f"{'='*60}")
        
        # Return worst exit code
        return max(exit_codes)
        
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
        return 130
    except Exception as e:
        print(f"\n\nTest runner failed with exception: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
