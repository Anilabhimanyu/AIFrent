class Employee:
    
    company_name = "ABC Corp"
    total_employees = 0
    
    def __init__(self, emp_id, name, department, salary):
        self.emp_id = emp_id
        self.name = name
        self.department = department
        self.__salary = salary # private attribute
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
            

    def __str__(self):
        return f"[Employee] {self.name} | ID: {self.emp_id} | Dept: {self.department} | Salary: {self.salary}" # if str is not there and
    
    def __repr__(self):
        return f" object of employee"

emp1=Employee(1,"anil","IT",1000)
emp2=Employee(2,"sunil","IT",4000)
emp3=Employee(3,"linga","IT",7000)
emp4=Employee(4,"sudheer","HR",1500)
emp5=Employee(5,"rahul","Finance",2000)

print(emp1)
print(repr(emp1))

