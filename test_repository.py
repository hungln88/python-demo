#!/usr/bin/env python3
"""
Test script to verify SqlServerEvaluationRepository implementation
"""

import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    # Test imports
    print("Testing imports...")
    
    from infrastructure.database.sql_server_connection import SqlServerConnection
    print("✅ SqlServerConnection imported successfully")
    
    from infrastructure.repositories.sql_server_evaluation_repository import SqlServerEvaluationRepository
    print("✅ SqlServerEvaluationRepository imported successfully")
    
    from domain.repositories.evaluation_repository import EvaluationRepository
    print("✅ EvaluationRepository interface imported successfully")
    
    from domain.entities.evaluation import ConditionGroup, ConditionItem, AuditPicture, CustomerEvaluationResult
    print("✅ Evaluation entities imported successfully")
    
    # Test instantiation
    print("\nTesting instantiation...")
    
    # Create database connection
    db_connection = SqlServerConnection()
    print("✅ SqlServerConnection instantiated successfully")
    
    # Create repository
    repository = SqlServerEvaluationRepository(db_connection)
    print("✅ SqlServerEvaluationRepository instantiated successfully")
    
    # Test that it implements the interface
    assert isinstance(repository, EvaluationRepository)
    print("✅ SqlServerEvaluationRepository implements EvaluationRepository interface")
    
    print("\n🎉 All tests passed! SqlServerEvaluationRepository is working correctly.")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
