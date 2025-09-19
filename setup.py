"""
Setup script for Display Program Management System
Created: 2025-09-19
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False


def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True


def install_requirements():
    """Install Python requirements"""
    if not Path("requirements.txt").exists():
        print("❌ requirements.txt not found")
        return False
    
    return run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installing Python dependencies"
    )


def setup_database():
    """Setup database schema and sample data"""
    print("\n🗄️ Database Setup")
    print("Please ensure SQL Server is running and accessible")
    
    # Check if SQL files exist
    if not Path("schema.sql").exists():
        print("❌ schema.sql not found")
        return False
    
    if not Path("sample_data.sql").exists():
        print("❌ sample_data.sql not found")
        return False
    
    print("📋 Database setup options:")
    print("1. Use sqlcmd (requires SQL Server command line tools)")
    print("2. Manual setup (run SQL files manually)")
    print("3. Skip database setup")
    
    choice = input("Choose option (1-3): ").strip()
    
    if choice == "1":
        # Try to setup using sqlcmd
        server = input("SQL Server instance (default: localhost): ").strip() or "localhost"
        
        success = True
        success &= run_command(
            f'sqlcmd -S {server} -d master -i schema.sql',
            "Creating database schema"
        )
        
        if success:
            success &= run_command(
                f'sqlcmd -S {server} -d DisplayProgramDB -i sample_data.sql',
                "Inserting sample data"
            )
        
        return success
    
    elif choice == "2":
        print("📋 Manual setup instructions:")
        print("1. Open SQL Server Management Studio or Azure Data Studio")
        print("2. Connect to your SQL Server instance")
        print("3. Open and execute schema.sql")
        print("4. Open and execute sample_data.sql")
        print("5. Verify tables are created with data")
        input("Press Enter when database setup is complete...")
        return True
    
    else:
        print("⏭️ Skipping database setup")
        return True


def test_application():
    """Test the application"""
    print("\n🧪 Testing Application")
    
    try:
        # Import main modules to check for import errors
        from database import DatabaseConnection
        from models import RegisterItem
        from business_logic import DisplayProgramService
        
        print("✅ All modules imported successfully")
        
        # Test database connection
        db_conn = DatabaseConnection()
        if db_conn.test_connection():
            print("✅ Database connection test passed")
            return True
        else:
            print("❌ Database connection test failed")
            print("Please check your SQL Server connection and database setup")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please check that all dependencies are installed")
        return False
    except Exception as e:
        print(f"❌ Application test failed: {e}")
        return False


def main():
    """Main setup function"""
    print("=" * 60)
    print("    DISPLAY PROGRAM MANAGEMENT SYSTEM SETUP")
    print("    Thiết lập Hệ thống Quản lý Chương trình Trưng bày")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install requirements
    print("\n📦 Installing Dependencies")
    if not install_requirements():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Setup database
    if not setup_database():
        print("❌ Database setup failed")
        print("You can run the setup again or setup the database manually")
    
    # Test application
    if not test_application():
        print("❌ Application test failed")
        print("Please check the error messages above and resolve issues")
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("=" * 40)
    print("📋 Next steps:")
    print("1. Run: python main.py")
    print("2. Try option 9 (Test Scenarios) to verify everything works")
    print("3. Explore the different menu options")
    print("4. Check README.md for detailed usage instructions")
    print("\n🚀 Happy coding!")


if __name__ == "__main__":
    main()
