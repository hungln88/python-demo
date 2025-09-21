# Hướng dẫn sử dụng Diagrams trên planttext.com

## 🎯 Vấn đề với emoji

Planttext.com có thể gặp lỗi khi xử lý các emoji trong PlantUML. Để giải quyết vấn đề này, tôi đã tạo các version khác nhau:

## 📋 Danh sách files tương thích

### 1. **CLEAN_ARCHITECTURE_SIMPLE_FIXED.puml** ⭐ (Khuyến nghị cho planttext.com)
- **Mô tả**: Version đơn giản nhất, chỉ có text và arrows
- **Tương thích**: ✅ planttext.com, ✅ plantuml.com
- **Sử dụng**: Copy nội dung và paste vào https://www.planttext.com/

### 2. **CLEAN_ARCHITECTURE_FIXED.puml**
- **Mô tả**: Version với packages, dễ hiểu
- **Tương thích**: ✅ planttext.com, ✅ plantuml.com
- **Sử dụng**: Copy nội dung và paste vào https://www.planttext.com/

### 3. **CLEAN_ARCHITECTURE_TEXT_FIXED.puml**
- **Mô tả**: Version đầy đủ thông tin, chỉ có text
- **Tương thích**: ✅ planttext.com, ✅ plantuml.com
- **Sử dụng**: Copy nội dung và paste vào https://www.planttext.com/

## 🚀 Cách sử dụng

### Bước 1: Chọn file phù hợp
```bash
# Khuyến nghị cho planttext.com:
CLEAN_ARCHITECTURE_SIMPLE_FIXED.puml  # Đơn giản nhất
CLEAN_ARCHITECTURE_FIXED.puml         # Với packages
CLEAN_ARCHITECTURE_TEXT_FIXED.puml    # Đầy đủ thông tin
```

### Bước 2: Copy nội dung
- Mở file .puml trong text editor
- Select All (Ctrl+A)
- Copy (Ctrl+C)

### Bước 3: Paste vào planttext.com
- Mở https://www.planttext.com/
- Paste nội dung vào text area
- Diagram sẽ tự động render

## 🔧 Troubleshooting

### Lỗi thường gặp:

1. **"Syntax error"**
   - **Nguyên nhân**: Emoji hoặc ký tự đặc biệt
   - **Giải pháp**: Sử dụng version NO_EMOJI hoặc ENGLISH

2. **"Component not found"**
   - **Nguyên nhân**: Thiếu package definition
   - **Giải pháp**: Sử dụng version MINIMAL

3. **"Theme not found"**
   - **Nguyên nhân**: Theme không hỗ trợ
   - **Giải pháp**: Thay `!theme plain` thành `!theme aws-orange`

### Các platform khác:

- **plantuml.com**: Hỗ trợ emoji tốt hơn
- **VS Code PlantUML**: Hỗ trợ đầy đủ
- **IntelliJ PlantUML**: Hỗ trợ đầy đủ

## 📊 So sánh các version

| Version | Emoji | Ngôn ngữ | Kích thước | Tương thích | Khuyến nghị |
|---------|-------|----------|------------|-------------|-------------|
| CLEAN_ARCHITECTURE_SIMPLE_FIXED.puml | ❌ | Tiếng Anh | Rất nhỏ | ✅ planttext.com | ⭐ Tốt nhất |
| CLEAN_ARCHITECTURE_FIXED.puml | ❌ | Tiếng Anh | Nhỏ | ✅ planttext.com | ✅ Tốt |
| CLEAN_ARCHITECTURE_TEXT_FIXED.puml | ❌ | Tiếng Anh | Trung bình | ✅ planttext.com | ✅ Tốt |

## 🎯 Khuyến nghị

### Cho planttext.com:
1. **CLEAN_ARCHITECTURE_SIMPLE_FIXED.puml** - Tốt nhất (đơn giản nhất)
2. **CLEAN_ARCHITECTURE_FIXED.puml** - Tốt (với packages)
3. **CLEAN_ARCHITECTURE_TEXT_FIXED.puml** - Tốt (đầy đủ thông tin)

### Cho plantuml.com:
- Tất cả 3 files đều tương thích với plantuml.com

## 🔄 Cách tạo version mới

Nếu cần tạo version khác:

1. **Copy file gốc**
2. **Thay thế emoji**:
   ```bash
   # Tìm và thay thế:
   🎨 → [PRESENTATION]
   📋 → [APPLICATION]
   🧠 → [DOMAIN]
   🔧 → [INFRASTRUCTURE]
   ```

3. **Thay thế ký tự đặc biệt**:
   ```bash
   # Tìm và thay thế:
   ✅ → [OK]
   ❌ → [FAIL]
   🚀 → [START]
   ```

4. **Test trên planttext.com**

## 📝 Lưu ý

- Luôn test trên platform trước khi sử dụng
- Giữ lại file gốc có emoji để sử dụng trên platform khác
- Cập nhật documentation khi tạo version mới
