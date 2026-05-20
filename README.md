# Employee Management System

A production-grade, RESTful Employee Management System built with Python and Flask. This project strictly adheres to a Clean Layered Architecture, ensuring separation of concerns, high testability, and scalability.

---

## 🛠️ Tech Stack
- **Framework**: Flask (with Blueprints and Application Factory)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy (via Flask-SQLAlchemy)
- **Migrations**: Alembic (via Flask-Migrate)
- **Validation**: Pydantic
- **Testing**: pytest & pytest-mock
- **Package Manager**: uv

---

## 🏗️ Architecture Overview

The application is structured into distinct layers to separate HTTP routing, business logic, and database access:

- **Controllers (`app/controllers`)**: The HTTP layer. Responsible only for parsing JSON requests, routing them to the correct service, and returning standardized JSON responses. They contain **zero** business logic.
- **Services (`app/services`)**: The heart of the application. Responsible for validating data (using Pydantic), enforcing business rules (e.g., checking for duplicate emails), and orchestrating repository calls. They are completely decoupled from Flask and HTTP.
- **Repositories (`app/repositories`)**: The database layer. Responsible exclusively for SQLAlchemy queries and transactions. They abstract the database so services never touch raw ORM objects directly.
- **Exceptions (`app/exceptions`)**: Custom domain exceptions (`NotFoundError`, `DuplicateEmailError`) that allow the service layer to safely communicate errors to the global error handlers.
- **Schemas (`app/schemas`)**: Pydantic models used as an anti-corruption layer to strictly validate incoming and outgoing data.

---

## 🚀 Setup Instructions

### 1. Prerequisites
- Python 3.13+
- [uv](https://github.com/astral-sh/uv) (Extremely fast Python package manager)
- PostgreSQL running locally or via Docker

### 2. Environment Setup

Create a virtual environment and install all dependencies using `uv`:

```bash
# Create and activate virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install all dependencies (runtime + dev)
uv sync
```

### 3. Configuration

Copy the example environment file and configure your database URL:

```bash
cp .env.example .env
```
Ensure your `DATABASE_URL` in `.env` points to a valid PostgreSQL database. Example:
`DATABASE_URL=postgresql://postgres:password@localhost:5432/employee_db`

### 4. Database Migrations

Initialize the database schema:

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 5. Running the Application

Start the Flask development server:

```bash
python run.py
```
The API will be available at `http://127.0.0.1:5000`.

---

## 🧪 Running Tests

The test suite leverages `pytest` and `pytest-mock` to test the business logic in total isolation from the database, ensuring blazing fast execution.

```bash
pytest tests/ -v
```

---

## 📖 API Documentation

All API responses follow a standardized envelope format:
**Success**: `{"success": true, "message": "...", "data": {}}`
**Error**: `{"success": false, "message": "...", "errors": []}`

### 1. Create Employee
**POST** `/employees`

**Request Body:**
```json
{
    "name": "Jane Doe",
    "email": "jane.doe@example.com",
    "department": "Engineering"
}
```

**Response (201 Created):**
```json
{
    "success": true,
    "message": "Employee created successfully",
    "data": {
        "id": 1,
        "name": "Jane Doe",
        "email": "jane.doe@example.com",
        "department": "Engineering",
        "date_joined": "2026-05-18T00:00:00Z",
        "created_at": "2026-05-18T10:00:00Z",
        "updated_at": "2026-05-18T10:00:00Z"
    }
}
```

### 2. Get All Employees
**GET** `/employees`

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Employees retrieved successfully",
    "data": [
        {
            "id": 1,
            "name": "Jane Doe",
            "email": "jane.doe@example.com",
            "department": "Engineering",
            "date_joined": "2026-05-18T00:00:00Z",
            "created_at": "2026-05-18T10:00:00Z",
            "updated_at": "2026-05-18T10:00:00Z"
        }
    ]
}
```

### 3. Update Employee
**PUT** `/employees/<id>`

**Request Body (Partial updates supported):**
```json
{
    "department": "Product Management"
}
```

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Employee updated successfully",
    "data": {
        "id": 1,
        "name": "Jane Doe",
        "email": "jane.doe@example.com",
        "department": "Product Management",
        "date_joined": "2026-05-18T00:00:00Z",
        "created_at": "2026-05-18T10:00:00Z",
        "updated_at": "2026-05-18T10:00:00Z"
    }
}
```

### 4. Delete Employee
**DELETE** `/employees/<id>`

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Employee deleted successfully",
    "data": {}
}
```

### 5. Error Example (Duplicate Email)
**POST** `/employees` (with an existing email)

**Response (409 Conflict):**
```json
{
    "success": false,
    "message": "Employee with email jane.doe@example.com already exists.",
    "errors": []
}
```
