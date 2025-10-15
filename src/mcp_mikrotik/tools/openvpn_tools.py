"""
OpenVPN tool definitions and handlers for MCP server.
"""
from typing import Dict, Any, List, Callable
from ..scope.openvpn import (
    mikrotik_list_openvpn_interfaces,
    mikrotik_list_openvpn_servers,
    mikrotik_get_openvpn_server_status,
    mikrotik_create_openvpn_client,
    mikrotik_remove_openvpn_interface,
    mikrotik_update_openvpn_client,
    mikrotik_get_openvpn_status,
    mikrotik_enable_openvpn_client,
    mikrotik_disable_openvpn_client
)
from mcp.types import Tool


def get_openvpn_tools() -> List[Tool]:
    """Return the list of OpenVPN management tools."""
    return [
        Tool(
            name="mikrotik_list_openvpn_interfaces",
            description="Lists all OpenVPN client interfaces (READ-ONLY, safe)",
            inputSchema={
                "type": "object",
                "properties": {
                    "name_filter": {
                        "type": "string",
                        "description": "Filter by interface name"
                    },
                    "disabled_only": {
                        "type": "boolean",
                        "description": "Show only disabled interfaces"
                    }
                },
                "required": []
            },
        ),
        Tool(
            name="mikrotik_list_openvpn_servers",
            description="Lists OpenVPN server interfaces (READ-ONLY, safe)",
            inputSchema={
                "type": "object",
                "properties": {
                    "name_filter": {
                        "type": "string",
                        "description": "Filter by server name"
                    }
                },
                "required": []
            },
        ),
        Tool(
            name="mikrotik_get_openvpn_server_status",
            description="Get OpenVPN server status (READ-ONLY, safe)",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        Tool(
            name="mikrotik_create_openvpn_client",
            description="Creates an OpenVPN client interface",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Interface name (e.g., 'ovpn-client-aws')"
                    },
                    "connect_to": {
                        "type": "string",
                        "description": "Server IP address or hostname"
                    },
                    "port": {
                        "type": "integer",
                        "description": "OpenVPN port (default: 1194)"
                    },
                    "user": {
                        "type": "string",
                        "description": "Username for authentication"
                    },
                    "password": {
                        "type": "string",
                        "description": "Password for authentication"
                    },
                    "certificate": {
                        "type": "string",
                        "description": "Certificate name for cert-based auth"
                    },
                    "auth": {
                        "type": "string",
                        "enum": ["sha1", "sha256", "sha512"],
                        "description": "Authentication method (default: sha1)"
                    },
                    "cipher": {
                        "type": "string",
                        "enum": ["aes128", "aes192", "aes256", "blowfish128"],
                        "description": "Encryption cipher (default: aes128)"
                    },
                    "mode": {
                        "type": "string",
                        "enum": ["ip", "ethernet"],
                        "description": "Connection mode (default: ip)"
                    },
                    "comment": {
                        "type": "string",
                        "description": "Optional comment"
                    }
                },
                "required": ["name", "connect_to"]
            },
        ),
        Tool(
            name="mikrotik_remove_openvpn_interface",
            description="Removes an OpenVPN interface",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Interface name to remove"
                    }
                },
                "required": ["name"]
            },
        ),
        Tool(
            name="mikrotik_update_openvpn_client",
            description="Updates OpenVPN client settings",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Interface name"
                    },
                    "connect_to": {
                        "type": "string",
                        "description": "New server address"
                    },
                    "port": {
                        "type": "integer",
                        "description": "New port"
                    },
                    "user": {
                        "type": "string",
                        "description": "New username"
                    },
                    "password": {
                        "type": "string",
                        "description": "New password"
                    },
                    "disabled": {
                        "type": "boolean",
                        "description": "Enable/disable interface"
                    },
                    "comment": {
                        "type": "string",
                        "description": "Update comment"
                    }
                },
                "required": ["name"]
            },
        ),
        Tool(
            name="mikrotik_get_openvpn_status",
            description="Get detailed status of OpenVPN interface (READ-ONLY, safe)",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Interface name"
                    }
                },
                "required": ["name"]
            },
        ),
        Tool(
            name="mikrotik_enable_openvpn_client",
            description="Enable OpenVPN client interface (will attempt connection)",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Interface name to enable"
                    }
                },
                "required": ["name"]
            },
        ),
        Tool(
            name="mikrotik_disable_openvpn_client",
            description="Disable OpenVPN client interface (safe, just disconnects)",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Interface name to disable"
                    }
                },
                "required": ["name"]
            },
        ),
    ]


def get_openvpn_handlers() -> Dict[str, Callable]:
    """Return the handlers for OpenVPN management tools."""
    return {
        "mikrotik_list_openvpn_interfaces": lambda args: mikrotik_list_openvpn_interfaces(
            args.get("name_filter"),
            args.get("disabled_only", False)
        ),
        "mikrotik_list_openvpn_servers": lambda args: mikrotik_list_openvpn_servers(
            args.get("name_filter")
        ),
        "mikrotik_get_openvpn_server_status": lambda args: mikrotik_get_openvpn_server_status(),
        "mikrotik_create_openvpn_client": lambda args: mikrotik_create_openvpn_client(
            args["name"],
            args["connect_to"],
            args.get("port", 1194),
            args.get("user"),
            args.get("password"),
            args.get("certificate"),
            args.get("auth", "sha1"),
            args.get("cipher", "aes128"),
            args.get("mode", "ip"),
            args.get("comment")
        ),
        "mikrotik_remove_openvpn_interface": lambda args: mikrotik_remove_openvpn_interface(
            args["name"]
        ),
        "mikrotik_update_openvpn_client": lambda args: mikrotik_update_openvpn_client(
            args["name"],
            args.get("connect_to"),
            args.get("port"),
            args.get("user"),
            args.get("password"),
            args.get("disabled"),
            args.get("comment")
        ),
        "mikrotik_get_openvpn_status": lambda args: mikrotik_get_openvpn_status(
            args["name"]
        ),
        "mikrotik_enable_openvpn_client": lambda args: mikrotik_enable_openvpn_client(
            args["name"]
        ),
        "mikrotik_disable_openvpn_client": lambda args: mikrotik_disable_openvpn_client(
            args["name"]
        ),
    }

