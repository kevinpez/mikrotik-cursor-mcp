from mcp.types import Tool
from typing import Any, Dict
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

# Tool definitions
mikrotik_firewall_layer7_tool = Tool(
    name="mcp_mikrotik-cursor-mcp_mikrotik_firewall_layer7",
    description=(
        "Manage MikroTik Layer 7 protocol matchers for deep packet inspection. "
        "Available actions: list_layer7_protocols, create_layer7_protocol, get_layer7_protocol, "
        "update_layer7_protocol, remove_layer7_protocol, enable_layer7_protocol, "
        "disable_layer7_protocol, create_common_layer7_protocols"
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "description": (
                    "The action to perform. Available: list_layer7_protocols, create_layer7_protocol, "
                    "get_layer7_protocol, update_layer7_protocol, remove_layer7_protocol, "
                    "enable_layer7_protocol, disable_layer7_protocol, create_common_layer7_protocols"
                ),
                "enum": [
                    "list_layer7_protocols",
                    "create_layer7_protocol",
                    "get_layer7_protocol",
                    "update_layer7_protocol",
                    "remove_layer7_protocol",
                    "enable_layer7_protocol",
                    "disable_layer7_protocol",
                    "create_common_layer7_protocols"
                ]
            }
        },
        "required": ["action"],
        "additionalProperties": True
    }
)

# Handler function
def handle_firewall_layer7_tool(arguments: Dict[str, Any]) -> str:
    """Handle Layer 7 protocol tool requests."""
    action = arguments.get("action")
    
    if action == "list_layer7_protocols":
        return mikrotik_list_layer7_protocols(
            name_filter=arguments.get("name_filter"),
            disabled_only=arguments.get("disabled_only", False)
        )
    
    elif action == "create_layer7_protocol":
        name = arguments.get("name")
        regexp = arguments.get("regexp")
        
        if not name:
            return "Error: 'name' parameter is required for create_layer7_protocol action."
        if not regexp:
            return "Error: 'regexp' parameter is required for create_layer7_protocol action."
        
        return mikrotik_create_layer7_protocol(
            name=name,
            regexp=regexp,
            comment=arguments.get("comment"),
            disabled=arguments.get("disabled", False)
        )
    
    elif action == "get_layer7_protocol":
        protocol_id = arguments.get("protocol_id")
        
        if not protocol_id:
            return "Error: 'protocol_id' parameter is required for get_layer7_protocol action."
        
        return mikrotik_get_layer7_protocol(protocol_id)
    
    elif action == "update_layer7_protocol":
        protocol_id = arguments.get("protocol_id")
        
        if not protocol_id:
            return "Error: 'protocol_id' parameter is required for update_layer7_protocol action."
        
        return mikrotik_update_layer7_protocol(
            protocol_id=protocol_id,
            name=arguments.get("name"),
            regexp=arguments.get("regexp"),
            comment=arguments.get("comment"),
            disabled=arguments.get("disabled")
        )
    
    elif action == "remove_layer7_protocol":
        protocol_id = arguments.get("protocol_id")
        
        if not protocol_id:
            return "Error: 'protocol_id' parameter is required for remove_layer7_protocol action."
        
        return mikrotik_remove_layer7_protocol(protocol_id)
    
    elif action == "enable_layer7_protocol":
        protocol_id = arguments.get("protocol_id")
        
        if not protocol_id:
            return "Error: 'protocol_id' parameter is required for enable_layer7_protocol action."
        
        return mikrotik_enable_layer7_protocol(protocol_id)
    
    elif action == "disable_layer7_protocol":
        protocol_id = arguments.get("protocol_id")
        
        if not protocol_id:
            return "Error: 'protocol_id' parameter is required for disable_layer7_protocol action."
        
        return mikrotik_disable_layer7_protocol(protocol_id)
    
    elif action == "create_common_layer7_protocols":
        return mikrotik_create_common_layer7_protocols()
    
    else:
        return f"Error: Unknown action '{action}' for Layer 7 protocol management."

