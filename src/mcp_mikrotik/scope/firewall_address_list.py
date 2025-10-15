from typing import Optional
from ..connector import execute_mikrotik_command
from ..logger import app_logger

def mikrotik_list_address_lists(
    list_filter: Optional[str] = None,
    address_filter: Optional[str] = None,
    dynamic_only: bool = False,
    disabled_only: bool = False
) -> str:
    """
    Lists firewall address list entries on MikroTik device.
    
    Args:
        list_filter: Filter by list name
        address_filter: Filter by address
        dynamic_only: Show only dynamic entries
        disabled_only: Show only disabled entries
    
    Returns:
        List of address list entries
    """
    app_logger.info(f"Listing address list entries: list={list_filter}")
    
    cmd = "/ip firewall address-list print detail"
    
    # Add filters
    filters = []
    if list_filter:
        filters.append(f'list="{list_filter}"')
    if address_filter:
        filters.append(f'address~"{address_filter}"')
    if dynamic_only:
        filters.append("dynamic=yes")
    if disabled_only:
        filters.append("disabled=yes")
    
    if filters:
        cmd += " where " + " ".join(filters)
    
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "" or result.strip() == "no such item":
        return "No address list entries found matching the criteria."
    
    return f"ADDRESS LIST ENTRIES:\n\n{result}"

def mikrotik_add_address_list_entry(
    list_name: str,
    address: str,
    timeout: Optional[str] = None,
    comment: Optional[str] = None,
    disabled: bool = False
) -> str:
    """
    Adds an entry to a firewall address list.
    
    Args:
        list_name: Name of the address list
        address: IP address or CIDR range
        timeout: Optional timeout (e.g., "1h", "30m", "1d", "1w")
        comment: Optional comment
        disabled: Whether to disable the entry after creation
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Adding address list entry: list={list_name}, address={address}, timeout={timeout}")
    
    if not list_name or list_name.strip() == "":
        return "Error: List name cannot be empty."
    
    if not address or address.strip() == "":
        return "Error: Address cannot be empty."
    
    # Build the command
    cmd = f'/ip firewall address-list add list="{list_name}" address={address}'
    
    if timeout:
        # Validate timeout format
        if not _validate_timeout(timeout):
            return f"Error: Invalid timeout format '{timeout}'. Use format like: 1h, 30m, 1d, 1w"
        cmd += f" timeout={timeout}"
    
    if comment:
        cmd += f' comment="{comment}"'
    
    if disabled:
        cmd += " disabled=yes"
    
    result = execute_mikrotik_command(cmd)
    
    # Check if creation was successful
    if result.strip():
        if "*" in result or result.strip().isdigit():
            # Success
            entry_id = result.strip()
            details_cmd = f"/ip firewall address-list print detail where .id={entry_id}"
            details = execute_mikrotik_command(details_cmd)
            
            if details.strip():
                return f"Address list entry added successfully:\n\n{details}"
            else:
                return f"Address list entry added with ID: {result}"
        else:
            return f"Failed to add address list entry: {result}"
    else:
        return "Address list entry creation completed but unable to verify."

def mikrotik_remove_address_list_entry(entry_id: str) -> str:
    """
    Removes an entry from a firewall address list.
    
    Args:
        entry_id: ID of the address list entry to remove
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Removing address list entry: entry_id={entry_id}")
    
    # First check if the entry exists
    check_cmd = f"/ip firewall address-list print count-only where .id={entry_id}"
    count = execute_mikrotik_command(check_cmd)
    
    if count.strip() == "0":
        return f"Address list entry with ID '{entry_id}' not found."
    
    # Remove the entry
    cmd = f"/ip firewall address-list remove {entry_id}"
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to remove address list entry: {result}"
    
    return f"Address list entry with ID '{entry_id}' removed successfully."

def mikrotik_update_address_list_entry(
    entry_id: str,
    address: Optional[str] = None,
    timeout: Optional[str] = None,
    comment: Optional[str] = None,
    disabled: Optional[bool] = None
) -> str:
    """
    Updates an existing address list entry.
    
    Args:
        entry_id: ID of the entry to update
        address: New address
        timeout: New timeout (e.g., "1h", "30m", "1d", "1w", or "none" to remove)
        comment: New comment
        disabled: Enable/disable the entry
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Updating address list entry: entry_id={entry_id}")
    
    # Build the command
    cmd = f"/ip firewall address-list set {entry_id}"
    
    updates = []
    if address:
        updates.append(f"address={address}")
    
    if timeout is not None:
        if timeout.lower() == "none" or timeout == "":
            updates.append("!timeout")
        else:
            if not _validate_timeout(timeout):
                return f"Error: Invalid timeout format '{timeout}'. Use format like: 1h, 30m, 1d, 1w"
            updates.append(f"timeout={timeout}")
    
    if comment is not None:
        updates.append(f'comment="{comment}"')
    
    if disabled is not None:
        updates.append(f'disabled={"yes" if disabled else "no"}')
    
    if not updates:
        return "No updates specified."
    
    cmd += " " + " ".join(updates)
    
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to update address list entry: {result}"
    
    # Get the updated entry details
    details_cmd = f"/ip firewall address-list print detail where .id={entry_id}"
    details = execute_mikrotik_command(details_cmd)
    
    return f"Address list entry updated successfully:\n\n{details}"

def mikrotik_get_address_list_entry(entry_id: str) -> str:
    """
    Gets detailed information about a specific address list entry.
    
    Args:
        entry_id: ID of the address list entry
    
    Returns:
        Detailed information about the entry
    """
    app_logger.info(f"Getting address list entry details: entry_id={entry_id}")
    
    cmd = f"/ip firewall address-list print detail where .id={entry_id}"
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return f"Address list entry with ID '{entry_id}' not found."
    
    return f"ADDRESS LIST ENTRY DETAILS:\n\n{result}"

def mikrotik_list_address_list_names() -> str:
    """
    Lists all unique address list names currently in use.
    
    Returns:
        List of address list names
    """
    app_logger.info("Listing all address list names")
    
    # Get all address lists and extract unique list names
    cmd = "/ip firewall address-list print terse"
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return "No address lists found."
    
    # Parse the output to extract unique list names
    list_names = set()
    for line in result.split('\n'):
        if 'list=' in line:
            # Extract list name from the line
            parts = line.split('list=')
            if len(parts) > 1:
                list_name = parts[1].split()[0].strip('"')
                list_names.add(list_name)
    
    if not list_names:
        return "No address lists found."
    
    return "ADDRESS LIST NAMES:\n\n" + "\n".join(sorted(list_names))

def mikrotik_clear_address_list(list_name: str) -> str:
    """
    Removes all entries from a specific address list.
    
    Args:
        list_name: Name of the address list to clear
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Clearing address list: list_name={list_name}")
    
    # Get all entries for this list
    cmd = f'/ip firewall address-list remove [find list="{list_name}"]'
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to clear address list '{list_name}': {result}"
    
    return f"Address list '{list_name}' cleared successfully."

def mikrotik_enable_address_list_entry(entry_id: str) -> str:
    """
    Enables an address list entry.
    
    Args:
        entry_id: ID of the entry to enable
    
    Returns:
        Command output or error message
    """
    return mikrotik_update_address_list_entry(entry_id, disabled=False)

def mikrotik_disable_address_list_entry(entry_id: str) -> str:
    """
    Disables an address list entry.
    
    Args:
        entry_id: ID of the entry to disable
    
    Returns:
        Command output or error message
    """
    return mikrotik_update_address_list_entry(entry_id, disabled=True)

def _validate_timeout(timeout: str) -> bool:
    """
    Validates timeout format.
    
    Args:
        timeout: Timeout string (e.g., "1h", "30m", "1d", "1w")
    
    Returns:
        True if valid, False otherwise
    """
    if not timeout:
        return False
    
    # Check if it matches the pattern: number + unit
    import re
    pattern = r'^\d+[smhdw]$'
    return bool(re.match(pattern, timeout.lower()))

