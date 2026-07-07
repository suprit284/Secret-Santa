import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.models import Employee, Assignment
from src.validators import AssignmentValidator


class TestAssignmentValidator:
    """Tests for AssignmentValidator."""
    
    def setup_method(self):
        self.validator = AssignmentValidator()
        self.employees = [
            Employee("John", "john@co.com"),
            Employee("Jane", "jane@co.com"),
            Employee("Bob", "bob@co.com")
        ]
    
    def test_validate_employees_valid(self):
        """Test valid employee list."""
        self.validator.validate_employees(self.employees)
    
    def test_validate_employees_empty(self):
        """Test empty employee list."""
        with pytest.raises(ValueError, match="Employee list cannot be empty"):
            self.validator.validate_employees([])
    
    def test_validate_employees_duplicate_email(self):
        """Test duplicate email in employee list."""
        employees = [
            Employee("John", "john@co.com"),
            Employee("Jane", "john@co.com")  # Duplicate email
        ]
        with pytest.raises(ValueError, match="Duplicate employee emails found"):
            self.validator.validate_employees(employees)
    
    def test_validate_assignments_valid(self):
        """Test valid assignments."""
        assignments = [
            Assignment(self.employees[0], self.employees[1]),
            Assignment(self.employees[1], self.employees[2]),
            Assignment(self.employees[2], self.employees[0])
        ]
        self.validator.validate_assignments(assignments, self.employees)
    
    def test_validate_assignments_self_assignment(self):
        """Test self-assignment validation."""
        assignments = [
            Assignment(self.employees[0], self.employees[0]),  # Self assignment
            Assignment(self.employees[1], self.employees[2]),
            Assignment(self.employees[2], self.employees[1])
        ]
        with pytest.raises(ValueError, match="Self-assignment detected"):
            self.validator.validate_assignments(assignments, self.employees)
    
    def test_validate_assignments_duplicate_giver(self):
        """Test duplicate giver validation."""
        assignments = [
            Assignment(self.employees[0], self.employees[1]),
            Assignment(self.employees[0], self.employees[2]),  # Duplicate giver
            Assignment(self.employees[2], self.employees[1])
        ]
        with pytest.raises(ValueError, match="Duplicate givers found"):
            self.validator.validate_assignments(assignments, self.employees)
    
    def test_validate_assignments_duplicate_receiver(self):
        """Test duplicate receiver validation."""
        assignments = [
            Assignment(self.employees[0], self.employees[1]),
            Assignment(self.employees[1], self.employees[2]),
            Assignment(self.employees[2], self.employees[1])  # Duplicate receiver
        ]
        with pytest.raises(ValueError, match="Duplicate receivers found"):
            self.validator.validate_assignments(assignments, self.employees)