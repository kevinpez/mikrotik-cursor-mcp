from typing import Dict, Any, List, Callable
from ..scope.interfaces import (
    mikrotik_list_interfaces, mikrotik_get_interface_stats, mikrotik_enable_interface,
    mikrotik_disable_interface, mikrotik_get_interface_monitor, mikrotik_list_bridge_ports,
    mikrotik_add_bridge_port, mikrotik_remove_bridge_port, mikrotik_get_interface_traffic
)
from mcp.types import Tool

def get_interface_tools() -> List[Tool]:
    """Return the list of interface management tools."""
    return [
        Tool(
            name="mikrotik_list_interfaces",
            description="Lists all network interfaces",
            inputSchema={
                "type": "object",
                "properties": {
                    "name_filter": {"type": "string"},
                    "type_filter": {"type": "string"},
                    "running_only": {"type": "boolean"},
                    "disabled_only": {"type": "boolean"}
                },
                "required": []
            },
        ),
        Tool(
            name="mikrotik_get_interface_stats",
            description="Gets traffic statistics for a specific interface",
            inputSchema={
                "type": "object",
                "properties": {
                    "interface_name": {"type": "string"}
                },
                "required": ["interface_name"]
            },
        ),
        Tool(
            name="mikrotik_enable_interface",
            description="Enables a network interface",
            inputSchema={
                "type": "object",
                "properties": {
                    "interface_name": {"type": "string"}
                },
                "required": ["interface_name"]
            },
        ),
        Tool(
            name="mikrotik_disable_interface",
            description="Disables a network interface",
            inputSchema={
                "type": "object",
                "properties": {
                    "interface_name": {"type": "string"}
                },
                "required": ["interface_name"]
            },
        ),
        Tool(
            name="mikrotik_get_interface_monitor",
            description="Monitor interface traffic in real-time (snapshot)",
            inputSchema={
                "type": "object",
                "properties": {
                    "interface_name": {"type": "string"}
                },
                "required": ["interface_name"]
            },
        ),
        Tool(
            name="mikrotik_list_bridge_ports",
            description="Lists bridge ports",
            inputSchema={
                "type": "object",
                "properties": {
                    "bridge_name": {"type": "string"}
                },
                "required": []
            },
        ),
        Tool(
            name="mikrotik_add_bridge_port",
            description="Adds an interface to a bridge",
            inputSchema={
                "type": "object",
                "properties": {
                    "bridge": {"type": "string"},
                    "interface": {"type": "string"}
                },
                "required": ["bridge", "interface"]
            },
        ),
        Tool(
            name="mikrotik_remove_bridge_port",
            description="Removes an interface from its bridge",
            inputSchema={
                "type": "object",
                "properties": {
                    "interface": {"type": "string"}
                },
                "required": ["interface"]
            },
        ),
        Tool(
            name="mikrotik_get_interface_traffic",
            description="Gets current traffic for an interface",
            inputSchema={
                "type": "object",
                "properties": {
                    "interface_name": {"type": "string"}
                },
                "required": ["interface_name"]
            },
        ),
    ]

def get_interface_handlers() -> Dict[str, Callable]:
    """Return the handlers for interface management tools."""
    return {
        "mikrotik_list_interfaces": lambda args: mikrotik_list_interfaces(
            args.get("name_filter"),
            args.get("type_filter"),
            args.get("running_only", False),
            args.get("disabled_only", False)
        ),
        "mikrotik_get_interface_stats": lambda args: mikrotik_get_interface_stats(
            args["interface_name"]
        ),
        "mikrotik_enable_interface": lambda args: mikrotik_enable_interface(
            args["interface_name"]
        ),
        "mikrotik_disable_interface": lambda args: mikrotik_disable_interface(
            args["interface_name"]
        ),
        "mikrotik_get_interface_monitor": lambda args: mikrotik_get_interface_monitor(
            args["interface_name"]
        ),
        "mikrotik_list_bridge_ports": lambda args: mikrotik_list_bridge_ports(
            args.get("bridge_name")
        ),
        "mikrotik_add_bridge_port": lambda args: mikrotik_add_bridge_port(
            args["bridge"],
            args["interface"]
        ),
        "mikrotik_remove_bridge_port": lambda args: mikrotik_remove_bridge_port(
            args["interface"]
        ),
        "mikrotik_get_interface_traffic": lambda args: mikrotik_get_interface_traffic(
            args["interface_name"]
        ),
    }

