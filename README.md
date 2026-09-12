# **Sqlthon**

A simple package for SQLite3 operations.


## Quick Start
```python
from sqlthon import Connect

db = Connect('PATH_FILE')

db.add_table(
    'TABLE_NAME',
    db.Column(name='NAME_COLUMN')
)

db.add_record(
    'TABLE_NAME',
    ['VALUE']
)

db.save_to_data_base()
```

## پارامترهای add_table

| پارامتر | نوع | ضروری | توضیح |
|---------|-----|-------|-------|
| `name_table` | `str` | ✅ | نام جدول |
| `*columns` | `Column` | ✅ | ستون‌های جدول |
| `if_not_exist` | `bool` | ❌ | اگه True باشه، خطا نمیده |
## Installation

```bash
pip install sqlthon
