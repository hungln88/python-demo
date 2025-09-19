-- Sample Data for Display Program Management System
-- Created: 2025-09-19

USE DisplayProgramDB;
GO

-- Clear existing data
DELETE FROM audit_picture;
DELETE FROM condition_item;
DELETE FROM condition_group;
DELETE FROM register;
DELETE FROM register_item;
GO

-- Sample data for register_item (Program configurations)
INSERT INTO register_item (yyyymm, program_code, type_code, item, facing, unit) VALUES
(202509, 'PROG001', 'TYPE_BEVERAGE', 'KE_3_O', 4, 3),
(202509, 'PROG001', 'TYPE_BEVERAGE', 'KE_4_O', 4, 4),
(202509, 'PROG001', 'TYPE_BEVERAGE', 'KE_TRUONG_BAY', 6, 2),
(202509, 'PROG002', 'TYPE_SNACK', 'KE_3_O', 3, 3),
(202509, 'PROG002', 'TYPE_SNACK', 'KE_4_O', 3, 4),
(202509, 'PROG002', 'TYPE_SNACK', 'KE_TRUONG_BAY', 5, 2),
(202510, 'PROG001', 'TYPE_BEVERAGE', 'KE_3_O', 4, 3),
(202510, 'PROG001', 'TYPE_BEVERAGE', 'KE_4_O', 4, 4);
GO

-- Sample data for condition_group (Scheme criteria groups)
INSERT INTO condition_group (yyyymm, program_code, [group], type_code, group_point) VALUES
(202509, 'PROG001', 1, 'TYPE_BEVERAGE', 100),
(202509, 'PROG001', 2, 'TYPE_BEVERAGE', 150),
(202509, 'PROG002', 1, 'TYPE_SNACK', 80),
(202509, 'PROG002', 2, 'TYPE_SNACK', 120),
(202510, 'PROG001', 1, 'TYPE_BEVERAGE', 100);
GO

-- Sample data for condition_item (Specific conditions)
INSERT INTO condition_item (yyyymm, program_code, [group], condition_code, condition_min_value, condition_point) VALUES
-- PROG001 Group 1 conditions
(202509, 'PROG001', 1, 'CLEANLINESS', 80, 30),
(202509, 'PROG001', 1, 'PRODUCT_AVAILABILITY', 90, 40),
(202509, 'PROG001', 1, 'DISPLAY_QUALITY', 75, 30),
-- PROG001 Group 2 conditions
(202509, 'PROG001', 2, 'CLEANLINESS', 85, 40),
(202509, 'PROG001', 2, 'PRODUCT_AVAILABILITY', 95, 60),
(202509, 'PROG001', 2, 'DISPLAY_QUALITY', 80, 50),
-- PROG002 Group 1 conditions
(202509, 'PROG002', 1, 'CLEANLINESS', 75, 25),
(202509, 'PROG002', 1, 'PRODUCT_AVAILABILITY', 85, 35),
(202509, 'PROG002', 1, 'DISPLAY_QUALITY', 70, 20),
-- PROG002 Group 2 conditions
(202509, 'PROG002', 2, 'CLEANLINESS', 80, 35),
(202509, 'PROG002', 2, 'PRODUCT_AVAILABILITY', 90, 50),
(202509, 'PROG002', 2, 'DISPLAY_QUALITY', 75, 35),
-- Next month data
(202510, 'PROG001', 1, 'CLEANLINESS', 80, 30),
(202510, 'PROG001', 1, 'PRODUCT_AVAILABILITY', 90, 40),
(202510, 'PROG001', 1, 'DISPLAY_QUALITY', 75, 30);
GO

-- Sample data for register (Customer registrations)
INSERT INTO register (yyyymm, program_code, customer_code, display_type, register_qty, status) VALUES
(202509, 'PROG001', 'CUST001', 'KE_3_O', 2, 1),
(202509, 'PROG001', 'CUST001', 'KE_4_O', 1, 1),
(202509, 'PROG001', 'CUST002', 'KE_3_O', 3, 1),
(202509, 'PROG001', 'CUST002', 'KE_TRUONG_BAY', 1, 1),
(202509, 'PROG001', 'CUST003', 'KE_3_O', 1, 0), -- Inactive registration
(202509, 'PROG002', 'CUST001', 'KE_3_O', 2, 1),
(202509, 'PROG002', 'CUST004', 'KE_4_O', 2, 1),
(202509, 'PROG002', 'CUST005', 'KE_TRUONG_BAY', 1, 1),
(202510, 'PROG001', 'CUST001', 'KE_3_O', 2, 1),
(202510, 'PROG001', 'CUST002', 'KE_4_O', 1, 1);
GO

-- Sample data for audit_picture (Audit results)
INSERT INTO audit_picture (yyyymm, customer_code, condition_code, value, audit_date) VALUES
-- CUST001 audit results - Good performance
(202509, 'CUST001', 'CLEANLINESS', '85', '2025-09-15 10:30:00'),
(202509, 'CUST001', 'PRODUCT_AVAILABILITY', '92', '2025-09-15 10:30:00'),
(202509, 'CUST001', 'DISPLAY_QUALITY', '78', '2025-09-15 10:30:00'),
-- CUST002 audit results - Excellent performance
(202509, 'CUST002', 'CLEANLINESS', '90', '2025-09-16 14:20:00'),
(202509, 'CUST002', 'PRODUCT_AVAILABILITY', '96', '2025-09-16 14:20:00'),
(202509, 'CUST002', 'DISPLAY_QUALITY', '85', '2025-09-16 14:20:00'),
-- CUST003 audit results - Poor performance (but inactive anyway)
(202509, 'CUST003', 'CLEANLINESS', '65', '2025-09-17 09:15:00'),
(202509, 'CUST003', 'PRODUCT_AVAILABILITY', '70', '2025-09-17 09:15:00'),
(202509, 'CUST003', 'DISPLAY_QUALITY', '60', '2025-09-17 09:15:00'),
-- CUST004 audit results - Good performance for PROG002
(202509, 'CUST004', 'CLEANLINESS', '82', '2025-09-18 11:45:00'),
(202509, 'CUST004', 'PRODUCT_AVAILABILITY', '88', '2025-09-18 11:45:00'),
(202509, 'CUST004', 'DISPLAY_QUALITY', '76', '2025-09-18 11:45:00'),
-- CUST005 audit results - Below minimum for some criteria
(202509, 'CUST005', 'CLEANLINESS', '72', '2025-09-19 08:30:00'),
(202509, 'CUST005', 'PRODUCT_AVAILABILITY', '83', '2025-09-19 08:30:00'),
(202509, 'CUST005', 'DISPLAY_QUALITY', '68', '2025-09-19 08:30:00');
GO

PRINT 'Sample data inserted successfully!';

-- Verification queries
PRINT 'Data verification:';
SELECT 'register_item' as table_name, COUNT(*) as record_count FROM register_item
UNION ALL
SELECT 'condition_group', COUNT(*) FROM condition_group
UNION ALL
SELECT 'condition_item', COUNT(*) FROM condition_item
UNION ALL
SELECT 'register', COUNT(*) FROM register
UNION ALL
SELECT 'audit_picture', COUNT(*) FROM audit_picture;
GO
