# Environment-Based Testing - Quick Start

Guide for using `.env.test` to configure and run hardware validation tests.

---

## Environment Configuration

### Create `.env.test` File

Create a file named `.env.test` in the project root directory with your MikroTik router credentials:

```bash
MIKROTIK_HOST=192.168.88.1
MIKROTIK_USERNAME=admin
MIKROTIK_PASSWORD=your_password
MIKROTIK_PORT=22
MIKROTIK_LOG_LEVEL=INFO
```

**Security Note:** This file is in `.gitignore` - never commit credentials to version control.

---

## Running Tests

### Load Environment and Run (PowerShell)

```powershell
# Load credentials from .env.test
$env_content = Get-Content .env.test
foreach ($line in $env_content) { 
    if ($line -match '^([^=]+)=(.+)$') { 
        Set-Item -Path "env:$($matches[1])" -Value $matches[2]
    } 
}

# Run tests
python tests/hardware_validation.py -v
```

### Load Environment and Run (Bash)

```bash
# Load credentials from .env.test
export $(grep -v '^#' .env.test | xargs)

# Run tests
python tests/hardware_validation.py -v
```

---

## Test Commands

### Basic Testing

```bash
# All tests - compact output
python tests/hardware_validation.py

# All tests - verbose output
python tests/hardware_validation.py -v

# Specific category
python tests/hardware_validation.py --category System -v

# List available categories
python tests/hardware_validation.py --list-categories

# Save results to JSON
python tests/hardware_validation.py --report results.json
```

### Category-Specific Tests

```bash
# System information
python tests/hardware_validation.py --category System -v

# Firewall rules
python tests/hardware_validation.py --category Firewall -v

# Network interfaces
python tests/hardware_validation.py --category Interfaces -v

# DNS configuration
python tests/hardware_validation.py --category DNS -v

# DHCP servers
python tests/hardware_validation.py --category DHCP -v

# Network diagnostics
python tests/hardware_validation.py --category Diagnostics -v

# IPv6 configuration
python tests/hardware_validation.py --category IPv6 -v

# Routing
python tests/hardware_validation.py --category Routes -v
```

---

## Output Modes

### Verbose Mode (Detailed)

Shows complete information for each test:

```bash
python tests/hardware_validation.py -v
```

**Displays:**
- Command being executed
- Arguments passed
- Execution time
- Full result output
- Success/failure status

**Example Output:**
```
[1/10] get_system_identity

  Executing: mikrotik_get_system_identity
  Command executed in 0.45s
  
  Result:
  SYSTEM IDENTITY:
  name: test-router
  
  Command successful
```

### Compact Mode (Quick Summary)

Shows one line per test:

```bash
python tests/hardware_validation.py
```

**Displays:**
- Handler position [1/10]
- Handler name
- Pass/fail status
- Execution time

**Example Output:**
```
[1/10] get_system_identity         PASS (0.45s)
[2/10] get_system_resources         PASS (0.38s)
[3/10] get_system_health            PASS (0.41s)
```

### Save Report (JSON)

Save detailed results to file:

```bash
python tests/hardware_validation.py -v --report results.json
```

---

## Test Scripts

### PowerShell Script

Create `run_tests.ps1`:

```powershell
# Load .env.test credentials
$env_content = Get-Content .env.test
foreach ($line in $env_content) { 
    if ($line -match '^([^=]+)=(.+)$') { 
        Set-Item -Path "env:$($matches[1])" -Value $matches[2]
    } 
}

# Run tests
if ($args.Count -gt 0) {
    python tests/hardware_validation.py -v --category $args[0]
} else {
    python tests/hardware_validation.py -v
}
```

**Usage:**
```powershell
.\run_tests.ps1              # All tests
.\run_tests.ps1 System       # System category
.\run_tests.ps1 Firewall     # Firewall category
```

### Batch Script (Windows)

Create `run_tests.bat`:

```batch
@echo off
REM Load .env.test
for /f "tokens=1,2 delims==" %%a in (type .env.test) do (
    set "%%a=%%b"
)

REM Run tests
python tests/hardware_validation.py -v %1
```

**Usage:**
```batch
run_tests.bat                    # All tests
run_tests.bat --category System  # Specific category
```

### Bash Script (Linux/Mac)

Create `run_tests.sh`:

```bash
#!/bin/bash

# Load .env.test
export $(grep -v '^#' .env.test | xargs)

# Run tests
if [ $# -gt 0 ]; then
    python tests/hardware_validation.py -v --category "$1"
else
    python tests/hardware_validation.py -v
fi
```

**Usage:**
```bash
./run_tests.sh              # All tests
./run_tests.sh System       # System category
./run_tests.sh Firewall     # Firewall category
```

---

## Available Test Categories

The hardware validation suite includes 19 categories:

1. **System** - Router identity, clock, resources, health
2. **Backup** - Backup creation and restoration
3. **Certificates** - Certificate management
4. **Containers** - Container lifecycle management
5. **DHCP** - DHCP server and client configuration
6. **DNS** - DNS settings and static entries
7. **Diagnostics** - Ping, traceroute, ARP, neighbors
8. **Firewall** - Filter rules, NAT, mangle, RAW
9. **Hotspot** - Hotspot server and user management
10. **IP Services** - SSH, API, Winbox access control
11. **IPv6** - IPv6 addresses, routing, DHCPv6
12. **Interfaces** - Physical and virtual interfaces
13. **Logs** - System logging and log management
14. **OpenVPN** - OpenVPN client/server configuration
15. **Queues** - Bandwidth limiting and QoS
16. **Routes** - Static routes and routing table
17. **Routing Filters** - Route filtering rules
18. **CAPsMAN** - Controller configuration for wireless
19. **Users** - User and group management
20. **Wireless** - Wireless interface configuration
21. **WireGuard** - WireGuard VPN tunnels

---

## Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `MIKROTIK_HOST` | Router IP address or hostname | `192.168.88.1` |
| `MIKROTIK_USERNAME` | SSH/API username | `admin` |
| `MIKROTIK_PASSWORD` | SSH/API password | `your_password` |

### Optional Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MIKROTIK_PORT` | `22` | SSH port number |
| `MIKROTIK_LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `MIKROTIK_CMD_TIMEOUT` | `30` | Command timeout in seconds |
| `MIKROTIK_CONNECT_TIMEOUT` | `10` | Connection timeout in seconds |

---

## Security Best Practices

### Protect Credentials

1. **Never commit** `.env.test` to version control
2. **Verify** `.env.test` is in `.gitignore`
3. **Use strong** passwords or SSH keys
4. **Restrict** file permissions: `chmod 600 .env.test`

### SSH Key Authentication

For enhanced security, use SSH key authentication:

```bash
MIKROTIK_HOST=192.168.88.1
MIKROTIK_USERNAME=admin
MIKROTIK_SSH_KEY=/path/to/private/key
MIKROTIK_PORT=22
```

### Access Control

Limit MikroTik API/SSH access:

1. Restrict source IPs in `/ip service`
2. Use strong passwords or keys
3. Enable firewall rules
4. Monitor access logs

---

## Troubleshooting

### Connection Failed

**Symptom:** `Failed to connect to router`

**Solutions:**
- Verify `MIKROTIK_HOST` is correct
- Check network connectivity: `ping <MIKROTIK_HOST>`
- Verify router is powered on
- Check firewall allows SSH/API access

### Authentication Failed

**Symptom:** `Authentication failed` or `invalid user name or password`

**Solutions:**
- Verify `MIKROTIK_USERNAME` and `MIKROTIK_PASSWORD`
- Check user account is enabled on router
- Verify user has sufficient permissions
- Check for special characters in password

### Module Not Found

**Symptom:** `ModuleNotFoundError`

**Solutions:**
- Activate virtual environment: `.venv\Scripts\activate`
- Install dependencies: `pip install -r requirements.txt`
- Install package: `pip install -e .`

### Timeout Errors

**Symptom:** Commands timing out

**Solutions:**
- Increase timeout: `MIKROTIK_CMD_TIMEOUT=60`
- Check router CPU usage
- Verify network latency
- Reduce concurrent operations

---

## Common Workflows

### Daily Monitoring

```powershell
# Windows Task Scheduler script
$env_content = Get-Content .env.test
foreach ($line in $env_content) { 
    if ($line -match '^([^=]+)=(.+)$') { 
        Set-Item -Path "env:$($matches[1])" -Value $matches[2]
    } 
}

$date = Get-Date -Format "yyyyMMdd-HHmmss"
python tests/hardware_validation.py --report "daily-$date.json"
```

### Pre-Deployment Validation

```bash
# Validate before deploying changes
export $(grep -v '^#' .env.test | xargs)
python tests/hardware_validation.py --report pre_deploy.json
```

### Post-Configuration Check

```bash
# Verify specific category after changes
export $(grep -v '^#' .env.test | xargs)
python tests/hardware_validation.py --category Firewall -v
```

### CI/CD Integration

```yaml
# GitHub Actions example
- name: Load test environment
  run: export $(grep -v '^#' .env.test | xargs)
  
- name: Run validation
  run: python tests/hardware_validation.py --report ${{ github.sha }}.json
```

---

## Example .env.test File

```bash
# MikroTik Router Connection
MIKROTIK_HOST=192.168.88.1
MIKROTIK_USERNAME=admin
MIKROTIK_PASSWORD=your_secure_password

# Connection Settings
MIKROTIK_PORT=22
MIKROTIK_CMD_TIMEOUT=30
MIKROTIK_CONNECT_TIMEOUT=10

# Logging
MIKROTIK_LOG_LEVEL=INFO

# Optional: SSH Key Authentication
# MIKROTIK_SSH_KEY=/path/to/ssh/key

# Optional: Known Hosts File
# MIKROTIK_KNOWN_HOSTS=/path/to/known_hosts
```

---

## Additional Resources

- **[Testing Guide](TESTING.md)** - Complete testing documentation
- **[Hardware Testing Guide](tests/HARDWARE_TESTING_GUIDE.md)** - Detailed hardware test guide
- **[Quick Reference](tests/QUICK_REFERENCE.md)** - Command quick reference

---

## License

See main project [LICENSE](LICENSE) file.
