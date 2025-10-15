from typing import Dict, Any, List, Callable
from ..scope.interfaces import (
    mikrotik_list_interfaces, mikrotik_get_interface_stats, mikrotik_enable_interface,
    mikrotik_disable_interface, mikrotik_get_interface_monitor, mikrotik_list_bridge_ports,
    mikrotik_add_bridge_port, mikrotik_remove_bridge_port, mikrotik_get_interface_traffic
)
from ..scope.bridge_advanced import (
    mikrotik_list_bridges, mikrotik_create_bridge, mikrotik_update_bridge,
    mikrotik_list_bridge_vlans, mikrotik_add_bridge_vlan, mikrotik_remove_bridge_vlan,
    mikrotik_set_bridge_port_vlan, mikrotik_enable_bridge_vlan_filtering,
    mikrotik_disable_bridge_vlan_filtering, mikrotik_get_bridge_settings,
    mikrotik_set_bridge_protocol, mikrotik_enable_igmp_snooping,
    mikrotik_disable_igmp_snooping, mikrotik_create_vlan_aware_bridge
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
        # Advanced Bridge tools
        Tool(
            name="mikrotik_list_bridges",
            description="Lists bridge interfaces with advanced settings (READ-ONLY, safe)",
            inputSchema={
                "type": "object",
                "properties": {
                    "name_filter": {"type": "string"},
                    "disabled_only": {"type": "boolean"}
                },
                "required": []
            },
        ),
        Tool(
            name="mikrotik_create_bridge",
            description="Creates a bridge with advanced options (VLAN filtering, STP, IGMP)",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "vlan_filtering": {"type": "boolean", "default": False},
                    "protocol_mode": {"type": "string", "enum": ["none", "rstp", "stp", "mstp"], "default": "rstp"},
                    "priority": {"type": "integer", "default": 32768},
                    "igmp_snooping": {"type": "boolean", "default": False},
                    "mtu": {"type": "integer", "default": 1500},
                    "comment": {"type": "string"},
                    "disabled": {"type": "boolean"}
                },
                "required": ["name"]
            },
        ),
        Tool(
            name="mikrotik_update_bridge",
            description="Updates bridge settings",
            inputSchema={
                "type": "object",
                "properties": {
                    "bridge_id": {"type": "string"},
                    "vlan_filtering": {"type": "boolean"},
                    "protocol_mode": {"type": "string", "enum": ["none", "rstp", "stp", "mstp"]},
                    "priority": {"type": "integer"},
                    "igmp_snooping": {"type": "boolean"},
                    "comment": {"type": "string"},
                    "disabled": {"type": "boolean"}
                },
                "required": ["bridge_id"]
            },
        ),
        Tool(
            name="mikrotik_list_bridge_vlans",
            description="Lists VLAN configurations on bridges (READ-ONLY, safe)",
            inputSchema={
                "type": "object",
                "properties": {
                    "bridge_filter": {"type": "string"},
                    "vlan_ids": {"type": "string"}
                },
                "required": []
            },
        ),
        Tool(
            name="mikrotik_add_bridge_vlan",
            description="Adds VLAN configuration to a bridge",
            inputSchema={
                "type": "object",
                "properties": {
                    "bridge": {"type": "string"},
                    "vlan_ids": {"type": "string", "description": "VLAN IDs (e.g., '10' or '10-20')"},
                    "tagged": {"type": "string", "description": "Tagged ports (comma-separated)"},
                    "untagged": {"type": "string", "description": "Untagged ports (comma-separated)"},
                    "comment": {"type": "string"}
                },
                "required": ["bridge", "vlan_ids", "tagged"]
            },
        ),
        Tool(
            name="mikrotik_remove_bridge_vlan",
            description="Removes VLAN configuration from a bridge",
            inputSchema={
                "type": "object",
                "properties": {
                    "vlan_id": {"type": "string"}
                },
                "required": ["vlan_id"]
            },
        ),
        Tool(
            name="mikrotik_set_bridge_port_vlan",
            description="Configures VLAN settings for a bridge port",
            inputSchema={
                "type": "object",
                "properties": {
                    "port": {"type": "string"},
                    "bridge": {"type": "string"},
                    "pvid": {"type": "integer", "default": 1},
                    "frame_types": {"type": "string", "enum": ["admit-all", "admit-only-vlan-tagged", "admit-only-untagged-and-priority-tagged"], "default": "admit-all"},
                    "ingress_filtering": {"type": "boolean", "default": False}
                },
                "required": ["port", "bridge"]
            },
        ),
        Tool(
            name="mikrotik_enable_bridge_vlan_filtering",
            description="Enables VLAN filtering on a bridge",
            inputSchema={
                "type": "object",
                "properties": {
                    "bridge_name": {"type": "string"}
                },
                "required": ["bridge_name"]
            },
        ),
        Tool(
            name="mikrotik_disable_bridge_vlan_filtering",
            description="Disables VLAN filtering on a bridge",
            inputSchema={
                "type": "object",
                "properties": {
                    "bridge_name": {"type": "string"}
                },
                "required": ["bridge_name"]
            },
        ),
        Tool(
            name="mikrotik_get_bridge_settings",
            description="Gets detailed settings for a bridge (READ-ONLY, safe)",
            inputSchema={
                "type": "object",
                "properties": {
                    "bridge_id": {"type": "string"}
                },
                "required": ["bridge_id"]
            },
        ),
        Tool(
            name="mikrotik_set_bridge_protocol",
            description="Sets spanning tree protocol for a bridge",
            inputSchema={
                "type": "object",
                "properties": {
                    "bridge_id": {"type": "string"},
                    "protocol_mode": {"type": "string", "enum": ["none", "rstp", "stp", "mstp"]},
                    "priority": {"type": "integer"}
                },
                "required": ["bridge_id", "protocol_mode"]
            },
        ),
        Tool(
            name="mikrotik_enable_igmp_snooping",
            description="Enables IGMP snooping on a bridge",
            inputSchema={
                "type": "object",
                "properties": {
                    "bridge_id": {"type": "string"}
                },
                "required": ["bridge_id"]
            },
        ),
        Tool(
            name="mikrotik_disable_igmp_snooping",
            description="Disables IGMP snooping on a bridge",
            inputSchema={
                "type": "object",
                "properties": {
                    "bridge_id": {"type": "string"}
                },
                "required": ["bridge_id"]
            },
        ),
        Tool(
            name="mikrotik_create_vlan_aware_bridge",
            description="Creates a complete VLAN-aware bridge setup",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "ports": {"type": "array", "items": {"type": "string"}},
                    "vlan_config": {"type": "array"},
                    "protocol_mode": {"type": "string", "default": "rstp"}
                },
                "required": ["name", "ports", "vlan_config"]
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
        # Advanced Bridge handlers
        "mikrotik_list_bridges": lambda args: mikrotik_list_bridges(
            args.get("name_filter"),
            args.get("disabled_only", False)
        ),
        "mikrotik_create_bridge": lambda args: mikrotik_create_bridge(
            args["name"],
            args.get("vlan_filtering", False),
            args.get("protocol_mode", "rstp"),
            args.get("priority", 32768),
            args.get("igmp_snooping", False),
            args.get("mtu", 1500),
            args.get("comment"),
            args.get("disabled", False)
        ),
        "mikrotik_update_bridge": lambda args: mikrotik_update_bridge(
            args["bridge_id"],
            args.get("vlan_filtering"),
            args.get("protocol_mode"),
            args.get("priority"),
            args.get("igmp_snooping"),
            args.get("comment"),
            args.get("disabled")
        ),
        "mikrotik_list_bridge_vlans": lambda args: mikrotik_list_bridge_vlans(
            args.get("bridge_filter"),
            args.get("vlan_ids")
        ),
        "mikrotik_add_bridge_vlan": lambda args: mikrotik_add_bridge_vlan(
            args["bridge"],
            args["vlan_ids"],
            args["tagged"],
            args.get("untagged"),
            args.get("comment")
        ),
        "mikrotik_remove_bridge_vlan": lambda args: mikrotik_remove_bridge_vlan(
            args["vlan_id"]
        ),
        "mikrotik_set_bridge_port_vlan": lambda args: mikrotik_set_bridge_port_vlan(
            args["port"],
            args["bridge"],
            args.get("pvid", 1),
            args.get("frame_types", "admit-all"),
            args.get("ingress_filtering", False)
        ),
        "mikrotik_enable_bridge_vlan_filtering": lambda args: mikrotik_enable_bridge_vlan_filtering(
            args["bridge_name"]
        ),
        "mikrotik_disable_bridge_vlan_filtering": lambda args: mikrotik_disable_bridge_vlan_filtering(
            args["bridge_name"]
        ),
        "mikrotik_get_bridge_settings": lambda args: mikrotik_get_bridge_settings(
            args["bridge_id"]
        ),
        "mikrotik_set_bridge_protocol": lambda args: mikrotik_set_bridge_protocol(
            args["bridge_id"],
            args["protocol_mode"],
            args.get("priority")
        ),
        "mikrotik_enable_igmp_snooping": lambda args: mikrotik_enable_igmp_snooping(
            args["bridge_id"]
        ),
        "mikrotik_disable_igmp_snooping": lambda args: mikrotik_disable_igmp_snooping(
            args["bridge_id"]
        ),
        "mikrotik_create_vlan_aware_bridge": lambda args: mikrotik_create_vlan_aware_bridge(
            args["name"],
            args["ports"],
            args["vlan_config"],
            args.get("protocol_mode", "rstp")
        ),
    }

