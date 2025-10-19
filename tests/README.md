# MikroTik MCP Test Suite

Comprehensive testing for the MikroTik Cursor MCP server.

---

## Overview

The test suite validates all MikroTik handler functions against live RouterOS hardware, ensuring compatibility and correctness across different RouterOS versions and configurations.

---

## Test Structure

```
tests/
├── README.md                      # This file
├── hardware_validation.py         # Hardware validation suite
├── HARDWARE_TESTING_GUIDE.md      # Detailed testing guide
├── QUICK_REFERENCE.md             # Command quick reference
├── test_core.py                   # Core functionality tests
├── test_comprehensive.py          # Comprehensive integration tests
└── integration/                   # Integration test modules
    ├── test_integration_runner.py
    ├── test_all_handlers.py
    ├── comprehensive_test_suite.py
    └── test_simple_integration.py
```

---

## Running Tests

### Hardware Validation (Recommended)

Test all handlers against your actual MikroTik router:

```bash
# Test all categories
python tests/hardware_validation.py

# Test specific category with verbose output
python tests/hardware_validation.py --category System -v

# Save results to JSON
python tests/hardware_validation.py --report results.json

# List available categories
python tests/hardware_validation.py --list-categories
```

### Core Tests

Test fundamental MCP functionality:

```bash
# Using pytest
pytest tests/test_core.py

# Using Python directly
python tests/test_core.py
```

### Comprehensive Tests

Test all MCP tools and handlers:

```bash
pytest tests/test_comprehensive.py
```

### Integration Tests

Test against live router (requires configuration):

```bash
pytest tests/integration/
```

---

## Test Configuration

Create `.env.test` in project root:

```bash
MIKROTIK_HOST=192.168.88.1
MIKROTIK_USERNAME=admin
MIKROTIK_PASSWORD=your_password
MIKROTIK_PORT=22
MIKROTIK_LOG_LEVEL=INFO
```

**Security Note:** The `.env.test` file is in `.gitignore` - never commit credentials.

---

## Test Types

### Hardware Validation Tests

**Purpose:** Validate all 440+ handlers against live hardware

**Features:**
- Tests every MikroTik handler function
- Real-time progress with status indicators
- Category-based organization (19 categories)
- Safe execution with automatic skip of dangerous operations
- Detailed JSON reports for CI/CD

**Output Modes:**
- **Compact**: One line per handler with pass/fail status
- **Verbose**: Detailed command execution information

### Core Tests

**Purpose:** Verify fundamental MCP functionality

**Coverage:**
- Connection management
- SSH client functionality  
- Basic RouterOS commands
- Error handling
- Configuration validation

### Comprehensive Tests

**Purpose:** Ensure complete feature coverage

**Coverage:**
- All 19 MCP tool categories
- Category-based tool organization
- Tool handler registration
- Schema validation
- End-to-end workflows

### Integration Tests

**Purpose:** Validate against actual MikroTik hardware

**Coverage:**
- Real router connectivity
- Command execution on live devices
- Multi-router scenarios
- Performance testing

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

## Contributing Tests

When adding new features:

1. Write tests first (TDD approach)
2. Ensure tests pass locally
3. Add integration tests for router interaction
4. Update this README if adding new test types
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

## Documentation

- **[Hardware Testing Guide](HARDWARE_TESTING_GUIDE.md)** - Comprehensive hardware test documentation
- **[Quick Reference](QUICK_REFERENCE.md)** - Quick command reference
- **[Main Testing Guide](../TESTING.md)** - Project-wide testing documentation

---

## License

See main project [LICENSE](../LICENSE) file.
