'''

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