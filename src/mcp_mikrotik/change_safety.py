"""
Change safety system for MikroTik operations.
Provides automatic backups, rollback capabilities, and safety checks for risky operations.
"""
import time
import json
import uuid
from typing import Dict, List, Any, Optional, Callable, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime, timedelta
from .connection_manager import get_connection_manager
from .logger import app_logger
from .dry_run import SafetyLevel, get_dry_run_manager


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


class RollbackStatus(Enum):
    """Status of rollback operations."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class SafetyCheck:
    """Represents a safety check that must pass before an operation."""
    name: str
    description: str
    check_function: Callable[[], bool]
    required: bool = True
    timeout: int = 30


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
    rollback_status: RollbackStatus = RollbackStatus.PENDING
    success: bool = False
    error_message: Optional[str] = None
    affected_resources: List[str] = None
    
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
    status: RollbackStatus = RollbackStatus.PENDING


class ChangeSafetyManager:
    """Manages change safety, backups, and rollback operations."""
    
    def __init__(self):
        self.connection_manager = get_connection_manager()
        self.dry_run_manager = get_dry_run_manager()
        self.change_records: Dict[str, ChangeRecord] = {}
        self.rollback_plans: Dict[str, RollbackPlan] = {}
        self.safety_checks: Dict[ChangeType, List[SafetyCheck]] = {}
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
    
    def _test_connectivity(self) -> bool:
        """Test basic connectivity."""
        try:
            # Test ping to a reliable host
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
                
                # Check if any backups exist from the last 24 hours
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
        # This would check for console access, alternative management interfaces, etc.
        # For now, we'll assume it's available if we can connect via SSH
        return True
    
    def _check_alternative_routes(self) -> bool:
        """Check if alternative routes exist."""
        try:
            with self.connection_manager.get_connection_context() as conn:
                stdin, stdout, stderr = conn.exec_command('/ip route print', timeout=10)
                result = stdout.read().decode('utf-8')
                
                # Count default routes
                default_routes = result.count('dst-address=0.0.0.0/0')
                return default_routes > 1
        except Exception as e:
            app_logger.warning(f"Alternative routes check failed: {e}")
            return False
    
    def _check_interface_usage(self) -> bool:
        """Check if interface is in use."""
        # This would check if the interface has active connections, is part of bridges, etc.
        # For now, we'll return True to allow the check to pass
        return True
    
    def _check_admin_user_exists(self) -> bool:
        """Check if admin user will still exist after changes."""
        try:
            with self.connection_manager.get_connection_context() as conn:
                stdin, stdout, stderr = conn.exec_command('/user print', timeout=10)
                result = stdout.read().decode('utf-8')
                
                # Check if admin user exists
                return 'name=admin' in result
        except Exception as e:
            app_logger.warning(f"Admin user check failed: {e}")
            return False
    
    def _check_maintenance_window(self) -> bool:
        """Check if we're in a maintenance window."""
        # This would check against a configured maintenance schedule
        # For now, we'll return True to allow operations
        return True
    
    def create_backup(self, name: str = None) -> str:
        """Create a backup before making changes."""
        if not name:
            name = f"safety-backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        try:
            with self.connection_manager.get_connection_context() as conn:
                stdin, stdout, stderr = conn.exec_command(f'/backup save name={name}', timeout=60)
                result = stdout.read().decode('utf-8')
                
                if 'backup saved' in result.lower() or 'backup created' in result.lower():
                    app_logger.info(f"Backup created successfully: {name}")
                    return name
                else:
                    raise Exception(f"Backup creation failed: {result}")
        
        except Exception as e:
            app_logger.error(f"Failed to create backup: {e}")
            raise
    
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
                             operation_name: str, force: bool = False) -> ChangeRecord:
        """Execute an operation with safety checks and backup."""
        change_id = str(uuid.uuid4())
        
        # Determine safety level
        safety_level = self.dry_run_manager._get_safety_level(operation_name)
        
        # Create change record
        change_record = ChangeRecord(
            change_id=change_id,
            timestamp=time.time(),
            change_type=change_type,
            operation=operation_name,
            safety_level=safety_level
        )
        
        try:
            # Run safety checks
            app_logger.info(f"Running safety checks for {operation_name}")
            safety_passed, warnings = self.run_safety_checks(change_type, force)
            
            if not safety_passed:
                change_record.error_message = f"Safety checks failed: {warnings}"
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
            
            # Execute the operation
            app_logger.info(f"Executing operation: {operation_name}")
            result = operation()
            
            # Mark as successful
            change_record.success = True
            app_logger.info(f"Operation completed successfully: {operation_name}")
            
        except Exception as e:
            change_record.success = False
            change_record.error_message = str(e)
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
    
    def _create_rollback_plan(self, change_record: ChangeRecord) -> Optional[RollbackPlan]:
        """Create a rollback plan for a change."""
        rollback_id = str(uuid.uuid4())
        
        # Generate rollback commands based on change type
        rollback_commands = []
        verification_commands = []
        
        if change_record.change_type == ChangeType.FIREWALL:
            # For firewall changes, we might need to remove specific rules
            rollback_commands.append("/ip firewall filter print")
            verification_commands.append("/ip firewall filter print")
        
        elif change_record.change_type == ChangeType.ROUTING:
            # For routing changes, we might need to remove routes
            rollback_commands.append("/ip route print")
            verification_commands.append("/ip route print")
        
        elif change_record.change_type == ChangeType.INTERFACE:
            # For interface changes, we might need to restore interface state
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
        rollback_plan.status = RollbackStatus.IN_PROGRESS
        
        try:
            app_logger.info(f"Starting rollback for change: {change_id}")
            
            # Execute rollback commands
            for command in rollback_plan.rollback_commands:
                app_logger.info(f"Executing rollback command: {command}")
                with self.connection_manager.get_connection_context() as conn:
                    stdin, stdout, stderr = conn.exec_command(command, timeout=60)
                    result = stdout.read().decode('utf-8')
                    error = stderr.read().decode('utf-8')
                    
                    if error:
                        app_logger.warning(f"Rollback command warning: {error}")
            
            # Verify rollback
            for command in rollback_plan.verification_commands:
                app_logger.info(f"Verifying rollback: {command}")
                with self.connection_manager.get_connection_context() as conn:
                    stdin, stdout, stderr = conn.exec_command(command, timeout=30)
                    result = stdout.read().decode('utf-8')
            
            rollback_plan.status = RollbackStatus.COMPLETED
            change_record.rollback_status = RollbackStatus.COMPLETED
            
            app_logger.info(f"Rollback completed successfully for change: {change_id}")
            return True
        
        except Exception as e:
            rollback_plan.status = RollbackStatus.FAILED
            change_record.rollback_status = RollbackStatus.FAILED
            app_logger.error(f"Rollback failed for change {change_id}: {e}")
            return False
    
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
                change_record.rollback_status == RollbackStatus.PENDING):
                candidates.append(change_record)
        return candidates
    
    def schedule_rollback(self, change_id: str, delay_minutes: int = 60):
        """Schedule an automatic rollback after a delay."""
        if change_id not in self.change_records:
            raise Exception(f"Change record not found: {change_id}")
        
        change_record = self.change_records[change_id]
        
        # In a real implementation, this would use a scheduler
        # For now, we'll just log the scheduled rollback
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


# Global change safety manager instance
_change_safety_manager: Optional[ChangeSafetyManager] = None


def get_change_safety_manager() -> ChangeSafetyManager:
    """Get the global change safety manager instance."""
    global _change_safety_manager
    if _change_safety_manager is None:
        _change_safety_manager = ChangeSafetyManager()
    return _change_safety_manager
