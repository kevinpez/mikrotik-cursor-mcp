"""
Connectivity tools: PPPoE, Tunnels (EoIP, GRE), and Bonding.
"""
from typing import Dict, Any, List, Callable
from ..scope.pppoe import (
    mikrotik_list_pppoe_clients, mikrotik_create_pppoe_client,
    mikrotik_remove_pppoe_client, mikrotik_get_pppoe_status,
    mikrotik_list_pppoe_servers
)
from ..scope.tunnels import (
    mikrotik_list_eoip_tunnels, mikrotik_create_eoip_tunnel, mikrotik_remove_eoip_tunnel,
    mikrotik_list_gre_tunnels, mikrotik_create_gre_tunnel, mikrotik_remove_gre_tunnel,
    mikrotik_list_tunnels
)
from ..scope.bonding import (
    mikrotik_list_bonding_interfaces, mikrotik_create_bonding_interface,
    mikrotik_add_bonding_slave, mikrotik_remove_bonding_interface
)
from mcp.types import Tool


def get_connectivity_tools() -> List[Tool]:
    """Return PPPoE, tunnel, and bonding tools."""
    return [
        # PPPoE tools
        Tool(
            name="mikrotik_list_pppoe_clients",
            description="List PPPoE client interfaces (READ-ONLY, safe)",
            inputSchema={"type": "object", "properties": {"name_filter": {"type": "string"}, "disabled_only": {"type": "boolean"}}, "required": []},
        ),
        Tool(
            name="mikrotik_create_pppoe_client",
            description="Create PPPoE client for ISP connection",
            inputSchema={"type": "object", "properties": {"name": {"type": "string"}, "interface": {"type": "string"}, "user": {"type": "string"}, "password": {"type": "string"}, "add_default_route": {"type": "boolean"}, "use_peer_dns": {"type": "boolean"}, "comment": {"type": "string"}}, "required": ["name", "interface", "user", "password"]},
        ),
        Tool(
            name="mikrotik_remove_pppoe_client",
            description="Remove PPPoE client interface",
            inputSchema={"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]},
        ),
        Tool(
            name="mikrotik_get_pppoe_status",
            description="Get PPPoE client status (READ-ONLY, safe)",
            inputSchema={"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]},
        ),
        Tool(
            name="mikrotik_list_pppoe_servers",
            description="List PPPoE servers (READ-ONLY, safe)",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        # EoIP tunnel tools
        Tool(
            name="mikrotik_list_eoip_tunnels",
            description="List EoIP tunnels (READ-ONLY, safe)",
            inputSchema={"type": "object", "properties": {"name_filter": {"type": "string"}}, "required": []},
        ),
        Tool(
            name="mikrotik_create_eoip_tunnel",
            description="Create EoIP (Ethernet over IP) tunnel",
            inputSchema={"type": "object", "properties": {"name": {"type": "string"}, "remote_address": {"type": "string"}, "tunnel_id": {"type": "integer"}, "local_address": {"type": "string"}, "mtu": {"type": "integer"}, "comment": {"type": "string"}}, "required": ["name", "remote_address", "tunnel_id"]},
        ),
        Tool(
            name="mikrotik_remove_eoip_tunnel",
            description="Remove EoIP tunnel",
            inputSchema={"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]},
        ),
        # GRE tunnel tools
        Tool(
            name="mikrotik_list_gre_tunnels",
            description="List GRE tunnels (READ-ONLY, safe)",
            inputSchema={"type": "object", "properties": {"name_filter": {"type": "string"}}, "required": []},
        ),
        Tool(
            name="mikrotik_create_gre_tunnel",
            description="Create GRE (Generic Routing Encapsulation) tunnel",
            inputSchema={"type": "object", "properties": {"name": {"type": "string"}, "remote_address": {"type": "string"}, "local_address": {"type": "string"}, "mtu": {"type": "integer"}, "comment": {"type": "string"}}, "required": ["name", "remote_address"]},
        ),
        Tool(
            name="mikrotik_remove_gre_tunnel",
            description="Remove GRE tunnel",
            inputSchema={"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]},
        ),
        Tool(
            name="mikrotik_list_tunnels",
            description="List all tunnel types (EoIP, GRE) (READ-ONLY, safe)",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        # Bonding tools
        Tool(
            name="mikrotik_list_bonding_interfaces",
            description="List bonding (link aggregation) interfaces (READ-ONLY, safe)",
            inputSchema={"type": "object", "properties": {"name_filter": {"type": "string"}}, "required": []},
        ),
        Tool(
            name="mikrotik_create_bonding_interface",
            description="Create bonding interface for link aggregation",
            inputSchema={"type": "object", "properties": {"name": {"type": "string"}, "mode": {"type": "string", "enum": ["balance-rr", "active-backup", "balance-xor", "broadcast", "802.3ad", "balance-tlb", "balance-alb"]}, "slaves": {"type": "string"}, "mtu": {"type": "integer"}, "comment": {"type": "string"}}, "required": ["name"]},
        ),
        Tool(
            name="mikrotik_add_bonding_slave",
            description="Add interface to bonding group",
            inputSchema={"type": "object", "properties": {"bonding_interface": {"type": "string"}, "slave_interface": {"type": "string"}}, "required": ["bonding_interface", "slave_interface"]},
        ),
        Tool(
            name="mikrotik_remove_bonding_interface",
            description="Remove bonding interface",
            inputSchema={"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]},
        ),
    ]


def get_connectivity_handlers() -> Dict[str, Callable]:
    """Return handlers for connectivity tools."""
    return {
        "mikrotik_list_pppoe_clients": lambda args: mikrotik_list_pppoe_clients(args.get("name_filter"), args.get("disabled_only", False)),
        "mikrotik_create_pppoe_client": lambda args: mikrotik_create_pppoe_client(args["name"], args["interface"], args["user"], args["password"], args.get("add_default_route", True), args.get("use_peer_dns", True), args.get("comment")),
        "mikrotik_remove_pppoe_client": lambda args: mikrotik_remove_pppoe_client(args["name"]),
        "mikrotik_get_pppoe_status": lambda args: mikrotik_get_pppoe_status(args["name"]),
        "mikrotik_list_pppoe_servers": lambda args: mikrotik_list_pppoe_servers(),
        "mikrotik_list_eoip_tunnels": lambda args: mikrotik_list_eoip_tunnels(args.get("name_filter")),
        "mikrotik_create_eoip_tunnel": lambda args: mikrotik_create_eoip_tunnel(args["name"], args["remote_address"], args["tunnel_id"], args.get("local_address"), args.get("mtu", 1500), args.get("comment")),
        "mikrotik_remove_eoip_tunnel": lambda args: mikrotik_remove_eoip_tunnel(args["name"]),
        "mikrotik_list_gre_tunnels": lambda args: mikrotik_list_gre_tunnels(args.get("name_filter")),
        "mikrotik_create_gre_tunnel": lambda args: mikrotik_create_gre_tunnel(args["name"], args["remote_address"], args.get("local_address"), args.get("mtu", 1476), args.get("comment")),
        "mikrotik_remove_gre_tunnel": lambda args: mikrotik_remove_gre_tunnel(args["name"]),
        "mikrotik_list_tunnels": lambda args: mikrotik_list_tunnels(),
        "mikrotik_list_bonding_interfaces": lambda args: mikrotik_list_bonding_interfaces(args.get("name_filter")),
        "mikrotik_create_bonding_interface": lambda args: mikrotik_create_bonding_interface(args["name"], args.get("mode", "802.3ad"), args.get("slaves"), args.get("mtu", 1500), args.get("comment")),
        "mikrotik_add_bonding_slave": lambda args: mikrotik_add_bonding_slave(args["bonding_interface"], args["slave_interface"]),
        "mikrotik_remove_bonding_interface": lambda args: mikrotik_remove_bonding_interface(args["name"]),
    }

