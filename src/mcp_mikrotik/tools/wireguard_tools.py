"""
WireGuard VPN tool definitions and handlers for MCP server.
"""
from typing import Dict, Any, List, Callable
from ..scope.wireguard import (
    mikrotik_list_wireguard_interfaces, mikrotik_create_wireguard_interface,
    mikrotik_remove_wireguard_interface, mikrotik_update_wireguard_interface,
    mikrotik_get_wireguard_interface, mikrotik_list_wireguard_peers,
    mikrotik_add_wireguard_peer, mikrotik_remove_wireguard_peer,
    mikrotik_update_wireguard_peer, mikrotik_enable_wireguard_interface,
    mikrotik_disable_wireguard_interface
)
from mcp.types import Tool


def get_wireguard_tools() -> List[Tool]:
    """Return the list of WireGuard management tools."""
    return [
        Tool(
            name="mikrotik_list_wireguard_interfaces",
            description="Lists all WireGuard interfaces",
            inputSchema={
                "type": "object",
                "properties": {
                    "name_filter": {
                        "type": "string",
                        "description": "Filter by interface name (supports wildcards)"
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
            name="mikrotik_create_wireguard_interface",
            description="Creates a new WireGuard interface",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Interface name (e.g., 'wireguard-aws')"
                    },
                    "listen_port": {
                        "type": "integer",
                        "description": "UDP port to listen on (default: 51820)"
                    },
                    "private_key": {
                        "type": "string",
                        "description": "Base64-encoded private key (RouterOS generates one if not provided)"
                    },
                    "mtu": {
                        "type": "integer",
                        "description": "MTU size (default: 1420)"
                    },
                    "comment": {
                        "type": "string",
                        "description": "Optional comment"
                    }
                },
                "required": ["name"]
            },
        ),
        Tool(
            name="mikrotik_remove_wireguard_interface",
            description="Removes a WireGuard interface",
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
            name="mikrotik_update_wireguard_interface",
            description="Updates WireGuard interface settings",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Interface name"
                    },
                    "listen_port": {
                        "type": "integer",
                        "description": "New UDP listen port"
                    },
                    "mtu": {
                        "type": "integer",
                        "description": "New MTU size"
                    },
                    "private_key": {
                        "type": "string",
                        "description": "New private key"
                    },
                    "disabled": {
                        "type": "boolean",
                        "description": "Enable/disable the interface"
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
            name="mikrotik_get_wireguard_interface",
            description="Gets detailed information about a WireGuard interface",
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
            name="mikrotik_enable_wireguard_interface",
            description="Enables a WireGuard interface",
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
            name="mikrotik_disable_wireguard_interface",
            description="Disables a WireGuard interface",
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
        Tool(
            name="mikrotik_list_wireguard_peers",
            description="Lists WireGuard peers",
            inputSchema={
                "type": "object",
                "properties": {
                    "interface": {
                        "type": "string",
                        "description": "Filter by interface name"
                    },
                    "endpoint_filter": {
                        "type": "string",
                        "description": "Filter by endpoint address"
                    }
                },
                "required": []
            },
        ),
        Tool(
            name="mikrotik_add_wireguard_peer",
            description="Adds a WireGuard peer to an interface",
            inputSchema={
                "type": "object",
                "properties": {
                    "interface": {
                        "type": "string",
                        "description": "WireGuard interface name"
                    },
                    "public_key": {
                        "type": "string",
                        "description": "Base64-encoded public key of the peer"
                    },
                    "endpoint_address": {
                        "type": "string",
                        "description": "Peer's IP address or hostname"
                    },
                    "endpoint_port": {
                        "type": "integer",
                        "description": "Peer's UDP port"
                    },
                    "allowed_address": {
                        "type": "string",
                        "description": "Allowed IP addresses (CIDR notation, e.g., '10.13.13.1/32')"
                    },
                    "preshared_key": {
                        "type": "string",
                        "description": "Optional preshared key for additional security"
                    },
                    "persistent_keepalive": {
                        "type": "string",
                        "description": "Keepalive interval (e.g., '25s', '30s')"
                    },
                    "comment": {
                        "type": "string",
                        "description": "Optional comment"
                    }
                },
                "required": ["interface", "public_key"]
            },
        ),
        Tool(
            name="mikrotik_remove_wireguard_peer",
            description="Removes a WireGuard peer",
            inputSchema={
                "type": "object",
                "properties": {
                    "interface": {
                        "type": "string",
                        "description": "WireGuard interface name"
                    },
                    "public_key": {
                        "type": "string",
                        "description": "Public key of the peer to remove"
                    },
                    "peer_id": {
                        "type": "string",
                        "description": "Peer ID number (alternative to public_key)"
                    }
                },
                "required": ["interface"]
            },
        ),
        Tool(
            name="mikrotik_update_wireguard_peer",
            description="Updates WireGuard peer settings",
            inputSchema={
                "type": "object",
                "properties": {
                    "interface": {
                        "type": "string",
                        "description": "WireGuard interface name"
                    },
                    "public_key": {
                        "type": "string",
                        "description": "Public key of the peer to update"
                    },
                    "endpoint_address": {
                        "type": "string",
                        "description": "New endpoint address"
                    },
                    "endpoint_port": {
                        "type": "integer",
                        "description": "New endpoint port"
                    },
                    "allowed_address": {
                        "type": "string",
                        "description": "New allowed addresses"
                    },
                    "preshared_key": {
                        "type": "string",
                        "description": "New preshared key"
                    },
                    "persistent_keepalive": {
                        "type": "string",
                        "description": "New keepalive interval"
                    },
                    "disabled": {
                        "type": "boolean",
                        "description": "Enable/disable the peer"
                    },
                    "comment": {
                        "type": "string",
                        "description": "Update comment"
                    }
                },
                "required": ["interface", "public_key"]
            },
        ),
    ]


def get_wireguard_handlers() -> Dict[str, Callable]:
    """Return the handlers for WireGuard management tools."""
    return {
        "mikrotik_list_wireguard_interfaces": lambda args: mikrotik_list_wireguard_interfaces(
            args.get("name_filter"),
            args.get("disabled_only", False)
        ),
        "mikrotik_create_wireguard_interface": lambda args: mikrotik_create_wireguard_interface(
            args["name"],
            args.get("listen_port", 51820),
            args.get("private_key"),
            args.get("mtu", 1420),
            args.get("comment")
        ),
        "mikrotik_remove_wireguard_interface": lambda args: mikrotik_remove_wireguard_interface(
            args["name"]
        ),
        "mikrotik_update_wireguard_interface": lambda args: mikrotik_update_wireguard_interface(
            args["name"],
            args.get("listen_port"),
            args.get("mtu"),
            args.get("private_key"),
            args.get("disabled"),
            args.get("comment")
        ),
        "mikrotik_get_wireguard_interface": lambda args: mikrotik_get_wireguard_interface(
            args["name"]
        ),
        "mikrotik_enable_wireguard_interface": lambda args: mikrotik_enable_wireguard_interface(
            args["name"]
        ),
        "mikrotik_disable_wireguard_interface": lambda args: mikrotik_disable_wireguard_interface(
            args["name"]
        ),
        "mikrotik_list_wireguard_peers": lambda args: mikrotik_list_wireguard_peers(
            args.get("interface"),
            args.get("endpoint_filter")
        ),
        "mikrotik_add_wireguard_peer": lambda args: mikrotik_add_wireguard_peer(
            args["interface"],
            args["public_key"],
            args.get("endpoint_address"),
            args.get("endpoint_port"),
            args.get("allowed_address"),
            args.get("preshared_key"),
            args.get("persistent_keepalive"),
            args.get("comment")
        ),
        "mikrotik_remove_wireguard_peer": lambda args: mikrotik_remove_wireguard_peer(
            args["interface"],
            args.get("public_key"),
            args.get("peer_id")
        ),
        "mikrotik_update_wireguard_peer": lambda args: mikrotik_update_wireguard_peer(
            args["interface"],
            args["public_key"],
            args.get("endpoint_address"),
            args.get("endpoint_port"),
            args.get("allowed_address"),
            args.get("preshared_key"),
            args.get("persistent_keepalive"),
            args.get("disabled"),
            args.get("comment")
        ),
    }

