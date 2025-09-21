"""
SQL Server Registration Repository - Infrastructure Implementation
Triển khai Registration Repository cho SQL Server - Hạ tầng
"""

import logging
from typing import List, Optional
from datetime import datetime

from domain.repositories.registration_repository import RegistrationRepository
from domain.entities.registration import Registration
from infrastructure.database.sql_server_connection import SqlServerConnection


class SqlServerRegistrationRepository(RegistrationRepository):
    """
    SQL Server Implementation của Registration Repository
    
    Class này triển khai các thao tác với dữ liệu đăng ký sử dụng SQL Server database.
    Nó implement interface RegistrationRepository từ Domain Layer.
    """
    
    def __init__(self, db_connection: SqlServerConnection):
        """
        Khởi tạo repository với database connection
        
        Args:
            db_connection (SqlServerConnection): Database connection instance
        """
        self.db_connection = db_connection
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initialized SqlServerRegistrationRepository")
    
    def get_registrations(self, yyyymm: int, customer_code: Optional[str] = None, active_only: bool = True) -> List[Registration]:
        """
        Lấy danh sách đăng ký
        
        Args:
            yyyymm (int): Tháng năm
            customer_code (Optional[str]): Mã khách hàng (optional)
            active_only (bool): Chỉ lấy đăng ký active (default: True)
            
        Returns:
            List[Registration]: Danh sách đăng ký
        """
        try:
            with self.db_connection.get_connection() as conn:
                cursor = conn.cursor()
                
                # Build query based on parameters
                where_conditions = ["yyyymm = ?"]
                params = [yyyymm]
                
                if customer_code:
                    where_conditions.append("customer_code = ?")
                    params.append(customer_code)
                
                if active_only:
                    where_conditions.append("status = 1")
                
                query = f"""
                    SELECT yyyymm, program_code, customer_code, display_type, register_qty, status
                    FROM register
                    WHERE {' AND '.join(where_conditions)}
                    ORDER BY customer_code, program_code, display_type
                """
                
                cursor.execute(query, params)
                rows = cursor.fetchall()
                
                registrations = []
                for row in rows:
                    registration = Registration(
                        yyyymm=row[0],
                        program_code=row[1],
                        customer_code=row[2],
                        display_type=row[3],
                        register_qty=row[4],
                        status=bool(row[5]),
                        created_at=None,  # Not stored in register table
                        updated_at=None   # Not stored in register table
                    )
                    registrations.append(registration)
                
                self.logger.info(f"Retrieved {len(registrations)} registrations for {yyyymm}")
                return registrations
                
        except Exception as e:
            self.logger.error(f"Error getting registrations: {e}")
            raise
    
    def get_registration(self, yyyymm: int, customer_code: str, program_code: str, display_type: str) -> Optional[Registration]:
        """
        Lấy đăng ký cụ thể
        
        Args:
            yyyymm (int): Tháng năm
            customer_code (str): Mã khách hàng
            program_code (str): Mã chương trình
            display_type (str): Loại kệ trưng bày
            
        Returns:
            Optional[Registration]: Đăng ký hoặc None
        """
        try:
            with self.db_connection.get_connection() as conn:
                cursor = conn.cursor()
                
                query = """
                    SELECT yyyymm, program_code, customer_code, display_type, register_qty, status
                    FROM register
                    WHERE yyyymm = ? AND customer_code = ? AND program_code = ? AND display_type = ?
                """
                cursor.execute(query, (yyyymm, customer_code, program_code, display_type))
                row = cursor.fetchone()
                
                if row:
                    registration = Registration(
                        yyyymm=row[0],
                        program_code=row[1],
                        customer_code=row[2],
                        display_type=row[3],
                        register_qty=row[4],
                        status=bool(row[5]),
                        created_at=None,  # Not stored in register table
                        updated_at=None   # Not stored in register table
                    )
                    self.logger.info(f"Retrieved registration for {customer_code}-{program_code}-{display_type} in {yyyymm}")
                    return registration
                else:
                    self.logger.info(f"Registration not found for {customer_code}-{program_code}-{display_type} in {yyyymm}")
                    return None
                    
        except Exception as e:
            self.logger.error(f"Error getting registration: {e}")
            raise
    
    def get_customer_programs(self, yyyymm: int, customer_code: str) -> List[str]:
        """
        Lấy danh sách chương trình mà khách hàng đã đăng ký
        
        Args:
            yyyymm (int): Tháng năm
            customer_code (str): Mã khách hàng
            
        Returns:
            List[str]: Danh sách mã chương trình
        """
        try:
            with self.db_connection.get_connection() as conn:
                cursor = conn.cursor()
                
                query = """
                    SELECT DISTINCT program_code
                    FROM register
                    WHERE yyyymm = ? AND customer_code = ? AND status = 1
                    ORDER BY program_code
                """
                cursor.execute(query, (yyyymm, customer_code))
                rows = cursor.fetchall()
                
                programs = [row[0] for row in rows]
                self.logger.info(f"Retrieved {len(programs)} programs for customer {customer_code} in {yyyymm}")
                return programs
                
        except Exception as e:
            self.logger.error(f"Error getting customer programs: {e}")
            raise
    
    def get_program_customers(self, yyyymm: int, program_code: str) -> List[str]:
        """
        Lấy danh sách khách hàng đã đăng ký chương trình
        
        Args:
            yyyymm (int): Tháng năm
            program_code (str): Mã chương trình
            
        Returns:
            List[str]: Danh sách mã khách hàng
        """
        try:
            with self.db_connection.get_connection() as conn:
                cursor = conn.cursor()
                
                query = """
                    SELECT DISTINCT customer_code
                    FROM register
                    WHERE yyyymm = ? AND program_code = ? AND status = 1
                    ORDER BY customer_code
                """
                cursor.execute(query, (yyyymm, program_code))
                rows = cursor.fetchall()
                
                customers = [row[0] for row in rows]
                self.logger.info(f"Retrieved {len(customers)} customers for program {program_code} in {yyyymm}")
                return customers
                
        except Exception as e:
            self.logger.error(f"Error getting program customers: {e}")
            raise
    
    def save_registration(self, registration: Registration) -> bool:
        """
        Lưu đăng ký
        
        Args:
            registration (Registration): Đăng ký cần lưu
            
        Returns:
            bool: True nếu lưu thành công, False nếu thất bại
        """
        try:
            with self.db_connection.get_connection() as conn:
                cursor = conn.cursor()
                
                # Use MERGE (UPSERT) to handle both INSERT and UPDATE
                query = """
                    MERGE register AS target
                    USING (SELECT ? AS yyyymm, ? AS program_code, ? AS customer_code, 
                                  ? AS display_type, ? AS register_qty, ? AS status) AS source
                    ON target.yyyymm = source.yyyymm 
                       AND target.program_code = source.program_code
                       AND target.customer_code = source.customer_code
                       AND target.display_type = source.display_type
                    WHEN MATCHED THEN
                        UPDATE SET register_qty = source.register_qty, status = source.status
                    WHEN NOT MATCHED THEN
                        INSERT (yyyymm, program_code, customer_code, display_type, register_qty, status)
                        VALUES (source.yyyymm, source.program_code, source.customer_code, 
                               source.display_type, source.register_qty, source.status);
                """
                
                cursor.execute(query, (
                    registration.yyyymm,
                    registration.program_code,
                    registration.customer_code,
                    registration.display_type,
                    registration.register_qty,
                    registration.status
                ))
                
                conn.commit()
                self.logger.info(f"Saved registration for {registration.customer_code}-{registration.program_code}-{registration.display_type} in {registration.yyyymm}")
                return True
                
        except Exception as e:
            self.logger.error(f"Error saving registration: {e}")
            return False
    
    def update_registration(self, registration: Registration) -> bool:
        """
        Cập nhật đăng ký
        
        Args:
            registration (Registration): Đăng ký cần cập nhật
            
        Returns:
            bool: True nếu cập nhật thành công, False nếu thất bại
        """
        try:
            with self.db_connection.get_connection() as conn:
                cursor = conn.cursor()
                
                query = """
                    UPDATE register 
                    SET register_qty = ?, status = ?
                    WHERE yyyymm = ? AND program_code = ? AND customer_code = ? AND display_type = ?
                """
                
                cursor.execute(query, (
                    registration.register_qty,
                    registration.status,
                    registration.yyyymm,
                    registration.program_code,
                    registration.customer_code,
                    registration.display_type
                ))
                
                if cursor.rowcount > 0:
                    conn.commit()
                    self.logger.info(f"Updated registration for {registration.customer_code}-{registration.program_code}-{registration.display_type} in {registration.yyyymm}")
                    return True
                else:
                    self.logger.warning(f"No registration found to update for {registration.customer_code}-{registration.program_code}-{registration.display_type} in {registration.yyyymm}")
                    return False
                
        except Exception as e:
            self.logger.error(f"Error updating registration: {e}")
            return False
    
    def delete_registration(self, yyyymm: int, customer_code: str, program_code: str, display_type: str) -> bool:
        """
        Xóa đăng ký
        
        Args:
            yyyymm (int): Tháng năm
            customer_code (str): Mã khách hàng
            program_code (str): Mã chương trình
            display_type (str): Loại kệ trưng bày
            
        Returns:
            bool: True nếu xóa thành công, False nếu thất bại
        """
        try:
            with self.db_connection.get_connection() as conn:
                cursor = conn.cursor()
                
                query = """
                    DELETE FROM register 
                    WHERE yyyymm = ? AND program_code = ? AND customer_code = ? AND display_type = ?
                """
                
                cursor.execute(query, (yyyymm, program_code, customer_code, display_type))
                
                if cursor.rowcount > 0:
                    conn.commit()
                    self.logger.info(f"Deleted registration for {customer_code}-{program_code}-{display_type} in {yyyymm}")
                    return True
                else:
                    self.logger.warning(f"No registration found to delete for {customer_code}-{program_code}-{display_type} in {yyyymm}")
                    return False
                
        except Exception as e:
            self.logger.error(f"Error deleting registration: {e}")
            return False
    
    def exists(self, yyyymm: int, customer_code: str, program_code: str, display_type: str) -> bool:
        """
        Kiểm tra đăng ký có tồn tại không
        
        Args:
            yyyymm (int): Tháng năm
            customer_code (str): Mã khách hàng
            program_code (str): Mã chương trình
            display_type (str): Loại kệ trưng bày
            
        Returns:
            bool: True nếu tồn tại, False nếu không
        """
        try:
            with self.db_connection.get_connection() as conn:
                cursor = conn.cursor()
                
                query = """
                    SELECT COUNT(1)
                    FROM register 
                    WHERE yyyymm = ? AND program_code = ? AND customer_code = ? AND display_type = ?
                """
                
                cursor.execute(query, (yyyymm, program_code, customer_code, display_type))
                count = cursor.fetchone()[0]
                
                exists = count > 0
                self.logger.info(f"Registration exists check for {customer_code}-{program_code}-{display_type} in {yyyymm}: {exists}")
                return exists
                
        except Exception as e:
            self.logger.error(f"Error checking registration existence: {e}")
            raise
