import json
from app.exceptions.custom_exceptions import ValidationException

def test_get_all_employees(client, mocker):
    # Arrange
    mocker.patch('app.controllers.employee_controller.EmployeeService.get_all_employees', return_value=[])

    # Act
    response = client.get('/employees')

    # Assert
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert data['data'] == []

def test_create_employee_validation_error(client, mocker):
    # Arrange
    mocker.patch('app.controllers.employee_controller.EmployeeService.create_employee', side_effect=ValidationException("Invalid data"))

    # Act
    response = client.post('/employees', json={"bad": "data"})

    # Assert
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] is False
    assert data['message'] == "Invalid data"
