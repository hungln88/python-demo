"""
Main Entry Point - Dependency Injection Container
Điểm vào chính - Container Dependency Injection

📚 HƯỚNG DẪN CHO NGƯỜI MỚI:
===============================================

Dependency Injection Container là gì?
------------------------------------
Dependency Injection Container là một pattern giúp quản lý dependencies trong ứng dụng.
Thay vì tạo objects trực tiếp, container sẽ:
1. Tạo và quản lý lifecycle của objects
2. Inject dependencies vào các objects cần thiết
3. Đảm bảo mỗi dependency chỉ được tạo một lần (Singleton pattern)
4. Giúp code dễ test và maintain

Tại sao cần Dependency Injection?
---------------------------------
1. LOOSE COUPLING: Objects không phụ thuộc vào concrete classes
2. EASY TESTING: Dễ dàng mock dependencies cho testing
3. SINGLE RESPONSIBILITY: Mỗi class chỉ lo tạo một loại object
4. CONFIGURATION: Dễ dàng thay đổi implementation

Cách hoạt động:
--------------
1. Container tạo instances của các dependencies
2. Khi cần object, container inject dependencies vào
3. Objects sử dụng dependencies thông qua interfaces
4. Dễ dàng thay đổi implementation mà không ảnh hưởng code

Ví dụ:
------
# Thay vì:
service = EvaluationService(repo1, repo2, repo3)

# Container sẽ:
service = container.get_evaluation_service()  # Tự động inject dependencies
"""

import logging
from typing import Optional

# Domain Layer - Business Logic
from domain.services.evaluation_service import EvaluationService
from domain.repositories.evaluation_repository import EvaluationRepository
from domain.repositories.registration_repository import RegistrationRepository
from domain.repositories.program_repository import ProgramRepository

# Application Layer - Use Cases
from application.use_cases.evaluate_customer_use_case import EvaluateCustomerUseCase

# Infrastructure Layer - External Dependencies
from infrastructure.database.sql_server_connection import SqlServerConnection

# Presentation Layer - User Interface
from presentation.cli.evaluation_cli import EvaluationCLI


class DependencyContainer:
    """
    Dependency Container - Quản lý dependency injection
    
    📝 GIẢI THÍCH CHO NGƯỜI MỚI:
    ============================
    
    Container này chịu trách nhiệm:
    1. Tạo và quản lý lifecycle của tất cả dependencies
    2. Inject dependencies vào các objects cần thiết
    3. Đảm bảo mỗi dependency chỉ được tạo một lần (Singleton)
    4. Cung cấp interface đơn giản để lấy dependencies
    
    Cách hoạt động:
    - Lazy initialization: Chỉ tạo object khi cần
    - Singleton pattern: Mỗi dependency chỉ có một instance
    - Dependency injection: Tự động inject dependencies
    - Clean separation: Mỗi method chỉ lo tạo một loại object
    
    Ví dụ sử dụng:
    -------------
    container = DependencyContainer()
    cli = container.get_evaluation_cli()  # Tự động inject tất cả dependencies
    """
    
    def __init__(self):
        """
        Khởi tạo container
        
        📝 GIẢI THÍCH:
        - Tất cả dependencies được khởi tạo là None
        - Sẽ được tạo khi cần (lazy initialization)
        - Mỗi dependency chỉ được tạo một lần
        """
        # Infrastructure Dependencies
        self._db_connection: Optional[SqlServerConnection] = None
        
        # Repository Dependencies (Domain Layer)
        self._evaluation_repo: Optional[EvaluationRepository] = None
        self._registration_repo: Optional[RegistrationRepository] = None
        self._program_repo: Optional[ProgramRepository] = None
        
        # Service Dependencies (Domain Layer)
        self._evaluation_service: Optional[EvaluationService] = None
        
        # Use Case Dependencies (Application Layer)
        self._evaluation_use_case: Optional[EvaluateCustomerUseCase] = None
        
        # Presentation Dependencies (Presentation Layer)
        self._evaluation_cli: Optional[EvaluationCLI] = None
    
    def get_database_connection(self) -> SqlServerConnection:
        """
        Lấy database connection
        
        📝 GIẢI THÍCH:
        - Database connection là infrastructure dependency
        - Được tạo một lần và tái sử dụng (Singleton pattern)
        - Lazy initialization: Chỉ tạo khi cần
        
        Returns:
            SqlServerConnection: Database connection instance
        """
        if self._db_connection is None:
            print("🔧 Creating database connection...")
            self._db_connection = SqlServerConnection()
        return self._db_connection
    
    def get_evaluation_repository(self) -> EvaluationRepository:
        """
        Lấy evaluation repository
        
        📝 GIẢI THÍCH:
        - Repository là interface từ Domain Layer
        - Cần concrete implementation từ Infrastructure Layer
        - Hiện tại chưa implement, sẽ raise NotImplementedError
        
        Returns:
            EvaluationRepository: Evaluation repository instance
        """
        if self._evaluation_repo is None:
            # TODO: Implement concrete evaluation repository
            # 📝 GIẢI THÍCH: Cần tạo SqlServerEvaluationRepository trong infrastructure layer
            raise NotImplementedError("EvaluationRepository implementation needed - Create SqlServerEvaluationRepository in infrastructure layer")
        return self._evaluation_repo
    
    def get_registration_repository(self) -> RegistrationRepository:
        """
        Lấy registration repository
        
        📝 GIẢI THÍCH:
        - Repository là interface từ Domain Layer
        - Cần concrete implementation từ Infrastructure Layer
        - Hiện tại chưa implement, sẽ raise NotImplementedError
        
        Returns:
            RegistrationRepository: Registration repository instance
        """
        if self._registration_repo is None:
            # TODO: Implement concrete registration repository
            # 📝 GIẢI THÍCH: Cần tạo SqlServerRegistrationRepository trong infrastructure layer
            raise NotImplementedError("RegistrationRepository implementation needed - Create SqlServerRegistrationRepository in infrastructure layer")
        return self._registration_repo
    
    def get_program_repository(self) -> ProgramRepository:
        """
        Lấy program repository
        
        📝 GIẢI THÍCH:
        - Repository là interface từ Domain Layer
        - Cần concrete implementation từ Infrastructure Layer
        - Hiện tại chưa implement, sẽ raise NotImplementedError
        
        Returns:
            ProgramRepository: Program repository instance
        """
        if self._program_repo is None:
            # TODO: Implement concrete program repository
            # 📝 GIẢI THÍCH: Cần tạo SqlServerProgramRepository trong infrastructure layer
            raise NotImplementedError("ProgramRepository implementation needed - Create SqlServerProgramRepository in infrastructure layer")
        return self._program_repo
    
    def get_evaluation_service(self) -> EvaluationService:
        """
        Lấy evaluation service
        
        📝 GIẢI THÍCH:
        - Service là Domain Layer component
        - Cần inject các repository dependencies
        - Tự động tạo repositories nếu chưa có
        
        Returns:
            EvaluationService: Evaluation service instance
        """
        if self._evaluation_service is None:
            print("🔧 Creating evaluation service...")
            self._evaluation_service = EvaluationService(
                evaluation_repo=self.get_evaluation_repository(),
                registration_repo=self.get_registration_repository(),
                program_repo=self.get_program_repository()
            )
        return self._evaluation_service
    
    def get_evaluation_use_case(self) -> EvaluateCustomerUseCase:
        """
        Lấy evaluation use case
        
        📝 GIẢI THÍCH:
        - Use Case là Application Layer component
        - Cần inject evaluation service dependency
        - Tự động tạo service nếu chưa có
        
        Returns:
            EvaluateCustomerUseCase: Evaluation use case instance
        """
        if self._evaluation_use_case is None:
            print("🔧 Creating evaluation use case...")
            self._evaluation_use_case = EvaluateCustomerUseCase(
                evaluation_service=self.get_evaluation_service()
            )
        return self._evaluation_use_case
    
    def get_evaluation_cli(self) -> EvaluationCLI:
        """
        Lấy evaluation CLI
        
        📝 GIẢI THÍCH:
        - CLI là Presentation Layer component
        - Cần inject evaluation use case dependency
        - Tự động tạo use case nếu chưa có
        
        Returns:
            EvaluationCLI: Evaluation CLI instance
        """
        if self._evaluation_cli is None:
            print("🔧 Creating evaluation CLI...")
            self._evaluation_cli = EvaluationCLI(
                evaluation_use_case=self.get_evaluation_use_case()
            )
        return self._evaluation_cli


def main():
    """
    Main entry point - Điểm vào chính của ứng dụng
    
    📚 HƯỚNG DẪN CHO NGƯỜI MỚI:
    ============================
    
    Function main() là entry point của ứng dụng:
    1. Thiết lập logging system
    2. Khởi tạo dependency container
    3. Test database connection
    4. Chạy CLI interface
    
    Cách hoạt động:
    - Logging: Ghi log để debug và monitor
    - Container: Quản lý tất cả dependencies
    - Database: Kiểm tra kết nối trước khi chạy
    - CLI: Cung cấp interface cho user
    
    Lỗi thường gặp:
    - Database connection failed: Kiểm tra database server
    - Import errors: Kiểm tra Python path
    - NotImplementedError: Cần implement repository classes
    """
    # Thiết lập logging system
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger(__name__)
    logger.info("🚀 Starting Display Program Management System")
    logger.info("📚 Clean Architecture Implementation")
    
    try:
        print("🔧 Initializing Dependency Container...")
        # Khởi tạo dependency container
        container = DependencyContainer()
        print("✅ Dependency Container initialized")
        
        print("🗄️ Testing Database Connection...")
        # Test database connection
        db_conn = container.get_database_connection()
        if db_conn.test_connection():
            logger.info("✅ Database connection successful")
            print("✅ Database connection successful")
        else:
            logger.error("❌ Database connection failed")
            print("❌ Database connection failed")
            print("💡 Please check database server and connection settings")
            return
        
        print("🖥️ Starting CLI Interface...")
        # Lấy CLI và chạy
        cli = container.get_evaluation_cli()
        cli.run_interactive()
        
    except NotImplementedError as e:
        logger.error(f"❌ Implementation missing: {e}")
        print(f"❌ Implementation missing: {e}")
        print("💡 Please implement the missing repository classes in infrastructure layer")
        print("📚 See README.md for detailed instructions")
    except Exception as e:
        logger.error(f"💥 Application error: {e}")
        print(f"💥 Application error: {e}")
        print("💡 Please check the error message and fix the issue")
        raise


if __name__ == "__main__":
    """
    Entry point khi chạy file trực tiếp
    
    📝 GIẢI THÍCH:
    - Khi chạy: py src/main.py
    - __name__ sẽ là "__main__"
    - Function main() sẽ được gọi
    - sys.exit() để trả về exit code
    """
    main()
