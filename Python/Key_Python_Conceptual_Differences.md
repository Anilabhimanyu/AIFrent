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

