from typing import Dict, Any, List, Callable
from ..scope.packages import (
    mikrotik_list_packages,
    mikrotik_get_package,
    mikrotik_enable_package,
    mikrotik_disable_package,
    mikrotik_uninstall_package,
    mikrotik_update_packages,
    mikrotik_install_updates,
    mikrotik_download_package,
    mikrotik_get_package_update_status,
    mikrotik_set_update_channel,
    mikrotik_list_available_packages
)
from ..scope.scheduler import (
    mikrotik_list_scheduled_tasks,
    mikrotik_get_scheduled_task,
    mikrotik_create_scheduled_task,
    mikrotik_update_scheduled_task,
    mikrotik_remove_scheduled_task,
    mikrotik_enable_scheduled_task,
    mikrotik_disable_scheduled_task,
    mikrotik_run_scheduled_task,
    mikrotik_create_backup_schedule
)
from ..scope.watchdog import (
    mikrotik_get_watchdog_status,
    mikrotik_enable_watchdog,
    mikrotik_disable_watchdog,
    mikrotik_get_watchdog_types,
    mikrotik_set_watchdog_ping_target,
    mikrotik_reset_watchdog_ping_target,
    mikrotik_create_watchdog_script,
    mikrotik_create_basic_watchdog_monitor
)
from ..scope.system import (
    mikrotik_get_system_resources, mikrotik_get_system_health, mikrotik_get_system_identity,
    mikrotik_set_system_identity, mikrotik_get_system_clock, mikrotik_get_ntp_client,
    mikrotik_set_ntp_client, mikrotik_reboot_system, mikrotik_get_routerboard,
    mikrotik_get_license, mikrotik_get_uptime
)
from mcp.types import Tool

def get_system_tools() -> List[Tool]:
    """Return the list of system management tools."""
    return [
        Tool(
            name="mikrotik_get_system_resources",
            description="Gets system resource usage (CPU, RAM, disk, uptime)",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        Tool(
            name="mikrotik_get_system_health",
            description="Gets system health (temperature, voltage, fans)",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        Tool(
            name="mikrotik_get_system_identity",
            description="Gets system identity/name",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        Tool(
            name="mikrotik_set_system_identity",
            description="Sets system identity/name",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"}
                },
                "required": ["name"]
            },
        ),
        Tool(
            name="mikrotik_get_system_clock",
            description="Gets system clock settings",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        Tool(
            name="mikrotik_get_ntp_client",
            description="Gets NTP client configuration",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        Tool(
            name="mikrotik_set_ntp_client",
            description="Configures NTP client for time synchronization",
            inputSchema={
                "type": "object",
                "properties": {
                    "enabled": {"type": "boolean"},
                    "servers": {"type": "string"},
                    "mode": {"type": "string", "enum": ["unicast", "broadcast", "multicast"]}
                },
                "required": []
            },
        ),
        Tool(
            name="mikrotik_reboot_system",
            description="Reboots the MikroTik device (requires confirmation)",
            inputSchema={
                "type": "object",
                "properties": {
                    "confirm": {"type": "boolean"}
                },
                "required": ["confirm"]
            },
        ),
        Tool(
            name="mikrotik_get_routerboard",
            description="Gets RouterBOARD hardware information",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        Tool(
            name="mikrotik_get_license",
            description="Gets RouterOS license information",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        Tool(
            name="mikrotik_get_uptime",
            description="Gets system uptime",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        # Package management tools
        Tool(
            name="mikrotik_list_packages",
            description="Lists installed packages on MikroTik device (READ-ONLY, safe)",
            inputSchema={
                "type": "object",
                "properties": {
                    "disabled_only": {"type": "boolean"},
                    "name_filter": {"type": "string"}
                },
                "required": []
            },
        ),
        Tool(
            name="mikrotik_get_package",
            description="Gets detailed information about a specific package (READ-ONLY, safe)",
            inputSchema={
                "type": "object",
                "properties": {
                    "package_name": {"type": "string"}
                },
                "required": ["package_name"]
            },
        ),
        Tool(
            name="mikrotik_enable_package",
            description="Enables a package (requires reboot)",
            inputSchema={
                "type": "object",
                "properties": {
                    "package_name": {"type": "string"}
                },
                "required": ["package_name"]
            },
        ),
        Tool(
            name="mikrotik_disable_package",
            description="Disables a package (requires reboot)",
            inputSchema={
                "type": "object",
                "properties": {
                    "package_name": {"type": "string"}
                },
                "required": ["package_name"]
            },
        ),
        Tool(
            name="mikrotik_uninstall_package",
            description="Uninstalls a package (⚠️ requires reboot)",
            inputSchema={
                "type": "object",
                "properties": {
                    "package_name": {"type": "string"}
                },
                "required": ["package_name"]
            },
        ),
        Tool(
            name="mikrotik_update_packages",
            description="Checks for and downloads package updates",
            inputSchema={
                "type": "object",
                "properties": {
                    "channel": {"type": "string", "enum": ["stable", "testing", "development"]}
                },
                "required": []
            },
        ),
        Tool(
            name="mikrotik_install_updates",
            description="Installs downloaded package updates (⚠️ reboots router!)",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        Tool(
            name="mikrotik_download_package",
            description="Downloads a package from a URL",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {"type": "string"}
                },
                "required": ["url"]
            },
        ),
        Tool(
            name="mikrotik_get_package_update_status",
            description="Gets the current package update status (READ-ONLY, safe)",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        Tool(
            name="mikrotik_set_update_channel",
            description="Sets the update channel for package updates",
            inputSchema={
                "type": "object",
                "properties": {
                    "channel": {"type": "string", "enum": ["stable", "testing", "development", "long-term"]}
                },
                "required": ["channel"]
            },
        ),
        Tool(
            name="mikrotik_list_available_packages",
            description="Lists all available packages that can be installed (READ-ONLY, safe)",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        # Scheduler tools
        Tool(
            name="mikrotik_list_scheduled_tasks",
            description="Lists scheduled tasks on MikroTik device (READ-ONLY, safe)",
            inputSchema={
                "type": "object",
                "properties": {
                    "name_filter": {"type": "string"},
                    "disabled_only": {"type": "boolean"}
                },
                "required": []
            },
        ),
        Tool(
            name="mikrotik_get_scheduled_task",
            description="Gets detailed information about a specific scheduled task (READ-ONLY, safe)",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "string"}
                },
                "required": ["task_id"]
            },
        ),
        Tool(
            name="mikrotik_create_scheduled_task",
            description="Creates a scheduled task on MikroTik device",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "on_event": {"type": "string", "description": "Script code or script name to execute"},
                    "start_date": {"type": "string", "description": "Start date (MMM/DD/YYYY)"},
                    "start_time": {"type": "string", "description": "Start time (HH:MM:SS)"},
                    "interval": {"type": "string", "description": "Run interval (e.g., 1d, 1h30m, 5m)"},
                    "policy": {"type": "string"},
                    "comment": {"type": "string"},
                    "disabled": {"type": "boolean"}
                },
                "required": ["name", "on_event"]
            },
        ),
        Tool(
            name="mikrotik_update_scheduled_task",
            description="Updates an existing scheduled task",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "string"},
                    "name": {"type": "string"},
                    "on_event": {"type": "string"},
                    "start_date": {"type": "string"},
                    "start_time": {"type": "string"},
                    "interval": {"type": "string"},
                    "policy": {"type": "string"},
                    "comment": {"type": "string"},
                    "disabled": {"type": "boolean"}
                },
                "required": ["task_id"]
            },
        ),
        Tool(
            name="mikrotik_remove_scheduled_task",
            description="Removes a scheduled task",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "string"}
                },
                "required": ["task_id"]
            },
        ),
        Tool(
            name="mikrotik_enable_scheduled_task",
            description="Enables a scheduled task",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "string"}
                },
                "required": ["task_id"]
            },
        ),
        Tool(
            name="mikrotik_disable_scheduled_task",
            description="Disables a scheduled task",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "string"}
                },
                "required": ["task_id"]
            },
        ),
        Tool(
            name="mikrotik_run_scheduled_task",
            description="Manually runs a scheduled task immediately",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "string"}
                },
                "required": ["task_id"]
            },
        ),
        Tool(
            name="mikrotik_create_backup_schedule",
            description="Creates a scheduled backup task",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "interval": {"type": "string", "description": "Backup interval (e.g., 1d, 12h, 1w)"},
                    "backup_name_prefix": {"type": "string", "default": "auto-backup"},
                    "password": {"type": "string"}
                },
                "required": ["name", "interval"]
            },
        ),
        # Watchdog tools
        Tool(
            name="mikrotik_get_watchdog_status",
            description="Gets the current watchdog status and settings (READ-ONLY, safe)",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        Tool(
            name="mikrotik_enable_watchdog",
            description="Enables and configures the watchdog",
            inputSchema={
                "type": "object",
                "properties": {
                    "watchdog_timer": {"type": "boolean", "default": True},
                    "automatic_supout": {"type": "boolean", "default": True},
                    "auto_send_supout": {"type": "boolean", "default": False},
                    "send_email_to": {"type": "string"},
                    "send_smtp_server": {"type": "string"},
                    "no_ping_delay": {"type": "string"},
                    "ping_start_after_boot": {"type": "string"},
                    "ping_timeout": {"type": "string"}
                },
                "required": []
            },
        ),
        Tool(
            name="mikrotik_disable_watchdog",
            description="Disables the watchdog",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        Tool(
            name="mikrotik_get_watchdog_types",
            description="Lists available watchdog timer types (READ-ONLY, safe)",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        Tool(
            name="mikrotik_set_watchdog_ping_target",
            description="Sets the ping target for watchdog monitoring (reboots if ping fails)",
            inputSchema={
                "type": "object",
                "properties": {
                    "ip_address": {"type": "string"}
                },
                "required": ["ip_address"]
            },
        ),
        Tool(
            name="mikrotik_reset_watchdog_ping_target",
            description="Removes the ping target from watchdog monitoring",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        Tool(
            name="mikrotik_create_watchdog_script",
            description="Creates a watchdog monitoring script",
            inputSchema={
                "type": "object",
                "properties": {
                    "script_name": {"type": "string"},
                    "script_content": {"type": "string"},
                    "trigger_type": {"type": "string", "enum": ["reboot", "email", "both"], "default": "reboot"}
                },
                "required": ["script_name", "script_content"]
            },
        ),
        Tool(
            name="mikrotik_create_basic_watchdog_monitor",
            description="Creates a basic watchdog monitoring setup",
            inputSchema={
                "type": "object",
                "properties": {
                    "monitor_name": {"type": "string"},
                    "check_interval": {"type": "string", "default": "5m"},
                    "ping_target": {"type": "string"},
                    "reboot_on_failure": {"type": "boolean", "default": True}
                },
                "required": ["monitor_name"]
            },
        ),
    ]

def get_system_handlers() -> Dict[str, Callable]:
    """Return the handlers for system management tools."""
    return {
        "mikrotik_get_system_resources": lambda args: mikrotik_get_system_resources(),
        "mikrotik_get_system_health": lambda args: mikrotik_get_system_health(),
        "mikrotik_get_system_identity": lambda args: mikrotik_get_system_identity(),
        "mikrotik_set_system_identity": lambda args: mikrotik_set_system_identity(
            args["name"]
        ),
        "mikrotik_get_system_clock": lambda args: mikrotik_get_system_clock(),
        "mikrotik_get_ntp_client": lambda args: mikrotik_get_ntp_client(),
        "mikrotik_set_ntp_client": lambda args: mikrotik_set_ntp_client(
            args.get("enabled", True),
            args.get("servers"),
            args.get("mode")
        ),
        "mikrotik_reboot_system": lambda args: mikrotik_reboot_system(
            args.get("confirm", False)
        ),
        "mikrotik_get_routerboard": lambda args: mikrotik_get_routerboard(),
        "mikrotik_get_license": lambda args: mikrotik_get_license(),
        "mikrotik_get_uptime": lambda args: mikrotik_get_uptime(),
        # Package management handlers
        "mikrotik_list_packages": lambda args: mikrotik_list_packages(
            args.get("disabled_only", False),
            args.get("name_filter")
        ),
        "mikrotik_get_package": lambda args: mikrotik_get_package(
            args["package_name"]
        ),
        "mikrotik_enable_package": lambda args: mikrotik_enable_package(
            args["package_name"]
        ),
        "mikrotik_disable_package": lambda args: mikrotik_disable_package(
            args["package_name"]
        ),
        "mikrotik_uninstall_package": lambda args: mikrotik_uninstall_package(
            args["package_name"]
        ),
        "mikrotik_update_packages": lambda args: mikrotik_update_packages(
            args.get("channel")
        ),
        "mikrotik_install_updates": lambda args: mikrotik_install_updates(),
        "mikrotik_download_package": lambda args: mikrotik_download_package(
            args["url"]
        ),
        "mikrotik_get_package_update_status": lambda args: mikrotik_get_package_update_status(),
        "mikrotik_set_update_channel": lambda args: mikrotik_set_update_channel(
            args["channel"]
        ),
        "mikrotik_list_available_packages": lambda args: mikrotik_list_available_packages(),
        # Scheduler handlers
        "mikrotik_list_scheduled_tasks": lambda args: mikrotik_list_scheduled_tasks(
            args.get("name_filter"),
            args.get("disabled_only", False)
        ),
        "mikrotik_get_scheduled_task": lambda args: mikrotik_get_scheduled_task(
            args["task_id"]
        ),
        "mikrotik_create_scheduled_task": lambda args: mikrotik_create_scheduled_task(
            args["name"],
            args["on_event"],
            args.get("start_date"),
            args.get("start_time"),
            args.get("interval"),
            args.get("policy"),
            args.get("comment"),
            args.get("disabled", False)
        ),
        "mikrotik_update_scheduled_task": lambda args: mikrotik_update_scheduled_task(
            args["task_id"],
            args.get("name"),
            args.get("on_event"),
            args.get("start_date"),
            args.get("start_time"),
            args.get("interval"),
            args.get("policy"),
            args.get("comment"),
            args.get("disabled")
        ),
        "mikrotik_remove_scheduled_task": lambda args: mikrotik_remove_scheduled_task(
            args["task_id"]
        ),
        "mikrotik_enable_scheduled_task": lambda args: mikrotik_enable_scheduled_task(
            args["task_id"]
        ),
        "mikrotik_disable_scheduled_task": lambda args: mikrotik_disable_scheduled_task(
            args["task_id"]
        ),
        "mikrotik_run_scheduled_task": lambda args: mikrotik_run_scheduled_task(
            args["task_id"]
        ),
        "mikrotik_create_backup_schedule": lambda args: mikrotik_create_backup_schedule(
            args["name"],
            args["interval"],
            args.get("backup_name_prefix", "auto-backup"),
            args.get("password")
        ),
        # Watchdog handlers
        "mikrotik_get_watchdog_status": lambda args: mikrotik_get_watchdog_status(),
        "mikrotik_enable_watchdog": lambda args: mikrotik_enable_watchdog(
            args.get("watchdog_timer", True),
            args.get("automatic_supout", True),
            args.get("auto_send_supout", False),
            args.get("send_email_to"),
            args.get("send_smtp_server"),
            args.get("no_ping_delay"),
            args.get("ping_start_after_boot"),
            args.get("ping_timeout")
        ),
        "mikrotik_disable_watchdog": lambda args: mikrotik_disable_watchdog(),
        "mikrotik_get_watchdog_types": lambda args: mikrotik_get_watchdog_types(),
        "mikrotik_set_watchdog_ping_target": lambda args: mikrotik_set_watchdog_ping_target(
            args["ip_address"]
        ),
        "mikrotik_reset_watchdog_ping_target": lambda args: mikrotik_reset_watchdog_ping_target(),
        "mikrotik_create_watchdog_script": lambda args: mikrotik_create_watchdog_script(
            args["script_name"],
            args["script_content"],
            args.get("trigger_type", "reboot")
        ),
        "mikrotik_create_basic_watchdog_monitor": lambda args: mikrotik_create_basic_watchdog_monitor(
            args["monitor_name"],
            args.get("check_interval", "5m"),
            args.get("ping_target"),
            args.get("reboot_on_failure", True)
        ),
    }

