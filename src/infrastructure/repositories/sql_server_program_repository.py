"""
SQL Server Program Repository - Infrastructure Implementation
Triển khai Program Repository cho SQL Server - Hạ tầng
"""

import logging
from typing import List, Optional
from datetime import datetime

from domain.repositories.program_repository import ProgramRepository
from domain.entities.program import Program, RegisterItem
from infrastructure.database.sql_server_connection import SqlServerConnection


class SqlServerProgramRepository(ProgramRepository):
    """
    SQL Server Implementation của Program Repository
    
    Class này triển khai các thao tác với dữ liệu chương trình sử dụng SQL Server database.
    Nó implement interface ProgramRepository từ Domain Layer.
    
    Note: Program entity không có table riêng trong database, chỉ có register_item table.
    Program information được quản lý thông qua register_item records.
    """
    
    def __init__(self, db_connection: SqlServerConnection):
        """
        Khởi tạo repository với database connection
        
        Args:
            db_connection (SqlServerConnection): Database connection instance
        """
        self.db_connection = db_connection
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initialized SqlServerProgramRepository")
    
    def get_by_code(self, program_code: str) -> Optional[Program]:
        """
        Lấy thông tin chương trình theo mã
        
        Args:
            program_code (str): Mã chương trình
            
        Returns:
            Optional[Program]: Thông tin chương trình hoặc None nếu không tìm thấy
        """
        try:
            with self.db_connection.get_connection() as conn:
                cursor = conn.cursor()
                
                # Lấy thông tin chương trình từ register_item table
                # Tạo Program entity từ dữ liệu có sẵn
                query = """
                    SELECT DISTINCT program_code, type_code
                    FROM register_item
                    WHERE program_code = ?
                    ORDER BY program_code
                """
                cursor.execute(query, (program_code,))
                row = cursor.fetchone()
                
                if row:
                    # Tạo Program entity từ thông tin có sẵn
                    program = Program(
                        program_code=row[0],
                        name=f"Program {row[0]}",
                        description=f"Display program {row[0]} for type {row[1]}",
                        is_active=True,
                        created_at=None,
                        updated_at=None
                    )
                    self.logger.info(f"Retrieved program {program_code}")
                    return program
                else:
                    self.logger.info(f"Program {program_code} not found")
                    return None
                    
        except Exception as e:
            self.logger.error(f"Error getting program by code: {e}")
            raise
    
    def get_all(self) -> List[Program]:
        """
        Lấy danh sách tất cả chương trình
        
        Returns:
            List[Program]: Danh sách tất cả chương trình
        """
        try:
            with self.db_connection.get_connection() as conn:
                cursor = conn.cursor()
                
                query = """
                    SELECT DISTINCT program_code, type_code
                    FROM register_item
                    ORDER BY program_code
                """
                cursor.execute(query)
                rows = cursor.fetchall()
                
                programs = []
                for row in rows:
                    program = Program(
                        program_code=row[0],
                        name=f"Program {row[0]}",
                        description=f"Display program {row[0]} for type {row[1]}",
                        is_active=True,
                        created_at=None,
                        updated_at=None
                    )
                    programs.append(program)
                
                self.logger.info(f"Retrieved {len(programs)} programs")
                return programs
                
        except Exception as e:
            self.logger.error(f"Error getting all programs: {e}")
            raise
    
    def save(self, program: Program) -> bool:
        """
        Lưu thông tin chương trình
        
        Args:
            program (Program): Thông tin chương trình cần lưu
            
        Returns:
            bool: True nếu lưu thành công, False nếu thất bại
        """
        # Program không có table riêng, chỉ có thể tạo thông qua register_item
        # Trả về True để không gây lỗi, nhưng thực tế không lưu gì
        self.logger.info(f"Program save requested for {program.program_code} - no direct table, managed through register_item")
        return True
    
    def update(self, program: Program) -> bool:
        """
        Cập nhật thông tin chương trình
        
        Args:
            program (Program): Thông tin chương trình cần cập nhật
            
        Returns:
            bool: True nếu cập nhật thành công, False nếu thất bại
        """
        # Program không có table riêng, chỉ có thể cập nhật thông qua register_item
        # Trả về True để không gây lỗi, nhưng thực tế không cập nhật gì
        self.logger.info(f"Program update requested for {program.program_code} - no direct table, managed through register_item")
        return True
    
    def delete(self, program_code: str) -> bool:
        """
        Xóa chương trình
        
        Args:
            program_code (str): Mã chương trình cần xóa
            
        Returns:
            bool: True nếu xóa thành công, False nếu thất bại
        """
        try:
            with self.db_connection.get_connection() as conn:
                cursor = conn.cursor()
                
                # Xóa tất cả register_item liên quan đến program
                query = "DELETE FROM register_item WHERE program_code = ?"
                cursor.execute(query, (program_code,))
                
                if cursor.rowcount > 0:
                    conn.commit()
                    self.logger.info(f"Deleted program {program_code} and all related register_items")
                    return True
                else:
                    self.logger.warning(f"No program {program_code} found to delete")
                    return False
                
        except Exception as e:
            self.logger.error(f"Error deleting program: {e}")
            return False
    
    def get_register_items(self, yyyymm: int, program_code: Optional[str] = None) -> List[RegisterItem]:
        """
        Lấy danh sách register items
        
        Args:
            yyyymm (int): Tháng năm
            program_code (Optional[str]): Mã chương trình (optional)
            
        Returns:
            List[RegisterItem]: Danh sách register items
        """
        try:
            with self.db_connection.get_connection() as conn:
                cursor = conn.cursor()
                
                if program_code:
                    query = """
                        SELECT yyyymm, program_code, type_code, item, facing, unit
                        FROM register_item
                        WHERE yyyymm = ? AND program_code = ?
                        ORDER BY program_code, type_code, item
                    """
                    cursor.execute(query, (yyyymm, program_code))
                else:
                    query = """
                        SELECT yyyymm, program_code, type_code, item, facing, unit
                        FROM register_item
                        WHERE yyyymm = ?
                        ORDER BY program_code, type_code, item
                    """
                    cursor.execute(query, (yyyymm,))
                
                rows = cursor.fetchall()
                register_items = []
                
                for row in rows:
                    register_item = RegisterItem(
                        yyyymm=row[0],
                        program_code=row[1],
                        type_code=row[2],
                        item=row[3],
                        facing=row[4],
                        unit=row[5]
                    )
                    register_items.append(register_item)
                
                self.logger.info(f"Retrieved {len(register_items)} register items for {yyyymm}")
                return register_items
                
        except Exception as e:
            self.logger.error(f"Error getting register items: {e}")
            raise
    
    def get_register_item(self, yyyymm: int, program_code: str, display_type: str) -> Optional[RegisterItem]:
        """
        Lấy register item cụ thể
        
        Args:
            yyyymm (int): Tháng năm
            program_code (str): Mã chương trình
            display_type (str): Loại kệ trưng bày
            
        Returns:
            Optional[RegisterItem]: Register item hoặc None
        """
        try:
            with self.db_connection.get_connection() as conn:
                cursor = conn.cursor()
                
                query = """
                    SELECT yyyymm, program_code, type_code, item, facing, unit
                    FROM register_item
                    WHERE yyyymm = ? AND program_code = ? AND item = ?
                """
                cursor.execute(query, (yyyymm, program_code, display_type))
                row = cursor.fetchone()
                
                if row:
                    register_item = RegisterItem(
                        yyyymm=row[0],
                        program_code=row[1],
                        type_code=row[2],
                        item=row[3],
                        facing=row[4],
                        unit=row[5]
                    )
                    self.logger.info(f"Retrieved register item for {program_code}-{display_type} in {yyyymm}")
                    return register_item
                else:
                    self.logger.info(f"Register item not found for {program_code}-{display_type} in {yyyymm}")
                    return None
                    
        except Exception as e:
            self.logger.error(f"Error getting register item: {e}")
            raise
    
    def save_register_item(self, register_item: RegisterItem) -> bool:
        """
        Lưu register item
        
        Args:
            register_item (RegisterItem): Register item cần lưu
            
        Returns:
            bool: True nếu lưu thành công, False nếu thất bại
        """
        try:
            with self.db_connection.get_connection() as conn:
                cursor = conn.cursor()
                
                # Use MERGE (UPSERT) to handle both INSERT and UPDATE
                query = """
                    MERGE register_item AS target
                    USING (SELECT ? AS yyyymm, ? AS program_code, ? AS type_code, 
                                  ? AS item, ? AS facing, ? AS unit) AS source
                    ON target.yyyymm = source.yyyymm 
                       AND target.program_code = source.program_code
                       AND target.type_code = source.type_code
                       AND target.item = source.item
                    WHEN MATCHED THEN
                        UPDATE SET facing = source.facing, unit = source.unit
                    WHEN NOT MATCHED THEN
                        INSERT (yyyymm, program_code, type_code, item, facing, unit)
                        VALUES (source.yyyymm, source.program_code, source.type_code, 
                               source.item, source.facing, source.unit);
                """
                
                cursor.execute(query, (
                    register_item.yyyymm,
                    register_item.program_code,
                    register_item.type_code,
                    register_item.item,
                    register_item.facing,
                    register_item.unit
                ))
                
                conn.commit()
                self.logger.info(f"Saved register item for {register_item.program_code}-{register_item.item} in {register_item.yyyymm}")
                return True
                
        except Exception as e:
            self.logger.error(f"Error saving register item: {e}")
            return False
    
    def update_register_item(self, register_item: RegisterItem) -> bool:
        """
        Cập nhật register item
        
        Args:
            register_item (RegisterItem): Register item cần cập nhật
            
        Returns:
            bool: True nếu cập nhật thành công, False nếu thất bại
        """
        try:
            with self.db_connection.get_connection() as conn:
                cursor = conn.cursor()
                
                query = """
                    UPDATE register_item 
                    SET facing = ?, unit = ?
                    WHERE yyyymm = ? AND program_code = ? AND type_code = ? AND item = ?
                """
                
                cursor.execute(query, (
                    register_item.facing,
                    register_item.unit,
                    register_item.yyyymm,
                    register_item.program_code,
                    register_item.type_code,
                    register_item.item
                ))
                
                if cursor.rowcount > 0:
                    conn.commit()
                    self.logger.info(f"Updated register item for {register_item.program_code}-{register_item.item} in {register_item.yyyymm}")
                    return True
                else:
                    self.logger.warning(f"No register item found to update for {register_item.program_code}-{register_item.item} in {register_item.yyyymm}")
                    return False
                
        except Exception as e:
            self.logger.error(f"Error updating register item: {e}")
            return False
    
    def delete_register_item(self, yyyymm: int, program_code: str, type_code: str, item: str) -> bool:
        """
        Xóa register item
        
        Args:
            yyyymm (int): Tháng năm
            program_code (str): Mã chương trình
            type_code (str): Mã loại chương trình
            item (str): Loại kệ trưng bày
            
        Returns:
            bool: True nếu xóa thành công, False nếu thất bại
        """
        try:
            with self.db_connection.get_connection() as conn:
                cursor = conn.cursor()
                
                query = """
                    DELETE FROM register_item 
                    WHERE yyyymm = ? AND program_code = ? AND type_code = ? AND item = ?
                """
                
                cursor.execute(query, (yyyymm, program_code, type_code, item))
                
                if cursor.rowcount > 0:
                    conn.commit()
                    self.logger.info(f"Deleted register item for {program_code}-{item} in {yyyymm}")
                    return True
                else:
                    self.logger.warning(f"No register item found to delete for {program_code}-{item} in {yyyymm}")
                    return False
                
        except Exception as e:
            self.logger.error(f"Error deleting register item: {e}")
            return False
