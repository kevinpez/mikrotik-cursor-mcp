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

### Run Both Core and Comprehensive
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
- **Purpose**: Tests specific features with actual MikroTik containers
- **Duration**: ~2-5 minutes per test
- **Tests**: User management, new features, etc.
- **Requires**: Docker and testcontainers

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

# Run both core and comprehensive with verbose output
python run_tests.py all --verbose
```

## Test Categories

The comprehensive test covers these categories:
- **system**: System monitoring and management
- **interfaces**: Network interface management
- **ip**: IP address and pool management
- **dhcp**: DHCP server configuration
- **dns**: DNS settings and static entries
- **routes**: Routing table and static routes
- **firewall**: Firewall rules (filter, NAT, mangle, raw)
- **diagnostics**: Network diagnostics (ping, traceroute, etc.)
- **users**: User management
- **logs**: System logs
- **backup**: Backup management
- **queues**: QoS queue management
- **vlan**: VLAN interfaces
- **wireguard**: WireGuard VPN
- **openvpn**: OpenVPN configuration
- **wireless**: Wireless interfaces and security
- **hotspot**: Hotspot/captive portal
- **ipv6**: IPv6 configuration
- **container**: RouterOS v7.x containers

## Integration Tests

Integration tests use Docker containers to test with real MikroTik RouterOS:

```bash
# Run integration tests with pytest
pytest tests/integration/ -v

# Run specific integration test
pytest tests/integration/test_mikrotik_user_integration.py -v
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
