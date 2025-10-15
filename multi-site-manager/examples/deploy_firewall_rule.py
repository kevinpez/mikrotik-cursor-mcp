#!/usr/bin/env python3
"""
Example: Deploy Firewall Rule Across Multiple Sites

This example shows how to deploy a consistent firewall rule
across all your sites.
"""
import sys
from pathlib import Path

# Add parent lib directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.bulk_operations import BulkOperations
from rich.console import Console
from rich.table import Table

console = Console()

def deploy_block_malicious_ips():
    """Deploy rule to block known malicious IP ranges."""
    
    console.print("\n[bold cyan]Deploying Firewall Rule: Block RFC1918 from WAN[/bold cyan]\n")
    
    # Define the rule
    rule_config = {
        'chain': 'input',
        'action': 'drop',
        'src-address-list': 'rfc1918',
        'in-interface': 'ether1',  # Adjust to your WAN interface
        'comment': 'Block RFC1918 from WAN (security)'
    }
    
    # Deploy to all sites
    bulk_ops = BulkOperations()
    results = bulk_ops.deploy_firewall_rule(rule_config)
    
    # Display results
    table = Table(title="Firewall Deployment Results")
    table.add_column("Site", style="cyan")
    table.add_column("Status", style="bold")
    table.add_column("Details", style="dim")
    
    for site_id, result in results.items():
        if result.get('success'):
            status = "[green]✓ Success[/green]"
            details = "Rule deployed"
        else:
            status = "[red]✗ Failed[/red]"
            details = result.get('error', 'Unknown error')
        
        table.add_row(site_id, status, details)
    
    console.print(table)

def deploy_allow_management():
    """Deploy rule to allow management access from specific network."""
    
    console.print("\n[bold cyan]Deploying Firewall Rule: Allow Management Access[/bold cyan]\n")
    
    # Define the rule
    rule_config = {
        'chain': 'input',
        'action': 'accept',
        'src-address': '192.168.1.0/24',  # Your management network
        'protocol': 'tcp',
        'dst-port': '22,8291',  # SSH and Winbox
        'comment': 'Allow management from trusted network'
    }
    
    # Deploy to all production sites only
    bulk_ops = BulkOperations()
    results = bulk_ops.execute_by_tag('production', 
                                      bulk_ops._build_firewall_command(rule_config))
    
    console.print(f"[green]Deployed to {len(results)} production sites[/green]")

def deploy_basic_security_rules():
    """Deploy a set of basic security rules to all sites."""
    
    console.print("\n[bold cyan]Deploying Basic Security Ruleset[/bold cyan]\n")
    
    rules = [
        {
            'chain': 'input',
            'action': 'accept',
            'connection-state': 'established,related,untracked',
            'comment': 'Accept established/related connections'
        },
        {
            'chain': 'input',
            'action': 'drop',
            'connection-state': 'invalid',
            'comment': 'Drop invalid connections'
        },
        {
            'chain': 'input',
            'action': 'accept',
            'protocol': 'icmp',
            'comment': 'Accept ICMP'
        }
    ]
    
    bulk_ops = BulkOperations()
    
    for i, rule in enumerate(rules, 1):
        console.print(f"\nDeploying rule {i}/{len(rules)}: {rule['comment']}")
        results = bulk_ops.deploy_firewall_rule(rule)
        
        success_count = sum(1 for r in results.values() if r.get('success'))
        console.print(f"  ✓ {success_count}/{len(results)} sites")

if __name__ == '__main__':
    console.print("\n[bold]MikroTik Multi-Site Firewall Deployment[/bold]\n")
    
    # Show menu
    console.print("Select deployment option:")
    console.print("1. Block RFC1918 from WAN")
    console.print("2. Allow management access")
    console.print("3. Deploy basic security ruleset")
    console.print("4. Exit")
    
    choice = input("\nEnter choice (1-4): ")
    
    if choice == '1':
        deploy_block_malicious_ips()
    elif choice == '2':
        deploy_allow_management()
    elif choice == '3':
        deploy_basic_security_rules()
    elif choice == '4':
        console.print("[yellow]Exiting...[/yellow]")
        sys.exit(0)
    else:
        console.print("[red]Invalid choice![/red]")
        sys.exit(1)
    
    console.print("\n[green]Deployment complete![/green]\n")

