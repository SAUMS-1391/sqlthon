class Field:
    __slots__ = ("name",)
    def __init__(self, name):
        _analysis_code(name)
        self.name = name
    
    def __gt__(self, value): return _Expression(self, ">", value)
    def __lt__(self, value): return _Expression(self, "<", value)
    def __ge__(self, value): return _Expression(self, ">=", value)
    def __le__(self, value): return _Expression(self, "<=", value)
    def __eq__(self, value): return _Expression(self, "=", value)
    def __ne__(self, value): return _Expression(self, "!=", value)
    def __invert__(self): return _Expression(self, "NOT", None)
    def not_like(self, value): return _Expression(self, "NOT LIKE", value)
    def like(self, value):
        return _Expression(self, "LIKE", value)
    def startswith(self, value):
        return _Expression(self, "LIKE", f"{value}%")
    def endswith(self, value):
        return _Expression(self, "LIKE", f"%{value}")
    def contains(self, value):
        return _Expression(self, "LIKE", f"%{value}%")
    def in_(self, value):
        return _Expression(self, "IN", value)
    def not_in(self, value):
        return _Expression(self, "NOT IN", value)
    def between(self, value):
        return _Expression(self, "BETWEEN", value)
    def is_null(self):
        return _Expression(self, "IS NULL", None)
    def is_not_null(self):
        return _Expression(self, "IS NOT NULL", None)


class _Expression:
    __slots__ = ("left", "op", "right")
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    
    def __and__(self, other):
        return _Expression(self, "AND", other)
    def __or__(self, other):
        return _Expression(self, "OR", other)


class _Aggregate:
    __slots__ = ("func", "column")
    def __init__(self, func, column="*"):
        if not column == "*":
            _analysis_code(column)
        self.func = func
        self.column = column
    
    def __gt__(self, value): return _Expression(self, ">", value)
    def __lt__(self, value): return _Expression(self, "<", value)
    def __ge__(self, value): return _Expression(self, ">=", value)
    def __le__(self, value): return _Expression(self, "<=", value)
    def __eq__(self, value): return _Expression(self, "=", value)
    def __ne__(self, value): return _Expression(self, "!=", value)
    
    def __str__(self):
        return f"{self.func}({self.column})"


def _compile(expr):
    if isinstance(expr.left, _Expression) or isinstance(expr.right, _Expression):
        left_sql, left_params = _compile(expr.left)
        right_sql, right_params = _compile(expr.right)
        sql = f"({left_sql}) {expr.op} ({right_sql})"
        params = left_params + right_params
        return sql, params
    elif expr.op in ("IN", "NOT IN"):
        placeholders = ", ".join(["?"] * len(expr.right))
        sql = f'"{expr.left.name}" {expr.op} ({placeholders})'
        params = tuple(expr.right)
        return sql, params
    elif expr.op == "BETWEEN":
        sql = f'"{expr.left.name}" BETWEEN ? AND ?'
        params = tuple(expr.right)
        return sql, params
    elif expr.op in ("IS NULL", "IS NOT NULL"):
        sql = f'"{expr.left.name}" {expr.op}'
        return sql, ()
    elif isinstance(expr.left, _Aggregate):
        sql = f"{expr.left} {expr.op} ?"
        params = (expr.right,)
        return sql, params
    else:
        sql = f'"{expr.left.name}" {expr.op} ?'
        params = (expr.right,)
        return sql, params


def _analysis_code(query):
    from re import match
    if isinstance(query, (list, tuple)):
        for i in query:
            _analysis_code(i)
        return
    if not match("^[A-Za-z_][A-Za-z0-9_.(), ]*$", query) or any(word in query.lower() for word in ("sqlite_", "union", "select", "blob", "pragma")):
        for i in {"NOT", "NULL", "PRIMARY", "KEY", "UNIQUE", "DEFAULT",
            "CHECK", "AUTOINCREMENT", "REFERENCES", "COLLATE",
            "TRUE", "FALSE", "CURRENT_TIMESTAMP", "ON", "DELETE",
            "UPDATE", "CASCADE", "RESTRICT", "SET", "NO", "ACTION",
            "PRECISION", "DOUBLE", "UNSIGNED", "BIG", "INT",
            "NATIVE", "CHARACTER", "VARYING",}:
            if not i in query:
                raise YouHackerError(f"you hacker for {query!r}.") from None


class Connect:
    __slots__ = ("_con", "_cur", "_changes", "_path")
    def __init__(self, database_path: str) -> None:
        from sqlite3 import connect as _cn
        self._path = database_path
        self._con = _cn(database_path)
        self._cur = self._con.cursor()
        self._changes: list = []
        del _cn
    
    # ____________| TABLE |____________
    def add_table(self, table_name: str, *columns: tuple, if_not_exists=False) -> None:
        _analysis_code(table_name)
        query = "CREATE TABLE "
        if if_not_exists:
            query += "IF NOT EXISTS "
        query += f"{table_name} ("
        for column in columns:
            _analysis_code(column)
            name, type = column[0], column[1]
            try:
                limits = column[2]
                query += f"""{name} {type} {" ".join(limits)}"""
            except:
                query += f"{name} {type}"

            query += ", "
        query = query[:-2]+")"
        self._changes.append((query,))
    
    def rename_table(self, old_name_table: str, new_name_table: str) -> None:
        _analysis_code(old_name_table)
        _analysis_code(new_name_table)
        self._changes.append((f"ALTER TABLE {old_name_table} RENAME TO {new_name_table}",))
        
    def drop_table(self, table_name: str) -> None:
        _analysis_code(table_name)
        self._changes.append((f"DROP TABLE {table_name}",))
    
    def exist_table(self, table_name: str) -> bool:
        _analysis_code(table_name)
        return table_name in [i[0] for i in self._cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
    
    def copy_table(self, table_name: str, new_name_table: str) -> None:
        _analysis_code(table_name)
        _analysis_code(new_name_table)
        self._changes.append((f"CREATE TABLE {new_name_table} AS SELECT * FROM {table_name}",))
    
    def get_tables(self) -> list:
        return [i[0] for i in self._cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
    
    # ____________| COLUMN |____________
    def add_column(self, table_name: str, column_name: str, column_type: str, limits: list | str=[]) -> None:
        _analysis_code(table_name)
        _analysis_code(column_name)
        _analysis_code(column_type)
        if limits:
            _analysis_code(limits)
            limits = " ".join(limits)
        else:
            limits = ""
        self._changes.append((f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type} {limits}",))
    
    def drop_column(self, table_name: str, column_name: str) -> None:
        _analysis_code(table_name)
        _analysis_code(column_name)
        self._changes.append((f"ALTER TABLE {table_name} DROP COLUMN {column_name}",))
    
    def rename_column(self, table_name: str, old_name_column: str, new_name_column: str) -> None:
        _analysis_code(table_name)
        _analysis_code(old_name_column)
        _analysis_code(new_name_column)
        self._changes.append((f"ALTER TABLE {table_name} RENAME COLUMN {old_name_column} TO {new_name_column}",))
    
    def exist_column(self, table_name: str, column_name: str) -> bool:
        _analysis_code(table_name)
        _analysis_code(column_name)
        return column_name in [i[1] for i in self._cur.execute(f"PRAGMA table_info({table_name})").fetchall()]
    
    def get_columns(self, table_name: str) -> list:
        _analysis_code(table_name)
        return [i[1] for i in self._cur.execute(f"PRAGMA table_info({table_name})").fetchall()]
    
    # ____________| RECORD |____________
    def find_record(self, table_name: str, columns: None | tuple=None, compound: None | tuple=None, condition: None | _Expression=None, bundle: None | tuple=None, filter_bundle: None | tuple=None, sort: None | tuple=None, several: None | int=None, jump: int=0, unique: bool=False):
        _analysis_code(table_name)
        query = "SELECT "
        param = ()
        if unique:
            query += "DISTINCT "
        if columns:
            _analysis_code(columns)
        query += f"""{", ".join(columns) if columns else "*"} FROM {table_name}"""
        if compound:
            if compound[0].upper() not in ("INNER", "LEFT"):
                raise YouHackerError(f"you hacker for {query!r}.") from None
            _analysis_code(compound)
            query += f" {compound[0]} JOIN \"{compound[1]}\" ON {compound[2]} = {compound[3]}"
        if condition:
            _: tuple = _compile(condition)
            query += f" WHERE {_[0]}"
            param += _[1]
            del _
        if bundle:
            _analysis_code(bundle)
            query += f" GROUP BY {", ".join(bundle)}"
        if filter_bundle:
            __: tuple = _compile(filter_bundle)
            query += f" HAVING {__[0]}"
            param += __[1]
            del __
            
        if sort:
            _analysis_code(sort)
            query += " ORDER BY "
            if sort[-1].upper() == "ASC" or sort[-1].upper() == "DESC":
               query += f"{", ".join(sort[:-1])} {sort[-1]}"
            else:
                query += ", ".join(sort)
        if several is not None:
            if not isinstance(several, int):
                raise YouHackerError(f"you hacker for {several!r}.")
            query += f" LIMIT {several}"
            if jump:
                if not isinstance(jump, int):
                    raise YouHackerError(f"you hacker for {jump!r}.")
                query += f" OFFSET {jump}"
        return self._cur.execute(query, param).fetchall()
        
    def add_record(self, table_name: str, record_info: tuple) -> None:
        _analysis_code(table_name)
        self._changes.append((f"""INSERT INTO {table_name} VALUES({", ".join(["?"]*len(record_info))})""", record_info))
    
    def add_records(self, table_name: str, info_records: tuple) -> None:
        _analysis_code(table_name)
        try:
            self._cur.executemany(f"""INSERT INTO {table_name} VALUES ({", ".join(["?"]*len(info_records[0]))})""", info_records)
            self._con.commit()
        except Exception as e:
            _handler_error(e)
        
    def delete_record(self, table_name, condition):
        _analysis_code(table_name)
        query = f"DELETE FROM {table_name}"
        sql_where, params = _compile(condition)
        query += " WHERE " + sql_where
        self._changes.append((query, params))
    
    def delete_all_record(self, table_name: str) -> None:
        _analysis_code(table_name)
        self._changes.append((f"DELETE FROM {table_name}",))
    
    def edit_record(self, table_name, new_info_record, condition=None):
        _analysis_code(table_name)
        query = f"UPDATE {table_name} SET "
        params = ()
        
        set_parts = []
        for key, value in new_info_record.items():
            _analysis_code(key)
            set_parts.append(f'"{key}" = ?')
            params += (value,)
        query += ", ".join(set_parts)
        
        if condition:
            sql_where, where_params = _compile(condition)
            query += " WHERE " + sql_where
            params += where_params
        
        self._changes.append((query, params))
    
    def count_record(self, table_name: str) -> int:
        _analysis_code(table_name)
        return self._cur.execute(f"SELECT COUNT(*) FROM {table_name}").fetchall()[0][0]
    
    def upsert_record(self, table_name: str, info_record: tuple, conflict: tuple) -> None:
        _analysis_code(table_name)
        _analysis_code(conflict)
        query = f"""INSERT INTO {table_name} VALUES ({", ".join(["?"]*len(info_record))}) ON CONFLICT(\"{'", "'.join(conflict)}\") DO UPDATE SET """
        param = info_record
        colue = dict(zip(self.get_columns(table_name), info_record)) # columns value
        for i in conflict:
            del colue[i]
        for key, value in colue.items():
            query += f'"{key}"=?, '
            param += (value,)
        query = query[:-2]
        self._changes.append((query, param))
    
    # ____________| INDEX |_________
    def add_index(self, table_name: str, column_name: str, unique: bool=False) -> None:
        _analysis_code(table_name)
        _analysis_code(column_name)
        self._changes.append((f"CREATE INDEX{" UNIQUE" if unique else ""} {table_name}_{column_name} ON {table_name} ({column_name})",))
    
    def delete_index(self, table_name: str, column_name: str) -> None:
        _analysis_code(table_name)
        _analysis_code(column_name)
        self._changes.append((f"DROP INDEX {table_name}_{column_name}",))
    
    # ____________| VIEW |_________
    def add_view(self, view_name: str, query: str) -> None:
        raise YouHackerError("add_view is disabled for security reasons.")
    
    def delete_view(self, view_name: str) -> None:
        _analysis_code(view_name)
        self._changes.append((f"DROP VIEW {view_name}",))
    
    def exist_view(self, view_name: str) -> bool:
        _analysis_code(view_name)
        return view_name in [i[0] for i in self._cur.execute("SELECT name FROM sqlite_master WHERE type='view'").fetchall()]
    
    # ____________| BACKUP |_________
    def backup_database(self, backup_path: str | None=None) -> None:
        from shutil import copy2
        from os.path import abspath, dirname, join
        self._con.commit()
        allowed_dir = dirname(abspath(self._path))
        if backup_path:
            if not abspath(backup_path).startswith(allowed_dir):
                raise YouHackerError(f"you hacker for {backup_path!r}.")
            copy2(self._path, backup_path)
        else:
            copy2(self._path, join(allowed_dir, "backup.db"))
    
    # ____________| PANDAS |_________
    def to_dataframe(self, table_name: str) -> "pd.DataFrame":
        _analysis_code(table_name)
        import pandas as pd
        columns = self.get_columns(table_name)
        result = self._cur.execute(f"SELECT * FROM {table_name}").fetchall()
        return pd.DataFrame(result, columns=columns)
    
    # ____________| CSV |_________
    def load_csv(self, table_name: str, csv_path: str) -> None:
        _analysis_code(table_name)
        from os.path import abspath, dirname
        allowed_dir = dirname(abspath(self._path))
        if not abspath(csv_path).startswith(allowed_dir):
            raise YouHackerError(f"you hacker for {csv_path!r}.")
        import csv as _csv
        
        with open(csv_path) as file:
            reader = _csv.reader(file)
            header = next(reader)
            
            self.add_table(table_name, (header[0], "TEXT"))
            for column in header[1:]:
                self.add_column(table_name, column, "TEXT")
            
            self.save_to_database()
            
            records = []
            for row in reader:
                records.append(tuple(row))
            if records:
                self.add_records(table_name, tuple(records))
            
    def to_csv(self, table_name: str, csv_path: str) -> None:
        _analysis_code(table_name)
        from os.path import abspath, dirname
        allowed_dir = dirname(abspath(self._path))
        if not abspath(csv_path).startswith(allowed_dir):
            raise YouHackerError(f"you hacker for {csv_path!r}.")
        import csv as _csv
        with open(csv_path, "w") as f:
            writer = _csv.writer(f)
            writer.writerow(self.get_columns(table_name))
            for row in self.find_record(table_name):
                writer.writerow(row)
    
    # ____________| OTHER |_________
    def last_id(self) -> int:
        return self._cur.execute("SELECT last_insert_rowid()").fetchall()[0][0]
    
    def database_info(self) -> dict:
        from os.path import basename, exists, getsize
        return {
            "name": basename(self._path),
            "size": getsize(self._path) if exists(self._path) else 0,
            "count_tables": len(self.get_tables())
        }
    
        
    # ____________| BASIC |_________
    def run_query(self, code: str, parameters: tuple=()) -> list:
        raise YouHackerError("run_query is disabled for security reasons.")
        
    def optimize(self) -> None:
        self.save_to_database()
        self._cur.execute("VACUUM")
        self._con.commit()

    def save_to_database(self) -> None:
        try:
            with self._con:
                for sql_code in self._changes:
                    self._cur.execute(*sql_code)
            self._changes.clear()
        except Exception as e:
            _handler_error(e)
    
    def close(self):
        self._con.close()
    
    # ____________| MAGICALS |_________
    def __enter__(self) -> "Connect":
        return self
    
    def __exit__(self, exc_type, exc_value, exc_tb) -> None:
        self.save_to_database()
        self.close()
        

# ____________| ERRORS |_________
class SqlthonError(Exception):__module__ = None
class YouHackerError(SqlthonError, PermissionError):__module__ = None
class TableError(SqlthonError):__module__ = None
class TableNotFoundError(TableError):__module__ = None
class TableAlreadyExistsError(TableError):__module__ = None
class ColumnError(SqlthonError):__module__ = None
class ColumnNotFoundError(ColumnError):__module__ = None
class RecordError(SqlthonError):__module__ = None
class UniqueConstraintError(RecordError):__module__ = None
class NotNullConstraintError(RecordError):__module__ = None
class DataTypeError(RecordError):__module__ = None
class ForeignKeyError(RecordError):__module__ = None
class CheckConstraintError(RecordError):__module__ = None
class PrimaryKeyError(RecordError):__module__ = None
class QueryError(SqlthonError):__module__ = None
class SyntaxError_(QueryError):__module__ = None
class NoSuchFunctionError(QueryError):__module__ = None
class WrongNumberOfArgumentsError(QueryError):__module__ = None
class DatabaseError(SqlthonError):__module__ = None
class DatabaseLockedError(DatabaseError):__module__ = None
class DatabaseReadOnlyError(DatabaseError):__module__ = None
class DatabaseCorruptError(DatabaseError):__module__ = None
class DatabaseFullError(DatabaseError):__module__ = None
class DatabaseBusyError(DatabaseError):__module__ = None
class IndexError_(SqlthonError):__module__ = None
class IndexNotFoundError(IndexError_):__module__ = None
class IndexAlreadyExistsError(IndexError_):__module__ = None
class ViewError(SqlthonError):__module__ = None
class ViewNotFoundError(ViewError):__module__ = None
class ViewAlreadyExistsError(ViewError):__module__ = None
class TransactionError(SqlthonError):__module__ = None
class TransactionAlreadyActiveError(TransactionError):__module__ = None
class TransactionNotActiveError(TransactionError):__module__ = None
class BackupError(SqlthonError):__module__ = None
class BackupPathError(BackupError):__module__ = None
class BackupPermissionError(BackupError):__module__ = None
class CsvError(SqlthonError):__module__ = None
class CsvFileNotFoundError(CsvError):__module__ = None
class CsvFormatError(CsvError):__module__ = None
class PandasError(SqlthonError):__module__ = None
class PandasNotInstalledError(PandasError):__module__ = None
class ValidationError(SqlthonError):__module__ = None
class InvalidColumnCountError(ValidationError):__module__ = None
class InvalidValueError(ValidationError):__module__ = None


def _handler_error(e: Exception):
            msg = str(e).lower()
            
            if "no such table" in msg:
                raise TableNotFoundError(f"no table with name {msg.split()[-1]!r}.") from None
            
            elif "already exists" in msg:
                raise TableAlreadyExistsError(f"table {msg.split()[1]!r} alredy existed.") from None
                
            elif "no such column" in msg:
                raise ColumnNotFoundError(f"no column with name {msg.split()[-1]!r}.") from None
            
            elif "unique constraint" in msg:
                raise UniqueConstraintError(f"this field {msg.split()[-1]!r} already existed.") from None
            
            elif "not null constraint" in msg:
                raise NotNullConstraintError(f"this field cannot be left empty and you sent it {msg.split()[-1]!r}.") from None
            
            elif "datatype mismatch" in msg:
                raise DataTypeError(msg) from None
            
            elif "foreign key constraint" in msg:
                raise ForeignKeyError(msg) from None
            
            elif "check constraint" in msg:
                raise CheckConstraintError(f"check constraint failed {msg.split(": ")[-1]!r}.") from None
            
            elif "primary key" in msg:
                raise PrimaryKeyError(msg) from  None
            
            elif "no such function" in msg:
                raise NoSuchFunctionError(f"no function with name {msg.split()[-1]!r}.") from None
            
            elif "wrong number of arguments" in msg:
                raise WrongNumberOfArgumentsError(msg) from None
            
            elif "syntax error" in msg:
                raise SyntaxError_(f"invalid {msg.split()[-1].replace('"', "'")}") from None
            
            elif "database is locked" in msg:
                raise DatabaseLockedError(msg) from None
            
            elif "readonly database" in msg:
                raise DatabaseReadOnlyError(msg) from None
            
            elif "malformed" in msg:
                raise DatabaseCorruptError(msg) from None
            
            elif "disk is full" in msg:
                raise DatabaseFullError(msg) from None
            
            elif "database is busy" in msg:
                raise DatabaseBusyError(msg) from None
            
            elif "no such index" in msg:
                raise IndexNotFoundError(f"no index with name {msg.split()[-1]!r}.") from None
            
            elif "index already exists" in msg:
                raise IndexAlreadyExistsError(f"index {msg.split()[1]!r} already existed.") from None
            
            elif "no such view" in msg:
                raise ViewNotFoundError(f"no view with name {msg.split()[-1]!r}.") from None
            
            elif "view already exists" in msg:
                raise ViewAlreadyExistsError(f"view {msg.split()[1]!r} already existed.") from None
            
            elif "transaction within a transaction" in msg:
                raise TransactionAlreadyActiveError(msg) from None
            
            elif "no transaction is active" in msg:
                raise TransactionNotActiveError(msg) from None
            
            else:
                raise SqlthonError(msg) from None
