"""
Intelligent Workflow tools for MikroTik operations.
Provides risk-based workflow management with automatic safety measures.
"""
from mcp.types import Tool
from ..safety.intelligent_workflow import get_workflow_manager


def get_intelligent_workflow_tools() -> list[Tool]:
    """Get all intelligent workflow tools."""
    return [
        Tool(
            name="mikrotik_execute_with_intelligent_workflow",
            description="Execute a MikroTik command using intelligent risk-based workflow. Automatically determines if the operation is low-risk (direct execution) or high-risk (dry-run preview → approval → safe mode → execution). Provides comprehensive safety measures including log monitoring and state verification.",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The MikroTik RouterOS command to execute"
                    },
                    "user_approved": {
                        "type": "boolean",
                        "description": "Whether the user has already approved this operation (skip dry-run preview)",
                        "default": False
                    }
                },
                "required": ["command"]
            },
        ),
        Tool(
            name="mikrotik_assess_command_risk",
            description="Assess the risk level of a MikroTik command without executing it. Returns detailed risk analysis including warnings and recommended safety measures.",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The MikroTik RouterOS command to assess"
                    }
                },
                "required": ["command"]
            },
        ),
        Tool(
            name="mikrotik_show_dry_run_preview",
            description="Show a dry-run preview of a MikroTik command with risk assessment and request user approval. This is automatically called for high-risk operations.",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The MikroTik RouterOS command to preview"
                    }
                },
                "required": ["command"]
            },
        ),
        Tool(
            name="mikrotik_execute_approved_operation",
            description="Execute a previously approved MikroTik operation with full safety measures (Safe Mode, log monitoring, state verification). Use this after approving a dry-run preview.",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The approved MikroTik RouterOS command to execute"
                    }
                },
                "required": ["command"]
            },
        ),
    ]


def get_intelligent_workflow_handlers() -> dict:
    """Get all intelligent workflow tool handlers."""
    return {
        "mikrotik_execute_with_intelligent_workflow": lambda args: _execute_with_workflow(
            args["command"], args.get("user_approved", False)
        ),
        "mikrotik_assess_command_risk": lambda args: _assess_command_risk(args["command"]),
        "mikrotik_show_dry_run_preview": lambda args: _show_dry_run_preview(args["command"]),
        "mikrotik_execute_approved_operation": lambda args: _execute_approved_operation(args["command"]),
    }


def _execute_with_workflow(command: str, user_approved: bool = False) -> str:
    """Execute command with intelligent workflow."""
    workflow_manager = get_workflow_manager()
    result = workflow_manager.execute_intelligent_workflow(command, user_approved)
    return result.message


def _assess_command_risk(command: str) -> str:
    """Assess the risk level of a command."""
    workflow_manager = get_workflow_manager()
    assessment = workflow_manager.assess_risk(command)
    
    result = f"""🔍 **RISK ASSESSMENT**

**Command:** `{command}`

**Risk Level:** {assessment.risk_level.value.upper()}

**Reason:** {assessment.reason}

**Estimated Impact:** {assessment.estimated_impact}

**Safety Requirements:**
- **Requires Approval:** {'Yes' if assessment.requires_approval else 'No'}
- **Requires Safe Mode:** {'Yes' if assessment.requires_safe_mode else 'No'}

**Warnings:**
"""
    for warning in assessment.warnings:
        result += f"- ⚠️ {warning}\n"
    
    return result


def _show_dry_run_preview(command: str) -> str:
    """Show dry-run preview and request approval."""
    workflow_manager = get_workflow_manager()
    assessment = workflow_manager.assess_risk(command)
    return workflow_manager._show_dry_run_preview(command, assessment)


def _execute_approved_operation(command: str) -> str:
    """Execute an approved operation with full safety measures."""
    workflow_manager = get_workflow_manager()
    result = workflow_manager.execute_intelligent_workflow(command, user_approved=True)
    return result.message
