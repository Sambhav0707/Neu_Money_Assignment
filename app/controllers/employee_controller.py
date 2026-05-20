"""
This is the HTTP Layer (Controller). 
Its ONLY responsibility is to define API routes (endpoints), parse incoming HTTP 
requests (JSON data, path parameters), pass that data to the Service layer, 
and format the Service layer's result into a standardized JSON HTTP response. 

This layer contains absolutely ZERO business logic or database interactions.
"""

from flask import Blueprint, request
from app.services.employee_service import EmployeeService
from app.schemas.employee_schema import EmployeeResponseSchema
from app.utils.response import success_response

employee_bp = Blueprint('employees', __name__, url_prefix='/employees')

@employee_bp.route('', methods=['POST'])
def create_employee():
    data = request.get_json() or {}
    employee = EmployeeService.create_employee(data)
    response_data = EmployeeResponseSchema.model_validate(employee).model_dump(mode='json')
    return success_response(data=response_data, message="Employee created successfully", status_code=201)

@employee_bp.route('', methods=['GET'])
def get_all_employees():
    employees = EmployeeService.get_all_employees()
    response_data = [EmployeeResponseSchema.model_validate(e).model_dump(mode='json') for e in employees]
    return success_response(data=response_data, message="Employees retrieved successfully", status_code=200)

@employee_bp.route('/<int:employee_id>', methods=['GET'])
def get_employee(employee_id: int):
    employee = EmployeeService.get_employee(employee_id)
    response_data = EmployeeResponseSchema.model_validate(employee).model_dump(mode='json')
    return success_response(data=response_data, message="Employee retrieved successfully", status_code=200)

@employee_bp.route('/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id: int):
    data = request.get_json() or {}
    employee = EmployeeService.update_employee(employee_id, data)
    response_data = EmployeeResponseSchema.model_validate(employee).model_dump(mode='json')
    return success_response(data=response_data, message="Employee updated successfully", status_code=200)

@employee_bp.route('/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id: int):
    EmployeeService.delete_employee(employee_id)
    return success_response(message="Employee deleted successfully", status_code=200)
