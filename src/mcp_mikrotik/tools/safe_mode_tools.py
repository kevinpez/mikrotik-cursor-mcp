"""
Safe Mode tools for MikroTik RouterOS.
Provides access to RouterOS's built-in safe mode functionality.
"""
from mcp.types import Tool
from ..scope import safe_mode


def get_safe_mode_tools() -> list[Tool]:
    """Get all safe mode related tools."""
    return [
        Tool(
            name="mikrotik_enter_safe_mode",
            description="Enter MikroTik Safe Mode for safe configuration changes with automatic rollback",
            inputSchema={
                "type": "object",
                "properties": {
                    "timeout_minutes": {
                        "type": "integer",
                        "description": "Optional timeout in minutes (default: 10 minutes). Changes will be automatically reverted after this time if Safe Mode is not explicitly exited.",
                        "minimum": 1,
                        "maximum": 60
                    }
                },
                "required": []
            },
        ),
        Tool(
            name="mikrotik_exit_safe_mode",
            description="Exit MikroTik Safe Mode and make all changes permanent",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        Tool(
            name="mikrotik_get_safe_mode_status",
            description="Get the current Safe Mode status and configuration",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        Tool(
            name="mikrotik_set_safe_mode_timeout",
            description="Set the Safe Mode timeout period (1-60 minutes)",
            inputSchema={
                "type": "object",
                "properties": {
                    "timeout_minutes": {
                        "type": "integer",
                        "description": "Timeout period in minutes (1-60). After this time, changes will be automatically reverted if Safe Mode is not explicitly exited.",
                        "minimum": 1,
                        "maximum": 60
                    }
                },
                "required": ["timeout_minutes"]
            },
        ),
        Tool(
            name="mikrotik_force_exit_safe_mode",
            description="Force exit Safe Mode immediately (emergency use only)",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        Tool(
            name="mikrotik_get_safe_mode_history",
            description="Get the history of changes made during the current Safe Mode session",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        Tool(
            name="mikrotik_create_safe_mode_backup",
            description="Create a backup before entering Safe Mode (recommended best practice)",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
    ]


def get_safe_mode_handlers() -> dict:
    """Get all safe mode tool handlers."""
    return {
        "mikrotik_enter_safe_mode": lambda args: safe_mode.mikrotik_enter_safe_mode(
            args.get("timeout_minutes")
        ),
        "mikrotik_exit_safe_mode": lambda args: safe_mode.mikrotik_exit_safe_mode(),
        "mikrotik_get_safe_mode_status": lambda args: safe_mode.mikrotik_get_safe_mode_status(),
        "mikrotik_set_safe_mode_timeout": lambda args: safe_mode.mikrotik_set_safe_mode_timeout(
            args["timeout_minutes"]
        ),
        "mikrotik_force_exit_safe_mode": lambda args: safe_mode.mikrotik_force_exit_safe_mode(),
        "mikrotik_get_safe_mode_history": lambda args: safe_mode.mikrotik_get_safe_mode_history(),
        "mikrotik_create_safe_mode_backup": lambda args: safe_mode.mikrotik_create_safe_mode_backup(),
    }
