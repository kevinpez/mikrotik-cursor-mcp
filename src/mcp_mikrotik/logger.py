"""
Enhanced logging system with structured JSON logs, request IDs, and timing.
Provides production-ready observability for MikroTik MCP operations.
"""
import json
import logging
import time
import uuid
import threading
from typing import Dict, Any, Optional, Union
from dataclasses import dataclass, asdict
from datetime import datetime
from contextlib import contextmanager
import os


@dataclass
class LogContext:
    """Context for structured logging."""
    request_id: str
    operation: str
    start_time: float
    user_id: Optional[str] = None
    site_id: Optional[str] = None
    safety_level: Optional[str] = None


class StructuredFormatter(logging.Formatter):
    """Custom formatter for structured JSON logging."""
    
    def format(self, record):
        # Create structured log entry
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add request context if available
        if hasattr(record, 'request_id'):
            log_entry["request_id"] = record.request_id
        
        if hasattr(record, 'operation'):
            log_entry["operation"] = record.operation
        
        if hasattr(record, 'duration_ms'):
            log_entry["duration_ms"] = record.duration_ms
        
        if hasattr(record, 'site_id'):
            log_entry["site_id"] = record.site_id
        
        if hasattr(record, 'safety_level'):
            log_entry["safety_level"] = record.safety_level
        
        
        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields
        for key, value in record.__dict__.items():
            if key not in ['name', 'msg', 'args', 'levelname', 'levelno', 'pathname', 
                          'filename', 'module', 'lineno', 'funcName', 'created', 
                          'msecs', 'relativeCreated', 'thread', 'threadName', 
                          'processName', 'process', 'getMessage', 'exc_info', 
                          'exc_text', 'stack_info']:
                log_entry[key] = value
        
        return json.dumps(log_entry, default=str)


class RequestContextFilter(logging.Filter):
    """Filter to add request context to log records."""
    
    def filter(self, record):
        # Get current context from thread-local storage
        context = getattr(self, '_context', None)
        if context:
            record.request_id = context.request_id
            record.operation = context.operation
            record.site_id = context.site_id
            record.safety_level = context.safety_level
            
            # Calculate duration if this is the end of an operation
            if hasattr(record, 'operation_end'):
                record.duration_ms = round((time.time() - context.start_time) * 1000, 2)
        
        return True


class MikroTikLogger:
    """Enhanced logger for MikroTik MCP operations."""
    
    def __init__(self, name: str = "mikrotik_mcp"):
        self.name = name
        self.logger = logging.getLogger(name)
        self._context_storage = threading.local()
        
        # Configure logging
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging configuration."""
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Create console handler with structured formatter
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(StructuredFormatter())
        
        # Add request context filter
        context_filter = RequestContextFilter()
        context_filter._context = None  # Will be set per request
        console_handler.addFilter(context_filter)
        
        self.logger.addHandler(console_handler)
        self.logger.setLevel(logging.INFO)
        
        # Prevent propagation to root logger
        self.logger.propagate = False
    
    def _get_context(self) -> Optional[LogContext]:
        """Get current request context."""
        return getattr(self._context_storage, 'context', None)
    
    def _set_context(self, context: LogContext):
        """Set current request context."""
        self._context_storage.context = context
    
    def _clear_context(self):
        """Clear current request context."""
        if hasattr(self._context_storage, 'context'):
            delattr(self._context_storage, 'context')
    
    @contextmanager
    def request_context(self, operation: str, site_id: Optional[str] = None, 
                       safety_level: Optional[str] = None,
                       user_id: Optional[str] = None):
        """
        Context manager for request-scoped logging.
        
        Args:
            operation: Name of the operation being performed
            site_id: Identifier for the site/router
            safety_level: Safety level of the operation
            user_id: User performing the operation
        """
        context = LogContext(
            request_id=str(uuid.uuid4()),
            operation=operation,
            start_time=time.time(),
            site_id=site_id,
            safety_level=safety_level,
            user_id=user_id
        )
        
        old_context = self._get_context()
        self._set_context(context)
        
        try:
            self.info(f"Starting operation: {operation}", extra={
                'operation_start': True,
                'site_id': site_id,
                'safety_level': safety_level,
            })
            yield context
        finally:
            self.info(f"Completed operation: {operation}", extra={
                'operation_end': True,
                'site_id': site_id,
                'safety_level': safety_level,
            })
            self._set_context(old_context)
    
    def _log_with_context(self, level: int, msg: str, *args, **kwargs):
        """Log with current context."""
        context = self._get_context()
        if context:
            kwargs.setdefault('request_id', context.request_id)
            kwargs.setdefault('operation', context.operation)
            kwargs.setdefault('site_id', context.site_id)
            kwargs.setdefault('safety_level', context.safety_level)
        
        self.logger.log(level, msg, *args, **kwargs)
    
    def debug(self, msg: str, *args, **kwargs):
        """Log debug message."""
        self._log_with_context(logging.DEBUG, msg, *args, **kwargs)
    
    def info(self, msg: str, *args, **kwargs):
        """Log info message."""
        self._log_with_context(logging.INFO, msg, *args, **kwargs)
    
    def warning(self, msg: str, *args, **kwargs):
        """Log warning message."""
        self._log_with_context(logging.WARNING, msg, *args, **kwargs)
    
    def error(self, msg: str, *args, **kwargs):
        """Log error message."""
        self._log_with_context(logging.ERROR, msg, *args, **kwargs)
    
    def critical(self, msg: str, *args, **kwargs):
        """Log critical message."""
        self._log_with_context(logging.CRITICAL, msg, *args, **kwargs)
    
    def log_operation(self, operation: str, level: str = "info", 
                     duration_ms: Optional[float] = None, **extra):
        """
        Log an operation with timing and context.
        
        Args:
            operation: Operation name
            level: Log level
            duration_ms: Operation duration in milliseconds
            **extra: Additional fields to include
        """
        log_data = {
            'operation': operation,
            'duration_ms': duration_ms,
            **extra
        }
        
        getattr(self, level)(f"Operation: {operation}", extra=log_data)
    
    def log_routeros_command(self, command: str, success: bool, 
                           duration_ms: Optional[float] = None, 
                           error: Optional[str] = None):
        """
        Log RouterOS command execution.
        
        Args:
            command: RouterOS command executed
            success: Whether command succeeded
            duration_ms: Command duration in milliseconds
            error: Error message if command failed
        """
        level = "info" if success else "error"
        extra = {
            'routeros_command': command,
            'command_success': success,
            'duration_ms': duration_ms
        }
        
        if error:
            extra['error'] = error
        
        self._log_with_context(
            getattr(logging, level.upper()),
            f"RouterOS command: {command} ({'SUCCESS' if success else 'FAILED'})",
            extra=extra
        )
    
    def log_safety_event(self, event_type: str, safety_level: str, 
                        operation: str, **extra):
        """
        Log safety-related events.
        
        Args:
            event_type: Type of safety event
            safety_level: Safety level of the operation
            operation: Operation being performed
            **extra: Additional context
        """
        self.warning(f"Safety event: {event_type}", extra={
            'safety_event': event_type,
            'safety_level': safety_level,
            'operation': operation,
            **extra
        })
    


# Global logger instance
app_logger = MikroTikLogger("mikrotik_mcp")

# Backward compatibility
def get_logger(name: str = None) -> MikroTikLogger:
    """Get logger instance (backward compatibility)."""
    if name:
        return MikroTikLogger(name)
    return app_logger