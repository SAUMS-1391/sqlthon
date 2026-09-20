# **Sqlthon**
*A Simple Package For SQLite3 Operations.*

---

## نصب

```bash
pip install sqlthon
```

---

## شروع سریع

```python
from sqlthon import Connect, Field
from sqlthon.keywords import *

db = Connect("test.db")

db.add_table(
    "users",
    ("id", INT, [PRIMARY_KEY, AUTO_INCREMENT]),
    ("name", STR, [NOT_NULL]),
    ("email", STR, [UNIQUE])
)

db.add_record("users", (1, "Ali", "ali@example.com"))
db.save_to_data_base()

result = db.find_record("users", condition=Field("id") == 1)
print(result)

db.close()
```

---

## Connect

کلاس اصلی برای اتصال به دیتابیس.

| پارامتر | اجباری/اختیاری | نوع | توضیحات |
|---------|----------------|-----|---------|
| `database_path` | اجباری | `str` | مسیر فایل دیتابیس |

```python
db = Connect("test.db")
```

---

## Table

### add_table

ساخت جدول جدید.

| پارامتر | اجباری/اختیاری | نوع | توضیحات |
|---------|----------------|-----|---------|
| `table_name` | اجباری | `str` | نام جدول |
| `*columns` | اجباری | `tuple` | مشخصات ستون‌ها |
| `if_not_exists` | اختیاری | `bool` | اگر `True` باشد و جدول وجود داشته باشد، ارور نمی‌دهد. پیش‌فرض `False` |

**ساختار هر ستون:**
```python
(column_name, column_type, [limits])
```

```python
db.add_table(
    "users",
    ("id", INT, [PRIMARY_KEY, AUTO_INCREMENT]),
    ("name", STR, [NOT_NULL]),
    ("email", STR, [UNIQUE])
)

db.add_table("logs", ("message", STR), if_not_exists=True)
```

### rename_table

تغییر نام جدول.

| پارامتر | اجباری/اختیاری | نوع |
|---------|----------------|-----|
| `old_name_table` | اجباری | `str` |
| `new_name_table` | اجباری | `str` |

```python
db.rename_table("users", "members")
```

### drop_table

حذف کامل جدول.

| پارامتر | اجباری/اختیاری | نوع |
|---------|----------------|-----|
| `table_name` | اجباری | `str` |

```python
db.drop_table("users")
```

### exist_table

بررسی وجود جدول.

| پارامتر | اجباری/اختیاری | نوع |
|---------|----------------|-----|
| `table_name` | اجباری | `str` |

**خروجی:** `bool`

```python
if db.exist_table("users"):
    print("وجود دارد")
```

### copy_table

کپی جدول.

| پارامتر | اجباری/اختیاری | نوع |
|---------|----------------|-----|
| `table_name` | اجباری | `str` |
| `new_name_table` | اجباری | `str` |

```python
db.copy_table("users", "users_backup")
```

---

## Column

### add_column

اضافه کردن ستون جدید.

| پارامتر | اجباری/اختیاری | نوع |
|---------|----------------|-----|
| `table_name` | اجباری | `str` |
| `column_name` | اجباری | `str` |
| `column_type` | اجباری | `str` |
| `limits` | اختیاری | `list` |

```python
db.add_column("users", "email", STR, [UNIQUE])
```

### drop_column

حذف ستون.

| پارامتر | اجباری/اختیاری | نوع |
|---------|----------------|-----|
| `table_name` | اجباری | `str` |
| `column_name` | اجباری | `str` |

```python
db.drop_column("users", "tel")
```

### rename_column

تغییر نام ستون.

| پارامتر | اجباری/اختیاری | نوع |
|---------|----------------|-----|
| `table_name` | اجباری | `str` |
| `old_name_column` | اجباری | `str` |
| `new_name_column` | اجباری | `str` |

```python
db.rename_column("users", "name", "full_name")
```

### exist_column

بررسی وجود ستون.

| پارامتر | اجباری/اختیاری | نوع |
|---------|----------------|-----|
| `table_name` | اجباری | `str` |
| `column_name` | اجباری | `str` |

**خروجی:** `bool`

```python
if db.exist_column("users", "email"):
    print("ستون وجود دارد")
```

### get_columns

دریافت لیست ستون‌ها.

| پارامتر | اجباری/اختیاری | نوع |
|---------|----------------|-----|
| `table_name` | اجباری | `str` |

**خروجی:** `list`

```python
columns = db.get_columns("users")
print(columns)  # ['id', 'name', 'email']
```

---

## Record

### add_record

اضافه کردن رکورد جدید.

| پارامتر | اجباری/اختیاری | نوع |
|---------|----------------|-----|
| `table_name` | اجباری | `str` |
| `record_info` | اجباری | `tuple` |

```python
db.add_record("users", (1, "Ali", "ali@example.com"))
```

### find_record

جستجوی رکوردها. این متد قدرتمندترین متد پکیج است.

| پارامتر | اجباری/اختیاری | نوع | توضیحات |
|---------|----------------|-----|---------|
| `table_name` | اجباری | `str` | نام جدول |
| `columns` | اختیاری | `tuple` | ستون‌های مورد نظر |
| `compound` | اختیاری | `tuple` | اتصال به جدول دیگر |
| `condition` | اختیاری | `_Expression` | شرط فیلتر (WHERE) |
| `bundle` | اختیاری | `tuple` | گروه‌بندی (GROUP BY) |
| `filter_bundle` | اختیاری | `_Expression` | شرط گروه (HAVING) |
| `sort` | اختیاری | `tuple` | مرتب‌سازی (ORDER BY) |
| `several` | اختیاری | `int` | تعداد رکورد (LIMIT) |
| `jump` | اختیاری | `int` | پرش (OFFSET) |
| `unique` | اختیاری | `bool` | حذف تکراری (DISTINCT) |

**خروجی:** `list`

```python
# ساده
db.find_record("users")

# با ستون‌های خاص
db.find_record("users", columns=("name", "age"))

# با شرط
db.find_record("users", condition=Field("age") > 18)

# با شرط ترکیبی
db.find_record(
    "users",
    condition=(Field("age") > 18) & (Field("city") == "Tehran")
)

# با مرتب‌سازی
db.find_record("users", sort=("name", "DESC"))

# با گروه‌بندی
db.find_record(
    "users",
    columns=("city", COUNT()),
    bundle=("city",)
)

# با شرط گروه
db.find_record(
    "users",
    columns=("city", COUNT()),
    bundle=("city",),
    filter_bundle=COUNT() > 5
)

# با اتصال
db.find_record(
    "users",
    columns=("users.name", "orders.price"),
    compound=("LEFT", "orders", "users.id", "orders.user_id")
)

# با محدودیت
db.find_record("users", several=10, jump=5)

# با حذف تکراری
db.find_record("users", columns=("city",), unique=True)
```

**compound (JOIN):**
```python
(join_type, table_name, column1, column2)
```
*   `join_type`: `INNER` یا `LEFT`
*   `table_name`: اسم جدول دوم
*   `column1`: ستون از جدول اول
*   `column2`: ستون از جدول دوم

**sort:**
```python
("column1",)                    # یک ستون، نزولی
("column1", "ASC")              # یک ستون، صعودی
("column1", "column2")          # دو ستون، نزولی
("column1", "column2", "ASC")   # دو ستون، صعودی
```

### delete_record

حذف رکورد.

| پارامتر | اجباری/اختیاری | نوع |
|---------|----------------|-----|
| `table_name` | اجباری | `str` |
| `condition` | اختیاری | `_Expression` |

```python
db.delete_record("users", condition=Field("age") < 18)
db.delete_record("users")  # حذف همه رکوردها
```

### edit_record

ویرایش رکورد.

| پارامتر | اجباری/اختیاری | نوع |
|---------|----------------|-----|
| `table_name` | اجباری | `str` |
| `new_info_record` | اجباری | `dict` |
| `condition` | اختیاری | `_Expression` |

```python
db.edit_record(
    "users",
    {"name": "Hassan", "age": 25},
    condition=Field("id") == 5
)
```

### count_record

شمارش رکوردها.

| پارامتر | اجباری/اختیاری | نوع |
|---------|----------------|-----|
| `table_name` | اجباری | `str` |

**خروجی:** `int`

```python
count = db.count_record("users")
print(count)
```

---

## Index

### add_index

ساخت ایندکس برای سرعت بیشتر جستجو.

| پارامتر | اجباری/اختیاری | نوع |
|---------|----------------|-----|
| `table_name` | اجباری | `str` |
| `column_name` | اجباری | `str` |
| `unique` | اختیاری | `bool` |

```python
db.add_index("users", "city")
db.add_index("users", "email", unique=True)
```

### delete_index

حذف ایندکس.

| پارامتر | اجباری/اختیاری | نوع |
|---------|----------------|-----|
| `table_name` | اجباری | `str` |
| `column_name` | اجباری | `str` |

```python
db.delete_index("users", "city")
```

---

## View

### add_view

ساخت ویو (جدول مجازی).

| پارامتر | اجباری/اختیاری | نوع |
|---------|----------------|-----|
| `view_name` | اجباری | `str` |
| `query` | اجباری | `str` |

```python
db.add_view("adults", "SELECT name, city FROM users WHERE age >= 18")
```

### delete_view

حذف ویو.

| پارامتر | اجباری/اختیاری | نوع |
|---------|----------------|-----|
| `view_name` | اجباری | `str` |

```python
db.delete_view("adults")
```

### exist_view

بررسی وجود ویو.

| پارامتر | اجباری/اختیاری | نوع |
|---------|----------------|-----|
| `view_name` | اجباری | `str` |

**خروجی:** `bool`

```python
if db.exist_view("adults"):
    print("ویو وجود دارد")
```

---

## انواع داده

| نام | توضیحات |
|-----|---------|
| `STR` | متن |
| `INT` | عدد صحیح |
| `FLOAT` | عدد اعشاری |
| `BOOL` | 0 یا 1 (False یا True) |
| `BLOB` | داده‌ی باینری (فایل، عکس، ...) |

---

## محدودیت‌ها

| نام | توضیحات |
|-----|---------|
| `UNIQUE` | مقدار تکراری مجاز نیست |
| `NOT_NULL` | مقدار خالی مجاز نیست |
| `PRIMARY_KEY` | کلید اصلی جدول |
| `AUTO_INCREMENT` | به صورت خودکار پر می‌شود |
| `DEFAULT(value)` | مقدار پیش‌فرض |
| `CHECK(condition)` | شرط برای مقدار |
| `FOREIGN_KEY(table, column)` | ارجاع به جدول دیگر |
| `DEFAULT_NOW()` | تاریخ و زمان فعلی |

---

## توابع تجمیعی

| نام | توضیحات |
|-----|---------|
| `COUNT(query)` | تعداد |
| `SUM(query)` | مجموع |
| `AVG(query)` | میانگین |
| `MIN(query)` | کمینه |
| `MAX(query)` | بیشینه |

```python
COUNT()
COUNT("id")
SUM("price")
AVG("age")
```

---

## Field

`Field` برای ساخت شرط‌های پیچیده استفاده می‌شود.

```python
from sqlthon import Field

Field("age") > 18
Field("name") == "Ali"
(Field("age") > 18) & (Field("city") == "Tehran")
(Field("age") > 18) | (Field("city") == "Tehran")
```

---

## Other

### run_code

اجرای کوئری خام SQL.

| پارامتر | اجباری/اختیاری | نوع |
|---------|----------------|-----|
| `code` | اجباری | `str` |
| `parameters` | اختیاری | `tuple` |

**خروجی:** `list`

```python
db.run_code("SELECT * FROM users WHERE age > ?", (18,))
```

### save_to_data_base

ذخیره‌ی تمام تغییرات جمع‌شده.

```python
db.add_table("users", ("id", INT), ("name", STR))
db.save_to_data_base()
```

### close

بستن اتصال به دیتابیس.

```python
db.close()
```

---

## مثال کامل

```python
from sqlthon import Connect, Field
from sqlthon.keywords import *

db = Connect("shop.db")

db.add_table(
    "users",
    ("id", INT, [PRIMARY_KEY, AUTO_INCREMENT]),
    ("name", STR, [NOT_NULL]),
    ("email", STR, [UNIQUE]),
    ("city", STR)
)

db.add_table(
    "orders",
    ("id", INT, [PRIMARY_KEY, AUTO_INCREMENT]),
    ("user_id", INT),
    ("price", FLOAT)
)

db.add_record("users", (1, "Ali", "ali@example.com", "Tehran"))
db.add_record("users", (2, "Sara", "sara@example.com", "Shiraz"))
db.add_record("orders", (1, 1, 100.0))
db.add_record("orders", (2, 1, 200.0))

db.save_to_data_base()

result = db.find_record(
    "users",
    columns=("users.name", "orders.price"),
    compound=("LEFT", "orders", "users.id", "orders.user_id")
)

print(result)

db.close()
```

---

**سازنده:** SAUMS
**ایمیل:** saums1391@gmail.com
