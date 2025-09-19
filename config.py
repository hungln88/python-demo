"""
Configuration settings for Display Program Management System
Created: 2025-09-19
"""

import os
from typing import Optional


class DatabaseConfig:
    """Database configuration settings"""
    
    # Default SQL Server settings
    DEFAULT_SERVER = "localhost"
    DEFAULT_DATABASE = "DisplayProgramDB"
    DEFAULT_TRUSTED_CONNECTION = True
    
    @classmethod
    def get_server(cls) -> str:
        """Get database server from environment or default"""
        return os.getenv('DB_SERVER', cls.DEFAULT_SERVER)
    
    @classmethod
    def get_database(cls) -> str:
        """Get database name from environment or default"""
        return os.getenv('DB_DATABASE', cls.DEFAULT_DATABASE)
    
    @classmethod
    def get_username(cls) -> Optional[str]:
        """Get database username from environment"""
        return os.getenv('DB_USERNAME')
    
    @classmethod
    def get_password(cls) -> Optional[str]:
        """Get database password from environment"""
        return os.getenv('DB_PASSWORD')
    
    @classmethod
    def use_trusted_connection(cls) -> bool:
        """Check if should use Windows Authentication"""
        return os.getenv('DB_TRUSTED_CONNECTION', 'true').lower() in ['true', '1', 'yes']


class AppConfig:
    """Application configuration settings"""
    
    # Logging settings
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Application settings
    APP_NAME = "Display Program Management System"
    APP_VERSION = "1.0.0"
    
    # Business rules
    MIN_REGISTER_QTY = 1
    MAX_REGISTER_QTY = 999
    MIN_CONDITION_VALUE = 0
    MAX_CONDITION_VALUE = 100
    
    # Display types
    VALID_DISPLAY_TYPES = ['KE_3_O', 'KE_4_O', 'KE_TRUONG_BAY']
    
    # Condition codes
    VALID_CONDITION_CODES = ['CLEANLINESS', 'PRODUCT_AVAILABILITY', 'DISPLAY_QUALITY']
    
    # Program types
    VALID_PROGRAM_TYPES = ['TYPE_BEVERAGE', 'TYPE_SNACK']


class Messages:
    """Application messages in Vietnamese and English"""
    
    # Success messages
    SUCCESS_DB_CONNECTION = "✅ Database connection successful! / Kết nối database thành công!"
    SUCCESS_OPERATION = "✅ Operation completed successfully! / Thao tác hoàn thành thành công!"
    
    # Error messages
    ERROR_DB_CONNECTION = "❌ Failed to connect to database / Không thể kết nối database"
    ERROR_INVALID_INPUT = "❌ Invalid input / Dữ liệu đầu vào không hợp lệ"
    ERROR_NOT_FOUND = "❌ Record not found / Không tìm thấy bản ghi"
    ERROR_OPERATION_FAILED = "❌ Operation failed / Thao tác thất bại"
    
    # Info messages
    INFO_NO_DATA = "ℹ️ No data found / Không có dữ liệu"
    INFO_PROCESSING = "⏳ Processing... / Đang xử lý..."
    
    # Validation messages
    VALIDATION_REQUIRED_FIELD = "Field is required / Trường bắt buộc"
    VALIDATION_INVALID_FORMAT = "Invalid format / Định dạng không hợp lệ"
    VALIDATION_OUT_OF_RANGE = "Value out of range / Giá trị ngoài phạm vi"


# Environment-specific configurations
class DevelopmentConfig:
    """Development environment configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig:
    """Production environment configuration"""
    DEBUG = False
    TESTING = False


class TestingConfig:
    """Testing environment configuration"""
    DEBUG = True
    TESTING = True
    DATABASE_NAME = "DisplayProgramDB_Test"


def get_config():
    """Get configuration based on environment"""
    env = os.getenv('ENVIRONMENT', 'development').lower()
    
    if env == 'production':
        return ProductionConfig()
    elif env == 'testing':
        return TestingConfig()
    else:
        return DevelopmentConfig()
