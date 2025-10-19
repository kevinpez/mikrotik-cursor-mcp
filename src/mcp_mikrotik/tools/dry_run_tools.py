"""
MCP tools for dry-run and safety operations.
Provides safe preview of changes before applying them.
"""

from typing import Dict, Any, List, Optional, Callable
from mcp.types import Tool
from ..dry_run import get_dry_run_manager, OperationType
from ..safety_manager import get_unified_safety_manager, DesiredState
from ..logger import app_logger
from ..settings.configuration import (
    get_config_summary, 
    set_dry_run_mode, 
    set_safety_mode,
    get_dry_run_mode,
    get_safety_mode
)


def get_dry_run_tools() -> List[Tool]:
    """Return the list of dry-run and safety tools."""
    return [
        # Dry-run analysis tool
        Tool(
            name="mikrotik_dry_run_analysis",
            description="Analyze a RouterOS command for safety and impact without executing it",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "RouterOS command to analyze (e.g., '/ip firewall filter add chain=input action=accept protocol=tcp dst-port=8080')"
                    },
                    "operation_type": {
                        "type": "string",
                        "enum": ["create", "update", "delete", "execute"],
                        "default": "execute",
                        "description": "Type of operation being performed"
                    },
                    "format": {
                        "type": "string",
                        "enum": ["text", "json", "markdown"],
                        "default": "text",
                        "description": "Output format for the analysis"
                    }
                },
                "required": ["command"]
            }
        ),
        
        # Plan creation tool
        Tool(
            name="mikrotik_create_plan",
            description="Create a deployment plan with multiple operations and analyze their combined impact",
            inputSchema={
                "type": "object",
                "properties": {
                    "operations": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "command": {"type": "string", "description": "RouterOS command"},
                                "operation_type": {
                                    "type": "string",
                                    "enum": ["create", "update", "delete", "execute"],
                                    "default": "execute"
                                }
                            },
                            "required": ["command"]
                        },
                        "description": "List of operations to include in the plan"
                    },
                    "format": {
                        "type": "string",
                        "enum": ["text", "json", "markdown"],
                        "default": "text",
                        "description": "Output format for the plan"
                    }
                },
                "required": ["operations"]
            }
        ),
        
        # Safety check tool
        Tool(
            name="mikrotik_safety_check",
            description="Check the safety level and warnings for a RouterOS command",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "RouterOS command to check"
                    },
                    "operation_type": {
                        "type": "string",
                        "enum": ["create", "update", "delete", "execute"],
                        "default": "execute"
                    }
                },
                "required": ["command"]
            }
        ),
        
        # Idempotency check tool
        Tool(
            name="mikrotik_check_idempotency",
            description="Check if a resource is in the desired state (idempotency check)",
            inputSchema={
                "type": "object",
                "properties": {
                    "resource_type": {
                        "type": "string",
                        "enum": ["firewall_rule", "ip_address", "dhcp_server", "route"],
                        "description": "Type of resource to check"
                    },
                    "properties": {
                        "type": "object",
                        "description": "Desired properties of the resource"
                    }
                },
                "required": ["resource_type", "properties"]
            }
        ),
        
        # Ensure desired state tool
        Tool(
            name="mikrotik_ensure_desired_state",
            description="Ensure a resource is in the desired state, creating or updating as needed",
            inputSchema={
                "type": "object",
                "properties": {
                    "desired_states": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "resource_type": {
                                    "type": "string",
                                    "enum": ["firewall_rule", "ip_address", "dhcp_server", "route"]
                                },
                                "properties": {"type": "object"},
                                "priority": {"type": "integer", "default": 0}
                            },
                            "required": ["resource_type", "properties"]
                        },
                        "description": "List of desired states to ensure"
                    },
                    "max_retries": {
                        "type": "integer",
                        "default": 3,
                        "description": "Maximum number of retry attempts"
                    }
                },
                "required": ["desired_states"]
            }
        ),
        
        # Batch safety analysis tool
        Tool(
            name="mikrotik_batch_safety_analysis",
            description="Analyze multiple commands for safety in batch",
            inputSchema={
                "type": "object",
                "properties": {
                    "commands": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "command": {"type": "string"},
                                "operation_type": {
                                    "type": "string",
                                    "enum": ["create", "update", "delete", "execute"],
                                    "default": "execute"
                                }
                            },
                            "required": ["command"]
                        },
                        "description": "List of commands to analyze"
                    },
                    "format": {
                        "type": "string",
                        "enum": ["text", "json", "markdown"],
                        "default": "text"
                    }
                },
                "required": ["commands"]
            }
        ),
        
        # Configuration management tools
        Tool(
            name="mikrotik_get_settings",
            description="Get current MCP server settings including dry-run mode, safety mode, connection info",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        
        Tool(
            name="mikrotik_toggle_dry_run",
            description="Enable or disable dry-run mode at runtime without restarting Cursor",
            inputSchema={
                "type": "object",
                "properties": {
                    "enabled": {
                        "type": "boolean",
                        "description": "true to enable dry-run mode, false to disable"
                    }
                },
                "required": ["enabled"]
            }
        ),
        
        Tool(
            name="mikrotik_toggle_safety_mode",
            description="Enable or disable safety mode at runtime",
            inputSchema={
                "type": "object",
                "properties": {
                    "enabled": {
                        "type": "boolean",
                        "description": "true to enable safety mode, false to disable"
                    }
                },
                "required": ["enabled"]
            }
        )
    ]


async def mikrotik_dry_run_analysis(command: str, operation_type: str = "execute", format: str = "text") -> Dict[str, Any]:
    """Analyze a RouterOS command for safety and impact."""
    try:
        app_logger.info(f"Dry-run analysis requested for command: {command}")
        
        # Convert string to enum
        op_type = OperationType(operation_type)
        
        # Get dry-run manager and analyze command
        dry_run_manager = get_dry_run_manager()
        result = dry_run_manager.dry_run_operation(command, op_type)
        
        # Format output based on requested format
        if format == "json":
            from dataclasses import asdict
            output = asdict(result)
        elif format == "markdown":
            output = _format_markdown_result(result)
        else:  # text format
            output = _format_text_result(result)
        
        app_logger.info(f"Dry-run analysis completed for command: {command}")
        
        return {
            "success": True,
            "result": output,
            "operation_id": result.operation_id,
            "safety_level": result.safety_level.value,
            "requires_confirmation": result.requires_confirmation
        }
        
    except Exception as e:
        app_logger.error(f"Error in dry-run analysis: {e}")
        return {
            "success": False,
            "error": str(e)
        }


async def mikrotik_create_plan(operations: List[Dict[str, Any]], format: str = "text") -> Dict[str, Any]:
    """Create a deployment plan with multiple operations."""
    try:
        app_logger.info(f"Plan creation requested with {len(operations)} operations")
        
        # Convert operations to tuples
        op_tuples = []
        for op in operations:
            command = op["command"]
            op_type = OperationType(op.get("operation_type", "execute"))
            op_tuples.append((command, op_type))
        
        # Create plan
        dry_run_manager = get_dry_run_manager()
        plan = dry_run_manager.create_plan(op_tuples)
        
        # Format output
        if format == "json":
            from dataclasses import asdict
            output = asdict(plan)
        elif format == "markdown":
            output = dry_run_manager.format_plan_output(plan, "markdown")
        else:  # text format
            output = dry_run_manager.format_plan_output(plan, "text")
        
        app_logger.info(f"Plan created successfully: {plan.plan_id}")
        
        return {
            "success": True,
            "plan": output,
            "plan_id": plan.plan_id,
            "total_operations": plan.total_operations,
            "requires_confirmation": plan.requires_confirmation,
            "risk_summary": {k.value: v for k, v in plan.risk_summary.items()}
        }
        
    except Exception as e:
        app_logger.error(f"Error creating plan: {e}")
        return {
            "success": False,
            "error": str(e)
        }


async def mikrotik_safety_check(command: str, operation_type: str = "execute") -> Dict[str, Any]:
    """Check the safety level and warnings for a command."""
    try:
        app_logger.info(f"Safety check requested for command: {command}")
        
        # Convert string to enum
        op_type = OperationType(operation_type)
        
        # Get dry-run manager and analyze command
        dry_run_manager = get_dry_run_manager()
        result = dry_run_manager.dry_run_operation(command, op_type)
        
        app_logger.info(f"Safety check completed for command: {command}")
        
        return {
            "success": True,
            "command": command,
            "safety_level": result.safety_level.value,
            "impact": result.estimated_impact,
            "requires_confirmation": result.requires_confirmation,
            "warnings": result.warnings,
            "errors": result.errors
        }
        
    except Exception as e:
        app_logger.error(f"Error in safety check: {e}")
        return {
            "success": False,
            "error": str(e)
        }


async def mikrotik_check_idempotency(resource_type: str, properties: Dict[str, Any]) -> Dict[str, Any]:
    """Check if a resource is in the desired state."""
    try:
        app_logger.info(f"Idempotency check requested for {resource_type}")
        
        # Create desired state
        desired_state = DesiredState(
            resource_type=resource_type,
            properties=properties
        )
        
        # Check idempotency
        safety_manager = get_unified_safety_manager()
        result = safety_manager.check_idempotency(desired_state.resource_type, desired_state.properties)
        
        app_logger.info(f"Idempotency check completed for {resource_type}")
        
        return {
            "success": True,
            "resource_type": resource_type,
            "state": result.state.value,
            "action_required": result.action_required,
            "message": result.message,
            "differences": result.differences,
            "current_state": result.current_state,
            "desired_state": result.desired_state
        }
        
    except Exception as e:
        app_logger.error(f"Error in idempotency check: {e}")
        return {
            "success": False,
            "error": str(e)
        }


async def mikrotik_ensure_desired_state(desired_states: List[Dict[str, Any]], max_retries: int = 3) -> Dict[str, Any]:
    """Ensure resources are in the desired state."""
    try:
        app_logger.info(f"Ensure desired state requested for {len(desired_states)} resources")
        
        # Convert to DesiredState objects
        states = []
        for state_dict in desired_states:
            state = DesiredState(
                resource_type=state_dict["resource_type"],
                properties=state_dict["properties"],
                priority=state_dict.get("priority", 0)
            )
            states.append(state)
        
        # Ensure desired states
        safety_manager = get_unified_safety_manager()
        results = safety_manager.ensure_desired_state(states, max_retries)
        
        app_logger.info(f"Ensure desired state completed for {len(desired_states)} resources")
        
        # Convert results to serializable format
        serializable_results = {}
        for resource_type, result in results.items():
            serializable_results[resource_type] = {
                "state": result.state.value,
                "action_required": result.action_required,
                "message": result.message,
                "differences": result.differences
            }
        
        return {
            "success": True,
            "results": serializable_results,
            "total_resources": len(desired_states)
        }
        
    except Exception as e:
        app_logger.error(f"Error ensuring desired state: {e}")
        return {
            "success": False,
            "error": str(e)
        }


async def mikrotik_batch_safety_analysis(commands: List[Dict[str, Any]], format: str = "text") -> Dict[str, Any]:
    """Analyze multiple commands for safety in batch."""
    try:
        app_logger.info(f"Batch safety analysis requested for {len(commands)} commands")
        
        dry_run_manager = get_dry_run_manager()
        results = []
        
        for cmd_dict in commands:
            command = cmd_dict["command"]
            op_type = OperationType(cmd_dict.get("operation_type", "execute"))
            
            result = dry_run_manager.dry_run_operation(command, op_type)
            
            results.append({
                "command": command,
                "operation_type": op_type.value,
                "safety_level": result.safety_level.value,
                "impact": result.estimated_impact,
                "requires_confirmation": result.requires_confirmation,
                "warnings": result.warnings,
                "errors": result.errors
            })
        
        app_logger.info(f"Batch safety analysis completed for {len(commands)} commands")
        
        return {
            "success": True,
            "results": results,
            "total_commands": len(commands),
            "summary": _generate_batch_summary(results)
        }
        
    except Exception as e:
        app_logger.error(f"Error in batch safety analysis: {e}")
        return {
            "success": False,
            "error": str(e)
        }


def _format_text_result(result) -> str:
    """Format dry-run result as text."""
    output = []
    output.append(f"Operation ID: {result.operation_id}")
    output.append(f"Safety Level: {result.safety_level.value}")
    output.append(f"Impact: {result.estimated_impact}")
    output.append(f"Confirmation Required: {'Yes' if result.requires_confirmation else 'No'}")
    
    if result.warnings:
        output.append("\nWarnings:")
        for warning in result.warnings:
            output.append(f"  {warning}")
    
    if result.errors:
        output.append("\nErrors:")
        for error in result.errors:
            output.append(f"  {error}")
    
    return "\n".join(output)


def _format_markdown_result(result) -> str:
    """Format dry-run result as markdown."""
    output = []
    output.append(f"# Dry-Run Analysis")
    output.append("")
    output.append(f"**Operation ID:** `{result.operation_id}`")
    output.append(f"**Safety Level:** {result.safety_level.value}")
    output.append(f"**Impact:** {result.estimated_impact}")
    output.append(f"**Confirmation Required:** {'Yes' if result.requires_confirmation else 'No'}")
    output.append("")
    
    if result.warnings:
        output.append("## Warnings")
        output.append("")
        for warning in result.warnings:
            output.append(f"- {warning}")
        output.append("")
    
    if result.errors:
        output.append("## Errors")
        output.append("")
        for error in result.errors:
            output.append(f"- {error}")
        output.append("")
    
    return "\n".join(output)


def _generate_batch_summary(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate summary for batch analysis results."""
    summary = {
        "total_commands": len(results),
        "safety_levels": {},
        "requires_confirmation": 0,
        "total_warnings": 0,
        "total_errors": 0
    }
    
    for result in results:
        # Count safety levels
        safety_level = result["safety_level"]
        summary["safety_levels"][safety_level] = summary["safety_levels"].get(safety_level, 0) + 1
        
        # Count confirmation requirements
        if result["requires_confirmation"]:
            summary["requires_confirmation"] += 1
        
        # Count warnings and errors
        summary["total_warnings"] += len(result["warnings"])
        summary["total_errors"] += len(result["errors"])
    
    return summary


def mikrotik_get_settings() -> Dict[str, Any]:
    """Get current MCP server settings."""
    try:
        settings = get_config_summary()
        app_logger.info("Settings retrieved successfully")
        return {
            "success": True,
            "settings": settings
        }
    except Exception as e:
        app_logger.error(f"Error getting settings: {e}")
        return {
            "success": False,
            "error": str(e)
        }


def mikrotik_toggle_dry_run(enabled: bool) -> Dict[str, Any]:
    """Toggle dry-run mode at runtime."""
    try:
        old_state = get_dry_run_mode()
        new_state = set_dry_run_mode(enabled)
        app_logger.info(f"Dry-run mode toggled: {old_state} → {new_state}")
        return {
            "success": True,
            "message": f"Dry-run mode {'enabled' if new_state else 'disabled'}",
            "previous_state": old_state,
            "current_state": new_state
        }
    except Exception as e:
        app_logger.error(f"Error toggling dry-run mode: {e}")
        return {
            "success": False,
            "error": str(e)
        }


def mikrotik_toggle_safety_mode(enabled: bool) -> Dict[str, Any]:
    """Toggle safety mode at runtime."""
    try:
        old_state = get_safety_mode()
        new_state = set_safety_mode(enabled)
        app_logger.info(f"Safety mode toggled: {old_state} → {new_state}")
        return {
            "success": True,
            "message": f"Safety mode {'enabled' if new_state else 'disabled'}",
            "previous_state": old_state,
            "current_state": new_state
        }
    except Exception as e:
        app_logger.error(f"Error toggling safety mode: {e}")
        return {
            "success": False,
            "error": str(e)
        }


def get_dry_run_handlers() -> Dict[str, Callable]:
    """Return the dry-run tool handlers."""
    
    # Synchronous wrapper for async functions
    def sync_idempotency_check(args):
        import asyncio
        return asyncio.run(mikrotik_check_idempotency(args['resource_type'], args['properties']))
    
    def sync_safety_check(args):
        import asyncio
        return asyncio.run(mikrotik_safety_check(args['command'], args.get('operation_type', 'execute')))
    
    def sync_dry_run_analysis(args):
        import asyncio
        return asyncio.run(mikrotik_dry_run_analysis(args['command']))
    
    return {
        "mikrotik_dry_run_analysis": sync_dry_run_analysis,
        "mikrotik_create_plan": mikrotik_create_plan,
        "mikrotik_safety_check": sync_safety_check,
        "mikrotik_check_idempotency": sync_idempotency_check,
        "mikrotik_ensure_desired_state": mikrotik_ensure_desired_state,
        "mikrotik_batch_safety_analysis": mikrotik_batch_safety_analysis,
        "mikrotik_get_settings": mikrotik_get_settings,
        "mikrotik_toggle_dry_run": mikrotik_toggle_dry_run,
        "mikrotik_toggle_safety_mode": mikrotik_toggle_safety_mode,
    }
