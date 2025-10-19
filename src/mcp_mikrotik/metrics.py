"""
Prometheus metrics exporter for MikroTik MCP operations.
Provides production-ready monitoring and observability.
"""
import time
import threading
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from collections import defaultdict, Counter
import json
from .logger import app_logger


@dataclass
class MetricValue:
    """Represents a metric value with labels."""
    name: str
    value: float
    labels: Dict[str, str]
    timestamp: float


class PrometheusMetrics:
    """Prometheus metrics collector for MikroTik MCP operations."""
    
    def __init__(self):
        self._metrics: Dict[str, List[MetricValue]] = defaultdict(list)
        self._lock = threading.Lock()
        self._start_time = time.time()
        
        # Initialize default metrics
        self._initialize_default_metrics()
    
    def _initialize_default_metrics(self):
        """Initialize default system metrics."""
        self._add_metric("mikrotik_mcp_start_time_seconds", 
                        time.time(), {"version": "4.8.0"})
    
    def _add_metric(self, name: str, value: float, labels: Dict[str, str] = None):
        """Add a metric value."""
        if labels is None:
            labels = {}
        
        with self._lock:
            self._metrics[name].append(MetricValue(
                name=name,
                value=value,
                labels=labels,
                timestamp=time.time()
            ))
    
    def increment_counter(self, name: str, labels: Dict[str, str] = None, value: float = 1.0):
        """Increment a counter metric."""
        self._add_metric(name, value, labels)
    
    def set_gauge(self, name: str, value: float, labels: Dict[str, str] = None):
        """Set a gauge metric value."""
        self._add_metric(name, value, labels)
    
    def observe_histogram(self, name: str, value: float, labels: Dict[str, str] = None):
        """Observe a histogram metric value."""
        self._add_metric(name, value, labels)
    
    def record_operation_duration(self, operation: str, duration_ms: float, 
                                success: bool, site_id: str = None):
        """Record operation duration metrics."""
        labels = {
            "operation": operation,
            "success": str(success).lower()
        }
        if site_id:
            labels["site_id"] = site_id
        
        # Record duration histogram
        self.observe_histogram("mikrotik_mcp_operation_duration_seconds", 
                              duration_ms / 1000.0, labels)
        
        # Increment operation counter
        self.increment_counter("mikrotik_mcp_operations_total", labels)
    
    def record_routeros_command(self, command: str, duration_ms: float, 
                              success: bool, site_id: str = None):
        """Record RouterOS command metrics."""
        # Extract command category
        category = "unknown"
        if command.startswith("/ip firewall"):
            category = "firewall"
        elif command.startswith("/ip route"):
            category = "routing"
        elif command.startswith("/interface"):
            category = "interface"
        elif command.startswith("/system"):
            category = "system"
        elif command.startswith("/ip dhcp"):
            category = "dhcp"
        elif command.startswith("/ip dns"):
            category = "dns"
        elif command.startswith("/user"):
            category = "user"
        elif command.startswith("/backup"):
            category = "backup"
        elif command.startswith("/log"):
            category = "log"
        elif command.startswith("/wireguard"):
            category = "wireguard"
        elif command.startswith("/openvpn"):
            category = "openvpn"
        elif command.startswith("/container"):
            category = "container"
        elif command.startswith("/queue"):
            category = "queue"
        elif command.startswith("/hotspot"):
            category = "hotspot"
        elif command.startswith("/wireless"):
            category = "wireless"
        elif command.startswith("/vlan"):
            category = "vlan"
        elif command.startswith("/ipv6"):
            category = "ipv6"
        elif command.startswith("/routing"):
            category = "routing"
        
        labels = {
            "command_category": category,
            "success": str(success).lower()
        }
        if site_id:
            labels["site_id"] = site_id
        
        # Record command duration
        self.observe_histogram("mikrotik_mcp_routeros_command_duration_seconds", 
                              duration_ms / 1000.0, labels)
        
        # Increment command counter
        self.increment_counter("mikrotik_mcp_routeros_commands_total", labels)
    
    def record_connection_event(self, event_type: str, site_id: str = None, 
                              success: bool = True):
        """Record connection events."""
        labels = {
            "event_type": event_type,
            "success": str(success).lower()
        }
        if site_id:
            labels["site_id"] = site_id
        
        self.increment_counter("mikrotik_mcp_connection_events_total", labels)
    
    def record_safety_event(self, safety_level: str, operation: str, 
                          site_id: str = None):
        """Record safety events."""
        labels = {
            "safety_level": safety_level,
            "operation": operation
        }
        if site_id:
            labels["site_id"] = site_id
        
        self.increment_counter("mikrotik_mcp_safety_events_total", labels)
    
    
    def record_error(self, error_type: str, operation: str, site_id: str = None):
        """Record error events."""
        labels = {
            "error_type": error_type,
            "operation": operation
        }
        if site_id:
            labels["site_id"] = site_id
        
        self.increment_counter("mikrotik_mcp_errors_total", labels)
    
    def get_metrics(self) -> str:
        """Get metrics in Prometheus format."""
        with self._lock:
            output = []
            
            # Add HELP and TYPE comments
            output.append("# HELP mikrotik_mcp_operations_total Total number of MCP operations")
            output.append("# TYPE mikrotik_mcp_operations_total counter")
            output.append("")
            
            output.append("# HELP mikrotik_mcp_operation_duration_seconds Duration of MCP operations in seconds")
            output.append("# TYPE mikrotik_mcp_operation_duration_seconds histogram")
            output.append("")
            
            output.append("# HELP mikrotik_mcp_routeros_commands_total Total number of RouterOS commands executed")
            output.append("# TYPE mikrotik_mcp_routeros_commands_total counter")
            output.append("")
            
            output.append("# HELP mikrotik_mcp_routeros_command_duration_seconds Duration of RouterOS commands in seconds")
            output.append("# TYPE mikrotik_mcp_routeros_command_duration_seconds histogram")
            output.append("")
            
            output.append("# HELP mikrotik_mcp_connection_events_total Total number of connection events")
            output.append("# TYPE mikrotik_mcp_connection_events_total counter")
            output.append("")
            
            output.append("# HELP mikrotik_mcp_safety_events_total Total number of safety events")
            output.append("# TYPE mikrotik_mcp_safety_events_total counter")
            output.append("")
            
            
            output.append("# HELP mikrotik_mcp_errors_total Total number of errors")
            output.append("# TYPE mikrotik_mcp_errors_total counter")
            output.append("")
            
            output.append("# HELP mikrotik_mcp_start_time_seconds Start time of the MCP server")
            output.append("# TYPE mikrotik_mcp_start_time_seconds gauge")
            output.append("")
            
            # Add metric values
            for metric_name, values in self._metrics.items():
                if not values:
                    continue
                
                # Group by labels for counters and gauges
                if "total" in metric_name or "start_time" in metric_name:
                    label_groups = defaultdict(list)
                    for value in values:
                        label_key = tuple(sorted(value.labels.items()))
                        label_groups[label_key].append(value)
                    
                    for label_key, group_values in label_groups.items():
                        if "total" in metric_name:
                            # Sum counter values
                            total_value = sum(v.value for v in group_values)
                        else:
                            # Use latest gauge value
                            total_value = group_values[-1].value
                        
                        # Format labels
                        if label_key:
                            label_str = "{" + ",".join(f'{k}="{v}"' for k, v in label_key) + "}"
                        else:
                            label_str = ""
                        
                        output.append(f"{metric_name}{label_str} {total_value}")
                else:
                    # For histograms, output all values
                    for value in values:
                        if value.labels:
                            label_str = "{" + ",".join(f'{k}="{v}"' for k, v in value.labels.items()) + "}"
                        else:
                            label_str = ""
                        output.append(f"{metric_name}{label_str} {value.value}")
                
                output.append("")
            
            return "\n".join(output)
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get health status for the metrics system."""
        with self._lock:
            uptime = time.time() - self._start_time
            
            # Count recent operations (last 5 minutes)
            recent_cutoff = time.time() - 300
            recent_operations = 0
            recent_errors = 0
            
            for values in self._metrics.values():
                for value in values:
                    if value.timestamp > recent_cutoff:
                        if "operations_total" in value.name:
                            recent_operations += value.value
                        elif "errors_total" in value.name:
                            recent_errors += value.value
            
            return {
                "status": "healthy",
                "uptime_seconds": uptime,
                "recent_operations": recent_operations,
                "recent_errors": recent_errors,
                "error_rate": recent_errors / max(recent_operations, 1),
                "metrics_count": len(self._metrics),
                "timestamp": time.time()
            }


# Global metrics instance
_metrics_instance: Optional[PrometheusMetrics] = None


def get_metrics() -> PrometheusMetrics:
    """Get the global metrics instance."""
    global _metrics_instance
    if _metrics_instance is None:
        _metrics_instance = PrometheusMetrics()
    return _metrics_instance


class MetricsMiddleware:
    """Middleware to automatically collect metrics from operations."""
    
    def __init__(self, metrics: PrometheusMetrics = None):
        self.metrics = metrics or get_metrics()
    
    def record_operation(self, operation: str, duration_ms: float, 
                        success: bool, site_id: str = None):
        """Record operation metrics."""
        self.metrics.record_operation_duration(operation, duration_ms, success, site_id)
        
        if not success:
            self.metrics.record_error("operation_failed", operation, site_id)
    
    def record_routeros_command(self, command: str, duration_ms: float, 
                              success: bool, site_id: str = None):
        """Record RouterOS command metrics."""
        self.metrics.record_routeros_command(command, duration_ms, success, site_id)
        
        if not success:
            self.metrics.record_error("routeros_command_failed", command, site_id)
    
    def record_connection(self, event_type: str, site_id: str = None, 
                         success: bool = True):
        """Record connection metrics."""
        self.metrics.record_connection_event(event_type, site_id, success)
    
    def record_safety(self, safety_level: str, operation: str, site_id: str = None):
        """Record safety metrics."""
        self.metrics.record_safety_event(safety_level, operation, site_id)
    
