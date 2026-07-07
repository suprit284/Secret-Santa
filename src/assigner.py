import random
from typing import List, Dict, Optional, Tuple
from src.models import Employee, Assignment
from src.validators import AssignmentValidator


class SecretSantaAssigner:
    """Secret Santa assignment engine."""
    
    def __init__(self):
        self.validator = AssignmentValidator()
    
    def assign(self, employees: List[Employee], previous_assignments: Optional[List[Assignment]] = None) -> List[Assignment]:
        """
        Generate Secret Santa assignments with all constraints.
        
        Args:
            employees: List of Employee objects
            previous_assignments: Optional list of previous year's assignments
            
        Returns:
            List of Assignment objects
            
        Raises:
            ValueError: If no valid assignment found
        """
        # Validate input
        self.validator.validate_employees(employees)
        if previous_assignments:
            self.validator.validate_previous_assignments(previous_assignments, employees)
        
        # Build previous assignments lookup
        prev_lookup = {}
        if previous_assignments:
            prev_lookup = {a.giver.email: a.receiver.email for a in previous_assignments}
        
        # Try to find a valid assignment
        for attempt in range(100):  # Try 100 times
            shuffled = employees.copy()
            random.shuffle(shuffled)
            
            assignments = self._try_assign(shuffled, prev_lookup)
            
            if assignments:
                try:
                    self.validator.validate_assignments(assignments, employees)
                    return assignments
                except ValueError:
                    continue  # Try again
        
        raise ValueError("Could not find valid assignment after 100 attempts")
    
    def _try_assign(self, employees: List[Employee], prev_lookup: Dict[str, str]) -> Optional[List[Assignment]]:
        """
        Try to assign using rotation method.
        
        Args:
            employees: Shuffled list of employees
            prev_lookup: Previous year's assignments lookup
            
        Returns:
            List of assignments or None if invalid
        """
        n = len(employees)
        emails = [emp.email for emp in employees]
        
        # Try different rotations
        for offset in range(1, n):
            rotated = emails[offset:] + emails[:offset]
            
            valid = True
            for i, giver in enumerate(employees):
                receiver_email = rotated[i]
                
                # Check self-assignment
                if giver.email == receiver_email:
                    valid = False
                    break
                
                # Check previous year repeat
                if giver.email in prev_lookup and prev_lookup[giver.email] == receiver_email:
                    valid = False
                    break
            
            if valid:
                # Create assignments
                assignments = []
                for i, giver in enumerate(employees):
                    receiver_email = rotated[i]
                    receiver = self._find_employee_by_email(employees, receiver_email)
                    assignments.append(Assignment(giver, receiver))
                return assignments
        
        return None
    
    def _find_employee_by_email(self, employees: List[Employee], email: str) -> Employee:
        """Find employee by email."""
        for emp in employees:
            if emp.email == email:
                return emp
        raise ValueError(f"Employee not found with email: {email}")