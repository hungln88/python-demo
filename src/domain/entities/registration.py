"""
Registration Entity - Domain Model
Thực thể Đăng ký - Mô hình Domain
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Registration:
    """
    Registration Entity - Đăng ký chương trình của khách hàng
    
    Attributes:
        yyyymm (int): Tháng năm theo định dạng YYYYMM
        program_code (str): Mã chương trình
        customer_code (str): Mã khách hàng
        display_type (str): Loại kệ trưng bày đăng ký
        register_qty (int): Số lượng đăng ký
        status (bool): Trạng thái đăng ký (True = active, False = inactive)
        created_at (datetime): Ngày tạo đăng ký
        updated_at (datetime): Ngày cập nhật cuối
    """
    yyyymm: int
    program_code: str
    customer_code: str
    display_type: str
    register_qty: int
    status: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @property
    def is_active(self) -> bool:
        """
        Kiểm tra đăng ký có đang hoạt động không
        
        Returns:
            bool: True nếu đăng ký đang hoạt động, False nếu không
        """
        return self.status
    
    @property
    def is_inactive(self) -> bool:
        """
        Kiểm tra đăng ký có bị ngừng hoạt động không
        
        Returns:
            bool: True nếu đăng ký bị ngừng, False nếu đang hoạt động
        """
        return not self.status
    
    def activate(self) -> None:
        """Kích hoạt đăng ký"""
        self.status = True
        self.updated_at = datetime.now()
    
    def deactivate(self) -> None:
        """Ngừng đăng ký"""
        self.status = False
        self.updated_at = datetime.now()
    
    def __eq__(self, other) -> bool:
        """So sánh hai Registration có bằng nhau không"""
        if not isinstance(other, Registration):
            return False
        return (self.yyyymm == other.yyyymm and 
                self.program_code == other.program_code and
                self.customer_code == other.customer_code and
                self.display_type == other.display_type)
    
    def __hash__(self) -> int:
        """Hash cho Registration"""
        return hash((self.yyyymm, self.program_code, self.customer_code, self.display_type))
    
    def __str__(self) -> str:
        """String representation"""
        status = "Active" if self.is_active else "Inactive"
        return f"Registration({self.customer_code}-{self.program_code}: {self.register_qty} units, {status})"
    
    def __repr__(self) -> str:
        """Debug representation"""
        return f"Registration(yyyymm={self.yyyymm}, program_code='{self.program_code}', customer_code='{self.customer_code}', display_type='{self.display_type}', register_qty={self.register_qty}, status={self.status})"
