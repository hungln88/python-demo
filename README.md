# Display Program Management System
## Hệ thống Quản lý Chương trình Trưng bày

A comprehensive Python application for managing display programs, customer registrations, audits, and reward eligibility checking.

## 🏗️ System Architecture

### Database Schema
- **register_item**: Program configurations (display types, facing, units)
- **register**: Customer registrations for programs
- **condition_group**: Criteria groups for programs
- **condition_item**: Specific condition requirements and points
- **audit_picture**: Audit results from field inspections

### Business Flow
1. **Program Configuration**: Operations team configures display programs in `register_item`
2. **Criteria Setup**: Configure evaluation criteria in `condition_group` and `condition_item`
3. **Customer Registration**: Customers/shopping centers register for programs in `register`
4. **Audit Process**: Company supervisors conduct audits and record results in `audit_picture`
5. **Evaluation**: System evaluates customers against criteria to determine reward eligibility

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8+
- SQL Server (LocalDB, Express, or Full)
- ODBC Driver 17 for SQL Server

### Installation

1. **Clone/Download the project files**
2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup SQL Server Database:**
   ```bash
   # Run the schema creation script
   sqlcmd -S localhost -d master -i schema.sql
   
   # Insert sample data
   sqlcmd -S localhost -d DisplayProgramDB -i sample_data.sql
   ```

4. **Configure Database Connection:**
   - Edit `database.py` if needed to adjust connection settings
   - Default: Uses Windows Authentication to connect to localhost
   - For custom settings, modify the `DatabaseConnection` initialization in `main.py`

### Alternative SQL Server Setup
If you don't have SQL Server installed, you can use SQL Server Express or LocalDB:

```bash
# Download SQL Server Express (free)
# Or install LocalDB
sqllocaldb create DisplayProgramInstance
sqllocaldb start DisplayProgramInstance
```

## 🎯 Usage

### Running the Application
```bash
python main.py
```

### Main Features

#### 1. 📊 Program Summary
- View performance summary for specific programs
- Shows eligible/failed customer counts
- Displays success rates and common failure reasons

#### 2. 👤 Customer Summary  
- View individual customer performance across all programs
- Shows points earned vs maximum possible
- Details program-specific results

#### 3. 🎯 Eligible Customers
- List customers who meet all criteria for rewards
- Filter by specific program or view all programs
- Shows points and success rates

#### 4. ❌ Failed Customers
- List customers who don't meet criteria
- Shows specific failure reasons
- Helps identify areas for improvement

#### 5. 📈 Monthly Report
- Comprehensive monthly analysis
- Overall statistics and program breakdowns
- Customer performance summaries

#### 6. 📝 Registration Management
- Add new customer registrations
- Validates against available programs
- Checks display type compatibility

#### 7. 🔍 Audit Management
- Add audit results from field inspections
- Links to condition codes for evaluation
- Timestamp tracking for audit dates

#### 8. 🧪 Test Scenarios
- Run predefined test cases with sample data
- Verify system functionality
- Demonstrate business logic

## 📋 Sample Data

The system includes comprehensive sample data:

### Programs
- **PROG001**: Beverage program with 3-slot, 4-slot, and display shelves
- **PROG002**: Snack program with similar display options

### Customers
- **CUST001-CUST005**: Various performance levels
- Mix of active/inactive registrations
- Different display type preferences

### Evaluation Criteria
- **CLEANLINESS**: Store cleanliness standards
- **PRODUCT_AVAILABILITY**: Stock availability requirements  
- **DISPLAY_QUALITY**: Display presentation standards

### Test Results
Sample data includes audit results showing:
- High performers (CUST001, CUST002)
- Poor performers (CUST003, CUST005)
- Mixed performance scenarios

## 🔧 Code Structure

```
├── models.py           # Data models and classes
├── database.py         # Database connection and operations
├── business_logic.py   # Core business logic and evaluation
├── main.py            # CLI application interface
├── schema.sql         # Database schema creation
├── sample_data.sql    # Sample data for testing
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## 🎨 Key Features

### Business Logic
- **Comprehensive Evaluation**: Multi-criteria customer assessment
- **Flexible Scoring**: Point-based evaluation system
- **Status Tracking**: Active/inactive registration management
- **Failure Analysis**: Detailed failure reason tracking

### Database Design
- **Referential Integrity**: Foreign key constraints
- **Performance Optimized**: Strategic indexing
- **Scalable Schema**: Supports multiple programs and time periods

### User Interface
- **Bilingual Support**: Vietnamese and English
- **Intuitive Navigation**: Clear menu system
- **Rich Reporting**: Detailed summaries and statistics
- **Error Handling**: Comprehensive validation and error messages

## 🔍 Business Rules

### Evaluation Logic
1. Customer must be actively registered for a program
2. All condition criteria must have audit results
3. Audit values must meet minimum thresholds
4. Points awarded only for criteria that meet minimums
5. Overall eligibility requires meeting ALL criteria

### Registration Validation
- Program must exist for the specified month
- Display type must be valid for the program
- Quantity must be positive
- Duplicate registrations are prevented by primary key

### Audit Requirements
- Must link to existing condition codes
- Values should be numeric for evaluation
- Timestamp tracking for audit trail

## 🚀 Future Enhancements

### Potential Additions
- **Web Interface**: Flask/FastAPI web application
- **API Endpoints**: REST API for integration
- **Advanced Reporting**: Charts and visualizations
- **Email Notifications**: Automated alerts
- **Data Export**: Excel/PDF report generation
- **Multi-language Support**: Full localization
- **Role-based Access**: User authentication and authorization

### Performance Optimizations
- **Caching**: Redis integration for frequent queries
- **Batch Processing**: Bulk operations for large datasets
- **Background Jobs**: Async processing for reports

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Verify SQL Server is running
   - Check connection string in `database.py`
   - Ensure ODBC Driver 17 is installed

2. **Schema Creation Errors**
   - Run as administrator if permission issues
   - Verify database doesn't already exist
   - Check SQL Server version compatibility

3. **Import Errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version (3.8+ required)

4. **No Data Found**
   - Run `sample_data.sql` to insert test data
   - Verify correct month format (YYYYMM)
   - Check database connection

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Verify sample data is loaded correctly
3. Test with the provided test scenarios
4. Check logs for detailed error messages

---

**Created**: September 19, 2025  
**Version**: 1.0  
**Python**: 3.8+  
**Database**: SQL Server
