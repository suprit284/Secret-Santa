import os
from datetime import datetime
from typing import Optional, List
from src.models import Employee, Assignment
from src.assigner import SecretSantaAssigner
from src.file_handler import FileHandler
from src.validators import AssignmentValidator


class SecretSantaApp:
    """Main application for Secret Santa."""
    
    def __init__(self):
        self.assigner = SecretSantaAssigner()
        self.file_handler = FileHandler()
        self.validator = AssignmentValidator()
    
    def run(self, employees_file: str, output_file: str, previous_file: Optional[str] = None) -> None:
        """
        Run the Secret Santa assignment.
        
        Args:
            employees_file: Path to employees CSV
            output_file: Path to output CSV
            previous_file: Optional path to previous year's assignments
        """
        try:
            # Step 1: Read employees
            print(f"📂 Reading employees from: {employees_file}")
            employees = self.file_handler.read_employees(employees_file)
            print(f"✅ Loaded {len(employees)} employees")
            
            # Step 2: Read previous assignments (if provided)
            previous_assignments = None
            if previous_file and os.path.exists(previous_file):
                print(f"📂 Reading previous assignments from: {previous_file}")
                previous_assignments = self.file_handler.read_assignments(previous_file)
                print(f"✅ Loaded {len(previous_assignments)} previous assignments")
            
            # Step 3: Generate new assignments
            print("🎄 Generating Secret Santa assignments...")
            assignments = self.assigner.assign(employees, previous_assignments)
            print(f"✅ Generated {len(assignments)} assignments")
            
            # Step 4: Validate assignments
            self.validator.validate_assignments(assignments, employees)
            print("✅ All constraints validated")
            
            # Step 5: Write assignments
            self.file_handler.write_assignments(assignments, output_file)
            print(f"✅ Assignments saved to: {output_file}")
            
            # Step 6: Print summary
            self._print_summary(assignments, employees, previous_assignments)
            
        except Exception as e:
            print(f"❌ Error: {e}")
            raise
    
    def _print_summary(self, assignments: List[Assignment], employees: List[Employee], 
                      previous_assignments: Optional[List[Assignment]] = None) -> None:
        """Print assignment summary."""
        print("\n" + "="*70)
        print("🎄 SECRET SANTA ASSIGNMENTS COMPLETE 🎄")
        print("="*70)
        
        print(f"\n📊 Statistics:")
        print(f"   Total employees: {len(employees)}")
        print(f"   Total assignments: {len(assignments)}")
        
        # Check constraints
        giver_set = set(a.giver.email for a in assignments)
        receiver_set = set(a.receiver.email for a in assignments)
        
        print(f"\n✅ Constraint Verification:")
        print(f"   Unique givers: {len(giver_set)}")
        print(f"   Unique receivers: {len(receiver_set)}")
        print(f"   No self-assignment: {all(a.giver.email != a.receiver.email for a in assignments)}")
        
        # Check previous year repeats
        if previous_assignments:
            prev_lookup = {a.giver.email: a.receiver.email for a in previous_assignments}
            repeats = 0
            repeat_details = []
            for a in assignments:
                if a.giver.email in prev_lookup and prev_lookup[a.giver.email] == a.receiver.email:
                    repeats += 1
                    repeat_details.append(a.giver.name)
            
            if repeats > 0:
                print(f"   ⚠️  Repeats from last year: {repeats} ({', '.join(repeat_details)})")
            else:
                print(f"   ✅ No repeats from last year")
        
        print("\n📊 Assignments:")
        print("-"*70)
        for i, assignment in enumerate(assignments, 1):
            print(f"{i:2}. {assignment.giver.name:20} → {assignment.receiver.name}")
        print("-"*70)


def main():
    """CLI entry point."""
    # Configuration
    EMPLOYEES_FILE = r"C:\Users\samko\Downloads\Employee-List.csv"
    PREVIOUS_FILE = r"C:\Users\samko\Downloads\secret_santa_assignments_20260707_115929.csv"
    OUTPUT_DIR = r"C:\Users\samko\Downloads"
    
    try:
        # Create output file with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"{OUTPUT_DIR}/secret_santa_assignments_{timestamp}.csv"
        
        # Run application
        app = SecretSantaApp()
        app.run(EMPLOYEES_FILE, output_file, PREVIOUS_FILE)
        
    except FileNotFoundError as e:
        print(f"❌ File not found: {e}")
        return 1
    except ValueError as e:
        print(f"❌ Validation error: {e}")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())