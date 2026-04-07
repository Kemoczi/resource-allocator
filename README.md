# Resource Allocator

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.x-red)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57)
![License](https://img.shields.io/badge/License-MIT-green)

Lightweight application for allocating network resources.  
Built with **FastAPI**, **SQLAlchemy**, and **SQLite** provides a clean foundation for resource tracking, allocation workflows, and future API expansion.


---

## Getting Started

### Prerequisites

Make sure you have the following installed:

- Python 3.10 or newer
- pip

### 1. Clone the repository and enter the directory
`git clone https://github.com/Kemoczi/resource-allocator.git`

`cd resource-allocator`
### 2. Create a virtual environment
`python -m venv venv`
### 3. Activate the virtual environment

**Windows:**
`venv\Scripts\activate.ps1`

**Linux / macOS:**
`source venv/bin/activate`
### 4. Install dependencies
`pip install -r requirements.txt`


## Usage
### 1. Initialize the database
`python app/init_db.py`
### 2. Run the application
`uvicorn app.main:app`