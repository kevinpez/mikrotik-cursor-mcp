from typing import List, Optional, Dict, Any

from ..connector import execute_mikrotik_command
from ..logger import app_logger


def mikrotik_detect_wireless_interface_type() -> Optional[str]:
    """
    Detects the wireless interface type based on RouterOS version.

    Returns:
        The appropriate wireless interface command path or None if not supported
    """
    app_logger.info("Detecting wireless interface type")

    # Try different wireless interface types in order of preference
    interface_types = [
        "/interface wifi",  # RouterOS v7.x (newest)
        "/interface wifiwave2",  # RouterOS v7.x (alternative)
        "/interface wireless",  # RouterOS v6.x
        "/interface wlan"  # Older versions
    ]

    for interface_type in interface_types:
        try:
            app_logger.debug(f"Testing interface type: {interface_type}")

            # Use a simpler test command that's less likely to hang
            test_cmd = f"{interface_type} print count-only"
            result = execute_mikrotik_command(test_cmd)

            app_logger.debug(f"Result for {interface_type}: {result}")

            # Check for specific error patterns
            if result and isinstance(result, str):
                result_lower = result.lower()
                if ("bad command name" in result_lower or
                        "failure:" in result_lower or
                        "no such command prefix" in result_lower or
                        "invalid command name" in result_lower):
                    app_logger.debug(f"Interface type {interface_type} not supported")
                    continue
                else:
                    # If we get a numeric result or no error, this type is supported
                    app_logger.info(f"Detected wireless interface type: {interface_type}")
                    return interface_type

        except Exception as e:
            app_logger.debug(f"Interface type {interface_type} failed with exception: {e}")
            continue

    # If none work, return None
    app_logger.warning("No wireless interface type detected")
    return None


def mikrotik_create_wireless_interface(
        name: str,
        ssid: Optional[str] = None,
        disabled: bool = False,
        comment: Optional[str] = None,
        **kwargs  # This captures any additional parameters like radio_name, mode, etc.
) -> str:
    """
    Creates a wireless interface on MikroTik device.

    Args:
        name: Name of the wireless interface
        ssid: Network SSID name
        disabled: Whether to disable the interface
        comment: Optional comment
        **kwargs: Additional parameters (radio_name, mode, etc.) for legacy compatibility

    Returns:
        Command output or error message
    """
    app_logger.info(f"Creating wireless interface: name={name}, ssid={ssid}")

    # Detect wireless interface type
    interface_type = mikrotik_detect_wireless_interface_type()

    if not interface_type:
        return "Error: No wireless interface support detected on this device."

    # Build the command based on interface type
    if interface_type == "/interface wifi":
        # RouterOS v7.x newest wifi syntax - simplified
        cmd = f"{interface_type} add name={name}"

        if ssid:
            cmd += f' ssid="{ssid}"'
        if disabled:
            cmd += " disabled=yes"
        if comment:
            cmd += f' comment="{comment}"'

    elif interface_type == "/interface wifiwave2":
        # RouterOS v7.x wifiwave2 syntax
        cmd = f"{interface_type} add name={name}"

        if ssid:
            cmd += f' ssid="{ssid}"'
        if disabled:
            cmd += " disabled=yes"
        if comment:
            cmd += f' comment="{comment}"'

    else:
        # Legacy wireless syntax (RouterOS v6.x and older)
        radio_name = kwargs.get('radio_name')
        mode = kwargs.get('mode', 'ap-bridge')

        if not radio_name:
            return "Error: radio_name is required for legacy wireless systems. Please specify the radio interface (e.g., 'wlan1')."

        cmd = f"{interface_type} add name={name} radio-name={radio_name} mode={mode}"

        if ssid:
            cmd += f' ssid="{ssid}"'
        if disabled:
            cmd += " disabled=yes"
        if comment:
            cmd += f' comment="{comment}"'

        # Add other legacy parameters if provided
        for param in ['frequency', 'band', 'channel_width', 'security_profile']:
            if param in kwargs and kwargs[param]:
                cmd += f" {param.replace('_', '-')}={kwargs[param]}"

    app_logger.info(f"Executing command: {cmd}")
    result = execute_mikrotik_command(cmd)

    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to create wireless interface: {result}"

    # Get the created interface details
    details_cmd = f'{interface_type} print detail where name="{name}"'
    details = execute_mikrotik_command(details_cmd)

    return f"Wireless interface created successfully using {interface_type}:\n\n{details}"


def mikrotik_list_wireless_interfaces(
        name_filter: Optional[str] = None,
        disabled_only: bool = False,
        running_only: bool = False
) -> str:
    """
    Lists wireless interfaces on MikroTik device.

    Args:
        name_filter: Filter by interface name
        disabled_only: Show only disabled interfaces
        running_only: Show only running interfaces

    Returns:
        List of wireless interfaces
    """
    app_logger.info(f"Listing wireless interfaces with filters: name={name_filter}")

    # Try multiple interface types to ensure we find all wireless interfaces
    interface_types_to_try = [
        "/interface wifi",
        "/interface wifiwave2",
        "/interface wireless",
        "/interface wlan"
    ]

    all_results = []
    working_types = []

    for interface_type in interface_types_to_try:
        try:
            # Build the command
            cmd = f"{interface_type} print"

            # Add filters
            filters = []
            if name_filter:
                filters.append(f'name~"{name_filter}"')
            if disabled_only:
                filters.append("disabled=yes")
            if running_only:
                filters.append("running=yes")

            if filters:
                cmd += " where " + " and ".join(filters)

            result = execute_mikrotik_command(cmd)

            # Check if command worked and has results
            if (result and
                    result.strip() != "" and
                    "bad command name" not in result.lower() and
                    "failure:" not in result.lower() and
                    "no such command prefix" not in result.lower()):
                working_types.append(interface_type)
                all_results.append(f"=== {interface_type.upper()} ===\n{result}")

        except Exception as e:
            app_logger.debug(f"Interface type {interface_type} failed: {e}")
            continue

    # If we found results, return them
    if all_results:
        return f"WIRELESS INTERFACES:\n\n" + "\n\n".join(all_results)

    # If no results found, try to show all interfaces to help debug
    try:
        all_interfaces_cmd = "/interface print"
        all_interfaces = execute_mikrotik_command(all_interfaces_cmd)
        return f"""No wireless interfaces found matching the criteria.

DEBUGGING INFO:
Working interface types: {', '.join(working_types) if working_types else 'None detected'}

ALL INTERFACES ON DEVICE:
{all_interfaces}

NOTE: If you see wireless interfaces above, they might be using a different command structure."""

    except Exception:
        return "No wireless interfaces found matching the criteria."


def mikrotik_get_wireless_interface(name: str) -> str:
    """
    Gets detailed information about a specific wireless interface.

    Args:
        name: Name of the wireless interface

    Returns:
        Detailed information about the wireless interface
    """
    app_logger.info(f"Getting wireless interface details: name={name}")

    # Detect wireless interface type
    interface_type = mikrotik_detect_wireless_interface_type()

    if not interface_type:
        return "Error: No wireless interface support detected on this device."

    cmd = f'{interface_type} print detail where name="{name}"'
    result = execute_mikrotik_command(cmd)

    if not result or result.strip() == "":
        return f"Wireless interface '{name}' not found."

    return f"WIRELESS INTERFACE DETAILS:\n\n{result}"


def mikrotik_remove_wireless_interface(name: str) -> str:
    """
    Removes a wireless interface from MikroTik device.

    Args:
        name: Name of the wireless interface to remove

    Returns:
        Command output or error message
    """
    app_logger.info(f"Removing wireless interface: name={name}")

    # Detect wireless interface type
    interface_type = mikrotik_detect_wireless_interface_type()

    if not interface_type:
        return "Error: No wireless interface support detected on this device."

    # Check if interface exists
    check_cmd = f'{interface_type} print count-only where name="{name}"'
    count = execute_mikrotik_command(check_cmd)

    if count.strip() == "0":
        return f"Wireless interface '{name}' not found."

    # Remove the interface
    cmd = f'{interface_type} remove [find name="{name}"]'
    result = execute_mikrotik_command(cmd)

    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to remove wireless interface: {result}"

    return f"Wireless interface '{name}' removed successfully."


def mikrotik_enable_wireless_interface(name: str) -> str:
    """
    Enables a wireless interface.

    Args:
        name: Name of the wireless interface

    Returns:
        Command output or error message
    """
    app_logger.info(f"Enabling wireless interface: {name}")

    # Detect wireless interface type
    interface_type = mikrotik_detect_wireless_interface_type()

    if not interface_type:
        return "Error: No wireless interface support detected on this device."

    cmd = f'{interface_type} enable [find name="{name}"]'
    result = execute_mikrotik_command(cmd)

    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to enable wireless interface: {result}"

    return f"Wireless interface '{name}' enabled successfully."


def mikrotik_disable_wireless_interface(name: str) -> str:
    """
    Disables a wireless interface.

    Args:
        name: Name of the wireless interface

    Returns:
        Command output or error message
    """
    app_logger.info(f"Disabling wireless interface: {name}")

    # Detect wireless interface type
    interface_type = mikrotik_detect_wireless_interface_type()

    if not interface_type:
        return "Error: No wireless interface support detected on this device."

    cmd = f'{interface_type} disable [find name="{name}"]'
    result = execute_mikrotik_command(cmd)

    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to disable wireless interface: {result}"

    return f"Wireless interface '{name}' disabled successfully."


def mikrotik_scan_wireless_networks(
        interface: str,
        duration: int = 5
) -> str:
    """
    Scans for wireless networks using specified interface.

    Args:
        interface: Wireless interface to use for scanning
        duration: Scan duration in seconds

    Returns:
        List of discovered wireless networks
    """
    app_logger.info(f"Scanning wireless networks on interface: {interface}")

    # Detect wireless interface type
    interface_type = mikrotik_detect_wireless_interface_type()

    if not interface_type:
        return "Error: No wireless interface support detected on this device."

    # Different scan commands for different versions
    scan_cmd = f'{interface_type} scan {interface} duration={duration}'

    result = execute_mikrotik_command(scan_cmd)

    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to scan wireless networks: {result}"

    return f"WIRELESS NETWORK SCAN RESULTS:\n\n{result}"


def mikrotik_get_wireless_registration_table(
        interface: Optional[str] = None
) -> str:
    """
    Gets the wireless registration table (connected clients).

    Args:
        interface: Filter by specific wireless interface

    Returns:
        List of registered wireless clients
    """
    app_logger.info(f"Getting wireless registration table for interface: {interface}")

    # Detect wireless interface type
    interface_type = mikrotik_detect_wireless_interface_type()

    if not interface_type:
        return "Error: No wireless interface support detected on this device."

    # Build command
    cmd = f"{interface_type} registration-table print"

    if interface:
        cmd += f' where interface="{interface}"'

    result = execute_mikrotik_command(cmd)

    if not result or result.strip() == "":
        return "No wireless clients registered."

    return f"WIRELESS REGISTRATION TABLE:\n\n{result}"


def mikrotik_check_wireless_support() -> str:
    """
    Checks if the device supports wireless functionality and returns detailed information.

    Returns:
        Information about wireless support and available packages
    """
    app_logger.info("Checking wireless support")

    # Check RouterOS version
    version_cmd = "/system resource print"
    version_result = execute_mikrotik_command(version_cmd)

    # Check installed packages
    package_cmd = "/system package print"
    package_result = execute_mikrotik_command(package_cmd)

    # Check available interfaces
    interface_cmd = "/interface print"
    interface_result = execute_mikrotik_command(interface_cmd)

    # Detect wireless interface type
    wireless_type = mikrotik_detect_wireless_interface_type()

    report = f"""WIRELESS SUPPORT CHECK:

RouterOS Version:
{version_result}

Installed Packages:
{package_result}

Available Interfaces:
{interface_result}

Detected Wireless Interface Type: {wireless_type if wireless_type else 'None detected'}

Compatibility Notes:
- RouterOS v7.x uses '/interface wifi' (newest system)
- RouterOS v7.x also supports '/interface wifiwave2' (alternative)
- RouterOS v6.x uses '/interface wireless' (legacy system)  
- Older versions may use '/interface wlan'

USAGE EXAMPLES:
For RouterOS v7.x:
  mikrotik_create_wireless_interface(name="wlan1", ssid="MyNetwork")

For legacy systems:
  mikrotik_create_wireless_interface(name="wlan1", radio_name="wlan1", ssid="MyNetwork")
"""

    return report


# ============================================================================
# SECURITY PROFILES
# ============================================================================

def mikrotik_create_wireless_security_profile(
        name: str,
        mode: str = "dynamic-keys",
        authentication_types: Optional[str] = None,
        wpa_pre_shared_key: Optional[str] = None,
        wpa2_pre_shared_key: Optional[str] = None,
        **kwargs
) -> str:
    """
    Creates a wireless security profile (RouterOS v6.x only).
    
    Args:
        name: Security profile name
        mode: Security mode (static-keys-required, dynamic-keys, static-keys-optional)
        authentication_types: Authentication types (comma-separated: wpa-psk, wpa2-psk, wpa-eap, wpa2-eap)
        wpa_pre_shared_key: WPA pre-shared key
        wpa2_pre_shared_key: WPA2 pre-shared key
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Creating wireless security profile: {name}")
    
    interface_type = mikrotik_detect_wireless_interface_type()
    if interface_type in ["/interface wifi", "/interface wifiwave2"]:
        return "Security profiles are not used in RouterOS v7.x. Configure security directly on the wireless interface."
    
    # Build command for v6.x
    cmd = f"/interface wireless security-profiles add name={name} mode={mode}"
    
    if authentication_types:
        cmd += f" authentication-types={authentication_types}"
    if wpa_pre_shared_key:
        cmd += f' wpa-pre-shared-key="{wpa_pre_shared_key}"'
    if wpa2_pre_shared_key:
        cmd += f' wpa2-pre-shared-key="{wpa2_pre_shared_key}"'
    
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to create security profile: {result}"
    
    return f"Security profile '{name}' created successfully."


def mikrotik_list_wireless_security_profiles() -> str:
    """
    Lists all wireless security profiles (RouterOS v6.x only).
    
    Returns:
        List of security profiles
    """
    app_logger.info("Listing wireless security profiles")
    
    interface_type = mikrotik_detect_wireless_interface_type()
    if interface_type in ["/interface wifi", "/interface wifiwave2"]:
        return "Security profiles are not used in RouterOS v7.x. Security is configured directly on wireless interfaces."
    
    cmd = "/interface wireless security-profiles print"
    result = execute_mikrotik_command(cmd)
    
    return f"WIRELESS SECURITY PROFILES:\n\n{result}"


def mikrotik_get_wireless_security_profile(name: str) -> str:
    """
    Gets detailed information about a security profile (RouterOS v6.x only).
    
    Args:
        name: Security profile name
    
    Returns:
        Security profile details
    """
    app_logger.info(f"Getting security profile: {name}")
    
    interface_type = mikrotik_detect_wireless_interface_type()
    if interface_type in ["/interface wifi", "/interface wifiwave2"]:
        return "Security profiles are not used in RouterOS v7.x. Check security configuration on wireless interfaces directly."
    
    cmd = f'/interface wireless security-profiles print detail where name="{name}"'
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return f"Security profile '{name}' not found."
    
    return f"SECURITY PROFILE DETAILS:\n\n{result}"


def mikrotik_remove_wireless_security_profile(name: str) -> str:
    """
    Removes a wireless security profile (RouterOS v6.x only).
    
    Args:
        name: Security profile name
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Removing security profile: {name}")
    
    interface_type = mikrotik_detect_wireless_interface_type()
    if interface_type in ["/interface wifi", "/interface wifiwave2"]:
        return "Security profiles are not used in RouterOS v7.x. Security is configured directly on wireless interfaces."
    
    cmd = f'/interface wireless security-profiles remove [find name="{name}"]'
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to remove security profile: {result}"
    
    return f"Security profile '{name}' removed successfully."


def mikrotik_update_wireless_security_profile(name: str, **kwargs) -> str:
    """
    Updates a wireless security profile (RouterOS v6.x only).
    
    Args:
        name: Security profile name
        **kwargs: Parameters to update
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Updating security profile: {name}")
    
    interface_type = mikrotik_detect_wireless_interface_type()
    if interface_type in ["/interface wifi", "/interface wifiwave2"]:
        return "Security profiles are not used in RouterOS v7.x."
    
    updates = []
    
    for key in ['mode', 'authentication_types', 'wpa_pre_shared_key', 'wpa2_pre_shared_key']:
        if key in kwargs and kwargs[key]:
            param_name = key.replace('_', '-')
            value = kwargs[key]
            if 'key' in key:
                updates.append(f'{param_name}="{value}"')
            else:
                updates.append(f"{param_name}={value}")
    
    if not updates:
        return "No updates specified."
    
    cmd = f'/interface wireless security-profiles set [find name="{name}"] {" ".join(updates)}'
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to update security profile: {result}"
    
    return f"Security profile '{name}' updated successfully."


# ============================================================================
# ACCESS LISTS
# ============================================================================

def mikrotik_create_wireless_access_list(
        interface: str,
        mac_address: str,
        signal_range: Optional[str] = None,
        authentication: bool = True,
        forwarding: bool = True,
        **kwargs
) -> str:
    """
    Creates a wireless access list entry (RouterOS v6.x only).
    
    Args:
        interface: Wireless interface name
        mac_address: MAC address to allow/deny
        signal_range: Signal range (e.g., "-120..120")
        authentication: Allow authentication
        forwarding: Allow forwarding
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Creating access list entry for MAC: {mac_address}")
    
    interface_type = mikrotik_detect_wireless_interface_type()
    if interface_type in ["/interface wifi", "/interface wifiwave2"]:
        return "Access lists are configured differently in RouterOS v7.x. Use firewall rules or WiFi access lists."
    
    cmd = f'/interface wireless access-list add interface={interface} mac-address={mac_address}'
    cmd += f' authentication={"yes" if authentication else "no"}'
    cmd += f' forwarding={"yes" if forwarding else "no"}'
    
    if signal_range:
        cmd += f' signal-range={signal_range}'
    
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to create access list entry: {result}"
    
    return f"Access list entry created for MAC '{mac_address}' on interface '{interface}'."


def mikrotik_list_wireless_access_list(interface: Optional[str] = None) -> str:
    """
    Lists wireless access list entries (RouterOS v6.x only).
    
    Args:
        interface: Filter by interface name
    
    Returns:
        List of access list entries
    """
    app_logger.info("Listing wireless access list")
    
    interface_type = mikrotik_detect_wireless_interface_type()
    if interface_type in ["/interface wifi", "/interface wifiwave2"]:
        return "Access lists are configured differently in RouterOS v7.x. Check firewall rules or WiFi access lists."
    
    cmd = "/interface wireless access-list print"
    
    if interface:
        cmd += f' where interface="{interface}"'
    
    result = execute_mikrotik_command(cmd)
    
    return f"WIRELESS ACCESS LIST:\n\n{result}"


def mikrotik_remove_wireless_access_list_entry(entry_id: str) -> str:
    """
    Removes a wireless access list entry (RouterOS v6.x only).
    
    Args:
        entry_id: Entry ID or MAC address
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Removing access list entry: {entry_id}")
    
    interface_type = mikrotik_detect_wireless_interface_type()
    if interface_type in ["/interface wifi", "/interface wifiwave2"]:
        return "Access lists are configured differently in RouterOS v7.x."
    
    # Try to remove by ID first, then by MAC address
    if entry_id.isdigit():
        cmd = f"/interface wireless access-list remove {entry_id}"
    else:
        cmd = f'/interface wireless access-list remove [find mac-address={entry_id}]'
    
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to remove access list entry: {result}"
    
    return f"Access list entry '{entry_id}' removed successfully."


# ============================================================================
# MONITORING & STATISTICS
# ============================================================================

def mikrotik_get_wireless_interface_monitor(interface: str) -> str:
    """
    Gets real-time monitoring information for a wireless interface.
    
    Args:
        interface: Wireless interface name
    
    Returns:
        Real-time monitoring data
    """
    app_logger.info(f"Getting wireless monitor data for: {interface}")
    
    interface_type = mikrotik_detect_wireless_interface_type()
    
    if not interface_type:
        return "Error: No wireless interface support detected on this device."
    
    cmd = f"{interface_type} monitor {interface} once"
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to get monitor data: {result}"
    
    return f"WIRELESS INTERFACE MONITOR:\n\n{result}"


def mikrotik_get_wireless_frequencies() -> str:
    """
    Gets available wireless frequencies (RouterOS v6.x only).
    
    Returns:
        List of available frequencies
    """
    app_logger.info("Getting wireless frequencies")
    
    interface_type = mikrotik_detect_wireless_interface_type()
    if interface_type in ["/interface wifi", "/interface wifiwave2"]:
        return "Frequency management is different in RouterOS v7.x. Check channel configurations directly on interfaces."
    
    cmd = "/interface wireless frequency print"
    result = execute_mikrotik_command(cmd)
    
    return f"WIRELESS FREQUENCIES:\n\n{result}"


def mikrotik_export_wireless_config() -> str:
    """
    Exports the complete wireless configuration.
    
    Returns:
        Wireless configuration export
    """
    app_logger.info("Exporting wireless configuration")
    
    interface_type = mikrotik_detect_wireless_interface_type()
    
    if not interface_type:
        return "Error: No wireless interface support detected on this device."
    
    cmd = f"{interface_type} export"
    result = execute_mikrotik_command(cmd)
    
    return f"WIRELESS CONFIGURATION EXPORT:\n\n{result}"


def mikrotik_update_wireless_interface(name: str, **kwargs) -> str:
    """
    Updates an existing wireless interface.
    """
    app_logger.info(f"Updating wireless interface: name={name}")

    # Detect wireless interface type
    interface_type = mikrotik_detect_wireless_interface_type()

    if not interface_type:
        return "Error: No wireless interface support detected on this device."

    # Check if interface exists
    check_cmd = f'{interface_type} print count-only where name="{name}"'
    count = execute_mikrotik_command(check_cmd)

    if count.strip() == "0":
        return f"Wireless interface '{name}' not found."

    # Build update command
    updates = []

    if 'new_name' in kwargs and kwargs['new_name']:
        updates.append(f"name={kwargs['new_name']}")
    if 'ssid' in kwargs and kwargs['ssid']:
        updates.append(f'ssid="{kwargs["ssid"]}"')
    if 'disabled' in kwargs and kwargs['disabled'] is not None:
        updates.append(f"disabled={'yes' if kwargs['disabled'] else 'no'}")
    if 'comment' in kwargs and kwargs['comment']:
        updates.append(f'comment="{kwargs["comment"]}"')

    if not updates:
        return "No updates specified."

    cmd = f'{interface_type} set [find name="{name}"] {" ".join(updates)}'
    result = execute_mikrotik_command(cmd)

    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to update wireless interface: {result}"

    # Get updated details
    target_name = kwargs.get('new_name', name)
    details_cmd = f'{interface_type} print detail where name="{target_name}"'
    details = execute_mikrotik_command(details_cmd)

    return f"Wireless interface updated successfully:\n\n{details}"