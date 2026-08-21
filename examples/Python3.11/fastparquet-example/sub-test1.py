import unittest
import importlib.metadata
import os
import tempfile
import numpy as np
import pandas as pd
import fastparquet


class TestFastparquetLibrary(unittest.TestCase):

    def setUp(self):
        """Create a small DataFrame and a temp directory for file tests."""
        self.tmpdir = tempfile.TemporaryDirectory()
        self.df = pd.DataFrame({
            "id": range(10),
            "value": np.arange(10, dtype=np.float64),
            "label": [f"item_{i}" for i in range(10)],
        })

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_fastparquet_import(self):
        """Check that fastparquet can be imported."""
        try:
            import fastparquet  # noqa: F401
        except ImportError:
            self.fail("fastparquet is not installed")

    def test_fastparquet_version(self):
        """Verify fastparquet version."""
        version = importlib.metadata.version("fastparquet")
        assert "2024.11.0" in version, f"'2024.11.0' not found in version string: {version}"

    def test_write_creates_file(self):
        """Writing a DataFrame should create a Parquet file on disk."""
        path = os.path.join(self.tmpdir.name, "test.parquet")
        fastparquet.write(path, self.df)
        self.assertTrue(os.path.exists(path))
        self.assertGreater(os.path.getsize(path), 0)

    def test_read_roundtrip_row_count(self):
        """Row count should be preserved after write/read round-trip."""
        path = os.path.join(self.tmpdir.name, "roundtrip.parquet")
        fastparquet.write(path, self.df)
        pf = fastparquet.ParquetFile(path)
        df_read = pf.to_pandas()
        self.assertEqual(len(df_read), len(self.df))

    def test_read_roundtrip_columns(self):
        """Column names should be preserved after write/read round-trip."""
        path = os.path.join(self.tmpdir.name, "cols.parquet")
        fastparquet.write(path, self.df)
        pf = fastparquet.ParquetFile(path)
        df_read = pf.to_pandas()
        self.assertEqual(sorted(df_read.columns.tolist()), sorted(self.df.columns.tolist()))

    def test_column_projection(self):
        """Reading a subset of columns should return only those columns."""
        path = os.path.join(self.tmpdir.name, "proj.parquet")
        fastparquet.write(path, self.df)
        pf = fastparquet.ParquetFile(path)
        df_proj = pf.to_pandas(columns=["id", "value"])
        self.assertEqual(df_proj.columns.tolist(), ["id", "value"])

    def test_snappy_compression(self):
        """Snappy-compressed Parquet should round-trip correctly."""
        path = os.path.join(self.tmpdir.name, "snappy.parquet")
        fastparquet.write(path, self.df, compression="SNAPPY")
        pf = fastparquet.ParquetFile(path)
        df_read = pf.to_pandas()
        self.assertEqual(len(df_read), len(self.df))

    def test_parquetfile_count(self):
        """ParquetFile.count() should return the correct number of rows."""
        path = os.path.join(self.tmpdir.name, "count.parquet")
        fastparquet.write(path, self.df)
        pf = fastparquet.ParquetFile(path)
        self.assertEqual(pf.count(), len(self.df))


if __name__ == "__main__":
    unittest.main()
