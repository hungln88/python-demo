"""
Test cases for models.py - Comprehensive test coverage
Các test case cho models.py - Bao phủ test toàn diện
Created: 2025-09-19

Tệp này chứa các test case đầy đủ cho tất cả các model trong models.py.
Mỗi test case được thiết kế để kiểm tra một chức năng cụ thể và đảm bảo
tính chính xác của business logic.
"""

import unittest
from datetime import datetime
from models import (
    RegisterItem, Register, ConditionGroup, ConditionItem, 
    AuditPicture, CustomerEvaluationResult,
    DisplayType, ConditionCode, ProgramType,
    validate_yyyymm, format_yyyymm_display
)


class TestRegisterItem(unittest.TestCase):
    """
    Test cases cho class RegisterItem
    Kiểm tra chức năng cấu hình chương trình trưng bày
    """
    
    def setUp(self):
        """Thiết lập dữ liệu test cho mỗi test case"""
        self.valid_item = RegisterItem(
            yyyymm=202509,
            program_code="PROG001",
            type_code="TYPE_BEVERAGE",
            item="KE_3_O",
            facing=4,
            unit=3
        )
    
    def test_register_item_creation(self):
        """Test tạo RegisterItem với dữ liệu hợp lệ"""
        item = self.valid_item
        self.assertEqual(item.yyyymm, 202509)
        self.assertEqual(item.program_code, "PROG001")
        self.assertEqual(item.type_code, "TYPE_BEVERAGE")
        self.assertEqual(item.item, "KE_3_O")
        self.assertEqual(item.facing, 4)
        self.assertEqual(item.unit, 3)
    
    def test_register_item_equality(self):
        """Test so sánh hai RegisterItem"""
        item1 = self.valid_item
        item2 = RegisterItem(202509, "PROG001", "TYPE_BEVERAGE", "KE_3_O", 5, 2)  # facing, unit khác
        item3 = RegisterItem(202509, "PROG001", "TYPE_BEVERAGE", "KE_4_O", 4, 3)  # item khác
        
        # Cùng key fields (yyyymm, program_code, type_code, item) => bằng nhau
        self.assertEqual(item1, item2)
        # Khác item => không bằng nhau
        self.assertNotEqual(item1, item3)
        # So sánh với object khác loại
        self.assertNotEqual(item1, "not a RegisterItem")
    
    def test_get_total_capacity(self):
        """Test tính tổng sức chứa kệ"""
        item = self.valid_item
        expected_capacity = 4 * 3  # facing * unit = 12
        self.assertEqual(item.get_total_capacity(), expected_capacity)
        
        # Test với giá trị khác
        item2 = RegisterItem(202509, "PROG001", "TYPE_BEVERAGE", "KE_4_O", 6, 4)
        self.assertEqual(item2.get_total_capacity(), 24)
    
    def test_is_valid_positive_cases(self):
        """Test validation với dữ liệu hợp lệ"""
        valid_cases = [
            RegisterItem(202509, "PROG001", "TYPE_BEVERAGE", "KE_3_O", 4, 3),
            RegisterItem(202312, "PROG002", "TYPE_SNACK", "KE_4_O", 1, 1),
            RegisterItem(209912, "TEST", "TEST_TYPE", "TEST_ITEM", 10, 5)
        ]
        
        for item in valid_cases:
            with self.subTest(item=item):
                self.assertTrue(item.is_valid(), f"Item should be valid: {item}")
    
    def test_is_valid_negative_cases(self):
        """Test validation với dữ liệu không hợp lệ"""
        invalid_cases = [
            # Năm quá cũ
            RegisterItem(202200, "PROG001", "TYPE_BEVERAGE", "KE_3_O", 4, 3),
            # Program code rỗng
            RegisterItem(202509, "", "TYPE_BEVERAGE", "KE_3_O", 4, 3),
            RegisterItem(202509, "   ", "TYPE_BEVERAGE", "KE_3_O", 4, 3),
            # Type code rỗng
            RegisterItem(202509, "PROG001", "", "KE_3_O", 4, 3),
            # Item rỗng
            RegisterItem(202509, "PROG001", "TYPE_BEVERAGE", "", 4, 3),
            # Facing không dương
            RegisterItem(202509, "PROG001", "TYPE_BEVERAGE", "KE_3_O", 0, 3),
            RegisterItem(202509, "PROG001", "TYPE_BEVERAGE", "KE_3_O", -1, 3),
            # Unit không dương
            RegisterItem(202509, "PROG001", "TYPE_BEVERAGE", "KE_3_O", 4, 0),
            RegisterItem(202509, "PROG001", "TYPE_BEVERAGE", "KE_3_O", 4, -1),
        ]
        
        for item in invalid_cases:
            with self.subTest(item=item):
                self.assertFalse(item.is_valid(), f"Item should be invalid: {item}")


class TestRegister(unittest.TestCase):
    """
    Test cases cho class Register
    Kiểm tra chức năng đăng ký chương trình của khách hàng
    """
    
    def setUp(self):
        """Thiết lập dữ liệu test"""
        self.active_registration = Register(
            yyyymm=202509,
            program_code="PROG001",
            customer_code="CUST001",
            display_type="KE_3_O",
            register_qty=2,
            status=True
        )
        
        self.inactive_registration = Register(
            yyyymm=202509,
            program_code="PROG001",
            customer_code="CUST002",
            display_type="KE_4_O",
            register_qty=1,
            status=False
        )
    
    def test_register_creation(self):
        """Test tạo Register với dữ liệu hợp lệ"""
        reg = self.active_registration
        self.assertEqual(reg.yyyymm, 202509)
        self.assertEqual(reg.program_code, "PROG001")
        self.assertEqual(reg.customer_code, "CUST001")
        self.assertEqual(reg.display_type, "KE_3_O")
        self.assertEqual(reg.register_qty, 2)
        self.assertTrue(reg.status)
    
    def test_register_equality(self):
        """Test so sánh hai Register"""
        reg1 = self.active_registration
        reg2 = Register(202509, "PROG001", "CUST001", "KE_3_O", 5, False)  # qty, status khác
        reg3 = Register(202509, "PROG001", "CUST002", "KE_3_O", 2, True)   # customer khác
        
        # Cùng key fields => bằng nhau
        self.assertEqual(reg1, reg2)
        # Khác customer => không bằng nhau
        self.assertNotEqual(reg1, reg3)
    
    def test_is_active_property(self):
        """Test property is_active"""
        self.assertTrue(self.active_registration.is_active)
        self.assertFalse(self.inactive_registration.is_active)
    
    def test_is_inactive_property(self):
        """Test property is_inactive"""
        self.assertFalse(self.active_registration.is_inactive)
        self.assertTrue(self.inactive_registration.is_inactive)
    
    def test_get_registration_info(self):
        """Test lấy thông tin tóm tắt đăng ký"""
        active_info = self.active_registration.get_registration_info()
        inactive_info = self.inactive_registration.get_registration_info()
        
        self.assertIn("CUST001", active_info)
        self.assertIn("PROG001", active_info)
        self.assertIn("2 kệ", active_info)
        self.assertIn("KE_3_O", active_info)
        self.assertIn("Hoạt động", active_info)
        
        self.assertIn("CUST002", inactive_info)
        self.assertIn("Tạm ngừng", inactive_info)
    
    def test_is_valid_positive_cases(self):
        """Test validation với dữ liệu hợp lệ"""
        valid_cases = [
            self.active_registration,
            self.inactive_registration,
            Register(202312, "TEST", "CUSTOMER", "DISPLAY", 100, True)
        ]
        
        for reg in valid_cases:
            with self.subTest(reg=reg):
                self.assertTrue(reg.is_valid(), f"Registration should be valid: {reg}")
    
    def test_is_valid_negative_cases(self):
        """Test validation với dữ liệu không hợp lệ"""
        invalid_cases = [
            # Năm không hợp lệ
            Register(202200, "PROG001", "CUST001", "KE_3_O", 2, True),
            # Program code rỗng
            Register(202509, "", "CUST001", "KE_3_O", 2, True),
            Register(202509, "   ", "CUST001", "KE_3_O", 2, True),
            # Customer code rỗng
            Register(202509, "PROG001", "", "KE_3_O", 2, True),
            # Display type rỗng
            Register(202509, "PROG001", "CUST001", "", 2, True),
            # Quantity không dương
            Register(202509, "PROG001", "CUST001", "KE_3_O", 0, True),
            Register(202509, "PROG001", "CUST001", "KE_3_O", -1, True),
        ]
        
        for reg in invalid_cases:
            with self.subTest(reg=reg):
                self.assertFalse(reg.is_valid(), f"Registration should be invalid: {reg}")


class TestConditionGroup(unittest.TestCase):
    """Test cases cho class ConditionGroup"""
    
    def setUp(self):
        self.valid_group = ConditionGroup(
            yyyymm=202509,
            program_code="PROG001",
            group=1,
            type_code="TYPE_BEVERAGE",
            group_point=100
        )
    
    def test_condition_group_creation(self):
        """Test tạo ConditionGroup"""
        group = self.valid_group
        self.assertEqual(group.yyyymm, 202509)
        self.assertEqual(group.program_code, "PROG001")
        self.assertEqual(group.group, 1)
        self.assertEqual(group.type_code, "TYPE_BEVERAGE")
        self.assertEqual(group.group_point, 100)
    
    def test_condition_group_equality(self):
        """Test so sánh ConditionGroup"""
        group1 = self.valid_group
        group2 = ConditionGroup(202509, "PROG001", 1, "TYPE_SNACK", 80)  # type_code, point khác
        group3 = ConditionGroup(202509, "PROG001", 2, "TYPE_BEVERAGE", 100)  # group khác
        
        self.assertEqual(group1, group2)  # Cùng yyyymm, program_code, group
        self.assertNotEqual(group1, group3)  # Khác group
    
    def test_is_valid_positive_cases(self):
        """Test validation hợp lệ"""
        valid_cases = [
            self.valid_group,
            ConditionGroup(202312, "TEST", 5, "TYPE_TEST", 1)
        ]
        
        for group in valid_cases:
            with self.subTest(group=group):
                self.assertTrue(group.is_valid())
    
    def test_is_valid_negative_cases(self):
        """Test validation không hợp lệ"""
        invalid_cases = [
            ConditionGroup(202200, "PROG001", 1, "TYPE_BEVERAGE", 100),  # năm cũ
            ConditionGroup(202509, "", 1, "TYPE_BEVERAGE", 100),  # program rỗng
            ConditionGroup(202509, "PROG001", 0, "TYPE_BEVERAGE", 100),  # group không dương
            ConditionGroup(202509, "PROG001", 1, "", 100),  # type_code rỗng
            ConditionGroup(202509, "PROG001", 1, "TYPE_BEVERAGE", 0),  # point không dương
        ]
        
        for group in invalid_cases:
            with self.subTest(group=group):
                self.assertFalse(group.is_valid())


class TestConditionItem(unittest.TestCase):
    """Test cases cho class ConditionItem"""
    
    def setUp(self):
        self.valid_item = ConditionItem(
            yyyymm=202509,
            program_code="PROG001",
            group=1,
            condition_code="CLEANLINESS",
            condition_min_value=80,
            condition_point=30
        )
    
    def test_condition_item_creation(self):
        """Test tạo ConditionItem"""
        item = self.valid_item
        self.assertEqual(item.yyyymm, 202509)
        self.assertEqual(item.program_code, "PROG001")
        self.assertEqual(item.group, 1)
        self.assertEqual(item.condition_code, "CLEANLINESS")
        self.assertEqual(item.condition_min_value, 80)
        self.assertEqual(item.condition_point, 30)
    
    def test_meets_minimum(self):
        """Test kiểm tra đạt yêu cầu tối thiểu"""
        item = self.valid_item  # min_value = 80
        
        # Test các trường hợp đạt yêu cầu
        self.assertTrue(item.meets_minimum(80))  # Bằng đúng
        self.assertTrue(item.meets_minimum(85))  # Lớn hơn
        self.assertTrue(item.meets_minimum(100))  # Lớn hơn nhiều
        
        # Test các trường hợp không đạt
        self.assertFalse(item.meets_minimum(79))  # Nhỏ hơn 1
        self.assertFalse(item.meets_minimum(0))   # Nhỏ hơn nhiều
        self.assertFalse(item.meets_minimum(-5))  # Âm
    
    def test_calculate_points(self):
        """Test tính điểm dựa trên giá trị thực tế"""
        item = self.valid_item  # min_value = 80, point = 30
        
        # Đạt yêu cầu => được full point
        self.assertEqual(item.calculate_points(80), 30)
        self.assertEqual(item.calculate_points(90), 30)
        self.assertEqual(item.calculate_points(100), 30)
        
        # Không đạt => 0 điểm
        self.assertEqual(item.calculate_points(79), 0)
        self.assertEqual(item.calculate_points(50), 0)
        self.assertEqual(item.calculate_points(0), 0)
    
    def test_get_performance_ratio(self):
        """Test tính tỷ lệ hiệu suất"""
        item = self.valid_item  # min_value = 80
        
        self.assertEqual(item.get_performance_ratio(80), 1.0)  # 80/80 = 1.0
        self.assertEqual(item.get_performance_ratio(100), 1.25)  # 100/80 = 1.25
        self.assertEqual(item.get_performance_ratio(40), 0.5)  # 40/80 = 0.5
        
        # Test trường hợp min_value = 0
        zero_item = ConditionItem(202509, "PROG001", 1, "TEST", 0, 10)
        self.assertEqual(zero_item.get_performance_ratio(50), 0.0)
    
    def test_is_valid_positive_cases(self):
        """Test validation hợp lệ"""
        valid_cases = [
            self.valid_item,
            ConditionItem(202312, "TEST", 1, "TEST_CODE", 0, 1),  # min_value = 0
            ConditionItem(202312, "TEST", 1, "TEST_CODE", 100, 1),  # min_value = 100
        ]
        
        for item in valid_cases:
            with self.subTest(item=item):
                self.assertTrue(item.is_valid())
    
    def test_is_valid_negative_cases(self):
        """Test validation không hợp lệ"""
        invalid_cases = [
            ConditionItem(202200, "PROG001", 1, "CLEANLINESS", 80, 30),  # năm cũ
            ConditionItem(202509, "", 1, "CLEANLINESS", 80, 30),  # program rỗng
            ConditionItem(202509, "PROG001", 0, "CLEANLINESS", 80, 30),  # group không dương
            ConditionItem(202509, "PROG001", 1, "", 80, 30),  # condition_code rỗng
            ConditionItem(202509, "PROG001", 1, "CLEANLINESS", -1, 30),  # min_value < 0
            ConditionItem(202509, "PROG001", 1, "CLEANLINESS", 101, 30),  # min_value > 100
            ConditionItem(202509, "PROG001", 1, "CLEANLINESS", 80, 0),  # point không dương
        ]
        
        for item in invalid_cases:
            with self.subTest(item=item):
                self.assertFalse(item.is_valid())


class TestAuditPicture(unittest.TestCase):
    """Test cases cho class AuditPicture"""
    
    def setUp(self):
        self.valid_audit = AuditPicture(
            yyyymm=202509,
            customer_code="CUST001",
            condition_code="CLEANLINESS",
            value="85",
            audit_date=datetime(2025, 9, 15, 10, 30)
        )
    
    def test_audit_picture_creation(self):
        """Test tạo AuditPicture"""
        audit = self.valid_audit
        self.assertEqual(audit.yyyymm, 202509)
        self.assertEqual(audit.customer_code, "CUST001")
        self.assertEqual(audit.condition_code, "CLEANLINESS")
        self.assertEqual(audit.value, "85")
        self.assertIsNotNone(audit.audit_date)
    
    def test_numeric_value_property(self):
        """Test chuyển đổi value thành số"""
        test_cases = [
            ("85", 85),
            ("85.7", 85),  # Float được làm tròn xuống
            ("100", 100),
            ("0", 0),
            ("invalid", 0),  # Giá trị không hợp lệ => 0
            ("", 0),  # Chuỗi rỗng => 0
        ]
        
        for value_str, expected in test_cases:
            with self.subTest(value=value_str):
                audit = AuditPicture(202509, "CUST001", "TEST", value_str)
                self.assertEqual(audit.numeric_value, expected)
    
    def test_is_valid_value_property(self):
        """Test kiểm tra giá trị hợp lệ (0-100)"""
        valid_values = ["0", "50", "100", "85.5"]
        invalid_values = ["-1", "101", "150", "invalid", ""]
        
        for value in valid_values:
            with self.subTest(value=value):
                audit = AuditPicture(202509, "CUST001", "TEST", value)
                self.assertTrue(audit.is_valid_value, f"Value {value} should be valid")
        
        for value in invalid_values:
            with self.subTest(value=value):
                audit = AuditPicture(202509, "CUST001", "TEST", value)
                self.assertFalse(audit.is_valid_value, f"Value {value} should be invalid")
    
    def test_get_audit_summary(self):
        """Test lấy thông tin tóm tắt audit"""
        audit = self.valid_audit
        summary = audit.get_audit_summary()
        
        self.assertIn("CUST001", summary)
        self.assertIn("CLEANLINESS", summary)
        self.assertIn("85", summary)
        self.assertIn("15/09/2025", summary)  # Định dạng ngày dd/mm/yyyy
        
        # Test với audit không có ngày
        audit_no_date = AuditPicture(202509, "CUST002", "TEST", "90")
        summary_no_date = audit_no_date.get_audit_summary()
        self.assertIn("Chưa xác định", summary_no_date)
    
    def test_is_valid_positive_cases(self):
        """Test validation hợp lệ"""
        valid_cases = [
            self.valid_audit,
            AuditPicture(202312, "CUSTOMER", "CONDITION", "0"),
            AuditPicture(202312, "CUSTOMER", "CONDITION", "100"),
        ]
        
        for audit in valid_cases:
            with self.subTest(audit=audit):
                self.assertTrue(audit.is_valid())
    
    def test_is_valid_negative_cases(self):
        """Test validation không hợp lệ"""
        invalid_cases = [
            AuditPicture(202200, "CUST001", "CLEANLINESS", "85"),  # năm cũ
            AuditPicture(202509, "", "CLEANLINESS", "85"),  # customer rỗng
            AuditPicture(202509, "CUST001", "", "85"),  # condition rỗng
            AuditPicture(202509, "CUST001", "CLEANLINESS", ""),  # value rỗng
            AuditPicture(202509, "CUST001", "CLEANLINESS", "invalid"),  # value không hợp lệ
            AuditPicture(202509, "CUST001", "CLEANLINESS", "101"),  # value > 100
            AuditPicture(202509, "CUST001", "CLEANLINESS", "-1"),  # value < 0
        ]
        
        for audit in invalid_cases:
            with self.subTest(audit=audit):
                self.assertFalse(audit.is_valid())


class TestCustomerEvaluationResult(unittest.TestCase):
    """Test cases cho class CustomerEvaluationResult"""
    
    def setUp(self):
        self.excellent_result = CustomerEvaluationResult(
            yyyymm=202509,
            customer_code="CUST001",
            program_code="PROG001",
            total_points=90,
            max_possible_points=100,
            meets_criteria=True,
            failed_conditions=[],
            registration_status=True
        )
        
        self.failed_result = CustomerEvaluationResult(
            yyyymm=202509,
            customer_code="CUST002",
            program_code="PROG001",
            total_points=60,
            max_possible_points=100,
            meets_criteria=False,
            failed_conditions=["CLEANLINESS_BELOW_MINIMUM", "DISPLAY_QUALITY_BELOW_MINIMUM"],
            registration_status=True
        )
        
        self.inactive_result = CustomerEvaluationResult(
            yyyymm=202509,
            customer_code="CUST003",
            program_code="PROG001",
            total_points=100,
            max_possible_points=100,
            meets_criteria=True,
            failed_conditions=[],
            registration_status=False  # Không hoạt động
        )
    
    def test_success_rate_property(self):
        """Test tính tỷ lệ thành công"""
        self.assertEqual(self.excellent_result.success_rate, 90.0)  # 90/100 * 100
        self.assertEqual(self.failed_result.success_rate, 60.0)  # 60/100 * 100
        
        # Test trường hợp max_possible_points = 0
        zero_result = CustomerEvaluationResult(
            202509, "CUST", "PROG", 0, 0, False, [], True
        )
        self.assertEqual(zero_result.success_rate, 0.0)
    
    def test_is_eligible_for_reward_property(self):
        """Test kiểm tra đủ điều kiện nhận thưởng"""
        # Đạt tiêu chí + đăng ký hoạt động => đủ điều kiện
        self.assertTrue(self.excellent_result.is_eligible_for_reward)
        
        # Không đạt tiêu chí => không đủ điều kiện
        self.assertFalse(self.failed_result.is_eligible_for_reward)
        
        # Đạt tiêu chí nhưng đăng ký không hoạt động => không đủ điều kiện
        self.assertFalse(self.inactive_result.is_eligible_for_reward)
    
    def test_performance_grade_property(self):
        """Test xếp loại hiệu suất"""
        test_cases = [
            (95, "Xuất sắc"),  # >= 90%
            (90, "Xuất sắc"),
            (85, "Tốt"),      # >= 80%
            (80, "Tốt"),
            (75, "Trung bình"),  # >= 70%
            (70, "Trung bình"),
            (65, "Yếu"),      # < 70%
            (0, "Yếu"),
        ]
        
        for points, expected_grade in test_cases:
            with self.subTest(points=points):
                result = CustomerEvaluationResult(
                    202509, "CUST", "PROG", points, 100, True, [], True
                )
                self.assertEqual(result.performance_grade, expected_grade)
    
    def test_get_failure_summary(self):
        """Test lấy tóm tắt lý do thất bại"""
        # Không có lỗi
        self.assertEqual(self.excellent_result.get_failure_summary(), "Đạt tất cả tiêu chí")
        
        # Có lỗi
        failure_summary = self.failed_result.get_failure_summary()
        self.assertIn("Thất bại:", failure_summary)
        self.assertIn("CLEANLINESS_BELOW_MINIMUM", failure_summary)
        self.assertIn("DISPLAY_QUALITY_BELOW_MINIMUM", failure_summary)
    
    def test_get_detailed_summary(self):
        """Test lấy thông tin chi tiết"""
        summary = self.excellent_result.get_detailed_summary()
        
        # Kiểm tra các thông tin cần thiết có trong summary
        self.assertIn("CUST001", summary)
        self.assertIn("PROG001", summary)
        self.assertIn("202509", summary)
        self.assertIn("90/100", summary)
        self.assertIn("90.0%", summary)
        self.assertIn("Xuất sắc", summary)
        self.assertIn("Hoạt động", summary)
        self.assertIn("Có", summary)  # Đủ điều kiện nhận thưởng
        
        # Test với kết quả thất bại
        failed_summary = self.failed_result.get_detailed_summary()
        self.assertIn("Không", failed_summary)  # Không đủ điều kiện


class TestEnumClasses(unittest.TestCase):
    """Test cases cho các enum classes"""
    
    def test_display_type_enum(self):
        """Test DisplayType enum"""
        # Test constants
        self.assertEqual(DisplayType.KE_3_O, "KE_3_O")
        self.assertEqual(DisplayType.KE_4_O, "KE_4_O")
        self.assertEqual(DisplayType.KE_TRUONG_BAY, "KE_TRUONG_BAY")
        
        # Test all_types method
        all_types = DisplayType.all_types()
        self.assertEqual(len(all_types), 3)
        self.assertIn("KE_3_O", all_types)
        self.assertIn("KE_4_O", all_types)
        self.assertIn("KE_TRUONG_BAY", all_types)
        
        # Test is_valid_type method
        self.assertTrue(DisplayType.is_valid_type("KE_3_O"))
        self.assertTrue(DisplayType.is_valid_type("KE_4_O"))
        self.assertTrue(DisplayType.is_valid_type("KE_TRUONG_BAY"))
        self.assertFalse(DisplayType.is_valid_type("INVALID"))
        self.assertFalse(DisplayType.is_valid_type(""))
        
        # Test get_description method
        desc_3o = DisplayType.get_description("KE_3_O")
        self.assertIn("3 ô", desc_3o)
        
        desc_invalid = DisplayType.get_description("INVALID")
        self.assertIn("không xác định", desc_invalid)
    
    def test_condition_code_enum(self):
        """Test ConditionCode enum"""
        # Test constants
        self.assertEqual(ConditionCode.CLEANLINESS, "CLEANLINESS")
        self.assertEqual(ConditionCode.PRODUCT_AVAILABILITY, "PRODUCT_AVAILABILITY")
        self.assertEqual(ConditionCode.DISPLAY_QUALITY, "DISPLAY_QUALITY")
        
        # Test all_codes method
        all_codes = ConditionCode.all_codes()
        self.assertEqual(len(all_codes), 3)
        
        # Test is_valid_code method
        self.assertTrue(ConditionCode.is_valid_code("CLEANLINESS"))
        self.assertFalse(ConditionCode.is_valid_code("INVALID"))
        
        # Test get_description method
        desc = ConditionCode.get_description("CLEANLINESS")
        self.assertIn("sạch sẽ", desc.lower())
    
    def test_program_type_enum(self):
        """Test ProgramType enum"""
        # Test constants
        self.assertEqual(ProgramType.TYPE_BEVERAGE, "TYPE_BEVERAGE")
        self.assertEqual(ProgramType.TYPE_SNACK, "TYPE_SNACK")
        
        # Test all_types method
        all_types = ProgramType.all_types()
        self.assertEqual(len(all_types), 2)
        
        # Test is_valid_type method
        self.assertTrue(ProgramType.is_valid_type("TYPE_BEVERAGE"))
        self.assertFalse(ProgramType.is_valid_type("INVALID"))
        
        # Test get_description method
        desc = ProgramType.get_description("TYPE_BEVERAGE")
        self.assertIn("đồ uống", desc.lower())


class TestHelperFunctions(unittest.TestCase):
    """Test cases cho các helper functions"""
    
    def test_validate_yyyymm_positive_cases(self):
        """Test validate_yyyymm với giá trị hợp lệ"""
        valid_cases = [
            202301,  # Tháng 1/2023
            202312,  # Tháng 12/2023
            202509,  # Tháng 9/2025
            209912,  # Tháng 12/2099
        ]
        
        for yyyymm in valid_cases:
            with self.subTest(yyyymm=yyyymm):
                self.assertTrue(validate_yyyymm(yyyymm), f"{yyyymm} should be valid")
    
    def test_validate_yyyymm_negative_cases(self):
        """Test validate_yyyymm với giá trị không hợp lệ"""
        invalid_cases = [
            202200,  # Năm 2022 (quá cũ)
            210001,  # Năm 2100 (quá xa)
            202300,  # Tháng 0 (không tồn tại)
            202313,  # Tháng 13 (không tồn tại)
            202399,  # Tháng 99 (không tồn tại)
        ]
        
        for yyyymm in invalid_cases:
            with self.subTest(yyyymm=yyyymm):
                self.assertFalse(validate_yyyymm(yyyymm), f"{yyyymm} should be invalid")
    
    def test_format_yyyymm_display(self):
        """Test format_yyyymm_display"""
        test_cases = [
            (202509, "Tháng 09/2025"),
            (202312, "Tháng 12/2023"),
            (202401, "Tháng 01/2024"),
        ]
        
        for yyyymm, expected in test_cases:
            with self.subTest(yyyymm=yyyymm):
                result = format_yyyymm_display(yyyymm)
                self.assertEqual(result, expected)
        
        # Test với giá trị không hợp lệ
        invalid_result = format_yyyymm_display(202313)
        self.assertIn("không hợp lệ", invalid_result)


if __name__ == '__main__':
    # Chạy tất cả test cases
    # Cấu hình test runner để hiển thị thông tin chi tiết
    unittest.main(verbosity=2, buffer=True)
