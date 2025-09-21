"""
Domain Entities - Core Business Objects
Các thực thể Domain - Đối tượng nghiệp vụ cốt lõi
"""

from .customer import Customer
from .program import Program, RegisterItem
from .evaluation import ConditionGroup, ConditionItem, AuditPicture, CustomerEvaluationResult
from .registration import Registration

__all__ = [
    'Customer',
    'Program', 
    'RegisterItem',
    'ConditionGroup',
    'ConditionItem', 
    'AuditPicture',
    'CustomerEvaluationResult',
    'Registration'
]
