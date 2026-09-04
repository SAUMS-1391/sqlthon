import sqlite3 as sq


class DB:
    __slots__ = ("_con", "_cur", "_changes")
    def __init__(self, path: str) -> None:
        self._con = sq.connect(path)
        self._cur = self._con.cursor()
        self._changes = []
    
        
    class Column:
        __slots__ = ("_name", "_type", "_limits")
        def __init__(self, name_column: str, type: str="", limits: list=[]):
            self._name = name_column
            self._type = " "+type if type else ""
            self._limits = limits
    
    
    def add_table(self, name_table: str, *columns: Column, if_not_exist: bool=False) -> None:
        text = "CREATE TABLE "
        if if_not_exist:
            text += "IF NOT EXISTS "
        text += f"{name_table} ("
        for column in columns:
            text += column._name + column._type
            if column._limits:
                text += " " + str(column._limits).replace("[", "").replace("'", "").replace("]", "").replace(",", "")
            text += ", "
        text = f"{text[:-2]})"
        
        self._changes.append((text,))
    
    
    def add_record(self, name_table: str, *record: list) -> None:
        self._changes.append((f"INSERT INTO {name_table} VALUES ({"?, "*(len(record)-1)}?)", record))
    
    
    def find_table(self, word: str="") -> list:
        self._cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [tup[0] for tup in self._cur.fetchall()]
        return [table for table in tables if word in table]


    def find_record(self, name_table: str, columns: list|str="*", where: dict|str="") -> list:
        text = "SELECT "
        if type(columns) == list:
            columns = str(columns).replace("[", "").replace("]", "").replace("'", "")
        text += columns+" FROM "+name_table
        if where:
            equal = " WHERE " + str(list(where.keys())).replace("]", ", ").replace("[", "").replace("'", "").replace(", ", "=? and ")[:-5]
            where = tuple(where.values())
        try:
            text += equal
        except:
            pass
            
        self._cur.execute(text, where)
        return self._cur.fetchall()
    
    
    def delete_table(self, name_table: str):
        self._changes.append((f"DROP TABLE {name_table}",))
    
    
    def delete_record(self, name_table: str, info_record: dict={}) -> None:
        text = f"DELETE FROM {name_table}"
        if info_record:
            text += " WHERE "
            equal = tuple(info_record.values())
            info_record = str(list(info_record.keys())).replace("[", "").replace("'", "").replace("]", ", ").replace(", ", "=? ").replace(" ", " AND ")[:-5]
        try:
            equal
            self._changes.append((text+info_record, equal))
        except:
            self._changes.append((text,))
        
        
    def edit_record(self, name_table: str, new_record: dict, old_record: dict) -> None:
        text = "UPDATE "+name_table+" SET "
        equal = tuple(old_record.values())+tuple(new_record.values())
        old_record = str(list(old_record.keys())).replace("[", "").replace("'", "").replace("]", ", ").replace(", ", "=? ").replace(" ", ", ")[:-2]
        new_record = str(list(new_record.keys())).replace("[", "").replace("'", "").replace("]", ", ").replace(", ", "=? ").replace(" ", " AND ")[:-4]
        
        text += old_record+" WHERE "+new_record
        self._changes.append((text, equal))
    
    
    def run_code(self, code: str, parameters: tuple=()) -> list | None:
        self._cur.execute(code, parameters)
        self._con.commit()
        try:
            return self._cur.fetchall()
        except:
            pass
    
    
    def close(self):
        self._con.close()
    

    def save_to_data_base(self) -> None:
        with self._con:
            for sql_code in self._changes:
                self._cur.execute(*sql_code)
        self._changes.clear()