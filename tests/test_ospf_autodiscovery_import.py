from mcp_mikrotik.scope.ospf_autodiscovery import mikrotik_auto_assign_ospf_subnet
from mcp_mikrotik.tools.tool_registry import get_all_handlers, get_all_tools


def test_ospf_autodiscovery_registry_imports() -> None:
    tools = {tool.name for tool in get_all_tools()}
    handlers = get_all_handlers()

    expected_names = {
        "mikrotik_scan_mikrotik_neighbors",
        "mikrotik_get_ospf_assignments",
        "mikrotik_auto_assign_ospf_subnet",
        "mikrotik_auto_configure_ospf_instance",
        "mikrotik_auto_configure_ospf_area",
        "mikrotik_auto_configure_ospf_networks",
        "mikrotik_auto_configure_ospf_interfaces",
        "mikrotik_enable_ospf_instance",
        "mikrotik_auto_discovery_ospf_complete",
        "mikrotik_get_ospf_auto_discovery_status",
    }

    assert expected_names <= tools
    assert expected_names <= set(handlers)


def test_auto_assign_ospf_subnet_is_deterministic() -> None:
    first = mikrotik_auto_assign_ospf_subnet("site-a", "10.0.0.0/16")
    second = mikrotik_auto_assign_ospf_subnet("site-a", "10.0.0.0/16")

    assert first == second
    assert "site_id: site-a" in first
    assert "subnet: 10.0." in first
    assert "router_id_network:" in first
