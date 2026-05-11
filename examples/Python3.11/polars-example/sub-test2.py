import polars as pl
from datetime import datetime, timedelta

print("Sub-test 2: Date/Time operations and string manipulation")

#create dataframe with dates
dates = [datetime(2024, 1, 1) + timedelta(days=i*7) for i in range(10)]
df = pl.DataFrame({
    "date": dates,
    "product": ["Product_A", "Product_B", "Product_C", "Product_A", "Product_B",
                "Product_C", "Product_A", "Product_B", "Product_C", "Product_A"],
    "sales": [100, 150, 120, 180, 160, 140, 200, 170, 190, 210]
})

print("Original DataFrame:")
print(df)

#date operations
df_with_date_parts = df.with_columns([
    pl.col("date").dt.year().alias("year"),
    pl.col("date").dt.month().alias("month"),
    pl.col("date").dt.day().alias("day"),
    pl.col("date").dt.weekday().alias("weekday")
])
print("\nDataFrame with date parts:")
print(df_with_date_parts)

#string operations
df_strings = df.with_columns([
    pl.col("product").str.to_lowercase().alias("product_lower"),
    pl.col("product").str.replace("_", "-").alias("product_dash"),
    pl.col("product").str.len_chars().alias("product_length")
])
print("\nString operations:")
print(df_strings.select(["product", "product_lower", "product_dash", "product_length"]))

#group by and aggregate
grouped = df.group_by("product").agg([
    pl.col("sales").sum().alias("total_sales"),
    pl.col("sales").mean().alias("avg_sales"),
    pl.col("date").count().alias("num_transactions")
])
print("\nGrouped by product:")
print(grouped)

print("\nSub-test 2 completed successfully!")
