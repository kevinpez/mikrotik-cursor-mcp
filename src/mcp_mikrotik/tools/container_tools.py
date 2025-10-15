from typing import Dict, Any, List, Callable
from ..scope.container import (
    mikrotik_list_containers, mikrotik_create_container, mikrotik_remove_container,
    mikrotik_start_container, mikrotik_stop_container, mikrotik_get_container,
    mikrotik_get_container_config, mikrotik_set_container_registry,
    mikrotik_set_container_tmpdir, mikrotik_list_container_envs,
    mikrotik_create_container_env, mikrotik_remove_container_env,
    mikrotik_list_container_mounts, mikrotik_create_container_mount,
    mikrotik_remove_container_mount, mikrotik_list_container_veths,
    mikrotik_create_container_veth, mikrotik_remove_container_veth
)
from mcp.types import Tool


def get_container_tools() -> List[Tool]:
    """Return container management tools."""
    return [
        # Container Management
        Tool(
            name="mikrotik_list_containers",
            description="Lists all containers",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        Tool(
            name="mikrotik_create_container",
            description="Creates a container",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Container name"},
                    "image": {"type": "string", "description": "Container image"},
                    "interface": {"type": "string", "description": "Network interface"},
                    "envlist": {"type": "string", "description": "Environment list"},
                    "root_dir": {"type": "string", "description": "Root directory"},
                    "cmd": {"type": "string", "description": "Command to execute"},
                    "mounts": {"type": "string", "description": "Mount points"},
                    "start": {"type": "boolean", "description": "Start after creation"},
                    "comment": {"type": "string", "description": "Comment"}
                },
                "required": ["name", "image"]
            },
        ),
        Tool(
            name="mikrotik_remove_container",
            description="Removes a container",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Container name"}
                },
                "required": ["name"]
            },
        ),
        Tool(
            name="mikrotik_start_container",
            description="Starts a container",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Container name"}
                },
                "required": ["name"]
            },
        ),
        Tool(
            name="mikrotik_stop_container",
            description="Stops a container",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Container name"}
                },
                "required": ["name"]
            },
        ),
        Tool(
            name="mikrotik_get_container",
            description="Gets container details",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Container name"}
                },
                "required": ["name"]
            },
        ),
        
        # Container Config
        Tool(
            name="mikrotik_get_container_config",
            description="Gets container configuration",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        Tool(
            name="mikrotik_set_container_registry",
            description="Sets container registry",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "Registry URL"},
                    "username": {"type": "string", "description": "Username"},
                    "password": {"type": "string", "description": "Password"}
                },
                "required": ["url"]
            },
        ),
        Tool(
            name="mikrotik_set_container_tmpdir",
            description="Sets container tmpdir",
            inputSchema={
                "type": "object",
                "properties": {
                    "tmpdir": {"type": "string", "description": "Temporary directory"}
                },
                "required": ["tmpdir"]
            },
        ),
        
        # Container Environments
        Tool(
            name="mikrotik_list_container_envs",
            description="Lists container environments",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        Tool(
            name="mikrotik_create_container_env",
            description="Creates container environment variable",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Environment name"},
                    "key": {"type": "string", "description": "Variable key"},
                    "value": {"type": "string", "description": "Variable value"}
                },
                "required": ["name", "key", "value"]
            },
        ),
        Tool(
            name="mikrotik_remove_container_env",
            description="Removes container environment",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Environment name"}
                },
                "required": ["name"]
            },
        ),
        
        # Container Mounts
        Tool(
            name="mikrotik_list_container_mounts",
            description="Lists container mounts",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        Tool(
            name="mikrotik_create_container_mount",
            description="Creates container mount point",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Mount name"},
                    "src": {"type": "string", "description": "Source path"},
                    "dst": {"type": "string", "description": "Destination path"}
                },
                "required": ["name", "src", "dst"]
            },
        ),
        Tool(
            name="mikrotik_remove_container_mount",
            description="Removes container mount",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Mount name"}
                },
                "required": ["name"]
            },
        ),
        
        # Container VETHs
        Tool(
            name="mikrotik_list_container_veths",
            description="Lists container veth interfaces",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        Tool(
            name="mikrotik_create_container_veth",
            description="Creates container veth interface",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Veth name"},
                    "address": {"type": "string", "description": "IP address"},
                    "gateway": {"type": "string", "description": "Gateway"}
                },
                "required": ["name"]
            },
        ),
        Tool(
            name="mikrotik_remove_container_veth",
            description="Removes container veth interface",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Veth name"}
                },
                "required": ["name"]
            },
        ),
    ]


def get_container_handlers() -> Dict[str, Callable]:
    """Return container handlers."""
    return {
        "mikrotik_list_containers": lambda args: mikrotik_list_containers(),
        "mikrotik_create_container": lambda args: mikrotik_create_container(
            name=args["name"],
            image=args["image"],
            interface=args.get("interface"),
            envlist=args.get("envlist"),
            root_dir=args.get("root_dir"),
            cmd=args.get("cmd"),
            mounts=args.get("mounts"),
            start=args.get("start", True),
            comment=args.get("comment")
        ),
        "mikrotik_remove_container": lambda args: mikrotik_remove_container(
            args["name"]
        ),
        "mikrotik_start_container": lambda args: mikrotik_start_container(
            args["name"]
        ),
        "mikrotik_stop_container": lambda args: mikrotik_stop_container(
            args["name"]
        ),
        "mikrotik_get_container": lambda args: mikrotik_get_container(
            args["name"]
        ),
        "mikrotik_get_container_config": lambda args: mikrotik_get_container_config(),
        "mikrotik_set_container_registry": lambda args: mikrotik_set_container_registry(
            url=args["url"],
            username=args.get("username"),
            password=args.get("password")
        ),
        "mikrotik_set_container_tmpdir": lambda args: mikrotik_set_container_tmpdir(
            args["tmpdir"]
        ),
        "mikrotik_list_container_envs": lambda args: mikrotik_list_container_envs(),
        "mikrotik_create_container_env": lambda args: mikrotik_create_container_env(
            name=args["name"],
            key=args["key"],
            value=args["value"]
        ),
        "mikrotik_remove_container_env": lambda args: mikrotik_remove_container_env(
            args["name"]
        ),
        "mikrotik_list_container_mounts": lambda args: mikrotik_list_container_mounts(),
        "mikrotik_create_container_mount": lambda args: mikrotik_create_container_mount(
            name=args["name"],
            src=args["src"],
            dst=args["dst"]
        ),
        "mikrotik_remove_container_mount": lambda args: mikrotik_remove_container_mount(
            args["name"]
        ),
        "mikrotik_list_container_veths": lambda args: mikrotik_list_container_veths(),
        "mikrotik_create_container_veth": lambda args: mikrotik_create_container_veth(
            name=args["name"],
            address=args.get("address"),
            gateway=args.get("gateway")
        ),
        "mikrotik_remove_container_veth": lambda args: mikrotik_remove_container_veth(
            args["name"]
        ),
    }


