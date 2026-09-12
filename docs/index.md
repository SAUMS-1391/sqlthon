# Sqlthon

A simple package for SQLite3 operations.

## نصب

pip install sqlthon

## مثال

from sqlthon import Connect

db = Connect("test.db")
db.add_record("users", "Ali", 25)
db.save_to_data_base()
db.close()
