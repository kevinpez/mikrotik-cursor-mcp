# MikroTik Network Topology Design
## Multi-Site OSPF Network Configuration

### Network Overview
- **Main Network:** 192.168.88.0/24 (Management/Backbone)
- **OSPF Area 0:** Backbone area for inter-router communication
- **Individual Subnets:** Each router gets its own /24 subnet

### Router Subnet Allocation

| Router | IP Address | Subnet | OSPF Router ID | Area | Description |
|--------|------------|--------|----------------|------|-------------|
| home-main | 192.168.88.1 | 192.168.1.0/24 | 1.1.1.1 | 0 | Main Router (RB5009) |
| 007-rb2011 | 192.168.88.186 | 192.168.7.0/24 | 7.7.7.7 | 0 | Site 007 |
| 003-rb4011 | 192.168.88.198 | 192.168.3.0/24 | 3.3.3.3 | 0 | Site 003 |
| 002-rb4011 | 192.168.88.228 | 192.168.2.0/24 | 2.2.2.2 | 0 | Site 002 |
| 005-rb850 | 192.168.88.230 | 192.168.5.0/24 | 5.5.5.5 | 0 | Site 005 |
| sw-000-crs-328 | 192.168.88.232 | 192.168.10.0/24 | 10.10.10.10 | 0 | Switch/Infrastructure |

### Network Topology

```
                    [home-main]
                   192.168.88.1
                   192.168.1.1/24
                    Router ID: 1.1.1.1
                         |
                         |
    ┌────────────────────┼────────────────────┐
    |                    |                    |
[007-rb2011]        [003-rb4011]        [002-rb4011]
192.168.88.186      192.168.88.198      192.168.88.228
192.168.7.1/24      192.168.3.1/24      192.168.2.1/24
Router ID: 7.7.7.7  Router ID: 3.3.3.3  Router ID: 2.2.2.2
    |                    |                    |
    └────────────────────┼────────────────────┘
                         |
                    [005-rb850]
                   192.168.88.230
                   192.168.5.1/24
                    Router ID: 5.5.5.5
                         |
                         |
                    [sw-000-crs-328]
                   192.168.88.232
                   192.168.10.1/24
                    Router ID: 10.10.10.10
```

### OSPF Configuration Details

#### OSPF Instance Settings
- **Instance Name:** ospf-v2
- **Router ID:** Unique for each router (see table above)
- **Area 0:** Backbone area
- **Hello Interval:** 10 seconds
- **Dead Interval:** 40 seconds
- **Cost:** 1 for all interfaces

#### Network Advertisements
Each router will advertise:
1. **Loopback Interface:** Router ID subnet
2. **Local Subnet:** Assigned /24 subnet
3. **Management Network:** 192.168.88.0/24 (if applicable)

### Implementation Steps

1. **Configure Loopback Interfaces**
   - Create loopback interface with Router ID IP
   - Enable OSPF on loopback

2. **Configure Local Subnets**
   - Add IP addresses to bridge or main interface
   - Enable OSPF on local subnet

3. **Configure OSPF Instance**
   - Create OSPF instance with unique Router ID
   - Configure Area 0 (backbone)

4. **Configure OSPF Networks**
   - Add networks to OSPF area
   - Set appropriate costs

5. **Configure OSPF Interfaces**
   - Enable OSPF on management interface
   - Set interface parameters

### Security Considerations

- **OSPF Authentication:** MD5 authentication between neighbors
- **Interface Filtering:** Restrict OSPF to management network
- **Route Filtering:** Control which routes are advertised

### Expected Results

After configuration:
- All routers will have OSPF neighbor relationships
- Routes to all subnets will be dynamically learned
- Failover and load balancing capabilities
- Centralized routing management
