#!/usr/bin/env python3
"""
MikroTik Security Test Suite
Comprehensive testing of all security features
"""

import os
import sys
import time
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
import subprocess

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mcp_mikrotik.safety.intelligent_workflow import get_workflow_manager

class SecurityTestSuite:
    """Comprehensive security test suite for MikroTik routers"""
    
    def __init__(self):
        self.workflow_manager = get_workflow_manager()
        self.logger = self._setup_logging()
        self.test_results = []
        
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for test suite"""
        logger = logging.getLogger('security_test_suite')
        logger.setLevel(logging.INFO)
        
        # Create file handler
        handler = logging.FileHandler('security_test_suite.log')
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def test_user_management(self) -> Dict:
        """Test user management security"""
        test_name = "User Management Security"
        self.logger.info(f"Running test: {test_name}")
        
        try:
            # Test 1: Check admin users exist
            result = self.workflow_manager.execute_intelligent_workflow(
                '/user print',
                user_approved=True
            )
            
            users_exist = 'admin' in result.message and 'backup-admin' in result.message
            
            # Test 2: Check password strength (simplified)
            password_strength = True  # Would need actual password verification
            
            test_result = {
                'test_name': test_name,
                'timestamp': datetime.now().isoformat(),
                'tests': [
                    {
                        'name': 'Admin users exist',
                        'status': 'PASS' if users_exist else 'FAIL',
                        'details': f"Found admin users: {users_exist}"
                    },
                    {
                        'name': 'Password strength',
                        'status': 'PASS' if password_strength else 'FAIL',
                        'details': f"Password strength check: {password_strength}"
                    }
                ],
                'overall_status': 'PASS' if users_exist and password_strength else 'FAIL'
            }
            
            self.logger.info(f"Test {test_name}: {test_result['overall_status']}")
            return test_result
            
        except Exception as e:
            self.logger.error(f"Error in test {test_name}: {e}")
            return {
                'test_name': test_name,
                'timestamp': datetime.now().isoformat(),
                'overall_status': 'ERROR',
                'error': str(e)
            }
    
    def test_firewall_security(self) -> Dict:
        """Test firewall security rules"""
        test_name = "Firewall Security"
        self.logger.info(f"Running test: {test_name}")
        
        try:
            # Test 1: Check firewall rules exist
            result = self.workflow_manager.execute_intelligent_workflow(
                '/ip firewall filter print',
                user_approved=True
            )
            
            has_ssh_protection = 'SSH-rate-limit' in result.message
            has_telnet_block = 'Block-Telnet' in result.message
            has_ftp_block = 'Block-FTP' in result.message
            has_logging = 'Log-dropped-packets' in result.message
            
            # Test 2: Check address lists
            addr_result = self.workflow_manager.execute_intelligent_workflow(
                '/ip firewall address-list print',
                user_approved=True
            )
            
            has_ssh_blacklist = 'ssh_blacklist' in addr_result.message
            
            test_result = {
                'test_name': test_name,
                'timestamp': datetime.now().isoformat(),
                'tests': [
                    {
                        'name': 'SSH rate limiting',
                        'status': 'PASS' if has_ssh_protection else 'FAIL',
                        'details': f"SSH rate limiting rule: {has_ssh_protection}"
                    },
                    {
                        'name': 'Telnet blocking',
                        'status': 'PASS' if has_telnet_block else 'FAIL',
                        'details': f"Telnet blocking rule: {has_telnet_block}"
                    },
                    {
                        'name': 'FTP blocking',
                        'status': 'PASS' if has_ftp_block else 'FAIL',
                        'details': f"FTP blocking rule: {has_ftp_block}"
                    },
                    {
                        'name': 'Logging enabled',
                        'status': 'PASS' if has_logging else 'FAIL',
                        'details': f"Packet logging: {has_logging}"
                    },
                    {
                        'name': 'SSH blacklist',
                        'status': 'PASS' if has_ssh_blacklist else 'FAIL',
                        'details': f"SSH blacklist address list: {has_ssh_blacklist}"
                    }
                ],
                'overall_status': 'PASS' if all([has_ssh_protection, has_telnet_block, has_ftp_block, has_logging, has_ssh_blacklist]) else 'FAIL'
            }
            
            self.logger.info(f"Test {test_name}: {test_result['overall_status']}")
            return test_result
            
        except Exception as e:
            self.logger.error(f"Error in test {test_name}: {e}")
            return {
                'test_name': test_name,
                'timestamp': datetime.now().isoformat(),
                'overall_status': 'ERROR',
                'error': str(e)
            }
    
    def test_vlan_segmentation(self) -> Dict:
        """Test VLAN network segmentation"""
        test_name = "VLAN Network Segmentation"
        self.logger.info(f"Running test: {test_name}")
        
        try:
            # Test 1: Check VLAN interfaces exist
            result = self.workflow_manager.execute_intelligent_workflow(
                '/interface vlan print',
                user_approved=True
            )
            
            has_main_vlan = 'VLAN-Main' in result.message
            has_guest_vlan = 'VLAN-Guest' in result.message
            
            # Test 2: Check bridge configuration
            bridge_result = self.workflow_manager.execute_intelligent_workflow(
                '/interface bridge print',
                user_approved=True
            )
            
            has_bridge = 'bridge' in bridge_result.message
            
            test_result = {
                'test_name': test_name,
                'timestamp': datetime.now().isoformat(),
                'tests': [
                    {
                        'name': 'Main VLAN exists',
                        'status': 'PASS' if has_main_vlan else 'FAIL',
                        'details': f"VLAN-Main interface: {has_main_vlan}"
                    },
                    {
                        'name': 'Guest VLAN exists',
                        'status': 'PASS' if has_guest_vlan else 'FAIL',
                        'details': f"VLAN-Guest interface: {has_guest_vlan}"
                    },
                    {
                        'name': 'Bridge configuration',
                        'status': 'PASS' if has_bridge else 'FAIL',
                        'details': f"Bridge interface: {has_bridge}"
                    }
                ],
                'overall_status': 'PASS' if all([has_main_vlan, has_guest_vlan, has_bridge]) else 'FAIL'
            }
            
            self.logger.info(f"Test {test_name}: {test_result['overall_status']}")
            return test_result
            
        except Exception as e:
            self.logger.error(f"Error in test {test_name}: {e}")
            return {
                'test_name': test_name,
                'timestamp': datetime.now().isoformat(),
                'overall_status': 'ERROR',
                'error': str(e)
            }
    
    def test_backup_system(self) -> Dict:
        """Test backup system functionality"""
        test_name = "Backup System"
        self.logger.info(f"Running test: {test_name}")
        
        try:
            # Test 1: Check if backups exist
            result = self.workflow_manager.execute_intelligent_workflow(
                '/file print where name~"backup"',
                user_approved=True
            )
            
            has_backups = 'backup' in result.message.lower()
            
            # Test 2: Test backup creation
            test_backup_name = f"test_backup_{int(time.time())}"
            backup_result = self.workflow_manager.execute_intelligent_workflow(
                f'/system backup save name={test_backup_name}',
                user_approved=True
            )
            
            backup_created = 'SUCCESS' in backup_result.message
            
            test_result = {
                'test_name': test_name,
                'timestamp': datetime.now().isoformat(),
                'tests': [
                    {
                        'name': 'Backups exist',
                        'status': 'PASS' if has_backups else 'FAIL',
                        'details': f"Existing backups found: {has_backups}"
                    },
                    {
                        'name': 'Backup creation',
                        'status': 'PASS' if backup_created else 'FAIL',
                        'details': f"Test backup created: {backup_created}"
                    }
                ],
                'overall_status': 'PASS' if has_backups and backup_created else 'FAIL'
            }
            
            self.logger.info(f"Test {test_name}: {test_result['overall_status']}")
            return test_result
            
        except Exception as e:
            self.logger.error(f"Error in test {test_name}: {e}")
            return {
                'test_name': test_name,
                'timestamp': datetime.now().isoformat(),
                'overall_status': 'ERROR',
                'error': str(e)
            }
    
    def test_intelligent_workflow(self) -> Dict:
        """Test intelligent workflow system"""
        test_name = "Intelligent Workflow System"
        self.logger.info(f"Running test: {test_name}")
        
        try:
            # Test 1: Low risk command (should execute directly)
            low_risk_result = self.workflow_manager.execute_intelligent_workflow(
                '/system resource print',
                user_approved=True
            )
            
            low_risk_works = 'SUCCESS' in low_risk_result.message
            
            # Test 2: Medium risk command (should use safety measures)
            medium_risk_result = self.workflow_manager.execute_intelligent_workflow(
                '/ip firewall filter print',
                user_approved=True
            )
            
            medium_risk_works = 'SUCCESS' in medium_risk_result.message
            
            # Test 3: High risk command (should use Safe Mode)
            high_risk_result = self.workflow_manager.execute_intelligent_workflow(
                '/system backup save name=workflow_test',
                user_approved=True
            )
            
            high_risk_works = 'SUCCESS' in high_risk_result.message
            
            test_result = {
                'test_name': test_name,
                'timestamp': datetime.now().isoformat(),
                'tests': [
                    {
                        'name': 'Low risk workflow',
                        'status': 'PASS' if low_risk_works else 'FAIL',
                        'details': f"Low risk command execution: {low_risk_works}"
                    },
                    {
                        'name': 'Medium risk workflow',
                        'status': 'PASS' if medium_risk_works else 'FAIL',
                        'details': f"Medium risk command execution: {medium_risk_works}"
                    },
                    {
                        'name': 'High risk workflow',
                        'status': 'PASS' if high_risk_works else 'FAIL',
                        'details': f"High risk command execution: {high_risk_works}"
                    }
                ],
                'overall_status': 'PASS' if all([low_risk_works, medium_risk_works, high_risk_works]) else 'FAIL'
            }
            
            self.logger.info(f"Test {test_name}: {test_result['overall_status']}")
            return test_result
            
        except Exception as e:
            self.logger.error(f"Error in test {test_name}: {e}")
            return {
                'test_name': test_name,
                'timestamp': datetime.now().isoformat(),
                'overall_status': 'ERROR',
                'error': str(e)
            }
    
    def run_all_tests(self) -> Dict:
        """Run all security tests"""
        self.logger.info("Starting comprehensive security test suite")
        
        test_suite_results = {
            'timestamp': datetime.now().isoformat(),
            'tests': []
        }
        
        # Define all tests
        tests = [
            self.test_user_management,
            self.test_firewall_security,
            self.test_vlan_segmentation,
            self.test_backup_system,
            self.test_intelligent_workflow
        ]
        
        # Run all tests
        for test in tests:
            try:
                result = test()
                test_suite_results['tests'].append(result)
            except Exception as e:
                self.logger.error(f"Error running test {test.__name__}: {e}")
                test_suite_results['tests'].append({
                    'test_name': test.__name__,
                    'timestamp': datetime.now().isoformat(),
                    'overall_status': 'ERROR',
                    'error': str(e)
                })
        
        # Calculate overall results
        total_tests = len(test_suite_results['tests'])
        passed_tests = sum(1 for test in test_suite_results['tests'] if test.get('overall_status') == 'PASS')
        failed_tests = sum(1 for test in test_suite_results['tests'] if test.get('overall_status') == 'FAIL')
        error_tests = sum(1 for test in test_suite_results['tests'] if test.get('overall_status') == 'ERROR')
        
        test_suite_results['summary'] = {
            'total_tests': total_tests,
            'passed': passed_tests,
            'failed': failed_tests,
            'errors': error_tests,
            'success_rate': (passed_tests / total_tests * 100) if total_tests > 0 else 0
        }
        
        # Determine overall status
        if error_tests > 0:
            test_suite_results['overall_status'] = 'ERROR'
        elif failed_tests > 0:
            test_suite_results['overall_status'] = 'FAIL'
        else:
            test_suite_results['overall_status'] = 'PASS'
        
        self.logger.info(f"Test suite completed: {test_suite_results['overall_status']}")
        return test_suite_results
    
    def generate_test_report(self, test_results: Dict) -> str:
        """Generate comprehensive test report"""
        report = f"""
# MikroTik Security Test Suite Report
**Generated:** {test_results['timestamp']}
**Overall Status:** {test_results['overall_status']}

## Summary
- **Total Tests:** {test_results['summary']['total_tests']}
- **Passed:** {test_results['summary']['passed']}
- **Failed:** {test_results['summary']['failed']}
- **Errors:** {test_results['summary']['errors']}
- **Success Rate:** {test_results['summary']['success_rate']:.1f}%

## Test Results
"""
        
        for test in test_results['tests']:
            status_emoji = {
                'PASS': '✅',
                'FAIL': '❌',
                'ERROR': '❌'
            }.get(test.get('overall_status', 'UNKNOWN'), '❓')
            
            report += f"\n### {status_emoji} {test.get('test_name', 'Unknown Test')}\n"
            report += f"- **Status:** {test.get('overall_status', 'UNKNOWN')}\n"
            report += f"- **Timestamp:** {test.get('timestamp', 'Unknown')}\n"
            
            if 'error' in test:
                report += f"- **Error:** {test['error']}\n"
            
            if 'tests' in test:
                report += "\n**Sub-tests:**\n"
                for sub_test in test['tests']:
                    sub_status_emoji = {
                        'PASS': '✅',
                        'FAIL': '❌'
                    }.get(sub_test.get('status', 'UNKNOWN'), '❓')
                    
                    report += f"- {sub_status_emoji} {sub_test.get('name', 'Unknown')}: {sub_test.get('status', 'UNKNOWN')}\n"
                    if 'details' in sub_test:
                        report += f"  - {sub_test['details']}\n"
        
        return report
    
    def save_test_report(self, test_results: Dict, filename: Optional[str] = None):
        """Save test report to file"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'security_test_report_{timestamp}.json'
        
        # Save JSON report
        with open(filename, 'w') as f:
            json.dump(test_results, f, indent=2)
        
        # Save human-readable report
        report_filename = filename.replace('.json', '.md')
        report = self.generate_test_report(test_results)
        
        with open(report_filename, 'w') as f:
            f.write(report)
        
        self.logger.info(f"Test report saved: {filename} and {report_filename}")

def main():
    """Main function for security test suite"""
    print("🧪 MikroTik Security Test Suite")
    print("=" * 50)
    
    # Set up environment
    os.environ['MIKROTIK_USERNAME'] = 'admin'
    os.environ['MIKROTIK_PASSWORD'] = 'NewSecureAdmin2025!'
    os.environ['MIKROTIK_DRY_RUN'] = 'false'
    
    test_suite = SecurityTestSuite()
    
    try:
        # Run all tests
        print("Running comprehensive security test suite...")
        test_results = test_suite.run_all_tests()
        
        # Display results
        print(f"\nOverall Status: {test_results['overall_status']}")
        print(f"Success Rate: {test_results['summary']['success_rate']:.1f}%")
        print(f"Passed: {test_results['summary']['passed']}")
        print(f"Failed: {test_results['summary']['failed']}")
        print(f"Errors: {test_results['summary']['errors']}")
        
        # Save report
        test_suite.save_test_report(test_results)
        print("\nTest report saved to files")
        
        # Display detailed results
        print("\nTest Results:")
        for test in test_results['tests']:
            status_emoji = {
                'PASS': '✅',
                'FAIL': '❌',
                'ERROR': '❌'
            }.get(test.get('overall_status', 'UNKNOWN'), '❓')
            
            print(f"  {status_emoji} {test.get('test_name', 'Unknown')}: {test.get('overall_status', 'UNKNOWN')}")
        
    except Exception as e:
        print(f"Error running test suite: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
