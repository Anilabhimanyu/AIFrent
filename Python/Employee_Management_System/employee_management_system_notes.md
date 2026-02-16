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

# Activity set3: Inheritance ( Add Manager Role)
**Inheritance** is an OOP concept where a child class (subclass) inherits attributes and methods from a parent class (superclass).

## Theory

### **Core Idea**
- Creates **"is-a" relationship**: Manager **is-a** Employee
- Child class **extends** parent class functionality
- Promotes **code reuse** and **hierarchy**

### **Key Components**
```
Parent Class (Base/Superclass)
    ↑
Child Class (Derived/Subclass)
```

### **How It Works**
1. **Automatic Inheritance**: Child gets ALL parent attributes/methods
2. **`super()`**: Explicitly calls parent methods
3. **Method Override**: Child can redefine parent methods
4. **New Features**: Child adds its own attributes/methods

### **Syntax**
```python
class ChildClass(ParentClass):  # Inheritance happens here
    def __init__(self, ...):
        super().__init__(...)    # Call parent constructor
        self.new_attribute = ... # Child-specific
```

### **Benefits**
- **DRY Principle**: Don't Repeat Yourself
- **Polymorphism**: Same interface, different behaviors
- **Extensibility**: Easy to add specialized classes

### **Types**
- **Single**: `class B(A)`
- **Multiple**: `class C(A, B)` (Python supports)
- **Multilevel**: `D → C → B → A`
- **Hierarchical**: Multiple children from one parent

**Purpose**: Build specialized classes from general ones without duplicating code.

# Activity set4: Composition + Project System

## Relationship Decision Guide

### **Inheritance** (`is-a`)
**When**: True hierarchical "is-a" relationship
```
Car is-a Vehicle ✓ Inheritance
Manager is-a Employee ✓ Inheritance
```
**Use**: Natural type hierarchy, polymorphism needed

### **Composition** (`has-a`, strong ownership)
**When**: Whole-part relationship, part can't exist without whole
```
House has-a Room (room dies if house destroyed) ✓ Composition
Car has-a Engine (engine belongs exclusively to car) ✓ Composition
```
**Syntax**: 
```python
class Car:
    def __init__(self):
        self.engine = Engine()  # Composition
```

### **Aggregation** (`has-a`, weak ownership) 
**When**: Whole-part relationship, part can exist independently
```
Department has-a Employee (employee can move to another dept) ✓ Aggregation
University has-a Student (student can transfer) ✓ Aggregation
```
**Syntax**:
```python
class Department:
    def __init__(self):
        self.employees = []  # Aggregation (external reference)
```

## Quick Decision Matrix

| Relationship | Question | Example |
|--------------|----------|---------|
| **Inheritance** | Is it truly the same type? | `Dog is-a Animal` |
| **Composition** | Does part die without whole? | `Wheel belongs to Car` |
| **Aggregation** | Can part exist separately? | `Professor works for University` |

## Golden Rule
```
"is-a" → Inheritance (rare)
"has-a" → Composition/Aggregation (common)
"Favor composition over inheritance"
```

# Activity set5: Magic Methods & Comparision
**Question: What are Magic Methods in Python?**

### ✅ Magic Methods (also called Dunder Methods)

Magic methods are **special predefined methods in Python** that start and end with double underscores:

👉 `__method__`

That’s why they are called **dunder** methods (**double underscore**).

Example:

* `__init__`
* `__str__`
* `__lt__`
* `__eq__`

---

## ✅ Why are they called "Magic"?

Because Python **automatically calls them internally** when you use operators or built-in functions.

You don’t call them directly most of the time.

---

## ✅ Example 1: `__init__` (Object creation)

```python
emp = Employee()
```

Python internally calls:

```python
Employee.__init__(emp)
```

---

## ✅ Example 2: `__str__` (print object)

```python
print(emp)
```

Python internally calls:

```python
emp.__str__()
```

So you control what gets printed.

---

## ✅ Example 3: `__lt__` (less than `<`)

```python
emp1 < emp2
```

Python internally calls:

```python
emp1.__lt__(emp2)
```

So you decide what `<` means (salary comparison, age comparison, etc.)

---

## ✅ Example 4: `__eq__` (equal `==`)

```python
emp1 == emp2
```

Python internally calls:

```python
emp1.__eq__(emp2)
```

---

# 🔥 Simple Definition

### Magic methods let you **customize the behavior of Python operators and built-in functions** for your class.

So your objects can behave like built-in types.

---

## ⭐ Real-Life Analogy

Python says:

> "If you define these special methods, I’ll automatically use them when needed."

That’s the magic.
