from typing import Dict, Any, List, Callable
from ..scope.config import mikrotik_config_set, mikrotik_config_get
from mcp.types import Tool

def get_config_tools() -> List[Tool]:
    """Return the list of configuration tools."""
    return [
        # Configuration tools
        Tool(
            name="mikrotik_config_set",
            description="Updates MikroTik connection configuration",
            inputSchema={
                "type": "object",
                "properties": {
                    "host": {"type": "string"},
                    "username": {"type": "string"},
                    "password": {"type": "string"},
                    "port": {"type": "integer"}
                },
                "required": []
            },
        ),
        Tool(
            name="mikrotik_config_get",
            description="Shows current MikroTik connection configuration",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
    ]

def get_config_handlers() -> Dict[str, Callable]:
    """Return the handlers for configuration tools."""
    return {
        "mikrotik_config_set": lambda args: mikrotik_config_set(
            args.get("host"),
            args.get("username"),
            args.get("password"),
            args.get("port")
        ),
        "mikrotik_config_get": lambda args: mikrotik_config_get(),
    }
