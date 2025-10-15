# Quick Start Guide - Multi-Site Manager

Get up and running in **5 minutes** ⚡

---

## Prerequisites

✅ Python 3.8 or higher  
✅ SSH access to your MikroTik routers  
✅ MikroTik Cursor MCP installed (parent project)

---

## Step 1: Install (2 minutes)

```bash
# Navigate to multi-site manager
cd mikrotik-mcp/multi-site-manager

# Install dependencies
pip install -r requirements.txt

# Copy configuration template
cp sites.yaml.example sites.yaml
```

---

## Step 2: Configure Your Sites (2 minutes)

Edit `sites.yaml` with your routers:

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
    tags: ["production"]
```

**Minimum required fields:**
- `name` - Human-readable name
- `host` - IP address or hostname
- `username` - SSH username
- `password` - SSH password (or use `ssh_key`)

---

## Step 3: Test Connection (30 seconds)

```bash
# Check if your router is reachable
python site_manager.py status
```

**Expected output:**
```
Site ID    Name            Host           Status  Last Check
────────────────────────────────────────────────────────────
home-main  My Home Router  192.168.88.1   ●       2025-10-15...
```

✅ Green dot (●) means connected!  
❌ Red X (✗) means connection failed

---

## Step 4: Your First Commands (1 minute)

### Health Check
```bash
python site_manager.py health --all
```

### Create Backup
```bash
python site_manager.py backup create --all
```

### List Backups
```bash
python site_manager.py backup list
```

### Execute Command on All Sites
```bash
python site_manager.py bulk execute "/system identity print" --sites all
```

---

## Common Commands

### Check Site Status
```bash
python site_manager.py status                    # All sites
python site_manager.py status --site home-main   # One site
```

### Health Monitoring
```bash
python site_manager.py health --all                        # All sites
python site_manager.py health --site home-main             # One site
python site_manager.py health --all --format html --output report.html
```

### Backup Operations
```bash
python site_manager.py backup create --all       # Backup all
python site_manager.py backup create --site home-main
python site_manager.py backup list
python site_manager.py backup restore home-main --date 2025-10-15
```

### Bulk Operations
```bash
python site_manager.py bulk execute "<command>" --sites all
python site_manager.py bulk execute "<command>" --sites site1,site2
```

---

## Adding More Sites

### Option 1: Edit sites.yaml manually
```yaml
sites:
  vacation-home:
    name: "Vacation Property"
    host: "vacation.example.com"
    username: "admin"
    password: "different-password"
    ssh_port: 22
    priority: "medium"
```

### Option 2: Use CLI (interactive)
```bash
python site_manager.py site add vacation-home
# Follow the prompts
```

---

## Organizing Sites

### By Groups
```yaml
groups:
  production:
    - home-main
    - office-main
  
  testing:
    - lab-network
```

Use with:
```bash
python site_manager.py bulk execute "command" --group production
```

### By Tags
```yaml
sites:
  home-main:
    tags: ["production", "wifi-6", "home"]
```

### By Priority
```yaml
sites:
  critical-router:
    priority: "high"    # high, medium, or low
```

---

## Automating with Cron

### Daily Backup + Health Check
```bash
# Edit crontab
crontab -e

# Add this line (runs at 2 AM daily)
0 2 * * * cd /path/to/multi-site-manager && python site_manager.py backup create --all && python site_manager.py health --all --format html --output /var/www/health.html
```

### Use the Example Script
```bash
# Make executable
chmod +x examples/daily_operations.sh

# Edit script with your paths
nano examples/daily_operations.sh

# Add to cron
0 2 * * * /path/to/examples/daily_operations.sh
```

---

## Troubleshooting

### ❌ Connection Failed

**Check router is reachable:**
```bash
ping 192.168.88.1
```

**Verify SSH is enabled:**
```
# On your router (via Winbox/WebFig):
System → Users → Active sessions (should show SSH)
```

**Test SSH manually:**
```bash
ssh admin@192.168.88.1
```

### ❌ Command Failed

**Test on single site first:**
```bash
python site_manager.py bulk execute "/system identity print" --sites home-main
```

**Check logs:**
```bash
cat logs/multi-site-manager.log
```

### ❌ Backup Failed

**Check backup directory exists:**
```bash
ls -la backups/
```

**Force new backup:**
```bash
python site_manager.py backup create --site home-main --force
```

---

## Next Steps

### ✅ Daily Operations
- Set up automated backups (cron)
- Configure health check alerts
- Review backup retention policies

### ✅ Security Hardening
```bash
# Use SSH keys instead of passwords
ssh_key: "/path/to/private_key"

# Set file permissions
chmod 600 sites.yaml

# Use non-standard SSH ports
ssh_port: 2222
```

### ✅ Advanced Usage
- Deploy firewall rules across sites
- Synchronize user accounts
- Build custom health checks
- Integrate with monitoring systems

---

## Getting Help

- **Full Documentation:** [README.md](README.md)
- **Example Scripts:** `examples/` directory
- **Command Help:** `python site_manager.py --help`
- **Sub-command Help:** `python site_manager.py backup --help`

---

## Quick Reference Card

| Task | Command |
|------|---------|
| Check status | `python site_manager.py status` |
| Health check | `python site_manager.py health --all` |
| Backup all | `python site_manager.py backup create --all` |
| List backups | `python site_manager.py backup list` |
| Execute command | `python site_manager.py bulk execute "cmd" --sites all` |
| Add site | `python site_manager.py site add <id>` |
| View site | `python site_manager.py site info <id>` |
| HTML report | `python site_manager.py health --all --format html` |

---

**🎉 You're all set! Start managing your MikroTik sites from a single interface.**

Need more details? Check the [full README](README.md) or explore the [examples](examples/) directory.
