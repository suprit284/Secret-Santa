import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.models import Employee, Assignment
from src.assigner import SecretSantaAssigner


class TestSecretSantaAssigner:
    """Tests for SecretSantaAssigner."""
    
    def setup_method(self):
        self.assigner = SecretSantaAssigner()
        self.employees = [
            Employee("John", "john@co.com"),
            Employee("Jane", "jane@co.com"),
            Employee("Bob", "bob@co.com"),
            Employee("Alice", "alice@co.com")
        ]
    
    def test_assign_valid(self):
        """Test valid assignment generation."""
        assignments = self.assigner.assign(self.employees)
        
        assert len(assignments) == len(self.employees)
        assert all(a.giver.email != a.receiver.email for a in assignments)
        
        # Check one-to-one mapping
        givers = {a.giver.email for a in assignments}
        receivers = {a.receiver.email for a in assignments}
        assert givers == set(e.email for e in self.employees)
        assert receivers == set(e.email for e in self.employees)
    
    def test_assign_with_previous(self):
        """Test assignment with previous year's data."""
        previous_assignments = [
            Assignment(self.employees[0], self.employees[1]),
            Assignment(self.employees[1], self.employees[2]),
            Assignment(self.employees[2], self.employees[3]),
            Assignment(self.employees[3], self.employees[0])
        ]
        
        assignments = self.assigner.assign(self.employees, previous_assignments)
        
        # Check no repeats from previous year
        prev_lookup = {a.giver.email: a.receiver.email for a in previous_assignments}
        for a in assignments:
            if a.giver.email in prev_lookup:
                assert a.receiver.email != prev_lookup[a.giver.email]
    
    def test_assign_without_self_assignment(self):
        """Test that no self-assignment occurs."""
        for _ in range(10):  # Test multiple times
            assignments = self.assigner.assign(self.employees)
            for a in assignments:
                assert a.giver.email != a.receiver.email
    
    def test_assign_all_employees_included(self):
        """Test all employees are included as givers and receivers."""
        assignments = self.assigner.assign(self.employees)
        
        employee_emails = set(e.email for e in self.employees)
        giver_emails = set(a.giver.email for a in assignments)
        receiver_emails = set(a.receiver.email for a in assignments)
        
        assert employee_emails == giver_emails
        assert employee_emails == receiver_emails
    
    def test_assign_single_employee(self):
        """Test with single employee (should raise error)."""
        employees = [Employee("John", "john@co.com")]
        
        with pytest.raises(ValueError, match="Could not find valid assignment"):
            self.assigner.assign(employees)
    
    def test_assign_empty_employees(self):
        """Test with empty employee list."""
        with pytest.raises(ValueError, match="Employee list cannot be empty"):
            self.assigner.assign([])