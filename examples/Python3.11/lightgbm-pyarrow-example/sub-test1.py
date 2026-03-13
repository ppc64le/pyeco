import pyarrow as pa
import pyarrow.parquet as pq
import pyarrow.dataset as ds
import pandas as pd
import numpy as np
import shutil
import os
import io


def test_nested_structs_and_lists():
    print("\n--- Test 1: Nested Structs, Lists, and Null Handling ---")

    # Define a schema with nested struct and list fields
    schema = pa.schema([
        ('user_id', pa.int64()),
        ('profile', pa.struct([
            ('name', pa.string()),
            ('emails', pa.list_(pa.string())),
            ('is_active', pa.bool_())
        ]))
    ])

    # Data with one null profile
    data = [
        (1, {"name": "Alice", "emails": ["alice@example.com"], "is_active": True}),
        (2, {"name": "Bob", "emails": [], "is_active": False}),
        (3, None)
    ]

    user_ids = [row[0] for row in data]
    profiles = pa.array([row[1] for row in data], type=schema.field("profile").type)

    table = pa.table([user_ids, profiles], schema=schema)

    print("Schema:")
    print(table.schema)

    print("\nTable content:")
    print(table.to_pandas())

    assert table.num_rows == 3
    assert table.column("profile")[2].as_py() is None
    print("Test passed: Nested struct with nulls handled correctly.")


def test_chunked_arrays():
    print("\n--- Test 2: Chunked Arrays and Table Concatenation ---")

    # Create and concatenate two Arrow tables
    t1 = pa.table({"a": [1, 2], "b": ["x", "y"]})
    t2 = pa.table({"a": [3, 4], "b": ["z", "w"]})
    combined = pa.concat_tables([t1, t2])

    print("Combined Table:")
    print(combined.to_pandas())

    assert combined.num_rows == 4
    assert combined["a"].to_pylist() == [1, 2, 3, 4]
    print("Test passed: Chunked arrays concatenated successfully.")


def test_partitioned_parquet_read_filter():
    print("\n--- Test 3: Partitioned Parquet Write and Filtered Read ---")

    dataset_path = "test_dataset"
    if os.path.exists(dataset_path):
        shutil.rmtree(dataset_path)

    # Create a table with a partition column
    table = pa.table({
        "name": ["Alice", "Bob", "Charlie", "Diana"],
        "age": [25, 32, 37, 29],
        "country": ["US", "UK", "US", "UK"]
    })

    # Write partitioned dataset
    pq.write_to_dataset(table, root_path=dataset_path, partition_cols=["country"])
    print(f"Partitioned data written to: {dataset_path}/")

    # Read dataset with hive-style partition detection
    dataset = ds.dataset(dataset_path, format="parquet", partitioning="hive")
    filtered = dataset.to_table(filter=(ds.field("country") == "US"))

    print("\nFiltered result (country == 'US'):")
    print(filtered.to_pandas())

    df = filtered.to_pandas()
    assert set(df["name"]) == {"Alice", "Charlie"}

    shutil.rmtree(dataset_path)
    print("Test passed: Partitioned Parquet write/read and filter working as expected.")


def test_pandas_interop():
    print("\n--- Test 4: Pandas ↔ PyArrow Round-trip ---")

    df = pd.DataFrame({
        "col1": np.random.rand(5),
        "col2": pd.date_range("2023-01-01", periods=5),
        "col3": pd.Categorical(["a", "b", "a", "c", "b"])
    })

    print("Original DataFrame:")
    print(df)

    table = pa.Table.from_pandas(df)
    df_back = table.to_pandas()

    print("\nRound-tripped DataFrame:")
    print(df_back)

    pd.testing.assert_frame_equal(df.reset_index(drop=True), df_back.reset_index(drop=True))
    print("Test passed: Pandas and Arrow round-trip is consistent.")


def test_in_memory_parquet():
    print("\n--- Test 5: In-Memory Parquet I/O ---")

    df = pd.DataFrame({
        "id": [1, 2, 3],
        "value": ["A", "B", "C"]
    })

    print("Original DataFrame:")
    print(df)

    table = pa.Table.from_pandas(df)

    sink = pa.BufferOutputStream()
    pq.write_table(table, sink)

    buf = sink.getvalue()
    reader = pa.BufferReader(buf)
    table_from_buf = pq.read_table(reader)

    df_back = table_from_buf.to_pandas()

    print("\nDataFrame read from memory:")
    print(df_back)

    pd.testing.assert_frame_equal(df, df_back)
    print("Test passed: In-memory Parquet write/read successful.")


if __name__ == "__main__":
    print("Starting PyArrow functionality tests...")

    try:
        test_nested_structs_and_lists()
        test_chunked_arrays()
        test_partitioned_parquet_read_filter()
        test_pandas_interop()
        test_in_memory_parquet()
        print("\nAll tests passed successfully.")

    except AssertionError as e:
        print("\nTest failed with an assertion error:")
        print(str(e))
    except Exception as ex:
        print("\nTest failed with an unexpected error:")
        print(str(ex))
