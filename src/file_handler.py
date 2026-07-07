import pandas as pd
import os
from typing import List, Optional
from src.models import Employee, Assignment


class FileHandler:
    """Handles file operations for Secret Santa."""
    
    @staticmethod
    def read_employees(file_path: str) -> List[Employee]:
        """
        Read employees from CSV file.
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            List of Employee objects
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is invalid
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            df = pd.read_csv(file_path)
        except Exception as e:
            raise ValueError(f"Failed to read CSV file: {e}")
        
        # Validate columns
        required_cols = ['Employee_Name', 'Employee_EmailID']
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")
        
        # Convert to Employee objects
        employees = []
        for _, row in df.iterrows():
            employees.append(
                Employee(
                    name=str(row['Employee_Name']).strip(),
                    email=str(row['Employee_EmailID']).strip()
                )
            )
        
        return employees
    
    @staticmethod
    def read_assignments(file_path: str) -> List[Assignment]:
        """
        Read assignments from CSV file.
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            List of Assignment objects
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is invalid
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            df = pd.read_csv(file_path)
        except Exception as e:
            raise ValueError(f"Failed to read CSV file: {e}")
        
        # Validate columns
        required_cols = ['Employee_Name', 'Employee_EmailID', 'Secret_Santa_Name', 'Secret_Santa_EmailID']
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")
        
        # Convert to Assignment objects
        assignments = []
        for _, row in df.iterrows():
            giver = Employee(
                name=str(row['Employee_Name']).strip(),
                email=str(row['Employee_EmailID']).strip()
            )
            receiver = Employee(
                name=str(row['Secret_Santa_Name']).strip(),
                email=str(row['Secret_Santa_EmailID']).strip()
            )
            assignments.append(Assignment(giver, receiver))
        
        return assignments
    
    @staticmethod
    def write_assignments(assignments: List[Assignment], file_path: str) -> None:
        """
        Write assignments to CSV file.
        
        Args:
            assignments: List of Assignment objects
            file_path: Path to output CSV file
            
        Raises:
            ValueError: If assignments is empty
        """
        if not assignments:
            raise ValueError("No assignments to write")
        
        # Create directory if needed
        os.makedirs(os.path.dirname(file_path) or '.', exist_ok=True)
        
        # Convert to DataFrame
        data = [a.to_dict() for a in assignments]
        df = pd.DataFrame(data)
        
        # Ensure correct column order
        columns = ['Employee_Name', 'Employee_EmailID', 'Secret_Santa_Name', 'Secret_Santa_EmailID']
        df = df[columns]
        
        # Write to file
        df.to_csv(file_path, index=False)