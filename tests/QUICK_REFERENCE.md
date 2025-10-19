# Hardware Testing Quick Reference Card

## Setup (One-Time)

```bash
# Linux/Mac
export MIKROTIK_HOST="192.168.88.1"
export MIKROTIK_USER="admin"
export MIKROTIK_PASSWORD="your-password"

# Windows PowerShell
$env:MIKROTIK_HOST="192.168.88.1"
$env:MIKROTIK_USER="admin"
$env:MIKROTIK_PASSWORD="your-password"

# Windows CMD
set MIKROTIK_HOST=192.168.88.1
set MIKROTIK_USER=admin
set MIKROTIK_PASSWORD=your-password
```

## Most Common Commands

### Test Everything
```bash
python tests/hardware_validation.py
```

### Test Specific Category
```bash
python tests/hardware_validation.py --category System
python tests/hardware_validation.py --category Firewall
python tests/hardware_validation.py --category Routing
```

### See All Categories
```bash
python tests/hardware_validation.py --list-categories
```

### Verbose Output (Show Details)
```bash
python tests/hardware_validation.py -v
python tests/hardware_validation.py --category Firewall -v
```

### Save Report
```bash
python tests/hardware_validation.py --report results.json
python tests/hardware_validation.py -v --category System --report system.json
```

## All Test Categories

Quick copy-paste commands for each category:

```bash
# Network Basics
python tests/hardware_validation.py --category System
python tests/hardware_validation.py --category Interfaces
python tests/hardware_validation.py --category "IP Management"
python tests/hardware_validation.py --category DNS

# Security
python tests/hardware_validation.py --category Firewall
python tests/hardware_validation.py --category Users
python tests/hardware_validation.py --category Certificates

# Routing & VPN
python tests/hardware_validation.py --category Routing
python tests/hardware_validation.py --category WireGuard
python tests/hardware_validation.py --category OpenVPN
python tests/hardware_validation.py --category "Tunnels/VPN"

# Services
python tests/hardware_validation.py --category DHCP
python tests/hardware_validation.py --category DHCPv6
python tests/hardware_validation.py --category Hotspot
python tests/hardware_validation.py --category "QoS/Queues"

# Advanced
python tests/hardware_validation.py --category IPv6
python tests/hardware_validation.py --category Wireless
python tests/hardware_validation.py --category VLAN
python tests/hardware_validation.py --category Containers

# Utilities
python tests/hardware_validation.py --category Diagnostics
python tests/hardware_validation.py --category Backup
python tests/hardware_validation.py --category Logs
```

## Output Symbols

- `✓ PASS` = Command worked ✅
- `✗ FAIL` = Command failed ❌
- `⊘ SKIP` = Command skipped (not supported or dangerous) ⚠️

## Example Workflows

### Quick Health Check (5 categories, ~2 min)
```bash
python tests/hardware_validation.py --category System
python tests/hardware_validation.py --category Interfaces
python tests/hardware_validation.py --category Firewall
python tests/hardware_validation.py --category Routing
python tests/hardware_validation.py --category DNS
```

### Complete Validation (~10 min)
```bash
python tests/hardware_validation.py -v --report full_validation.json
```

### Regression Testing (Before/After Changes)
```bash
# Before changes
python tests/hardware_validation.py --report before.json

# Make your changes...

# After changes
python tests/hardware_validation.py --report after.json

# Compare
diff before.json after.json
```

## Troubleshooting

### Can't Connect
```bash
# Verify router is reachable
ping $MIKROTIK_HOST

# Test SSH manually
ssh admin@$MIKROTIK_HOST

# Check environment variables
echo $MIKROTIK_HOST
echo $MIKROTIK_USER
```

### Many "Not Supported" Errors
This is **normal**! Different routers have different features:
- No wireless on non-wireless routers
- No containers on older RouterOS
- Different capabilities per model

### Want More Details
Use verbose mode:
```bash
python tests/hardware_validation.py -v --category System
```

## CI/CD Integration

### Single Command for CI
```bash
python tests/hardware_validation.py --report ci_results.json || exit 1
```

### Check Specific Pass Rate
```bash
python tests/hardware_validation.py --report results.json
# Exit code 0 = all passed
# Exit code 1 = some failures
```

## Pro Tips

1. **Start with one category** to understand the output
2. **Use verbose mode** when debugging specific commands
3. **Save reports** for historical comparison
4. **Test after RouterOS upgrades** to catch breaking changes
5. **Category names are case-sensitive** (use --list-categories)

## Help

Full documentation: `tests/HARDWARE_TESTING_GUIDE.md`

```bash
python tests/hardware_validation.py --help
```

