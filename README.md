# **Sqlthon**

A simple package for SQLite3 operations.


## Quick Start
```python
from sqlthon import Connect, Field
from sqlthon.keywords import *

with Connect("test.db") as db:
    db.add_table(
        "users",
        ("id", INT, [PRIMARY_KEY, AUTO_INCREMENT]),
        ("name", STR, [NOT_NULL]),
        ("email", STR, [UNIQUE])
    )
    db.add_record("users", (1, "Ali", "ali@example.com"))
    db.save_to_database()
    
    result = db.find_record("users", condition=Field("id") == 1)
    print(result)
```

---

## Document
https://sqlthon.readthedocs.io/fa/latest

## Installation

```bash
pip install sqlthon
