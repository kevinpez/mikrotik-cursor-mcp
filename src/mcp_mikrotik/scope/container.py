from typing import Optional

from ..connector import execute_mikrotik_command
from ..api_fallback import api_fallback_execute
from ..logger import app_logger


# ============================================================================
# CONTAINER MANAGEMENT
# ============================================================================

def mikrotik_list_containers() -> str:
    """
    Lists all containers on MikroTik device.
    
    Returns:
        List of containers
    """
    app_logger.info("Listing containers")
    
    cmd = "/container print"
    result = execute_mikrotik_command(cmd)
    
    return f"CONTAINERS:\n\n{result}"


def mikrotik_create_container(
        name: str,
        image: str,
        interface: Optional[str] = None,
        envlist: Optional[str] = None,
        root_dir: Optional[str] = None,
        cmd: Optional[str] = None,
        mounts: Optional[str] = None,
        start: bool = True,
        comment: Optional[str] = None
) -> str:
    """
    Creates a container.
    
    Args:
        name: Container name
        image: Container image name/tag
        interface: Network interface (e.g., "veth1")
        envlist: Environment variable list name
        root_dir: Root directory path
        cmd: Command to execute
        mounts: Mount points
        start: Start container after creation
        comment: Optional comment
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Creating container: {name}")
    
    cmd_str = f'/container add name={name} remote-image="{image}"'
    
    if interface:
        cmd_str += f" interface={interface}"
    if envlist:
        cmd_str += f" envlist={envlist}"
    if root_dir:
        cmd_str += f' root-dir="{root_dir}"'
    if cmd:
        cmd_str += f' cmd="{cmd}"'
    if mounts:
        cmd_str += f' mounts="{mounts}"'
    if start:
        cmd_str += " start-on-boot=yes"
    if comment:
        cmd_str += f' comment="{comment}"'
    
    result = execute_mikrotik_command(cmd_str)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to create container: {result}"
    
    return f"Container '{name}' created successfully."


def mikrotik_remove_container(name: str) -> str:
    """
    Removes a container.
    
    Args:
        name: Container name
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Removing container: {name}")
    
    cmd = f'/container remove [find name="{name}"]'
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to remove container: {result}"
    
    return f"Container '{name}' removed successfully."


def mikrotik_start_container(name: str) -> str:
    """
    Starts a container.
    
    Args:
        name: Container name
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Starting container: {name}")
    
    cmd = f'/container start [find name="{name}"]'
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to start container: {result}"
    
    return f"Container '{name}' started successfully."


def mikrotik_stop_container(name: str) -> str:
    """
    Stops a container.
    
    Args:
        name: Container name
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Stopping container: {name}")
    
    cmd = f'/container stop [find name="{name}"]'
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to stop container: {result}"
    
    return f"Container '{name}' stopped successfully."


def mikrotik_get_container(name: str) -> str:
    """
    Gets detailed information about a container.
    
    Args:
        name: Container name
    
    Returns:
        Container details
    """
    app_logger.info(f"Getting container details: {name}")
    
    cmd = f'/container print detail where name="{name}"'
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return f"Container '{name}' not found."
    
    return f"CONTAINER DETAILS:\n\n{result}"


# ============================================================================
# CONTAINER CONFIG
# ============================================================================

def mikrotik_get_container_config() -> str:
    """
    Gets container configuration settings.
    
    Returns:
        Container configuration
    """
    app_logger.info("Getting container configuration")
    
    cmd = "/container config print"
    result = execute_mikrotik_command(cmd)
    
    return f"CONTAINER CONFIGURATION:\n\n{result}"


def mikrotik_set_container_registry(
        url: str,
        username: Optional[str] = None,
        password: Optional[str] = None
) -> str:
    """
    Sets container registry URL and credentials.
    
    Args:
        url: Registry URL
        username: Registry username
        password: Registry password
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Setting container registry: {url}")
    
    cmd = f'/container config set registry-url="{url}"'
    
    if username:
        cmd += f' registry-username="{username}"'
    if password:
        cmd += f' registry-password="{password}"'
    
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to set container registry: {result}"
    
    return "Container registry configured successfully."


def mikrotik_set_container_tmpdir(tmpdir: str) -> str:
    """
    Sets container temporary directory.
    
    Args:
        tmpdir: Temporary directory path
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Setting container tmpdir: {tmpdir}")
    
    cmd = f'/container config set tmpdir="{tmpdir}"'
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to set container tmpdir: {result}"
    
    return "Container tmpdir configured successfully."


# ============================================================================
# CONTAINER ENVIRONMENTS
# ============================================================================

def mikrotik_list_container_envs() -> str:
    """
    Lists all container environment variable lists.
    
    Returns:
        List of environment variable lists
    """
    app_logger.info("Listing container environments")
    
    cmd = "/container envs print"
    result = execute_mikrotik_command(cmd)
    
    return f"CONTAINER ENVIRONMENTS:\n\n{result}"


def mikrotik_create_container_env(name: str, key: str, value: str) -> str:
    """
    Creates a container environment variable.
    
    Args:
        name: Environment list name
        key: Variable name
        value: Variable value
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Creating container environment: {name}")
    
    cmd = f'/container envs add name={name} key="{key}" value="{value}"'
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to create container environment: {result}"
    
    return f"Container environment '{name}' created successfully."


def mikrotik_remove_container_env(name: str) -> str:
    """
    Removes a container environment variable.
    
    Args:
        name: Environment list name
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Removing container environment: {name}")
    
    cmd = f'/container envs remove [find name="{name}"]'
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to remove container environment: {result}"
    
    return f"Container environment '{name}' removed successfully."


# ============================================================================
# CONTAINER MOUNTS
# ============================================================================

def mikrotik_list_container_mounts() -> str:
    """
    Lists all container mount points.
    
    Returns:
        List of mount points
    """
    app_logger.info("Listing container mounts")
    
    cmd = "/container mounts print"
    result = execute_mikrotik_command(cmd)
    
    return f"CONTAINER MOUNTS:\n\n{result}"


def mikrotik_create_container_mount(
        name: str,
        src: str,
        dst: str
) -> str:
    """
    Creates a container mount point.
    
    Args:
        name: Mount name
        src: Source path on host
        dst: Destination path in container
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Creating container mount: {name}")
    
    cmd = f'/container mounts add name={name} src="{src}" dst="{dst}"'
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to create container mount: {result}"
    
    return f"Container mount '{name}' created successfully."


def mikrotik_remove_container_mount(name: str) -> str:
    """
    Removes a container mount point.
    
    Args:
        name: Mount name
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Removing container mount: {name}")
    
    cmd = f'/container mounts remove [find name="{name}"]'
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to remove container mount: {result}"
    
    return f"Container mount '{name}' removed successfully."


# ============================================================================
# CONTAINER VETHs (Virtual Ethernet)
# ============================================================================

def mikrotik_list_container_veths() -> str:
    """
    Lists all container virtual ethernet interfaces.
    
    Returns:
        List of veth interfaces
    """
    app_logger.info("Listing container veths")
    
    cmd = "/interface veth print"
    result = execute_mikrotik_command(cmd)
    
    return f"CONTAINER VETHS:\n\n{result}"


def mikrotik_create_container_veth(
        name: str,
        address: Optional[str] = None,
        gateway: Optional[str] = None
) -> str:
    """
    Creates a container virtual ethernet interface.
    
    Args:
        name: Veth interface name
        address: IP address for the veth
        gateway: Gateway address
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Creating container veth: {name}")
    
    cmd = f"/interface veth add name={name}"
    
    if address:
        cmd += f' address="{address}"'
    if gateway:
        cmd += f' gateway="{gateway}"'
    
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to create container veth: {result}"
    
    return f"Container veth '{name}' created successfully."


def mikrotik_remove_container_veth(name: str) -> str:
    """
    Removes a container virtual ethernet interface.
    
    Args:
        name: Veth interface name
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Removing container veth: {name}")
    
    cmd = f'/interface veth remove [find name="{name}"]'
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to remove container veth: {result}"
    
    return f"Container veth '{name}' removed successfully."

