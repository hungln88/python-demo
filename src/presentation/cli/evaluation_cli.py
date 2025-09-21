"""
Evaluation CLI - Command Line Interface for Evaluation
CLI Đánh giá - Giao diện dòng lệnh cho đánh giá
"""

import sys
from typing import Optional
from application.use_cases.evaluate_customer_use_case import EvaluateCustomerUseCase
from domain.services.evaluation_service import EvaluationService


class EvaluationCLI:
    """
    Evaluation CLI - Giao diện dòng lệnh cho việc đánh giá khách hàng
    
    CLI này cung cấp interface đơn giản để thực hiện đánh giá khách hàng
    thông qua command line.
    """
    
    def __init__(self, evaluation_use_case: EvaluateCustomerUseCase):
        """
        Khởi tạo Evaluation CLI
        
        Args:
            evaluation_use_case (EvaluateCustomerUseCase): Use case đánh giá khách hàng
        """
        self.evaluation_use_case = evaluation_use_case
    
    def run_interactive(self):
        """
        Chạy CLI ở chế độ tương tác
        """
        print("=" * 60)
        print("🔍 DISPLAY PROGRAM EVALUATION CLI")
        print("=" * 60)
        print("Giao diện đánh giá chương trình trưng bày")
        print()
        
        while True:
            try:
                print("Nhập thông tin đánh giá:")
                print("-" * 40)
                
                # Nhập tháng/năm
                yyyymm_input = input("Tháng/năm (YYYYMM, ví dụ: 202509): ").strip()
                if not yyyymm_input:
                    print("❌ Tháng/năm không được để trống!")
                    continue
                
                try:
                    yyyymm = int(yyyymm_input)
                except ValueError:
                    print("❌ Định dạng tháng/năm không hợp lệ!")
                    continue
                
                # Nhập mã khách hàng
                customer_code = input("Mã khách hàng: ").strip()
                if not customer_code:
                    print("❌ Mã khách hàng không được để trống!")
                    continue
                
                # Nhập mã chương trình
                program_code = input("Mã chương trình: ").strip()
                if not program_code:
                    print("❌ Mã chương trình không được để trống!")
                    continue
                
                print()
                print("🔄 Đang thực hiện đánh giá...")
                print("-" * 40)
                
                # Thực hiện đánh giá
                result = self.evaluation_use_case.execute_with_validation(
                    yyyymm, customer_code, program_code
                )
                
                # Hiển thị kết quả
                self._display_result(result)
                
                print()
                choice = input("Tiếp tục đánh giá? (y/n): ").strip().lower()
                if choice not in ['y', 'yes', 'có', 'c']:
                    break
                
                print()
                
            except KeyboardInterrupt:
                print("\n\n👋 Tạm biệt!")
                break
            except Exception as e:
                print(f"❌ Lỗi: {e}")
                print()
        
        print("👋 Cảm ơn bạn đã sử dụng hệ thống!")
    
    def run_single_evaluation(
        self, 
        yyyymm: int, 
        customer_code: str, 
        program_code: str
    ) -> dict:
        """
        Chạy đánh giá đơn lẻ
        
        Args:
            yyyymm (int): Tháng/năm
            customer_code (str): Mã khách hàng
            program_code (str): Mã chương trình
            
        Returns:
            dict: Kết quả đánh giá
        """
        print(f"🔍 Đánh giá khách hàng {customer_code} - Chương trình {program_code} - Tháng {yyyymm}")
        print("=" * 70)
        
        result = self.evaluation_use_case.execute_with_validation(
            yyyymm, customer_code, program_code
        )
        
        self._display_result(result)
        return result
    
    def _display_result(self, result: dict):
        """
        Hiển thị kết quả đánh giá
        
        Args:
            result (dict): Kết quả đánh giá
        """
        if not result.get("success", False):
            print(f"❌ Lỗi: {result.get('error', 'Unknown error')}")
            print(f"📝 Chi tiết: {result.get('message', 'No details')}")
            return
        
        data = result["data"]
        
        print("📊 KẾT QUẢ ĐÁNH GIÁ:")
        print("-" * 40)
        print(f"👤 Khách hàng: {data['customer_code']}")
        print(f"📋 Chương trình: {data['program_code']}")
        print(f"📅 Tháng: {data['yyyymm']}")
        print()
        
        print("📈 ĐIỂM SỐ:")
        print(f"  • Tổng điểm: {data['total_points']}/{data['max_possible_points']}")
        print(f"  • Tỷ lệ thành công: {data['success_rate']:.1f}%")
        print()
        
        print("✅ TRẠNG THÁI:")
        status_icon = "✅" if data['meets_criteria'] else "❌"
        print(f"  • Đạt tiêu chí: {status_icon} {'CÓ' if data['meets_criteria'] else 'KHÔNG'}")
        
        reg_icon = "✅" if data['registration_status'] else "❌"
        print(f"  • Đăng ký active: {reg_icon} {'CÓ' if data['registration_status'] else 'KHÔNG'}")
        
        reward_icon = "🏆" if data['is_eligible_for_reward'] else "🚫"
        print(f"  • Đủ điều kiện nhận thưởng: {reward_icon} {'CÓ' if data['is_eligible_for_reward'] else 'KHÔNG'}")
        print()
        
        if data['failed_conditions']:
            print("❌ CÁC ĐIỀU KIỆN KHÔNG ĐẠT:")
            for condition in data['failed_conditions']:
                print(f"  • {condition}")
            print()
        
        print(f"📝 Tóm tắt: {data['failure_summary']}")
    
    def run_batch_evaluation(self, evaluations: list):
        """
        Chạy đánh giá hàng loạt
        
        Args:
            evaluations (list): Danh sách các đánh giá cần thực hiện
        """
        print("🔄 ĐÁNH GIÁ HÀNG LOẠT")
        print("=" * 50)
        print(f"📊 Tổng số đánh giá: {len(evaluations)}")
        print()
        
        results = []
        for i, eval_data in enumerate(evaluations, 1):
            print(f"[{i}/{len(evaluations)}] Đang đánh giá {eval_data['customer_code']}...")
            
            result = self.evaluation_use_case.execute_with_validation(
                eval_data['yyyymm'],
                eval_data['customer_code'],
                eval_data['program_code']
            )
            
            results.append(result)
            
            if result.get("success", False):
                data = result["data"]
                status = "✅ PASS" if data['is_eligible_for_reward'] else "❌ FAIL"
                print(f"    {status} - {data['total_points']}/{data['max_possible_points']} điểm")
            else:
                print(f"    ❌ ERROR - {result.get('message', 'Unknown error')}")
        
        print()
        print("📊 TỔNG KẾT:")
        print("-" * 30)
        
        successful = sum(1 for r in results if r.get("success", False))
        eligible = sum(1 for r in results if r.get("success", False) and r["data"]["is_eligible_for_reward"])
        
        print(f"✅ Thành công: {successful}/{len(evaluations)}")
        print(f"🏆 Đủ điều kiện: {eligible}/{len(evaluations)}")
        print(f"📈 Tỷ lệ thành công: {(successful/len(evaluations)*100):.1f}%")
        print(f"🏆 Tỷ lệ đủ điều kiện: {(eligible/len(evaluations)*100):.1f}%")
        
        return results
