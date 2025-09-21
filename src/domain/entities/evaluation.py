"""
Evaluation Entities - Domain Models
Các thực thể Đánh giá - Mô hình Domain
"""

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


@dataclass
class ConditionGroup:
    """
    ConditionGroup Entity - Nhóm điều kiện đánh giá
    
    Attributes:
        yyyymm (int): Tháng năm theo định dạng YYYYMM
        program_code (str): Mã chương trình
        group (int): Số thứ tự nhóm
        type_code (str): Mã loại chương trình
        group_point (int): Số điểm cần đạt trong nhóm này
    """
    yyyymm: int
    program_code: str
    group: int
    type_code: str
    group_point: int
    
    def __eq__(self, other) -> bool:
        """So sánh hai ConditionGroup có bằng nhau không"""
        if not isinstance(other, ConditionGroup):
            return False
        return (self.yyyymm == other.yyyymm and 
                self.program_code == other.program_code and
                self.group == other.group)
    
    def __hash__(self) -> int:
        """Hash cho ConditionGroup"""
        return hash((self.yyyymm, self.program_code, self.group))
    
    def __str__(self) -> str:
        """String representation"""
        return f"ConditionGroup({self.program_code}-Group{self.group}: {self.group_point} points)"
    
    def __repr__(self) -> str:
        """Debug representation"""
        return f"ConditionGroup(yyyymm={self.yyyymm}, program_code='{self.program_code}', group={self.group}, type_code='{self.type_code}', group_point={self.group_point})"


@dataclass
class ConditionItem:
    """
    ConditionItem Entity - Điều kiện đánh giá cụ thể
    
    Attributes:
        yyyymm (int): Tháng năm theo định dạng YYYYMM
        program_code (str): Mã chương trình
        group (int): Số thứ tự nhóm
        condition_code (str): Mã điều kiện
        condition_min_value (int): Giá trị tối thiểu cần đạt
        condition_point (int): Điểm được cộng khi đạt điều kiện
    """
    yyyymm: int
    program_code: str
    group: int
    condition_code: str
    condition_min_value: int
    condition_point: int
    
    def __eq__(self, other) -> bool:
        """So sánh hai ConditionItem có bằng nhau không"""
        if not isinstance(other, ConditionItem):
            return False
        return (self.yyyymm == other.yyyymm and 
                self.program_code == other.program_code and
                self.group == other.group and
                self.condition_code == other.condition_code)
    
    def __hash__(self) -> int:
        """Hash cho ConditionItem"""
        return hash((self.yyyymm, self.program_code, self.group, self.condition_code))
    
    def meets_minimum(self, actual_value: int) -> bool:
        """
        Kiểm tra xem giá trị thực tế có đạt yêu cầu tối thiểu không
        
        Args:
            actual_value (int): Giá trị thực tế đo được
            
        Returns:
            bool: True nếu đạt yêu cầu, False nếu không
        """
        return actual_value >= self.condition_min_value
    
    def __str__(self) -> str:
        """String representation"""
        return f"ConditionItem({self.condition_code}: min={self.condition_min_value}, points={self.condition_point})"
    
    def __repr__(self) -> str:
        """Debug representation"""
        return f"ConditionItem(yyyymm={self.yyyymm}, program_code='{self.program_code}', group={self.group}, condition_code='{self.condition_code}', condition_min_value={self.condition_min_value}, condition_point={self.condition_point})"


@dataclass
class AuditPicture:
    """
    AuditPicture Entity - Kết quả audit thực tế
    
    Attributes:
        yyyymm (int): Tháng năm theo định dạng YYYYMM
        customer_code (str): Mã khách hàng
        condition_code (str): Mã điều kiện được audit
        value (str): Giá trị đo được (dạng string)
        audit_date (datetime): Ngày thực hiện audit
    """
    yyyymm: int
    customer_code: str
    condition_code: str
    value: str
    audit_date: Optional[datetime] = None
    
    @property
    def numeric_value(self) -> int:
        """
        Chuyển đổi value từ string sang int
        
        Returns:
            int: Giá trị số của audit result
            
        Raises:
            ValueError: Nếu value không thể chuyển đổi thành số
        """
        try:
            return int(self.value)
        except ValueError:
            raise ValueError(f"Cannot convert audit value '{self.value}' to integer")
    
    def __eq__(self, other) -> bool:
        """So sánh hai AuditPicture có bằng nhau không"""
        if not isinstance(other, AuditPicture):
            return False
        return (self.yyyymm == other.yyyymm and 
                self.customer_code == other.customer_code and
                self.condition_code == other.condition_code)
    
    def __hash__(self) -> int:
        """Hash cho AuditPicture"""
        return hash((self.yyyymm, self.customer_code, self.condition_code))
    
    def __str__(self) -> str:
        """String representation"""
        return f"AuditPicture({self.customer_code}-{self.condition_code}: {self.value})"
    
    def __repr__(self) -> str:
        """Debug representation"""
        return f"AuditPicture(yyyymm={self.yyyymm}, customer_code='{self.customer_code}', condition_code='{self.condition_code}', value='{self.value}', audit_date={self.audit_date})"


@dataclass
class CustomerEvaluationResult:
    """
    CustomerEvaluationResult Entity - Kết quả đánh giá khách hàng
    
    Attributes:
        yyyymm (int): Tháng năm đánh giá
        customer_code (str): Mã khách hàng
        program_code (str): Mã chương trình
        total_points (int): Tổng điểm đạt được
        max_possible_points (int): Tổng điểm tối đa có thể đạt
        meets_criteria (bool): Có đạt tất cả tiêu chí không
        failed_conditions (List[str]): Danh sách các điều kiện không đạt
        registration_status (bool): Trạng thái đăng ký (active/inactive)
    """
    yyyymm: int
    customer_code: str
    program_code: str
    total_points: int
    max_possible_points: int
    meets_criteria: bool
    failed_conditions: List[str]
    registration_status: bool
    
    @property
    def is_eligible_for_reward(self) -> bool:
        """
        Kiểm tra khách hàng có đủ điều kiện nhận thưởng không
        
        Returns:
            bool: True nếu đủ điều kiện, False nếu không
        """
        return self.meets_criteria and self.registration_status
    
    @property
    def success_rate(self) -> float:
        """
        Tính tỷ lệ thành công (phần trăm)
        
        Returns:
            float: Tỷ lệ thành công từ 0.0 đến 100.0
        """
        if self.max_possible_points == 0:
            return 0.0
        return (self.total_points / self.max_possible_points) * 100.0
    
    def get_failure_summary(self) -> str:
        """
        Lấy tóm tắt lý do thất bại
        
        Returns:
            str: Chuỗi mô tả lý do thất bại
        """
        if not self.failed_conditions:
            return "No failures"
        
        if len(self.failed_conditions) == 1:
            return f"Failed: {self.failed_conditions[0]}"
        
        return f"Failed {len(self.failed_conditions)} conditions: {', '.join(self.failed_conditions[:3])}{'...' if len(self.failed_conditions) > 3 else ''}"
    
    def __eq__(self, other) -> bool:
        """So sánh hai CustomerEvaluationResult có bằng nhau không"""
        if not isinstance(other, CustomerEvaluationResult):
            return False
        return (self.yyyymm == other.yyyymm and 
                self.customer_code == other.customer_code and
                self.program_code == other.program_code)
    
    def __hash__(self) -> int:
        """Hash cho CustomerEvaluationResult"""
        return hash((self.yyyymm, self.customer_code, self.program_code))
    
    def __str__(self) -> str:
        """String representation"""
        status = "ELIGIBLE" if self.is_eligible_for_reward else "NOT_ELIGIBLE"
        return f"CustomerEvaluationResult({self.customer_code}-{self.program_code}: {self.total_points}/{self.max_possible_points} points, {status})"
    
    def __repr__(self) -> str:
        """Debug representation"""
        return f"CustomerEvaluationResult(yyyymm={self.yyyymm}, customer_code='{self.customer_code}', program_code='{self.program_code}', total_points={self.total_points}, max_possible_points={self.max_possible_points}, meets_criteria={self.meets_criteria}, registration_status={self.registration_status})"
