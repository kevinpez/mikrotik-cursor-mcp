#!/usr/bin/env python3
"""
Generate comprehensive integration tests for all MCP handlers.
This script analyzes all handlers and generates appropriate tests.
"""

import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from mcp_mikrotik.tools.tool_registry import get_all_handlers


def categorize_handlers(handlers):
    """Categorize handlers by operation type and category."""
    categories = {}
    
    for name in sorted(handlers.keys()):
        # Extract category (second part of name)
        parts = name.split('_')
        if len(parts) < 2:
            continue
            
        operation = parts[1]  # list, get, create, remove, etc.
        category = parts[2] if len(parts) > 2 else 'general'
        
        key = f"{category}_{operation}"
        if category not in categories:
            categories[category] = {}
        if operation not in categories[category]:
            categories[category][operation] = []
        categories[category][operation].append(name)
    
    return categories


def main():
    """Generate test statistics."""
    handlers = get_all_handlers()
    categories = categorize_handlers(handlers)
    
    print(f"Total Handlers: {len(handlers)}")
    print(f"\nCategories: {len(categories)}")
    
    # Count by operation type
    operations = {}
    for name in handlers.keys():
        op = name.split('_')[1] if '_' in name else 'other'
        operations[op] = operations.get(op, 0) + 1
    
    print(f"\nBy Operation Type:")
    for op, count in sorted(operations.items(), key=lambda x: -x[1])[:15]:
        print(f"  {op:15s}: {count:3d}")
    
    # Safe operations (read-only)
    safe_ops = ['list', 'get', 'check', 'show', 'print', 'monitor', 'scan', 'search', 'export']
    safe_handlers = [h for h in handlers.keys() if any(h.split('_')[1] == op for op in safe_ops if '_' in h)]
    
    print(f"\nSafe (Read-Only) Handlers: {len(safe_handlers)}")
    print(f"Write Handlers: {len(handlers) - len(safe_handlers)}")
    
    # Generate test counts by category
    print(f"\nHandlers by Category:")
    cat_counts = {}
    for name in handlers.keys():
        parts = name.split('_')
        cat = parts[2] if len(parts) > 2 else 'general'
        cat_counts[cat] = cat_counts.get(cat, 0) + 1
    
    for cat, count in sorted(cat_counts.items(), key=lambda x: -x[1])[:20]:
        print(f"  {cat:20s}: {count:3d}")


if __name__ == '__main__':
    main()

