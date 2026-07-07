from typing import List, Dict, Optional
from src.models import Employee, Assignment


class AssignmentValidator:
    """Validator for Secret Santa assignments."""
    
    @staticmethod
    def validate_employees(employees: List[Employee]) -> None:
        """
        Validate employee list.
        
        Args:
            employees: List of Employee objects
            
        Raises:
            ValueError: If validation fails
        """
        if not employees:
            raise ValueError("Employee list cannot be empty")
        
        # Check for duplicate emails
        emails = [emp.email for emp in employees]
        if len(emails) != len(set(emails)):
            raise ValueError("Duplicate employee emails found")
        
        # Check for empty names or emails
        for emp in employees:
            if not emp.name or not emp.name.strip():
                raise ValueError(f"Employee with email {emp.email} has empty name")
            if not emp.email or not emp.email.strip():
                raise ValueError(f"Employee with name {emp.name} has empty email")
    
    @staticmethod
    def validate_assignments(assignments: List[Assignment], employees: List[Employee]) -> None:
        """
        Validate assignments against constraints.
        
        Constraints:
        1. No self-assignment
        2. One-to-one mapping (each employee gives exactly once)
        3. One-to-one mapping (each employee receives exactly once)
        4. All employees are included
        
        Args:
            assignments: List of Assignment objects
            employees: List of all Employee objects
            
        Raises:
            ValueError: If validation fails
        """
        if not assignments:
            raise ValueError("Assignments list cannot be empty")
        
        if len(assignments) != len(employees):
            raise ValueError(f"Number of assignments ({len(assignments)}) does not match employees ({len(employees)})")
        
        # Check 1: No self-assignment
        for assignment in assignments:
            if assignment.giver.email == assignment.receiver.email:
                raise ValueError(f"Self-assignment detected for {assignment.giver.name}")
        
        # Check 2: Each employee gives exactly once
        givers = [a.giver.email for a in assignments]
        if len(givers) != len(set(givers)):
            duplicate_givers = [email for email in set(givers) if givers.count(email) > 1]
            raise ValueError(f"Duplicate givers found: {duplicate_givers}")
        
        # Check 3: Each employee receives exactly once
        receivers = [a.receiver.email for a in assignments]
        if len(receivers) != len(set(receivers)):
            duplicate_receivers = [email for email in set(receivers) if receivers.count(email) > 1]
            raise ValueError(f"Duplicate receivers found: {duplicate_receivers}")
        
        # Check 4: All employees are included as givers and receivers
        all_emails = set(emp.email for emp in employees)
        giver_emails = set(givers)
        receiver_emails = set(receivers)
        
        if all_emails != giver_emails:
            missing = all_emails - giver_emails
            raise ValueError(f"Missing givers: {missing}")
        
        if all_emails != receiver_emails:
            missing = all_emails - receiver_emails
            raise ValueError(f"Missing receivers: {missing}")
    
    @staticmethod
    def validate_previous_assignments(prev_assignments: List[Assignment], employees: List[Employee]) -> None:
        """
        Validate previous year's assignments.
        
        Args:
            prev_assignments: List of previous Assignment objects
            employees: List of all Employee objects
            
        Raises:
            ValueError: If validation fails
        """
        if not prev_assignments:
            return
        
        # Check if previous assignments cover all employees
        prev_givers = [a.giver.email for a in prev_assignments]
        prev_receivers = [a.receiver.email for a in prev_assignments]
        
        all_emails = set(emp.email for emp in employees)
        
        if set(prev_givers) != all_emails:
            missing = all_emails - set(prev_givers)
            raise ValueError(f"Previous assignments missing givers: {missing}")
        
        if set(prev_receivers) != all_emails:
            missing = all_emails - set(prev_receivers)
            raise ValueError(f"Previous assignments missing receivers: {missing}")