# Setup Guide

Complete setup and configuration guide for the MikroTik Cursor MCP server.

---

## Prerequisites

- **Router**: MikroTik router with RouterOS 6.0+ (tested on RouterOS 7.19.4)
- **Computer**: Windows 10/11, macOS, or Linux
- **Software**: Python 3.8+, Cursor IDE
- **Network**: SSH access to your MikroTik router

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/kevinpez/mikrotik-cursor-mcp.git
cd mikrotik-cursor-mcp
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Router Configuration

### Gather Router Information

You'll need:
- **Router IP**: Usually `192.168.88.1` (default MikroTik IP)
- **Username**: Usually `admin`
- **Password**: Your router password
- **SSH Port**: Usually `22`

### Test SSH Access

```bash
ssh admin@192.168.88.1
# Enter your password when prompted
```

### Enable API Access (Recommended)

1. Open WinBox or SSH to your router
2. Go to **IP → Services**
3. Enable **API** service
4. Set **API** to listen on port `8728`

---

## Cursor MCP Configuration

### 1. Locate Cursor MCP Configuration

**Windows**: `%APPDATA%\Cursor\User\globalStorage\cursor.mcp\mcp.json`  
**macOS**: `~/Library/Application Support/Cursor/User/globalStorage/cursor.mcp/mcp.json`  
**Linux**: `~/.config/Cursor/User/globalStorage/cursor.mcp/mcp.json`

### 2. Add MikroTik MCP Server

```json
{
  "mcpServers": {
    "mikrotik-cursor-mcp": {
      "command": "C:\\path\\to\\mikrotik-mcp\\.venv\\Scripts\\python.exe",
      "args": ["C:\\path\\to\\mikrotik-mcp\\src\\mcp_mikrotik\\server.py"],
      "env": {
        "MIKROTIK_HOST": "192.168.88.1",
        "MIKROTIK_USERNAME": "admin",
        "MIKROTIK_PASSWORD": "your_password",
        "MIKROTIK_PORT": "22"
      }
    }
  }
}
```

### 3. Restart Cursor

After updating the configuration, restart Cursor IDE to load the MCP server.

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

## Testing Your Setup

### Load Environment and Run Tests

**PowerShell (Windows):**
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

**Bash (Linux/Mac):**
```bash
# Load credentials from .env.test
export $(grep -v '^#' .env.test | xargs)

# Run tests
python tests/hardware_validation.py -v
```

### Quick Test Commands

```bash
# Test all handlers
python tests/hardware_validation.py

# Test specific category
python tests/hardware_validation.py --category System -v

# Save results to JSON
python tests/hardware_validation.py --report results.json

# List available categories
python tests/hardware_validation.py --list-categories
```

---

## Using the MCP Server

### In Cursor IDE

Once configured, you can use natural language to manage your MikroTik router:

```
"Show me the system resources and uptime"
"List all network interfaces and their status"
"Create a firewall rule to allow SSH from 10.0.0.0/8"
"Set up a WireGuard VPN to my AWS server at 52.1.2.3"
```

### Available Categories

The MCP server provides 440+ actions across 19 categories:

- **System** - Identity, resources, clock, health
- **Firewall** - Filter, NAT, mangle, RAW rules
- **Interfaces** - Physical, virtual, bridge, VLAN
- **Routes** - Static routes, BGP, OSPF
- **IPv6** - Addresses, routes, DHCPv6, firewall
- **Wireless** - Interfaces, CAPsMAN, security
- **DNS** - Settings, static entries, cache
- **DHCP** - Servers, pools, leases
- **Users** - User management, groups
- **WireGuard** - VPN interfaces and peers
- **OpenVPN** - Client, server, certificates
- **Containers** - Docker lifecycle, networking
- **Certificates** - PKI, CA, SSL/TLS
- **Backup** - Create, restore, export
- **Hotspot** - Servers, users, captive portal
- **IP Management** - Addresses, pools, services
- **Queues** - Simple queues, queue trees
- **Logs** - View, search, clear
- **Diagnostics** - Ping, traceroute, ARP

---

## Troubleshooting

### Connection Issues

**Issue:** `Failed to connect to router`

**Solutions:**
1. Verify `MIKROTIK_HOST` in configuration
2. Check network connectivity: `ping 192.168.88.1`
3. Verify SSH/API is enabled on router
4. Check firewall rules allow access

### Authentication Failures

**Issue:** `Authentication failed`

**Solutions:**
1. Verify credentials in configuration
2. Check user has sufficient permissions
3. Ensure user account is enabled

### Import Errors

**Issue:** `ModuleNotFoundError`

**Solutions:**
1. Activate virtual environment
2. Install dependencies: `pip install -r requirements.txt`
3. Install package: `pip install -e .`

### MCP Server Not Loading

**Issue:** MCP server not appearing in Cursor

**Solutions:**
1. Check JSON syntax in mcp.json
2. Verify file paths are correct
3. Restart Cursor IDE
4. Check Cursor logs for errors

---

## Security Best Practices

### Credential Management

- Never commit credentials to version control
- Use environment variables for sensitive data
- Regularly rotate passwords
- Use dedicated service accounts when possible

### Network Security

- Restrict SSH/API access to specific IP ranges
- Use strong passwords or SSH keys
- Enable firewall rules to protect services
- Regularly update RouterOS firmware

### Testing Safety

- Use test environment when possible
- Create backups before making changes
- Test changes in non-production environments
- Use Safe Mode for risky operations

---

## Next Steps

1. **Run Tests**: Verify your setup with the hardware validation suite
2. **Explore Features**: Try different natural language commands
3. **Read Documentation**: Check the [Testing Guide](TESTING.md) for detailed testing procedures
4. **Join Community**: Report issues and contribute improvements

---

## Support

- **Issues**: [GitHub Issues](https://github.com/kevinpez/mikrotik-cursor-mcp/issues)
- **Documentation**: See [README.md](README.md) for project overview
- **Testing**: See [TESTING.md](TESTING.md) for testing procedures

---

**Last Updated**: 2025-10-19  
**Version**: 4.8.1
