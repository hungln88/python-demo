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
-- PROG001: Chương trình đồ uống với 2 groups
-- Group 1: Yêu cầu 2/3 sản phẩm đạt tiêu chí (group_point = 2)
-- Group 2: Yêu cầu 3/3 sản phẩm đạt tiêu chí (group_point = 3)
INSERT INTO condition_group (yyyymm, program_code, [group], type_code, group_point) VALUES
(202509, 'PROG001', 1, 'TYPE_BEVERAGE', 2),  -- Chỉ cần 2/3 sản phẩm đạt
(202509, 'PROG001', 2, 'TYPE_BEVERAGE', 3),  -- Cần 3/3 sản phẩm đạt
(202509, 'PROG002', 1, 'TYPE_SNACK', 2),     -- Chỉ cần 2/3 sản phẩm đạt
(202509, 'PROG002', 2, 'TYPE_SNACK', 3),     -- Cần 3/3 sản phẩm đạt
(202510, 'PROG001', 1, 'TYPE_BEVERAGE', 2);  -- Chỉ cần 2/3 sản phẩm đạt
GO

-- Sample data for condition_item (Specific conditions)
-- Mỗi condition_item có condition_point = 1 (nếu đạt thì được 1 điểm)
-- Group sẽ đạt nếu tổng điểm >= group_point
INSERT INTO condition_item (yyyymm, program_code, [group], condition_code, condition_min_value, condition_point) VALUES
-- PROG001 Group 1 conditions (3 sản phẩm, cần 2/3 đạt)
(202509, 'PROG001', 1, 'SPA_CLEANLINESS', 80, 1),      -- Sản phẩm A: Độ sạch sẽ
(202509, 'PROG001', 1, 'SPA_AVAILABILITY', 90, 1),     -- Sản phẩm A: Tình trạng có hàng
(202509, 'PROG001', 1, 'SPA_DISPLAY', 75, 1),          -- Sản phẩm A: Chất lượng trưng bày
-- PROG001 Group 2 conditions (3 sản phẩm, cần 3/3 đạt)
(202509, 'PROG001', 2, 'SPB_CLEANLINESS', 85, 1),      -- Sản phẩm B: Độ sạch sẽ
(202509, 'PROG001', 2, 'SPB_AVAILABILITY', 95, 1),     -- Sản phẩm B: Tình trạng có hàng
(202509, 'PROG001', 2, 'SPB_DISPLAY', 80, 1),          -- Sản phẩm B: Chất lượng trưng bày
-- PROG002 Group 1 conditions (3 sản phẩm, cần 2/3 đạt)
(202509, 'PROG002', 1, 'SNACK_CLEANLINESS', 75, 1),    -- Snack: Độ sạch sẽ
(202509, 'PROG002', 1, 'SNACK_AVAILABILITY', 85, 1),   -- Snack: Tình trạng có hàng
(202509, 'PROG002', 1, 'SNACK_DISPLAY', 70, 1),        -- Snack: Chất lượng trưng bày
-- PROG002 Group 2 conditions (3 sản phẩm, cần 3/3 đạt)
(202509, 'PROG002', 2, 'PREMIUM_CLEANLINESS', 80, 1),  -- Premium: Độ sạch sẽ
(202509, 'PROG002', 2, 'PREMIUM_AVAILABILITY', 90, 1), -- Premium: Tình trạng có hàng
(202509, 'PROG002', 2, 'PREMIUM_DISPLAY', 75, 1),      -- Premium: Chất lượng trưng bày
-- Next month data
(202510, 'PROG001', 1, 'SPA_CLEANLINESS', 80, 1),
(202510, 'PROG001', 1, 'SPA_AVAILABILITY', 90, 1),
(202510, 'PROG001', 1, 'SPA_DISPLAY', 75, 1);
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
-- CUST001: Đạt Group 1 (2/3), Không đạt Group 2 (1/3) → FAIL
-- CUST002: Đạt cả 2 Groups (3/3 và 3/3) → PASS
-- CUST003: Không đạt cả 2 Groups → FAIL (và inactive)
-- CUST004: Đạt Group 1 (2/3), Không đạt Group 2 (1/3) → FAIL
-- CUST005: Đạt Group 1 (2/3), Không đạt Group 2 (1/3) → FAIL
INSERT INTO audit_picture (yyyymm, customer_code, condition_code, value, audit_date) VALUES
-- CUST001 audit results - Group 1: 2/3 đạt, Group 2: 1/3 đạt
(202509, 'CUST001', 'SPA_CLEANLINESS', '85', '2025-09-15 10:30:00'),      -- Đạt (85 >= 80)
(202509, 'CUST001', 'SPA_AVAILABILITY', '92', '2025-09-15 10:30:00'),    -- Đạt (92 >= 90)
(202509, 'CUST001', 'SPA_DISPLAY', '70', '2025-09-15 10:30:00'),         -- Không đạt (70 < 75)
(202509, 'CUST001', 'SPB_CLEANLINESS', '80', '2025-09-15 10:30:00'),     -- Không đạt (80 < 85)
(202509, 'CUST001', 'SPB_AVAILABILITY', '90', '2025-09-15 10:30:00'),    -- Không đạt (90 < 95)
(202509, 'CUST001', 'SPB_DISPLAY', '75', '2025-09-15 10:30:00'),         -- Không đạt (75 < 80)
-- CUST002 audit results - Group 1: 3/3 đạt, Group 2: 3/3 đạt
(202509, 'CUST002', 'SPA_CLEANLINESS', '90', '2025-09-16 14:20:00'),     -- Đạt (90 >= 80)
(202509, 'CUST002', 'SPA_AVAILABILITY', '95', '2025-09-16 14:20:00'),    -- Đạt (95 >= 90)
(202509, 'CUST002', 'SPA_DISPLAY', '80', '2025-09-16 14:20:00'),         -- Đạt (80 >= 75)
(202509, 'CUST002', 'SPB_CLEANLINESS', '90', '2025-09-16 14:20:00'),     -- Đạt (90 >= 85)
(202509, 'CUST002', 'SPB_AVAILABILITY', '98', '2025-09-16 14:20:00'),    -- Đạt (98 >= 95)
(202509, 'CUST002', 'SPB_DISPLAY', '85', '2025-09-16 14:20:00'),         -- Đạt (85 >= 80)
-- CUST003 audit results - Group 1: 0/3 đạt, Group 2: 0/3 đạt (inactive anyway)
(202509, 'CUST003', 'SPA_CLEANLINESS', '65', '2025-09-17 09:15:00'),     -- Không đạt (65 < 80)
(202509, 'CUST003', 'SPA_AVAILABILITY', '70', '2025-09-17 09:15:00'),    -- Không đạt (70 < 90)
(202509, 'CUST003', 'SPA_DISPLAY', '60', '2025-09-17 09:15:00'),         -- Không đạt (60 < 75)
(202509, 'CUST003', 'SPB_CLEANLINESS', '70', '2025-09-17 09:15:00'),     -- Không đạt (70 < 85)
(202509, 'CUST003', 'SPB_AVAILABILITY', '80', '2025-09-17 09:15:00'),    -- Không đạt (80 < 95)
(202509, 'CUST003', 'SPB_DISPLAY', '65', '2025-09-17 09:15:00'),         -- Không đạt (65 < 80)
-- CUST004 audit results - Group 1: 2/3 đạt, Group 2: 1/3 đạt
(202509, 'CUST004', 'SNACK_CLEANLINESS', '82', '2025-09-18 11:45:00'),   -- Đạt (82 >= 75)
(202509, 'CUST004', 'SNACK_AVAILABILITY', '88', '2025-09-18 11:45:00'),  -- Đạt (88 >= 85)
(202509, 'CUST004', 'SNACK_DISPLAY', '65', '2025-09-18 11:45:00'),       -- Không đạt (65 < 70)
(202509, 'CUST004', 'PREMIUM_CLEANLINESS', '75', '2025-09-18 11:45:00'), -- Không đạt (75 < 80)
(202509, 'CUST004', 'PREMIUM_AVAILABILITY', '85', '2025-09-18 11:45:00'),-- Không đạt (85 < 90)
(202509, 'CUST004', 'PREMIUM_DISPLAY', '70', '2025-09-18 11:45:00'),     -- Không đạt (70 < 75)
-- CUST005 audit results - Group 1: 2/3 đạt, Group 2: 1/3 đạt
(202509, 'CUST005', 'SNACK_CLEANLINESS', '80', '2025-09-19 08:30:00'),   -- Đạt (80 >= 75)
(202509, 'CUST005', 'SNACK_AVAILABILITY', '90', '2025-09-19 08:30:00'),  -- Đạt (90 >= 85)
(202509, 'CUST005', 'SNACK_DISPLAY', '65', '2025-09-19 08:30:00'),       -- Không đạt (65 < 70)
(202509, 'CUST005', 'PREMIUM_CLEANLINESS', '75', '2025-09-19 08:30:00'), -- Không đạt (75 < 80)
(202509, 'CUST005', 'PREMIUM_AVAILABILITY', '85', '2025-09-19 08:30:00'),-- Không đạt (85 < 90)
(202509, 'CUST005', 'PREMIUM_DISPLAY', '70', '2025-09-19 08:30:00');     -- Không đạt (70 < 75)
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
