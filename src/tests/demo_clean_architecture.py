#!/usr/bin/env python3
"""
Clean Architecture Demo - Comprehensive Demo for Beginners
Demo Clean Architecture - Demo toàn diện cho người mới

📚 HƯỚNG DẪN CHO NGƯỜI MỚI HỌC CLEAN ARCHITECTURE:
=======================================================

Clean Architecture là gì?
-------------------------
Clean Architecture là một kiến trúc phần mềm được thiết kế bởi Robert C. Martin (Uncle Bob).
Mục tiêu chính là tạo ra code dễ test, dễ bảo trì và linh hoạt.

Tại sao cần Clean Architecture?
-------------------------------
1. SEPARATION OF CONCERNS (Tách biệt mối quan tâm):
   - Mỗi layer có trách nhiệm riêng biệt
   - Dễ hiểu và debug
   - Dễ thay đổi một phần mà không ảnh hưởng phần khác

2. DEPENDENCY INVERSION (Đảo ngược phụ thuộc):
   - High-level modules không phụ thuộc vào low-level modules
   - Cả hai đều phụ thuộc vào abstractions (interfaces)
   - Dễ dàng thay đổi implementation

3. TESTABILITY (Khả năng test):
   - Domain logic có thể test độc lập
   - Infrastructure có thể mock
   - Dễ dàng viết unit tests

4. MAINTAINABILITY (Khả năng bảo trì):
   - Code dễ đọc và hiểu
   - Dễ thêm tính năng mới
   - Dễ sửa lỗi

CẤU TRÚC CLEAN ARCHITECTURE:
============================

┌─────────────────────────────────────────┐
│           PRESENTATION LAYER            │  ← User Interface (CLI, Web, API)
│         (Giao diện người dùng)          │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│           APPLICATION LAYER             │  ← Use Cases (Business Operations)
│         (Lớp ứng dụng)                  │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│             DOMAIN LAYER                │  ← Business Logic & Entities
│         (Lớp nghiệp vụ)                 │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│          INFRASTRUCTURE LAYER           │  ← External Dependencies
│         (Lớp hạ tầng)                   │
└─────────────────────────────────────────┘

NGUYÊN TẮC QUAN TRỌNG:
=====================
1. DEPENDENCY RULE: Dependencies chỉ được trỏ vào trong (inner layers)
2. INTERFACE SEGREGATION: Sử dụng interfaces thay vì concrete classes
3. SINGLE RESPONSIBILITY: Mỗi class chỉ có một lý do để thay đổi
4. OPEN/CLOSED: Mở cho extension, đóng cho modification

CÁCH CHẠY DEMO:
===============
- Chạy demo: py src/tests/demo_clean_architecture.py
- Chạy tests: py src/tests/test_clean_architecture.py
- Chạy ứng dụng: py src/main.py
"""

import sys
import os
from datetime import datetime

# Thêm src vào Python path để có thể import các module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def demo_clean_architecture():
    """
    Demo Clean Architecture - Comprehensive demonstration
    Demo Clean Architecture - Demo toàn diện
    
    📝 GIẢI THÍCH:
    - Function này sẽ demo từng layer của Clean Architecture
    - Mỗi section sẽ giải thích chi tiết cho người mới
    - Sẽ tạo và sử dụng các objects từ mỗi layer
    """
    print("🚀 CLEAN ARCHITECTURE COMPREHENSIVE DEMO")
    print("=" * 70)
    print("📚 Demo toàn diện Clean Architecture cho người mới học")
    print("🎯 Mục tiêu: Hiểu rõ cách Clean Architecture hoạt động")
    print()
    
    try:
        # ========================================
        # DEMO 1: DOMAIN LAYER - Business Logic
        # ========================================
        print("📦 DEMO 1: DOMAIN LAYER - Business Logic")
        print("=" * 50)
        print("🎯 Mục tiêu: Hiểu Domain Layer chứa gì và tại sao quan trọng")
        print()
        
        print("📝 GIẢI THÍCH DOMAIN LAYER:")
        print("   • Domain Layer là trái tim của ứng dụng")
        print("   • Chứa business logic và rules")
        print("   • Không phụ thuộc vào bất kỳ layer nào khác")
        print("   • Bao gồm: Entities, Value Objects, Domain Services")
        print()
        
        # Import Domain Entities
        print("🔧 Importing Domain Entities...")
        from domain.entities.customer import Customer
        from domain.entities.program import Program, RegisterItem
        from domain.entities.evaluation import ConditionGroup, ConditionItem, AuditPicture, CustomerEvaluationResult
        from domain.entities.registration import Registration
        print("✅ Domain entities imported successfully")
        print()
        
        # Tạo và demo Customer Entity
        print("👤 Creating Customer Entity:")
        customer = Customer(
            customer_code="CUST001",
            name="Demo Customer",
            email="demo@example.com",
            phone="0123456789"
        )
        print(f"   • Customer: {customer}")
        print(f"   • String representation: {str(customer)}")
        print(f"   • Debug representation: {repr(customer)}")
        print(f"   • Hash value: {hash(customer)}")
        print("   📝 GIẢI THÍCH: Customer là một Entity - có identity và lifecycle")
        print()
        
        # Tạo và demo Program Entity
        print("📋 Creating Program Entity:")
        program = Program(
            program_code="PROG001",
            name="Demo Display Program",
            description="Chương trình trưng bày sản phẩm",
            is_active=True
        )
        print(f"   • Program: {program}")
        print(f"   • Is Active: {program.is_active}")
        print("   📝 GIẢI THÍCH: Program là một Entity - đại diện cho chương trình trưng bày")
        print()
        
        # Tạo và demo RegisterItem Entity
        print("🏪 Creating RegisterItem Entity:")
        register_item = RegisterItem(
            yyyymm=202509,
            program_code="PROG001",
            type_code="TYPE_BEVERAGE",
            item="KE_3_O",
            facing=4,
            unit=3
        )
        print(f"   • Register Item: {register_item}")
        print(f"   • Facing: {register_item.facing} sản phẩm/ô")
        print(f"   • Unit: {register_item.unit} ô/kệ")
        print("   📝 GIẢI THÍCH: RegisterItem là Value Object - cấu hình kệ trưng bày")
        print()
        
        # Tạo và demo ConditionGroup Entity
        print("📊 Creating ConditionGroup Entity:")
        condition_group = ConditionGroup(
            yyyymm=202509,
            program_code="PROG001",
            group=1,
            type_code="TYPE_BEVERAGE",
            group_point=2
        )
        print(f"   • Condition Group: {condition_group}")
        print(f"   • Required Points: {condition_group.group_point}")
        print("   📝 GIẢI THÍCH: ConditionGroup định nghĩa nhóm điều kiện đánh giá")
        print()
        
        # Tạo và demo ConditionItem Entity với Business Logic
        print("📝 Creating ConditionItem Entity with Business Logic:")
        condition_item = ConditionItem(
            yyyymm=202509,
            program_code="PROG001",
            group=1,
            condition_code="SPA_CLEANLINESS",
            condition_min_value=80,
            condition_point=1
        )
        print(f"   • Condition Item: {condition_item}")
        print(f"   • Min Value: {condition_item.condition_min_value}")
        print(f"   • Points: {condition_item.condition_point}")
        
        # Demo business logic
        print("   🧠 Testing Business Logic:")
        test_values = [85, 75, 90, 80, 95]
        for value in test_values:
            meets = condition_item.meets_minimum(value)
            status = "✅ PASS" if meets else "❌ FAIL"
            print(f"      Value {value}: {status}")
        print("   📝 GIẢI THÍCH: ConditionItem chứa business logic - kiểm tra điều kiện")
        print()
        
        # Tạo và demo AuditPicture Entity
        print("📸 Creating AuditPicture Entity:")
        audit_picture = AuditPicture(
            yyyymm=202509,
            customer_code="CUST001",
            condition_code="SPA_CLEANLINESS",
            value="85",
            audit_date=datetime.now()
        )
        print(f"   • Audit Picture: {audit_picture}")
        print(f"   • Value: {audit_picture.value}")
        print(f"   • Numeric Value: {audit_picture.numeric_value}")
        print("   📝 GIẢI THÍCH: AuditPicture chứa kết quả audit thực tế")
        print()
        
        # Tạo và demo Registration Entity
        print("📝 Creating Registration Entity:")
        registration = Registration(
            yyyymm=202509,
            program_code="PROG001",
            customer_code="CUST001",
            display_type="KE_3_O",
            register_qty=3,
            status=True
        )
        print(f"   • Registration: {registration}")
        print(f"   • Is Active: {registration.is_active}")
        print(f"   • Is Inactive: {registration.is_inactive}")
        
        # Demo business methods
        print("   🔄 Testing Business Methods:")
        registration.deactivate()
        print(f"      After deactivate: {registration.is_active}")
        registration.activate()
        print(f"      After activate: {registration.is_active}")
        print("   📝 GIẢI THÍCH: Registration có business methods để quản lý trạng thái")
        print()
        
        # Tạo và demo CustomerEvaluationResult Entity
        print("🏆 Creating CustomerEvaluationResult Entity:")
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
        print(f"   • Evaluation Result: {evaluation_result}")
        print(f"   • Total Points: {evaluation_result.total_points}/{evaluation_result.max_possible_points}")
        print(f"   • Success Rate: {evaluation_result.success_rate:.1f}%")
        print(f"   • Meets Criteria: {evaluation_result.meets_criteria}")
        print(f"   • Registration Status: {evaluation_result.registration_status}")
        print(f"   • Is Eligible: {evaluation_result.is_eligible_for_reward}")
        print(f"   • Failure Summary: {evaluation_result.get_failure_summary()}")
        print("   📝 GIẢI THÍCH: CustomerEvaluationResult chứa kết quả đánh giá cuối cùng")
        print()
        
        # ========================================
        # DEMO 2: DOMAIN REPOSITORIES - Interfaces
        # ========================================
        print("📦 DEMO 2: DOMAIN REPOSITORIES - Interfaces")
        print("=" * 50)
        print("🎯 Mục tiêu: Hiểu Repository Pattern và Dependency Inversion")
        print()
        
        print("📝 GIẢI THÍCH REPOSITORY PATTERN:")
        print("   • Repository Pattern tách biệt business logic khỏi data access")
        print("   • Domain layer chỉ biết về interfaces, không biết implementation")
        print("   • Dễ dàng thay đổi database mà không ảnh hưởng business logic")
        print("   • Dễ dàng mock cho testing")
        print()
        
        # Import Repository Interfaces
        print("🔧 Importing Repository Interfaces...")
        from domain.repositories.customer_repository import CustomerRepository
        from domain.repositories.program_repository import ProgramRepository
        from domain.repositories.evaluation_repository import EvaluationRepository
        from domain.repositories.registration_repository import RegistrationRepository
        print("✅ Repository interfaces imported successfully")
        print()
        
        # Demo Repository Interfaces
        print("🔍 Analyzing Repository Interfaces:")
        print(f"   • CustomerRepository methods: {[method for method in dir(CustomerRepository) if not method.startswith('_')]}")
        print(f"   • ProgramRepository methods: {[method for method in dir(ProgramRepository) if not method.startswith('_')]}")
        print(f"   • EvaluationRepository methods: {[method for method in dir(EvaluationRepository) if not method.startswith('_')]}")
        print(f"   • RegistrationRepository methods: {[method for method in dir(RegistrationRepository) if not method.startswith('_')]}")
        print("   📝 GIẢI THÍCH: Interfaces định nghĩa contract cho data access")
        print()
        
        # ========================================
        # DEMO 3: DOMAIN SERVICES - Business Logic
        # ========================================
        print("📦 DEMO 3: DOMAIN SERVICES - Business Logic")
        print("=" * 50)
        print("🎯 Mục tiêu: Hiểu Domain Services và complex business logic")
        print()
        
        print("📝 GIẢI THÍCH DOMAIN SERVICES:")
        print("   • Domain Services chứa business logic phức tạp")
        print("   • Logic không thuộc về entity cụ thể nào")
        print("   • Orchestrate (điều phối) các entities và repositories")
        print("   • Chứa business rules và workflows")
        print()
        
        # Import Domain Service
        print("🔧 Importing Domain Service...")
        from domain.services.evaluation_service import EvaluationService
        print("✅ Domain service imported successfully")
        print()
        
        # Demo Domain Service
        print("🔍 Analyzing Domain Service:")
        print(f"   • EvaluationService methods: {[method for method in dir(EvaluationService) if not method.startswith('_')]}")
        print("   📝 GIẢI THÍCH: EvaluationService chứa logic đánh giá khách hàng")
        print()
        
        # ========================================
        # DEMO 4: APPLICATION LAYER - Use Cases
        # ========================================
        print("📦 DEMO 4: APPLICATION LAYER - Use Cases")
        print("=" * 50)
        print("🎯 Mục tiêu: Hiểu Application Layer và Use Cases")
        print()
        
        print("📝 GIẢI THÍCH APPLICATION LAYER:")
        print("   • Application Layer chứa Use Cases")
        print("   • Use Cases là business operations cụ thể")
        print("   • Orchestrate Domain Services và Repositories")
        print("   • Cung cấp interface đơn giản cho Presentation Layer")
        print("   • Chứa application-specific business logic")
        print()
        
        # Import Use Case
        print("🔧 Importing Use Case...")
        from application.use_cases.evaluate_customer_use_case import EvaluateCustomerUseCase
        print("✅ Use case imported successfully")
        print()
        
        # Demo Use Case
        print("🔍 Analyzing Use Case:")
        print(f"   • EvaluateCustomerUseCase methods: {[method for method in dir(EvaluateCustomerUseCase) if not method.startswith('_')]}")
        print("   📝 GIẢI THÍCH: Use Case đóng gói business operation 'evaluate customer'")
        print()
        
        # ========================================
        # DEMO 5: INFRASTRUCTURE LAYER - External Dependencies
        # ========================================
        print("📦 DEMO 5: INFRASTRUCTURE LAYER - External Dependencies")
        print("=" * 50)
        print("🎯 Mục tiêu: Hiểu Infrastructure Layer và external dependencies")
        print()
        
        print("📝 GIẢI THÍCH INFRASTRUCTURE LAYER:")
        print("   • Infrastructure Layer chứa external dependencies")
        print("   • Database connections, external APIs, file systems")
        print("   • Implement các interfaces từ Domain Layer")
        print("   • Có thể thay đổi mà không ảnh hưởng business logic")
        print("   • Chứa technical concerns")
        print()
        
        # Import Infrastructure
        print("🔧 Importing Infrastructure...")
        from infrastructure.database.sql_server_connection import SqlServerConnection
        print("✅ Infrastructure imported successfully")
        print()
        
        # Demo Database Connection
        print("🗄️ Testing Database Connection:")
        db_conn = SqlServerConnection()
        print("   • Database connection object created")
        
        if db_conn.test_connection():
            print("   ✅ Database connection test successful")
            info = db_conn.get_server_info()
            print(f"   📊 Server: {info.get('server', 'Unknown')}")
            print(f"   📊 Database: {info.get('database', 'Unknown')}")
        else:
            print("   ⚠️ Database connection test failed - this is expected if database is not available")
        
        print("   📝 GIẢI THÍCH: Database connection là infrastructure concern")
        print()
        
        # ========================================
        # DEMO 6: PRESENTATION LAYER - User Interface
        # ========================================
        print("📦 DEMO 6: PRESENTATION LAYER - User Interface")
        print("=" * 50)
        print("🎯 Mục tiêu: Hiểu Presentation Layer và user interfaces")
        print()
        
        print("📝 GIẢI THÍCH PRESENTATION LAYER:")
        print("   • Presentation Layer chứa user interfaces")
        print("   • CLI, Web UI, REST API, GraphQL API")
        print("   • Sử dụng Use Cases từ Application Layer")
        print("   • Không chứa business logic")
        print("   • Chỉ chứa presentation logic")
        print()
        
        # Import Presentation
        print("🔧 Importing Presentation...")
        from presentation.cli.evaluation_cli import EvaluationCLI
        print("✅ Presentation imported successfully")
        print()
        
        # Demo CLI
        print("🖥️ Analyzing CLI Interface:")
        print(f"   • EvaluationCLI methods: {[method for method in dir(EvaluationCLI) if not method.startswith('_')]}")
        print("   📝 GIẢI THÍCH: CLI cung cấp command-line interface cho users")
        print()
        
        # ========================================
        # DEMO 7: CONFIGURATION SYSTEM
        # ========================================
        print("📦 DEMO 7: CONFIGURATION SYSTEM")
        print("=" * 50)
        print("🎯 Mục tiêu: Hiểu Configuration System và settings management")
        print()
        
        print("📝 GIẢI THÍCH CONFIGURATION SYSTEM:")
        print("   • Configuration System quản lý settings")
        print("   • Database connections, API keys, feature flags")
        print("   • Hỗ trợ environment-based configuration")
        print("   • Tách biệt configuration khỏi code")
        print("   • Dễ dàng deploy trong các môi trường khác nhau")
        print()
        
        # Import Configuration
        print("🔧 Importing Configuration...")
        from config.settings import Settings, DatabaseSettings, LoggingSettings
        print("✅ Configuration imported successfully")
        print()
        
        # Demo Configuration
        print("⚙️ Testing Configuration System:")
        
        # Default settings
        settings = Settings.default()
        print("   • Default settings created")
        print(f"   📊 Database Server: {settings.database.server}")
        print(f"   📊 Database Name: {settings.database.database}")
        print(f"   📊 Log Level: {settings.logging.level}")
        print(f"   📊 App Name: {settings.app_name}")
        print(f"   📊 App Version: {settings.app_version}")
        
        # Environment settings
        env_settings = Settings.from_env()
        print("   • Environment settings created")
        print(f"   📊 Debug Mode: {env_settings.debug}")
        
        print("   📝 GIẢI THÍCH: Configuration system giúp ứng dụng linh hoạt")
        print()
        
        # ========================================
        # DEMO 8: CLEAN ARCHITECTURE BENEFITS
        # ========================================
        print("📦 DEMO 8: CLEAN ARCHITECTURE BENEFITS")
        print("=" * 50)
        print("🎯 Mục tiêu: Hiểu lợi ích của Clean Architecture")
        print()
        
        print("✅ SEPARATION OF CONCERNS (Tách biệt mối quan tâm):")
        print("   • Domain: Business logic và entities")
        print("   • Application: Use cases và orchestration")
        print("   • Infrastructure: External dependencies")
        print("   • Presentation: User interfaces")
        print("   • Mỗi layer có trách nhiệm riêng biệt")
        print()
        
        print("✅ DEPENDENCY INVERSION (Đảo ngược phụ thuộc):")
        print("   • High-level modules không phụ thuộc vào low-level modules")
        print("   • Cả hai đều phụ thuộc vào abstractions (interfaces)")
        print("   • Dễ dàng thay đổi implementation")
        print("   • Dễ dàng test với mocks")
        print()
        
        print("✅ TESTABILITY (Khả năng test):")
        print("   • Domain logic có thể test độc lập")
        print("   • Infrastructure có thể mock cho testing")
        print("   • Clear boundaries giữa các layers")
        print("   • Dễ dàng viết unit tests")
        print()
        
        print("✅ MAINTAINABILITY (Khả năng bảo trì):")
        print("   • Thay đổi một layer không ảnh hưởng đến layer khác")
        print("   • Dễ dàng thêm tính năng mới")
        print("   • Code organization rõ ràng")
        print("   • Dễ dàng debug và fix bugs")
        print()
        
        print("✅ SCALABILITY (Khả năng mở rộng):")
        print("   • Dễ dàng thêm new features")
        print("   • Dễ dàng thay đổi technology stack")
        print("   • Phù hợp cho team development")
        print("   • Dễ dàng onboard new developers")
        print()
        
        # ========================================
        # DEMO 9: PRACTICAL EXAMPLES
        # ========================================
        print("📦 DEMO 9: PRACTICAL EXAMPLES")
        print("=" * 50)
        print("🎯 Mục tiêu: Xem Clean Architecture hoạt động trong thực tế")
        print()
        
        print("🔄 BUSINESS WORKFLOW EXAMPLE:")
        print("   1. User nhập thông tin qua CLI (Presentation Layer)")
        print("   2. CLI gọi Use Case (Application Layer)")
        print("   3. Use Case gọi Domain Service (Domain Layer)")
        print("   4. Domain Service sử dụng Repository Interface (Domain Layer)")
        print("   5. Repository Implementation truy cập Database (Infrastructure Layer)")
        print("   6. Kết quả được trả về theo thứ tự ngược lại")
        print()
        
        print("🧪 TESTING EXAMPLE:")
        print("   • Unit Test Domain Logic: Mock repositories")
        print("   • Integration Test: Use real database")
        print("   • End-to-End Test: Test toàn bộ workflow")
        print("   • Mỗi layer có thể test độc lập")
        print()
        
        print("🔧 MAINTENANCE EXAMPLE:")
        print("   • Thay đổi Database: Chỉ cần thay đổi Infrastructure Layer")
        print("   • Thay đổi UI: Chỉ cần thay đổi Presentation Layer")
        print("   • Thay đổi Business Logic: Chỉ cần thay đổi Domain Layer")
        print("   • Các layer khác không bị ảnh hưởng")
        print()
        
        # ========================================
        # DEMO 10: NEXT STEPS
        # ========================================
        print("📦 DEMO 10: NEXT STEPS")
        print("=" * 50)
        print("🎯 Mục tiêu: Biết bước tiếp theo để học Clean Architecture")
        print()
        
        print("📚 HỌC THÊM VỀ CLEAN ARCHITECTURE:")
        print("   1. Đọc 'Clean Architecture' by Robert C. Martin")
        print("   2. Thực hành với các dự án nhỏ")
        print("   3. Học về Design Patterns")
        print("   4. Thực hành Dependency Injection")
        print("   5. Học về Testing Strategies")
        print()
        
        print("🛠️ THỰC HÀNH VỚI DỰ ÁN NÀY:")
        print("   1. Chạy tests: py src/tests/test_clean_architecture.py")
        print("   2. Chạy demo: py src/tests/demo_clean_architecture.py")
        print("   3. Đọc code trong từng layer")
        print("   4. Thử thêm tính năng mới")
        print("   5. Viết tests cho tính năng mới")
        print()
        
        print("🎉 CLEAN ARCHITECTURE DEMO COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        print("📚 Bạn đã hiểu cơ bản về Clean Architecture!")
        print("🚀 Hãy tiếp tục học và thực hành để trở thành expert!")
        
        return 0
        
    except Exception as e:
        print(f"❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()
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
    exit_code = demo_clean_architecture()
    sys.exit(exit_code)
