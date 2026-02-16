# Activity set 6: Abstraction + Polymorphism (Payroll_system)

## Abstract Classes Theory
**Abstract Classes** define a blueprint with some methods left unimplemented. **Polymorphism** lets objects of different classes respond to the same method call differently.

### **Purpose**
- Force subclasses to implement specific methods
- Define common interface + shared code
- Cannot be instantiated directly

### **Syntax (Python `abc` module)**
```python
from abc import ABC, abstractmethod

class Shape(ABC):           # Abstract base class
    @abstractmethod
    def area(self):         # Must be implemented by subclasses
        pass
    
    def common_method(self):  # Concrete method (shared)
        print("Common behavior")
```

## Polymorphism Theory

### **Core Idea**
"One interface, multiple implementations"
```
shapes = [Circle(), Square(), Triangle()]
for shape in shapes:
    print(shape.area())  # Each calls its OWN area() method
```

### **How It Works**
1. **Parent reference** holds **child objects**
2. **Method call** resolves to child's implementation (dynamic dispatch)
3. Same **method name**, different **behaviors**

## Relationship
```
Abstract Class → ENFORCES Polymorphism
Polymorphism   → ENABLED BY Abstract Classes
```

## Decision Guide
| Use Case | Abstract Class | Interface |
|----------|---------------|-----------|
| Shared code + contract | ✓ Abstract Class | ✗ Interface only |
| Pure contract | Interface | Interface |
| Python preference | Abstract classes | Protocols/dataclasses |

**Abstract classes = Template + Polymorphism enforcer**

## Interface vs Abstract Class

### **Abstract Class**
**CAN have**: Concrete methods + abstract methods + attributes
```
class Shape(ABC):
    def common_method(self):      # ✅ Concrete (shared code)
        print("All shapes have area")
    
    @abstractmethod
    def area(self): pass         # Must implement
```

### **Interface** 
**ONLY has**: Abstract methods (method signatures, NO implementation)
```
class Drawable(Protocol):     # Python uses Protocol/Zope Interface
    def draw(self): ...        # ONLY signature, no body
    def area(self): ...
```

## Key Differences

| Feature | Abstract Class | Interface |
|---------|----------------|-----------|
| **Concrete methods** | ✅ Yes | ❌ No |
| **Attributes/State** | ✅ Yes | ❌ No |
| **Constructor** | ✅ Yes | ❌ No |
| **Inheritance** | Single (Python allows multiple) | Multiple |
| **Purpose** | "is-a" + shared code | "can-do" contract |

## Python Reality
**Python has NO formal interfaces**. Uses:
1. **Abstract Classes** (`abc.ABC`) - Most common
2. **Protocols** (`typing.Protocol`) - Structural typing
3. **Zope Interface** - Explicit interfaces

## Decision Guide
```
Need shared code?     → Abstract Class
Pure contract only?   → Protocol/Abstract Class
Multiple behaviors?   → Multiple inheritance of ABCs
```

**Python mantra**: "Abstract classes cover 99% of interface use cases"

# Activity set7: Real World Error Handling & Custom Exceptions
# Real World Error Handling & Custom Exceptions

Custom exceptions make code **production-ready** by providing **specific, meaningful errors** instead of generic ones.

## Custom Exception Theory

### **Why Custom Exceptions?**
```
❌ Generic: "ValueError: Invalid input"
✅ Specific: "InsufficientFundsError: Balance $100 < Withdrawal $200"
```

### **Structure**
```python
class CustomError(Exception):
    def __init__(self, message, code=None, data=None):
        self.message = message
        self.code = code
        self.data = data
        super().__init__(self.message)
```

## HR System: Real-World Examples

```python
# Custom Exceptions
class InsufficientFundsError(Exception):
    """Raised when salary deduction exceeds available funds"""
    pass

class InvalidEmployeeIdError(Exception):
    """Raised for invalid/non-existent employee ID"""
    pass

class PromotionDeniedError(Exception):
    """Raised when employee not eligible for promotion"""
    def __init__(self, reason):
        super().__init__(f"Promotion denied: {reason}")

class HRSystem:
    def __init__(self):
        self.employees = {
            1001: {"name": "Alice", "salary": 50000, "department": "Engineering"},
            1002: {"name": "Bob", "salary": 60000, "department": "HR"}
        }
    
    def get_employee(self, emp_id):
        """Fetch employee with validation"""
        if emp_id not in self.employees:
            raise InvalidEmployeeIdError(f"Employee ID {emp_id} not found")
        return self.employees[emp_id]
    
    def process_overtime(self, emp_id, hours, rate=100):
        """Real-world: Payroll overtime processing"""
        try:
            emp = self.get_employee(emp_id)
            overtime_pay = hours * rate
            
            if overtime_pay > emp["salary"] * 0.5:  # Business rule
                raise PromotionDeniedError("Overtime exceeds 50% of salary")
            
            print(f"✅ Processed {hours} hours overtime: ₹{overtime_pay}")
            return overtime_pay
            
        except InvalidEmployeeIdError as e:
            print(f"❌ ID Error: {e}")
            return 0
        except PromotionDeniedError as e:
            print(f"⚠️  Policy: {e}")
            return 0
        except Exception as e:
            print(f"💥 Unexpected: {type(e).__name__}: {e}")
            raise  # Re-raise for logging

# Real-world usage
hr = HRSystem()
hr.process_overtime(1001, 10)      # ✅ Works
hr.process_overtime(1005, 5)       # ❌ Invalid ID
hr.process_overtime(1001, 400)     # ⚠️ Policy violation
```

## Output
```
✅ Processed 10 hours overtime: ₹1000
❌ ID Error: Employee ID 1005 not found
⚠️  Policy: Promotion denied: Overtime exceeds 50% of salary
```

## Best Practices
```
1. Inherit from Exception (not BaseException)
2. Specific > Generic naming
3. Include context (codes, data)
4. Document purpose
5. Handle + Log + Re-raise when needed
```

**Production Code Pattern**: Custom exceptions + `try/except` + Logging

==============================================

