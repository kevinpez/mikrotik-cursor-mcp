# Testing Guide

This document explains how to test the MikroTik Cursor MCP server.

## Quick Start

### Run Core Tests (Recommended)
```bash
python run_tests.py core
```

### Run All Tests
```bash
python run_tests.py comprehensive
```

### Run Integration Tests
```bash
python run_tests.py integration
```

### Run All Test Types
```bash
python run_tests.py all
```

## Test Types

### 1. Core Tests (`test_core.py`)
- **Purpose**: Tests essential functionality that users commonly use
- **Duration**: ~30 seconds
- **Tests**: 14 core features including system info, interfaces, DHCP, DNS, firewall, etc.
- **Safe**: Runs in dry-run mode by default

### 2. Comprehensive Tests (`test_comprehensive.py`)
- **Purpose**: Tests all 426+ features across 19 categories
- **Duration**: ~5-10 minutes
- **Tests**: Every available MikroTik MCP function
- **Safe**: Runs in dry-run mode by default

### 3. Integration Tests (`tests/integration/`)
- **Purpose**: Tests against your actual MikroTik router
- **Duration**: ~30 seconds
- **Tests**: Real router connectivity and functionality
- **Requires**: Access to your MikroTik router
- **Safe**: Runs in dry-run mode by default

## Command Line Options

### Common Options
- `--verbose, -v`: Show detailed output for each test
- `--dry-run`: Test in dry-run mode (default, safe)
- `--live`: Run live tests (will make changes to router)
- `--save-report`: Save detailed JSON report

### Comprehensive Test Options
- `--category, -c`: Test only specific category (e.g., firewall, system)

## Examples

```bash
# Basic core test
python run_tests.py core

# Verbose comprehensive test
python run_tests.py comprehensive --verbose

# Test only firewall features
python run_tests.py comprehensive --category firewall

# Run live tests (WARNING: will make changes)
python run_tests.py core --live

# Save detailed report
python run_tests.py comprehensive --save-report

# Run integration tests
python run_tests.py integration

# Run all test types with verbose output
python run_tests.py all --verbose
```

## Test Categories

The comprehensive test covers these categories with current success rates (82.7% overall):

### 100% Success Categories ✅
- **system**: System monitoring and management (7/7)
- **interfaces**: Network interface management (8/8)
- **routes**: Routing table and static routes (4/4)
- **firewall**: Firewall rules (filter, NAT, mangle, raw) (1/1)
- **users**: User management (3/3)
- **backup**: Backup management (5/5)
- **queues**: QoS queue management (2/2)
- **openvpn**: OpenVPN configuration (9/9)

### High Success Categories (80%+) 🟡
- **ip**: IP address and pool management (36/42 - 85.7%)
- **wireless**: Wireless interfaces and security (18/21 - 85.7%)
- **hotspot**: Hotspot/captive portal (7/8 - 87.5%)
- **ipv6**: IPv6 configuration (23/27 - 85.2%)
- **wireguard**: WireGuard VPN (9/11 - 81.8%)
- **logs**: System logs (6/8 - 75.0%)

### Categories Being Improved 🔧
- **dhcp**: DHCP server configuration (17/23 - 73.9%)
- **container**: RouterOS v7.x containers (13/18 - 72.2%)
- **vlan**: VLAN interfaces (8/12 - 66.7%)
- **dns**: DNS settings and static entries (10/16 - 62.5%)

## Integration Tests

Integration tests run against your actual MikroTik router:

```bash
# Run integration tests
python run_tests.py integration

# Run integration tests with verbose output
python tests/integration/test_integration_runner.py --verbose

# Run simple integration test directly
python tests/integration/test_simple_integration.py --verbose
```

## Configuration

### Environment Variables
- `MIKROTIK_DRY_RUN=true`: Enable dry-run mode (default)
- `MIKROTIK_HOST`: Router IP address
- `MIKROTIK_USERNAME`: Router username
- `MIKROTIK_PASSWORD`: Router password
- `MIKROTIK_PORT`: Router port (default: 8728)

### Configuration Files
- `mcp-config.json.example`: Example MCP configuration
- `env.example`: Example environment variables

## Troubleshooting

### Common Issues

1. **Connection Failed**
   - Check router IP, username, and password
   - Verify router is accessible from test machine
   - Check firewall settings

2. **Tests Failing**
   - Most failures are expected if features aren't configured
   - Check the error messages for specific issues
   - Use `--verbose` for detailed output

3. **Permission Denied**
   - Ensure user has appropriate permissions on router
   - Some tests require admin privileges

### Getting Help

- Use `--verbose` flag for detailed output
- Check the JSON report files for detailed error information
- Review the test logs for specific failure reasons

## Safety

- **Default Mode**: All tests run in dry-run mode by default
- **Live Mode**: Only use `--live` flag when you want to make actual changes
- **Backup**: Always backup your router before running live tests
- **Testing**: Test on non-production routers first

## Reports

Test reports are saved as JSON files with detailed information:
- Test results and timing
- Error messages and stack traces
- Router configuration details
- Success rates by category

Use `--save-report` to generate these files.
