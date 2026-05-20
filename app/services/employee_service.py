"""
This is the Business Logic Layer (Service).
This is the heart of the application. It orchestrates the validation of data, 
enforces business rules (like checking if an email is already taken), and calls 
the Repository layer to save or fetch data. 

This layer is completely decoupled from Flask, HTTP requests, and raw database queries, 
making it incredibly easy to test in isolation.
"""

from typing import List
from pydantic import ValidationError

from app.models.employee import Employee
from app.repositories.employee_repository import EmployeeRepository
from app.schemas.employee_schema import EmployeeCreateSchema, EmployeeUpdateSchema
from app.exceptions.custom_exceptions import NotFoundError, DuplicateEmailError, ValidationException


class EmployeeService:
    """
    Service class for Employee management.
    Orchestrates validation, business rules, and repository access.
    Does not know anything about HTTP or Flask context.
    """

    @staticmethod
    def create_employee(data: dict) -> Employee:
        try:
            schema = EmployeeCreateSchema(**data)
        except ValidationError as e:
            raise ValidationException(str(e))

        # Check for duplicate email
        if EmployeeRepository.get_employee_by_email(schema.email):
            raise DuplicateEmailError(f"Employee with email {schema.email} already exists.")

        return EmployeeRepository.create_employee(schema.model_dump(exclude_unset=True))

    @staticmethod
    def get_all_employees() -> List[Employee]:
        return EmployeeRepository.get_all_employees()

    @staticmethod
    def get_employee(employee_id: int) -> Employee:
        employee = EmployeeRepository.get_employee_by_id(employee_id)
        if not employee:
            raise NotFoundError(f"Employee with ID {employee_id} not found.")
        return employee

    @staticmethod
    def update_employee(employee_id: int, data: dict) -> Employee:
        # Validate partial update data
        try:
            schema = EmployeeUpdateSchema(**data)
        except ValidationError as e:
            raise ValidationException(str(e))

        employee = EmployeeRepository.get_employee_by_id(employee_id)
        if not employee:
            raise NotFoundError(f"Employee with ID {employee_id} not found.")

        # If email is being updated, ensure it's not taken by another employee
        if schema.email and schema.email != employee.email:
            if EmployeeRepository.get_employee_by_email(schema.email):
                raise DuplicateEmailError(f"Email {schema.email} is already in use by another employee.")

        update_dict = schema.model_dump(exclude_unset=True)
        return EmployeeRepository.update_employee(employee, update_dict)

    @staticmethod
    def delete_employee(employee_id: int) -> None:
        employee = EmployeeRepository.get_employee_by_id(employee_id)
        if not employee:
            raise NotFoundError(f"Employee with ID {employee_id} not found.")
        
        EmployeeRepository.delete_employee(employee)
