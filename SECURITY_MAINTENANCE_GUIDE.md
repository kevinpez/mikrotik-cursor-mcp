# MikroTik Security Maintenance Guide

## 🔧 Daily Operations

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

# Address lists
/ip firewall address-list print
```

## 📅 Weekly Tasks

### Backup Verification
```bash
# List backups
/file print where name~"backup"

# Create new backup
/system backup save name=weekly-backup-$(date +%Y%m%d)

# Verify backup integrity
/file print where name="weekly-backup-$(date +%Y%m%d)"
```

### Security Rule Review
```bash
# Review firewall rules
/ip firewall filter print

# Check address lists
/ip firewall address-list print

# Review user accounts
/user print
```

## 📊 Monthly Tasks

### Password Rotation
```bash
# Generate new passwords (use strong passwords)
# Update admin password
/user set admin password=NewPassword$(date +%m%Y)!

# Update backup admin
/user set backup-admin password=BackupPassword$(date +%m%Y)!

# Update network admin
/user set network-admin password=NetworkPassword$(date +%m%Y)!
```

### Security Audit
```bash
# Check for failed login attempts
/log print where topics~"auth" and message~"failed"

# Review blocked IPs
/ip firewall address-list print where list="ssh_blacklist"

# Check system uptime
/system resource print
```

## 🔍 Troubleshooting

### Connection Issues
```bash
# Test connectivity
/ping 8.8.8.8 count=5

# Check routing
/ip route print

# Check DNS
/ip dns print
```

### Firewall Issues
```bash
# Check rule order
/ip firewall filter print

# Test rule effectiveness
/ip firewall connection print

# Clear address lists if needed
/ip firewall address-list remove [find list="ssh_blacklist"]
```

### VLAN Issues
```bash
# Check VLAN status
/interface vlan print

# Check bridge configuration
/interface bridge print

# Check VLAN ports
/interface bridge port print
```

## 🚨 Emergency Procedures

### Locked Out of Router
1. **Physical Access:** Use console cable
2. **Reset Button:** Hold for 10 seconds
3. **Netinstall:** Reinstall RouterOS
4. **Backup Recovery:** Restore from backup

### Security Breach Response
1. **Immediate Actions:**
   ```bash
   # Block suspicious IPs
   /ip firewall address-list add list=emergency_block address=<suspicious_ip>
   
   # Disable affected services
   /ip service disable ssh
   /ip service disable www
   
   # Check logs
   /log print where time>$(date -d "1 hour ago" +%H:%M:%S)
   ```

2. **Investigation:**
   ```bash
   # Check active connections
   /ip firewall connection print
   
   # Review authentication logs
   /log print where topics~"auth"
   
   # Check for unauthorized changes
   /system backup save name=incident-backup-$(date +%Y%m%d-%H%M)
   ```

3. **Recovery:**
   ```bash
   # Restore from clean backup
   /system backup load name=security-backup
   
   # Re-enable services
   /ip service enable ssh
   /ip service enable www
   
   # Update passwords
   /user set admin password=EmergencyPassword2025!
   ```

## 📋 Configuration Backup Commands

### Full Configuration Backup
```bash
# Create timestamped backup
/system backup save name=config-backup-$(date +%Y%m%d-%H%M)

# Export configuration
/export file=config-export-$(date +%Y%m%d)

# Backup to external location
/tool fetch url="ftp://backup-server/backups/config-$(date +%Y%m%d).backup" upload=yes src-file=config-backup-$(date +%Y%m%d-%H%M)
```

### Selective Backups
```bash
# Firewall rules only
/ip firewall filter export file=firewall-rules-$(date +%Y%m%d)

# User accounts only
/user export file=users-$(date +%Y%m%d)

# VLAN configuration only
/interface vlan export file=vlans-$(date +%Y%m%d)
```

## 🔐 Security Best Practices

### Password Management
- Use strong passwords (16+ characters)
- Include mixed case, numbers, symbols
- Rotate passwords monthly
- Never reuse passwords
- Store passwords securely

### Access Control
- Limit admin access to necessary users
- Use SSH keys when possible
- Monitor all administrative access
- Log all configuration changes
- Regular access reviews

### Network Security
- Keep RouterOS updated
- Monitor firewall logs daily
- Review and update rules regularly
- Use VLANs for network segmentation
- Implement proper backup procedures

### Monitoring
- Set up log monitoring
- Configure SNMP for monitoring tools
- Use automated backup systems
- Monitor system resources
- Track security events

## 📞 Emergency Contacts

### Technical Support
- **MikroTik Support:** support@mikrotik.com
- **Documentation:** help.mikrotik.com
- **Community Forum:** forum.mikrotik.com

### Security Resources
- **CVE Database:** cve.mitre.org
- **Security Advisories:** mikrotik.com/security
- **Best Practices:** wiki.mikrotik.com

## 📚 Additional Resources

### Documentation
- RouterOS Manual: help.mikrotik.com
- Security Guide: wiki.mikrotik.com/wiki/Security
- Backup Guide: wiki.mikrotik.com/wiki/Backup

### Tools
- WinBox: GUI management tool
- The Dude: Network monitoring
- Netinstall: RouterOS installation tool
- MCP Server: Intelligent automation system

---
*Maintenance guide for MikroTik security implementation*
