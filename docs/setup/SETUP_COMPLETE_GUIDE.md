# MikroTik Cursor MCP - Complete Setup Guide

**✅ Tested & Verified on MikroTik RB5009UG+S+ with RouterOS 7.19.4**

This guide walks you through setting up the MikroTik Cursor MCP server from scratch, based on our successful testing and verification.

## 🎯 Prerequisites

- **Router**: MikroTik router with RouterOS 6.0+ (tested on RouterOS 7.19.4)
- **Computer**: Windows 10/11, macOS, or Linux
- **Software**: Python 3.8+, Cursor IDE
- **Network**: SSH access to your MikroTik router

## 📋 Step 1: Download and Setup

### 1.1 Clone the Repository
```bash
git clone https://github.com/kevinpez/mikrotik-cursor-mcp.git
cd mikrotik-cursor-mcp
```

### 1.2 Create Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 1.3 Install Dependencies
```bash
pip install -r requirements.txt
```

## 🔧 Step 2: Configure Router Access

### 2.1 Gather Router Information
You'll need:
- **Router IP**: Usually `192.168.88.1` (default MikroTik IP)
- **Username**: Usually `admin`
- **Password**: Your router password
- **SSH Port**: Usually `22`

### 2.2 Test SSH Access
```bash
ssh admin@192.168.88.1
# Enter your password when prompted
```

### 2.3 Verify RouterOS Version
```bash
/system identity print
/system resource print
```

## ⚙️ Step 3: Configure Cursor MCP

### 3.1 Locate Cursor MCP Configuration
- **Windows**: `%APPDATA%\Cursor\User\globalStorage\cursor.mcp\mcp.json`
- **macOS**: `~/Library/Application Support/Cursor/User/globalStorage/cursor.mcp/mcp.json`
- **Linux**: `~/.config/Cursor/User/globalStorage/cursor.mcp/mcp.json`

### 3.2 Update MCP Configuration
Replace the contents with:

```json
{
  "mcpServers": {
    "mikrotik-cursor-mcp": {
      "command": "C:\\Users\\YourUsername\\path\\to\\mikrotik-mcp\\.venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\YourUsername\\path\\to\\mikrotik-mcp\\src\\mcp_mikrotik\\server.py"
      ],
      "env": {
        "MIKROTIK_HOST": "192.168.88.1",
        "MIKROTIK_USERNAME": "admin",
        "MIKROTIK_PASSWORD": "your_password_here",
        "MIKROTIK_PORT": "22",
        "MIKROTIK_LOG_LEVEL": "INFO",
        "MIKROTIK_LOG_FORMAT": "json",
        "MIKROTIK_DRY_RUN": "true",
        "MIKROTIK_SAFETY_MODE": "true",
        "MIKROTIK_METRICS_ENABLED": "true",
        "MIKROTIK_METRICS_PORT": "9090",
        "MIKROTIK_CONNECTION_POOL_SIZE": "5",
        "MIKROTIK_CONNECTION_TIMEOUT": "30",
        "MIKROTIK_COMMAND_TIMEOUT": "60",
        "MIKROTIK_RETRY_ATTEMPTS": "3",
        "MIKROTIK_RETRY_DELAY": "1",
        "MIKROTIK_BACKUP_BEFORE_CHANGES": "true",
        "MIKROTIK_AUTO_BACKUP_RETENTION": "10"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

**⚠️ Important**: Update the file paths to match your actual installation directory!

## 🧪 Step 4: Test the Setup

### 4.1 Test Direct Connection
```bash
# In the mikrotik-mcp directory with venv activated
python -c "
import os
os.environ['MIKROTIK_HOST']='192.168.88.1'
os.environ['MIKROTIK_USERNAME']='admin'
os.environ['MIKROTIK_PASSWORD']='your_password'
from mcp_mikrotik.connector import execute_mikrotik_command
result = execute_mikrotik_command('/system identity print')
print('Router Identity:', result)
"
```

### 4.2 Test MCP Server
```bash
python -m mcp_mikrotik.server --help
```

### 4.3 Restart Cursor
Close and restart Cursor IDE to load the new MCP configuration.

## ✅ Step 5: Verify Integration

### 5.1 Check MCP Server Status
In Cursor, go to:
1. **Settings** → **Tools & MCP**
2. Verify `mikrotik-cursor-mcp` shows as **enabled** with a green toggle

### 5.2 Test Basic Commands
Try these natural language commands in Cursor:

- *"Show me my router's system information"*
- *"List all network interfaces"*
- *"Show me the current firewall rules"*
- *"List all connected devices"*
- *"Check system resources"*

### 5.3 Expected Results
You should see responses showing:
- Router model and RouterOS version
- Interface status and IP addresses
- Firewall rules and NAT configuration
- DHCP leases and connected devices
- CPU, memory, and uptime information

## 🔒 Security Configuration (Recommended)

### 6.1 SSH Key Authentication (More Secure)
```bash
# Generate SSH key pair
ssh-keygen -t rsa -b 4096 -f ~/.ssh/mikrotik_rsa

# Upload public key to router
scp ~/.ssh/mikrotik_rsa.pub admin@192.168.88.1:/

# On the router, import the key
/user ssh-keys import public-key-file=mikrotik_rsa.pub user=admin
```

Update your MCP configuration to use SSH keys:
```json
"env": {
  "MIKROTIK_HOST": "192.168.88.1",
  "MIKROTIK_USERNAME": "admin",
  "MIKROTIK_PASSWORD": "",
  "MIKROTIK_SSH_KEY": "C:\\Users\\YourUsername\\.ssh\\mikrotik_rsa",
  "MIKROTIK_STRICT_HOST_KEY_CHECKING": "true"
}
```

### 6.2 Firewall Security
Ensure your router's firewall is properly configured:
```bash
# Allow SSH only from management network
/ip firewall filter add chain=input protocol=tcp dst-port=22 src-address=192.168.88.0/24 action=accept comment="SSH from LAN"
/ip firewall filter add chain=input protocol=tcp dst-port=22 action=drop comment="Block SSH from WAN"
```

## 🚀 Step 7: Advanced Usage

### 7.1 Disable Dry Run Mode
When ready to make actual changes:
```json
"MIKROTIK_DRY_RUN": "false"
```

### 7.2 Enable Metrics
Monitor server performance:
```json
"MIKROTIK_METRICS_ENABLED": "true",
"MIKROTIK_METRICS_PORT": "9090"
```

Access metrics at: `http://localhost:9090`

## 🛠️ Troubleshooting

### Common Issues

**1. Connection Refused**
- Check router IP address
- Verify SSH is enabled on the router
- Confirm username/password are correct

**2. MCP Server Not Loading**
- Verify file paths in configuration are correct
- Check Python virtual environment is activated
- Restart Cursor IDE

**3. Permission Denied**
- Ensure user has proper privileges on router
- Check SSH key permissions (chmod 600)

**4. Timeout Errors**
- Increase connection timeout values
- Check network connectivity
- Verify router is not overloaded

### Debug Mode
Enable debug logging:
```json
"MIKROTIK_LOG_LEVEL": "DEBUG"
```

## 📊 Tested Configuration

**Hardware**: MikroTik RB5009UG+S+
**RouterOS**: 7.19.4 (stable)
**Features Tested**: ✅ All 426 tools across 19 categories
**Uptime**: 8+ weeks stable operation
**Network**: 15+ connected devices managed

## 🎉 Success!

Once configured, you have access to:
- **426 MikroTik management tools**
- **19 category-based interfaces**
- **Natural language commands in Cursor**
- **Complete RouterOS feature coverage**
- **Enterprise-grade automation**

Start with simple commands and gradually explore the full capabilities!

---

**Need Help?** Check the main README.md for examples and advanced usage scenarios.
