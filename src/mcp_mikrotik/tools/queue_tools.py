from typing import Dict, Any, List, Callable
from ..scope.queues import (
    mikrotik_list_simple_queues, mikrotik_create_simple_queue, mikrotik_remove_simple_queue,
    mikrotik_enable_simple_queue, mikrotik_disable_simple_queue, mikrotik_update_simple_queue,
    mikrotik_list_queue_types
)
from ..scope.queue_tree import (
    mikrotik_list_queue_trees, mikrotik_get_queue_tree, mikrotik_create_queue_tree,
    mikrotik_update_queue_tree, mikrotik_remove_queue_tree, mikrotik_enable_queue_tree,
    mikrotik_disable_queue_tree, mikrotik_create_htb_queue_tree,
    mikrotik_create_priority_queue_tree, mikrotik_list_pcq_queues,
    mikrotik_create_pcq_queue, mikrotik_remove_pcq_queue,
    mikrotik_create_traffic_shaping_tree
)
from mcp.types import Tool

def get_queue_tools() -> List[Tool]:
    """Return the list of queue management tools."""
    return [
        Tool(
            name="mikrotik_list_simple_queues",
            description="Lists simple queues (bandwidth limits)",
            inputSchema={
                "type": "object",
                "properties": {
                    "name_filter": {"type": "string"},
                    "target_filter": {"type": "string"},
                    "disabled_only": {"type": "boolean"}
                },
                "required": []
            },
        ),
        Tool(
            name="mikrotik_create_simple_queue",
            description="Creates a simple queue (bandwidth limit for IP/subnet)",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "target": {"type": "string"},
                    "max_limit": {"type": "string"},
                    "limit_at": {"type": "string"},
                    "burst_limit": {"type": "string"},
                    "burst_threshold": {"type": "string"},
                    "burst_time": {"type": "string"},
                    "priority": {"type": "integer"},
                    "comment": {"type": "string"},
                    "disabled": {"type": "boolean"}
                },
                "required": ["name", "target", "max_limit"]
            },
        ),
        Tool(
            name="mikrotik_remove_simple_queue",
            description="Removes a simple queue",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"}
                },
                "required": ["name"]
            },
        ),
        Tool(
            name="mikrotik_enable_simple_queue",
            description="Enables a simple queue",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"}
                },
                "required": ["name"]
            },
        ),
        Tool(
            name="mikrotik_disable_simple_queue",
            description="Disables a simple queue",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"}
                },
                "required": ["name"]
            },
        ),
        Tool(
            name="mikrotik_update_simple_queue",
            description="Updates a simple queue configuration",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "max_limit": {"type": "string"},
                    "limit_at": {"type": "string"},
                    "burst_limit": {"type": "string"},
                    "burst_threshold": {"type": "string"},
                    "burst_time": {"type": "string"},
                    "priority": {"type": "integer"},
                    "comment": {"type": "string"}
                },
                "required": ["name"]
            },
        ),
        Tool(
            name="mikrotik_list_queue_types",
            description="Lists available queue types",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        # Queue Tree tools
        Tool(
            name="mikrotik_list_queue_trees",
            description="Lists queue tree entries (hierarchical QoS) (READ-ONLY, safe)",
            inputSchema={
                "type": "object",
                "properties": {
                    "name_filter": {"type": "string"},
                    "parent_filter": {"type": "string"},
                    "disabled_only": {"type": "boolean"},
                    "invalid_only": {"type": "boolean"}
                },
                "required": []
            },
        ),
        Tool(
            name="mikrotik_get_queue_tree",
            description="Gets detailed information about a queue tree (READ-ONLY, safe)",
            inputSchema={
                "type": "object",
                "properties": {
                    "queue_id": {"type": "string"}
                },
                "required": ["queue_id"]
            },
        ),
        Tool(
            name="mikrotik_create_queue_tree",
            description="Creates a queue tree entry for hierarchical bandwidth management",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "parent": {"type": "string", "description": "Parent queue or interface"},
                    "packet_mark": {"type": "string"},
                    "max_limit": {"type": "string", "description": "Max rate (e.g., '10M', '1G')"},
                    "limit_at": {"type": "string", "description": "Guaranteed rate"},
                    "priority": {"type": "integer", "default": 8},
                    "queue": {"type": "string", "default": "default"},
                    "burst_limit": {"type": "string"},
                    "burst_threshold": {"type": "string"},
                    "burst_time": {"type": "string"},
                    "comment": {"type": "string"},
                    "disabled": {"type": "boolean"}
                },
                "required": ["name", "parent"]
            },
        ),
        Tool(
            name="mikrotik_update_queue_tree",
            description="Updates queue tree settings",
            inputSchema={
                "type": "object",
                "properties": {
                    "queue_id": {"type": "string"},
                    "name": {"type": "string"},
                    "parent": {"type": "string"},
                    "packet_mark": {"type": "string"},
                    "max_limit": {"type": "string"},
                    "limit_at": {"type": "string"},
                    "priority": {"type": "integer"},
                    "queue": {"type": "string"},
                    "burst_limit": {"type": "string"},
                    "burst_threshold": {"type": "string"},
                    "burst_time": {"type": "string"},
                    "comment": {"type": "string"},
                    "disabled": {"type": "boolean"}
                },
                "required": ["queue_id"]
            },
        ),
        Tool(
            name="mikrotik_remove_queue_tree",
            description="Removes a queue tree entry",
            inputSchema={
                "type": "object",
                "properties": {
                    "queue_id": {"type": "string"}
                },
                "required": ["queue_id"]
            },
        ),
        Tool(
            name="mikrotik_enable_queue_tree",
            description="Enables a queue tree entry",
            inputSchema={
                "type": "object",
                "properties": {
                    "queue_id": {"type": "string"}
                },
                "required": ["queue_id"]
            },
        ),
        Tool(
            name="mikrotik_disable_queue_tree",
            description="Disables a queue tree entry",
            inputSchema={
                "type": "object",
                "properties": {
                    "queue_id": {"type": "string"}
                },
                "required": ["queue_id"]
            },
        ),
        Tool(
            name="mikrotik_create_htb_queue_tree",
            description="Creates hierarchical HTB queue tree structure",
            inputSchema={
                "type": "object",
                "properties": {
                    "interface": {"type": "string"},
                    "total_download": {"type": "string", "description": "Total download bandwidth (e.g., '100M')"},
                    "total_upload": {"type": "string", "description": "Total upload bandwidth (e.g., '20M')"}
                },
                "required": ["interface", "total_download", "total_upload"]
            },
        ),
        Tool(
            name="mikrotik_create_priority_queue_tree",
            description="Creates priority-based queue tree structure",
            inputSchema={
                "type": "object",
                "properties": {
                    "interface": {"type": "string"},
                    "total_bandwidth": {"type": "string"},
                    "priorities": {"type": "array"}
                },
                "required": ["interface", "total_bandwidth", "priorities"]
            },
        ),
        Tool(
            name="mikrotik_list_pcq_queues",
            description="Lists PCQ (Per Connection Queue) queue types (READ-ONLY, safe)",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        Tool(
            name="mikrotik_create_pcq_queue",
            description="Creates a PCQ queue type for per-connection bandwidth management",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "rate": {"type": "string", "description": "Data rate (e.g., '10M')"},
                    "classifier": {"type": "string", "enum": ["src-address", "dst-address", "src-port", "dst-port"]},
                    "pcq_limit": {"type": "integer", "default": 50},
                    "pcq_total_limit": {"type": "integer", "default": 2000},
                    "comment": {"type": "string"}
                },
                "required": ["name", "rate"]
            },
        ),
        Tool(
            name="mikrotik_remove_pcq_queue",
            description="Removes a PCQ queue type",
            inputSchema={
                "type": "object",
                "properties": {
                    "queue_name": {"type": "string"}
                },
                "required": ["queue_name"]
            },
        ),
        Tool(
            name="mikrotik_create_traffic_shaping_tree",
            description="Creates complete traffic shaping tree with multiple classes",
            inputSchema={
                "type": "object",
                "properties": {
                    "interface": {"type": "string"},
                    "total_bandwidth": {"type": "string"},
                    "traffic_classes": {"type": "array"}
                },
                "required": ["interface", "total_bandwidth", "traffic_classes"]
            },
        ),
    ]

def get_queue_handlers() -> Dict[str, Callable]:
    """Return the handlers for queue management tools."""
    return {
        "mikrotik_list_simple_queues": lambda args: mikrotik_list_simple_queues(
            args.get("name_filter"),
            args.get("target_filter"),
            args.get("disabled_only", False)
        ),
        "mikrotik_create_simple_queue": lambda args: mikrotik_create_simple_queue(
            args["name"],
            args["target"],
            args["max_limit"],
            args.get("limit_at"),
            args.get("burst_limit"),
            args.get("burst_threshold"),
            args.get("burst_time"),
            args.get("priority"),
            args.get("comment"),
            args.get("disabled", False)
        ),
        "mikrotik_remove_simple_queue": lambda args: mikrotik_remove_simple_queue(
            args["name"]
        ),
        "mikrotik_enable_simple_queue": lambda args: mikrotik_enable_simple_queue(
            args["name"]
        ),
        "mikrotik_disable_simple_queue": lambda args: mikrotik_disable_simple_queue(
            args["name"]
        ),
        "mikrotik_update_simple_queue": lambda args: mikrotik_update_simple_queue(
            args["name"],
            args.get("max_limit"),
            args.get("limit_at"),
            args.get("burst_limit"),
            args.get("burst_threshold"),
            args.get("burst_time"),
            args.get("priority"),
            args.get("comment")
        ),
        "mikrotik_list_queue_types": lambda args: mikrotik_list_queue_types(),
        # Queue Tree handlers
        "mikrotik_list_queue_trees": lambda args: mikrotik_list_queue_trees(
            args.get("name_filter"),
            args.get("parent_filter"),
            args.get("disabled_only", False),
            args.get("invalid_only", False)
        ),
        "mikrotik_get_queue_tree": lambda args: mikrotik_get_queue_tree(
            args["queue_id"]
        ),
        "mikrotik_create_queue_tree": lambda args: mikrotik_create_queue_tree(
            args["name"],
            args["parent"],
            args.get("packet_mark"),
            args.get("max_limit"),
            args.get("limit_at"),
            args.get("priority", 8),
            args.get("queue", "default"),
            args.get("burst_limit"),
            args.get("burst_threshold"),
            args.get("burst_time"),
            args.get("comment"),
            args.get("disabled", False)
        ),
        "mikrotik_update_queue_tree": lambda args: mikrotik_update_queue_tree(
            args["queue_id"],
            args.get("name"),
            args.get("parent"),
            args.get("packet_mark"),
            args.get("max_limit"),
            args.get("limit_at"),
            args.get("priority"),
            args.get("queue"),
            args.get("burst_limit"),
            args.get("burst_threshold"),
            args.get("burst_time"),
            args.get("comment"),
            args.get("disabled")
        ),
        "mikrotik_remove_queue_tree": lambda args: mikrotik_remove_queue_tree(
            args["queue_id"]
        ),
        "mikrotik_enable_queue_tree": lambda args: mikrotik_enable_queue_tree(
            args["queue_id"]
        ),
        "mikrotik_disable_queue_tree": lambda args: mikrotik_disable_queue_tree(
            args["queue_id"]
        ),
        "mikrotik_create_htb_queue_tree": lambda args: mikrotik_create_htb_queue_tree(
            args["interface"],
            args["total_download"],
            args["total_upload"]
        ),
        "mikrotik_create_priority_queue_tree": lambda args: mikrotik_create_priority_queue_tree(
            args["interface"],
            args["total_bandwidth"],
            args["priorities"]
        ),
        "mikrotik_list_pcq_queues": lambda args: mikrotik_list_pcq_queues(),
        "mikrotik_create_pcq_queue": lambda args: mikrotik_create_pcq_queue(
            args["name"],
            args["rate"],
            args.get("classifier"),
            args.get("pcq_limit", 50),
            args.get("pcq_total_limit", 2000),
            args.get("comment")
        ),
        "mikrotik_remove_pcq_queue": lambda args: mikrotik_remove_pcq_queue(
            args["queue_name"]
        ),
        "mikrotik_create_traffic_shaping_tree": lambda args: mikrotik_create_traffic_shaping_tree(
            args["interface"],
            args["total_bandwidth"],
            args["traffic_classes"]
        ),
    }

