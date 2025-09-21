"""
Settings - Application Configuration
Cấu hình - Thiết lập ứng dụng
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class DatabaseSettings:
    """
    Database Settings - Cấu hình cơ sở dữ liệu
    """
    server: str = "xxxx"
    database: str = "xxxx"
    username: str = "xxxx"
    password: str = "xxxx"
    trusted_connection: bool = False
    timeout: int = 30
    max_retries: int = 3
    
    @classmethod
    def from_env(cls) -> 'DatabaseSettings':
        """
        Tạo settings từ environment variables
        
        Returns:
            DatabaseSettings: Settings từ environment
        """
        return cls(
            server=os.getenv("DB_SERVER", "xxxx"),
            database=os.getenv("DB_DATABASE", "xxxx"),
            username=os.getenv("DB_USERNAME", "xxxx"),
            password=os.getenv("DB_PASSWORD", "xxxx"),
            trusted_connection=os.getenv("DB_TRUSTED_CONNECTION", "false").lower() == "true",
            timeout=int(os.getenv("DB_TIMEOUT", "30")),
            max_retries=int(os.getenv("DB_MAX_RETRIES", "3"))
        )


@dataclass
class LoggingSettings:
    """
    Logging Settings - Cấu hình logging
    """
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_path: Optional[str] = None
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5
    
    @classmethod
    def from_env(cls) -> 'LoggingSettings':
        """
        Tạo settings từ environment variables
        
        Returns:
            LoggingSettings: Settings từ environment
        """
        return cls(
            level=os.getenv("LOG_LEVEL", "INFO"),
            format=os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"),
            file_path=os.getenv("LOG_FILE_PATH"),
            max_file_size=int(os.getenv("LOG_MAX_FILE_SIZE", str(10 * 1024 * 1024))),
            backup_count=int(os.getenv("LOG_BACKUP_COUNT", "5"))
        )


@dataclass
class Settings:
    """
    Application Settings - Cấu hình tổng thể của ứng dụng
    """
    database: DatabaseSettings
    logging: LoggingSettings
    app_name: str = "Display Program Management System"
    app_version: str = "1.0.0"
    debug: bool = False
    
    @classmethod
    def from_env(cls) -> 'Settings':
        """
        Tạo settings từ environment variables
        
        Returns:
            Settings: Settings từ environment
        """
        return cls(
            database=DatabaseSettings.from_env(),
            logging=LoggingSettings.from_env(),
            app_name=os.getenv("APP_NAME", "Display Program Management System"),
            app_version=os.getenv("APP_VERSION", "1.0.0"),
            debug=os.getenv("DEBUG", "false").lower() == "true"
        )
    
    @classmethod
    def default(cls) -> 'Settings':
        """
        Tạo settings mặc định
        
        Returns:
            Settings: Settings mặc định
        """
        return cls(
            database=DatabaseSettings(),
            logging=LoggingSettings(),
            debug=False
        )
