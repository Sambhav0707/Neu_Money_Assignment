from typing import List, Optional
from app.extensions import db
from app.models.employee import Employee

class EmployeeRepository:
    """
    Repository class for the Employee model.
    Handles all direct database interactions.
    Does not contain any business logic or validation.
    """

    @staticmethod
    def create_employee(employee_data: dict) -> Employee:
        employee = Employee(**employee_data)
        db.session.add(employee)
        db.session.commit()
        return employee

    @staticmethod
    def get_all_employees() -> List[Employee]:
        return Employee.query.all()

    @staticmethod
    def get_employee_by_id(employee_id: int) -> Optional[Employee]:
        return db.session.get(Employee, employee_id)

    @staticmethod
    def get_employee_by_email(email: str) -> Optional[Employee]:
        return Employee.query.filter_by(email=email).first()

    @staticmethod
    def update_employee(employee: Employee, update_data: dict) -> Employee:
        for key, value in update_data.items():
            setattr(employee, key, value)
        db.session.commit()
        return employee

    @staticmethod
    def delete_employee(employee: Employee) -> None:
        db.session.delete(employee)
        db.session.commit()
