"""
Registration Repository Interface - Domain Contract
Giao diện Registration Repository - Hợp đồng Domain
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.registration import Registration


class RegistrationRepository(ABC):
    """
    Abstract Registration Repository - Định nghĩa các thao tác với Registration
    
    Interface này định nghĩa các phương thức cần thiết để thao tác với
    dữ liệu đăng ký mà không phụ thuộc vào implementation cụ thể.
    """
    
    @abstractmethod
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
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
    def get_customer_programs(self, yyyymm: int, customer_code: str) -> List[str]:
        """
        Lấy danh sách chương trình mà khách hàng đã đăng ký
        
        Args:
            yyyymm (int): Tháng năm
            customer_code (str): Mã khách hàng
            
        Returns:
            List[str]: Danh sách mã chương trình
        """
        pass
    
    @abstractmethod
    def get_program_customers(self, yyyymm: int, program_code: str) -> List[str]:
        """
        Lấy danh sách khách hàng đã đăng ký chương trình
        
        Args:
            yyyymm (int): Tháng năm
            program_code (str): Mã chương trình
            
        Returns:
            List[str]: Danh sách mã khách hàng
        """
        pass
    
    @abstractmethod
    def save_registration(self, registration: Registration) -> bool:
        """
        Lưu đăng ký
        
        Args:
            registration (Registration): Đăng ký cần lưu
            
        Returns:
            bool: True nếu lưu thành công, False nếu thất bại
        """
        pass
    
    @abstractmethod
    def update_registration(self, registration: Registration) -> bool:
        """
        Cập nhật đăng ký
        
        Args:
            registration (Registration): Đăng ký cần cập nhật
            
        Returns:
            bool: True nếu cập nhật thành công, False nếu thất bại
        """
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
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
        pass
