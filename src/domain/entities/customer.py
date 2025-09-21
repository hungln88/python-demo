"""
Customer Entity - Domain Model
Thực thể Khách hàng - Mô hình Domain
"""

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


@dataclass
class Customer:
    """
    Customer Entity - Đại diện cho khách hàng trong hệ thống
    
    Attributes:
        customer_code (str): Mã khách hàng duy nhất
        name (str): Tên khách hàng
        email (str): Email liên hệ
        phone (str): Số điện thoại
        address (str): Địa chỉ
        created_at (datetime): Ngày tạo
        updated_at (datetime): Ngày cập nhật cuối
    """
    customer_code: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __eq__(self, other) -> bool:
        """So sánh hai Customer có bằng nhau không"""
        if not isinstance(other, Customer):
            return False
        return self.customer_code == other.customer_code
    
    def __hash__(self) -> int:
        """Hash cho Customer"""
        return hash(self.customer_code)
    
    def __str__(self) -> str:
        """String representation"""
        return f"Customer({self.customer_code}: {self.name})"
    
    def __repr__(self) -> str:
        """Debug representation"""
        return f"Customer(customer_code='{self.customer_code}', name='{self.name}')"
