# -*- coding: utf-8 -*-
"""
Auto Error Catcher - Automatically capture and learn from errors

Features:
- Decorator-based automatic error capture
- Context manager error handling
- Automatic attribution analysis
- Improvement suggestions generation

Usage:
    # Method 1: Decorator
    @auto_catch()
    def my_function():
        ...
    
    # Method 2: Context manager
    with AutoErrorCatcher() as catcher:
        ...
    
    # Method 3: Manual capture
    try:
        dangerous_operation()
    except Exception as e:
        catch_and_learn(e, "function_name")
"""

import functools
import traceback
from typing import Callable, Any, Optional, Dict
from datetime import datetime
from dataclasses import dataclass, asdict
import os
import sys


@dataclass
class ErrorRecord:
    """Error record data structure"""
    error_type: str
    error_message: str
    function_name: str
    timestamp: str
    traceback_str: str
    category: str
    suggestion: str
    related_skill: Optional[str] = None


# Error classification database
ERROR_CATEGORIES = {
    "FileNotFoundError": {
        "category": "file_error",
        "suggestion": "Check if file path exists. Consider using os.path.exists() for pre-check.",
        "related_skill": None
    },
    "PermissionError": {
        "category": "permission_error",
        "suggestion": "Check file/directory permissions. Consider running with elevated privileges.",
        "related_skill": None
    },
    "ModuleNotFoundError": {
        "category": "import_error",
        "suggestion": "Check if module is installed. Try: pip install <module-name>",
        "related_skill": None
    },
    "sqlite3.OperationalError": {
        "category": "database_error",
        "suggestion": "Check if database is locked or corrupted.",
        "related_skill": None
    },
    "KeyError": {
        "category": "key_error",
        "suggestion": "Check if dictionary/JSON key exists. Use .get() method for safe access.",
        "related_skill": None
    },
    "TypeError": {
        "category": "type_error",
        "suggestion": "Check if data types match expected types.",
        "related_skill": None
    },
    "ValueError": {
        "category": "value_error",
        "suggestion": "Check if value is within expected range or format.",
        "related_skill": None
    },
    "TimeoutError": {
        "category": "timeout_error",
        "suggestion": "Increase timeout value or check network connection.",
        "related_skill": None
    },
    "ConnectionError": {
        "category": "network_error",
        "suggestion": "Check network connection status.",
        "related_skill": None
    },
    "json.JSONDecodeError": {
        "category": "parse_error",
        "suggestion": "Check JSON format. Use JSON validator to verify.",
        "related_skill": None
    },
    "UnicodeDecodeError": {
        "category": "encoding_error",
        "suggestion": "Specify correct encoding (encoding='utf-8') or use errors='ignore'.",
        "related_skill": None
    },
}


class AutoErrorCatcher:
    """
    Automatic error catcher context manager
    
    Example:
        with AutoErrorCatcher() as catcher:
            risky_operation()
        
        if catcher.error:
            print(f"Error caught: {catcher.error}")
    """
    
    def __init__(self, function_name: str = "unknown", db_path: Optional[str] = None):
        """
        Initialize error catcher
        
        Args:
            function_name: Name of the function for logging
            db_path: Path to evolution database (optional, uses default if not provided)
        """
        self.function_name = function_name
        self.db_path = db_path
        self.error: Optional[ErrorRecord] = None
        self._error_occurred = False
    
    def __enter__(self):
        """Enter context"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context - capture error if occurred"""
        if exc_type is not None:
            self.error = self._create_error_record(
                error_type=exc_type.__name__,
                error_message=str(exc_val),
                traceback_str=''.join(traceback.format_exception(exc_type, exc_val, exc_tb))
            )
            self._error_occurred = True
            # Log error (optional - can be integrated with logging system)
            print(f"⚠️  Error caught in {self.function_name}: {exc_type.__name__}")
        return False  # Don't suppress exception
    
    def _create_error_record(
        self,
        error_type: str,
        error_message: str,
        traceback_str: str
    ) -> ErrorRecord:
        """Create error record with classification"""
        category_info = ERROR_CATEGORIES.get(error_type, {
            "category": "unknown",
            "suggestion": "Review error message and traceback for clues.",
            "related_skill": None
        })
        
        return ErrorRecord(
            error_type=error_type,
            error_message=error_message,
            function_name=self.function_name,
            timestamp=datetime.now().isoformat(),
            traceback_str=traceback_str,
            category=category_info["category"],
            suggestion=category_info["suggestion"],
            related_skill=category_info.get("related_skill")
        )
    
    @property
    def has_error(self) -> bool:
        """Check if error occurred"""
        return self._error_occurred
    
    def get_suggestion(self) -> str:
        """Get improvement suggestion"""
        if self.error:
            return self.error.suggestion
        return "No error occurred"


def auto_catch(function_name: Optional[str] = None, db_path: Optional[str] = None):
    """
    Decorator to automatically capture and log errors
    
    Args:
        function_name: Optional custom function name (defaults to function.__name__)
        db_path: Optional database path
    
    Example:
        @auto_catch()
        def risky_function():
            ...
        
        @auto_catch("custom_name")
        def another_function():
            ...
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            name = function_name or func.__name__
            with AutoErrorCatcher(function_name=name, db_path=db_path) as catcher:
                return func(*args, **kwargs)
        return wrapper
    return decorator


def catch_and_learn(
    error: Exception,
    function_name: str = "unknown",
    context: Optional[Dict[str, Any]] = None
) -> ErrorRecord:
    """
    Manually capture error and create learning record
    
    Args:
        error: The exception object
        function_name: Name of the function where error occurred
        context: Optional context information
    
    Returns:
        ErrorRecord object
    """
    catcher = AutoErrorCatcher(function_name=function_name)
    error_record = catcher._create_error_record(
        error_type=type(error).__name__,
        error_message=str(error),
        traceback_str=traceback.format_exc()
    )
    
    # Log error
    print(f"⚠️  Error captured: {error_record.error_type} in {function_name}")
    print(f"   Suggestion: {error_record.suggestion}")
    
    return error_record
