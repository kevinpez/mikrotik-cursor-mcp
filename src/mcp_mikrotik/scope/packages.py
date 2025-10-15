from typing import Optional
from ..connector import execute_mikrotik_command
from ..logger import app_logger

def mikrotik_list_packages(
    disabled_only: bool = False,
    name_filter: Optional[str] = None
) -> str:
    """
    Lists installed packages on MikroTik device.
    
    Args:
        disabled_only: Show only disabled packages
        name_filter: Filter by package name
    
    Returns:
        List of installed packages
    """
    app_logger.info(f"Listing packages: disabled_only={disabled_only}")
    
    cmd = "/system package print detail"
    
    # Add filters
    filters = []
    if disabled_only:
        filters.append("disabled=yes")
    if name_filter:
        filters.append(f'name~"{name_filter}"')
    
    if filters:
        cmd += " where " + " ".join(filters)
    
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "" or result.strip() == "no such item":
        return "No packages found matching the criteria."
    
    return f"INSTALLED PACKAGES:\n\n{result}"

def mikrotik_get_package(package_name: str) -> str:
    """
    Gets detailed information about a specific package.
    
    Args:
        package_name: Name of the package
    
    Returns:
        Detailed information about the package
    """
    app_logger.info(f"Getting package details: package_name={package_name}")
    
    cmd = f'/system package print detail where name="{package_name}"'
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return f"Package '{package_name}' not found."
    
    return f"PACKAGE DETAILS:\n\n{result}"

def mikrotik_enable_package(package_name: str) -> str:
    """
    Enables a package.
    
    Args:
        package_name: Name of the package to enable
    
    Returns:
        Command output or error message
    
    Note: Router reboot may be required for changes to take effect
    """
    app_logger.info(f"Enabling package: package_name={package_name}")
    
    cmd = f'/system package enable {package_name}'
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to enable package '{package_name}': {result}"
    
    return f"Package '{package_name}' has been enabled. A router reboot may be required for changes to take effect."

def mikrotik_disable_package(package_name: str) -> str:
    """
    Disables a package.
    
    Args:
        package_name: Name of the package to disable
    
    Returns:
        Command output or error message
    
    Note: Router reboot may be required for changes to take effect
    """
    app_logger.info(f"Disabling package: package_name={package_name}")
    
    cmd = f'/system package disable {package_name}'
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to disable package '{package_name}': {result}"
    
    return f"Package '{package_name}' has been disabled. A router reboot may be required for changes to take effect."

def mikrotik_uninstall_package(package_name: str) -> str:
    """
    Uninstalls a package from the device.
    
    Args:
        package_name: Name of the package to uninstall
    
    Returns:
        Command output or error message
    
    Warning: This will remove the package from the system. A reboot is required.
    """
    app_logger.info(f"Uninstalling package: package_name={package_name}")
    
    cmd = f'/system package uninstall {package_name}'
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to uninstall package '{package_name}': {result}"
    
    return f"Package '{package_name}' has been marked for uninstallation. A router reboot is required to complete the process."

def mikrotik_update_packages(channel: Optional[str] = None) -> str:
    """
    Checks for and downloads package updates.
    
    Args:
        channel: Update channel (stable, testing, development)
    
    Returns:
        Command output or error message
    
    Note: This only downloads updates. Use install_updates to apply them.
    """
    app_logger.info(f"Checking for package updates: channel={channel}")
    
    # Set channel if provided
    if channel:
        valid_channels = ["stable", "testing", "development"]
        if channel not in valid_channels:
            return f"Error: Invalid channel '{channel}'. Must be one of: {', '.join(valid_channels)}"
        
        set_channel_cmd = f'/system package update set channel={channel}'
        execute_mikrotik_command(set_channel_cmd)
    
    # Check for updates
    check_cmd = "/system package update check-for-updates"
    result = execute_mikrotik_command(check_cmd)
    
    # Get update status
    status_cmd = "/system package update print"
    status = execute_mikrotik_command(status_cmd)
    
    return f"PACKAGE UPDATE CHECK:\n\n{status}"

def mikrotik_install_updates() -> str:
    """
    Installs downloaded package updates.
    
    Returns:
        Command output or error message
    
    Warning: This will reboot the router to apply updates!
    """
    app_logger.info("Installing package updates")
    
    # Check if updates are available
    status_cmd = "/system package update print"
    status = execute_mikrotik_command(status_cmd)
    
    if "status: System is already up to date" in status:
        return "No updates available. System is already up to date."
    
    # Install updates
    cmd = "/system package update install"
    result = execute_mikrotik_command(cmd)
    
    return f"Package updates are being installed. The router will reboot automatically.\n\nStatus before update:\n{status}"

def mikrotik_download_package(url: str) -> str:
    """
    Downloads a package from a URL to the router.
    
    Args:
        url: URL of the package file (.npk)
    
    Returns:
        Command output or error message
    
    Note: After download, reboot the router to install the package
    """
    app_logger.info(f"Downloading package from: url={url}")
    
    if not url or url.strip() == "":
        return "Error: URL cannot be empty."
    
    if not url.endswith('.npk'):
        return "Error: Package URL must point to a .npk file."
    
    # Extract filename from URL
    filename = url.split('/')[-1]
    
    cmd = f'/tool fetch url="{url}" dst-path={filename}'
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to download package: {result}"
    
    return f"Package '{filename}' has been downloaded. Reboot the router to install it.\n\nDownload result:\n{result}"

def mikrotik_get_package_update_status() -> str:
    """
    Gets the current package update status.
    
    Returns:
        Package update status including channel and available updates
    """
    app_logger.info("Getting package update status")
    
    cmd = "/system package update print detail"
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return "Unable to get package update status."
    
    return f"PACKAGE UPDATE STATUS:\n\n{result}"

def mikrotik_set_update_channel(channel: str) -> str:
    """
    Sets the update channel for package updates.
    
    Args:
        channel: Update channel (stable, testing, development, long-term)
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Setting update channel: channel={channel}")
    
    valid_channels = ["stable", "testing", "development", "long-term"]
    if channel not in valid_channels:
        return f"Error: Invalid channel '{channel}'. Must be one of: {', '.join(valid_channels)}"
    
    cmd = f'/system package update set channel={channel}'
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to set update channel: {result}"
    
    # Get the updated status
    status_cmd = "/system package update print"
    status = execute_mikrotik_command(status_cmd)
    
    return f"Update channel set to '{channel}'.\n\nCurrent status:\n{status}"

def mikrotik_list_available_packages() -> str:
    """
    Lists all available packages that can be installed.
    
    Returns:
        List of available packages
    
    Note: This shows packages available for download from MikroTik servers
    """
    app_logger.info("Listing available packages")
    
    # First, update the available packages list
    check_cmd = "/system package update check-for-updates"
    execute_mikrotik_command(check_cmd)
    
    # Get the list
    cmd = "/system package update print"
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return "Unable to retrieve available packages list."
    
    return f"AVAILABLE PACKAGES:\n\n{result}"

