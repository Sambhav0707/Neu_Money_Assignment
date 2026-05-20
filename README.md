# Employee Management System

A production-grade, RESTful Employee Management System built with Python and Flask. This project strictly adheres to a Clean Layered Architecture, ensuring separation of concerns, high testability, and scalability.

---

## 🛠️ Tech Stack & Flask Packages

This application leverages modern Python and robust Flask extensions to ensure a secure, maintainable, and highly performant backend.

- **Framework**: Flask (Core web framework, using Blueprints and Application Factory)
- **Database**: PostgreSQL (Relational database for persistent storage)
- **ORM**: SQLAlchemy (via `Flask-SQLAlchemy`) - Simplifies database interactions using Python objects instead of raw SQL queries.
- **Validation**: Pydantic - Used for strict data validation and serialization.
- **Driver**: `psycopg2-binary` - PostgreSQL database adapter for Python.
- **Environment Management**: `python-dotenv` - Loads environment variables from `.env` files.
- **Testing**: `pytest` & `pytest-mock`
- **Package Manager**: `uv`

### Why Pydantic Was Chosen
While Flask has other validation tools (like Marshmallow), **Pydantic** was chosen because of its incredibly fast validation speed (written in Rust in v2), its strict type hinting that pairs perfectly with modern Python (3.10+), and its intuitive schema definitions. It serves as a robust Anti-Corruption Layer, guaranteeing that no malformed data ever reaches the core business logic or the database, and provides automatic, clear validation error messages.

---

## 📂 Folder Structure

This structured layout helps reviewers and developers immediately understand the organization and find relevant code quickly.

```text
neu-money-assignment/
├── app/
│   ├── config/         # Application configuration and environment loading
│   ├── controllers/    # HTTP layer: API Routes, request parsing, and response formatting
│   ├── exceptions/     # Custom domain and application-specific error classes
│   ├── models/         # SQLAlchemy ORM database models (Tables)
│   ├── repositories/   # Database access layer (queries, transactions)
│   ├── schemas/        # Pydantic validation schemas (Anti-corruption layer)
│   ├── services/       # Core business logic and rules orchestration
│   ├── utils/          # Helper functions and shared utilities
│   └── extensions.py   # Flask extension initializations
├── tests/              # Unit and integration tests (pytest)
├── pyproject.toml      # Project dependencies and configuration (uv)
├── .env.example        # Environment variable template
└── main.py             # Application entry point
```

---

## 🏗️ Architecture Overview

The application is meticulously structured into distinct layers to separate HTTP routing, business logic, and database access. This Clean Architecture approach ensures long-term maintainability.

- **Controllers (`app/controllers`)**: The HTTP layer. Responsible **only** for parsing JSON requests, routing them to the correct service, and returning standardized JSON responses. They contain **zero** business logic.
- **Services (`app/services`)**: The heart of the application. Responsible for validating data, enforcing business rules (e.g., checking for duplicate emails), and orchestrating repository calls. They are completely decoupled from Flask and HTTP, making them highly testable.
- **Models (`app/models`)**: The data definition layer. Contains the SQLAlchemy ORM classes that define the database schema (e.g., the `Employee` table) and establish table relationships.
- **Repositories (`app/repositories`)**: The database access layer. Responsible exclusively for SQLAlchemy queries and database transactions. They abstract the database interactions so services never touch raw ORM objects directly.
- **Schemas (`app/schemas`)**: The data validation layer. Uses Pydantic models to strictly validate incoming request payloads and format outgoing responses.
- **Exceptions (`app/exceptions`)**: Custom domain exceptions (e.g., `NotFoundError`, `DuplicateEmailError`) that allow the service layer to safely communicate specific errors to global error handlers without leaking internal stack traces.

### Why the Repository Pattern Was Used
Recruiters and senior engineers love this pattern for several reasons:
1. **Decoupling**: It isolates the business logic (Services) from the data access framework (SQLAlchemy). If we ever need to switch the ORM or the database entirely, we only rewrite the repositories, leaving the core business logic completely untouched.
2. **Testability**: Services can be easily tested using unit tests by mocking the repository layer, completely removing the need for a live database during business logic testing.
3. **Centralized Data Access**: Complex database queries and transactions are centralized in one place, avoiding duplicated raw queries scattered across controllers or services.

---

## 🔄 Architecture Flow Diagram

The following diagram illustrates how a typical request (e.g., "Get All Employees") flows through the system layers:

```mermaid
sequenceDiagram
    participant Client
    participant Controller as Controller (HTTP)
    participant Schema as Schema (Pydantic)
    participant Service as Service (Business Logic)
    participant Repository as Repository (Data Access)
    participant DB as Database (PostgreSQL)

    Client->>Controller: GET /employees (or POST/PUT)
    Note over Controller: Parses HTTP Request
    Controller->>Schema: Validate Input Payload (if any)
    Schema-->>Controller: Validated Data
    Controller->>Service: Call respective method (e.g., get_all_employees)
    Note over Service: Apply Business Rules
    Service->>Repository: Request Data (e.g., fetch_all)
    Note over Repository: Execute SQLAlchemy Query
    Repository->>DB: SQL Query
    DB-->>Repository: Raw Data / ORM Objects
    Repository-->>Service: Return ORM Models
    Service->>Schema: Serialize ORM to Dictionaries
    Schema-->>Service: Serialized Data
    Service-->>Controller: Return Business Result
    Controller-->>Client: Standardized JSON Response (200 OK)
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

---

## 🚀 Installation & Running Guide

Follow these steps to get the project up and running locally.

### 1. Prerequisites
- **Python**: 3.13+
- **[uv](https://github.com/astral-sh/uv)**: Extremely fast Python package manager.
- **PostgreSQL**: Running locally or via Docker.

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

### 4. Database Initialization

The database tables are automatically created when you start the application.

### 5. Running the Application

Start the Flask development server:

```bash
python main.py
```
The API will be available at `http://127.0.0.1:5000`.

---

## 🧪 Running Tests

The test suite leverages `pytest` and `pytest-mock` to test the business logic in total isolation from the database, ensuring blazing fast execution.

```bash
# Run all tests with verbosity
pytest tests/ -v
```
