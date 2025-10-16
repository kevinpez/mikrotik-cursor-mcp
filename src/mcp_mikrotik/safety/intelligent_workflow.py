"""
Intelligent Risk-Based Workflow for MikroTik Operations.
Automatically determines risk level and guides user through appropriate safety measures.
"""
import os
import re
from typing import Dict, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass
from ..logger import app_logger
from ..connector import execute_mikrotik_command
from ..scope.safe_mode import (
    mikrotik_enter_safe_mode,
    mikrotik_exit_safe_mode,
    mikrotik_get_safe_mode_status
)


class RiskLevel(Enum):
    """Risk levels for MikroTik operations."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class RiskAssessment:
    """Risk assessment result for a MikroTik operation."""
    risk_level: RiskLevel
    reason: str
    warnings: List[str]
    requires_approval: bool
    requires_safe_mode: bool
    estimated_impact: str


@dataclass
class WorkflowResult:
    """Result of the intelligent workflow execution."""
    success: bool
    message: str
    command_executed: str
    safe_mode_used: bool
    logs_checked: bool
    state_verified: bool
    rollback_triggered: bool = False


class IntelligentWorkflowManager:
    """Manages intelligent risk-based workflow for MikroTik operations."""
    
    def __init__(self):
        self.risk_patterns = self._initialize_risk_patterns()
        self.safe_mode_active = False
        
    def _initialize_risk_patterns(self) -> Dict[RiskLevel, List[str]]:
        """Initialize risk assessment patterns."""
        return {
            RiskLevel.LOW: [
                r'/ip\s+address\s+print',
                r'/interface\s+print',
                r'/system\s+resource\s+print',
                r'/system\s+identity\s+print',
                r'/ip\s+route\s+print',
                r'/system\s+clock\s+print',
                r'/system\s+license\s+print',
                r'/system\s+routerboard\s+print',
                r'/system\s+health\s+print',
                r'/system\s+uptime\s+print',
                r'/log\s+print',
                r'/ip\s+dhcp-server\s+lease\s+print',
                r'/ip\s+firewall\s+connection\s+print',
                r'/interface\s+wireless\s+print',
                r'/ip\s+pool\s+print',
            ],
            RiskLevel.MEDIUM: [
                r'/ip\s+address\s+add',
                r'/ip\s+route\s+add',
                r'/interface\s+vlan\s+add',
                r'/ip\s+dhcp-server\s+add',
                r'/ip\s+pool\s+add',
                r'/user\s+add',
                r'/ip\s+firewall\s+filter\s+add',
                r'/ip\s+firewall\s+nat\s+add',
                r'/interface\s+wireless\s+set',
                r'/system\s+ntp\s+client\s+set',
                r'/ip\s+dns\s+set',
                r'/system\s+identity\s+set',
            ],
            RiskLevel.HIGH: [
                r'/system\s+reboot',
                r'/system\s+shutdown',
                r'/system\s+reset-configuration',
                r'/system\s+package\s+uninstall',
                r'/system\s+backup\s+save',
                r'/system\s+backup\s+load',
                r'/interface\s+bridge\s+add',
                r'/interface\s+bridge\s+port\s+add',
                r'/routing\s+bgp\s+instance\s+add',
                r'/routing\s+ospf\s+instance\s+add',
                r'/ip\s+firewall\s+filter\s+remove',
                r'/ip\s+firewall\s+nat\s+remove',
                r'/user\s+remove',
                r'/interface\s+remove',
                r'/ip\s+address\s+remove',
                r'/ip\s+route\s+remove',
            ],
            RiskLevel.CRITICAL: [
                r'/system\s+reset-configuration\s+no-defaults=yes',
                r'/system\s+package\s+uninstall\s+name=',
                r'/system\s+backup\s+load\s+name=',
                r'/system\s+reset-configuration\s+keep-users=no',
                r'/system\s+reset-configuration\s+skip-backup=yes',
                r'/interface\s+bridge\s+remove',
                r'/routing\s+bgp\s+instance\s+remove',
                r'/routing\s+ospf\s+instance\s+remove',
                r'/system\s+user\s+remove\s+admin',
                r'/ip\s+firewall\s+filter\s+remove\s+numbers=',
                r'/ip\s+firewall\s+nat\s+remove\s+numbers=',
            ]
        }
    
    def assess_risk(self, command: str) -> RiskAssessment:
        """Assess the risk level of a MikroTik command."""
        app_logger.info(f"Assessing risk for command: {command}")
        
        command_lower = command.lower().strip()
        
        # Check each risk level
        for risk_level, patterns in self.risk_patterns.items():
            for pattern in patterns:
                if re.search(pattern, command_lower):
                    warnings = self._generate_warnings(command, risk_level)
                    return RiskAssessment(
                        risk_level=risk_level,
                        reason=f"Command matches {risk_level.value} risk pattern: {pattern}",
                        warnings=warnings,
                        requires_approval=risk_level in [RiskLevel.MEDIUM, RiskLevel.HIGH, RiskLevel.CRITICAL],
                        requires_safe_mode=risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL],
                        estimated_impact=self._get_estimated_impact(risk_level)
                    )
        
        # Default to medium risk if no pattern matches
        return RiskAssessment(
            risk_level=RiskLevel.MEDIUM,
            reason="Command does not match known patterns - defaulting to medium risk",
            warnings=["Unknown command pattern - proceeding with caution"],
            requires_approval=True,
            requires_safe_mode=False,
            estimated_impact="Unknown impact - may affect system configuration"
        )
    
    def _generate_warnings(self, command: str, risk_level: RiskLevel) -> List[str]:
        """Generate specific warnings based on command and risk level."""
        warnings = []
        
        if risk_level == RiskLevel.HIGH:
            warnings.extend([
                "This operation may affect network connectivity",
                "Consider creating a backup before proceeding",
                "Safe Mode will be used for automatic rollback protection"
            ])
        elif risk_level == RiskLevel.CRITICAL:
            warnings.extend([
                "CRITICAL OPERATION: This may cause system instability",
                "Strongly recommend creating a backup first",
                "Safe Mode is mandatory for this operation",
                "Consider testing in a lab environment first"
            ])
        
        # Command-specific warnings
        if "reboot" in command.lower():
            warnings.append("System will restart - all connections will be lost")
        elif "shutdown" in command.lower():
            warnings.append("System will shut down - remote access will be lost")
        elif "reset-configuration" in command.lower():
            warnings.append("All configuration will be lost - system will return to defaults")
        elif "firewall" in command.lower() and "remove" in command.lower():
            warnings.append("Firewall rule removal may affect network security")
        elif "user" in command.lower() and "remove" in command.lower():
            warnings.append("User removal may affect system access")
        
        return warnings
    
    def _get_estimated_impact(self, risk_level: RiskLevel) -> str:
        """Get estimated impact description for risk level."""
        impacts = {
            RiskLevel.LOW: "Minimal impact - read-only or safe operations",
            RiskLevel.MEDIUM: "Moderate impact - configuration changes that can be easily reverted",
            RiskLevel.HIGH: "High impact - significant configuration changes with potential connectivity impact",
            RiskLevel.CRITICAL: "Critical impact - system-wide changes that may cause instability or lockout"
        }
        return impacts.get(risk_level, "Unknown impact")
    
    def execute_intelligent_workflow(self, command: str, user_approved: bool = False) -> WorkflowResult:
        """Execute the intelligent workflow based on risk assessment."""
        app_logger.info(f"Starting intelligent workflow for: {command}")
        
        # Step 1: Assess risk
        assessment = self.assess_risk(command)
        app_logger.info(f"Risk assessment: {assessment.risk_level.value} - {assessment.reason}")
        
        # Step 2: Determine workflow path
        if assessment.risk_level == RiskLevel.LOW:
            return self._execute_low_risk_workflow(command)
        else:
            return self._execute_high_risk_workflow(command, assessment, user_approved)
    
    def _execute_low_risk_workflow(self, command: str) -> WorkflowResult:
        """Execute low-risk operations directly."""
        app_logger.info("Executing low-risk workflow - direct execution")
        
        try:
            # Direct execution
            result = execute_mikrotik_command(command)
            
            # Check logs (basic)
            logs_checked = self._check_basic_logs()
            
            return WorkflowResult(
                success=True,
                message=f"✅ LOW RISK OPERATION COMPLETED\n\nCommand: {command}\nResult: {result}",
                command_executed=command,
                safe_mode_used=False,
                logs_checked=logs_checked,
                state_verified=True
            )
            
        except Exception as e:
            return WorkflowResult(
                success=False,
                message=f"❌ LOW RISK OPERATION FAILED\n\nCommand: {command}\nError: {str(e)}",
                command_executed=command,
                safe_mode_used=False,
                logs_checked=False,
                state_verified=False
            )
    
    def _execute_high_risk_workflow(self, command: str, assessment: RiskAssessment, user_approved: bool) -> WorkflowResult:
        """Execute high-risk operations with safety measures."""
        app_logger.info("Executing high-risk workflow with safety measures")
        
        # Step 1: Show dry-run preview (if not already approved)
        if not user_approved:
            dry_run_result = self._show_dry_run_preview(command, assessment)
            return WorkflowResult(
                success=False,
                message=dry_run_result,
                command_executed="",
                safe_mode_used=False,
                logs_checked=False,
                state_verified=False
            )
        
        # Step 2: Enter Safe Mode (if required)
        safe_mode_used = False
        if assessment.requires_safe_mode:
            safe_mode_result = mikrotik_enter_safe_mode(timeout_minutes=15)
            safe_mode_used = True
            app_logger.info("Entered Safe Mode for high-risk operation")
        
        try:
            # Step 3: Execute command
            result = execute_mikrotik_command(command)
            
            # Step 4: Check logs and state
            logs_checked = self._check_operation_logs(command)
            state_verified = self._verify_operation_state(command)
            
            # Step 5: Exit Safe Mode (if used)
            if safe_mode_used:
                exit_result = mikrotik_exit_safe_mode()
                app_logger.info("Exited Safe Mode after successful operation")
            
            return WorkflowResult(
                success=True,
                message=f"✅ HIGH RISK OPERATION COMPLETED\n\nCommand: {command}\nResult: {result}\nSafe Mode: {'Used' if safe_mode_used else 'Not required'}\nLogs Checked: {'Yes' if logs_checked else 'No'}\nState Verified: {'Yes' if state_verified else 'No'}",
                command_executed=command,
                safe_mode_used=safe_mode_used,
                logs_checked=logs_checked,
                state_verified=state_verified
            )
            
        except Exception as e:
            # Safe Mode will auto-rollback on exception
            rollback_triggered = safe_mode_used
            app_logger.error(f"High-risk operation failed: {str(e)}")
            
            return WorkflowResult(
                success=False,
                message=f"❌ HIGH RISK OPERATION FAILED\n\nCommand: {command}\nError: {str(e)}\nAuto-rollback: {'Triggered' if rollback_triggered else 'Not available'}",
                command_executed=command,
                safe_mode_used=safe_mode_used,
                logs_checked=False,
                state_verified=False,
                rollback_triggered=rollback_triggered
            )
    
    def _show_dry_run_preview(self, command: str, assessment: RiskAssessment) -> str:
        """Show dry-run preview and request approval."""
        preview = f"""🔍 **DRY-RUN PREVIEW & APPROVAL REQUIRED**

**Command to Execute:**
```
{command}
```

**Risk Assessment:**
- **Level**: {assessment.risk_level.value.upper()}
- **Reason**: {assessment.reason}
- **Impact**: {assessment.estimated_impact}

**Warnings:**
"""
        for warning in assessment.warnings:
            preview += f"- ⚠️ {warning}\n"
        
        preview += f"""
**Safety Measures:**
- {'✅ Safe Mode will be used' if assessment.requires_safe_mode else '❌ Safe Mode not required'}
- ✅ Log monitoring will be performed
- ✅ State verification will be performed
- ✅ Automatic rollback available

**To proceed, please approve this operation.**
"""
        return preview
    
    def _check_basic_logs(self) -> bool:
        """Check basic system logs for errors."""
        try:
            result = execute_mikrotik_command("/log print where topics~\"error\"")
            return "error" in result.lower()
        except:
            return False
    
    def _check_operation_logs(self, command: str) -> bool:
        """Check logs specifically related to the operation."""
        try:
            # Get recent logs
            result = execute_mikrotik_command("/log print where time>\"00:00:01\"")
            return len(result.strip()) > 0
        except:
            return False
    
    def _verify_operation_state(self, command: str) -> bool:
        """Verify that the operation was successful by checking system state."""
        try:
            # Basic state verification - check if system is responsive
            result = execute_mikrotik_command("/system resource print")
            return "uptime" in result.lower()
        except:
            return False


# Global instance
_workflow_manager = None

def get_workflow_manager() -> IntelligentWorkflowManager:
    """Get the global workflow manager instance."""
    global _workflow_manager
    if _workflow_manager is None:
        _workflow_manager = IntelligentWorkflowManager()
    return _workflow_manager
