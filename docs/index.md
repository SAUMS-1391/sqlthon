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
db.save_to_database()

result = db.find_record("users", condition=Field("id") == 1)
print(result)

db.close()
```

---

## Connect

کلاس اصلی برای اتصال به دیتابیس است. تمام عملیات دیتابیس از طریق این کلاس انجام می‌شود.

| پارامتر | اجباری/اختیاری | نوع | توضیحات |
|---------|----------------|-----|---------|
| `database_path` | **اجباری** | `str` | مسیر فایل دیتابیس. اگر فایل وجود نداشته باشد، ساخته می‌شود. |

```python
db = Connect("test.db")
```

**نکته:** برای دیتابیس در حافظه (موقت) می‌توانید از `Connect(":memory:")` استفاده کنید.

---

## Table

### add_table

ساخت جدول جدید با ستون‌های مشخص.

| پارامتر | اجباری/اختیاری | نوع | توضیحات |
|---------|----------------|-----|---------|
| `table_name` | **اجباری** | `str` | نام جدول |
| `*columns` | **اجباری** | `tuple` | مشخصات ستون‌ها به صورت تاپل |
| `if_not_exists` | **اختیاری=`False`** | `bool` | اگر `True` باشد و جدول وجود داشته باشد، ارور نمی‌دهد. |

**ساختار هر ستون:**
```python
(column_name, column_type, [limits])
```

| عضو | اجباری/اختیاری | نوع | توضیحات |
|-----|----------------|-----|---------|
| `column_name` | **اجباری** | `str` | نام ستون |
| `column_type` | **اجباری** | `str` | نوع داده (مثل `STR`, `INT`, ...) |
| `limits` | **اختیاری=`[]`** | `list` | لیست محدودیت‌ها (مثل `UNIQUE`, `NOT_NULL`, ...) |

```python
db.add_table(
    "users",
    ("id", INT, [PRIMARY_KEY, AUTO_INCREMENT]),
    ("name", STR, [NOT_NULL]),
    ("email", STR, [UNIQUE])
)

db.add_table("logs", ("message", STR), if_not_exists=True)
```

---

### rename_table

تغییر نام جدول.

| پارامتر | اجباری/اختیاری | نوع | توضیحات |
|---------|----------------|-----|---------|
| `old_name_table` | **اجباری** | `str` | نام فعلی جدول |
| `new_name_table` | **اجباری** | `str` | نام جدید جدول |

```python
db.rename_table("users", "members")
```

---

### drop_table

حذف کامل جدول (ساختار و داده‌ها).

| پارامتر | اجباری/اختیاری | نوع | توضیحات |
|---------|----------------|-----|---------|
| `table_name` | **اجباری** | `str` | نام جدول |

```python
db.drop_table("users")
```

---

### exist_table

بررسی وجود جدول.

| پارامتر | اجباری/اختیاری | نوع | توضیحات |
|---------|----------------|-----|---------|
| `table_name` | **اجباری** | `str` | نام جدول |

**خروجی:** `bool` (True اگر وجود داشته باشد)

```python
if db.exist_table("users"):
    print("جدول وجود دارد")
```

---

### copy_table

کپی جدول (ساختار و داده‌ها).

| پارامتر | اجباری/اختیاری | نوع | توضیحات |
|---------|----------------|-----|---------|
| `table_name` | **اجباری** | `str` | نام جدول مبدأ |
| `new_name_table` | **اجباری** | `str` | نام جدول مقصد |

```python
db.copy_table("users", "users_backup")
```

---

### get_tables

دریافت لیست تمام جدول‌های دیتابیس.

**خروجی:** `list`

```python
tables = db.get_tables()
print(tables)  # ['users', 'orders', 'logs']
```

---

## Column

### add_column

اضافه کردن ستون جدید به جدول موجود.

| پارامتر | اجباری/اختیاری | نوع | توضیحات |
|---------|----------------|-----|---------|
| `table_name` | **اجباری** | `str` | نام جدول |
| `column_name` | **اجباری** | `str` | نام ستون جدید |
| `column_type` | **اجباری** | `str` | نوع داده |
| `limits` | **اختیاری=`[]`** | `list` | محدودیت‌ها |

```python
db.add_column("users", "email", STR, [UNIQUE])
```

---

### drop_column

حذف ستون از جدول.

| پارامتر | اجباری/اختیاری | نوع | توضیحات |
|---------|----------------|-----|---------|
| `table_name` | **اجباری** | `str` | نام جدول |
| `column_name` | **اجباری** | `str` | نام ستون |

```python
db.drop_column("users", "tel")
```

---

### rename_column

تغییر نام ستون.

| پارامتر | اجباری/اختیاری | نوع | توضیحات |
|---------|----------------|-----|---------|
| `table_name` | **اجباری** | `str` | نام جدول |
| `old_name_column` | **اجباری** | `str` | نام فعلی ستون |
| `new_name_column` | **اجباری** | `str` | نام جدید ستون |

```python
db.rename_column("users", "name", "full_name")
```

---

### exist_column

بررسی وجود ستون.

| پارامتر | اجباری/اختیاری | نوع | توضیحات |
|---------|----------------|-----|---------|
| `table_name` | **اجباری** | `str` | نام جدول |
| `column_name` | **اجباری** | `str` | نام ستون |

**خروجی:** `bool`

```python
if db.exist_column("users", "email"):
    print("ستون وجود دارد")
```

---

### get_columns

دریافت لیست ستون‌های جدول.

| پارامتر | اجباری/اختیاری | نوع | توضیحات |
|---------|----------------|-----|---------|
| `table_name` | **اجباری** | `str` | نام جدول |

**خروجی:** `list`

```python
columns = db.get_columns("users")
print(columns)  # ['id', 'name', 'email']
```

---

## Record

### add_record

اضافه کردن یک رکورد جدید.

| پارامتر | اجباری/اختیاری | نوع | توضیحات |
|---------|----------------|-----|---------|
| `table_name` | **اجباری** | `str` | نام جدول |
| `record_info` | **اجباری** | `tuple` | مقادیر رکورد به ترتیب ستون‌ها |

```python
db.add_record("users", (1, "Ali", "ali@example.com"))
```

---

### add_records

اضافه کردن چند رکورد به صورت همزمان (۱۰۰ برابر سریع‌تر از حلقه).

| پارامتر | اجباری/اختیاری | نوع | توضیحات |
|---------|----------------|-----|---------|
| `table_name` | **اجباری** | `str` | نام جدول |
| `info_records` | **اجباری** | `tuple` | لیست تاپل‌های رکورد |

```python
db.add_records("users", [
    (1, "Ali", "ali@example.com"),
    (2, "Sara", "sara@example.com"),
    (3, "Reza", "reza@example.com"),
])
```

**نکته:** این متد خودبه‌خود اجرا می‌شود و با صدا زدن متد `save_to_database()` ذخیره نمی‌شود چون از قبل شده است

---

### find_record

جستجوی رکوردها. این **قدرتمندترین متد پکیج** است.

| پارامتر | اجباری/اختیاری | نوع | توضیحات |
|---------|----------------|-----|---------|
| `table_name` | **اجباری** | `str` | نام جدول |
| `columns` | **اختیاری=`None`** | `tuple` | ستون‌های مورد نظر |
| `compound` | **اختیاری=`None`** | `tuple` | اتصال به جدول دیگر (JOIN) |
| `condition` | **اختیاری=`None`** | `_Expression` | شرط فیلتر (WHERE) |
| `bundle` | **اختیاری=`None`** | `tuple` | گروه‌بندی (GROUP BY) |
| `filter_bundle` | **اختیاری=`None`** | `_Expression` | شرط گروه (HAVING) |
| `sort` | **اختیاری=`None`** | `tuple` | مرتب‌سازی (ORDER BY) |
| `several` | **اختیاری=`None`** | `int` | تعداد رکورد (LIMIT) |
| `jump` | **اختیاری=`0`** | `int` | پرش (OFFSET) |
| `unique` | **اختیاری=`False`** | `bool` | حذف تکراری (DISTINCT) |

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

# با اتصال (JOIN)
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

---

### delete_record

حذف رکوردها.

| پارامتر | اجباری/اختیاری | نوع | توضیحات |
|---------|----------------|-----|---------|
| `table_name` | **اجباری** | `str` | نام جدول |
| `condition` | **اجباری** | `_Expression` | شرط حذف |

```python
db.delete_record("users", condition=Field("age") < 18)
db.delete_record("users")  # حذف همه رکوردها
```

---

### delete_all_record

پاک کردن تمامی رکورد های یک جدول.

پارامتر | اجباری/اختیاری | نوع | توضیحات |
|------|-----|--------|------|
| `table_name` | **اجباری** | `str` | نام جدول

**خروجی:** `None`

```python
db.delete_all_record("users")
```

---

### edit_record

ویرایش رکوردها.

| پارامتر | اجباری/اختیاری | نوع | توضیحات |
|---------|----------------|-----|---------|
| `table_name` | **اجباری** | `str` | نام جدول |
| `new_info_record` | **اجباری** | `dict` | مقادیر جدید |
| `condition` | **اختیاری=`None`** | `_Expression` | شرط ویرایش |

**خروجی:** `None`

```python
db.edit_record(
    "users",
    {"name": "Hassan", "age": 25},
    condition=Field("id") == 5
)
```

---

### count_record

شمارش رکوردهای جدول.

| پارامتر | اجباری/اختیاری | نوع | توضیحات |
|---------|----------------|-----|---------|
| `table_name` | **اجباری** | `str` | نام جدول |

**خروجی:** `int`

```python
count = db.count_record("users")
print(count)
```

---

### upsert_record

ترکیبی از **Insert** و **Update** است. اگر رکورد وجود داشته باشد، آن را آپدیت می‌کند و اگر وجود نداشته باشد، رکورد جدید اضافه می‌کند.

| پارامتر | اجباری/اختیاری | نوع | توضیحات |
|---------|----------------|-----|---------|
| `table_name` | **اجباری** | `str` | نام جدول |
| `info_record` | **اجباری** | `tuple` | اطلاعات رکورد |
| `conflict` | **اجباری** | `tuple` | نام ستون هایی که کلید تداخل هستند |

**خروجی:** `None`

```python
count = db.count_record("users")
print(count)
```

---

## Index

### add_index

ساخت ایندکس برای سرعت بیشتر جستجو.

| پارامتر | اجباری/اختیاری | نوع | توضیحات |
|---------|----------------|-----|---------|
| `table_name` | **اجباری** | `str` | نام جدول |
| `column_name` | **اجباری** | `str` | نام ستون |
| `unique` | **اختیاری=`False`** | `bool` | ایندکس یکتا |

```python
db.add_index("users", "city")
db.add_index("users", "email", unique=True)
```

---

### delete_index

حذف ایندکس.

| پارامتر | اجباری/اختیاری | نوع | توضیحات |
|---------|----------------|-----|---------|
| `table_name` | **اجباری** | `str` | نام جدول |
| `column_name` | **اجباری** | `str` | نام ستون |

```python
db.delete_index("users", "city")
```

---

## View

### add_view

ساخت ویو (جدول مجازی).

| پارامتر | اجباری/اختیاری | نوع | توضیحات |
|---------|----------------|-----|---------|
| `view_name` | **اجباری** | `str` | نام ویو |
| `query` | **اجباری** | `str` | کوئری SELECT |

```python
db.add_view("adults", "SELECT name, city FROM users WHERE age >= 18")
```

---

### delete_view

حذف ویو.

| پارامتر | اجباری/اختیاری | نوع | توضیحات |
|---------|----------------|-----|---------|
| `view_name` | **اجباری** | `str` | نام ویو |

```python
db.delete_view("adults")
```

---

### exist_view

بررسی وجود ویو.

| پارامتر | اجباری/اختیاری | نوع | توضیحات |
|---------|----------------|-----|---------|
| `view_name` | **اجباری** | `str` | نام ویو |

**خروجی:** `bool`

```python
if db.exist_view("adults"):
    print("ویو وجود دارد")
```

---

## Backup

### backup_database

پشتیبان‌گیری از کل دیتابیس.

| پارامتر | اجباری/اختیاری | نوع | توضیحات |
|---------|----------------|-----|---------|
| `backup_path` | **اجباری** | `str` | مسیر فایل پشتیبان |

```python
db.backup_database("backup.db")
```

---

## Pandas

### to_dataframe

تبدیل جدول به DataFrame پانداس (برای تحلیل داده).

| پارامتر | اجباری/اختیاری | نوع | توضیحات |
|---------|----------------|-----|---------|
| `table_name` | **اجباری** | `str` | نام جدول |

**خروجی:** `pd.DataFrame`

```python
df = db.to_dataframe("users")
print(df)
print(df.mean())  # میانگین
df.plot()         # نمودار
```

---

## Csv

### load_csv

آوردن یک فایل `.csv` در دیتابیس.

| پارامتر | اجباری/اختیاری | نوع | توضیحات |
|---------|----------------|-----|---------|
| `table_name` | **اجباری** | `str` | نام جدول |
| `csv_path` | **اجباری** | `str` | مسیر فایل |

```python
db.load_csv("csv_table", "example.csv")
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

`Field` برای ساخت شرط‌های پیچیده استفاده می‌شود. با عملگرهای پایتون (`>`, `<`, `==`, `&`, `|`) کار می‌کند.

```python
from sqlthon import Field

Field("age") > 18
Field("name") == "Ali"
(Field("age") > 18) & (Field("city") == "Tehran")
(Field("age") > 18) | (Field("city") == "Tehran")
```

---

## Other

### last_id

شناسه‌ی آخرین رکوردی که به جدول اضافه شده رو برمی‌گردونه. این متد مخصوص ستون‌هایی هست که `AUTO_INCREMENT` دارن و بعد از `add_record` استفاده می‌شه.

```python
db.add_record("users", ("Ali", 25))
db.save_to_database()

user_id = db.last_id()
print(user_id) # -> 1
```

---

### database_info

اطلاعات لازم از دیتابیس.

```python
db.database_info() # -> dict
```

## Basic

### run_query

اجرای کوئری خام SQL.

| پارامتر | اجباری/اختیاری | نوع | توضیحات |
|---------|----------------|-----|---------|
| `code` | **اجباری** | `str` | کوئری SQL |
| `parameters` | **اختیاری=`()`** | `tuple` | پارامترهای کوئری |

**خروجی:** `list`

```python
db.run_query("SELECT * FROM users WHERE age > ?", (18,))
db.run_query("CREATE VIEW adults AS SELECT * FROM users WHERE age >= 18")
```

---

### optimize

بهینه‌تر کردن حجم و سرعت دیتابیس.

**خروجی:** `None`

```python
db.optimize()
```

**نکته:** این تابع کمی زمان می‌برد و اینکه خودش قبل از بهینه کردن تغییرات را ذخیره می‌کند که در واقع یعنی save_to_database() می‌زند.
---

### save_to_database

ذخیره‌ی تمام تغییرات جمع‌شده در `_changes`.

```python
db.add_table("users", ("id", INT), ("name", STR))
db.add_record("users", (1, "Ali"))
db.save_to_database()
```

---

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

db.save_to_database()

result = db.find_record(
    "users",
    columns=("users.name", "orders.price"),
    compound=("LEFT", "orders", "users.id", "orders.user_id")
)

print(result)

db.close()
```

---

**آخرین به‌روزرسانی:** نسخه 0.0.11
**سازنده:** SAUMS
**ایمیل:** saums1391@gmail.com
