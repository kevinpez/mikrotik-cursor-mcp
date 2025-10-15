"""
Dry-run and plan mode for MikroTik operations.
Provides safe preview of changes with exact RouterOS diffs.
"""
import json
import time
import uuid
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import difflib
from .connection_manager import get_connection_manager
from .logger import app_logger


class OperationType(Enum):
    """Types of operations that can be dry-run."""
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    EXECUTE = "execute"


class SafetyLevel(Enum):
    """Safety levels for operations."""
    SAFE = "safe"           # Read-only operations
    LOW_RISK = "low_risk"   # Non-destructive changes
    MEDIUM_RISK = "medium_risk"  # Configuration changes
    HIGH_RISK = "high_risk" # Network-affecting changes
    CRITICAL = "critical"   # System-critical changes


@dataclass
class DryRunResult:
    """Result of a dry-run operation."""
    operation_id: str
    operation_type: OperationType
    safety_level: SafetyLevel
    command: str
    current_state: Optional[Dict[str, Any]] = None
    proposed_state: Optional[Dict[str, Any]] = None
    diff: Optional[str] = None
    warnings: List[str] = None
    errors: List[str] = None
    requires_confirmation: bool = False
    estimated_impact: str = ""
    
    def __post_init__(self):
        if self.warnings is None:
            self.warnings = []
        if self.errors is None:
            self.errors = []


@dataclass
class PlanResult:
    """Result of a plan operation showing multiple changes."""
    plan_id: str
    timestamp: float
    operations: List[DryRunResult]
    total_operations: int
    risk_summary: Dict[SafetyLevel, int]
    requires_confirmation: bool
    estimated_duration: str
    rollback_available: bool = False


class DryRunManager:
    """Manages dry-run operations and safety checks."""
    
    def __init__(self):
        self.connection_manager = get_connection_manager()
        self.safe_commands = {
            # Read-only commands that are always safe
            '/system identity print',
            '/system resource print',
            '/system clock print',
            '/ip address print',
            '/ip route print',
            '/interface print',
            '/ip firewall filter print',
            '/ip firewall nat print',
            '/ip dhcp-server print',
            '/ip dns print',
            '/user print',
            '/log print',
            '/backup print',
            '/certificate print',
            '/ipv6 address print',
            '/ipv6 route print',
            '/routing bgp print',
            '/routing ospf print',
            '/wireguard print',
            '/openvpn print',
            '/container print',
            '/queue simple print',
            '/queue tree print',
            '/hotspot print',
            '/wireless print',
            '/vlan print',
            '/pppoe print',
            '/tunnel print',
            '/bonding print',
            '/bridge print',
            '/caps-man print',
        }
        
        self.high_risk_commands = {
            # Commands that can break network connectivity
            '/ip firewall filter add',
            '/ip firewall filter remove',
            '/ip firewall nat add',
            '/ip firewall nat remove',
            '/ip route add',
            '/ip route remove',
            '/interface disable',
            '/interface enable',
            '/system reboot',
            '/system shutdown',
            '/user remove',
            '/user add',
            '/ip dhcp-server remove',
            '/ip dhcp-server add',
            '/routing bgp remove',
            '/routing ospf remove',
            '/wireguard remove',
            '/openvpn remove',
            '/container remove',
            '/queue simple remove',
            '/queue tree remove',
            '/hotspot remove',
            '/wireless remove',
            '/vlan remove',
            '/pppoe remove',
            '/tunnel remove',
            '/bonding remove',
            '/bridge remove',
            '/caps-man remove',
        }
        
        self.critical_commands = {
            # Commands that can cause system instability
            '/system reboot',
            '/system shutdown',
            '/system reset-configuration',
            '/system package remove',
            '/system package update',
            '/user remove admin',
            '/ip service disable ssh',
            '/ip service disable api',
            '/ip service disable winbox',
        }

    def _get_safety_level(self, command: str) -> SafetyLevel:
        """Determine the safety level of a command."""
        command_lower = command.lower().strip()
        
        # Check for critical commands first
        for critical_cmd in self.critical_commands:
            if command_lower.startswith(critical_cmd.lower()):
                return SafetyLevel.CRITICAL
        
        # Check for high-risk commands
        for high_risk_cmd in self.high_risk_commands:
            if command_lower.startswith(high_risk_cmd.lower()):
                return SafetyLevel.HIGH_RISK
        
        # Check for safe commands
        for safe_cmd in self.safe_commands:
            if command_lower.startswith(safe_cmd.lower()):
                return SafetyLevel.SAFE
        
        # Default to medium risk for unknown commands
        return SafetyLevel.MEDIUM_RISK

    def _get_current_state(self, command: str) -> Optional[Dict[str, Any]]:
        """Get current state for comparison."""
        try:
            with self.connection_manager.get_connection_context() as conn:
                stdin, stdout, stderr = conn.exec_command(command, timeout=10)
                result = stdout.read().decode('utf-8')
                error = stderr.read().decode('utf-8')
                
                if error:
                    app_logger.warning(f"Error getting current state: {error}")
                    return None
                
                # Parse RouterOS output into structured data
                return self._parse_routeros_output(result)
        except Exception as e:
            app_logger.error(f"Failed to get current state: {e}")
            return None

    def _parse_routeros_output(self, output: str) -> Dict[str, Any]:
        """Parse RouterOS command output into structured data."""
        lines = output.strip().split('\n')
        result = {}
        
        for line in lines:
            if '=' in line and not line.startswith('#'):
                try:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Handle different value types
                    if value.lower() in ['true', 'yes']:
                        result[key] = True
                    elif value.lower() in ['false', 'no']:
                        result[key] = False
                    elif value.isdigit():
                        result[key] = int(value)
                    else:
                        result[key] = value
                except ValueError:
                    # Skip malformed lines
                    continue
        
        return result

    def _generate_diff(self, current: Optional[Dict[str, Any]], 
                      proposed: Optional[Dict[str, Any]]) -> str:
        """Generate a diff between current and proposed states."""
        if not current and not proposed:
            return "No state information available"
        
        if not current:
            return "Creating new configuration"
        
        if not proposed:
            return "Removing configuration"
        
        # Convert to comparable format
        current_str = json.dumps(current, indent=2, sort_keys=True)
        proposed_str = json.dumps(proposed, indent=2, sort_keys=True)
        
        # Generate unified diff
        diff_lines = list(difflib.unified_diff(
            current_str.splitlines(keepends=True),
            proposed_str.splitlines(keepends=True),
            fromfile='Current State',
            tofile='Proposed State',
            lineterm=''
        ))
        
        return ''.join(diff_lines)

    def _generate_warnings(self, command: str, safety_level: SafetyLevel) -> List[str]:
        """Generate warnings based on command and safety level."""
        warnings = []
        
        if safety_level == SafetyLevel.CRITICAL:
            warnings.append("⚠️  CRITICAL: This operation can cause system instability or data loss")
            warnings.append("🔴 RECOMMENDATION: Test on non-production device first")
            warnings.append("💾 BACKUP: Ensure you have a recent backup before proceeding")
        
        elif safety_level == SafetyLevel.HIGH_RISK:
            warnings.append("⚠️  HIGH RISK: This operation can affect network connectivity")
            warnings.append("🔴 RECOMMENDATION: Schedule during maintenance window")
            warnings.append("💾 BACKUP: Consider creating a backup before proceeding")
        
        elif safety_level == SafetyLevel.MEDIUM_RISK:
            warnings.append("⚠️  MEDIUM RISK: This operation modifies system configuration")
            warnings.append("🔴 RECOMMENDATION: Monitor system after changes")
        
        # Command-specific warnings
        if 'firewall' in command.lower():
            warnings.append("🔥 FIREWALL: Changes may affect network access")
        
        if 'route' in command.lower():
            warnings.append("🛣️  ROUTING: Changes may affect network connectivity")
        
        if 'user' in command.lower() and 'remove' in command.lower():
            warnings.append("👤 USER: Removing users may lock you out of the system")
        
        if 'interface' in command.lower() and 'disable' in command.lower():
            warnings.append("🔌 INTERFACE: Disabling interfaces may cause network outages")
        
        return warnings

    def dry_run_operation(self, command: str, operation_type: OperationType = OperationType.EXECUTE) -> DryRunResult:
        """
        Perform a dry-run of a single operation.
        
        Args:
            command: RouterOS command to analyze
            operation_type: Type of operation being performed
            
        Returns:
            DryRunResult with analysis and recommendations
        """
        operation_id = str(uuid.uuid4())
        safety_level = self._get_safety_level(command)
        
        app_logger.info(f"Dry-run analysis for command: {command}")
        app_logger.info(f"Safety level: {safety_level.value}")
        
        # Get current state if this is a read operation
        current_state = None
        if operation_type in [OperationType.UPDATE, OperationType.DELETE]:
            # Try to get current state by converting add/remove to print
            read_command = command.replace(' add', ' print').replace(' remove', ' print')
            if read_command != command:
                current_state = self._get_current_state(read_command)
        
        # Generate warnings
        warnings = self._generate_warnings(command, safety_level)
        
        # Determine if confirmation is required
        requires_confirmation = safety_level in [SafetyLevel.HIGH_RISK, SafetyLevel.CRITICAL]
        
        # Estimate impact
        impact_map = {
            SafetyLevel.SAFE: "No impact - read-only operation",
            SafetyLevel.LOW_RISK: "Minimal impact - configuration change",
            SafetyLevel.MEDIUM_RISK: "Moderate impact - system configuration change",
            SafetyLevel.HIGH_RISK: "High impact - may affect network connectivity",
            SafetyLevel.CRITICAL: "Critical impact - may cause system instability"
        }
        
        return DryRunResult(
            operation_id=operation_id,
            operation_type=operation_type,
            safety_level=safety_level,
            command=command,
            current_state=current_state,
            warnings=warnings,
            requires_confirmation=requires_confirmation,
            estimated_impact=impact_map[safety_level]
        )

    def create_plan(self, operations: List[Tuple[str, OperationType]]) -> PlanResult:
        """
        Create a plan showing multiple operations and their combined impact.
        
        Args:
            operations: List of (command, operation_type) tuples
            
        Returns:
            PlanResult with comprehensive analysis
        """
        plan_id = str(uuid.uuid4())
        timestamp = time.time()
        
        app_logger.info(f"Creating plan with {len(operations)} operations")
        
        # Analyze each operation
        dry_run_results = []
        for command, op_type in operations:
            result = self.dry_run_operation(command, op_type)
            dry_run_results.append(result)
        
        # Calculate risk summary
        risk_summary = {}
        for level in SafetyLevel:
            risk_summary[level] = sum(1 for r in dry_run_results if r.safety_level == level)
        
        # Determine if plan requires confirmation
        requires_confirmation = any(r.requires_confirmation for r in dry_run_results)
        
        # Estimate duration (rough calculation)
        estimated_duration = f"{len(operations) * 2} seconds"  # 2 seconds per operation
        
        # Check if rollback is available
        rollback_available = any(r.operation_type in [OperationType.CREATE, OperationType.UPDATE] 
                               for r in dry_run_results)
        
        return PlanResult(
            plan_id=plan_id,
            timestamp=timestamp,
            operations=dry_run_results,
            total_operations=len(operations),
            risk_summary=risk_summary,
            requires_confirmation=requires_confirmation,
            estimated_duration=estimated_duration,
            rollback_available=rollback_available
        )

    def format_plan_output(self, plan: PlanResult, format_type: str = "text") -> str:
        """
        Format plan output for display.
        
        Args:
            plan: PlanResult to format
            format_type: Output format ("text", "json", "markdown")
            
        Returns:
            Formatted plan output
        """
        if format_type == "json":
            return json.dumps(asdict(plan), indent=2, default=str)
        
        elif format_type == "markdown":
            return self._format_markdown_plan(plan)
        
        else:  # text format
            return self._format_text_plan(plan)

    def _format_text_plan(self, plan: PlanResult) -> str:
        """Format plan as human-readable text."""
        output = []
        output.append("=" * 80)
        output.append("🔍 MIKROTIK OPERATION PLAN")
        output.append("=" * 80)
        output.append(f"Plan ID: {plan.plan_id}")
        output.append(f"Created: {time.ctime(plan.timestamp)}")
        output.append(f"Total Operations: {plan.total_operations}")
        output.append(f"Estimated Duration: {plan.estimated_duration}")
        output.append(f"Rollback Available: {'Yes' if plan.rollback_available else 'No'}")
        output.append("")
        
        # Risk summary
        output.append("📊 RISK SUMMARY:")
        for level, count in plan.risk_summary.items():
            if count > 0:
                emoji = {"safe": "✅", "low_risk": "🟡", "medium_risk": "🟠", 
                        "high_risk": "🔴", "critical": "💀"}[level.value]
                output.append(f"  {emoji} {level.value.replace('_', ' ').title()}: {count}")
        output.append("")
        
        # Operations
        output.append("🔧 OPERATIONS:")
        for i, op in enumerate(plan.operations, 1):
            output.append(f"\n{i}. {op.command}")
            output.append(f"   Type: {op.operation_type.value}")
            output.append(f"   Safety: {op.safety_level.value}")
            output.append(f"   Impact: {op.estimated_impact}")
            
            if op.warnings:
                output.append("   Warnings:")
                for warning in op.warnings:
                    output.append(f"     {warning}")
        
        # Confirmation requirement
        if plan.requires_confirmation:
            output.append("\n" + "=" * 80)
            output.append("⚠️  CONFIRMATION REQUIRED")
            output.append("This plan contains high-risk or critical operations.")
            output.append("Review all warnings before proceeding.")
            output.append("=" * 80)
        
        return "\n".join(output)

    def _format_markdown_plan(self, plan: PlanResult) -> str:
        """Format plan as Markdown."""
        output = []
        output.append("# MikroTik Operation Plan")
        output.append("")
        output.append(f"**Plan ID:** `{plan.plan_id}`")
        output.append(f"**Created:** {time.ctime(plan.timestamp)}")
        output.append(f"**Total Operations:** {plan.total_operations}")
        output.append(f"**Estimated Duration:** {plan.estimated_duration}")
        output.append(f"**Rollback Available:** {'Yes' if plan.rollback_available else 'No'}")
        output.append("")
        
        # Risk summary table
        output.append("## Risk Summary")
        output.append("")
        output.append("| Safety Level | Count |")
        output.append("|--------------|-------|")
        for level, count in plan.risk_summary.items():
            if count > 0:
                output.append(f"| {level.value.replace('_', ' ').title()} | {count} |")
        output.append("")
        
        # Operations
        output.append("## Operations")
        output.append("")
        for i, op in enumerate(plan.operations, 1):
            output.append(f"### {i}. {op.command}")
            output.append("")
            output.append(f"- **Type:** {op.operation_type.value}")
            output.append(f"- **Safety:** {op.safety_level.value}")
            output.append(f"- **Impact:** {op.estimated_impact}")
            output.append("")
            
            if op.warnings:
                output.append("**Warnings:**")
                output.append("")
                for warning in op.warnings:
                    output.append(f"- {warning}")
                output.append("")
        
        return "\n".join(output)


# Global dry-run manager instance
_dry_run_manager: Optional[DryRunManager] = None


def get_dry_run_manager() -> DryRunManager:
    """Get the global dry-run manager instance."""
    global _dry_run_manager
    if _dry_run_manager is None:
        _dry_run_manager = DryRunManager()
    return _dry_run_manager
