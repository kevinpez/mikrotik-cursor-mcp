from typing import Dict, Any, List, Callable
from ..scope.system import (
    mikrotik_get_system_resources, mikrotik_get_system_health, mikrotik_get_system_identity,
    mikrotik_set_system_identity, mikrotik_get_system_clock, mikrotik_get_ntp_client,
    mikrotik_set_ntp_client, mikrotik_reboot_system, mikrotik_get_routerboard,
    mikrotik_get_license, mikrotik_get_uptime
)
from mcp.types import Tool

def get_system_tools() -> List[Tool]:
    """Return the list of system management tools."""
    return [
        Tool(
            name="mikrotik_get_system_resources",
            description="Gets system resource usage (CPU, RAM, disk, uptime)",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        Tool(
            name="mikrotik_get_system_health",
            description="Gets system health (temperature, voltage, fans)",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        Tool(
            name="mikrotik_get_system_identity",
            description="Gets system identity/name",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        Tool(
            name="mikrotik_set_system_identity",
            description="Sets system identity/name",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"}
                },
                "required": ["name"]
            },
        ),
        Tool(
            name="mikrotik_get_system_clock",
            description="Gets system clock settings",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        Tool(
            name="mikrotik_get_ntp_client",
            description="Gets NTP client configuration",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        Tool(
            name="mikrotik_set_ntp_client",
            description="Configures NTP client for time synchronization",
            inputSchema={
                "type": "object",
                "properties": {
                    "enabled": {"type": "boolean"},
                    "servers": {"type": "string"},
                    "mode": {"type": "string", "enum": ["unicast", "broadcast", "multicast"]}
                },
                "required": []
            },
        ),
        Tool(
            name="mikrotik_reboot_system",
            description="Reboots the MikroTik device (requires confirmation)",
            inputSchema={
                "type": "object",
                "properties": {
                    "confirm": {"type": "boolean"}
                },
                "required": ["confirm"]
            },
        ),
        Tool(
            name="mikrotik_get_routerboard",
            description="Gets RouterBOARD hardware information",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        Tool(
            name="mikrotik_get_license",
            description="Gets RouterOS license information",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        Tool(
            name="mikrotik_get_uptime",
            description="Gets system uptime",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
    ]

def get_system_handlers() -> Dict[str, Callable]:
    """Return the handlers for system management tools."""
    return {
        "mikrotik_get_system_resources": lambda args: mikrotik_get_system_resources(),
        "mikrotik_get_system_health": lambda args: mikrotik_get_system_health(),
        "mikrotik_get_system_identity": lambda args: mikrotik_get_system_identity(),
        "mikrotik_set_system_identity": lambda args: mikrotik_set_system_identity(
            args["name"]
        ),
        "mikrotik_get_system_clock": lambda args: mikrotik_get_system_clock(),
        "mikrotik_get_ntp_client": lambda args: mikrotik_get_ntp_client(),
        "mikrotik_set_ntp_client": lambda args: mikrotik_set_ntp_client(
            args.get("enabled", True),
            args.get("servers"),
            args.get("mode")
        ),
        "mikrotik_reboot_system": lambda args: mikrotik_reboot_system(
            args.get("confirm", False)
        ),
        "mikrotik_get_routerboard": lambda args: mikrotik_get_routerboard(),
        "mikrotik_get_license": lambda args: mikrotik_get_license(),
        "mikrotik_get_uptime": lambda args: mikrotik_get_uptime(),
    }

