"""
SQL Server Connection - Infrastructure Implementation
Kết nối SQL Server - Triển khai hạ tầng
"""

import pyodbc
import logging
from typing import Optional
from contextlib import contextmanager


class SqlServerConnection:
    """
    SQL Server Connection - Quản lý kết nối SQL Server
    
    Class này chịu trách nhiệm quản lý kết nối đến SQL Server database
    và cung cấp context manager để đảm bảo connection được đóng đúng cách.
    """
    
    def __init__(
        self, 
        server: str = "10.90.97.14", 
        database: str = "WMS", 
        username: str = "sa", 
        password: str = "abcd@1234", 
        trusted_connection: bool = False
    ):
        """
        Khởi tạo kết nối SQL Server
        
        Args:
            server (str): Tên server SQL Server
            database (str): Tên database cần kết nối
            username (str): Username cho SQL authentication
            password (str): Password cho SQL authentication
            trusted_connection (bool): Sử dụng Windows Authentication
        """
        # Thiết lập logging trước
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.trusted_connection = trusted_connection
        self.connection_string = self._build_connection_string()
        
        self.logger.info(f"Initialized SQL Server connection for {database} on {server}")
    
    def _build_connection_string(self) -> str:
        """
        Xây dựng connection string cho SQL Server
        
        Returns:
            str: Connection string hoàn chỉnh
        """
        if self.trusted_connection:
            conn_str = (
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={self.server};"
                f"DATABASE={self.database};"
                f"Trusted_Connection=yes;"
            )
        else:
            conn_str = (
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={self.server};"
                f"DATABASE={self.database};"
                f"UID={self.username};"
                f"PWD={self.password};"
                f"MultipleActiveResultSets=True;"
            )
        
        self.logger.debug(f"Built connection string for {self.server}/{self.database}")
        return conn_str
    
    @contextmanager
    def get_connection(self):
        """
        Context manager để quản lý database connection
        
        Yields:
            pyodbc.Connection: Database connection
        """
        conn = None
        try:
            self.logger.debug("Establishing database connection")
            conn = pyodbc.connect(self.connection_string)
            self.logger.debug("Database connection established")
            yield conn
        except Exception as e:
            self.logger.error(f"Database error: {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                self.logger.debug("Closing database connection")
                conn.close()
                self.logger.debug("Database connection closed")
    
    def test_connection(self) -> bool:
        """
        Test kết nối database
        
        Returns:
            bool: True nếu kết nối thành công, False nếu thất bại
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                return result[0] == 1
        except Exception as e:
            self.logger.error(f"Connection test failed: {e}")
            return False
    
    def get_server_info(self) -> dict:
        """
        Lấy thông tin server
        
        Returns:
            dict: Thông tin server
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT @@VERSION")
                version = cursor.fetchone()[0]
                
                cursor.execute("SELECT DB_NAME()")
                current_db = cursor.fetchone()[0]
                
                return {
                    "server": self.server,
                    "database": current_db,
                    "version": version,
                    "connection_string": self.connection_string
                }
        except Exception as e:
            self.logger.error(f"Failed to get server info: {e}")
            return {
                "server": self.server,
                "database": self.database,
                "error": str(e)
            }
