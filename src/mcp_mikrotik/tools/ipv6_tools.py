from typing import Dict, Any, List, Callable
from ..scope.ipv6 import (
    mikrotik_list_ipv6_addresses, mikrotik_add_ipv6_address, mikrotik_remove_ipv6_address,
    mikrotik_get_ipv6_address, mikrotik_list_ipv6_routes, mikrotik_add_ipv6_route,
    mikrotik_remove_ipv6_route, mikrotik_list_ipv6_neighbors, mikrotik_get_ipv6_nd_settings,
    mikrotik_set_ipv6_nd, mikrotik_list_ipv6_pools, mikrotik_create_ipv6_pool,
    mikrotik_remove_ipv6_pool, mikrotik_get_ipv6_settings, mikrotik_set_ipv6_forward
)
from ..scope.ipv6_firewall import (
    mikrotik_list_ipv6_filter_rules, mikrotik_create_ipv6_filter_rule,
    mikrotik_remove_ipv6_filter_rule, mikrotik_list_ipv6_nat_rules,
    mikrotik_create_ipv6_nat_rule, mikrotik_remove_ipv6_nat_rule,
    mikrotik_list_ipv6_address_lists, mikrotik_add_ipv6_address_list,
    mikrotik_remove_ipv6_address_list_entry, mikrotik_list_ipv6_mangle_rules,
    mikrotik_create_ipv6_mangle_rule, mikrotik_remove_ipv6_mangle_rule
)
from ..scope.ipv6_dhcp import (
    mikrotik_list_dhcpv6_servers, mikrotik_create_dhcpv6_server,
    mikrotik_remove_dhcpv6_server, mikrotik_get_dhcpv6_server,
    mikrotik_list_dhcpv6_leases, mikrotik_create_dhcpv6_static_lease,
    mikrotik_remove_dhcpv6_lease, mikrotik_list_dhcpv6_clients,
    mikrotik_create_dhcpv6_client, mikrotik_remove_dhcpv6_client,
    mikrotik_get_dhcpv6_client, mikrotik_list_dhcpv6_options,
    mikrotik_create_dhcpv6_option, mikrotik_remove_dhcpv6_option
)
from mcp.types import Tool


def get_ipv6_tools() -> List[Tool]:
    """Return IPv6 management tools."""
    return [
        # IPv6 Address Management
        Tool(
            name="mikrotik_list_ipv6_addresses",
            description="Lists IPv6 addresses",
            inputSchema={
                "type": "object",
                "properties": {
                    "interface": {"type": "string", "description": "Filter by interface"}
                },
                "required": []
            },
        ),
        Tool(
            name="mikrotik_add_ipv6_address",
            description="Adds an IPv6 address",
            inputSchema={
                "type": "object",
                "properties": {
                    "address": {"type": "string", "description": "IPv6 address with prefix"},
                    "interface": {"type": "string", "description": "Interface name"},
                    "advertise": {"type": "boolean", "description": "Advertise prefix"},
                    "eui_64": {"type": "boolean", "description": "Use EUI-64"},
                    "no_dad": {"type": "boolean", "description": "Disable DAD"},
                    "comment": {"type": "string", "description": "Comment"}
                },
                "required": ["address", "interface"]
            },
        ),
        Tool(
            name="mikrotik_remove_ipv6_address",
            description="Removes an IPv6 address",
            inputSchema={
                "type": "object",
                "properties": {
                    "address": {"type": "string", "description": "IPv6 address"}
                },
                "required": ["address"]
            },
        ),
        Tool(
            name="mikrotik_get_ipv6_address",
            description="Gets IPv6 address details",
            inputSchema={
                "type": "object",
                "properties": {
                    "address": {"type": "string", "description": "IPv6 address"}
                },
                "required": ["address"]
            },
        ),
        
        # IPv6 Routes
        Tool(
            name="mikrotik_list_ipv6_routes",
            description="Lists IPv6 routes",
            inputSchema={
                "type": "object",
                "properties": {
                    "dst_address": {"type": "string", "description": "Filter by destination"}
                },
                "required": []
            },
        ),
        Tool(
            name="mikrotik_add_ipv6_route",
            description="Adds an IPv6 route",
            inputSchema={
                "type": "object",
                "properties": {
                    "dst_address": {"type": "string", "description": "Destination prefix"},
                    "gateway": {"type": "string", "description": "Gateway address"},
                    "interface": {"type": "string", "description": "Interface name"},
                    "distance": {"type": "integer", "description": "Administrative distance"},
                    "comment": {"type": "string", "description": "Comment"}
                },
                "required": ["dst_address"]
            },
        ),
        Tool(
            name="mikrotik_remove_ipv6_route",
            description="Removes an IPv6 route",
            inputSchema={
                "type": "object",
                "properties": {
                    "dst_address": {"type": "string", "description": "Destination address"}
                },
                "required": ["dst_address"]
            },
        ),
        
        # IPv6 Neighbors
        Tool(
            name="mikrotik_list_ipv6_neighbors",
            description="Lists IPv6 neighbors",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        Tool(
            name="mikrotik_get_ipv6_nd_settings",
            description="Gets IPv6 ND settings for interface",
            inputSchema={
                "type": "object",
                "properties": {
                    "interface": {"type": "string", "description": "Interface name"}
                },
                "required": ["interface"]
            },
        ),
        Tool(
            name="mikrotik_set_ipv6_nd",
            description="Configures IPv6 Neighbor Discovery",
            inputSchema={
                "type": "object",
                "properties": {
                    "interface": {"type": "string", "description": "Interface name"},
                    "ra_interval": {"type": "string", "description": "RA interval"},
                    "ra_lifetime": {"type": "string", "description": "RA lifetime"},
                    "hop_limit": {"type": "integer", "description": "Hop limit"},
                    "advertise_mac_address": {"type": "boolean", "description": "Advertise MAC"},
                    "advertise_dns": {"type": "boolean", "description": "Advertise DNS"}
                },
                "required": ["interface"]
            },
        ),
        
        # IPv6 Pools
        Tool(
            name="mikrotik_list_ipv6_pools",
            description="Lists IPv6 pools",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        Tool(
            name="mikrotik_create_ipv6_pool",
            description="Creates an IPv6 pool",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Pool name"},
                    "prefix": {"type": "string", "description": "IPv6 prefix"},
                    "prefix_length": {"type": "integer", "description": "Prefix length"},
                    "comment": {"type": "string", "description": "Comment"}
                },
                "required": ["name", "prefix"]
            },
        ),
        Tool(
            name="mikrotik_remove_ipv6_pool",
            description="Removes an IPv6 pool",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Pool name"}
                },
                "required": ["name"]
            },
        ),
        
        # IPv6 Settings
        Tool(
            name="mikrotik_get_ipv6_settings",
            description="Gets global IPv6 settings",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        Tool(
            name="mikrotik_set_ipv6_forward",
            description="Enables/disables IPv6 forwarding",
            inputSchema={
                "type": "object",
                "properties": {
                    "enabled": {"type": "boolean", "description": "Enable forwarding"}
                },
                "required": ["enabled"]
            },
        ),
    ]


def get_ipv6_handlers() -> Dict[str, Callable]:
    """Return IPv6 handlers."""
    return {
        "mikrotik_list_ipv6_addresses": lambda args: mikrotik_list_ipv6_addresses(
            args.get("interface")
        ),
        "mikrotik_add_ipv6_address": lambda args: mikrotik_add_ipv6_address(
            address=args["address"],
            interface=args["interface"],
            advertise=args.get("advertise", True),
            eui_64=args.get("eui_64", False),
            no_dad=args.get("no_dad", False),
            comment=args.get("comment")
        ),
        "mikrotik_remove_ipv6_address": lambda args: mikrotik_remove_ipv6_address(
            args["address"]
        ),
        "mikrotik_get_ipv6_address": lambda args: mikrotik_get_ipv6_address(
            args["address"]
        ),
        "mikrotik_list_ipv6_routes": lambda args: mikrotik_list_ipv6_routes(
            args.get("dst_address")
        ),
        "mikrotik_add_ipv6_route": lambda args: mikrotik_add_ipv6_route(
            dst_address=args["dst_address"],
            gateway=args.get("gateway"),
            interface=args.get("interface"),
            distance=args.get("distance", 1),
            comment=args.get("comment")
        ),
        "mikrotik_remove_ipv6_route": lambda args: mikrotik_remove_ipv6_route(
            args["dst_address"]
        ),
        "mikrotik_list_ipv6_neighbors": lambda args: mikrotik_list_ipv6_neighbors(),
        "mikrotik_get_ipv6_nd_settings": lambda args: mikrotik_get_ipv6_nd_settings(
            args["interface"]
        ),
        "mikrotik_set_ipv6_nd": lambda args: mikrotik_set_ipv6_nd(
            interface=args["interface"],
            ra_interval=args.get("ra_interval"),
            ra_lifetime=args.get("ra_lifetime"),
            hop_limit=args.get("hop_limit"),
            advertise_mac_address=args.get("advertise_mac_address"),
            advertise_dns=args.get("advertise_dns")
        ),
        "mikrotik_list_ipv6_pools": lambda args: mikrotik_list_ipv6_pools(),
        "mikrotik_create_ipv6_pool": lambda args: mikrotik_create_ipv6_pool(
            name=args["name"],
            prefix=args["prefix"],
            prefix_length=args.get("prefix_length", 64),
            comment=args.get("comment")
        ),
        "mikrotik_remove_ipv6_pool": lambda args: mikrotik_remove_ipv6_pool(
            args["name"]
        ),
        "mikrotik_get_ipv6_settings": lambda args: mikrotik_get_ipv6_settings(),
        "mikrotik_set_ipv6_forward": lambda args: mikrotik_set_ipv6_forward(
            args["enabled"]
        ),
    }


def get_ipv6_firewall_tools() -> List[Tool]:
    """Return IPv6 firewall tools."""
    return [
        # Filter Rules
        Tool(
            name="mikrotik_list_ipv6_filter_rules",
            description="Lists IPv6 firewall filter rules",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        Tool(
            name="mikrotik_create_ipv6_filter_rule",
            description="Creates an IPv6 firewall filter rule",
            inputSchema={
                "type": "object",
                "properties": {
                    "chain": {"type": "string", "description": "Chain name"},
                    "rule_action": {"type": "string", "description": "Rule action"},
                    "protocol": {"type": "string", "description": "Protocol"},
                    "src_address": {"type": "string", "description": "Source address"},
                    "dst_address": {"type": "string", "description": "Destination address"},
                    "src_port": {"type": "string", "description": "Source port"},
                    "dst_port": {"type": "string", "description": "Destination port"},
                    "in_interface": {"type": "string", "description": "Input interface"},
                    "out_interface": {"type": "string", "description": "Output interface"},
                    "connection_state": {"type": "string", "description": "Connection state"},
                    "disabled": {"type": "boolean", "description": "Disable rule"},
                    "comment": {"type": "string", "description": "Comment"}
                },
                "required": ["chain", "rule_action"]
            },
        ),
        Tool(
            name="mikrotik_remove_ipv6_filter_rule",
            description="Removes an IPv6 firewall filter rule",
            inputSchema={
                "type": "object",
                "properties": {
                    "rule_id": {"type": "string", "description": "Rule ID"}
                },
                "required": ["rule_id"]
            },
        ),
        
        # NAT Rules
        Tool(
            name="mikrotik_list_ipv6_nat_rules",
            description="Lists IPv6 NAT rules",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        Tool(
            name="mikrotik_create_ipv6_nat_rule",
            description="Creates an IPv6 NAT rule",
            inputSchema={
                "type": "object",
                "properties": {
                    "chain": {"type": "string", "description": "Chain name"},
                    "action": {"type": "string", "description": "NAT action"},
                    "src_address": {"type": "string", "description": "Source address"},
                    "dst_address": {"type": "string", "description": "Destination address"},
                    "out_interface": {"type": "string", "description": "Output interface"},
                    "to_addresses": {"type": "string", "description": "Translation address"},
                    "comment": {"type": "string", "description": "Comment"}
                },
                "required": ["chain", "action"]
            },
        ),
        Tool(
            name="mikrotik_remove_ipv6_nat_rule",
            description="Removes an IPv6 NAT rule",
            inputSchema={
                "type": "object",
                "properties": {
                    "rule_id": {"type": "string", "description": "Rule ID"}
                },
                "required": ["rule_id"]
            },
        ),
        
        # Address Lists
        Tool(
            name="mikrotik_list_ipv6_address_lists",
            description="Lists IPv6 address lists",
            inputSchema={
                "type": "object",
                "properties": {
                    "list_name": {"type": "string", "description": "Filter by list name"}
                },
                "required": []
            },
        ),
        Tool(
            name="mikrotik_add_ipv6_address_list",
            description="Adds address to IPv6 address list",
            inputSchema={
                "type": "object",
                "properties": {
                    "list_name": {"type": "string", "description": "List name"},
                    "address": {"type": "string", "description": "IPv6 address"},
                    "timeout": {"type": "string", "description": "Timeout"},
                    "comment": {"type": "string", "description": "Comment"}
                },
                "required": ["list_name", "address"]
            },
        ),
        Tool(
            name="mikrotik_remove_ipv6_address_list_entry",
            description="Removes IPv6 address list entry",
            inputSchema={
                "type": "object",
                "properties": {
                    "entry_id": {"type": "string", "description": "Entry ID"}
                },
                "required": ["entry_id"]
            },
        ),
        
        # Mangle Rules
        Tool(
            name="mikrotik_list_ipv6_mangle_rules",
            description="Lists IPv6 mangle rules",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        Tool(
            name="mikrotik_create_ipv6_mangle_rule",
            description="Creates an IPv6 mangle rule",
            inputSchema={
                "type": "object",
                "properties": {
                    "chain": {"type": "string", "description": "Chain name"},
                    "action": {"type": "string", "description": "Mangle action"},
                    "protocol": {"type": "string", "description": "Protocol"},
                    "src_address": {"type": "string", "description": "Source address"},
                    "dst_address": {"type": "string", "description": "Destination address"},
                    "new_routing_mark": {"type": "string", "description": "Routing mark"},
                    "passthrough": {"type": "boolean", "description": "Passthrough"},
                    "comment": {"type": "string", "description": "Comment"}
                },
                "required": ["chain", "action"]
            },
        ),
        Tool(
            name="mikrotik_remove_ipv6_mangle_rule",
            description="Removes an IPv6 mangle rule",
            inputSchema={
                "type": "object",
                "properties": {
                    "rule_id": {"type": "string", "description": "Rule ID"}
                },
                "required": ["rule_id"]
            },
        ),
    ]


def get_ipv6_firewall_handlers() -> Dict[str, Callable]:
    """Return IPv6 firewall handlers."""
    return {
        "mikrotik_list_ipv6_filter_rules": lambda args: mikrotik_list_ipv6_filter_rules(),
        "mikrotik_create_ipv6_filter_rule": lambda args: mikrotik_create_ipv6_filter_rule(
            chain=args["chain"],
            rule_action=args["rule_action"],
            protocol=args.get("protocol"),
            src_address=args.get("src_address"),
            dst_address=args.get("dst_address"),
            src_port=args.get("src_port"),
            dst_port=args.get("dst_port"),
            in_interface=args.get("in_interface"),
            out_interface=args.get("out_interface"),
            connection_state=args.get("connection_state"),
            disabled=args.get("disabled", False),
            comment=args.get("comment")
        ),
        "mikrotik_remove_ipv6_filter_rule": lambda args: mikrotik_remove_ipv6_filter_rule(
            args["rule_id"]
        ),
        "mikrotik_list_ipv6_nat_rules": lambda args: mikrotik_list_ipv6_nat_rules(),
        "mikrotik_create_ipv6_nat_rule": lambda args: mikrotik_create_ipv6_nat_rule(
            chain=args["chain"],
            action=args["action"],
            src_address=args.get("src_address"),
            dst_address=args.get("dst_address"),
            out_interface=args.get("out_interface"),
            to_addresses=args.get("to_addresses"),
            comment=args.get("comment")
        ),
        "mikrotik_remove_ipv6_nat_rule": lambda args: mikrotik_remove_ipv6_nat_rule(
            args["rule_id"]
        ),
        "mikrotik_list_ipv6_address_lists": lambda args: mikrotik_list_ipv6_address_lists(
            args.get("list_name")
        ),
        "mikrotik_add_ipv6_address_list": lambda args: mikrotik_add_ipv6_address_list(
            list_name=args["list_name"],
            address=args["address"],
            timeout=args.get("timeout"),
            comment=args.get("comment")
        ),
        "mikrotik_remove_ipv6_address_list_entry": lambda args: mikrotik_remove_ipv6_address_list_entry(
            args["entry_id"]
        ),
        "mikrotik_list_ipv6_mangle_rules": lambda args: mikrotik_list_ipv6_mangle_rules(),
        "mikrotik_create_ipv6_mangle_rule": lambda args: mikrotik_create_ipv6_mangle_rule(
            chain=args["chain"],
            action=args["action"],
            protocol=args.get("protocol"),
            src_address=args.get("src_address"),
            dst_address=args.get("dst_address"),
            new_routing_mark=args.get("new_routing_mark"),
            passthrough=args.get("passthrough", True),
            comment=args.get("comment")
        ),
        "mikrotik_remove_ipv6_mangle_rule": lambda args: mikrotik_remove_ipv6_mangle_rule(
            args["rule_id"]
        ),
    }


def get_dhcpv6_tools() -> List[Tool]:
    """Return DHCPv6 tools."""
    return [
        # DHCPv6 Server
        Tool(
            name="mikrotik_list_dhcpv6_servers",
            description="Lists DHCPv6 servers",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        Tool(
            name="mikrotik_create_dhcpv6_server",
            description="Creates a DHCPv6 server",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Server name"},
                    "interface": {"type": "string", "description": "Interface"},
                    "address_pool": {"type": "string", "description": "Address pool"},
                    "lease_time": {"type": "string", "description": "Lease time"},
                    "disabled": {"type": "boolean", "description": "Disable server"}
                },
                "required": ["name", "interface", "address_pool"]
            },
        ),
        Tool(
            name="mikrotik_remove_dhcpv6_server",
            description="Removes a DHCPv6 server",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Server name"}
                },
                "required": ["name"]
            },
        ),
        Tool(
            name="mikrotik_get_dhcpv6_server",
            description="Gets DHCPv6 server details",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Server name"}
                },
                "required": ["name"]
            },
        ),
        
        # DHCPv6 Leases
        Tool(
            name="mikrotik_list_dhcpv6_leases",
            description="Lists DHCPv6 leases",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        Tool(
            name="mikrotik_create_dhcpv6_static_lease",
            description="Creates a DHCPv6 static lease",
            inputSchema={
                "type": "object",
                "properties": {
                    "address": {"type": "string", "description": "IPv6 address"},
                    "duid": {"type": "string", "description": "Client DUID"},
                    "server": {"type": "string", "description": "Server name"},
                    "comment": {"type": "string", "description": "Comment"}
                },
                "required": ["address", "duid"]
            },
        ),
        Tool(
            name="mikrotik_remove_dhcpv6_lease",
            description="Removes a DHCPv6 lease",
            inputSchema={
                "type": "object",
                "properties": {
                    "lease_id": {"type": "string", "description": "Lease ID"}
                },
                "required": ["lease_id"]
            },
        ),
        
        # DHCPv6 Client
        Tool(
            name="mikrotik_list_dhcpv6_clients",
            description="Lists DHCPv6 clients",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        Tool(
            name="mikrotik_create_dhcpv6_client",
            description="Creates a DHCPv6 client",
            inputSchema={
                "type": "object",
                "properties": {
                    "interface": {"type": "string", "description": "Interface"},
                    "pool_name": {"type": "string", "description": "Pool name"},
                    "pool_prefix_length": {"type": "integer", "description": "Prefix length"},
                    "add_default_route": {"type": "boolean", "description": "Add default route"},
                    "request": {"type": "string", "description": "Request type"},
                    "disabled": {"type": "boolean", "description": "Disable client"}
                },
                "required": ["interface"]
            },
        ),
        Tool(
            name="mikrotik_remove_dhcpv6_client",
            description="Removes a DHCPv6 client",
            inputSchema={
                "type": "object",
                "properties": {
                    "interface": {"type": "string", "description": "Interface"}
                },
                "required": ["interface"]
            },
        ),
        Tool(
            name="mikrotik_get_dhcpv6_client",
            description="Gets DHCPv6 client details",
            inputSchema={
                "type": "object",
                "properties": {
                    "interface": {"type": "string", "description": "Interface"}
                },
                "required": ["interface"]
            },
        ),
        
        # DHCPv6 Options
        Tool(
            name="mikrotik_list_dhcpv6_options",
            description="Lists DHCPv6 options",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        Tool(
            name="mikrotik_create_dhcpv6_option",
            description="Creates a DHCPv6 option",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Option name"},
                    "code": {"type": "integer", "description": "Option code"},
                    "value": {"type": "string", "description": "Option value"}
                },
                "required": ["name", "code", "value"]
            },
        ),
        Tool(
            name="mikrotik_remove_dhcpv6_option",
            description="Removes a DHCPv6 option",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Option name"}
                },
                "required": ["name"]
            },
        ),
    ]


def get_dhcpv6_handlers() -> Dict[str, Callable]:
    """Return DHCPv6 handlers."""
    return {
        "mikrotik_list_dhcpv6_servers": lambda args: mikrotik_list_dhcpv6_servers(),
        "mikrotik_create_dhcpv6_server": lambda args: mikrotik_create_dhcpv6_server(
            name=args["name"],
            interface=args["interface"],
            address_pool=args["address_pool"],
            lease_time=args.get("lease_time", "1d"),
            disabled=args.get("disabled", False)
        ),
        "mikrotik_remove_dhcpv6_server": lambda args: mikrotik_remove_dhcpv6_server(
            args["name"]
        ),
        "mikrotik_get_dhcpv6_server": lambda args: mikrotik_get_dhcpv6_server(
            args["name"]
        ),
        "mikrotik_list_dhcpv6_leases": lambda args: mikrotik_list_dhcpv6_leases(),
        "mikrotik_create_dhcpv6_static_lease": lambda args: mikrotik_create_dhcpv6_static_lease(
            address=args["address"],
            duid=args["duid"],
            server=args.get("server"),
            comment=args.get("comment")
        ),
        "mikrotik_remove_dhcpv6_lease": lambda args: mikrotik_remove_dhcpv6_lease(
            args["lease_id"]
        ),
        "mikrotik_list_dhcpv6_clients": lambda args: mikrotik_list_dhcpv6_clients(),
        "mikrotik_create_dhcpv6_client": lambda args: mikrotik_create_dhcpv6_client(
            interface=args["interface"],
            pool_name=args.get("pool_name"),
            pool_prefix_length=args.get("pool_prefix_length", 64),
            add_default_route=args.get("add_default_route", True),
            request=args.get("request", "address"),
            disabled=args.get("disabled", False)
        ),
        "mikrotik_remove_dhcpv6_client": lambda args: mikrotik_remove_dhcpv6_client(
            args["interface"]
        ),
        "mikrotik_get_dhcpv6_client": lambda args: mikrotik_get_dhcpv6_client(
            args["interface"]
        ),
        "mikrotik_list_dhcpv6_options": lambda args: mikrotik_list_dhcpv6_options(),
        "mikrotik_create_dhcpv6_option": lambda args: mikrotik_create_dhcpv6_option(
            name=args["name"],
            code=args["code"],
            value=args["value"]
        ),
        "mikrotik_remove_dhcpv6_option": lambda args: mikrotik_remove_dhcpv6_option(
            args["name"]
        ),
    }

