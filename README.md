# 🎄 Secret Santa 

A modular, production-ready Python application for assigning Secret Santa pairs with guaranteed constraints. Perfect for office Secret Santa events, family gift exchanges, or any scenario requiring fair, random pair assignments.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![pytest](https://img.shields.io/badge/pytest-7.0+-green.svg)](https://docs.pytest.org/)
[![Code Style](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)

## 📋 Table of Contents

- [Features](#-features)
- [Problem Statement](#-problem-statement)
- [Project Structure](#-project-structure)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Usage](#-usage)
- [Input/Output Format](#-inputoutput-format)
- [Visual Diagrams](#visual-diagrams)


## ✨ Features

- ✅ **No Self-Assignment**: Guarantees no employee is assigned to themselves
- ✅ **One-to-One Mapping**: Each employee gives exactly once and receives exactly once
- ✅ **No Repeats**: Prevents assigning the same Secret Santa pair as the previous year
- ✅ **Modular Architecture**: Clean OOP design with separation of concerns
- ✅ **CSV Support**: Simple CSV input/output for easy integration
- ✅ **Comprehensive Testing**: Unit and integration tests with 90%+ coverage
- ✅ **Robust Validation**: Input validation and constraint enforcement
- ✅ **Error Handling**: Graceful error handling with clear messages
- ✅ **Type Hints**: Type annotations for better code clarity
- ✅ **Randomization**: Random assignments while maintaining all constraints

## 🎯 Problem Statement

Design and implement a Secret Santa assignment system that:

1. Takes a list of employees from a CSV file
2. Assigns each employee a Secret Santa recipient
3. Ensures no employee is their own Secret Santa
4. Ensures each employee gives to exactly one person
5. Ensures each employee receives from exactly one person
6. Prevents the same assignment from repeating from the previous year
7. Outputs the assignments to a CSV file with 4 columns

## 📁 Project Structure

```
secret-santa/
├── src/
│   ├── __init__.py
│   ├── models.py           # Data models (Employee, Assignment)
│   ├── validators.py       # Validation logic
│   ├── assigner.py         # Core assignment algorithm
│   ├── file_handler.py     # CSV I/O operations
│   └── main.py             # Main application
├── tests/
│   ├── __init__.py
│   ├── test_validators.py   # Validator unit tests
│   ├── test_assigner.py     # Assigner unit tests
│   ├── test_file_handler.py # File handler unit tests
│   └── test_integration.py  # End-to-end integration tests
├── requirements.txt         # Project dependencies
├── README.md               # Documentation
└── .gitignore             # Git ignore file
```


## 🏗️ Architecture

### Module Overview

The application follows clean separation of concerns with five main modules:

| Module | Purpose | Key Classes/Functions |
|--------|---------|----------------------|
| **models.py** | Data models | `Employee`, `Assignment` |
| **validators.py** | Validation logic | `AssignmentValidator` |
| **assigner.py** | Core algorithm | `SecretSantaAssigner` |
| **file_handler.py** | File operations | `FileHandler` |
| **main.py** | Application orchestration | `SecretSantaApp` |



## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Step-by-Step Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/suprit284/Secret-Santa.git
   cd secret-santa
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Mac/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify installation:**
   ```bash
   python -c "import pandas; print('✅ Pandas installed successfully')"
   ```



## 🚀 Usage

### Basic Usage

1. **Prepare your employee CSV file** with the required format (see [Input Format](#-inputformat) below)

2. **Update the configuration** in `src/main.py`:
   ```python
   EMPLOYEES_FILE = "employees.csv"  # Path to your employee CSV
   PREVIOUS_FILE = None  # Set to "previous_assignments.csv" if you have one
   OUTPUT_DIR = "outputs"  # Directory for output files
   ```

3. **Run the application:**
   ```bash
   python -m src.main
   ```

4. **Check the output** in the `outputs/` directory.

### Usage with Command Line Arguments

You can also provide file paths as command line arguments:

```bash
# Basic usage
python -m src.main employees.csv

# With previous year's assignments
python -m src.main employees.csv previous_assignments.csv

# With custom output directory
python -m src.main employees.csv previous_assignments.csv outputs/
```

### Programmatic Usage

```python
from src.main import SecretSantaApp

# Initialize application
app = SecretSantaApp()

# Run with custom parameters
app.run(
    employees_file="employees.csv",
    output_file="outputs/assignments.csv",
    previous_file="previous_assignments.csv"  # Optional
)
```

### Example Workflow

1. **Create your employee CSV** (`employees.csv`):
   ```csv
   Employee_Name,Employee_EmailID
   John Doe,john.doe@company.com
   Jane Smith,jane.smith@company.com
   Bob Johnson,bob.johnson@company.com
   Alice Williams,alice.williams@company.com
   ```

2. **Run the application:**
   ```bash
   python -m src.main
   ```

3. **Output** (`outputs/secret_santa_assignments_20260707_123456.csv`):
   ```csv
   Employee_Name,Employee_EmailID,Secret_Santa_Name,Secret_Santa_EmailID
   John Doe,john.doe@company.com,Jane Smith,jane.smith@company.com
   Jane Smith,jane.smith@company.com,Bob Johnson,bob.johnson@company.com
   Bob Johnson,bob.johnson@company.com,Alice Williams,alice.williams@company.com
   Alice Williams,alice.williams@company.com,John Doe,john.doe@company.com
   ```

### With Previous Year's Assignments

To prevent repeats from last year, provide the previous year's assignments file:

```python
# In src/main.py
EMPLOYEES_FILE = "employees.csv"
PREVIOUS_FILE = "previous_assignments.csv"  # Path to last year's assignments
OUTPUT_DIR = "outputs"
```

Or via command line:
```bash
python -m src.main employees.csv previous_assignments.csv
```

### Environment Variables

You can also use environment variables for configuration:

```bash
# Set environment variables
export EMPLOYEES_FILE="employees.csv"
export PREVIOUS_FILE="previous_assignments.csv"
export OUTPUT_DIR="outputs"

# Run the application
python -m src.main
```

### Docker Usage (Optional)

If you prefer using Docker:

```bash
# Build the image
docker build -t secret-santa .

# Run with mounted volumes
docker run -v $(pwd)/data:/app/data secret-santa python -m src.main
```



## 📊 Input/Output Format

### Input CSV Format

The input file must be a CSV with exactly **two columns**:

| Column | Description | Required |
|--------|-------------|----------|
| `Employee_Name` | Full name of the employee | ✅ Yes |
| `Employee_EmailID` | Email address (must be unique) | ✅ Yes |

**Example Input File (`employees.csv`):**

```csv
Employee_Name,Employee_EmailID
John Doe,john.doe@company.com
Jane Smith,jane.smith@company.com
Bob Johnson,bob.johnson@company.com
Alice Williams,alice.williams@company.com
Charlie Brown,charlie.brown@company.com
Diana Prince,diana.prince@company.com
```

**Validation Rules:**

| Rule | Description |
|------|-------------|
| ✅ **Header Required** | First row must be: `Employee_Name,Employee_EmailID` |
| ✅ **Unique Emails** | All email addresses must be unique |
| ✅ **Non-empty Fields** | Names and emails cannot be empty |
| ✅ **Minimum 2 Employees** | At least 2 employees required |
| ✅ **No Duplicate Names** | Duplicate names are allowed but emails must be unique |

**Common Errors and Fixes:**

| Error | Cause | Solution |
|-------|-------|----------|
| `Missing required column: Employee_Name` | Column name mismatch | Rename column to `Employee_Name` |
| `Duplicate Employee_EmailID found` | Duplicate email addresses | Remove duplicate emails |
| `Employee file is empty` | Empty CSV file | Add at least 2 employees |

### Output CSV Format

The output file contains **four columns**:

| Column | Description |
|--------|-------------|
| `Employee_Name` | Name of the giver |
| `Employee_EmailID` | Email of the giver |
| `Secret_Santa_Name` | Name of the receiver (Secret Santa) |
| `Secret_Santa_EmailID` | Email of the receiver (Secret Santa) |

**Example Output File:**

```csv
Employee_Name,Employee_EmailID,Secret_Santa_Name,Secret_Santa_EmailID
John Doe,john.doe@company.com,Diana Prince,diana.prince@company.com
Jane Smith,jane.smith@company.com,Charlie Brown,charlie.brown@company.com
Bob Johnson,bob.johnson@company.com,Alice Williams,alice.williams@company.com
Alice Williams,alice.williams@company.com,Bob Johnson,bob.johnson@company.com
Charlie Brown,charlie.brown@company.com,Jane Smith,jane.smith@company.com
Diana Prince,diana.prince@company.com,John Doe,john.doe@company.com
```

**Output Validation Guarantees:**

| Constraint | Verification |
|------------|--------------|
| ✅ No Self-Assignment | No employee has themselves as Secret Santa |
| ✅ One-to-One Mapping | Each employee gives exactly once |
| ✅ One-to-One Mapping | Each employee receives exactly once |
| ✅ No Repeats | No repeat from previous year (if previous data provided) |
| ✅ All Included | All employees appear as both givers and receivers |

### Previous Year's Assignments Format

If you want to prevent repeats, the previous year's file must match the **output format**:

```csv
Employee_Name,Employee_EmailID,Secret_Santa_Name,Secret_Santa_EmailID
John Doe,john.doe@company.com,Jane Smith,jane.smith@company.com
Jane Smith,jane.smith@company.com,Bob Johnson,bob.johnson@company.com
Bob Johnson,bob.johnson@company.com,Alice Williams,alice.williams@company.com
Alice Williams,alice.williams@company.com,Charlie Brown,charlie.brown@company.com
Charlie Brown,charlie.brown@company.com,Diana Prince,diana.prince@company.com
Diana Prince,diana.prince@company.com,John Doe,john.doe@company.com
```

### File Naming Convention

The application automatically generates output files with timestamps:

```
secret_santa_assignments_YYYYMMDD_HHMMSS.csv
```

**Examples:**
- `secret_santa_assignments_20260707_123456.csv`
- `secret_santa_assignments_20260707_143022.csv`

### CSV Best Practices

1. **Use UTF-8 Encoding**: Ensure your CSV is saved with UTF-8 encoding
2. **No BOM**: Avoid Byte Order Mark (BOM) in CSV files
3. **Comma Delimiter**: Use comma (`,`) as the delimiter
4. **Double Quotes**: Enclose fields with commas or special characters in double quotes
5. **No Blank Rows**: Avoid empty rows at the end of the file

### Example: Creating Input CSV from Excel

If you have an Excel file, you can convert it to CSV:

1. Open the Excel file
2. **File → Save As**
3. Choose **CSV (Comma delimited) (*.csv)**
4. Click **Save**
5. Click **Yes** on any warnings

### Sample Data

You can use the sample data provided in `employees_sample.csv`:

```csv
Employee_Name,Employee_EmailID
John Doe,john.doe@company.com
Jane Smith,jane.smith@company.com
Bob Johnson,bob.johnson@company.com
Alice Williams,alice.williams@company.com
Charlie Brown,charlie.brown@company.com
Diana Prince,diana.prince@company.com
```

**Quick Test Command:**

```bash
# Run with sample data
python -m src.main employees_sample.csv
```

## Visual Diagrams

For detailed visual understanding, refer to the following diagrams: 

| Diagram | File | Description |
|---------|------|-------------|
| 📊 Project Structure Diagram | [`diagrams/Project_Structure.mmd`](diagrams/Project_Structure.png) | Complete project structure and module organization |
| 🏗️ Class Diagram | [`diagrams/Class_Architetcure_Dependencies.mmd`](diagrams/Class_Architetcure_Dependencies.png) | Class relationships, dependencies, and inheritance |
| 🔄 Data Flow Diagram | [`diagrams/Test_Architecture.mmd`](diagrams/Test_Architecture.png) |  Testing |