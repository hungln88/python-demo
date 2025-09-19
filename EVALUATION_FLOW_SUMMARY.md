# 🎯 CUSTOMER EVALUATION FLOW - CHI TIẾT NGHIỆP VỤ ĐÁNH GIÁ KHÁCH HÀNG

## 📋 Tổng quan

Đây là tài liệu chi tiết về **flow nghiệp vụ đánh giá khách hàng có đủ điều kiện nhận thưởng** trong hệ thống Display Program Management. Flow này là **CORE BUSINESS LOGIC** quan trọng nhất của hệ thống.

---

## 🔄 BUSINESS FLOW TỔNG QUAN

```
[Operations] Cấu hình chương trình → [Customer] Đăng ký → [Supervisor] Audit → [System] Đánh giá → [Result] Quyền nhận thưởng
```

### 📊 Data Flow Diagram

```
register_item (Cấu hình chương trình)
    ↓
condition_group + condition_item (Tiêu chí đánh giá)
    ↓
register (Đăng ký khách hàng)
    ↓
audit_picture (Kết quả audit)
    ↓
CustomerEvaluationResult (Kết quả đánh giá cuối cùng)
```

---

## 🎯 DETAILED EVALUATION FLOW (5 BƯỚC)

### **STEP 1: KIỂM TRA ĐĂNG KÝ** (Registration Verification)

#### Purpose: Xác minh customer có đăng ký hợp lệ cho chương trình

#### Process:
```python
# 1. Lấy TẤT CẢ đăng ký của customer trong tháng (bao gồm inactive)
registrations = repo.get_registrations(yyyymm, customer_code, active_only=False)

# 2. Tìm đăng ký cụ thể cho program_code
program_registration = find_registration_for_program(registrations, program_code)

# 3. Kiểm tra kết quả
if not program_registration:
    return LOẠI_NGAY("NOT_REGISTERED")
```

#### Business Rules:
- ✅ **PASS**: Customer có đăng ký cho program (dù active hay inactive)
- ❌ **FAIL**: Customer không có đăng ký → **LOẠI NGAY**, không cần kiểm tra tiêu chí

#### Output:
- `registration_status`: True/False (active/inactive)
- Nếu không có đăng ký → Return ngay với failed result

---

### **STEP 2: LẤY TIÊU CHÍ CHƯƠNG TRÌNH** (Get Program Criteria)

#### Purpose: Lấy tất cả tiêu chí đánh giá được cấu hình cho chương trình

#### Process:
```python
# 1. Lấy tất cả condition_items của program trong tháng
condition_items = repo.get_condition_items(yyyymm, program_code)

# 2. Kiểm tra có tiêu chí không
if not condition_items:
    return LOẠI("NO_CONDITIONS_DEFINED")
```

#### Business Rules:
- ✅ **PASS**: Program có ít nhất 1 condition được định nghĩa
- ❌ **FAIL**: Program không có tiêu chí → **LỖI CẤU HÌNH**

#### Data Structure:
```python
ConditionItem:
    - condition_code: str (CLEANLINESS, PRODUCT_AVAILABILITY, DISPLAY_QUALITY)
    - condition_min_value: int (0-100, yêu cầu tối thiểu)
    - condition_point: int (điểm được cộng nếu đạt)
```

---

### **STEP 3: LẤY KẾT QUẢ AUDIT** (Get Audit Results)

#### Purpose: Lấy kết quả đo đạc thực tế từ audit của supervisors

#### Process:
```python
# 1. Lấy tất cả audit results của customer trong tháng
audit_results = repo.get_audit_results(yyyymm, customer_code)

# 2. Tạo dictionary để lookup nhanh
audit_dict = {audit.condition_code: audit for audit in audit_results}
```

#### Business Rules:
- Audit results chứa giá trị thực tế đo được tại điểm bán
- Mỗi audit có: condition_code, value (string), audit_date
- Value được convert thành numeric_value (int) để so sánh

#### Data Structure:
```python
AuditPicture:
    - condition_code: str (phải match với condition_item)
    - value: str (giá trị đo được, ví dụ: "85")
    - numeric_value: int (convert từ value để so sánh)
    - audit_date: datetime (thời gian audit)
```

---

### **STEP 4: SO SÁNH & TÍNH ĐIỂM** (Compare & Calculate Points)

#### Purpose: So sánh từng audit result với tiêu chí và tính điểm

#### Process:
```python
total_points = 0
max_possible_points = 0
failed_conditions = []

for condition in condition_items:
    # A. Cộng điểm tối đa có thể đạt
    max_possible_points += condition.condition_point
    
    # B. Kiểm tra có audit result không
    audit_result = audit_dict.get(condition.condition_code)
    if not audit_result:
        failed_conditions.append(f"{condition.condition_code}_NOT_AUDITED")
        continue
    
    # C. So sánh với yêu cầu tối thiểu
    actual_value = audit_result.numeric_value
    if actual_value >= condition.condition_min_value:
        # ĐẠT → Cộng điểm
        total_points += condition.condition_point
    else:
        # KHÔNG ĐẠT → Thêm vào failed list
        failed_conditions.append(f"{condition.condition_code}_BELOW_MINIMUM({actual_value}<{condition.condition_min_value})")
```

#### Business Rules:
- **ALL OR NOTHING**: Phải đạt TẤT CẢ conditions, không có "bù trừ"
- **Minimum Threshold**: `actual_value >= condition_min_value`
- **Points**: Chỉ cộng điểm cho conditions đạt yêu cầu
- **No Audit = Fail**: Thiếu audit cho bất kỳ condition nào → Thất bại

#### Examples:
```
Condition: CLEANLINESS (min: 80, points: 30)
- Audit: 85 → ĐẠT → +30 điểm
- Audit: 75 → KHÔNG ĐẠT → 0 điểm, thêm vào failed_conditions

Condition: PRODUCT_AVAILABILITY (min: 90, points: 40)  
- Không có audit → 0 điểm, thêm "PRODUCT_AVAILABILITY_NOT_AUDITED"
```

---

### **STEP 5: XÁC ĐỊNH KẾT QUẢ CUỐI CÙNG** (Final Determination)

#### Purpose: Quyết định customer có đủ điều kiện nhận thưởng không

#### Process:
```python
# 1. Kiểm tra đạt tất cả tiêu chí
meets_criteria = len(failed_conditions) == 0

# 2. Kiểm tra quyền nhận thưởng
is_eligible_for_reward = meets_criteria AND registration_status_active

# 3. Tạo kết quả cuối cùng
return CustomerEvaluationResult(
    total_points=total_points,
    max_possible_points=max_possible_points,
    meets_criteria=meets_criteria,
    failed_conditions=failed_conditions,
    registration_status=registration.is_active
)
```

#### Business Rules:
- **meets_criteria**: True chỉ khi `failed_conditions` rỗng
- **is_eligible_for_reward**: `meets_criteria = True` AND `registration_status = Active`
- Nếu registration inactive dù đạt tiêu chí → Vẫn không được thưởng

---

## 📊 SCENARIOS & EXAMPLES

### ✅ **Scenario A: THÀNH CÔNG**
```
Input:
- Customer: CUST001
- Program: PROG001  
- Registration: ACTIVE ✅

Conditions & Audit Results:
- CLEANLINESS: audit=85, min=80 ✅ → +30 điểm
- PRODUCT_AVAILABILITY: audit=92, min=90 ✅ → +40 điểm
- DISPLAY_QUALITY: audit=78, min=75 ✅ → +30 điểm

Result:
- total_points: 100/100
- meets_criteria: True
- is_eligible_for_reward: True
- failed_conditions: []
```

### ❌ **Scenario B: THẤT BẠI (1 condition không đạt)**
```
Input:
- Customer: CUST002
- Program: PROG001
- Registration: ACTIVE ✅

Conditions & Audit Results:
- CLEANLINESS: audit=85, min=80 ✅ → +30 điểm
- PRODUCT_AVAILABILITY: audit=88, min=90 ❌ → 0 điểm
- DISPLAY_QUALITY: audit=78, min=75 ✅ → +30 điểm

Result:
- total_points: 60/100
- meets_criteria: False
- is_eligible_for_reward: False
- failed_conditions: ["PRODUCT_AVAILABILITY_BELOW_MINIMUM(88<90)"]
```

### ⏸️ **Scenario C: REGISTRATION INACTIVE**
```
Input:
- Customer: CUST003
- Program: PROG001
- Registration: INACTIVE ❌

Conditions & Audit Results:
- Tất cả conditions đạt ✅

Result:
- total_points: 100/100
- meets_criteria: True
- is_eligible_for_reward: False (vì registration inactive)
- failed_conditions: []
```

### 🚫 **Scenario D: KHÔNG ĐĂNG KÝ**
```
Input:
- Customer: CUST999
- Program: PROG001
- Registration: NONE ❌

Result:
- total_points: 0/0
- meets_criteria: False
- is_eligible_for_reward: False
- failed_conditions: ["NOT_REGISTERED"]
```

---

## 🛠️ IMPLEMENTATION DETAILS

### Core Method: `evaluate_customer()`

```python
def evaluate_customer(self, yyyymm: int, customer_code: str, program_code: str) -> CustomerEvaluationResult:
    """
    🎯 CORE METHOD: Đánh giá khách hàng có đủ điều kiện nhận thưởng hay không
    
    Returns CustomerEvaluationResult với:
    - total_points: Tổng điểm đạt được
    - max_possible_points: Tổng điểm tối đa
    - meets_criteria: Đạt tất cả tiêu chí không
    - failed_conditions: Danh sách lý do thất bại
    - registration_status: Trạng thái đăng ký
    """
```

### Helper Methods:

1. **`explain_evaluation_flow()`**: Tạo báo cáo chi tiết về quá trình đánh giá
2. **`get_eligible_customers_for_rewards()`**: Lấy danh sách customers đủ điều kiện
3. **`get_failed_customers()`**: Lấy danh sách customers thất bại

### Logging & Debugging:

```python
# Detailed logging at each step
self.logger.info(f"🔍 Starting evaluation for {customer_code}")
self.logger.debug(f"Step 1: Checking registration")
self.logger.debug(f"✅ Registration found - Status: Active")
self.logger.info(f"🎉 EVALUATION SUCCESS: meets all criteria")
```

---

## 🎯 BUSINESS IMPACT

### 💰 Financial Impact:
- **Eligible customers** → Nhận hoa hồng/thưởng
- **Failed customers** → Không nhận thưởng
- **Success rate** → KPI đánh giá hiệu quả chương trình

### 📈 Management Reports:
- Tỷ lệ thành công theo chương trình
- Phân tích lý do thất bại phổ biến
- Hiệu quả đầu tư chương trình marketing

### 🔧 Operational Use:
- Danh sách thanh toán hàng tháng
- Feedback cho customers về performance
- Cải thiện chương trình dựa trên kết quả

---

## 🧪 TESTING & VALIDATION

### Test Cases Coverage:
- ✅ Customer đạt tất cả tiêu chí
- ❌ Customer thiếu 1 condition
- ❌ Customer thiếu audit
- ❌ Customer không đăng ký
- ⏸️ Customer có đăng ký inactive
- 🔧 Program không có tiêu chí

### Demo Script:
```bash
python demo_evaluation_flow.py
```

### Unit Tests:
```bash
python run_tests.py test_business_logic
```

---

## 📚 RELATED FILES

| File | Purpose |
|------|---------|
| `business_logic.py` | Core evaluation logic với detailed comments |
| `models.py` | Data structures và validation |
| `database.py` | Data access operations |
| `demo_evaluation_flow.py` | Interactive demo với examples |
| `test_business_logic.py` | Unit tests cho evaluation logic |
| `DEVELOPER_GUIDE.md` | Complete developer documentation |

---

## 🎉 CONCLUSION

Customer evaluation flow là **trái tim** của Display Program Management System. Nó quyết định:

1. **Ai được thưởng** (financial impact)
2. **Tại sao được thưởng** (transparency)  
3. **Làm thế nào cải thiện** (continuous improvement)

Flow này được thiết kế với:
- ✅ **Tính minh bạch**: Mọi bước đều có log chi tiết
- ✅ **Tính công bằng**: Rules áp dụng đồng nhất cho tất cả
- ✅ **Tính chính xác**: Validation ở mọi bước
- ✅ **Tính mở rộng**: Dễ thêm tiêu chí mới

**🚀 Ready for production with enterprise-grade reliability!**
