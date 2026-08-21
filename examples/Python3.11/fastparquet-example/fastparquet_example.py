import os
import tempfile
import numpy as np
import pandas as pd
import fastparquet


def create_sample_dataframe():
    """Create a sample Pandas DataFrame representing sensor readings."""
    rng = np.random.default_rng(42)
    n = 500
    df = pd.DataFrame({
        "timestamp": pd.date_range("2024-01-01", periods=n, freq="1min"),
        "sensor_id": rng.integers(1, 6, size=n),
        "temperature": rng.uniform(15.0, 35.0, size=n).round(2),
        "humidity": rng.uniform(30.0, 90.0, size=n).round(2),
        "pressure": rng.uniform(990.0, 1030.0, size=n).round(1),
        "status": rng.choice(["OK", "WARN", "ERROR"], size=n, p=[0.85, 0.10, 0.05]),
    })
    return df


def demo_write_read(df, path):
    """Write a DataFrame to Parquet and read it back, verifying round-trip integrity."""
    print(f"Writing {len(df)} rows to: {path}")
    fastparquet.write(path, df)

    pf = fastparquet.ParquetFile(path)
    df_read = pf.to_pandas()

    print(f"Read back {len(df_read)} rows, {len(df_read.columns)} columns.")
    print(f"Columns: {df_read.columns.tolist()}")
    assert len(df_read) == len(df), "Row count mismatch after round-trip"
    assert list(df_read.columns) == list(df.columns), "Column mismatch after round-trip"
    return df_read


def demo_column_selection(path):
    """Read only selected columns from a Parquet file (projection pushdown)."""
    pf = fastparquet.ParquetFile(path)
    df_subset = pf.to_pandas(columns=["timestamp", "sensor_id", "temperature"])
    print(f"\nProjection pushdown — selected columns: {df_subset.columns.tolist()}")
    print(df_subset.head(3).to_string(index=False))
    return df_subset


def demo_compression(df, tmpdir):
    """Write the same data with different compression codecs and compare file sizes."""
    codecs = ["UNCOMPRESSED", "SNAPPY", "GZIP"]
    sizes = {}
    for codec in codecs:
        fpath = os.path.join(tmpdir, f"sensor_{codec.lower()}.parquet")
        fastparquet.write(fpath, df, compression=codec)
        sizes[codec] = os.path.getsize(fpath)

    print("\nFile sizes by compression codec:")
    for codec, size in sizes.items():
        print(f"  {codec:14s}: {size:>8,} bytes")


def demo_metadata(path):
    """Inspect Parquet file metadata."""
    pf = fastparquet.ParquetFile(path)
    print(f"\nParquet metadata:")
    print(f"  Rows:     {pf.count()}")
    print(f"  Columns:  {len(pf.columns)}")
    print(f"  Schema:   {[str(c) for c in pf.schema.column(i).name for i in range(len(pf.columns))]}"
          if False else f"  Schema fields: {pf.columns}")


if __name__ == "__main__":
    print("=== fastparquet Example: Columnar Parquet I/O with Pandas ===\n")

    df = create_sample_dataframe()
    print(f"Sample DataFrame shape: {df.shape}")
    print(df.head(3).to_string(index=False))

    with tempfile.TemporaryDirectory() as tmpdir:
        parquet_path = os.path.join(tmpdir, "sensor_data.parquet")

        print("\n--- 1. Write & Read Round-trip ---")
        df_read = demo_write_read(df, parquet_path)

        print("\n--- 2. Column Projection ---")
        demo_column_selection(parquet_path)

        print("\n--- 3. Compression Comparison ---")
        demo_compression(df, tmpdir)

        print("\n--- 4. File Metadata ---")
        pf = fastparquet.ParquetFile(parquet_path)
        print(f"  Rows:    {pf.count()}")
        print(f"  Columns: {pf.columns}")

    print("\nfastparquet example completed successfully.")
