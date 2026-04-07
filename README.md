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

### 5. Initialize the database
`python app/init_db.py`
### 6. Run the application
`uvicorn app.main:app`
### 7. Open FastAPI Swagger UI in browser:
`http://127.0.0.1:8000/docs`

Or use other Postman if you want.

## Usage
### Initial Resources

The database is seeded with the following resources:

| Location | Device | Interface ID | Physical Speed | Optics | Assigned |
|----------|--------|--------------|----------------|--------|----------|
| London   | PE1    | Port1        | 10G            | 10GBASE-LR     | No |
| London   | PE1    | Port2        | 10G            | 10GBASE-LR     | No |
| London   | PE1    | Port3        | 100G           | 100GBASE-ER    | No |
| London   | PE1    | Port4        | 1G             | 1GBASE-LR      | No |
| London   | PE1    | Port5        | 1G             | 1GBASE-SR      | No |
| London   | PE2    | Port1        | 1G             | 1GBASE-SR      | No |
| London   | PE2    | Port2        | 100G           | 100GBASE-LR    | No |
| London   | PE2    | Port3        | 10G            | 10GBASE-LR     | No |
| London   | PE2    | Port4        | 10G            | 10GBASE-SR     | No |
| London   | PE2    | Port5        | 10G            | 10GBASE-LR     | No |

**Request body** must contain at least one of following resource properties: location, physical speed, optics.

For example:
```
{
    "location": "London",
    "phy_speed": "10G",
    "optics": "10GBASE-LR"
}
```
In response API will send first unassigned resource which corresponds to set criteria and change it's "Assigned" state to True. Every resource once assigned cannot be assigned again. If there are no resources with matching criteria API will repond with 404 error with proper text detail.

### Freeing up resources
If you want to unassign all of the resources, run:

`python app/free_resources.py`