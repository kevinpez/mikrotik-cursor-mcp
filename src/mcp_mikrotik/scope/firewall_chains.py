from typing import Optional, List
from ..connector import execute_mikrotik_command
from ..api_fallback import api_fallback_execute
from ..logger import app_logger

def mikrotik_list_custom_chains(chain_type: str = "filter") -> str:
    """
    Lists all custom chains in use for a given chain type.
    
    Args:
        chain_type: Type of chain (filter, nat, mangle, raw)
    
    Returns:
        List of custom chains
    """
    app_logger.info(f"Listing custom chains for {chain_type}")
    
    valid_types = ["filter", "nat", "mangle", "raw"]
    if chain_type not in valid_types:
        return f"Error: Invalid chain type '{chain_type}'. Must be one of: {', '.join(valid_types)}"
    
    # Get all rules with action=jump to identify custom chains
    if chain_type == "filter":
        cmd = "/ip firewall filter print terse where action=jump"
    elif chain_type == "nat":
        cmd = "/ip firewall nat print terse where action=jump"
    elif chain_type == "mangle":
        cmd = "/ip firewall mangle print terse where action=jump"
    else:  # raw
        cmd = "/ip firewall raw print terse where action=jump"
    
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "" or result.strip() == "no such item":
        return f"No custom chains found for {chain_type}."
    
    # Extract unique jump targets (custom chain names)
    custom_chains = set()
    for line in result.split('\n'):
        if 'jump-target=' in line:
            # Extract chain name
            parts = line.split('jump-target=')
            if len(parts) > 1:
                chain_name = parts[1].split()[0].strip('"')
                custom_chains.add(chain_name)
    
    if not custom_chains:
        return f"No custom chains found for {chain_type}."
    
    return f"CUSTOM CHAINS ({chain_type.upper()}):\n\n" + "\n".join(sorted(custom_chains))

def mikrotik_create_jump_rule(
    chain_type: str,
    source_chain: str,
    target_chain: str,
    src_address: Optional[str] = None,
    dst_address: Optional[str] = None,
    protocol: Optional[str] = None,
    src_port: Optional[str] = None,
    dst_port: Optional[str] = None,
    in_interface: Optional[str] = None,
    out_interface: Optional[str] = None,
    comment: Optional[str] = None,
    place_before: Optional[str] = None
) -> str:
    """
    Creates a jump rule to redirect traffic to a custom chain.
    
    Args:
        chain_type: Type of chain (filter, nat, mangle, raw)
        source_chain: Source chain to jump from (input, forward, output, etc.)
        target_chain: Target custom chain name to jump to
        src_address: Source IP address filter
        dst_address: Destination IP address filter
        protocol: Protocol filter
        src_port: Source port filter
        dst_port: Destination port filter
        in_interface: Input interface filter
        out_interface: Output interface filter
        comment: Optional comment
        place_before: Place this rule before another rule (by number)
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Creating jump rule: {source_chain} -> {target_chain} ({chain_type})")
    
    valid_types = ["filter", "nat", "mangle", "raw"]
    if chain_type not in valid_types:
        return f"Error: Invalid chain type '{chain_type}'. Must be one of: {', '.join(valid_types)}"
    
    if not target_chain or target_chain.strip() == "":
        return "Error: Target chain name cannot be empty."
    
    # Build the command based on chain type
    if chain_type == "filter":
        cmd = f'/ip firewall filter add chain={source_chain} action=jump jump-target="{target_chain}"'
    elif chain_type == "nat":
        cmd = f'/ip firewall nat add chain={source_chain} action=jump jump-target="{target_chain}"'
    elif chain_type == "mangle":
        cmd = f'/ip firewall mangle add chain={source_chain} action=jump jump-target="{target_chain}"'
    else:  # raw
        cmd = f'/ip firewall raw add chain={source_chain} action=jump jump-target="{target_chain}"'
    
    # Add optional filters
    if src_address:
        cmd += f" src-address={src_address}"
    if dst_address:
        cmd += f" dst-address={dst_address}"
    if protocol:
        cmd += f" protocol={protocol}"
    if src_port:
        cmd += f" src-port={src_port}"
    if dst_port:
        cmd += f" dst-port={dst_port}"
    if in_interface:
        cmd += f' in-interface="{in_interface}"'
    if out_interface:
        cmd += f' out-interface="{out_interface}"'
    if comment:
        cmd += f' comment="{comment}"'
    if place_before:
        cmd += f" place-before={place_before}"
    
    result = execute_mikrotik_command(cmd)
    
    # Check if creation was successful
    if result.strip():
        if "*" in result or result.strip().isdigit():
            return f"Jump rule created successfully. Traffic from '{source_chain}' will now jump to '{target_chain}'"
        else:
            return f"Failed to create jump rule: {result}"
    else:
        return f"Jump rule creation completed for '{target_chain}' chain."

def mikrotik_list_rules_in_chain(chain_type: str, chain_name: str) -> str:
    """
    Lists all rules in a specific chain.
    
    Args:
        chain_type: Type of chain (filter, nat, mangle, raw)
        chain_name: Name of the chain
    
    Returns:
        List of rules in the chain
    """
    app_logger.info(f"Listing rules in chain: {chain_name} ({chain_type})")
    
    valid_types = ["filter", "nat", "mangle", "raw"]
    if chain_type not in valid_types:
        return f"Error: Invalid chain type '{chain_type}'. Must be one of: {', '.join(valid_types)}"
    
    # Build the command
    if chain_type == "filter":
        cmd = f'/ip firewall filter print detail where chain="{chain_name}"'
    elif chain_type == "nat":
        cmd = f'/ip firewall nat print detail where chain="{chain_name}"'
    elif chain_type == "mangle":
        cmd = f'/ip firewall mangle print detail where chain="{chain_name}"'
    else:  # raw
        cmd = f'/ip firewall raw print detail where chain="{chain_name}"'
    
    result = execute_mikrotik_command(cmd)
    
    if not result or result.strip() == "" or result.strip() == "no such item":
        return f"No rules found in chain '{chain_name}' ({chain_type})."
    
    return f"RULES IN CHAIN '{chain_name}' ({chain_type.upper()}):\n\n{result}"

def mikrotik_delete_custom_chain(chain_type: str, chain_name: str) -> str:
    """
    Deletes all rules in a custom chain and removes jump rules to it.
    
    Args:
        chain_type: Type of chain (filter, nat, mangle, raw)
        chain_name: Name of the custom chain to delete
    
    Returns:
        Command output or error message
    """
    app_logger.info(f"Deleting custom chain: {chain_name} ({chain_type})")
    
    valid_types = ["filter", "nat", "mangle", "raw"]
    if chain_type not in valid_types:
        return f"Error: Invalid chain type '{chain_type}'. Must be one of: {', '.join(valid_types)}"
    
    results = []
    
    # Step 1: Remove all rules IN the custom chain
    if chain_type == "filter":
        cmd1 = f'/ip firewall filter remove [find chain="{chain_name}"]'
    elif chain_type == "nat":
        cmd1 = f'/ip firewall nat remove [find chain="{chain_name}"]'
    elif chain_type == "mangle":
        cmd1 = f'/ip firewall mangle remove [find chain="{chain_name}"]'
    else:  # raw
        cmd1 = f'/ip firewall raw remove [find chain="{chain_name}"]'
    
    result1 = execute_mikrotik_command(cmd1)
    results.append(f"Removed rules in chain '{chain_name}': {result1 if result1 else 'Success'}")
    
    # Step 2: Remove jump rules TO the custom chain
    if chain_type == "filter":
        cmd2 = f'/ip firewall filter remove [find action=jump jump-target="{chain_name}"]'
    elif chain_type == "nat":
        cmd2 = f'/ip firewall nat remove [find action=jump jump-target="{chain_name}"]'
    elif chain_type == "mangle":
        cmd2 = f'/ip firewall mangle remove [find action=jump jump-target="{chain_name}"]'
    else:  # raw
        cmd2 = f'/ip firewall raw remove [find action=jump jump-target="{chain_name}"]'
    
    result2 = execute_mikrotik_command(cmd2)
    results.append(f"Removed jump rules to '{chain_name}': {result2 if result2 else 'Success'}")
    
    return f"CUSTOM CHAIN DELETION RESULTS:\n\n" + "\n".join(results)

def mikrotik_create_custom_chain_with_rules(
    chain_type: str,
    source_chain: str,
    custom_chain_name: str,
    rules: List[dict],
    match_criteria: Optional[dict] = None
) -> str:
    """
    Creates a complete custom chain with jump rule and rules inside it.
    
    Args:
        chain_type: Type of chain (filter, nat, mangle, raw)
        source_chain: Source chain to jump from (input, forward, output, etc.)
        custom_chain_name: Name of the custom chain
        rules: List of rule dictionaries with action and parameters
        match_criteria: Optional criteria for the jump rule (src_address, dst_address, etc.)
    
    Returns:
        Setup result
    """
    app_logger.info(f"Creating custom chain: {custom_chain_name} ({chain_type})")
    
    valid_types = ["filter", "nat", "mangle", "raw"]
    if chain_type not in valid_types:
        return f"Error: Invalid chain type '{chain_type}'. Must be one of: {', '.join(valid_types)}"
    
    results = []
    
    # Step 1: Create jump rule to custom chain
    jump_comment = f"Jump to custom chain: {custom_chain_name}"
    match_criteria = match_criteria or {}
    
    jump_result = mikrotik_create_jump_rule(
        chain_type=chain_type,
        source_chain=source_chain,
        target_chain=custom_chain_name,
        src_address=match_criteria.get("src_address"),
        dst_address=match_criteria.get("dst_address"),
        protocol=match_criteria.get("protocol"),
        src_port=match_criteria.get("src_port"),
        dst_port=match_criteria.get("dst_port"),
        in_interface=match_criteria.get("in_interface"),
        out_interface=match_criteria.get("out_interface"),
        comment=jump_comment
    )
    results.append(f"✓ Jump rule: {jump_result}")
    
    # Step 2: Create rules in custom chain
    for idx, rule in enumerate(rules, 1):
        action = rule.get("action", "accept")
        comment = rule.get("comment", f"Rule {idx} in {custom_chain_name}")
        
        # Build command based on chain type
        if chain_type == "filter":
            cmd = f'/ip firewall filter add chain="{custom_chain_name}" action={action}'
        elif chain_type == "nat":
            cmd = f'/ip firewall nat add chain="{custom_chain_name}" action={action}'
        elif chain_type == "mangle":
            cmd = f'/ip firewall mangle add chain="{custom_chain_name}" action={action}'
        else:  # raw
            cmd = f'/ip firewall raw add chain="{custom_chain_name}" action={action}'
        
        # Add rule parameters
        for key, value in rule.items():
            if key not in ["action", "comment"] and value:
                if key in ["in_interface", "out_interface", "jump_target"]:
                    cmd += f' {key.replace("_", "-")}="{value}"'
                else:
                    cmd += f' {key.replace("_", "-")}={value}'
        
        cmd += f' comment="{comment}"'
        
        result = execute_mikrotik_command(cmd)
        if "*" in result or not result.strip() or result.strip().isdigit():
            results.append(f"✓ Rule {idx}: {comment}")
        else:
            results.append(f"✗ Rule {idx}: {result}")
    
    return f"CUSTOM CHAIN CREATION RESULTS:\n\n" + "\n".join(results)

