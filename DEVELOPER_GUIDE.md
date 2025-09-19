# Developer Guide - Hướng dẫn Phát triển
## Display Program Management System

### 📚 Mục lục
1. [Giới thiệu](#giới-thiệu)
2. [Cấu trúc Project](#cấu-trúc-project)
3. [Kiến thức cần thiết](#kiến-thức-cần-thiết)
4. [Hướng dẫn Setup](#hướng-dẫn-setup)
5. [Hiểu Business Logic](#hiểu-business-logic)
6. [Code Architecture](#code-architecture)
7. [Testing Guide](#testing-guide)
8. [Common Tasks](#common-tasks)
9. [Troubleshooting](#troubleshooting)

---

## 🎯 Giới thiệu

Hệ thống Display Program Management là một ứng dụng quản lý chương trình trưng bày sản phẩm tại các điểm bán. Hệ thống giúp:

- **Vận hành**: Cấu hình các chương trình trưng bày
- **Khách hàng**: Đăng ký tham gia chương trình
- **Giám sát**: Kiểm tra chất lượng trưng bày
- **Hệ thống**: Tự động đánh giá và xác định quyền nhận thưởng

### 🎭 Các Vai trò trong Hệ thống
- **Operations Team**: Cấu hình chương trình và tiêu chí
- **Customers/Retailers**: Đăng ký và tham gia chương trình
- **Supervisors**: Thực hiện audit tại điểm bán
- **System**: Tự động xử lý đánh giá và báo cáo

---

## 📁 Cấu trúc Project

```
display-program-management/
├── 📄 models.py              # Data models và business objects
├── 🗄️ database.py           # Database connection và repository
├── 🧠 business_logic.py     # Core business logic
├── 🖥️ main.py              # CLI application
├── ⚙️ config.py            # Configuration management
├── 📋 requirements.txt      # Python dependencies
├── 🗃️ schema.sql           # Database schema
├── 📊 sample_data.sql       # Sample data for testing
├── 🧪 test_*.py            # Test files
├── 🏃 run_tests.py         # Test runner
├── 🛠️ setup.py            # Setup script
├── 📖 README.md            # Main documentation
└── 📚 DEVELOPER_GUIDE.md   # This file
```

### 📂 File Functions

| File | Chức năng | Khi nào sửa |
|------|-----------|-------------|
| `models.py` | Định nghĩa data structures | Thêm field mới, thay đổi business rules |
| `database.py` | Database operations | Thêm query mới, thay đổi schema |
| `business_logic.py` | Business rules và calculations | Thay đổi logic đánh giá, thêm features |
| `main.py` | User interface | Thêm menu options, cải thiện UX |
| `config.py` | System configuration | Thêm settings, environment configs |

---

## 🧠 Kiến thức cần thiết

### 👶 Cho người mới bắt đầu Python
Bạn cần hiểu:
- **Basic Python**: Variables, functions, classes
- **Data Types**: Lists, dictionaries, tuples
- **Object-Oriented Programming**: Classes, inheritance
- **Exception Handling**: try/except blocks
- **Modules và Imports**: import statements

### 📚 Concepts quan trọng

#### 1. **Dataclasses** (Python 3.7+)
```python
from dataclasses import dataclass

@dataclass
class RegisterItem:
    yyyymm: int
    program_code: str
    # Tự động tạo __init__, __repr__, __eq__
```

#### 2. **Context Managers**
```python
with self.db.get_connection() as conn:
    # Connection tự động đóng khi ra khỏi block
    cursor = conn.cursor()
    # ... thực hiện operations
```

#### 3. **Type Hints**
```python
def get_items(self, month: int) -> List[RegisterItem]:
    # Giúp IDE hiểu kiểu dữ liệu và catch lỗi
    return []
```

#### 4. **Repository Pattern**
```python
# Tách biệt business logic khỏi data access
class DisplayProgramRepository:
    def get_items(self) -> List[RegisterItem]:
        # Database operations
        pass

class DisplayProgramService:
    def __init__(self, repository: DisplayProgramRepository):
        self.repo = repository
    
    def evaluate_customer(self):
        # Business logic sử dụng repository
        items = self.repo.get_items()
```

---

## 🚀 Hướng dẫn Setup

### 1. **Environment Setup**
```bash
# Tạo virtual environment (khuyến nghị)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. **Database Setup**
```bash
# Option 1: Sử dụng setup script
python setup.py

# Option 2: Manual setup
sqlcmd -S localhost -d master -i schema.sql
sqlcmd -S localhost -d DisplayProgramDB -i sample_data.sql
```

### 3. **Verify Setup**
```bash
# Test database connection
python -c "from database import DatabaseConnection; print('OK' if DatabaseConnection().test_connection() else 'FAIL')"

# Run tests
python run_tests.py

# Start application
python main.py
```

---

## 💼 Hiểu Business Logic

### 🔄 Business Flow

```
1. [Operations] Cấu hình chương trình
   ↓
2. [Operations] Thiết lập tiêu chí đánh giá  
   ↓
3. [Customers] Đăng ký tham gia chương trình
   ↓
4. [Supervisors] Audit tại điểm bán
   ↓
5. [System] Đánh giá và xác định quyền thưởng
```

### 📊 Data Flow

```
register_item (Program Config)
    ↓
register (Customer Registration) 
    ↓
condition_group + condition_item (Evaluation Criteria)
    ↓
audit_picture (Audit Results)
    ↓
CustomerEvaluationResult (Final Assessment)
```

### 🎯 Key Business Rules

1. **Evaluation Logic**:
   - Khách hàng phải đạt TẤT CẢ tiêu chí tối thiểu
   - Chỉ tính điểm cho tiêu chí đạt yêu cầu
   - Phải có đăng ký hoạt động để nhận thưởng

2. **Data Validation**:
   - YYYYMM format: 202301-209912
   - Percentage values: 0-100
   - Quantity values: > 0

3. **Audit Requirements**:
   - Mỗi condition_code phải có audit result
   - Audit date được tự động ghi nhận
   - Giá trị audit phải là số hợp lệ

---

## 🏗️ Code Architecture

### 🎨 Design Patterns Được Sử dụng

#### 1. **Repository Pattern**
```python
# Tách biệt data access khỏi business logic
class DisplayProgramRepository:
    def get_register_items(self) -> List[RegisterItem]:
        # Database operations
        pass

class DisplayProgramService:
    def __init__(self, repository):
        self.repo = repository
    
    def evaluate_customer(self):
        # Business logic
        items = self.repo.get_register_items()
```

#### 2. **Data Transfer Objects (DTO)**
```python
@dataclass
class CustomerEvaluationResult:
    # Immutable data structure để transfer kết quả
    total_points: int
    max_possible_points: int
    meets_criteria: bool
```

#### 3. **Context Manager Pattern**
```python
@contextmanager
def get_connection(self):
    conn = None
    try:
        conn = pyodbc.connect(self.connection_string)
        yield conn
    finally:
        if conn:
            conn.close()
```

### 🔧 Code Organization

#### **Layer Architecture**
```
┌─────────────────────┐
│   Presentation      │ ← main.py (CLI Interface)
├─────────────────────┤
│   Business Logic    │ ← business_logic.py (Services)
├─────────────────────┤  
│   Data Access       │ ← database.py (Repository)
├─────────────────────┤
│   Domain Models     │ ← models.py (Entities)
├─────────────────────┤
│   Database          │ ← SQL Server
└─────────────────────┘
```

#### **Dependency Flow**
- **main.py** → **business_logic.py** → **database.py** → **models.py**
- Mỗi layer chỉ phụ thuộc vào layer dưới
- Models không phụ thuộc vào bất kỳ layer nào khác

---

## 🧪 Testing Guide

### 🎯 Testing Strategy

#### **1. Unit Tests**
```python
# Test individual functions/methods
def test_register_item_validation(self):
    item = RegisterItem(202509, "PROG001", "TYPE_BEVERAGE", "KE_3_O", 4, 3)
    self.assertTrue(item.is_valid())
```

#### **2. Integration Tests**
```python
# Test interaction between components
def test_repository_with_database(self):
    repo = DisplayProgramRepository(real_db_connection)
    items = repo.get_register_items(202509)
    self.assertIsInstance(items[0], RegisterItem)
```

#### **3. Mock Tests**
```python
# Test without real database
@patch('database.pyodbc.connect')
def test_get_register_items_success(self, mock_connect):
    mock_conn = Mock()
    # ... setup mocks
    result = self.repo.get_register_items(202509)
```

### 🏃 Running Tests

```bash
# Chạy tất cả tests
python run_tests.py

# Chạy tests cho module cụ thể
python run_tests.py test_models
python run_tests.py test_database

# Kiểm tra test coverage
python run_tests.py --coverage

# Chạy một test class cụ thể
python -m unittest test_models.TestRegisterItem

# Chạy một test method cụ thể
python -m unittest test_models.TestRegisterItem.test_register_item_creation
```

### 📊 Test Coverage Goals

- **Models**: 100% (simple data structures)
- **Database**: 90% (mock most operations)
- **Business Logic**: 95% (core functionality)
- **Main**: 80% (UI interactions)

---

## 🛠️ Common Tasks

### ➕ Thêm Field Mới vào Model

1. **Cập nhật Model**:
```python
@dataclass
class RegisterItem:
    # Existing fields...
    new_field: str  # Thêm field mới
    
    def is_valid(self) -> bool:
        return (
            # Existing validations...
            len(self.new_field.strip()) > 0  # Validate field mới
        )
```

2. **Cập nhật Database Schema**:
```sql
ALTER TABLE register_item 
ADD new_field VARCHAR(50) NOT NULL DEFAULT '';
```

3. **Cập nhật Repository**:
```python
def get_register_items(self, yyyymm: int) -> List[RegisterItem]:
    query = """
        SELECT yyyymm, program_code, type_code, item, facing, unit, new_field
        FROM register_item 
        WHERE yyyymm = ?
    """
    # Update mapping
    return [RegisterItem(
        yyyymm=row[0],
        # ... existing fields
        new_field=row[6]  # Thêm field mới
    ) for row in rows]
```

4. **Cập nhật Tests**:
```python
def test_register_item_with_new_field(self):
    item = RegisterItem(202509, "PROG001", "TYPE_BEVERAGE", "KE_3_O", 4, 3, "new_value")
    self.assertTrue(item.is_valid())
```

### 📝 Thêm Business Rule Mới

1. **Thêm vào Business Logic**:
```python
class DisplayProgramService:
    def new_business_rule(self, customer_code: str) -> bool:
        # Implement new rule
        pass
    
    def evaluate_customer(self, ...):
        # Existing logic...
        if not self.new_business_rule(customer_code):
            failed_conditions.append("NEW_RULE_FAILED")
```

2. **Thêm Tests**:
```python
def test_new_business_rule(self):
    service = DisplayProgramService(mock_repo)
    result = service.new_business_rule("CUST001")
    self.assertTrue(result)
```

### 🔍 Thêm Query Mới

1. **Thêm vào Repository**:
```python
def get_customers_by_criteria(self, criteria: str) -> List[str]:
    """New query method"""
    query = """
        SELECT DISTINCT customer_code
        FROM register r
        WHERE r.status = 1 AND r.program_code LIKE ?
    """
    
    with self.db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (f"%{criteria}%",))
        rows = cursor.fetchall()
        return [row[0] for row in rows]
```

2. **Thêm Tests**:
```python
def test_get_customers_by_criteria(self):
    # Mock setup
    result = self.repo.get_customers_by_criteria("PROG")
    self.assertIsInstance(result, list)
```

---

## 🐛 Troubleshooting

### ❌ Common Errors

#### **1. Database Connection Issues**
```
Error: pyodbc.Error: ('08001', '[08001] [Microsoft][ODBC Driver 17 for SQL Server]...')
```
**Solutions**:
- Kiểm tra SQL Server đang chạy
- Verify connection string trong `config.py`
- Kiểm tra firewall settings
- Thử connection string khác:
```python
# LocalDB
db = DatabaseConnection("(localdb)\\MSSQLLocalDB", "DisplayProgramDB")

# SQL Server Express
db = DatabaseConnection("localhost\\SQLEXPRESS", "DisplayProgramDB")
```

#### **2. Import Errors**
```
ModuleNotFoundError: No module named 'models'
```
**Solutions**:
- Đảm bảo đang chạy từ project root directory
- Kiểm tra virtual environment đã activate
- Verify tất cả files trong cùng directory

#### **3. Data Validation Errors**
```
AssertionError: RegisterItem should be valid
```
**Solutions**:
- Kiểm tra `is_valid()` method trong model
- Verify data format (YYYYMM, positive numbers)
- Check required fields không empty

#### **4. Test Failures**
```
FAILED test_models.py::TestRegisterItem::test_register_item_creation
```
**Solutions**:
- Chạy test individual: `python -m unittest test_models.TestRegisterItem.test_register_item_creation`
- Kiểm tra test data setup
- Verify mock configurations

### 🔧 Debugging Tips

#### **1. Enable Debug Logging**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

#### **2. Print SQL Queries**
```python
# Trong repository methods
self.logger.debug(f"Executing query: {query}")
self.logger.debug(f"With parameters: {params}")
```

#### **3. Validate Data at Runtime**
```python
def insert_register_item(self, item: RegisterItem) -> bool:
    # Add debug prints
    print(f"Inserting item: {item}")
    print(f"Is valid: {item.is_valid()}")
    
    if not item.is_valid():
        print(f"Validation failed for: {item}")
        return False
```

#### **4. Test Database Connection**
```python
# Quick connection test
from database import DatabaseConnection
db = DatabaseConnection()
print("Connection test:", db.test_connection())
print("Server info:", db.get_server_info())
```

### 📚 Learning Resources

#### **Python Resources**
- [Python Official Tutorial](https://docs.python.org/3/tutorial/)
- [Real Python](https://realpython.com/) - Practical Python tutorials
- [Python Type Hints](https://docs.python.org/3/library/typing.html)

#### **SQL Server Resources**
- [SQL Server Documentation](https://docs.microsoft.com/en-us/sql/sql-server/)
- [pyodbc Documentation](https://pyodbc.readthedocs.io/)

#### **Testing Resources**
- [Python unittest](https://docs.python.org/3/library/unittest.html)
- [unittest.mock](https://docs.python.org/3/library/unittest.mock.html)

---

## 🎯 Best Practices

### ✅ Code Quality

1. **Always use type hints**
```python
def get_items(self, month: int) -> List[RegisterItem]:
    pass
```

2. **Write docstrings for all public methods**
```python
def evaluate_customer(self, yyyymm: int, customer_code: str) -> CustomerEvaluationResult:
    """
    Đánh giá khách hàng theo tiêu chí chương trình
    
    Args:
        yyyymm: Tháng/năm đánh giá
        customer_code: Mã khách hàng
        
    Returns:
        CustomerEvaluationResult: Kết quả đánh giá chi tiết
    """
```

3. **Use meaningful variable names**
```python
# Good
customer_evaluation_result = self.evaluate_customer(...)

# Bad  
result = self.eval(...)
```

4. **Handle exceptions appropriately**
```python
try:
    # Database operation
    pass
except pyodbc.IntegrityError as e:
    # Specific error handling
    self.logger.error(f"Data integrity error: {e}")
    return False
except Exception as e:
    # General error handling
    self.logger.error(f"Unexpected error: {e}")
    raise
```

### 🧪 Testing Best Practices

1. **Test one thing at a time**
2. **Use descriptive test names**
3. **Follow AAA pattern**: Arrange, Act, Assert
4. **Mock external dependencies**
5. **Test both happy path and error cases**

### 🗃️ Database Best Practices

1. **Always use parameterized queries**
2. **Use transactions for multi-step operations**
3. **Handle connection cleanup properly**
4. **Log database operations for debugging**
5. **Validate data before database operations**

---

## 🚀 Next Steps

Sau khi đã hiểu hệ thống, bạn có thể:

1. **Thêm Features Mới**:
   - Email notifications cho audit results
   - Web dashboard thay vì CLI
   - Export reports to Excel/PDF
   - Advanced analytics và charts

2. **Performance Optimization**:
   - Database indexing
   - Connection pooling
   - Caching frequently accessed data
   - Batch operations

3. **Architecture Improvements**:
   - Add API layer (REST/GraphQL)
   - Implement microservices
   - Add authentication/authorization
   - Containerization với Docker

4. **Integration**:
   - Connect với external systems
   - Real-time data sync
   - Message queues
   - Event-driven architecture

---

## 📞 Support

Nếu gặp vấn đề:

1. **Kiểm tra logs** trong console output
2. **Chạy tests** để verify system integrity
3. **Tham khảo documentation** trong code comments
4. **Debug step-by-step** với print statements
5. **Kiểm tra database** trực tiếp với SQL queries

**Happy Coding! 🎉**
