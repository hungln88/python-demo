"""
Customer Repository Interface - Domain Contract
Giao diện Customer Repository - Hợp đồng Domain
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.customer import Customer


class CustomerRepository(ABC):
    """
    Abstract Customer Repository - Định nghĩa các thao tác với Customer
    
    Interface này định nghĩa các phương thức cần thiết để thao tác với
    dữ liệu Customer mà không phụ thuộc vào implementation cụ thể.
    """
    
    @abstractmethod
    def get_by_code(self, customer_code: str) -> Optional[Customer]:
        """
        Lấy thông tin khách hàng theo mã
        
        Args:
            customer_code (str): Mã khách hàng
            
        Returns:
            Optional[Customer]: Thông tin khách hàng hoặc None nếu không tìm thấy
        """
        pass
    
    @abstractmethod
    def get_all(self) -> List[Customer]:
        """
        Lấy danh sách tất cả khách hàng
        
        Returns:
            List[Customer]: Danh sách tất cả khách hàng
        """
        pass
    
    @abstractmethod
    def save(self, customer: Customer) -> bool:
        """
        Lưu thông tin khách hàng
        
        Args:
            customer (Customer): Thông tin khách hàng cần lưu
            
        Returns:
            bool: True nếu lưu thành công, False nếu thất bại
        """
        pass
    
    @abstractmethod
    def update(self, customer: Customer) -> bool:
        """
        Cập nhật thông tin khách hàng
        
        Args:
            customer (Customer): Thông tin khách hàng cần cập nhật
            
        Returns:
            bool: True nếu cập nhật thành công, False nếu thất bại
        """
        pass
    
    @abstractmethod
    def delete(self, customer_code: str) -> bool:
        """
        Xóa khách hàng
        
        Args:
            customer_code (str): Mã khách hàng cần xóa
            
        Returns:
            bool: True nếu xóa thành công, False nếu thất bại
        """
        pass
    
    @abstractmethod
    def exists(self, customer_code: str) -> bool:
        """
        Kiểm tra khách hàng có tồn tại không
        
        Args:
            customer_code (str): Mã khách hàng
            
        Returns:
            bool: True nếu tồn tại, False nếu không
        """
        pass
