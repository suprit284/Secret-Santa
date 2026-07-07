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
- [Constraints & Validation](#-constraints--validation)
- [Testing](#-testing)
- [Error Handling](#-error-handling)
- [Configuration](#-configuration)
- [Contributing](#-contributing)
- [License](#-license)
- [Quick Start](#-quick-start)

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
   git clone https://github.com/yourusername/secret-santa.git
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
