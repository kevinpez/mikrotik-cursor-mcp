#!/bin/bash
#
# Example script for running MikroTik MCP hardware validation tests
# This demonstrates various ways to use the hardware validation suite
#

set -e  # Exit on error

echo "MikroTik MCP Hardware Validation Examples"
echo "=========================================="
echo ""

# Check if environment variables are set
if [ -z "$MIKROTIK_HOST" ]; then
    echo "ERROR: MIKROTIK_HOST environment variable not set"
    echo ""
    echo "Please set your MikroTik connection details:"
    echo "  export MIKROTIK_HOST=\"192.168.88.1\""
    echo "  export MIKROTIK_USER=\"admin\""
    echo "  export MIKROTIK_PASSWORD=\"your-password\""
    echo ""
    exit 1
fi

echo "Router: $MIKROTIK_HOST"
echo "User: ${MIKROTIK_USER:-admin}"
echo ""

# Create reports directory
mkdir -p test_reports

# Example 1: Quick system check
echo "Example 1: Quick System Health Check"
echo "--------------------------------------"
python tests/hardware_validation.py --category System
echo ""

# Example 2: Test firewall with verbose output
echo "Example 2: Detailed Firewall Testing"
echo "-------------------------------------"
python tests/hardware_validation.py --category Firewall -v
echo ""

# Example 3: Full validation with report
echo "Example 3: Complete Hardware Validation"
echo "----------------------------------------"
python tests/hardware_validation.py --report test_reports/full_validation_$(date +%Y%m%d_%H%M%S).json
echo ""

# Example 4: Test critical categories
echo "Example 4: Test Critical Categories"
echo "------------------------------------"
for category in System Interfaces Firewall Routing; do
    echo "Testing $category..."
    python tests/hardware_validation.py --category "$category" --report "test_reports/${category}_$(date +%Y%m%d).json"
done
echo ""

echo "All examples completed!"
echo "Reports saved to test_reports/"
ls -lh test_reports/

