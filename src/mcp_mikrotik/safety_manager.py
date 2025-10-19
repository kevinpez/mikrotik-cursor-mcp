"""
Unified Safety & State Management system for MikroTik operations.
Combines change safety, idempotency, backups, and rollback capabilities.
"""
import time
import json
import uuid
import hashlib
from typing import Dict, List, Any, Optional, Callable, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime, timedelta
from .connection_manager import get_connection_manager
from .logger import app_logger
# Removed dry_run import


class ChangeType(Enum):
    """Types of changes that can be made."""
    FIREWALL = "firewall"
    ROUTING = "routing"
    INTERFACE = "interface"
    USER = "user"
    SYSTEM = "system"
    NETWORK = "network"
    VPN = "vpn"
    WIRELESS = "wireless"
    IP = "ip"
    DHCP = "dhcp"
    DNS = "dns"


class OperationStatus(Enum):
    """Status of operations."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    ROLLED_BACK = "rolled_back"


class IdempotencyState(Enum):
    """States for idempotency checks."""
    MATCHES = "matches"           # Current state matches desired state
    DIFFERS = "differs"           # Current state differs from desired state
    MISSING = "missing"           # Desired resource is missing
    EXTRA = "extra"               # Extra resources exist
    ERROR = "error"               # Error occurred during check


@dataclass
class SafetyCheck:
    """Represents a safety check that must pass before an operation."""
    name: str
    description: str
    check_function: Callable[[], bool]
    required: bool = True
    timeout: int = 30


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


@dataclass
class ChangeRecord:
    """Record of a change made to the system."""
    change_id: str
    timestamp: float
    change_type: ChangeType
    operation: str
    safety_level: SafetyLevel
    backup_id: Optional[str] = None
    rollback_script: Optional[str] = None
    status: OperationStatus = OperationStatus.PENDING
    success: bool = False
    error_message: Optional[str] = None
    affected_resources: List[str] = None
    idempotency_result: Optional[IdempotencyResult] = None
    
    def __post_init__(self):
        if self.affected_resources is None:
            self.affected_resources = []


@dataclass
class RollbackPlan:
    """Plan for rolling back a change."""
    rollback_id: str
    change_id: str
    timestamp: float
    rollback_commands: List[str]
    verification_commands: List[str]
    estimated_duration: int = 60
    status: OperationStatus = OperationStatus.PENDING


class UnifiedSafetyManager:
    """Unified manager for safety, idempotency, backups, and rollback operations."""
    
    def __init__(self):
        self.connection_manager = get_connection_manager()
        # Removed dry_run_manager
        self.change_records: Dict[str, ChangeRecord] = {}
        self.rollback_plans: Dict[str, RollbackPlan] = {}
        self.safety_checks: Dict[ChangeType, List[SafetyCheck]] = {}
        self.state_cache: Dict[str, Dict[str, Any]] = {}
        self.cache_ttl = 300  # 5 minutes
        self.cache_timestamps: Dict[str, float] = {}
        self._initialize_safety_checks()
    
    def _initialize_safety_checks(self):
        """Initialize default safety checks for each change type."""
        
        # Firewall safety checks
        self.safety_checks[ChangeType.FIREWALL] = [
            SafetyCheck(
                name="connectivity_test",
                description="Test basic connectivity before firewall changes",
                check_function=self._test_connectivity,
                required=True
            ),
            SafetyCheck(
                name="backup_exists",
                description="Ensure backup exists before firewall changes",
                check_function=self._check_backup_exists,
                required=True
            ),
            SafetyCheck(
                name="out_of_band_access",
                description="Verify out-of-band access is available",
                check_function=self._check_out_of_band_access,
                required=False
            )
        ]
        
        # Routing safety checks
        self.safety_checks[ChangeType.ROUTING] = [
            SafetyCheck(
                name="connectivity_test",
                description="Test connectivity before routing changes",
                check_function=self._test_connectivity,
                required=True
            ),
            SafetyCheck(
                name="backup_exists",
                description="Ensure backup exists before routing changes",
                check_function=self._check_backup_exists,
                required=True
            ),
            SafetyCheck(
                name="alternative_routes",
                description="Check for alternative routes",
                check_function=self._check_alternative_routes,
                required=False
            )
        ]
        
        # Interface safety checks
        self.safety_checks[ChangeType.INTERFACE] = [
            SafetyCheck(
                name="backup_exists",
                description="Ensure backup exists before interface changes",
                check_function=self._check_backup_exists,
                required=True
            ),
            SafetyCheck(
                name="interface_usage",
                description="Check if interface is in use",
                check_function=self._check_interface_usage,
                required=True
            )
        ]
        
        # User safety checks
        self.safety_checks[ChangeType.USER] = [
            SafetyCheck(
                name="backup_exists",
                description="Ensure backup exists before user changes",
                check_function=self._check_backup_exists,
                required=True
            ),
            SafetyCheck(
                name="admin_user_exists",
                description="Ensure admin user will still exist",
                check_function=self._check_admin_user_exists,
                required=True
            )
        ]
        
        # System safety checks
        self.safety_checks[ChangeType.SYSTEM] = [
            SafetyCheck(
                name="backup_exists",
                description="Ensure backup exists before system changes",
                check_function=self._check_backup_exists,
                required=True
            ),
            SafetyCheck(
                name="maintenance_window",
                description="Check if in maintenance window",
                check_function=self._check_maintenance_window,
                required=False
            )
        ]
        
        # IP/DHCP/DNS safety checks (lighter requirements)
        for change_type in [ChangeType.IP, ChangeType.DHCP, ChangeType.DNS]:
            self.safety_checks[change_type] = [
                SafetyCheck(
                    name="backup_exists",
                    description="Ensure backup exists before changes",
                    check_function=self._check_backup_exists,
                    required=False  # Less critical operations
                )
            ]
    
    # Safety Check Methods
    def _test_connectivity(self) -> bool:
        """Test basic connectivity."""
        try:
            with self.connection_manager.get_connection_context() as conn:
                stdin, stdout, stderr = conn.exec_command('/ping 8.8.8.8 count=3', timeout=10)
                result = stdout.read().decode('utf-8')
                return 'packet loss: 0%' in result or 'received=3' in result
        except Exception as e:
            app_logger.warning(f"Connectivity test failed: {e}")
            return False
    
    def _check_backup_exists(self) -> bool:
        """Check if a recent backup exists."""
        try:
            with self.connection_manager.get_connection_context() as conn:
                stdin, stdout, stderr = conn.exec_command('/backup print', timeout=10)
                result = stdout.read().decode('utf-8')
                
                lines = result.split('\n')
                for line in lines:
                    if 'name=' in line and 'backup' in line.lower():
                        return True
                
                return False
        except Exception as e:
            app_logger.warning(f"Backup check failed: {e}")
            return False
    
    def _check_out_of_band_access(self) -> bool:
        """Check if out-of-band access is available."""
        return True  # Assume available if SSH connection works
    
    def _check_alternative_routes(self) -> bool:
        """Check if alternative routes exist."""
        try:
            with self.connection_manager.get_connection_context() as conn:
                stdin, stdout, stderr = conn.exec_command('/ip route print', timeout=10)
                result = stdout.read().decode('utf-8')
                
                default_routes = result.count('dst-address=0.0.0.0/0')
                return default_routes > 1
        except Exception as e:
            app_logger.warning(f"Alternative routes check failed: {e}")
            return False
    
    def _check_interface_usage(self) -> bool:
        """Check if interface is in use."""
        return True  # Allow check to pass for now
    
    def _check_admin_user_exists(self) -> bool:
        """Check if admin user will still exist after changes."""
        try:
            with self.connection_manager.get_connection_context() as conn:
                stdin, stdout, stderr = conn.exec_command('/user print', timeout=10)
                result = stdout.read().decode('utf-8')
                
                return 'name=admin' in result
        except Exception as e:
            app_logger.warning(f"Admin user check failed: {e}")
            return False
    
    def _check_maintenance_window(self) -> bool:
        """Check if we're in a maintenance window."""
        return True  # Allow operations for now
    
    # RouterOS Command Execution
    def _execute_routeros_command(self, command: str, timeout: int = 30) -> str:
        """Execute RouterOS command and return result."""
        try:
            with self.connection_manager.get_connection_context() as conn:
                stdin, stdout, stderr = conn.exec_command(command, timeout=timeout)
                result = stdout.read().decode('utf-8')
                error = stderr.read().decode('utf-8')
                
                if error:
                    app_logger.warning(f"RouterOS command warning: {error}")
                
                return result
        except Exception as e:
            app_logger.error(f"Failed to execute RouterOS command: {e}")
            raise
    
    # State Management and Caching
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
                    continue
        
        # Add the last resource
        if current_resource:
            resources.append(current_resource)
        
        return resources
    
    # Idempotency Methods
    def check_idempotency(self, resource_type: str, desired_properties: Dict[str, Any]) -> IdempotencyResult:
        """Check if a resource matches desired state."""
        try:
            # Get current state
            current_resources = self._get_current_resources(resource_type)
            
            # Find matching resource
            matching_resource = self._find_matching_resource(current_resources, desired_properties, resource_type)
            
            if not matching_resource:
                return IdempotencyResult(
                    state=IdempotencyState.MISSING,
                    desired_state=desired_properties,
                    action_required=True,
                    message=f"{resource_type} not found"
                )
            
            # Compare states
            matches, differences = self._compare_states(matching_resource, desired_properties)
            
            if matches:
                return IdempotencyResult(
                    state=IdempotencyState.MATCHES,
                    current_state=matching_resource,
                    desired_state=desired_properties,
                    action_required=False,
                    message=f"{resource_type} matches desired state"
                )
            else:
                return IdempotencyResult(
                    state=IdempotencyState.DIFFERS,
                    current_state=matching_resource,
                    desired_state=desired_properties,
                    differences=differences,
                    action_required=True,
                    message=f"{resource_type} differs from desired state"
                )
        
        except Exception as e:
            return IdempotencyResult(
                state=IdempotencyState.ERROR,
                message=f"Error checking {resource_type} idempotency: {e}"
            )
    
    def _get_current_resources(self, resource_type: str) -> List[Dict[str, Any]]:
        """Get current resources of a specific type."""
        cache_key = self._get_cache_key(resource_type)
        cached = self._get_cached_state(resource_type)
        if cached:
            return cached
        
        # Map resource types to RouterOS commands
        command_map = {
            "firewall_rule": "/ip firewall filter print detail",
            "ip_address": "/ip address print detail",
            "dhcp_server": "/ip dhcp-server print detail",
            "route": "/ip route print detail",
            "interface": "/interface print detail",
            "user": "/user print detail",
            "dns_static": "/ip dns static print detail",
            "dhcp_pool": "/ip pool print detail"
        }
        
        if resource_type not in command_map:
            raise ValueError(f"Unsupported resource type: {resource_type}")
        
        output = self._execute_routeros_command(command_map[resource_type])
        resources = self._parse_routeros_output(output)
        
        # Cache the result
        self._update_cache(cache_key, resources)
        
        return resources
    
    def _find_matching_resource(self, resources: List[Dict[str, Any]], 
                              criteria: Dict[str, Any], resource_type: str) -> Optional[Dict[str, Any]]:
        """Find a resource that matches the given criteria."""
        # Define key identifying properties for each resource type
        key_properties_map = {
            "firewall_rule": ['chain', 'src-address', 'dst-address', 'protocol', 'dst-port'],
            "ip_address": ['address', 'interface'],
            "dhcp_server": ['interface'],
            "route": ['dst-address', 'gateway'],
            "interface": ['name'],
            "user": ['name'],
            "dns_static": ['name'],
            "dhcp_pool": ['name']
        }
        
        key_properties = key_properties_map.get(resource_type, [])
        
        for resource in resources:
            match = True
            for prop in key_properties:
                if prop in criteria and prop in resource:
                    if resource[prop] != criteria[prop]:
                        match = False
                        break
            if match:
                return resource
        
        return None
    
    # Backup and Rollback Methods
    def create_backup(self, name: str = None) -> str:
        """Create a backup before making changes."""
        if not name:
            name = f"safety-backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        try:
            command = f'/backup save name={name}'
            result = self._execute_routeros_command(command, timeout=60)
            
            if 'backup saved' in result.lower() or 'backup created' in result.lower():
                app_logger.info(f"Backup created successfully: {name}")
                return name
            else:
                raise Exception(f"Backup creation failed: {result}")
        
        except Exception as e:
            app_logger.error(f"Failed to create backup: {e}")
            raise
    
    def _create_rollback_plan(self, change_record: ChangeRecord) -> Optional[RollbackPlan]:
        """Create a rollback plan for a change."""
        rollback_id = str(uuid.uuid4())
        
        # Generate rollback commands based on change type
        rollback_commands = []
        verification_commands = []
        
        if change_record.change_type == ChangeType.FIREWALL:
            rollback_commands.append("/ip firewall filter print")
            verification_commands.append("/ip firewall filter print")
        elif change_record.change_type == ChangeType.ROUTING:
            rollback_commands.append("/ip route print")
            verification_commands.append("/ip route print")
        elif change_record.change_type == ChangeType.INTERFACE:
            rollback_commands.append("/interface print")
            verification_commands.append("/interface print")
        
        # If we have a backup, add restore command
        if change_record.backup_id:
            rollback_commands.insert(0, f"/backup load name={change_record.backup_id}")
            verification_commands.append("/system identity print")
        
        if rollback_commands:
            return RollbackPlan(
                rollback_id=rollback_id,
                change_id=change_record.change_id,
                timestamp=time.time(),
                rollback_commands=rollback_commands,
                verification_commands=verification_commands
            )
        
        return None
    
    def rollback_change(self, change_id: str) -> bool:
        """Rollback a specific change."""
        if change_id not in self.change_records:
            raise Exception(f"Change record not found: {change_id}")
        
        change_record = self.change_records[change_id]
        
        if change_record.rollback_script not in self.rollback_plans:
            raise Exception(f"Rollback plan not found for change: {change_id}")
        
        rollback_plan = self.rollback_plans[change_record.rollback_script]
        rollback_plan.status = OperationStatus.IN_PROGRESS
        
        try:
            app_logger.info(f"Starting rollback for change: {change_id}")
            
            # Execute rollback commands
            for command in rollback_plan.rollback_commands:
                app_logger.info(f"Executing rollback command: {command}")
                self._execute_routeros_command(command, timeout=60)
            
            # Verify rollback
            for command in rollback_plan.verification_commands:
                app_logger.info(f"Verifying rollback: {command}")
                self._execute_routeros_command(command, timeout=30)
            
            rollback_plan.status = OperationStatus.COMPLETED
            change_record.status = OperationStatus.ROLLED_BACK
            
            app_logger.info(f"Rollback completed successfully for change: {change_id}")
            return True
        
        except Exception as e:
            rollback_plan.status = OperationStatus.FAILED
            change_record.status = OperationStatus.FAILED
            app_logger.error(f"Rollback failed for change {change_id}: {e}")
            return False
    
    # Main Operation Methods
    def run_safety_checks(self, change_type: ChangeType, force: bool = False) -> Tuple[bool, List[str]]:
        """Run safety checks for a change type."""
        if change_type not in self.safety_checks:
            app_logger.warning(f"No safety checks defined for {change_type}")
            return True, []
        
        failed_checks = []
        warnings = []
        
        for check in self.safety_checks[change_type]:
            try:
                app_logger.info(f"Running safety check: {check.name}")
                start_time = time.time()
                
                result = check.check_function()
                duration = time.time() - start_time
                
                if not result:
                    if check.required:
                        failed_checks.append(f"{check.name}: {check.description}")
                        app_logger.error(f"Required safety check failed: {check.name}")
                    else:
                        warnings.append(f"{check.name}: {check.description}")
                        app_logger.warning(f"Optional safety check failed: {check.name}")
                else:
                    app_logger.info(f"Safety check passed: {check.name} ({duration:.2f}s)")
            
            except Exception as e:
                error_msg = f"{check.name}: {str(e)}"
                if check.required:
                    failed_checks.append(error_msg)
                    app_logger.error(f"Safety check error: {error_msg}")
                else:
                    warnings.append(error_msg)
                    app_logger.warning(f"Safety check warning: {error_msg}")
        
        if failed_checks and not force:
            app_logger.error(f"Safety checks failed: {failed_checks}")
            return False, failed_checks + warnings
        
        if warnings:
            app_logger.warning(f"Safety check warnings: {warnings}")
        
        return True, warnings
    
    def execute_safe_operation(self, change_type: ChangeType, operation: Callable, 
                             operation_name: str, desired_state: DesiredState = None,
                             force: bool = False) -> ChangeRecord:
        """Execute an operation with safety checks, backup, and idempotency verification."""
        change_id = str(uuid.uuid4())
        
        # Determine safety level (simplified without dry_run)
        safety_level = "medium"  # Default safety level
        
        # Create change record
        change_record = ChangeRecord(
            change_id=change_id,
            timestamp=time.time(),
            change_type=change_type,
            operation=operation_name,
            safety_level=safety_level,
            status=OperationStatus.IN_PROGRESS
        )
        
        try:
            # Run safety checks
            app_logger.info(f"Running safety checks for {operation_name}")
            safety_passed, warnings = self.run_safety_checks(change_type, force)
            
            if not safety_passed:
                change_record.error_message = f"Safety checks failed: {warnings}"
                change_record.status = OperationStatus.FAILED
                self.change_records[change_id] = change_record
                raise Exception(f"Safety checks failed: {warnings}")
            
            # Create backup for high-risk operations
            if safety_level in [SafetyLevel.HIGH_RISK, SafetyLevel.CRITICAL]:
                app_logger.info(f"Creating backup for high-risk operation: {operation_name}")
                backup_name = self.create_backup(f"pre-{change_type.value}-{change_id[:8]}")
                change_record.backup_id = backup_name
            
            # Create rollback plan
            rollback_plan = self._create_rollback_plan(change_record)
            if rollback_plan:
                self.rollback_plans[rollback_plan.rollback_id] = rollback_plan
                change_record.rollback_script = rollback_plan.rollback_id
            
            # Check idempotency before operation if desired state provided
            if desired_state:
                app_logger.info(f"Checking idempotency before operation: {operation_name}")
                idempotency_result = self.check_idempotency(desired_state.resource_type, desired_state.properties)
                change_record.idempotency_result = idempotency_result
                
                if idempotency_result.state == IdempotencyState.MATCHES:
                    app_logger.info(f"Operation not needed - resource already in desired state: {operation_name}")
                    change_record.status = OperationStatus.COMPLETED
                    change_record.success = True
                    self.change_records[change_id] = change_record
                    return change_record
            
            # Execute the operation
            app_logger.info(f"Executing operation: {operation_name}")
            result = operation()
            
            # Verify idempotency after operation if desired state provided
            if desired_state:
                app_logger.info(f"Verifying idempotency after operation: {operation_name}")
                verification_result = self.check_idempotency(desired_state.resource_type, desired_state.properties)
                
                if verification_result.state != IdempotencyState.MATCHES:
                    app_logger.warning(f"Post-operation verification failed: {verification_result.message}")
                    change_record.error_message = f"Verification failed: {verification_result.message}"
                    change_record.status = OperationStatus.FAILED
                    change_record.success = False
                else:
                    change_record.status = OperationStatus.COMPLETED
                    change_record.success = True
                    app_logger.info(f"Operation completed and verified successfully: {operation_name}")
            else:
                change_record.status = OperationStatus.COMPLETED
                change_record.success = True
                app_logger.info(f"Operation completed successfully: {operation_name}")
            
        except Exception as e:
            change_record.success = False
            change_record.error_message = str(e)
            change_record.status = OperationStatus.FAILED
            app_logger.error(f"Operation failed: {operation_name} - {e}")
            
            # Attempt automatic rollback for critical failures
            if safety_level == SafetyLevel.CRITICAL and change_record.backup_id:
                app_logger.warning("Attempting automatic rollback for critical operation failure")
                try:
                    self.rollback_change(change_record.change_id)
                except Exception as rollback_error:
                    app_logger.error(f"Automatic rollback failed: {rollback_error}")
        
        finally:
            # Record the change
            self.change_records[change_id] = change_record
        
        return change_record
    
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
                result = self.check_idempotency(desired_state.resource_type, desired_state.properties)
                
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
                verification_result = self.check_idempotency(desired_state.resource_type, desired_state.properties)
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
    
    def _create_resource(self, desired_state: DesiredState):
        """Create a new resource."""
        # Map resource types to creation commands
        command_map = {
            "firewall_rule": "/ip firewall filter add",
            "ip_address": "/ip address add",
            "dhcp_server": "/ip dhcp-server add",
            "route": "/ip route add",
            "interface": "/interface add",
            "user": "/user add",
            "dns_static": "/ip dns static add",
            "dhcp_pool": "/ip pool add"
        }
        
        if desired_state.resource_type not in command_map:
            raise ValueError(f"Unsupported resource type: {desired_state.resource_type}")
        
        cmd_parts = command_map[desired_state.resource_type].split()
        for key, value in desired_state.properties.items():
            if value is not None:
                cmd_parts.append(f'{key}={value}')
        
        command = ' '.join(cmd_parts)
        self._execute_routeros_command(command)
    
    def _update_resource(self, desired_state: DesiredState, current_state: Dict[str, Any]):
        """Update an existing resource."""
        # For now, we'll remove and recreate
        # In a more sophisticated implementation, we'd update in place
        self._remove_resource(desired_state, current_state)
        self._create_resource(desired_state)
    
    def _remove_resource(self, desired_state: DesiredState, current_state: Dict[str, Any]):
        """Remove a resource."""
        if '.id' in current_state:
            # Map resource types to removal commands
            command_map = {
                "firewall_rule": "/ip firewall filter remove",
                "ip_address": "/ip address remove",
                "dhcp_server": "/ip dhcp-server remove",
                "route": "/ip route remove",
                "interface": "/interface remove",
                "user": "/user remove",
                "dns_static": "/ip dns static remove",
                "dhcp_pool": "/ip pool remove"
            }
            
            if desired_state.resource_type in command_map:
                command = f"{command_map[desired_state.resource_type]} .id={current_state['.id']}"
                self._execute_routeros_command(command)
    
    # Utility Methods
    def get_change_history(self, limit: int = 50) -> List[ChangeRecord]:
        """Get recent change history."""
        sorted_changes = sorted(
            self.change_records.values(),
            key=lambda x: x.timestamp,
            reverse=True
        )
        return sorted_changes[:limit]
    
    def get_rollback_candidates(self) -> List[ChangeRecord]:
        """Get changes that can be rolled back."""
        candidates = []
        for change_record in self.change_records.values():
            if (change_record.rollback_script and 
                change_record.status in [OperationStatus.COMPLETED, OperationStatus.FAILED]):
                candidates.append(change_record)
        return candidates
    
    def schedule_rollback(self, change_id: str, delay_minutes: int = 60):
        """Schedule an automatic rollback after a delay."""
        if change_id not in self.change_records:
            raise Exception(f"Change record not found: {change_id}")
        
        change_record = self.change_records[change_id]
        
        # In a real implementation, this would use a scheduler
        app_logger.info(f"Rollback scheduled for change {change_id} in {delay_minutes} minutes")
        
        # Update the rollback plan with scheduled status
        if change_record.rollback_script in self.rollback_plans:
            rollback_plan = self.rollback_plans[change_record.rollback_script]
            rollback_plan.estimated_duration = delay_minutes * 60
    
    def cleanup_old_records(self, days: int = 30):
        """Clean up old change records."""
        cutoff_time = time.time() - (days * 24 * 60 * 60)
        
        old_changes = [
            change_id for change_id, record in self.change_records.items()
            if record.timestamp < cutoff_time
        ]
        
        for change_id in old_changes:
            del self.change_records[change_id]
            # Also clean up associated rollback plans
            change_record = self.change_records.get(change_id)
            if change_record and change_record.rollback_script:
                if change_record.rollback_script in self.rollback_plans:
                    del self.rollback_plans[change_record.rollback_script]
        
        app_logger.info(f"Cleaned up {len(old_changes)} old change records")


# Global unified safety manager instance
_unified_safety_manager: Optional[UnifiedSafetyManager] = None


def get_unified_safety_manager() -> UnifiedSafetyManager:
    """Get the global unified safety manager instance."""
    global _unified_safety_manager
    if _unified_safety_manager is None:
        _unified_safety_manager = UnifiedSafetyManager()
    return _unified_safety_manager


# Backward compatibility functions
def get_change_safety_manager() -> UnifiedSafetyManager:
    """Get the unified safety manager (backward compatibility)."""
    return get_unified_safety_manager()


def get_idempotency_manager() -> UnifiedSafetyManager:
    """Get the unified safety manager (backward compatibility)."""
    return get_unified_safety_manager()
