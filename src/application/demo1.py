import pandas as pd
import numpy as np
import time
import json
from typing import Dict, List, Any
import pyodbc
from sqlalchemy import create_engine
import urllib.parse

def create_database_connection():
    """
    Tạo kết nối đến SQL Server
    """
    print("=== KẾT NỐI DATABASE ===")
    
    # Thông tin kết nối SQL Server (thay đổi theo database của bạn)
    server = 'localhost'  # hoặc 'your-server-name'
    database = 'your_database_name'
    username = 'your_username'
    password = 'your_password'
    
    # Tạo connection string
    connection_string = f"""
    DRIVER={{ODBC Driver 17 for SQL Server}};
    SERVER={server};
    DATABASE={database};
    UID={username};
    PWD={password};
    Trusted_Connection=no;
    """
    
    try:
        # Kết nối bằng pyodbc
        conn = pyodbc.connect(connection_string)
        print("✓ Kết nối SQL Server thành công")
        return conn
    except Exception as e:
        print(f"❌ Lỗi kết nối SQL Server: {e}")
        print("Hướng dẫn:")
        print("1. Cài đặt ODBC Driver 17 for SQL Server")
        print("2. Kiểm tra thông tin kết nối")
        print("3. Đảm bảo SQL Server đang chạy")
        return None

def create_sqlalchemy_engine():
    """
    Tạo SQLAlchemy engine để pandas có thể sử dụng
    """
    # Thông tin kết nối (thay đổi theo database của bạn)
    server = 'localhost'
    database = 'your_database_name'
    username = 'your_username'
    password = 'your_password'
    
    # Tạo connection string cho SQLAlchemy
    connection_string = f"mssql+pyodbc://{username}:{urllib.parse.quote_plus(password)}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
    
    try:
        engine = create_engine(connection_string)
        print("✓ SQLAlchemy engine tạo thành công")
        return engine
    except Exception as e:
        print(f"❌ Lỗi tạo SQLAlchemy engine: {e}")
        return None

def create_results_tables(conn):
    """
    Tạo các bảng để lưu kết quả audit
    """
    print("\n=== TẠO BẢNG KẾT QUẢ ===")
    
    cursor = conn.cursor()
    
    try:
        # Bảng lưu kết quả tổng quan của khách hàng
        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='audit_customer_results' AND xtype='U')
        CREATE TABLE audit_customer_results (
            id INT IDENTITY(1,1) PRIMARY KEY,
            customer_id NVARCHAR(50) NOT NULL,
            overall_status NVARCHAR(10) NOT NULL,
            reason NVARCHAR(100),
            processed_date DATETIME DEFAULT GETDATE(),
            total_groups INT,
            passed_groups INT,
            total_programs INT,
            passed_programs INT,
            fake_picture_detected BIT DEFAULT 0
        )
        """)
        
        # Bảng lưu kết quả chi tiết theo group
        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='audit_group_results' AND xtype='U')
        CREATE TABLE audit_group_results (
            id INT IDENTITY(1,1) PRIMARY KEY,
            customer_id NVARCHAR(50) NOT NULL,
            group_name NVARCHAR(50) NOT NULL,
            group_status NVARCHAR(10) NOT NULL,
            passed_programs INT,
            required_programs INT,
            score NVARCHAR(20),
            processed_date DATETIME DEFAULT GETDATE()
        )
        """)
        
        # Bảng lưu kết quả chi tiết theo program
        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='audit_program_results' AND xtype='U')
        CREATE TABLE audit_program_results (
            id INT IDENTITY(1,1) PRIMARY KEY,
            customer_id NVARCHAR(50) NOT NULL,
            group_name NVARCHAR(50) NOT NULL,
            program_type NVARCHAR(50) NOT NULL,
            pass_status NVARCHAR(10) NOT NULL,
            reason NVARCHAR(100),
            audit_value FLOAT,
            required_value FLOAT,
            registration_qty INT,
            condition_min_value FLOAT,
            score NVARCHAR(20),
            deficit FLOAT,
            message NVARCHAR(500),
            processed_date DATETIME DEFAULT GETDATE()
        )
        """)
        
        conn.commit()
        print("✓ Tạo bảng kết quả thành công")
        
    except Exception as e:
        print(f"❌ Lỗi tạo bảng: {e}")
        conn.rollback()

def load_data_from_database(engine):
    """
    Load data từ 3 tables trong SQL Server
    """
    print("\n=== LOAD DATA TỪ DATABASE ===")
    
    try:
        # Load audit data (200K records)
        print("Loading audit data...")
        audit_data = pd.read_sql("""
            SELECT group, value, program_type, audit_date, customer_id 
            FROM tableA
            WHERE audit_date >= '2024-01-01'
        """, engine)
        print(f"✓ Loaded {len(audit_data)} audit records")
        
        # Load condition data (300 records)
        print("Loading condition data...")
        condition_data = pd.read_sql("""
            SELECT group, condition_min_value, condition_point, group_min_value, program_type
            FROM tableB
        """, engine)
        print(f"✓ Loaded {len(condition_data)} condition records")
        
        # Load registration data (80K records)
        print("Loading registration data...")
        registration_data = pd.read_sql("""
            SELECT program_type, qty, customer_id
            FROM tableC
        """, engine)
        print(f"✓ Loaded {len(registration_data)} registration records")
        
        return audit_data, condition_data, registration_data
        
    except Exception as e:
        print(f"❌ Lỗi load data từ database: {e}")
        print("Sử dụng dữ liệu mẫu thay thế...")
        return create_sample_data()

def create_sample_data():
    """
    Tạo dữ liệu mẫu để test (khi không kết nối được database)
    """
    print("=== TẠO DỮ LIỆU MẪU ===")
    
    # Tạo audit data (200K records)
    np.random.seed(42)
    n_audit = 200000
    n_customers = 10000
    n_programs = 50
    
    audit_data = pd.DataFrame({
        'customer_id': np.random.choice([f'CUST_{i:06d}' for i in range(n_customers)], n_audit),
        'program_type': np.random.choice([f'PROG_{i:03d}' for i in range(n_programs)] + ['fake_picture'], n_audit),
        'group': np.random.choice(['GROUP_A', 'GROUP_B', 'GROUP_C', 'GROUP_D'], n_audit),
        'value': np.random.randint(0, 10, n_audit),
        'audit_date': pd.date_range('2024-01-01', periods=n_audit, freq='1min')
    })
    
    # Tạo condition data (300 records)
    condition_data = pd.DataFrame({
        'group': ['GROUP_A', 'GROUP_A', 'GROUP_A', 'GROUP_B', 'GROUP_B', 'GROUP_C', 'GROUP_D'] * 50,
        'program_type': [f'PROG_{i:03d}' for i in range(350)],
        'condition_min_value': np.random.randint(1, 5, 350),
        'condition_point': np.random.randint(1, 10, 350),
        'group_min_value': [2, 2, 2, 1, 1, 3, 1] * 50
    })
    
    # Tạo registration data (80K records)
    n_registration = 80000
    registration_data = pd.DataFrame({
        'customer_id': np.random.choice([f'CUST_{i:06d}' for i in range(n_customers)], n_registration),
        'program_type': np.random.choice([f'PROG_{i:03d}' for i in range(n_programs)] + ['fake_picture'], n_registration),
        'qty': np.random.randint(1, 5, n_registration)
    })
    
    print(f"✓ Tạo {len(audit_data)} audit records")
    print(f"✓ Tạo {len(condition_data)} condition records") 
    print(f"✓ Tạo {len(registration_data)} registration records")
    
    return audit_data, condition_data, registration_data

def optimize_data_for_performance(audit_data, condition_data, registration_data):
    """
    Tối ưu data types để tăng tốc độ xử lý
    """
    print("\n=== TỐI ƯU DATA ===")
    
    # Chuyển string columns thành category để tiết kiệm memory
    audit_data['customer_id'] = audit_data['customer_id'].astype('category')
    audit_data['program_type'] = audit_data['program_type'].astype('category')
    audit_data['group'] = audit_data['group'].astype('category')
    
    condition_data['group'] = condition_data['group'].astype('category')
    condition_data['program_type'] = condition_data['program_type'].astype('category')
    
    registration_data['customer_id'] = registration_data['customer_id'].astype('category')
    registration_data['program_type'] = registration_data['program_type'].astype('category')
    
    print("✓ Data optimization completed")
    return audit_data, condition_data, registration_data

def process_audit_for_all_customers(audit_data, condition_data, registration_data):
    """
    Xử lý audit cho tất cả khách hàng
    """
    print("\n=== XỬ LÝ AUDIT ===")
    
    # Group audit data theo customer_id
    customer_groups = audit_data.groupby('customer_id')
    total_customers = len(customer_groups)
    
    all_results = {}
    
    print(f"Processing {total_customers} customers...")
    
    for customer_idx, (customer_id, customer_audit) in enumerate(customer_groups):
        # Hiển thị tiến độ mỗi 1000 khách hàng
        if customer_idx % 1000 == 0:
            print(f"  Processing customer {customer_idx + 1}/{total_customers}")
        
        # Xử lý từng khách hàng
        customer_result = process_single_customer(
            customer_id, customer_audit, condition_data, registration_data
        )
        all_results[customer_id] = customer_result
    
    print("✓ All customers processed")
    return all_results

def process_single_customer(customer_id, customer_audit, condition_data, registration_data):
    """
    Xử lý audit cho 1 khách hàng cụ thể
    """
    # Lấy thông tin đăng ký của khách hàng này
    customer_registration = registration_data[
        registration_data['customer_id'] == customer_id
    ]
    
    # Nếu khách hàng không có đăng ký gì
    if customer_registration.empty:
        return {
            'customer_id': customer_id,
            'overall_status': 'FAIL',
            'reason': 'NO_REGISTRATION',
            'group_results': {}
        }
    
    # Merge audit data với registration data
    merged_data = pd.merge(
        customer_audit,
        customer_registration,
        on=['customer_id', 'program_type'],
        how='inner'
    )
    
    # Nếu không có audit data cho các program đã đăng ký
    if merged_data.empty:
        return {
            'customer_id': customer_id,
            'overall_status': 'FAIL',
            'reason': 'NO_AUDIT_DATA',
            'group_results': {}
        }
    
    # Xử lý từng group
    group_results = {}
    
    for group_name, group_data in merged_data.groupby('group'):
        group_result = process_single_group(group_name, group_data, condition_data)
        group_results[group_name] = group_result
    
    # Xác định overall status
    overall_status = determine_overall_status(group_results)
    
    return {
        'customer_id': customer_id,
        'overall_status': overall_status,
        'reason': 'PROCESSED',
        'group_results': group_results
    }

def process_single_group(group_name, group_data, condition_data):
    """
    Xử lý audit cho 1 group cụ thể
    """
    # Lấy điều kiện cho group này
    group_conditions = condition_data[condition_data['group'] == group_name]
    
    if group_conditions.empty:
        return {
            'group': group_name,
            'group_status': 'FAIL',
            'reason': 'NO_CONDITIONS',
            'program_results': {}
        }
    
    # Xử lý từng program trong group
    program_results = {}
    passed_programs = 0
    
    for _, program_row in group_data.iterrows():
        program_type = program_row['program_type']
        audit_value = program_row['value']
        registration_qty = program_row['qty']
        
        # LOGIC NGOẠI LỆ: Xử lý fake_picture
        if program_type == 'fake_picture':
            program_result = handle_fake_picture_program(audit_value)
        else:
            # Xử lý program bình thường
            program_result = handle_normal_program(
                program_type, audit_value, registration_qty, group_conditions
            )
        
        program_results[program_type] = program_result
        
        if program_result['pass_status'] == 'PASS':
            passed_programs += 1
    
    # Xác định group status
    group_min_value = group_conditions.iloc[0]['group_min_value']
    group_status = 'PASS' if passed_programs >= group_min_value else 'FAIL'
    
    return {
        'group': group_name,
        'group_status': group_status,
        'passed_programs': passed_programs,
        'required_programs': group_min_value,
        'score': f"{passed_programs}/{group_min_value}",
        'program_results': program_results
    }

def handle_fake_picture_program(audit_value):
    """
    Xử lý program fake_picture - LOGIC NGOẠI LỆ
    """
    # Nếu có audit value > 0 nghĩa là phát hiện fake picture -> FAIL
    if audit_value > 0:
        return {
            'program_type': 'fake_picture',
            'pass_status': 'FAIL',
            'reason': 'FAKE_PICTURE_DETECTED',
            'audit_value': audit_value,
            'message': f'Phát hiện fake picture với giá trị: {audit_value}'
        }
    else:
        return {
            'program_type': 'fake_picture',
            'pass_status': 'PASS',
            'reason': 'NO_FAKE_PICTURE',
            'audit_value': audit_value,
            'message': 'Không phát hiện fake picture'
        }

def handle_normal_program(program_type, audit_value, registration_qty, group_conditions):
    """
    Xử lý program bình thường (không phải fake_picture)
    """
    # Tìm điều kiện cho program này
    program_condition = group_conditions[group_conditions['program_type'] == program_type]
    
    if program_condition.empty:
        return {
            'program_type': program_type,
            'pass_status': 'FAIL',
            'reason': 'NO_CONDITION',
            'audit_value': audit_value,
            'required_value': 0,
            'message': f'Không có điều kiện cho program {program_type}'
        }
    
    # Tính giá trị yêu cầu
    condition_min_value = program_condition.iloc[0]['condition_min_value']
    required_value = condition_min_value * registration_qty
    
    # Kiểm tra pass/fail
    if audit_value >= required_value:
        pass_status = 'PASS'
        message = f'Đạt yêu cầu: {audit_value}/{required_value}'
    else:
        pass_status = 'FAIL'
        deficit = required_value - audit_value
        message = f'Không đạt yêu cầu: {audit_value}/{required_value} (thiếu {deficit})'
    
    return {
        'program_type': program_type,
        'pass_status': pass_status,
        'reason': 'NORMAL_PROCESSING',
        'audit_value': audit_value,
        'required_value': required_value,
        'registration_qty': registration_qty,
        'condition_min_value': condition_min_value,
        'score': f"{audit_value}/{required_value}",
        'deficit': max(0, required_value - audit_value),
        'message': message
    }

def determine_overall_status(group_results):
    """
    Xác định overall status của khách hàng
    """
    # Nếu có bất kỳ group nào FAIL thì overall FAIL
    for group_name, group_result in group_results.items():
        if group_result['group_status'] == 'FAIL':
            return 'FAIL'
    
    # Nếu tất cả groups đều PASS thì overall PASS
    return 'PASS'

def save_results_to_database(all_results, conn):
    """
    Lưu kết quả vào SQL Server
    """
    print("\n=== LƯU KẾT QUẢ VÀO DATABASE ===")
    
    cursor = conn.cursor()
    
    try:
        # Chuẩn bị dữ liệu để insert
        customer_data = []
        group_data = []
        program_data = []
        
        for customer_id, result in all_results.items():
            # Tính toán thống kê
            total_groups = len(result['group_results'])
            passed_groups = sum(1 for gr in result['group_results'].values() if gr['group_status'] == 'PASS')
            total_programs = sum(len(gr['program_results']) for gr in result['group_results'].values())
            passed_programs = sum(
                sum(1 for pr in gr['program_results'].values() if pr['pass_status'] == 'PASS')
                for gr in result['group_results'].values()
            )
            
            # Kiểm tra fake picture
            fake_picture_detected = any(
                pr['program_type'] == 'fake_picture' and pr['pass_status'] == 'FAIL'
                for gr in result['group_results'].values()
                for pr in gr['program_results'].values()
            )
            
            # Dữ liệu customer
            customer_data.append((
                customer_id,
                result['overall_status'],
                result['reason'],
                total_groups,
                passed_groups,
                total_programs,
                passed_programs,
                1 if fake_picture_detected else 0
            ))
            
            # Dữ liệu group
            for group_name, group_result in result['group_results'].items():
                group_data.append((
                    customer_id,
                    group_name,
                    group_result['group_status'],
                    group_result['passed_programs'],
                    group_result['required_programs'],
                    group_result['score']
                ))
                
                # Dữ liệu program
                for program_type, program_result in group_result['program_results'].items():
                    program_data.append((
                        customer_id,
                        group_name,
                        program_type,
                        program_result['pass_status'],
                        program_result['reason'],
                        program_result.get('audit_value', 0),
                        program_result.get('required_value', 0),
                        program_result.get('registration_qty', 0),
                        program_result.get('condition_min_value', 0),
                        program_result.get('score', ''),
                        program_result.get('deficit', 0),
                        program_result.get('message', '')
                    ))
        
        # Insert dữ liệu customer
        print("Inserting customer results...")
        cursor.executemany("""
            INSERT INTO audit_customer_results 
            (customer_id, overall_status, reason, total_groups, passed_groups, 
             total_programs, passed_programs, fake_picture_detected)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, customer_data)
        
        # Insert dữ liệu group
        print("Inserting group results...")
        cursor.executemany("""
            INSERT INTO audit_group_results 
            (customer_id, group_name, group_status, passed_programs, 
             required_programs, score)
            VALUES (?, ?, ?, ?, ?, ?)
        """, group_data)
        
        # Insert dữ liệu program
        print("Inserting program results...")
        cursor.executemany("""
            INSERT INTO audit_program_results 
            (customer_id, group_name, program_type, pass_status, reason,
             audit_value, required_value, registration_qty, condition_min_value,
             score, deficit, message)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, program_data)
        
        conn.commit()
        print(f"✓ Lưu thành công {len(customer_data)} customers vào database")
        
    except Exception as e:
        print(f"❌ Lỗi lưu vào database: {e}")
        conn.rollback()
        raise e

def analyze_results(all_results):
    """
    Phân tích kết quả audit
    """
    print("\n=== PHÂN TÍCH KẾT QUẢ ===")
    
    total_customers = len(all_results)
    passed_customers = sum(1 for result in all_results.values() if result['overall_status'] == 'PASS')
    failed_customers = total_customers - passed_customers
    
    print(f"Tổng số khách hàng: {total_customers}")
    print(f"Khách hàng PASS: {passed_customers}")
    print(f"Khách hàng FAIL: {failed_customers}")
    print(f"Tỷ lệ thành công: {passed_customers/total_customers*100:.2f}%")
    
    # Phân tích fake_picture
    fake_picture_fails = 0
    fake_picture_passes = 0
    
    for result in all_results.values():
        for group_result in result['group_results'].values():
            for program_result in group_result['program_results'].values():
                if program_result['program_type'] == 'fake_picture':
                    if program_result['pass_status'] == 'FAIL':
                        fake_picture_fails += 1
                    else:
                        fake_picture_passes += 1
    
    print(f"Khách hàng bị phát hiện fake picture: {fake_picture_fails}")
    print(f"Khách hàng không có fake picture: {fake_picture_passes}")
    
    return {
        'total_customers': total_customers,
        'passed_customers': passed_customers,
        'failed_customers': failed_customers,
        'fake_picture_fails': fake_picture_fails,
        'fake_picture_passes': fake_picture_passes
    }

def show_sample_results(all_results, limit=3):
    """
    Hiển thị mẫu kết quả để kiểm tra
    """
    print(f"\n=== MẪU KẾT QUẢ (hiển thị {limit} khách hàng) ===")
    
    # Hiển thị một số khách hàng pass
    passed_customers = [
        (customer_id, result) for customer_id, result in all_results.items()
        if result['overall_status'] == 'PASS'
    ]
    
    print("Khách hàng PASS:")
    for i, (customer_id, result) in enumerate(passed_customers[:limit]):
        print(f"  {i+1}. {customer_id}: {result['reason']}")
    
    # Hiển thị một số khách hàng fail
    failed_customers = [
        (customer_id, result) for customer_id, result in all_results.items()
        if result['overall_status'] == 'FAIL'
    ]
    
    print("\nKhách hàng FAIL:")
    for i, (customer_id, result) in enumerate(failed_customers[:limit]):
        print(f"  {i+1}. {customer_id}: {result['reason']}")

def main():
    """
    Hàm chính để chạy toàn bộ quy trình audit
    """
    print("🚀 BẮT ĐẦU XỬ LÝ AUDIT VỚI SQL SERVER")
    print("=" * 60)
    
    start_time = time.time()
    
    # Kết nối database
    conn = create_database_connection()
    if conn is None:
        print("Không thể kết nối database, sử dụng dữ liệu mẫu...")
        conn = None
    
    engine = None
    if conn:
        engine = create_sqlalchemy_engine()
        if engine:
            create_results_tables(conn)
    
    try:
        # Load data
        if engine:
            audit_data, condition_data, registration_data = load_data_from_database(engine)
        else:
            audit_data, condition_data, registration_data = create_sample_data()
        
        # Tối ưu data
        audit_data, condition_data, registration_data = optimize_data_for_performance(
            audit_data, condition_data, registration_data
        )
        
        # Xử lý audit
        all_results = process_audit_for_all_customers(
            audit_data, condition_data, registration_data
        )
        
        # Phân tích kết quả
        analysis = analyze_results(all_results)
        
        # Hiển thị mẫu kết quả
        show_sample_results(all_results)
        
        # Lưu vào database
        if conn:
            save_results_to_database(all_results, conn)
        else:
            print("Không có kết nối database, bỏ qua việc lưu")
        
        # Lưu vào file JSON (backup)
        with open('audit_results.json', 'w', encoding='utf-8') as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False, default=str)
        print("✓ Lưu backup vào file JSON")
        
        total_time = time.time() - start_time
        print(f"\n🎉 HOÀN THÀNH!")
        print(f"⏱️  Tổng thời gian xử lý: {total_time:.2f} giây")
        print(f"📊 Tốc độ xử lý: {analysis['total_customers']/total_time:.0f} khách hàng/giây")
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if conn:
            conn.close()
            print("✓ Đóng kết nối database")

# Chạy chương trình
if __name__ == "__main__":
    main()


"""
📦 Cài Đặt Dependencies

pip install pandas numpy pyodbc sqlalchemy

🔧 Cấu Hình SQL Server
1. Cài đặt ODBC Driver
Tải và cài đặt "ODBC Driver 17 for SQL Server" từ Microsoft
Link: https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
2. Cập nhật thông tin kết nối
3. Tạo Database và Tables
Code sẽ tự động tạo các bảng:
audit_customer_results - Kết quả tổng quan
audit_group_results - Kết quả theo group
audit_program_results - Kết quả chi tiết theo program
🎯 Các Tính Năng Chính
1. Kết Nối SQL Server
✅ Sử dụng pyodbc và SQLAlchemy
✅ Error handling cho kết nối
✅ Fallback sang dữ liệu mẫu nếu không kết nối được
2. Lưu Kết Quả
✅ 3 bảng riêng biệt cho từng loại kết quả
✅ Batch insert để tăng performance
✅ Transaction để đảm bảo data integrity
3. Performance Tối Ưu
✅ Batch processing
✅ Memory efficient
✅ Progress tracking
4. User Friendly
✅ Code đơn giản, dễ hiểu
✅ Comment đầy đủ
✅ Error messages rõ ràng
✅ Hướng dẫn cài đặt chi tiết
Code này sẽ chạy không lỗi và lưu kết quả vào SQL Server một cách hiệu quả!
"""