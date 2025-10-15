"""
Validation helpers for MikroTik MCP tools.
Provides better error messages and input validation.
"""
import re
from typing import Optional, Tuple


def validate_ip_address(ip: str) -> Tuple[bool, str]:
    """
    Validate IP address format.
    
    Args:
        ip: IP address to validate
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    # IPv4 regex
    ipv4_pattern = r'^(\d{1,3}\.){3}\d{1,3}(/\d{1,2})?$'
    
    if not re.match(ipv4_pattern, ip):
        return False, f"Invalid IP address format: {ip}. Expected format: 192.168.1.1 or 192.168.1.1/24"
    
    # Validate octets are 0-255
    parts = ip.split('/')[0].split('.')
    for part in parts:
        if not 0 <= int(part) <= 255:
            return False, f"Invalid IP octet: {part}. Must be 0-255"
    
    # Validate CIDR if present
    if '/' in ip:
        cidr = int(ip.split('/')[1])
        if not 0 <= cidr <= 32:
            return False, f"Invalid CIDR: /{cidr}. Must be /0 to /32"
    
    return True, ""


def validate_wireguard_key(key: str) -> Tuple[bool, str]:
    """
    Validate WireGuard key format (base64, 44 characters).
    
    Args:
        key: WireGuard key to validate
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    # WireGuard keys are base64 encoded, 44 characters
    if len(key) != 44:
        return False, f"Invalid WireGuard key length: {len(key)}. Expected 44 characters"
    
    # Check base64 format
    base64_pattern = r'^[A-Za-z0-9+/]{43}=$'
    if not re.match(base64_pattern, key):
        return False, f"Invalid WireGuard key format. Must be base64 (A-Z, a-z, 0-9, +, /) ending with '='"
    
    return True, ""


def validate_port(port: int) -> Tuple[bool, str]:
    """
    Validate port number.
    
    Args:
        port: Port number to validate
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not 1 <= port <= 65535:
        return False, f"Invalid port number: {port}. Must be 1-65535"
    
    return True, ""


def validate_interface_name(name: str) -> Tuple[bool, str]:
    """
    Validate MikroTik interface name.
    
    Args:
        name: Interface name to validate
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    # MikroTik interface names: alphanumeric, dash, underscore
    if not re.match(r'^[a-zA-Z0-9_-]+$', name):
        return False, f"Invalid interface name: {name}. Use only letters, numbers, dash, underscore"
    
    if len(name) > 64:
        return False, f"Interface name too long: {len(name)} chars. Maximum 64 characters"
    
    return True, ""


def validate_keepalive(keepalive: str) -> Tuple[bool, str]:
    """
    Validate keepalive interval format.
    
    Args:
        keepalive: Keepalive interval (e.g., '25s', '1m30s')
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Format: number + unit (s for seconds, m for minutes, h for hours)
    pattern = r'^\d+[smh](\d+[smh])?$'
    
    if not re.match(pattern, keepalive):
        return False, f"Invalid keepalive format: {keepalive}. Use format like '25s', '1m', '1m30s'"
    
    return True, ""


def format_bytes(bytes_value: int) -> str:
    """
    Format bytes into human-readable format.
    
    Args:
        bytes_value: Number of bytes
    
    Returns:
        Formatted string (e.g., "1.5 KB", "2.3 MB")
    """
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    value = float(bytes_value)
    unit_index = 0
    
    while value >= 1024 and unit_index < len(units) - 1:
        value /= 1024
        unit_index += 1
    
    return f"{value:.2f} {units[unit_index]}"


def parse_mikrotik_time(time_str: str) -> Optional[int]:
    """
    Parse MikroTik time format to seconds.
    
    Args:
        time_str: Time string (e.g., '1w2d3h4m5s')
    
    Returns:
        Total seconds or None if invalid
    """
    units = {
        'w': 604800,  # weeks
        'd': 86400,   # days
        'h': 3600,    # hours
        'm': 60,      # minutes
        's': 1        # seconds
    }
    
    total_seconds = 0
    current_number = ''
    
    for char in time_str:
        if char.isdigit():
            current_number += char
        elif char in units:
            if current_number:
                total_seconds += int(current_number) * units[char]
                current_number = ''
        else:
            return None  # Invalid character
    
    return total_seconds if total_seconds > 0 else None

