# Example Scripts

Practical examples for automating multi-site operations.

---

## Available Examples

### 1. `daily_operations.sh`
**Purpose:** Automated daily health checks and backups  
**Schedule:** Run via cron at 2 AM daily

**Features:**
- Creates backups of all sites
- Generates HTML health report
- Cleans up old backups (30 days)
- Cleans up old reports (14 days)
- Optional email notifications

**Usage:**
```bash
# Make executable
chmod +x daily_operations.sh

# Edit configuration
nano daily_operations.sh

# Test run
./daily_operations.sh

# Add to cron
crontab -e
# Add: 0 2 * * * /path/to/daily_operations.sh
```

---

### 2. `deploy_firewall_rule.py`
**Purpose:** Deploy consistent firewall rules across sites  
**Use Case:** Standardize security policies

**Features:**
- Deploy single rules
- Deploy rule sets
- Target specific site groups
- Interactive menu

**Usage:**
```bash
# Run interactively
python deploy_firewall_rule.py

# Customize for your needs
# Edit the script to add your own rules
```

---

## Creating Custom Scripts

### Template Structure
```python
#!/usr/bin/env python3
import sys
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.site_connector import SiteConnector
from lib.health_monitor import HealthMonitor
from lib.backup_manager import BackupManager
from lib.bulk_operations import BulkOperations

def main():
    # Your automation here
    connector = SiteConnector()
    sites = connector.get_sites()
    
    # Do something with sites
    pass

if __name__ == '__main__':
    main()
```

### Example Use Cases

#### Alert on High CPU
```python
from lib.health_monitor import HealthMonitor

monitor = HealthMonitor()
health = monitor.check_all_sites()

for site_id, data in health.items():
    if data.get('cpu_load', 0) > 80:
        print(f"ALERT: {site_id} CPU at {data['cpu_load']}%")
        # Send email/SMS/Slack notification
```

#### Sync Users Across Sites
```python
from lib.bulk_operations import BulkOperations

bulk = BulkOperations()

# Create standard admin user on all sites
user_cmd = '/user add name=backup-admin group=full password=SecurePass123'
results = bulk.execute_all(user_cmd)

for site_id, result in results.items():
    if result['success']:
        print(f"✓ {site_id}: User created")
    else:
        print(f"✗ {site_id}: {result['error']}")
```

#### Weekly Firmware Check
```python
from lib.site_connector import SiteConnector

connector = SiteConnector()

for site_id in connector.get_sites():
    result = connector.execute_command(site_id, '/system package update check-for-updates')
    print(f"{site_id}: {result['output']}")
```

---

## Best Practices

1. **Test First:** Always test on a single site before bulk operations
2. **Use Groups:** Target groups instead of "all" for safer deployments
3. **Log Everything:** Keep audit trails of all operations
4. **Error Handling:** Check success status before proceeding
5. **Backup First:** Create backups before making changes

---

## Contributing Examples

Have a useful script? Consider sharing it:
1. Add it to this directory
2. Document what it does
3. Include usage examples
4. Submit a pull request

---

## Need Help?

- **Main Documentation:** [../README.md](../README.md)
- **Quick Start:** [../QUICK_START.md](../QUICK_START.md)
- **Library Reference:** Check docstrings in `../lib/` modules

