from typing import List, Optional, Dict, Any

from ..connector import execute_mikrotik_command
from ..logger import app_logger


# ============================================================================
# CAPSMAN MANAGER
# ============================================================================

def mikrotik_enable_capsman() -> str:
    """
    Enables CAPsMAN (Controlled Access Point System Manager).
    
    Returns:
        Command output or error message
    """
    app_logger.info("Enabling CAPsMAN")
    
    cmd = "/caps-man manager set enabled=yes"
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to enable CAPsMAN: {result}"
    
    return "CAPsMAN enabled successfully."


def mikrotik_disable_capsman() -> str:
    """
    Disables CAPsMAN.
    
    Returns:
        Command output or error message
    """
    app_logger.info("Disabling CAPsMAN")
    
    cmd = "/caps-man manager set enabled=no"
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to disable CAPsMAN: {result}"
    
    return "CAPsMAN disabled successfully."


def mikrotik_get_capsman_status() -> str:
    """
    Gets CAPsMAN manager status.
    
    Returns:
        CAPsMAN status information
    """
    app_logger.info("Getting CAPsMAN status")
    
    cmd = "/caps-man manager print"
    result = execute_mikrotik_command(cmd)
    
    return f"CAPSMAN MANAGER STATUS:\n\n{result}"


# ============================================================================
# CAPSMAN INTERFACES (CONTROLLED APs)
# ============================================================================

def mikrotik_list_capsman_interfaces() -> str:
    """
    Lists all CAPsMAN controlled wireless interfaces.
    
    Returns:
        List of CAPsMAN interfaces
    """
    app_logger.info("Listing CAPsMAN interfaces")
    
    cmd = "/caps-man interface print"
    result = execute_mikrotik_command(cmd)
    
    return f"CAPSMAN INTERFACES:\n\n{result}"


def mikrotik_get_capsman_interface(name: str) -> str:
    """
    Gets detailed information about a CAPsMAN interface.
    
    Args:
        name: Interface name
    
    Returns:
        Interface details
    """
    app_logger.info(f"Getting CAPsMAN interface: {name}")
    
    cmd = f'/caps-man interface print detail where name="{name}"'
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return f"CAPsMAN interface '{name}' not found."
    
    return f"CAPSMAN INTERFACE DETAILS:\n\n{result}"


# ============================================================================
# CAPSMAN CONFIGURATION
# ============================================================================

def mikrotik_create_capsman_configuration(
        name: str,
        ssid: str,
        country: Optional[str] = None,
        mode: str = "ap",
        **kwargs
) -> str:
    """
    Creates a CAPsMAN configuration profile.
    
    Args:
        name: Configuration profile name
        ssid: Network SSID
        country: Country code (e.g., "united states")
        mode: Operating mode (ap, bridge, station)
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Creating CAPsMAN configuration: {name}")
    
    cmd = f'/caps-man configuration add name={name} ssid="{ssid}" mode={mode}'
    
    if country:
        cmd += f' country="{country}"'
    
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to create CAPsMAN configuration: {result}"
    
    return f"CAPsMAN configuration '{name}' created successfully."


def mikrotik_list_capsman_configurations() -> str:
    """
    Lists all CAPsMAN configuration profiles.
    
    Returns:
        List of configurations
    """
    app_logger.info("Listing CAPsMAN configurations")
    
    cmd = "/caps-man configuration print"
    result = execute_mikrotik_command(cmd)
    
    return f"CAPSMAN CONFIGURATIONS:\n\n{result}"


def mikrotik_remove_capsman_configuration(name: str) -> str:
    """
    Removes a CAPsMAN configuration profile.
    
    Args:
        name: Configuration profile name
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Removing CAPsMAN configuration: {name}")
    
    cmd = f'/caps-man configuration remove [find name="{name}"]'
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to remove CAPsMAN configuration: {result}"
    
    return f"CAPsMAN configuration '{name}' removed successfully."


# ============================================================================
# CAPSMAN PROVISIONING
# ============================================================================

def mikrotik_create_capsman_provisioning_rule(
        name: str,
        action: str = "create-enabled",
        master_configuration: Optional[str] = None,
        **kwargs
) -> str:
    """
    Creates a CAPsMAN provisioning rule.
    
    Args:
        name: Rule name
        action: Provisioning action (create-enabled, create-disabled)
        master_configuration: Configuration profile to apply
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Creating CAPsMAN provisioning rule: {name}")
    
    cmd = f"/caps-man provisioning add name={name} action={action}"
    
    if master_configuration:
        cmd += f" master-configuration={master_configuration}"
    
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to create provisioning rule: {result}"
    
    return f"CAPsMAN provisioning rule '{name}' created successfully."


def mikrotik_list_capsman_provisioning_rules() -> str:
    """
    Lists all CAPsMAN provisioning rules.
    
    Returns:
        List of provisioning rules
    """
    app_logger.info("Listing CAPsMAN provisioning rules")
    
    cmd = "/caps-man provisioning print"
    result = execute_mikrotik_command(cmd)
    
    return f"CAPSMAN PROVISIONING RULES:\n\n{result}"


def mikrotik_remove_capsman_provisioning_rule(name: str) -> str:
    """
    Removes a CAPsMAN provisioning rule.
    
    Args:
        name: Rule name
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Removing CAPsMAN provisioning rule: {name}")
    
    cmd = f'/caps-man provisioning remove [find name="{name}"]'
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to remove provisioning rule: {result}"
    
    return f"CAPsMAN provisioning rule '{name}' removed successfully."


# ============================================================================
# CAPSMAN REGISTRATION
# ============================================================================

def mikrotik_list_capsman_registration_table() -> str:
    """
    Lists all registered CAPsMAN clients.
    
    Returns:
        List of registered clients
    """
    app_logger.info("Listing CAPsMAN registration table")
    
    cmd = "/caps-man registration-table print"
    result = execute_mikrotik_command(cmd)
    
    return f"CAPSMAN REGISTRATION TABLE:\n\n{result}"


def mikrotik_list_capsman_remote_caps() -> str:
    """
    Lists all remote CAPs (Access Points) connected to this CAPsMAN.
    
    Returns:
        List of remote CAPs
    """
    app_logger.info("Listing CAPsMAN remote CAPs")
    
    cmd = "/caps-man remote-cap print"
    result = execute_mikrotik_command(cmd)
    
    return f"CAPSMAN REMOTE CAPS:\n\n{result}"


def mikrotik_get_capsman_remote_cap(identity: str) -> str:
    """
    Gets detailed information about a specific remote CAP.
    
    Args:
        identity: Remote CAP identity/name
    
    Returns:
        Remote CAP details
    """
    app_logger.info(f"Getting CAPsMAN remote CAP: {identity}")
    
    cmd = f'/caps-man remote-cap print detail where identity="{identity}"'
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return f"Remote CAP '{identity}' not found."
    
    return f"CAPSMAN REMOTE CAP DETAILS:\n\n{result}"


# ============================================================================
# CAPSMAN DATAPATH
# ============================================================================

def mikrotik_create_capsman_datapath(
        name: str,
        bridge: Optional[str] = None,
        vlan_mode: Optional[str] = None,
        **kwargs
) -> str:
    """
    Creates a CAPsMAN datapath configuration.
    
    Args:
        name: Datapath name
        bridge: Bridge interface to use
        vlan_mode: VLAN mode (no-tag, use-tag)
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Creating CAPsMAN datapath: {name}")
    
    cmd = f"/caps-man datapath add name={name}"
    
    if bridge:
        cmd += f" bridge={bridge}"
    if vlan_mode:
        cmd += f" vlan-mode={vlan_mode}"
    
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to create CAPsMAN datapath: {result}"
    
    return f"CAPsMAN datapath '{name}' created successfully."


def mikrotik_list_capsman_datapaths() -> str:
    """
    Lists all CAPsMAN datapath configurations.
    
    Returns:
        List of datapaths
    """
    app_logger.info("Listing CAPsMAN datapaths")
    
    cmd = "/caps-man datapath print"
    result = execute_mikrotik_command(cmd)
    
    return f"CAPSMAN DATAPATHS:\n\n{result}"


def mikrotik_remove_capsman_datapath(name: str) -> str:
    """
    Removes a CAPsMAN datapath configuration.
    
    Args:
        name: Datapath name
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Removing CAPsMAN datapath: {name}")
    
    cmd = f'/caps-man datapath remove [find name="{name}"]'
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to remove CAPsMAN datapath: {result}"
    
    return f"CAPsMAN datapath '{name}' removed successfully."

