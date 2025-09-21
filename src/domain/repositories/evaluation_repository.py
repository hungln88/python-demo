"""
Evaluation Repository Interface - Domain Contract
Giao diện Evaluation Repository - Hợp đồng Domain
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.evaluation import ConditionGroup, ConditionItem, AuditPicture, CustomerEvaluationResult


class EvaluationRepository(ABC):
    """
    Abstract Evaluation Repository - Định nghĩa các thao tác với dữ liệu đánh giá
    
    Interface này định nghĩa các phương thức cần thiết để thao tác với
    dữ liệu đánh giá mà không phụ thuộc vào implementation cụ thể.
    """
    
    # ConditionGroup operations
    @abstractmethod
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
        pass
    
    @abstractmethod
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
        pass
    
    # ConditionItem operations
    @abstractmethod
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
        pass
    
    @abstractmethod
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
        pass
    
    # AuditPicture operations
    @abstractmethod
    def get_audit_results(self, yyyymm: int, customer_code: Optional[str] = None) -> List[AuditPicture]:
        """
        Lấy kết quả audit
        
        Args:
            yyyymm (int): Tháng năm
            customer_code (Optional[str]): Mã khách hàng (optional)
            
        Returns:
            List[AuditPicture]: Danh sách kết quả audit
        """
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
    def save_audit_result(self, audit: AuditPicture) -> bool:
        """
        Lưu kết quả audit
        
        Args:
            audit (AuditPicture): Kết quả audit cần lưu
            
        Returns:
            bool: True nếu lưu thành công, False nếu thất bại
        """
        pass
    
    # Evaluation operations
    @abstractmethod
    def save_evaluation_result(self, result: CustomerEvaluationResult) -> bool:
        """
        Lưu kết quả đánh giá khách hàng
        
        Args:
            result (CustomerEvaluationResult): Kết quả đánh giá cần lưu
            
        Returns:
            bool: True nếu lưu thành công, False nếu thất bại
        """
        pass
    
    @abstractmethod
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
        pass
