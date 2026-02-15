'''
# Activity set1: Class Fundamentals (Real life domain - HR Systems)

**Class Variable**: Variable shared by all instances of a class, defined directly in the class body.

```python
class Dog:
    species = "Canine"  # Class variable
```

**Function**: Standalone code block that performs a task.

```python
def add(a, b):  # Function
    return a + b
```

**Method**: Function bound to a class/object, receives `self` as first parameter.

```python
class Dog:
    def bark(self):  # Method
        return "Woof!"
```

**Attribute**: Data stored on an object/class (accessed with dot notation).

```python
class Dog:
    def __init__(self, name):
        self.name = "Buddy"  # Instance attribute
```

**Variable**: General term for any named storage location (local, global, instance, class).

**__str__ vs __repr__**
String Representation (__repr__)
The __repr__ method returns a developer-friendly, unambiguous string representation of an object, often resembling valid Python code for recreation. It's used by the repr() function and interactive prompts.

Informal String (__str__)
The __str__ method provides a human-readable string, called by str() or print(). It falls back to __repr__ if not defined.

| Aspect         | __repr__                             | __str__                      |
| -------------- | ------------------------------------ | ---------------------------- |
| Purpose        | Debug/developer-focused, unambiguous | User-friendly, readable      |
| Called by      | repr(), REPL                         | print(), str()               |
| Fallback       | Default object ID                    | Uses __repr__ if missing     |
| Example Output | Point(3, 4)                          | Point at (3, 4) realpython+1 |
'''
===============================================================


# Activity set2: Encapsulation and validation


Encapsulation bundles data and methods together in a class while hiding internal details from outside access.

## Core Concept
Encapsulation protects object data by restricting direct access, using naming conventions like `_protected` (single underscore) and `__private` (double underscore). Access happens through public methods or properties.

## Simple Example
```python
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner          # Public attribute
        self.__balance = balance    # Private attribute
    
    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
    
    def get_balance(self):
        return self.__balance
    
    def withdraw(self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount

# Usage
account = BankAccount("Alice", 1000)
account.deposit(500)
print(account.get_balance())  # 1500
# print(account.__balance)   # Error: protected
```

## Property Decorators
Use `@property` for controlled access with validation.

```python
class Student:
    def __init__(self, name, age):
        self.name = name
        self.__age = age
    
    @property
    def age(self):
        return self.__age
    
    @age.setter
    def age(self, value):
        if 0 <= value <= 120:
            self.__age = value
        else:
            print("Invalid age")

stud = Student("Bob", 20)
stud.age = 25      # Valid
stud.age = 150     # Prints "Invalid age"
print(stud.age)    # 25
```

## Key Benefits
- **Data Protection**: Prevents invalid changes
- **Code Organization**: Clean public interface
- **Flexibility**: Internal changes don't break external code

Note:
Use **if-else conditions** for validation in most cases. Use **try-except** only for handling unpredictable errors.

## When to Use Each

### **If-Else (Recommended 90% of time)**
**Use for**: Predictable validation rules, input checking, business logic
```python
@salary.setter
def salary(self, value):
    if value <= 0:
        print("Invalid: Salary must be positive")
    else:
        self.__salary = value  # Simple, readable, fast
```

### **Try-Except (Exception Handling)**
**Use for**: External operations, file I/O, network calls, type conversion errors
```python
def set_salary_from_file(self, filename):
    try:
        with open(filename) as f:
            value = float(f.read())
            self.salary = value  # Calls setter with validation
    except FileNotFoundError:
        print("File not found")
    except ValueError:
        print("Invalid number in file")
```

## Updated Employee Example
```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        if salary > 0:
            self.__salary = salary
        else:
            raise ValueError("Salary must be positive")
    
    @property
    def salary(self):
        return self.__salary
    
    @salary.setter
    def salary(self, value):
        if value > 0:  # if-else for validation
            self.__salary = value
        else:
            raise ValueError("Salary must be positive")
    
    def increment(self, percentage):
        if 0 < percentage <= 50:  # if-else validation
            self.__salary *= (1 + percentage/100)
        else:
            raise ValueError("Percentage must be 0-50%")
```

## Rule of Thumb
```
Validation rules → if-else
Runtime errors   → try-except
```

**if-else** = "Is this input valid?"  
**try-except** = "What if this operation fails?"
