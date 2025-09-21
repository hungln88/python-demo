"""
Domain Repository Interfaces - Abstract Contracts
Giao diện Repository Domain - Hợp đồng trừu tượng
"""

from .customer_repository import CustomerRepository
from .program_repository import ProgramRepository
from .evaluation_repository import EvaluationRepository
from .registration_repository import RegistrationRepository

__all__ = [
    'CustomerRepository',
    'ProgramRepository', 
    'EvaluationRepository',
    'RegistrationRepository'
]
