# MikroTik IP Services Management Guide

## 🎯 **Overview**

The MikroTik Cursor MCP now includes comprehensive IP Services management capabilities. This is the **proper MikroTik way** to control service access instead of using complex firewall rules.

## 🔧 **Available Tools**

### **Core IP Services Tools:**

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

## 🛡️ **Security Best Practices**

### **Recommended Configuration:**

```bash
# Secure services - restrict to local network only
/ip service set ssh address=192.168.88.0/24
/ip service set winbox address=192.168.88.0/24
/ip service set api address=192.168.88.0/24

# Disable insecure services entirely
/ip service set telnet disabled=yes
/ip service set ftp disabled=yes
```

### **Using the MCP Tools:**

```python
# One-click secure configuration
mikrotik_configure_secure_services(local_network="192.168.88.0/24")

# Or configure individual services
mikrotik_set_service_address(service_name="ssh", address="192.168.88.0/24")
mikrotik_disable_ip_service(service_name="telnet")
```

## 📋 **Service Reference**

| Service | Default Port | Purpose | Security Recommendation |
|---------|-------------|---------|------------------------|
| **SSH** | 22 | Secure shell access | Restrict to local network |
| **Winbox** | 8291 | GUI management | Restrict to local network |
| **API** | 8728 | API access | Restrict to local network |
| **Telnet** | 23 | Unencrypted shell | **DISABLE** |
| **FTP** | 21 | File transfer | **DISABLE** |
| **WWW** | 80 | Web interface | Consider restricting |
| **HTTPS** | 443 | Secure web interface | Consider restricting |

## 🚀 **Quick Start Examples**

### **1. Check Current Status:**
```python
# Get overview of all services
mikrotik_get_service_status()
```

### **2. Secure Your Router:**
```python
# One command to secure everything
mikrotik_configure_secure_services()
```

### **3. Restore Defaults (if needed):**
```python
# Allow access from anywhere (less secure)
mikrotik_restore_default_services()
```

### **4. Custom Configuration:**
```python
# Allow SSH only from specific IP
mikrotik_set_service_address("ssh", "192.168.1.100/32")

# Change SSH port for security
mikrotik_set_service_port("ssh", 2222)

# Disable unused services
mikrotik_disable_ip_service("telnet")
mikrotik_disable_ip_service("ftp")
```

## 🔍 **Address Format Examples**

| Address | Meaning | Use Case |
|---------|---------|----------|
| `0.0.0.0/0` | Anywhere | Default (less secure) |
| `192.168.88.0/24` | Local network | Home/office network |
| `192.168.1.100/32` | Single IP | Specific device only |
| `10.0.0.0/8` | Private network | Corporate network |

## ⚡ **Why IP Services vs Firewall Rules?**

### **IP Services (Recommended):**
- ✅ **Built-in MikroTik feature** - designed for this purpose
- ✅ **Cleaner configuration** - single setting per service
- ✅ **More efficient** - handled at service level
- ✅ **Less resource usage** - no firewall processing
- ✅ **Easier to manage** - no rule conflicts

### **Firewall Rules (Complex):**
- ❌ **More complex** - multiple rules needed
- ❌ **Resource intensive** - every packet processed
- ❌ **Harder to manage** - rules can conflict
- ❌ **More prone to problems** - like connection timeouts

## 🧪 **Testing**

The IP services tools are included in the comprehensive test suite:

```bash
# Test all IP services functionality
python test_comprehensive.py --category ip_services

# Test with dry-run mode (safe)
python test_comprehensive.py --category ip_services --dry-run
```

## 📚 **Integration with Other Tools**

### **With Intelligent Workflow:**
```python
# Use intelligent workflow for safe changes
from src.mcp_mikrotik.safety.intelligent_workflow import get_workflow_manager
manager = get_workflow_manager()

# Safe service configuration
result = manager.execute_intelligent_workflow(
    '/ip service set ssh address=192.168.88.0/24',
    user_approved=True
)
```

### **With Multi-Site Manager:**
```python
# Configure services across multiple sites
from multi_site_manager.site_manager import SiteManager
manager = SiteManager()

# Apply secure configuration to all sites
manager.execute_bulk_command(
    '/ip service set ssh address=192.168.88.0/24',
    group='production'
)
```

## 🔧 **Troubleshooting**

### **Connection Issues:**
1. **Check service status:** `mikrotik_get_service_status()`
2. **Verify address settings:** `mikrotik_get_ip_service("ssh")`
3. **Test connectivity:** `mikrotik_diagnostics_ping("192.168.88.1")`

### **Common Problems:**
- **Locked out:** Use console access to restore defaults
- **Wrong network:** Check your local network range
- **Service disabled:** Use `mikrotik_enable_ip_service()`

## 📖 **Additional Resources**

- [MikroTik IP Services Documentation](https://help.mikrotik.com/docs/display/ROS/IP+Services)
- [Security Best Practices Guide](SECURITY_IMPLEMENTATION_REPORT.md)
- [Intelligent Workflow Guide](INTELLIGENT_WORKFLOW_GUIDE.md)
- [Multi-Site Manager Guide](multi-site-manager/README.md)

---

**🎉 The MikroTik Cursor MCP now provides the proper, efficient way to manage service access controls!**
