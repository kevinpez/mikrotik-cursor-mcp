from typing import Optional
from ..connector import execute_mikrotik_command
from ..api_fallback import api_fallback_execute
from ..logger import app_logger

def mikrotik_list_layer7_protocols(
    name_filter: Optional[str] = None,
    disabled_only: bool = False
) -> str:
    """
    Lists Layer 7 protocol matchers on MikroTik device.
    
    Args:
        name_filter: Filter by protocol name
        disabled_only: Show only disabled protocols
    
    Returns:
        List of Layer 7 protocol matchers
    """
    app_logger.info(f"Listing Layer 7 protocols: name_filter={name_filter}")
    
    cmd = "/ip firewall layer7-protocol print detail"
    
    # Add filters
    filters = []
    if name_filter:
        filters.append(f'name~"{name_filter}"')
    if disabled_only:
        filters.append("disabled=yes")
    
    if filters:
        cmd += " where " + " ".join(filters)
    
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "" or result.strip() == "no such item":
        return "No Layer 7 protocols found matching the criteria."
    
    return f"LAYER 7 PROTOCOLS:\n\n{result}"

def mikrotik_create_layer7_protocol(
    name: str,
    regexp: str,
    comment: Optional[str] = None,
    disabled: bool = False
) -> str:
    """
    Creates a Layer 7 protocol matcher on MikroTik device.
    
    Args:
        name: Name for the Layer 7 protocol matcher
        regexp: Regular expression to match protocol traffic
        comment: Optional comment
        disabled: Whether to disable the protocol after creation
    
    Returns:
        Command output or error message
    
    Examples:
        - HTTP: regexp="^.*(get|post|head).*(http/1\\\\.).*$"
        - YouTube: regexp="^.*(youtube.com|googlevideo.com).*$"
        - Facebook: regexp="^.*(facebook.com|fbcdn.net).*$"
        - Skype: regexp="^.*(skype|skypeassets).*$"
    """
    app_logger.info(f"Creating Layer 7 protocol: name={name}")
    
    # Validate name
    if not name or name.strip() == "":
        return "Error: Protocol name cannot be empty."
    
    if not regexp or regexp.strip() == "":
        return "Error: Regular expression cannot be empty."
    
    # Build the command
    cmd = f'/ip firewall layer7-protocol add name="{name}" regexp="{regexp}"'
    
    if comment:
        cmd += f' comment="{comment}"'
    
    if disabled:
        cmd += " disabled=yes"
    
    result = execute_mikrotik_command(cmd)
    
    # Check if creation was successful
    if result.strip():
        if "*" in result or result.strip().isdigit():
            # Success
            protocol_id = result.strip()
            details_cmd = f"/ip firewall layer7-protocol print detail where .id={protocol_id}"
            details = execute_mikrotik_command(details_cmd)
            
            if details.strip():
                return f"Layer 7 protocol created successfully:\n\n{details}"
            else:
                return f"Layer 7 protocol created with ID: {result}"
        else:
            return f"Failed to create Layer 7 protocol: {result}"
    else:
        return "Layer 7 protocol creation completed but unable to verify."

def mikrotik_get_layer7_protocol(protocol_id: str) -> str:
    """
    Gets detailed information about a specific Layer 7 protocol matcher.
    
    Args:
        protocol_id: ID or name of the Layer 7 protocol
    
    Returns:
        Detailed information about the protocol
    """
    app_logger.info(f"Getting Layer 7 protocol details: protocol_id={protocol_id}")
    
    # Try by ID first
    cmd = f"/ip firewall layer7-protocol print detail where .id={protocol_id}"
    result = execute_mikrotik_command(cmd)
    
    # If not found by ID, try by name
    if not result or result.strip() == "":
        cmd = f'/ip firewall layer7-protocol print detail where name="{protocol_id}"'
        result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return f"Layer 7 protocol with ID or name '{protocol_id}' not found."
    
    return f"LAYER 7 PROTOCOL DETAILS:\n\n{result}"

def mikrotik_update_layer7_protocol(
    protocol_id: str,
    name: Optional[str] = None,
    regexp: Optional[str] = None,
    comment: Optional[str] = None,
    disabled: Optional[bool] = None
) -> str:
    """
    Updates an existing Layer 7 protocol matcher.
    
    Args:
        protocol_id: ID or name of the protocol to update
        name: New name
        regexp: New regular expression
        comment: New comment
        disabled: Enable/disable the protocol
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Updating Layer 7 protocol: protocol_id={protocol_id}")
    
    # Build the command
    cmd = f"/ip firewall layer7-protocol set {protocol_id}"
    
    updates = []
    if name:
        updates.append(f'name="{name}"')
    if regexp:
        updates.append(f'regexp="{regexp}"')
    if comment is not None:
        updates.append(f'comment="{comment}"')
    if disabled is not None:
        updates.append(f'disabled={"yes" if disabled else "no"}')
    
    if not updates:
        return "No updates specified."
    
    cmd += " " + " ".join(updates)
    
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to update Layer 7 protocol: {result}"
    
    # Get the updated protocol details
    details_cmd = f"/ip firewall layer7-protocol print detail where .id={protocol_id}"
    details = execute_mikrotik_command(details_cmd)
    
    return f"Layer 7 protocol updated successfully:\n\n{details}"

def mikrotik_remove_layer7_protocol(protocol_id: str) -> str:
    """
    Removes a Layer 7 protocol matcher.
    
    Args:
        protocol_id: ID or name of the protocol to remove
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Removing Layer 7 protocol: protocol_id={protocol_id}")
    
    # First check if the protocol exists
    check_cmd = f"/ip firewall layer7-protocol print count-only where .id={protocol_id}"
    count = execute_mikrotik_command(check_cmd)
    
    if count.strip() == "0":
        # Try by name
        check_cmd = f'/ip firewall layer7-protocol print count-only where name="{protocol_id}"'
        count = execute_mikrotik_command(check_cmd)
        
        if count.strip() == "0":
            return f"Layer 7 protocol with ID or name '{protocol_id}' not found."
    
    # Remove the protocol
    cmd = f"/ip firewall layer7-protocol remove {protocol_id}"
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to remove Layer 7 protocol: {result}"
    
    return f"Layer 7 protocol '{protocol_id}' removed successfully."

def mikrotik_enable_layer7_protocol(protocol_id: str) -> str:
    """
    Enables a Layer 7 protocol matcher.
    
    Args:
        protocol_id: ID or name of the protocol to enable
    
    Returns:
        Command output or error message
    """
    return mikrotik_update_layer7_protocol(protocol_id, disabled=False)

def mikrotik_disable_layer7_protocol(protocol_id: str) -> str:
    """
    Disables a Layer 7 protocol matcher.
    
    Args:
        protocol_id: ID or name of the protocol to disable
    
    Returns:
        Command output or error message
    """
    return mikrotik_update_layer7_protocol(protocol_id, disabled=True)

def mikrotik_create_common_layer7_protocols() -> str:
    """
    Creates common Layer 7 protocol matchers for popular services.
    
    Returns:
        Setup result
    """
    app_logger.info("Creating common Layer 7 protocol matchers")
    
    results = []
    
    # Define common protocols
    protocols = [
        {
            "name": "http-get",
            "regexp": "^.*(get|post|head).*(http/1\\.).*$",
            "comment": "HTTP GET/POST/HEAD requests"
        },
        {
            "name": "youtube",
            "regexp": "^.*(youtube\\.com|googlevideo\\.com).*$",
            "comment": "YouTube video traffic"
        },
        {
            "name": "facebook",
            "regexp": "^.*(facebook\\.com|fbcdn\\.net|fbsbx\\.com).*$",
            "comment": "Facebook traffic"
        },
        {
            "name": "netflix",
            "regexp": "^.*(netflix\\.com|nflxvideo\\.net).*$",
            "comment": "Netflix streaming"
        },
        {
            "name": "spotify",
            "regexp": "^.*(spotify\\.com|scdn\\.co).*$",
            "comment": "Spotify music streaming"
        },
        {
            "name": "zoom",
            "regexp": "^.*(zoom\\.us|zoomgov\\.com).*$",
            "comment": "Zoom video conferencing"
        },
        {
            "name": "teams",
            "regexp": "^.*(teams\\.microsoft\\.com|skype\\.com).*$",
            "comment": "Microsoft Teams"
        },
        {
            "name": "whatsapp",
            "regexp": "^.*(whatsapp\\.com|whatsapp\\.net).*$",
            "comment": "WhatsApp messaging"
        }
    ]
    
    for protocol in protocols:
        cmd = f'/ip firewall layer7-protocol add name="{protocol["name"]}" regexp="{protocol["regexp"]}" comment="{protocol["comment"]}"'
        result = execute_mikrotik_command(cmd)
        
        if not result or "*" in result or result.strip().isdigit():
            results.append(f"✓ {protocol['name']}: Created successfully")
        else:
            results.append(f"✗ {protocol['name']}: {result}")
    
    return "COMMON LAYER 7 PROTOCOLS SETUP RESULTS:\n\n" + "\n".join(results)

