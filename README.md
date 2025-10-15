# MikroTik Cursor MCP

**Enterprise-grade MikroTik automation optimized for Cursor IDE**

[![Version](https://img.shields.io/badge/version-4.8.0-blue.svg)](https://github.com/kevinpez/mikrotik-cursor-mcp)
[![Coverage](https://img.shields.io/badge/RouterOS%20Coverage-99%25-brightgreen.svg)](https://github.com/kevinpez/mikrotik-cursor-mcp)
[![Actions](https://img.shields.io/badge/Actions-382-blue.svg)](https://github.com/kevinpez/mikrotik-cursor-mcp)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

*Evolution of [mikrotik-mcp](https://github.com/jeff-nasseri/mikrotik-mcp) by [@jeff-nasseri](https://github.com/jeff-nasseri) - now with 99% RouterOS coverage, 382 actions, and complete enterprise features*

---

## 🎯 **What Is This?**

A **production-ready MCP (Model Context Protocol) server** that lets you manage MikroTik routers using **natural language** in Cursor IDE. Instead of remembering complex RouterOS commands, just describe what you want to do.

**Example:**
> "Create a WireGuard VPN tunnel to my AWS EC2 instance at 52.1.2.3"

The MCP server handles all the technical details - generating keys, configuring interfaces, setting up routes, and creating firewall rules.

---

## ⚡ **Key Highlights**

### **Comprehensive Coverage**
- ✅ **99% RouterOS Feature Coverage** (382 actions) - ENTERPRISE-COMPLETE!
- ✅ **19 Category-Based Tools** (optimized for Cursor)
- ✅ **Enterprise Features** (BGP, OSPF with Auth, IPv6 with Relay, Containers, VRRP, PKI)
- ✅ **Dual-Stack Networking** (Full IPv4 + IPv6)
- ✅ **Advanced QoS** (Queue Trees, PCQ, HTB)
- ✅ **High Availability** (VRRP, Watchdog)
- ✅ **Deep Packet Inspection** (Layer 7 Protocols)

### **Production-Ready**
- ✅ **Tested on Live Networks** (zero downtime)
- ✅ **Safety-First Design** (backup-before-change)
- ✅ **Natural Language Interface** (in Cursor IDE)
- ✅ **Workflow Automation** (one-command complex operations)

### **Modern Features**
- ✅ **VPN Suite** (WireGuard, OpenVPN, Certificate Management)
- ✅ **Container Support** (Docker on RouterOS v7.x)
- ✅ **Dynamic Routing** (BGP, OSPF, Route Filters)
- ✅ **Advanced Wireless** (CAPsMAN, security profiles)
- ✅ **Layer 7 DPI** (Application-aware firewall)
- ✅ **Advanced QoS** (Queue trees, PCQ, traffic shaping)
- ✅ **High Availability** (VRRP redundancy)
- ✅ **Automation** (Script scheduler, watchdog monitoring)

---

## 📦 **Installation**

### Prerequisites
- Python 3.8+
- Cursor IDE
- MikroTik RouterOS device with SSH enabled
- Network access to the router

### Quick Setup

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
        "MIKROTIK_PORT": "22"
      }
    }
  }
}
```

**Important:** Replace the paths and credentials with your actual values.

### Verify Installation

1. **Restart Cursor IDE** completely
2. Open a new Cursor chat
3. Try: "List all backups on my MikroTik router"

If configured correctly, you'll see your router's backups!

---

## 🎨 **What Can It Do?**

### **19 Categories × 259 Actions**

| Category | Actions | Capabilities |
|----------|---------|--------------|
| **🔥 Firewall** | 23 | Filter rules, NAT, port forwarding, mangle, RAW, connection tracking |
| **📡 DHCP** | 7 | DHCP servers, pools, leases, networks |
| **🌐 DNS** | 9 | DNS settings, static entries, cache management |
| **🛣️ Routes** | 27 | Static routes, BGP, OSPF, route filtering, routing marks |
| **🔌 Interfaces** | 22 | Statistics, enable/disable, bridges, PPPoE, tunnels, bonding |
| **📊 Diagnostics** | 7 | Ping, traceroute, bandwidth tests, DNS lookup, ARP table |
| **👥 Users** | 5 | User management, groups, permissions |
| **💾 Backup** | 4 | Create, list, restore backups, export config |
| **📝 Logs** | 4 | View, search, clear, export logs |
| **📶 Wireless** | 34 | Interfaces, CAPsMAN, security profiles, access lists, monitoring |
| **⚙️ System** | 11 | Resources, health, identity, NTP, reboot, license |
| **🏷️ VLAN** | 4 | VLAN interfaces, tagging |
| **🌍 IP** | 8 | IPv4 addresses, pools |
| **🔒 WireGuard** | 11 | Interfaces, peers, keys, tunnels |
| **🔐 OpenVPN** | 9 | Client/server interfaces, certificates |
| **🎯 Queues** | 7 | Bandwidth limiting, QoS, traffic shaping |
| **🏨 Hotspot** | 10 | Captive portal, users, walled garden |
| **🌐 IPv6** | 39 | Addresses, routes, ND, DHCPv6, firewall, pools |
| **📦 Container** | 18 | Docker containers, images, volumes, networking |

**Total: 259 actions providing 90% RouterOS coverage!**

---

## 🚀 **Usage Examples**

### **Natural Language Commands**

Just describe what you want to do in Cursor chat:

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
"Create a port forward: external 8080 → internal 192.168.1.100:80"
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

## 🏗️ **Architecture**

### Category-Based Organization

Unlike traditional flat tool structures, this MCP uses **category-based tools** that dramatically reduce complexity:

```
Traditional:                    This MCP:
├─ mikrotik_list_firewall       ├─ mikrotik_firewall
├─ mikrotik_create_firewall        ├─ list_filter_rules
├─ mikrotik_update_firewall        ├─ create_filter_rule
├─ mikrotik_list_nat               ├─ list_nat_rules
├─ mikrotik_create_nat             └─ ... (23 actions)
├─ mikrotik_port_forward        
... (100+ tools)                └─ mikrotik_ipv6 (39 actions)

❌ Exceeds Cursor limits         ✅ Within Cursor limits
❌ Hard to navigate              ✅ Easy to discover
❌ Slow loading                  ✅ Fast loading
```

### Technology Stack

- **Python 3.8+** - Core language
- **MCP SDK** - Model Context Protocol
- **Paramiko** - SSH connectivity
- **RouterOS CLI** - Direct command execution

### How It Works

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│  Cursor     │ Natural │  MikroTik    │   SSH   │  RouterOS   │
│  IDE + AI   │─────────▶   MCP        ├─────────▶   Device    │
│             │ Language │  Server      │         │             │
└─────────────┘         └──────────────┘         └─────────────┘
     │                         │                         │
     │  1. "Create VPN"        │                         │
     │─────────────────────────▶                         │
     │                         │  2. Generate config     │
     │                         │  3. Execute commands    │
     │                         ├────────────────────────▶│
     │                         │  4. Verify results      │
     │                         │◀────────────────────────│
     │  5. "VPN created ✓"     │                         │
     │◀─────────────────────────                         │
```

---

## 📚 **Feature Deep Dive**

### 🔥 **Firewall Management**

**23 actions** covering complete firewall functionality:

- **Filter Rules:** Allow, drop, reject traffic
- **NAT:** Source NAT, destination NAT, masquerade
- **Port Forwarding:** Easy external-to-internal mapping
- **Mangle:** Packet marking, routing marks
- **RAW:** Pre-connection tracking rules
- **Connection Tracking:** View active connections

**Example Workflow:**
```
1. "Create a filter rule to allow established connections"
2. "Add NAT masquerade on ether1"
3. "Set up port forwarding: 8080 → 192.168.1.100:80"
4. "Show me current connection tracking"
```

### 🌐 **IPv6 Support (NEW in v4.0.0)**

**39 actions** providing complete dual-stack networking:

- **Address Management:** Add, remove, list IPv6 addresses
- **Route Management:** Static IPv6 routes
- **Neighbor Discovery:** RA, SLAAC configuration
- **DHCPv6 Server:** Prefix delegation, stateful addressing
- **DHCPv6 Client:** Request prefixes from upstream
- **IPv6 Firewall:** Complete filter/NAT/mangle support
- **IPv6 Pools:** Manage IPv6 address pools

**Example Workflow:**
```
1. "Add IPv6 address 2001:db8::1/64 to bridgeLocal"
2. "Enable IPv6 router advertisements on bridge"
3. "Create DHCPv6 server with prefix delegation"
4. "Add IPv6 firewall rule to allow ICMPv6"
```

### 📦 **Container Support (NEW in v4.0.0)**

**18 actions** for Docker on RouterOS v7.x:

- **Lifecycle:** Create, start, stop, remove containers
- **Registry:** Configure private registries
- **Environment:** Manage environment variables
- **Storage:** Volume mounts
- **Networking:** Veth interfaces

**Example Workflow:**
```
1. "Set container registry to docker.io"
2. "Create container from nginx:latest"
3. "Create veth interface for container"
4. "Start the nginx container"
```

### 🔒 **VPN Suite**

**WireGuard (11 actions):**
- Interface management
- Peer configuration
- Automatic key generation
- Tunnel setup

**OpenVPN (9 actions):**
- Client configuration
- Server management
- Certificate handling

**Example:**
```
"Create WireGuard interface wg0 with public key ABC123..."
"Add WireGuard peer with endpoint 52.1.2.3:51820"
"List all WireGuard peers and their status"
```

### 🛣️ **Dynamic Routing**

**27 routing actions** including enterprise protocols:

**BGP (8 actions):**
- BGP instances
- Peer management
- Network advertisement
- Route viewing

**OSPF (7 actions):**
- OSPF instances
- Area configuration
- Interface setup
- Neighbor status

**Route Filters (2 actions):**
- Filter creation
- Policy-based routing

### 📡 **Wireless Management**

**34 actions** for complete wireless control:

**Basic Management:**
- Create/remove interfaces
- Enable/disable radios
- Security profiles (v6.x)
- Access lists

**CAPsMAN (Centralized Management):**
- Controller setup
- Configuration profiles
- Automatic provisioning
- Remote AP management

**Monitoring:**
- Client registration table
- Signal strength
- Frequency scanning

---

## 🎯 **Real-World Use Cases**

### **Home Lab Automation**
```
✓ "Set up WireGuard VPN to access my home network"
✓ "Create guest WiFi with isolated network"
✓ "Block ads using DNS firewall rules"
✓ "Set up bandwidth limits for IoT devices"
```

### **Enterprise Deployment**
```
✓ "Configure BGP peering with ISP"
✓ "Set up multi-site OSPF routing"
✓ "Deploy CAPsMAN for centralized AP management"
✓ "Create IPv6 dual-stack network"
```

### **Cloud Integration**
```
✓ "VPN tunnel to AWS VPC"
✓ "Connect to Azure Virtual Network"
✓ "Site-to-site VPN with GCP"
✓ "Container-based services on edge router"
```

### **Security & Compliance**
```
✓ "Implement zero-trust firewall rules"
✓ "Set up hotspot with captive portal"
✓ "Create segmented VLANs for PCI compliance"
✓ "Enable connection tracking for audit"
```

---

## 📈 **Version History**

### v4.0.0 - MAJOR (Current)
- ✅ **IPv6 Support** (39 actions)
- ✅ **Container Management** (18 actions)
- ✅ **90% RouterOS Coverage**
- ✅ **259 Total Actions**

### v3.5.0
- ✅ **Advanced Wireless** (17 actions)
- ✅ **CAPsMAN Support** (17 actions)
- ✅ **88% Coverage**

### v3.0.0 - MAJOR
- ✅ **BGP Support** (8 actions)
- ✅ **OSPF Support** (7 actions)
- ✅ **Route Filtering**
- ✅ **85% Coverage**

### v2.6.0
- ✅ **Hotspot Management** (10 actions)

### v2.5.0
- ✅ **PPPoE Support**
- ✅ **Tunnel Management** (EoIP, GRE)
- ✅ **Link Bonding**

### v2.4.0
- ✅ **Advanced Firewall** (mangle, RAW)
- ✅ **Connection Tracking**

### v2.3.0
- ✅ **OpenVPN Support** (9 actions)

### v2.1.0
- ✅ **WireGuard Support** (11 actions)

### v1.0.0
- ✅ **Initial Release**
- ✅ **Basic RouterOS Functions**

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

---

## 🔒 **Security Considerations**

### Credentials
- **Never commit credentials** to version control
- Use environment variables for sensitive data
- Consider using SSH keys instead of passwords

### Network Access
- Ensure **secure SSH access** to router
- Use **firewall rules** to restrict management access
- Enable **two-factor authentication** if available

### Backup Strategy
- **Always create backups** before major changes
- This MCP includes built-in backup commands
- Store backups in multiple locations

### Testing
- **Test on non-production** routers first
- Use **isolated VLANs** for experiments
- Have **out-of-band access** available

---

## 🐛 **Troubleshooting**

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
2. Check SSH is enabled: `/ip service print`
3. Test manual SSH: `ssh admin@192.168.88.1`
4. Verify firewall rules allow SSH

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

## 🤝 **Contributing**

Contributions are welcome! Here's how:

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

## 📄 **License**

MIT License - see [LICENSE](LICENSE) file

---

## 🙏 **Acknowledgments**

- **[@jeff-nasseri](https://github.com/jeff-nasseri)** - Original mikrotik-mcp project (~5,000 lines)
- **[@kevinpez](https://github.com/kevinpez)** - Nested architecture & enhancements (~1,500 lines)
- **MikroTik** - For excellent RouterOS
- **Anthropic** - For Claude and MCP protocol
- **Cursor Team** - For amazing AI-powered IDE

---

## 📞 **Support**

- **GitHub Issues:** [Report bugs or request features](https://github.com/kevinpez/mikrotik-cursor-mcp/issues)
- **GitHub Discussions:** [Ask questions or share use cases](https://github.com/kevinpez/mikrotik-cursor-mcp/discussions)
- **Documentation:** [Complete Setup Guide](SETUP_GUIDE.md) | [Capabilities Reference](CAPABILITIES.md) | [Real-World Examples](REAL_WORLD_EXAMPLES.md)
- **Troubleshooting:** See [SETUP_GUIDE.md](SETUP_GUIDE.md#troubleshooting) section

---

## 🌟 **Star History**

If this project helped you, please ⭐ star it on GitHub!

---

**Built with ❤️ for the MikroTik community**

*Making RouterOS automation accessible through natural language*
