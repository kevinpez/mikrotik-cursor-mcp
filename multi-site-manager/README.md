# MikroTik Multi-Site Manager

**Centralized management for multiple MikroTik routers across different locations**

## Overview

The Multi-Site Manager extends the MikroTik MCP server to manage multiple routers from a single interface. Perfect for:
- Multiple office locations
- Home + vacation property
- Client networks (MSP use case)
- Lab + production environments

## Features

### ✅ **Centralized Management**
- Single configuration for all sites
- Bulk operations across sites
- Consistent security policies
- Synchronized configurations

### ✅ **Site Health Monitoring**
- Real-time status of all sites
- Resource utilization tracking
- Connection state monitoring
- Alert system for issues

### ✅ **Backup Management**
- Automated backup scheduling
- Centralized backup storage
- Version history tracking
- Quick restore capabilities

### ✅ **Bulk Operations**
- Deploy firewall rules to all sites
- Update configurations simultaneously
- Synchronized firmware updates
- Mass user management

### ✅ **Site Comparison**
- Configuration drift detection
- Compliance checking
- Performance comparison
- Security posture analysis

## Quick Start

### 1. Install Requirements

```bash
cd multi-site-manager
pip install -r requirements.txt
```

### 2. Configure Sites

Edit `sites.yaml`:

```yaml
sites:
  home-main:
    name: "Home Network - Main"
    host: "192.168.88.1"
    username: "admin"
    password: "your-password"
    ssh_port: 22
    location: "Home Office"
    priority: "high"
    
  vacation-home:
    name: "Vacation Property"
    host: "vacation.example.com"
    username: "admin"
    password: "your-password"
    ssh_port: 22
    location: "Lake House"
    priority: "medium"
```

### 3. Run Manager

```bash
# Check status of all sites
python site_manager.py status

# Backup all sites
python site_manager.py backup --all

# Deploy firewall rule to all sites
python site_manager.py firewall deploy --rule "block_suspicious" --sites all

# Get health report
python site_manager.py health --format html
```

## Architecture

```
multi-site-manager/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── sites.yaml               # Site configuration
├── config/
│   ├── global_policies.yaml # Global security policies
│   ├── firewall_templates/  # Reusable firewall configs
│   └── user_templates/      # Standard user configs
├── site_manager.py          # Main CLI tool
├── lib/
│   ├── site_connector.py    # Connect to sites
│   ├── bulk_operations.py   # Bulk ops engine
│   ├── health_monitor.py    # Health monitoring
│   ├── backup_manager.py    # Backup system
│   └── comparison.py        # Config comparison
├── backups/                 # Centralized backup storage
├── logs/                    # Operation logs
└── reports/                 # Health reports

```

## Usage Examples

### Health Check
```bash
# Check all sites
python site_manager.py health

# Check specific site
python site_manager.py health --site home-main

# Generate HTML report
python site_manager.py health --format html --output report.html
```

### Backup Management
```bash
# Backup all sites
python site_manager.py backup --all

# Backup specific site
python site_manager.py backup --site home-main

# List all backups
python site_manager.py backup list

# Restore from backup
python site_manager.py backup restore --site home-main --date 2025-10-15
```

### Bulk Operations
```bash
# Deploy firewall rule to all sites
python site_manager.py firewall deploy --rule block_malicious --all

# Update user on all sites
python site_manager.py user update --username admin --password newpass --all

# Add DHCP static lease to all sites
python site_manager.py dhcp add-static --ip 192.168.88.100 --mac aa:bb:cc:dd:ee:ff --all
```

### Configuration Comparison
```bash
# Compare configurations
python site_manager.py compare --sites home-main,vacation-home

# Check for drift from template
python site_manager.py compare --template standard-config.yaml

# Security posture comparison
python site_manager.py compare --type security
```

### Site Discovery
```bash
# Auto-discover MikroTik routers on network
python site_manager.py discover --network 192.168.1.0/24

# Add discovered site
python site_manager.py site add --from-discovery
```

## Configuration Files

### sites.yaml
Main configuration file for all sites:

```yaml
sites:
  site-id:
    name: "Human-readable name"
    host: "IP or hostname"
    username: "admin"
    password: "password"  # Or use ssh_key
    ssh_key: "/path/to/key"  # Optional
    ssh_port: 22
    location: "Physical location"
    priority: "high|medium|low"
    tags: ["production", "office"]
    monitoring:
      enabled: true
      interval: 300  # seconds
    backup:
      enabled: true
      schedule: "daily"  # daily, weekly, monthly
      retention: 30  # days
```

### global_policies.yaml
Policies applied to all sites:

```yaml
policies:
  firewall:
    - name: "Block RFC1918 from WAN"
      chain: "input"
      action: "drop"
      src-address-list: "rfc1918"
      in-interface: "ether1"
      
  users:
    - name: "admin"
      group: "full"
      password_policy: "strong"
      
  security:
    disable_services:
      - "telnet"
      - "ftp"
    enable_services:
      - "ssh"
      - "winbox-ssl"
```

## API Usage

You can also use the Python API directly:

```python
from lib.site_manager import SiteManager

# Initialize manager
manager = SiteManager('sites.yaml')

# Get all sites
sites = manager.get_all_sites()

# Execute command on all sites
results = manager.execute_all('system identity print')

# Deploy firewall rule
manager.deploy_firewall_rule(
    rule_name='block_suspicious',
    sites=['home-main', 'vacation-home']
)

# Get health status
health = manager.get_health_status('home-main')
print(f"CPU: {health['cpu']}%")
print(f"Memory: {health['memory_used']}/{health['memory_total']}")
```

## Best Practices

### Security
1. **Use SSH Keys** instead of passwords where possible
2. **Encrypt sites.yaml** if storing passwords
3. **Restrict SSH access** to management network only
4. **Enable logging** for all management operations
5. **Regular backups** before bulk operations

### Operations
1. **Test on single site first** before bulk deployment
2. **Use tags** to group similar sites
3. **Set priorities** for critical sites
4. **Schedule backups** during low-traffic hours
5. **Monitor health** continuously

### Organization
1. **Document site purposes** in site configuration
2. **Use consistent naming** across sites
3. **Tag environments** (prod, dev, test)
4. **Version control** your configuration files
5. **Keep backup retention policy** reasonable

## Troubleshooting

### Connection Issues
```bash
# Test connectivity to site
python site_manager.py test-connection --site home-main

# View last successful connection
python site_manager.py site info --site home-main
```

### Backup Issues
```bash
# Verify backup integrity
python site_manager.py backup verify --backup-id abc123

# Force backup creation
python site_manager.py backup --site home-main --force
```

### Operation Failures
```bash
# View operation logs
python site_manager.py logs --site home-main --last 10

# Rollback last operation
python site_manager.py rollback --site home-main
```

## Roadmap

- [ ] Web dashboard for multi-site management
- [ ] Mobile app for site monitoring
- [ ] Automated firmware update orchestration
- [ ] VPN mesh auto-configuration
- [ ] Advanced analytics and reporting
- [ ] Integration with monitoring systems (Prometheus, Grafana)
- [ ] Slack/Teams notifications
- [ ] Compliance reporting (PCI-DSS, HIPAA)

## Contributing

This is part of the MikroTik Cursor MCP project. See main README for contribution guidelines.

## License

MIT License - See main project LICENSE file

