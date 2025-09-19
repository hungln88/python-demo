"""
Test cases for database.py - Comprehensive database testing
Test cases cho database.py - Kiểm thử database toàn diện
Created: 2025-09-19

Tệp này chứa các test case để kiểm tra:
1. DatabaseConnection - kết nối và quản lý database
2. DisplayProgramRepository - các thao tác CRUD
3. Error handling và transaction management
4. Data integrity và validation

Note: Để chạy các test này, cần có SQL Server và database DisplayProgramDB
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
import pyodbc

from database import DatabaseConnection, DisplayProgramRepository
from models import RegisterItem, Register, ConditionGroup, ConditionItem, AuditPicture


class TestDatabaseConnection(unittest.TestCase):
    """Test cases cho DatabaseConnection class"""
    
    def setUp(self):
        """Thiết lập test environment"""
        self.db_config = {
            'server': 'test_server',
            'database': 'test_db',
            'username': 'test_user',
            'password': 'test_pass'
        }
    
    def test_init_with_trusted_connection(self):
        """Test khởi tạo với Windows Authentication"""
        db = DatabaseConnection(
            server=self.db_config['server'],
            database=self.db_config['database'],
            trusted_connection=True
        )
        
        self.assertEqual(db.server, self.db_config['server'])
        self.assertEqual(db.database, self.db_config['database'])
        self.assertTrue(db.trusted_connection)
        self.assertIn('Trusted_Connection=yes', db.connection_string)
    
    def test_init_with_sql_authentication(self):
        """Test khởi tạo với SQL Server Authentication"""
        db = DatabaseConnection(
            server=self.db_config['server'],
            database=self.db_config['database'],
            username=self.db_config['username'],
            password=self.db_config['password'],
            trusted_connection=False
        )
        
        self.assertEqual(db.server, self.db_config['server'])
        self.assertEqual(db.database, self.db_config['database'])
        self.assertEqual(db.username, self.db_config['username'])
        self.assertEqual(db.password, self.db_config['password'])
        self.assertFalse(db.trusted_connection)
        self.assertIn('UID=test_user', db.connection_string)
        self.assertIn('PWD=test_pass', db.connection_string)
    
    def test_build_connection_string_trusted(self):
        """Test xây dựng connection string với Windows Auth"""
        db = DatabaseConnection('server1', 'db1', trusted_connection=True)
        conn_str = db._build_connection_string()
        
        expected_parts = [
            'DRIVER={ODBC Driver 17 for SQL Server}',
            'SERVER=server1',
            'DATABASE=db1',
            'Trusted_Connection=yes'
        ]
        
        for part in expected_parts:
            self.assertIn(part, conn_str)
    
    def test_build_connection_string_sql_auth(self):
        """Test xây dựng connection string với SQL Auth"""
        db = DatabaseConnection('server1', 'db1', 'user1', 'pass1', False)
        conn_str = db._build_connection_string()
        
        expected_parts = [
            'DRIVER={ODBC Driver 17 for SQL Server}',
            'SERVER=server1',
            'DATABASE=db1',
            'UID=user1',
            'PWD=pass1'
        ]
        
        for part in expected_parts:
            self.assertIn(part, conn_str)
    
    @patch('database.pyodbc.connect')
    def test_get_connection_success(self, mock_connect):
        """Test context manager khi kết nối thành công"""
        # Setup mock
        mock_conn = Mock()
        mock_connect.return_value = mock_conn
        
        db = DatabaseConnection()
        
        # Test context manager
        with db.get_connection() as conn:
            self.assertEqual(conn, mock_conn)
            self.assertFalse(conn.autocommit)
        
        # Verify connection was closed
        mock_conn.close.assert_called_once()
    
    @patch('database.pyodbc.connect')
    def test_get_connection_with_exception(self, mock_connect):
        """Test context manager khi có exception"""
        # Setup mock để raise exception
        mock_conn = Mock()
        mock_connect.return_value = mock_conn
        
        db = DatabaseConnection()
        
        # Test exception handling
        with self.assertRaises(ValueError):
            with db.get_connection() as conn:
                raise ValueError("Test exception")
        
        # Verify rollback và close được gọi
        mock_conn.rollback.assert_called_once()
        mock_conn.close.assert_called_once()
    
    @patch('database.pyodbc.connect')
    def test_test_connection_success(self, mock_connect):
        """Test kiểm tra kết nối thành công"""
        # Setup mock
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = [1]
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        
        db = DatabaseConnection()
        result = db.test_connection()
        
        self.assertTrue(result)
        mock_cursor.execute.assert_called_once_with("SELECT 1")
    
    @patch('database.pyodbc.connect')
    def test_test_connection_failure(self, mock_connect):
        """Test kiểm tra kết nối thất bại"""
        # Setup mock để raise exception
        mock_connect.side_effect = pyodbc.Error("Connection failed")
        
        db = DatabaseConnection()
        result = db.test_connection()
        
        self.assertFalse(result)
    
    @patch('database.pyodbc.connect')
    def test_get_server_info_success(self, mock_connect):
        """Test lấy thông tin server thành công"""
        # Setup mock
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = ["SQL Server 2019", "SERVER01"]
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        
        db = DatabaseConnection(database="TestDB")
        result = db.get_server_info()
        
        expected = {
            'version': 'SQL Server 2019',
            'server_name': 'SERVER01',
            'database': 'TestDB'
        }
        
        self.assertEqual(result, expected)
    
    @patch('database.pyodbc.connect')
    def test_get_server_info_failure(self, mock_connect):
        """Test lấy thông tin server thất bại"""
        mock_connect.side_effect = pyodbc.Error("Server info failed")
        
        db = DatabaseConnection()
        result = db.get_server_info()
        
        self.assertIn('error', result)


class TestDisplayProgramRepository(unittest.TestCase):
    """Test cases cho DisplayProgramRepository class"""
    
    def setUp(self):
        """Thiết lập test environment"""
        # Tạo mock database connection
        self.mock_db = Mock(spec=DatabaseConnection)
        self.repo = DisplayProgramRepository(self.mock_db)
        
        # Sample data cho testing
        self.sample_register_item = RegisterItem(
            yyyymm=202509,
            program_code="PROG001",
            type_code="TYPE_BEVERAGE",
            item="KE_3_O",
            facing=4,
            unit=3
        )
        
        self.sample_register = Register(
            yyyymm=202509,
            program_code="PROG001",
            customer_code="CUST001",
            display_type="KE_3_O",
            register_qty=2,
            status=True
        )
    
    def test_repository_initialization(self):
        """Test khởi tạo repository"""
        self.assertEqual(self.repo.db, self.mock_db)
        self.assertIsNotNone(self.repo.logger)
    
    @patch('database.pyodbc')
    def test_get_register_items_success(self, mock_pyodbc):
        """Test lấy register items thành công"""
        # Setup mock connection và cursor
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [
            (202509, "PROG001", "TYPE_BEVERAGE", "KE_3_O", 4, 3),
            (202509, "PROG001", "TYPE_BEVERAGE", "KE_4_O", 4, 4)
        ]
        mock_conn.cursor.return_value = mock_cursor
        self.mock_db.get_connection.return_value.__enter__.return_value = mock_conn
        
        # Execute method
        result = self.repo.get_register_items(202509, "PROG001")
        
        # Verify results
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], RegisterItem)
        self.assertEqual(result[0].program_code, "PROG001")
        self.assertEqual(result[0].item, "KE_3_O")
        
        # Verify query execution
        expected_query = """
            SELECT yyyymm, program_code, type_code, item, facing, unit
            FROM register_item 
            WHERE yyyymm = ?
         AND program_code = ? ORDER BY program_code, type_code, item"""
        
        mock_cursor.execute.assert_called_once()
        args = mock_cursor.execute.call_args[0]
        # Normalize whitespace for comparison
        actual_query = ' '.join(args[0].split())
        expected_query_norm = ' '.join(expected_query.split())
        self.assertEqual(actual_query, expected_query_norm)
        self.assertEqual(args[1], [202509, "PROG001"])
    
    def test_get_register_items_without_program_code(self):
        """Test lấy register items không chỉ định program_code"""
        # Setup mock
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = []
        mock_conn.cursor.return_value = mock_cursor
        self.mock_db.get_connection.return_value.__enter__.return_value = mock_conn
        
        # Execute
        result = self.repo.get_register_items(202509)
        
        # Verify query không có điều kiện program_code
        args = mock_cursor.execute.call_args[0]
        self.assertNotIn("AND program_code", args[0])
        self.assertEqual(args[1], [202509])
    
    def test_get_register_items_exception(self):
        """Test get_register_items khi có exception"""
        # Setup mock để raise exception
        self.mock_db.get_connection.side_effect = Exception("Database error")
        
        # Verify exception is raised
        with self.assertRaises(Exception):
            self.repo.get_register_items(202509)
    
    @patch('database.pyodbc')
    def test_insert_register_item_success(self, mock_pyodbc):
        """Test insert register item thành công"""
        # Setup mock
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        self.mock_db.get_connection.return_value.__enter__.return_value = mock_conn
        
        # Execute
        result = self.repo.insert_register_item(self.sample_register_item)
        
        # Verify
        self.assertTrue(result)
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        
        # Check query parameters
        args = mock_cursor.execute.call_args[0]
        expected_params = (202509, "PROG001", "TYPE_BEVERAGE", "KE_3_O", 4, 3)
        self.assertEqual(args[1], expected_params)
    
    def test_insert_register_item_invalid_data(self):
        """Test insert với dữ liệu không hợp lệ"""
        # Tạo RegisterItem không hợp lệ
        invalid_item = RegisterItem(
            yyyymm=202200,  # Năm không hợp lệ
            program_code="",
            type_code="TYPE_BEVERAGE", 
            item="KE_3_O",
            facing=4,
            unit=3
        )
        
        # Execute
        result = self.repo.insert_register_item(invalid_item)
        
        # Verify
        self.assertFalse(result)
        # Verify không gọi database operation
        self.mock_db.get_connection.assert_not_called()
    
    @patch('database.pyodbc')
    def test_insert_register_item_integrity_error(self, mock_pyodbc):
        """Test insert khi có lỗi integrity (duplicate key)"""
        # Setup mock để raise IntegrityError
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_cursor.execute.side_effect = pyodbc.IntegrityError("Duplicate key")
        mock_conn.cursor.return_value = mock_cursor
        self.mock_db.get_connection.return_value.__enter__.return_value = mock_conn
        
        # Execute
        result = self.repo.insert_register_item(self.sample_register_item)
        
        # Verify
        self.assertFalse(result)
        # Verify không commit
        mock_conn.commit.assert_not_called()
    
    @patch('database.pyodbc')
    def test_update_register_item_success(self, mock_pyodbc):
        """Test update register item thành công"""
        # Setup mock
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_cursor.rowcount = 1  # 1 row affected
        mock_conn.cursor.return_value = mock_cursor
        self.mock_db.get_connection.return_value.__enter__.return_value = mock_conn
        
        # Execute
        result = self.repo.update_register_item(self.sample_register_item)
        
        # Verify
        self.assertTrue(result)
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
    
    def test_update_register_item_not_found(self):
        """Test update khi không tìm thấy record"""
        # Setup mock
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_cursor.rowcount = 0  # No rows affected
        mock_conn.cursor.return_value = mock_cursor
        self.mock_db.get_connection.return_value.__enter__.return_value = mock_conn
        
        # Execute
        result = self.repo.update_register_item(self.sample_register_item)
        
        # Verify
        self.assertFalse(result)
        # Verify không commit
        mock_conn.commit.assert_not_called()
    
    @patch('database.pyodbc')
    def test_delete_register_item_success(self, mock_pyodbc):
        """Test delete register item thành công"""
        # Setup mock
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_cursor.rowcount = 1  # 1 row deleted
        mock_conn.cursor.return_value = mock_cursor
        self.mock_db.get_connection.return_value.__enter__.return_value = mock_conn
        
        # Execute
        result = self.repo.delete_register_item(
            202509, "PROG001", "TYPE_BEVERAGE", "KE_3_O"
        )
        
        # Verify
        self.assertTrue(result)
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        
        # Check parameters
        args = mock_cursor.execute.call_args[0]
        expected_params = (202509, "PROG001", "TYPE_BEVERAGE", "KE_3_O")
        self.assertEqual(args[1], expected_params)
    
    def test_delete_register_item_not_found(self):
        """Test delete khi không tìm thấy record"""
        # Setup mock
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_cursor.rowcount = 0  # No rows deleted
        mock_conn.cursor.return_value = mock_cursor
        self.mock_db.get_connection.return_value.__enter__.return_value = mock_conn
        
        # Execute
        result = self.repo.delete_register_item(
            202509, "PROG001", "TYPE_BEVERAGE", "KE_3_O"
        )
        
        # Verify
        self.assertFalse(result)
        mock_conn.commit.assert_not_called()


class TestRepositoryTransactionHandling(unittest.TestCase):
    """Test cases cho transaction handling trong repository"""
    
    def setUp(self):
        self.mock_db = Mock(spec=DatabaseConnection)
        self.repo = DisplayProgramRepository(self.mock_db)
    
    def test_transaction_rollback_on_exception(self):
        """Test transaction được rollback khi có exception"""
        # Setup mock để raise exception trong execute
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_cursor.execute.side_effect = Exception("SQL Error")
        mock_conn.cursor.return_value = mock_cursor
        
        # Setup context manager
        context_manager = Mock()
        context_manager.__enter__.return_value = mock_conn
        context_manager.__exit__.return_value = None
        self.mock_db.get_connection.return_value = context_manager
        
        # Execute và verify exception
        result = self.repo.insert_register_item(RegisterItem(
            202509, "PROG001", "TYPE_BEVERAGE", "KE_3_O", 4, 3
        ))
        
        # Verify result is False (error handled)
        self.assertFalse(result)
        
        # Verify commit không được gọi
        mock_conn.commit.assert_not_called()
    
    def test_connection_cleanup(self):
        """Test connection được cleanup đúng cách"""
        # Setup mock
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = []
        mock_conn.cursor.return_value = mock_cursor
        
        # Setup context manager
        context_manager = Mock()
        context_manager.__enter__.return_value = mock_conn
        self.mock_db.get_connection.return_value = context_manager
        
        # Execute
        self.repo.get_register_items(202509)
        
        # Verify context manager được sử dụng đúng cách
        self.mock_db.get_connection.assert_called_once()
        context_manager.__enter__.assert_called_once()


class TestRepositoryErrorHandling(unittest.TestCase):
    """Test cases cho error handling trong repository"""
    
    def setUp(self):
        self.mock_db = Mock(spec=DatabaseConnection)
        self.repo = DisplayProgramRepository(self.mock_db)
    
    def test_database_connection_error(self):
        """Test xử lý lỗi kết nối database"""
        # Setup mock để raise connection error
        self.mock_db.get_connection.side_effect = pyodbc.Error("Connection failed")
        
        # Test với get_register_items (method raise exception)
        with self.assertRaises(pyodbc.Error):
            self.repo.get_register_items(202509)
        
        # Test với insert method (method return False)
        item = RegisterItem(202509, "PROG001", "TYPE_BEVERAGE", "KE_3_O", 4, 3)
        result = self.repo.insert_register_item(item)
        self.assertFalse(result)
    
    def test_sql_execution_error(self):
        """Test xử lý lỗi SQL execution"""
        # Setup mock
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_cursor.execute.side_effect = pyodbc.Error("SQL syntax error")
        mock_conn.cursor.return_value = mock_cursor
        
        context_manager = Mock()
        context_manager.__enter__.return_value = mock_conn
        self.mock_db.get_connection.return_value = context_manager
        
        # Test insert method
        item = RegisterItem(202509, "PROG001", "TYPE_BEVERAGE", "KE_3_O", 4, 3)
        result = self.repo.insert_register_item(item)
        
        # Verify error handling
        self.assertFalse(result)
        mock_conn.commit.assert_not_called()


if __name__ == '__main__':
    # Cấu hình test runner
    unittest.main(verbosity=2, buffer=True)
