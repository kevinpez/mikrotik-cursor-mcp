# Changelog

All notable changes to the MikroTik Cursor MCP project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [4.8.1] - 2025-01-15

### Added - Production-Ready Features

#### 🔒 **Universal Dry-Run/Plan Mode**
- **Dry-run system** with exact RouterOS diffs before applying changes
- **Safety levels** (Safe, Low Risk, Medium Risk, High Risk, Critical)
- **Plan mode** for complex multi-operation changes
- **Diff visualization** showing current vs proposed state
- **Warning system** with operation-specific safety alerts
- **Confirmation requirements** for high-risk operations

#### 📊 **Enhanced Observability**
- **Structured JSON logging** with request IDs and timing
- **Prometheus metrics** for production monitoring
- **Request context tracking** across operations
- **Performance metrics** (operation duration, success rates)
- **Safety event logging** for audit trails
- **RouterOS command tracking** with timing and success rates

#### 🏢 **Multi-Site Scaling**
- **Circuit breakers** for per-device failure isolation
- **Rate limiting** with token bucket algorithm
- **Concurrent operation controls** with thread pools
- **Automatic retry logic** with exponential backoff
- **Health monitoring** across all sites
- **Bulk operations** with failure isolation
- **Site status tracking** with error rates and response times

#### 🛡️ **Security Enhancements**
- **Comprehensive security guide** (SECURITY.md)
- **Least-privilege RouterOS group** documentation
- **SSH key management** best practices
- **Credential protection** guidelines
- **Network security** recommendations
- **Audit logging** procedures
- **Incident response** procedures

#### 🧪 **Testing Infrastructure**
- **CHR integration testing** with Cloud Hosted Router
- **Container-based testing** with Docker RouterOS
- **Golden file testing** for configuration comparison
- **Performance testing** with load and stress tests
- **Security testing** with authentication validation
- **Comprehensive Makefile** with test targets
- **CI/CD pipeline** with GitHub Actions

#### 📦 **Distribution & Packaging**
- **Tagged releases** with automated changelog generation
- **Docker container** with multi-stage builds
- **PyPI packaging** with proper metadata
- **GitHub Container Registry** integration
- **Multi-architecture support** (production, development, multi-site)
- **Health checks** and monitoring integration

#### 🎯 **Cursor/MCP Ergonomics**
- **Ready-to-use mcp-config.json** with all options
- **Natural language examples** with 50+ command patterns
- **Quick start guide** for 5-minute setup
- **Comprehensive documentation** with troubleshooting
- **Example conversations** for common use cases
- **Safety command examples** with dry-run usage

### Enhanced

#### 🔧 **Core System**
- **Enhanced logging** with structured JSON output
- **Improved error handling** with detailed error messages
- **Better connection management** with health checks
- **Optimized performance** with connection pooling
- **Enhanced security** with credential protection

#### 📚 **Documentation**
- **Comprehensive README** with feature overview
- **Quick start guide** for rapid deployment
- **Natural language examples** for easy adoption
- **Security guide** for production deployment
- **Testing guide** with CHR and container support
- **API documentation** with all 382 actions

#### 🏗️ **Architecture**
- **Modular design** with clear separation of concerns
- **Plugin architecture** for easy extension
- **Configuration management** with environment variables
- **Error recovery** with automatic retry mechanisms
- **Resource management** with proper cleanup

### Fixed

#### 🐛 **Bug Fixes**
- **Connection timeout** handling improvements
- **SSH key authentication** reliability fixes
- **Memory leak** prevention in long-running operations
- **Error message** clarity improvements
- **Configuration validation** enhancements

#### 🔧 **Stability**
- **Thread safety** improvements in concurrent operations
- **Resource cleanup** on connection failures
- **Error propagation** fixes in multi-site operations
- **Timeout handling** for slow operations
- **Graceful shutdown** procedures

### Security

#### 🔒 **Security Improvements**
- **Credential masking** in logs and output
- **SSH key validation** before connection attempts
- **Input sanitization** for RouterOS commands
- **Permission validation** for user operations
- **Audit trail** for all configuration changes

## [4.8.0] - 2024-12-01

### Added
- **DHCPv6 Relay** (2 actions)
- **OSPF Authentication** (2 actions)
- **99% RouterOS Coverage** achieved
- **382 Total Actions** across 19 categories

### Enhanced
- **BGP peer management** with authentication
- **OSPF area configuration** with security
- **IPv6 routing** with advanced features
- **Container management** for RouterOS v7.x

## [4.7.0] - 2024-11-15

### Added
- **Layer 7 Protocols** (10 actions)
- **Certificate & PKI** (11 actions)
- **VRRP High Availability** (12 actions)
- **Queue Trees & PCQ** (13 actions)
- **Advanced Bridge Features** (14 actions)
- **98% RouterOS Coverage**
- **378 Total Actions**

### Enhanced
- **Deep packet inspection** capabilities
- **SSL/TLS certificate** management
- **High availability** configurations
- **Advanced QoS** with traffic shaping
- **Bridge management** with VLAN support

## [4.0.0] - 2024-10-01

### Added
- **IPv6 Support** (39 actions)
- **Container Management** (18 actions)
- **90% RouterOS Coverage**
- **259 Total Actions**

### Enhanced
- **Dual-stack networking** support
- **Docker integration** for RouterOS v7.x
- **IPv6 firewall** and routing
- **Container networking** with veth interfaces

## [3.5.0] - 2024-09-01

### Added
- **Advanced Wireless** (17 actions)
- **CAPsMAN Support** (17 actions)
- **88% Coverage**

### Enhanced
- **Centralized wireless** management
- **Security profiles** for wireless
- **Access list** management
- **Wireless monitoring** capabilities

## [3.0.0] - 2024-08-01

### Added
- **BGP Support** (8 actions)
- **OSPF Support** (7 actions)
- **Route Filtering**
- **85% Coverage**

### Enhanced
- **Dynamic routing** protocols
- **Route policy** management
- **BGP peer** configuration
- **OSPF area** setup

## [2.6.0] - 2024-07-01

### Added
- **Hotspot Management** (10 actions)

### Enhanced
- **Captive portal** configuration
- **User management** for hotspots
- **Walled garden** setup
- **Hotspot monitoring**

## [2.5.0] - 2024-06-01

### Added
- **PPPoE Support**
- **Tunnel Management** (EoIP, GRE)
- **Link Bonding**

### Enhanced
- **WAN connectivity** options
- **Site-to-site** tunneling
- **Link aggregation** support

## [2.4.0] - 2024-05-01

### Added
- **Advanced Firewall** (mangle, RAW)
- **Connection Tracking**

### Enhanced
- **Packet marking** capabilities
- **Pre-connection** filtering
- **Connection state** monitoring

## [2.3.0] - 2024-04-01

### Added
- **OpenVPN Support** (9 actions)

### Enhanced
- **VPN client** configuration
- **Certificate** management
- **Tunnel monitoring**

## [2.1.0] - 2024-03-01

### Added
- **WireGuard Support** (11 actions)

### Enhanced
- **Modern VPN** protocol support
- **Key management** automation
- **Tunnel configuration**

## [1.0.0] - 2024-02-01

### Added
- **Initial Release**
- **Basic RouterOS Functions**
- **MCP Integration**
- **Cursor IDE Support**

---

## Migration Guide

### Upgrading to 4.8.1

#### New Configuration Options
Add these environment variables to your `mcp.json`:

```json
{
  "env": {
    "MIKROTIK_LOG_LEVEL": "INFO",
    "MIKROTIK_LOG_FORMAT": "json",
    "MIKROTIK_DRY_RUN": "false",
    "MIKROTIK_SAFETY_MODE": "true",
    "MIKROTIK_METRICS_ENABLED": "true"
  }
}
```

#### New Dependencies
The following packages are now required:
- `pyyaml>=6.0`
- `prometheus-client>=0.19.0`

#### Breaking Changes
- **None** - This is a backward-compatible release

#### New Features to Try
1. **Dry-run mode**: Use `"Show me what this would do (dry-run)"` for any operation
2. **Multi-site management**: Set up the multi-site manager for bulk operations
3. **Enhanced monitoring**: Enable metrics for production monitoring
4. **Security improvements**: Follow the new SECURITY.md guide

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute to this project.

## Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/kevinpez/mikrotik-cursor-mcp/issues)
- **GitHub Discussions**: [Ask questions or share use cases](https://github.com/kevinpez/mikrotik-cursor-mcp/discussions)
- **Documentation**: See [README.md](README.md) for complete documentation

---

**Full Changelog**: [4.8.0...4.8.1](https://github.com/kevinpez/mikrotik-cursor-mcp/compare/v4.8.0...v4.8.1)