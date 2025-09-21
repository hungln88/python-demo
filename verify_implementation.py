#!/usr/bin/env python3
"""
Verify SqlServerEvaluationRepository Implementation
"""

import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def verify_imports():
    """Verify all imports work correctly"""
    try:
        print("🔍 Testing imports...")
        
        # Test domain imports
        from domain.entities.evaluation import ConditionGroup, ConditionItem, AuditPicture, CustomerEvaluationResult
        print("✅ Domain entities imported successfully")
        
        from domain.repositories.evaluation_repository import EvaluationRepository
        print("✅ Domain repository interface imported successfully")
        
        # Test infrastructure imports
        from infrastructure.database.sql_server_connection import SqlServerConnection
        print("✅ Infrastructure database connection imported successfully")
        
        from infrastructure.repositories.sql_server_evaluation_repository import SqlServerEvaluationRepository
        print("✅ Infrastructure repository imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def verify_instantiation():
    """Verify objects can be instantiated"""
    try:
        print("\n🔧 Testing instantiation...")
        
        # Create database connection
        db_connection = SqlServerConnection()
        print("✅ SqlServerConnection instantiated successfully")
        
        # Create repository
        repository = SqlServerEvaluationRepository(db_connection)
        print("✅ SqlServerEvaluationRepository instantiated successfully")
        
        # Verify it implements the interface
        assert isinstance(repository, EvaluationRepository)
        print("✅ SqlServerEvaluationRepository implements EvaluationRepository interface")
        
        return True
        
    except Exception as e:
        print(f"❌ Instantiation error: {e}")
        return False

def verify_methods():
    """Verify all required methods exist"""
    try:
        print("\n📋 Testing method signatures...")
        
        from infrastructure.repositories.sql_server_evaluation_repository import SqlServerEvaluationRepository
        from infrastructure.database.sql_server_connection import SqlServerConnection
        
        db_connection = SqlServerConnection()
        repository = SqlServerEvaluationRepository(db_connection)
        
        # Check all required methods exist
        required_methods = [
            'get_condition_groups',
            'get_condition_group_by_id', 
            'get_condition_items_by_group',
            'get_condition_items',
            'get_audit_results',
            'get_audit_result',
            'save_audit_result',
            'save_evaluation_result',
            'get_evaluation_result'
        ]
        
        for method_name in required_methods:
            assert hasattr(repository, method_name), f"Missing method: {method_name}"
            print(f"✅ Method {method_name} exists")
        
        return True
        
    except Exception as e:
        print(f"❌ Method verification error: {e}")
        return False

def main():
    """Main verification function"""
    print("🚀 Verifying SqlServerEvaluationRepository Implementation")
    print("=" * 60)
    
    success = True
    
    # Test imports
    if not verify_imports():
        success = False
    
    # Test instantiation
    if not verify_instantiation():
        success = False
    
    # Test methods
    if not verify_methods():
        success = False
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 All verifications passed! SqlServerEvaluationRepository is ready to use.")
        print("\n📝 Next steps:")
        print("1. Implement SqlServerRegistrationRepository")
        print("2. Implement SqlServerProgramRepository") 
        print("3. Test with actual database connection")
        print("4. Run the full application")
    else:
        print("❌ Some verifications failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
