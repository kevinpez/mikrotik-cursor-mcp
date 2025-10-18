# OSPF Auto-Discovery MCP Usage Example

## Quick Start Guide

This guide shows how to use the OSPF auto-discovery functionality through the MCP interface.

## Step 1: Check Current Status

First, let's see what OSPF configuration currently exists:

```json
{
  "tool": "mikrotik_get_ospf_auto_discovery_status",
  "parameters": {}
}
```

## Step 2: Scan for MikroTik Neighbors

Discover MikroTik devices on your network:

```json
{
  "tool": "mikrotik_scan_mikrotik_neighbors",
  "parameters": {}
}
```

## Step 3: Assign OSPF Subnet for a New Site

Assign a unique subnet and Router ID for a new site:

```json
{
  "tool": "mikrotik_auto_assign_ospf_subnet",
  "parameters": {
    "site_id": "home-main",
    "base_subnet": "192.168.100.0/24"
  }
}
```

## Step 4: Complete Auto-Discovery Configuration

Run the complete auto-discovery for a site:

```json
{
  "tool": "mikrotik_auto_discovery_ospf_complete",
  "parameters": {
    "site_id": "home-main",
    "management_interface": "ether1",
    "instance_name": "auto-ospf",
    "area_name": "backbone"
  }
}
```

## Step 5: Verify Configuration

Check that everything is configured correctly:

```json
{
  "tool": "mikrotik_get_ospf_auto_discovery_status",
  "parameters": {}
}
```

## Step 6: Check Assignments

View all OSPF assignments:

```json
{
  "tool": "mikrotik_get_ospf_assignments",
  "parameters": {}
}
```

## Individual Configuration Steps

If you prefer to configure OSPF step by step:

### 1. Create OSPF Instance

```json
{
  "tool": "mikrotik_auto_configure_ospf_instance",
  "parameters": {
    "instance_name": "auto-ospf",
    "router_id": "100.100.100.100",
    "comment": "Auto-OSPF Instance for home-main"
  }
}
```

### 2. Create OSPF Area

```json
{
  "tool": "mikrotik_auto_configure_ospf_area",
  "parameters": {
    "area_name": "backbone",
    "instance_name": "auto-ospf",
    "area_id": "0.0.0.0",
    "comment": "Backbone Area"
  }
}
```

### 3. Configure OSPF Networks

```json
{
  "tool": "mikrotik_auto_configure_ospf_networks",
  "parameters": {
    "subnet": "192.168.100.0/24",
    "router_id": "100.100.100.100",
    "area_name": "backbone",
    "instance_name": "auto-ospf"
  }
}
```

### 4. Configure OSPF Interfaces

```json
{
  "tool": "mikrotik_auto_configure_ospf_interfaces",
  "parameters": {
    "management_interface": "ether1",
    "area_name": "backbone",
    "instance_name": "auto-ospf"
  }
}
```

### 5. Enable OSPF Instance

```json
{
  "tool": "mikrotik_enable_ospf_instance",
  "parameters": {
    "instance_name": "auto-ospf"
  }
}
```

## Monitoring Commands

### Check OSPF Neighbors

```json
{
  "tool": "mikrotik_list_ospf_neighbors",
  "parameters": {}
}
```

### Check OSPF Routes

```json
{
  "tool": "mikrotik_list_ospf_routes",
  "parameters": {}
}
```

### Check OSPF Status

```json
{
  "tool": "mikrotik_get_ospf_status",
  "parameters": {
    "instance": "auto-ospf"
  }
}
```

## Multi-Site Configuration

To configure multiple sites, repeat the process for each site:

```json
{
  "tool": "mikrotik_auto_discovery_ospf_complete",
  "parameters": {
    "site_id": "site-002",
    "management_interface": "ether1"
  }
}
```

```json
{
  "tool": "mikrotik_auto_discovery_ospf_complete",
  "parameters": {
    "site_id": "site-003",
    "management_interface": "ether1"
  }
}
```

## Expected Results

After running the auto-discovery, you should see:

1. **OSPF Instances**: Each site has an `auto-ospf` instance
2. **OSPF Areas**: Each site has a `backbone` area
3. **OSPF Networks**: Local subnets and Router IDs are advertised
4. **OSPF Interfaces**: Management, bridge, and loopback interfaces configured
5. **OSPF Neighbors**: Neighbors discovered and established
6. **OSPF Routes**: Routes learned from other OSPF routers

## Troubleshooting

If OSPF neighbors are not establishing:

1. Check network connectivity between routers
2. Verify OSPF interfaces are configured correctly
3. Ensure OSPF instances are enabled
4. Check firewall rules that might block OSPF traffic

Use the status commands to diagnose issues:

```json
{
  "tool": "mikrotik_get_ospf_auto_discovery_status",
  "parameters": {}
}
```

This will show you the complete OSPF configuration and help identify any issues.
