"""
Program Entity - Domain Model
Thực thể Chương trình - Mô hình Domain
"""

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


@dataclass
class Program:
    """
    Program Entity - Đại diện cho chương trình trưng bày
    
    Attributes:
        program_code (str): Mã chương trình duy nhất
        name (str): Tên chương trình
        description (str): Mô tả chương trình
        start_date (datetime): Ngày bắt đầu
        end_date (datetime): Ngày kết thúc
        is_active (bool): Trạng thái hoạt động
        created_at (datetime): Ngày tạo
        updated_at (datetime): Ngày cập nhật cuối
    """
    program_code: str
    name: str
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __eq__(self, other) -> bool:
        """So sánh hai Program có bằng nhau không"""
        if not isinstance(other, Program):
            return False
        return self.program_code == other.program_code
    
    def __hash__(self) -> int:
        """Hash cho Program"""
        return hash(self.program_code)
    
    def __str__(self) -> str:
        """String representation"""
        return f"Program({self.program_code}: {self.name})"
    
    def __repr__(self) -> str:
        """Debug representation"""
        return f"Program(program_code='{self.program_code}', name='{self.name}')"


@dataclass
class RegisterItem:
    """
    RegisterItem Entity - Cấu hình kệ trưng bày cho chương trình
    
    Attributes:
        yyyymm (int): Tháng năm theo định dạng YYYYMM
        program_code (str): Mã chương trình
        type_code (str): Mã loại chương trình (TYPE_BEVERAGE, TYPE_SNACK)
        item (str): Loại kệ trưng bày (KE_3_O, KE_4_O, KE_TRUONG_BAY)
        facing (int): Số lượng sản phẩm trong 1 ô trưng bày
        unit (int): Số lượng ô trưng bày trong 1 kệ
    """
    yyyymm: int
    program_code: str
    type_code: str
    item: str
    facing: int
    unit: int
    
    def __eq__(self, other) -> bool:
        """So sánh hai RegisterItem có bằng nhau không"""
        if not isinstance(other, RegisterItem):
            return False
        return (self.yyyymm == other.yyyymm and 
                self.program_code == other.program_code and
                self.type_code == other.type_code and
                self.item == other.item)
    
    def __hash__(self) -> int:
        """Hash cho RegisterItem"""
        return hash((self.yyyymm, self.program_code, self.type_code, self.item))
    
    def __str__(self) -> str:
        """String representation"""
        return f"RegisterItem({self.program_code}-{self.item}: {self.unit} units, {self.facing} facing)"
    
    def __repr__(self) -> str:
        """Debug representation"""
        return f"RegisterItem(yyyymm={self.yyyymm}, program_code='{self.program_code}', type_code='{self.type_code}', item='{self.item}', facing={self.facing}, unit={self.unit})"
