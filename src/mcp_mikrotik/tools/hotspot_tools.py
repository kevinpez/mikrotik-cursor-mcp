"""
Hotspot tool definitions for MCP server.
"""
from typing import Dict, Any, List, Callable
from ..scope.hotspot import (
    mikrotik_list_hotspot_servers, mikrotik_create_hotspot_server, mikrotik_remove_hotspot_server,
    mikrotik_list_hotspot_users, mikrotik_create_hotspot_user, mikrotik_list_hotspot_active,
    mikrotik_list_hotspot_profiles, mikrotik_create_hotspot_profile,
    mikrotik_list_walled_garden, mikrotik_add_walled_garden
)
from mcp.types import Tool


def get_hotspot_tools() -> List[Tool]:
    """Return hotspot management tools."""
    return [
        Tool(
            name="mikrotik_list_hotspot_servers",
            description="List hotspot servers (READ-ONLY, safe)",
            inputSchema={"type": "object", "properties": {"name_filter": {"type": "string"}}, "required": []},
        ),
        Tool(
            name="mikrotik_create_hotspot_server",
            description="Create hotspot server on interface",
            inputSchema={"type": "object", "properties": {"name": {"type": "string"}, "interface": {"type": "string"}, "address_pool": {"type": "string"}, "profile": {"type": "string"}, "comment": {"type": "string"}}, "required": ["name", "interface", "address_pool"]},
        ),
        Tool(
            name="mikrotik_remove_hotspot_server",
            description="Remove hotspot server",
            inputSchema={"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]},
        ),
        Tool(
            name="mikrotik_list_hotspot_users",
            description="List hotspot users (READ-ONLY, safe)",
            inputSchema={"type": "object", "properties": {"server_filter": {"type": "string"}}, "required": []},
        ),
        Tool(
            name="mikrotik_create_hotspot_user",
            description="Create hotspot user with credentials",
            inputSchema={"type": "object", "properties": {"name": {"type": "string"}, "password": {"type": "string"}, "server": {"type": "string"}, "profile": {"type": "string"}, "limit_uptime": {"type": "string"}, "comment": {"type": "string"}}, "required": ["name", "password"]},
        ),
        Tool(
            name="mikrotik_list_hotspot_active",
            description="List active hotspot sessions (READ-ONLY, safe)",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="mikrotik_list_hotspot_profiles",
            description="List hotspot profiles (READ-ONLY, safe)",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="mikrotik_create_hotspot_profile",
            description="Create hotspot profile with bandwidth/time limits",
            inputSchema={"type": "object", "properties": {"name": {"type": "string"}, "rate_limit": {"type": "string"}, "session_timeout": {"type": "string"}, "idle_timeout": {"type": "string"}, "shared_users": {"type": "integer"}, "comment": {"type": "string"}}, "required": ["name"]},
        ),
        Tool(
            name="mikrotik_list_walled_garden",
            description="List walled garden entries (READ-ONLY, safe)",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="mikrotik_add_walled_garden",
            description="Add site to walled garden (accessible without login)",
            inputSchema={"type": "object", "properties": {"dst_host": {"type": "string"}, "comment": {"type": "string"}}, "required": ["dst_host"]},
        ),
    ]


def get_hotspot_handlers() -> Dict[str, Callable]:
    """Return handlers for hotspot tools."""
    return {
        "mikrotik_list_hotspot_servers": lambda args: mikrotik_list_hotspot_servers(args.get("name_filter")),
        "mikrotik_create_hotspot_server": lambda args: mikrotik_create_hotspot_server(args["name"], args["interface"], args["address_pool"], args.get("profile", "default"), args.get("comment")),
        "mikrotik_remove_hotspot_server": lambda args: mikrotik_remove_hotspot_server(args["name"]),
        "mikrotik_list_hotspot_users": lambda args: mikrotik_list_hotspot_users(args.get("server_filter")),
        "mikrotik_create_hotspot_user": lambda args: mikrotik_create_hotspot_user(args["name"], args["password"], args.get("server", "all"), args.get("profile", "default"), args.get("limit_uptime"), args.get("comment")),
        "mikrotik_list_hotspot_active": lambda args: mikrotik_list_hotspot_active(),
        "mikrotik_list_hotspot_profiles": lambda args: mikrotik_list_hotspot_profiles(),
        "mikrotik_create_hotspot_profile": lambda args: mikrotik_create_hotspot_profile(args["name"], args.get("rate_limit"), args.get("session_timeout"), args.get("idle_timeout"), args.get("shared_users", 1), args.get("comment")),
        "mikrotik_list_walled_garden": lambda args: mikrotik_list_walled_garden(),
        "mikrotik_add_walled_garden": lambda args: mikrotik_add_walled_garden(args["dst_host"], args.get("comment")),
    }

