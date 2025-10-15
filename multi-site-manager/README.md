# MikroTik Multi-Site Manager

> **Centralized management for multiple MikroTik routers from a single CLI**

Manage unlimited MikroTik sites with automated backups, health monitoring, and bulk operations. Built on the MikroTik Cursor MCP foundation.

---

## Why Use This?

**Before:** SSH into each router individually → Run commands → Keep track manually  
**After:** One command manages all your routers simultaneously

**Perfect for:**
- 🏠 Multiple properties (home + vacation home + lab)
- 🏢 Multi-office businesses  
- 🔧 MSPs managing client networks
- 🎓 Network labs and testing environments

---

## Quick Start

### 1. Setup (2 minutes)

```bash
cd multi-site-manager
pip install -r requirements.txt
cp sites.yaml.example sites.yaml
```

Edit `sites.yaml` with your routers:
```yaml
sites:
  home-main:
    name: "Home Router"
    host: "192.168.88.1"
    username: "admin"
    password: "your-password"
```

### 2. First Commands (30 seconds)

```bash
# Check all sites
python site_manager.py status

# Health check
python site_manager.py health --all

# Create backups
python site_manager.py backup create --all
```

**📖 Full setup guide:** See [QUICK_START.md](QUICK_START.md)

---

## Core Features

### 🏥 Health Monitoring
Monitor CPU, memory, interfaces, DHCP leases across all sites
```bash
python site_manager.py health --all
python site_manager.py health --all --format html --output report.html
```

### 💾 Automated Backups
Schedule and manage backups with retention policies
```bash
python site_manager.py backup create --all
python site_manager.py backup list
python site_manager.py backup restore home-main --date 2025-10-15
```

### ⚡ Bulk Operations
Execute commands across multiple sites simultaneously
```bash
python site_manager.py bulk execute "/system identity print" --sites all
python site_manager.py bulk execute "command" --group production
```

### 🏷️ Site Organization
Organize by tags, groups, and priorities
```yaml
sites:
  home-main:
    tags: ["production", "home"]
    priority: "high"

groups:
  production: [home-main, office-main]
```

---

## Command Reference

### Status & Health
```bash
status                              # Connection status
status --site <site-id>            # Specific site
health --all                        # Health check all
health --site <site-id>            # Health check one
health --all --format html         # HTML report
```

### Backups
```bash
backup create --all                 # Backup all sites
backup create --site <site-id>     # Backup one site
backup list                         # List all backups
backup list --site <site-id>       # List for site
backup restore <site-id> --date <date>
```

### Bulk Operations
```bash
bulk execute "<command>" --sites all
bulk execute "<command>" --sites site1,site2
bulk execute "<command>" --group <group-name>
```

### Site Management
```bash
site add <site-id>                  # Add new site
site remove <site-id>               # Remove site
site info <site-id>                 # View site details
```

---

## Project Structure

```
multi-site-manager/
├── site_manager.py              # Main CLI tool
├── sites.yaml                   # Your site configuration
├── lib/
│   ├── site_connector.py        # Connection management
│   ├── health_monitor.py        # Health checks
│   ├── backup_manager.py        # Backup system
│   └── bulk_operations.py       # Bulk operations
├── examples/
│   ├── daily_operations.sh      # Automation script
│   └── deploy_firewall_rule.py  # Deployment example
├── backups/                     # Backup storage (auto-created)
└── logs/                        # Operation logs (auto-created)
```

---

## Configuration

### Basic Site Configuration

```yaml
sites:
  site-id:
    name: "Site Name"
    host: "192.168.88.1"              # IP or hostname
    username: "admin"
    password: "password"               # Or use ssh_key
    ssh_port: 22
    location: "Physical location"
    priority: "high"                   # high/medium/low
    tags: ["production", "office"]
    
    monitoring:
      enabled: true
      interval: 300                    # seconds
    
    backup:
      enabled: true
      schedule: "daily"                # daily/weekly/monthly
      retention_days: 30
```

### Site Groups

```yaml
groups:
  production:
    - home-main
    - office-main
  
  testing:
    - lab-network
```

---

## Common Use Cases

### Daily Health Check & Backup
```bash
#!/bin/bash
# Add to cron: 0 2 * * *
cd /path/to/multi-site-manager
python site_manager.py backup create --all
python site_manager.py health --all --format html --output daily_report.html
```

### Deploy Firewall Rule to All Sites
```bash
python site_manager.py bulk execute \
  "/ip firewall filter add chain=input action=accept src-address=10.0.0.0/8" \
  --sites all
```

### Update DNS on Production Sites
```bash
python site_manager.py bulk execute \
  "/ip dns set servers=8.8.8.8,8.8.4.4" \
  --group production
```

### Compare Configurations
```bash
# Get firewall rules from all sites
python site_manager.py bulk execute "/ip firewall filter print" --sites all

# Review differences manually or pipe to diff tool
```

---

## Automation Examples

### Daily Operations (Cron)
```bash
# /etc/cron.d/mikrotik-multi-site
0 2 * * * /path/to/examples/daily_operations.sh
```

### Python Script Integration
```python
from lib.site_connector import SiteConnector
from lib.health_monitor import HealthMonitor

# Get health status
monitor = HealthMonitor()
health = monitor.check_all_sites()

# Alert if any site unhealthy
for site_id, data in health.items():
    if data.get('health_score', 100) < 80:
        send_alert(f"{site_id} health score: {data['health_score']}")
```

---

## Performance

- **Single site check:** < 2 seconds
- **10 sites parallel:** < 5 seconds
- **Scalability:** Designed for 100+ sites

---

## Requirements

- **Python:** 3.8+
- **Network:** SSH access to routers (port 22)
- **Disk:** ~10MB + backup storage
- **Dependencies:** See requirements.txt

---

## Security Best Practices

1. **Use SSH keys** instead of passwords where possible
2. **Encrypt sites.yaml** if storing passwords
3. **Restrict file permissions:** `chmod 600 sites.yaml`
4. **Use non-standard SSH ports** for internet-facing routers
5. **Enable logging** for audit trail

---

## Troubleshooting

### Connection Failed
```bash
# Test specific site
python site_manager.py status --site <site-id>

# Verify router is reachable
ping <router-ip>
```

### Command Failed
```bash
# Check logs
cat logs/multi-site-manager.log

# Test command on single site first
python site_manager.py bulk execute "<command>" --sites test-site
```

### Backup Issues
```bash
# Force new backup
python site_manager.py backup create --site <site-id> --force

# Check backup directory
ls -la backups/<site-id>/
```

---

## Advanced Usage

### Custom Health Checks
Extend `lib/health_monitor.py` to add:
- VPN tunnel status
- Wireless client counts
- Bandwidth monitoring
- Custom metrics

### Cloud Backup Integration
Modify `lib/backup_manager.py` to:
- Upload to S3/Azure/GCS
- Encrypt backups
- Implement differential backups

### Monitoring Integration
Build integrations with:
- Prometheus & Grafana
- Nagios/Zabbix
- Slack/Teams alerts
- Email notifications

---

## Contributing

This is part of the [MikroTik Cursor MCP](https://github.com/kevinpez/mikrotik-cursor-mcp) project.

---

## License

MIT License - See main project [LICENSE](../LICENSE) file

---

## Support

- **Documentation:** [QUICK_START.md](QUICK_START.md)
- **Examples:** See `examples/` directory
- **Issues:** GitHub Issues
- **Parent Project:** [MikroTik Cursor MCP](https://github.com/kevinpez/mikrotik-cursor-mcp)

---

**Built on:** MikroTik Cursor MCP v4.8.1 (99% RouterOS coverage, 383 actions)
