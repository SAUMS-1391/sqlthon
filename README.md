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
## Installation

```bash
pip install sqlthon
