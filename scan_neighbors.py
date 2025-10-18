#!/usr/bin/env python3
"""
Quick MikroTik Neighbor Scanner
Simple script to scan for MikroTik devices and populate site configuration
"""

import os
import sys
from pathlib import Path

# Add the multi-site-manager directory to path
sys.path.insert(0, str(Path(__file__).parent / 'multi-site-manager'))

from lib.neighbor_scanner import MikroTikNeighborScanner
from rich.console import Console

console = Console()

def main():
    """Main function for quick neighbor scanning."""
    console.print("[bold cyan]MikroTik Network Neighbor Scanner[/bold cyan]")
    console.print("=" * 50)
    
    # Get router connection details
    router_host = input("Enter router IP/hostname: ").strip()
    if not router_host:
        console.print("[red]Router host is required[/red]")
        return 1
    
    username = input("Enter username (default: admin): ").strip() or "admin"
    password = input("Enter password: ").strip()
    if not password:
        console.print("[red]Password is required[/red]")
        return 1
    
    port = input("Enter SSH port (default: 22): ").strip()
    port = int(port) if port.isdigit() else 22
    
    # Initialize scanner
    scanner = MikroTikNeighborScanner()
    
    try:
        # Perform scan
        console.print(f"\n[bold cyan]Scanning for MikroTik neighbors from {router_host}...[/bold cyan]\n")
        scan_result = scanner.scan_from_router(router_host, username, password, port)
        
        # Display results
        scanner.display_scan_results(scan_result)
        
        if scan_result['mikrotik_devices']:
            # Ask if user wants to populate site config
            populate = input("\nDo you want to populate the site configuration? (y/N): ").strip().lower()
            
            if populate in ['y', 'yes']:
                default_password = input("Enter default password for discovered devices (or press Enter for 'changeme'): ").strip()
                
                console.print(f"\n[bold yellow]Populating site configuration...[/bold yellow]")
                population_result = scanner.populate_site_config(
                    scan_result['mikrotik_devices'],
                    username,
                    default_password or 'changeme'
                )
                
                scanner.display_population_results(population_result)
                
                console.print(f"\n[green]✓ Site configuration updated![/green]")
                console.print(f"[dim]You can now use the multi-site manager to manage these devices.[/dim]")
        else:
            console.print(f"\n[yellow]No MikroTik devices found on the network.[/yellow]")
        
        return 0
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        return 1

if __name__ == '__main__':
    sys.exit(main())
