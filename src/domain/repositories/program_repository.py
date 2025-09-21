"""
Program Repository Interface - Domain Contract
Giao diện Program Repository - Hợp đồng Domain
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.program import Program, RegisterItem


class ProgramRepository(ABC):
    """
    Abstract Program Repository - Định nghĩa các thao tác với Program và RegisterItem
    
    Interface này định nghĩa các phương thức cần thiết để thao tác với
    dữ liệu chương trình mà không phụ thuộc vào implementation cụ thể.
    """
    
    # Program operations
    @abstractmethod
    def get_by_code(self, program_code: str) -> Optional[Program]:
        """
        Lấy thông tin chương trình theo mã
        
        Args:
            program_code (str): Mã chương trình
            
        Returns:
            Optional[Program]: Thông tin chương trình hoặc None nếu không tìm thấy
        """
        pass
    
    @abstractmethod
    def get_all(self) -> List[Program]:
        """
        Lấy danh sách tất cả chương trình
        
        Returns:
            List[Program]: Danh sách tất cả chương trình
        """
        pass
    
    @abstractmethod
    def save(self, program: Program) -> bool:
        """
        Lưu thông tin chương trình
        
        Args:
            program (Program): Thông tin chương trình cần lưu
            
        Returns:
            bool: True nếu lưu thành công, False nếu thất bại
        """
        pass
    
    @abstractmethod
    def update(self, program: Program) -> bool:
        """
        Cập nhật thông tin chương trình
        
        Args:
            program (Program): Thông tin chương trình cần cập nhật
            
        Returns:
            bool: True nếu cập nhật thành công, False nếu thất bại
        """
        pass
    
    @abstractmethod
    def delete(self, program_code: str) -> bool:
        """
        Xóa chương trình
        
        Args:
            program_code (str): Mã chương trình cần xóa
            
        Returns:
            bool: True nếu xóa thành công, False nếu thất bại
        """
        pass
    
    # RegisterItem operations
    @abstractmethod
    def get_register_items(self, yyyymm: int, program_code: Optional[str] = None) -> List[RegisterItem]:
        """
        Lấy danh sách register items
        
        Args:
            yyyymm (int): Tháng năm
            program_code (Optional[str]): Mã chương trình (optional)
            
        Returns:
            List[RegisterItem]: Danh sách register items
        """
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
    def save_register_item(self, register_item: RegisterItem) -> bool:
        """
        Lưu register item
        
        Args:
            register_item (RegisterItem): Register item cần lưu
            
        Returns:
            bool: True nếu lưu thành công, False nếu thất bại
        """
        pass
    
    @abstractmethod
    def update_register_item(self, register_item: RegisterItem) -> bool:
        """
        Cập nhật register item
        
        Args:
            register_item (RegisterItem): Register item cần cập nhật
            
        Returns:
            bool: True nếu cập nhật thành công, False nếu thất bại
        """
        pass
    
    @abstractmethod
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
        pass
