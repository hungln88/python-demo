"""
Business logic for Display Program Management System
Logic nghiệp vụ cho Hệ thống Quản lý Chương trình Trưng bày
Created: 2025-09-19

Tệp này chứa core business logic để:
1. Đánh giá khách hàng theo tiêu chí chương trình (Customer Evaluation)
2. Xác định quyền nhận thưởng (Reward Eligibility)
3. Tạo báo cáo và thống kê (Reporting)
4. Validate business rules (Validation)

BUSINESS FLOW TỔNG QUAN:
=========================
1. [Operations] Cấu hình chương trình trong register_item
2. [Operations] Thiết lập tiêu chí đánh giá trong condition_group + condition_item
3. [Customers] Đăng ký tham gia chương trình trong register
4. [Supervisors] Thực hiện audit tại điểm bán, ghi kết quả vào audit_picture
5. [System] Đánh giá customer theo tiêu chí và xác định quyền nhận thưởng

CUSTOMER EVALUATION FLOW:
========================
Step 1: Kiểm tra đăng ký (Registration Check)
Step 2: Lấy tiêu chí chương trình (Get Program Criteria)
Step 3: Lấy kết quả audit (Get Audit Results)
Step 4: So sánh audit vs tiêu chí (Compare & Calculate Points)
Step 5: Xác định đủ điều kiện (Determine Eligibility)
"""

import logging
from typing import List, Dict, Optional, Tuple
from collections import defaultdict

from models import (
    RegisterItem, Register, ConditionGroup, ConditionItem, 
    AuditPicture, CustomerEvaluationResult
)
from database import DisplayProgramRepository


class DisplayProgramService:
    """
    Service class chính cho quản lý chương trình trưng bày
    
    Class này chứa tất cả business logic để:
    - Đánh giá khách hàng theo tiêu chí chương trình
    - Xác định quyền nhận thưởng
    - Tạo báo cáo và thống kê
    - Validate các business rules
    
    Attributes:
        repo (DisplayProgramRepository): Repository để truy cập dữ liệu
        logger (Logger): Logger để ghi log các thao tác
    """
    
    def __init__(self, repository: DisplayProgramRepository):
        """
        Khởi tạo service với repository
        
        Args:
            repository: Repository instance để truy cập database
        """
        self.repo = repository
        self.logger = logging.getLogger(__name__)
        
        self.logger.info("DisplayProgramService initialized")
    
    def evaluate_customer(self, yyyymm: int, customer_code: str, program_code: str) -> CustomerEvaluationResult:
        """
        🎯 CORE METHOD: Đánh giá khách hàng có đủ điều kiện nhận thưởng hay không
        
        Đây là method quan trọng nhất của hệ thống, thực hiện việc đánh giá toàn diện
        một khách hàng theo các tiêu chí của chương trình để xác định quyền nhận thưởng.
        
        📋 DETAILED EVALUATION FLOW:
        ============================
        
        STEP 1: KIỂM TRA ĐĂNG KÝ (Registration Verification)
        ---------------------------------------------------
        - Lấy tất cả đăng ký của customer trong tháng (bao gồm cả inactive)
        - Tìm đăng ký cụ thể cho program_code
        - Nếu không có đăng ký → LOẠI (NOT_REGISTERED)
        
        STEP 2: LẤY TIÊU CHÍ CHƯƠNG TRÌNH (Get Program Criteria)
        --------------------------------------------------------
        - Lấy tất cả condition_items của program trong tháng
        - Mỗi condition_item có: condition_code, min_value, points
        - Nếu không có tiêu chí → LOẠI (NO_CONDITIONS_DEFINED)
        
        STEP 3: LẤY KẾT QUẢ AUDIT (Get Audit Results)
        ---------------------------------------------
        - Lấy tất cả audit_picture của customer trong tháng
        - Tạo dictionary mapping: condition_code → audit_result
        - Audit results chứa giá trị thực tế đo được tại điểm bán
        
        STEP 4: SO SÁNH & TÍNH ĐIỂM (Compare & Calculate Points)
        --------------------------------------------------------
        For mỗi condition_item:
        a) Cộng condition_point vào max_possible_points
        b) Kiểm tra có audit_result tương ứng không
           - Nếu không có → Thêm vào failed_conditions: "CONDITION_NOT_AUDITED"
           - Nếu có → Tiếp tục step c
        c) So sánh actual_value vs condition_min_value
           - Nếu actual_value >= min_value → Đạt tiêu chí, cộng điểm
           - Nếu actual_value < min_value → Không đạt, thêm vào failed_conditions
        
        STEP 5: XÁC ĐỊNH KẾT QUẢ CUỐI CÙNG (Final Determination)
        --------------------------------------------------------
        - meets_criteria = True nếu failed_conditions rỗng (đạt TẤT CẢ tiêu chí)
        - is_eligible_for_reward = meets_criteria AND registration_status = active
        
        Args:
            yyyymm (int): Tháng/năm đánh giá (format YYYYMM)
            customer_code (str): Mã khách hàng cần đánh giá
            program_code (str): Mã chương trình cần đánh giá
        
        Returns:
            CustomerEvaluationResult: Kết quả đánh giá chi tiết bao gồm:
                - total_points: Tổng điểm đạt được
                - max_possible_points: Tổng điểm tối đa có thể đạt
                - meets_criteria: Có đạt tất cả tiêu chí không
                - failed_conditions: Danh sách tiêu chí không đạt
                - registration_status: Trạng thái đăng ký (active/inactive)
        
        Business Rules:
            1. Customer PHẢI có đăng ký cho program
            2. Program PHẢI có ít nhất 1 condition được định nghĩa
            3. Customer PHẢI được audit cho TẤT CẢ các conditions
            4. Customer PHẢI đạt minimum value cho TẤT CẢ conditions
            5. Chỉ đăng ký ACTIVE mới có quyền nhận thưởng
        
        Example:
            >>> service = DisplayProgramService(repo)
            >>> result = service.evaluate_customer(202509, "CUST001", "PROG001")
            >>> if result.is_eligible_for_reward:
            ...     print(f"Customer đủ điều kiện nhận thưởng: {result.total_points}/{result.max_possible_points} điểm")
            ... else:
            ...     print(f"Customer không đủ điều kiện: {result.get_failure_summary()}")
        """
        
        self.logger.info(f"🔍 Starting evaluation for customer {customer_code} in program {program_code} ({yyyymm})")
        
        # ==========================================
        # STEP 1: KIỂM TRA ĐĂNG KÝ
        # ==========================================
        self.logger.debug(f"Step 1: Checking registration for {customer_code}")
        
        # Lấy TẤT CẢ đăng ký của customer (bao gồm cả inactive) để kiểm tra đầy đủ
        registrations = self.repo.get_registrations(yyyymm, customer_code, active_only=False)
        
        # Tìm đăng ký cụ thể cho program này
        program_registration = next(
            (r for r in registrations if r.program_code == program_code), 
            None
        )
        
        # Nếu không có đăng ký → LOẠI ngay
        if not program_registration:
            self.logger.warning(f"❌ Customer {customer_code} not registered for program {program_code}")
            return CustomerEvaluationResult(
                yyyymm=yyyymm,
                customer_code=customer_code,
                program_code=program_code,
                total_points=0,
                max_possible_points=0,
                meets_criteria=False,
                failed_conditions=["NOT_REGISTERED"],
                registration_status=False
            )
        
        self.logger.debug(f"✅ Registration found - Status: {'Active' if program_registration.is_active else 'Inactive'}")
        
        # ==========================================
        # STEP 2: LẤY TIÊU CHÍ CHƯƠNG TRÌNH
        # ==========================================
        self.logger.debug(f"Step 2: Getting program criteria for {program_code}")
        
        # Lấy tất cả condition_items của program trong tháng này
        condition_items = self.repo.get_condition_items(yyyymm, program_code)
        
        # Nếu program không có tiêu chí → LOẠI (lỗi cấu hình)
        if not condition_items:
            self.logger.error(f"❌ No conditions defined for program {program_code} in {yyyymm}")
            return CustomerEvaluationResult(
                yyyymm=yyyymm,
                customer_code=customer_code,
                program_code=program_code,
                total_points=0,
                max_possible_points=0,
                meets_criteria=False,
                failed_conditions=["NO_CONDITIONS_DEFINED"],
                registration_status=program_registration.is_active
            )
        
        self.logger.debug(f"✅ Found {len(condition_items)} conditions for program {program_code}")
        
        # ==========================================
        # STEP 3: LẤY KẾT QUẢ AUDIT
        # ==========================================
        self.logger.debug(f"Step 3: Getting audit results for {customer_code}")
        
        # Lấy tất cả audit results của customer trong tháng
        audit_results = self.repo.get_audit_results(yyyymm, customer_code)
        
        # Tạo dictionary để lookup nhanh: condition_code → audit_result
        audit_dict = {audit.condition_code: audit for audit in audit_results}
        
        self.logger.debug(f"✅ Found audit results for {len(audit_dict)} conditions")
        
        # ==========================================
        # STEP 4: SO SÁNH & TÍNH ĐIỂM
        # ==========================================
        self.logger.debug(f"Step 4: Comparing audit results vs criteria")
        
        # Khởi tạo variables để tính toán
        total_points = 0              # Tổng điểm customer đạt được
        max_possible_points = 0       # Tổng điểm tối đa có thể đạt
        failed_conditions = []        # Danh sách các lý do thất bại
        
        # Duyệt qua từng tiêu chí của program
        for condition in condition_items:
            # Cộng điểm tối đa có thể đạt
            max_possible_points += condition.condition_point
            
            self.logger.debug(f"  📊 Evaluating condition: {condition.condition_code} "
                            f"(min: {condition.condition_min_value}, points: {condition.condition_point})")
            
            # Kiểm tra có kết quả audit cho condition này không
            audit_result = audit_dict.get(condition.condition_code)
            if not audit_result:
                # Không có audit → THẤT BẠI
                failure_reason = f"{condition.condition_code}_NOT_AUDITED"
                failed_conditions.append(failure_reason)
                self.logger.debug(f"    ❌ No audit result found for {condition.condition_code}")
                continue
            
            # Lấy giá trị thực tế từ audit
            actual_value = audit_result.numeric_value
            
            # So sánh với yêu cầu tối thiểu
            if condition.meets_minimum(actual_value):
                # ĐẠT yêu cầu → Cộng điểm
                total_points += condition.condition_point
                self.logger.debug(f"    ✅ PASSED: {actual_value} >= {condition.condition_min_value} "
                                f"→ +{condition.condition_point} points")
            else:
                # KHÔNG ĐẠT yêu cầu → Thêm vào failed list
                failure_reason = (f"{condition.condition_code}_BELOW_MINIMUM"
                                f"({actual_value}<{condition.condition_min_value})")
                failed_conditions.append(failure_reason)
                self.logger.debug(f"    ❌ FAILED: {actual_value} < {condition.condition_min_value} "
                                f"→ No points")
        
        # ==========================================
        # STEP 5: XÁC ĐỊNH KẾT QUẢ CUỐI CÙNG
        # ==========================================
        self.logger.debug(f"Step 5: Determining final result")
        
        # Customer chỉ đạt tiêu chí nếu KHÔNG có lỗi nào
        meets_criteria = len(failed_conditions) == 0
        
        # Tính success rate
        success_rate = (total_points / max_possible_points * 100) if max_possible_points > 0 else 0
        
        # Log kết quả cuối cùng
        if meets_criteria:
            self.logger.info(f"🎉 EVALUATION SUCCESS: {customer_code} meets all criteria "
                           f"({total_points}/{max_possible_points} points, {success_rate:.1f}%)")
        else:
            self.logger.info(f"💥 EVALUATION FAILED: {customer_code} failed {len(failed_conditions)} conditions "
                           f"({total_points}/{max_possible_points} points, {success_rate:.1f}%)")
            for failure in failed_conditions:
                self.logger.debug(f"    ❌ {failure}")
        
        # Tạo và trả về kết quả đánh giá
        result = CustomerEvaluationResult(
            yyyymm=yyyymm,
            customer_code=customer_code,
            program_code=program_code,
            total_points=total_points,
            max_possible_points=max_possible_points,
            meets_criteria=meets_criteria,
            failed_conditions=failed_conditions,
            registration_status=program_registration.is_active
        )
        
        # Log thông tin về quyền nhận thưởng
        if result.is_eligible_for_reward:
            self.logger.info(f"🏆 REWARD ELIGIBLE: {customer_code} is eligible for rewards")
        else:
            reason = "inactive registration" if not result.registration_status else "failed criteria"
            self.logger.info(f"🚫 REWARD INELIGIBLE: {customer_code} not eligible due to {reason}")
        
        return result
    
    def evaluate_all_customers_for_program(self, yyyymm: int, program_code: str) -> List[CustomerEvaluationResult]:
        """
        📊 Đánh giá TẤT CẢ khách hàng đăng ký một chương trình cụ thể
        
        Method này sử dụng evaluate_customer() để đánh giá từng khách hàng
        một cách riêng biệt, sau đó tổng hợp kết quả.
        
        Flow:
        1. Lấy danh sách tất cả customers đăng ký program (chỉ active)
        2. For mỗi customer: gọi evaluate_customer()
        3. Tổng hợp tất cả kết quả vào một list
        
        Args:
            yyyymm: Tháng/năm đánh giá
            program_code: Mã chương trình cần đánh giá
            
        Returns:
            List[CustomerEvaluationResult]: Danh sách kết quả đánh giá của tất cả customers
            
        Use Case:
            - Tạo báo cáo hiệu suất chương trình
            - Xác định tỷ lệ thành công của chương trình
            - Phân tích lý do thất bại phổ biến
        """
        self.logger.info(f"🔍 Evaluating all customers for program {program_code} ({yyyymm})")
        
        # Lấy danh sách customers đã đăng ký program (chỉ active)
        customers = self.repo.get_program_customers(yyyymm, program_code)
        results = []
        
        self.logger.debug(f"Found {len(customers)} customers registered for {program_code}")
        
        # Đánh giá từng customer
        for customer_code in customers:
            self.logger.debug(f"Evaluating customer {customer_code}...")
            result = self.evaluate_customer(yyyymm, customer_code, program_code)
            results.append(result)
        
        # Log summary
        eligible_count = sum(1 for r in results if r.is_eligible_for_reward)
        self.logger.info(f"📊 Program {program_code} evaluation complete: "
                        f"{eligible_count}/{len(results)} customers eligible for rewards")
        
        return results
    
    def evaluate_customer_all_programs(self, yyyymm: int, customer_code: str) -> List[CustomerEvaluationResult]:
        """Evaluate a customer against all programs they're registered for"""
        programs = self.repo.get_customer_programs(yyyymm, customer_code)
        results = []
        
        for program_code in programs:
            result = self.evaluate_customer(yyyymm, customer_code, program_code)
            results.append(result)
        
        return results
    
    def get_eligible_customers_for_rewards(self, yyyymm: int, program_code: str = None) -> List[CustomerEvaluationResult]:
        """
        🏆 Lấy danh sách khách hàng ĐỦ ĐIỀU KIỆN nhận thưởng
        
        Method này là output chính của hệ thống - xác định customers nào
        sẽ được trả thưởng dựa trên kết quả đánh giá.
        
        REWARD ELIGIBILITY CRITERIA:
        ============================
        Customer được coi là đủ điều kiện nhận thưởng khi:
        1. Có đăng ký ACTIVE cho chương trình
        2. ĐẠT TẤT CẢ tiêu chí tối thiểu (meets_criteria = True)
        3. Đã được audit đầy đủ cho tất cả conditions
        
        Args:
            yyyymm: Tháng/năm cần lấy danh sách
            program_code: Mã chương trình cụ thể (None = tất cả chương trình)
            
        Returns:
            List[CustomerEvaluationResult]: Chỉ những customers đủ điều kiện nhận thưởng
            
        Business Impact:
            - Kết quả này được dùng để tính toán số tiền thưởng
            - Tạo danh sách thanh toán hoa hồng
            - Báo cáo hiệu quả chương trình cho management
        """
        self.logger.info(f"🏆 Getting eligible customers for rewards ({yyyymm})")
        
        if program_code:
            # Đánh giá cho chương trình cụ thể
            self.logger.debug(f"Evaluating specific program: {program_code}")
            results = self.evaluate_all_customers_for_program(yyyymm, program_code)
        else:
            # Đánh giá cho TẤT CẢ chương trình
            self.logger.debug("Evaluating all programs")
            results = []
            registrations = self.repo.get_registrations(yyyymm, active_only=True)
            processed = set()  # Tránh đánh giá trùng lặp
            
            for reg in registrations:
                key = (reg.customer_code, reg.program_code)
                if key not in processed:
                    result = self.evaluate_customer(yyyymm, reg.customer_code, reg.program_code)
                    results.append(result)
                    processed.add(key)
        
        # Lọc chỉ lấy customers đủ điều kiện nhận thưởng
        eligible_customers = [r for r in results if r.is_eligible_for_reward]
        
        # Log kết quả
        total_evaluated = len(results)
        eligible_count = len(eligible_customers)
        eligibility_rate = (eligible_count / total_evaluated * 100) if total_evaluated > 0 else 0
        
        self.logger.info(f"🎯 REWARD ELIGIBILITY SUMMARY: {eligible_count}/{total_evaluated} customers eligible "
                        f"({eligibility_rate:.1f}% success rate)")
        
        # Log chi tiết customers đủ điều kiện
        if eligible_customers:
            self.logger.debug("Eligible customers:")
            for result in eligible_customers:
                self.logger.debug(f"  ✅ {result.customer_code} - {result.program_code}: "
                                f"{result.total_points}/{result.max_possible_points} points")
        
        return eligible_customers
    
    def get_failed_customers(self, yyyymm: int, program_code: str = None) -> List[CustomerEvaluationResult]:
        """Get customers who failed to meet criteria"""
        if program_code:
            results = self.evaluate_all_customers_for_program(yyyymm, program_code)
        else:
            # Evaluate all customers for all programs
            results = []
            registrations = self.repo.get_registrations(yyyymm, active_only=True)
            processed = set()
            
            for reg in registrations:
                key = (reg.customer_code, reg.program_code)
                if key not in processed:
                    result = self.evaluate_customer(yyyymm, reg.customer_code, reg.program_code)
                    results.append(result)
                    processed.add(key)
        
        # Filter only failed customers (registered and active but not meeting criteria)
        return [r for r in results if r.registration_status and not r.meets_criteria]
    
    def generate_program_summary(self, yyyymm: int, program_code: str) -> Dict:
        """Generate summary report for a program"""
        results = self.evaluate_all_customers_for_program(yyyymm, program_code)
        
        eligible_count = sum(1 for r in results if r.is_eligible_for_reward)
        failed_count = sum(1 for r in results if r.registration_status and not r.meets_criteria)
        inactive_count = sum(1 for r in results if not r.registration_status)
        
        # Get condition items for reference
        condition_items = self.repo.get_condition_items(yyyymm, program_code)
        condition_groups = self.repo.get_condition_groups(yyyymm, program_code)
        
        # Analyze common failure reasons
        failure_analysis = defaultdict(int)
        for result in results:
            if not result.meets_criteria:
                for failure in result.failed_conditions:
                    failure_analysis[failure] += 1
        
        return {
            'yyyymm': yyyymm,
            'program_code': program_code,
            'total_customers': len(results),
            'eligible_customers': eligible_count,
            'failed_customers': failed_count,
            'inactive_customers': inactive_count,
            'success_rate': (eligible_count / len(results) * 100) if results else 0,
            'condition_groups': len(condition_groups),
            'condition_items': len(condition_items),
            'common_failures': dict(failure_analysis),
            'detailed_results': results
        }
    
    def generate_customer_summary(self, yyyymm: int, customer_code: str) -> Dict:
        """Generate summary report for a customer"""
        results = self.evaluate_customer_all_programs(yyyymm, customer_code)
        
        eligible_programs = [r for r in results if r.is_eligible_for_reward]
        failed_programs = [r for r in results if r.registration_status and not r.meets_criteria]
        
        total_points = sum(r.total_points for r in results)
        max_possible_points = sum(r.max_possible_points for r in results)
        
        return {
            'yyyymm': yyyymm,
            'customer_code': customer_code,
            'total_programs': len(results),
            'eligible_programs': len(eligible_programs),
            'failed_programs': len(failed_programs),
            'total_points': total_points,
            'max_possible_points': max_possible_points,
            'overall_success_rate': (total_points / max_possible_points * 100) if max_possible_points > 0 else 0,
            'program_details': results
        }
    
    def generate_monthly_report(self, yyyymm: int) -> Dict:
        """Generate comprehensive monthly report"""
        # Get basic statistics
        stats = self.repo.get_monthly_statistics(yyyymm)
        
        # Get all active registrations
        registrations = self.repo.get_registrations(yyyymm, active_only=True)
        
        # Group by program
        program_results = {}
        customer_results = {}
        
        processed_combinations = set()
        
        for reg in registrations:
            key = (reg.customer_code, reg.program_code)
            if key not in processed_combinations:
                result = self.evaluate_customer(yyyymm, reg.customer_code, reg.program_code)
                
                # Add to program results
                if reg.program_code not in program_results:
                    program_results[reg.program_code] = []
                program_results[reg.program_code].append(result)
                
                # Add to customer results
                if reg.customer_code not in customer_results:
                    customer_results[reg.customer_code] = []
                customer_results[reg.customer_code].append(result)
                
                processed_combinations.add(key)
        
        # Calculate overall metrics
        all_results = []
        for program_list in program_results.values():
            all_results.extend(program_list)
        
        total_eligible = sum(1 for r in all_results if r.is_eligible_for_reward)
        total_failed = sum(1 for r in all_results if r.registration_status and not r.meets_criteria)
        
        return {
            'yyyymm': yyyymm,
            'basic_stats': stats,
            'total_evaluations': len(all_results),
            'total_eligible_for_rewards': total_eligible,
            'total_failed_criteria': total_failed,
            'overall_success_rate': (total_eligible / len(all_results) * 100) if all_results else 0,
            'program_summaries': {
                program: self.generate_program_summary(yyyymm, program) 
                for program in program_results.keys()
            },
            'customer_summaries': {
                customer: self.generate_customer_summary(yyyymm, customer) 
                for customer in customer_results.keys()
            }
        }
    
    def validate_registration(self, registration: Register) -> Tuple[bool, List[str]]:
        """Validate if a registration is valid"""
        errors = []
        
        # Check if program exists
        register_items = self.repo.get_register_items(registration.yyyymm, registration.program_code)
        if not register_items:
            errors.append(f"Program {registration.program_code} not found for {registration.yyyymm}")
            return False, errors
        
        # Check if display type is valid for the program
        valid_display_types = [item.item for item in register_items]
        if registration.display_type not in valid_display_types:
            errors.append(f"Display type {registration.display_type} not valid for program {registration.program_code}")
        
        # Check quantity is positive
        if registration.register_qty <= 0:
            errors.append("Registration quantity must be positive")
        
        return len(errors) == 0, errors
    
    def explain_evaluation_flow(self, yyyymm: int, customer_code: str, program_code: str) -> str:
        """
        📖 GIẢI THÍCH CHI TIẾT FLOW ĐÁNH GIÁ CUSTOMER
        
        Method này tạo ra một báo cáo chi tiết về quá trình đánh giá customer,
        giúp hiểu rõ tại sao customer đạt hoặc không đạt tiêu chí.
        
        Returns:
            str: Báo cáo chi tiết về quá trình đánh giá
        """
        
        explanation = []
        explanation.append("=" * 80)
        explanation.append(f"📋 CUSTOMER EVALUATION FLOW EXPLANATION")
        explanation.append(f"    Giải thích chi tiết quá trình đánh giá khách hàng")
        explanation.append("=" * 80)
        explanation.append(f"🎯 Customer: {customer_code}")
        explanation.append(f"🎯 Program: {program_code}")
        explanation.append(f"🎯 Month: {yyyymm}")
        explanation.append("")
        
        # STEP 1: Registration Check
        explanation.append("STEP 1: KIỂM TRA ĐĂNG KÝ (Registration Check)")
        explanation.append("-" * 50)
        
        registrations = self.repo.get_registrations(yyyymm, customer_code, active_only=False)
        program_registration = next((r for r in registrations if r.program_code == program_code), None)
        
        if not program_registration:
            explanation.append("❌ RESULT: Customer KHÔNG có đăng ký cho program này")
            explanation.append("   → LOẠI NGAY - Không đủ điều kiện nhận thưởng")
            return "\n".join(explanation)
        
        explanation.append(f"✅ RESULT: Tìm thấy đăng ký")
        explanation.append(f"   - Display Type: {program_registration.display_type}")
        explanation.append(f"   - Quantity: {program_registration.register_qty}")
        explanation.append(f"   - Status: {'ACTIVE' if program_registration.is_active else 'INACTIVE'}")
        explanation.append("")
        
        # STEP 2: Program Criteria
        explanation.append("STEP 2: LẤY TIÊU CHÍ CHƯƠNG TRÌNH (Get Program Criteria)")
        explanation.append("-" * 50)
        
        condition_items = self.repo.get_condition_items(yyyymm, program_code)
        
        if not condition_items:
            explanation.append("❌ RESULT: Program KHÔNG có tiêu chí được định nghĩa")
            explanation.append("   → LOẠI - Lỗi cấu hình chương trình")
            return "\n".join(explanation)
        
        explanation.append(f"✅ RESULT: Tìm thấy {len(condition_items)} tiêu chí đánh giá")
        explanation.append("   Danh sách tiêu chí:")
        
        total_max_points = 0
        for i, condition in enumerate(condition_items, 1):
            total_max_points += condition.condition_point
            explanation.append(f"   {i}. {condition.condition_code}:")
            explanation.append(f"      - Yêu cầu tối thiểu: {condition.condition_min_value}")
            explanation.append(f"      - Điểm nếu đạt: {condition.condition_point}")
        
        explanation.append(f"   📊 Tổng điểm tối đa có thể đạt: {total_max_points}")
        explanation.append("")
        
        # STEP 3: Audit Results
        explanation.append("STEP 3: LẤY KẾT QUẢ AUDIT (Get Audit Results)")
        explanation.append("-" * 50)
        
        audit_results = self.repo.get_audit_results(yyyymm, customer_code)
        audit_dict = {audit.condition_code: audit for audit in audit_results}
        
        explanation.append(f"✅ RESULT: Tìm thấy kết quả audit cho {len(audit_dict)} tiêu chí")
        explanation.append("   Kết quả audit:")
        
        for condition_code, audit in audit_dict.items():
            explanation.append(f"   - {condition_code}: {audit.value}")
            if audit.audit_date:
                explanation.append(f"     (Audit date: {audit.audit_date.strftime('%Y-%m-%d %H:%M')})")
        explanation.append("")
        
        # STEP 4: Comparison & Calculation
        explanation.append("STEP 4: SO SÁNH & TÍNH ĐIỂM (Compare & Calculate Points)")
        explanation.append("-" * 50)
        
        total_points = 0
        failed_conditions = []
        
        for i, condition in enumerate(condition_items, 1):
            explanation.append(f"   {i}. Đánh giá tiêu chí: {condition.condition_code}")
            
            audit_result = audit_dict.get(condition.condition_code)
            if not audit_result:
                explanation.append(f"      ❌ KHÔNG có kết quả audit")
                explanation.append(f"      → Thất bại: {condition.condition_code}_NOT_AUDITED")
                failed_conditions.append(f"{condition.condition_code}_NOT_AUDITED")
                continue
            
            actual_value = audit_result.numeric_value
            explanation.append(f"      📊 Giá trị thực tế: {actual_value}")
            explanation.append(f"      📊 Yêu cầu tối thiểu: {condition.condition_min_value}")
            
            if condition.meets_minimum(actual_value):
                total_points += condition.condition_point
                explanation.append(f"      ✅ ĐẠT yêu cầu → +{condition.condition_point} điểm")
            else:
                failure_reason = f"{condition.condition_code}_BELOW_MINIMUM({actual_value}<{condition.condition_min_value})"
                failed_conditions.append(failure_reason)
                explanation.append(f"      ❌ KHÔNG ĐẠT yêu cầu → 0 điểm")
                explanation.append(f"      → Thất bại: {failure_reason}")
        
        explanation.append("")
        explanation.append(f"📊 TỔNG KẾT ĐIỂM: {total_points}/{total_max_points}")
        success_rate = (total_points / total_max_points * 100) if total_max_points > 0 else 0
        explanation.append(f"📊 TỶ LỆ THÀNH CÔNG: {success_rate:.1f}%")
        explanation.append("")
        
        # STEP 5: Final Determination
        explanation.append("STEP 5: XÁC ĐỊNH KẾT QUẢ CUỐI CÙNG (Final Determination)")
        explanation.append("-" * 50)
        
        meets_criteria = len(failed_conditions) == 0
        
        explanation.append(f"🎯 Đạt tất cả tiêu chí: {'CÓ' if meets_criteria else 'KHÔNG'}")
        explanation.append(f"🎯 Đăng ký active: {'CÓ' if program_registration.is_active else 'KHÔNG'}")
        
        is_eligible = meets_criteria and program_registration.is_active
        
        explanation.append("")
        explanation.append("🏆 KẾT QUẢ CUỐI CÙNG:")
        if is_eligible:
            explanation.append("   ✅ CUSTOMER ĐỦ ĐIỀU KIỆN NHẬN THƯỞNG")
            explanation.append("   🎉 Sẽ được tính hoa hồng cho tháng này")
        else:
            explanation.append("   ❌ CUSTOMER KHÔNG ĐỦ ĐIỀU KIỆN NHẬN THƯỞNG")
            if not program_registration.is_active:
                explanation.append("   📋 Lý do: Đăng ký không active")
            else:
                explanation.append("   📋 Lý do: Không đạt tiêu chí")
                explanation.append("   📋 Chi tiết thất bại:")
                for failure in failed_conditions:
                    explanation.append(f"      • {failure}")
        
        explanation.append("")
        explanation.append("=" * 80)
        
        return "\n".join(explanation)
