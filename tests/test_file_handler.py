import pytest
import tempfile
import os
import pandas as pd
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.models import Employee, Assignment
from src.file_handler import FileHandler


class TestFileHandler:
    """Tests for FileHandler."""
    
    def setup_method(self):
        self.file_handler = FileHandler()
        self.temp_dir = tempfile.mkdtemp()
        
        self.employees = [
            Employee("John", "john@co.com"),
            Employee("Jane", "jane@co.com"),
            Employee("Bob", "bob@co.com")
        ]
    
    def teardown_method(self):
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_read_employees_valid(self):
        """Test reading valid employee CSV."""
        file_path = os.path.join(self.temp_dir, "employees.csv")
        data = {
            'Employee_Name': ['John', 'Jane', 'Bob'],
            'Employee_EmailID': ['john@co.com', 'jane@co.com', 'bob@co.com']
        }
        pd.DataFrame(data).to_csv(file_path, index=False)
        
        employees = self.file_handler.read_employees(file_path)
        assert len(employees) == 3
        assert employees[0].name == "John"
        assert employees[0].email == "john@co.com"
    
    def test_read_employees_missing_file(self):
        """Test reading non-existent file."""
        with pytest.raises(FileNotFoundError):
            self.file_handler.read_employees("non_existent.csv")
    
    def test_read_employees_invalid_columns(self):
        """Test reading CSV with missing columns."""
        file_path = os.path.join(self.temp_dir, "invalid.csv")
        data = {'Name': ['John'], 'Email': ['john@co.com']}
        pd.DataFrame(data).to_csv(file_path, index=False)
        
        with pytest.raises(ValueError, match="Missing required column"):
            self.file_handler.read_employees(file_path)
    
    def test_write_assignments_valid(self):
        """Test writing assignments to CSV."""
        assignments = [
            Assignment(self.employees[0], self.employees[1]),
            Assignment(self.employees[1], self.employees[2]),
            Assignment(self.employees[2], self.employees[0])
        ]
        
        file_path = os.path.join(self.temp_dir, "assignments.csv")
        self.file_handler.write_assignments(assignments, file_path)
        
        assert os.path.exists(file_path)
        
        df = pd.read_csv(file_path)
        assert len(df) == 3
        assert list(df.columns) == ['Employee_Name', 'Employee_EmailID', 
                                    'Secret_Santa_Name', 'Secret_Santa_EmailID']
    
    def test_write_assignments_empty(self):
        """Test writing empty assignments."""
        with pytest.raises(ValueError, match="No assignments to write"):
            self.file_handler.write_assignments([], "output.csv")