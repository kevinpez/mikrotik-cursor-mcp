from typing import Dict, Any, List, Callable
from ..scope.logs import (
    mikrotik_get_logs, mikrotik_get_logs_by_severity, mikrotik_get_logs_by_topic,
    mikrotik_search_logs, mikrotik_get_system_events, mikrotik_get_security_logs,
    mikrotik_clear_logs, mikrotik_get_log_statistics, mikrotik_export_logs,
    mikrotik_monitor_logs
)
from mcp.types import Tool

def get_log_tools() -> List[Tool]:
    """Return the list of log tools."""
    return [
        # Log tools
        Tool(
            name="mikrotik_get_logs",
            description="Gets logs from MikroTik device with filtering options",
            inputSchema={
                "type": "object",
                "properties": {
                    "topics": {"type": "string"},
                    "action": {"type": "string"},
                    "time_filter": {"type": "string"},
                    "message_filter": {"type": "string"},
                    "prefix_filter": {"type": "string"},
                    "limit": {"type": "integer"},
                    "follow": {"type": "boolean"},
                    "print_as": {"type": "string", "enum": ["value", "detail", "terse"]}
                },
                "required": []
            },
        ),
        Tool(
            name="mikrotik_get_logs_by_severity",
            description="Gets logs filtered by severity level",
            inputSchema={
                "type": "object",
                "properties": {
                    "severity": {"type": "string", "enum": ["debug", "info", "warning", "error", "critical"]},
                    "time_filter": {"type": "string"},
                    "limit": {"type": "integer"}
                },
                "required": ["severity"]
            },
        ),
        Tool(
            name="mikrotik_get_logs_by_topic",
            description="Gets logs for a specific topic/facility",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {"type": "string"},
                    "time_filter": {"type": "string"},
                    "limit": {"type": "integer"}
                },
                "required": ["topic"]
            },
        ),
        Tool(
            name="mikrotik_search_logs",
            description="Searches logs for a specific term",
            inputSchema={
                "type": "object",
                "properties": {
                    "search_term": {"type": "string"},
                    "time_filter": {"type": "string"},
                    "case_sensitive": {"type": "boolean"},
                    "limit": {"type": "integer"}
                },
                "required": ["search_term"]
            },
        ),
        Tool(
            name="mikrotik_get_system_events",
            description="Gets system-related log events",
            inputSchema={
                "type": "object",
                "properties": {
                    "event_type": {"type": "string"},
                    "time_filter": {"type": "string"},
                    "limit": {"type": "integer"}
                },
                "required": []
            },
        ),
        Tool(
            name="mikrotik_get_security_logs",
            description="Gets security-related log entries",
            inputSchema={
                "type": "object",
                "properties": {
                    "time_filter": {"type": "string"},
                    "limit": {"type": "integer"}
                },
                "required": []
            },
        ),
        Tool(
            name="mikrotik_clear_logs",
            description="Clears all logs from MikroTik device",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        Tool(
            name="mikrotik_get_log_statistics",
            description="Gets statistics about log entries",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        Tool(
            name="mikrotik_export_logs",
            description="Exports logs to a file on the MikroTik device",
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {"type": "string"},
                    "topics": {"type": "string"},
                    "time_filter": {"type": "string"},
                    "format": {"type": "string", "enum": ["plain", "csv"]}
                },
                "required": []
            },
        ),
        Tool(
            name="mikrotik_monitor_logs",
            description="Monitors logs in real-time for a specified duration",
            inputSchema={
                "type": "object",
                "properties": {
                    "topics": {"type": "string"},
                    "action": {"type": "string"},
                    "duration": {"type": "integer"}
                },
                "required": []
            },
        ),
    ]

def get_log_handlers() -> Dict[str, Callable]:
    """Return the handlers for log tools."""
    return {
        "mikrotik_get_logs": lambda args: mikrotik_get_logs(
            args.get("topics"),
            args.get("action"),
            args.get("time_filter"),
            args.get("message_filter"),
            args.get("prefix_filter"),
            args.get("limit"),
            args.get("follow", False),
            args.get("print_as", "value")
        ),
        "mikrotik_get_logs_by_severity": lambda args: mikrotik_get_logs_by_severity(
            args["severity"],
            args.get("time_filter"),
            args.get("limit")
        ),
        "mikrotik_get_logs_by_topic": lambda args: mikrotik_get_logs_by_topic(
            args["topic"],
            args.get("time_filter"),
            args.get("limit")
        ),
        "mikrotik_search_logs": lambda args: mikrotik_search_logs(
            args["search_term"],
            args.get("time_filter"),
            args.get("case_sensitive", False),
            args.get("limit")
        ),
        "mikrotik_get_system_events": lambda args: mikrotik_get_system_events(
            args.get("event_type"),
            args.get("time_filter"),
            args.get("limit")
        ),
        "mikrotik_get_security_logs": lambda args: mikrotik_get_security_logs(
            args.get("time_filter"),
            args.get("limit")
        ),
        "mikrotik_clear_logs": lambda args: mikrotik_clear_logs(),
        "mikrotik_get_log_statistics": lambda args: mikrotik_get_log_statistics(),
        "mikrotik_export_logs": lambda args: mikrotik_export_logs(
            args.get("filename"),
            args.get("topics"),
            args.get("time_filter"),
            args.get("format", "plain")
        ),
        "mikrotik_monitor_logs": lambda args: mikrotik_monitor_logs(
            args.get("topics"),
            args.get("action"),
            args.get("duration", 10)
        ),
    }
