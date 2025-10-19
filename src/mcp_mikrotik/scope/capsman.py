from typing import List, Optional, Dict, Any

from ..connector import execute_mikrotik_command
from ..api_fallback import api_fallback_execute
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
    
    try:
        # RouterOS v7 uses wifiwave2
        result = api_fallback_execute("/interface/wifiwave2/cap-man/print", {})
        
        if result and "not found" not in result.lower() and result.strip():
            return f"CAPSMAN MANAGER STATUS (v7):\n\n{result}"
        
        # Try older CAPsMAN syntax
        cmd = "/caps-man manager print"
        result = execute_mikrotik_command(cmd)
        
        if result and "syntax error" not in result.lower():
            return f"CAPSMAN MANAGER STATUS:\n\n{result}"
        
        return "CAPsMAN not available on this device/RouterOS version.\n\nNote: RouterOS v7 uses WiFiWave2 instead of legacy CAPsMAN."
        
    except Exception as e:
        return "CAPsMAN not available on this device/RouterOS version.\n\nNote: RouterOS v7 uses WiFiWave2 instead of legacy CAPsMAN."


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
    
    # Try WiFi Wave2/v7 syntax first
    cmd_v7 = "/interface wifiwave2 cap print"
    result = execute_mikrotik_command(cmd_v7)
    
    # If v7 syntax fails, try CAPsMAN (v6)
    if not result or "syntax error" in result.lower() or "bad command" in result.lower():
        cmd_v6 = "/caps-man interface print"
        result = execute_mikrotik_command(cmd_v6)
    
    # If both fail, try cap-man (alternate spelling)
    if not result or "syntax error" in result.lower() or "bad command" in result.lower():
        cmd_alt = "/cap-man interface print"
        result = execute_mikrotik_command(cmd_alt)
    
    if not result or result.strip() == "":
        return "CAPsMAN not configured or not supported on this device."
    
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
    
    try:
        # RouterOS v7 uses wifiwave2 configurations
        result = api_fallback_execute("/interface/wifiwave2/configuration/print", {})
        
        if result and result.strip() and "not found" not in result.lower():
            return f"CAPSMAN CONFIGURATIONS (v7):\n\n{result}"
        
        # Fallback to v6 syntax
        cmd = "/caps-man configuration print"
        result = execute_mikrotik_command(cmd)
        
        if result and result.strip():
            return f"CAPSMAN CONFIGURATIONS:\n\n{result}"
        
        return "No CAPsMAN configurations found. CAPsMAN may not be enabled."
        
    except Exception as e:
        return "CAPsMAN not available on this RouterOS version."


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
    
    try:
        # RouterOS v7 uses wifiwave2 provisioning
        result = api_fallback_execute("/interface/wifiwave2/provisioning/print", {})
        
        if result and result.strip() and "not found" not in result.lower():
            return f"CAPSMAN PROVISIONING RULES (v7):\n\n{result}"
        
        # Fallback to v6 syntax
        cmd = "/caps-man provisioning print"
        result = execute_mikrotik_command(cmd)
        
        if result and result.strip():
            return f"CAPSMAN PROVISIONING RULES:\n\n{result}"
        
        return "No CAPsMAN provisioning rules found."
        
    except Exception as e:
        return "CAPsMAN not available on this RouterOS version."


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
    
    try:
        # RouterOS v7 uses wifiwave2 registration table
        result = api_fallback_execute("/interface/wifiwave2/registration-table/print", {})
        
        if result and result.strip() and "not found" not in result.lower():
            return f"CAPSMAN REGISTRATION TABLE (v7):\n\n{result}"
        
        # Fallback to v6 syntax
        cmd = "/caps-man registration-table print"
        result = execute_mikrotik_command(cmd)
        
        if result and result.strip():
            return f"CAPSMAN REGISTRATION TABLE:\n\n{result}"
        
        return "No CAPsMAN clients registered."
        
    except Exception as e:
        return "CAPsMAN not available on this RouterOS version."


def mikrotik_list_capsman_remote_caps() -> str:
    """
    Lists all remote CAPs (Access Points) connected to this CAPsMAN.
    
    Returns:
        List of remote CAPs
    """
    app_logger.info("Listing CAPsMAN remote CAPs")
    
    try:
        # RouterOS v7 uses wifiwave2 cap
        result = api_fallback_execute("/interface/wifiwave2/cap/print", {})
        
        if result and result.strip() and "not found" not in result.lower():
            return f"CAPSMAN REMOTE CAPS (v7):\n\n{result}"
        
        # Fallback to v6 syntax
        cmd = "/caps-man remote-cap print"
        result = execute_mikrotik_command(cmd)
        
        if result and result.strip():
            return f"CAPSMAN REMOTE CAPS:\n\n{result}"
        
        return "No remote CAPs connected."
        
    except Exception as e:
        return "CAPsMAN not available on this RouterOS version."


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
    
    try:
        # RouterOS v7 uses wifiwave2 datapath
        result = api_fallback_execute("/interface/wifiwave2/datapath/print", {})
        
        if result and result.strip() and "not found" not in result.lower():
            return f"CAPSMAN DATAPATHS (v7):\n\n{result}"
        
        # Fallback to v6 syntax
        cmd = "/caps-man datapath print"
        result = execute_mikrotik_command(cmd)
        
        if result and result.strip():
            return f"CAPSMAN DATAPATHS:\n\n{result}"
        
        return "No CAPsMAN datapaths configured."
        
    except Exception as e:
        return "CAPsMAN not available on this RouterOS version."


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


