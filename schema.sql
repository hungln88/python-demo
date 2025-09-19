-- Display Program Management System Schema for SQL Server
-- Created: 2025-09-19

USE master;
GO

-- Create database if it doesn't exist
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'DisplayProgramDB')
BEGIN
    CREATE DATABASE DisplayProgramDB;
END
GO

USE DisplayProgramDB;
GO

-- Drop tables if they exist (for clean setup)
IF OBJECT_ID('audit_picture', 'U') IS NOT NULL DROP TABLE audit_picture;
IF OBJECT_ID('condition_item', 'U') IS NOT NULL DROP TABLE condition_item;
IF OBJECT_ID('condition_group', 'U') IS NOT NULL DROP TABLE condition_group;
IF OBJECT_ID('register', 'U') IS NOT NULL DROP TABLE register;
IF OBJECT_ID('register_item', 'U') IS NOT NULL DROP TABLE register_item;
GO

-- Thông tin chương trình do vận hành cấu hình 
CREATE TABLE register_item (
    yyyymm INTEGER NOT NULL,
    program_code VARCHAR(50) NOT NULL,
    type_code VARCHAR(50) NOT NULL, -- mã chương trình
    item VARCHAR(50) NOT NULL, -- enum loại kệ trưng bày, kệ 3 ô trưng bày, kệ 4 ô trưng bày
    facing INTEGER NOT NULL, -- số sản phẩm trong 1 ô trưng bày
    unit INTEGER NOT NULL, -- số lượng ô trưng bày trong kệ
    CONSTRAINT PK_register_item PRIMARY KEY (yyyymm, program_code, type_code, item)
);
GO

-- Thông tin khách hàng đăng ký chương trình với số lượng
CREATE TABLE register (
    yyyymm INTEGER NOT NULL,
    program_code VARCHAR(50) NOT NULL,
    customer_code VARCHAR(50) NOT NULL, -- mã khách hàng
    display_type VARCHAR(50) NOT NULL, -- ref tới register_item.item: enum loại kệ trưng bày
    register_qty INTEGER NOT NULL, -- số lượng đăng ký
    status BIT NOT NULL, -- trạng thái, 0 --> ngừng, 1: đang đăng ký
    CONSTRAINT PK_register PRIMARY KEY (yyyymm, program_code, customer_code, display_type)
);
GO

-- chứa thông tin scheme từng tiêu chí
CREATE TABLE condition_group (
    yyyymm INTEGER NOT NULL,
    program_code VARCHAR(50) NOT NULL,
    [group] INTEGER NOT NULL,
    type_code VARCHAR(50) NOT NULL, -- link với type_code trong table register_item
    group_point INTEGER NOT NULL,
    CONSTRAINT PK_condition_group PRIMARY KEY (yyyymm, program_code, [group])
);
GO

-- chứa thông tin ghi nhận giá trị cấu hình từng tiêu chí của scheme
CREATE TABLE condition_item (
    yyyymm INTEGER NOT NULL,
    program_code VARCHAR(50) NOT NULL,
    [group] INTEGER NOT NULL, -- ref tới condition_group.group
    condition_code VARCHAR(50) NOT NULL,
    condition_min_value INTEGER NOT NULL,
    condition_point INTEGER NOT NULL,
    CONSTRAINT PK_condition_item PRIMARY KEY (yyyymm, program_code, [group], condition_code)
);
GO

-- table chứa thông tin kết quả thực tế của khách hàng được kiểm tra
CREATE TABLE audit_picture (
    yyyymm INTEGER NOT NULL,
    customer_code VARCHAR(50) NOT NULL,
    condition_code VARCHAR(50) NOT NULL, -- ref tới condition_item.condition_code
    value VARCHAR(50) NOT NULL,
    audit_date DATETIME DEFAULT GETDATE(),
    CONSTRAINT PK_audit_picture PRIMARY KEY (yyyymm, customer_code, condition_code)
);
GO

-- Add foreign key constraints
ALTER TABLE register 
ADD CONSTRAINT FK_register_register_item 
FOREIGN KEY (yyyymm, program_code, display_type) 
REFERENCES register_item(yyyymm, program_code, item);
GO

ALTER TABLE condition_item 
ADD CONSTRAINT FK_condition_item_condition_group 
FOREIGN KEY (yyyymm, program_code, [group]) 
REFERENCES condition_group(yyyymm, program_code, [group]);
GO

-- Create indexes for better performance
CREATE INDEX IX_register_customer ON register(customer_code, yyyymm);
CREATE INDEX IX_audit_picture_customer ON audit_picture(customer_code, yyyymm);
CREATE INDEX IX_condition_item_code ON condition_item(condition_code);
GO

PRINT 'Database schema created successfully!';
