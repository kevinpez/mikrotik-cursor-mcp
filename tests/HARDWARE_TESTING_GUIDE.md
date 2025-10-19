# MikroTik MCP Hardware Testing Guide

This guide explains how to run comprehensive hardware validation tests for the MikroTik MCP server.

## Overview

The hardware validation suite tests **every MCP command** against real MikroTik hardware, providing:

- ✅ Real-time progress with clear visual feedback
- ✅ Detailed per-command results showing what works and what fails
- ✅ Categorized testing (System, Firewall, Routing, etc.)
- ✅ Safe execution with automatic rollback
- ✅ Comprehensive JSON reports for analysis
- ✅ Color-coded CLI output for easy scanning

## Prerequisites

### 1. Environment Setup

You must configure your MikroTik connection details:

```bash
# On Linux/Mac
export MIKROTIK_HOST="192.168.88.1"
export MIKROTIK_USER="admin"
export MIKROTIK_PASSWORD="your-password"

# On Windows PowerShell
$env:MIKROTIK_HOST="192.168.88.1"
$env:MIKROTIK_USER="admin"
$env:MIKROTIK_PASSWORD="your-password"

# On Windows CMD
set MIKROTIK_HOST=192.168.88.1
set MIKROTIK_USER=admin
set MIKROTIK_PASSWORD=your-password
```

### 2. Dependencies

Ensure all dependencies are installed:

```bash
pip install -r requirements.txt
```

## Running Tests

### Quick Start - Test Everything

```bash
python tests/hardware_validation.py
```

This will:
1. Connect to your router
2. Test all command categories
3. Show real-time progress
4. Display comprehensive results

### Test Specific Category

```bash
# Test only System commands
python tests/hardware_validation.py --category System

# Test only Firewall commands
python tests/hardware_validation.py --category Firewall

# Test only Routing commands
python tests/hardware_validation.py --category Routing
```

### List Available Categories

```bash
python tests/hardware_validation.py --list-categories
```

Output example:
```
Available Test Categories:

   1. Backup                  (4 handlers)
   2. Certificates            (2 handlers)
   3. Containers              (17 handlers)
   4. DHCP                    (10 handlers)
   5. DHCPv6                  (16 handlers)
   6. Diagnostics             (7 handlers)
   7. DNS                     (7 handlers)
   8. Firewall                (47 handlers)
   9. Hotspot                 (10 handlers)
  10. Interfaces              (35 handlers)
  ... and more
```

### Verbose Output

Show detailed information for each test:

```bash
python tests/hardware_validation.py --verbose
python tests/hardware_validation.py -v --category System
```

Verbose mode shows:
- Command execution details
- Response output (truncated)
- Timing information
- Detailed error messages

### Save Results to File

Generate a detailed JSON report:

```bash
python tests/hardware_validation.py --report results.json
python tests/hardware_validation.py -v --category Firewall --report firewall_test.json
```

## Understanding the Output

### Real-Time Progress

During testing, you'll see:

```
Testing Category: System
────────────────────────────────────────────────────────────────────────────────
 [1/15] get_system_identity                              ✓ PASS
 [2/15] get_system_resources                             ✓ PASS
 [3/15] get_system_health                                ✓ PASS
 [4/15] get_uptime                                       ✓ PASS
 [5/15] list_packages                                    ✓ PASS
```

### Status Symbols

- `✓ PASS` (Green) - Command worked successfully
- `✗ FAIL` (Red) - Command failed or returned an error
- `⊘ SKIP` (Yellow) - Command skipped (not supported or dangerous)

### Category Summary

After each category:

```
Category Summary:
  Passed:  12/15 (80.0%)
  Failed:  1
  Skipped: 2
  Duration: 3.45s
```

### Final Results

At the end, you get a comprehensive report:

```
================================================================================
HARDWARE VALIDATION RESULTS
================================================================================

Overall Statistics:
  Total Tests:    245
  Passed:         198 (80.8%)
  Failed:         15
  Skipped:        32
  Duration:       45.23s

Results by Category:
────────────────────────────────────────────────────────────────────────────────
  ✓ System                    : 12/15 (80.0%) [F:1 S:2]
  ✓ Interfaces                : 28/35 (80.0%) [F:2 S:5]
  ✓ Firewall                  : 42/47 (89.4%) [F:3 S:2]
  ⚠ Routing                   : 15/28 (53.6%) [F:8 S:5]
  ✓ DNS                       :  6/7 (85.7%) [F:0 S:1]
  ... and more
```

## Test Categories

The following categories are tested:

### Network Basics
- **System** - System info, resources, NTP, identity
- **Interfaces** - Interface management, monitoring, bridges
- **IP Management** - IP addresses, pools, services
- **DNS** - DNS settings, static entries, cache

### Security & Firewall
- **Firewall** - Filter rules, NAT, mangle, raw, address lists
- **Users** - User management
- **Certificates** - Certificate management

### Routing & VPN
- **Routing** - Static routes, BGP, OSPF
- **WireGuard** - WireGuard VPN interfaces and peers
- **OpenVPN** - OpenVPN client and server
- **Tunnels/VPN** - PPPoE, EoIP, GRE tunnels

### Services
- **DHCP** - DHCP servers, networks, leases
- **DHCPv6** - DHCPv6 servers and clients
- **Hotspot** - Hotspot servers and users
- **QoS/Queues** - Traffic shaping and queues

### Advanced
- **IPv6** - IPv6 addressing, routing, firewall
- **Wireless** - Wireless interfaces, security, CAPsMAN
- **VLAN** - VLAN interface management
- **Containers** - Container management (RouterOS 7.x)

### Utilities
- **Diagnostics** - Ping, traceroute, ARP, neighbors
- **Backup** - Backup creation and listing
- **Logs** - Log viewing and searching
- **Safety/Workflow** - Safe mode and intelligent workflows

## Safety Features

The test suite includes multiple safety features:

### 1. Protected Resources
Never modifies:
- Critical interfaces (ether1, bridge, wlan1)
- Admin user account
- Critical services (SSH, API)

### 2. Dangerous Operations Skipped
Automatically skips:
- System reboot
- Backup restore
- User deletion
- Service disabling
- Log/connection flushing

### 3. Test Object Prefixing
All test objects created are prefixed with `mcp-hwtest-` for easy identification and cleanup.

### 4. Connectivity Checks
- Initial connectivity check before tests
- Final connectivity check after tests
- Warnings if connectivity is lost

### 5. Read-Only by Default
Most tests are read-only operations. Write operations are carefully controlled.

## Interpreting Results

### High Pass Rate (>90%)
✅ Your MCP server is working excellently with your hardware.

### Medium Pass Rate (70-90%)
⚠️ Most features work, but some issues need attention. Check failed tests.

### Low Pass Rate (<70%)
❌ Significant issues detected. Common causes:
- RouterOS version incompatibility
- Missing hardware features (no wireless, no containers, etc.)
- Configuration issues
- Network connectivity problems

### Common Skip Reasons

1. **"Feature not supported on this router model"**
   - Your router doesn't have this hardware/feature
   - Example: Wireless commands on a non-wireless router
   - This is normal and expected

2. **"Requires specific resource ID"**
   - Command needs an existing resource to operate on
   - Example: Deleting a specific firewall rule needs the rule ID
   - Safe to skip for validation

3. **"Dangerous operation - manually skipped"**
   - Command could disrupt router operation
   - Example: System reboot, user deletion
   - Intentionally skipped for safety

## Troubleshooting

### Cannot Connect to Router

```
✗ Cannot connect to router: Connection refused
```

**Solutions:**
1. Verify MIKROTIK_HOST is correct
2. Check firewall allows SSH from your IP
3. Verify credentials are correct
4. Test manual SSH: `ssh admin@192.168.88.1`

### Many "Not Supported" Errors

```
⊘ SKIP Feature not supported on this router model
```

**This is normal!** Different router models have different features:
- RouterBOARD vs x86
- Wireless vs non-wireless
- RouterOS version differences
- Hardware capabilities

### Connection Lost After Tests

```
⚠ WARNING: Lost connectivity to router!
```

**Possible causes:**
1. Test accidentally modified critical interface
2. Firewall rule blocked connection
3. Network issue

**Recovery:**
1. Access router via Winbox or console
2. Check for test objects (prefix: `mcp-hwtest-`)
3. Remove any test objects
4. Check interface and firewall configs

## JSON Report Format

When using `--report`, you get a detailed JSON file:

```json
{
  "start_time": "2025-10-19T10:30:00",
  "router_info": {
    "identity": "MikroTik"
  },
  "total_handlers": 245,
  "total_tests": 245,
  "passed": 198,
  "failed": 15,
  "skipped": 32,
  "duration_seconds": 45.23,
  "categories": {
    "System": {
      "total": 15,
      "passed": 12,
      "failed": 1,
      "skipped": 2,
      "duration": 3.45,
      "handlers": {
        "mikrotik_get_system_identity": {
          "status": "passed",
          "duration": 0.234
        }
      }
    }
  },
  "errors": [
    {
      "handler": "mikrotik_some_command",
      "category": "System",
      "reason": "Command returned error",
      "output": "ERROR: ..."
    }
  ]
}
```

Use this for:
- Automated CI/CD testing
- Historical comparison
- Detailed analysis
- Bug reporting

## Integration with CI/CD

Example GitHub Actions workflow:

```yaml
name: Hardware Validation

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - run: |
          export MIKROTIK_HOST=${{ secrets.MIKROTIK_HOST }}
          export MIKROTIK_USER=${{ secrets.MIKROTIK_USER }}
          export MIKROTIK_PASSWORD=${{ secrets.MIKROTIK_PASSWORD }}
          python tests/hardware_validation.py --report results.json
      - uses: actions/upload-artifact@v2
        with:
          name: test-results
          path: results.json
```

## Best Practices

### 1. Test on Non-Production Routers
Always test on development/test routers first.

### 2. Regular Testing
Run tests after:
- Code changes
- RouterOS upgrades
- Configuration changes
- Adding new features

### 3. Category-Specific Testing
During development, test specific categories:
```bash
# Working on firewall features?
python tests/hardware_validation.py -v --category Firewall --report fw.json
```

### 4. Compare Results
Save reports over time to track:
- Regression detection
- RouterOS upgrade impact
- Feature availability changes

### 5. Review Skipped Tests
Periodically review skipped tests to ensure they're skipped for valid reasons.

## Support

If you encounter issues:

1. **Check the output** - Error messages usually explain the problem
2. **Run with --verbose** - Get detailed information
3. **Test specific category** - Isolate the problem area
4. **Save a report** - Include in bug reports
5. **Check router logs** - Router may have additional details

## Example Workflows

### Quick Health Check
```bash
# Fast check - test critical categories only
python tests/hardware_validation.py --category System
python tests/hardware_validation.py --category Firewall
python tests/hardware_validation.py --category Routing
```

### Complete Validation
```bash
# Full test suite with report
python tests/hardware_validation.py -v --report full_validation_$(date +%Y%m%d).json
```

### Regression Testing
```bash
# Before making changes
python tests/hardware_validation.py --report before.json

# Make your changes...

# After changes
python tests/hardware_validation.py --report after.json

# Compare results
diff before.json after.json
```

### CI/CD Pipeline
```bash
# Automated testing
python tests/hardware_validation.py --report ci_results.json
exit_code=$?
if [ $exit_code -eq 0 ]; then
  echo "All tests passed!"
else
  echo "Tests failed - check results"
  cat ci_results.json
fi
exit $exit_code
```

