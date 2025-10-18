# MikroTik Neighbor Scanner

## Quick Start

The neighbor scanner automatically discovers MikroTik devices on your network and adds them to your site configuration.

### Basic Usage

```bash
# Quick scan and populate
python scan_neighbors.py

# Or use the multi-site manager
python site_manager.py site scan --host 192.168.88.1 --username admin --password YourPassword --populate
```

### What It Does

1. **Scans** your network from a MikroTik router using neighbor discovery
2. **Identifies** MikroTik devices by platform, MAC address, and device information
3. **Populates** your `sites.yaml` file with discovered devices
4. **Enables** management of all devices through the multi-site manager

### Example Output

```
Scan Results from 192.168.88.1

Discovered MikroTik Devices:
  - 192.168.88.186 : 007-RB2011
  - 192.168.88.198 : 003-RB4011  
  - 192.168.88.228 : 002-RB4011
  - 192.168.88.230 : 005-RB850
  - 192.168.88.232 : SW-000-CRS-328

Population Results:
  Added sites: 5
  Skipped sites: 0
```

### After Discovery

Once devices are discovered, you can manage them all:

```bash
# Check status of all sites
python site_manager.py status

# Health check all devices
python site_manager.py health --all

# Backup all devices
python site_manager.py backup create --all

# Run commands on all devices
python site_manager.py bulk execute "/system identity print" --sites all
```

### Requirements

- Access to a MikroTik router on your network
- SSH credentials for the router
- MikroTik devices with neighbor discovery enabled (CDP/MNDP)

### Files

- `lib/neighbor_scanner.py` - Main scanner implementation
- `scan_neighbors.py` - Standalone scanning script
- `sites.yaml` - Updated with discovered devices

For detailed documentation, see `NEIGHBOR_SCANNER_GUIDE.md` in the project root.
