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

