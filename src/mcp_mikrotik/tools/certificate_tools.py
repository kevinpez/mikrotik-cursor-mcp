from typing import Dict, Any, List, Callable
from mcp.types import Tool
from ..scope.certificates import (
    mikrotik_list_certificates,
    mikrotik_get_certificate,
    mikrotik_create_certificate,
    mikrotik_sign_certificate,
    mikrotik_import_certificate,
    mikrotik_export_certificate,
    mikrotik_remove_certificate,
    mikrotik_create_ca_certificate,
    mikrotik_revoke_certificate,
    mikrotik_trust_certificate,
    mikrotik_get_certificate_fingerprint
)

def get_certificate_tools() -> List[Tool]:
    """Return the list of certificate management tools."""
    return [
        Tool(
            name="mikrotik_list_certificates",
            description="Lists certificates on MikroTik device (READ-ONLY, safe)",
            inputSchema={
                "type": "object",
                "properties": {
                    "name_filter": {"type": "string"},
                    "common_name_filter": {"type": "string"},
                    "invalid_only": {"type": "boolean"},
                    "expired_only": {"type": "boolean"}
                },
                "required": []
            },
        ),
        Tool(
            name="mikrotik_get_certificate",
            description="Gets detailed information about a specific certificate (READ-ONLY, safe)",
            inputSchema={
                "type": "object",
                "properties": {
                    "cert_id": {"type": "string"}
                },
                "required": ["cert_id"]
            },
        ),
        Tool(
            name="mikrotik_create_certificate",
            description="Creates a new self-signed certificate",
            inputSchema={
                "type": "object",
                "properties": {
                    "common_name": {"type": "string"},
                    "name": {"type": "string"},
                    "key_size": {"type": "integer", "enum": [1024, 2048, 4096], "default": 2048},
                    "days_valid": {"type": "integer", "default": 365},
                    "country": {"type": "string"},
                    "state": {"type": "string"},
                    "locality": {"type": "string"},
                    "organization": {"type": "string"},
                    "unit": {"type": "string"},
                    "subject_alt_name": {"type": "string"},
                    "key_usage": {"type": "string"}
                },
                "required": ["common_name"]
            },
        ),
        Tool(
            name="mikrotik_sign_certificate",
            description="Signs a certificate (self-sign or with CA)",
            inputSchema={
                "type": "object",
                "properties": {
                    "cert_id": {"type": "string"},
                    "ca": {"type": "string", "description": "CA certificate name (optional for self-sign)"}
                },
                "required": ["cert_id"]
            },
        ),
        Tool(
            name="mikrotik_import_certificate",
            description="Imports a certificate from a file on the router",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string"},
                    "passphrase": {"type": "string"},
                    "name": {"type": "string"}
                },
                "required": ["file_path"]
            },
        ),
        Tool(
            name="mikrotik_export_certificate",
            description="Exports a certificate to a file",
            inputSchema={
                "type": "object",
                "properties": {
                    "cert_id": {"type": "string"},
                    "file_name": {"type": "string"},
                    "export_passphrase": {"type": "string"},
                    "type_": {"type": "string", "enum": ["pem", "pkcs12"], "default": "pem"}
                },
                "required": ["cert_id"]
            },
        ),
        Tool(
            name="mikrotik_remove_certificate",
            description="Removes a certificate from the device",
            inputSchema={
                "type": "object",
                "properties": {
                    "cert_id": {"type": "string"}
                },
                "required": ["cert_id"]
            },
        ),
        Tool(
            name="mikrotik_create_ca_certificate",
            description="Creates a Certificate Authority (CA) certificate",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "common_name": {"type": "string"},
                    "key_size": {"type": "integer", "enum": [1024, 2048, 4096], "default": 2048},
                    "days_valid": {"type": "integer", "default": 3650},
                    "country": {"type": "string"},
                    "organization": {"type": "string"}
                },
                "required": ["name", "common_name"]
            },
        ),
        Tool(
            name="mikrotik_revoke_certificate",
            description="Revokes a certificate (marks as not trusted)",
            inputSchema={
                "type": "object",
                "properties": {
                    "cert_id": {"type": "string"}
                },
                "required": ["cert_id"]
            },
        ),
        Tool(
            name="mikrotik_trust_certificate",
            description="Marks a certificate as trusted",
            inputSchema={
                "type": "object",
                "properties": {
                    "cert_id": {"type": "string"}
                },
                "required": ["cert_id"]
            },
        ),
        Tool(
            name="mikrotik_get_certificate_fingerprint",
            description="Gets the fingerprint of a certificate (READ-ONLY, safe)",
            inputSchema={
                "type": "object",
                "properties": {
                    "cert_id": {"type": "string"}
                },
                "required": ["cert_id"]
            },
        ),
    ]

def get_certificate_handlers() -> Dict[str, Callable]:
    """Return the handlers for certificate management tools."""
    return {
        "mikrotik_list_certificates": lambda args: mikrotik_list_certificates(
            args.get("name_filter"),
            args.get("common_name_filter"),
            args.get("invalid_only", False),
            args.get("expired_only", False)
        ),
        "mikrotik_get_certificate": lambda args: mikrotik_get_certificate(
            args["cert_id"]
        ),
        "mikrotik_create_certificate": lambda args: mikrotik_create_certificate(
            args["common_name"],
            args.get("name"),
            args.get("key_size", 2048),
            args.get("days_valid", 365),
            args.get("country"),
            args.get("state"),
            args.get("locality"),
            args.get("organization"),
            args.get("unit"),
            args.get("subject_alt_name"),
            args.get("key_usage")
        ),
        "mikrotik_sign_certificate": lambda args: mikrotik_sign_certificate(
            args["cert_id"],
            args.get("ca")
        ),
        "mikrotik_import_certificate": lambda args: mikrotik_import_certificate(
            args["file_path"],
            args.get("passphrase"),
            args.get("name")
        ),
        "mikrotik_export_certificate": lambda args: mikrotik_export_certificate(
            args["cert_id"],
            args.get("file_name"),
            args.get("export_passphrase"),
            args.get("type_", "pem")
        ),
        "mikrotik_remove_certificate": lambda args: mikrotik_remove_certificate(
            args["cert_id"]
        ),
        "mikrotik_create_ca_certificate": lambda args: mikrotik_create_ca_certificate(
            args["name"],
            args["common_name"],
            args.get("key_size", 2048),
            args.get("days_valid", 3650),
            args.get("country"),
            args.get("organization")
        ),
        "mikrotik_revoke_certificate": lambda args: mikrotik_revoke_certificate(
            args["cert_id"]
        ),
        "mikrotik_trust_certificate": lambda args: mikrotik_trust_certificate(
            args["cert_id"]
        ),
        "mikrotik_get_certificate_fingerprint": lambda args: mikrotik_get_certificate_fingerprint(
            args["cert_id"]
        ),
    }

