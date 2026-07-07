import pytest
import tempfile
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
from src.models import Employee, Assignment
from src.assigner import SecretSantaAssigner
from src.file_handler import FileHandler
from src.validators import AssignmentValidator
from src.main import SecretSantaApp


class TestIntegration:
    """Integration tests for the complete workflow."""
    
    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.employees_file = os.path.join(self.temp_dir, "employees.csv")
        self.output_file = os.path.join(self.temp_dir, "output.csv")
        self.previous_file = os.path.join(self.temp_dir, "previous.csv")
        
        # Create test employees
        data = {
            'Employee_Name': ['John', 'Jane', 'Bob', 'Alice', 'Charlie'],
            'Employee_EmailID': ['john@co.com', 'jane@co.com', 'bob@co.com', 
                               'alice@co.com', 'charlie@co.com']
        }
        pd.DataFrame(data).to_csv(self.employees_file, index=False)
    
    def teardown_method(self):
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_full_workflow_no_previous(self):
        """Test full workflow without previous assignments."""
        app = SecretSantaApp()
        app.run(self.employees_file, self.output_file, None)
        
        assert os.path.exists(self.output_file)
        df = pd.read_csv(self.output_file)
        assert len(df) == 5
        assert list(df.columns) == ['Employee_Name', 'Employee_EmailID', 
                                    'Secret_Santa_Name', 'Secret_Santa_EmailID']
        
        # Verify no self-assignments
        assert (df['Employee_EmailID'] != df['Secret_Santa_EmailID']).all()
        
        # Verify one-to-one mapping
        assert len(df['Employee_EmailID'].unique()) == 5
        assert len(df['Secret_Santa_EmailID'].unique()) == 5
    
    def test_full_workflow_with_previous(self):
        """Test full workflow with previous assignments."""
        # Create previous assignments
        prev_data = {
            'Employee_Name': ['John', 'Jane', 'Bob', 'Alice', 'Charlie'],
            'Employee_EmailID': ['john@co.com', 'jane@co.com', 'bob@co.com', 
                               'alice@co.com', 'charlie@co.com'],
            'Secret_Santa_Name': ['Jane', 'Bob', 'Alice', 'Charlie', 'John'],
            'Secret_Santa_EmailID': ['jane@co.com', 'bob@co.com', 'alice@co.com', 
                                   'charlie@co.com', 'john@co.com']
        }
        pd.DataFrame(prev_data).to_csv(self.previous_file, index=False)
        
        app = SecretSantaApp()
        app.run(self.employees_file, self.output_file, self.previous_file)
        
        assert os.path.exists(self.output_file)
        df = pd.read_csv(self.output_file)
        
        # Verify no repeats from previous year
        prev_lookup = {
            row['Employee_EmailID']: row['Secret_Santa_EmailID']
            for _, row in pd.read_csv(self.previous_file).iterrows()
        }
        
        for _, row in df.iterrows():
            if row['Employee_EmailID'] in prev_lookup:
                assert row['Secret_Santa_EmailID'] != prev_lookup[row['Employee_EmailID']]
    
    def test_invalid_employees_file(self):
        """Test with invalid employees file."""
        app = SecretSantaApp()
        with pytest.raises(FileNotFoundError):
            app.run("non_existent.csv", self.output_file, None)