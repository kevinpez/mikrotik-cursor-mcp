"""
Idempotency system for MikroTik operations.
Ensures operations can be safely repeated and desired state is achieved.
"""
import time
import hashlib
import json
from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass, asdict
from enum import Enum
from .connection_manager import get_connection_manager
from .logger import app_logger


class IdempotencyState(Enum):
    """States for idempotency checks."""
    MATCHES = "matches"           # Current state matches desired state
    DIFFERS = "differs"           # Current state differs from desired state
    MISSING = "missing"           # Desired resource is missing
    EXTRA = "extra"               # Extra resources exist
    ERROR = "error"               # Error occurred during check


@dataclass
class IdempotencyResult:
    """Result of an idempotency check."""
    state: IdempotencyState
    current_state: Optional[Dict[str, Any]] = None
    desired_state: Optional[Dict[str, Any]] = None
    differences: List[str] = None
    action_required: bool = False
    message: str = ""
    
    def __post_init__(self):
        if self.differences is None:
            self.differences = []


@dataclass
class DesiredState:
    """Represents a desired state for a resource."""
    resource_type: str
    resource_id: Optional[str] = None
    properties: Dict[str, Any] = None
    dependencies: List[str] = None
    priority: int = 0
    
    def __post_init__(self):
        if self.properties is None:
            self.properties = {}
        if self.dependencies is None:
            self.dependencies = []


class IdempotencyManager:
    """Manages idempotency checks and desired state enforcement."""
    
    def __init__(self):
        self.connection_manager = get_connection_manager()
        self.state_cache: Dict[str, Dict[str, Any]] = {}
        self.cache_ttl = 300  # 5 minutes
        self.cache_timestamps: Dict[str, float] = {}
    
    def _get_cache_key(self, resource_type: str, resource_id: str = None) -> str:
        """Generate cache key for resource."""
        if resource_id:
            return f"{resource_type}:{resource_id}"
        return resource_type
    
    def _is_cache_valid(self, cache_key: str) -> bool:
        """Check if cache entry is still valid."""
        if cache_key not in self.cache_timestamps:
            return False
        
        age = time.time() - self.cache_timestamps[cache_key]
        return age < self.cache_ttl
    
    def _update_cache(self, cache_key: str, data: Dict[str, Any]):
        """Update cache with new data."""
        self.state_cache[cache_key] = data
        self.cache_timestamps[cache_key] = time.time()
    
    def _get_cached_state(self, resource_type: str, resource_id: str = None) -> Optional[Dict[str, Any]]:
        """Get cached state if valid."""
        cache_key = self._get_cache_key(resource_type, resource_id)
        if self._is_cache_valid(cache_key):
            return self.state_cache.get(cache_key)
        return None
    
    def _normalize_state(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize state for comparison."""
        normalized = {}
        for key, value in state.items():
            # Convert to string for consistent comparison
            if isinstance(value, (int, float)):
                normalized[key] = str(value)
            elif isinstance(value, bool):
                normalized[key] = str(value).lower()
            elif isinstance(value, list):
                normalized[key] = sorted([str(item) for item in value])
            else:
                normalized[key] = str(value)
        return normalized
    
    def _compare_states(self, current: Dict[str, Any], desired: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Compare current and desired states."""
        current_norm = self._normalize_state(current)
        desired_norm = self._normalize_state(desired)
        
        differences = []
        
        # Check for missing properties in current state
        for key, desired_value in desired_norm.items():
            if key not in current_norm:
                differences.append(f"Missing property: {key}")
            elif current_norm[key] != desired_value:
                differences.append(f"Property '{key}' differs: current='{current_norm[key]}', desired='{desired_value}'")
        
        # Check for extra properties in current state (optional)
        for key in current_norm:
            if key not in desired_norm and not key.startswith('.'):  # Ignore internal properties
                differences.append(f"Extra property: {key}")
        
        return len(differences) == 0, differences
    
    def _execute_routeros_command(self, command: str) -> str:
        """Execute RouterOS command and return result."""
        try:
            with self.connection_manager.get_connection_context() as conn:
                stdin, stdout, stderr = conn.exec_command(command, timeout=30)
                result = stdout.read().decode('utf-8')
                error = stderr.read().decode('utf-8')
                
                if error:
                    app_logger.warning(f"RouterOS command warning: {error}")
                
                return result
        except Exception as e:
            app_logger.error(f"Failed to execute RouterOS command: {e}")
            raise
    
    def _parse_routeros_output(self, output: str) -> List[Dict[str, Any]]:
        """Parse RouterOS command output into structured data."""
        resources = []
        lines = output.strip().split('\n')
        
        current_resource = {}
        for line in lines:
            if line.startswith('Flags:'):
                # Start of new resource
                if current_resource:
                    resources.append(current_resource)
                current_resource = {}
            elif '=' in line and not line.startswith('#'):
                try:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Handle different value types
                    if value.lower() in ['true', 'yes']:
                        current_resource[key] = True
                    elif value.lower() in ['false', 'no']:
                        current_resource[key] = False
                    elif value.isdigit():
                        current_resource[key] = int(value)
                    elif value.replace('.', '').isdigit():
                        current_resource[key] = float(value)
                    else:
                        current_resource[key] = value
                except ValueError:
                    # Skip malformed lines
                    continue
        
        # Add the last resource
        if current_resource:
            resources.append(current_resource)
        
        return resources
    
    def check_firewall_rule_idempotency(self, desired_rule: Dict[str, Any]) -> IdempotencyResult:
        """Check if firewall rule matches desired state."""
        try:
            # Get current firewall rules
            output = self._execute_routeros_command('/ip firewall filter print detail')
            current_rules = self._parse_routeros_output(output)
            
            # Find matching rule
            matching_rule = None
            for rule in current_rules:
                if self._rule_matches_criteria(rule, desired_rule):
                    matching_rule = rule
                    break
            
            if not matching_rule:
                return IdempotencyResult(
                    state=IdempotencyState.MISSING,
                    desired_state=desired_rule,
                    action_required=True,
                    message="Firewall rule not found"
                )
            
            # Compare states
            matches, differences = self._compare_states(matching_rule, desired_rule)
            
            if matches:
                return IdempotencyResult(
                    state=IdempotencyState.MATCHES,
                    current_state=matching_rule,
                    desired_state=desired_rule,
                    action_required=False,
                    message="Firewall rule matches desired state"
                )
            else:
                return IdempotencyResult(
                    state=IdempotencyState.DIFFERS,
                    current_state=matching_rule,
                    desired_state=desired_rule,
                    differences=differences,
                    action_required=True,
                    message="Firewall rule differs from desired state"
                )
        
        except Exception as e:
            return IdempotencyResult(
                state=IdempotencyState.ERROR,
                message=f"Error checking firewall rule idempotency: {e}"
            )
    
    def _rule_matches_criteria(self, rule: Dict[str, Any], criteria: Dict[str, Any]) -> bool:
        """Check if a rule matches the given criteria."""
        # Match on key identifying properties
        key_properties = ['chain', 'src-address', 'dst-address', 'protocol', 'dst-port']
        
        for prop in key_properties:
            if prop in criteria and prop in rule:
                if rule[prop] != criteria[prop]:
                    return False
        
        return True
    
    def check_ip_address_idempotency(self, desired_address: Dict[str, Any]) -> IdempotencyResult:
        """Check if IP address matches desired state."""
        try:
            # Get current IP addresses
            output = self._execute_routeros_command('/ip address print detail')
            current_addresses = self._parse_routeros_output(output)
            
            # Find matching address
            matching_address = None
            for addr in current_addresses:
                if (addr.get('address') == desired_address.get('address') and 
                    addr.get('interface') == desired_address.get('interface')):
                    matching_address = addr
                    break
            
            if not matching_address:
                return IdempotencyResult(
                    state=IdempotencyState.MISSING,
                    desired_state=desired_address,
                    action_required=True,
                    message="IP address not found"
                )
            
            # Compare states
            matches, differences = self._compare_states(matching_address, desired_address)
            
            if matches:
                return IdempotencyResult(
                    state=IdempotencyState.MATCHES,
                    current_state=matching_address,
                    desired_state=desired_address,
                    action_required=False,
                    message="IP address matches desired state"
                )
            else:
                return IdempotencyResult(
                    state=IdempotencyState.DIFFERS,
                    current_state=matching_address,
                    desired_state=desired_address,
                    differences=differences,
                    action_required=True,
                    message="IP address differs from desired state"
                )
        
        except Exception as e:
            return IdempotencyResult(
                state=IdempotencyState.ERROR,
                message=f"Error checking IP address idempotency: {e}"
            )
    
    def check_dhcp_server_idempotency(self, desired_server: Dict[str, Any]) -> IdempotencyResult:
        """Check if DHCP server matches desired state."""
        try:
            # Get current DHCP servers
            output = self._execute_routeros_command('/ip dhcp-server print detail')
            current_servers = self._parse_routeros_output(output)
            
            # Find matching server
            matching_server = None
            for server in current_servers:
                if server.get('interface') == desired_server.get('interface'):
                    matching_server = server
                    break
            
            if not matching_server:
                return IdempotencyResult(
                    state=IdempotencyState.MISSING,
                    desired_state=desired_server,
                    action_required=True,
                    message="DHCP server not found"
                )
            
            # Compare states
            matches, differences = self._compare_states(matching_server, desired_server)
            
            if matches:
                return IdempotencyResult(
                    state=IdempotencyState.MATCHES,
                    current_state=matching_server,
                    desired_state=desired_server,
                    action_required=False,
                    message="DHCP server matches desired state"
                )
            else:
                return IdempotencyResult(
                    state=IdempotencyState.DIFFERS,
                    current_state=matching_server,
                    desired_state=desired_server,
                    differences=differences,
                    action_required=True,
                    message="DHCP server differs from desired state"
                )
        
        except Exception as e:
            return IdempotencyResult(
                state=IdempotencyState.ERROR,
                message=f"Error checking DHCP server idempotency: {e}"
            )
    
    def check_route_idempotency(self, desired_route: Dict[str, Any]) -> IdempotencyResult:
        """Check if route matches desired state."""
        try:
            # Get current routes
            output = self._execute_routeros_command('/ip route print detail')
            current_routes = self._parse_routeros_output(output)
            
            # Find matching route
            matching_route = None
            for route in current_routes:
                if (route.get('dst-address') == desired_route.get('dst-address') and
                    route.get('gateway') == desired_route.get('gateway')):
                    matching_route = route
                    break
            
            if not matching_route:
                return IdempotencyResult(
                    state=IdempotencyState.MISSING,
                    desired_state=desired_route,
                    action_required=True,
                    message="Route not found"
                )
            
            # Compare states
            matches, differences = self._compare_states(matching_route, desired_route)
            
            if matches:
                return IdempotencyResult(
                    state=IdempotencyState.MATCHES,
                    current_state=matching_route,
                    desired_state=desired_route,
                    action_required=False,
                    message="Route matches desired state"
                )
            else:
                return IdempotencyResult(
                    state=IdempotencyState.DIFFERS,
                    current_state=matching_route,
                    desired_state=desired_route,
                    differences=differences,
                    action_required=True,
                    message="Route differs from desired state"
                )
        
        except Exception as e:
            return IdempotencyResult(
                state=IdempotencyState.ERROR,
                message=f"Error checking route idempotency: {e}"
            )
    
    def ensure_desired_state(self, desired_states: List[DesiredState], 
                           max_retries: int = 3) -> Dict[str, IdempotencyResult]:
        """Ensure all desired states are achieved."""
        results = {}
        
        # Sort by priority (higher priority first)
        sorted_states = sorted(desired_states, key=lambda x: x.priority, reverse=True)
        
        for desired_state in sorted_states:
            result = self._ensure_single_state(desired_state, max_retries)
            results[desired_state.resource_type] = result
        
        return results
    
    def _ensure_single_state(self, desired_state: DesiredState, max_retries: int) -> IdempotencyResult:
        """Ensure a single desired state is achieved."""
        for attempt in range(max_retries):
            try:
                # Check current state
                result = self._check_resource_idempotency(desired_state)
                
                if result.state == IdempotencyState.MATCHES:
                    app_logger.info(f"Resource {desired_state.resource_type} already in desired state")
                    return result
                
                if result.state == IdempotencyState.MISSING:
                    app_logger.info(f"Creating resource {desired_state.resource_type}")
                    self._create_resource(desired_state)
                elif result.state == IdempotencyState.DIFFERS:
                    app_logger.info(f"Updating resource {desired_state.resource_type}")
                    self._update_resource(desired_state, result.current_state)
                
                # Wait a moment for changes to take effect
                time.sleep(1)
                
                # Verify the change
                verification_result = self._check_resource_idempotency(desired_state)
                if verification_result.state == IdempotencyState.MATCHES:
                    app_logger.info(f"Successfully ensured desired state for {desired_state.resource_type}")
                    return verification_result
                
                app_logger.warning(f"Attempt {attempt + 1} failed for {desired_state.resource_type}")
                
            except Exception as e:
                app_logger.error(f"Error ensuring state for {desired_state.resource_type}: {e}")
                if attempt == max_retries - 1:
                    return IdempotencyResult(
                        state=IdempotencyState.ERROR,
                        message=f"Failed to ensure desired state after {max_retries} attempts: {e}"
                    )
        
        return IdempotencyResult(
            state=IdempotencyState.ERROR,
            message=f"Failed to achieve desired state after {max_retries} attempts"
        )
    
    def _check_resource_idempotency(self, desired_state: DesiredState) -> IdempotencyResult:
        """Check idempotency for a specific resource type."""
        if desired_state.resource_type == "firewall_rule":
            return self.check_firewall_rule_idempotency(desired_state.properties)
        elif desired_state.resource_type == "ip_address":
            return self.check_ip_address_idempotency(desired_state.properties)
        elif desired_state.resource_type == "dhcp_server":
            return self.check_dhcp_server_idempotency(desired_state.properties)
        elif desired_state.resource_type == "route":
            return self.check_route_idempotency(desired_state.properties)
        else:
            return IdempotencyResult(
                state=IdempotencyState.ERROR,
                message=f"Unsupported resource type: {desired_state.resource_type}"
            )
    
    def _create_resource(self, desired_state: DesiredState):
        """Create a new resource."""
        if desired_state.resource_type == "firewall_rule":
            self._create_firewall_rule(desired_state.properties)
        elif desired_state.resource_type == "ip_address":
            self._create_ip_address(desired_state.properties)
        elif desired_state.resource_type == "dhcp_server":
            self._create_dhcp_server(desired_state.properties)
        elif desired_state.resource_type == "route":
            self._create_route(desired_state.properties)
    
    def _update_resource(self, desired_state: DesiredState, current_state: Dict[str, Any]):
        """Update an existing resource."""
        # For now, we'll remove and recreate
        # In a more sophisticated implementation, we'd update in place
        self._remove_resource(desired_state, current_state)
        self._create_resource(desired_state)
    
    def _remove_resource(self, desired_state: DesiredState, current_state: Dict[str, Any]):
        """Remove a resource."""
        if desired_state.resource_type == "firewall_rule":
            self._remove_firewall_rule(current_state)
        elif desired_state.resource_type == "ip_address":
            self._remove_ip_address(current_state)
        elif desired_state.resource_type == "dhcp_server":
            self._remove_dhcp_server(current_state)
        elif desired_state.resource_type == "route":
            self._remove_route(current_state)
    
    def _create_firewall_rule(self, properties: Dict[str, Any]):
        """Create a firewall rule."""
        cmd_parts = ['/ip', 'firewall', 'filter', 'add']
        for key, value in properties.items():
            if value is not None:
                cmd_parts.append(f'{key}={value}')
        
        command = ' '.join(cmd_parts)
        self._execute_routeros_command(command)
    
    def _remove_firewall_rule(self, current_state: Dict[str, Any]):
        """Remove a firewall rule."""
        if '.id' in current_state:
            command = f"/ip firewall filter remove .id={current_state['.id']}"
            self._execute_routeros_command(command)
    
    def _create_ip_address(self, properties: Dict[str, Any]):
        """Create an IP address."""
        cmd_parts = ['/ip', 'address', 'add']
        for key, value in properties.items():
            if value is not None:
                cmd_parts.append(f'{key}={value}')
        
        command = ' '.join(cmd_parts)
        self._execute_routeros_command(command)
    
    def _remove_ip_address(self, current_state: Dict[str, Any]):
        """Remove an IP address."""
        if '.id' in current_state:
            command = f"/ip address remove .id={current_state['.id']}"
            self._execute_routeros_command(command)
    
    def _create_dhcp_server(self, properties: Dict[str, Any]):
        """Create a DHCP server."""
        cmd_parts = ['/ip', 'dhcp-server', 'add']
        for key, value in properties.items():
            if value is not None:
                cmd_parts.append(f'{key}={value}')
        
        command = ' '.join(cmd_parts)
        self._execute_routeros_command(command)
    
    def _remove_dhcp_server(self, current_state: Dict[str, Any]):
        """Remove a DHCP server."""
        if '.id' in current_state:
            command = f"/ip dhcp-server remove .id={current_state['.id']}"
            self._execute_routeros_command(command)
    
    def _create_route(self, properties: Dict[str, Any]):
        """Create a route."""
        cmd_parts = ['/ip', 'route', 'add']
        for key, value in properties.items():
            if value is not None:
                cmd_parts.append(f'{key}={value}')
        
        command = ' '.join(cmd_parts)
        self._execute_routeros_command(command)
    
    def _remove_route(self, current_state: Dict[str, Any]):
        """Remove a route."""
        if '.id' in current_state:
            command = f"/ip route remove .id={current_state['.id']}"
            self._execute_routeros_command(command)


# Global idempotency manager instance
_idempotency_manager: Optional[IdempotencyManager] = None


def get_idempotency_manager() -> IdempotencyManager:
    """Get the global idempotency manager instance."""
    global _idempotency_manager
    if _idempotency_manager is None:
        _idempotency_manager = IdempotencyManager()
    return _idempotency_manager
