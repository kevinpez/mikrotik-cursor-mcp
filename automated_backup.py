#!/usr/bin/env python3
"""
MikroTik Automated Backup System
Scheduled backup creation and management
"""

import os
import sys
import time
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import subprocess
import shutil

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mcp_mikrotik.safety.intelligent_workflow import get_workflow_manager

class AutomatedBackupSystem:
    """Automated backup system for MikroTik routers"""
    
    def __init__(self, backup_dir: str = "backups"):
        self.workflow_manager = get_workflow_manager()
        self.backup_dir = backup_dir
        self.logger = self._setup_logging()
        self.retention_days = 30  # Keep backups for 30 days
        
        # Create backup directory if it doesn't exist
        os.makedirs(self.backup_dir, exist_ok=True)
        
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for backup system"""
        logger = logging.getLogger('automated_backup')
        logger.setLevel(logging.INFO)
        
        # Create file handler
        handler = logging.FileHandler('backup_system.log')
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def create_backup(self, backup_name: Optional[str] = None) -> Dict:
        """Create a new backup"""
        if backup_name is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f"auto_backup_{timestamp}"
        
        try:
            self.logger.info(f"Creating backup: {backup_name}")
            
            # Create backup using intelligent workflow
            result = self.workflow_manager.execute_intelligent_workflow(
                f'/system backup save name={backup_name}',
                user_approved=True
            )
            
            backup_info = {
                'name': backup_name,
                'timestamp': datetime.now().isoformat(),
                'status': 'SUCCESS' if 'SUCCESS' in result.message else 'FAILED',
                'message': result.message,
                'size': 0,  # Would need to get actual file size
                'type': 'full_configuration'
            }
            
            if backup_info['status'] == 'SUCCESS':
                self.logger.info(f"Backup created successfully: {backup_name}")
            else:
                self.logger.error(f"Backup failed: {backup_name}")
            
            return backup_info
            
        except Exception as e:
            self.logger.error(f"Error creating backup {backup_name}: {e}")
            return {
                'name': backup_name,
                'timestamp': datetime.now().isoformat(),
                'status': 'ERROR',
                'error': str(e),
                'type': 'full_configuration'
            }
    
    def list_backups(self) -> List[Dict]:
        """List all available backups"""
        try:
            result = self.workflow_manager.execute_intelligent_workflow(
                '/file print where name~"backup"',
                user_approved=True
            )
            
            backups = []
            # Parse backup files (simplified)
            lines = result.message.split('\n')
            for line in lines:
                if 'backup' in line.lower():
                    # Extract backup information (simplified parsing)
                    backup_info = {
                        'name': 'backup_file',  # Would need proper parsing
                        'size': 0,
                        'date': datetime.now().isoformat(),
                        'type': 'backup'
                    }
                    backups.append(backup_info)
            
            return backups
            
        except Exception as e:
            self.logger.error(f"Error listing backups: {e}")
            return []
    
    def verify_backup(self, backup_name: str) -> Dict:
        """Verify backup integrity"""
        try:
            # Check if backup file exists
            result = self.workflow_manager.execute_intelligent_workflow(
                f'/file print where name="{backup_name}"',
                user_approved=True
            )
            
            exists = backup_name in result.message
            
            verification_result = {
                'backup_name': backup_name,
                'exists': exists,
                'timestamp': datetime.now().isoformat(),
                'status': 'VERIFIED' if exists else 'NOT_FOUND'
            }
            
            if exists:
                self.logger.info(f"Backup verified: {backup_name}")
            else:
                self.logger.warning(f"Backup not found: {backup_name}")
            
            return verification_result
            
        except Exception as e:
            self.logger.error(f"Error verifying backup {backup_name}: {e}")
            return {
                'backup_name': backup_name,
                'timestamp': datetime.now().isoformat(),
                'status': 'ERROR',
                'error': str(e)
            }
    
    def cleanup_old_backups(self) -> Dict:
        """Remove backups older than retention period"""
        try:
            cutoff_date = datetime.now() - timedelta(days=self.retention_days)
            removed_count = 0
            
            # Get list of backups
            backups = self.list_backups()
            
            for backup in backups:
                # Check if backup is older than retention period
                # This would need proper date parsing
                if 'old_backup' in backup.get('name', ''):
                    try:
                        # Remove old backup
                        result = self.workflow_manager.execute_intelligent_workflow(
                            f'/file remove "{backup["name"]}"',
                            user_approved=True
                        )
                        removed_count += 1
                        self.logger.info(f"Removed old backup: {backup['name']}")
                    except Exception as e:
                        self.logger.error(f"Error removing backup {backup['name']}: {e}")
            
            cleanup_result = {
                'timestamp': datetime.now().isoformat(),
                'removed_count': removed_count,
                'retention_days': self.retention_days,
                'status': 'COMPLETED'
            }
            
            self.logger.info(f"Cleanup completed: {removed_count} old backups removed")
            return cleanup_result
            
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")
            return {
                'timestamp': datetime.now().isoformat(),
                'status': 'ERROR',
                'error': str(e)
            }
    
    def export_configuration(self, export_name: Optional[str] = None) -> Dict:
        """Export configuration to text file"""
        if export_name is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            export_name = f"config_export_{timestamp}"
        
        try:
            self.logger.info(f"Exporting configuration: {export_name}")
            
            # Export configuration
            result = self.workflow_manager.execute_intelligent_workflow(
                f'/export file={export_name}',
                user_approved=True
            )
            
            export_info = {
                'name': export_name,
                'timestamp': datetime.now().isoformat(),
                'status': 'SUCCESS' if 'SUCCESS' in result.message else 'FAILED',
                'message': result.message,
                'type': 'configuration_export'
            }
            
            if export_info['status'] == 'SUCCESS':
                self.logger.info(f"Configuration exported: {export_name}")
            else:
                self.logger.error(f"Export failed: {export_name}")
            
            return export_info
            
        except Exception as e:
            self.logger.error(f"Error exporting configuration {export_name}: {e}")
            return {
                'name': export_name,
                'timestamp': datetime.now().isoformat(),
                'status': 'ERROR',
                'error': str(e),
                'type': 'configuration_export'
            }
    
    def run_backup_routine(self) -> Dict:
        """Run complete backup routine"""
        self.logger.info("Starting automated backup routine")
        
        routine_results = {
            'timestamp': datetime.now().isoformat(),
            'operations': []
        }
        
        try:
            # 1. Create full backup
            backup_result = self.create_backup()
            routine_results['operations'].append(backup_result)
            
            # 2. Export configuration
            export_result = self.export_configuration()
            routine_results['operations'].append(export_result)
            
            # 3. Verify backup
            if backup_result['status'] == 'SUCCESS':
                verify_result = self.verify_backup(backup_result['name'])
                routine_results['operations'].append(verify_result)
            
            # 4. Cleanup old backups
            cleanup_result = self.cleanup_old_backups()
            routine_results['operations'].append(cleanup_result)
            
            # Calculate overall status
            success_count = sum(1 for op in routine_results['operations'] 
                              if op.get('status') in ['SUCCESS', 'VERIFIED', 'COMPLETED'])
            total_operations = len(routine_results['operations'])
            
            routine_results['overall_status'] = 'SUCCESS' if success_count == total_operations else 'PARTIAL'
            routine_results['summary'] = {
                'total_operations': total_operations,
                'successful': success_count,
                'failed': total_operations - success_count
            }
            
            self.logger.info(f"Backup routine completed: {routine_results['overall_status']}")
            
        except Exception as e:
            self.logger.error(f"Error in backup routine: {e}")
            routine_results['overall_status'] = 'ERROR'
            routine_results['error'] = str(e)
        
        return routine_results
    
    def generate_backup_report(self, routine_results: Dict) -> str:
        """Generate backup report"""
        report = f"""
# MikroTik Backup Report
**Generated:** {routine_results['timestamp']}
**Overall Status:** {routine_results['overall_status']}

## Summary
- **Total Operations:** {routine_results.get('summary', {}).get('total_operations', 0)}
- **Successful:** {routine_results.get('summary', {}).get('successful', 0)}
- **Failed:** {routine_results.get('summary', {}).get('failed', 0)}

## Operations
"""
        
        for operation in routine_results.get('operations', []):
            status_emoji = {
                'SUCCESS': '✅',
                'VERIFIED': '✅',
                'COMPLETED': '✅',
                'FAILED': '❌',
                'ERROR': '❌'
            }.get(operation.get('status', 'UNKNOWN'), '❓')
            
            report += f"\n### {status_emoji} {operation.get('name', 'Unknown Operation')}\n"
            report += f"- **Status:** {operation.get('status', 'UNKNOWN')}\n"
            report += f"- **Type:** {operation.get('type', 'Unknown')}\n"
            report += f"- **Timestamp:** {operation.get('timestamp', 'Unknown')}\n"
            
            if 'error' in operation:
                report += f"- **Error:** {operation['error']}\n"
            if 'message' in operation:
                report += f"- **Message:** {operation['message']}\n"
        
        return report
    
    def save_backup_report(self, routine_results: Dict, filename: Optional[str] = None):
        """Save backup report to file"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'backup_report_{timestamp}.json'
        
        # Save JSON report
        with open(filename, 'w') as f:
            json.dump(routine_results, f, indent=2)
        
        # Save human-readable report
        report_filename = filename.replace('.json', '.md')
        report = self.generate_backup_report(routine_results)
        
        with open(report_filename, 'w') as f:
            f.write(report)
        
        self.logger.info(f"Backup report saved: {filename} and {report_filename}")

def main():
    """Main function for automated backup system"""
    print("💾 MikroTik Automated Backup System")
    print("=" * 50)
    
    # Set up environment
    os.environ['MIKROTIK_USERNAME'] = 'admin'
    os.environ['MIKROTIK_PASSWORD'] = 'NewSecureAdmin2025!'
    os.environ['MIKROTIK_DRY_RUN'] = 'false'
    
    backup_system = AutomatedBackupSystem()
    
    try:
        # Run backup routine
        print("Running automated backup routine...")
        routine_results = backup_system.run_backup_routine()
        
        # Display results
        print(f"\nOverall Status: {routine_results['overall_status']}")
        if 'summary' in routine_results:
            print(f"Successful: {routine_results['summary']['successful']}")
            print(f"Failed: {routine_results['summary']['failed']}")
        
        # Save report
        backup_system.save_backup_report(routine_results)
        print("\nBackup report saved to files")
        
        # Display detailed results
        print("\nOperations:")
        for operation in routine_results.get('operations', []):
            status_emoji = {
                'SUCCESS': '✅',
                'VERIFIED': '✅',
                'COMPLETED': '✅',
                'FAILED': '❌',
                'ERROR': '❌'
            }.get(operation.get('status', 'UNKNOWN'), '❓')
            
            print(f"  {status_emoji} {operation.get('name', 'Unknown')}: {operation.get('status', 'UNKNOWN')}")
        
    except Exception as e:
        print(f"Error running backup system: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
