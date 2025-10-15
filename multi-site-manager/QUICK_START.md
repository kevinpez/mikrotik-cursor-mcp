# Multi-Site Manager - Quick Start Guide

Get up and running with multi-site management in 5 minutes!

## Step 1: Install Dependencies (2 minutes)

```bash
cd multi-site-manager
pip install -r requirements.txt
```

## Step 2: Configure Your Sites (2 minutes)

```bash
# Copy example configuration
cp sites.yaml.example sites.yaml

# Edit with your actual sites
nano sites.yaml  # or use your favorite editor
```

**Minimum configuration:**
```yaml
sites:
  home-main:
    name: "My Home Router"
    host: "192.168.88.1"
    username: "admin"
    password: "your-password"
    ssh_port: 22
    location: "Home"
    priority: "high"
```

## Step 3: Test Connection (30 seconds)

```bash
# Check if sites are reachable
python site_manager.py status
```

You should see:
```
Site ID    Name            Host           Status  Last Check
─────────────────────────────────────────────────────────────
home-main  My Home Router  192.168.88.1   ●       2025-10-15...
```

## Step 4: Your First Commands (30 seconds)

```bash
# Get health status
python site_manager.py health --all

# Create backup
python site_manager.py backup create --all

# List DHCP leases from all sites
python site_manager.py bulk execute "/ip dhcp-server lease print" --sites all
```

## Common Use Cases

### Daily Backup

```bash
# Backup all sites
python site_manager.py backup create --all

# List backups
python site_manager.py backup list

# Restore if needed
python site_manager.py backup restore home-main --date 2025-10-15
```

### Health Monitoring

```bash
# Quick health check
python site_manager.py health --all

# Generate HTML report
python site_manager.py health --all --format html --output health_report.html

# Check specific site
python site_manager.py health --site home-main
```

### Bulk Operations

```bash
# Get system info from all sites
python site_manager.py bulk execute "/system identity print" --sites all

# Update DNS on all sites
python site_manager.py bulk execute "/ip dns set servers=8.8.8.8,8.8.4.4" --sites all

# Check all firewall rules
python site_manager.py bulk execute "/ip firewall filter print" --sites all
```

### Site Management

```bash
# Add new site
python site_manager.py site add vacation-home

# View site info
python site_manager.py site info home-main

# Remove site
python site_manager.py site remove old-site
```

## Pro Tips

### 1. Use Site Groups
Define groups in `sites.yaml`:
```yaml
groups:
  production:
    - home-main
    - office-main
  testing:
    - lab-network
```

Then operate on groups:
```bash
python site_manager.py bulk execute "command" --group production
```

### 2. Use Tags
Tag your sites for easy filtering:
```yaml
sites:
  home-main:
    tags:
      - "production"
      - "home"
      - "wifi-6"
```

### 3. Automate with Cron

Create a daily backup script:
```bash
#!/bin/bash
cd /path/to/multi-site-manager
python site_manager.py backup create --all
python site_manager.py health --all --format html --output /var/www/health.html
```

Add to crontab:
```
0 2 * * * /path/to/backup_script.sh
```

### 4. Generate Reports

```bash
# HTML health report
python site_manager.py health --all --format html --output report.html

# JSON for processing
python site_manager.py health --all --format json > health.json

# Status table
python site_manager.py status --format table
```

## Troubleshooting

### Connection Failed

```bash
# Test individual site
python site_manager.py status --site home-main

# Check if router is reachable
ping 192.168.88.1

# Verify SSH is enabled on router
```

### Command Failed

```bash
# Try running command directly
python site_manager.py bulk execute "/system identity print" --sites home-main

# Check logs
cat logs/multi-site-manager.log
```

### Backup Failed

```bash
# Force new backup
python site_manager.py backup create --site home-main --force

# Check backup directory
ls -la backups/home-main/
```

## Next Steps

1. **Automate Monitoring** - Set up scheduled health checks
2. **Configure Alerts** - Add email/SMS notifications
3. **Build Workflows** - Create custom automation scripts
4. **Explore Advanced Features** - Try configuration comparison, bulk deployments

## Need Help?

- Check the main README.md for detailed documentation
- View example configurations in sites.yaml.example
- Run `python site_manager.py --help` for command help

## Common Commands Reference

| Command | Description |
|---------|-------------|
| `status` | Show connection status |
| `health --all` | Health check all sites |
| `backup create --all` | Backup all sites |
| `backup list` | List all backups |
| `bulk execute "cmd" --sites all` | Run command on all sites |
| `site add <id>` | Add new site |
| `site info <id>` | View site details |

---

**You're all set!** Start managing your MikroTik sites from a single interface. 🚀

