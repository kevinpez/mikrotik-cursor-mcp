import sys
from logger import app_logger
from typing import Dict, List, Any
from scope.vlan import mikrotik_create_vlan_interface, mikrotik_list_vlan_interfaces, mikrotik_get_vlan_interface, mikrotik_update_vlan_interface, mikrotik_remove_vlan_interface
from scope.ip_address import mikrotik_add_ip_address, mikrotik_list_ip_addresses, mikrotik_get_ip_address, mikrotik_remove_ip_address
from scope.dhcp import mikrotik_create_dhcp_server, mikrotik_list_dhcp_servers, mikrotik_get_dhcp_server, mikrotik_create_dhcp_network, mikrotik_create_dhcp_pool, mikrotik_remove_dhcp_server
from scope.config import mikrotik_config_set, mikrotik_config_get
from scope.firewall_nat import mikrotik_create_nat_rule, mikrotik_list_nat_rules, mikrotik_get_nat_rule, mikrotik_update_nat_rule, mikrotik_remove_nat_rule, mikrotik_move_nat_rule, mikrotik_enable_nat_rule, mikrotik_disable_nat_rule
from scope.ip_pool import mikrotik_create_ip_pool, mikrotik_list_ip_pools, mikrotik_get_ip_pool, mikrotik_update_ip_pool, mikrotik_remove_ip_pool, mikrotik_list_ip_pool_used, mikrotik_expand_ip_pool
from scope.backup import mikrotik_create_backup, mikrotik_list_backups, mikrotik_create_export, mikrotik_export_section, mikrotik_download_file, mikrotik_upload_file, mikrotik_restore_backup, mikrotik_import_configuration, mikrotik_remove_file, mikrotik_backup_info
from scope.logs import mikrotik_get_logs, mikrotik_get_logs_by_severity, mikrotik_get_logs_by_topic, mikrotik_search_logs, mikrotik_get_system_events, mikrotik_get_security_logs, mikrotik_clear_logs, mikrotik_get_log_statistics, mikrotik_export_logs, mikrotik_monitor_logs
from scope.firewall_filter import mikrotik_create_filter_rule, mikrotik_list_filter_rules, mikrotik_get_filter_rule, mikrotik_update_filter_rule, mikrotik_remove_filter_rule, mikrotik_move_filter_rule, mikrotik_enable_filter_rule, mikrotik_disable_filter_rule, mikrotik_create_basic_firewall_setup
from scope.routes import mikrotik_add_route, mikrotik_list_routes, mikrotik_get_route, mikrotik_update_route, mikrotik_remove_route, mikrotik_enable_route, mikrotik_disable_route, mikrotik_get_routing_table, mikrotik_check_route_path, mikrotik_get_route_cache, mikrotik_flush_route_cache, mikrotik_add_default_route, mikrotik_add_blackhole_route, mikrotik_get_route_statistics
from scope.dns import mikrotik_set_dns_servers, mikrotik_get_dns_settings, mikrotik_add_dns_static, mikrotik_list_dns_static, mikrotik_get_dns_static, mikrotik_update_dns_static, mikrotik_remove_dns_static, mikrotik_enable_dns_static, mikrotik_disable_dns_static, mikrotik_get_dns_cache, mikrotik_flush_dns_cache, mikrotik_get_dns_cache_statistics, mikrotik_add_dns_regexp, mikrotik_test_dns_query, mikrotik_export_dns_config
from scope.users import mikrotik_add_user, mikrotik_list_users, mikrotik_get_user, mikrotik_update_user, mikrotik_remove_user, mikrotik_disable_user, mikrotik_enable_user, mikrotik_add_user_group, mikrotik_list_user_groups, mikrotik_get_user_group, mikrotik_update_user_group, mikrotik_remove_user_group, mikrotik_get_active_users, mikrotik_disconnect_user, mikrotik_export_user_config, mikrotik_set_user_ssh_keys, mikrotik_list_user_ssh_keys, mikrotik_remove_user_ssh_key


# Try to import mcp with error handling
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import TextContent, Tool
except ImportError as e:
    print(f"Error importing MCP: {e}")
    print(f"Current Python path: {sys.path}")
    sys.exit(1)


async def serve() -> None:
    """
    Main function to run the MCP server for MikroTik commands.
    """
    app_logger.info("Starting MikroTik MCP server")
    server = Server("mcp-mikrotik")

    @server.list_tools()
    async def list_tools() -> List[Tool]:
        app_logger.info("Listing available tools")
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
            
            # VLAN interface tools
            Tool(
                name="mikrotik_create_vlan_interface",
                description="Creates a VLAN interface on MikroTik device",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "vlan_id": {"type": "integer", "minimum": 1, "maximum": 4094},
                        "interface": {"type": "string"},
                        "comment": {"type": "string"},
                        "disabled": {"type": "boolean"},
                        "mtu": {"type": "integer"},
                        "use_service_tag": {"type": "boolean"},
                        "arp": {"type": "string", "enum": ["enabled", "disabled", "proxy-arp", "reply-only"]},
                        "arp_timeout": {"type": "string"}
                    },
                    "required": ["name", "vlan_id", "interface"]
                },
            ),
            Tool(
                name="mikrotik_list_vlan_interfaces",
                description="Lists VLAN interfaces on MikroTik device",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name_filter": {"type": "string"},
                        "vlan_id_filter": {"type": "integer"},
                        "interface_filter": {"type": "string"},
                        "disabled_only": {"type": "boolean"}
                    },
                    "required": []
                },
            ),
            Tool(
                name="mikrotik_get_vlan_interface",
                description="Gets detailed information about a specific VLAN interface",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"}
                    },
                    "required": ["name"]
                },
            ),
            Tool(
                name="mikrotik_update_vlan_interface",
                description="Updates an existing VLAN interface on MikroTik device",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "new_name": {"type": "string"},
                        "vlan_id": {"type": "integer", "minimum": 1, "maximum": 4094},
                        "interface": {"type": "string"},
                        "comment": {"type": "string"},
                        "disabled": {"type": "boolean"},
                        "mtu": {"type": "integer"},
                        "use_service_tag": {"type": "boolean"},
                        "arp": {"type": "string", "enum": ["enabled", "disabled", "proxy-arp", "reply-only"]},
                        "arp_timeout": {"type": "string"}
                    },
                    "required": ["name"]
                },
            ),
            Tool(
                name="mikrotik_remove_vlan_interface",
                description="Removes a VLAN interface from MikroTik device",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"}
                    },
                    "required": ["name"]
                },
            ),
            
            # IP Address tools
            Tool(
                name="mikrotik_add_ip_address",
                description="Adds an IP address to an interface",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "address": {"type": "string"},
                        "interface": {"type": "string"},
                        "network": {"type": "string"},
                        "broadcast": {"type": "string"},
                        "comment": {"type": "string"},
                        "disabled": {"type": "boolean"}
                    },
                    "required": ["address", "interface"]
                },
            ),
            Tool(
                name="mikrotik_list_ip_addresses",
                description="Lists IP addresses on MikroTik device",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "interface_filter": {"type": "string"},
                        "address_filter": {"type": "string"},
                        "network_filter": {"type": "string"},
                        "disabled_only": {"type": "boolean"},
                        "dynamic_only": {"type": "boolean"}
                    },
                    "required": []
                },
            ),
            Tool(
                name="mikrotik_get_ip_address",
                description="Gets detailed information about a specific IP address",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "address_id": {"type": "string"}
                    },
                    "required": ["address_id"]
                },
            ),
            Tool(
                name="mikrotik_remove_ip_address",
                description="Removes an IP address from MikroTik device",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "address_id": {"type": "string"}
                    },
                    "required": ["address_id"]
                },
            ),
            
            # DHCP Server tools
            Tool(
                name="mikrotik_create_dhcp_server",
                description="Creates a DHCP server on MikroTik device",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "interface": {"type": "string"},
                        "lease_time": {"type": "string"},
                        "address_pool": {"type": "string"},
                        "disabled": {"type": "boolean"},
                        "authoritative": {"type": "string", "enum": ["yes", "no", "after-2sec-delay"]},
                        "delay_threshold": {"type": "string"},
                        "comment": {"type": "string"}
                    },
                    "required": ["name", "interface"]
                },
            ),
            Tool(
                name="mikrotik_list_dhcp_servers",
                description="Lists DHCP servers on MikroTik device",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name_filter": {"type": "string"},
                        "interface_filter": {"type": "string"},
                        "disabled_only": {"type": "boolean"},
                        "invalid_only": {"type": "boolean"}
                    },
                    "required": []
                },
            ),
            Tool(
                name="mikrotik_get_dhcp_server",
                description="Gets detailed information about a specific DHCP server",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"}
                    },
                    "required": ["name"]
                },
            ),
            Tool(
                name="mikrotik_create_dhcp_network",
                description="Creates a DHCP network configuration",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "network": {"type": "string"},
                        "gateway": {"type": "string"},
                        "netmask": {"type": "string"},
                        "dns_servers": {"type": "array", "items": {"type": "string"}},
                        "domain": {"type": "string"},
                        "wins_servers": {"type": "array", "items": {"type": "string"}},
                        "ntp_servers": {"type": "array", "items": {"type": "string"}},
                        "dhcp_option": {"type": "array", "items": {"type": "string"}},
                        "comment": {"type": "string"}
                    },
                    "required": ["network", "gateway"]
                },
            ),
            Tool(
                name="mikrotik_create_dhcp_pool",
                description="Creates a DHCP address pool",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "ranges": {"type": "string"},
                        "next_pool": {"type": "string"},
                        "comment": {"type": "string"}
                    },
                    "required": ["name", "ranges"]
                },
            ),
            Tool(
                name="mikrotik_remove_dhcp_server",
                description="Removes a DHCP server from MikroTik device",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"}
                    },
                    "required": ["name"]
                },
            ),
            # NAT tools
            Tool(
                name="mikrotik_create_nat_rule",
                description="Creates a NAT rule on MikroTik device",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "chain": {"type": "string", "enum": ["srcnat", "dstnat"]},
                        "action": {"type": "string"},
                        "src_address": {"type": "string"},
                        "dst_address": {"type": "string"},
                        "src_port": {"type": "string"},
                        "dst_port": {"type": "string"},
                        "protocol": {"type": "string"},
                        "in_interface": {"type": "string"},
                        "out_interface": {"type": "string"},
                        "to_addresses": {"type": "string"},
                        "to_ports": {"type": "string"},
                        "comment": {"type": "string"},
                        "disabled": {"type": "boolean"},
                        "log": {"type": "boolean"},
                        "log_prefix": {"type": "string"},
                        "place_before": {"type": "string"}
                    },
                    "required": ["chain", "action"]
                },
            ),
            Tool(
                name="mikrotik_list_nat_rules",
                description="Lists NAT rules on MikroTik device",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "chain_filter": {"type": "string"},
                        "action_filter": {"type": "string"},
                        "src_address_filter": {"type": "string"},
                        "dst_address_filter": {"type": "string"},
                        "protocol_filter": {"type": "string"},
                        "interface_filter": {"type": "string"},
                        "disabled_only": {"type": "boolean"},
                        "invalid_only": {"type": "boolean"}
                    },
                    "required": []
                },
            ),
            Tool(
                name="mikrotik_get_nat_rule",
                description="Gets detailed information about a specific NAT rule",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "rule_id": {"type": "string"}
                    },
                    "required": ["rule_id"]
                },
            ),
            Tool(
                name="mikrotik_update_nat_rule",
                description="Updates an existing NAT rule on MikroTik device",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "rule_id": {"type": "string"},
                        "chain": {"type": "string"},
                        "action": {"type": "string"},
                        "src_address": {"type": "string"},
                        "dst_address": {"type": "string"},
                        "src_port": {"type": "string"},
                        "dst_port": {"type": "string"},
                        "protocol": {"type": "string"},
                        "in_interface": {"type": "string"},
                        "out_interface": {"type": "string"},
                        "to_addresses": {"type": "string"},
                        "to_ports": {"type": "string"},
                        "comment": {"type": "string"},
                        "disabled": {"type": "boolean"},
                        "log": {"type": "boolean"},
                        "log_prefix": {"type": "string"}
                    },
                    "required": ["rule_id"]
                },
            ),
            Tool(
                name="mikrotik_remove_nat_rule",
                description="Removes a NAT rule from MikroTik device",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "rule_id": {"type": "string"}
                    },
                    "required": ["rule_id"]
                },
            ),
            Tool(
                name="mikrotik_move_nat_rule",
                description="Moves a NAT rule to a different position in the chain",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "rule_id": {"type": "string"},
                        "destination": {"type": "integer"}
                    },
                    "required": ["rule_id", "destination"]
                },
            ),
            Tool(
                name="mikrotik_enable_nat_rule",
                description="Enables a NAT rule",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "rule_id": {"type": "string"}
                    },
                    "required": ["rule_id"]
                },
            ),
            Tool(
                name="mikrotik_disable_nat_rule",
                description="Disables a NAT rule",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "rule_id": {"type": "string"}
                    },
                    "required": ["rule_id"]
                },
            ),
            # IP Pool tools
            Tool(
                name="mikrotik_create_ip_pool",
                description="Creates an IP pool on MikroTik device",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "ranges": {"type": "string"},
                        "next_pool": {"type": "string"},
                        "comment": {"type": "string"}
                    },
                    "required": ["name", "ranges"]
                },
            ),
            Tool(
                name="mikrotik_list_ip_pools",
                description="Lists IP pools on MikroTik device",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name_filter": {"type": "string"},
                        "ranges_filter": {"type": "string"},
                        "include_used": {"type": "boolean"}
                    },
                    "required": []
                },
            ),
            Tool(
                name="mikrotik_get_ip_pool",
                description="Gets detailed information about a specific IP pool",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"}
                    },
                    "required": ["name"]
                },
            ),
            Tool(
                name="mikrotik_update_ip_pool",
                description="Updates an existing IP pool on MikroTik device",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "new_name": {"type": "string"},
                        "ranges": {"type": "string"},
                        "next_pool": {"type": "string"},
                        "comment": {"type": "string"}
                    },
                    "required": ["name"]
                },
            ),
            Tool(
                name="mikrotik_remove_ip_pool",
                description="Removes an IP pool from MikroTik device",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"}
                    },
                    "required": ["name"]
                },
            ),
            Tool(
                name="mikrotik_list_ip_pool_used",
                description="Lists used addresses from IP pools",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "pool_name": {"type": "string"},
                        "address_filter": {"type": "string"},
                        "mac_filter": {"type": "string"},
                        "info_filter": {"type": "string"}
                    },
                    "required": []
                },
            ),
            Tool(
                name="mikrotik_expand_ip_pool",
                description="Expands an existing IP pool by adding more ranges",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "additional_ranges": {"type": "string"}
                    },
                    "required": ["name", "additional_ranges"]
                },
            ),
            # Backup and Export tools
            Tool(
                name="mikrotik_create_backup",
                description="Creates a system backup on MikroTik device",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "dont_encrypt": {"type": "boolean"},
                        "include_password": {"type": "boolean"},
                        "comment": {"type": "string"}
                    },
                    "required": []
                },
            ),
            Tool(
                name="mikrotik_list_backups",
                description="Lists backup files on MikroTik device",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name_filter": {"type": "string"},
                        "include_exports": {"type": "boolean"}
                    },
                    "required": []
                },
            ),
            Tool(
                name="mikrotik_create_export",
                description="Creates a configuration export on MikroTik device",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "file_format": {"type": "string", "enum": ["rsc", "json", "xml"]},
                        "export_type": {"type": "string", "enum": ["full", "compact", "verbose"]},
                        "hide_sensitive": {"type": "boolean"},
                        "verbose": {"type": "boolean"},
                        "compact": {"type": "boolean"},
                        "comment": {"type": "string"}
                    },
                    "required": []
                },
            ),
            Tool(
                name="mikrotik_export_section",
                description="Exports a specific configuration section",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "section": {"type": "string"},
                        "name": {"type": "string"},
                        "hide_sensitive": {"type": "boolean"},
                        "compact": {"type": "boolean"}
                    },
                    "required": ["section"]
                },
            ),
            Tool(
                name="mikrotik_download_file",
                description="Downloads a file from MikroTik device",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "filename": {"type": "string"},
                        "file_type": {"type": "string", "enum": ["backup", "export"]}
                    },
                    "required": ["filename"]
                },
            ),
            Tool(
                name="mikrotik_upload_file",
                description="Uploads a file to MikroTik device",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "filename": {"type": "string"},
                        "content_base64": {"type": "string"}
                    },
                    "required": ["filename", "content_base64"]
                },
            ),
            Tool(
                name="mikrotik_restore_backup",
                description="Restores a system backup on MikroTik device",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "filename": {"type": "string"},
                        "password": {"type": "string"}
                    },
                    "required": ["filename"]
                },
            ),
            Tool(
                name="mikrotik_import_configuration",
                description="Imports a configuration script file",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "filename": {"type": "string"},
                        "run_after_reset": {"type": "boolean"},
                        "verbose": {"type": "boolean"}
                    },
                    "required": ["filename"]
                },
            ),
            Tool(
                name="mikrotik_remove_file",
                description="Removes a file from MikroTik device",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "filename": {"type": "string"}
                    },
                    "required": ["filename"]
                },
            ),
            Tool(
                name="mikrotik_backup_info",
                description="Gets detailed information about a backup file",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "filename": {"type": "string"}
                    },
                    "required": ["filename"]
                },
            ),
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
            # Firewall Filter tools
            Tool(
                name="mikrotik_create_filter_rule",
                description="Creates a firewall filter rule on MikroTik device",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "chain": {"type": "string", "enum": ["input", "forward", "output"]},
                        "action": {"type": "string"},
                        "src_address": {"type": "string"},
                        "dst_address": {"type": "string"},
                        "src_port": {"type": "string"},
                        "dst_port": {"type": "string"},
                        "protocol": {"type": "string"},
                        "in_interface": {"type": "string"},
                        "out_interface": {"type": "string"},
                        "connection_state": {"type": "string"},
                        "connection_nat_state": {"type": "string"},
                        "src_address_list": {"type": "string"},
                        "dst_address_list": {"type": "string"},
                        "limit": {"type": "string"},
                        "tcp_flags": {"type": "string"},
                        "comment": {"type": "string"},
                        "disabled": {"type": "boolean"},
                        "log": {"type": "boolean"},
                        "log_prefix": {"type": "string"},
                        "place_before": {"type": "string"}
                    },
                    "required": ["chain", "action"]
                },
            ),
            Tool(
                name="mikrotik_list_filter_rules",
                description="Lists firewall filter rules on MikroTik device",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "chain_filter": {"type": "string"},
                        "action_filter": {"type": "string"},
                        "src_address_filter": {"type": "string"},
                        "dst_address_filter": {"type": "string"},
                        "protocol_filter": {"type": "string"},
                        "interface_filter": {"type": "string"},
                        "disabled_only": {"type": "boolean"},
                        "invalid_only": {"type": "boolean"},
                        "dynamic_only": {"type": "boolean"}
                    },
                    "required": []
                },
            ),
            Tool(
                name="mikrotik_get_filter_rule",
                description="Gets detailed information about a specific firewall filter rule",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "rule_id": {"type": "string"}
                    },
                    "required": ["rule_id"]
                },
            ),
            Tool(
                name="mikrotik_update_filter_rule",
                description="Updates an existing firewall filter rule on MikroTik device",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "rule_id": {"type": "string"},
                        "chain": {"type": "string"},
                        "action": {"type": "string"},
                        "src_address": {"type": "string"},
                        "dst_address": {"type": "string"},
                        "src_port": {"type": "string"},
                        "dst_port": {"type": "string"},
                        "protocol": {"type": "string"},
                        "in_interface": {"type": "string"},
                        "out_interface": {"type": "string"},
                        "connection_state": {"type": "string"},
                        "connection_nat_state": {"type": "string"},
                        "src_address_list": {"type": "string"},
                        "dst_address_list": {"type": "string"},
                        "limit": {"type": "string"},
                        "tcp_flags": {"type": "string"},
                        "comment": {"type": "string"},
                        "disabled": {"type": "boolean"},
                        "log": {"type": "boolean"},
                        "log_prefix": {"type": "string"}
                    },
                    "required": ["rule_id"]
                },
            ),
            Tool(
                name="mikrotik_remove_filter_rule",
                description="Removes a firewall filter rule from MikroTik device",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "rule_id": {"type": "string"}
                    },
                    "required": ["rule_id"]
                },
            ),
            Tool(
                name="mikrotik_move_filter_rule",
                description="Moves a firewall filter rule to a different position",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "rule_id": {"type": "string"},
                        "destination": {"type": "integer"}
                    },
                    "required": ["rule_id", "destination"]
                },
            ),
            Tool(
                name="mikrotik_enable_filter_rule",
                description="Enables a firewall filter rule",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "rule_id": {"type": "string"}
                    },
                    "required": ["rule_id"]
                },
            ),
            Tool(
                name="mikrotik_disable_filter_rule",
                description="Disables a firewall filter rule",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "rule_id": {"type": "string"}
                    },
                    "required": ["rule_id"]
                },
            ),
            Tool(
                name="mikrotik_create_basic_firewall_setup",
                description="Creates a basic firewall setup with common security rules",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": []
                },
            ),
            # Route tools
            Tool(
                name="mikrotik_add_route",
                description="Adds a route to MikroTik routing table",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "dst_address": {"type": "string"},
                        "gateway": {"type": "string"},
                        "distance": {"type": "integer"},
                        "scope": {"type": "integer"},
                        "target_scope": {"type": "integer"},
                        "routing_mark": {"type": "string"},
                        "comment": {"type": "string"},
                        "disabled": {"type": "boolean"},
                        "vrf_interface": {"type": "string"},
                        "pref_src": {"type": "string"},
                        "check_gateway": {"type": "string"}
                    },
                    "required": ["dst_address", "gateway"]
                },
            ),
            Tool(
                name="mikrotik_list_routes",
                description="Lists routes in MikroTik routing table",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "dst_filter": {"type": "string"},
                        "gateway_filter": {"type": "string"},
                        "routing_mark_filter": {"type": "string"},
                        "distance_filter": {"type": "integer"},
                        "active_only": {"type": "boolean"},
                        "disabled_only": {"type": "boolean"},
                        "dynamic_only": {"type": "boolean"},
                        "static_only": {"type": "boolean"}
                    },
                    "required": []
                },
            ),
            Tool(
                name="mikrotik_get_route",
                description="Gets detailed information about a specific route",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "route_id": {"type": "string"}
                    },
                    "required": ["route_id"]
                },
            ),
            Tool(
                name="mikrotik_update_route",
                description="Updates an existing route in MikroTik routing table",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "route_id": {"type": "string"},
                        "dst_address": {"type": "string"},
                        "gateway": {"type": "string"},
                        "distance": {"type": "integer"},
                        "scope": {"type": "integer"},
                        "target_scope": {"type": "integer"},
                        "routing_mark": {"type": "string"},
                        "comment": {"type": "string"},
                        "disabled": {"type": "boolean"},
                        "vrf_interface": {"type": "string"},
                        "pref_src": {"type": "string"},
                        "check_gateway": {"type": "string"}
                    },
                    "required": ["route_id"]
                },
            ),
            Tool(
                name="mikrotik_remove_route",
                description="Removes a route from MikroTik routing table",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "route_id": {"type": "string"}
                    },
                    "required": ["route_id"]
                },
            ),
            Tool(
                name="mikrotik_enable_route",
                description="Enables a route",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "route_id": {"type": "string"}
                    },
                    "required": ["route_id"]
                },
            ),
            Tool(
                name="mikrotik_disable_route",
                description="Disables a route",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "route_id": {"type": "string"}
                    },
                    "required": ["route_id"]
                },
            ),
            Tool(
                name="mikrotik_get_routing_table",
                description="Gets a specific routing table",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "table_name": {"type": "string"},
                        "protocol_filter": {"type": "string"},
                        "active_only": {"type": "boolean"}
                    },
                    "required": []
                },
            ),
            Tool(
                name="mikrotik_check_route_path",
                description="Checks the route path to a destination",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "destination": {"type": "string"},
                        "source": {"type": "string"},
                        "routing_mark": {"type": "string"}
                    },
                    "required": ["destination"]
                },
            ),
            Tool(
                name="mikrotik_get_route_cache",
                description="Gets the route cache",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": []
                },
            ),
            Tool(
                name="mikrotik_flush_route_cache",
                description="Flushes the route cache",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": []
                },
            ),
            Tool(
                name="mikrotik_add_default_route",
                description="Adds a default route (0.0.0.0/0)",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "gateway": {"type": "string"},
                        "distance": {"type": "integer"},
                        "comment": {"type": "string"},
                        "check_gateway": {"type": "string"}
                    },
                    "required": ["gateway"]
                },
            ),
            Tool(
                name="mikrotik_add_blackhole_route",
                description="Adds a blackhole route",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "dst_address": {"type": "string"},
                        "distance": {"type": "integer"},
                        "comment": {"type": "string"}
                    },
                    "required": ["dst_address"]
                },
            ),
            Tool(
                name="mikrotik_get_route_statistics",
                description="Gets routing table statistics",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": []
                },
            ),
            # DNS tools
            Tool(
                name="mikrotik_set_dns_servers",
                description="Sets DNS server configuration on MikroTik device",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "servers": {"type": "array", "items": {"type": "string"}},
                        "allow_remote_requests": {"type": "boolean"},
                        "max_udp_packet_size": {"type": "integer"},
                        "max_concurrent_queries": {"type": "integer"},
                        "cache_size": {"type": "integer"},
                        "cache_max_ttl": {"type": "string"},
                        "use_doh": {"type": "boolean"},
                        "doh_server": {"type": "string"},
                        "verify_doh_cert": {"type": "boolean"}
                    },
                    "required": ["servers"]
                },
            ),
            Tool(
                name="mikrotik_get_dns_settings",
                description="Gets current DNS configuration",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": []
                },
            ),
            Tool(
                name="mikrotik_add_dns_static",
                description="Adds a static DNS entry",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "address": {"type": "string"},
                        "cname": {"type": "string"},
                        "mx_preference": {"type": "integer"},
                        "mx_exchange": {"type": "string"},
                        "text": {"type": "string"},
                        "srv_priority": {"type": "integer"},
                        "srv_weight": {"type": "integer"},
                        "srv_port": {"type": "integer"},
                        "srv_target": {"type": "string"},
                        "ttl": {"type": "string"},
                        "comment": {"type": "string"},
                        "disabled": {"type": "boolean"},
                        "regexp": {"type": "string"}
                    },
                    "required": ["name"]
                },
            ),
            Tool(
                name="mikrotik_list_dns_static",
                description="Lists static DNS entries",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name_filter": {"type": "string"},
                        "address_filter": {"type": "string"},
                        "type_filter": {"type": "string"},
                        "disabled_only": {"type": "boolean"},
                        "regexp_only": {"type": "boolean"}
                    },
                    "required": []
                },
            ),
            Tool(
                name="mikrotik_get_dns_static",
                description="Gets details of a specific static DNS entry",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "entry_id": {"type": "string"}
                    },
                    "required": ["entry_id"]
                },
            ),
            Tool(
                name="mikrotik_update_dns_static",
                description="Updates an existing static DNS entry",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "entry_id": {"type": "string"},
                        "name": {"type": "string"},
                        "address": {"type": "string"},
                        "cname": {"type": "string"},
                        "mx_preference": {"type": "integer"},
                        "mx_exchange": {"type": "string"},
                        "text": {"type": "string"},
                        "srv_priority": {"type": "integer"},
                        "srv_weight": {"type": "integer"},
                        "srv_port": {"type": "integer"},
                        "srv_target": {"type": "string"},
                        "ttl": {"type": "string"},
                        "comment": {"type": "string"},
                        "disabled": {"type": "boolean"},
                        "regexp": {"type": "string"}
                    },
                    "required": ["entry_id"]
                },
            ),
            Tool(
                name="mikrotik_remove_dns_static",
                description="Removes a static DNS entry",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "entry_id": {"type": "string"}
                    },
                    "required": ["entry_id"]
                },
            ),
            Tool(
                name="mikrotik_enable_dns_static",
                description="Enables a static DNS entry",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "entry_id": {"type": "string"}
                    },
                    "required": ["entry_id"]
                },
            ),
            Tool(
                name="mikrotik_disable_dns_static",
                description="Disables a static DNS entry",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "entry_id": {"type": "string"}
                    },
                    "required": ["entry_id"]
                },
            ),
            Tool(
                name="mikrotik_get_dns_cache",
                description="Gets the current DNS cache",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": []
                },
            ),
            Tool(
                name="mikrotik_flush_dns_cache",
                description="Flushes the DNS cache",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": []
                },
            ),
            Tool(
                name="mikrotik_get_dns_cache_statistics",
                description="Gets DNS cache statistics",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": []
                },
            ),
            Tool(
                name="mikrotik_add_dns_regexp",
                description="Adds a DNS regexp entry for pattern matching",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "regexp": {"type": "string"},
                        "address": {"type": "string"},
                        "ttl": {"type": "string"},
                        "comment": {"type": "string"},
                        "disabled": {"type": "boolean"}
                    },
                    "required": ["regexp", "address"]
                },
            ),
            Tool(
                name="mikrotik_test_dns_query",
                description="Tests a DNS query",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "server": {"type": "string"},
                        "type": {"type": "string"}
                    },
                    "required": ["name"]
                },
            ),
            Tool(
                name="mikrotik_export_dns_config",
                description="Exports DNS configuration to a file",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "filename": {"type": "string"}
                    },
                    "required": []
                },
            ),
            # User Management tools
            Tool(
                name="mikrotik_add_user",
                description="Adds a new user to MikroTik device",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "password": {"type": "string"},
                        "group": {"type": "string"},
                        "address": {"type": "string"},
                        "comment": {"type": "string"},
                        "disabled": {"type": "boolean"}
                    },
                    "required": ["name", "password"]
                },
            ),
            Tool(
                name="mikrotik_list_users",
                description="Lists users on MikroTik device",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name_filter": {"type": "string"},
                        "group_filter": {"type": "string"},
                        "disabled_only": {"type": "boolean"},
                        "active_only": {"type": "boolean"}
                    },
                    "required": []
                },
            ),
            Tool(
                name="mikrotik_get_user",
                description="Gets detailed information about a specific user",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"}
                    },
                    "required": ["name"]
                },
            ),
            Tool(
                name="mikrotik_update_user",
                description="Updates an existing user on MikroTik device",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "new_name": {"type": "string"},
                        "password": {"type": "string"},
                        "group": {"type": "string"},
                        "address": {"type": "string"},
                        "comment": {"type": "string"},
                        "disabled": {"type": "boolean"}
                    },
                    "required": ["name"]
                },
            ),
            Tool(
                name="mikrotik_remove_user",
                description="Removes a user from MikroTik device",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"}
                    },
                    "required": ["name"]
                },
            ),
            Tool(
                name="mikrotik_disable_user",
                description="Disables a user account",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"}
                    },
                    "required": ["name"]
                },
            ),
            Tool(
                name="mikrotik_enable_user",
                description="Enables a user account",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"}
                    },
                    "required": ["name"]
                },
            ),
            Tool(
                name="mikrotik_add_user_group",
                description="Adds a new user group to MikroTik device",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "policy": {"type": "array", "items": {"type": "string"}},
                        "skin": {"type": "string"},
                        "comment": {"type": "string"}
                    },
                    "required": ["name", "policy"]
                },
            ),
            Tool(
                name="mikrotik_list_user_groups",
                description="Lists user groups on MikroTik device",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name_filter": {"type": "string"},
                        "policy_filter": {"type": "string"}
                    },
                    "required": []
                },
            ),
            Tool(
                name="mikrotik_get_user_group",
                description="Gets detailed information about a specific user group",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"}
                    },
                    "required": ["name"]
                },
            ),
            Tool(
                name="mikrotik_update_user_group",
                description="Updates an existing user group on MikroTik device",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "new_name": {"type": "string"},
                        "policy": {"type": "array", "items": {"type": "string"}},
                        "skin": {"type": "string"},
                        "comment": {"type": "string"}
                    },
                    "required": ["name"]
                },
            ),
            Tool(
                name="mikrotik_remove_user_group",
                description="Removes a user group from MikroTik device",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"}
                    },
                    "required": ["name"]
                },
            ),
            Tool(
                name="mikrotik_get_active_users",
                description="Gets currently active/logged-in users",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": []
                },
            ),
            Tool(
                name="mikrotik_disconnect_user",
                description="Disconnects an active user session",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string"}
                    },
                    "required": ["user_id"]
                },
            ),
            Tool(
                name="mikrotik_export_user_config",
                description="Exports user configuration to a file",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "filename": {"type": "string"}
                    },
                    "required": []
                },
            ),
            Tool(
                name="mikrotik_set_user_ssh_keys",
                description="Sets SSH public keys for a user",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "username": {"type": "string"},
                        "key_file": {"type": "string"}
                    },
                    "required": ["username", "key_file"]
                },
            ),
            Tool(
                name="mikrotik_list_user_ssh_keys",
                description="Lists SSH keys for a specific user",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "username": {"type": "string"}
                    },
                    "required": ["username"]
                },
            ),
            Tool(
                name="mikrotik_remove_user_ssh_key",
                description="Removes an SSH key",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "key_id": {"type": "string"}
                    },
                    "required": ["key_id"]
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
        app_logger.info(f"Tool call: {name} with arguments {arguments}")

        result = ""

        # Use a dictionary mapping for "switch-case" approach
        command_handlers = {
            # Configuration commands
            "mikrotik_config_set": lambda: mikrotik_config_set(
                arguments.get("host"),
                arguments.get("username"),
                arguments.get("password"),
                arguments.get("port")
            ),
            "mikrotik_config_get": lambda: mikrotik_config_get(),
            
            # VLAN interface commands
            "mikrotik_create_vlan_interface": lambda: mikrotik_create_vlan_interface(
                arguments["name"],
                arguments["vlan_id"],
                arguments["interface"],
                arguments.get("comment"),
                arguments.get("disabled", False),
                arguments.get("mtu"),
                arguments.get("use_service_tag", False),
                arguments.get("arp", "enabled"),
                arguments.get("arp_timeout")
            ),
            "mikrotik_list_vlan_interfaces": lambda: mikrotik_list_vlan_interfaces(
                arguments.get("name_filter"),
                arguments.get("vlan_id_filter"),
                arguments.get("interface_filter"),
                arguments.get("disabled_only", False)
            ),
            "mikrotik_get_vlan_interface": lambda: mikrotik_get_vlan_interface(
                arguments["name"]
            ),
            "mikrotik_update_vlan_interface": lambda: mikrotik_update_vlan_interface(
                arguments["name"],
                arguments.get("new_name"),
                arguments.get("vlan_id"),
                arguments.get("interface"),
                arguments.get("comment"),
                arguments.get("disabled"),
                arguments.get("mtu"),
                arguments.get("use_service_tag"),
                arguments.get("arp"),
                arguments.get("arp_timeout")
            ),
            "mikrotik_remove_vlan_interface": lambda: mikrotik_remove_vlan_interface(
                arguments["name"]
            ),
            
            # IP Address commands
            "mikrotik_add_ip_address": lambda: mikrotik_add_ip_address(
                arguments["address"],
                arguments["interface"],
                arguments.get("network"),
                arguments.get("broadcast"),
                arguments.get("comment"),
                arguments.get("disabled", False)
            ),
            "mikrotik_list_ip_addresses": lambda: mikrotik_list_ip_addresses(
                arguments.get("interface_filter"),
                arguments.get("address_filter"),
                arguments.get("network_filter"),
                arguments.get("disabled_only", False),
                arguments.get("dynamic_only", False)
            ),
            "mikrotik_get_ip_address": lambda: mikrotik_get_ip_address(
                arguments["address_id"]
            ),
            "mikrotik_remove_ip_address": lambda: mikrotik_remove_ip_address(
                arguments["address_id"]
            ),
            
            # DHCP Server commands
            "mikrotik_create_dhcp_server": lambda: mikrotik_create_dhcp_server(
                arguments["name"],
                arguments["interface"],
                arguments.get("lease_time", "1d"),
                arguments.get("address_pool"),
                arguments.get("disabled", False),
                arguments.get("authoritative", "yes"),
                arguments.get("delay_threshold"),
                arguments.get("comment")
            ),
            "mikrotik_list_dhcp_servers": lambda: mikrotik_list_dhcp_servers(
                arguments.get("name_filter"),
                arguments.get("interface_filter"),
                arguments.get("disabled_only", False),
                arguments.get("invalid_only", False)
            ),
            "mikrotik_get_dhcp_server": lambda: mikrotik_get_dhcp_server(
                arguments["name"]
            ),
            "mikrotik_create_dhcp_network": lambda: mikrotik_create_dhcp_network(
                arguments["network"],
                arguments["gateway"],
                arguments.get("netmask"),
                arguments.get("dns_servers"),
                arguments.get("domain"),
                arguments.get("wins_servers"),
                arguments.get("ntp_servers"),
                arguments.get("dhcp_option"),
                arguments.get("comment")
            ),
            "mikrotik_create_dhcp_pool": lambda: mikrotik_create_dhcp_pool(
                arguments["name"],
                arguments["ranges"],
                arguments.get("next_pool"),
                arguments.get("comment")
            ),
            "mikrotik_remove_dhcp_server": lambda: mikrotik_remove_dhcp_server(
                arguments["name"]
            ),
            # NAT commands
            "mikrotik_create_nat_rule": lambda: mikrotik_create_nat_rule(
                arguments["chain"],
                arguments["action"],
                arguments.get("src_address"),
                arguments.get("dst_address"),
                arguments.get("src_port"),
                arguments.get("dst_port"),
                arguments.get("protocol"),
                arguments.get("in_interface"),
                arguments.get("out_interface"),
                arguments.get("to_addresses"),
                arguments.get("to_ports"),
                arguments.get("comment"),
                arguments.get("disabled", False),
                arguments.get("log", False),
                arguments.get("log_prefix"),
                arguments.get("place_before")
            ),
            "mikrotik_list_nat_rules": lambda: mikrotik_list_nat_rules(
                arguments.get("chain_filter"),
                arguments.get("action_filter"),
                arguments.get("src_address_filter"),
                arguments.get("dst_address_filter"),
                arguments.get("protocol_filter"),
                arguments.get("interface_filter"),
                arguments.get("disabled_only", False),
                arguments.get("invalid_only", False)
            ),
            "mikrotik_get_nat_rule": lambda: mikrotik_get_nat_rule(
                arguments["rule_id"]
            ),
            "mikrotik_update_nat_rule": lambda: mikrotik_update_nat_rule(
                arguments["rule_id"],
                arguments.get("chain"),
                arguments.get("action"),
                arguments.get("src_address"),
                arguments.get("dst_address"),
                arguments.get("src_port"),
                arguments.get("dst_port"),
                arguments.get("protocol"),
                arguments.get("in_interface"),
                arguments.get("out_interface"),
                arguments.get("to_addresses"),
                arguments.get("to_ports"),
                arguments.get("comment"),
                arguments.get("disabled"),
                arguments.get("log"),
                arguments.get("log_prefix")
            ),
            "mikrotik_remove_nat_rule": lambda: mikrotik_remove_nat_rule(
                arguments["rule_id"]
            ),
            "mikrotik_move_nat_rule": lambda: mikrotik_move_nat_rule(
                arguments["rule_id"],
                arguments["destination"]
            ),
            "mikrotik_enable_nat_rule": lambda: mikrotik_enable_nat_rule(
                arguments["rule_id"]
            ),
            "mikrotik_disable_nat_rule": lambda: mikrotik_disable_nat_rule(
                arguments["rule_id"]
            ),
            # IP Pool commands
            "mikrotik_create_ip_pool": lambda: mikrotik_create_ip_pool(
                arguments["name"],
                arguments["ranges"],
                arguments.get("next_pool"),
                arguments.get("comment")
            ),
            "mikrotik_list_ip_pools": lambda: mikrotik_list_ip_pools(
                arguments.get("name_filter"),
                arguments.get("ranges_filter"),
                arguments.get("include_used", False)
            ),
            "mikrotik_get_ip_pool": lambda: mikrotik_get_ip_pool(
                arguments["name"]
            ),
            "mikrotik_update_ip_pool": lambda: mikrotik_update_ip_pool(
                arguments["name"],
                arguments.get("new_name"),
                arguments.get("ranges"),
                arguments.get("next_pool"),
                arguments.get("comment")
            ),
            "mikrotik_remove_ip_pool": lambda: mikrotik_remove_ip_pool(
                arguments["name"]
            ),
            "mikrotik_list_ip_pool_used": lambda: mikrotik_list_ip_pool_used(
                arguments.get("pool_name"),
                arguments.get("address_filter"),
                arguments.get("mac_filter"),
                arguments.get("info_filter")
            ),
            "mikrotik_expand_ip_pool": lambda: mikrotik_expand_ip_pool(
                arguments["name"],
                arguments["additional_ranges"]
            ),
            # Backup and Export commands
            "mikrotik_create_backup": lambda: mikrotik_create_backup(
                arguments.get("name"),
                arguments.get("dont_encrypt", False),
                arguments.get("include_password", True),
                arguments.get("comment")
            ),
            "mikrotik_list_backups": lambda: mikrotik_list_backups(
                arguments.get("name_filter"),
                arguments.get("include_exports", False)
            ),
            "mikrotik_create_export": lambda: mikrotik_create_export(
                arguments.get("name"),
                arguments.get("file_format", "rsc"),
                arguments.get("export_type", "full"),
                arguments.get("hide_sensitive", True),
                arguments.get("verbose", False),
                arguments.get("compact", False),
                arguments.get("comment")
            ),
            "mikrotik_export_section": lambda: mikrotik_export_section(
                arguments["section"],
                arguments.get("name"),
                arguments.get("hide_sensitive", True),
                arguments.get("compact", False)
            ),
            "mikrotik_download_file": lambda: mikrotik_download_file(
                arguments["filename"],
                arguments.get("file_type", "backup")
            ),
            "mikrotik_upload_file": lambda: mikrotik_upload_file(
                arguments["filename"],
                arguments["content_base64"]
            ),
            "mikrotik_restore_backup": lambda: mikrotik_restore_backup(
                arguments["filename"],
                arguments.get("password")
            ),
            "mikrotik_import_configuration": lambda: mikrotik_import_configuration(
                arguments["filename"],
                arguments.get("run_after_reset", False),
                arguments.get("verbose", False)
            ),
            "mikrotik_remove_file": lambda: mikrotik_remove_file(
                arguments["filename"]
            ),
            "mikrotik_backup_info": lambda: mikrotik_backup_info(
                arguments["filename"]
            ),
            # Log commands
            "mikrotik_get_logs": lambda: mikrotik_get_logs(
                arguments.get("topics"),
                arguments.get("action"),
                arguments.get("time_filter"),
                arguments.get("message_filter"),
                arguments.get("prefix_filter"),
                arguments.get("limit"),
                arguments.get("follow", False),
                arguments.get("print_as", "value")
            ),
            "mikrotik_get_logs_by_severity": lambda: mikrotik_get_logs_by_severity(
                arguments["severity"],
                arguments.get("time_filter"),
                arguments.get("limit")
            ),
            "mikrotik_get_logs_by_topic": lambda: mikrotik_get_logs_by_topic(
                arguments["topic"],
                arguments.get("time_filter"),
                arguments.get("limit")
            ),
            "mikrotik_search_logs": lambda: mikrotik_search_logs(
                arguments["search_term"],
                arguments.get("time_filter"),
                arguments.get("case_sensitive", False),
                arguments.get("limit")
            ),
            "mikrotik_get_system_events": lambda: mikrotik_get_system_events(
                arguments.get("event_type"),
                arguments.get("time_filter"),
                arguments.get("limit")
            ),
            "mikrotik_get_security_logs": lambda: mikrotik_get_security_logs(
                arguments.get("time_filter"),
                arguments.get("limit")
            ),
            "mikrotik_clear_logs": lambda: mikrotik_clear_logs(),
            "mikrotik_get_log_statistics": lambda: mikrotik_get_log_statistics(),
            "mikrotik_export_logs": lambda: mikrotik_export_logs(
                arguments.get("filename"),
                arguments.get("topics"),
                arguments.get("time_filter"),
                arguments.get("format", "plain")
            ),
            "mikrotik_monitor_logs": lambda: mikrotik_monitor_logs(
                arguments.get("topics"),
                arguments.get("action"),
                arguments.get("duration", 10)
            ),
            # Firewall Filter commands
            "mikrotik_create_filter_rule": lambda: mikrotik_create_filter_rule(
                arguments["chain"],
                arguments["action"],
                arguments.get("src_address"),
                arguments.get("dst_address"),
                arguments.get("src_port"),
                arguments.get("dst_port"),
                arguments.get("protocol"),
                arguments.get("in_interface"),
                arguments.get("out_interface"),
                arguments.get("connection_state"),
                arguments.get("connection_nat_state"),
                arguments.get("src_address_list"),
                arguments.get("dst_address_list"),
                arguments.get("limit"),
                arguments.get("tcp_flags"),
                arguments.get("comment"),
                arguments.get("disabled", False),
                arguments.get("log", False),
                arguments.get("log_prefix"),
                arguments.get("place_before")
            ),
            "mikrotik_list_filter_rules": lambda: mikrotik_list_filter_rules(
                arguments.get("chain_filter"),
                arguments.get("action_filter"),
                arguments.get("src_address_filter"),
                arguments.get("dst_address_filter"),
                arguments.get("protocol_filter"),
                arguments.get("interface_filter"),
                arguments.get("disabled_only", False),
                arguments.get("invalid_only", False),
                arguments.get("dynamic_only", False)
            ),
            "mikrotik_get_filter_rule": lambda: mikrotik_get_filter_rule(
                arguments["rule_id"]
            ),
            "mikrotik_update_filter_rule": lambda: mikrotik_update_filter_rule(
                arguments["rule_id"],
                arguments.get("chain"),
                arguments.get("action"),
                arguments.get("src_address"),
                arguments.get("dst_address"),
                arguments.get("src_port"),
                arguments.get("dst_port"),
                arguments.get("protocol"),
                arguments.get("in_interface"),
                arguments.get("out_interface"),
                arguments.get("connection_state"),
                arguments.get("connection_nat_state"),
                arguments.get("src_address_list"),
                arguments.get("dst_address_list"),
                arguments.get("limit"),
                arguments.get("tcp_flags"),
                arguments.get("comment"),
                arguments.get("disabled"),
                arguments.get("log"),
                arguments.get("log_prefix")
            ),
            "mikrotik_remove_filter_rule": lambda: mikrotik_remove_filter_rule(
                arguments["rule_id"]
            ),
            "mikrotik_move_filter_rule": lambda: mikrotik_move_filter_rule(
                arguments["rule_id"],
                arguments["destination"]
            ),
            "mikrotik_enable_filter_rule": lambda: mikrotik_enable_filter_rule(
                arguments["rule_id"]
            ),
            "mikrotik_disable_filter_rule": lambda: mikrotik_disable_filter_rule(
                arguments["rule_id"]
            ),
            "mikrotik_create_basic_firewall_setup": lambda: mikrotik_create_basic_firewall_setup(),
            # Route commands
            "mikrotik_add_route": lambda: mikrotik_add_route(
                arguments["dst_address"],
                arguments["gateway"],
                arguments.get("distance"),
                arguments.get("scope"),
                arguments.get("target_scope"),
                arguments.get("routing_mark"),
                arguments.get("comment"),
                arguments.get("disabled", False),
                arguments.get("vrf_interface"),
                arguments.get("pref_src"),
                arguments.get("check_gateway")
            ),
            "mikrotik_list_routes": lambda: mikrotik_list_routes(
                arguments.get("dst_filter"),
                arguments.get("gateway_filter"),
                arguments.get("routing_mark_filter"),
                arguments.get("distance_filter"),
                arguments.get("active_only", False),
                arguments.get("disabled_only", False),
                arguments.get("dynamic_only", False),
                arguments.get("static_only", False)
            ),
            "mikrotik_get_route": lambda: mikrotik_get_route(
                arguments["route_id"]
            ),
            "mikrotik_update_route": lambda: mikrotik_update_route(
                arguments["route_id"],
                arguments.get("dst_address"),
                arguments.get("gateway"),
                arguments.get("distance"),
                arguments.get("scope"),
                arguments.get("target_scope"),
                arguments.get("routing_mark"),
                arguments.get("comment"),
                arguments.get("disabled"),
                arguments.get("vrf_interface"),
                arguments.get("pref_src"),
                arguments.get("check_gateway")
            ),
            "mikrotik_remove_route": lambda: mikrotik_remove_route(
                arguments["route_id"]
            ),
            "mikrotik_enable_route": lambda: mikrotik_enable_route(
                arguments["route_id"]
            ),
            "mikrotik_disable_route": lambda: mikrotik_disable_route(
                arguments["route_id"]
            ),
            "mikrotik_get_routing_table": lambda: mikrotik_get_routing_table(
                arguments.get("table_name", "main"),
                arguments.get("protocol_filter"),
                arguments.get("active_only", True)
            ),
            "mikrotik_check_route_path": lambda: mikrotik_check_route_path(
                arguments["destination"],
                arguments.get("source"),
                arguments.get("routing_mark")
            ),
            "mikrotik_get_route_cache": lambda: mikrotik_get_route_cache(),
            "mikrotik_flush_route_cache": lambda: mikrotik_flush_route_cache(),
            "mikrotik_add_default_route": lambda: mikrotik_add_default_route(
                arguments["gateway"],
                arguments.get("distance", 1),
                arguments.get("comment"),
                arguments.get("check_gateway", "ping")
            ),
            "mikrotik_add_blackhole_route": lambda: mikrotik_add_blackhole_route(
                arguments["dst_address"],
                arguments.get("distance", 1),
                arguments.get("comment")
            ),
            "mikrotik_get_route_statistics": lambda: mikrotik_get_route_statistics(),
            # DNS commands
            "mikrotik_set_dns_servers": lambda: mikrotik_set_dns_servers(
                arguments["servers"],
                arguments.get("allow_remote_requests", False),
                arguments.get("max_udp_packet_size"),
                arguments.get("max_concurrent_queries"),
                arguments.get("cache_size"),
                arguments.get("cache_max_ttl"),
                arguments.get("use_doh", False),
                arguments.get("doh_server"),
                arguments.get("verify_doh_cert", True)
            ),
            "mikrotik_get_dns_settings": lambda: mikrotik_get_dns_settings(),
            "mikrotik_add_dns_static": lambda: mikrotik_add_dns_static(
                arguments["name"],
                arguments.get("address"),
                arguments.get("cname"),
                arguments.get("mx_preference"),
                arguments.get("mx_exchange"),
                arguments.get("text"),
                arguments.get("srv_priority"),
                arguments.get("srv_weight"),
                arguments.get("srv_port"),
                arguments.get("srv_target"),
                arguments.get("ttl"),
                arguments.get("comment"),
                arguments.get("disabled", False),
                arguments.get("regexp")
            ),
            "mikrotik_list_dns_static": lambda: mikrotik_list_dns_static(
                arguments.get("name_filter"),
                arguments.get("address_filter"),
                arguments.get("type_filter"),
                arguments.get("disabled_only", False),
                arguments.get("regexp_only", False)
            ),
            "mikrotik_get_dns_static": lambda: mikrotik_get_dns_static(
                arguments["entry_id"]
            ),
            "mikrotik_update_dns_static": lambda: mikrotik_update_dns_static(
                arguments["entry_id"],
                arguments.get("name"),
                arguments.get("address"),
                arguments.get("cname"),
                arguments.get("mx_preference"),
                arguments.get("mx_exchange"),
                arguments.get("text"),
                arguments.get("srv_priority"),
                arguments.get("srv_weight"),
                arguments.get("srv_port"),
                arguments.get("srv_target"),
                arguments.get("ttl"),
                arguments.get("comment"),
                arguments.get("disabled"),
                arguments.get("regexp")
            ),
            "mikrotik_remove_dns_static": lambda: mikrotik_remove_dns_static(
                arguments["entry_id"]
            ),
            "mikrotik_enable_dns_static": lambda: mikrotik_enable_dns_static(
                arguments["entry_id"]
            ),
            "mikrotik_disable_dns_static": lambda: mikrotik_disable_dns_static(
                arguments["entry_id"]
            ),
            "mikrotik_get_dns_cache": lambda: mikrotik_get_dns_cache(),
            "mikrotik_flush_dns_cache": lambda: mikrotik_flush_dns_cache(),
            "mikrotik_get_dns_cache_statistics": lambda: mikrotik_get_dns_cache_statistics(),
            "mikrotik_add_dns_regexp": lambda: mikrotik_add_dns_regexp(
                arguments["regexp"],
                arguments["address"],
                arguments.get("ttl", "1d"),
                arguments.get("comment"),
                arguments.get("disabled", False)
            ),
            "mikrotik_test_dns_query": lambda: mikrotik_test_dns_query(
                arguments["name"],
                arguments.get("server"),
                arguments.get("type", "A")
            ),
            "mikrotik_export_dns_config": lambda: mikrotik_export_dns_config(
                arguments.get("filename")
            ),
            # User Management commands
            "mikrotik_add_user": lambda: mikrotik_add_user(
                arguments["name"],
                arguments["password"],
                arguments.get("group", "read"),
                arguments.get("address"),
                arguments.get("comment"),
                arguments.get("disabled", False)
            ),
            "mikrotik_list_users": lambda: mikrotik_list_users(
                arguments.get("name_filter"),
                arguments.get("group_filter"),
                arguments.get("disabled_only", False),
                arguments.get("active_only", False)
            ),
            "mikrotik_get_user": lambda: mikrotik_get_user(
                arguments["name"]
            ),
            "mikrotik_update_user": lambda: mikrotik_update_user(
                arguments["name"],
                arguments.get("new_name"),
                arguments.get("password"),
                arguments.get("group"),
                arguments.get("address"),
                arguments.get("comment"),
                arguments.get("disabled")
            ),
            "mikrotik_remove_user": lambda: mikrotik_remove_user(
                arguments["name"]
            ),
            "mikrotik_disable_user": lambda: mikrotik_disable_user(
                arguments["name"]
            ),
            "mikrotik_enable_user": lambda: mikrotik_enable_user(
                arguments["name"]
            ),
            "mikrotik_add_user_group": lambda: mikrotik_add_user_group(
                arguments["name"],
                arguments["policy"],
                arguments.get("skin"),
                arguments.get("comment")
            ),
            "mikrotik_list_user_groups": lambda: mikrotik_list_user_groups(
                arguments.get("name_filter"),
                arguments.get("policy_filter")
            ),
            "mikrotik_get_user_group": lambda: mikrotik_get_user_group(
                arguments["name"]
            ),
            "mikrotik_update_user_group": lambda: mikrotik_update_user_group(
                arguments["name"],
                arguments.get("new_name"),
                arguments.get("policy"),
                arguments.get("skin"),
                arguments.get("comment")
            ),
            "mikrotik_remove_user_group": lambda: mikrotik_remove_user_group(
                arguments["name"]
            ),
            "mikrotik_get_active_users": lambda: mikrotik_get_active_users(),
            "mikrotik_disconnect_user": lambda: mikrotik_disconnect_user(
                arguments["user_id"]
            ),
            "mikrotik_export_user_config": lambda: mikrotik_export_user_config(
                arguments.get("filename")
            ),
            "mikrotik_set_user_ssh_keys": lambda: mikrotik_set_user_ssh_keys(
                arguments["username"],
                arguments["key_file"]
            ),
            "mikrotik_list_user_ssh_keys": lambda: mikrotik_list_user_ssh_keys(
                arguments["username"]
            ),
            "mikrotik_remove_user_ssh_key": lambda: mikrotik_remove_user_ssh_key(
                arguments["key_id"]
            ),
        }

        # Execute the corresponding handler or return an error if the command is not found
        if name in command_handlers:
            try:
                result = command_handlers[name]()
            except Exception as e:
                error_msg = f"Error executing {name}: {str(e)}"
                app_logger.error(error_msg)
                return [TextContent(type="text", text=error_msg)]
        else:
            error_msg = f"Unknown tool: {name}"
            app_logger.error(error_msg)
            return [TextContent(type="text", text=error_msg)]

        return [TextContent(type="text", text=result)]

    app_logger.info("Creating initialization options")
    options = server.create_initialization_options()

    app_logger.info("Starting stdio server")
    async with stdio_server() as (read_stream, write_stream):
        app_logger.info("Running MCP server")
        await server.run(read_stream, write_stream, options, raise_exceptions=True)
