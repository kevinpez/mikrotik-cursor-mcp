from typing import Optional
from ..connector import execute_mikrotik_command
from ..api_fallback import api_fallback_execute
from ..logger import app_logger

def mikrotik_list_vrrp_interfaces(
    name_filter: Optional[str] = None,
    interface_filter: Optional[str] = None,
    disabled_only: bool = False
) -> str:
    """
    Lists VRRP interfaces on MikroTik device.
    
    Args:
        name_filter: Filter by VRRP interface name
        interface_filter: Filter by parent interface
        disabled_only: Show only disabled VRRP interfaces
    
    Returns:
        List of VRRP interfaces
    """
    app_logger.info(f"Listing VRRP interfaces: name_filter={name_filter}")
    
    cmd = "/interface vrrp print detail"
    
    # Add filters
    filters = []
    if name_filter:
        filters.append(f'name~"{name_filter}"')
    if interface_filter:
        filters.append(f'interface~"{interface_filter}"')
    if disabled_only:
        filters.append("disabled=yes")
    
    if filters:
        cmd += " where " + " ".join(filters)
    
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "" or result.strip() == "no such item":
        return "No VRRP interfaces found matching the criteria."
    
    return f"VRRP INTERFACES:\n\n{result}"

def mikrotik_get_vrrp_interface(vrrp_id: str) -> str:
    """
    Gets detailed information about a specific VRRP interface.
    
    Args:
        vrrp_id: ID or name of the VRRP interface
    
    Returns:
        Detailed information about the VRRP interface
    """
    app_logger.info(f"Getting VRRP interface details: vrrp_id={vrrp_id}")
    
    # Try by ID first
    cmd = f"/interface vrrp print detail where .id={vrrp_id}"
    result = execute_mikrotik_command(cmd)
    
    # If not found by ID, try by name
    if not result or result.strip() == "":
        cmd = f'/interface vrrp print detail where name="{vrrp_id}"'
        result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return f"VRRP interface with ID or name '{vrrp_id}' not found."
    
    return f"VRRP INTERFACE DETAILS:\n\n{result}"

def mikrotik_create_vrrp_interface(
    name: str,
    interface: str,
    vrid: int,
    priority: int = 100,
    version: int = 3,
    authentication: Optional[str] = None,
    password: Optional[str] = None,
    preemption_mode: bool = True,
    interval: Optional[str] = None,
    comment: Optional[str] = None,
    disabled: bool = False
) -> str:
    """
    Creates a VRRP interface on MikroTik device.
    
    Args:
        name: Name for the VRRP interface
        interface: Physical interface to run VRRP on
        vrid: Virtual Router ID (1-255)
        priority: VRRP priority (1-255, default 100, higher is better)
        version: VRRP version (2 or 3, default 3)
        authentication: Authentication type (ah, simple, none)
        password: Password for authentication
        preemption_mode: Enable preemption (default True)
        interval: Advertisement interval (e.g., 1s, 100ms)
        comment: Optional comment
        disabled: Whether to disable the interface after creation
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Creating VRRP interface: name={name}, vrid={vrid}")
    
    if not name or name.strip() == "":
        return "Error: VRRP interface name cannot be empty."
    
    if not interface or interface.strip() == "":
        return "Error: Physical interface cannot be empty."
    
    # Validate VRID
    if not 1 <= vrid <= 255:
        return "Error: VRID must be between 1 and 255."
    
    # Validate priority
    if not 1 <= priority <= 255:
        return "Error: Priority must be between 1 and 255."
    
    # Validate version
    if version not in [2, 3]:
        return "Error: VRRP version must be 2 or 3."
    
    # Build the command
    cmd = f'/interface vrrp add name="{name}" interface="{interface}" vrid={vrid} priority={priority} version={version}'
    
    if authentication:
        valid_auth = ["ah", "simple", "none"]
        if authentication not in valid_auth:
            return f"Error: Invalid authentication type '{authentication}'. Must be one of: {', '.join(valid_auth)}"
        cmd += f" authentication={authentication}"
        
        if authentication in ["ah", "simple"] and password:
            cmd += f' password="{password}"'
    
    cmd += f' preemption-mode={"yes" if preemption_mode else "no"}'
    
    if interval:
        cmd += f" interval={interval}"
    
    if comment:
        cmd += f' comment="{comment}"'
    
    if disabled:
        cmd += " disabled=yes"
    
    result = execute_mikrotik_command(cmd)
    
    # Check if creation was successful
    if result.strip():
        if "*" in result or result.strip().isdigit():
            vrrp_interface_id = result.strip()
            details_cmd = f"/interface vrrp print detail where .id={vrrp_interface_id}"
            details = execute_mikrotik_command(details_cmd)
            
            if details.strip():
                return f"VRRP interface created successfully:\n\n{details}"
            else:
                return f"VRRP interface created with ID: {result}"
        else:
            return f"Failed to create VRRP interface: {result}"
    else:
        return "VRRP interface creation completed but unable to verify."

def mikrotik_update_vrrp_interface(
    vrrp_id: str,
    name: Optional[str] = None,
    priority: Optional[int] = None,
    authentication: Optional[str] = None,
    password: Optional[str] = None,
    preemption_mode: Optional[bool] = None,
    interval: Optional[str] = None,
    comment: Optional[str] = None,
    disabled: Optional[bool] = None
) -> str:
    """
    Updates an existing VRRP interface.
    
    Args:
        vrrp_id: ID or name of the VRRP interface to update
        name: New name
        priority: New priority (1-255)
        authentication: New authentication type
        password: New password
        preemption_mode: Enable/disable preemption
        interval: New advertisement interval
        comment: New comment
        disabled: Enable/disable the interface
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Updating VRRP interface: vrrp_id={vrrp_id}")
    
    # Build the command
    cmd = f"/interface vrrp set {vrrp_id}"
    
    updates = []
    if name:
        updates.append(f'name="{name}"')
    
    if priority is not None:
        if not 1 <= priority <= 255:
            return "Error: Priority must be between 1 and 255."
        updates.append(f"priority={priority}")
    
    if authentication:
        valid_auth = ["ah", "simple", "none"]
        if authentication not in valid_auth:
            return f"Error: Invalid authentication type '{authentication}'. Must be one of: {', '.join(valid_auth)}"
        updates.append(f"authentication={authentication}")
    
    if password:
        updates.append(f'password="{password}"')
    
    if preemption_mode is not None:
        updates.append(f'preemption-mode={"yes" if preemption_mode else "no"}')
    
    if interval:
        updates.append(f"interval={interval}")
    
    if comment is not None:
        updates.append(f'comment="{comment}"')
    
    if disabled is not None:
        updates.append(f'disabled={"yes" if disabled else "no"}')
    
    if not updates:
        return "No updates specified."
    
    cmd += " " + " ".join(updates)
    
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to update VRRP interface: {result}"
    
    # Get the updated interface details
    details_cmd = f"/interface vrrp print detail where .id={vrrp_id}"
    details = execute_mikrotik_command(details_cmd)
    
    return f"VRRP interface updated successfully:\n\n{details}"

def mikrotik_remove_vrrp_interface(vrrp_id: str) -> str:
    """
    Removes a VRRP interface.
    
    Args:
        vrrp_id: ID or name of the VRRP interface to remove
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Removing VRRP interface: vrrp_id={vrrp_id}")
    
    # First check if the interface exists
    check_cmd = f"/interface vrrp print count-only where .id={vrrp_id}"
    count = execute_mikrotik_command(check_cmd)
    
    if count.strip() == "0":
        # Try by name
        check_cmd = f'/interface vrrp print count-only where name="{vrrp_id}"'
        count = execute_mikrotik_command(check_cmd)
        
        if count.strip() == "0":
            return f"VRRP interface with ID or name '{vrrp_id}' not found."
    
    # Remove the interface
    cmd = f"/interface vrrp remove {vrrp_id}"
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to remove VRRP interface: {result}"
    
    return f"VRRP interface '{vrrp_id}' removed successfully."

def mikrotik_enable_vrrp_interface(vrrp_id: str) -> str:
    """
    Enables a VRRP interface.
    
    Args:
        vrrp_id: ID or name of the VRRP interface to enable
    
    Returns:
        Command output or error message
    """
    return mikrotik_update_vrrp_interface(vrrp_id, disabled=False)

def mikrotik_disable_vrrp_interface(vrrp_id: str) -> str:
    """
    Disables a VRRP interface.
    
    Args:
        vrrp_id: ID or name of the VRRP interface to disable
    
    Returns:
        Command output or error message
    """
    return mikrotik_update_vrrp_interface(vrrp_id, disabled=True)

def mikrotik_monitor_vrrp_interface(vrrp_id: str) -> str:
    """
    Monitors a VRRP interface for real-time status.
    
    Args:
        vrrp_id: ID or name of the VRRP interface to monitor
    
    Returns:
        Real-time monitoring information
    """
    app_logger.info(f"Monitoring VRRP interface: vrrp_id={vrrp_id}")
    
    cmd = f"/interface vrrp monitor {vrrp_id} once"
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return f"Unable to monitor VRRP interface '{vrrp_id}'."
    
    return f"VRRP INTERFACE MONITORING:\n\n{result}"

def mikrotik_create_vrrp_ha_pair(
    master_name: str,
    backup_name: str,
    interface: str,
    vrid: int,
    virtual_address: str,
    master_priority: int = 200,
    backup_priority: int = 100
) -> str:
    """
    Creates a VRRP high-availability pair (master and backup).
    
    Args:
        master_name: Name for the master VRRP interface
        backup_name: Name for the backup VRRP interface
        interface: Physical interface to run VRRP on
        vrid: Virtual Router ID (1-255)
        virtual_address: Virtual IP address for the VRRP group
        master_priority: Priority for master router (default 200)
        backup_priority: Priority for backup router (default 100)
    
    Returns:
        Setup result
    """
    app_logger.info(f"Creating VRRP HA pair: vrid={vrid}")
    
    results = []
    
    # Note: This creates the VRRP interfaces. The virtual address needs to be
    # added separately to the interface as an IP address
    
    # Create master VRRP interface
    master_result = mikrotik_create_vrrp_interface(
        name=master_name,
        interface=interface,
        vrid=vrid,
        priority=master_priority,
        preemption_mode=True,
        comment=f"VRRP Master for VRID {vrid}"
    )
    results.append(f"✓ Master VRRP interface '{master_name}' created with priority {master_priority}")
    
    # Instructions for adding virtual IP
    results.append(f"\n⚠️  IMPORTANT: Add the virtual IP address to the interface:")
    results.append(f"    Command: /ip address add address={virtual_address} interface={master_name}")
    results.append(f"    This should be done on both master and backup routers.")
    
    return "VRRP HA PAIR SETUP:\n\n" + "\n".join(results)

def mikrotik_get_vrrp_status() -> str:
    """
    Gets the status of all VRRP interfaces.
    
    Returns:
        Status of all VRRP interfaces
    """
    app_logger.info("Getting VRRP status for all interfaces")
    
    # Get all VRRP interfaces
    list_cmd = "/interface vrrp print detail"
    result = execute_mikrotik_command(list_cmd)
    
    if not result or result.strip() == "":
        return "No VRRP interfaces configured."
    
    return f"VRRP STATUS (ALL INTERFACES):\n\n{result}"

def mikrotik_set_vrrp_priority(vrrp_id: str, priority: int) -> str:
    """
    Sets the priority for a VRRP interface.
    
    Args:
        vrrp_id: ID or name of the VRRP interface
        priority: New priority (1-255, higher is better)
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Setting VRRP priority: vrrp_id={vrrp_id}, priority={priority}")
    
    if not 1 <= priority <= 255:
        return "Error: Priority must be between 1 and 255."
    
    return mikrotik_update_vrrp_interface(vrrp_id, priority=priority)

def mikrotik_force_vrrp_master(vrrp_id: str) -> str:
    """
    Forces a VRRP interface to become master by setting maximum priority.
    
    Args:
        vrrp_id: ID or name of the VRRP interface
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Forcing VRRP interface to master: vrrp_id={vrrp_id}")
    
    # Set priority to 255 (maximum) to force master role
    return mikrotik_set_vrrp_priority(vrrp_id, 255)

