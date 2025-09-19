"""
Data models for Display Program Management System
Các model dữ liệu cho Hệ thống Quản lý Chương trình Trưng bày
Created: 2025-09-19

Tệp này chứa tất cả các data model (mô hình dữ liệu) đại diện cho các bảng trong database.
Mỗi class tương ứng với một bảng và chứa các thuộc tính và phương thức liên quan.
"""

from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime


@dataclass
class RegisterItem:
    """
    Model cho bảng register_item - Thông tin cấu hình chương trình trưng bày
    
    Bảng này chứa thông tin về các chương trình trưng bày được cấu hình bởi bộ phận vận hành.
    Mỗi chương trình có thể có nhiều loại kệ trưng bày khác nhau với cấu hình riêng.
    
    Attributes:
        yyyymm (int): Tháng năm theo định dạng YYYYMM (ví dụ: 202509 = tháng 9/2025)
        program_code (str): Mã chương trình (ví dụ: PROG001, PROG002)
        type_code (str): Mã loại chương trình (ví dụ: TYPE_BEVERAGE, TYPE_SNACK)
        item (str): Loại kệ trưng bày (KE_3_O, KE_4_O, KE_TRUONG_BAY)
        facing (int): Số lượng sản phẩm trong 1 ô trưng bày
        unit (int): Số lượng ô trưng bày trong 1 kệ
    
    Example:
        >>> item = RegisterItem(202509, "PROG001", "TYPE_BEVERAGE", "KE_3_O", 4, 3)
        >>> print(f"Chương trình {item.program_code} có {item.unit} ô, mỗi ô {item.facing} sản phẩm")
    """
    yyyymm: int
    program_code: str
    type_code: str  # mã chương trình
    item: str  # enum loại kệ trưng bày, kệ 3 ô trưng bày, kệ 4 ô trưng bày
    facing: int  # số sản phẩm trong 1 ô trưng bày
    unit: int  # số lượng ô trưng bày trong kệ

    def __eq__(self, other) -> bool:
        """
        So sánh hai RegisterItem có bằng nhau không
        
        Hai RegisterItem được coi là bằng nhau nếu có cùng:
        - yyyymm (tháng/năm)
        - program_code (mã chương trình)  
        - type_code (mã loại chương trình)
        - item (loại kệ)
        
        Args:
            other: Đối tượng khác để so sánh
            
        Returns:
            bool: True nếu bằng nhau, False nếu khác nhau
        """
        if not isinstance(other, RegisterItem):
            return False
        return (self.yyyymm == other.yyyymm and 
                self.program_code == other.program_code and
                self.type_code == other.type_code and
                self.item == other.item)
    
    def get_total_capacity(self) -> int:
        """
        Tính tổng sức chứa của kệ trưng bày
        
        Returns:
            int: Tổng số sản phẩm có thể trưng bày = unit * facing
        """
        return self.unit * self.facing
    
    def is_valid(self) -> bool:
        """
        Kiểm tra tính hợp lệ của RegisterItem
        
        Returns:
            bool: True nếu dữ liệu hợp lệ, False nếu không hợp lệ
        """
        return (
            self.yyyymm > 202300 and  # Năm hợp lệ
            len(self.program_code.strip()) > 0 and  # Có mã chương trình
            len(self.type_code.strip()) > 0 and  # Có mã loại
            len(self.item.strip()) > 0 and  # Có loại kệ
            self.facing > 0 and  # Facing phải dương
            self.unit > 0  # Unit phải dương
        )


@dataclass
class Register:
    """
    Model cho bảng register - Thông tin đăng ký chương trình của khách hàng
    
    Bảng này lưu thông tin về việc khách hàng/trung tâm thương mại đăng ký tham gia 
    các chương trình trưng bày với số lượng kệ cụ thể để nhận hoa hồng.
    
    Attributes:
        yyyymm (int): Tháng năm đăng ký (YYYYMM)
        program_code (str): Mã chương trình đăng ký
        customer_code (str): Mã khách hàng/trung tâm thương mại
        display_type (str): Loại kệ đăng ký (phải tồn tại trong register_item)
        register_qty (int): Số lượng kệ đăng ký
        status (bool): Trạng thái đăng ký (True=đang hoạt động, False=tạm ngừng)
    
    Example:
        >>> reg = Register(202509, "PROG001", "CUST001", "KE_3_O", 2, True)
        >>> print(f"Khách hàng {reg.customer_code} đăng ký {reg.register_qty} kệ loại {reg.display_type}")
    """
    yyyymm: int
    program_code: str
    customer_code: str  # mã khách hàng
    display_type: str  # ref tới register_item.item: enum loại kệ trưng bày
    register_qty: int  # số lượng đăng ký
    status: bool  # trạng thái, False --> ngừng, True: đang đăng ký

    def __eq__(self, other) -> bool:
        """
        So sánh hai đăng ký có bằng nhau không
        
        Hai đăng ký được coi là bằng nhau nếu có cùng:
        - yyyymm, program_code, customer_code, display_type
        
        Args:
            other: Đối tượng khác để so sánh
            
        Returns:
            bool: True nếu bằng nhau, False nếu khác nhau
        """
        if not isinstance(other, Register):
            return False
        return (self.yyyymm == other.yyyymm and 
                self.program_code == other.program_code and
                self.customer_code == other.customer_code and
                self.display_type == other.display_type)

    @property
    def is_active(self) -> bool:
        """
        Kiểm tra đăng ký có đang hoạt động không
        
        Returns:
            bool: True nếu đăng ký đang hoạt động, False nếu tạm ngừng
        """
        return self.status
    
    @property
    def is_inactive(self) -> bool:
        """
        Kiểm tra đăng ký có bị tạm ngừng không
        
        Returns:
            bool: True nếu tạm ngừng, False nếu đang hoạt động
        """
        return not self.status
    
    def get_registration_info(self) -> str:
        """
        Lấy thông tin tóm tắt về đăng ký
        
        Returns:
            str: Chuỗi mô tả thông tin đăng ký
        """
        status_text = "Hoạt động" if self.is_active else "Tạm ngừng"
        return f"KH {self.customer_code} - {self.program_code}: {self.register_qty} kệ {self.display_type} ({status_text})"
    
    def is_valid(self) -> bool:
        """
        Kiểm tra tính hợp lệ của đăng ký
        
        Returns:
            bool: True nếu dữ liệu hợp lệ, False nếu không hợp lệ
        """
        return (
            self.yyyymm > 202300 and  # Năm hợp lệ
            len(self.program_code.strip()) > 0 and  # Có mã chương trình
            len(self.customer_code.strip()) > 0 and  # Có mã khách hàng
            len(self.display_type.strip()) > 0 and  # Có loại kệ
            self.register_qty > 0  # Số lượng phải dương
        )


@dataclass
class ConditionGroup:
    """
    Model cho bảng condition_group - Nhóm tiêu chí đánh giá chương trình
    
    Bảng này chứa thông tin về các nhóm tiêu chí được sử dụng để đánh giá 
    hiệu suất của khách hàng trong các chương trình trưng bày.
    
    Attributes:
        yyyymm (int): Tháng năm áp dụng tiêu chí
        program_code (str): Mã chương trình áp dụng
        group (int): Số thứ tự nhóm tiêu chí (1, 2, 3...)
        type_code (str): Mã loại chương trình (liên kết với register_item.type_code)
        group_point (int): Tổng điểm tối đa của nhóm tiêu chí này
    
    Example:
        >>> group = ConditionGroup(202509, "PROG001", 1, "TYPE_BEVERAGE", 100)
        >>> print(f"Nhóm {group.group} của {group.program_code} có tối đa {group.group_point} điểm")
    """
    yyyymm: int
    program_code: str
    group: int
    type_code: str  # link với type_code trong table register_item
    group_point: int

    def __eq__(self, other) -> bool:
        """
        So sánh hai nhóm tiêu chí có bằng nhau không
        
        Args:
            other: Đối tượng khác để so sánh
            
        Returns:
            bool: True nếu bằng nhau (cùng yyyymm, program_code, group)
        """
        if not isinstance(other, ConditionGroup):
            return False
        return (self.yyyymm == other.yyyymm and 
                self.program_code == other.program_code and
                self.group == other.group)
    
    def is_valid(self) -> bool:
        """
        Kiểm tra tính hợp lệ của nhóm tiêu chí
        
        Returns:
            bool: True nếu dữ liệu hợp lệ
        """
        return (
            self.yyyymm > 202300 and
            len(self.program_code.strip()) > 0 and
            self.group > 0 and
            len(self.type_code.strip()) > 0 and
            self.group_point > 0
        )


@dataclass
class ConditionItem:
    """
    Model cho bảng condition_item - Chi tiết tiêu chí đánh giá cụ thể
    
    Bảng này chứa thông tin chi tiết về từng tiêu chí đánh giá trong một nhóm,
    bao gồm giá trị tối thiểu yêu cầu và điểm số được cấp nếu đạt yêu cầu.
    
    Attributes:
        yyyymm (int): Tháng năm áp dụng
        program_code (str): Mã chương trình
        group (int): Nhóm tiêu chí (tham chiếu condition_group.group)
        condition_code (str): Mã tiêu chí (CLEANLINESS, PRODUCT_AVAILABILITY, DISPLAY_QUALITY)
        condition_min_value (int): Giá trị tối thiểu để đạt tiêu chí (0-100)
        condition_point (int): Điểm được cấp nếu đạt tiêu chí
    
    Example:
        >>> item = ConditionItem(202509, "PROG001", 1, "CLEANLINESS", 80, 30)
        >>> print(f"Tiêu chí {item.condition_code}: tối thiểu {item.condition_min_value}%, được {item.condition_point} điểm")
    """
    yyyymm: int
    program_code: str
    group: int  # ref tới condition_group.group
    condition_code: str
    condition_min_value: int
    condition_point: int

    def __eq__(self, other) -> bool:
        """
        So sánh hai tiêu chí có bằng nhau không
        
        Args:
            other: Đối tượng khác để so sánh
            
        Returns:
            bool: True nếu bằng nhau (cùng yyyymm, program_code, group, condition_code)
        """
        if not isinstance(other, ConditionItem):
            return False
        return (self.yyyymm == other.yyyymm and 
                self.program_code == other.program_code and
                self.group == other.group and
                self.condition_code == other.condition_code)

    def meets_minimum(self, actual_value: int) -> bool:
        """
        Kiểm tra giá trị thực tế có đạt yêu cầu tối thiểu không
        
        Args:
            actual_value (int): Giá trị thực tế từ kết quả audit
            
        Returns:
            bool: True nếu đạt yêu cầu (>=condition_min_value), False nếu không đạt
        
        Example:
            >>> item = ConditionItem(202509, "PROG001", 1, "CLEANLINESS", 80, 30)
            >>> item.meets_minimum(85)  # True - đạt yêu cầu
            >>> item.meets_minimum(75)  # False - không đạt yêu cầu
        """
        return actual_value >= self.condition_min_value
    
    def calculate_points(self, actual_value: int) -> int:
        """
        Tính điểm được cấp dựa trên giá trị thực tế
        
        Args:
            actual_value (int): Giá trị thực tế từ audit
            
        Returns:
            int: Điểm được cấp (condition_point nếu đạt, 0 nếu không đạt)
        """
        return self.condition_point if self.meets_minimum(actual_value) else 0
    
    def get_performance_ratio(self, actual_value: int) -> float:
        """
        Tính tỷ lệ hiệu suất so với yêu cầu tối thiểu
        
        Args:
            actual_value (int): Giá trị thực tế
            
        Returns:
            float: Tỷ lệ hiệu suất (actual_value / condition_min_value)
        """
        if self.condition_min_value == 0:
            return 0.0
        return actual_value / self.condition_min_value
    
    def is_valid(self) -> bool:
        """
        Kiểm tra tính hợp lệ của tiêu chí
        
        Returns:
            bool: True nếu dữ liệu hợp lệ
        """
        return (
            self.yyyymm > 202300 and
            len(self.program_code.strip()) > 0 and
            self.group > 0 and
            len(self.condition_code.strip()) > 0 and
            0 <= self.condition_min_value <= 100 and
            self.condition_point > 0
        )


@dataclass
class AuditPicture:
    """
    Model cho bảng audit_picture - Kết quả kiểm tra thực tế của khách hàng
    
    Bảng này lưu trữ kết quả kiểm tra thực tế của các giám sát viên công ty
    khi đi kiểm tra tại các điểm bán của khách hàng/trung tâm thương mại.
    
    Attributes:
        yyyymm (int): Tháng năm kiểm tra
        customer_code (str): Mã khách hàng được kiểm tra
        condition_code (str): Mã tiêu chí được đánh giá (tham chiếu condition_item.condition_code)
        value (str): Giá trị đo được (thường là số từ 0-100)
        audit_date (datetime, optional): Ngày giờ thực hiện kiểm tra
    
    Example:
        >>> audit = AuditPicture(202509, "CUST001", "CLEANLINESS", "85", datetime.now())
        >>> print(f"KH {audit.customer_code} đạt {audit.numeric_value}% cho tiêu chí {audit.condition_code}")
    """
    yyyymm: int
    customer_code: str
    condition_code: str  # ref tới condition_item.condition_code
    value: str
    audit_date: Optional[datetime] = None

    def __eq__(self, other) -> bool:
        """
        So sánh hai kết quả audit có bằng nhau không
        
        Args:
            other: Đối tượng khác để so sánh
            
        Returns:
            bool: True nếu bằng nhau (cùng yyyymm, customer_code, condition_code)
        """
        if not isinstance(other, AuditPicture):
            return False
        return (self.yyyymm == other.yyyymm and 
                self.customer_code == other.customer_code and
                self.condition_code == other.condition_code)

    @property
    def numeric_value(self) -> int:
        """
        Chuyển đổi giá trị chuỗi thành số nguyên để so sánh
        
        Returns:
            int: Giá trị số (0 nếu không thể chuyển đổi)
        
        Example:
            >>> audit = AuditPicture(202509, "CUST001", "CLEANLINESS", "85.5")
            >>> audit.numeric_value  # 85
        """
        try:
            # Cố gắng chuyển thành float rồi int để xử lý cả số thập phân
            return int(float(self.value))
        except (ValueError, TypeError):
            return 0
    
    @property
    def is_valid_value(self) -> bool:
        """
        Kiểm tra giá trị audit có hợp lệ không (0-100)
        
        Returns:
            bool: True nếu giá trị trong khoảng 0-100
        """
        numeric_val = self.numeric_value
        return 0 <= numeric_val <= 100
    
    def get_audit_summary(self) -> str:
        """
        Lấy thông tin tóm tắt về kết quả audit
        
        Returns:
            str: Chuỗi mô tả kết quả audit
        """
        date_str = self.audit_date.strftime("%d/%m/%Y") if self.audit_date else "Chưa xác định"
        return f"{self.customer_code} - {self.condition_code}: {self.value} ({date_str})"
    
    def is_valid(self) -> bool:
        """
        Kiểm tra tính hợp lệ của kết quả audit
        
        Returns:
            bool: True nếu dữ liệu hợp lệ
        """
        return (
            self.yyyymm > 202300 and
            len(self.customer_code.strip()) > 0 and
            len(self.condition_code.strip()) > 0 and
            len(self.value.strip()) > 0 and
            self.is_valid_value
        )


@dataclass
class CustomerEvaluationResult:
    """
    Kết quả đánh giá khách hàng theo tiêu chí chương trình
    
    Class này chứa kết quả đánh giá tổng hợp của một khách hàng đối với
    một chương trình cụ thể, bao gồm điểm số, tình trạng đạt yêu cầu và quyền nhận thưởng.
    
    Attributes:
        yyyymm (int): Tháng năm đánh giá
        customer_code (str): Mã khách hàng
        program_code (str): Mã chương trình
        total_points (int): Tổng điểm đạt được
        max_possible_points (int): Tổng điểm tối đa có thể đạt
        meets_criteria (bool): Có đạt tất cả tiêu chí không
        failed_conditions (List[str]): Danh sách các tiêu chí không đạt
        registration_status (bool): Trạng thái đăng ký (hoạt động/tạm ngừng)
    
    Example:
        >>> result = CustomerEvaluationResult(202509, "CUST001", "PROG001", 90, 100, True, [], True)
        >>> print(f"{result.customer_code}: {result.success_rate:.1f}% - {'Nhận thưởng' if result.is_eligible_for_reward else 'Không nhận thưởng'}")
    """
    yyyymm: int
    customer_code: str
    program_code: str
    total_points: int
    max_possible_points: int
    meets_criteria: bool
    failed_conditions: List[str]
    registration_status: bool

    def __eq__(self, other) -> bool:
        """
        So sánh hai kết quả đánh giá có bằng nhau không
        
        Args:
            other: Đối tượng khác để so sánh
            
        Returns:
            bool: True nếu bằng nhau (cùng yyyymm, customer_code, program_code)
        """
        if not isinstance(other, CustomerEvaluationResult):
            return False
        return (self.yyyymm == other.yyyymm and 
                self.customer_code == other.customer_code and
                self.program_code == other.program_code)

    @property
    def success_rate(self) -> float:
        """
        Tính tỷ lệ thành công theo phần trăm
        
        Returns:
            float: Tỷ lệ thành công (0.0 - 100.0)
        
        Example:
            >>> result = CustomerEvaluationResult(..., total_points=80, max_possible_points=100, ...)
            >>> result.success_rate  # 80.0
        """
        if self.max_possible_points == 0:
            return 0.0
        return (self.total_points / self.max_possible_points) * 100

    @property
    def is_eligible_for_reward(self) -> bool:
        """
        Kiểm tra khách hàng có đủ điều kiện nhận thưởng không
        
        Để đủ điều kiện nhận thưởng, khách hàng phải:
        1. Đạt tất cả các tiêu chí (meets_criteria = True)
        2. Có đăng ký hoạt động (registration_status = True)
        
        Returns:
            bool: True nếu đủ điều kiện nhận thưởng
        """
        return self.meets_criteria and self.registration_status
    
    @property
    def performance_grade(self) -> str:
        """
        Xếp loại hiệu suất dựa trên tỷ lệ thành công
        
        Returns:
            str: Xếp hạng (Xuất sắc, Tốt, Trung bình, Yếu)
        """
        rate = self.success_rate
        if rate >= 90:
            return "Xuất sắc"
        elif rate >= 80:
            return "Tốt"
        elif rate >= 70:
            return "Trung bình"
        else:
            return "Yếu"
    
    def get_failure_summary(self) -> str:
        """
        Lấy tóm tắt các lý do không đạt yêu cầu
        
        Returns:
            str: Chuỗi mô tả các lý do thất bại
        """
        if not self.failed_conditions:
            return "Đạt tất cả tiêu chí"
        return f"Thất bại: {', '.join(self.failed_conditions)}"
    
    def get_detailed_summary(self) -> str:
        """
        Lấy thông tin chi tiết về kết quả đánh giá
        
        Returns:
            str: Chuỗi mô tả chi tiết
        """
        status = "Hoạt động" if self.registration_status else "Tạm ngừng"
        eligible = "Có" if self.is_eligible_for_reward else "Không"
        
        return (
            f"KH {self.customer_code} - {self.program_code} ({self.yyyymm}):\n"
            f"  Điểm: {self.total_points}/{self.max_possible_points} ({self.success_rate:.1f}%)\n"
            f"  Xếp hạng: {self.performance_grade}\n"
            f"  Trạng thái đăng ký: {status}\n"
            f"  Đủ điều kiện nhận thưởng: {eligible}\n"
            f"  {self.get_failure_summary()}"
        )


# Enums for display types - Các hằng số cho loại kệ trưng bày
class DisplayType:
    """
    Các loại kệ trưng bày hỗ trợ trong hệ thống
    
    Class này định nghĩa các hằng số cho các loại kệ trưng bày khác nhau
    mà khách hàng có thể đăng ký trong các chương trình.
    """
    KE_3_O = "KE_3_O"  # Kệ 3 ô trưng bày
    KE_4_O = "KE_4_O"  # Kệ 4 ô trưng bày  
    KE_TRUONG_BAY = "KE_TRUONG_BAY"  # Kệ trưng bày đặc biệt

    @classmethod
    def all_types(cls) -> List[str]:
        """
        Lấy danh sách tất cả các loại kệ trưng bày
        
        Returns:
            List[str]: Danh sách tất cả loại kệ hợp lệ
        """
        return [cls.KE_3_O, cls.KE_4_O, cls.KE_TRUONG_BAY]
    
    @classmethod
    def is_valid_type(cls, display_type: str) -> bool:
        """
        Kiểm tra loại kệ có hợp lệ không
        
        Args:
            display_type (str): Loại kệ cần kiểm tra
            
        Returns:
            bool: True nếu hợp lệ, False nếu không hợp lệ
        """
        return display_type in cls.all_types()
    
    @classmethod
    def get_description(cls, display_type: str) -> str:
        """
        Lấy mô tả chi tiết về loại kệ
        
        Args:
            display_type (str): Loại kệ
            
        Returns:
            str: Mô tả loại kệ
        """
        descriptions = {
            cls.KE_3_O: "Kệ trưng bày 3 ô - phù hợp cho sản phẩm nhỏ",
            cls.KE_4_O: "Kệ trưng bày 4 ô - phù hợp cho đa dạng sản phẩm",
            cls.KE_TRUONG_BAY: "Kệ trưng bày đặc biệt - thu hút sự chú ý"
        }
        return descriptions.get(display_type, "Loại kệ không xác định")


# Enums for condition codes - Các mã tiêu chí đánh giá
class ConditionCode:
    """
    Các tiêu chí đánh giá hiệu suất trưng bày
    
    Class này định nghĩa các tiêu chí chuẩn được sử dụng để đánh giá
    chất lượng trưng bày sản phẩm tại các điểm bán.
    """
    CLEANLINESS = "CLEANLINESS"  # Độ sạch sẽ của khu vực trưng bày
    PRODUCT_AVAILABILITY = "PRODUCT_AVAILABILITY"  # Tình trạng có hàng trên kệ
    DISPLAY_QUALITY = "DISPLAY_QUALITY"  # Chất lượng bố trí trưng bày

    @classmethod
    def all_codes(cls) -> List[str]:
        """
        Lấy danh sách tất cả các mã tiêu chí
        
        Returns:
            List[str]: Danh sách tất cả mã tiêu chí hợp lệ
        """
        return [cls.CLEANLINESS, cls.PRODUCT_AVAILABILITY, cls.DISPLAY_QUALITY]
    
    @classmethod
    def is_valid_code(cls, condition_code: str) -> bool:
        """
        Kiểm tra mã tiêu chí có hợp lệ không
        
        Args:
            condition_code (str): Mã tiêu chí cần kiểm tra
            
        Returns:
            bool: True nếu hợp lệ, False nếu không hợp lệ
        """
        return condition_code in cls.all_codes()
    
    @classmethod
    def get_description(cls, condition_code: str) -> str:
        """
        Lấy mô tả chi tiết về tiêu chí
        
        Args:
            condition_code (str): Mã tiêu chí
            
        Returns:
            str: Mô tả tiêu chí
        """
        descriptions = {
            cls.CLEANLINESS: "Độ sạch sẽ - Đánh giá tình trạng vệ sinh khu vực trưng bày",
            cls.PRODUCT_AVAILABILITY: "Sẵn hàng - Đánh giá tình trạng có hàng trên kệ",
            cls.DISPLAY_QUALITY: "Chất lượng trưng bày - Đánh giá cách bố trí và trình bày sản phẩm"
        }
        return descriptions.get(condition_code, "Tiêu chí không xác định")


# Enums for program types - Các loại chương trình
class ProgramType:
    """
    Các loại chương trình trưng bày
    
    Class này định nghĩa các loại chương trình trưng bày khác nhau
    dựa trên nhóm sản phẩm.
    """
    TYPE_BEVERAGE = "TYPE_BEVERAGE"  # Chương trình trưng bày đồ uống
    TYPE_SNACK = "TYPE_SNACK"  # Chương trình trưng bày snack/đồ ăn nhẹ

    @classmethod
    def all_types(cls) -> List[str]:
        """
        Lấy danh sách tất cả các loại chương trình
        
        Returns:
            List[str]: Danh sách tất cả loại chương trình hợp lệ
        """
        return [cls.TYPE_BEVERAGE, cls.TYPE_SNACK]
    
    @classmethod
    def is_valid_type(cls, program_type: str) -> bool:
        """
        Kiểm tra loại chương trình có hợp lệ không
        
        Args:
            program_type (str): Loại chương trình cần kiểm tra
            
        Returns:
            bool: True nếu hợp lệ, False nếu không hợp lệ
        """
        return program_type in cls.all_types()
    
    @classmethod
    def get_description(cls, program_type: str) -> str:
        """
        Lấy mô tả chi tiết về loại chương trình
        
        Args:
            program_type (str): Loại chương trình
            
        Returns:
            str: Mô tả loại chương trình
        """
        descriptions = {
            cls.TYPE_BEVERAGE: "Chương trình trưng bày đồ uống - nước giải khát, cà phê, trà",
            cls.TYPE_SNACK: "Chương trình trưng bày đồ ăn nhẹ - snack, kẹo, bánh"
        }
        return descriptions.get(program_type, "Loại chương trình không xác định")


# Helper functions - Các hàm tiện ích
def validate_yyyymm(yyyymm: int) -> bool:
    """
    Kiểm tra tính hợp lệ của định dạng tháng/năm YYYYMM
    
    Args:
        yyyymm (int): Tháng năm theo định dạng YYYYMM
        
    Returns:
        bool: True nếu hợp lệ (2023-2099, tháng 01-12)
    
    Example:
        >>> validate_yyyymm(202509)  # True
        >>> validate_yyyymm(202513)  # False - tháng 13 không tồn tại
    """
    if yyyymm < 202301 or yyyymm > 209912:
        return False
    
    year = yyyymm // 100
    month = yyyymm % 100
    
    return 2023 <= year <= 2099 and 1 <= month <= 12


def format_yyyymm_display(yyyymm: int) -> str:
    """
    Định dạng tháng/năm thành chuỗi hiển thị thân thiện
    
    Args:
        yyyymm (int): Tháng năm theo định dạng YYYYMM
        
    Returns:
        str: Chuỗi hiển thị (ví dụ: "Tháng 09/2025")
    
    Example:
        >>> format_yyyymm_display(202509)
        'Tháng 09/2025'
    """
    if not validate_yyyymm(yyyymm):
        return f"Tháng không hợp lệ: {yyyymm}"
    
    year = yyyymm // 100
    month = yyyymm % 100
    
    return f"Tháng {month:02d}/{year}"


# Helper functions - Các hàm tiện ích
def validate_yyyymm(yyyymm: int) -> bool:
    """
    Kiểm tra tính hợp lệ của định dạng tháng/năm YYYYMM
    
    Args:
        yyyymm (int): Tháng năm theo định dạng YYYYMM
        
    Returns:
        bool: True nếu hợp lệ (2023-2099, tháng 01-12)
    
    Example:
        >>> validate_yyyymm(202509)  # True
        >>> validate_yyyymm(202513)  # False - tháng 13 không tồn tại
    """
    if yyyymm < 202301 or yyyymm > 209912:
        return False
    
    year = yyyymm // 100
    month = yyyymm % 100
    
    return 2023 <= year <= 2099 and 1 <= month <= 12


def format_yyyymm_display(yyyymm: int) -> str:
    """
    Định dạng tháng/năm thành chuỗi hiển thị thân thiện
    
    Args:
        yyyymm (int): Tháng năm theo định dạng YYYYMM
        
    Returns:
        str: Chuỗi hiển thị (ví dụ: "Tháng 09/2025")
    
    Example:
        >>> format_yyyymm_display(202509)
        'Tháng 09/2025'
    """
    if not validate_yyyymm(yyyymm):
        return f"Tháng không hợp lệ: {yyyymm}"
    
    year = yyyymm // 100
    month = yyyymm % 100
    
    return f"Tháng {month:02d}/{year}"
