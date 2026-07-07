from dataclasses import dataclass
from typing import Optional

@dataclass
class Employee:
    """Employee data model."""
    name: str
    email: str
    
    def __hash__(self):
        return hash(self.email)
    
    def __eq__(self, other):
        if isinstance(other, Employee):
            return self.email == other.email
        return False

@dataclass
class Assignment:
    """Secret Santa assignment model."""
    giver: Employee
    receiver: Employee
    
    def to_dict(self):
        return {
            'Employee_Name': self.giver.name,
            'Employee_EmailID': self.giver.email,
            'Secret_Santa_Name': self.receiver.name,
            'Secret_Santa_EmailID': self.receiver.email
        }