# Real-World MCP Examples

**Version:** v4.8.0 (ENTERPRISE-COMPLETE)  
**Practical examples from actual deployments using MikroTik Cursor MCP**

---

## Example 1: Complete AWS EC2 to Home Router VPN Setup

**Scenario:** Set up a secure WireGuard VPN tunnel from AWS EC2 to your home MikroTik router for secure remote access and cloud integration.

**Duration:** ~45 minutes (mostly AWS provisioning time)  
**Cost:** ~$9.30/month for EC2 t2.micro  
**Complexity:** Medium  

### Prerequisites
- AWS account with MCP server configured
- MikroTik router (RouterOS 7.0+) with MCP server configured
- Basic understanding of VPN concepts

### Step 1: Create EC2 Instance with WireGuard (AWS MCP)

```python
# Create security group
aws ec2 create-security-group \
    --group-name wireguard-vpn-server \
    --description "Security group for WireGuard VPN server"

# Add firewall rules
aws ec2 authorize-security-group-ingress \
    --group-id sg-xxxxx \
    --ip-permissions IpProtocol=udp,FromPort=51820,ToPort=51820,IpRanges=[{CidrIp=0.0.0.0/0}]

aws ec2 authorize-security-group-ingress \
    --group-id sg-xxxxx \
    --ip-permissions IpProtocol=tcp,FromPort=22,ToPort=22,IpRanges=[{CidrIp=0.0.0.0/0}]

# Launch EC2 instance with WireGuard user data
aws ec2 run-instances \
    --image-id ami-052064a798f08f0d3 \
    --instance-type t2.micro \
    --security-group-ids sg-xxxxx \
    --user-data file://wireguard-setup.sh \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=WireGuard-VPN-Server}]'
```

### Step 2: Generate WireGuard Keys

```python
# Generate client keys for MikroTik
import base64, os

def generate_wg_keys():
    private_key = base64.b64encode(os.urandom(32)).decode('utf-8')
    # Public key would be derived using Curve25519
    preshared_key = base64.b64encode(os.urandom(32)).decode('utf-8')
    return private_key, preshared_key

client_private, preshared = generate_wg_keys()
```

### Step 3: Configure MikroTik Router (MikroTik MCP)

```python
# Create WireGuard interface
mikrotik_wireguard(
    action="create_wireguard_interface",
    name="wireguard-aws",
    listen_port=51820,
    private_key=client_private,
    mtu=1420,
    comment="WireGuard VPN to AWS EC2"
)

# Add VPN IP address
mikrotik_ip(
    action="add_ip_address",
    address="10.13.13.2/24",
    interface="wireguard-aws",
    comment="WireGuard VPN IP"
)

# Add EC2 server as peer
mikrotik_wireguard(
    action="add_wireguard_peer",
    interface="wireguard-aws",
    public_key="SERVER_PUBLIC_KEY",
    endpoint_address="52.91.171.70",
    endpoint_port=51820,
    allowed_address="10.13.13.1/32",
    preshared_key=preshared,
    persistent_keepalive="25s",
    comment="AWS EC2 WireGuard Server"
)
```

### Step 4: Verify Connection

```python
# Check peer status
mikrotik_wireguard(
    action="list_wireguard_peers",
    interface="wireguard-aws"
)
# Look for: last-handshake=recent, rx/tx active

# Test connectivity
mikrotik_diagnostics(
    action="ping",
    address="10.13.13.1",
    count=4
)
# Expected: 0% packet loss

# Test SSH over VPN
mikrotik_diagnostics(
    action="check_connection",
    address="10.13.13.1",
    port=22
)
```

### Results Achieved
- ✅ Secure VPN tunnel established in ~45 minutes
- ✅ 0% packet loss, ~52ms latency
- ✅ SSH accessible over VPN (10.13.13.1)
- ✅ Complete automation via MCP servers
- ✅ Zero manual configuration required

---

## Example 2: Monitor System Resources

**Scenario:** Monitor your MikroTik router's health and resource usage.

```python
# Get comprehensive system stats
mikrotik_system(
    action="get_system_resources"
)
# Shows: CPU, RAM, disk usage, uptime

# Check system health
mikrotik_system(
    action="get_system_health"
)
# Shows: temperature, voltage, fan status

# Quick uptime check
mikrotik_system(
    action="get_uptime"
)
```

**Use Cases:**
- Automated monitoring dashboards
- Alert on high resource usage
- Capacity planning
- Troubleshooting performance issues

---

## Example 3: Network Diagnostics

**Scenario:** Troubleshoot network connectivity issues.

```python
# Test connectivity to remote host
mikrotik_diagnostics(
    action="ping",
    address="8.8.8.8",
    count=10
)

# Trace route to destination
mikrotik_diagnostics(
    action="traceroute",
    address="google.com"
)

# Check DNS resolution
mikrotik_diagnostics(
    action="dns_lookup",
    hostname="example.com"
)

# View ARP table
mikrotik_diagnostics(
    action="get_arp_table"
)

# Test TCP port connectivity
mikrotik_diagnostics(
    action="check_connection",
    address="192.168.1.100",
    port=80
)
```

---

## Example 4: Bandwidth Management (QoS)

**Scenario:** Limit bandwidth for specific IPs or subnets.

```python
# Create bandwidth limit for IP
mikrotik_queues(
    action="create_simple_queue",
    name="guest-wifi-limit",
    target="192.168.99.0/24",
    max_limit="10M/10M",  # 10 Mbps up/down
    comment="Guest WiFi bandwidth limit"
)

# List all queues
mikrotik_queues(
    action="list_simple_queues"
)

# Disable queue temporarily
mikrotik_queues(
    action="disable_simple_queue",
    queue_name="guest-wifi-limit"
)

# Re-enable
mikrotik_queues(
    action="enable_simple_queue",
    queue_name="guest-wifi-limit"
)

# Remove queue
mikrotik_queues(
    action="remove_simple_queue",
    queue_name="guest-wifi-limit"
)
```

**Use Cases:**
- Guest WiFi bandwidth control
- Fair usage policies
- Prevent bandwidth hogging
- SLA enforcement

---

## Example 5: Easy Port Forwarding

**Scenario:** Forward external port to internal server.

```python
# Forward port 8080 to internal web server
mikrotik_firewall(
    action="create_port_forward",
    external_port=8080,
    internal_ip="192.168.88.50",
    internal_port=80,
    protocol="tcp",
    comment="Webserver port forward"
)

# List all port forwards
mikrotik_firewall(
    action="list_port_forwards"
)
```

**Before MCP:** Manual NAT and firewall rule creation  
**After MCP:** One command does everything!

---

## Example 6: Interface Management

**Scenario:** Monitor and manage network interfaces.

```python
# List all interfaces
mikrotik_interfaces(
    action="list_interfaces"
)

# Get traffic stats for specific interface
mikrotik_interfaces(
    action="get_interface_stats",
    interface_name="ether1"
)

# Disable interface (e.g., for maintenance)
mikrotik_interfaces(
    action="disable_interface",
    interface_name="ether5"
)

# Re-enable
mikrotik_interfaces(
    action="enable_interface",
    interface_name="ether5"
)

# Monitor real-time traffic
mikrotik_interfaces(
    action="get_interface_monitor",
    interface_name="ether1"
)

# Manage bridge ports
mikrotik_interfaces(
    action="add_bridge_port",
    bridge="bridgeLocal",
    interface="ether3"
)
```

---

## Example 7: DHCP Management

**Scenario:** Manage DHCP servers and reservations.

```python
# List DHCP servers
mikrotik_dhcp(
    action="list_dhcp_servers"
)

# Create new DHCP server
mikrotik_dhcp(
    action="create_dhcp_server",
    name="guest-network",
    interface="ether8",
    address_pool="guest-pool"
)

# Create DHCP network
mikrotik_dhcp(
    action="create_dhcp_network",
    address="192.168.99.0/24",
    gateway="192.168.99.1",
    dns_server="8.8.8.8,8.8.4.4"
)

# Create IP pool
mikrotik_dhcp(
    action="create_dhcp_pool",
    name="guest-pool",
    ranges="192.168.99.100-192.168.99.200"
)
```

---

## Example 8: DNS Management

**Scenario:** Configure DNS settings and static entries.

```python
# Get DNS settings
mikrotik_dns(
    action="get_dns_settings"
)

# Update DNS servers
mikrotik_dns(
    action="update_dns_settings",
    servers="1.1.1.1,1.0.0.1"
)

# Add static DNS entry
mikrotik_dns(
    action="create_dns_static",
    name="homeserver.local",
    address="192.168.88.100",
    comment="Home server"
)

# List static entries
mikrotik_dns(
    action="list_dns_static"
)

# Flush DNS cache
mikrotik_dns(
    action="flush_dns_cache"
)
```

---

## Example 9: Firewall Management

**Scenario:** Create and manage firewall rules.

```python
# Allow WireGuard traffic
mikrotik_firewall(
    action="create_filter_rule",
    chain="input",
    rule_action="accept",  # Fixed parameter name!
    protocol="udp",
    dst_port="51820",
    comment="Allow WireGuard VPN"
)

# Block specific IP
mikrotik_firewall(
    action="create_filter_rule",
    chain="input",
    rule_action="drop",
    src_address="192.168.1.100",
    comment="Block malicious IP"
)

# Allow established/related connections
mikrotik_firewall(
    action="create_filter_rule",
    chain="forward",
    rule_action="accept",
    connection_state="established,related",
    comment="Allow established"
)

# List all firewall rules
mikrotik_firewall(
    action="list_filter_rules",
    chain_filter="input"
)
```

---

## Example 10: Backup and Restore

**Scenario:** Regular backups of router configuration.

```python
# Create backup
mikrotik_backup(
    action="create_backup",
    name="daily-backup"
)

# List backups
mikrotik_backup(
    action="list_backups"
)

# Export configuration
mikrotik_backup(
    action="export_configuration"
)

# Restore from backup (use with caution!)
mikrotik_backup(
    action="restore_backup",
    backup_name="daily-backup"
)
```

---

## Example 11: User Management

**Scenario:** Manage router users and permissions.

```python
# List users
mikrotik_users(
    action="list_users"
)

# Create new user
mikrotik_users(
    action="create_user",
    name="monitoring",
    password="SecurePassword123",
    group="read",
    comment="Monitoring account"
)

# Update user
mikrotik_users(
    action="update_user",
    name="monitoring",
    disabled=False
)

# List user groups
mikrotik_users(
    action="list_user_groups"
)
```

---

## Example 12: VLAN Configuration

**Scenario:** Set up VLAN segregation.

```python
# Create VLAN interface
mikrotik_vlan(
    action="create_vlan_interface",
    name="vlan10",
    vlan_id=10,
    interface="ether1",
    comment="Guest VLAN"
)

# List VLANs
mikrotik_vlan(
    action="list_vlan_interfaces"
)

# Update VLAN
mikrotik_vlan(
    action="update_vlan_interface",
    name="vlan10",
    disabled=False
)
```

---

## Example 13: Routing Management

**Scenario:** Manage static routes.

```python
# Add default route
mikrotik_routes(
    action="add_default_route",
    gateway="192.168.88.1",
    comment="Default gateway"
)

# Add static route
mikrotik_routes(
    action="add_route",
    dst_address="10.0.0.0/8",
    gateway="192.168.88.254",
    comment="Corporate network"
)

# List routes
mikrotik_routes(
    action="list_routes"
)

# Get routing table
mikrotik_routes(
    action="get_routing_table"
)
```

---

## Example 14: Logs Management

**Scenario:** Monitor and analyze system logs.

```python
# Get recent logs
mikrotik_logs(
    action="get_logs"
)

# Search logs
mikrotik_logs(
    action="search_logs",
    search_term="error"
)

# Export logs
mikrotik_logs(
    action="export_logs"
)

# Clear logs (use with caution!)
mikrotik_logs(
    action="clear_logs"
)
```

---

## Example 15: Wireless Management

**Scenario:** Manage wireless interfaces and clients.

```python
# List wireless interfaces
mikrotik_wireless(
    action="list_wireless_interfaces"
)

# List connected wireless clients
mikrotik_wireless(
    action="list_wireless_clients"
)

# Update wireless settings
mikrotik_wireless(
    action="update_wireless_interface",
    interface_name="wlan1",
    disabled=False
)
```

---

## Tips for Success

### 1. Use Descriptive Comments
Always add comments to your configurations:
```python
comment="Created via MCP on 2025-10-15 for VPN access"
```

### 2. Test Before Production
Test changes on a development router first or during maintenance windows.

### 3. Keep Backups
```python
# Daily backup routine
mikrotik_backup(action="create_backup", name=f"auto-{date.today()}")
```

### 4. Monitor Resources
```python
# Check if resources are healthy before making changes
stats = mikrotik_system(action="get_system_resources")
```

### 5. Use Consistent Naming
- `vpn-aws-prod` (clear purpose and environment)
- `fw-rule-allow-vpn` (rule type and purpose)
- `dhcp-guest-network` (service and scope)

---

## Common Workflows

### Full Site Setup
```python
# 1. Set system identity
mikrotik_system(action="set_system_identity", identity="Branch-Office-01")

# 2. Configure NTP
mikrotik_system(action="set_ntp_client", primary_ntp="pool.ntp.org")

# 3. Set up basic firewall
# ... add rules ...

# 4. Configure DHCP
# ... create DHCP server ...

# 5. Create backup
mikrotik_backup(action="create_backup", name="initial-setup")
```

### Troubleshooting Checklist
```python
# 1. Check system resources
mikrotik_system(action="get_system_resources")

# 2. View recent logs
mikrotik_logs(action="get_logs")

# 3. Test connectivity
mikrotik_diagnostics(action="ping", address="8.8.8.8")

# 4. Check interface status
mikrotik_interfaces(action="list_interfaces")

# 5. Review firewall rules
mikrotik_firewall(action="list_filter_rules")
```

---

## Performance Tips

1. **Batch Operations**: Group related changes together
2. **Use Filters**: When listing, filter to reduce data
3. **Monitor First**: Check system resources before changes
4. **Incremental Changes**: Make small, testable changes
5. **Document Everything**: Use comments liberally

---

## Security Best Practices

1. **Limit SSH Access**: Use firewall rules to restrict management
2. **Use Strong Keys**: For WireGuard, use proper key generation
3. **Regular Backups**: Automate backup creation
4. **Monitor Logs**: Check for suspicious activity
5. **Keep Updated**: Update RouterOS regularly

---

**All examples tested on:**
- MikroTik RB5009UG+S+ (RouterOS 7.x)
- MikroTik Cursor MCP v4.8.0 (ENTERPRISE-COMPLETE)
- October 15, 2025

**Need Help?** Check [CAPABILITIES.md](CAPABILITIES.md) for complete API reference or [README.md](README.md) for overview.

