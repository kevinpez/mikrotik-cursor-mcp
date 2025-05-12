# MikroTik Router Management

A Python package for managing MikroTik routers via SSH using the Model Context Protocol (MCP) architecture. This package provides a modular, well-organized approach to managing MikroTik devices through SSH.

## Features

- **VLAN Interface Management**
  - Create VLAN interfaces with various configurations
  - List existing VLAN interfaces with filtering
  - Get detailed information about specific VLAN interfaces
  - Update VLAN interface configurations
  - Remove VLAN interfaces

- **IP Address Management**
  - Add IP addresses to interfaces
  - List IP addresses with filtering options
  - Get detailed information about specific IP addresses
  - Remove IP addresses

- **DHCP Server Management**
  - Create DHCP servers and configure them
  - Create DHCP address pools
  - Create DHCP network configurations
  - List DHCP servers with filtering
  - Get detailed information about DHCP servers
  - Remove DHCP servers

- **Connection Configuration**
  - Configure MikroTik device connection parameters
  - Support for custom SSH credentials and ports
  - Secure password handling

## Project Structure

The project is organized into the following modules:

```
mikrotik/
├── __init__.py          # Package initialization
├── __main__.py          # Entry point for running as a module
├── config/              # Configuration settings
│   ├── __init__.py
│   └── settings.py      # Default settings and configuration functions
├── core/                # Core functionality
│   ├── __init__.py
│   └── ssh_client.py    # SSH client for MikroTik communication
├── services/            # Service modules for different MikroTik features
│   ├── __init__.py
│   ├── dhcp.py          # DHCP server management
│   ├── ip.py            # IP address management
│   └── vlan.py          # VLAN interface management
├── utils/               # Utility functions
│   ├── __init__.py
│   └── logger.py        # Logging configuration
└── server.py            # MCP server implementation
```

## Prerequisites

- Python 3.7 or higher
- MikroTik device with SSH access enabled
- SSH credentials for the MikroTik device

## Installation

1. Install the required Python packages:

```bash
pip install mcp paramiko
```

2. Clone or download the MikroTik management package:

```bash
git clone https://github.com/yourusername/mikrotik-manager.git
cd mikrotik-manager
```

## Configuration

The package comes with default configuration that can be customized:

```python
DEFAULT_MIKROTIK_HOST = "192.168.88.1"  # Your MikroTik device IP
DEFAULT_MIKROTIK_USER = "admin"         # Your MikroTik username
DEFAULT_MIKROTIK_PASS = "IZJ7E56PCQ"    # Your MikroTik password
```

You can override these defaults using command-line arguments or the configuration functions.

## Usage

### Running the Server

Run the server with default configuration:

```bash
python -m mikrotik
```

Run with custom configuration:

```bash
python -m mikrotik --host 192.168.1.1 --username myuser --password mypass --port 22 --debug
```

### Command Line Arguments

- `--host`: MikroTik device IP/hostname (default: 192.168.88.1)
- `--username`: SSH username (default: admin)
- `--password`: SSH password
- `--port`: SSH port (default: 22)
- `--debug`: Enable debug logging

### Testing with mcp-cli

You can test all available tools using the `mcp-cli` command. Here are examples for each tool:

#### Configuration Tools

1. **Get current configuration**:
```bash
uv run mcp-cli cmd --server mikrotik --tool mikrotik_config_get --tool-args '{}'
```

2. **Update configuration**:
```bash
uv run mcp-cli cmd --server mikrotik --tool mikrotik_config_set --tool-args '{"host": "192.168.1.1", "username": "admin", "password": "newpass", "port": 22}'
```

#### VLAN Interface Tools

3. **Create a VLAN interface**:
```bash
uv run mcp-cli cmd --server mikrotik --tool mikrotik_create_vlan_interface --tool-args '{"name": "vlan100", "vlan_id": 100, "interface": "ether1", "comment": "Test VLAN"}'
```

4. **List all VLAN interfaces**:
```bash
uv run mcp-cli cmd --server mikrotik --tool mikrotik_list_vlan_interfaces --tool-args '{}'
```

### Using as a Library

You can also use the package as a library in your Python code:

```python
from mikrotik.config.settings import config_set
from mikrotik.services.vlan import create_vlan_interface, list_vlan_interfaces

# Configure connection
config_set(host="192.168.88.1", username="admin", password="yourpassword")

# Create a VLAN interface
result = create_vlan_interface(
    name="vlan100",
    vlan_id=100,
    interface="ether1",
    comment="Management VLAN"
)
print(result)

# List VLAN interfaces
vlans = list_vlan_interfaces()
print(vlans)
```

## Complete Tool Reference

Here's a complete list of all available tools with their parameters:

| Tool Name | Description | Required Parameters | Optional Parameters |
|-----------|-------------|-------------------|-------------------|
| `mikrotik_config_get` | Get current connection config | None | None |
| `mikrotik_config_set` | Update connection config | None | `host`, `username`, `password`, `port` |
| `mikrotik_create_vlan_interface` | Create a new VLAN interface | `name`, `vlan_id`, `interface` | `comment`, `disabled`, `mtu`, `use_service_tag`, `arp`, `arp_timeout` |
| `mikrotik_list_vlan_interfaces` | List VLAN interfaces | None | `name_filter`, `vlan_id_filter`, `interface_filter`, `disabled_only` |
| `mikrotik_get_vlan_interface` | Get VLAN interface details | `name` | None |
| `mikrotik_update_vlan_interface` | Update VLAN interface | `name` | `new_name`, `vlan_id`, `interface`, `comment`, `disabled`, `mtu`, `use_service_tag`, `arp`, `arp_timeout` |
| `mikrotik_remove_vlan_interface` | Remove VLAN interface | `name` | None |

## MikroTik Configuration

Before using this package, ensure your MikroTik device has SSH enabled:

```
/ip service enable ssh
/ip service set ssh port=22
```

Also, ensure the user account has sufficient privileges to manage interfaces:

```
/user group add name=interface-admin policy=read,write,test,api,ssh
/user add name=mcp-user group=interface-admin password=yourpassword
```

## Security Considerations

1. **Credentials**: The package stores credentials in memory. Use environment variables or secure credential management in production.

2. **SSH Security**: The package uses paramiko with AutoAddPolicy for SSH connections. In production, consider implementing proper host key verification.

3. **Network Security**: Ensure SSH access to your MikroTik device is properly secured with firewall rules.

## Troubleshooting

### Connection Issues

1. Verify SSH is enabled on the MikroTik device
2. Check firewall rules allow SSH access
3. Ensure the correct port is being used (default is 22)
4. Verify username and password are correct
5. Check if the MikroTik device is reachable from your network

### Command Execution Issues

1. Verify the user has appropriate permissions
2. Check MikroTik log for any errors: `/log print`
3. Enable debug logging with the `--debug` flag

## Error Messages

Common error messages and their meanings:

- **"Failed to connect to MikroTik device"**: Connection could not be established. Check host, credentials, and network connectivity.
- **"Invalid VLAN ID"**: VLAN ID must be between 1 and 4094.
- **"VLAN interface not found"**: The specified interface doesn't exist.
- **"failure: already have interface with such name"**: Interface name is already in use.

## Development

### Adding New Features

To add new MikroTik commands:

1. Create a new function in the appropriate service module
2. Add appropriate logging and error handling
3. Register the tool in the `list_tools()` function in server.py
4. Add the command handler to the `command_handlers` dictionary

## License

This package is provided as-is for use with MikroTik devices. Ensure you comply with MikroTik's licensing terms when using their products.

## Version History

- 2.0.0: Refactored into modular package structure
  - Organized code into logical modules
  - Improved error handling and logging
  - Added support for command-line arguments
  - Enhanced documentation

- 1.0.0: Initial release with VLAN interface management
  - Create, list, get, update, and remove VLAN interfaces
  - Connection configuration management
  - Command-line argument support
