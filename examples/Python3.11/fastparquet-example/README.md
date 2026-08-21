## Purpose: Demonstrates reading and writing Apache Parquet columnar data files using the fastparquet library with Pandas integration.

### Packages used:
fastparquet
numpy
pandas

### Functionality:

- Creates a sample Pandas DataFrame representing sensor readings (timestamp, sensor ID, temperature, humidity, pressure, status).
- Writes the DataFrame to a Parquet file and reads it back, verifying round-trip integrity.
- Demonstrates column projection (reading only selected columns from the Parquet file).
- Compares file sizes across compression codecs: UNCOMPRESSED, SNAPPY, and GZIP.
- Inspects Parquet file metadata (row count and column names).

### How to run the example :
```
chmod +x install_test_example.sh
./install_test_example.sh
```

### License:
It's covered under Apache 2.0 licenses
