"""
Evaluation Service - Domain Business Logic
Dịch vụ Đánh giá - Logic nghiệp vụ Domain
"""

from typing import List, Optional
from domain.entities.evaluation import ConditionGroup, ConditionItem, AuditPicture, CustomerEvaluationResult
from domain.repositories.evaluation_repository import EvaluationRepository
from domain.repositories.registration_repository import RegistrationRepository
from domain.repositories.program_repository import ProgramRepository


class EvaluationService:
    """
    Evaluation Service - Xử lý logic đánh giá khách hàng
    
    Service này chứa logic nghiệp vụ chính cho việc đánh giá khách hàng
    có đủ điều kiện nhận thưởng hay không.
    """
    
    def __init__(
        self,
        evaluation_repo: EvaluationRepository,
        registration_repo: RegistrationRepository,
        program_repo: ProgramRepository
    ):
        """
        Khởi tạo Evaluation Service
        
        Args:
            evaluation_repo (EvaluationRepository): Repository cho dữ liệu đánh giá
            registration_repo (RegistrationRepository): Repository cho dữ liệu đăng ký
            program_repo (ProgramRepository): Repository cho dữ liệu chương trình
        """
        self.evaluation_repo = evaluation_repo
        self.registration_repo = registration_repo
        self.program_repo = program_repo
    
    def evaluate_customer(
        self, 
        yyyymm: int, 
        customer_code: str, 
        program_code: str
    ) -> CustomerEvaluationResult:
        """
        Đánh giá khách hàng có đủ điều kiện nhận thưởng hay không
        
        Args:
            yyyymm (int): Tháng/năm đánh giá (format YYYYMM)
            customer_code (str): Mã khách hàng cần đánh giá
            program_code (str): Mã chương trình cần đánh giá
        
        Returns:
            CustomerEvaluationResult: Kết quả đánh giá chi tiết
        """
        # Step 1: Kiểm tra đăng ký
        registrations = self.registration_repo.get_registrations(
            yyyymm, customer_code, active_only=False
        )
        
        program_registration = next(
            (r for r in registrations if r.program_code == program_code), 
            None
        )
        
        if not program_registration:
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
        
        # Step 2: Lấy cấu hình chương trình
        register_item = self.program_repo.get_register_item(
            yyyymm, program_code, program_registration.display_type
        )
        
        if not register_item:
            return CustomerEvaluationResult(
                yyyymm=yyyymm,
                customer_code=customer_code,
                program_code=program_code,
                total_points=0,
                max_possible_points=0,
                meets_criteria=False,
                failed_conditions=["NO_REGISTER_ITEM_FOUND"],
                registration_status=program_registration.is_active
            )
        
        # Step 3: Lấy condition groups
        condition_groups = self.evaluation_repo.get_condition_groups(
            yyyymm, program_code, register_item.type_code
        )
        
        if not condition_groups:
            return CustomerEvaluationResult(
                yyyymm=yyyymm,
                customer_code=customer_code,
                program_code=program_code,
                total_points=0,
                max_possible_points=0,
                meets_criteria=False,
                failed_conditions=["NO_CONDITION_GROUPS_DEFINED"],
                registration_status=program_registration.is_active
            )
        
        # Step 4: Lấy kết quả audit
        audit_results = self.evaluation_repo.get_audit_results(yyyymm, customer_code)
        audit_dict = {audit.condition_code: audit for audit in audit_results}
        
        # Step 5: Đánh giá theo từng group
        total_points = 0
        max_possible_points = 0
        failed_conditions = []
        all_groups_passed = True
        
        for group in condition_groups:
            group_items = self.evaluation_repo.get_condition_items_by_group(
                yyyymm, program_code, group.group
            )
            
            if not group_items:
                failed_conditions.append(f"GROUP_{group.group}_NO_ITEMS")
                all_groups_passed = False
                continue
            
            group_score = 0
            group_max_points = 0
            
            for item in group_items:
                group_max_points += item.condition_point
                max_possible_points += item.condition_point
                
                audit_result = audit_dict.get(item.condition_code)
                if not audit_result:
                    failure_reason = f"{item.condition_code}_NOT_AUDITED"
                    failed_conditions.append(failure_reason)
                    continue
                
                actual_value = audit_result.numeric_value
                
                if item.meets_minimum(actual_value):
                    group_score += item.condition_point
                    total_points += item.condition_point
                else:
                    failure_reason = f"{item.condition_code}_BELOW_MINIMUM({actual_value}<{item.condition_min_value})"
                    failed_conditions.append(failure_reason)
            
            if group_score < group.group_point:
                all_groups_passed = False
                failed_conditions.append(f"GROUP_{group.group}_INSUFFICIENT_POINTS({group_score}<{group.group_point})")
        
        # Step 6: Xác định kết quả cuối cùng
        meets_criteria = all_groups_passed and len(failed_conditions) == 0
        
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
        
        # Lưu kết quả đánh giá
        self.evaluation_repo.save_evaluation_result(result)
        
        return result
    
    def get_evaluation_result(
        self, 
        yyyymm: int, 
        customer_code: str, 
        program_code: str
    ) -> Optional[CustomerEvaluationResult]:
        """
        Lấy kết quả đánh giá đã lưu
        
        Args:
            yyyymm (int): Tháng năm
            customer_code (str): Mã khách hàng
            program_code (str): Mã chương trình
            
        Returns:
            Optional[CustomerEvaluationResult]: Kết quả đánh giá hoặc None
        """
        return self.evaluation_repo.get_evaluation_result(yyyymm, customer_code, program_code)
    
    def evaluate_all_customers_for_program(
        self, 
        yyyymm: int, 
        program_code: str
    ) -> List[CustomerEvaluationResult]:
        """
        Đánh giá tất cả khách hàng đăng ký một chương trình
        
        Args:
            yyyymm (int): Tháng năm
            program_code (str): Mã chương trình
            
        Returns:
            List[CustomerEvaluationResult]: Danh sách kết quả đánh giá
        """
        customer_codes = self.registration_repo.get_program_customers(yyyymm, program_code)
        results = []
        
        for customer_code in customer_codes:
            result = self.evaluate_customer(yyyymm, customer_code, program_code)
            results.append(result)
        
        return results
    
    def get_eligible_customers(
        self, 
        yyyymm: int, 
        program_code: Optional[str] = None
    ) -> List[CustomerEvaluationResult]:
        """
        Lấy danh sách khách hàng đủ điều kiện nhận thưởng
        
        Args:
            yyyymm (int): Tháng năm
            program_code (Optional[str]): Mã chương trình (optional)
            
        Returns:
            List[CustomerEvaluationResult]: Danh sách khách hàng đủ điều kiện
        """
        if program_code:
            results = self.evaluate_all_customers_for_program(yyyymm, program_code)
        else:
            # Lấy tất cả chương trình và đánh giá
            # Implementation này có thể được tối ưu hóa
            results = []
        
        return [r for r in results if r.is_eligible_for_reward]
