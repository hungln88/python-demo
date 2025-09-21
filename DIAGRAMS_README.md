# Clean Architecture Diagrams - Display Program Management System

## 📊 Tổng quan các Diagrams

Bộ diagrams này mô tả chi tiết cấu trúc và flow của Clean Architecture trong dự án Display Program Management System.

## 🎯 Danh sách Diagrams

### 1. **CLEAN_ARCHITECTURE_FLOW_DIAGRAM.puml** - Diagram tổng quan
- **Mục đích**: Mô tả cấu trúc tổng thể của Clean Architecture
- **Nội dung**: 
  - 4 layers chính (Presentation, Application, Domain, Infrastructure)
  - Dependency flow và nguyên tắc
  - Business flow example
  - Testing strategy
- **Phù hợp cho**: Người mới học Clean Architecture

### 2. **SIMPLE_CLEAN_ARCHITECTURE_FLOW.puml** - Diagram đơn giản (có emoji)
- **Mục đích**: Mô tả cấu trúc đơn giản, dễ hiểu
- **Nội dung**:
  - 4 layers cơ bản
  - Dependency flow
  - Business flow example
  - Clean Architecture principles
- **Phù hợp cho**: Người mới bắt đầu
- **Lưu ý**: Có thể gây lỗi trên một số platform do emoji

### 3. **SIMPLE_CLEAN_ARCHITECTURE_FLOW_NO_EMOJI.puml** - Diagram không emoji
- **Mục đích**: Version tương thích với planttext.com
- **Nội dung**: Giống version có emoji nhưng không có emoji
- **Phù hợp cho**: Sử dụng trên planttext.com và các platform khác

### 4. **SIMPLE_CLEAN_ARCHITECTURE_FLOW_ENGLISH.puml** - Diagram tiếng Anh
- **Mục đích**: Version hoàn toàn bằng tiếng Anh
- **Nội dung**: Giống version tiếng Việt nhưng bằng tiếng Anh
- **Phù hợp cho**: Sử dụng quốc tế

### 5. **SIMPLE_CLEAN_ARCHITECTURE_FLOW_MINIMAL.puml** - Diagram tối giản
- **Mục đích**: Version đơn giản nhất, tương thích tối đa
- **Nội dung**: Chỉ có cấu trúc cơ bản, không có notes dài
- **Phù hợp cho**: Platform có giới hạn hoặc cần load nhanh

### 3. **CLEAN_ARCHITECTURE_SEQUENCE_DIAGRAM.puml** - Sequence Diagram
- **Mục đích**: Mô tả flow xử lý cụ thể khi đánh giá khách hàng
- **Nội dung**:
  - Step-by-step flow từ User đến Database
  - Method calls giữa các components
  - Error handling flow
  - Testing flow
- **Phù hợp cho**: Hiểu chi tiết cách code hoạt động

### 4. **CLEAN_ARCHITECTURE_COMPONENT_DIAGRAM.puml** - Component Diagram
- **Mục đích**: Mô tả cấu trúc chi tiết của từng component
- **Nội dung**:
  - Chi tiết methods và properties của mỗi class
  - Dependencies giữa các components
  - Testing strategy
  - Configuration management
- **Phù hợp cho**: Developers cần hiểu chi tiết implementation

## 🚀 Cách sử dụng Diagrams

### 1. **Xem Diagrams online**

#### **Cho planttext.com (khuyến nghị):**
```bash
# Sử dụng version không emoji:
SIMPLE_CLEAN_ARCHITECTURE_FLOW_NO_EMOJI.puml
# hoặc
SIMPLE_CLEAN_ARCHITECTURE_FLOW_ENGLISH.puml
# hoặc
SIMPLE_CLEAN_ARCHITECTURE_FLOW_MINIMAL.puml

# Copy nội dung và paste vào:
# https://www.planttext.com/
```

#### **Cho plantuml.com:**
```bash
# Sử dụng version có emoji:
SIMPLE_CLEAN_ARCHITECTURE_FLOW.puml

# Copy nội dung và paste vào:
# https://www.plantuml.com/plantuml/uml/
```

### 2. **Generate images từ PlantUML**
```bash
# Cài đặt PlantUML
# https://plantuml.com/download

# Generate PNG
java -jar plantuml.jar CLEAN_ARCHITECTURE_FLOW_DIAGRAM.puml

# Generate SVG
java -jar plantuml.jar -tsvg CLEAN_ARCHITECTURE_FLOW_DIAGRAM.puml
```

### 3. **Sử dụng trong IDE**
- **VS Code**: Cài extension "PlantUML"
- **IntelliJ**: Cài plugin "PlantUML integration"
- **Eclipse**: Cài plugin "PlantUML"

## 📚 Hướng dẫn đọc Diagrams

### **Cho người mới học Clean Architecture:**

1. **Bắt đầu với SIMPLE_CLEAN_ARCHITECTURE_FLOW.puml**
   - Hiểu 4 layers cơ bản
   - Xem dependency flow
   - Đọc Clean Architecture principles

2. **Tiếp tục với CLEAN_ARCHITECTURE_FLOW_DIAGRAM.puml**
   - Hiểu chi tiết hơn về từng layer
   - Xem business flow example
   - Hiểu testing strategy

3. **Xem CLEAN_ARCHITECTURE_SEQUENCE_DIAGRAM.puml**
   - Hiểu flow xử lý cụ thể
   - Xem method calls
   - Hiểu error handling

4. **Cuối cùng xem CLEAN_ARCHITECTURE_COMPONENT_DIAGRAM.puml**
   - Hiểu chi tiết implementation
   - Xem methods và properties
   - Hiểu testing strategy

### **Cho Developers có kinh nghiệm:**

1. **Xem CLEAN_ARCHITECTURE_COMPONENT_DIAGRAM.puml trước**
   - Hiểu cấu trúc chi tiết
   - Xem dependencies
   - Hiểu testing strategy

2. **Xem CLEAN_ARCHITECTURE_SEQUENCE_DIAGRAM.puml**
   - Hiểu flow xử lý
   - Xem method calls
   - Hiểu error handling

3. **Xem CLEAN_ARCHITECTURE_FLOW_DIAGRAM.puml**
   - Hiểu tổng quan architecture
   - Xem business flow
   - Hiểu principles

## 🎯 Key Concepts trong Diagrams

### **1. Dependency Rule**
- Dependencies chỉ được trỏ vào trong (inner layers)
- Domain layer không phụ thuộc vào bất kỳ layer nào
- Sử dụng interfaces để tách biệt implementation

### **2. Layer Responsibilities**
- **Presentation**: User interface (CLI, Web, API)
- **Application**: Use cases và orchestration
- **Domain**: Business logic và entities
- **Infrastructure**: External dependencies (Database, APIs)

### **3. Business Flow**
1. User tương tác qua Presentation Layer
2. Presentation gọi Use Case trong Application Layer
3. Use Case gọi Domain Service
4. Domain Service sử dụng Repository Interfaces
5. Repository Implementations truy cập Database
6. Kết quả trả về theo thứ tự ngược lại

### **4. Testing Strategy**
- **Unit Tests**: Test từng component riêng biệt
- **Integration Tests**: Test interaction giữa components
- **End-to-End Tests**: Test toàn bộ workflow

## 🔧 Customization

### **Thêm component mới:**
1. Mở file .puml tương ứng
2. Thêm component vào layer phù hợp
3. Thêm dependencies
4. Update notes và comments

### **Thay đổi styling:**
1. Sửa theme: `!theme plain` → `!theme aws-orange`
2. Thay đổi colors: `#lightblue` → `#lightgreen`
3. Thêm icons: `component "Name" as Alias`

### **Thêm flow mới:**
1. Mở CLEAN_ARCHITECTURE_SEQUENCE_DIAGRAM.puml
2. Thêm participants mới
3. Thêm sequence calls
4. Thêm notes và comments

## 📝 Best Practices

### **1. Khi tạo diagram mới:**
- Sử dụng naming convention rõ ràng
- Thêm comments và notes chi tiết
- Sử dụng colors phù hợp
- Group related components

### **2. Khi update diagram:**
- Giữ nguyên structure cơ bản
- Update dependencies khi cần
- Thêm notes cho changes
- Test diagram trước khi commit

### **3. Khi share diagram:**
- Export thành PNG hoặc SVG
- Thêm context và explanation
- Link đến source code
- Update documentation

## 🐛 Troubleshooting

### **Common Issues:**

1. **Diagram không hiển thị:**
   - Kiểm tra syntax PlantUML
   - Sử dụng online editor để test
   - Check file encoding (UTF-8)

2. **Dependencies không đúng:**
   - Kiểm tra arrow directions
   - Verify component names
   - Check layer boundaries

3. **Styling issues:**
   - Kiểm tra theme syntax
   - Verify color codes
   - Check component definitions

### **Getting Help:**
- PlantUML Documentation: https://plantuml.com/
- Online Editor: https://www.plantuml.com/plantuml/uml/
- VS Code Extension: PlantUML
- Community: Stack Overflow

## 🎉 Kết luận

Bộ diagrams này cung cấp cái nhìn toàn diện về Clean Architecture trong dự án Display Program Management System. Sử dụng chúng để:

- ✅ Hiểu cấu trúc và flow của ứng dụng
- ✅ Onboard new developers
- ✅ Plan và design new features
- ✅ Debug và troubleshoot issues
- ✅ Document architecture decisions

**Hãy bắt đầu với SIMPLE_CLEAN_ARCHITECTURE_FLOW.puml để hiểu cơ bản!** 🚀
