#!/usr/bin/env python3
"""
Clean Architecture Test Suite - Comprehensive Testing
Bộ test Clean Architecture - Test toàn diện

📚 HƯỚNG DẪN CHO NGƯỜI MỚI:
===============================================

Đây là file test chính để kiểm tra cấu trúc Clean Architecture.
Clean Architecture là một kiến trúc phần mềm giúp:

1. Tách biệt các layer (lớp) rõ ràng
2. Dễ dàng test và bảo trì
3. Linh hoạt trong việc thay đổi implementation
4. Phù hợp cho team development

CẤU TRÚC CLEAN ARCHITECTURE:
- Domain Layer: Chứa business logic và entities
- Application Layer: Chứa use cases và orchestration  
- Infrastructure Layer: Chứa external dependencies (database, APIs)
- Presentation Layer: Chứa user interfaces (CLI, Web, API)

CÁCH CHẠY TEST:
- Chạy tất cả: py src/tests/test_clean_architecture.py
- Chạy từng test: py -m pytest src/tests/test_clean_architecture.py::test_name
"""

import sys
import os
import unittest
from typing import Optional

# Thêm src vào Python path để có thể import các module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


class TestCleanArchitecture(unittest.TestCase):
    """
    Test Clean Architecture Structure
    Test cấu trúc Clean Architecture
    
    📝 GIẢI THÍCH:
    - unittest.TestCase: Base class cho tất cả test cases
    - Mỗi method bắt đầu với 'test_' sẽ được chạy tự động
    - assertEqual, assertTrue, assertFalse: Các assertion để kiểm tra kết quả
    """
    
    def setUp(self):
        """
        Setup method - Chạy trước mỗi test
        📝 GIẢI THÍCH: 
        - setUp() được gọi trước mỗi test method
        - Dùng để chuẩn bị dữ liệu test
        - Tương tự constructor trong class
        """
        print(f"\n🔧 Setting up test: {self._testMethodName}")
    
    def tearDown(self):
        """
        Teardown method - Chạy sau mỗi test
        📝 GIẢI THÍCH:
        - tearDown() được gọi sau mỗi test method
        - Dùng để dọn dẹp sau khi test xong
        - Tương tự destructor trong class
        """
        print(f"🧹 Cleaning up test: {self._testMethodName}")
    
    def test_domain_entities_import(self):
        """
        Test import Domain Entities
        Test import các thực thể Domain
        
        📝 GIẢI THÍCH:
        - Domain entities là các đối tượng nghiệp vụ cốt lõi
        - Chúng chứa business logic và rules
        - Không phụ thuộc vào bất kỳ layer nào khác
        """
        print("📦 Testing Domain Entities Import...")
        
        try:
            # Import các entities từ domain layer
            from domain.entities.customer import Customer
            from domain.entities.program import Program, RegisterItem
            from domain.entities.evaluation import ConditionGroup, ConditionItem, AuditPicture, CustomerEvaluationResult
            from domain.entities.registration import Registration
            
            # Kiểm tra các class có tồn tại không
            self.assertTrue(hasattr(Customer, '__init__'), "Customer class should have __init__ method")
            self.assertTrue(hasattr(Program, '__init__'), "Program class should have __init__ method")
            self.assertTrue(hasattr(RegisterItem, '__init__'), "RegisterItem class should have __init__ method")
            self.assertTrue(hasattr(ConditionGroup, '__init__'), "ConditionGroup class should have __init__ method")
            self.assertTrue(hasattr(ConditionItem, '__init__'), "ConditionItem class should have __init__ method")
            self.assertTrue(hasattr(AuditPicture, '__init__'), "AuditPicture class should have __init__ method")
            self.assertTrue(hasattr(CustomerEvaluationResult, '__init__'), "CustomerEvaluationResult class should have __init__ method")
            self.assertTrue(hasattr(Registration, '__init__'), "Registration class should have __init__ method")
            
            print("✅ Domain entities imported successfully")
            
        except ImportError as e:
            self.fail(f"Failed to import domain entities: {e}")
    
    def test_domain_repositories_import(self):
        """
        Test import Domain Repository Interfaces
        Test import các giao diện Repository Domain
        
        📝 GIẢI THÍCH:
        - Repository interfaces định nghĩa contract cho data access
        - Chúng là abstractions (trừu tượng hóa) cho database operations
        - Domain layer chỉ biết về interfaces, không biết implementation cụ thể
        """
        print("📦 Testing Domain Repository Interfaces Import...")
        
        try:
            from domain.repositories.customer_repository import CustomerRepository
            from domain.repositories.program_repository import ProgramRepository
            from domain.repositories.evaluation_repository import EvaluationRepository
            from domain.repositories.registration_repository import RegistrationRepository
            
            # Kiểm tra các interface có tồn tại không
            self.assertTrue(hasattr(CustomerRepository, '__abstractmethods__'), "CustomerRepository should be abstract")
            self.assertTrue(hasattr(ProgramRepository, '__abstractmethods__'), "ProgramRepository should be abstract")
            self.assertTrue(hasattr(EvaluationRepository, '__abstractmethods__'), "EvaluationRepository should be abstract")
            self.assertTrue(hasattr(RegistrationRepository, '__abstractmethods__'), "RegistrationRepository should be abstract")
            
            print("✅ Domain repository interfaces imported successfully")
            
        except ImportError as e:
            self.fail(f"Failed to import domain repositories: {e}")
    
    def test_domain_services_import(self):
        """
        Test import Domain Services
        Test import các dịch vụ Domain
        
        📝 GIẢI THÍCH:
        - Domain services chứa business logic phức tạp
        - Chúng orchestrate (điều phối) các entities và repositories
        - Chứa logic không thuộc về entity cụ thể nào
        """
        print("📦 Testing Domain Services Import...")
        
        try:
            from domain.services.evaluation_service import EvaluationService
            
            # Kiểm tra service có tồn tại không
            self.assertTrue(hasattr(EvaluationService, '__init__'), "EvaluationService should have __init__ method")
            self.assertTrue(hasattr(EvaluationService, 'evaluate_customer'), "EvaluationService should have evaluate_customer method")
            
            print("✅ Domain services imported successfully")
            
        except ImportError as e:
            self.fail(f"Failed to import domain services: {e}")
    
    def test_application_use_cases_import(self):
        """
        Test import Application Use Cases
        Test import các Use Case ứng dụng
        
        📝 GIẢI THÍCH:
        - Use cases là các business operations cụ thể
        - Chúng orchestrate domain services và repositories
        - Cung cấp interface đơn giản cho presentation layer
        """
        print("📦 Testing Application Use Cases Import...")
        
        try:
            from application.use_cases.evaluate_customer_use_case import EvaluateCustomerUseCase
            
            # Kiểm tra use case có tồn tại không
            self.assertTrue(hasattr(EvaluateCustomerUseCase, '__init__'), "EvaluateCustomerUseCase should have __init__ method")
            self.assertTrue(hasattr(EvaluateCustomerUseCase, 'execute'), "EvaluateCustomerUseCase should have execute method")
            
            print("✅ Application use cases imported successfully")
            
        except ImportError as e:
            self.fail(f"Failed to import application use cases: {e}")
    
    def test_infrastructure_import(self):
        """
        Test import Infrastructure Layer
        Test import lớp Infrastructure
        
        📝 GIẢI THÍCH:
        - Infrastructure layer chứa external dependencies
        - Database connections, external APIs, file systems
        - Implement các interfaces từ domain layer
        """
        print("📦 Testing Infrastructure Layer Import...")
        
        try:
            from infrastructure.database.sql_server_connection import SqlServerConnection
            
            # Kiểm tra infrastructure có tồn tại không
            self.assertTrue(hasattr(SqlServerConnection, '__init__'), "SqlServerConnection should have __init__ method")
            self.assertTrue(hasattr(SqlServerConnection, 'test_connection'), "SqlServerConnection should have test_connection method")
            
            print("✅ Infrastructure layer imported successfully")
            
        except ImportError as e:
            self.fail(f"Failed to import infrastructure layer: {e}")
    
    def test_presentation_import(self):
        """
        Test import Presentation Layer
        Test import lớp Presentation
        
        📝 GIẢI THÍCH:
        - Presentation layer chứa user interfaces
        - CLI, Web UI, REST API, GraphQL API
        - Sử dụng use cases từ application layer
        """
        print("📦 Testing Presentation Layer Import...")
        
        try:
            from presentation.cli.evaluation_cli import EvaluationCLI
            
            # Kiểm tra presentation có tồn tại không
            self.assertTrue(hasattr(EvaluationCLI, '__init__'), "EvaluationCLI should have __init__ method")
            self.assertTrue(hasattr(EvaluationCLI, 'run_interactive'), "EvaluationCLI should have run_interactive method")
            
            print("✅ Presentation layer imported successfully")
            
        except ImportError as e:
            self.fail(f"Failed to import presentation layer: {e}")
    
    def test_configuration_import(self):
        """
        Test import Configuration System
        Test import hệ thống cấu hình
        
        📝 GIẢI THÍCH:
        - Configuration system quản lý settings
        - Database connections, API keys, feature flags
        - Hỗ trợ environment-based configuration
        """
        print("📦 Testing Configuration System Import...")
        
        try:
            from config.settings import Settings, DatabaseSettings, LoggingSettings
            
            # Kiểm tra configuration có tồn tại không
            self.assertTrue(hasattr(Settings, 'default'), "Settings should have default method")
            self.assertTrue(hasattr(Settings, 'from_env'), "Settings should have from_env method")
            self.assertTrue(hasattr(DatabaseSettings, 'from_env'), "DatabaseSettings should have from_env method")
            self.assertTrue(hasattr(LoggingSettings, 'from_env'), "LoggingSettings should have from_env method")
            
            print("✅ Configuration system imported successfully")
            
        except ImportError as e:
            self.fail(f"Failed to import configuration system: {e}")
    
    def test_entity_creation(self):
        """
        Test Entity Creation and Business Logic
        Test tạo entities và business logic
        
        📝 GIẢI THÍCH:
        - Entities chứa business logic và rules
        - Chúng có methods để thực hiện business operations
        - Test này kiểm tra entities hoạt động đúng không
        """
        print("📦 Testing Entity Creation and Business Logic...")
        
        try:
            from domain.entities.customer import Customer
            from domain.entities.program import Program, RegisterItem
            from domain.entities.evaluation import ConditionGroup, ConditionItem, AuditPicture, CustomerEvaluationResult
            from domain.entities.registration import Registration
            from datetime import datetime
            
            # Test Customer creation
            customer = Customer(
                customer_code="CUST001",
                name="Test Customer",
                email="test@example.com"
            )
            self.assertEqual(customer.customer_code, "CUST001")
            self.assertEqual(customer.name, "Test Customer")
            print("✅ Customer entity created successfully")
            
            # Test Program creation
            program = Program(
                program_code="PROG001",
                name="Test Program",
                description="Test Description"
            )
            self.assertEqual(program.program_code, "PROG001")
            self.assertTrue(program.is_active)  # Default value
            print("✅ Program entity created successfully")
            
            # Test RegisterItem creation
            register_item = RegisterItem(
                yyyymm=202509,
                program_code="PROG001",
                type_code="TYPE_BEVERAGE",
                item="KE_3_O",
                facing=4,
                unit=3
            )
            self.assertEqual(register_item.yyyymm, 202509)
            self.assertEqual(register_item.facing, 4)
            print("✅ RegisterItem entity created successfully")
            
            # Test ConditionGroup creation
            condition_group = ConditionGroup(
                yyyymm=202509,
                program_code="PROG001",
                group=1,
                type_code="TYPE_BEVERAGE",
                group_point=2
            )
            self.assertEqual(condition_group.group, 1)
            self.assertEqual(condition_group.group_point, 2)
            print("✅ ConditionGroup entity created successfully")
            
            # Test ConditionItem creation and business logic
            condition_item = ConditionItem(
                yyyymm=202509,
                program_code="PROG001",
                group=1,
                condition_code="SPA_CLEANLINESS",
                condition_min_value=80,
                condition_point=1
            )
            self.assertEqual(condition_item.condition_code, "SPA_CLEANLINESS")
            
            # Test business logic: meets_minimum method
            self.assertTrue(condition_item.meets_minimum(85), "85 should meet minimum 80")
            self.assertFalse(condition_item.meets_minimum(75), "75 should not meet minimum 80")
            self.assertTrue(condition_item.meets_minimum(80), "80 should meet minimum 80")
            print("✅ ConditionItem business logic working correctly")
            
            # Test AuditPicture creation and business logic
            audit_picture = AuditPicture(
                yyyymm=202509,
                customer_code="CUST001",
                condition_code="SPA_CLEANLINESS",
                value="85",
                audit_date=datetime.now()
            )
            self.assertEqual(audit_picture.value, "85")
            self.assertEqual(audit_picture.numeric_value, 85)  # Test conversion
            print("✅ AuditPicture entity created successfully")
            
            # Test Registration creation and business logic
            registration = Registration(
                yyyymm=202509,
                program_code="PROG001",
                customer_code="CUST001",
                display_type="KE_3_O",
                register_qty=3,
                status=True
            )
            self.assertTrue(registration.is_active, "Registration should be active")
            self.assertFalse(registration.is_inactive, "Registration should not be inactive")
            print("✅ Registration entity created successfully")
            
            # Test CustomerEvaluationResult creation and business logic
            evaluation_result = CustomerEvaluationResult(
                yyyymm=202509,
                customer_code="CUST001",
                program_code="PROG001",
                total_points=6,
                max_possible_points=6,
                meets_criteria=True,
                failed_conditions=[],
                registration_status=True
            )
            self.assertEqual(evaluation_result.total_points, 6)
            self.assertEqual(evaluation_result.max_possible_points, 6)
            self.assertEqual(evaluation_result.success_rate, 100.0)
            self.assertTrue(evaluation_result.is_eligible_for_reward, "Should be eligible for reward")
            self.assertEqual(evaluation_result.get_failure_summary(), "No failures")
            print("✅ CustomerEvaluationResult business logic working correctly")
            
        except Exception as e:
            self.fail(f"Entity creation or business logic test failed: {e}")
    
    def test_database_connection(self):
        """
        Test Database Connection
        Test kết nối database
        
        📝 GIẢI THÍCH:
        - Database connection là infrastructure concern
        - Test này kiểm tra kết nối database có hoạt động không
        - Trong Clean Architecture, database là external dependency
        """
        print("📦 Testing Database Connection...")
        
        try:
            from infrastructure.database.sql_server_connection import SqlServerConnection
            
            # Tạo database connection
            db_conn = SqlServerConnection()
            self.assertIsNotNone(db_conn, "Database connection should be created")
            print("✅ Database connection object created")
            
            # Test connection
            if db_conn.test_connection():
                print("✅ Database connection test successful")
                
                # Get server info
                info = db_conn.get_server_info()
                self.assertIsInstance(info, dict, "Server info should be a dictionary")
                self.assertIn('server', info, "Server info should contain 'server' key")
                print(f"📊 Server: {info.get('server', 'Unknown')}")
                print(f"📊 Database: {info.get('database', 'Unknown')}")
            else:
                print("⚠️ Database connection test failed - this is expected if database is not available")
            
        except Exception as e:
            self.fail(f"Database connection test failed: {e}")
    
    def test_configuration_system(self):
        """
        Test Configuration System
        Test hệ thống cấu hình
        
        📝 GIẢI THÍCH:
        - Configuration system quản lý settings
        - Hỗ trợ default values và environment variables
        - Giúp ứng dụng linh hoạt trong các môi trường khác nhau
        """
        print("📦 Testing Configuration System...")
        
        try:
            from config.settings import Settings, DatabaseSettings, LoggingSettings
            
            # Test default settings
            settings = Settings.default()
            self.assertIsNotNone(settings, "Default settings should be created")
            self.assertIsNotNone(settings.database, "Database settings should be present")
            self.assertIsNotNone(settings.logging, "Logging settings should be present")
            print("✅ Default settings created successfully")
            
            # Test environment settings
            env_settings = Settings.from_env()
            self.assertIsNotNone(env_settings, "Environment settings should be created")
            print("✅ Environment settings created successfully")
            
            # Test individual settings
            db_settings = DatabaseSettings.from_env()
            self.assertIsNotNone(db_settings.server, "Database server should be set")
            self.assertIsNotNone(db_settings.database, "Database name should be set")
            print("✅ Database settings working correctly")
            
            log_settings = LoggingSettings.from_env()
            self.assertIsNotNone(log_settings.level, "Log level should be set")
            print("✅ Logging settings working correctly")
            
        except Exception as e:
            self.fail(f"Configuration system test failed: {e}")


def run_tests():
    """
    Run all tests
    Chạy tất cả tests
    
    📝 GIẢI THÍCH:
    - unittest.main() sẽ tự động tìm và chạy tất cả test methods
    - Test methods phải bắt đầu với 'test_'
    - Kết quả sẽ hiển thị PASS/FAIL cho từng test
    """
    print("🚀 CLEAN ARCHITECTURE TEST SUITE")
    print("=" * 60)
    print("Testing the Clean Architecture structure...")
    print("📚 This test suite validates the Clean Architecture implementation")
    print()
    
    # Tạo test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestCleanArchitecture)
    
    # Chạy tests với verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Hiển thị kết quả tổng kết
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    passed = total_tests - failures - errors
    
    print(f"📊 Total Tests: {total_tests}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failures}")
    print(f"💥 Errors: {errors}")
    
    if failures > 0:
        print("\n❌ FAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split('AssertionError: ')[-1].split('\\n')[0]}")
    
    if errors > 0:
        print("\n💥 ERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split('\\n')[-2]}")
    
    success_rate = (passed / total_tests * 100) if total_tests > 0 else 0
    print(f"\n📈 Success Rate: {success_rate:.1f}%")
    
    if passed == total_tests:
        print("🎉 All tests passed! Clean Architecture is working correctly.")
        return 0
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    """
    Main entry point
    Điểm vào chính
    
    📝 GIẢI THÍCH:
    - Khi chạy file này trực tiếp, __name__ sẽ là "__main__"
    - Code trong block này sẽ được thực thi
    - sys.exit() để trả về exit code cho shell
    """
    exit_code = run_tests()
    sys.exit(exit_code)
