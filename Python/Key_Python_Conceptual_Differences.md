## Question: Difference between `sort()` and `sorted()` in Python

### ✅ `sort()`

* Works only on **lists**
* **Modifies the same list** (in-place)
* Returns **None**

Example:

```python
nums = [5, 2, 9]
nums.sort()
print(nums)   # [2, 5, 9]
```

---

### ✅ `sorted()`

* Works on **any iterable** (list, tuple, set, string, etc.)
* **Does not modify original**
* Returns a **new sorted list**

Example:

```python
nums = [5, 2, 9]
new_nums = sorted(nums)

print(nums)      # [5, 2, 9]
print(new_nums)  # [2, 5, 9]
```

---

### 🔥 Quick Summary Table

| Feature          | `sort()`      | `sorted()`         |
| ---------------- | ------------- | ------------------ |
| Works on         | Only list     | Any iterable       |
| Changes original | Yes           | No                 |
| Returns          | None          | New list           |
| Usage            | `list.sort()` | `sorted(iterable)` |

---

### ⭐ When to use?

* Use **`sort()`** if you want to update the same list.
* Use **`sorted()`** if you want to keep original data unchanged.

======================================

**Q: What is the difference between normal inheritance override and abstract class override?**

**A:**

* In **normal inheritance**, overriding a method is **optional** (child may or may not override).
* In **abstract class (ABC)**, overriding abstract methods is **mandatory** (child must override, otherwise object cannot be created).

======================================

**Q: Should an abstract class have `__init__` parameters?**
**A:** Not compulsory. Abstract class *may or may not* have `__init__`.

**Q: Should a child class implement all abstract methods?**
**A:** Yes. Child class *must* implement all abstract methods, otherwise object cannot be created.

**Q: What is mandatory in abstract class concept?**
**A:** Implementing abstract methods in child class is mandatory, not having `__init__`.

======================================
**Q: If `Employee.__lt__` compares salary, how can I sort tasks by deadline?**
**A:** `Employee.__lt__` is only used when sorting **Employee objects**. For tasks, Python uses `Task.__lt__` (if defined) or you can use `sorted(tasks, key=lambda x: x.deadline)` to sort by deadline.

======================================
**Q: If `__str__` is there, why does printing a list still show `<Task object at ...>`?**

**A:** Because when you print a **list**, Python does **not** use `__str__()` of objects.
It uses `__repr__()` of each object inside the list.

---

### Example

```python
print(task1)        # uses __str__
print([task1])      # uses __repr__
```

So:

* `print(task1)` → calls `task1.__str__()`
* `print([task1])` → calls `task1.__repr__()`

---

**Q: Then what happens if `__repr__` is not defined?**
**A:** Python uses default repr:

```
<__main__.Task object at 0x...>
```

---

✅ That’s why for clean list printing, define `__repr__` also.

===================================================

**Q: If `__repr__` is not there, will Python automatically use `__str__`?**
**A:** ❌ No, not always.

### ✅ Correct rule:

* If you do `print(obj)` → Python uses `__str__()`
* If `__str__` is missing → then Python falls back to `__repr__()`

So fallback is:

👉 **`__str__` missing → use `__repr__`**

---

**Q: If `__repr__` is missing, will it use `__str__`?**
**A:** ❌ No. Python will use default internal repr like:

```
<__main__.Task object at 0x...>
```

---

### ✅ Final Conclusion

✔ `print(obj)` prefers `__str__`
✔ If no `__str__`, then uses `__repr__`
❌ If no `__repr__`, it does NOT automatically use `__str__` (especially inside list printing)

============================================
## Composition + Dependency Injection (DI)
**Composition provides the structure. DI provides the flexibility.**
## How They Work Together
### **Composition** = Object Structure
```
class Car:                    # Composition
    def __init__(self, engine):  
        self.engine = engine   # HAS-A relationship
```
### **Dependency Injection** = Object Wiring
```
# WITHOUT DI (tight coupling)
class Car:
    def __init__(self):
        self.engine = Engine()  # Car KNOWS how to create Engine ❌

# WITH DI (loose coupling)  
class Car:
    def __init__(self, engine):  # Car receives dependency ✅
        self.engine = engine
```
## Complete Example: HR System
```python
# Dependencies (composed parts)
class Database:
    def save_employee(self, emp):
        print(f"Saved {emp['name']} to DB")

class EmailService:
    def send_notification(self, emp):
        print(f"Email sent to {emp['name']}")

# Main class using composition + DI
class HRSystem:
    def __init__(self, db: Database, email: EmailService):  # DI via constructor
        self.db = db              # Composition (has-a)
        self.email = email        # Composition (has-a)
    
    def onboard_employee(self, emp):
        self.db.save_employee(emp)
        self.email.send_notification(emp)

# Usage - Easy to swap dependencies
db = Database()
email = EmailService()
hr = HRSystem(db, email)  # Inject dependencies

# For testing, inject mocks
mock_db = MockDatabase()
test_hr = HRSystem(mock_db, email)
```
## Key Benefits
| Without DI | With DI + Composition |
|------------|----------------------|
| `Car` creates `Engine` | `Car` receives `Engine` |
| Hard to test | Easy unit testing |
| Tight coupling | Loose coupling |
| Hard to swap | Dependencies swappable |
## Real-World Pattern
```
1. Define interfaces/protocols
2. Use composition (self.service = service)
3. Inject via constructor
4. Test with mock dependencies
```

**Composition** = **"What parts do I need?"**  
**DI** = **"Someone else provides those parts"**

**Result**: Flexible, testable, maintainable code [stackoverflow](https://stackoverflow.com/questions/11945182/how-does-dependency-injection-aid-object-composition)
=======================================

