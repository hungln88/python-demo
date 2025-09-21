"""
Evaluate Customer Use Case - Application Business Logic
Use Case Đánh giá Khách hàng - Logic nghiệp vụ ứng dụng
"""

from typing import Optional
from domain.services.evaluation_service import EvaluationService
from domain.entities.evaluation import CustomerEvaluationResult


class EvaluateCustomerUseCase:
    """
    Use Case: Đánh giá khách hàng có đủ điều kiện nhận thưởng
    
    Use case này đóng gói logic đánh giá khách hàng và cung cấp
    interface đơn giản cho presentation layer.
    """
    
    def __init__(self, evaluation_service: EvaluationService):
        """
        Khởi tạo Use Case
        
        Args:
            evaluation_service (EvaluationService): Service đánh giá
        """
        self.evaluation_service = evaluation_service
    
    def execute(
        self, 
        yyyymm: int, 
        customer_code: str, 
        program_code: str
    ) -> CustomerEvaluationResult:
        """
        Thực hiện đánh giá khách hàng
        
        Args:
            yyyymm (int): Tháng/năm đánh giá (format YYYYMM)
            customer_code (str): Mã khách hàng cần đánh giá
            program_code (str): Mã chương trình cần đánh giá
        
        Returns:
            CustomerEvaluationResult: Kết quả đánh giá chi tiết
        
        Raises:
            ValueError: Nếu tham số đầu vào không hợp lệ
        """
        # Validation
        if not customer_code or not customer_code.strip():
            raise ValueError("Customer code cannot be empty")
        
        if not program_code or not program_code.strip():
            raise ValueError("Program code cannot be empty")
        
        if yyyymm < 202001 or yyyymm > 999912:
            raise ValueError("Invalid year-month format. Expected YYYYMM")
        
        # Execute evaluation
        return self.evaluation_service.evaluate_customer(
            yyyymm, customer_code.strip(), program_code.strip()
        )
    
    def execute_with_validation(
        self, 
        yyyymm: int, 
        customer_code: str, 
        program_code: str
    ) -> dict:
        """
        Thực hiện đánh giá khách hàng và trả về kết quả dạng dictionary
        
        Args:
            yyyymm (int): Tháng/năm đánh giá (format YYYYMM)
            customer_code (str): Mã khách hàng cần đánh giá
            program_code (str): Mã chương trình cần đánh giá
        
        Returns:
            dict: Kết quả đánh giá dạng dictionary
        """
        try:
            result = self.execute(yyyymm, customer_code, program_code)
            
            return {
                "success": True,
                "data": {
                    "yyyymm": result.yyyymm,
                    "customer_code": result.customer_code,
                    "program_code": result.program_code,
                    "total_points": result.total_points,
                    "max_possible_points": result.max_possible_points,
                    "success_rate": result.success_rate,
                    "meets_criteria": result.meets_criteria,
                    "registration_status": result.registration_status,
                    "is_eligible_for_reward": result.is_eligible_for_reward,
                    "failed_conditions": result.failed_conditions,
                    "failure_summary": result.get_failure_summary()
                }
            }
        except ValueError as e:
            return {
                "success": False,
                "error": "Validation Error",
                "message": str(e)
            }
        except Exception as e:
            return {
                "success": False,
                "error": "System Error",
                "message": str(e)
            }
