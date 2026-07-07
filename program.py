import pandas as pd
import random
from datetime import datetime
import os
from typing import Optional, Dict, List


class SecretSantaAssigner:
    """
    Secret Santa assignment engine with guaranteed constraints:
    1. No employee can be their own Secret Santa
    2. Each employee has exactly one Secret Santa (one-to-one)
    3. No repeat from previous year (if previous data provided)
    """
    
    def __init__(self, employees_file: str, previous_assignments_file: Optional[str] = None):
        """
        Initialize the assigner.
        
        Args:
            employees_file: Path to CSV with Employee_Name and Employee_EmailID
            previous_assignments_file: Optional path to previous year's assignments CSV
        """
        self.employees_df = pd.read_csv(employees_file)
        self.previous_assignments = None
        
        if previous_assignments_file and os.path.exists(previous_assignments_file):
            self.previous_assignments = pd.read_csv(previous_assignments_file)
        
        self._validate_data()
    
    def _validate_data(self) -> None:
        """Validate input data structure and integrity."""
        required_cols = ['Employee_Name', 'Employee_EmailID']
        
        for col in required_cols:
            if col not in self.employees_df.columns:
                raise ValueError(f"Missing required column: {col}")
        
        if self.employees_df['Employee_EmailID'].duplicated().any():
            raise ValueError("Duplicate Employee_EmailID found")
        
        if self.employees_df.empty:
            raise ValueError("Employee file is empty")
        
        # Store employee list for reuse
        self.employee_list = self.employees_df.to_dict('records')
        self.employee_emails = [e['Employee_EmailID'] for e in self.employee_list]
    
    def _get_previous_dict(self) -> Dict[str, str]:
        """Convert previous assignments to lookup dictionary."""
        if self.previous_assignments is None:
            return {}
        
        # Ensure previous file has the required columns
        if 'Secret_Santa_EmailID' not in self.previous_assignments.columns:
            raise ValueError("Previous assignments file must have 'Secret_Santa_EmailID' column")
        
        return dict(zip(
            self.previous_assignments['Employee_EmailID'],
            self.previous_assignments['Secret_Santa_EmailID']
        ))
    
    def assign(self) -> pd.DataFrame:
        """
        Generate Secret Santa assignments using a robust algorithm.
        
        Algorithm:
        1. Create a list of all employees
        2. Shuffle the list randomly
        3. Use a rotation method with constraints
        4. Ensure no self-assignment and one-to-one mapping
        
        Returns:
            DataFrame with columns: Employee_Name, Employee_EmailID,
                                   Secret_Santa_Name, Secret_Santa_EmailID
        """
        employees = self.employee_list.copy()
        prev_dict = self._get_previous_dict()
        
        # Shuffle for randomization
        random.shuffle(employees)
        
        # Get all employee emails
        all_emails = [e['Employee_EmailID'] for e in employees]
        n = len(employees)
        
        # Try different rotations to avoid self-assignment and previous year repeats
        for offset in range(1, n):
            # Create a rotated list
            rotated = all_emails[offset:] + all_emails[:offset]
            
            # Check if this rotation works
            valid = True
            for i, giver in enumerate(employees):
                recipient_email = rotated[i]
                
                # Constraint 1: No self-assignment
                if giver['Employee_EmailID'] == recipient_email:
                    valid = False
                    break
                
                # Constraint 2: No previous year repeat
                if giver['Employee_EmailID'] in prev_dict:
                    if prev_dict[giver['Employee_EmailID']] == recipient_email:
                        valid = False
                        break
            
            if valid:
                # This rotation works, create assignments
                assignments = []
                for i, giver in enumerate(employees):
                    recipient_email = rotated[i]
                    recipient = self._get_employee_by_email(recipient_email)
                    
                    assignments.append({
                        'Employee_Name': giver['Employee_Name'],
                        'Employee_EmailID': giver['Employee_EmailID'],
                        'Secret_Santa_Name': recipient['Employee_Name'],
                        'Secret_Santa_EmailID': recipient['Employee_EmailID']
                    })
                
                # Validate before returning
                self._validate_assignments(assignments)
                return pd.DataFrame(assignments)
        
        # If no rotation worked, try a different shuffle
        # This should rarely happen, but as a fallback, do a direct shuffle with validation
        for attempt in range(100):  # Try 100 times
            random.shuffle(employees)
            all_emails = [e['Employee_EmailID'] for e in employees]
            
            # Create a simple rotation
            rotated = all_emails[1:] + all_emails[:1]  # Shift by 1
            
            valid = True
            for i, giver in enumerate(employees):
                recipient_email = rotated[i]
                
                if giver['Employee_EmailID'] == recipient_email:
                    valid = False
                    break
                
                if giver['Employee_EmailID'] in prev_dict:
                    if prev_dict[giver['Employee_EmailID']] == recipient_email:
                        valid = False
                        break
            
            if valid:
                assignments = []
                for i, giver in enumerate(employees):
                    recipient_email = rotated[i]
                    recipient = self._get_employee_by_email(recipient_email)
                    
                    assignments.append({
                        'Employee_Name': giver['Employee_Name'],
                        'Employee_EmailID': giver['Employee_EmailID'],
                        'Secret_Santa_Name': recipient['Employee_Name'],
                        'Secret_Santa_EmailID': recipient['Employee_EmailID']
                    })
                
                self._validate_assignments(assignments)
                return pd.DataFrame(assignments)
        
        # If we still can't find a valid assignment, raise an error
        raise RuntimeError("Could not find valid assignment with all constraints")
    
    def _get_employee_by_email(self, email: str) -> Dict:
        """Get employee details by email."""
        for emp in self.employee_list:
            if emp['Employee_EmailID'] == email:
                return emp
        raise ValueError(f"Employee not found with email: {email}")
    
    def _validate_assignments(self, assignments: List[Dict]) -> None:
        """
        Validate that all constraints are satisfied.
        
        Constraints checked:
        1. No self-assignment
        2. Each employee gives exactly once
        3. Each employee receives exactly once
        """
        # Check 1: No self-assignment
        for assignment in assignments:
            if assignment['Employee_EmailID'] == assignment['Secret_Santa_EmailID']:
                raise RuntimeError(f"❌ Self-assignment detected for {assignment['Employee_Name']}")
        
        # Check 2: Each employee gives exactly once
        givers = [a['Employee_EmailID'] for a in assignments]
        if len(givers) != len(set(givers)):
            raise RuntimeError("❌ Duplicate givers found - each employee should give exactly once")
        
        # Check 3: Each employee receives exactly once
        recipients = [a['Secret_Santa_EmailID'] for a in assignments]
        if len(recipients) != len(set(recipients)):
            raise RuntimeError("❌ Duplicate recipients found - each employee should receive exactly once")
        
        # Check 4: All employees from input are in assignments
        all_employees = set(self.employee_emails)
        assigned_givers = set(givers)
        assigned_recipients = set(recipients)
        
        if all_employees != assigned_givers:
            missing = all_employees - assigned_givers
            raise RuntimeError(f"❌ Missing givers: {missing}")
        
        if all_employees != assigned_recipients:
            missing = all_employees - assigned_recipients
            raise RuntimeError(f"❌ Missing recipients: {missing}")
        
        print("✅ All constraints validated successfully!")
        print(f"   - No self-assignments: ✅")
        print(f"   - Each employee gives exactly once: ✅")
        print(f"   - Each employee receives exactly once: ✅")
    
    def save_assignments(self, output_file: str) -> pd.DataFrame:
        """
        Generate and save assignments to CSV.
        
        Args:
            output_file: Path for output CSV
            
        Returns:
            DataFrame with assignments
        """
        os.makedirs(os.path.dirname(output_file) or '.', exist_ok=True)
        
        assignments = self.assign()
        assignments.to_csv(output_file, index=False)
        
        print(f"✅ Assignments saved to: {output_file}")
        print(f"📊 Total employees: {len(assignments)}")
        
        return assignments


def main():
    """CLI entry point."""
    
    # ============================================
    # CONFIGURATION - UPDATE THESE PATHS
    # ============================================
    
    # Input CSV file
    EMPLOYEES_CSV = r"C:\Users\samko\Downloads\Employee-List.csv"
    
    # Optional: Previous year's assignments CSV (if you have one)
    PREVIOUS_FILE = r"C:\Users\samko\Downloads\secret_santa_assignments_20260707_115929.csv"
    
    # Output directory
    OUTPUT_DIR = r"C:\Users\samko\Downloads"
    
    # ============================================
    # SCRIPT EXECUTION
    # ============================================
    
    try:
        # Check if input file exists
        if not os.path.exists(EMPLOYEES_CSV):
            print(f"❌ CSV file not found: {EMPLOYEES_CSV}")
            print("Please ensure the CSV file exists or check the path.")
            return 1
        
        print(f"📂 Reading employee data from: {EMPLOYEES_CSV}")
        
        # Initialize assigner
        assigner = SecretSantaAssigner(EMPLOYEES_CSV, PREVIOUS_FILE)
        
        # Generate assignments
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"{OUTPUT_DIR}/secret_santa_assignments_{timestamp}.csv"
        
        result = assigner.save_assignments(output_file)
        
        # Print summary
        print("\n" + "="*70)
        print("🎄 SECRET SANTA ASSIGNMENTS COMPLETE 🎄")
        print("="*70)
        
        # Display statistics
        print("\n📊 Constraint Verification:")
        print(f"   ✅ Total employees: {len(result)}")
        print(f"   ✅ Unique givers: {len(result['Employee_EmailID'].unique())}")
        print(f"   ✅ Unique recipients: {len(result['Secret_Santa_EmailID'].unique())}")
        print(f"   ✅ No self-assignments: {not (result['Employee_EmailID'] == result['Secret_Santa_EmailID']).any()}")
        
        # Check for previous year repeats
        if PREVIOUS_FILE and os.path.exists(PREVIOUS_FILE):
            prev_df = pd.read_csv(PREVIOUS_FILE)
            repeats = 0
            repeat_details = []
            for _, row in result.iterrows():
                prev_match = prev_df[prev_df['Employee_EmailID'] == row['Employee_EmailID']]
                if not prev_match.empty:
                    if prev_match.iloc[0]['Secret_Santa_EmailID'] == row['Secret_Santa_EmailID']:
                        repeats += 1
                        repeat_details.append(row['Employee_Name'])
            
            if repeats > 0:
                print(f"   ⚠️  {repeats} assignments repeated from last year: {repeat_details}")
            else:
                print(f"   ✅ No repeats from last year's assignments")
        
        print(f"\n📁 Output CSV: {output_file}")
        print("\n📊 All Assignments:")
        print(result.to_string(index=False))
        
        # Verification matrix
        print("\n" + "="*70)
        print("🔍 VERIFICATION MATRIX")
        print("="*70)
        
        giver_set = set(result['Employee_EmailID'])
        recipient_set = set(result['Secret_Santa_EmailID'])
        
        print(f"Total Givers: {len(giver_set)}")
        print(f"Total Recipients: {len(recipient_set)}")
        
        # Check if giver and recipient sets match
        if giver_set == recipient_set:
            print("✅ Giver and Recipient sets match perfectly!")
        
        # Check for self-assignment again
        self_assignments = result[result['Employee_EmailID'] == result['Secret_Santa_EmailID']]
        if len(self_assignments) > 0:
            print(f"❌ ERROR: {len(self_assignments)} self-assignments found!")
            print(self_assignments)
        else:
            print("✅ No self-assignments found!")
        
        print("\n" + "="*70)
        print("✨ Done! All constraints satisfied.")
        
    except FileNotFoundError as e:
        print(f"❌ File not found: {e}")
        return 1
    except ValueError as e:
        print(f"❌ Data validation error: {e}")
        return 1
    except RuntimeError as e:
        print(f"❌ Constraint violation: {e}")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())