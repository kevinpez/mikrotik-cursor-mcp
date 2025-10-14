from typing import Dict, Any, List, Callable
from ..scope.diagnostics import (
    mikrotik_ping, mikrotik_traceroute, mikrotik_bandwidth_test, mikrotik_dns_lookup,
    mikrotik_check_connection, mikrotik_get_arp_table, mikrotik_get_neighbors
)
from mcp.types import Tool

def get_diagnostic_tools() -> List[Tool]:
    """Return the list of network diagnostic tools."""
    return [
        Tool(
            name="mikrotik_ping",
            description="Ping a host from the MikroTik router",
            inputSchema={
                "type": "object",
                "properties": {
                    "address": {"type": "string"},
                    "count": {"type": "integer"},
                    "size": {"type": "integer"},
                    "interval": {"type": "string"},
                    "src_address": {"type": "string"},
                    "interface": {"type": "string"}
                },
                "required": ["address"]
            },
        ),
        Tool(
            name="mikrotik_traceroute",
            description="Traceroute to a host from the MikroTik router",
            inputSchema={
                "type": "object",
                "properties": {
                    "address": {"type": "string"},
                    "src_address": {"type": "string"},
                    "interface": {"type": "string"},
                    "max_hops": {"type": "integer"}
                },
                "required": ["address"]
            },
        ),
        Tool(
            name="mikrotik_bandwidth_test",
            description="Run bandwidth test to another MikroTik device",
            inputSchema={
                "type": "object",
                "properties": {
                    "address": {"type": "string"},
                    "duration": {"type": "integer"},
                    "direction": {"type": "string", "enum": ["transmit", "receive", "both"]},
                    "protocol": {"type": "string", "enum": ["tcp", "udp"]},
                    "local_tx_speed": {"type": "string"},
                    "remote_tx_speed": {"type": "string"}
                },
                "required": ["address"]
            },
        ),
        Tool(
            name="mikrotik_dns_lookup",
            description="Perform DNS lookup from the router",
            inputSchema={
                "type": "object",
                "properties": {
                    "hostname": {"type": "string"},
                    "server": {"type": "string"}
                },
                "required": ["hostname"]
            },
        ),
        Tool(
            name="mikrotik_check_connection",
            description="Check if a port/host is reachable",
            inputSchema={
                "type": "object",
                "properties": {
                    "address": {"type": "string"},
                    "port": {"type": "integer"},
                    "protocol": {"type": "string", "enum": ["tcp", "udp"]}
                },
                "required": ["address"]
            },
        ),
        Tool(
            name="mikrotik_get_arp_table",
            description="Get ARP table entries",
            inputSchema={
                "type": "object",
                "properties": {
                    "interface": {"type": "string"},
                    "address": {"type": "string"}
                },
                "required": []
            },
        ),
        Tool(
            name="mikrotik_get_neighbors",
            description="Get neighboring MikroTik devices via MAC discovery",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
    ]

def get_diagnostic_handlers() -> Dict[str, Callable]:
    """Return the handlers for network diagnostic tools."""
    return {
        "mikrotik_ping": lambda args: mikrotik_ping(
            args["address"],
            args.get("count", 4),
            args.get("size"),
            args.get("interval"),
            args.get("src_address"),
            args.get("interface")
        ),
        "mikrotik_traceroute": lambda args: mikrotik_traceroute(
            args["address"],
            args.get("src_address"),
            args.get("interface"),
            args.get("max_hops")
        ),
        "mikrotik_bandwidth_test": lambda args: mikrotik_bandwidth_test(
            args["address"],
            args.get("duration", 10),
            args.get("direction", "both"),
            args.get("protocol", "tcp"),
            args.get("local_tx_speed"),
            args.get("remote_tx_speed")
        ),
        "mikrotik_dns_lookup": lambda args: mikrotik_dns_lookup(
            args["hostname"],
            args.get("server")
        ),
        "mikrotik_check_connection": lambda args: mikrotik_check_connection(
            args["address"],
            args.get("port"),
            args.get("protocol", "tcp")
        ),
        "mikrotik_get_arp_table": lambda args: mikrotik_get_arp_table(
            args.get("interface"),
            args.get("address")
        ),
        "mikrotik_get_neighbors": lambda args: mikrotik_get_neighbors(),
    }

