import polars as pl
import numpy as np
from datetime import datetime, timedelta

print(" Starting Polars comprehensive example...\n")

# --- 1. Create DataFrames from various sources ---
print("1. Creating DataFrames...")

#from dictionary
df_dict = pl.DataFrame({
    "name": ["Alice", "Bob", "Charlie", "David", "Eve"],
    "age": [25, 30, 35, 28, 32],
    "city": ["New York", "London", "Paris", "Tokyo", "Berlin"],
    "salary": [70000, 85000, 92000, 78000, 88000]
})
print("DataFrame from dict:\n", df_dict)

#from numpy arrays
np_data = np.random.rand(5, 3)
df_numpy = pl.DataFrame(np_data, schema=["col1", "col2", "col3"])
print("\nDataFrame from numpy:\n", df_numpy.head())

# --- 2. Basic operations ---
print("\n2. Basic operations...")

#select columns
selected = df_dict.select(["name", "age"])
print("Selected columns:\n", selected)

#filter rows
filtered = df_dict.filter(pl.col("age") > 28)
print("\nFiltered (age > 28):\n", filtered)

#sort
sorted_df = df_dict.sort("salary", descending=True)
print("\nSorted by salary:\n", sorted_df)

# --- 3. Expressions and transformations ---
print("\n3. Expressions and transformations...")

#add new columns with expressions
df_transformed = df_dict.with_columns([
    (pl.col("salary") * 1.1).alias("salary_with_bonus"),
    pl.col("name").str.to_uppercase().alias("name_upper"),
    (pl.col("age") / 10).alias("age_decade")
])
print("Transformed DataFrame:\n", df_transformed)

# --- 4. Aggregations ---
print("\n4. Aggregations...")

#group by and aggregate
df_with_dept = df_dict.with_columns(
    pl.Series("department", ["IT", "HR", "IT", "HR", "IT"])
)

grouped = df_with_dept.group_by("department").agg([
    pl.col("salary").mean().alias("avg_salary"),
    pl.col("age").max().alias("max_age"),
    pl.col("name").count().alias("employee_count")
])
print("Grouped by department:\n", grouped)

# --- 5. Date/Time operations ---
print("\n5. Date/Time operations...")

dates = [datetime(2024, 1, 1) + timedelta(days=i*30) for i in range(5)]
df_dates = pl.DataFrame({
    "date": dates,
    "value": [100, 150, 120, 180, 160]
})

df_dates = df_dates.with_columns([
    pl.col("date").dt.year().alias("year"),
    pl.col("date").dt.month().alias("month"),
    pl.col("date").dt.day().alias("day")
])
print("Date operations:\n", df_dates)

# --- 6. String operations ---
print("\n6. String operations...")

df_strings = pl.DataFrame({
    "text": ["hello world", "POLARS rocks", "Data Science", "python 3.12", "Machine Learning"]
})

df_strings = df_strings.with_columns([
    pl.col("text").str.to_lowercase().alias("lowercase"),
    pl.col("text").str.len_chars().alias("length"),
    pl.col("text").str.contains("a").alias("contains_a")
])
print("String operations:\n", df_strings)

# --- 7. Joins ---
print("\n7. Joins...")

df_left = pl.DataFrame({
    "id": [1, 2, 3, 4],
    "name": ["Alice", "Bob", "Charlie", "David"]
})

df_right = pl.DataFrame({
    "id": [2, 3, 4, 5],
    "score": [85, 92, 78, 88]
})

joined = df_left.join(df_right, on="id", how="inner")
print("Inner join:\n", joined)

# --- 8. Lazy evaluation ---
print("\n8. Lazy evaluation...")

lazy_df = df_dict.lazy()
result = (
    lazy_df
    .filter(pl.col("age") > 25)
    .select(["name", "salary"])
    .sort("salary", descending=True)
    .collect()
)
print("Lazy evaluation result:\n", result)

# --- 9. Window functions ---
print("\n9. Window functions...")

df_window = df_with_dept.with_columns([
    pl.col("salary").rank().over("department").alias("salary_rank"),
    pl.col("salary").mean().over("department").alias("dept_avg_salary")
])
print("Window functions:\n", df_window)

# --- 10. Null handling ---
print("\n10. Null handling...")

df_nulls = pl.DataFrame({
    "a": [1, 2, None, 4, 5],
    "b": [None, 2, 3, None, 5]
})

df_filled = df_nulls.fill_null(0)
print("Filled nulls:\n", df_filled)

df_dropped = df_nulls.drop_nulls()
print("\nDropped nulls:\n", df_dropped)

# --- 11. Pivot operations ---
print("\n11. Pivot operations...")

df_pivot = pl.DataFrame({
    "product": ["A", "B", "A", "B", "A", "B"],
    "quarter": ["Q1", "Q1", "Q2", "Q2", "Q3", "Q3"],
    "sales": [100, 150, 120, 180, 140, 200]
})

pivoted = df_pivot.pivot(
    values="sales",
    index="product",
    columns="quarter"
)
print("Pivoted DataFrame:\n", pivoted)

# --- 12. Statistical operations ---
print("\n12. Statistical operations...")

stats = df_dict.select([
    pl.col("age").mean().alias("mean_age"),
    pl.col("age").std().alias("std_age"),
    pl.col("salary").median().alias("median_salary"),
    pl.col("salary").quantile(0.75).alias("salary_75th_percentile")
])
print("Statistics:\n", stats)

# --- 13. CSV I/O ---
print("\n13. CSV I/O...")

#write to CSV
df_dict.write_csv("test_output.csv")
print("Written to CSV: test_output.csv")

#read from CSV
df_read = pl.read_csv("test_output.csv")
print("Read from CSV:\n", df_read)

#cleanup
import os
os.remove("test_output.csv")

print("\nPolars comprehensive example completed successfully!")

