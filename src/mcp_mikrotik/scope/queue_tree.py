from typing import Optional
from ..connector import execute_mikrotik_command
from ..api_fallback import api_fallback_execute
from ..logger import app_logger

def mikrotik_list_queue_trees(
    name_filter: Optional[str] = None,
    parent_filter: Optional[str] = None,
    disabled_only: bool = False,
    invalid_only: bool = False
) -> str:
    """
    Lists queue tree entries on MikroTik device.
    
    Args:
        name_filter: Filter by queue tree name
        parent_filter: Filter by parent queue
        disabled_only: Show only disabled entries
        invalid_only: Show only invalid entries
    
    Returns:
        List of queue tree entries
    """
    app_logger.info(f"Listing queue trees: name_filter={name_filter}")
    
    cmd = "/queue tree print detail"
    
    filters = []
    if name_filter:
        filters.append(f'name~"{name_filter}"')
    if parent_filter:
        filters.append(f'parent~"{parent_filter}"')
    if disabled_only:
        filters.append("disabled=yes")
    if invalid_only:
        filters.append("invalid=yes")
    
    if filters:
        cmd += " where " + " ".join(filters)
    
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return "No queue trees found matching the criteria."
    
    return f"QUEUE TREES:\n\n{result}"

def mikrotik_get_queue_tree(queue_id: str) -> str:
    """
    Gets detailed information about a specific queue tree.
    
    Args:
        queue_id: ID or name of the queue tree
    
    Returns:
        Detailed information about the queue tree
    """
    app_logger.info(f"Getting queue tree details: queue_id={queue_id}")
    
    cmd = f'/queue tree print detail where (.id={queue_id} or name="{queue_id}")'
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return f"Queue tree with ID or name '{queue_id}' not found."
    
    return f"QUEUE TREE DETAILS:\n\n{result}"

def mikrotik_create_queue_tree(
    name: str,
    parent: str,
    packet_mark: Optional[str] = None,
    max_limit: Optional[str] = None,
    limit_at: Optional[str] = None,
    priority: int = 8,
    queue: str = "default",
    burst_limit: Optional[str] = None,
    burst_threshold: Optional[str] = None,
    burst_time: Optional[str] = None,
    comment: Optional[str] = None,
    disabled: bool = False
) -> str:
    """
    Creates a queue tree entry on MikroTik device.
    
    Args:
        name: Name for the queue tree
        parent: Parent queue or interface (e.g., "global", "ether1", or another queue name)
        packet_mark: Packet mark to match
        max_limit: Maximum data rate (e.g., "10M", "1G", "512k")
        limit_at: Guaranteed data rate
        priority: Queue priority (1-8, lower is higher priority)
        queue: Queue type (default, pcq-upload, pcq-download, etc.)
        burst_limit: Burst rate limit
        burst_threshold: Burst threshold
        burst_time: Burst time
        comment: Optional comment
        disabled: Whether to disable the queue after creation
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Creating queue tree: name={name}, parent={parent}")
    
    if not name or name.strip() == "":
        return "Error: Queue tree name cannot be empty."
    
    if not parent or parent.strip() == "":
        return "Error: Parent cannot be empty."
    
    # Validate priority
    if not 1 <= priority <= 8:
        return "Error: Priority must be between 1 and 8."
    
    # Build the command
    cmd = f'/queue tree add name="{name}" parent="{parent}"'
    
    if packet_mark:
        cmd += f' packet-mark="{packet_mark}"'
    
    if max_limit:
        cmd += f' max-limit={max_limit}'
    
    if limit_at:
        cmd += f' limit-at={limit_at}'
    
    cmd += f' priority={priority}'
    cmd += f' queue={queue}'
    
    if burst_limit:
        cmd += f' burst-limit={burst_limit}'
    
    if burst_threshold:
        cmd += f' burst-threshold={burst_threshold}'
    
    if burst_time:
        cmd += f' burst-time={burst_time}'
    
    if comment:
        cmd += f' comment="{comment}"'
    
    if disabled:
        cmd += " disabled=yes"
    
    result = execute_mikrotik_command(cmd)
    
    if result.strip() and ("*" in result or result.strip().isdigit()):
        queue_id = result.strip()
        details_cmd = f"/queue tree print detail where .id={queue_id}"
        details = execute_mikrotik_command(details_cmd)
        
        if details.strip():
            return f"Queue tree created successfully:\n\n{details}"
        else:
            return f"Queue tree created with ID: {result}"
    else:
        return f"Failed to create queue tree: {result}" if result else "Queue tree creation completed."

def mikrotik_update_queue_tree(
    queue_id: str,
    name: Optional[str] = None,
    parent: Optional[str] = None,
    packet_mark: Optional[str] = None,
    max_limit: Optional[str] = None,
    limit_at: Optional[str] = None,
    priority: Optional[int] = None,
    queue: Optional[str] = None,
    burst_limit: Optional[str] = None,
    burst_threshold: Optional[str] = None,
    burst_time: Optional[str] = None,
    comment: Optional[str] = None,
    disabled: Optional[bool] = None
) -> str:
    """
    Updates an existing queue tree entry.
    
    Args:
        queue_id: ID or name of the queue tree to update
        name: New name
        parent: New parent
        packet_mark: New packet mark
        max_limit: New maximum data rate
        limit_at: New guaranteed data rate
        priority: New priority (1-8)
        queue: New queue type
        burst_limit: New burst limit
        burst_threshold: New burst threshold
        burst_time: New burst time
        comment: New comment
        disabled: Enable/disable the queue
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Updating queue tree: queue_id={queue_id}")
    
    cmd = f"/queue tree set {queue_id}"
    updates = []
    
    if name:
        updates.append(f'name="{name}"')
    
    if parent:
        updates.append(f'parent="{parent}"')
    
    if packet_mark is not None:
        if packet_mark == "":
            updates.append("!packet-mark")
        else:
            updates.append(f'packet-mark="{packet_mark}"')
    
    if max_limit:
        updates.append(f'max-limit={max_limit}')
    
    if limit_at:
        updates.append(f'limit-at={limit_at}')
    
    if priority is not None:
        if not 1 <= priority <= 8:
            return "Error: Priority must be between 1 and 8."
        updates.append(f'priority={priority}')
    
    if queue:
        updates.append(f'queue={queue}')
    
    if burst_limit:
        updates.append(f'burst-limit={burst_limit}')
    
    if burst_threshold:
        updates.append(f'burst-threshold={burst_threshold}')
    
    if burst_time:
        updates.append(f'burst-time={burst_time}')
    
    if comment is not None:
        updates.append(f'comment="{comment}"')
    
    if disabled is not None:
        updates.append(f'disabled={"yes" if disabled else "no"}')
    
    if not updates:
        return "No updates specified."
    
    cmd += " " + " ".join(updates)
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to update queue tree: {result}"
    
    details_cmd = f"/queue tree print detail where .id={queue_id}"
    details = execute_mikrotik_command(details_cmd)
    return f"Queue tree updated successfully:\n\n{details}"

def mikrotik_remove_queue_tree(queue_id: str) -> str:
    """
    Removes a queue tree entry.
    
    Args:
        queue_id: ID or name of the queue tree to remove
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Removing queue tree: queue_id={queue_id}")
    
    check_cmd = f"/queue tree print count-only where .id={queue_id}"
    count = execute_mikrotik_command(check_cmd)
    
    if count.strip() == "0":
        check_cmd = f'/queue tree print count-only where name="{queue_id}"'
        count = execute_mikrotik_command(check_cmd)
        
        if count.strip() == "0":
            return f"Queue tree with ID or name '{queue_id}' not found."
    
    cmd = f"/queue tree remove {queue_id}"
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to remove queue tree: {result}"
    
    return f"Queue tree '{queue_id}' removed successfully."

def mikrotik_enable_queue_tree(queue_id: str) -> str:
    """
    Enables a queue tree entry.
    
    Args:
        queue_id: ID or name of the queue tree to enable
    
    Returns:
        Command output or error message
    """
    return mikrotik_update_queue_tree(queue_id, disabled=False)

def mikrotik_disable_queue_tree(queue_id: str) -> str:
    """
    Disables a queue tree entry.
    
    Args:
        queue_id: ID or name of the queue tree to disable
    
    Returns:
        Command output or error message
    """
    return mikrotik_update_queue_tree(queue_id, disabled=True)

def mikrotik_create_htb_queue_tree(
    interface: str,
    total_download: str,
    total_upload: str
) -> str:
    """
    Creates a hierarchical HTB (Hierarchical Token Bucket) queue tree structure.
    
    Args:
        interface: Interface to apply QoS to
        total_download: Total download bandwidth (e.g., "100M")
        total_upload: Total upload bandwidth (e.g., "20M")
    
    Returns:
        Setup result
    """
    app_logger.info(f"Creating HTB queue tree for interface: {interface}")
    
    results = []
    
    # Create parent download queue
    download_parent = f"{interface}-download"
    cmd1 = f'/queue tree add name="{download_parent}" parent="{interface}" max-limit={total_download} comment="Download parent queue"'
    result1 = execute_mikrotik_command(cmd1)
    results.append(f"✓ Download parent created: {download_parent} ({total_download})")
    
    # Create parent upload queue
    upload_parent = f"{interface}-upload"
    cmd2 = f'/queue tree add name="{upload_parent}" parent=global max-limit={total_upload} comment="Upload parent queue"'
    result2 = execute_mikrotik_command(cmd2)
    results.append(f"✓ Upload parent created: {upload_parent} ({total_upload})")
    
    results.append("\n✓ HTB queue tree structure created.")
    results.append("  Next steps:")
    results.append(f"  1. Create child queues under '{download_parent}' and '{upload_parent}'")
    results.append("  2. Use packet marks to classify traffic")
    results.append("  3. Set priorities and limits for each child queue")
    
    return "HTB QUEUE TREE SETUP:\n\n" + "\n".join(results)

def mikrotik_create_priority_queue_tree(
    interface: str,
    total_bandwidth: str,
    priorities: list
) -> str:
    """
    Creates a priority-based queue tree structure.
    
    Args:
        interface: Interface to apply QoS to
        total_bandwidth: Total bandwidth (e.g., "100M")
        priorities: List of priority configurations [{"name": "high", "priority": 1, "limit": "50M", "packet_mark": "high-priority"}]
    
    Returns:
        Setup result
    """
    app_logger.info(f"Creating priority queue tree for interface: {interface}")
    
    results = []
    
    # Create parent queue
    parent_name = f"{interface}-parent"
    cmd = f'/queue tree add name="{parent_name}" parent="{interface}" max-limit={total_bandwidth} comment="Priority queue parent"'
    execute_mikrotik_command(cmd)
    results.append(f"✓ Parent queue created: {parent_name}")
    
    # Create priority queues
    for prio in priorities:
        queue_name = prio.get("name", f"priority-{prio.get('priority')}")
        priority_val = prio.get("priority", 8)
        max_limit = prio.get("limit", total_bandwidth)
        packet_mark = prio.get("packet_mark")
        
        cmd = f'/queue tree add name="{queue_name}" parent="{parent_name}" priority={priority_val} max-limit={max_limit}'
        
        if packet_mark:
            cmd += f' packet-mark="{packet_mark}"'
        
        cmd += f' comment="Priority {priority_val} queue"'
        
        execute_mikrotik_command(cmd)
        results.append(f"✓ Priority queue created: {queue_name} (priority={priority_val}, limit={max_limit})")
    
    return "PRIORITY QUEUE TREE SETUP:\n\n" + "\n".join(results)

def mikrotik_list_pcq_queues() -> str:
    """
    Lists PCQ (Per Connection Queue) queue types.
    
    Returns:
        List of PCQ queues
    """
    app_logger.info("Listing PCQ queues")
    
    cmd = "/queue type print detail where kind=pcq"
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return "No PCQ queues found."
    
    return f"PCQ QUEUES:\n\n{result}"

def mikrotik_create_pcq_queue(
    name: str,
    rate: str,
    classifier: Optional[str] = None,
    pcq_limit: int = 50,
    pcq_total_limit: int = 2000,
    comment: Optional[str] = None
) -> str:
    """
    Creates a PCQ (Per Connection Queue) type.
    
    Args:
        name: Name for the PCQ queue
        rate: Data rate (e.g., "10M", "1G")
        classifier: Classifier (src-address, dst-address, src-port, dst-port)
        pcq_limit: PCQ limit (KiB per connection)
        pcq_total_limit: PCQ total limit (KiB total)
        comment: Optional comment
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Creating PCQ queue: name={name}, rate={rate}")
    
    if not name or name.strip() == "":
        return "Error: PCQ queue name cannot be empty."
    
    cmd = f'/queue type add name="{name}" kind=pcq pcq-rate={rate}'
    
    if classifier:
        valid_classifiers = ["src-address", "dst-address", "src-port", "dst-port", ""]
        if classifier not in valid_classifiers:
            return f"Error: Invalid classifier. Must be one of: {', '.join(valid_classifiers[:-1])}"
        cmd += f' pcq-classifier={classifier}'
    
    cmd += f' pcq-limit={pcq_limit}KiB'
    cmd += f' pcq-total-limit={pcq_total_limit}KiB'
    
    if comment:
        cmd += f' comment="{comment}"'
    
    result = execute_mikrotik_command(cmd)
    
    if result.strip() and ("*" in result or result.strip().isdigit()):
        return f"PCQ queue type '{name}' created successfully."
    else:
        return f"Failed to create PCQ queue: {result}" if result else "PCQ queue created."

def mikrotik_remove_pcq_queue(queue_name: str) -> str:
    """
    Removes a PCQ queue type.
    
    Args:
        queue_name: Name of the PCQ queue to remove
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Removing PCQ queue: queue_name={queue_name}")
    
    cmd = f'/queue type remove [find name="{queue_name}"]'
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to remove PCQ queue: {result}"
    
    return f"PCQ queue '{queue_name}' removed successfully."

def mikrotik_create_traffic_shaping_tree(
    interface: str,
    total_bandwidth: str,
    traffic_classes: list
) -> str:
    """
    Creates a complete traffic shaping tree with multiple classes.
    
    Args:
        interface: Interface to apply shaping to
        total_bandwidth: Total bandwidth (e.g., "100M")
        traffic_classes: List of traffic class configs [{"name": "voip", "mark": "voip-traffic", "priority": 1, "limit": "10M", "guaranteed": "5M"}]
    
    Returns:
        Setup result
    """
    app_logger.info(f"Creating traffic shaping tree for: {interface}")
    
    results = []
    
    # Create root queue
    root_name = f"{interface}-root"
    root_cmd = f'/queue tree add name="{root_name}" parent="{interface}" max-limit={total_bandwidth} comment="Traffic shaping root"'
    execute_mikrotik_command(root_cmd)
    results.append(f"✓ Root queue created: {root_name} ({total_bandwidth})")
    
    # Create traffic class queues
    for tc in traffic_classes:
        class_name = tc.get("name")
        packet_mark = tc.get("mark")
        priority = tc.get("priority", 8)
        max_limit = tc.get("limit", total_bandwidth)
        limit_at = tc.get("guaranteed")
        
        cmd = f'/queue tree add name="{class_name}" parent="{root_name}" priority={priority} max-limit={max_limit}'
        
        if packet_mark:
            cmd += f' packet-mark="{packet_mark}"'
        
        if limit_at:
            cmd += f' limit-at={limit_at}'
        
        cmd += f' comment="Traffic class: {class_name}"'
        
        execute_mikrotik_command(cmd)
        results.append(f"✓ Traffic class created: {class_name} (priority={priority}, max={max_limit})")
    
    results.append(f"\n✓ Traffic shaping tree created with {len(traffic_classes)} classes.")
    
    return "TRAFFIC SHAPING TREE SETUP:\n\n" + "\n".join(results)

