from typing import Dict, Any, List, Callable
from ..scope.ip_services import (
    mikrotik_list_ip_services, mikrotik_get_ip_service, mikrotik_set_service_address,
    mikrotik_enable_ip_service, mikrotik_disable_ip_service, mikrotik_set_service_port,
    mikrotik_configure_secure_services, mikrotik_restore_default_services,
    mikrotik_get_service_status, mikrotik_create_service_backup
)
from mcp.types import Tool

def get_ip_services_tools() -> List[Tool]:
    """Return the list of IP services management tools."""
    return [
        # IP Services Management tools
        Tool(
            name="mikrotik_list_ip_services",
            description="List all IP services and their current configuration",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        Tool(
            name="mikrotik_get_ip_service",
            description="Get configuration for a specific IP service",
            inputSchema={
                "type": "object",
                "properties": {
                    "service_name": {
                        "type": "string",
                        "description": "Name of the service (ssh, winbox, api, telnet, ftp, etc.)"
                    }
                },
                "required": ["service_name"]
            },
        ),
        Tool(
            name="mikrotik_set_service_address",
            description="Set the 'Available From' address for an IP service to control access",
            inputSchema={
                "type": "object",
                "properties": {
                    "service_name": {
                        "type": "string",
                        "description": "Name of the service (ssh, winbox, api, telnet, ftp, etc.)"
                    },
                    "address": {
                        "type": "string",
                        "description": "IP address or network (e.g., '192.168.88.0/24' for local network only, '0.0.0.0/0' for anywhere)"
                    }
                },
                "required": ["service_name", "address"]
            },
        ),
        Tool(
            name="mikrotik_enable_ip_service",
            description="Enable an IP service",
            inputSchema={
                "type": "object",
                "properties": {
                    "service_name": {
                        "type": "string",
                        "description": "Name of the service to enable"
                    }
                },
                "required": ["service_name"]
            },
        ),
        Tool(
            name="mikrotik_disable_ip_service",
            description="Disable an IP service",
            inputSchema={
                "type": "object",
                "properties": {
                    "service_name": {
                        "type": "string",
                        "description": "Name of the service to disable"
                    }
                },
                "required": ["service_name"]
            },
        ),
        Tool(
            name="mikrotik_set_service_port",
            description="Set the port for an IP service",
            inputSchema={
                "type": "object",
                "properties": {
                    "service_name": {
                        "type": "string",
                        "description": "Name of the service"
                    },
                    "port": {
                        "type": "integer",
                        "description": "Port number for the service",
                        "minimum": 1,
                        "maximum": 65535
                    }
                },
                "required": ["service_name", "port"]
            },
        ),
        Tool(
            name="mikrotik_configure_secure_services",
            description="Configure secure IP services - restrict SSH, Winbox, and API to local network only, disable insecure services",
            inputSchema={
                "type": "object",
                "properties": {
                    "local_network": {
                        "type": "string",
                        "description": "Local network to allow access from (default: 192.168.88.0/24)",
                        "default": "192.168.88.0/24"
                    }
                },
                "required": []
            },
        ),
        Tool(
            name="mikrotik_restore_default_services",
            description="Restore IP services to default configuration (allow from anywhere)",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        Tool(
            name="mikrotik_get_service_status",
            description="Get status summary of all IP services with security information",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        Tool(
            name="mikrotik_create_service_backup",
            description="Create a backup of current IP services configuration",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
    ]

def get_ip_services_handlers() -> Dict[str, Callable]:
    """Return the handlers for IP services tools."""
    return {
        "mikrotik_list_ip_services": mikrotik_list_ip_services,
        "mikrotik_get_ip_service": mikrotik_get_ip_service,
        "mikrotik_set_service_address": mikrotik_set_service_address,
        "mikrotik_enable_ip_service": mikrotik_enable_ip_service,
        "mikrotik_disable_ip_service": mikrotik_disable_ip_service,
        "mikrotik_set_service_port": mikrotik_set_service_port,
        "mikrotik_configure_secure_services": mikrotik_configure_secure_services,
        "mikrotik_restore_default_services": mikrotik_restore_default_services,
        "mikrotik_get_service_status": mikrotik_get_service_status,
        "mikrotik_create_service_backup": mikrotik_create_service_backup,
    }
