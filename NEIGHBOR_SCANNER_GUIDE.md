# MikroTik Network Neighbor Scanner Guide

## Overview

The MikroTik Network Neighbor Scanner is a powerful tool that automatically discovers MikroTik devices on your network using neighbor discovery protocols and populates your multi-site configuration. This eliminates the need to manually add each MikroTik device to your site management system.

## Features

- 🔍 **Automatic Discovery** - Finds MikroTik devices using RouterOS neighbor discovery
- 🎯 **Smart Identification** - Identifies MikroTik devices by platform, MAC address, and other indicators
- 📝 **Auto-Population** - Automatically adds discovered devices to site configuration
- 🎨 **Rich Output** - Beautiful formatted tables and progress indicators
- 🔧 **Integration** - Works seamlessly with the multi-site manager
- 📊 **Detailed Logging** - Comprehensive logging for troubleshooting

## How It Works

The scanner uses multiple RouterOS commands to discover devices:

1. **`/ip neighbor print detail`** - Primary neighbor discovery
2. **`/ip arp print detail`** - ARP table entries
3. **`/interface print detail`** - Interface information

It then analyzes the results to identify MikroTik devices based on:
- Platform information (MikroTik, RouterOS)
- MAC address OUI prefixes
- Device identity and board information
- Software version details

## Usage

### Option 1: Quick Scan Script

The simplest way to use the scanner:

```bash
python scan_neighbors.py
```

This will prompt you for:
- Router IP/hostname
- Username (default: admin)
- Password
- SSH port (default: 22)
- Whether to populate site configuration

### Option 2: Multi-Site Manager Command

Use the integrated command in the multi-site manager:

```bash
cd multi-site-manager
python site_manager.py site scan --host 192.168.88.1 --username admin --password YourPassword --populate
```

**Command Options:**
- `--host` - Router IP/hostname to scan from
- `--username` - SSH username (default: admin)
- `--password` - SSH password
- `--port` - SSH port (default: 22)
- `--populate` - Automatically populate site config
- `--default-password` - Default password for discovered devices

### Option 3: Direct Python Usage

For programmatic usage:

```python
from multi_site_manager.lib.neighbor_scanner import MikroTikNeighborScanner

# Initialize scanner
scanner = MikroTikNeighborScanner()

# Scan from a router
result = scanner.scan_from_router('192.168.88.1', 'admin', 'password')

# Display results
scanner.display_scan_results(result)

# Populate site configuration
if result['mikrotik_devices']:
    population_result = scanner.populate_site_config(
        result['mikrotik_devices'],
        'admin',
        'default_password'
    )
    scanner.display_population_results(population_result)
```

## Example Output

### Scan Results
```
Scan Results from 192.168.88.1

┌─────────────────────────────────────────────────────────┐
│                    Scan Summary                         │
├─────────────────────────────────────────────────────────┤
│ Neighbors Found    │ 5                                  │
│ ARP Entries        │ 12                                 │
│ Interfaces         │ 8                                  │
│ MikroTik Devices   │ 5                                  │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│              Discovered MikroTik Devices                │
├─────────────────────────────────────────────────────────┤
│ IP Address    │ Identity        │ MAC Address    │ Source │
├─────────────────────────────────────────────────────────┤
│ 192.168.88.186│ 007-RB2011      │ 64:D1:54:69:D9:0A │ neighbor │
│ 192.168.88.198│ 003-RB4011      │ C4:AD:34:D9:85:FE │ neighbor │
│ 192.168.88.228│ 002-RB4011      │ B8:69:F4:F2:CA:10 │ neighbor │
│ 192.168.88.230│ 005-RB850       │ 64:D1:54:13:6F:3F │ neighbor │
│ 192.168.88.232│ SW-000-CRS-328  │ 74:4D:28:6B:4F:B3 │ neighbor │
└─────────────────────────────────────────────────────────┘
```

### Population Results
```
Population Summary
┌─────────────────────────────────────────────────────────┐
│ Total Discovered    │ 5                                  │
│ Sites Added         │ 5                                  │
│ Sites Skipped       │ 0                                  │
└─────────────────────────────────────────────────────────┘

Added Sites
┌─────────────────────────────────────────────────────────┐
│ Site ID        │ IP Address      │ Name                 │
├─────────────────────────────────────────────────────────┤
│ 007-rb2011     │ 192.168.88.186  │ 007-RB2011           │
│ 003-rb4011     │ 192.168.88.198  │ 003-RB4011           │
│ 002-rb4011     │ 192.168.88.228  │ 002-RB4011           │
│ 005-rb850      │ 192.168.88.230  │ 005-RB850            │
│ sw-000-crs-328 │ 192.168.88.232  │ SW-000-CRS-328       │
└─────────────────────────────────────────────────────────┘
```

## Site Configuration

Discovered devices are automatically added to your `sites.yaml` file with the following structure:

```yaml
sites:
  007-rb2011:
    name: 007-RB2011
    host: 192.168.88.186
    username: admin
    password: NewSecureAdmin2025!
    ssh_port: 22
    location: Discovered via neighbor
    priority: medium
    tags:
    - discovered
    - auto-populated
    notes: Auto-discovered on 2025-10-18T00:19:56.766149
    discovery_info:
      source: neighbor
      discovered_at: '2025-10-18T00:19:56.766149'
      mac_address: 64:D1:54:69:D9:0A
      interface: sfp-sfpplus1,bridge
```

## Device Identification

The scanner identifies MikroTik devices using multiple criteria:

### Platform Detection
- Looks for "MikroTik", "RouterOS", "RouterBoard" in platform field
- Checks for MikroTik-specific board names (RB, CCR, CR, HEX, HAP, etc.)

### MAC Address Detection
Known MikroTik OUI prefixes:
- `00:0C:42` - MikroTik
- `4C:5E:0C` - MikroTik
- `48:8F:5A` - MikroTik
- `D4:CA:6D` - MikroTik
- `E4:8D:8C` - MikroTik

### Device Information
- Identity field containing MikroTik device names
- Board information (RB2011, RB4011, CRS328, etc.)
- Software ID and version information

## Troubleshooting

### Common Issues

**No devices discovered:**
- Ensure the router has neighbor discovery enabled
- Check that devices are on the same network segment
- Verify that CDP/MNDP protocols are running

**Authentication errors:**
- Verify credentials for the source router
- Check SSH access and port configuration
- Ensure the user has appropriate permissions

**Parsing errors:**
- Check RouterOS version compatibility
- Verify command output format
- Review log files for detailed error information

### Log Files

The scanner creates detailed logs in:
- `neighbor_scan.log` - Scanner-specific logs
- `multi-site-manager.log` - Multi-site manager logs

### Debug Mode

For detailed debugging, you can modify the logging level in the scanner:

```python
scanner.logger.setLevel(logging.DEBUG)
```

## Integration with Multi-Site Manager

Once devices are discovered and added to the site configuration, you can use all multi-site manager features:

### Status Check
```bash
python site_manager.py status
```

### Health Monitoring
```bash
python site_manager.py health --all
```

### Bulk Operations
```bash
python site_manager.py bulk execute "/system identity print" --sites all
```

### Backup Management
```bash
python site_manager.py backup create --all
```

## Security Considerations

- **Credentials**: The scanner uses the same credentials for all discovered devices
- **Network Access**: Ensure proper network segmentation and access controls
- **Logging**: Sensitive information may be logged - review log files
- **Permissions**: Use appropriate user accounts with minimal required permissions

## Best Practices

1. **Regular Scanning**: Run the scanner periodically to discover new devices
2. **Credential Management**: Use consistent credentials across your MikroTik devices
3. **Network Documentation**: Keep track of device locations and purposes
4. **Backup Strategy**: Create backups before making bulk changes
5. **Testing**: Test commands on a single device before running bulk operations

## Advanced Usage

### Custom Discovery Methods

You can extend the scanner to use additional discovery methods:

```python
class CustomNeighborScanner(MikroTikNeighborScanner):
    def _get_custom_discovery(self, execute_command):
        # Add custom discovery logic
        result = execute_command('/your/custom/command')
        return self._parse_custom_output(result)
```

### Filtering Results

Filter discovered devices based on criteria:

```python
# Filter by device type
rb_devices = [d for d in devices if 'RB' in d.get('board', '')]

# Filter by IP range
local_devices = [d for d in devices if d['ip'].startswith('192.168.88.')]
```

### Batch Processing

Process multiple networks:

```python
routers = [
    ('192.168.1.1', 'admin', 'password1'),
    ('192.168.2.1', 'admin', 'password2'),
    ('10.0.0.1', 'admin', 'password3')
]

all_devices = []
for host, username, password in routers:
    result = scanner.scan_from_router(host, username, password)
    all_devices.extend(result['mikrotik_devices'])

scanner.populate_site_config(all_devices)
```

## Support

For issues or questions:
1. Check the log files for detailed error information
2. Verify RouterOS version compatibility
3. Test connectivity to individual devices
4. Review the multi-site manager documentation

## Changelog

### Version 1.0.0
- Initial release
- Basic neighbor discovery
- Auto-population of site configuration
- Integration with multi-site manager
- Rich output formatting
- Comprehensive logging
