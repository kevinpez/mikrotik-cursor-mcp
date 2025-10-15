# WireGuard VPN Feature for MikroTik MCP Server

**Added:** October 15, 2025

## Overview

WireGuard VPN management has been added to the MikroTik MCP server, enabling full automation of WireGuard interface and peer configuration on MikroTik routers through MCP tools.

## Features Added

### WireGuard Interface Management
- ✅ List all WireGuard interfaces with filtering options
- ✅ Create new WireGuard interfaces with custom settings
- ✅ Remove WireGuard interfaces
- ✅ Update interface configuration (port, MTU, keys)
- ✅ Get detailed interface information
- ✅ Enable/disable interfaces

### WireGuard Peer Management
- ✅ List all peers with filtering
- ✅ Add peers with full configuration
- ✅ Remove peers by public key or ID
- ✅ Update peer settings (endpoint, allowed IPs, keepalive)

## Usage

### Using Nested Tool (Recommended)

The WireGuard functionality is available through the `mikrotik_wireguard` nested tool with the following actions:

```python
# List all WireGuard interfaces
mikrotik_wireguard(action="list_wireguard_interfaces")

# Create a new interface
mikrotik_wireguard(
    action="create_wireguard_interface",
    name="wireguard-aws",
    listen_port=51820,
    private_key="YOUR_PRIVATE_KEY_BASE64",
    mtu=1420,
    comment="VPN to AWS EC2"
)

# Add a peer
mikrotik_wireguard(
    action="add_wireguard_peer",
    interface="wireguard-aws",
    public_key="SERVER_PUBLIC_KEY_BASE64",
    endpoint_address="52.91.171.70",
    endpoint_port=51820,
    allowed_address="10.13.13.1/32",
    preshared_key="PRESHARED_KEY_BASE64",
    persistent_keepalive="25s",
    comment="AWS EC2 Server"
)

# List peers
mikrotik_wireguard(
    action="list_wireguard_peers",
    interface="wireguard-aws"
)

# Update interface
mikrotik_wireguard(
    action="update_wireguard_interface",
    name="wireguard-aws",
    mtu=1380
)

# Remove peer
mikrotik_wireguard(
    action="remove_wireguard_peer",
    interface="wireguard-aws",
    public_key="PEER_PUBLIC_KEY"
)
```

### Available Actions

1. **list_wireguard_interfaces** - List all WireGuard interfaces
2. **create_wireguard_interface** - Create a new WireGuard interface
3. **remove_wireguard_interface** - Remove a WireGuard interface
4. **update_wireguard_interface** - Update interface settings
5. **get_wireguard_interface** - Get detailed interface info
6. **enable_wireguard_interface** - Enable an interface
7. **disable_wireguard_interface** - Disable an interface
8. **list_wireguard_peers** - List all peers
9. **add_wireguard_peer** - Add a new peer
10. **remove_wireguard_peer** - Remove a peer
11. **update_wireguard_peer** - Update peer settings

## Example: Complete VPN Setup

Here's how to set up a complete WireGuard VPN connection to an AWS EC2 server:

```python
# Step 1: Create the WireGuard interface
result = mikrotik_wireguard(
    action="create_wireguard_interface",
    name="wireguard-aws",
    listen_port=51820,
    private_key="TSvQzGFm4FfI+MP+jcXFosjOXvZmD6//0nN34KuOHoU=",
    mtu=1420,
    comment="WireGuard VPN to AWS EC2"
)

# Step 2: Add IP address to the interface (using IP tools)
mikrotik_ip(
    action="add_ip_address",
    address="10.13.13.2/24",
    interface="wireguard-aws",
    comment="WireGuard VPN IP"
)

# Step 3: Add the peer (EC2 server)
mikrotik_wireguard(
    action="add_wireguard_peer",
    interface="wireguard-aws",
    public_key="MUJxbw8J894wzMTMSZ8XW1AaXosq4bljXkHbUI9RGSM=",
    preshared_key="WP7fPHFKxEpgCo454ndfEeJuwbz5c5rPiZmeqP4a+kE=",
    endpoint_address="52.91.171.70",
    endpoint_port=51820,
    allowed_address="10.13.13.1/32",
    persistent_keepalive="25s",
    comment="AWS EC2 WireGuard Server"
)

# Step 4: Add firewall rules (using firewall tools)
mikrotik_firewall(
    action="create_filter_rule",
    chain="input",
    protocol="udp",
    dst_port="51820",
    action_type="accept",
    comment="Allow WireGuard"
)

mikrotik_firewall(
    action="create_filter_rule",
    chain="forward",
    in_interface="wireguard-aws",
    action_type="accept",
    comment="Allow WireGuard Forward In"
)

mikrotik_firewall(
    action="create_filter_rule",
    chain="forward",
    out_interface="wireguard-aws",
    action_type="accept",
    comment="Allow WireGuard Forward Out"
)

# Step 5: Verify the connection
mikrotik_wireguard(
    action="list_wireguard_peers",
    interface="wireguard-aws"
)

# Step 6: Test connectivity
mikrotik_diagnostics(
    action="ping",
    address="10.13.13.1",
    count=4
)
```

## Files Modified

1. **src/mcp_mikrotik/scope/wireguard.py** - Core WireGuard functions
2. **src/mcp_mikrotik/tools/wireguard_tools.py** - Tool definitions and handlers
3. **src/mcp_mikrotik/serve.py** - Added wireguard category
4. **src/mcp_mikrotik/tools/tool_registry.py** - Registered wireguard handlers

## Requirements

- MikroTik RouterOS 7.0+ (WireGuard support)
- MCP server running with MikroTik connection configured

## Testing

To test the new functionality:

```python
# List current interfaces
result = mikrotik_wireguard(action="list_wireguard_interfaces")
print(result)

# Create test interface
result = mikrotik_wireguard(
    action="create_wireguard_interface",
    name="wg-test",
    comment="Test interface"
)
print(result)

# Verify creation
result = mikrotik_wireguard(
    action="get_wireguard_interface",
    name="wg-test"
)
print(result)

# Clean up
result = mikrotik_wireguard(
    action="remove_wireguard_interface",
    name="wg-test"
)
print(result)
```

## Parameters Reference

### Interface Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| name | string | Yes | - | Interface name |
| listen_port | integer | No | 51820 | UDP port to listen on |
| private_key | string | No | auto-generated | Base64-encoded private key |
| mtu | integer | No | 1420 | MTU size |
| comment | string | No | - | Optional comment |

### Peer Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| interface | string | Yes | - | WireGuard interface name |
| public_key | string | Yes | - | Peer's public key (base64) |
| endpoint_address | string | No | - | Peer's IP/hostname |
| endpoint_port | integer | No | - | Peer's UDP port |
| allowed_address | string | No | - | Allowed IPs (CIDR) |
| preshared_key | string | No | - | Preshared key for extra security |
| persistent_keepalive | string | No | - | Keepalive interval (e.g., "25s") |
| comment | string | No | - | Optional comment |

## Integration with Other MCP Servers

This feature was designed to work seamlessly with other MCP servers. For example, the AWS MCP server can:

1. Create and configure an EC2 instance with WireGuard
2. Retrieve server keys and configuration
3. Pass configuration to MikroTik MCP server
4. Set up the complete VPN tunnel

See `WIREGUARD_VPN_SETUP.md` in the root directory for a complete example.

## Security Notes

- **Private keys are sensitive** - Handle them securely
- Always use **preshared keys** for additional security layer
- Consider **rotating keys** periodically (every 3-6 months)
- Use **allowed-address** to restrict peer access
- Keep **persistent-keepalive** reasonable (25-60 seconds)

## Troubleshooting

### Connection not establishing?
```python
# Check interface status
mikrotik_wireguard(action="get_wireguard_interface", name="wireguard-aws")

# Check peer status  
mikrotik_wireguard(action="list_wireguard_peers", interface="wireguard-aws")

# Look for "last-handshake" timestamp - should be recent
```

### High latency?
```python
# Reduce MTU
mikrotik_wireguard(
    action="update_wireguard_interface",
    name="wireguard-aws",
    mtu=1380
)
```

### Firewall blocking?
```python
# Verify firewall rules allow WireGuard traffic
mikrotik_firewall(action="list_filter_rules")
```

## Future Enhancements

Potential improvements for future versions:
- [ ] Automatic key generation helper
- [ ] Connection status monitoring
- [ ] Bandwidth statistics per peer
- [ ] Multiple peer management in single call
- [ ] Configuration export/import
- [ ] Integration with cloud provider APIs

## Contributing

To extend this feature:
1. Add new functions to `scope/wireguard.py`
2. Add corresponding tool definitions to `tools/wireguard_tools.py`
3. Update action lists in `serve.py`
4. Test thoroughly with real MikroTik hardware

## License

Same as the main MikroTik MCP server project.

---

**Created with ❤️ to enable full network automation through MCP servers**

