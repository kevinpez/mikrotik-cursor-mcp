#!/usr/bin/env python3
"""
MikroTik Multi-Site Manager
Centralized management for multiple MikroTik routers

Usage:
    python site_manager.py status              # Show all sites status
    python site_manager.py health --all        # Health check
    python site_manager.py backup --all        # Backup all sites
    python site_manager.py firewall deploy     # Deploy firewall rules
"""

import sys
import os
from pathlib import Path

# Add parent directory to path to import MCP modules
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir / 'src'))

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from datetime import datetime

# Import our library modules
from lib.site_connector import SiteConnector
from lib.health_monitor import HealthMonitor
from lib.backup_manager import BackupManager
from lib.bulk_operations import BulkOperations

console = Console()

# CLI Groups
@click.group()
@click.version_option(version='1.0.0')
def cli():
    """
    MikroTik Multi-Site Manager
    
    Centralized management for multiple MikroTik routers across different locations.
    """
    pass

# =============================================================================
# STATUS COMMAND
# =============================================================================

@cli.command()
@click.option('--site', help='Specific site ID')
@click.option('--format', type=click.Choice(['table', 'json']), default='table')
def status(site, format):
    """Show connection status of all sites or specific site."""
    console.print("\n[bold cyan]Checking Site Status...[/bold cyan]\n")
    
    connector = SiteConnector()
    sites = connector.get_sites(site_id=site)
    
    if format == 'table':
        table = Table(title="Site Status", box=box.ROUNDED)
        table.add_column("Site ID", style="cyan")
        table.add_column("Name", style="white")
        table.add_column("Host", style="yellow")
        table.add_column("Status", style="bold")
        table.add_column("Last Check", style="dim")
        
        for site_id, site_data in sites.items():
            status = connector.check_connection(site_id)
            status_color = "green" if status['connected'] else "red"
            status_text = f"[{status_color}]{'●' if status['connected'] else '✗'}[/{status_color}]"
            
            table.add_row(
                site_id,
                site_data['name'],
                site_data['host'],
                status_text,
                status.get('last_check', 'Never')
            )
        
        console.print(table)
    else:
        # JSON output
        import json
        results = {}
        for site_id in sites.keys():
            results[site_id] = connector.check_connection(site_id)
        console.print_json(data=results)

# =============================================================================
# HEALTH COMMAND
# =============================================================================

@cli.command()
@click.option('--site', help='Specific site ID')
@click.option('--all', 'all_sites', is_flag=True, help='Check all sites')
@click.option('--format', type=click.Choice(['table', 'json', 'html']), default='table')
@click.option('--output', help='Output file (for HTML format)')
def health(site, all_sites, format, output):
    """Perform health check on sites."""
    console.print("\n[bold cyan]Running Health Checks...[/bold cyan]\n")
    
    monitor = HealthMonitor()
    
    if all_sites:
        results = monitor.check_all_sites()
    elif site:
        results = {site: monitor.check_site(site)}
    else:
        console.print("[red]Please specify --site or --all[/red]")
        return
    
    if format == 'table':
        _display_health_table(results)
    elif format == 'json':
        import json
        console.print_json(data=results)
    elif format == 'html':
        html_content = _generate_health_html(results)
        if output:
            with open(output, 'w') as f:
                f.write(html_content)
            console.print(f"[green]Health report saved to {output}[/green]")
        else:
            console.print(html_content)

def _display_health_table(results):
    """Display health check results in table format."""
    for site_id, health_data in results.items():
        # Create panel for each site
        if health_data.get('error'):
            panel_content = f"[red]Error: {health_data['error']}[/red]"
            panel_style = "red"
        else:
            cpu = health_data.get('cpu_load', 'N/A')
            memory_pct = health_data.get('memory_percent', 'N/A')
            uptime = health_data.get('uptime', 'N/A')
            
            panel_content = f"""
[cyan]CPU Load:[/cyan] {cpu}%
[cyan]Memory Used:[/cyan] {memory_pct}%
[cyan]Uptime:[/cyan] {uptime}
[cyan]Interfaces Up:[/cyan] {health_data.get('interfaces_up', 0)}/{health_data.get('total_interfaces', 0)}
[cyan]DHCP Leases:[/cyan] {health_data.get('dhcp_leases', 0)}
            """.strip()
            
            # Determine health status color
            if cpu > 80 or memory_pct > 90:
                panel_style = "red"
            elif cpu > 60 or memory_pct > 75:
                panel_style = "yellow"
            else:
                panel_style = "green"
        
        panel = Panel(
            panel_content,
            title=f"[bold]{site_id}[/bold]",
            border_style=panel_style,
            box=box.ROUNDED
        )
        console.print(panel)

def _generate_health_html(results):
    """Generate HTML health report."""
    from jinja2 import Template
    
    template = Template('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Multi-Site Health Report</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1 { color: #333; }
            .site { border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 5px; }
            .healthy { border-left: 5px solid green; }
            .warning { border-left: 5px solid orange; }
            .critical { border-left: 5px solid red; }
            .metric { margin: 5px 0; }
            .label { font-weight: bold; }
        </style>
    </head>
    <body>
        <h1>Multi-Site Health Report</h1>
        <p>Generated: {{ timestamp }}</p>
        {% for site_id, data in results.items() %}
        <div class="site {{ data.status_class }}">
            <h2>{{ site_id }}</h2>
            {% if data.error %}
            <p style="color: red;">Error: {{ data.error }}</p>
            {% else %}
            <div class="metric"><span class="label">CPU Load:</span> {{ data.cpu_load }}%</div>
            <div class="metric"><span class="label">Memory Used:</span> {{ data.memory_percent }}%</div>
            <div class="metric"><span class="label">Uptime:</span> {{ data.uptime }}</div>
            <div class="metric"><span class="label">Interfaces:</span> {{ data.interfaces_up }}/{{ data.total_interfaces }} Up</div>
            {% endif %}
        </div>
        {% endfor %}
    </body>
    </html>
    ''')
    
    # Add status class to each site
    for site_data in results.values():
        if site_data.get('error'):
            site_data['status_class'] = 'critical'
        elif site_data.get('cpu_load', 0) > 80 or site_data.get('memory_percent', 0) > 90:
            site_data['status_class'] = 'critical'
        elif site_data.get('cpu_load', 0) > 60 or site_data.get('memory_percent', 0) > 75:
            site_data['status_class'] = 'warning'
        else:
            site_data['status_class'] = 'healthy'
    
    return template.render(
        results=results,
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )

# =============================================================================
# BACKUP COMMAND
# =============================================================================

@cli.group()
def backup():
    """Backup management commands."""
    pass

@backup.command('create')
@click.option('--site', help='Specific site ID')
@click.option('--all', 'all_sites', is_flag=True, help='Backup all sites')
@click.option('--force', is_flag=True, help='Force backup even if one exists today')
def backup_create(site, all_sites, force):
    """Create backup for site(s)."""
    console.print("\n[bold cyan]Creating Backups...[/bold cyan]\n")
    
    backup_mgr = BackupManager()
    
    if all_sites:
        results = backup_mgr.backup_all_sites(force=force)
    elif site:
        results = {site: backup_mgr.backup_site(site, force=force)}
    else:
        console.print("[red]Please specify --site or --all[/red]")
        return
    
    # Display results
    table = Table(title="Backup Results", box=box.ROUNDED)
    table.add_column("Site", style="cyan")
    table.add_column("Status", style="bold")
    table.add_column("File", style="yellow")
    table.add_column("Size", style="white")
    
    for site_id, result in results.items():
        if result['success']:
            status = "[green]✓ Success[/green]"
            file_name = result.get('filename', 'N/A')
            size = result.get('size', 'N/A')
        else:
            status = "[red]✗ Failed[/red]"
            file_name = result.get('error', 'Unknown error')
            size = "N/A"
        
        table.add_row(site_id, status, file_name, size)
    
    console.print(table)

@backup.command('list')
@click.option('--site', help='Filter by site ID')
def backup_list(site):
    """List all backups."""
    backup_mgr = BackupManager()
    backups = backup_mgr.list_backups(site_id=site)
    
    table = Table(title="Available Backups", box=box.ROUNDED)
    table.add_column("Site", style="cyan")
    table.add_column("Date", style="yellow")
    table.add_column("File", style="white")
    table.add_column("Size", style="dim")
    
    for backup_info in backups:
        table.add_row(
            backup_info['site_id'],
            backup_info['date'],
            backup_info['filename'],
            backup_info['size']
        )
    
    console.print(table)

@backup.command('restore')
@click.argument('site')
@click.option('--date', help='Backup date (YYYY-MM-DD)')
@click.option('--file', help='Specific backup file')
@click.confirmation_option(prompt='Are you sure you want to restore? This will overwrite current config!')
def backup_restore(site, date, file):
    """Restore site from backup."""
    console.print(f"\n[bold yellow]Restoring {site} from backup...[/bold yellow]\n")
    
    backup_mgr = BackupManager()
    result = backup_mgr.restore_backup(site, date=date, filename=file)
    
    if result['success']:
        console.print(f"[green]✓ Successfully restored {site}[/green]")
    else:
        console.print(f"[red]✗ Failed to restore: {result.get('error')}[/red]")

# =============================================================================
# BULK OPERATIONS
# =============================================================================

@cli.group()
def bulk():
    """Bulk operations across sites."""
    pass

@bulk.command('execute')
@click.argument('command')
@click.option('--sites', help='Comma-separated site IDs or "all"')
@click.option('--group', help='Site group name')
def bulk_execute(command, sites, group):
    """Execute command on multiple sites."""
    console.print(f"\n[bold cyan]Executing: {command}[/bold cyan]\n")
    
    bulk_ops = BulkOperations()
    
    if sites == 'all':
        results = bulk_ops.execute_all(command)
    elif sites:
        site_list = [s.strip() for s in sites.split(',')]
        results = bulk_ops.execute_sites(command, site_list)
    elif group:
        results = bulk_ops.execute_group(command, group)
    else:
        console.print("[red]Please specify --sites or --group[/red]")
        return
    
    # Display results
    for site_id, result in results.items():
        panel_style = "green" if result.get('success') else "red"
        panel_content = result.get('output', result.get('error', 'No output'))
        
        panel = Panel(
            panel_content,
            title=f"[bold]{site_id}[/bold]",
            border_style=panel_style
        )
        console.print(panel)

# =============================================================================
# SITE MANAGEMENT
# =============================================================================

@cli.group()
def site():
    """Manage sites configuration."""
    pass

@site.command('add')
@click.argument('site_id')
@click.option('--name', prompt=True, help='Site name')
@click.option('--host', prompt=True, help='Router IP/hostname')
@click.option('--username', prompt=True, default='admin', help='SSH username')
@click.option('--password', prompt=True, hide_input=True, help='SSH password')
def site_add(site_id, name, host, username, password):
    """Add a new site to configuration."""
    connector = SiteConnector()
    
    # Test connection first
    console.print(f"\n[cyan]Testing connection to {host}...[/cyan]")
    test_result = connector.test_new_site(host, username, password)
    
    if not test_result['success']:
        console.print(f"[red]Connection failed: {test_result['error']}[/red]")
        return
    
    console.print("[green]✓ Connection successful![/green]")
    
    # Add to configuration
    connector.add_site(site_id, {
        'name': name,
        'host': host,
        'username': username,
        'password': password,
        'ssh_port': 22,
        'location': '',
        'priority': 'medium',
        'tags': []
    })
    
    console.print(f"[green]✓ Site '{site_id}' added successfully![/green]")

@site.command('remove')
@click.argument('site_id')
@click.confirmation_option(prompt='Are you sure you want to remove this site?')
def site_remove(site_id):
    """Remove a site from configuration."""
    connector = SiteConnector()
    connector.remove_site(site_id)
    console.print(f"[green]✓ Site '{site_id}' removed.[/green]")

@site.command('info')
@click.argument('site_id')
def site_info(site_id):
    """Show detailed information about a site."""
    connector = SiteConnector()
    site_data = connector.get_site(site_id)
    
    if not site_data:
        console.print(f"[red]Site '{site_id}' not found[/red]")
        return
    
    # Create info panel
    info_text = f"""
[cyan]Name:[/cyan] {site_data.get('name', 'N/A')}
[cyan]Host:[/cyan] {site_data.get('host', 'N/A')}
[cyan]Username:[/cyan] {site_data.get('username', 'N/A')}
[cyan]Location:[/cyan] {site_data.get('location', 'N/A')}
[cyan]Priority:[/cyan] {site_data.get('priority', 'N/A')}
[cyan]Tags:[/cyan] {', '.join(site_data.get('tags', []))}
    """.strip()
    
    panel = Panel(info_text, title=f"[bold]{site_id}[/bold]", border_style="cyan")
    console.print(panel)

# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':
    try:
        cli()
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[red]Error: {str(e)}[/red]")
        sys.exit(1)

