"""
Tests for AutoErrorCatcher module
"""

import pytest
from self_evolution import AutoErrorCatcher, auto_catch, catch_and_learn


class TestAutoErrorCatcher:
    """Test cases for AutoErrorCatcher"""
    
    def test_context_manager_catches_error(self):
        """Test that context manager catches errors"""
        with AutoErrorCatcher("test_func") as catcher:
            raise ValueError("Test error")
        
        assert catcher.has_error
        assert catcher.error is not None
        assert catcher.error.error_type == "ValueError"
        assert "Test error" in catcher.error.error_message
    
    def test_context_manager_no_error(self):
        """Test context manager when no error occurs"""
        with AutoErrorCatcher("test_func") as catcher:
            result = 2 + 2
        
        assert not catcher.has_error
        assert catcher.error is None
    
    def test_error_suggestion(self):
        """Test that error suggestions are provided"""
        with AutoErrorCatcher("test_func") as catcher:
            raise FileNotFoundError("File not found")
        
        assert catcher.error is not None
        assert catcher.error.suggestion is not None
        assert len(catcher.error.suggestion) > 0
    
    def test_error_timestamp(self):
        """Test that error timestamp is recorded"""
        with AutoErrorCatcher("test_func") as catcher:
            raise RuntimeError("Test")
        
        assert catcher.error is not None
        assert catcher.error.timestamp is not None
        assert "T" in catcher.error.timestamp  # ISO format
    
    def test_error_category(self):
        """Test error categorization"""
        with AutoErrorCatcher("test_func") as catcher:
            raise KeyError("missing_key")
        
        assert catcher.error is not None
        assert catcher.error.category == "key_error"


class TestAutoCatchDecorator:
    """Test cases for auto_catch decorator"""
    
    def test_decorator_catches_error(self):
        """Test that decorator catches errors"""
        
        @auto_catch()
        def failing_function():
            raise TypeError("Type mismatch")
        
        # Should not raise, error is caught internally
        failing_function()
    
    def test_decorator_preserves_function_name(self):
        """Test that decorator preserves function metadata"""
        
        @auto_catch()
        def my_special_function():
            pass
        
        assert my_special_function.__name__ == "my_special_function"
    
    def test_decorator_with_custom_name(self):
        """Test decorator with custom function name"""
        
        @auto_catch("custom_name")
        def actual_function():
            raise ValueError("Error")
        
        actual_function()


class TestCatchAndLearn:
    """Test cases for catch_and_learn function"""
    
    def test_manual_capture(self):
        """Test manual error capture"""
        try:
            raise RuntimeError("Manual test")
        except Exception as e:
            error_record = catch_and_learn(e, "test_function")
            
            assert error_record.error_type == "RuntimeError"
            assert error_record.function_name == "test_function"
            assert "Manual test" in error_record.error_message
    
    def test_error_record_fields(self):
        """Test that all error record fields are populated"""
        try:
            raise ValueError("Test")
        except Exception as e:
            error_record = catch_and_learn(e, "test")
            
            assert error_record.error_type is not None
            assert error_record.error_message is not None
            assert error_record.function_name is not None
            assert error_record.timestamp is not None
            assert error_record.traceback_str is not None
            assert error_record.category is not None
            assert error_record.suggestion is not None


class TestErrorCategories:
    """Test error categorization system"""
    
    def test_file_error_category(self):
        """Test FileNotFoundError categorization"""
        with AutoErrorCatcher("test") as catcher:
            raise FileNotFoundError("Not found")
        
        assert catcher.error.category == "file_error"
    
    def test_permission_error_category(self):
        """Test PermissionError categorization"""
        with AutoErrorCatcher("test") as catcher:
            raise PermissionError("Access denied")
        
        assert catcher.error.category == "permission_error"
    
    def test_import_error_category(self):
        """Test ModuleNotFoundError categorization"""
        with AutoErrorCatcher("test") as catcher:
            raise ModuleNotFoundError("No module")
        
        assert catcher.error.category == "import_error"
    
    def test_unknown_error_category(self):
        """Test unknown error types"""
        with AutoErrorCatcher("test") as catcher:
            raise CustomError("Custom")
        
        assert catcher.error.category == "unknown"


class CustomError(Exception):
    """Custom exception for testing"""
    pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
