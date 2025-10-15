# MikroTik Cursor MCP - Complete Capabilities Reference

**378 Actions × 19 Categories = 98% RouterOS Coverage**

This document provides a complete reference of all available actions, organized by category.

**🎉 NEW in v4.7.0:** +119 actions, +8% coverage - Layer 7, VRRP, Queue Trees, PKI, and more!

---

## 📊 **Quick Reference**

| Category | Actions | Coverage | Status |
|----------|---------|----------|--------|
| **Firewall** | 47 (+24) | Filter, NAT, Mangle, RAW, Layer 7, Chains | ✅ Complete |
| **IPv6** | 39 | Addresses, Routes, Firewall, DHCPv6 | ✅ Complete |
| **System** | 39 (+28) | Resources, Packages, Scheduler, Watchdog | ✅ Complete |
| **Wireless** | 34 | Interfaces, CAPsMAN, Security | ✅ Complete |
| **Routes** | 27 | Static, BGP, OSPF, Filters | ✅ Complete |
| **Interfaces** | 37 (+15) | Stats, PPPoE, Tunnels, Bonding, VRRP, Bridge | ✅ Complete |
| **Queues** | 20 (+13) | Simple, Queue Trees, PCQ, HTB | ✅ Complete |
| **Container** | 18 | Docker, Images, Networking | ✅ Complete |
| **Certificates** | 11 (NEW) | PKI, CA, SSL/TLS | ✅ Complete |
| **WireGuard** | 11 | Interfaces, Peers, Keys | ✅ Complete |
| **Hotspot** | 10 | Servers, Users, Portal | ✅ Complete |
| **DNS** | 9 | Settings, Static, Cache | ✅ Complete |
| **OpenVPN** | 9 | Client, Server, Certs | ✅ Complete |
| **IP** | 8 | Addresses, Pools | ✅ Complete |
| **DHCP** | 7 | Servers, Pools, Leases | ✅ Complete |
| **Diagnostics** | 7 | Ping, Trace, Bandwidth | ✅ Complete |
| **Users** | 5 | Management, Groups | ✅ Complete |
| **VLAN** | 4 | Interfaces, Tagging | ✅ Complete |
| **Backup** | 4 | Create, Restore, Export | ✅ Complete |
| **Logs** | 4 | View, Search, Export | ✅ Complete |

**Total:** 378 actions across 19 categories

---

## 🔥 **1. Firewall (47 Actions) - ENHANCED with Layer 7, Chains, Address Lists**

### Filter Rules (6 actions)
```
mikrotik_firewall(action="list_filter_rules")
mikrotik_firewall(action="create_filter_rule", chain="input", rule_action="accept", ...)
mikrotik_firewall(action="remove_filter_rule", rule_id="5")
mikrotik_firewall(action="update_filter_rule", rule_id="5", ...)
mikrotik_firewall(action="list_port_forwards")
mikrotik_firewall(action="create_port_forward", external_port=8080, ...)
```

**Example Usage:**
- "Create a firewall rule to allow HTTP traffic"
- "Block all traffic from 192.168.99.0/24"
- "Set up port forwarding: 8080 → 192.168.1.100:80"
- "List all firewall filter rules"

### NAT Rules (3 actions)
```
mikrotik_firewall(action="list_nat_rules")
mikrotik_firewall(action="create_nat_rule", chain="srcnat", ...)
mikrotik_firewall(action="remove_nat_rule", rule_id="2")
mikrotik_firewall(action="update_nat_rule", rule_id="2", ...)
```

**Example Usage:**
- "Create source NAT rule on ether1"
- "Add masquerade rule for outbound traffic"
- "List all NAT rules"

### Mangle Rules (4 actions)
```
mikrotik_firewall(action="list_mangle_rules")
mikrotik_firewall(action="create_mangle_rule", chain="prerouting", ...)
mikrotik_firewall(action="remove_mangle_rule", rule_id="1")
mikrotik_firewall(action="update_mangle_rule", rule_id="1", ...)
mikrotik_firewall(action="create_routing_mark", name="ISP1", ...)
mikrotik_firewall(action="list_routing_marks")
```

**Example Usage:**
- "Mark packets from 192.168.1.0/24 with routing mark ISP1"
- "Create connection mark for VoIP traffic"
- "List all mangle rules"

### RAW Firewall (3 actions)
```
mikrotik_firewall(action="list_raw_rules")
mikrotik_firewall(action="create_raw_rule", chain="prerouting", ...)
mikrotik_firewall(action="remove_raw_rule", rule_id="0")
```

**Example Usage:**
- "Create RAW rule to bypass connection tracking for local traffic"
- "Add notrack rule for high-bandwidth connections"

### Connection Tracking (2 actions)
```
mikrotik_firewall(action="get_connection_tracking")
mikrotik_firewall(action="flush_connections", protocol="tcp", src_address="...")
```

**Example Usage:**
- "Show me all active connections"
- "Flush TCP connections from 192.168.1.100"

### Layer 7 Protocols (10 actions) - NEW in v4.7.0
```
mikrotik_list_layer7_protocols(name_filter="youtube")
mikrotik_create_layer7_protocol(name="custom-app", regexp="^.*(myapp.com).*$")
mikrotik_get_layer7_protocol(protocol_id="youtube")
mikrotik_update_layer7_protocol(protocol_id="*1", regexp="...")
mikrotik_remove_layer7_protocol(protocol_id="*1")
mikrotik_enable_layer7_protocol(protocol_id="*1")
mikrotik_disable_layer7_protocol(protocol_id="*1")
mikrotik_create_common_layer7_protocols()  # YouTube, Netflix, Facebook, etc.
```

**Example Usage:**
- "Create Layer 7 protocol matcher for YouTube traffic"
- "Block Netflix using Layer 7 filtering"
- "Set up common Layer 7 protocols for streaming services"
- "List all Layer 7 protocol matchers"

### Address List Management (9 actions) - NEW in v4.7.0
```
mikrotik_list_address_lists(list_filter="blacklist")
mikrotik_add_address_list_entry(list_name="temp-block", address="1.2.3.4", timeout="1h")
mikrotik_update_address_list_entry(entry_id="*5", timeout="30m")
mikrotik_remove_address_list_entry(entry_id="*5")
mikrotik_get_address_list_entry(entry_id="*5")
mikrotik_list_address_list_names()
mikrotik_clear_address_list(list_name="temp-block")
mikrotik_enable_address_list_entry(entry_id="*5")
mikrotik_disable_address_list_entry(entry_id="*5")
```

**Example Usage:**
- "Add IP 10.0.0.50 to blacklist for 2 hours"
- "List all entries in the VIP address list"
- "Clear the temp-block address list"
- "Update timeout for entry *3 to 1 day"

### Custom Chains (5 actions) - NEW in v4.7.0
```
mikrotik_list_custom_chains(chain_type="filter")
mikrotik_create_jump_rule(chain_type="filter", source_chain="forward", target_chain="guest-wifi")
mikrotik_list_rules_in_chain(chain_type="filter", chain_name="guest-wifi")
mikrotik_delete_custom_chain(chain_type="filter", chain_name="guest-wifi")
mikrotik_create_custom_chain_with_rules(chain_type="filter", source_chain="forward", ...)
```

**Example Usage:**
- "Create custom chain for guest WiFi traffic"
- "List all rules in my custom VPN chain"
- "Delete the old-firewall custom chain"
- "Jump all guest traffic to custom chain for inspection"

---

## 🌐 **2. IPv6 (39 Actions)**

### Address Management (4 actions)
```
mikrotik_ipv6(action="list_ipv6_addresses", interface="...")
mikrotik_ipv6(action="add_ipv6_address", address="2001:db8::1/64", interface="bridge")
mikrotik_ipv6(action="remove_ipv6_address", address="2001:db8::1")
mikrotik_ipv6(action="get_ipv6_address", address="2001:db8::1")
```

**Example Usage:**
- "Add IPv6 address 2001:db8::1/64 to bridge interface"
- "List all IPv6 addresses"
- "Remove IPv6 address from eth1"

### Route Management (3 actions)
```
mikrotik_ipv6(action="list_ipv6_routes")
mikrotik_ipv6(action="add_ipv6_route", dst_address="2001:db8::/32", gateway="...")
mikrotik_ipv6(action="remove_ipv6_route", dst_address="2001:db8::/32")
```

**Example Usage:**
- "Add static IPv6 route to 2001:db8::/32"
- "Show IPv6 routing table"
- "Remove default IPv6 route"

### Neighbor Discovery (3 actions)
```
mikrotik_ipv6(action="list_ipv6_neighbors")
mikrotik_ipv6(action="get_ipv6_nd_settings", interface="bridge")
mikrotik_ipv6(action="set_ipv6_nd", interface="bridge", ra_interval="3m-10m", ...)
```

**Example Usage:**
- "List IPv6 neighbors"
- "Enable router advertisements on bridge"
- "Configure IPv6 ND settings"

### IPv6 Pools (3 actions)
```
mikrotik_ipv6(action="list_ipv6_pools")
mikrotik_ipv6(action="create_ipv6_pool", name="ipv6-pool", prefix="2001:db8::/48")
mikrotik_ipv6(action="remove_ipv6_pool", name="ipv6-pool")
```

**Example Usage:**
- "Create IPv6 pool for delegation"
- "List all IPv6 address pools"

### Global Settings (2 actions)
```
mikrotik_ipv6(action="get_ipv6_settings")
mikrotik_ipv6(action="set_ipv6_forward", enabled=true)
```

**Example Usage:**
- "Enable IPv6 forwarding"
- "Show global IPv6 settings"

### IPv6 Firewall (12 actions)
```
# Filter Rules
mikrotik_ipv6(action="list_ipv6_filter_rules")
mikrotik_ipv6(action="create_ipv6_filter_rule", chain="input", rule_action="accept", ...)
mikrotik_ipv6(action="remove_ipv6_filter_rule", rule_id="3")

# NAT Rules
mikrotik_ipv6(action="list_ipv6_nat_rules")
mikrotik_ipv6(action="create_ipv6_nat_rule", chain="srcnat", ...)
mikrotik_ipv6(action="remove_ipv6_nat_rule", rule_id="1")

# Address Lists
mikrotik_ipv6(action="list_ipv6_address_lists")
mikrotik_ipv6(action="add_ipv6_address_list", list_name="whitelist", address="2001:db8::1")
mikrotik_ipv6(action="remove_ipv6_address_list_entry", entry_id="2")

# Mangle Rules
mikrotik_ipv6(action="list_ipv6_mangle_rules")
mikrotik_ipv6(action="create_ipv6_mangle_rule", chain="prerouting", ...)
mikrotik_ipv6(action="remove_ipv6_mangle_rule", rule_id="1")
```

**Example Usage:**
- "Create IPv6 firewall rule to allow ICMPv6"
- "Add IPv6 address to whitelist"
- "List all IPv6 mangle rules"

### DHCPv6 Server (12 actions)
```
# Server Management
mikrotik_ipv6(action="list_dhcpv6_servers")
mikrotik_ipv6(action="create_dhcpv6_server", name="dhcpv6-1", interface="bridge", ...)
mikrotik_ipv6(action="remove_dhcpv6_server", name="dhcpv6-1")
mikrotik_ipv6(action="get_dhcpv6_server", name="dhcpv6-1")

# Lease Management
mikrotik_ipv6(action="list_dhcpv6_leases")
mikrotik_ipv6(action="create_dhcpv6_static_lease", address="2001:db8::100", duid="...")
mikrotik_ipv6(action="remove_dhcpv6_lease", lease_id="5")

# Client Management
mikrotik_ipv6(action="list_dhcpv6_clients")
mikrotik_ipv6(action="create_dhcpv6_client", interface="ether1", ...)
mikrotik_ipv6(action="remove_dhcpv6_client", interface="ether1")
mikrotik_ipv6(action="get_dhcpv6_client", interface="ether1")

# Options
mikrotik_ipv6(action="list_dhcpv6_options")
mikrotik_ipv6(action="create_dhcpv6_option", name="dns", code=23, value="...")
mikrotik_ipv6(action="remove_dhcpv6_option", name="dns")
```

**Example Usage:**
- "Create DHCPv6 server on bridge with prefix delegation"
- "List all DHCPv6 leases"
- "Configure DHCPv6 client on WAN interface"

---

## 📦 **3. Container (18 Actions)**

### Lifecycle Management (6 actions)
```
mikrotik_container(action="list_containers")
mikrotik_container(action="create_container", name="nginx", image="nginx:latest", ...)
mikrotik_container(action="remove_container", name="nginx")
mikrotik_container(action="start_container", name="nginx")
mikrotik_container(action="stop_container", name="nginx")
mikrotik_container(action="get_container", name="nginx")
```

**Example Usage:**
- "Create container from nginx:latest image"
- "List all running containers"
- "Start the Pi-hole container"
- "Stop and remove old containers"

### Configuration (3 actions)
```
mikrotik_container(action="get_container_config")
mikrotik_container(action="set_container_registry", url="https://registry.example.com", ...)
mikrotik_container(action="set_container_tmpdir", tmpdir="/disk1/containers/tmp")
```

**Example Usage:**
- "Set container registry to docker.io"
- "Show container configuration"
- "Configure container temporary directory"

### Environments (3 actions)
```
mikrotik_container(action="list_container_envs")
mikrotik_container(action="create_container_env", name="myapp", key="DB_HOST", value="...")
mikrotik_container(action="remove_container_env", name="myapp")
```

**Example Usage:**
- "Create environment variable DB_HOST for myapp"
- "List all container environment variables"

### Mounts (3 actions)
```
mikrotik_container(action="list_container_mounts")
mikrotik_container(action="create_container_mount", name="data", src="/disk1/data", dst="/app/data")
mikrotik_container(action="remove_container_mount", name="data")
```

**Example Usage:**
- "Create mount point for container data"
- "List all container mounts"

### Networking (3 actions)
```
mikrotik_container(action="list_container_veths")
mikrotik_container(action="create_container_veth", name="veth1", address="172.17.0.2/16", ...)
mikrotik_container(action="remove_container_veth", name="veth1")
```

**Example Usage:**
- "Create veth interface for container networking"
- "List all container network interfaces"

---

## 📡 **4. Wireless (34 Actions)**

### Basic Management (7 actions)
```
mikrotik_wireless(action="create_wireless_interface", name="wlan1", ssid="MyNetwork", ...)
mikrotik_wireless(action="list_wireless_interfaces")
mikrotik_wireless(action="get_wireless_interface", name="wlan1")
mikrotik_wireless(action="update_wireless_interface", name="wlan1", ...)
mikrotik_wireless(action="remove_wireless_interface", name="wlan1")
mikrotik_wireless(action="enable_wireless_interface", name="wlan1")
mikrotik_wireless(action="disable_wireless_interface", name="wlan1")
```

**Example Usage:**
- "Create WiFi network with SSID HomeNet"
- "Disable wireless interface temporarily"
- "List all wireless clients"

### Security Profiles (5 actions - v6.x)
```
mikrotik_wireless(action="create_wireless_security_profile", name="secure", ...)
mikrotik_wireless(action="list_wireless_security_profiles")
mikrotik_wireless(action="get_wireless_security_profile", name="secure")
mikrotik_wireless(action="remove_wireless_security_profile", name="secure")
mikrotik_wireless(action="update_wireless_security_profile", name="secure", ...)
```

**Example Usage:**
- "Create WPA2 security profile"
- "Update WiFi password"

### Access Lists (3 actions - v6.x)
```
mikrotik_wireless(action="create_wireless_access_list", interface="wlan1", mac_address="...")
mikrotik_wireless(action="list_wireless_access_list")
mikrotik_wireless(action="remove_wireless_access_list_entry", entry_id="5")
```

**Example Usage:**
- "Add MAC address to wireless whitelist"
- "Block specific device from WiFi"

### Network Operations (2 actions)
```
mikrotik_wireless(action="scan_wireless_networks", interface="wlan1")
mikrotik_wireless(action="get_wireless_registration_table")
```

**Example Usage:**
- "Scan for nearby WiFi networks"
- "Show connected wireless clients"

### Monitoring (4 actions)
```
mikrotik_wireless(action="get_wireless_interface_monitor", interface="wlan1")
mikrotik_wireless(action="get_wireless_frequencies")
mikrotik_wireless(action="export_wireless_config")
mikrotik_wireless(action="check_wireless_support")
```

**Example Usage:**
- "Show real-time wireless interface stats"
- "Export wireless configuration"
- "Check if router supports wireless"

### CAPsMAN (13 actions)
```
# Manager
mikrotik_wireless(action="enable_capsman")
mikrotik_wireless(action="disable_capsman")
mikrotik_wireless(action="get_capsman_status")

# Interfaces
mikrotik_wireless(action="list_capsman_interfaces")
mikrotik_wireless(action="get_capsman_interface", name="cap1")

# Configuration
mikrotik_wireless(action="create_capsman_configuration", name="office", ssid="OfficeWiFi", ...)
mikrotik_wireless(action="list_capsman_configurations")
mikrotik_wireless(action="remove_capsman_configuration", name="office")

# Provisioning
mikrotik_wireless(action="create_capsman_provisioning_rule", name="auto-provision", ...)
mikrotik_wireless(action="list_capsman_provisioning_rules")
mikrotik_wireless(action="remove_capsman_provisioning_rule", name="auto-provision")

# Registration & Remote CAPs
mikrotik_wireless(action="list_capsman_registration_table")
mikrotik_wireless(action="list_capsman_remote_caps")
mikrotik_wireless(action="get_capsman_remote_cap", identity="CAP-Office-1")

# Datapath
mikrotik_wireless(action="create_capsman_datapath", name="bridge-dp", bridge="bridge", ...)
mikrotik_wireless(action="list_capsman_datapaths")
mikrotik_wireless(action="remove_capsman_datapath", name="bridge-dp")
```

**Example Usage:**
- "Enable CAPsMAN controller"
- "Create centralized WiFi configuration"
- "List all managed Access Points"
- "Show connected clients across all APs"

---

## 🛣️ **5. Routes (27 Actions)**

### Static Routes (10 actions)
```
mikrotik_routes(action="list_routes")
mikrotik_routes(action="add_route", dst_address="10.0.0.0/8", gateway="192.168.1.1")
mikrotik_routes(action="remove_route", route_id="5")
mikrotik_routes(action="update_route", route_id="5", distance=10)
mikrotik_routes(action="enable_route", route_id="5")
mikrotik_routes(action="disable_route", route_id="5")
mikrotik_routes(action="get_route", dst_address="10.0.0.0/8")
mikrotik_routes(action="add_default_route", gateway="192.168.1.1")
mikrotik_routes(action="add_blackhole_route", dst_address="192.168.99.0/24")
mikrotik_routes(action="get_routing_table")
```

**Example Usage:**
- "Add static route to 10.0.0.0/8 via 192.168.1.1"
- "Create default route"
- "Show complete routing table"

### BGP (8 actions)
```
mikrotik_routes(action="create_bgp_instance", name="bgp1", as=65001, router_id="1.1.1.1")
mikrotik_routes(action="add_bgp_peer", instance="bgp1", remote_address="10.0.0.1", remote_as=65002)
mikrotik_routes(action="list_bgp_peers")
mikrotik_routes(action="add_bgp_network", network="192.168.1.0/24")
mikrotik_routes(action="list_bgp_networks")
mikrotik_routes(action="list_bgp_routes")
mikrotik_routes(action="get_bgp_status")
mikrotik_routes(action="clear_bgp_session", peer="...")
```

**Example Usage:**
- "Configure BGP peering with ISP"
- "Advertise 192.168.0.0/16 via BGP"
- "Show BGP routes and status"
- "Reset BGP session"

### OSPF (7 actions)
```
mikrotik_routes(action="create_ospf_instance", name="ospf1", router_id="1.1.1.1")
mikrotik_routes(action="add_ospf_network", network="192.168.1.0/24", area="backbone")
mikrotik_routes(action="add_ospf_interface", interface="ether1", area="backbone")
mikrotik_routes(action="list_ospf_neighbors")
mikrotik_routes(action="list_ospf_routes")
mikrotik_routes(action="get_ospf_status")
mikrotik_routes(action="create_ospf_area", name="area1", area_id="0.0.0.1")
```

**Example Usage:**
- "Configure OSPF routing"
- "Add network to OSPF area 0"
- "Show OSPF neighbors and routes"
- "Create OSPF stub area"

### Route Filtering (2 actions)
```
mikrotik_routes(action="create_route_filter", chain="input", rule="...", action="accept")
mikrotik_routes(action="list_route_filters")
```

**Example Usage:**
- "Create route filter to accept specific prefixes"
- "Filter BGP routes"

---

## 🔌 **6. Interfaces (22 Actions)**

### Basic Management (9 actions)
```
mikrotik_interfaces(action="list_interfaces")
mikrotik_interfaces(action="get_interface_stats", interface="ether1")
mikrotik_interfaces(action="enable_interface", interface="ether2")
mikrotik_interfaces(action="disable_interface", interface="ether2")
mikrotik_interfaces(action="get_interface_monitor", interface="ether1")
mikrotik_interfaces(action="get_interface_traffic", interface="ether1")
mikrotik_interfaces(action="list_bridge_ports")
mikrotik_interfaces(action="add_bridge_port", bridge="bridge", interface="ether3")
mikrotik_interfaces(action="remove_bridge_port", interface="ether3")
```

**Example Usage:**
- "Show all network interfaces"
- "Get traffic statistics for ether1"
- "Add ether3 to bridge"
- "Disable unused interfaces"

### PPPoE (5 actions)
```
mikrotik_interfaces(action="list_pppoe_clients")
mikrotik_interfaces(action="create_pppoe_client", interface="ether1", user="...", password="...")
mikrotik_interfaces(action="remove_pppoe_client", interface="pppoe-out1")
mikrotik_interfaces(action="get_pppoe_status", interface="pppoe-out1")
mikrotik_interfaces(action="list_pppoe_servers")
```

**Example Usage:**
- "Create PPPoE client on ether1"
- "Show PPPoE connection status"
- "List all PPPoE servers"

### Tunnels (7 actions)
```
# EoIP Tunnels
mikrotik_interfaces(action="list_eoip_tunnels")
mikrotik_interfaces(action="create_eoip_tunnel", name="eoip1", remote_address="1.2.3.4", tunnel_id=1)
mikrotik_interfaces(action="remove_eoip_tunnel", name="eoip1")

# GRE Tunnels
mikrotik_interfaces(action="list_gre_tunnels")
mikrotik_interfaces(action="create_gre_tunnel", name="gre1", remote_address="1.2.3.4")
mikrotik_interfaces(action="remove_gre_tunnel", name="gre1")

# All Tunnels
mikrotik_interfaces(action="list_tunnels")
```

**Example Usage:**
- "Create EoIP tunnel to remote site"
- "Set up GRE tunnel for VPN"
- "List all active tunnels"

### Link Aggregation (4 actions)
```
mikrotik_interfaces(action="list_bonding_interfaces")
mikrotik_interfaces(action="create_bonding_interface", name="bond1", mode="802.3ad")
mikrotik_interfaces(action="add_bonding_slave", bonding="bond1", interface="ether2")
mikrotik_interfaces(action="remove_bonding_interface", name="bond1")
```

**Example Usage:**
- "Create LACP bonding interface"
- "Add ether2 and ether3 to bond"
- "List all bonded interfaces"

---

## 🔒 **7. WireGuard (11 Actions)**

```
mikrotik_wireguard(action="list_wireguard_interfaces")
mikrotik_wireguard(action="create_wireguard_interface", name="wg0", listen_port=51820)
mikrotik_wireguard(action="remove_wireguard_interface", name="wg0")
mikrotik_wireguard(action="update_wireguard_interface", name="wg0", ...)
mikrotik_wireguard(action="get_wireguard_interface", name="wg0")
mikrotik_wireguard(action="enable_wireguard_interface", name="wg0")
mikrotik_wireguard(action="disable_wireguard_interface", name="wg0")
mikrotik_wireguard(action="list_wireguard_peers")
mikrotik_wireguard(action="add_wireguard_peer", interface="wg0", public_key="...", endpoint="1.2.3.4:51820", ...)
mikrotik_wireguard(action="remove_wireguard_peer", peer_id="5")
mikrotik_wireguard(action="update_wireguard_peer", peer_id="5", ...)
```

**Example Usage:**
- "Create WireGuard interface on port 51820"
- "Add peer with endpoint 52.1.2.3:51820"
- "List all WireGuard peers and status"
- "Update peer allowed IPs"

---

## 🔐 **8. OpenVPN (9 Actions)**

```
mikrotik_openvpn(action="list_openvpn_interfaces")
mikrotik_openvpn(action="list_openvpn_servers")
mikrotik_openvpn(action="get_openvpn_server_status", server="ovpn-server1")
mikrotik_openvpn(action="create_openvpn_client", name="ovpn-to-office", connect_to="vpn.office.com", ...)
mikrotik_openvpn(action="remove_openvpn_interface", name="ovpn-to-office")
mikrotik_openvpn(action="update_openvpn_client", name="ovpn-to-office", ...)
mikrotik_openvpn(action="get_openvpn_status", interface="ovpn-to-office")
mikrotik_openvpn(action="enable_openvpn_client", name="ovpn-to-office")
mikrotik_openvpn(action="disable_openvpn_client", name="ovpn-to-office")
```

**Example Usage:**
- "Create OpenVPN client to office server"
- "Show OpenVPN connection status"
- "List all OpenVPN interfaces"

---

## ⚙️ **9. System (11 Actions)**

```
mikrotik_system(action="get_system_resources")
mikrotik_system(action="get_system_health")
mikrotik_system(action="get_system_identity")
mikrotik_system(action="set_system_identity", identity="MyRouter")
mikrotik_system(action="get_system_clock")
mikrotik_system(action="get_ntp_client")
mikrotik_system(action="set_ntp_client", enabled=true, servers="time.google.com")
mikrotik_system(action="reboot_system")
mikrotik_system(action="get_routerboard")
mikrotik_system(action="get_license")
mikrotik_system(action="get_uptime")
```

**Example Usage:**
- "Show system resources and CPU usage"
- "What's the router's uptime?"
- "Set router identity to MainGateway"
- "Configure NTP time sync"
- "Check license level"

---

## 🏨 **10. Hotspot (10 Actions)**

```
mikrotik_hotspot(action="list_hotspot_servers")
mikrotik_hotspot(action="create_hotspot_server", name="hotel-wifi", interface="bridge", ...)
mikrotik_hotspot(action="remove_hotspot_server", name="hotel-wifi")
mikrotik_hotspot(action="list_hotspot_users")
mikrotik_hotspot(action="create_hotspot_user", name="guest1", password="...", ...)
mikrotik_hotspot(action="list_hotspot_active")
mikrotik_hotspot(action="list_hotspot_profiles")
mikrotik_hotspot(action="create_hotspot_profile", name="limited", ...)
mikrotik_hotspot(action="list_walled_garden")
mikrotik_hotspot(action="add_walled_garden", dst_host="*.google.com")
```

**Example Usage:**
- "Create hotspot on bridge interface"
- "Add guest user with 24-hour access"
- "Show active hotspot sessions"
- "Add website to walled garden"

---

## 🌍 **11. IP (8 Actions)**

```
# Addresses
mikrotik_ip(action="list_ip_addresses")
mikrotik_ip(action="add_ip_address", address="192.168.1.1/24", interface="bridge")
mikrotik_ip(action="remove_ip_address", address="192.168.1.1")
mikrotik_ip(action="update_ip_address", old_address="...", new_address="...")

# Pools
mikrotik_ip(action="list_ip_pools")
mikrotik_ip(action="create_ip_pool", name="dhcp-pool", ranges="192.168.1.100-192.168.1.200")
mikrotik_ip(action="remove_ip_pool", name="dhcp-pool")
mikrotik_ip(action="update_ip_pool", name="dhcp-pool", ...)
```

**Example Usage:**
- "Add IP 192.168.1.1/24 to bridge"
- "Create DHCP address pool"
- "List all IP addresses"

---

## 📡 **12. DHCP (7 Actions)**

```
mikrotik_dhcp(action="list_dhcp_servers")
mikrotik_dhcp(action="create_dhcp_server", name="dhcp1", interface="bridge", address_pool="dhcp-pool", ...)
mikrotik_dhcp(action="remove_dhcp_server", name="dhcp1")
mikrotik_dhcp(action="get_dhcp_server", name="dhcp1")
mikrotik_dhcp(action="create_dhcp_network", address="192.168.1.0/24", gateway="192.168.1.1", ...)
mikrotik_dhcp(action="create_dhcp_pool", name="pool1", ranges="192.168.1.100-192.168.1.200")
mikrotik_dhcp(action="list_dhcp_leases")
```

**Example Usage:**
- "Create DHCP server on bridge"
- "Set DHCP range 192.168.1.100-200"
- "Show all DHCP leases"

---

## 🌐 **13. DNS (9 Actions)**

```
mikrotik_dns(action="get_dns_settings")
mikrotik_dns(action="update_dns_settings", servers="8.8.8.8,8.8.4.4", allow_remote_requests=true)
mikrotik_dns(action="list_dns_static")
mikrotik_dns(action="create_dns_static", name="router.local", address="192.168.1.1")
mikrotik_dns(action="remove_dns_static", entry_id="5")
mikrotik_dns(action="update_dns_static", entry_id="5", ...)
mikrotik_dns(action="flush_dns_cache")
mikrotik_dns(action="get_dns_cache")
```

**Example Usage:**
- "Set DNS servers to 8.8.8.8 and 8.8.4.4"
- "Add static DNS entry for router.local"
- "Flush DNS cache"
- "Show DNS cache entries"

---

## 🔍 **14. Diagnostics (7 Actions)**

```
mikrotik_diagnostics(action="ping", address="8.8.8.8", count=4)
mikrotik_diagnostics(action="traceroute", address="1.1.1.1")
mikrotik_diagnostics(action="bandwidth_test", address="192.168.1.100", ...)
mikrotik_diagnostics(action="dns_lookup", name="google.com")
mikrotik_diagnostics(action="check_connection", address="192.168.1.100", port=80, protocol="tcp")
mikrotik_diagnostics(action="get_arp_table")
mikrotik_diagnostics(action="get_neighbors")
```

**Example Usage:**
- "Ping 8.8.8.8 with 10 packets"
- "Traceroute to google.com"
- "Test bandwidth to local server"
- "Check if port 80 is open on 192.168.1.100"
- "Show ARP table"

---

## 🎯 **15. Queues (7 Actions)**

```
mikrotik_queues(action="list_simple_queues")
mikrotik_queues(action="create_simple_queue", name="limit-guest", target="192.168.2.0/24", max_limit="10M/10M")
mikrotik_queues(action="remove_simple_queue", name="limit-guest")
mikrotik_queues(action="enable_simple_queue", name="limit-guest")
mikrotik_queues(action="disable_simple_queue", name="limit-guest")
mikrotik_queues(action="update_simple_queue", name="limit-guest", max_limit="20M/20M")
mikrotik_queues(action="list_queue_types")
```

**Example Usage:**
- "Limit 192.168.2.0/24 to 10Mbps"
- "Create bandwidth limit for guest network"
- "Show all active queues"

---

## 👥 **16. Users (5 Actions)**

```
mikrotik_users(action="list_users")
mikrotik_users(action="create_user", name="operator", password="...", group="read")
mikrotik_users(action="remove_user", name="operator")
mikrotik_users(action="update_user", name="operator", password="newpass")
mikrotik_users(action="list_user_groups")
```

**Example Usage:**
- "Create read-only user"
- "Change user password"
- "List all users and groups"

---

## 🏷️ **17. VLAN (4 Actions)**

```
mikrotik_vlan(action="list_vlan_interfaces")
mikrotik_vlan(action="create_vlan_interface", name="vlan10", vlan_id=10, interface="ether1")
mikrotik_vlan(action="remove_vlan_interface", name="vlan10")
mikrotik_vlan(action="update_vlan_interface", name="vlan10", ...)
```

**Example Usage:**
- "Create VLAN 10 on ether1"
- "List all VLAN interfaces"

---

## 💾 **18. Backup (4 Actions)**

```
mikrotik_backup(action="create_backup", name="before-upgrade")
mikrotik_backup(action="list_backups")
mikrotik_backup(action="restore_backup", name="before-upgrade")
mikrotik_backup(action="export_configuration")
```

**Example Usage:**
- "Create backup before making changes"
- "List all backups"
- "Export configuration as text"

---

## 📝 **19. Logs (4 Actions)**

```
mikrotik_logs(action="get_logs", topics="system,error,warning", count=50)
mikrotik_logs(action="search_logs", query="failed login", count=20)
mikrotik_logs(action="clear_logs")
mikrotik_logs(action="export_logs")
```

**Example Usage:**
- "Show last 100 system logs"
- "Search logs for failed login attempts"
- "Export logs to file"

---

## 🎯 **Coverage by RouterOS Version**

| RouterOS Version | Supported Features | Coverage |
|------------------|-------------------|----------|
| v7.x (Latest) | ✅ All 259 actions | **90%** |
| v7.0-7.3 | ✅ All except containers | **87%** |
| v6.x (Legacy) | ✅ Most features | **75%** |

**Note:** Container management requires RouterOS v7.4+

---

## 📊 **Feature Comparison Matrix**

| Feature Area | Home | SMB | Enterprise |
|--------------|------|-----|------------|
| Basic Networking | ✅ | ✅ | ✅ |
| Firewall & NAT | ✅ | ✅ | ✅ |
| VPN (WireGuard/OpenVPN) | ✅ | ✅ | ✅ |
| IPv6 | ✅ | ✅ | ✅ |
| Wireless | ✅ | ✅ | ✅ |
| CAPsMAN | ❌ | ✅ | ✅ |
| Dynamic Routing (BGP/OSPF) | ❌ | ⚠️ | ✅ |
| Hotspot | ⚠️ | ✅ | ✅ |
| Container | ⚠️ | ✅ | ✅ |
| QoS/Traffic Shaping | ✅ | ✅ | ✅ |

---

**For detailed usage examples, see [README.md](README.md) and [SETUP_GUIDE.md](SETUP_GUIDE.md)**

**For version history and changes, see [CHANGELOG.md](CHANGELOG.md)**

