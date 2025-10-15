#!/usr/bin/env python3
"""
Example: Deploy Firewall Rules Across Multiple Sites

This example shows how to deploy consistent firewall rules
across all your sites for standardized security.

Usage:
    python deploy_firewall_rule.py

Features:
    - Interactive menu for different rule types
    - Deploy to all sites or specific groups
    - Pre-configured security rules
    - Easy to customize for your needs
"""

import sys
from pathlib import Path

# Add parent lib directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.bulk_operations import BulkOperations
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


def show_results(title, results):
    """Display deployment results in a table."""
    table = Table(title=title)
    table.add_column("Site", style="cyan")
    table.add_column("Status", style="bold")
    table.add_column("Details", style="dim")
    
    for site_id, result in results.items():
        if result.get('success'):
            status = "[green]✓ Success[/green]"
            details = "Rule deployed"
        else:
            status = "[red]✗ Failed[/red]"
            details = result.get('error', 'Unknown error')[:50]
        
        table.add_row(site_id, status, details)
    
    console.print(table)


def deploy_accept_established():
    """Deploy rule to accept established/related connections."""
    console.print("\n[bold cyan]Deploying: Accept Established/Related Connections[/bold cyan]")
    
    rule = {
        'chain': 'input',
        'action': 'accept',
        'connection-state': 'established,related,untracked',
        'comment': 'Accept established/related connections'
    }
    
    # Note: connection-state needs special handling in command
    cmd = f'/ip firewall filter add chain={rule["chain"]} action={rule["action"]} connection-state={rule["connection-state"]} comment="{rule["comment"]}"'
    
    bulk_ops = BulkOperations()
    results = bulk_ops.execute_all(cmd)
    
    show_results("Deployment Results", results)


def deploy_drop_invalid():
    """Deploy rule to drop invalid connections."""
    console.print("\n[bold cyan]Deploying: Drop Invalid Connections[/bold cyan]")
    
    rule = {
        'chain': 'input',
        'action': 'drop',
        'connection-state': 'invalid',
        'comment': 'Drop invalid connections'
    }
    
    cmd = f'/ip firewall filter add chain={rule["chain"]} action={rule["action"]} connection-state={rule["connection-state"]} comment="{rule["comment"]}"'
    
    bulk_ops = BulkOperations()
    results = bulk_ops.execute_all(cmd)
    
    show_results("Deployment Results", results)


def deploy_accept_icmp():
    """Deploy rule to accept ICMP (ping)."""
    console.print("\n[bold cyan]Deploying: Accept ICMP[/bold cyan]")
    
    rule = {
        'chain': 'input',
        'action': 'accept',
        'protocol': 'icmp',
        'comment': 'Accept ICMP (ping)'
    }
    
    bulk_ops = BulkOperations()
    results = bulk_ops.deploy_firewall_rule(rule)
    
    show_results("Deployment Results", results)


def deploy_allow_management():
    """Deploy rule to allow management access from trusted network."""
    console.print("\n[bold cyan]Deploying: Allow Management Access[/bold cyan]")
    console.print("[yellow]Note: Update src-address to match your management network[/yellow]\n")
    
    # Customize this for your network!
    management_network = "192.168.1.0/24"  # <-- CHANGE THIS
    
    rule = {
        'chain': 'input',
        'action': 'accept',
        'src-address': management_network,
        'protocol': 'tcp',
        'dst-port': '22,8291',  # SSH and Winbox
        'comment': 'Allow management from trusted network'
    }
    
    bulk_ops = BulkOperations()
    results = bulk_ops.deploy_firewall_rule(rule)
    
    show_results("Deployment Results", results)


def deploy_basic_security_set():
    """Deploy a basic security rule set."""
    console.print("\n[bold cyan]Deploying: Basic Security Rule Set[/bold cyan]")
    console.print("This will add 3 rules: Accept established, Drop invalid, Accept ICMP\n")
    
    rules = [
        ('Accept established/related', 'connection-state=established,related,untracked'),
        ('Drop invalid', 'connection-state=invalid'),
        ('Accept ICMP', 'protocol=icmp'),
    ]
    
    bulk_ops = BulkOperations()
    
    for i, (description, rule_part) in enumerate(rules, 1):
        console.print(f"\n[{i}/3] {description}")
        
        if 'connection-state' in rule_part:
            state = rule_part.split('=')[1]
            action = 'accept' if 'established' in state else 'drop'
            cmd = f'/ip firewall filter add chain=input action={action} {rule_part} comment="{description}"'
        else:
            cmd = f'/ip firewall filter add chain=input action=accept {rule_part} comment="{description}"'
        
        results = bulk_ops.execute_all(cmd)
        
        success_count = sum(1 for r in results.values() if r.get('success'))
        console.print(f"  ✓ Deployed to {success_count}/{len(results)} sites")
    
    console.print("\n[green]Basic security rule set deployment complete![/green]")


def show_menu():
    """Display the main menu."""
    panel = Panel(
        """
[bold]Choose a firewall rule deployment:[/bold]

[cyan]1.[/cyan] Accept Established/Related Connections
[cyan]2.[/cyan] Drop Invalid Connections
[cyan]3.[/cyan] Accept ICMP (ping)
[cyan]4.[/cyan] Allow Management Access (SSH + Winbox)
[cyan]5.[/cyan] Deploy Basic Security Rule Set (all above)
[cyan]6.[/cyan] Exit

[dim]Note: Rules are deployed to ALL sites. Test on a lab first![/dim]
        """,
        title="[bold]MikroTik Multi-Site Firewall Deployment[/bold]",
        border_style="cyan"
    )
    console.print(panel)


def main():
    """Main function."""
    console.clear()
    
    while True:
        show_menu()
        
        choice = console.input("\n[bold]Enter choice (1-6):[/bold] ").strip()
        
        try:
            if choice == '1':
                deploy_accept_established()
            elif choice == '2':
                deploy_drop_invalid()
            elif choice == '3':
                deploy_accept_icmp()
            elif choice == '4':
                deploy_allow_management()
            elif choice == '5':
                deploy_basic_security_set()
            elif choice == '6':
                console.print("\n[yellow]Exiting...[/yellow]\n")
                break
            else:
                console.print("\n[red]Invalid choice! Please enter 1-6.[/red]")
                continue
            
            # Ask if user wants to continue
            again = console.input("\n[bold]Deploy another rule? (y/n):[/bold] ").strip().lower()
            if again != 'y':
                console.print("\n[green]Done![/green]\n")
                break
                
            console.clear()
            
        except KeyboardInterrupt:
            console.print("\n\n[yellow]Operation cancelled by user[/yellow]\n")
            break
        except Exception as e:
            console.print(f"\n[red]Error: {str(e)}[/red]\n")
            continue


if __name__ == '__main__':
    main()
