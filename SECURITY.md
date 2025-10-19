# Security Guide

Comprehensive security guidelines for deploying and using the MikroTik Cursor MCP in production environments.

---

## Overview

The MikroTik Cursor MCP provides powerful automation capabilities that require careful security consideration. This guide covers:

- **Least-privilege access** - Minimal RouterOS permissions
- **Secure authentication** - SSH keys over passwords
- **Network isolation** - Management network restrictions
- **Audit logging** - Complete operation tracking
- **Credential protection** - Secure storage and handling

---

## RouterOS User Configuration

### Creating a Dedicated MCP User

Create a dedicated user account for the MCP server with minimal required permissions:

```bash
# Create MCP user with read-only access
/user add name=mcp-user password=SecurePassword123! group=read

# Or create with specific permissions
/user add name=mcp-user password=SecurePassword123! group=full
```

### User Groups and Permissions

**Recommended Groups:**
- `read` - For monitoring and status queries
- `read,sensitive` - For configuration viewing
- `full` - For configuration changes (use with caution)

**Custom Group Example:**
```bash
/user group add name=mcp-operations policy=local,telnet,ssh,ftp,reboot,read,write,policy,test,winbox,password,sniff,sensitive,api
```

---

## SSH Key Management

### Generate SSH Key Pair

```bash
# Generate RSA key pair
ssh-keygen -t rsa -b 4096 -f ~/.ssh/mikrotik_mcp_key

# Generate ED25519 key pair (recommended)
ssh-keygen -t ed25519 -f ~/.ssh/mikrotik_mcp_key
```

### Configure RouterOS for SSH Keys

```bash
# Add public key to router
/user ssh-keys import public-key-file=mcp_key.pub user=mcp-user

# Disable password authentication (optional)
/ip service set ssh disabled=no
/ip service set telnet disabled=yes
```

### MCP Configuration with SSH Keys

```json
{
  "mcpServers": {
    "mikrotik-cursor-mcp": {
      "command": "python",
      "args": ["src/mcp_mikrotik/server.py"],
      "env": {
        "MIKROTIK_HOST": "192.168.88.1",
        "MIKROTIK_USERNAME": "mcp-user",
        "MIKROTIK_SSH_KEY": "/path/to/mcp_key",
        "MIKROTIK_PORT": "22"
      }
    }
  }
}
```

---

## Network Security

### Management Network Isolation

```bash
# Create management VLAN
/interface vlan add interface=bridge name=mgmt-vlan vlan-id=100

# Add management IP
/ip address add address=192.168.100.1/24 interface=mgmt-vlan

# Restrict SSH to management network
/ip service set ssh address=192.168.100.0/24
```

### Firewall Rules for MCP Access

```bash
# Allow MCP server access
/ip firewall filter add chain=input src-address=192.168.100.10 action=accept comment="MCP Server Access"

# Block unauthorized SSH attempts
/ip firewall filter add chain=input protocol=tcp dst-port=22 action=drop comment="Block SSH"
```

### API Security

```bash
# Restrict API access
/ip service set api address=192.168.100.0/24

# Use TLS for API (RouterOS 7+)
/ip service set api-ssl address=192.168.100.0/24
```

---

## Credential Management

### Environment Variables

**Never hardcode credentials in configuration files:**

```json
{
  "env": {
    "MIKROTIK_HOST": "192.168.88.1",
    "MIKROTIK_USERNAME": "mcp-user",
    "MIKROTIK_PASSWORD": "${MIKROTIK_PASSWORD}",
    "MIKROTIK_PORT": "22"
  }
}
```

### Secret Management

**Use external secret management:**
- HashiCorp Vault
- AWS Secrets Manager
- Azure Key Vault
- Kubernetes Secrets

### Credential Rotation

```bash
# Regular password rotation
/user set mcp-user password=NewSecurePassword456!

# SSH key rotation
/user ssh-keys remove [find user=mcp-user]
/user ssh-keys import public-key-file=new_mcp_key.pub user=mcp-user
```

---

## Logging and Monitoring

### RouterOS Logging

```bash
# Enable comprehensive logging
/system logging add topics=info,debug action=memory

# Log to remote syslog
/system logging add topics=info,debug action=remote remote=192.168.100.5 remote-port=514

# Log to file
/system logging add topics=info,debug action=file file-name=mcp-operations
```

### MCP Server Logging

```bash
# Enable debug logging
export MIKROTIK_LOG_LEVEL=DEBUG

# Log to file
export MIKROTIK_LOG_FILE=/var/log/mikrotik-mcp.log
```

### Monitoring Commands

```bash
# Check active connections
/ip firewall connection print

# Monitor SSH connections
/log print where topics~"ssh"

# Check authentication attempts
/log print where topics~"auth"

# Monitor system resources
/system resource print
```

---

## Daily Security Operations

### Log Monitoring

```bash
# Check firewall drops
/log print where topics~"firewall"

# Check SSH connections
/log print where topics~"ssh"

# Check system errors
/log print where topics~"error"

# Check authentication attempts
/log print where topics~"auth"
```

### System Health Check

```bash
# System resources
/system resource print

# Interface status
/interface print

# Active connections
/ip firewall connection print

# User activity
/user active print
```

### Security Status Check

```bash
# Check enabled services
/ip service print

# Check firewall rules
/ip firewall filter print

# Check user accounts
/user print

# Check SSH keys
/user ssh-keys print
```

---

## Backup and Recovery

### Automated Backups

```bash
# Create backup script
/system script add name=backup-mcp source={
    /system backup save name=mcp-backup-$(/system clock get date)
    /file remove [find name~"mcp-backup" and creation-time<([/system clock get date]-7d)]
}

# Schedule daily backups
/system scheduler add name=backup-mcp-daily interval=1d on-event=backup-mcp
```

### Backup Verification

```bash
# List available backups
/file print where type=backup

# Test backup restoration (in test environment)
/system backup load name=mcp-backup-2025-10-19
```

---

## Incident Response

### Security Incident Checklist

1. **Immediate Response**
   - Disable affected user accounts
   - Block suspicious IP addresses
   - Enable additional logging
   - Create emergency backup

2. **Investigation**
   - Review logs for unauthorized access
   - Check for configuration changes
   - Verify backup integrity
   - Document findings

3. **Recovery**
   - Restore from clean backup if needed
   - Update passwords and SSH keys
   - Review and update firewall rules
   - Implement additional security measures

### Emergency Commands

```bash
# Disable all services except SSH
/ip service set telnet,ftp,www,api,winbox disabled=yes

# Block all external access
/ip firewall filter add chain=input action=drop comment="Emergency Block"

# Enable Safe Mode
/system safe-mode
```

---

## Best Practices

### General Security

- Use dedicated service accounts with minimal permissions
- Implement network segmentation for management traffic
- Enable comprehensive logging and monitoring
- Regular security audits and penetration testing
- Keep RouterOS firmware updated
- Use strong, unique passwords
- Implement multi-factor authentication where possible

### MCP-Specific Security

- Use SSH keys instead of passwords
- Restrict MCP server to specific IP addresses
- Monitor MCP operations through logs
- Test changes in non-production environments
- Use Safe Mode for risky operations
- Implement change approval workflows
- Regular backup and recovery testing

### Network Security

- Segment management networks
- Use VPNs for remote access
- Implement intrusion detection
- Regular firewall rule reviews
- Monitor for unusual traffic patterns
- Use encrypted protocols (SSH, TLS)

---

## Tools and Resources

### Security Tools
- WinBox: GUI management tool
- The Dude: Network monitoring
- Netinstall: RouterOS installation tool
- MCP Server: MikroTik automation system

### Documentation
- [RouterOS Security Guide](https://help.mikrotik.com/docs/display/ROS/Security)
- [SSH Key Management](https://help.mikrotik.com/docs/display/ROS/SSH)
- [Firewall Configuration](https://help.mikrotik.com/docs/display/ROS/IP+Firewall)

---

## Compliance and Auditing

### Audit Requirements

- Document all configuration changes
- Maintain access logs for compliance
- Regular security assessments
- Incident response procedures
- Backup and recovery testing

### Compliance Frameworks

- ISO 27001
- NIST Cybersecurity Framework
- SOC 2
- PCI DSS (if applicable)

---

*Security guide for MikroTik Cursor MCP Server*