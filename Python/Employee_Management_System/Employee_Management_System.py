from datetime import datetime

class Employee:
    
    company_name = "ABC Corp"
    total_employees = 0
    
    def __init__(self, emp_id, name, department, salary):
        self.emp_id = emp_id
        self.name = name
        self.department = department
        self.__salary = salary # private attribute

        # Composition: Employee HAS-A project
        self.project = None
        self.tasks = []
        Employee.total_employees+=1
        
    @property
    def salary(self):
        return self.__salary
    
    @salary.setter
    def salary(self, value):
        if value<0:
            print("Salary shouldn't be negative")
        elif value>10000:
            self.__salary = value
        else:
            raise ValueError("Invalid salary value")
        
    def get_details(self):
        return f" emp_id: {self.emp_id}, name: {self.name}, department: {self.department}, salary: {self.salary}"
    
    def apply_increment(self, percent):
        if 0 < percent <=100:
            self.__salary=self.salary+self.salary*percent/100
            print(f" Salary is increased by {percent}")
        else:
            print("Invalid Percentage")

    # ------------------ Composition Methods ------------------
    def assign_project(self, project):
        self.project = project
        return f" Project {project.project_id} : {project.project_name} : {project.client_name} is now assigned to user {self.name}"

    def get_project_details(self):
        if self.project is None:
            return f" Emp {self.name} don't have any projects assigned currently "
        return f" Emp Name: {self.name}, Project: {self.project.project_name}, Client: {self.project.client_name}"

    def __str__(self):
        return f"[Employee] {self.name} | ID: {self.emp_id} | Dept: {self.department} | Salary: {self.salary}" # if str is not there and
    
    def __repr__(self):
        return f" object of employee"

    # ------------------ Magic Methods ------------------
    def __eq__(self, other):
        return self.__salary == other.salary

    def __lt__(self, other):
        if not isinstance(other, Employee):
            return NotImplemented
        return self.__salary < other.salary

    def __gt__(self, other):
        if not isinstance(other, Employee):
            return NotImplemented
        return self.__salary > other.salary

    # Object Relationships
    def assign_task(self, task):
        self.tasks.append(task)
        return f" Task {task.task_id} is assigned to {self.name}"

    def list_tasks(self):
        return self.tasks

    def get_pending_tasks(self):
        return list(filter(lambda task: task.status != "Done", self.tasks))

    def sort_tasks_by_deadline(self):
        return sorted(self.tasks)



emp1=Employee(1,"anil",None,1000)
emp2=Employee(2,"sunil",None,4000)
emp3=Employee(3,"linga",None,7000)
emp4=Employee(4,"sudheer",None,1500)
emp5=Employee(5,"rahul",None,2000)

class Manager(Employee):
    def __init__(self, emp_id, name, department, salary, team_size):
        super().__init__(emp_id, name, department, salary)
        self.team_size = team_size
    def calculate_bonus(self):
        """Board bonus: 20% of salary per team member."""
        base_bonus = self.salary*0.10*self.team_size
        return base_bonus
    def get_details(self):
        return f" emp_id: {self.emp_id}, name: {self.name}, department: {self.department}, salary: {self.salary}, team_size: {self.team_size}, bonus: {self.calculate_bonus()}"

manager1=Manager("Amar", 5,"IT", 1000000, 12)
manager2 = Manager("Ramesh", 7, "IT", 900000, 7)

managers=[manager1, manager2]
for manager in managers:
    print(manager.get_details())
    
class Project:
    def __init__(self, project_id, project_name, client_name):
        self.project_id = project_id
        self.project_name = project_name
        self.client_name = client_name

project1 = Project(1, "Edufrent", "CM")
project2 = Project(2, "Agrifrent", "CVR")

emp1.assign_project(project1)
emp2.assign_project(project2)
emps = [emp1, emp2, emp3]
for emp in emps:
    print(emp.get_project_details())


def sort_employees_by_salary(employees):
    return sorted(employees) # uses __lt__ internally

employees = [emp1, emp2, emp3, emp4, emp5]

sorted_emps = sort_employees_by_salary(employees)

for emp in sorted_emps:
    print(emp.name, emp.salary)

print(emp1<emp2)

class Task:
    def __init__(self, task_id, description, status, deadline):
        self.task_id = task_id
        self.description = description
        self.status = status
        self.deadline = datetime.strptime(deadline, "%d-%m-%Y %H:%M:%S")

    def __repr__(self):
        return f"{self.task_id}, {self.description}, {self.status}, {self.deadline}"

    def __lt__(self, other):
        if not isinstance(other, Task):
            raise NotImplementedError
        return self.deadline < other.deadline

task1 = Task(1, "complete automation", "Not Started", "16-02-2026 23:00:00")
task2 = Task(2, "complete QA", "Pending", "18-02-2026 23:00:00")
emp1.assign_task(task1)
emp1.assign_task(task2)
emp2.assign_task(task2)

print(emp1.get_project_details())
print(emp1.get_pending_tasks())
print(emp1.sort_tasks_by_deadline())


class Department:
    def __init__(self, name, manager):
        self.name = name
        self.manager = manager
        self.employees = []

    def __repr__(self):
        return f"| {self.name}, {self.manager}, {self.employees} |"

    def add_employee(self,employee):
        employee.department = self
        self.employees.append(employee)

    def get_all_employees(self):
        return self.employees

    def department_summary(self):
        return f" name: {self.name}, manager: {self.manager}, total employees: {self.employees.count()}"

IT = Department("IT", manager1)
IT.add_employee(emp1)
print(emp1.get_details())





