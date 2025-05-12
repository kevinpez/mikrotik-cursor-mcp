# MikroTik MCP Server

A Model Context Protocol (MCP) server that provides tools for managing MikroTik devices through SSH. This server allows you to manage VLAN interfaces, IP addresses, and DHCP servers on MikroTik routers and switches.

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

## Prerequisites

- Python 3.7 or higher
- MikroTik device with SSH access enabled
- SSH credentials for the MikroTik device

## Installation

1. Install the required Python packages:

```bash
pip install mcp paramiko
```

2. Clone or download the MikroTik MCP server script.

## Configuration

The server comes with default configuration that can be customized:

```python
DEFAULT_MIKROTIK_HOST = "192.168.88.1"  # Your MikroTik device IP
DEFAULT_MIKROTIK_USER = "admin"         # Your MikroTik username
DEFAULT_MIKROTIK_PASS = "IZJ7E56PCQ"    # Your MikroTik password
```

You can override these defaults using command-line arguments or the configuration tools within the MCP server.

## Usage

### Starting the Server

Run the server with default configuration:

```bash
python mikrotik_mcp_server.py
```

Run with custom configuration:

```bash
python mikrotik_mcp_server.py --host 192.168.1.1 --username myuser --password mypass --port 22
```

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

5. **List VLAN interfaces with filters**:
```bash
# Filter by name
uv run mcp-cli cmd --server mikrotik --tool mikrotik_list_vlan_interfaces --tool-args '{"name_filter": "vlan1"}'

# Filter by VLAN ID
uv run mcp-cli cmd --server mikrotik --tool mikrotik_list_vlan_interfaces --tool-args '{"vlan_id_filter": 100}'

# Filter by interface
uv run mcp-cli cmd --server mikrotik --tool mikrotik_list_vlan_interfaces --tool-args '{"interface_filter": "ether1"}'

# Show only disabled interfaces
uv run mcp-cli cmd --server mikrotik --tool mikrotik_list_vlan_interfaces --tool-args '{"disabled_only": true}'
```

6. **Get specific VLAN interface details**:
```bash
uv run mcp-cli cmd --server mikrotik --tool mikrotik_get_vlan_interface --tool-args '{"name": "vlan100"}'
```

7. **Update a VLAN interface**:
```bash
# Update comment
uv run mcp-cli cmd --server mikrotik --tool mikrotik_update_vlan_interface --tool-args '{"name": "vlan100", "comment": "Updated comment"}'

# Change VLAN ID
uv run mcp-cli cmd --server mikrotik --tool mikrotik_update_vlan_interface --tool-args '{"name": "vlan100", "vlan_id": 101}'

# Disable interface
uv run mcp-cli cmd --server mikrotik --tool mikrotik_update_vlan_interface --tool-args '{"name": "vlan100", "disabled": true}'

# Update multiple properties
uv run mcp-cli cmd --server mikrotik --tool mikrotik_update_vlan_interface --tool-args '{"name": "vlan100", "new_name": "vlan101", "mtu": 1500, "comment": "Renamed VLAN"}'
```

8. **Remove a VLAN interface**:
```bash
uv run mcp-cli cmd --server mikrotik --tool mikrotik_remove_vlan_interface --tool-args '{"name": "vlan100"}'
```

### Complete Tool Reference

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

### Testing Workflow Example

Here's a complete testing workflow to verify all functionality:

```bash
# 1. Check current configuration
uv run mcp-cli cmd --server mikrotik --tool mikrotik_config_get --tool-args '{}'

# 2. Create a test VLAN
uv run mcp-cli cmd --server mikrotik --tool mikrotik_create_vlan_interface --tool-args '{"name": "test-vlan", "vlan_id": 999, "interface": "ether1", "comment": "Test VLAN for MCP"}'

# 3. List all VLANs to confirm creation
uv run mcp-cli cmd --server mikrotik --tool mikrotik_list_vlan_interfaces --tool-args '{}'

# 4. Get details of the created VLAN
uv run mcp-cli cmd --server mikrotik --tool mikrotik_get_vlan_interface --tool-args '{"name": "test-vlan"}'

# 5. Update the VLAN
uv run mcp-cli cmd --server mikrotik --tool mikrotik_update_vlan_interface --tool-args '{"name": "test-vlan", "comment": "Updated test VLAN", "mtu": 1400}'

# 6. Verify the update
uv run mcp-cli cmd --server mikrotik --tool mikrotik_get_vlan_interface --tool-args '{"name": "test-vlan"}'

# 7. Remove the test VLAN
uv run mcp-cli cmd --server mikrotik --tool mikrotik_remove_vlan_interface --tool-args '{"name": "test-vlan"}'

# 8. Confirm removal
uv run mcp-cli cmd --server mikrotik --tool mikrotik_list_vlan_interfaces --tool-args '{"name_filter": "test-vlan"}'
```

### Available Tools

#### 1. Connection Configuration

**mikrotik_config_set**
- Update MikroTik connection configuration
- Parameters:
  - `host` (optional): MikroTik device IP/hostname
  - `username` (optional): SSH username
  - `password` (optional): SSH password
  - `port` (optional): SSH port

**mikrotik_config_get**
- Show current MikroTik connection configuration
- No parameters required

#### 2. VLAN Interface Management

**mikrotik_create_vlan_interface**
- Create a new VLAN interface
- Required parameters:
  - `name`: Interface name
  - `vlan_id`: VLAN ID (1-4094)
  - `interface`: Parent interface (e.g., ether1, bridge1)
- Optional parameters:
  - `comment`: Description for the interface
  - `disabled`: Whether to disable the interface
  - `mtu`: Maximum Transmission Unit size
  - `use_service_tag`: Enable QinQ service tag
  - `arp`: ARP mode (enabled, disabled, proxy-arp, reply-only)
  - `arp_timeout`: ARP timeout value

**mikrotik_list_vlan_interfaces**
- List all VLAN interfaces with optional filtering
- Optional parameters:
  - `name_filter`: Filter by interface name (partial match)
  - `vlan_id_filter`: Filter by VLAN ID
  - `interface_filter`: Filter by parent interface
  - `disabled_only`: Show only disabled interfaces

**mikrotik_get_vlan_interface**
- Get detailed information about a specific VLAN interface
- Required parameters:
  - `name`: Interface name

**mikrotik_update_vlan_interface**
- Update an existing VLAN interface
- Required parameters:
  - `name`: Current interface name
- Optional parameters:
  - `new_name`: New interface name
  - `vlan_id`: New VLAN ID
  - `interface`: New parent interface
  - `comment`: New description
  - `disabled`: Enable/disable the interface
  - `mtu`: New MTU value
  - `use_service_tag`: Enable/disable service tag
  - `arp`: New ARP mode
  - `arp_timeout`: New ARP timeout

**mikrotik_remove_vlan_interface**
- Remove a VLAN interface
- Required parameters:
  - `name`: Interface name to remove

## Example Workflows

### Creating a Basic VLAN Interface

```json
{
  "tool": "mikrotik_create_vlan_interface",
  "arguments": {
    "name": "vlan100",
    "vlan_id": 100,
    "interface": "ether1",
    "comment": "Management VLAN"
  }
}
```

### Listing All VLAN Interfaces

```json
{
  "tool": "mikrotik_list_vlan_interfaces",
  "arguments": {}
}
```

### Filtering VLAN Interfaces

```json
{
  "tool": "mikrotik_list_vlan_interfaces",
  "arguments": {
    "vlan_id_filter": 100,
    "interface_filter": "ether1"
  }
}
```

### Updating a VLAN Interface

```json
{
  "tool": "mikrotik_update_vlan_interface",
  "arguments": {
    "name": "vlan100",
    "comment": "Updated Management VLAN",
    "mtu": 1500
  }
}
```

### Removing a VLAN Interface

```json
{
  "tool": "mikrotik_remove_vlan_interface",
  "arguments": {
    "name": "vlan100"
  }
}
```

## MikroTik Configuration

Before using this MCP server, ensure your MikroTik device has SSH enabled:

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

1. **Credentials**: The server stores credentials in memory. Use environment variables or secure credential management in production.

2. **SSH Security**: The server uses paramiko with AutoAddPolicy for SSH connections. In production, consider implementing proper host key verification.

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
3. Enable debug logging in the MCP server for more details

### VLAN Creation Issues

1. Ensure the parent interface exists
2. Verify VLAN ID is not already in use
3. Check if the interface name is unique
4. Confirm the user has interface management permissions

## Error Messages

Common error messages and their meanings:

- **"Failed to connect to MikroTik device"**: Connection could not be established. Check host, credentials, and network connectivity.
- **"Invalid VLAN ID"**: VLAN ID must be between 1 and 4094.
- **"VLAN interface not found"**: The specified interface doesn't exist.
- **"failure: already have interface with such name"**: Interface name is already in use.

## Development

### Adding New Features

To add new MikroTik commands:

1. Create a new function following the naming pattern `mikrotik_<action>_<resource>`
2. Add appropriate logging and error handling
3. Register the tool in the `list_tools()` function
4. Add the command handler to the `command_handlers` dictionary

### Testing

Test the server locally:

```python
# Test connection
mikrotik_config_get()

# Test VLAN creation
mikrotik_create_vlan_interface(
    name="test-vlan",
    vlan_id=999,
    interface="ether1"
)

# Test listing
mikrotik_list_vlan_interfaces()
```

## Future Enhancements

Potential features to add:

1. **Bridge Management**: Create and manage bridge interfaces
2. **IP Address Configuration**: Assign IP addresses to interfaces
3. **Firewall Rules**: Manage firewall filter and NAT rules
4. **Routing**: Configure static and dynamic routing
5. **Wireless**: Manage wireless interfaces and security profiles
6. **QoS**: Configure queues and traffic shaping
7. **System Information**: Get system status, resource usage, and logs
8. **Backup/Restore**: Create and restore configuration backups

## Contributing

When contributing to this project:

1. Follow the existing code structure and naming conventions
2. Add comprehensive error handling
3. Include logging for debugging
4. Document all new functions and parameters
5. Test thoroughly with actual MikroTik devices

## License

This MCP server is provided as-is for use with MikroTik devices. Ensure you comply with MikroTik's licensing terms when using their products.

## Support

For issues related to:
- MCP framework: Check the MCP documentation
- MikroTik commands: Refer to MikroTik documentation at https://help.mikrotik.com
- This server: Open an issue in the project repository

## Version History

- 1.0.0: Initial release with VLAN interface management
  - Create, list, get, update, and remove VLAN interfaces
  - Connection configuration management
  - Command-line argument support