from typing import Optional
from ..connector import execute_mikrotik_command
from ..logger import app_logger

def mikrotik_list_simple_queues(
    name_filter: Optional[str] = None,
    target_filter: Optional[str] = None,
    disabled_only: bool = False
) -> str:
    """List simple queues (bandwidth limits)"""
    app_logger.info(f"Listing simple queues: name={name_filter}")
    
    cmd = "/queue simple print"
    
    filters = []
    if name_filter:
        filters.append(f'name~"{name_filter}"')
    if target_filter:
        filters.append(f'target~"{target_filter}"')
    if disabled_only:
        filters.append("disabled=yes")
    
    if filters:
        cmd += " where " + " and ".join(filters)
    
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return "No simple queues found."
    
    return f"SIMPLE QUEUES:\n\n{result}"

def mikrotik_create_simple_queue(
    name: str,
    target: str,
    max_limit: str,
    limit_at: Optional[str] = None,
    burst_limit: Optional[str] = None,
    burst_threshold: Optional[str] = None,
    burst_time: Optional[str] = None,
    priority: Optional[int] = None,
    comment: Optional[str] = None,
    disabled: bool = False
) -> str:
    """Create a simple queue (bandwidth limit)"""
    app_logger.info(f"Creating simple queue: name={name}, target={target}")
    
    cmd = f'/queue simple add name="{name}" target={target} max-limit={max_limit}'
    
    if limit_at:
        cmd += f" limit-at={limit_at}"
    if burst_limit:
        cmd += f" burst-limit={burst_limit}"
    if burst_threshold:
        cmd += f" burst-threshold={burst_threshold}"
    if burst_time:
        cmd += f" burst-time={burst_time}"
    if priority is not None:
        cmd += f" priority={priority}/8"
    if comment:
        cmd += f' comment="{comment}"'
    if disabled:
        cmd += " disabled=yes"
    
    result = execute_mikrotik_command(cmd)
    
    if result.strip() and ("*" in result or result.strip().isdigit()):
        return f"Simple queue '{name}' created successfully.\n\nQueue ID: {result}"
    elif "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to create queue: {result}"
    else:
        return f"Simple queue '{name}' created successfully."

def mikrotik_remove_simple_queue(name: str) -> str:
    """Remove a simple queue"""
    app_logger.info(f"Removing simple queue: {name}")
    
    cmd = f'/queue simple remove [find where name="{name}"]'
    result = execute_mikrotik_command(cmd)
    
    if result.strip() == "" or "failure" not in result.lower():
        return f"Simple queue '{name}' removed successfully."
    else:
        return f"Failed to remove queue: {result}"

def mikrotik_enable_simple_queue(name: str) -> str:
    """Enable a simple queue"""
    app_logger.info(f"Enabling simple queue: {name}")
    
    cmd = f'/queue simple enable [find where name="{name}"]'
    result = execute_mikrotik_command(cmd)
    
    if result.strip() == "" or "failure" not in result.lower():
        return f"Simple queue '{name}' enabled successfully."
    else:
        return f"Failed to enable queue: {result}"

def mikrotik_disable_simple_queue(name: str) -> str:
    """Disable a simple queue"""
    app_logger.info(f"Disabling simple queue: {name}")
    
    cmd = f'/queue simple disable [find where name="{name}"]'
    result = execute_mikrotik_command(cmd)
    
    if result.strip() == "" or "failure" not in result.lower():
        return f"Simple queue '{name}' disabled successfully."
    else:
        return f"Failed to disable queue: {result}"

def mikrotik_update_simple_queue(
    name: str,
    max_limit: Optional[str] = None,
    limit_at: Optional[str] = None,
    burst_limit: Optional[str] = None,
    burst_threshold: Optional[str] = None,
    burst_time: Optional[str] = None,
    priority: Optional[int] = None,
    comment: Optional[str] = None
) -> str:
    """Update a simple queue"""
    app_logger.info(f"Updating simple queue: {name}")
    
    cmd = f'/queue simple set [find where name="{name}"]'
    
    updates = []
    if max_limit:
        updates.append(f"max-limit={max_limit}")
    if limit_at:
        updates.append(f"limit-at={limit_at}")
    if burst_limit:
        updates.append(f"burst-limit={burst_limit}")
    if burst_threshold:
        updates.append(f"burst-threshold={burst_threshold}")
    if burst_time:
        updates.append(f"burst-time={burst_time}")
    if priority is not None:
        updates.append(f"priority={priority}/8")
    if comment is not None:
        updates.append(f'comment="{comment}"')
    
    if not updates:
        return "No updates specified."
    
    cmd += " " + " ".join(updates)
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to update queue: {result}"
    
    return f"Simple queue '{name}' updated successfully."

def mikrotik_list_queue_types() -> str:
    """List available queue types"""
    app_logger.info("Listing queue types")
    
    cmd = "/queue type print"
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return "No queue types found."
    
    return f"QUEUE TYPES:\n\n{result}"

