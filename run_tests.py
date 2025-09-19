"""
Test runner script for Display Program Management System
Script chạy test cho Hệ thống Quản lý Chương trình Trưng bày
Created: 2025-09-19

Script này chạy tất cả test cases và tạo báo cáo coverage.
Hỗ trợ chạy test theo module hoặc chạy tất cả cùng lúc.
"""

import unittest
import sys
import os
from io import StringIO
import time
from datetime import datetime


class ColoredTestResult(unittest.TextTestResult):
    """Custom test result với màu sắc để dễ đọc hơn"""
    
    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.success_count = 0
    
    def addSuccess(self, test):
        super().addSuccess(test)
        self.success_count += 1
        if self.verbosity > 1:
            self.stream.write("✅ ")
            self.stream.write(str(test))
            self.stream.write(" ... OK\n")
    
    def addError(self, test, err):
        super().addError(test, err)
        if self.verbosity > 1:
            self.stream.write("❌ ")
            self.stream.write(str(test))
            self.stream.write(" ... ERROR\n")
    
    def addFailure(self, test, err):
        super().addFailure(test, err)
        if self.verbosity > 1:
            self.stream.write("❌ ")
            self.stream.write(str(test))
            self.stream.write(" ... FAIL\n")
    
    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        if self.verbosity > 1:
            self.stream.write("⏭️ ")
            self.stream.write(str(test))
            self.stream.write(f" ... SKIP ({reason})\n")


class ColoredTestRunner(unittest.TextTestRunner):
    """Custom test runner với màu sắc"""
    
    def __init__(self, **kwargs):
        kwargs['resultclass'] = ColoredTestResult
        super().__init__(**kwargs)
    
    def run(self, test):
        """Chạy test với thời gian và thống kê"""
        print("=" * 70)
        print("🧪 DISPLAY PROGRAM MANAGEMENT SYSTEM - TEST SUITE")
        print("   Bộ test cho Hệ thống Quản lý Chương trình Trưng bày")
        print("=" * 70)
        print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        start_time = time.time()
        result = super().run(test)
        end_time = time.time()
        
        # Tính toán thống kê
        total_tests = result.testsRun
        success_count = getattr(result, 'success_count', 0)
        error_count = len(result.errors)
        failure_count = len(result.failures)
        skip_count = len(result.skipped)
        
        duration = end_time - start_time
        
        print("\n" + "=" * 70)
        print("📊 TEST SUMMARY - TÓM TẮT KẾT QUẢ TEST")
        print("=" * 70)
        print(f"⏱️  Duration: {duration:.2f} seconds")
        print(f"🧪 Total tests: {total_tests}")
        print(f"✅ Passed: {success_count}")
        print(f"❌ Failed: {failure_count}")
        print(f"💥 Errors: {error_count}")
        print(f"⏭️  Skipped: {skip_count}")
        
        # Tính success rate
        if total_tests > 0:
            success_rate = (success_count / total_tests) * 100
            print(f"📈 Success rate: {success_rate:.1f}%")
            
            if success_rate == 100:
                print("🎉 ALL TESTS PASSED! - TẤT CẢ TEST THÀNH CÔNG!")
            elif success_rate >= 80:
                print("⚠️  MOSTLY PASSED - PHẦN LỚN THÀNH CÔNG")
            else:
                print("🚨 MANY FAILURES - NHIỀU TEST THẤT BẠI")
        
        print("=" * 70)
        
        # In chi tiết lỗi nếu có
        if result.errors:
            print("\n💥 ERRORS - CHI TIẾT LỖI:")
            for test, error in result.errors:
                print(f"\n❌ {test}:")
                print(error)
        
        if result.failures:
            print("\n❌ FAILURES - CHI TIẾT THẤT BẠI:")
            for test, failure in result.failures:
                print(f"\n❌ {test}:")
                print(failure)
        
        return result


def discover_tests(pattern='test_*.py'):
    """
    Tìm và load tất cả test cases
    
    Args:
        pattern: Pattern để tìm test files
        
    Returns:
        TestSuite: Test suite chứa tất cả tests
    """
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(start_dir, pattern=pattern)
    return suite


def run_specific_test_module(module_name):
    """
    Chạy test cho một module cụ thể
    
    Args:
        module_name: Tên module test (ví dụ: 'test_models')
    """
    try:
        # Import module
        module = __import__(module_name)
        
        # Load tests từ module
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromModule(module)
        
        # Chạy tests
        runner = ColoredTestRunner(verbosity=2)
        result = runner.run(suite)
        
        return result.wasSuccessful()
        
    except ImportError as e:
        print(f"❌ Cannot import test module '{module_name}': {e}")
        return False
    except Exception as e:
        print(f"❌ Error running tests for '{module_name}': {e}")
        return False


def run_all_tests():
    """Chạy tất cả test cases"""
    try:
        # Discover tất cả test files
        suite = discover_tests()
        
        # Chạy tests
        runner = ColoredTestRunner(verbosity=2)
        result = runner.run(suite)
        
        return result.wasSuccessful()
        
    except Exception as e:
        print(f"❌ Error running all tests: {e}")
        return False


def check_test_coverage():
    """
    Kiểm tra coverage của test cases
    Yêu cầu cài đặt: pip install coverage
    """
    try:
        import coverage
        print("\n📊 CHECKING TEST COVERAGE - KIỂM TRA ĐỘ BAO PHỦ TEST")
        print("=" * 50)
        
        # Tạo coverage instance
        cov = coverage.Coverage()
        cov.start()
        
        # Chạy tests
        suite = discover_tests()
        runner = unittest.TextTestRunner(verbosity=0, stream=StringIO())
        runner.run(suite)
        
        # Dừng coverage và tạo report
        cov.stop()
        cov.save()
        
        print("Coverage report:")
        cov.report(show_missing=True)
        
    except ImportError:
        print("⚠️  Coverage module not installed. Install with: pip install coverage")
    except Exception as e:
        print(f"❌ Error checking coverage: {e}")


def main():
    """Main function để chạy tests"""
    if len(sys.argv) > 1:
        # Chạy test cho module cụ thể
        module_name = sys.argv[1]
        
        if module_name == '--coverage':
            check_test_coverage()
        elif module_name == '--help':
            print_help()
        else:
            print(f"🎯 Running tests for module: {module_name}")
            success = run_specific_test_module(module_name)
            sys.exit(0 if success else 1)
    else:
        # Chạy tất cả tests
        print("🎯 Running all tests...")
        success = run_all_tests()
        
        # Kiểm tra coverage nếu có thể
        check_test_coverage()
        
        sys.exit(0 if success else 1)


def print_help():
    """In hướng dẫn sử dụng"""
    help_text = """
🧪 DISPLAY PROGRAM MANAGEMENT SYSTEM - TEST RUNNER
   Test Runner cho Hệ thống Quản lý Chương trình Trưng bày

Usage:
    python run_tests.py                    # Chạy tất cả tests
    python run_tests.py test_models        # Chạy tests cho models.py
    python run_tests.py test_database      # Chạy tests cho database.py
    python run_tests.py --coverage        # Chỉ kiểm tra coverage
    python run_tests.py --help            # Hiển thị help

Available test modules:
    - test_models: Test cho data models và business objects
    - test_database: Test cho database operations và repository
    - test_business_logic: Test cho business logic và evaluation
    - test_main: Test cho main application và CLI

Examples:
    # Chạy tất cả tests với báo cáo chi tiết
    python run_tests.py

    # Chạy chỉ tests cho models
    python run_tests.py test_models

    # Kiểm tra test coverage
    python run_tests.py --coverage

Requirements:
    - Python 3.8+
    - unittest (built-in)
    - coverage (optional, for coverage reports)

Note:
    - Một số tests cần SQL Server connection để chạy đầy đủ
    - Mock tests sẽ chạy mà không cần database thực
    - Sử dụng --coverage để kiểm tra độ bao phủ test
"""
    print(help_text)


if __name__ == '__main__':
    main()
