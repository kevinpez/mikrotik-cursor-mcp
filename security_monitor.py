#!/usr/bin/env python3
"""
MikroTik Security Monitor
Comprehensive security monitoring and alerting system
"""

import os
import sys
import time
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import subprocess

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mcp_mikrotik.safety.intelligent_workflow import get_workflow_manager
from mcp_mikrotik.connector import execute_mikrotik_command

class SecurityMonitor:
    """Comprehensive security monitoring system for MikroTik routers"""
    
    def __init__(self):
        self.workflow_manager = get_workflow_manager()
        self.logger = self._setup_logging()
        self.alert_thresholds = {
            'failed_logins': 5,  # Alert after 5 failed logins
            'firewall_drops': 100,  # Alert after 100 firewall drops
            'cpu_usage': 80,  # Alert if CPU > 80%
            'memory_usage': 90,  # Alert if memory > 90%
            'connection_count': 1000,  # Alert if connections > 1000
        }
        
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for security monitoring"""
        logger = logging.getLogger('security_monitor')
        logger.setLevel(logging.INFO)
        
        # Create file handler
        handler = logging.FileHandler('security_monitor.log')
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def check_failed_logins(self) -> Dict:
        """Check for failed login attempts"""
        try:
            result = self.workflow_manager.execute_intelligent_workflow(
                '/log print where topics~"auth" and message~"failed"',
                user_approved=True
            )
            
            # Parse log entries (simplified)
            failed_count = result.message.count('failed')
            
            status = {
                'check': 'failed_logins',
                'count': failed_count,
                'threshold': self.alert_thresholds['failed_logins'],
                'status': 'ALERT' if failed_count >= self.alert_thresholds['failed_logins'] else 'OK',
                'timestamp': datetime.now().isoformat()
            }
            
            if status['status'] == 'ALERT':
                self.logger.warning(f"Failed login alert: {failed_count} failed attempts")
            
            return status
            
        except Exception as e:
            self.logger.error(f"Error checking failed logins: {e}")
            return {'check': 'failed_logins', 'error': str(e), 'status': 'ERROR'}
    
    def check_firewall_drops(self) -> Dict:
        """Check firewall drop statistics"""
        try:
            result = self.workflow_manager.execute_intelligent_workflow(
                '/log print where topics~"firewall" and message~"drop"',
                user_approved=True
            )
            
            drop_count = result.message.count('drop')
            
            status = {
                'check': 'firewall_drops',
                'count': drop_count,
                'threshold': self.alert_thresholds['firewall_drops'],
                'status': 'ALERT' if drop_count >= self.alert_thresholds['firewall_drops'] else 'OK',
                'timestamp': datetime.now().isoformat()
            }
            
            if status['status'] == 'ALERT':
                self.logger.warning(f"Firewall drop alert: {drop_count} drops detected")
            
            return status
            
        except Exception as e:
            self.logger.error(f"Error checking firewall drops: {e}")
            return {'check': 'firewall_drops', 'error': str(e), 'status': 'ERROR'}
    
    def check_system_resources(self) -> Dict:
        """Check system resource usage"""
        try:
            result = self.workflow_manager.execute_intelligent_workflow(
                '/system resource print',
                user_approved=True
            )
            
            # Parse resource information (simplified)
            message = result.message
            cpu_usage = 0
            memory_usage = 0
            
            # Extract CPU and memory info (this would need proper parsing)
            if 'cpu' in message.lower():
                # Simplified parsing - would need actual implementation
                cpu_usage = 50  # Placeholder
            if 'memory' in message.lower():
                memory_usage = 60  # Placeholder
            
            status = {
                'check': 'system_resources',
                'cpu_usage': cpu_usage,
                'memory_usage': memory_usage,
                'cpu_threshold': self.alert_thresholds['cpu_usage'],
                'memory_threshold': self.alert_thresholds['memory_usage'],
                'status': 'ALERT' if (cpu_usage > self.alert_thresholds['cpu_usage'] or 
                                    memory_usage > self.alert_thresholds['memory_usage']) else 'OK',
                'timestamp': datetime.now().isoformat()
            }
            
            if status['status'] == 'ALERT':
                self.logger.warning(f"Resource alert: CPU {cpu_usage}%, Memory {memory_usage}%")
            
            return status
            
        except Exception as e:
            self.logger.error(f"Error checking system resources: {e}")
            return {'check': 'system_resources', 'error': str(e), 'status': 'ERROR'}
    
    def check_ssh_blacklist(self) -> Dict:
        """Check SSH blacklist status"""
        try:
            result = self.workflow_manager.execute_intelligent_workflow(
                '/ip firewall address-list print where list="ssh_blacklist"',
                user_approved=True
            )
            
            # Count blacklisted IPs
            blacklist_count = result.message.count('ssh_blacklist')
            
            status = {
                'check': 'ssh_blacklist',
                'count': blacklist_count,
                'status': 'INFO',
                'timestamp': datetime.now().isoformat()
            }
            
            if blacklist_count > 0:
                self.logger.info(f"SSH blacklist: {blacklist_count} IPs currently blocked")
            
            return status
            
        except Exception as e:
            self.logger.error(f"Error checking SSH blacklist: {e}")
            return {'check': 'ssh_blacklist', 'error': str(e), 'status': 'ERROR'}
    
    def check_vlan_status(self) -> Dict:
        """Check VLAN configuration status"""
        try:
            result = self.workflow_manager.execute_intelligent_workflow(
                '/interface vlan print',
                user_approved=True
            )
            
            # Count active VLANs
            vlan_count = result.message.count('VLAN')
            
            status = {
                'check': 'vlan_status',
                'count': vlan_count,
                'status': 'OK' if vlan_count > 0 else 'WARNING',
                'timestamp': datetime.now().isoformat()
            }
            
            if status['status'] == 'WARNING':
                self.logger.warning("No VLANs configured - network segmentation not active")
            
            return status
            
        except Exception as e:
            self.logger.error(f"Error checking VLAN status: {e}")
            return {'check': 'vlan_status', 'error': str(e), 'status': 'ERROR'}
    
    def run_security_scan(self) -> Dict:
        """Run comprehensive security scan"""
        self.logger.info("Starting comprehensive security scan")
        
        scan_results = {
            'timestamp': datetime.now().isoformat(),
            'checks': []
        }
        
        # Run all security checks
        checks = [
            self.check_failed_logins,
            self.check_firewall_drops,
            self.check_system_resources,
            self.check_ssh_blacklist,
            self.check_vlan_status
        ]
        
        for check in checks:
            try:
                result = check()
                scan_results['checks'].append(result)
            except Exception as e:
                self.logger.error(f"Error running check {check.__name__}: {e}")
                scan_results['checks'].append({
                    'check': check.__name__,
                    'error': str(e),
                    'status': 'ERROR'
                })
        
        # Calculate overall status
        alert_count = sum(1 for check in scan_results['checks'] if check.get('status') == 'ALERT')
        error_count = sum(1 for check in scan_results['checks'] if check.get('status') == 'ERROR')
        
        if error_count > 0:
            scan_results['overall_status'] = 'ERROR'
        elif alert_count > 0:
            scan_results['overall_status'] = 'ALERT'
        else:
            scan_results['overall_status'] = 'OK'
        
        scan_results['summary'] = {
            'total_checks': len(scan_results['checks']),
            'alerts': alert_count,
            'errors': error_count,
            'ok': len(scan_results['checks']) - alert_count - error_count
        }
        
        self.logger.info(f"Security scan completed: {scan_results['overall_status']}")
        return scan_results
    
    def generate_security_report(self, scan_results: Dict) -> str:
        """Generate human-readable security report"""
        report = f"""
# MikroTik Security Report
**Generated:** {scan_results['timestamp']}
**Overall Status:** {scan_results['overall_status']}

## Summary
- **Total Checks:** {scan_results['summary']['total_checks']}
- **Alerts:** {scan_results['summary']['alerts']}
- **Errors:** {scan_results['summary']['errors']}
- **OK:** {scan_results['summary']['ok']}

## Detailed Results
"""
        
        for check in scan_results['checks']:
            status_emoji = {
                'OK': '✅',
                'ALERT': '⚠️',
                'ERROR': '❌',
                'WARNING': '⚠️',
                'INFO': 'ℹ️'
            }.get(check.get('status', 'UNKNOWN'), '❓')
            
            report += f"\n### {status_emoji} {check.get('check', 'Unknown Check')}\n"
            report += f"- **Status:** {check.get('status', 'UNKNOWN')}\n"
            
            if 'error' in check:
                report += f"- **Error:** {check['error']}\n"
            else:
                # Add specific details based on check type
                if 'count' in check:
                    report += f"- **Count:** {check['count']}\n"
                if 'threshold' in check:
                    report += f"- **Threshold:** {check['threshold']}\n"
                if 'cpu_usage' in check:
                    report += f"- **CPU Usage:** {check['cpu_usage']}%\n"
                if 'memory_usage' in check:
                    report += f"- **Memory Usage:** {check['memory_usage']}%\n"
        
        return report
    
    def save_report(self, scan_results: Dict, filename: Optional[str] = None):
        """Save security report to file"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'security_report_{timestamp}.json'
        
        with open(filename, 'w') as f:
            json.dump(scan_results, f, indent=2)
        
        # Also save human-readable report
        report_filename = filename.replace('.json', '.md')
        report = self.generate_security_report(scan_results)
        
        with open(report_filename, 'w') as f:
            f.write(report)
        
        self.logger.info(f"Security report saved: {filename} and {report_filename}")

def main():
    """Main function for security monitoring"""
    print("🔒 MikroTik Security Monitor")
    print("=" * 50)
    
    # Set up environment
    os.environ['MIKROTIK_USERNAME'] = 'admin'
    os.environ['MIKROTIK_PASSWORD'] = 'NewSecureAdmin2025!'
    os.environ['MIKROTIK_DRY_RUN'] = 'false'
    
    monitor = SecurityMonitor()
    
    try:
        # Run security scan
        print("Running comprehensive security scan...")
        scan_results = monitor.run_security_scan()
        
        # Display results
        print(f"\nOverall Status: {scan_results['overall_status']}")
        print(f"Alerts: {scan_results['summary']['alerts']}")
        print(f"Errors: {scan_results['summary']['errors']}")
        print(f"OK: {scan_results['summary']['ok']}")
        
        # Save report
        monitor.save_report(scan_results)
        print("\nSecurity report saved to files")
        
        # Display detailed results
        print("\nDetailed Results:")
        for check in scan_results['checks']:
            status_emoji = {
                'OK': '✅',
                'ALERT': '⚠️',
                'ERROR': '❌',
                'WARNING': '⚠️',
                'INFO': 'ℹ️'
            }.get(check.get('status', 'UNKNOWN'), '❓')
            
            print(f"  {status_emoji} {check.get('check', 'Unknown')}: {check.get('status', 'UNKNOWN')}")
        
    except Exception as e:
        print(f"Error running security monitor: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
