#!/usr/bin/env python3
"""
Simple test to check import structure
"""

import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("Python path:", sys.path)
print("Current directory:", os.getcwd())

try:
    print("Testing basic imports...")
    
    # Test domain imports
    from domain.entities.evaluation import ConditionGroup
    print("✅ Domain entities imported")
    
    from domain.repositories.evaluation_repository import EvaluationRepository
    print("✅ Domain repository interface imported")
    
    # Test infrastructure imports
    from infrastructure.database.sql_server_connection import SqlServerConnection
    print("✅ Infrastructure database imported")
    
    from infrastructure.repositories.sql_server_evaluation_repository import SqlServerEvaluationRepository
    print("✅ Infrastructure repository imported")
    
    print("All imports successful!")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
