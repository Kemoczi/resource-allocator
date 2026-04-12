 # Resource Allocator

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.x-red)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57)
![License](https://img.shields.io/badge/License-MIT-green)

Simple backend application for network resource allocation training. 
Built with **FastAPI**, **SQLAlchemy**, and **SQLite**

1. Resources are stored in pre-seeded database
2. User makes API POST request to assign_interface endpoint with desired resource parameters inside request body
3. App reserves first unassigned matching resource and sends it back to the client



---

## Getting Started

### Prerequisites

- Python 3.10+

### 1. Clone the repository...
```bash
git clone https://github.com/Kemoczi/resource-allocator.git
```
... and enter the directory:
```bash
cd resource-allocator
```
### 2. Create virtual environment
```bash
python -m venv venv
```
### 3. Activate virtual environment

**Windows:**
```bash
venv\Scripts\activate.ps1
```

**Linux / macOS:**
```bash
source venv/bin/activate
```
### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Initialize the database
```bash
python app/init_db.py
```
### 6. Run the application
```bash
uvicorn app.main:app
```
### 7. FastAPI Swagger UI will be available in browser:
```
http://127.0.0.1:8000/docs
```

Of course you can also use Postman or any other HTTP client of your choice.

---
## Usage
### API Endpoints

### `GET /`
Simple health-style endpoint - returns welcome message.

### `GET /resources/`
Returns the current resource inventory.

### `POST /resources/assign-interface`
Assigns the first available resource matching the requested criteria.
### Initial Resources

The database `resources.db` is seeded with the following resources:

| Location | Device | Interface ID | Physical Speed | Optics | Assigned |
|----------|--------|--------------|----------------|--------|-------|
| London   | PE1    | Port1        | 10G            | 10GBASE-LR    | False |
| London   | PE1    | Port2        | 10G            | 10GBASE-LR    | False |
| London   | PE1    | Port3        | 100G           | 100GBASE-ER   | False |
| London   | PE1    | Port4        | 1G             | 1GBASE-LR     | False |
| London   | PE1    | Port5        | 1G             | 1GBASE-SR     | False |
| London   | PE2    | Port1        | 1G             | 1GBASE-SR     | False |
| London   | PE2    | Port2        | 100G           | 100GBASE-LR   | False |
| London   | PE2    | Port3        | 10G            | 10GBASE-LR    | False |
| London   | PE2    | Port4        | 10G            | 10GBASE-SR    | False |
| London   | PE2    | Port5        | 10G            | 10GBASE-LR    | False |

The **request body** may contain one or more of the following fields:

- `location`
- `phy_speed`
- `optics`

At least one parameter must be provided.

For example:
```json
{
    "location": "London",
    "phy_speed": "10G",
    "optics": "10GBASE-LR"
}
```
In response API will send first unassigned resource which corresponds to set criteria and change it's "Assigned" state to True. Every resource once assigned cannot be assigned again. If there are no resources with matching criteria API will repond with 404 error with proper text detail.
### Example success response

```json
{
  "id": 1,
  "location": "London",
  "device": "PE1",
  "interface_id": "Port1",
  "phy_speed": "10G",
  "optics": "10GBASE-LR",
  "assigned": true
}
```

### Example error response

```json
{
  "detail": "No resources with specified parameters available"
}
```
### Cleanup / Reset

To restore all `resources.db` entries to the unassigned state outside the API itself, run:

```bash
python -m app.free_resources
```

This was intentionally implemented as an external utility rather than as a public API endpoint, to keep cleanup separate from the application’s functional surface.

---
## Testing
This project uses PyTest for automated testing.
Test suite contains isolated API tests and a live integration-style tests running actual Uvicorn server.

Run all tests with:

```bash
pytest
```
Verbose mode provides more readable look:
```bash
pytest -v
```

If you want to see command output:

```bash
pytest -v -s
```

You may use NOX as well:
```bash
nox -s tests
```

### Markers
You may run only FastAPI TestClient isolated test cases:
```bash
pytest -v -m testclient
```
Or only live Uvicorn server test cases:
```bash
pytest -v -m live
```

---

## Test Plan
### Functional testing
The same functional test scenarios are executed in two ways:

- **FastAPI TestClient tests** - used for fast, isolated API validation,
- **Live server tests** - executed against a real Uvicorn process using HTTP requests.

The live server tests additionally validate response time using explicit timing checks.

Test coverage is organized by **test modules** for clarity:

### `tests/test_init.py`
Verifies basic application startup and initialization:

- root endpoint responds correctly,
- `/resources/` returns the expected seeded inventory.

### `tests/test_assign.py`
Verifies resource assignment behavior:

- assignment using a single filter:
  - `location`
  - `phy_speed`
  - `optics`
- assignment using combined filters,
- returned resource matches requested criteria,
- already assigned resources are not returned again,
- resource pool exhaustion returns a suitable error.

### `tests/test_error.py`
Verifies error handling:

- request with no filtering criteria returns a validation error,
- request with valid but non-matching criteria returns a suitable not-found error.

### Additional cleanup utility test
### `tests/test_cleanup.py` (TestClient only)
Verifies cleanup/reset behavior:

- assigned resources can be reset back to unassigned state,
- cleanup is validated only for isolated API environment


### Response time requirement (Uvicorn only)

The requirement states that the system should return either a usable interface or a suitable error in less than 2 seconds.

This is validated in live server tests for:

- a successful assignment response,
- an error response when no matching resource is available.

---
