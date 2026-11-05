"""Unit tests for the SSH client, using a mocked paramiko connection."""

from unittest.mock import MagicMock

import paramiko
import pytest

from mcp_mikrotik.mikrotik_ssh_client import MikroTikSSHClient


def _stream(text: str) -> MagicMock:
    stream = MagicMock()
    stream.read.return_value = text.encode("utf-8")
    return stream


@pytest.fixture
def fake_ssh(monkeypatch):
    """Replace paramiko.SSHClient with a mock and return the mock instance."""
    instance = MagicMock()
    monkeypatch.setattr(paramiko, "SSHClient", lambda: instance)
    return instance


def test_connect_success(fake_ssh):
    client = MikroTikSSHClient("192.0.2.1", "admin", "secret", port=2222)
    assert client.connect() is True
    kwargs = fake_ssh.connect.call_args.kwargs
    assert kwargs["hostname"] == "192.0.2.1"
    assert kwargs["port"] == 2222
    assert kwargs["username"] == "admin"


def test_connect_auth_failure_returns_false(fake_ssh):
    fake_ssh.connect.side_effect = paramiko.AuthenticationException("bad password")
    client = MikroTikSSHClient("192.0.2.1", "admin", "wrong")
    assert client.connect() is False


def test_connect_timeout_returns_false(fake_ssh):
    fake_ssh.connect.side_effect = TimeoutError("no route")
    assert MikroTikSSHClient("192.0.2.1", "admin", "x").connect() is False


def test_execute_command_returns_stdout(fake_ssh):
    fake_ssh.exec_command.return_value = (
        MagicMock(),
        _stream("name: core-router\n"),
        _stream(""),
    )
    client = MikroTikSSHClient("192.0.2.1", "admin", "secret")
    client.connect()
    assert client.execute_command("/system identity print") == "name: core-router\n"
    fake_ssh.exec_command.assert_called_once_with("/system identity print", timeout=30)


def test_execute_command_returns_stderr_when_no_stdout(fake_ssh):
    fake_ssh.exec_command.return_value = (
        MagicMock(),
        _stream(""),
        _stream("bad command name"),
    )
    client = MikroTikSSHClient("192.0.2.1", "admin", "secret")
    client.connect()
    assert client.execute_command("/bogus") == "bad command name"


def test_execute_command_requires_connection():
    client = MikroTikSSHClient("192.0.2.1", "admin", "secret")
    with pytest.raises(Exception, match="Not connected"):
        client.execute_command("/system identity print")
