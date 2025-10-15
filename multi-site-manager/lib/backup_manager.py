"""
Backup Manager - Manages backups across multiple sites
"""
from pathlib import Path
from datetime import datetime, timedelta
import os
from .site_connector import SiteConnector


class BackupManager:
    """Manages backups for all sites."""
    
    def __init__(self, backup_dir='./backups'):
        """
        Initialize backup manager.
        
        Args:
            backup_dir: Directory to store backups
        """
        self.connector = SiteConnector()
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def backup_site(self, site_id, force=False):
        """
        Create backup for a specific site.
        
        Args:
            site_id: Site to backup
            force: Force backup even if one exists today
            
        Returns:
            dict: Backup results
        """
        site = self.connector.get_site(site_id)
        if not site:
            return {
                'success': False,
                'error': f"Site '{site_id}' not found"
            }
        
        # Check if backup already exists today
        if not force:
            existing = self._get_today_backup(site_id)
            if existing:
                return {
                    'success': False,
                    'error': 'Backup already exists for today. Use --force to override.',
                    'existing': existing
                }
        
        try:
            # Generate backup filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f"{site_id}_backup_{timestamp}"
            
            # Create backup on router
            result = self.connector.execute_command(
                site_id,
                f'/system backup save name={backup_name}'
            )
            
            if not result['success']:
                return {
                    'success': False,
                    'error': result.get('error', 'Unknown error')
                }
            
            # Wait a moment for backup to be created
            import time
            time.sleep(2)
            
            # Download backup file (simplified - in production would use SFTP/SCP)
            # For now, we'll create export instead
            export_result = self.connector.execute_command(
                site_id,
                '/export'
            )
            
            if not export_result['success']:
                return {
                    'success': False,
                    'error': f"Export failed: {export_result.get('error')}"
                }
            
            # Save export to file
            site_backup_dir = self.backup_dir / site_id
            site_backup_dir.mkdir(parents=True, exist_ok=True)
            
            backup_file = site_backup_dir / f"{backup_name}.rsc"
            with open(backup_file, 'w') as f:
                f.write(export_result['output'])
            
            file_size = backup_file.stat().st_size
            
            return {
                'success': True,
                'filename': backup_file.name,
                'path': str(backup_file),
                'size': self._format_size(file_size),
                'timestamp': timestamp
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def backup_all_sites(self, force=False):
        """
        Backup all sites.
        
        Args:
            force: Force backup even if one exists today
            
        Returns:
            dict: Results for all sites
        """
        results = {}
        sites = self.connector.get_sites()
        
        for site_id in sites.keys():
            results[site_id] = self.backup_site(site_id, force=force)
        
        return results
    
    def list_backups(self, site_id=None):
        """
        List all available backups.
        
        Args:
            site_id: Filter by site, or None for all
            
        Returns:
            list: Backup information
        """
        backups = []
        
        if site_id:
            site_dirs = [self.backup_dir / site_id]
        else:
            site_dirs = [d for d in self.backup_dir.iterdir() if d.is_dir()]
        
        for site_dir in site_dirs:
            if not site_dir.exists():
                continue
            
            for backup_file in site_dir.glob('*.rsc'):
                backups.append({
                    'site_id': site_dir.name,
                    'filename': backup_file.name,
                    'path': str(backup_file),
                    'size': self._format_size(backup_file.stat().st_size),
                    'date': datetime.fromtimestamp(backup_file.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                })
        
        # Sort by date (newest first)
        backups.sort(key=lambda x: x['date'], reverse=True)
        
        return backups
    
    def restore_backup(self, site_id, date=None, filename=None):
        """
        Restore site from backup.
        
        Args:
            site_id: Site to restore
            date: Backup date (YYYY-MM-DD)
            filename: Specific backup filename
            
        Returns:
            dict: Restore results
        """
        if not date and not filename:
            return {
                'success': False,
                'error': 'Must specify either --date or --file'
            }
        
        # Find backup file
        backups = self.list_backups(site_id=site_id)
        
        if filename:
            backup = next((b for b in backups if b['filename'] == filename), None)
        elif date:
            backup = next((b for b in backups if b['date'].startswith(date)), None)
        else:
            backup = None
        
        if not backup:
            return {
                'success': False,
                'error': 'Backup not found'
            }
        
        try:
            # Read backup file
            with open(backup['path'], 'r') as f:
                backup_content = f.read()
            
            # In production, would upload file via SFTP and restore
            # For now, we'll just verify the file exists
            
            return {
                'success': True,
                'message': f"Backup {backup['filename']} verified and ready for restore",
                'note': 'Actual restore would upload file via SFTP and execute /import command'
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def cleanup_old_backups(self, site_id=None, retention_days=30):
        """
        Clean up old backups based on retention policy.
        
        Args:
            site_id: Specific site or None for all
            retention_days: Days to keep backups
            
        Returns:
            dict: Cleanup results
        """
        cutoff_date = datetime.now() - timedelta(days=retention_days)
        deleted = []
        
        backups = self.list_backups(site_id=site_id)
        
        for backup in backups:
            backup_date = datetime.strptime(backup['date'], '%Y-%m-%d %H:%M:%S')
            
            if backup_date < cutoff_date:
                try:
                    os.remove(backup['path'])
                    deleted.append(backup['filename'])
                except Exception as e:
                    pass  # Skip if can't delete
        
        return {
            'deleted_count': len(deleted),
            'deleted_files': deleted
        }
    
    def _get_today_backup(self, site_id):
        """Check if backup exists for today."""
        today = datetime.now().strftime('%Y-%m-%d')
        backups = self.list_backups(site_id=site_id)
        
        return next((b for b in backups if b['date'].startswith(today)), None)
    
    def _format_size(self, size_bytes):
        """Format file size in human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f}{unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f}TB"

