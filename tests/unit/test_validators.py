"""Unit tests for input validation helpers. No router needed."""

import pytest

from mcp_mikrotik.scope.validators import (
    format_bytes,
    parse_mikrotik_time,
    validate_interface_name,
    validate_ip_address,
    validate_keepalive,
    validate_port,
    validate_wireguard_key,
)


@pytest.mark.parametrize(
    "ip",
    ["192.168.88.1", "10.0.0.0/8", "0.0.0.0/0", "255.255.255.255/32"],
)
def test_valid_ip_addresses(ip):
    ok, err = validate_ip_address(ip)
    assert ok
    assert err == ""


@pytest.mark.parametrize(
    "ip, reason",
    [
        ("192.168.1", "format"),
        ("192.168.1.256", "octet"),
        ("10.0.0.1/33", "CIDR"),
        ("router.local", "format"),
    ],
)
def test_invalid_ip_addresses(ip, reason):
    ok, err = validate_ip_address(ip)
    assert not ok
    assert reason in err


def test_wireguard_key_accepts_44_char_base64():
    key = "A" * 43 + "="
    assert validate_wireguard_key(key) == (True, "")


@pytest.mark.parametrize("key", ["A" * 43, "A" * 44, "!" * 43 + "="])
def test_wireguard_key_rejects_bad_keys(key):
    ok, _ = validate_wireguard_key(key)
    assert not ok


@pytest.mark.parametrize("port", [1, 22, 8728, 65535, "443"])
def test_valid_ports(port):
    assert validate_port(port)[0]


@pytest.mark.parametrize("port", [0, 65536, -1, "ssh"])
def test_invalid_ports(port):
    assert not validate_port(port)[0]


def test_interface_names():
    assert validate_interface_name("ether1")[0]
    assert validate_interface_name("vlan_100-mgmt")[0]
    assert not validate_interface_name("ether 1")[0]
    assert not validate_interface_name("x" * 65)[0]


@pytest.mark.parametrize("value", ["25s", "1m", "1m30s", "2h"])
def test_valid_keepalive(value):
    assert validate_keepalive(value)[0]


@pytest.mark.parametrize("value", ["25", "s25", "1d", "1m30s5s"])
def test_invalid_keepalive(value):
    assert not validate_keepalive(value)[0]


@pytest.mark.parametrize(
    "value, expected",
    [
        (0, "0.00 B"),
        (1023, "1023.00 B"),
        (1024, "1.00 KB"),
        (1536, "1.50 KB"),
        (1024**3, "1.00 GB"),
    ],
)
def test_format_bytes(value, expected):
    assert format_bytes(value) == expected


@pytest.mark.parametrize(
    "text, seconds",
    [("5s", 5), ("4m5s", 245), ("1d", 86400), ("1w2d3h4m5s", 788645)],
)
def test_parse_mikrotik_time(text, seconds):
    assert parse_mikrotik_time(text) == seconds
