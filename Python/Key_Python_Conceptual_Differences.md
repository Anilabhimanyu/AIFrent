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


