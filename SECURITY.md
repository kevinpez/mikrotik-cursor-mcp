# Security Guide for MikroTik Cursor MCP

This document provides comprehensive security guidelines for deploying and using the MikroTik Cursor MCP in production environments.

## Table of Contents

- [Overview](#overview)
- [RouterOS User Configuration](#routeros-user-configuration)
- [SSH Key Management](#ssh-key-management)
- [Network Security](#network-security)
- [Credential Management](#credential-management)
- [Logging and Monitoring](#logging-and-monitoring)
- [Multi-Site Security](#multi-site-security)
- [Best Practices](#best-practices)
- [Incident Response](#incident-response)

## Overview

The MikroTik Cursor MCP provides powerful automation capabilities that require careful security consideration. This guide covers:

- **Least-privilege access** - Minimal RouterOS permissions
- **Secure authentication** - SSH keys over passwords
- **Network isolation** - Management network restrictions
- **Audit logging** - Complete operation tracking
- **Credential protection** - Secure storage and handling

## RouterOS User Configuration

### Creating a Dedicated MCP User

Create a dedicated user with minimal required permissions:

```bash
# Create MCP user group with specific permissions
/user group add name=mcp-users policy=local,telnet,ssh,ftp,reboot,read,write,policy,test,winbox,password,sniff,sensitive,api

# Create the MCP user
/user add name=mcp-user group=mcp-users password=your-secure-password
```

### Minimal Permission Policy

For maximum security, create a custom policy with only required permissions:

```bash
# Create minimal policy for MCP operations
/user group add name=mcp-minimal policy=local,ssh,read,write,api

# Required permissions breakdown:
# - local: Local terminal access
# - ssh: SSH access
# - read: Read configuration and status
# - write: Modify configuration
# - api: API access for advanced operations
```

### Permission Matrix

| Operation Category | Required Permissions | Risk Level |
|-------------------|---------------------|------------|
| **Read Operations** | `read` | Low |
| **System Info** | `read` | Low |
| **Backup/Restore** | `read`, `write` | Medium |
| **Firewall Rules** | `read`, `write` | High |
| **Routing Changes** | `read`, `write` | High |
| **User Management** | `read`, `write` | Critical |
| **System Reboot** | `read`, `write`, `reboot` | Critical |

### Recommended User Groups

#### Production Environment
```bash
# High-security production group
/user group add name=mcp-prod policy=local,ssh,read,write,api
```

#### Development/Testing
```bash
# More permissive for testing
/user group add name=mcp-dev policy=local,telnet,ssh,ftp,reboot,read,write,policy,test,winbox,password,sniff,sensitive,api
```

#### Read-Only Monitoring
```bash
# Read-only for monitoring systems
/user group add name=mcp-monitor policy=local,ssh,read,api
```

## SSH Key Management

### Generate SSH Keys

```bash
# Generate RSA key (recommended for RouterOS)
ssh-keygen -t rsa -b 4096 -f ~/.ssh/mikrotik_mcp_rsa -C "mcp-user@mikrotik"

# Generate Ed25519 key (more secure, if supported)
ssh-keygen -t ed25519 -f ~/.ssh/mikrotik_mcp_ed25519 -C "mcp-user@mikrotik"
```

### Deploy Public Key to RouterOS

```bash
# Method 1: Using RouterOS CLI
/user ssh-keys import public-key-file=mikrotik_mcp_rsa.pub user=mcp-user

# Method 2: Using WinBox
# 1. Go to System → Users
# 2. Select mcp-user
# 3. Click on "SSH Keys" tab
# 4. Import the public key file
```

### Configure SSH Client

```bash
# Add to ~/.ssh/config
Host mikrotik-*
    User mcp-user
    IdentityFile ~/.ssh/mikrotik_mcp_rsa
    StrictHostKeyChecking yes
    UserKnownHostsFile ~/.ssh/known_hosts
    ServerAliveInterval 30
    ServerAliveCountMax 3
```

### Key Rotation

```bash
# Rotate keys every 90 days
# 1. Generate new key pair
ssh-keygen -t rsa -b 4096 -f ~/.ssh/mikrotik_mcp_rsa_new

# 2. Deploy new public key
/user ssh-keys import public-key-file=mikrotik_mcp_rsa_new.pub user=mcp-user

# 3. Test new key
ssh -i ~/.ssh/mikrotik_mcp_rsa_new mcp-user@router-ip

# 4. Remove old key
/user ssh-keys remove [find user=mcp-user and key-owner="old-key-owner"]

# 5. Update MCP configuration
```

## Network Security

### Management Network Isolation

```bash
# Create dedicated management VLAN
/interface vlan add interface=ether1 name=mgmt-vlan vlan-id=100

# Assign management IP
/ip address add address=192.168.100.1/24 interface=mgmt-vlan

# Restrict SSH access to management network only
/ip firewall filter add chain=input protocol=tcp dst-port=22 src-address=192.168.100.0/24 action=accept
/ip firewall filter add chain=input protocol=tcp dst-port=22 action=drop
```

### Firewall Rules for MCP

```bash
# Allow MCP server access
/ip firewall filter add chain=input protocol=tcp dst-port=22 src-address=10.0.0.100 action=accept comment="MCP Server Access"

# Allow API access (if using API)
/ip firewall filter add chain=input protocol=tcp dst-port=8728 src-address=10.0.0.100 action=accept comment="MCP API Access"

# Log all SSH attempts
/ip firewall filter add chain=input protocol=tcp dst-port=22 action=log log-prefix="SSH-Attempt"
```

### VPN Access for Remote Management

```bash
# Create WireGuard interface for MCP access
/interface wireguard add name=wg-mcp listen-port=51820

# Add peer for MCP server
/interface wireguard peers add interface=wg-mcp public-key="MCP_SERVER_PUBLIC_KEY" allowed-address=10.0.0.100/32

# Allow WireGuard traffic
/ip firewall filter add chain=input protocol=udp dst-port=51820 action=accept comment="WireGuard MCP"
```

## Credential Management

### Environment Variables

```bash
# Production environment variables
export MIKROTIK_HOST="192.168.100.1"
export MIKROTIK_USERNAME="mcp-user"
export MIKROTIK_SSH_KEY="/secure/path/mikrotik_mcp_rsa"
export MIKROTIK_STRICT_HOST_KEY_CHECKING="true"
export MIKROTIK_KNOWN_HOSTS="/secure/path/known_hosts"
```

### Configuration File Security

```bash
# Secure configuration file permissions
chmod 600 ~/.cursor/mcp.json
chmod 600 ~/.ssh/mikrotik_mcp_rsa
chmod 644 ~/.ssh/mikrotik_mcp_rsa.pub
chmod 600 ~/.ssh/known_hosts
```

### Secret Management Systems

#### HashiCorp Vault Integration

```python
# Example Vault integration
import hvac

def get_mikrotik_credentials():
    client = hvac.Client(url='https://vault.company.com')
    client.token = os.getenv('VAULT_TOKEN')
    
    secret = client.secrets.kv.v2.read_secret_version(
        path='mikrotik/mcp-credentials'
    )
    
    return {
        'host': secret['data']['data']['host'],
        'username': secret['data']['data']['username'],
        'ssh_key': secret['data']['data']['ssh_key_path']
    }
```

#### AWS Secrets Manager

```python
# Example AWS Secrets Manager integration
import boto3
import json

def get_mikrotik_credentials():
    client = boto3.client('secretsmanager', region_name='us-east-1')
    
    response = client.get_secret_value(
        SecretId='mikrotik/mcp-credentials'
    )
    
    return json.loads(response['SecretString'])
```

## Logging and Monitoring

### RouterOS Logging Configuration

```bash
# Enable detailed logging
/system logging add topics=info,debug action=memory

# Log user activities
/system logging add topics=system action=memory

# Log firewall events
/system logging add topics=firewall action=memory

# Log SSH connections
/system logging add topics=ssh action=memory
```

### MCP Logging Configuration

```json
{
  "mcpServers": {
    "mikrotik-cursor-mcp": {
      "env": {
        "MIKROTIK_LOG_LEVEL": "INFO",
        "MIKROTIK_LOG_FORMAT": "json",
        "MIKROTIK_LOG_FILE": "/var/log/mikrotik-mcp.log",
        "MIKROTIK_AUDIT_LOG": "true"
      }
    }
  }
}
```

### Security Monitoring

```bash
# Monitor failed SSH attempts
/log print where topics~"ssh" and message~"failed"

# Monitor user changes
/log print where topics~"system" and message~"user"

# Monitor firewall changes
/log print where topics~"firewall" and message~"added\|removed"
```

## Multi-Site Security

### Site-Specific Credentials

```yaml
# sites.yaml with encrypted credentials
sites:
  production-router-1:
    name: "Production Router 1"
    host: "192.168.100.1"
    username: "mcp-prod-1"
    ssh_key_path: "/secure/keys/prod-1_rsa"
    tags: ["production", "critical"]
    
  staging-router-1:
    name: "Staging Router 1"
    host: "192.168.200.1"
    username: "mcp-staging-1"
    ssh_key_path: "/secure/keys/staging-1_rsa"
    tags: ["staging", "testing"]
```

### Credential Encryption

```bash
# Encrypt sites.yaml file
gpg --symmetric --cipher-algo AES256 sites.yaml

# Use encrypted file
python site_manager.py --config sites.yaml.gpg
```

### Network Segmentation

```bash
# Different management networks per environment
Production: 192.168.100.0/24
Staging:    192.168.200.0/24
Development: 192.168.300.0/24
```

## Best Practices

### 1. Principle of Least Privilege

- Create dedicated users with minimal required permissions
- Use separate credentials for different environments
- Regularly audit user permissions

### 2. Defense in Depth

- Network-level restrictions (firewall rules)
- Application-level authentication (SSH keys)
- Logging and monitoring at all levels

### 3. Regular Security Updates

```bash
# Update RouterOS regularly
/system package update install

# Update MCP dependencies
pip install --upgrade mikrotik-cursor-mcp

# Rotate SSH keys every 90 days
```

### 4. Backup and Recovery

```bash
# Regular configuration backups
/backup save name=security-backup-$(date +%Y%m%d)

# Test restore procedures
/backup load name=security-backup-20240101
```

### 5. Incident Response Preparation

```bash
# Create emergency access procedures
# 1. Out-of-band access (console)
# 2. Emergency user accounts
# 3. Rollback procedures
# 4. Contact information
```

## Incident Response

### Security Incident Checklist

1. **Immediate Response**
   - [ ] Isolate affected systems
   - [ ] Preserve logs and evidence
   - [ ] Notify security team
   - [ ] Document timeline

2. **Investigation**
   - [ ] Review access logs
   - [ ] Check for unauthorized changes
   - [ ] Analyze network traffic
   - [ ] Identify attack vector

3. **Recovery**
   - [ ] Restore from clean backup
   - [ ] Update credentials
   - [ ] Patch vulnerabilities
   - [ ] Strengthen security controls

4. **Post-Incident**
   - [ ] Conduct lessons learned
   - [ ] Update security procedures
   - [ ] Improve monitoring
   - [ ] Train staff

### Emergency Access Procedures

```bash
# Emergency console access
# 1. Physical access to router
# 2. Use console cable
# 3. Reset to factory defaults if necessary
# 4. Restore from secure backup

# Emergency network access
# 1. Use out-of-band management
# 2. VPN to management network
# 3. Emergency user account
```

## Compliance and Auditing

### Audit Trail Requirements

- All MCP operations logged with timestamps
- User identification for all actions
- Configuration changes tracked
- Access attempts monitored

### Compliance Frameworks

- **SOC 2**: Access controls, monitoring, incident response
- **ISO 27001**: Information security management
- **PCI DSS**: Network security for payment processing
- **HIPAA**: Healthcare data protection

### Regular Security Assessments

```bash
# Monthly security checklist
# 1. Review user accounts and permissions
# 2. Check SSH key validity
# 3. Review firewall rules
# 4. Analyze access logs
# 5. Test backup/restore procedures
# 6. Update security documentation
```

## Contact and Support

For security-related issues:

- **Security Issues**: security@company.com
- **Emergency Contact**: +1-XXX-XXX-XXXX
- **Documentation**: [Internal Security Wiki]
- **Incident Response**: [Internal IR Procedures]

---

**Remember**: Security is an ongoing process, not a one-time setup. Regular reviews, updates, and testing are essential for maintaining a secure environment.
