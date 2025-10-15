"""
Comprehensive feature registration tests.

Validates that:
- Every declared Tool has a corresponding handler.
- All nested category actions map to existing handlers.
- Handlers are callable.
- Tool/handler counts meet a conservative minimum.
"""

import os
import sys
from typing import Set


# Ensure src/ is importable when running tests without installation
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


def test_all_tools_have_handlers():
    from mcp_mikrotik.tools.tool_registry import get_all_tools, get_all_handlers

    tools = get_all_tools()
    handlers = get_all_handlers()

    tool_names: Set[str] = {t.name for t in tools}
    handler_names: Set[str] = set(handlers.keys())

    missing = sorted(tool_names - handler_names)
    assert not missing, f"Handlers missing for tools: {missing}"


def test_all_handlers_callable():
    from mcp_mikrotik.tools.tool_registry import get_all_handlers

    handlers = get_all_handlers()
    not_callable = sorted([name for name, fn in handlers.items() if not callable(fn)])
    assert not not_callable, f"Non-callable handlers: {not_callable}"


def test_nested_actions_resolve_to_handlers():
    from mcp_mikrotik.tools.tool_registry import get_all_handlers
    from mcp_mikrotik.serve import CATEGORY_ACTIONS

    handlers = get_all_handlers()
    missing = []
    for category, actions in CATEGORY_ACTIONS.items():
        for action in actions:
            handler_name = f"mikrotik_{action}"
            if handler_name not in handlers:
                missing.append((category, action, handler_name))

    assert not missing, (
        "Nested actions missing handlers: "
        + ", ".join([f"{c}.{a} -> {h}" for c, a, h in missing])
    )


def test_nested_tool_schemas_include_actions_enum():
    from mcp_mikrotik.serve import get_nested_tools, CATEGORY_ACTIONS, NESTED_TOOLS

    # Validate that action enums reflected in input schema match CATEGORY_ACTIONS
    tools = get_nested_tools()
    name_to_tool = {t.name: t for t in tools}

    mismatches = []
    for tool_def in NESTED_TOOLS:
        name = tool_def["name"]
        category = tool_def["category"]
        actions = CATEGORY_ACTIONS.get(category, [])

        tool = name_to_tool.get(name)
        assert tool is not None, f"Nested tool {name} not found in list_tools() output"

        schema = tool.inputSchema or {}
        props = schema.get("properties", {})
        action_prop = props.get("action", {})
        enum_values = action_prop.get("enum", [])
        if list(enum_values) != list(actions):
            mismatches.append((name, category))

    assert not mismatches, f"Action enums mismatch for: {mismatches}"


def test_minimum_tool_and_handler_counts():
    from mcp_mikrotik.tools.tool_registry import get_all_tools, get_all_handlers

    tools = get_all_tools()
    handlers = get_all_handlers()

    minimum = 380  # conservative floor aligned with README claims
    assert len(tools) >= minimum, f"Too few tools: {len(tools)} < {minimum}"
    assert len(handlers) >= minimum, f"Too few handlers: {len(handlers)} < {minimum}"


