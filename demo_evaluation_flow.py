"""
Demo script để minh họa chi tiết flow đánh giá customer
Demo script to illustrate detailed customer evaluation flow
Created: 2025-09-19

Script này giúp hiểu rõ cách hệ thống đánh giá customer có đủ điều kiện nhận thưởng hay không.
Bao gồm các scenarios khác nhau và giải thích chi tiết từng bước.
"""

import sys
import os

# Add current directory to path để import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import DatabaseConnection, DisplayProgramRepository
from business_logic import DisplayProgramService


def print_section_header(title: str):
    """In header cho mỗi section"""
    print("\n" + "="*80)
    print(f"🎯 {title}")
    print("="*80)


def demo_successful_evaluation():
    """Demo case: Customer đạt tất cả tiêu chí"""
    print_section_header("DEMO 1: CUSTOMER THÀNH CÔNG (Đủ điều kiện nhận thưởng)")
    
    try:
        # Khởi tạo service
        db_conn = DatabaseConnection()
        repo = DisplayProgramRepository(db_conn)
        service = DisplayProgramService(repo)
        
        # Đánh giá customer CUST001 - thường là high performer trong sample data
        customer_code = "CUST001"
        program_code = "PROG001"
        yyyymm = 202509
        
        print(f"📋 Đang đánh giá: {customer_code} cho chương trình {program_code} tháng {yyyymm}")
        print()
        
        # Lấy explanation chi tiết
        explanation = service.explain_evaluation_flow(yyyymm, customer_code, program_code)
        print(explanation)
        
        # Lấy kết quả đánh giá
        result = service.evaluate_customer(yyyymm, customer_code, program_code)
        
        print("\n📊 SUMMARY RESULT:")
        print(f"   - Total Points: {result.total_points}/{result.max_possible_points}")
        print(f"   - Success Rate: {result.success_rate:.1f}%")
        print(f"   - Meets Criteria: {'YES' if result.meets_criteria else 'NO'}")
        print(f"   - Registration Active: {'YES' if result.registration_status else 'NO'}")
        print(f"   - Eligible for Reward: {'YES' if result.is_eligible_for_reward else 'NO'}")
        
        if result.failed_conditions:
            print(f"   - Failed Conditions: {', '.join(result.failed_conditions)}")
        
    except Exception as e:
        print(f"❌ Error in demo: {e}")
        print("💡 Tip: Make sure database is running and sample data is loaded")


def demo_failed_evaluation():
    """Demo case: Customer không đạt tiêu chí"""
    print_section_header("DEMO 2: CUSTOMER THẤT BẠI (Không đủ điều kiện)")
    
    try:
        db_conn = DatabaseConnection()
        repo = DisplayProgramRepository(db_conn)
        service = DisplayProgramService(repo)
        
        # Đánh giá customer CUST005 - thường có performance thấp trong sample data
        customer_code = "CUST005"
        program_code = "PROG002"
        yyyymm = 202509
        
        print(f"📋 Đang đánh giá: {customer_code} cho chương trình {program_code} tháng {yyyymm}")
        print()
        
        # Lấy explanation chi tiết
        explanation = service.explain_evaluation_flow(yyyymm, customer_code, program_code)
        print(explanation)
        
        # Lấy kết quả đánh giá
        result = service.evaluate_customer(yyyymm, customer_code, program_code)
        
        print("\n📊 SUMMARY RESULT:")
        print(f"   - Total Points: {result.total_points}/{result.max_possible_points}")
        print(f"   - Success Rate: {result.success_rate:.1f}%")
        print(f"   - Meets Criteria: {'YES' if result.meets_criteria else 'NO'}")
        print(f"   - Registration Active: {'YES' if result.registration_status else 'NO'}")
        print(f"   - Eligible for Reward: {'YES' if result.is_eligible_for_reward else 'NO'}")
        
        if result.failed_conditions:
            print(f"   - Failed Conditions: {', '.join(result.failed_conditions)}")
        
    except Exception as e:
        print(f"❌ Error in demo: {e}")


def demo_not_registered():
    """Demo case: Customer không đăng ký"""
    print_section_header("DEMO 3: CUSTOMER KHÔNG ĐĂNG KÝ")
    
    try:
        db_conn = DatabaseConnection()
        repo = DisplayProgramRepository(db_conn)
        service = DisplayProgramService(repo)
        
        # Sử dụng customer không tồn tại
        customer_code = "CUST999"
        program_code = "PROG001"
        yyyymm = 202509
        
        print(f"📋 Đang đánh giá: {customer_code} cho chương trình {program_code} tháng {yyyymm}")
        print()
        
        # Lấy explanation chi tiết
        explanation = service.explain_evaluation_flow(yyyymm, customer_code, program_code)
        print(explanation)
        
    except Exception as e:
        print(f"❌ Error in demo: {e}")


def demo_business_rules_explanation():
    """Giải thích các business rules"""
    print_section_header("BUSINESS RULES EXPLANATION")
    
    rules = """
📋 CÁC QUY TẮC NGHIỆP VỤ (Business Rules):

1. 🔐 REGISTRATION REQUIREMENT (Yêu cầu đăng ký):
   - Customer PHẢI có đăng ký cho chương trình trong tháng đánh giá
   - Đăng ký phải ở trạng thái ACTIVE để có quyền nhận thưởng
   - Nếu không có đăng ký → LOẠI ngay, không cần kiểm tra tiêu chí

2. 📊 CRITERIA DEFINITION (Định nghĩa tiêu chí):
   - Mỗi chương trình phải có ít nhất 1 condition_item được định nghĩa
   - Mỗi condition có: condition_code, min_value, points
   - Nếu không có tiêu chí → LOẠI (lỗi cấu hình)

3. 🔍 AUDIT REQUIREMENT (Yêu cầu audit):
   - Customer phải được audit cho TẤT CẢ các condition_codes
   - Nếu thiếu audit cho bất kỳ condition nào → THẤT BẠI
   - Giá trị audit phải là số hợp lệ (0-100)

4. ⚖️ MINIMUM THRESHOLD (Ngưỡng tối thiểu):
   - Customer phải đạt minimum value cho TẤT CẢ conditions
   - Chỉ cần 1 condition không đạt → THẤT BẠI toàn bộ
   - Không có khái niệm "điểm bù" giữa các conditions

5. 🎯 POINTS CALCULATION (Tính điểm):
   - Chỉ cộng điểm cho conditions đạt minimum threshold
   - Conditions không đạt → 0 điểm
   - Tổng điểm chỉ có ý nghĩa thống kê, không ảnh hưởng kết quả

6. 🏆 REWARD ELIGIBILITY (Điều kiện nhận thưởng):
   - meets_criteria = True (đạt TẤT CẢ conditions)
   - registration_status = Active
   - Cả 2 điều kiện phải thỏa mãn

7. 📅 TIME SCOPE (Phạm vi thời gian):
   - Đánh giá theo tháng (yyyymm)
   - Chỉ xét đăng ký và audit trong cùng tháng
   - Không có carry-over giữa các tháng

EXAMPLES:
=========

Scenario A: THÀNH CÔNG
- Registration: ACTIVE ✅
- CLEANLINESS: 85 (min: 80) ✅ → +30 điểm
- PRODUCT_AVAILABILITY: 92 (min: 90) ✅ → +40 điểm  
- DISPLAY_QUALITY: 78 (min: 75) ✅ → +30 điểm
→ RESULT: 100/100 điểm, ĐỦ ĐIỀU KIỆN nhận thưởng

Scenario B: THẤT BẠI (1 condition không đạt)
- Registration: ACTIVE ✅
- CLEANLINESS: 85 (min: 80) ✅ → +30 điểm
- PRODUCT_AVAILABILITY: 88 (min: 90) ❌ → 0 điểm
- DISPLAY_QUALITY: 78 (min: 75) ✅ → +30 điểm
→ RESULT: 60/100 điểm, KHÔNG ĐỦ ĐIỀU KIỆN (thiếu 1 condition)

Scenario C: THẤT BẠI (registration inactive)
- Registration: INACTIVE ❌
- Tất cả conditions đạt ✅
→ RESULT: KHÔNG ĐỦ ĐIỀU KIỆN (dù đạt tiêu chí)
"""
    
    print(rules)


def main():
    """Main function chạy tất cả demos"""
    print("🎉 WELCOME TO DISPLAY PROGRAM EVALUATION FLOW DEMO")
    print("   Chào mừng đến với Demo Flow Đánh giá Chương trình Trưng bày")
    print()
    print("💡 Demo này sẽ minh họa cách hệ thống đánh giá customer có đủ điều kiện nhận thưởng")
    print("💡 Sử dụng sample data có sẵn trong database")
    print()
    
    try:
        # Kiểm tra database connection
        db_conn = DatabaseConnection()
        if not db_conn.test_connection():
            print("❌ Cannot connect to database!")
            print("💡 Please ensure:")
            print("   1. SQL Server is running")
            print("   2. DisplayProgramDB exists")
            print("   3. Sample data is loaded (run sample_data.sql)")
            return
        
        print("✅ Database connection OK")
        
        # Chạy các demo scenarios
        demo_business_rules_explanation()
        demo_successful_evaluation()
        demo_failed_evaluation()
        demo_not_registered()
        
        print_section_header("DEMO COMPLETED")
        print("🎉 All demo scenarios completed!")
        print()
        print("💡 Key Takeaways:")
        print("   1. Customer evaluation is a 5-step process")
        print("   2. ALL conditions must be met for reward eligibility")
        print("   3. Registration must be ACTIVE")
        print("   4. Audit results must exist for ALL conditions")
        print("   5. System provides detailed logging for troubleshooting")
        print()
        print("📚 For more details, see:")
        print("   - DEVELOPER_GUIDE.md: Complete documentation")
        print("   - business_logic.py: Source code with detailed comments")
        print("   - test_*.py: Unit tests with various scenarios")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        print("💡 Make sure database is properly set up and sample data is loaded")


if __name__ == "__main__":
    main()
