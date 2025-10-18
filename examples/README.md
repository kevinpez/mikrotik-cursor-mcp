# MikroTik MCP Configuration Examples

This directory contains example configurations for the MikroTik Cursor MCP server.

## Quick Start

1. Choose the appropriate example configuration for your setup
2. Copy it to your Cursor MCP configuration location
3. Update with your actual router credentials and paths
4. Restart Cursor IDE

---

## Configuration Files

### `mcp-config.json.example`
Basic MCP server configuration for Cursor IDE. Includes:
- Connection settings (host, username, password)
- Dry-run mode for safe testing
- Standard configuration

### `mcp-config-secure.json.example`
Advanced configuration with SSH key authentication:
- SSH key-based authentication
- Strict host key checking
- Production security settings

### `cursor-settings.json.example`
Recommended Cursor IDE settings for MikroTik MCP:
- MCP server integration
- Optimal AI model settings
- Workspace configuration

---

## Configuration Locations

### Windows
```
%APPDATA%\Cursor\User\globalStorage\cursor.mcp\mcp.json
```

### macOS
```
~/Library/Application Support/Cursor/User/globalStorage/cursor.mcp/mcp.json
```

### Linux
```
~/.config/Cursor/User/globalStorage/cursor.mcp/mcp.json
```

---

## Environment Variables

All sensitive values can be set via environment variables instead of hardcoding:

- `MIKROTIK_HOST` - Router IP address or hostname
- `MIKROTIK_USERNAME` - Router username
- `MIKROTIK_PASSWORD` - Router password
- `MIKROTIK_PORT` - SSH port (default: 22)
- `MIKROTIK_SSH_KEY` - Path to SSH private key
- `MIKROTIK_DRY_RUN` - Enable dry-run mode (true/false)

---

## Security Best Practices

1. **Never commit credentials** to version control
2. **Use SSH keys** instead of passwords when possible
3. **Enable dry-run mode** initially to test safely
4. **Restrict router access** with firewall rules
5. **Use dedicated user** with appropriate permissions
6. **Rotate credentials** regularly

---

## Need Help?

- See `docs/setup/SETUP_COMPLETE_GUIDE.md` for detailed setup instructions
- Check `docs/guides/` for usage guides
- Review `SECURITY.md` for security recommendations

