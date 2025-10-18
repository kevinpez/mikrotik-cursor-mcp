from typing import Optional
from ..connector import execute_mikrotik_command
from ..api_fallback import api_fallback_execute
from ..logger import app_logger

def mikrotik_list_scheduled_tasks(
    name_filter: Optional[str] = None,
    disabled_only: bool = False
) -> str:
    """
    Lists scheduled tasks on MikroTik device.
    
    Args:
        name_filter: Filter by task name
        disabled_only: Show only disabled tasks
    
    Returns:
        List of scheduled tasks
    """
    app_logger.info(f"Listing scheduled tasks: name_filter={name_filter}")
    
    cmd = "/system scheduler print detail"
    
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
        return "No scheduled tasks found matching the criteria."
    
    return f"SCHEDULED TASKS:\n\n{result}"

def mikrotik_get_scheduled_task(task_id: str) -> str:
    """
    Gets detailed information about a specific scheduled task.
    
    Args:
        task_id: ID or name of the scheduled task
    
    Returns:
        Detailed information about the task
    """
    app_logger.info(f"Getting scheduled task details: task_id={task_id}")
    
    # Try by ID first
    cmd = f"/system scheduler print detail where .id={task_id}"
    result = execute_mikrotik_command(cmd)
    
    # If not found by ID, try by name
    if not result or result.strip() == "":
        cmd = f'/system scheduler print detail where name="{task_id}"'
        result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return f"Scheduled task with ID or name '{task_id}' not found."
    
    return f"SCHEDULED TASK DETAILS:\n\n{result}"

def mikrotik_create_scheduled_task(
    name: str,
    on_event: str,
    start_date: Optional[str] = None,
    start_time: Optional[str] = None,
    interval: Optional[str] = None,
    policy: Optional[str] = None,
    comment: Optional[str] = None,
    disabled: bool = False
) -> str:
    """
    Creates a scheduled task on MikroTik device.
    
    Args:
        name: Name for the scheduled task
        on_event: Script code or script name to execute
        start_date: Start date (format: MMM/DD/YYYY, e.g., jan/01/2024)
        start_time: Start time (format: HH:MM:SS)
        interval: Run interval (e.g., 1d, 1h30m, 5m)
        policy: Execution policy (read, write, policy, test, password, sniff, sensitive, romon)
        comment: Optional comment
        disabled: Whether to disable the task after creation
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Creating scheduled task: name={name}")
    
    if not name or name.strip() == "":
        return "Error: Task name cannot be empty."
    
    if not on_event or on_event.strip() == "":
        return "Error: on_event (script) cannot be empty."
    
    # Build the command
    cmd = f'/system scheduler add name="{name}" on-event="{on_event}"'
    
    if start_date:
        cmd += f' start-date={start_date}'
    
    if start_time:
        cmd += f' start-time={start_time}'
    
    if interval:
        cmd += f' interval={interval}'
    
    if policy:
        cmd += f' policy={policy}'
    else:
        # Default policy
        cmd += ' policy=read,write,policy,test'
    
    if comment:
        cmd += f' comment="{comment}"'
    
    if disabled:
        cmd += " disabled=yes"
    
    result = execute_mikrotik_command(cmd)
    
    # Check if creation was successful
    if result.strip():
        if "*" in result or result.strip().isdigit():
            task_id = result.strip()
            details_cmd = f"/system scheduler print detail where .id={task_id}"
            details = execute_mikrotik_command(details_cmd)
            
            if details.strip():
                return f"Scheduled task created successfully:\n\n{details}"
            else:
                return f"Scheduled task created with ID: {result}"
        else:
            return f"Failed to create scheduled task: {result}"
    else:
        return "Scheduled task creation completed but unable to verify."

def mikrotik_update_scheduled_task(
    task_id: str,
    name: Optional[str] = None,
    on_event: Optional[str] = None,
    start_date: Optional[str] = None,
    start_time: Optional[str] = None,
    interval: Optional[str] = None,
    policy: Optional[str] = None,
    comment: Optional[str] = None,
    disabled: Optional[bool] = None
) -> str:
    """
    Updates an existing scheduled task.
    
    Args:
        task_id: ID or name of the task to update
        name: New name
        on_event: New script code or script name
        start_date: New start date
        start_time: New start time
        interval: New interval
        policy: New execution policy
        comment: New comment
        disabled: Enable/disable the task
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Updating scheduled task: task_id={task_id}")
    
    # Build the command
    cmd = f"/system scheduler set {task_id}"
    
    updates = []
    if name:
        updates.append(f'name="{name}"')
    if on_event:
        updates.append(f'on-event="{on_event}"')
    if start_date:
        updates.append(f'start-date={start_date}')
    if start_time:
        updates.append(f'start-time={start_time}')
    if interval:
        updates.append(f'interval={interval}')
    if policy:
        updates.append(f'policy={policy}')
    if comment is not None:
        updates.append(f'comment="{comment}"')
    if disabled is not None:
        updates.append(f'disabled={"yes" if disabled else "no"}')
    
    if not updates:
        return "No updates specified."
    
    cmd += " " + " ".join(updates)
    
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to update scheduled task: {result}"
    
    # Get the updated task details
    details_cmd = f"/system scheduler print detail where .id={task_id}"
    details = execute_mikrotik_command(details_cmd)
    
    return f"Scheduled task updated successfully:\n\n{details}"

def mikrotik_remove_scheduled_task(task_id: str) -> str:
    """
    Removes a scheduled task.
    
    Args:
        task_id: ID or name of the task to remove
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Removing scheduled task: task_id={task_id}")
    
    # First check if the task exists
    check_cmd = f"/system scheduler print count-only where .id={task_id}"
    count = execute_mikrotik_command(check_cmd)
    
    if count.strip() == "0":
        # Try by name
        check_cmd = f'/system scheduler print count-only where name="{task_id}"'
        count = execute_mikrotik_command(check_cmd)
        
        if count.strip() == "0":
            return f"Scheduled task with ID or name '{task_id}' not found."
    
    # Remove the task
    cmd = f"/system scheduler remove {task_id}"
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to remove scheduled task: {result}"
    
    return f"Scheduled task '{task_id}' removed successfully."

def mikrotik_enable_scheduled_task(task_id: str) -> str:
    """
    Enables a scheduled task.
    
    Args:
        task_id: ID or name of the task to enable
    
    Returns:
        Command output or error message
    """
    return mikrotik_update_scheduled_task(task_id, disabled=False)

def mikrotik_disable_scheduled_task(task_id: str) -> str:
    """
    Disables a scheduled task.
    
    Args:
        task_id: ID or name of the task to disable
    
    Returns:
        Command output or error message
    """
    return mikrotik_update_scheduled_task(task_id, disabled=True)

def mikrotik_run_scheduled_task(task_id: str) -> str:
    """
    Manually runs a scheduled task immediately.
    
    Args:
        task_id: ID or name of the task to run
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Running scheduled task: task_id={task_id}")
    
    # Get the task's on-event script
    cmd = f'/system scheduler print detail where (.id={task_id} or name="{task_id}")'
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return f"Scheduled task with ID or name '{task_id}' not found."
    
    # Extract the on-event script from the result
    on_event = None
    for line in result.split('\n'):
        if 'on-event=' in line:
            # Extract script
            parts = line.split('on-event=')
            if len(parts) > 1:
                on_event = parts[1].split('"')[1] if '"' in parts[1] else parts[1].split()[0]
                break
    
    if not on_event:
        return f"Could not extract script from task '{task_id}'."
    
    # Execute the script
    exec_cmd = f'/system script run [find name="{on_event}"]'
    exec_result = execute_mikrotik_command(exec_cmd)
    
    return f"Scheduled task '{task_id}' executed.\n\nResult:\n{exec_result if exec_result else 'Task executed successfully.'}"

def mikrotik_create_backup_schedule(
    name: str,
    interval: str,
    backup_name_prefix: str = "auto-backup",
    password: Optional[str] = None
) -> str:
    """
    Creates a scheduled backup task.
    
    Args:
        name: Name for the scheduled task
        interval: Backup interval (e.g., 1d, 12h, 1w)
        backup_name_prefix: Prefix for backup filenames
        password: Optional backup encryption password
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Creating backup schedule: name={name}, interval={interval}")
    
    # Create the backup script
    script_name = f"{name}-script"
    if password:
        script_content = f'/system backup save name="{backup_name_prefix}-[/system clock get date]" password="{password}"'
    else:
        script_content = f'/system backup save name="{backup_name_prefix}-[/system clock get date]"'
    
    # Create the script first
    create_script_cmd = f'/system script add name="{script_name}" source="{script_content}" policy=read,write,policy,test'
    script_result = execute_mikrotik_command(create_script_cmd)
    
    # Create the scheduled task
    task_result = mikrotik_create_scheduled_task(
        name=name,
        on_event=script_name,
        interval=interval,
        comment=f"Automatic backup every {interval}",
        policy="read,write,policy,test"
    )
    
    return f"Backup schedule created:\n\n{task_result}"

