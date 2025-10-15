"""
Workflow tool definitions for high-level automation tasks.
"""
from typing import Dict, Any, List, Callable
from ..scope.workflows import (
    mikrotik_setup_vpn_client,
    mikrotik_get_vpn_status
)
from mcp.types import Tool


def get_workflow_tools() -> List[Tool]:
    """Return the list of workflow automation tools."""
    return [
        Tool(
            name="mikrotik_setup_vpn_client",
            description="Complete VPN client setup in one command (creates interface, adds IP, configures peer, tests)",
            inputSchema={
                "type": "object",
                "properties": {
                    "vpn_name": {
                        "type": "string",
                        "description": "Name for the WireGuard interface (e.g., 'wireguard-aws')"
                    },
                    "local_vpn_ip": {
                        "type": "string",
                        "description": "This router's VPN IP with CIDR (e.g., '10.13.13.2/24')"
                    },
                    "remote_vpn_ip": {
                        "type": "string",
                        "description": "Remote server's VPN IP (e.g., '10.13.13.1')"
                    },
                    "remote_endpoint": {
                        "type": "string",
                        "description": "Remote server's public IP or hostname"
                    },
                    "remote_endpoint_port": {
                        "type": "integer",
                        "description": "Remote server's WireGuard port (usually 51820)"
                    },
                    "remote_public_key": {
                        "type": "string",
                        "description": "Remote server's WireGuard public key (base64)"
                    },
                    "local_private_key": {
                        "type": "string",
                        "description": "This router's WireGuard private key (base64)"
                    },
                    "preshared_key": {
                        "type": "string",
                        "description": "Optional preshared key for additional security"
                    },
                    "persistent_keepalive": {
                        "type": "string",
                        "description": "Keepalive interval (default: '25s')"
                    },
                    "mtu": {
                        "type": "integer",
                        "description": "MTU size (default: 1420)"
                    }
                },
                "required": [
                    "vpn_name", "local_vpn_ip", "remote_vpn_ip",
                    "remote_endpoint", "remote_endpoint_port",
                    "remote_public_key", "local_private_key"
                ]
            },
        ),
        Tool(
            name="mikrotik_get_vpn_status",
            description="Get comprehensive VPN status (interface, IP, peer, connectivity)",
            inputSchema={
                "type": "object",
                "properties": {
                    "interface": {
                        "type": "string",
                        "description": "WireGuard interface name"
                    }
                },
                "required": ["interface"]
            },
        ),
    ]


def get_workflow_handlers() -> Dict[str, Callable]:
    """Return the handlers for workflow automation tools."""
    return {
        "mikrotik_setup_vpn_client": lambda args: mikrotik_setup_vpn_client(
            args["vpn_name"],
            args["local_vpn_ip"],
            args["remote_vpn_ip"],
            args["remote_endpoint"],
            args["remote_endpoint_port"],
            args["remote_public_key"],
            args["local_private_key"],
            args.get("preshared_key"),
            args.get("persistent_keepalive", "25s"),
            args.get("mtu", 1420)
        ),
        "mikrotik_get_vpn_status": lambda args: mikrotik_get_vpn_status(
            args["interface"]
        ),
    }

