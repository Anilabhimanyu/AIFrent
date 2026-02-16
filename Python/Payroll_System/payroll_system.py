from abc import ABC, abstractmethod
from datetime import datetime

class Logger:
    @staticmethod
    def log_error(emp_id, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[ERROR] {timestamp} | EmpID: {emp_id} | {message}")

class EmployeeBase(ABC):

    def __init__(self, id, name):
        self.id = id
        self.name = name

    @abstractmethod
    def calculate_salary(self):
        pass

    @abstractmethod
    def get_role(self):
        pass

class InvalidSalaryException(Exception):
    pass


class FullTimeEmployee(EmployeeBase):
    def __init__(self, id, name, base_salary, bonus):
        super().__init__(id, name)

        if base_salary < 8000:
            raise InvalidSalaryException("Base salary must be at least 8000")

        if bonus < 0:
            raise InvalidSalaryException("Bonus cannot be negative")

        self.base_salary = base_salary
        self.bonus = bonus

    def calculate_salary(self):
        return self.base_salary + self.bonus

    def get_role(self):
        return "Full Time"

class ContractEmployee(EmployeeBase):
    def __init__(self, id, name, hourly_wage, hours_worked):
        super().__init__(id, name)

        if hourly_wage <= 0:
            raise InvalidSalaryException("Hourly wage must be positive")

        if hours_worked < 0:
            raise InvalidSalaryException("Hours worked cannot be negative")

        self.hourly_wage = hourly_wage
        self.hours_worked = hours_worked

    def calculate_salary(self):
        return self.hours_worked * self.hourly_wage

    def get_role(self):
        return "Contract"

try:
    emp1 = FullTimeEmployee(1, "Anil", 5000, 1000)   # invalid salary
except InvalidSalaryException as e:
    Logger.log_error("Error:", e)

try:
    emp2 = FullTimeEmployee(2, "Sunil", 10000, -500)  # invalid bonus
except InvalidSalaryException as e:
    Logger.log_error("Error:", e)


