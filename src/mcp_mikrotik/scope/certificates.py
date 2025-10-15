from typing import Optional
from ..connector import execute_mikrotik_command
from ..logger import app_logger

def mikrotik_list_certificates(
    name_filter: Optional[str] = None,
    common_name_filter: Optional[str] = None,
    invalid_only: bool = False,
    expired_only: bool = False
) -> str:
    """
    Lists certificates on MikroTik device.
    
    Args:
        name_filter: Filter by certificate name
        common_name_filter: Filter by common name
        invalid_only: Show only invalid certificates
        expired_only: Show only expired certificates
    
    Returns:
        List of certificates
    """
    app_logger.info(f"Listing certificates: name_filter={name_filter}")
    
    cmd = "/certificate print detail"
    
    # Add filters
    filters = []
    if name_filter:
        filters.append(f'name~"{name_filter}"')
    if common_name_filter:
        filters.append(f'common-name~"{common_name_filter}"')
    if invalid_only:
        filters.append("invalid=yes")
    if expired_only:
        filters.append("expired=yes")
    
    if filters:
        cmd += " where " + " ".join(filters)
    
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "" or result.strip() == "no such item":
        return "No certificates found matching the criteria."
    
    return f"CERTIFICATES:\n\n{result}"

def mikrotik_get_certificate(cert_id: str) -> str:
    """
    Gets detailed information about a specific certificate.
    
    Args:
        cert_id: ID or name of the certificate
    
    Returns:
        Detailed information about the certificate
    """
    app_logger.info(f"Getting certificate details: cert_id={cert_id}")
    
    # Try by ID first
    cmd = f"/certificate print detail where .id={cert_id}"
    result = execute_mikrotik_command(cmd)
    
    # If not found by ID, try by name
    if not result or result.strip() == "":
        cmd = f'/certificate print detail where name="{cert_id}"'
        result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return f"Certificate with ID or name '{cert_id}' not found."
    
    return f"CERTIFICATE DETAILS:\n\n{result}"

def mikrotik_create_certificate(
    common_name: str,
    name: Optional[str] = None,
    key_size: int = 2048,
    days_valid: int = 365,
    country: Optional[str] = None,
    state: Optional[str] = None,
    locality: Optional[str] = None,
    organization: Optional[str] = None,
    unit: Optional[str] = None,
    subject_alt_name: Optional[str] = None,
    key_usage: Optional[str] = None
) -> str:
    """
    Creates a new certificate on MikroTik device.
    
    Args:
        common_name: Common name for the certificate
        name: Name for the certificate (defaults to common_name)
        key_size: Key size (1024, 2048, 4096)
        days_valid: Number of days the certificate is valid
        country: Country code (e.g., US, UK, DE)
        state: State or province
        locality: City or locality
        organization: Organization name
        unit: Organizational unit
        subject_alt_name: Subject alternative names (e.g., "DNS:example.com,DNS:www.example.com")
        key_usage: Key usage (e.g., "digital-signature,key-encipherment")
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Creating certificate: common_name={common_name}")
    
    if not common_name or common_name.strip() == "":
        return "Error: Common name cannot be empty."
    
    # Use common_name as name if name is not provided
    if not name:
        name = common_name.replace(".", "_").replace("*", "wildcard")
    
    # Build the command
    cmd = f'/certificate add name="{name}" common-name="{common_name}" key-size={key_size} days-valid={days_valid}'
    
    if country:
        cmd += f' country="{country}"'
    if state:
        cmd += f' state="{state}"'
    if locality:
        cmd += f' locality="{locality}"'
    if organization:
        cmd += f' organization="{organization}"'
    if unit:
        cmd += f' unit="{unit}"'
    if subject_alt_name:
        cmd += f' subject-alt-name="{subject_alt_name}"'
    if key_usage:
        cmd += f' key-usage={key_usage}'
    
    result = execute_mikrotik_command(cmd)
    
    # Check if creation was successful
    if result.strip():
        if "*" in result or result.strip().isdigit():
            cert_id = result.strip()
            # Sign the certificate
            sign_cmd = f'/certificate sign {cert_id}'
            sign_result = execute_mikrotik_command(sign_cmd)
            
            # Get the details
            details_cmd = f"/certificate print detail where .id={cert_id}"
            details = execute_mikrotik_command(details_cmd)
            
            if details.strip():
                return f"Certificate created and signed successfully:\n\n{details}"
            else:
                return f"Certificate created with ID: {result}"
        else:
            return f"Failed to create certificate: {result}"
    else:
        return "Certificate creation completed but unable to verify."

def mikrotik_sign_certificate(cert_id: str, ca: Optional[str] = None) -> str:
    """
    Signs a certificate.
    
    Args:
        cert_id: ID or name of the certificate to sign
        ca: CA certificate to sign with (optional, self-signs if not provided)
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Signing certificate: cert_id={cert_id}, ca={ca}")
    
    cmd = f"/certificate sign {cert_id}"
    
    if ca:
        cmd += f' ca="{ca}"'
    
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to sign certificate: {result}"
    
    return f"Certificate '{cert_id}' signed successfully."

def mikrotik_import_certificate(
    file_path: str,
    passphrase: Optional[str] = None,
    name: Optional[str] = None
) -> str:
    """
    Imports a certificate from a file.
    
    Args:
        file_path: Path to the certificate file on the router
        passphrase: Passphrase for encrypted certificates
        name: Name to assign to the certificate
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Importing certificate: file_path={file_path}")
    
    if not file_path or file_path.strip() == "":
        return "Error: File path cannot be empty."
    
    cmd = f'/certificate import file-name="{file_path}"'
    
    if passphrase:
        cmd += f' passphrase="{passphrase}"'
    if name:
        cmd += f' name="{name}"'
    
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to import certificate: {result}"
    
    return f"Certificate imported successfully from '{file_path}':\n\n{result}"

def mikrotik_export_certificate(
    cert_id: str,
    file_name: Optional[str] = None,
    export_passphrase: Optional[str] = None,
    type_: str = "pem"
) -> str:
    """
    Exports a certificate to a file.
    
    Args:
        cert_id: ID or name of the certificate to export
        file_name: Name for the exported file (optional)
        export_passphrase: Passphrase to encrypt the private key
        type_: Export type (pem or pkcs12)
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Exporting certificate: cert_id={cert_id}")
    
    cmd = f"/certificate export {cert_id}"
    
    if file_name:
        cmd += f' file-name="{file_name}"'
    
    if export_passphrase:
        cmd += f' export-passphrase="{export_passphrase}"'
    
    if type_:
        cmd += f" type={type_}"
    
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to export certificate: {result}"
    
    return f"Certificate '{cert_id}' exported successfully:\n\n{result}"

def mikrotik_remove_certificate(cert_id: str) -> str:
    """
    Removes a certificate from MikroTik device.
    
    Args:
        cert_id: ID or name of the certificate to remove
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Removing certificate: cert_id={cert_id}")
    
    # First check if the certificate exists
    check_cmd = f"/certificate print count-only where .id={cert_id}"
    count = execute_mikrotik_command(check_cmd)
    
    if count.strip() == "0":
        # Try by name
        check_cmd = f'/certificate print count-only where name="{cert_id}"'
        count = execute_mikrotik_command(check_cmd)
        
        if count.strip() == "0":
            return f"Certificate with ID or name '{cert_id}' not found."
    
    # Remove the certificate
    cmd = f"/certificate remove {cert_id}"
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to remove certificate: {result}"
    
    return f"Certificate '{cert_id}' removed successfully."

def mikrotik_create_ca_certificate(
    name: str,
    common_name: str,
    key_size: int = 2048,
    days_valid: int = 3650,
    country: Optional[str] = None,
    organization: Optional[str] = None
) -> str:
    """
    Creates a Certificate Authority (CA) certificate.
    
    Args:
        name: Name for the CA certificate
        common_name: Common name for the CA
        key_size: Key size (1024, 2048, 4096)
        days_valid: Number of days the CA is valid (default 10 years)
        country: Country code
        organization: Organization name
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Creating CA certificate: name={name}")
    
    # Create the CA certificate
    cmd = f'/certificate add name="{name}" common-name="{common_name}" key-size={key_size} days-valid={days_valid} key-usage=key-cert-sign,crl-sign'
    
    if country:
        cmd += f' country="{country}"'
    if organization:
        cmd += f' organization="{organization}"'
    
    result = execute_mikrotik_command(cmd)
    
    if result.strip() and ("*" in result or result.strip().isdigit()):
        cert_id = result.strip()
        
        # Sign the CA certificate (self-sign)
        sign_cmd = f'/certificate sign {cert_id} ca-crl-host=127.0.0.1'
        sign_result = execute_mikrotik_command(sign_cmd)
        
        # Get the details
        details_cmd = f"/certificate print detail where .id={cert_id}"
        details = execute_mikrotik_command(details_cmd)
        
        return f"CA certificate created successfully:\n\n{details}"
    else:
        return f"Failed to create CA certificate: {result}"

def mikrotik_revoke_certificate(cert_id: str) -> str:
    """
    Revokes a certificate.
    
    Args:
        cert_id: ID or name of the certificate to revoke
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Revoking certificate: cert_id={cert_id}")
    
    cmd = f"/certificate set {cert_id} trusted=no"
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to revoke certificate: {result}"
    
    return f"Certificate '{cert_id}' has been revoked (set to not trusted)."

def mikrotik_trust_certificate(cert_id: str) -> str:
    """
    Marks a certificate as trusted.
    
    Args:
        cert_id: ID or name of the certificate to trust
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Trusting certificate: cert_id={cert_id}")
    
    cmd = f"/certificate set {cert_id} trusted=yes"
    result = execute_mikrotik_command(cmd)
    
    if "failure:" in result.lower() or "error" in result.lower():
        return f"Failed to trust certificate: {result}"
    
    return f"Certificate '{cert_id}' has been marked as trusted."

def mikrotik_get_certificate_fingerprint(cert_id: str) -> str:
    """
    Gets the fingerprint of a certificate.
    
    Args:
        cert_id: ID or name of the certificate
    
    Returns:
        Certificate fingerprint
    """
    app_logger.info(f"Getting certificate fingerprint: cert_id={cert_id}")
    
    cmd = f'/certificate print detail where .id={cert_id} or name="{cert_id}"'
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "":
        return f"Certificate with ID or name '{cert_id}' not found."
    
    # Extract fingerprint from the output
    lines = result.split('\n')
    fingerprint_line = None
    for line in lines:
        if 'fingerprint' in line.lower():
            fingerprint_line = line
            break
    
    if fingerprint_line:
        return f"CERTIFICATE FINGERPRINT:\n\n{fingerprint_line.strip()}"
    else:
        return f"CERTIFICATE DETAILS:\n\n{result}"

