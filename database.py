"""
Database connection and operations for Display Program Management System
Kết nối và thao tác cơ sở dữ liệu cho Hệ thống Quản lý Chương trình Trưng bày
Created: 2025-09-19

Tệp này chứa các class và method để:
1. Quản lý kết nối đến SQL Server database
2. Thực hiện các thao tác CRUD (Create, Read, Update, Delete) 
3. Xử lý exception và logging
4. Đảm bảo tính toàn vẹn dữ liệu thông qua transaction

Cấu trúc:
- DatabaseConnection: Quản lý kết nối database
- DisplayProgramRepository: Thực hiện các thao tác dữ liệu cụ thể
"""

import pyodbc
import logging
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime
from contextlib import contextmanager

from models import (
    RegisterItem, Register, ConditionGroup, ConditionItem, 
    AuditPicture, CustomerEvaluationResult
)


class DatabaseConnection:
    """
    Quản lý kết nối và cấu hình database SQL Server
    
    Class này chịu trách nhiệm:
    1. Xây dựng connection string cho SQL Server
    2. Quản lý connection pool và lifecycle
    3. Xử lý exception và rollback transaction khi có lỗi
    4. Cung cấp context manager để đảm bảo connection được đóng đúng cách
    
    Attributes:
        server (str): Tên server SQL Server (mặc định: localhost)
        database (str): Tên database (mặc định: DisplayProgramDB)
        username (str): Username cho SQL authentication (optional)
        password (str): Password cho SQL authentication (optional)  
        trusted_connection (bool): Sử dụng Windows Authentication (mặc định: True)
    
    Example:
        >>> db = DatabaseConnection()  # Sử dụng Windows Auth
        >>> db = DatabaseConnection("server", "db", "user", "pass", False)  # SQL Auth
    """
    
    def __init__(self, server: str = "localhost", database: str = "DisplayProgramDB", 
                 username: str = None, password: str = None, trusted_connection: bool = True):
        """
        Khởi tạo kết nối database
        
        Args:
            server: Tên SQL Server instance
            database: Tên database cần kết nối
            username: Username (chỉ cần khi trusted_connection=False)
            password: Password (chỉ cần khi trusted_connection=False)
            trusted_connection: True = Windows Auth, False = SQL Auth
        """
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.trusted_connection = trusted_connection
        self.connection_string = self._build_connection_string()
        
        # Thiết lập logging để theo dõi các thao tác database
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        self.logger.info(f"Initialized database connection for {database} on {server}")
    
    def _build_connection_string(self) -> str:
        """
        Xây dựng connection string cho SQL Server
        
        Phương thức private này tạo connection string phù hợp dựa trên
        loại authentication được chọn (Windows Auth hoặc SQL Auth).
        
        Returns:
            str: Connection string hoàn chỉnh cho pyodbc
        
        Note:
            - Windows Auth: Sử dụng Trusted_Connection=yes
            - SQL Auth: Sử dụng UID và PWD
        """
        if self.trusted_connection:
            # Windows Authentication - sử dụng tài khoản Windows hiện tại
            conn_str = (
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={self.server};"
                f"DATABASE={self.database};"
                f"Trusted_Connection=yes;"
            )
        else:
            # SQL Server Authentication - sử dụng username/password
            conn_str = (
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={self.server};"
                f"DATABASE={self.database};"
                f"UID={self.username};"
                f"PWD={self.password};"
            )
        
        self.logger.debug(f"Built connection string for {self.server}/{self.database}")
        return conn_str
    
    @contextmanager
    def get_connection(self):
        """
        Context manager để quản lý database connection
        
        Đây là cách an toàn nhất để làm việc với database connection.
        Context manager đảm bảo:
        1. Connection được tạo khi vào block
        2. Transaction được rollback nếu có exception
        3. Connection được đóng khi ra khỏi block
        
        Yields:
            pyodbc.Connection: Database connection object
            
        Example:
            >>> db = DatabaseConnection()
            >>> with db.get_connection() as conn:
            ...     cursor = conn.cursor()
            ...     cursor.execute("SELECT * FROM register")
            ...     results = cursor.fetchall()
            ...     conn.commit()  # Commit nếu thành công
        
        Note:
            - autocommit=False để có thể kiểm soát transaction
            - Tự động rollback nếu có exception
            - Luôn đóng connection trong finally block
        """
        conn = None
        try:
            # Tạo kết nối đến database
            conn = pyodbc.connect(self.connection_string)
            conn.autocommit = False  # Tắt auto-commit để kiểm soát transaction
            
            self.logger.debug("Database connection established")
            yield conn
            
        except Exception as e:
            # Nếu có lỗi, rollback transaction để đảm bảo tính nhất quán
            if conn:
                conn.rollback()
                self.logger.warning("Transaction rolled back due to error")
            
            self.logger.error(f"Database error: {e}")
            raise  # Re-raise exception để caller có thể xử lý
            
        finally:
            # Luôn đóng connection để tránh memory leak
            if conn:
                conn.close()
                self.logger.debug("Database connection closed")
    
    def test_connection(self) -> bool:
        """
        Kiểm tra kết nối database có hoạt động không
        
        Phương thức này thực hiện một query đơn giản để xác minh:
        1. Connection string đúng
        2. Database có thể truy cập
        3. Permissions đủ để thực hiện query
        
        Returns:
            bool: True nếu kết nối thành công, False nếu có lỗi
            
        Example:
            >>> db = DatabaseConnection()
            >>> if db.test_connection():
            ...     print("Database ready!")
            ... else:
            ...     print("Connection failed!")
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")  # Query đơn giản nhất
                result = cursor.fetchone()
                
                # Kiểm tra kết quả trả về đúng
                success = result and result[0] == 1
                
                if success:
                    self.logger.info("Database connection test successful")
                else:
                    self.logger.error("Database connection test failed - unexpected result")
                    
                return success
                
        except Exception as e:
            self.logger.error(f"Connection test failed: {e}")
            return False
    
    def get_server_info(self) -> Dict[str, str]:
        """
        Lấy thông tin về SQL Server instance
        
        Returns:
            Dict[str, str]: Thông tin server (version, edition, etc.)
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT @@VERSION as version, @@SERVERNAME as server_name")
                result = cursor.fetchone()
                
                return {
                    'version': result[0] if result else 'Unknown',
                    'server_name': result[1] if result else 'Unknown',
                    'database': self.database
                }
        except Exception as e:
            self.logger.error(f"Failed to get server info: {e}")
            return {'error': str(e)}


class DisplayProgramRepository:
    """
    Repository pattern cho các thao tác dữ liệu của Display Program Management
    
    Class này thực hiện pattern Repository để:
    1. Tách biệt business logic khỏi data access logic
    2. Cung cấp interface thống nhất cho các thao tác CRUD
    3. Xử lý mapping giữa database records và domain objects
    4. Đảm bảo data integrity và transaction safety
    
    Repository này bao gồm các nhóm operations:
    - RegisterItem operations: Quản lý cấu hình chương trình
    - Register operations: Quản lý đăng ký khách hàng
    - ConditionGroup/Item operations: Quản lý tiêu chí đánh giá
    - AuditPicture operations: Quản lý kết quả audit
    - Complex queries: Các query phức tạp cho reporting
    
    Attributes:
        db (DatabaseConnection): Connection manager để truy cập database
        logger (Logger): Logger để ghi lại các thao tác và lỗi
    
    Example:
        >>> db_conn = DatabaseConnection()
        >>> repo = DisplayProgramRepository(db_conn)
        >>> items = repo.get_register_items(202509, "PROG001")
    """
    
    def __init__(self, db_connection: DatabaseConnection):
        """
        Khởi tạo repository với database connection
        
        Args:
            db_connection: Instance của DatabaseConnection để quản lý kết nối
        """
        self.db = db_connection
        self.logger = logging.getLogger(__name__)
        
        self.logger.info("DisplayProgramRepository initialized")
    
    # ===== REGISTER ITEM OPERATIONS =====
    # Các thao tác liên quan đến cấu hình chương trình trưng bày
    
    def get_register_items(self, yyyymm: int, program_code: str = None) -> List[RegisterItem]:
        """
        Lấy danh sách cấu hình chương trình trưng bày
        
        Phương thức này truy vấn bảng register_item để lấy thông tin về các
        chương trình trưng bày đã được cấu hình bởi bộ phận vận hành.
        
        Args:
            yyyymm (int): Tháng/năm cần truy vấn (format: YYYYMM)
            program_code (str, optional): Mã chương trình cụ thể. 
                                        Nếu None, lấy tất cả chương trình
        
        Returns:
            List[RegisterItem]: Danh sách các cấu hình chương trình
        
        Example:
            >>> # Lấy tất cả chương trình tháng 9/2025
            >>> items = repo.get_register_items(202509)
            >>> # Lấy chỉ chương trình PROG001
            >>> items = repo.get_register_items(202509, "PROG001")
        
        Note:
            - Kết quả được sắp xếp theo program_code, type_code, item
            - Trả về list rỗng nếu không tìm thấy dữ liệu
        """
        # Xây dựng câu query với điều kiện cơ bản
        query = """
            SELECT yyyymm, program_code, type_code, item, facing, unit
            FROM register_item 
            WHERE yyyymm = ?
        """
        params = [yyyymm]
        
        # Thêm điều kiện lọc theo program_code nếu được cung cấp
        if program_code:
            query += " AND program_code = ?"
            params.append(program_code)
        
        # Sắp xếp kết quả để dễ đọc
        query += " ORDER BY program_code, type_code, item"
        
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                rows = cursor.fetchall()
                
                # Chuyển đổi từ database rows sang domain objects
                register_items = [RegisterItem(
                    yyyymm=row[0],
                    program_code=row[1],
                    type_code=row[2],
                    item=row[3],
                    facing=row[4],
                    unit=row[5]
                ) for row in rows]
                
                self.logger.info(f"Retrieved {len(register_items)} register items for {yyyymm}")
                return register_items
                
        except Exception as e:
            self.logger.error(f"Failed to get register items: {e}")
            raise
    
    def insert_register_item(self, item: RegisterItem) -> bool:
        """
        Thêm mới một cấu hình chương trình trưng bày
        
        Phương thức này thêm một RegisterItem mới vào database.
        Trước khi insert, sẽ validate dữ liệu để đảm bảo tính hợp lệ.
        
        Args:
            item (RegisterItem): Đối tượng RegisterItem cần thêm mới
        
        Returns:
            bool: True nếu thêm thành công, False nếu có lỗi
        
        Raises:
            Exception: Nếu có lỗi database hoặc validation
        
        Example:
            >>> item = RegisterItem(202509, "PROG001", "TYPE_BEVERAGE", "KE_3_O", 4, 3)
            >>> success = repo.insert_register_item(item)
            >>> if success:
            ...     print("Thêm cấu hình thành công!")
        
        Note:
            - Sẽ báo lỗi nếu đã tồn tại cấu hình với cùng key
            - Key = (yyyymm, program_code, type_code, item)
        """
        # Validate dữ liệu trước khi insert
        if not item.is_valid():
            self.logger.error(f"Invalid register item data: {item}")
            return False
        
        query = """
            INSERT INTO register_item (yyyymm, program_code, type_code, item, facing, unit)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (
                    item.yyyymm, item.program_code, item.type_code,
                    item.item, item.facing, item.unit
                ))
                conn.commit()
                
                self.logger.info(f"Successfully inserted register item: {item.program_code}/{item.item}")
                return True
                
        except pyodbc.IntegrityError as e:
            # Lỗi primary key duplicate hoặc foreign key violation
            self.logger.error(f"Data integrity error inserting register item: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Failed to insert register item: {e}")
            return False
    
    def update_register_item(self, item: RegisterItem) -> bool:
        """
        Cập nhật cấu hình chương trình trưng bày
        
        Args:
            item (RegisterItem): Đối tượng RegisterItem với thông tin mới
        
        Returns:
            bool: True nếu cập nhật thành công, False nếu có lỗi
        """
        if not item.is_valid():
            self.logger.error(f"Invalid register item data: {item}")
            return False
        
        query = """
            UPDATE register_item 
            SET facing = ?, unit = ?
            WHERE yyyymm = ? AND program_code = ? AND type_code = ? AND item = ?
        """
        
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (
                    item.facing, item.unit,
                    item.yyyymm, item.program_code, item.type_code, item.item
                ))
                
                if cursor.rowcount == 0:
                    self.logger.warning(f"No register item found to update: {item}")
                    return False
                
                conn.commit()
                self.logger.info(f"Successfully updated register item: {item.program_code}/{item.item}")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to update register item: {e}")
            return False
    
    def delete_register_item(self, yyyymm: int, program_code: str, type_code: str, item: str) -> bool:
        """
        Xóa cấu hình chương trình trưng bày
        
        Args:
            yyyymm: Tháng/năm
            program_code: Mã chương trình
            type_code: Mã loại chương trình
            item: Loại kệ trưng bày
        
        Returns:
            bool: True nếu xóa thành công, False nếu có lỗi
        """
        query = """
            DELETE FROM register_item 
            WHERE yyyymm = ? AND program_code = ? AND type_code = ? AND item = ?
        """
        
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (yyyymm, program_code, type_code, item))
                
                if cursor.rowcount == 0:
                    self.logger.warning(f"No register item found to delete: {program_code}/{item}")
                    return False
                
                conn.commit()
                self.logger.info(f"Successfully deleted register item: {program_code}/{item}")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to delete register item: {e}")
            return False
    
    # Register operations
    def get_registrations(self, yyyymm: int, customer_code: str = None, 
                         active_only: bool = True) -> List[Register]:
        """Get customer registrations"""
        query = """
            SELECT yyyymm, program_code, customer_code, display_type, register_qty, status
            FROM register 
            WHERE yyyymm = ?
        """
        params = [yyyymm]
        
        if customer_code:
            query += " AND customer_code = ?"
            params.append(customer_code)
        
        if active_only:
            query += " AND status = 1"
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            return [Register(
                yyyymm=row[0],
                program_code=row[1],
                customer_code=row[2],
                display_type=row[3],
                register_qty=row[4],
                status=bool(row[5])
            ) for row in rows]
    
    def insert_registration(self, registration: Register) -> bool:
        """Insert a new customer registration"""
        query = """
            INSERT INTO register (yyyymm, program_code, customer_code, display_type, register_qty, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (
                    registration.yyyymm, registration.program_code, registration.customer_code,
                    registration.display_type, registration.register_qty, registration.status
                ))
                conn.commit()
                return True
        except Exception as e:
            self.logger.error(f"Failed to insert registration: {e}")
            return False
    
    # ConditionGroup operations
    def get_condition_groups(self, yyyymm: int, program_code: str) -> List[ConditionGroup]:
        """Get condition groups for a program"""
        query = """
            SELECT yyyymm, program_code, [group], type_code, group_point
            FROM condition_group 
            WHERE yyyymm = ? AND program_code = ?
        """
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (yyyymm, program_code))
            rows = cursor.fetchall()
            
            return [ConditionGroup(
                yyyymm=row[0],
                program_code=row[1],
                group=row[2],
                type_code=row[3],
                group_point=row[4]
            ) for row in rows]
    
    # ConditionItem operations
    def get_condition_items(self, yyyymm: int, program_code: str, 
                           group: int = None) -> List[ConditionItem]:
        """Get condition items for a program and optionally for a specific group"""
        query = """
            SELECT yyyymm, program_code, [group], condition_code, condition_min_value, condition_point
            FROM condition_item 
            WHERE yyyymm = ? AND program_code = ?
        """
        params = [yyyymm, program_code]
        
        if group is not None:
            query += " AND [group] = ?"
            params.append(group)
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            return [ConditionItem(
                yyyymm=row[0],
                program_code=row[1],
                group=row[2],
                condition_code=row[3],
                condition_min_value=row[4],
                condition_point=row[5]
            ) for row in rows]
    
    # AuditPicture operations
    def get_audit_results(self, yyyymm: int, customer_code: str = None) -> List[AuditPicture]:
        """Get audit results"""
        query = """
            SELECT yyyymm, customer_code, condition_code, value, audit_date
            FROM audit_picture 
            WHERE yyyymm = ?
        """
        params = [yyyymm]
        
        if customer_code:
            query += " AND customer_code = ?"
            params.append(customer_code)
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            return [AuditPicture(
                yyyymm=row[0],
                customer_code=row[1],
                condition_code=row[2],
                value=row[3],
                audit_date=row[4]
            ) for row in rows]
    
    def insert_audit_result(self, audit: AuditPicture) -> bool:
        """Insert audit result"""
        query = """
            INSERT INTO audit_picture (yyyymm, customer_code, condition_code, value, audit_date)
            VALUES (?, ?, ?, ?, ?)
        """
        
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (
                    audit.yyyymm, audit.customer_code, audit.condition_code,
                    audit.value, audit.audit_date or datetime.now()
                ))
                conn.commit()
                return True
        except Exception as e:
            self.logger.error(f"Failed to insert audit result: {e}")
            return False
    
    # Complex queries
    def get_customer_programs(self, yyyymm: int, customer_code: str) -> List[str]:
        """Get all programs a customer is registered for"""
        query = """
            SELECT DISTINCT program_code 
            FROM register 
            WHERE yyyymm = ? AND customer_code = ? AND status = 1
        """
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (yyyymm, customer_code))
            rows = cursor.fetchall()
            
            return [row[0] for row in rows]
    
    def get_program_customers(self, yyyymm: int, program_code: str) -> List[str]:
        """Get all customers registered for a program"""
        query = """
            SELECT DISTINCT customer_code 
            FROM register 
            WHERE yyyymm = ? AND program_code = ? AND status = 1
        """
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (yyyymm, program_code))
            rows = cursor.fetchall()
            
            return [row[0] for row in rows]
    
    def get_monthly_statistics(self, yyyymm: int) -> Dict[str, Any]:
        """Get monthly statistics"""
        stats_query = """
            SELECT 
                COUNT(DISTINCT r.program_code) as total_programs,
                COUNT(DISTINCT r.customer_code) as total_customers,
                COUNT(DISTINCT CASE WHEN r.status = 1 THEN r.customer_code END) as active_customers,
                COUNT(DISTINCT ap.customer_code) as audited_customers
            FROM register r
            LEFT JOIN audit_picture ap ON r.yyyymm = ap.yyyymm AND r.customer_code = ap.customer_code
            WHERE r.yyyymm = ?
        """
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(stats_query, (yyyymm,))
            row = cursor.fetchone()
            
            return {
                'month': yyyymm,
                'total_programs': row[0] or 0,
                'total_customers': row[1] or 0,
                'active_customers': row[2] or 0,
                'audited_customers': row[3] or 0
            }
