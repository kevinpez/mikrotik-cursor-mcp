# Testing Guide

Comprehensive testing documentation for the MikroTik Cursor MCP server.

---

## Overview

The MikroTik MCP includes a hardware validation suite that tests all 440+ handler functions against live MikroTik routers. This ensures that every command works correctly with your specific RouterOS configuration.

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

## Test Modes

### Compact Mode (Default)

Shows one line per handler with pass/fail status:

```bash
python tests/hardware_validation.py --category System
```

**Output:**
```
[1/10] get_system_identity         PASS (0.45s)
[2/10] get_system_resources         PASS (0.38s)
[3/10] get_system_health            PASS (0.41s)
```

**Best for:**
- Quick status checks
- CI/CD pipelines
- Monitoring scripts
- Production validation

### Verbose Mode

Shows detailed command execution information:

```bash
python tests/hardware_validation.py --category System -v
```

**Output:**
```
[1/10] get_system_identity

  Executing: mikrotik_get_system_identity
  Command executed in 0.45s
  
  Result:
  SYSTEM IDENTITY:
  name: test-router
  
  Command successful
```

**Best for:**
- Debugging failures
- Learning RouterOS API
- Detailed analysis
- Development

---

## Test Categories

The test suite covers 19 functional categories:

| Category | Handlers | Description |
|----------|----------|-------------|
| **System** | 13 | Identity, resources, clock, health, packages |
| **Firewall** | 54 | Filter rules, NAT, mangle, RAW, Layer 7 |
| **Interfaces** | 53 | Physical, virtual, bridge, VLAN, bonding |
| **Routes** | 33 | Static routes, BGP, OSPF, filters |
| **IPv6** | 43 | Addresses, routes, DHCPv6, firewall |
| **Wireless** | 39 | Interfaces, CAPsMAN, security |
| **DNS** | 15 | Settings, static entries, cache |
| **DHCP** | 7 | Servers, pools, leases |
| **Users** | 18 | User management, groups, permissions |
| **WireGuard** | 11 | Interfaces, peers, keys |
| **OpenVPN** | 9 | Client, server, certificates |
| **Containers** | 18 | Docker lifecycle, images, networking |
| **Certificates** | 11 | PKI, CA, SSL/TLS |
| **Backup** | 10 | Create, restore, export |
| **Hotspot** | 10 | Servers, users, captive portal |
| **IP Management** | 18 | Addresses, pools, services |
| **Queues** | 20 | Simple queues, queue trees, QoS |
| **Logs** | 10 | View, search, clear |
| **Diagnostics** | 9 | Ping, traceroute, ARP, DNS lookup |

---

## Test Output Components

### Verbose Output

Each test shows:

1. **Handler Number** - Position in category [1/10]
2. **Handler Name** - Function being tested
3. **Executing** - Exact command name
4. **Arguments** - Parameters passed (if any)
5. **Execution Time** - How long it took
6. **Result** - Command output (first 500 chars)
7. **Status** - Success/failure/skip indicator

### Status Indicators

- **PASS** - Command executed successfully
- **FAIL** - Command returned error
- **SKIP** - Command skipped (requires arguments or dangerous)

---

## Common Test Scenarios

### Pre-Deployment Validation

Validate router before deploying changes:

```bash
python tests/hardware_validation.py --report pre_deploy_$(date +%Y%m%d).json
```

### Post-Configuration Check

Verify specific category after configuration changes:

```bash
python tests/hardware_validation.py --category Firewall -v
```

### Daily Monitoring

Schedule regular tests to catch configuration drift:

```powershell
# Windows Task Scheduler
python tests/hardware_validation.py --report daily_$(Get-Date -f 'yyyyMMdd').json
```

```bash
# Linux cron
0 2 * * * cd /path/to/mikrotik-mcp && python tests/hardware_validation.py --report daily_$(date +%Y%m%d).json
```

### CI/CD Integration

Integrate into continuous integration pipeline:

```yaml
# GitHub Actions example
- name: Validate MikroTik Configuration
  run: |
    python tests/hardware_validation.py --report ${{ github.sha }}.json
```

### Debug Specific Handler

Test individual handler in verbose mode:

```bash
python tests/hardware_validation.py --category System -v 2>&1 | grep -A 20 "get_system_identity"
```

---

## Understanding Results

### Expected Pass Rates

Different categories have different expected pass rates:

- **Read Operations** (list, get): 80-95%
- **Write Operations** (create, update): 30-50% (many require specific arguments)
- **Diagnostic Operations**: 60-80%

### Why Handlers Are Skipped

Handlers are skipped for safety or missing arguments:

- **Dangerous Operations**: reboot, clear_logs, factory_reset
- **Missing Arguments**: Operations requiring specific IDs, filenames, etc.
- **Hardware Dependent**: Features not available on all models

### Common "Failures" (Not Bugs)

Some failures are expected and indicate proper validation:

- **Missing Arguments**: Handler correctly validates input
- **Invalid IDs**: Cannot modify non-existent resources
- **Type Validation**: Handler rejects invalid parameter types
- **RouterOS Version**: Feature not available in current version

---

## Troubleshooting

### Connection Errors

**Symptom:** `Failed to connect to router`

**Solutions:**
1. Verify `MIKROTIK_HOST` in `.env.test`
2. Check network connectivity: `ping 192.168.88.1`
3. Verify credentials
4. Ensure SSH/API is enabled on router

### Authentication Failures

**Symptom:** `Authentication failed` or `invalid user name or password`

**Solutions:**
1. Verify password in `.env.test`
2. Check user has sufficient permissions
3. Ensure user account is enabled
4. Verify RouterOS user group settings

### Timeout Issues

**Symptom:** Commands timing out

**Solutions:**
1. Check router CPU usage: `/system resource print`
2. Verify network latency
3. Increase timeout in `.env.test`: `MIKROTIK_CMD_TIMEOUT=60`
4. Check for hanging processes on router

### Module Import Errors

**Symptom:** `ModuleNotFoundError` or import errors

**Solutions:**
1. Ensure virtual environment is activated
2. Install dependencies: `pip install -r requirements.txt`
3. Install package in development mode: `pip install -e .`

---

## Test Configuration

### Environment Variables

All test configuration via `.env.test`:

| Variable | Default | Purpose |
|----------|---------|---------|
| `MIKROTIK_HOST` | Required | Router IP address |
| `MIKROTIK_USERNAME` | Required | SSH/API username |
| `MIKROTIK_PASSWORD` | Required | SSH/API password |
| `MIKROTIK_PORT` | 22 | SSH port |
| `MIKROTIK_LOG_LEVEL` | INFO | Logging verbosity |
| `MIKROTIK_CMD_TIMEOUT` | 30 | Command timeout (seconds) |
| `MIKROTIK_CONNECT_TIMEOUT` | 10 | Connection timeout (seconds) |

### Loading Environment

**PowerShell (Windows):**
```powershell
$env_content = Get-Content .env.test
foreach ($line in $env_content) { 
    if ($line -match '^([^=]+)=(.+)$') { 
        Set-Item -Path "env:$($matches[1])" -Value $matches[2]
    } 
}
python tests/hardware_validation.py -v
```

**Bash (Linux/Mac):**
```bash
export $(grep -v '^#' .env.test | xargs)
python tests/hardware_validation.py -v
```

---

## Performance Metrics

### Typical Execution Times

- **Single Category**: 0.2 - 2.0 seconds
- **All Categories**: 30 - 60 seconds
- **Simple Queries** (get, list): <100ms
- **Diagnostic Commands** (ping): 1-2 seconds
- **Write Operations**: 100-500ms

### Performance Tips

1. **Use Category Testing**: Test only what you need
2. **Parallel Execution**: Run multiple category tests in parallel
3. **Local Router**: Test against local router for faster execution
4. **Skip Dangerous**: Skipped handlers save time

---

## Safety Features

### Protected Operations

The test suite automatically skips dangerous operations:

- **System reboot**
- **Factory reset**
- **Log clearing** (unless explicitly requested)
- **User deletion** (protects test user)
- **Configuration reset**

### Test Isolation

- Test prefixes identify test-created resources
- Automatic cleanup after tests
- No permanent configuration changes
- Read operations are prioritized

### Rollback Protection

- No destructive operations by default
- Explicit confirmation required for dangerous actions
- Test mode indicators
- Dry-run support for development

---

## Advanced Usage

### Custom Test Prefix

Set custom prefix for test resources:

```python
# In test file
TEST_PREFIX = "mytest-"
```

### Filter Specific Handlers

Test only handlers matching pattern:

```bash
python tests/hardware_validation.py --category System -v | grep "get_system"
```

### Export Results for Analysis

```bash
python tests/hardware_validation.py --report results.json
cat results.json | jq '.categories[] | select(.status=="FAIL")'
```

### Continuous Monitoring

Create monitoring script:

```python
#!/usr/bin/env python3
import subprocess
import json
from datetime import datetime

result = subprocess.run(
    ['python', 'tests/hardware_validation.py', '--report', 'temp.json'],
    capture_output=True
)

with open('temp.json') as f:
    data = json.load(f)
    
if data['summary']['failed'] > 0:
    # Send alert
    print(f"ALERT: {data['summary']['failed']} tests failed")
```

---

## Test Development

### Adding New Test Categories

Tests are auto-discovered from handler functions in `src/mcp_mikrotik/scope/`.

1. Create new scope file: `src/mcp_mikrotik/scope/myfeature.py`
2. Define handlers with `mikrotik_` prefix
3. Run tests - automatically included

### Handler Naming Convention

```python
def mikrotik_<action>_<resource>(action: str, **kwargs):
    """
    <Description of what handler does>
    
    Args:
        action: The action to perform
        **kwargs: Additional arguments
        
    Returns:
        dict: Result from RouterOS
    """
```

### Test Configuration Per Handler

Some handlers require specific test configurations. Add to test suite:

```python
HANDLER_CONFIG = {
    "mikrotik_create_user": {
        "skip": True,
        "reason": "Requires explicit confirmation"
    },
    "mikrotik_ping": {
        "args": {"address": "8.8.8.8", "count": 2}
    }
}
```

---

## Reporting Issues

When reporting test failures:

1. **Include RouterOS version**: `/system resource print`
2. **Run verbose mode**: `--category <Category> -v`
3. **Save results**: `--report issue.json`
4. **Check router logs**: `/log print`
5. **Verify network**: Test manual SSH connection

---

## Additional Resources

- **Hardware Testing Guide**: `tests/HARDWARE_TESTING_GUIDE.md`
- **Quick Reference**: `tests/QUICK_REFERENCE.md`
- **Example Scripts**: `examples/run_hardware_tests.{sh,bat}`
- **Test Suite Source**: `tests/hardware_validation.py`

---

## License

See main project [LICENSE](LICENSE) file.
