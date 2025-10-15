# MikroTik Cursor MCP - Complete Setup Guide

This guide walks you through setting up the MikroTik Cursor MCP server from scratch, including troubleshooting common issues.

---

## 📋 **Prerequisites**

### Required Software
- **Python 3.8 or higher** ([Download](https://www.python.org/downloads/))
- **Cursor IDE** ([Download](https://cursor.sh/))
- **Git** (optional, for cloning)

### Required Hardware
- **MikroTik RouterOS device** (any model with SSH access)
- **Network connectivity** to the router

### Required Knowledge
- Basic command line usage
- Router IP address and admin credentials
- SSH enabled on your MikroTik router

---

## 🔧 **Step 1: Prepare Your MikroTik Router**

### Enable SSH Service

Connect to your MikroTik via Winbox or WebFig and enable SSH:

```routeros
/ip service
set ssh port=22 disabled=no
```

**Verify SSH is running:**
```routeros
/ip service print where name=ssh
```

You should see:
```
name="ssh" port=22 disabled=no
```

### Create Admin User (Optional but Recommended)

For security, create a dedicated user instead of using `admin`:

```routeros
/user add name=mcp-user group=full password=your-secure-password
```

### Test SSH Access

From your computer:

**Windows (PowerShell):**
```powershell
ssh admin@192.168.88.1
```

**Linux/Mac:**
```bash
ssh admin@192.168.88.1
```

If this works, you're ready to proceed!

---

## 💻 **Step 2: Install Python (if needed)**

### Check if Python is Installed

```bash
python --version
# or
python3 --version
```

If you see `Python 3.8.x` or higher, you're good!

### Install Python (if needed)

**Windows:**
1. Download from [python.org](https://www.python.org/downloads/)
2. Run installer
3. ✅ **Check "Add Python to PATH"**
4. Click "Install Now"

**Linux (Debian/Ubuntu):**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

**macOS:**
```bash
brew install python3
```

---

## 📦 **Step 3: Install MikroTik Cursor MCP**

### Option A: Git Clone (Recommended)

```bash
# Clone the repository
git clone https://github.com/kevinpez/mikrotik-cursor-mcp.git

# Navigate to directory
cd mikrotik-cursor-mcp
```

### Option B: Download ZIP

1. Go to https://github.com/kevinpez/mikrotik-cursor-mcp
2. Click "Code" → "Download ZIP"
3. Extract to a folder (e.g., `C:\mikrotik-cursor-mcp`)
4. Open terminal in that folder

### Create Virtual Environment

**Windows (PowerShell):**
```powershell
# Create virtual environment
python -m venv .venv

# Activate it
.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

You should see `(.venv)` in your terminal prompt.

### Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Install the package
pip install -e .
```

**Expected output:**
```
Successfully installed mcp-mikrotik-cursor-mcp
```

---

## ⚙️ **Step 4: Configure Cursor IDE**

### Locate Cursor Configuration

**Windows:**
```
%USERPROFILE%\.cursor\mcp.json
```
Full path: `C:\Users\YourName\.cursor\mcp.json`

**Linux:**
```
~/.cursor/mcp.json
```

**macOS:**
```
~/.cursor/mcp.json
```

### Create/Edit mcp.json

If the file doesn't exist, create it. Add this configuration:

```json
{
  "mcpServers": {
    "mikrotik-cursor-mcp": {
      "command": "python",
      "args": [
        "-m",
        "mcp_mikrotik.server"
      ],
      "cwd": "C:\\path\\to\\mikrotik-cursor-mcp",
      "env": {
        "MIKROTIK_HOST": "192.168.88.1",
        "MIKROTIK_USERNAME": "admin",
        "MIKROTIK_PASSWORD": "your-password",
        "MIKROTIK_PORT": "22",
        "MIKROTIK_SSH_KEY": "C:\\Users\\John\\.ssh\\mikrotik_rsa",
        "MIKROTIK_STRICT_HOST_KEY_CHECKING": "false",
        "MIKROTIK_KNOWN_HOSTS": "C:\\Users\\John\\.ssh\\known_hosts",
        "MIKROTIK_CONNECT_TIMEOUT": "10",
        "MIKROTIK_CMD_TIMEOUT": "30"
      }
    }
  }
}
```

### Important Configuration Notes

1. **Update `cwd` path:** Change to your actual installation directory
   - Windows: Use double backslashes `\\` or forward slashes `/`
   - Example: `"C:\\Users\\John\\mikrotik-cursor-mcp"`
   - Or: `"C:/Users/John/mikrotik-cursor-mcp"`

2. **Update credentials and security options:** Replace with your router's details
   - `MIKROTIK_HOST`: Your router's IP address
   - `MIKROTIK_USERNAME`: Router admin username
   - `MIKROTIK_PASSWORD`: Router admin password
   - `MIKROTIK_PORT`: SSH port (usually 22)
   - `MIKROTIK_SSH_KEY`: Optional path to private key (use instead of password)
   - `MIKROTIK_STRICT_HOST_KEY_CHECKING`: `true` to reject unknown hosts (recommended for prod)
   - `MIKROTIK_KNOWN_HOSTS`: Path to known_hosts for strict checking
   - `MIKROTIK_CONNECT_TIMEOUT`: SSH connect timeout seconds
   - `MIKROTIK_CMD_TIMEOUT`: Per-command timeout seconds

3. **Use absolute paths:** Don't use `~` or relative paths

### Example Configurations

**Windows Example:**
```json
{
  "mcpServers": {
    "mikrotik-cursor-mcp": {
      "command": "C:\\Users\\John\\mikrotik-cursor-mcp\\.venv\\Scripts\\python.exe",
      "args": [
        "-m",
        "mcp_mikrotik.server"
      ],
      "cwd": "C:\\Users\\John\\mikrotik-cursor-mcp",
      "env": {
        "MIKROTIK_HOST": "192.168.1.1",
        "MIKROTIK_USERNAME": "admin",
        "MIKROTIK_PASSWORD": "mySecurePass123",
        "MIKROTIK_PORT": "22"
      }
    }
  }
}
```

**Linux Example:**
```json
{
  "mcpServers": {
    "mikrotik-cursor-mcp": {
      "command": "/home/john/mikrotik-cursor-mcp/.venv/bin/python",
      "args": [
        "-m",
        "mcp_mikrotik.server"
      ],
      "cwd": "/home/john/mikrotik-cursor-mcp",
      "env": {
        "MIKROTIK_HOST": "10.0.0.1",
        "MIKROTIK_USERNAME": "mcp-user",
        "MIKROTIK_PASSWORD": "SuperSecret456",
        "MIKROTIK_PORT": "22"
      }
    }
  }
}
```

---

## ✅ **Step 5: Test the Installation**

### Restart Cursor

**This is critical!** Cursor only loads MCP servers on startup.

1. Completely close Cursor (not just the window)
2. Reopen Cursor
3. Wait 10-15 seconds for MCP to initialize

### Test Basic Commands

Open a new Cursor chat and try these commands:

**Test 1: System Information**
```
Show me the system resources on my MikroTik router
```

**Expected response:**
```
SYSTEM RESOURCES:
uptime: 5d3h15m
version: 7.19.4 (stable)
free-memory: 850MiB
...
```

**Test 2: List Interfaces**
```
List all network interfaces
```

**Expected response:**
```
INTERFACES:
 # NAME       TYPE    STATUS
 0 ether1     ether   RUNNING
 1 ether2     ether   RUNNING
...
```

**Test 3: Create Backup**
```
Create a backup called test-backup
```

**Expected response:**
```
Backup created successfully: test-backup.backup
```

If these work, **congratulations!** Your setup is complete! 🎉

---

## 🔍 **Troubleshooting Common Issues**

### Issue: "MCP not loading" or "Tool not found"

**Symptoms:**
- Cursor doesn't recognize MikroTik commands
- No response to MikroTik queries

**Solutions:**

1. **Verify mcp.json location:**
   ```powershell
   # Windows PowerShell
   Test-Path $env:USERPROFILE\.cursor\mcp.json
   ```
   Should return `True`

2. **Check JSON syntax:**
   - Use [jsonlint.com](https://jsonlint.com/) to validate
   - Common errors: missing commas, extra commas, wrong quotes

3. **Verify Python path:**
   ```bash
   where python    # Windows
   which python3   # Linux/Mac
   ```

4. **Test MCP server manually:**
   ```bash
   cd C:\path\to\mikrotik-cursor-mcp
   .venv\Scripts\activate
   python -m mcp_mikrotik.server
   ```
   
   Should NOT show errors. Press Ctrl+C to stop.

5. **Restart Cursor completely:**
   - Close all windows
   - End Cursor process in Task Manager (Windows)
   - Or: `killall Cursor` (Linux/Mac)
   - Reopen Cursor

### Issue: "SSH connection failed"

**Symptoms:**
- Error: "Failed to connect to router"
- Error: "Authentication failed"

**Solutions:**

1. **Test SSH manually:**
   ```bash
   ssh admin@192.168.88.1
   ```
   - Should connect without errors
   - If this fails, MCP will also fail

2. **Check firewall:**
   ```routeros
   /ip firewall filter print where dst-port=22
   ```
   - Ensure no rules blocking SSH

3. **Verify credentials:**
   ```routeros
   /user print where name=admin
   ```
   - Check user exists and is enabled

4. **Check SSH service:**
   ```routeros
   /ip service print where name=ssh
   ```
   - Should show `disabled=no`

5. **Try different port:**
   - If using non-standard SSH port
   - Update `MIKROTIK_PORT` in mcp.json

### Issue: "Commands work but are slow"

**Symptoms:**
- Commands take 10+ seconds
- Timeouts on complex operations

**Solutions:**

1. **Check network latency:**
   ```bash
   ping 192.168.88.1
   ```
   - Should be < 50ms for local network

2. **Reduce router load:**
   ```routeros
   /system resource print
   ```
   - Check CPU usage < 80%

3. **Increase SSH timeout:**
   Add to mcp.json env:
   ```json
   "MIKROTIK_TIMEOUT": "30"
   ```

4. **Check router performance:**
   - Update to latest RouterOS
   - Reboot router if needed
   - Check disk space

### Issue: "Permission denied" errors

**Symptoms:**
- Commands fail with "insufficient permissions"
- Some features don't work

**Solutions:**

1. **Check user group:**
   ```routeros
   /user print where name=admin
   ```
   - Should show `group=full`

2. **Check specific permissions:**
   ```routeros
   /user group print where name=full
   ```
   - Should have `policy=...` with all policies

3. **Create admin user:**
   ```routeros
   /user add name=mcp-admin group=full password=securepass
   ```
   - Update mcp.json with new username

### Issue: "Some features not working"

**Symptoms:**
- "Command not found" errors
- "Bad command name" errors

**Solutions:**

1. **Check RouterOS version:**
   ```routeros
   /system resource print
   ```
   - Some features require v7.x
   - Containers require v7.x+
   - CAPsMAN might need package

2. **Check installed packages:**
   ```routeros
   /system package print
   ```
   - Install missing packages if needed

3. **Feature compatibility:**
   - Wireless: Requires wireless-capable device
   - CAPsMAN: Requires caps-man package
   - Containers: RouterOS v7.4+

---

## 🔒 **Security Best Practices**

### Use SSH Keys (Recommended)

Instead of passwords, use SSH keys:

**Generate SSH key:**
```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/mikrotik_rsa
```

**Add to MikroTik:**
```routeros
/user ssh-keys import public-key-file=mikrotik_rsa.pub user=admin
```

**Update mcp.json:**
```json
"env": {
  "MIKROTIK_HOST": "192.168.88.1",
  "MIKROTIK_USERNAME": "admin",
  "MIKROTIK_SSH_KEY": "/home/user/.ssh/mikrotik_rsa",
  "MIKROTIK_PORT": "22"
}
```

### Restrict SSH Access

```routeros
# Allow SSH only from management subnet
/ip firewall filter add chain=input protocol=tcp dst-port=22 src-address=192.168.1.0/24 action=accept
/ip firewall filter add chain=input protocol=tcp dst-port=22 action=drop
```

### Use Non-Standard Port

```routeros
/ip service set ssh port=2222
```

Update mcp.json:
```json
"MIKROTIK_PORT": "2222"
```

### Create Limited User

For read-only operations:

```routeros
/user group add name=mcp-readonly policy=read,test,api
/user add name=mcp-readonly group=mcp-readonly password=readpass
```

---

## 📊 **Verifying Setup**

### Complete Verification Checklist

Run these commands to verify everything works:

```
✓ "Show system resources"
✓ "List all interfaces"
✓ "Show firewall filter rules"
✓ "List all backups"
✓ "What's my router's uptime?"
✓ "Show me the ARP table"
✓ "List all DHCP leases"
✓ "Show current routes"
✓ "Display connection tracking"
✓ "List all users"
```

If all these work, your setup is **100% functional!**

---

## 🚀 **Next Steps**

1. **Read the README** - Learn about all 382 actions
2. **Check CAPABILITIES.md** - See detailed feature matrix
3. **Try examples** - Test different commands
4. **Create backups** - Before making changes
5. **Explore categories** - Try firewall, VPN, IPv6 features

---

## 📞 **Getting Help**

If you're still having issues:

1. **Check logs:**
   ```bash
   cat ~/.cursor/mcp-server.log    # Linux/Mac
   type %USERPROFILE%\.cursor\mcp-server.log    # Windows
   ```

2. **GitHub Issues:**
   - https://github.com/kevinpez/mikrotik-cursor-mcp/issues
   - Include: RouterOS version, Python version, error messages

3. **Discussions:**
   - https://github.com/kevinpez/mikrotik-cursor-mcp/discussions
   - Share your setup, ask questions

---

**Happy Automating! 🎉**

