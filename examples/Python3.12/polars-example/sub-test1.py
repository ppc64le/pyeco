import polars as pl
import numpy as np

print("Sub-test 1: Basic DataFrame operations and filtering")

#create sample data
df = pl.DataFrame({
    "id": [1, 2, 3, 4, 5],
    "name": ["Alice", "Bob", "Charlie", "David", "Eve"],
    "score": [85, 92, 78, 88, 95],
    "grade": ["B", "A", "C", "B", "A"]
})

print("Original DataFrame:")
print(df)

#filter operations
high_scorers = df.filter(pl.col("score") > 85)
print("\nHigh scorers (score > 85):")
print(high_scorers)

#select and transform
result = df.select([
    pl.col("name"),
    pl.col("score"),
    (pl.col("score") * 1.1).alias("score_with_bonus")
])
print("\nScores with 10% bonus:")
print(result)

#aggregations
stats = df.select([
    pl.col("score").mean().alias("avg_score"),
    pl.col("score").max().alias("max_score"),
    pl.col("score").min().alias("min_score")
])
print("\nScore statistics:")
print(stats)

print("\nSub-test 1 completed successfully!")

