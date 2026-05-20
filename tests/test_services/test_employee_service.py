import pytest
from app.services.employee_service import EmployeeService
from app.exceptions.custom_exceptions import DuplicateEmailError, NotFoundError

def test_create_employee_success(mocker):
    # Arrange
    mock_repo_get = mocker.patch('app.services.employee_service.EmployeeRepository.get_employee_by_email', return_value=None)
    mock_repo_create = mocker.patch('app.services.employee_service.EmployeeRepository.create_employee', return_value="employee_obj")
    
    data = {
        "name": "John Doe",
        "email": "john@example.com",
        "department": "Engineering"
    }

    # Act
    result = EmployeeService.create_employee(data)

    # Assert
    assert result == "employee_obj"
    mock_repo_get.assert_called_once_with("john@example.com")
    mock_repo_create.assert_called_once()

def test_create_employee_duplicate_email(mocker):
    # Arrange
    mocker.patch('app.services.employee_service.EmployeeRepository.get_employee_by_email', return_value="existing_employee")
    
    data = {
        "name": "John Doe",
        "email": "john@example.com",
        "department": "Engineering"
    }

    # Act & Assert
    with pytest.raises(DuplicateEmailError):
        EmployeeService.create_employee(data)

def test_update_employee_not_found(mocker):
    # Arrange
    mocker.patch('app.services.employee_service.EmployeeRepository.get_employee_by_id', return_value=None)
    
    # Act & Assert
    with pytest.raises(NotFoundError):
        EmployeeService.update_employee(999, {"name": "Jane"})
