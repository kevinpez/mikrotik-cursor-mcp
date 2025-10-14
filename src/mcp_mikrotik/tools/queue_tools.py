from typing import Dict, Any, List, Callable
from ..scope.queues import (
    mikrotik_list_simple_queues, mikrotik_create_simple_queue, mikrotik_remove_simple_queue,
    mikrotik_enable_simple_queue, mikrotik_disable_simple_queue, mikrotik_update_simple_queue,
    mikrotik_list_queue_types
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
    }

