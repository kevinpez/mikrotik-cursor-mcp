"""
Advanced routing tool definitions (BGP, OSPF, Route Filters).
"""
from typing import Dict, Any, List, Callable
from ..scope.bgp import (
    mikrotik_create_bgp_instance, mikrotik_add_bgp_peer, mikrotik_list_bgp_peers,
    mikrotik_add_bgp_network, mikrotik_list_bgp_networks, mikrotik_list_bgp_routes,
    mikrotik_get_bgp_status, mikrotik_clear_bgp_session
)
from ..scope.ospf import (
    mikrotik_create_ospf_instance, mikrotik_add_ospf_network, mikrotik_add_ospf_interface,
    mikrotik_list_ospf_neighbors, mikrotik_list_ospf_routes, mikrotik_get_ospf_status,
    mikrotik_create_ospf_area
)
from ..scope.routing_filters import (
    mikrotik_create_route_filter, mikrotik_list_route_filters
)
from mcp.types import Tool


def get_routing_advanced_tools() -> List[Tool]:
    """Return advanced routing tools (BGP, OSPF, filters)."""
    return [
        # BGP tools
        Tool(name="mikrotik_create_bgp_instance", description="Create BGP routing instance",
            inputSchema={"type": "object", "properties": {"name": {"type": "string"}, "as_number": {"type": "integer"}, "router_id": {"type": "string"}, "redistribute_connected": {"type": "boolean"}, "redistribute_static": {"type": "boolean"}, "comment": {"type": "string"}}, "required": ["name", "as_number", "router_id"]}),
        Tool(name="mikrotik_add_bgp_peer", description="Add BGP peer/neighbor",
            inputSchema={"type": "object", "properties": {"name": {"type": "string"}, "instance": {"type": "string"}, "remote_address": {"type": "string"}, "remote_as": {"type": "integer"}, "multihop": {"type": "boolean"}, "route_reflect": {"type": "boolean"}, "comment": {"type": "string"}}, "required": ["name", "instance", "remote_address", "remote_as"]}),
        Tool(name="mikrotik_list_bgp_peers", description="List BGP peers (READ-ONLY)",
            inputSchema={"type": "object", "properties": {"instance_filter": {"type": "string"}}, "required": []}),
        Tool(name="mikrotik_add_bgp_network", description="Advertise network via BGP",
            inputSchema={"type": "object", "properties": {"instance": {"type": "string"}, "network": {"type": "string"}, "synchronize": {"type": "boolean"}, "comment": {"type": "string"}}, "required": ["instance", "network"]}),
        Tool(name="mikrotik_list_bgp_networks", description="List BGP networks (READ-ONLY)",
            inputSchema={"type": "object", "properties": {"instance_filter": {"type": "string"}}, "required": []}),
        Tool(name="mikrotik_list_bgp_routes", description="View BGP routing table (READ-ONLY)",
            inputSchema={"type": "object", "properties": {}, "required": []}),
        Tool(name="mikrotik_get_bgp_status", description="Get BGP status (READ-ONLY)",
            inputSchema={"type": "object", "properties": {"instance": {"type": "string"}}, "required": []}),
        Tool(name="mikrotik_clear_bgp_session", description="Reset BGP session",
            inputSchema={"type": "object", "properties": {"peer": {"type": "string"}}, "required": ["peer"]}),
        # OSPF tools
        Tool(name="mikrotik_create_ospf_instance", description="Create OSPF routing instance",
            inputSchema={"type": "object", "properties": {"name": {"type": "string"}, "router_id": {"type": "string"}, "redistribute_connected": {"type": "boolean"}, "redistribute_static": {"type": "boolean"}, "comment": {"type": "string"}}, "required": []}),
        Tool(name="mikrotik_add_ospf_network", description="Add network to OSPF",
            inputSchema={"type": "object", "properties": {"network": {"type": "string"}, "area": {"type": "string"}, "instance": {"type": "string"}, "comment": {"type": "string"}}, "required": ["network"]}),
        Tool(name="mikrotik_add_ospf_interface", description="Configure OSPF on interface",
            inputSchema={"type": "object", "properties": {"interface": {"type": "string"}, "network_type": {"type": "string"}, "cost": {"type": "integer"}, "priority": {"type": "integer"}, "comment": {"type": "string"}}, "required": ["interface"]}),
        Tool(name="mikrotik_list_ospf_neighbors", description="List OSPF neighbors (READ-ONLY)",
            inputSchema={"type": "object", "properties": {}, "required": []}),
        Tool(name="mikrotik_list_ospf_routes", description="View OSPF routes (READ-ONLY)",
            inputSchema={"type": "object", "properties": {}, "required": []}),
        Tool(name="mikrotik_get_ospf_status", description="Get OSPF status (READ-ONLY)",
            inputSchema={"type": "object", "properties": {"instance": {"type": "string"}}, "required": []}),
        Tool(name="mikrotik_create_ospf_area", description="Configure OSPF area",
            inputSchema={"type": "object", "properties": {"name": {"type": "string"}, "area_id": {"type": "string"}, "instance": {"type": "string"}, "area_type": {"type": "string"}, "comment": {"type": "string"}}, "required": ["name", "area_id"]}),
        # Route filter tools
        Tool(name="mikrotik_create_route_filter", description="Create route filter rule",
            inputSchema={"type": "object", "properties": {"chain": {"type": "string"}, "prefix": {"type": "string"}, "prefix_length": {"type": "string"}, "action": {"type": "string"}, "comment": {"type": "string"}}, "required": ["chain", "prefix"]}),
        Tool(name="mikrotik_list_route_filters", description="List route filters (READ-ONLY)",
            inputSchema={"type": "object", "properties": {"chain_filter": {"type": "string"}}, "required": []}),
    ]


def get_routing_advanced_handlers() -> Dict[str, Callable]:
    """Return handlers for advanced routing tools."""
    return {
        "mikrotik_create_bgp_instance": lambda args: mikrotik_create_bgp_instance(args["name"], args["as_number"], args["router_id"], args.get("redistribute_connected", False), args.get("redistribute_static", False), args.get("comment")),
        "mikrotik_add_bgp_peer": lambda args: mikrotik_add_bgp_peer(args["name"], args["instance"], args["remote_address"], args["remote_as"], args.get("multihop", False), args.get("route_reflect", False), args.get("comment")),
        "mikrotik_list_bgp_peers": lambda args: mikrotik_list_bgp_peers(args.get("instance_filter")),
        "mikrotik_add_bgp_network": lambda args: mikrotik_add_bgp_network(args["instance"], args["network"], args.get("synchronize", False), args.get("comment")),
        "mikrotik_list_bgp_networks": lambda args: mikrotik_list_bgp_networks(args.get("instance_filter")),
        "mikrotik_list_bgp_routes": lambda args: mikrotik_list_bgp_routes(),
        "mikrotik_get_bgp_status": lambda args: mikrotik_get_bgp_status(args.get("instance")),
        "mikrotik_clear_bgp_session": lambda args: mikrotik_clear_bgp_session(args["peer"]),
        "mikrotik_create_ospf_instance": lambda args: mikrotik_create_ospf_instance(args.get("name", "default"), args.get("router_id"), args.get("redistribute_connected", False), args.get("redistribute_static", False), args.get("comment")),
        "mikrotik_add_ospf_network": lambda args: mikrotik_add_ospf_network(args["network"], args.get("area", "backbone"), args.get("instance", "default"), args.get("comment")),
        "mikrotik_add_ospf_interface": lambda args: mikrotik_add_ospf_interface(args["interface"], args.get("network_type", "broadcast"), args.get("cost", 10), args.get("priority", 1), args.get("comment")),
        "mikrotik_list_ospf_neighbors": lambda args: mikrotik_list_ospf_neighbors(),
        "mikrotik_list_ospf_routes": lambda args: mikrotik_list_ospf_routes(),
        "mikrotik_get_ospf_status": lambda args: mikrotik_get_ospf_status(args.get("instance", "default")),
        "mikrotik_create_ospf_area": lambda args: mikrotik_create_ospf_area(args["name"], args["area_id"], args.get("instance", "default"), args.get("area_type", "default"), args.get("comment")),
        "mikrotik_create_route_filter": lambda args: mikrotik_create_route_filter(args["chain"], args["prefix"], args.get("prefix_length"), args.get("action", "accept"), args.get("comment")),
        "mikrotik_list_route_filters": lambda args: mikrotik_list_route_filters(args.get("chain_filter")),
    }


