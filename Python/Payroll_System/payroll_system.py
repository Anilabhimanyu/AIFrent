from abc import ABC, abstractmethod

class EmployeeBase(ABC):
    @abstractmethod
    def calculate_salary(self):
        pass

    @abstractmethod
    def get_role(self):
        pass

class FullTimeEmployee(EmployeeBase):
    def __init__(self, base_salary, bonus):
        self.base_salary = base_salary
        self.bonus = bonus

    def calculate_salary(self):
        return self.base_salary + self.bonus

    def get_role(self):
        return "Full Time"

class ContractEmployee(EmployeeBase):
    def __init__(self, hourly_wage, hours_worked):
        self.hourly_wage = hourly_wage
        self.hours_worked = hours_worked

    def calculate_salary(self):
        return self.hours_worked * self.hourly_wage

    def get_role(self):
        return "Contract"

def print_salary_slips(employee: EmployeeBase):
    return f"Salary paid: {employee.calculate_salary()}"

emp1 = FullTimeEmployee(1000, 100)
emp2 = ContractEmployee(100, 8)

employees = [emp1, emp2]
total_company_expense=0
for employee in employees:
    total_company_expense += employee.calculate_salary()
    print(f"{employee.get_role()}, {print_salary_slips(employee)}")

