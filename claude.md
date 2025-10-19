# MikroTik MCP - Project Reference Guide

## Project Overview

**Project Name:** MikroTik Cursor MCP (Model Context Protocol Server)  
**Purpose:** Comprehensive automation and management of MikroTik RouterOS devices  
**Repository:** home-network-automation/mikrotik-mcp  
**Language:** Python  
**Architecture:** API-first with SSH fallback

---

## Project Structure

```
mikrotik-mcp/
├── src/
│   └── mcp_mikrotik/
│       ├── scope/             # Handler modules (46 files)
│       ├── tools/             # Tool definitions (30 files)
│       ├── safety/            # Safety manager
│       ├── settings/          # Configuration
│       ├── server.py          # MCP server
│       ├── api_connector.py   # RouterOS API client
│       ├── connection_manager.py
│       ├── mikrotik_ssh_client.py
│       └── logger.py
├── tests/
│   ├── hardware_validation.py # Hardware test suite
│   ├── test_core.py
│   ├── test_comprehensive.py
│   ├── integration/           # Integration tests
│   ├── HARDWARE_TESTING_GUIDE.md
│   ├── QUICK_REFERENCE.md
│   └── README.md
├── docs/
│   ├── guides/                # User guides
│   ├── setup/                 # Setup documentation
│   ├── testing/               # Testing documentation
│   ├── architecture/          # Architecture diagrams
│   ├── implementation/        # Implementation details
│   └── reports/               # Technical reports
├── examples/                  # Example scripts and configs
├── .env.test                  # Test environment configuration
├── README.md                  # Main documentation
├── TESTING.md                 # Testing guide
└── ENV_TEST_QUICK_START.md    # Environment setup guide
```

---

## Configuration

### Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `MIKROTIK_HOST` | Router IP address | Required |
| `MIKROTIK_USERNAME` | SSH/API username | Required |
| `MIKROTIK_PASSWORD` | SSH/API password | Required |
| `MIKROTIK_PORT` | SSH port | 22 |
| `MIKROTIK_LOG_LEVEL` | Logging verbosity | INFO |
| `MIKROTIK_CMD_TIMEOUT` | Command timeout (seconds) | 30 |
| `MIKROTIK_CONNECT_TIMEOUT` | Connection timeout (seconds) | 10 |

### Test Environment (.env.test)

Location: Project root directory

```bash
MIKROTIK_HOST=192.168.88.1
MIKROTIK_USERNAME=admin
MIKROTIK_PASSWORD=your_password
MIKROTIK_PORT=22
MIKROTIK_LOG_LEVEL=INFO
```

**Security:** File is in `.gitignore` - never commit credentials.

---

## Handler Categories

The MCP organizes 440+ handlers into 19 functional categories:

| Category | Handlers | Description |
|----------|----------|-------------|
| **Firewall** | 54 | Filter, NAT, Mangle, RAW, Layer 7, Chains, Address Lists |
| **System** | 42 | Identity, Resources, Packages, Scheduler, Watchdog |
| **IPv6** | 43 | Addresses, Routes, DHCPv6, Firewall, Neighbor Discovery |
| **Interfaces** | 53 | Physical, Virtual, Bridge, PPPoE, Tunnels, VLAN |
| **Wireless** | 39 | Interfaces, CAPsMAN, Security Profiles |
| **Routes** | 33 | Static, BGP, OSPF, Routing Filters |
| **Queues** | 20 | Simple, Queue Trees, Traffic Shaping |
| **Containers** | 18 | Docker Lifecycle, Images, Networking |
| **Users** | 18 | Management, Groups, Permissions |
| **IP Management** | 18 | Addresses, Pools, Services |
| **DNS** | 15 | Settings, Static Entries, Cache |
| **Certificates** | 11 | PKI, CA, SSL/TLS |
| **WireGuard** | 11 | VPN Interfaces, Peers, Keys |
| **Backup** | 10 | Create, Restore, Export |
| **Hotspot** | 10 | Servers, Users, Captive Portal |
| **Logs** | 10 | View, Search, Clear, Export |
| **OpenVPN** | 9 | Client, Server, Certificates |
| **Diagnostics** | 9 | Ping, Traceroute, ARP, DNS Lookup |
| **DHCP** | 7 | Servers, Pools, Leases |

---

## Testing Framework

### Hardware Validation Suite

Tests all handlers against live MikroTik hardware.

**Features:**
- Tests 440+ handler functions
- 19 test categories
- Verbose and compact output modes
- JSON report generation
- Safety features prevent dangerous operations
- Category-specific testing

**Usage:**
```bash
# All tests
python tests/hardware_validation.py

# Verbose output
python tests/hardware_validation.py -v

# Specific category
python tests/hardware_validation.py --category System -v

# Save report
python tests/hardware_validation.py --report results.json

# List categories
python tests/hardware_validation.py --list-categories
```

### Test Output Modes

**Verbose Mode:**
```
[1/10] get_system_identity

  Executing: mikrotik_get_system_identity
  Command executed in 0.45s
  
  Result:
  SYSTEM IDENTITY:
  name: test-router
  
  Command successful
```

**Compact Mode:**
```
[1/10] get_system_identity         PASS (0.45s)
[2/10] get_system_resources         PASS (0.38s)
```

### Status Indicators

- **PASS** - Handler executed successfully
- **FAIL** - Handler returned error
- **SKIP** - Handler skipped (dangerous or requires arguments)

---

## Common Workflows

### Running Tests

**PowerShell (Windows):**
```powershell
# Load environment
$env_content = Get-Content .env.test
foreach ($line in $env_content) { 
    if ($line -match '^([^=]+)=(.+)$') { 
        Set-Item -Path "env:$($matches[1])" -Value $matches[2]
    } 
}

# Run tests
python tests/hardware_validation.py -v
```

**Bash (Linux/Mac):**
```bash
# Load environment
export $(grep -v '^#' .env.test | xargs)

# Run tests
python tests/hardware_validation.py -v
```

### Category-Specific Testing

```bash
# System information
python tests/hardware_validation.py --category System -v

# Firewall configuration
python tests/hardware_validation.py --category Firewall -v

# Network diagnostics
python tests/hardware_validation.py --category Diagnostics -v

# DNS configuration
python tests/hardware_validation.py --category DNS -v

# IPv6 stack
python tests/hardware_validation.py --category IPv6 -v
```

### Automated Monitoring

```bash
# Daily validation with timestamped report
python tests/hardware_validation.py --report "daily_$(date +%Y%m%d).json"

# Pre-deployment validation
python tests/hardware_validation.py --report pre_deploy.json

# Post-configuration check
python tests/hardware_validation.py --category Firewall -v
```

---

## Connection Management

### API Connection (Primary)

- **Protocol:** RouterOS API
- **Ports:** 8728 (plain), 8729 (TLS)
- **Features:** Binary protocol, high performance
- **Fallback:** Automatic SSH fallback on failure

### SSH Connection (Fallback)

- **Protocol:** SSH (SSHv2)
- **Port:** 22 (default)
- **Features:** Text-based CLI commands
- **Retry:** 3 attempts with exponential backoff

---

## Safety Features

### Protected Operations

The following operations are automatically protected:

- **System reboot** - Skipped in test mode
- **Factory reset** - Skipped in test mode
- **Log clearing** - Requires explicit confirmation
- **User deletion** - Protects test user accounts
- **Configuration reset** - Skipped in test mode

### Test Mode Features

- **Safe defaults** - Handlers use non-destructive defaults
- **Automatic cleanup** - Test-created resources are removed
- **Test prefixes** - Resources marked with `mcp-test-` prefix
- **Skip dangerous** - Destructive operations automatically skipped
- **Rollback support** - Can revert test changes

---

## File Reference

### Core Files

| File | Purpose | Lines |
|------|---------|-------|
| `src/mcp_mikrotik/server.py` | Main MCP server | ~500 |
| `src/mcp_mikrotik/api_connector.py` | RouterOS API client | ~400 |
| `src/mcp_mikrotik/connection_manager.py` | Connection management | ~300 |
| `src/mcp_mikrotik/mikrotik_ssh_client.py` | SSH client | ~250 |

### Test Files

| File | Purpose |
|------|---------|
| `tests/hardware_validation.py` | Hardware validation suite |
| `tests/test_core.py` | Core functionality tests |
| `tests/test_comprehensive.py` | Comprehensive integration tests |
| `tests/integration/` | Integration test modules |

### Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Main project documentation |
| `TESTING.md` | Testing guide |
| `ENV_TEST_QUICK_START.md` | Environment setup guide |
| `tests/HARDWARE_TESTING_GUIDE.md` | Hardware testing details |
| `tests/QUICK_REFERENCE.md` | Command quick reference |

---

## Key Commands Reference

### Environment Setup

**PowerShell:**
```powershell
# Load .env.test
$env_content = Get-Content .env.test
foreach ($line in $env_content) { 
    if ($line -match '^([^=]+)=(.+)$') { 
        Set-Item -Path "env:$($matches[1])" -Value $matches[2]
    } 
}
```

**Bash:**
```bash
# Load .env.test
export $(grep -v '^#' .env.test | xargs)
```

### Test Execution

```bash
# All tests verbose
python tests/hardware_validation.py -v

# All tests compact
python tests/hardware_validation.py

# Specific category
python tests/hardware_validation.py --category System -v

# Save report
python tests/hardware_validation.py --report results.json

# List categories
python tests/hardware_validation.py --list-categories
```

---

## Performance Metrics

### Test Execution

- **Single category**: 0.2 - 2.0 seconds
- **All categories**: 30 - 60 seconds
- **Simple queries**: <100ms
- **Network diagnostics** (ping): 1-2 seconds
- **Write operations**: 100-500ms

### RouterOS Response

- **API latency**: 10-100ms
- **SSH latency**: 50-200ms
- **Ping to 8.8.8.8**: ~10ms
- **Command execution**: Sub-second for most operations

---

## Troubleshooting

### Connection Issues

**Symptom:** `Not connected to RouterOS API` or `Failed to connect`

**Solutions:**
1. Verify `MIKROTIK_HOST`, `MIKROTIK_USERNAME`, `MIKROTIK_PASSWORD` in `.env.test`
2. Check network connectivity: `ping <MIKROTIK_HOST>`
3. Verify SSH/API service is enabled on router
4. Check firewall rules allow access

### Authentication Failures

**Symptom:** `invalid user name or password (6)` or `Authentication failed`

**Solutions:**
1. Verify credentials in `.env.test`
2. Check user account is enabled on router
3. Verify user has sufficient permissions
4. Check for special characters in password

### Command Timeouts

**Symptom:** `Command timeout` or handler times out

**Solutions:**
1. Increase `MIKROTIK_CMD_TIMEOUT` in `.env.test`
2. Check router CPU usage: `/system resource print`
3. Verify network latency
4. Reduce concurrent operations

### Missing Arguments

**Symptom:** `Missing required argument: 'filename'`

**Solutions:**
- This is expected behavior - handler requires specific arguments
- Not a bug - indicates proper input validation
- Handler will be skipped in test mode

---

## Documentation Structure

### User Guides (docs/guides/)

- `INTELLIGENT_WORKFLOW_GUIDE.md` - Automation workflows
- `SECURITY_MAINTENANCE_GUIDE.md` - Security best practices
- `MIKROTIK_SAFE_MODE_GUIDE.md` - Safe operation procedures
- `OSPF_MCP_USAGE_EXAMPLE.md` - OSPF configuration examples
- `IP_SERVICES_GUIDE.md` - IP service management
- `NEIGHBOR_SCANNER_GUIDE.md` - Network discovery
- `TESTING_GUIDE.md` - Testing procedures

### Setup Documentation (docs/setup/)

- `SETUP_COMPLETE_GUIDE.md` - Detailed installation and configuration
- `DOCUMENTATION.md` - Documentation index

### Testing Documentation (docs/testing/)

- `TESTING_WORKFLOW.md` - Testing workflow
- `REAL_WORLD_EXAMPLES_TESTED.md` - Real-world test examples
- `TESTING_SUMMARY.md` - Testing overview

### Implementation Details (docs/implementation/)

- `AUTO_DISCOVERY_OSPF_IMPLEMENTATION_REPORT.md` - OSPF auto-discovery
- `OSPF_AUTODISCOVERY_MCP_INTEGRATION.md` - OSPF MCP integration
- `FINAL_SECURITY_REPORT.md` - Security implementation
- `SECURITY_IMPLEMENTATION_REPORT.md` - Security details
- `SAFETY_MODE_VERIFICATION.md` - Safety mode verification

### Technical Reports (docs/reports/)

- `API_CONVERSION_SUCCESS_REPORT.md` - API implementation
- `API_IMPROVEMENTS_REPORT.md` - API enhancements
- `CODE_REVIEW_REPORT_2025-10-18.md` - Code quality review
- `PROJECT_SUMMARY.md` - Project overview

---

## License

MIT License - See [LICENSE](LICENSE) file

---

**Last Updated:** 2025-10-19  
**Version:** 4.8.1  
**Status:** Production Ready
