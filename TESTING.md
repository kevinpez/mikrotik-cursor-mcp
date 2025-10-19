# Testing Guide

Comprehensive testing documentation for the MikroTik Cursor MCP server.

---

## Overview

The MikroTik MCP includes a hardware validation suite that tests all 440+ handler functions against live MikroTik routers. This ensures that every command works correctly with your specific RouterOS configuration.

**Test Suite Features:**
- Tests 440+ handler functions across 19 categories
- Real-time progress indicators
- Verbose and compact output modes
- JSON report generation
- Safety features prevent dangerous operations
- Category-specific testing

---

## Quick Start

### 1. Configure Environment

Create a `.env.test` file in the project root:

```bash
MIKROTIK_HOST=192.168.88.1
MIKROTIK_USERNAME=admin
MIKROTIK_PASSWORD=your_password
MIKROTIK_PORT=22
MIKROTIK_LOG_LEVEL=INFO
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Tests

```bash
# Test all handlers
python tests/hardware_validation.py

# Test with verbose output
python tests/hardware_validation.py -v

# Test specific category
python tests/hardware_validation.py --category System -v

# Save results to JSON
python tests/hardware_validation.py --report results.json

# List available categories
python tests/hardware_validation.py --list-categories
```

---

## Test Categories

The hardware validation suite covers 19 functional categories:

1. **System** - Identity, resources, clock, health
2. **Firewall** - Filter, NAT, mangle, RAW rules
3. **Interfaces** - Physical, virtual, bridge, VLAN
4. **Routes** - Static routes, BGP, OSPF
5. **IPv6** - Addresses, routes, DHCPv6, firewall
6. **Wireless** - Interfaces, CAPsMAN, security
7. **DNS** - Settings, static entries, cache
8. **DHCP** - Servers, pools, leases
9. **Users** - User management, groups
10. **WireGuard** - VPN interfaces and peers
11. **OpenVPN** - Client, server, certificates
12. **Containers** - Docker lifecycle, networking
13. **Certificates** - PKI, CA, SSL/TLS
14. **Backup** - Create, restore, export
15. **Hotspot** - Servers, users, captive portal
16. **IP Management** - Addresses, pools, services
17. **Queues** - Simple queues, queue trees
18. **Logs** - View, search, clear
19. **Diagnostics** - Ping, traceroute, ARP

---

## Output Formats

### Compact Mode (Default)

```
[1/10] get_system_identity         PASS (0.45s)
[2/10] get_system_resources         PASS (0.38s)
[3/10] get_system_health            PASS (0.41s)
```

### Verbose Mode

```
[1/10] get_system_identity

  Executing: mikrotik_get_system_identity
  Command executed in 0.45s
  
  Result:
  SYSTEM IDENTITY:
  name: test-router
  
  Command successful
```

### JSON Report

```json
{
  "summary": {
    "total": 440,
    "passed": 385,
    "failed": 35,
    "skipped": 20
  },
  "categories": [
    {
      "name": "System",
      "handlers": 13,
      "passed": 10,
      "failed": 0,
      "skipped": 3
    }
  ]
}
```

---

## Understanding Results

### Status Indicators

- **PASS** - Handler executed successfully
- **FAIL** - Handler returned error
- **SKIP** - Handler skipped (dangerous or requires arguments)

### Expected Pass Rates

- **Read Operations**: 80-95%
- **Write Operations**: 30-50% (many require specific arguments)
- **Diagnostic Operations**: 60-80%

### Why Handlers Skip

- **Dangerous operations**: reboot, factory_reset, clear_logs
- **Missing arguments**: Operations requiring specific IDs, filenames
- **Hardware dependent**: Features not available on all models
- **Version specific**: Feature requires newer RouterOS version

---

## Safety Features

The test suite includes multiple safety features:

### 1. Protected Resources
- System reboot operations
- Factory reset commands
- User account deletion
- Service disabling
- Log clearing operations

### 2. Test Mode Features
- Safe defaults for all operations
- Automatic cleanup of test resources
- Test prefixes for created resources
- Skip dangerous operations automatically
- Rollback support for test changes

### 3. Timeout Protection
- Long-running operations have timeouts
- Network operations are limited
- Interactive operations are skipped

---

## Common Test Workflows

### Quick Health Check (5 categories, ~2 min)
```bash
python tests/hardware_validation.py --category System
python tests/hardware_validation.py --category Interfaces
python tests/hardware_validation.py --category Firewall
python tests/hardware_validation.py --category DNS
python tests/hardware_validation.py --category Diagnostics
```

### Complete Validation (All categories, ~5 min)
```bash
python tests/hardware_validation.py --report complete_validation.json
```

### Development Testing (Specific category)
```bash
python tests/hardware_validation.py --category Wireless -v
```

### CI/CD Pipeline
```bash
python tests/hardware_validation.py --report ci_results.json
```

---

## Using pytest

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_core.py

# Run with coverage
pytest --cov=src/mcp_mikrotik

# Run with verbose output
pytest -v

# Run specific test function
pytest tests/test_core.py::test_connection

# Run tests matching pattern
pytest -k "firewall"
```

---

## Troubleshooting

### Connection Errors

**Issue:** `Failed to connect to router`

**Solutions:**
1. Verify `MIKROTIK_HOST` in `.env.test`
2. Check network connectivity: `ping 192.168.88.1`
3. Verify SSH/API is enabled on router
4. Check firewall rules allow access

### Authentication Errors

**Issue:** `Authentication failed`

**Solutions:**
1. Verify credentials in `.env.test`
2. Check user has sufficient permissions
3. Ensure user account is enabled

### Import Errors

**Issue:** `ModuleNotFoundError`

**Solutions:**
1. Activate virtual environment
2. Install dependencies: `pip install -r requirements.txt`
3. Install package: `pip install -e .`

### Timeout Issues

**Issue:** Commands timing out

**Solutions:**
1. Check router CPU usage
2. Verify network latency
3. Increase timeout: `MIKROTIK_CMD_TIMEOUT=60` in `.env.test`

---

## Performance Benchmarks

### Typical Execution Times

- **Core tests**: 5-10 seconds
- **Comprehensive tests**: 10-20 seconds
- **Hardware validation (single category)**: 0.2-2 seconds
- **Hardware validation (all categories)**: 30-60 seconds

### Optimization Tips

1. Test specific categories when developing
2. Use compact mode for quick checks
3. Run full suite in CI/CD only
4. Enable parallel test execution

---

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Test MikroTik MCP

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.8'
          
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          
      - name: Run tests
        run: pytest -v
        
      - name: Hardware validation
        if: github.event_name == 'push'
        env:
          MIKROTIK_HOST: ${{ secrets.MIKROTIK_HOST }}
          MIKROTIK_USERNAME: ${{ secrets.MIKROTIK_USERNAME }}
          MIKROTIK_PASSWORD: ${{ secrets.MIKROTIK_PASSWORD }}
        run: |
          python tests/hardware_validation.py --report results.json
          
      - name: Upload results
        uses: actions/upload-artifact@v2
        with:
          name: test-results
          path: results.json
```

---

## Contributing Tests

When adding new features:

1. Write tests first (TDD approach)
2. Ensure tests pass locally
3. Add integration tests for router interaction
4. Update this guide if adding new test types
5. Maintain test coverage above 90%

### Test Naming Convention

```python
# File: test_<module>.py
# Class: Test<Feature>
# Method: test_<specific_behavior>

def test_firewall_filter_rule_creation():
    """Test creating a firewall filter rule."""
    pass
```

---

## License

See main project [LICENSE](LICENSE) file.