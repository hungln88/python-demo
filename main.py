"""
Main application for Display Program Management System
Created: 2025-09-19
"""

import sys
import json
from datetime import datetime
from typing import Optional

from database import DatabaseConnection, DisplayProgramRepository
from business_logic import DisplayProgramService
from models import Register, RegisterItem, AuditPicture, ConditionGroup, ConditionItem


class DisplayProgramApp:
    """Main application class"""
    
    def __init__(self):
        # Initialize database connection
        self.db_conn = DatabaseConnection()
        self.repo = DisplayProgramRepository(self.db_conn)
        self.service = DisplayProgramService(self.repo)
        
        # Test connection
        if not self.db_conn.test_connection():
            print("❌ Failed to connect to database. Please check your SQL Server connection.")
            print("Make sure SQL Server is running and DisplayProgramDB exists.")
            sys.exit(1)
        else:
            print("✅ Database connection successful!")
    
    def print_banner(self):
        """Print application banner"""
        print("=" * 60)
        print("    DISPLAY PROGRAM MANAGEMENT SYSTEM")
        print("    Hệ thống quản lý chương trình trưng bày")
        print("=" * 60)
        print()
    
    def print_menu(self):
        """Print main menu"""
        print("\n📋 MAIN MENU - MENU CHÍNH:")
        print("1. 📊 View Program Summary (Xem tóm tắt chương trình)")
        print("2. 👤 View Customer Summary (Xem tóm tắt khách hàng)")
        print("3. 🎯 Check Eligible Customers (Kiểm tra khách hàng đủ điều kiện)")
        print("4. ❌ Check Failed Customers (Kiểm tra khách hàng không đạt)")
        print("5. 📈 Monthly Report (Báo cáo tháng)")
        print("6. 📝 Add Registration (Thêm đăng ký)")
        print("7. 🔍 Add Audit Result (Thêm kết quả kiểm tra)")
        print("8. 📋 View Database Statistics (Xem thống kê database)")
        print("9. 🧪 Run Test Scenarios (Chạy test scenarios)")
        print("0. ❌ Exit (Thoát)")
        print("-" * 40)
    
    def get_month_input(self) -> int:
        """Get month input from user"""
        while True:
            try:
                month_str = input("Enter month (YYYYMM format, e.g., 202509): ").strip()
                if len(month_str) != 6:
                    raise ValueError("Month must be in YYYYMM format")
                month = int(month_str)
                if month < 202301 or month > 209912:
                    raise ValueError("Month must be reasonable (202301-209912)")
                return month
            except ValueError as e:
                print(f"❌ Invalid input: {e}")
    
    def view_program_summary(self):
        """View program summary"""
        print("\n📊 PROGRAM SUMMARY")
        yyyymm = self.get_month_input()
        program_code = input("Enter program code (or press Enter for all): ").strip() or None
        
        if program_code:
            summary = self.service.generate_program_summary(yyyymm, program_code)
            self.print_program_summary(summary)
        else:
            # Show all programs
            registrations = self.repo.get_registrations(yyyymm, active_only=True)
            programs = list(set(r.program_code for r in registrations))
            
            if not programs:
                print("❌ No active programs found for this month")
                return
            
            for program in programs:
                summary = self.service.generate_program_summary(yyyymm, program)
                self.print_program_summary(summary)
                print("-" * 40)
    
    def print_program_summary(self, summary):
        """Print program summary"""
        print(f"\n🎯 Program: {summary['program_code']} ({summary['yyyymm']})")
        print(f"📊 Total Customers: {summary['total_customers']}")
        print(f"✅ Eligible: {summary['eligible_customers']}")
        print(f"❌ Failed: {summary['failed_customers']}")
        print(f"⏸️  Inactive: {summary['inactive_customers']}")
        print(f"📈 Success Rate: {summary['success_rate']:.1f}%")
        
        if summary['common_failures']:
            print("\n🔍 Common Failures:")
            for failure, count in summary['common_failures'].items():
                print(f"  • {failure}: {count} customers")
    
    def view_customer_summary(self):
        """View customer summary"""
        print("\n👤 CUSTOMER SUMMARY")
        yyyymm = self.get_month_input()
        customer_code = input("Enter customer code: ").strip()
        
        if not customer_code:
            print("❌ Customer code is required")
            return
        
        summary = self.service.generate_customer_summary(yyyymm, customer_code)
        self.print_customer_summary(summary)
    
    def print_customer_summary(self, summary):
        """Print customer summary"""
        print(f"\n👤 Customer: {summary['customer_code']} ({summary['yyyymm']})")
        print(f"📊 Total Programs: {summary['total_programs']}")
        print(f"✅ Eligible Programs: {summary['eligible_programs']}")
        print(f"❌ Failed Programs: {summary['failed_programs']}")
        print(f"🎯 Total Points: {summary['total_points']}/{summary['max_possible_points']}")
        print(f"📈 Overall Success Rate: {summary['overall_success_rate']:.1f}%")
        
        print("\n📋 Program Details:")
        for result in summary['program_details']:
            status = "✅" if result.is_eligible_for_reward else "❌"
            print(f"  {status} {result.program_code}: {result.total_points}/{result.max_possible_points} points")
            if result.failed_conditions:
                print(f"    Failures: {', '.join(result.failed_conditions)}")
    
    def check_eligible_customers(self):
        """Check eligible customers"""
        print("\n🎯 ELIGIBLE CUSTOMERS")
        yyyymm = self.get_month_input()
        program_code = input("Enter program code (or press Enter for all): ").strip() or None
        
        eligible = self.service.get_eligible_customers_for_rewards(yyyymm, program_code)
        
        if not eligible:
            print("❌ No eligible customers found")
            return
        
        print(f"\n✅ Found {len(eligible)} eligible customers:")
        for result in eligible:
            print(f"  • {result.customer_code} - {result.program_code}: "
                  f"{result.total_points}/{result.max_possible_points} points "
                  f"({result.success_rate:.1f}%)")
    
    def check_failed_customers(self):
        """Check failed customers"""
        print("\n❌ FAILED CUSTOMERS")
        yyyymm = self.get_month_input()
        program_code = input("Enter program code (or press Enter for all): ").strip() or None
        
        failed = self.service.get_failed_customers(yyyymm, program_code)
        
        if not failed:
            print("✅ No failed customers found")
            return
        
        print(f"\n❌ Found {len(failed)} failed customers:")
        for result in failed:
            print(f"  • {result.customer_code} - {result.program_code}: "
                  f"{result.total_points}/{result.max_possible_points} points")
            print(f"    Failures: {', '.join(result.failed_conditions)}")
    
    def monthly_report(self):
        """Generate monthly report"""
        print("\n📈 MONTHLY REPORT")
        yyyymm = self.get_month_input()
        
        print("⏳ Generating report...")
        report = self.service.generate_monthly_report(yyyymm)
        
        print(f"\n📊 Monthly Report for {yyyymm}")
        print("=" * 40)
        
        stats = report['basic_stats']
        print(f"📋 Basic Statistics:")
        print(f"  • Total Programs: {stats['total_programs']}")
        print(f"  • Total Customers: {stats['total_customers']}")
        print(f"  • Active Customers: {stats['active_customers']}")
        print(f"  • Audited Customers: {stats['audited_customers']}")
        
        print(f"\n🎯 Evaluation Results:")
        print(f"  • Total Evaluations: {report['total_evaluations']}")
        print(f"  • Eligible for Rewards: {report['total_eligible_for_rewards']}")
        print(f"  • Failed Criteria: {report['total_failed_criteria']}")
        print(f"  • Success Rate: {report['overall_success_rate']:.1f}%")
        
        print(f"\n📊 Program Summaries:")
        for program, summary in report['program_summaries'].items():
            print(f"  🎯 {program}: {summary['eligible_customers']}/{summary['total_customers']} eligible "
                  f"({summary['success_rate']:.1f}%)")
    
    def add_registration(self):
        """Add new registration"""
        print("\n📝 ADD REGISTRATION")
        
        try:
            yyyymm = self.get_month_input()
            program_code = input("Program code: ").strip()
            customer_code = input("Customer code: ").strip()
            display_type = input("Display type (KE_3_O, KE_4_O, KE_TRUONG_BAY): ").strip()
            register_qty = int(input("Quantity: ").strip())
            status_input = input("Status (active/inactive): ").strip().lower()
            status = status_input in ['active', 'true', '1', 'yes']
            
            registration = Register(
                yyyymm=yyyymm,
                program_code=program_code,
                customer_code=customer_code,
                display_type=display_type,
                register_qty=register_qty,
                status=status
            )
            
            # Validate registration
            is_valid, errors = self.service.validate_registration(registration)
            if not is_valid:
                print("❌ Registration validation failed:")
                for error in errors:
                    print(f"  • {error}")
                return
            
            # Insert registration
            if self.repo.insert_registration(registration):
                print("✅ Registration added successfully!")
            else:
                print("❌ Failed to add registration")
                
        except ValueError as e:
            print(f"❌ Invalid input: {e}")
    
    def add_audit_result(self):
        """Add audit result"""
        print("\n🔍 ADD AUDIT RESULT")
        
        try:
            yyyymm = self.get_month_input()
            customer_code = input("Customer code: ").strip()
            condition_code = input("Condition code (CLEANLINESS, PRODUCT_AVAILABILITY, DISPLAY_QUALITY): ").strip()
            value = input("Value (0-100): ").strip()
            
            audit = AuditPicture(
                yyyymm=yyyymm,
                customer_code=customer_code,
                condition_code=condition_code,
                value=value,
                audit_date=datetime.now()
            )
            
            if self.repo.insert_audit_result(audit):
                print("✅ Audit result added successfully!")
            else:
                print("❌ Failed to add audit result")
                
        except ValueError as e:
            print(f"❌ Invalid input: {e}")
    
    def view_database_statistics(self):
        """View database statistics"""
        print("\n📋 DATABASE STATISTICS")
        
        try:
            yyyymm = self.get_month_input()
            stats = self.repo.get_monthly_statistics(yyyymm)
            
            print(f"\n📊 Statistics for {yyyymm}:")
            print(f"  • Total Programs: {stats['total_programs']}")
            print(f"  • Total Customers: {stats['total_customers']}")
            print(f"  • Active Customers: {stats['active_customers']}")
            print(f"  • Audited Customers: {stats['audited_customers']}")
            
        except Exception as e:
            print(f"❌ Error retrieving statistics: {e}")
    
    def run_test_scenarios(self):
        """Run test scenarios with sample data"""
        print("\n🧪 RUNNING TEST SCENARIOS")
        print("Using sample data from month 202509...")
        
        yyyymm = 202509
        
        print("\n1. Testing Program Summary for PROG001:")
        summary = self.service.generate_program_summary(yyyymm, 'PROG001')
        self.print_program_summary(summary)
        
        print("\n2. Testing Customer Summary for CUST001:")
        customer_summary = self.service.generate_customer_summary(yyyymm, 'CUST001')
        self.print_customer_summary(customer_summary)
        
        print("\n3. Testing Eligible Customers:")
        eligible = self.service.get_eligible_customers_for_rewards(yyyymm, 'PROG001')
        print(f"Found {len(eligible)} eligible customers for PROG001")
        for result in eligible:
            print(f"  ✅ {result.customer_code}: {result.total_points}/{result.max_possible_points} points")
        
        print("\n4. Testing Failed Customers:")
        failed = self.service.get_failed_customers(yyyymm, 'PROG002')
        print(f"Found {len(failed)} failed customers for PROG002")
        for result in failed:
            print(f"  ❌ {result.customer_code}: {', '.join(result.failed_conditions)}")
        
        print("\n✅ Test scenarios completed!")
    
    def run(self):
        """Main application loop"""
        self.print_banner()
        
        while True:
            self.print_menu()
            
            try:
                choice = input("Enter your choice (0-9): ").strip()
                
                if choice == '0':
                    print("👋 Goodbye! Tạm biệt!")
                    break
                elif choice == '1':
                    self.view_program_summary()
                elif choice == '2':
                    self.view_customer_summary()
                elif choice == '3':
                    self.check_eligible_customers()
                elif choice == '4':
                    self.check_failed_customers()
                elif choice == '5':
                    self.monthly_report()
                elif choice == '6':
                    self.add_registration()
                elif choice == '7':
                    self.add_audit_result()
                elif choice == '8':
                    self.view_database_statistics()
                elif choice == '9':
                    self.run_test_scenarios()
                else:
                    print("❌ Invalid choice. Please try again.")
                
                input("\nPress Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye! Tạm biệt!")
                break
            except Exception as e:
                print(f"❌ An error occurred: {e}")
                input("Press Enter to continue...")


if __name__ == "__main__":
    app = DisplayProgramApp()
    app.run()
