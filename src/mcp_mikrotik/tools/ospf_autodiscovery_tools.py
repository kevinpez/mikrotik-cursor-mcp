"""
OSPF Auto-Discovery tool definitions for MikroTik RouterOS.
"""
from typing import Dict, Any, List, Callable
from ..scope.ospf_autodiscovery import (
    mikrotik_scan_mikrotik_neighbors,
    mikrotik_get_ospf_assignments,
    mikrotik_auto_assign_ospf_subnet,
    mikrotik_auto_configure_ospf_instance,
    mikrotik_auto_configure_ospf_area,
    mikrotik_auto_configure_ospf_networks,
    mikrotik_auto_configure_ospf_interfaces,
    mikrotik_enable_ospf_instance,
    mikrotik_auto_discovery_ospf_complete,
    mikrotik_get_ospf_auto_discovery_status
)
from mcp.types import Tool


def get_ospf_autodiscovery_tools() -> List[Tool]:
    """Return OSPF auto-discovery tools."""
    return [
        # Neighbor discovery tools
        Tool(
            name="mikrotik_scan_mikrotik_neighbors",
            description="Scan for MikroTik neighbors using MNDP (READ-ONLY, safe)",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        
        # Assignment management tools
        Tool(
            name="mikrotik_get_ospf_assignments",
            description="Get current OSPF subnet and Router ID assignments (READ-ONLY, safe)",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="mikrotik_auto_assign_ospf_subnet",
            description="Automatically assign a unique OSPF subnet and Router ID for a site",
            inputSchema={
                "type": "object",
                "properties": {
                    "site_id": {
                        "type": "string",
                        "description": "Unique identifier for the site"
                    },
                    "base_subnet": {
                        "type": "string",
                        "description": "Base subnet to start assignment from",
                        "default": "192.168.100.0/24"
                    }
                },
                "required": ["site_id"]
            }
        ),
        
        # OSPF configuration tools
        Tool(
            name="mikrotik_auto_configure_ospf_instance",
            description="Automatically configure OSPF instance with proper settings",
            inputSchema={
                "type": "object",
                "properties": {
                    "instance_name": {
                        "type": "string",
                        "description": "Name of the OSPF instance",
                        "default": "auto-ospf"
                    },
                    "router_id": {
                        "type": "string",
                        "description": "Router ID for the OSPF instance"
                    },
                    "comment": {
                        "type": "string",
                        "description": "Comment for the OSPF instance",
                        "default": "Auto-OSPF Instance"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="mikrotik_auto_configure_ospf_area",
            description="Automatically configure OSPF area",
            inputSchema={
                "type": "object",
                "properties": {
                    "area_name": {
                        "type": "string",
                        "description": "Name of the OSPF area",
                        "default": "backbone"
                    },
                    "instance_name": {
                        "type": "string",
                        "description": "Name of the OSPF instance",
                        "default": "auto-ospf"
                    },
                    "area_id": {
                        "type": "string",
                        "description": "Area ID for the OSPF area",
                        "default": "0.0.0.0"
                    },
                    "comment": {
                        "type": "string",
                        "description": "Comment for the OSPF area",
                        "default": "Backbone Area"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="mikrotik_auto_configure_ospf_networks",
            description="Automatically configure OSPF networks for a subnet and router ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "subnet": {
                        "type": "string",
                        "description": "Subnet to advertise (e.g., 192.168.100.0/24)"
                    },
                    "router_id": {
                        "type": "string",
                        "description": "Router ID subnet (e.g., 100.100.100.100/32)"
                    },
                    "area_name": {
                        "type": "string",
                        "description": "Name of the OSPF area",
                        "default": "backbone"
                    },
                    "instance_name": {
                        "type": "string",
                        "description": "Name of the OSPF instance",
                        "default": "auto-ospf"
                    }
                },
                "required": ["subnet", "router_id"]
            }
        ),
        Tool(
            name="mikrotik_auto_configure_ospf_interfaces",
            description="Automatically configure OSPF interfaces",
            inputSchema={
                "type": "object",
                "properties": {
                    "management_interface": {
                        "type": "string",
                        "description": "Management interface name",
                        "default": "ether1"
                    },
                    "area_name": {
                        "type": "string",
                        "description": "Name of the OSPF area",
                        "default": "backbone"
                    },
                    "instance_name": {
                        "type": "string",
                        "description": "Name of the OSPF instance",
                        "default": "auto-ospf"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="mikrotik_enable_ospf_instance",
            description="Enable OSPF instance",
            inputSchema={
                "type": "object",
                "properties": {
                    "instance_name": {
                        "type": "string",
                        "description": "Name of the OSPF instance to enable",
                        "default": "auto-ospf"
                    }
                },
                "required": []
            }
        ),
        
        # Complete auto-discovery tool
        Tool(
            name="mikrotik_auto_discovery_ospf_complete",
            description="Complete OSPF auto-discovery and configuration for a site",
            inputSchema={
                "type": "object",
                "properties": {
                    "site_id": {
                        "type": "string",
                        "description": "Unique identifier for the site"
                    },
                    "management_interface": {
                        "type": "string",
                        "description": "Management interface name",
                        "default": "ether1"
                    },
                    "instance_name": {
                        "type": "string",
                        "description": "Name of the OSPF instance",
                        "default": "auto-ospf"
                    },
                    "area_name": {
                        "type": "string",
                        "description": "Name of the OSPF area",
                        "default": "backbone"
                    }
                },
                "required": ["site_id"]
            }
        ),
        
        # Status and monitoring tools
        Tool(
            name="mikrotik_get_ospf_auto_discovery_status",
            description="Get comprehensive OSPF auto-discovery status (READ-ONLY, safe)",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
    ]


def get_ospf_autodiscovery_handlers() -> Dict[str, Callable]:
    """Return handlers for OSPF auto-discovery tools."""
    return {
        # Neighbor discovery handlers
        "mikrotik_scan_mikrotik_neighbors": lambda args: mikrotik_scan_mikrotik_neighbors(),
        
        # Assignment management handlers
        "mikrotik_get_ospf_assignments": lambda args: mikrotik_get_ospf_assignments(),
        "mikrotik_auto_assign_ospf_subnet": lambda args: mikrotik_auto_assign_ospf_subnet(
            site_id=args["site_id"],
            base_subnet=args.get("base_subnet", "192.168.100.0/24")
        ),
        
        # OSPF configuration handlers
        "mikrotik_auto_configure_ospf_instance": lambda args: mikrotik_auto_configure_ospf_instance(
            instance_name=args.get("instance_name", "auto-ospf"),
            router_id=args.get("router_id"),
            comment=args.get("comment", "Auto-OSPF Instance")
        ),
        "mikrotik_auto_configure_ospf_area": lambda args: mikrotik_auto_configure_ospf_area(
            area_name=args.get("area_name", "backbone"),
            instance_name=args.get("instance_name", "auto-ospf"),
            area_id=args.get("area_id", "0.0.0.0"),
            comment=args.get("comment", "Backbone Area")
        ),
        "mikrotik_auto_configure_ospf_networks": lambda args: mikrotik_auto_configure_ospf_networks(
            subnet=args["subnet"],
            router_id=args["router_id"],
            area_name=args.get("area_name", "backbone"),
            instance_name=args.get("instance_name", "auto-ospf")
        ),
        "mikrotik_auto_configure_ospf_interfaces": lambda args: mikrotik_auto_configure_ospf_interfaces(
            management_interface=args.get("management_interface", "ether1"),
            area_name=args.get("area_name", "backbone"),
            instance_name=args.get("instance_name", "auto-ospf")
        ),
        "mikrotik_enable_ospf_instance": lambda args: mikrotik_enable_ospf_instance(
            instance_name=args.get("instance_name", "auto-ospf")
        ),
        
        # Complete auto-discovery handler
        "mikrotik_auto_discovery_ospf_complete": lambda args: mikrotik_auto_discovery_ospf_complete(
            site_id=args["site_id"],
            management_interface=args.get("management_interface", "ether1"),
            instance_name=args.get("instance_name", "auto-ospf"),
            area_name=args.get("area_name", "backbone")
        ),
        
        # Status and monitoring handlers
        "mikrotik_get_ospf_auto_discovery_status": lambda args: mikrotik_get_ospf_auto_discovery_status(),
    }
