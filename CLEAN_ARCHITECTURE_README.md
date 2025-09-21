# Clean Architecture - Display Program Management System

## 🏗️ Cấu trúc Clean Architecture

Dự án đã được cấu trúc lại theo Clean Architecture với các layer rõ ràng và dependency inversion:

```
src/
├── domain/                    # Domain Layer - Business Logic
│   ├── entities/             # Core Business Objects
│   │   ├── customer.py       # Customer Entity
│   │   ├── program.py        # Program & RegisterItem Entities
│   │   ├── evaluation.py     # Evaluation Entities
│   │   └── registration.py   # Registration Entity
│   ├── repositories/         # Repository Interfaces
│   │   ├── customer_repository.py
│   │   ├── program_repository.py
│   │   ├── evaluation_repository.py
│   │   └── registration_repository.py
│   └── services/             # Domain Services
│       └── evaluation_service.py
├── application/              # Application Layer - Use Cases
│   ├── use_cases/           # Application Use Cases
│   │   └── evaluate_customer_use_case.py
│   └── dtos/                # Data Transfer Objects
├── infrastructure/          # Infrastructure Layer - External Dependencies
│   ├── database/            # Database Infrastructure
│   │   └── sql_server_connection.py
│   └── repositories/        # Repository Implementations
├── presentation/            # Presentation Layer - User Interface
│   ├── cli/                 # Command Line Interface
│   │   └── evaluation_cli.py
│   └── api/                 # REST API (Future)
├── config/                  # Configuration
│   └── settings.py
└── main.py                  # Dependency Injection Container
```

## 🎯 Nguyên tắc Clean Architecture

### 1. **Dependency Rule**
- Dependencies chỉ được trỏ vào trong (inner layers)
- Domain layer không phụ thuộc vào bất kỳ layer nào khác
- Application layer chỉ phụ thuộc vào Domain layer
- Infrastructure layer implement interfaces từ Domain layer

### 2. **Separation of Concerns**
- **Domain**: Chứa business logic và entities
- **Application**: Chứa use cases và orchestration
- **Infrastructure**: Chứa external dependencies (database, APIs)
- **Presentation**: Chứa user interfaces (CLI, Web, API)

### 3. **Dependency Inversion**
- High-level modules không phụ thuộc vào low-level modules
- Cả hai đều phụ thuộc vào abstractions (interfaces)
- Abstractions không phụ thuộc vào details

## 🔧 Cách sử dụng

### 1. **Khởi tạo ứng dụng**
```python
from src.main import main

# Chạy ứng dụng
main()
```

### 2. **Sử dụng CLI**
```python
from src.main import DependencyContainer

# Khởi tạo container
container = DependencyContainer()

# Lấy CLI và chạy
cli = container.get_evaluation_cli()
cli.run_interactive()
```

### 3. **Sử dụng Use Case trực tiếp**
```python
from src.main import DependencyContainer

container = DependencyContainer()
use_case = container.get_evaluation_use_case()

# Thực hiện đánh giá
result = use_case.execute(202509, "CUST001", "PROG001")
```

## 📋 Các thành phần chính

### **Domain Layer**
- **Entities**: Core business objects với business rules
- **Repositories**: Abstract interfaces cho data access
- **Services**: Domain business logic

### **Application Layer**
- **Use Cases**: Application-specific business logic
- **DTOs**: Data transfer objects

### **Infrastructure Layer**
- **Database**: SQL Server connection management
- **Repositories**: Concrete implementations của domain interfaces

### **Presentation Layer**
- **CLI**: Command line interface
- **API**: REST API (planned)

## 🚀 Lợi ích của Clean Architecture

### 1. **Testability**
- Dễ dàng unit test với mock objects
- Business logic tách biệt khỏi external dependencies

### 2. **Maintainability**
- Code dễ đọc và hiểu
- Thay đổi một layer không ảnh hưởng đến layer khác

### 3. **Flexibility**
- Dễ dàng thay đổi database hoặc UI
- Có thể thêm new features mà không ảnh hưởng existing code

### 4. **Scalability**
- Dễ dàng mở rộng và thêm tính năng mới
- Code structure rõ ràng cho team development

## 🔄 Dependency Flow

```
Presentation Layer
        ↓
Application Layer
        ↓
Domain Layer
        ↑
Infrastructure Layer
```

## 📝 TODO - Cần implement

### 1. **Repository Implementations**
- [ ] `SqlServerEvaluationRepository`
- [ ] `SqlServerRegistrationRepository`
- [ ] `SqlServerProgramRepository`
- [ ] `SqlServerCustomerRepository`

### 2. **Additional Use Cases**
- [ ] `GetEvaluationResultUseCase`
- [ ] `GetEligibleCustomersUseCase`
- [ ] `BatchEvaluationUseCase`

### 3. **API Layer**
- [ ] FastAPI implementation
- [ ] REST endpoints
- [ ] API documentation

### 4. **Testing**
- [ ] Unit tests cho domain layer
- [ ] Integration tests
- [ ] End-to-end tests

### 5. **Configuration**
- [ ] Environment-based configuration
- [ ] Logging configuration
- [ ] Database migration scripts

## 🎯 Next Steps

1. **Implement Repository Layer**: Tạo concrete implementations cho các repository interfaces
2. **Add Tests**: Viết unit tests và integration tests
3. **Create API**: Thêm REST API layer
4. **Add Validation**: Thêm input validation và error handling
5. **Documentation**: Tạo API documentation và user guides

## 📚 Tài liệu tham khảo

- [Clean Architecture by Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Python Clean Architecture Example](https://github.com/cosmic-python/code)
- [Dependency Injection in Python](https://python-dependency-injector.ets-labs.org/)
