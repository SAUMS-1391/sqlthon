from .core import _Aggregate
STR = "TEXT"
INT = "INTEGER"
FLOAT = "REAL"
BOOL = "BOOLEAN"
BLOB = "BLOB"



UNIQUE = "UNIQUE"
NOT_NULL = "NOT NULL"
PRIMARY_KEY = "PRIMARY KEY"
AUTO_INCREMENT = "AUTOINCREMENT"

LEFT = "LEFT"
INNER = "INNER"


def DEFAULT(value):
    if isinstance(value, str):
        return f"DEFAULT '{value}'"
    elif value is None:
        return "DEFAULT NULL"
    else:
        return f"DEFAULT {value}"

def CHECK(condition):
    return f"CHECK ({condition})"

def FOREIGN_KEY(table, column="id"):
    return f"REFERENCES {table}({column})"

CURRENT_TIMESTAMP = "CURRENT_TIMESTAMP"

def DEFAULT_NOW():
    return f"DEFAULT {CURRENT_TIMESTAMP}"



def COUNT(query="*"):
    return _Aggregate("COUNT", query)

def SUM(query):
    return _Aggregate("SUM", query)

def AVG(query):
    return _Aggregate("AVG", query)

def MIN(query):
    return _Aggregate("MIN", query)

def MAX(query):
    return _Aggregate("MAX", query)
