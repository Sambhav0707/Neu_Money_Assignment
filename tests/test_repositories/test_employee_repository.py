from app.repositories.employee_repository import EmployeeRepository

def test_create_and_get_employee(app):
    # Arrange
    data = {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "department": "HR"
    }
    
    # Act
    employee = EmployeeRepository.create_employee(data)
    fetched = EmployeeRepository.get_employee_by_id(employee.id)
    
    # Assert
    assert fetched is not None
    assert fetched.email == "jane@example.com"
