"""
Nested MikroTik MCP server with reduced tool count.
Instead of 100+ individual tools, we have ~10 category tools.
"""
import sys
from .logger import app_logger
from typing import Dict, List, Any

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import TextContent, Tool
except ImportError as e:
    print(f"Error importing MCP: {e}")
    print(f"Current Python path: {sys.path}")
    sys.exit(1)

from .tools.tool_registry import get_all_handlers

# Define the nested tool categories
NESTED_TOOLS = [
    {
        "name": "mikrotik_firewall",
        "description": "Manage MikroTik firewall rules (filter and NAT)",
        "category": "firewall"
    },
    {
        "name": "mikrotik_dhcp", 
        "description": "Manage MikroTik DHCP servers and pools",
        "category": "dhcp"
    },
    {
        "name": "mikrotik_dns",
        "description": "Manage MikroTik DNS settings and static entries", 
        "category": "dns"
    },
    {
        "name": "mikrotik_routes",
        "description": "Manage MikroTik routing table and static routes",
        "category": "routes"
    },
    {
        "name": "mikrotik_ip",
        "description": "Manage MikroTik IP addresses and pools",
        "category": "ip"
    },
    {
        "name": "mikrotik_vlan",
        "description": "Manage MikroTik VLAN interfaces",
        "category": "vlan"
    },
    {
        "name": "mikrotik_wireless",
        "description": "Manage MikroTik wireless interfaces and clients",
        "category": "wireless"
    },
    {
        "name": "mikrotik_users",
        "description": "Manage MikroTik users and groups",
        "category": "users"
    },
    {
        "name": "mikrotik_backup",
        "description": "Create and restore MikroTik backups",
        "category": "backup"
    },
    {
        "name": "mikrotik_logs",
        "description": "View and manage MikroTik system logs",
        "category": "logs"
    },
    {
        "name": "mikrotik_system",
        "description": "Monitor and manage system resources (CPU, RAM, uptime, NTP)",
        "category": "system"
    },
    {
        "name": "mikrotik_interfaces",
        "description": "Manage network interfaces (stats, enable/disable, bridge)",
        "category": "interfaces"
    },
    {
        "name": "mikrotik_diagnostics",
        "description": "Network diagnostic tools (ping, traceroute, DNS lookup, ARP)",
        "category": "diagnostics"
    },
    {
        "name": "mikrotik_queues",
        "description": "Manage bandwidth limits and QoS (simple queues)",
        "category": "queues"
    },
    {
        "name": "mikrotik_wireguard",
        "description": "Manage WireGuard VPN interfaces and peers",
        "category": "wireguard"
    }
]

# Map categories to their available actions
CATEGORY_ACTIONS = {
    "firewall": [
        "list_filter_rules", "create_filter_rule", "remove_filter_rule", "update_filter_rule",
        "list_nat_rules", "create_nat_rule", "remove_nat_rule", "update_nat_rule",
        "create_port_forward", "list_port_forwards"
    ],
    "dhcp": [
        "list_dhcp_servers", "create_dhcp_server", "remove_dhcp_server", "get_dhcp_server",
        "create_dhcp_network", "create_dhcp_pool"
    ],
    "dns": [
        "get_dns_settings", "update_dns_settings", "list_dns_static", "create_dns_static",
        "remove_dns_static", "update_dns_static", "flush_dns_cache", "get_dns_cache"
    ],
    "routes": [
        "list_routes", "add_route", "remove_route", "update_route", "enable_route", "disable_route",
        "get_route", "add_default_route", "add_blackhole_route", "get_routing_table"
    ],
    "ip": [
        "list_ip_addresses", "add_ip_address", "remove_ip_address", "update_ip_address",
        "list_ip_pools", "create_ip_pool", "remove_ip_pool", "update_ip_pool"
    ],
    "vlan": [
        "list_vlan_interfaces", "create_vlan_interface", "remove_vlan_interface", "update_vlan_interface"
    ],
    "wireless": [
        "list_wireless_interfaces", "list_wireless_clients", "update_wireless_interface"
    ],
    "users": [
        "list_users", "create_user", "remove_user", "update_user", "list_user_groups"
    ],
    "backup": [
        "create_backup", "list_backups", "restore_backup", "export_configuration"
    ],
    "logs": [
        "get_logs", "search_logs", "clear_logs", "export_logs"
    ],
    "system": [
        "get_system_resources", "get_system_health", "get_system_identity", "set_system_identity",
        "get_system_clock", "get_ntp_client", "set_ntp_client", "reboot_system",
        "get_routerboard", "get_license", "get_uptime"
    ],
    "interfaces": [
        "list_interfaces", "get_interface_stats", "enable_interface", "disable_interface",
        "get_interface_monitor", "list_bridge_ports", "add_bridge_port", "remove_bridge_port",
        "get_interface_traffic"
    ],
    "diagnostics": [
        "ping", "traceroute", "bandwidth_test", "dns_lookup", "check_connection",
        "get_arp_table", "get_neighbors"
    ],
    "queues": [
        "list_simple_queues", "create_simple_queue", "remove_simple_queue",
        "enable_simple_queue", "disable_simple_queue", "update_simple_queue", "list_queue_types"
    ],
    "wireguard": [
        "list_wireguard_interfaces", "create_wireguard_interface", "remove_wireguard_interface",
        "update_wireguard_interface", "get_wireguard_interface", "enable_wireguard_interface",
        "disable_wireguard_interface", "list_wireguard_peers", "add_wireguard_peer",
        "remove_wireguard_peer", "update_wireguard_peer"
    ]
}

def get_nested_tools() -> List[Tool]:
    """Return the nested tool definitions."""
    tools = []
    
    for tool_def in NESTED_TOOLS:
        category = tool_def["category"]
        actions = CATEGORY_ACTIONS.get(category, [])
        
        tool = Tool(
            name=tool_def["name"],
            description=f"{tool_def['description']}. Available actions: {', '.join(actions)}",
            inputSchema={
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": actions,
                        "description": f"The action to perform. Available: {', '.join(actions)}"
                    }
                },
                "required": ["action"],
                "additionalProperties": True
            }
        )
        tools.append(tool)
    
    return tools

async def serve() -> None:
    """
    Main function to run the nested MCP server for MikroTik commands.
    """
    app_logger.info("Starting Nested MikroTik MCP server")
    server = Server("mcp-mikrotik-nested")

    @server.list_tools()
    async def list_tools() -> List[Tool]:
        app_logger.info("Listing available nested tools")
        return get_nested_tools()

    @server.call_tool()
    async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
        app_logger.info(f"Nested tool call: {name} with arguments {arguments}")

        # Find the category from the tool name
        category = None
        for tool_def in NESTED_TOOLS:
            if tool_def["name"] == name:
                category = tool_def["category"]
                break
        
        if not category:
            error_msg = f"Unknown tool: {name}"
            app_logger.error(error_msg)
            return [TextContent(type="text", text=error_msg)]
        
        # Get the action
        action = arguments.get("action")
        if not action:
            available_actions = CATEGORY_ACTIONS.get(category, [])
            return [TextContent(type="text", text=f"Action required. Available actions for {category}: {', '.join(available_actions)}")]
        
        # Construct the original tool name
        original_tool_name = f"mikrotik_{action}"
        
        # Get the handler
        handlers = get_all_handlers()
        
        if original_tool_name in handlers:
            try:
                # Remove 'action' from arguments since the handler doesn't expect it
                handler_args = {k: v for k, v in arguments.items() if k != "action"}
                result = handlers[original_tool_name](handler_args)
                return [TextContent(type="text", text=result)]
            except Exception as e:
                error_msg = f"Error executing {category}.{action}: {str(e)}"
                app_logger.error(error_msg)
                return [TextContent(type="text", text=error_msg)]
        else:
            error_msg = f"Action '{action}' not found in category '{category}'"
            app_logger.error(error_msg)
            return [TextContent(type="text", text=error_msg)]

    app_logger.info("Creating initialization options")
    options = server.create_initialization_options()

    app_logger.info("Starting stdio server")
    async with stdio_server() as (read_stream, write_stream):
        app_logger.info("Running nested MCP server")
        await server.run(read_stream, write_stream, options, raise_exceptions=True)
