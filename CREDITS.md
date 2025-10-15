# Credits & Attribution

## 🙏 **Original Author**

This project is a fork and enhancement of the **MikroTik MCP Server** created by:

**Jeff Nasseri** ([@jeff-nasseri](https://github.com/jeff-nasseri))
- **Original Repository:** https://github.com/jeff-nasseri/mikrotik-mcp
- **Contribution:** Created the entire foundational MCP server for MikroTik RouterOS
- **Lines of Code:** ~5,000 lines (original implementation)
- **Scope Implementations:** All business logic in `scope/` directory
- **Tool Definitions:** All original tool definitions in `tools/` directory

### Original Project Features

Jeff Nasseri's original project provided:
- ✅ Complete MikroTik RouterOS SSH connectivity
- ✅ 100+ MCP tools for MikroTik management
- ✅ Comprehensive firewall management
- ✅ DHCP, DNS, routing, and VLAN support
- ✅ User management and backup functionality
- ✅ Wireless interface management
- ✅ System logging capabilities

**This project would not exist without Jeff's excellent foundational work!** 🌟

---

## 🔧 **Fork Enhancements**

**Kevin Pez** ([@kevinpez](https://github.com/kevinpez))
- **GitHub:** https://github.com/kevinpez
- **Repository:** https://github.com/kevinpez/mikrotik-cursor-mcp
- **Email:** kevinpez@users.noreply.github.com
- **Role:** Fork Maintainer & Enhancement Developer
- **Lines of Code:** ~1,500 lines (nested architecture + new features)
- **Contributions:**
  - **Architecture:** Nested tool architecture (100+ tools → 19 categories)
  - **Performance:** Connection pooling and optimization
  - **Features:** WireGuard, OpenVPN, IPv6, Containers, BGP, OSPF
  - **Coverage:** Expanded from 65% to 90% RouterOS coverage
  - **Actions:** Increased from 109 to 259 actions
  - **Documentation:** Comprehensive guides and examples
  - **Reliability:** Improved error handling and connection management

### Fork Objectives

This fork was created to:
1. **Solve tool count limitations** in Cursor (80-tool recommended limit)
2. **Improve performance** with faster loading times
3. **Maintain backward compatibility** with original version
4. **Enhance usability** through logical categorization
5. **Fix bugs** in route removal functionality

---

## 🎯 **How This Fork Relates to the Original**

### What We Kept (100%)
- ✅ All business logic from `scope/` directory
- ✅ All tool handlers from `tools/` directory
- ✅ SSH connectivity implementation
- ✅ Configuration management
- ✅ Logging infrastructure
- ✅ All original functionality

### What We Added
- ⭐ `serve.py` - Category-based server architecture
- ⭐ `server.py` - Unified entry point
- ⭐ Consolidated documentation in main README.md
- ⭐ Improved route removal logic

### What We Changed
- 🔧 Tool registration method (nested vs flat)
- 🔧 Server initialization (10 tools vs 100+)
- 🔧 Route removal to support CIDR lookups

---

## 📜 **License**

This fork maintains the same license as the original project. See [LICENSE](LICENSE) for details.

All credit for the original implementation belongs to Jeff Nasseri. This fork builds upon that excellent foundation.

---

## 🤝 **Collaboration**

### Upstream Sync

To stay in sync with the original project:

```bash
# Fetch upstream changes
git fetch upstream

# Merge upstream changes into your branch
git merge upstream/master
```

### Contributing Back

If you create features that would benefit the original project:
1. Submit a PR to the upstream repository
2. Share improvements with the community
3. Help improve both projects

---

## 🌟 **Thank You**

Special thanks to:

- **Jeff Nasseri** - For creating the original MikroTik MCP server
- **MCP Protocol Team** - For the Model Context Protocol
- **MikroTik** - For RouterOS and excellent documentation
- **Python Community** - For the libraries that make this possible

---

**If you use this project, please consider:**
- ⭐ Starring both this repo AND the [original repo](https://github.com/jeff-nasseri/mikrotik-mcp)
- 🐛 Reporting issues to help improve both projects
- 🤝 Contributing improvements back to the community

---

*This credits file will be updated as more contributors join the project.*
