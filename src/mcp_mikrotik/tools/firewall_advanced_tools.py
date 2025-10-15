"""
Advanced firewall tool definitions (Mangle, RAW, Connection Tracking, Layer 7).
"""
from typing import Dict, Any, List, Callable
from ..scope.firewall_mangle import (
    mikrotik_list_mangle_rules,
    mikrotik_create_mangle_rule,
    mikrotik_remove_mangle_rule,
    mikrotik_update_mangle_rule,
    mikrotik_create_routing_mark,
    mikrotik_list_routing_marks
)
from ..scope.firewall_raw import (
    mikrotik_list_raw_rules,
    mikrotik_create_raw_rule,
    mikrotik_remove_raw_rule
)
from ..scope.firewall_connection import (
    mikrotik_get_connection_tracking,
    mikrotik_flush_connections
)
from ..scope.firewall_layer7 import (
    mikrotik_list_layer7_protocols,
    mikrotik_create_layer7_protocol,
    mikrotik_get_layer7_protocol,
    mikrotik_update_layer7_protocol,
    mikrotik_remove_layer7_protocol,
    mikrotik_enable_layer7_protocol,
    mikrotik_disable_layer7_protocol,
    mikrotik_create_common_layer7_protocols
)
from ..scope.firewall_chains import (
    mikrotik_list_custom_chains,
    mikrotik_create_jump_rule,
    mikrotik_list_rules_in_chain,
    mikrotik_delete_custom_chain,
    mikrotik_create_custom_chain_with_rules
)
from mcp.types import Tool


def get_firewall_advanced_tools() -> List[Tool]:
    """Return advanced firewall tools (mangle, raw, connection tracking)."""
    return [
        # Mangle tools
        Tool(
            name="mikrotik_list_mangle_rules",
            description="List firewall mangle rules (READ-ONLY, safe)",
            inputSchema={
                "type": "object",
                "properties": {
                    "chain_filter": {"type": "string"},
                    "action_filter": {"type": "string"},
                    "disabled_only": {"type": "boolean"}
                },
                "required": []
            },
        ),
        Tool(
            name="mikrotik_create_mangle_rule",
            description="Create firewall mangle rule for packet/connection/routing marking",
            inputSchema={
                "type": "object",
                "properties": {
                    "chain": {"type": "string", "enum": ["prerouting", "postrouting", "input", "output", "forward"]},
                    "mangle_action": {"type": "string"},
                    "src_address": {"type": "string"},
                    "dst_address": {"type": "string"},
                    "protocol": {"type": "string"},
                    "src_port": {"type": "string"},
                    "dst_port": {"type": "string"},
                    "in_interface": {"type": "string"},
                    "out_interface": {"type": "string"},
                    "new_packet_mark": {"type": "string"},
                    "new_connection_mark": {"type": "string"},
                    "new_routing_mark": {"type": "string"},
                    "passthrough": {"type": "boolean"},
                    "comment": {"type": "string"}
                },
                "required": ["chain", "mangle_action"]
            },
        ),
        Tool(
            name="mikrotik_remove_mangle_rule",
            description="Remove firewall mangle rule",
            inputSchema={
                "type": "object",
                "properties": {
                    "rule_id": {"type": "string"}
                },
                "required": ["rule_id"]
            },
        ),
        Tool(
            name="mikrotik_update_mangle_rule",
            description="Update firewall mangle rule",
            inputSchema={
                "type": "object",
                "properties": {
                    "rule_id": {"type": "string"},
                    "mangle_action": {"type": "string"},
                    "new_packet_mark": {"type": "string"},
                    "new_connection_mark": {"type": "string"},
                    "new_routing_mark": {"type": "string"},
                    "disabled": {"type": "boolean"},
                    "comment": {"type": "string"}
                },
                "required": ["rule_id"]
            },
        ),
        Tool(
            name="mikrotik_create_routing_mark",
            description="Create routing mark for policy-based routing (helper)",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "src_address": {"type": "string"},
                    "dst_address": {"type": "string"},
                    "in_interface": {"type": "string"},
                    "comment": {"type": "string"}
                },
                "required": ["name"]
            },
        ),
        Tool(
            name="mikrotik_list_routing_marks",
            description="List all routing marks (READ-ONLY, safe)",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        # RAW tools
        Tool(
            name="mikrotik_list_raw_rules",
            description="List firewall RAW rules (READ-ONLY, safe)",
            inputSchema={
                "type": "object",
                "properties": {
                    "chain_filter": {"type": "string"},
                    "disabled_only": {"type": "boolean"}
                },
                "required": []
            },
        ),
        Tool(
            name="mikrotik_create_raw_rule",
            description="Create firewall RAW rule (bypasses connection tracking)",
            inputSchema={
                "type": "object",
                "properties": {
                    "chain": {"type": "string", "enum": ["prerouting", "output"]},
                    "raw_action": {"type": "string", "enum": ["accept", "drop", "notrack"]},
                    "src_address": {"type": "string"},
                    "dst_address": {"type": "string"},
                    "protocol": {"type": "string"},
                    "src_port": {"type": "string"},
                    "dst_port": {"type": "string"},
                    "in_interface": {"type": "string"},
                    "out_interface": {"type": "string"},
                    "comment": {"type": "string"}
                },
                "required": ["chain", "raw_action"]
            },
        ),
        Tool(
            name="mikrotik_remove_raw_rule",
            description="Remove firewall RAW rule",
            inputSchema={
                "type": "object",
                "properties": {
                    "rule_id": {"type": "string"}
                },
                "required": ["rule_id"]
            },
        ),
        # Connection tracking tools
        Tool(
            name="mikrotik_get_connection_tracking",
            description="View active connections (READ-ONLY, safe)",
            inputSchema={
                "type": "object",
                "properties": {
                    "protocol_filter": {"type": "string"},
                    "src_address_filter": {"type": "string"},
                    "dst_address_filter": {"type": "string"},
                    "limit": {"type": "integer"}
                },
                "required": []
            },
        ),
        Tool(
            name="mikrotik_flush_connections",
            description="Flush connections from tracking table (⚠️ terminates connections!)",
            inputSchema={
                "type": "object",
                "properties": {
                    "protocol": {"type": "string"},
                    "src_address": {"type": "string"},
                    "dst_address": {"type": "string"}
                },
                "required": []
            },
        ),
        # Layer 7 protocol tools
        Tool(
            name="mikrotik_list_layer7_protocols",
            description="List Layer 7 protocol matchers (READ-ONLY, safe)",
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
            name="mikrotik_create_layer7_protocol",
            description="Create Layer 7 protocol matcher for deep packet inspection",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "regexp": {"type": "string"},
                    "comment": {"type": "string"},
                    "disabled": {"type": "boolean"}
                },
                "required": ["name", "regexp"]
            },
        ),
        Tool(
            name="mikrotik_get_layer7_protocol",
            description="Get Layer 7 protocol matcher details (READ-ONLY, safe)",
            inputSchema={
                "type": "object",
                "properties": {
                    "protocol_id": {"type": "string"}
                },
                "required": ["protocol_id"]
            },
        ),
        Tool(
            name="mikrotik_update_layer7_protocol",
            description="Update Layer 7 protocol matcher",
            inputSchema={
                "type": "object",
                "properties": {
                    "protocol_id": {"type": "string"},
                    "name": {"type": "string"},
                    "regexp": {"type": "string"},
                    "comment": {"type": "string"},
                    "disabled": {"type": "boolean"}
                },
                "required": ["protocol_id"]
            },
        ),
        Tool(
            name="mikrotik_remove_layer7_protocol",
            description="Remove Layer 7 protocol matcher",
            inputSchema={
                "type": "object",
                "properties": {
                    "protocol_id": {"type": "string"}
                },
                "required": ["protocol_id"]
            },
        ),
        Tool(
            name="mikrotik_enable_layer7_protocol",
            description="Enable Layer 7 protocol matcher",
            inputSchema={
                "type": "object",
                "properties": {
                    "protocol_id": {"type": "string"}
                },
                "required": ["protocol_id"]
            },
        ),
        Tool(
            name="mikrotik_disable_layer7_protocol",
            description="Disable Layer 7 protocol matcher",
            inputSchema={
                "type": "object",
                "properties": {
                    "protocol_id": {"type": "string"}
                },
                "required": ["protocol_id"]
            },
        ),
        Tool(
            name="mikrotik_create_common_layer7_protocols",
            description="Create common Layer 7 protocol matchers (YouTube, Netflix, Facebook, etc.)",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        # Custom chains tools
        Tool(
            name="mikrotik_list_custom_chains",
            description="List all custom firewall chains in use (READ-ONLY, safe)",
            inputSchema={
                "type": "object",
                "properties": {
                    "chain_type": {"type": "string", "enum": ["filter", "nat", "mangle", "raw"], "default": "filter"}
                },
                "required": []
            },
        ),
        Tool(
            name="mikrotik_create_jump_rule",
            description="Create a jump rule to redirect traffic to a custom chain",
            inputSchema={
                "type": "object",
                "properties": {
                    "chain_type": {"type": "string", "enum": ["filter", "nat", "mangle", "raw"]},
                    "source_chain": {"type": "string"},
                    "target_chain": {"type": "string"},
                    "src_address": {"type": "string"},
                    "dst_address": {"type": "string"},
                    "protocol": {"type": "string"},
                    "src_port": {"type": "string"},
                    "dst_port": {"type": "string"},
                    "in_interface": {"type": "string"},
                    "out_interface": {"type": "string"},
                    "comment": {"type": "string"},
                    "place_before": {"type": "string"}
                },
                "required": ["chain_type", "source_chain", "target_chain"]
            },
        ),
        Tool(
            name="mikrotik_list_rules_in_chain",
            description="List all rules in a specific firewall chain (READ-ONLY, safe)",
            inputSchema={
                "type": "object",
                "properties": {
                    "chain_type": {"type": "string", "enum": ["filter", "nat", "mangle", "raw"]},
                    "chain_name": {"type": "string"}
                },
                "required": ["chain_type", "chain_name"]
            },
        ),
        Tool(
            name="mikrotik_delete_custom_chain",
            description="Delete a custom chain and all its rules (⚠️ destructive!)",
            inputSchema={
                "type": "object",
                "properties": {
                    "chain_type": {"type": "string", "enum": ["filter", "nat", "mangle", "raw"]},
                    "chain_name": {"type": "string"}
                },
                "required": ["chain_type", "chain_name"]
            },
        ),
        Tool(
            name="mikrotik_create_custom_chain_with_rules",
            description="Create a complete custom chain with jump rule and rules inside it",
            inputSchema={
                "type": "object",
                "properties": {
                    "chain_type": {"type": "string", "enum": ["filter", "nat", "mangle", "raw"]},
                    "source_chain": {"type": "string"},
                    "custom_chain_name": {"type": "string"},
                    "rules": {"type": "array"},
                    "match_criteria": {"type": "object"}
                },
                "required": ["chain_type", "source_chain", "custom_chain_name", "rules"]
            },
        ),
    ]


def get_firewall_advanced_handlers() -> Dict[str, Callable]:
    """Return handlers for advanced firewall tools."""
    return {
        # Mangle handlers
        "mikrotik_list_mangle_rules": lambda args: mikrotik_list_mangle_rules(
            args.get("chain_filter"),
            args.get("action_filter"),
            args.get("disabled_only", False)
        ),
        "mikrotik_create_mangle_rule": lambda args: mikrotik_create_mangle_rule(
            args["chain"],
            args["mangle_action"],
            args.get("src_address"),
            args.get("dst_address"),
            args.get("protocol"),
            args.get("src_port"),
            args.get("dst_port"),
            args.get("in_interface"),
            args.get("out_interface"),
            args.get("new_packet_mark"),
            args.get("new_connection_mark"),
            args.get("new_routing_mark"),
            args.get("passthrough", True),
            args.get("comment")
        ),
        "mikrotik_remove_mangle_rule": lambda args: mikrotik_remove_mangle_rule(
            args["rule_id"]
        ),
        "mikrotik_update_mangle_rule": lambda args: mikrotik_update_mangle_rule(
            args["rule_id"],
            args.get("mangle_action"),
            args.get("new_packet_mark"),
            args.get("new_connection_mark"),
            args.get("new_routing_mark"),
            args.get("disabled"),
            args.get("comment")
        ),
        "mikrotik_create_routing_mark": lambda args: mikrotik_create_routing_mark(
            args["name"],
            args.get("src_address"),
            args.get("dst_address"),
            args.get("in_interface"),
            args.get("comment")
        ),
        "mikrotik_list_routing_marks": lambda args: mikrotik_list_routing_marks(),
        # RAW handlers
        "mikrotik_list_raw_rules": lambda args: mikrotik_list_raw_rules(
            args.get("chain_filter"),
            args.get("disabled_only", False)
        ),
        "mikrotik_create_raw_rule": lambda args: mikrotik_create_raw_rule(
            args["chain"],
            args["raw_action"],
            args.get("src_address"),
            args.get("dst_address"),
            args.get("protocol"),
            args.get("src_port"),
            args.get("dst_port"),
            args.get("in_interface"),
            args.get("out_interface"),
            args.get("comment")
        ),
        "mikrotik_remove_raw_rule": lambda args: mikrotik_remove_raw_rule(
            args["rule_id"]
        ),
        # Connection tracking handlers
        "mikrotik_get_connection_tracking": lambda args: mikrotik_get_connection_tracking(
            args.get("protocol_filter"),
            args.get("src_address_filter"),
            args.get("dst_address_filter"),
            args.get("limit", 100)
        ),
        "mikrotik_flush_connections": lambda args: mikrotik_flush_connections(
            args.get("protocol"),
            args.get("src_address"),
            args.get("dst_address")
        ),
        # Layer 7 protocol handlers
        "mikrotik_list_layer7_protocols": lambda args: mikrotik_list_layer7_protocols(
            args.get("name_filter"),
            args.get("disabled_only", False)
        ),
        "mikrotik_create_layer7_protocol": lambda args: mikrotik_create_layer7_protocol(
            args["name"],
            args["regexp"],
            args.get("comment"),
            args.get("disabled", False)
        ),
        "mikrotik_get_layer7_protocol": lambda args: mikrotik_get_layer7_protocol(
            args["protocol_id"]
        ),
        "mikrotik_update_layer7_protocol": lambda args: mikrotik_update_layer7_protocol(
            args["protocol_id"],
            args.get("name"),
            args.get("regexp"),
            args.get("comment"),
            args.get("disabled")
        ),
        "mikrotik_remove_layer7_protocol": lambda args: mikrotik_remove_layer7_protocol(
            args["protocol_id"]
        ),
        "mikrotik_enable_layer7_protocol": lambda args: mikrotik_enable_layer7_protocol(
            args["protocol_id"]
        ),
        "mikrotik_disable_layer7_protocol": lambda args: mikrotik_disable_layer7_protocol(
            args["protocol_id"]
        ),
        "mikrotik_create_common_layer7_protocols": lambda args: mikrotik_create_common_layer7_protocols(),
        # Custom chains handlers
        "mikrotik_list_custom_chains": lambda args: mikrotik_list_custom_chains(
            args.get("chain_type", "filter")
        ),
        "mikrotik_create_jump_rule": lambda args: mikrotik_create_jump_rule(
            args["chain_type"],
            args["source_chain"],
            args["target_chain"],
            args.get("src_address"),
            args.get("dst_address"),
            args.get("protocol"),
            args.get("src_port"),
            args.get("dst_port"),
            args.get("in_interface"),
            args.get("out_interface"),
            args.get("comment"),
            args.get("place_before")
        ),
        "mikrotik_list_rules_in_chain": lambda args: mikrotik_list_rules_in_chain(
            args["chain_type"],
            args["chain_name"]
        ),
        "mikrotik_delete_custom_chain": lambda args: mikrotik_delete_custom_chain(
            args["chain_type"],
            args["chain_name"]
        ),
        "mikrotik_create_custom_chain_with_rules": lambda args: mikrotik_create_custom_chain_with_rules(
            args["chain_type"],
            args["source_chain"],
            args["custom_chain_name"],
            args["rules"],
            args.get("match_criteria")
        ),
    }



