# MikroTik Cursor MCP

A Model Context Protocol (MCP) server for managing MikroTik routers using natural language in Cursor IDE.

[![Version](https://img.shields.io/badge/version-4.8.1-blue.svg)](https://github.com/kevinpez/mikrotik-cursor-mcp)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

*Based on [mikrotik-mcp](https://github.com/jeff-nasseri/mikrotik-mcp) by [@jeff-nasseri](https://github.com/jeff-nasseri)*

---

## Overview

This MCP server provides a natural language interface to MikroTik RouterOS devices through Cursor IDE. It translates natural language requests into RouterOS commands via the MikroTik API with SSH fallback.

### Architecture

- **API-First Design**: Uses MikroTik API for fast, structured communication
- **SSH Fallback**: Automatically falls back to SSH when API is unavailable
- **Category-Based Tools**: Organizes 440+ actions into 19 logical categories
- **Dual Transport**: API and SSH support with automatic selection

---

## Quick Start

### Installation

```bash
cd mikrotik-mcp
python -m venv .venv
.venv\Scripts\activate  # Windows
# or: source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### Configure Cursor MCP

Update your Cursor MCP configuration file:

**Windows**: `%APPDATA%\Cursor\User\globalStorage\cursor.mcp\mcp.json`  
**macOS**: `~/Library/Application Support/Cursor/User/globalStorage/cursor.mcp/mcp.json`  
**Linux**: `~/.config/Cursor/User/globalStorage/cursor.mcp/mcp.json`

```json
{
  "mcpServers": {
    "mikrotik-cursor-mcp": {
      "command": "C:\\path\\to\\mikrotik-mcp\\.venv\\Scripts\\python.exe",
      "args": ["C:\\path\\to\\mikrotik-mcp\\src\\mcp_mikrotik\\server.py"],
      "env": {
        "MIKROTIK_HOST": "192.168.88.1",
        "MIKROTIK_USERNAME": "your_username", 
        "MIKROTIK_PASSWORD": "your_password"
      }
    }
  }
}
```

### Test Connection

Restart Cursor and ask: *"Show me my router's system information"*

For detailed setup instructions, see: **[SETUP_COMPLETE_GUIDE.md](docs/setup/SETUP_COMPLETE_GUIDE.md)**

---

## What Is This?

A production-ready MCP server that enables natural language management of MikroTik routers through Cursor IDE. Instead of memorizing RouterOS commands, describe your intent in plain language.

**Example:**
> "Create a WireGuard VPN tunnel to my AWS EC2 instance at 52.1.2.3"

The server translates this into the necessary RouterOS API calls or SSH commands to generate keys, configure interfaces, set up routes, and create firewall rules.

---

## Features

### Available Categories

| Category | Actions | Coverage |
|----------|---------|----------|
| **Firewall** | 54 | Filter, NAT, Mangle, RAW, Layer 7, Chains, Address Lists, Connections |
| **System** | 42 | Resources, Identity, Packages, Scheduler, Watchdog, Safe Mode |
| **IPv6** | 43 | Addresses, Routes, Firewall, DHCPv6, Neighbor Discovery |
| **Interfaces** | 53 | Physical, Virtual, Bridge, PPPoE, Tunnels, Bonding, VRRP, VLAN |
| **Wireless** | 39 | Interfaces, CAPsMAN, Security Profiles, Access Lists |
| **Routes** | 33 | Static, BGP, OSPF, Routing Filters |
| **Queues** | 20 | Simple, Queue Trees, Traffic Shaping |
| **Container** | 18 | Docker Containers, Images, Networking, Environment |
| **Certificates** | 11 | PKI, CA, SSL/TLS |
| **WireGuard** | 11 | Interfaces, Peers, Keys |
| **Hotspot** | 10 | Servers, Users, Captive Portal |
| **DNS** | 15 | Settings, Static Entries, Cache |
| **OpenVPN** | 9 | Client, Server, Certificates |
| **IP Management** | 18 | Addresses, Pools, Services |
| **DHCP** | 7 | Servers, Pools, Leases |
| **Users** | 18 | Management, Groups, Permissions |
| **Backup** | 10 | Create, Restore, Export |
| **Logs** | 10 | View, Search, Clear |
| **Diagnostics** | 9 | Ping, Traceroute, DNS Lookup, ARP, Neighbors |

**Total: 440+ actions across 19 categories**

### Core Capabilities

- **Dual-Stack Networking**: Full IPv4 and IPv6 support
- **VPN Suite**: WireGuard, OpenVPN, certificate management
- **Dynamic Routing**: BGP, OSPF with authentication, route filters
- **Container Support**: Docker containers on RouterOS v7.x
- **Advanced Wireless**: CAPsMAN centralized management
- **Layer 7 Inspection**: Application-aware firewall rules
- **QoS**: Queue trees, traffic shaping
- **High Availability**: VRRP redundancy
- **Automation**: Script scheduler, watchdog monitoring

---

## Installation

### Prerequisites

- Python 3.8+
- Cursor IDE
- MikroTik RouterOS device with SSH or API enabled
- Network access to the router

### Setup Steps

```bash
# 1. Clone the repository
git clone https://github.com/kevinpez/mikrotik-cursor-mcp.git
cd mikrotik-cursor-mcp

# 2. Create virtual environment
python -m venv .venv

# On Windows:
.venv\Scripts\activate

# On Linux/Mac:
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install the package
pip install -e .
```

### Configure Cursor IDE

Add this to your Cursor MCP configuration file (`%USERPROFILE%\.cursor\mcp.json` on Windows or `~/.cursor/mcp.json` on Linux/Mac):

```json
{
  "mcpServers": {
    "mikrotik-cursor-mcp": {
      "command": "python",
      "args": [
        "-m",
        "mcp_mikrotik.server"
      ],
      "cwd": "C:\\Users\\YourUsername\\mikrotik-cursor-mcp",
      "env": {
        "MIKROTIK_HOST": "192.168.88.1",
        "MIKROTIK_USERNAME": "admin",
        "MIKROTIK_PASSWORD": "your-password",
        "MIKROTIK_PORT": "22",
        "MIKROTIK_SSH_KEY": "C:\\Users\\YourUsername\\.ssh\\mikrotik_rsa", 
        "MIKROTIK_STRICT_HOST_KEY_CHECKING": "false",
        "MIKROTIK_KNOWN_HOSTS": "C:\\Users\\YourUsername\\.ssh\\known_hosts",
        "MIKROTIK_CONNECT_TIMEOUT": "10",
        "MIKROTIK_CMD_TIMEOUT": "30"
      }
    }
  }
}
```

**Important:** Replace the paths and credentials with your actual values.

### Verify Installation

1. Restart Cursor IDE completely
2. Open a new Cursor chat
3. Ask: "List all backups on my MikroTik router"

---

## Usage Examples

### Natural Language Commands

#### Basic Management
```
"Show me the system resources and uptime"
"List all network interfaces and their status"
"What's in my ARP table?"
"Create a backup called 'before-vpn-setup'"
```

#### Firewall & Security
```
"Create a firewall rule to allow SSH from 10.0.0.0/8"
"Block all traffic from 192.168.99.0/24"
"Show me active connections"
"Create a port forward: external 8080 to internal 192.168.1.100:80"
```

#### VPN Setup
```
"Set up a WireGuard VPN to my AWS server at 52.1.2.3"
"Create an OpenVPN client connection to my office"
"List all WireGuard interfaces and their status"
```

#### IPv6 Networking
```
"Add IPv6 address 2001:db8::1/64 to bridge"
"Enable IPv6 forwarding"
"List IPv6 neighbors"
"Create a DHCPv6 server on bridge interface"
```

#### Wireless Management
```
"List all wireless interfaces"
"Scan for nearby WiFi networks"
"Show connected wireless clients"
"Enable CAPsMAN controller"
```

#### Container Management (RouterOS v7.x)
```
"List all containers"
"Create a container from nginx:latest"
"Show container configuration"
"Create a veth interface for containers"
```

#### Dynamic Routing
```
"List BGP peers"
"Show OSPF neighbors"
"Create a route filter"
```

---

## Architecture

### Category-Based Organization

The MCP uses category-based tools to organize functionality:

```
Traditional Approach:          This MCP:
├─ mikrotik_list_firewall      ├─ mikrotik_firewall
├─ mikrotik_create_firewall        ├─ list_filter_rules
├─ mikrotik_update_firewall        ├─ create_filter_rule
├─ mikrotik_list_nat               ├─ list_nat_rules
├─ mikrotik_create_nat             └─ ... (54 actions)
├─ mikrotik_port_forward        
... (100+ separate tools)      └─ mikrotik_ipv6 (43 actions)
```

### Technology Stack

- **Python 3.8+** - Core language
- **MCP SDK** - Model Context Protocol implementation
- **RouterOS API** - Primary communication method
- **Paramiko** - SSH fallback connectivity
- **RouterOS CLI** - Command execution via SSH

### Communication Flow

```
┌───────────────┐       ┌────────────────────┐       ┌───────────────┐
│  Cursor IDE   │       │   MikroTik MCP     │       │   RouterOS    │
│      + AI     │──────▶│       Server       │──API▶ │    Device     │
└───────────────┘       └────────────────────┘       └───────────────┘
        │                          │                          │
│ Natural language request          │                          │
        │─────────────────────────▶                          │
        │                          │ Parse & translate        │
        │                          │ Execute via API/SSH      │
        │                          ├─────────────────────────▶
        │                          │ Verify results           │
        │                          │◀─────────────────────────│
│ Structured response               │                          │
◀─────────────────────────────────│                          │
```

---

## Testing

### Hardware Validation Suite

The project includes a comprehensive hardware validation suite that tests all handlers against live MikroTik hardware.

```bash
# Test all handlers
python tests/hardware_validation.py

# Test specific category with verbose output
python tests/hardware_validation.py --category System -v

# Save test results to JSON
python tests/hardware_validation.py --report results.json

# List available categories
python tests/hardware_validation.py --list-categories
```

### Test Configuration

Create a `.env.test` file in the project root:

```bash
MIKROTIK_HOST=192.168.88.1
MIKROTIK_USERNAME=admin
MIKROTIK_PASSWORD=your_password
MIKROTIK_PORT=22
MIKROTIK_LOG_LEVEL=INFO
```

### Test Categories

The test suite covers all 19 categories:
- System, Backup, Certificates, Containers
- DHCP, DNS, Diagnostics
- Firewall (Filter, NAT, Mangle, RAW)
- Hotspot, IP Services, IPv6
- Interfaces, Logs, OpenVPN
- Queues, Routes, Routing Filters
- Users, Wireless, WireGuard, CAPsMAN

See [TESTING.md](TESTING.md) for complete testing documentation.

---

## Security Considerations

### Credentials
- Never commit credentials to version control
- Use environment variables for sensitive data
- Consider SSH keys instead of passwords

### Network Access
- Ensure secure SSH/API access to router
- Use firewall rules to restrict management access
- Enable two-factor authentication if available

### Backup Strategy
- Create backups before major changes
- Use built-in backup commands
- Store backups in multiple locations

### Testing
- Test on non-production routers first
- Use isolated VLANs for experiments
- Maintain out-of-band access

---

## Troubleshooting

### MCP Not Loading

**Symptoms:** Cursor doesn't recognize MikroTik commands

**Solutions:**
1. Verify `mcp.json` path and format
2. Check Python path in configuration
3. Ensure virtual environment is activated
4. Restart Cursor completely

### Connection Issues

**Symptoms:** "Failed to connect" errors

**Solutions:**
1. Verify `MIKROTIK_HOST` is correct
2. Check SSH/API is enabled: `/ip service print`
3. Test manual SSH: `ssh admin@192.168.88.1`
4. Verify firewall rules allow SSH/API

### Command Failures

**Symptoms:** Commands return errors

**Solutions:**
1. Check RouterOS version compatibility
2. Verify required packages are installed
3. Check user permissions
4. Review router logs: `/log print`

### Performance Issues

**Symptoms:** Slow responses

**Solutions:**
1. Check network latency to router
2. Reduce concurrent operations
3. Verify router has sufficient resources
4. Update to latest RouterOS version

---

## Contributing

Contributions are welcome.

### Reporting Issues
- Use GitHub Issues
- Include RouterOS version
- Provide command examples
- Share error messages

### Feature Requests
- Check existing requests
- Describe use case
- Explain RouterOS capability

### Pull Requests
1. Fork the repository
2. Create feature branch
3. Test on live router
4. Update documentation
5. Submit PR with clear description

---

## License

MIT License - see [LICENSE](LICENSE) file

---

## Acknowledgments

- **[@jeff-nasseri](https://github.com/jeff-nasseri)** - Original mikrotik-mcp project
- **[@kevinpez](https://github.com/kevinpez)** - Extended implementation
- **MikroTik** - RouterOS platform
- **Anthropic** - Claude and MCP protocol
- **Cursor Team** - AI-powered IDE

---

## Support

- **GitHub Issues:** [Report bugs or request features](https://github.com/kevinpez/mikrotik-cursor-mcp/issues)
- **GitHub Discussions:** [Ask questions or share use cases](https://github.com/kevinpez/mikrotik-cursor-mcp/discussions)
- **Documentation:** See documentation section below

---

## Documentation

### Getting Started
- **[Quick Start](#quick-start)** - Installation and configuration
- **[Setup Guide](SETUP.md)** - Complete installation and configuration
- **[Testing Guide](TESTING.md)** - Comprehensive testing procedures

### User Guides
- **[Security Guide](SECURITY.md)** - Security best practices and hardening
- **[User Guides](GUIDES.md)** - IP Services and Safe Mode operations

### Development
- **[Contributing](CONTRIBUTING.md)** - Contribution guidelines
- **[Changelog](CHANGELOG.md)** - Version history
- **[Roadmap](ROADMAP.md)** - Future development plans
- **[License](LICENSE)** - MIT License

---

**MikroTik RouterOS automation through natural language**
