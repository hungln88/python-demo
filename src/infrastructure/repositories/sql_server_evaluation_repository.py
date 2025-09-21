"""
SQL Server Evaluation Repository - Infrastructure Implementation
Triển khai Evaluation Repository cho SQL Server - Hạ tầng
"""

import logging
from typing import List, Optional
from datetime import datetime

from domain.repositories.evaluation_repository import EvaluationRepository
from domain.entities.evaluation import ConditionGroup, ConditionItem, AuditPicture, CustomerEvaluationResult
from infrastructure.database.sql_server_connection import SqlServerConnection


class SqlServerEvaluationRepository(EvaluationRepository):
    """
    SQL Server Implementation của Evaluation Repository
    
    Class này triển khai các thao tác với dữ liệu đánh giá sử dụng SQL Server database.
    Nó implement interface EvaluationRepository từ Domain Layer.
    """
    
    def __init__(self, db_connection: SqlServerConnection):
        """
        Khởi tạo repository với database connection
        
        Args:
            db_connection (SqlServerConnection): Database connection instance
        """
        self.db_connection = db_connection
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initialized SqlServerEvaluationRepository")
    
    def get_condition_groups(self, yyyymm: int, program_code: str, type_code: Optional[str] = None) -> List[ConditionGroup]:
        """
        Lấy danh sách condition groups
        
        Args:
            yyyymm (int): Tháng năm
            program_code (str): Mã chương trình
            type_code (Optional[str]): Mã loại chương trình (optional)
            
        Returns:
            List[ConditionGroup]: Danh sách condition groups
        """
        try:
            with self.db_connection.get_connection() as conn:
                cursor = conn.cursor()
                
                if type_code:
                    query = """
                        SELECT yyyymm, program_code, [group], type_code, group_point
                        FROM condition_group
                        WHERE yyyymm = ? AND program_code = ? AND type_code = ?
                        ORDER BY [group]
                    """
                    cursor.execute(query, (yyyymm, program_code, type_code))
                else:
                    query = """
                        SELECT yyyymm, program_code, [group], type_code, group_point
                        FROM condition_group
                        WHERE yyyymm = ? AND program_code = ?
                        ORDER BY [group]
                    """
                    cursor.execute(query, (yyyymm, program_code))
                
                rows = cursor.fetchall()
                condition_groups = []
                
                for row in rows:
                    condition_group = ConditionGroup(
                        yyyymm=row[0],
                        program_code=row[1],
                        group=row[2],
                        type_code=row[3],
                        group_point=row[4]
                    )
                    condition_groups.append(condition_group)
                
                self.logger.info(f"Retrieved {len(condition_groups)} condition groups for {program_code} in {yyyymm}")
                return condition_groups
                
        except Exception as e:
            self.logger.error(f"Error getting condition groups: {e}")
            raise
    
    def get_condition_group_by_id(self, yyyymm: int, program_code: str, group: int) -> Optional[ConditionGroup]:
        """
        Lấy condition group theo ID
        
        Args:
            yyyymm (int): Tháng năm
            program_code (str): Mã chương trình
            group (int): Số thứ tự group
            
        Returns:
            Optional[ConditionGroup]: Condition group hoặc None
        """
        try:
            with self.db_connection.get_connection() as conn:
                cursor = conn.cursor()
                
                query = """
                    SELECT yyyymm, program_code, [group], type_code, group_point
                    FROM condition_group
                    WHERE yyyymm = ? AND program_code = ? AND [group] = ?
                """
                cursor.execute(query, (yyyymm, program_code, group))
                row = cursor.fetchone()
                
                if row:
                    condition_group = ConditionGroup(
                        yyyymm=row[0],
                        program_code=row[1],
                        group=row[2],
                        type_code=row[3],
                        group_point=row[4]
                    )
                    self.logger.info(f"Retrieved condition group {group} for {program_code} in {yyyymm}")
                    return condition_group
                else:
                    self.logger.info(f"Condition group {group} not found for {program_code} in {yyyymm}")
                    return None
                    
        except Exception as e:
            self.logger.error(f"Error getting condition group by ID: {e}")
            raise
    
    def get_condition_items_by_group(self, yyyymm: int, program_code: str, group: int) -> List[ConditionItem]:
        """
        Lấy danh sách condition items trong một group
        
        Args:
            yyyymm (int): Tháng năm
            program_code (str): Mã chương trình
            group (int): Số thứ tự group
            
        Returns:
            List[ConditionItem]: Danh sách condition items
        """
        try:
            with self.db_connection.get_connection() as conn:
                cursor = conn.cursor()
                
                query = """
                    SELECT yyyymm, program_code, [group], condition_code, condition_min_value, condition_point
                    FROM condition_item
                    WHERE yyyymm = ? AND program_code = ? AND [group] = ?
                    ORDER BY condition_code
                """
                cursor.execute(query, (yyyymm, program_code, group))
                rows = cursor.fetchall()
                
                condition_items = []
                for row in rows:
                    condition_item = ConditionItem(
                        yyyymm=row[0],
                        program_code=row[1],
                        group=row[2],
                        condition_code=row[3],
                        condition_min_value=row[4],
                        condition_point=row[5]
                    )
                    condition_items.append(condition_item)
                
                self.logger.info(f"Retrieved {len(condition_items)} condition items for group {group} in {program_code}")
                return condition_items
                
        except Exception as e:
            self.logger.error(f"Error getting condition items by group: {e}")
            raise
    
    def get_condition_items(self, yyyymm: int, program_code: str, group: Optional[int] = None) -> List[ConditionItem]:
        """
        Lấy danh sách condition items
        
        Args:
            yyyymm (int): Tháng năm
            program_code (str): Mã chương trình
            group (Optional[int]): Số thứ tự group (optional)
            
        Returns:
            List[ConditionItem]: Danh sách condition items
        """
        try:
            with self.db_connection.get_connection() as conn:
                cursor = conn.cursor()
                
                if group is not None:
                    query = """
                        SELECT yyyymm, program_code, [group], condition_code, condition_min_value, condition_point
                        FROM condition_item
                        WHERE yyyymm = ? AND program_code = ? AND [group] = ?
                        ORDER BY [group], condition_code
                    """
                    cursor.execute(query, (yyyymm, program_code, group))
                else:
                    query = """
                        SELECT yyyymm, program_code, [group], condition_code, condition_min_value, condition_point
                        FROM condition_item
                        WHERE yyyymm = ? AND program_code = ?
                        ORDER BY [group], condition_code
                    """
                    cursor.execute(query, (yyyymm, program_code))
                
                rows = cursor.fetchall()
                condition_items = []
                
                for row in rows:
                    condition_item = ConditionItem(
                        yyyymm=row[0],
                        program_code=row[1],
                        group=row[2],
                        condition_code=row[3],
                        condition_min_value=row[4],
                        condition_point=row[5]
                    )
                    condition_items.append(condition_item)
                
                self.logger.info(f"Retrieved {len(condition_items)} condition items for {program_code} in {yyyymm}")
                return condition_items
                
        except Exception as e:
            self.logger.error(f"Error getting condition items: {e}")
            raise
    
    def get_audit_results(self, yyyymm: int, customer_code: Optional[str] = None) -> List[AuditPicture]:
        """
        Lấy kết quả audit
        
        Args:
            yyyymm (int): Tháng năm
            customer_code (Optional[str]): Mã khách hàng (optional)
            
        Returns:
            List[AuditPicture]: Danh sách kết quả audit
        """
        try:
            with self.db_connection.get_connection() as conn:
                cursor = conn.cursor()
                
                if customer_code:
                    query = """
                        SELECT yyyymm, customer_code, condition_code, value, audit_date
                        FROM audit_picture
                        WHERE yyyymm = ? AND customer_code = ?
                        ORDER BY customer_code, condition_code
                    """
                    cursor.execute(query, (yyyymm, customer_code))
                else:
                    query = """
                        SELECT yyyymm, customer_code, condition_code, value, audit_date
                        FROM audit_picture
                        WHERE yyyymm = ?
                        ORDER BY customer_code, condition_code
                    """
                    cursor.execute(query, (yyyymm,))
                
                rows = cursor.fetchall()
                audit_results = []
                
                for row in rows:
                    audit_picture = AuditPicture(
                        yyyymm=row[0],
                        customer_code=row[1],
                        condition_code=row[2],
                        value=row[3],
                        audit_date=row[4] if row[4] else None
                    )
                    audit_results.append(audit_picture)
                
                self.logger.info(f"Retrieved {len(audit_results)} audit results for {yyyymm}")
                return audit_results
                
        except Exception as e:
            self.logger.error(f"Error getting audit results: {e}")
            raise
    
    def get_audit_result(self, yyyymm: int, customer_code: str, condition_code: str) -> Optional[AuditPicture]:
        """
        Lấy kết quả audit cụ thể
        
        Args:
            yyyymm (int): Tháng năm
            customer_code (str): Mã khách hàng
            condition_code (str): Mã điều kiện
            
        Returns:
            Optional[AuditPicture]: Kết quả audit hoặc None
        """
        try:
            with self.db_connection.get_connection() as conn:
                cursor = conn.cursor()
                
                query = """
                    SELECT yyyymm, customer_code, condition_code, value, audit_date
                    FROM audit_picture
                    WHERE yyyymm = ? AND customer_code = ? AND condition_code = ?
                """
                cursor.execute(query, (yyyymm, customer_code, condition_code))
                row = cursor.fetchone()
                
                if row:
                    audit_picture = AuditPicture(
                        yyyymm=row[0],
                        customer_code=row[1],
                        condition_code=row[2],
                        value=row[3],
                        audit_date=row[4] if row[4] else None
                    )
                    self.logger.info(f"Retrieved audit result for {customer_code}-{condition_code} in {yyyymm}")
                    return audit_picture
                else:
                    self.logger.info(f"Audit result not found for {customer_code}-{condition_code} in {yyyymm}")
                    return None
                    
        except Exception as e:
            self.logger.error(f"Error getting audit result: {e}")
            raise
    
    def save_audit_result(self, audit: AuditPicture) -> bool:
        """
        Lưu kết quả audit
        
        Args:
            audit (AuditPicture): Kết quả audit cần lưu
            
        Returns:
            bool: True nếu lưu thành công, False nếu thất bại
        """
        try:
            with self.db_connection.get_connection() as conn:
                cursor = conn.cursor()
                
                # Use MERGE (UPSERT) to handle both INSERT and UPDATE
                query = """
                    MERGE audit_picture AS target
                    USING (SELECT ? AS yyyymm, ? AS customer_code, ? AS condition_code, ? AS value, ? AS audit_date) AS source
                    ON target.yyyymm = source.yyyymm 
                       AND target.customer_code = source.customer_code 
                       AND target.condition_code = source.condition_code
                    WHEN MATCHED THEN
                        UPDATE SET value = source.value, audit_date = source.audit_date
                    WHEN NOT MATCHED THEN
                        INSERT (yyyymm, customer_code, condition_code, value, audit_date)
                        VALUES (source.yyyymm, source.customer_code, source.condition_code, source.value, source.audit_date);
                """
                
                cursor.execute(query, (
                    audit.yyyymm,
                    audit.customer_code,
                    audit.condition_code,
                    audit.value,
                    audit.audit_date or datetime.now()
                ))
                
                conn.commit()
                self.logger.info(f"Saved audit result for {audit.customer_code}-{audit.condition_code} in {audit.yyyymm}")
                return True
                
        except Exception as e:
            self.logger.error(f"Error saving audit result: {e}")
            return False
    
    def save_evaluation_result(self, result: CustomerEvaluationResult) -> bool:
        """
        Lưu kết quả đánh giá khách hàng
        
        Args:
            result (CustomerEvaluationResult): Kết quả đánh giá cần lưu
            
        Returns:
            bool: True nếu lưu thành công, False nếu thất bại
        """
        try:
            with self.db_connection.get_connection() as conn:
                cursor = conn.cursor()
                
                # Create a table to store evaluation results if it doesn't exist
                create_table_query = """
                    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='customer_evaluation_result' AND xtype='U')
                    CREATE TABLE customer_evaluation_result (
                        yyyymm INTEGER NOT NULL,
                        customer_code VARCHAR(50) NOT NULL,
                        program_code VARCHAR(50) NOT NULL,
                        total_points INTEGER NOT NULL,
                        max_possible_points INTEGER NOT NULL,
                        meets_criteria BIT NOT NULL,
                        failed_conditions VARCHAR(MAX),
                        registration_status BIT NOT NULL,
                        created_date DATETIME DEFAULT GETDATE(),
                        CONSTRAINT PK_customer_evaluation_result PRIMARY KEY (yyyymm, customer_code, program_code)
                    );
                """
                cursor.execute(create_table_query)
                
                # Use MERGE (UPSERT) to handle both INSERT and UPDATE
                query = """
                    MERGE customer_evaluation_result AS target
                    USING (SELECT ? AS yyyymm, ? AS customer_code, ? AS program_code, ? AS total_points, 
                                  ? AS max_possible_points, ? AS meets_criteria, ? AS failed_conditions, 
                                  ? AS registration_status) AS source
                    ON target.yyyymm = source.yyyymm 
                       AND target.customer_code = source.customer_code 
                       AND target.program_code = source.program_code
                    WHEN MATCHED THEN
                        UPDATE SET total_points = source.total_points,
                                  max_possible_points = source.max_possible_points,
                                  meets_criteria = source.meets_criteria,
                                  failed_conditions = source.failed_conditions,
                                  registration_status = source.registration_status
                    WHEN NOT MATCHED THEN
                        INSERT (yyyymm, customer_code, program_code, total_points, max_possible_points, 
                               meets_criteria, failed_conditions, registration_status)
                        VALUES (source.yyyymm, source.customer_code, source.program_code, 
                               source.total_points, source.max_possible_points, source.meets_criteria, 
                               source.failed_conditions, source.registration_status);
                """
                
                # Convert failed_conditions list to comma-separated string
                failed_conditions_str = ','.join(result.failed_conditions) if result.failed_conditions else ''
                
                cursor.execute(query, (
                    result.yyyymm,
                    result.customer_code,
                    result.program_code,
                    result.total_points,
                    result.max_possible_points,
                    result.meets_criteria,
                    failed_conditions_str,
                    result.registration_status
                ))
                
                conn.commit()
                self.logger.info(f"Saved evaluation result for {result.customer_code}-{result.program_code} in {result.yyyymm}")
                return True
                
        except Exception as e:
            self.logger.error(f"Error saving evaluation result: {e}")
            return False
    
    def get_evaluation_result(self, yyyymm: int, customer_code: str, program_code: str) -> Optional[CustomerEvaluationResult]:
        """
        Lấy kết quả đánh giá khách hàng
        
        Args:
            yyyymm (int): Tháng năm
            customer_code (str): Mã khách hàng
            program_code (str): Mã chương trình
            
        Returns:
            Optional[CustomerEvaluationResult]: Kết quả đánh giá hoặc None
        """
        try:
            with self.db_connection.get_connection() as conn:
                cursor = conn.cursor()
                
                query = """
                    SELECT yyyymm, customer_code, program_code, total_points, max_possible_points,
                           meets_criteria, failed_conditions, registration_status
                    FROM customer_evaluation_result
                    WHERE yyyymm = ? AND customer_code = ? AND program_code = ?
                """
                cursor.execute(query, (yyyymm, customer_code, program_code))
                row = cursor.fetchone()
                
                if row:
                    # Convert failed_conditions string back to list
                    failed_conditions = row[6].split(',') if row[6] else []
                    # Remove empty strings from the list
                    failed_conditions = [fc.strip() for fc in failed_conditions if fc.strip()]
                    
                    result = CustomerEvaluationResult(
                        yyyymm=row[0],
                        customer_code=row[1],
                        program_code=row[2],
                        total_points=row[3],
                        max_possible_points=row[4],
                        meets_criteria=bool(row[5]),
                        failed_conditions=failed_conditions,
                        registration_status=bool(row[7])
                    )
                    
                    self.logger.info(f"Retrieved evaluation result for {customer_code}-{program_code} in {yyyymm}")
                    return result
                else:
                    self.logger.info(f"Evaluation result not found for {customer_code}-{program_code} in {yyyymm}")
                    return None
                    
        except Exception as e:
            self.logger.error(f"Error getting evaluation result: {e}")
            raise
