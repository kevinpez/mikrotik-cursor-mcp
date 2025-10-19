# User Guides

Comprehensive guides for using MikroTik Cursor MCP features.

---

## IP Services Management

### Overview

The MikroTik Cursor MCP includes comprehensive IP Services management capabilities. This is the **proper MikroTik way** to control service access instead of using complex firewall rules.

### Available Tools

**Core IP Services Tools:**

1. **`mikrotik_list_ip_services`** - List all IP services and their configuration
2. **`mikrotik_get_ip_service`** - Get configuration for a specific service
3. **`mikrotik_set_service_address`** - Set "Available From" address for a service
4. **`mikrotik_enable_ip_service`** - Enable an IP service
5. **`mikrotik_disable_ip_service`** - Disable an IP service
6. **`mikrotik_set_service_port`** - Change the port for a service
7. **`mikrotik_configure_secure_services`** - One-click secure configuration
8. **`mikrotik_restore_default_services`** - Restore to default settings
9. **`mikrotik_get_service_status`** - Get security status summary
10. **`mikrotik_create_service_backup`** - Backup current configuration

### Security Best Practices

**Recommended Configuration:**

```bash
# Secure services - restrict to local network only
/ip service set ssh address=192.168.88.0/24
/ip service set winbox address=192.168.88.0/24
/ip service set api address=192.168.88.0/24

# Disable insecure services entirely
/ip service set telnet disabled=yes
/ip service set ftp disabled=yes
```

**Using the MCP Tools:**

```python
# One-click secure configuration
mikrotik_configure_secure_services(local_network="192.168.88.0/24")

# Or configure individual services
mikrotik_set_service_address(service_name="ssh", address="192.168.88.0/24")
mikrotik_disable_ip_service(service_name="telnet")
```

### Service Reference

| Service | Default Port | Purpose | Security Recommendation |
|---------|-------------|---------|------------------------|
| **SSH** | 22 | Secure shell access | Restrict to management network |
| **WinBox** | 8291 | GUI management | Restrict to management network |
| **API** | 8728 | API access | Restrict to management network |
| **Telnet** | 23 | Unencrypted shell | **Disable** |
| **FTP** | 21 | File transfer | **Disable** |
| **WWW** | 80 | Web interface | **Disable** or restrict |
| **API-SSL** | 8729 | Encrypted API | Use instead of API |

### Common Operations

**Check Current Configuration:**
```bash
"Show me all IP services and their current configuration"
```

**Secure All Services:**
```bash
"Configure secure IP services for my local network 192.168.88.0/24"
```

**Disable Insecure Services:**
```bash
"Disable telnet and FTP services"
```

**Restore Defaults:**
```bash
"Restore IP services to default configuration"
```

---

## Safe Mode Operations

### What is MikroTik Safe Mode?

MikroTik Safe Mode is a **built-in RouterOS feature** that provides automatic rollback capabilities for configuration changes. Unlike dry-run mode (which prevents changes entirely), Safe Mode allows you to make actual changes that are **temporary until explicitly committed**.

**Key Benefits:**
- **🔄 Automatic Rollback**: Changes are automatically reverted if connection is lost
- **⏰ Timeout Protection**: Changes revert after a configurable timeout period
- **💾 Change History**: Maintains history of up to 100 recent actions
- **🛡️ Safety Net**: Protects against accidental lockouts and misconfigurations

### Safe Mode Commands

**1. Enter Safe Mode**
```bash
"Enter Safe Mode with 15 minute timeout"
```
**Command**: `mikrotik_enter_safe_mode`
**Parameters**: 
- `timeout_minutes` (optional): 1-60 minutes (default: 10)

**2. Exit Safe Mode**
```bash
"Exit Safe Mode and make changes permanent"
```
**Command**: `mikrotik_exit_safe_mode`
**Effect**: Makes all temporary changes permanent

**3. Check Safe Mode Status**
```bash
"Check if Safe Mode is currently active"
```
**Command**: `mikrotik_get_safe_mode_status`
**Returns**: Current Safe Mode status and configuration

**4. Set Safe Mode Timeout**
```bash
"Set Safe Mode timeout to 30 minutes"
```
**Command**: `mikrotik_set_safe_mode_timeout`
**Parameters**: `timeout_minutes` (1-60)

**5. Force Exit Safe Mode**
```bash
"Force exit Safe Mode immediately"
```
**Command**: `mikrotik_force_exit_safe_mode`
**Effect**: Makes changes permanent immediately (use with caution)

**6. Get Safe Mode History**
```bash
"Show me the Safe Mode change history"
```
**Command**: `mikrotik_get_safe_mode_history`
**Returns**: List of recent Safe Mode operations

**7. Create Safe Mode Backup**
```bash
"Create a backup before entering Safe Mode"
```
**Command**: `mikrotik_create_safe_mode_backup`
**Best Practice**: Always backup before Safe Mode operations

### Safe Mode Process

**Recommended Safe Mode Process:**

1. **📋 Plan Your Changes**
   ```bash
   "Create a backup before making changes"
   ```

2. **🛡️ Enter Safe Mode**
   ```bash
   "Enter Safe Mode with 10 minute timeout"
   ```

3. **⚙️ Make Your Changes**
   ```bash
   "Add firewall rule to block 192.168.99.0/24"
   "Configure VLAN interface"
   "Update routing table"
   ```

4. **✅ Test Your Changes**
   ```bash
   "Check if the firewall rule is working"
   "Test connectivity to the new VLAN"
   "Verify routing is correct"
   ```

5. **💾 Commit or Rollback**
   ```bash
   # If changes work correctly:
   "Exit Safe Mode and make changes permanent"
   
   # If changes cause issues:
   # Just wait for timeout or disconnect - changes will auto-rollback
   ```

### Safe Mode Best Practices

**When to Use Safe Mode:**
- Making multiple related configuration changes
- Testing new network configurations
- Implementing complex firewall rules
- Making changes that could cause lockouts
- Updating routing configurations

**Safe Mode Timeout Guidelines:**
- **Simple changes**: 5-10 minutes
- **Complex configurations**: 15-30 minutes
- **Network testing**: 30-60 minutes
- **Never exceed 60 minutes** (RouterOS limit)

**Emergency Procedures:**
- **Connection lost**: Changes automatically rollback
- **Timeout reached**: Changes automatically rollback
- **Force exit**: Use only when you're certain changes are correct

### Safe Mode Examples

**Example 1: Firewall Configuration**
```bash
# 1. Create backup
"Create a backup called 'before-firewall-changes'"

# 2. Enter Safe Mode
"Enter Safe Mode with 15 minute timeout"

# 3. Make changes
"Add firewall rule to block 192.168.99.0/24"
"Add firewall rule to allow SSH from 10.0.0.0/8"

# 4. Test changes
"Show me the firewall rules"
"Test connectivity to 192.168.99.1"

# 5. Commit changes
"Exit Safe Mode and make changes permanent"
```

**Example 2: VLAN Configuration**
```bash
# 1. Enter Safe Mode
"Enter Safe Mode with 20 minute timeout"

# 2. Configure VLAN
"Create VLAN interface with ID 100 on bridge"
"Add IP address 192.168.100.1/24 to VLAN interface"
"Configure DHCP server for VLAN 100"

# 3. Test configuration
"Check VLAN interface status"
"Test DHCP server on VLAN 100"

# 4. Commit or rollback
"Exit Safe Mode and make changes permanent"
```

---

## Additional Resources

### Documentation
- [MikroTik IP Services Documentation](https://help.mikrotik.com/docs/display/ROS/IP+Services)
- [MikroTik Safe Mode Documentation](https://help.mikrotik.com/docs/display/ROS/Safe+Mode)

### Security Best Practices
- Always use Safe Mode for risky operations
- Create backups before making changes
- Test changes in non-production environments
- Use dedicated service accounts with minimal permissions
- Monitor logs for unauthorized access

### Troubleshooting

**Safe Mode Issues:**
- Safe Mode is a terminal-only feature and cannot be accessed via API/SSH
- Use direct console connection for Safe Mode operations
- Check RouterOS version compatibility

**IP Services Issues:**
- Verify service is enabled before configuring
- Check firewall rules don't conflict with service settings
- Ensure proper network access for service restrictions

---

*User guides for MikroTik Cursor MCP Server*
