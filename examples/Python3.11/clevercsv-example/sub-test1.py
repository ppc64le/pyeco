import unittest
import importlib.metadata
import io
import os
import tempfile
import clevercsv


CSV_COMMA = "name,age,city\nAlice,30,NYC\nBob,25,LA\n"
CSV_SEMICOLON = "name;age;city\nAlice;30;NYC\nBob;25;LA\n"
CSV_TAB = "name\tage\tcity\nAlice\t30\tNYC\nBob\t25\tLA\n"


class TestCleverCsvLibrary(unittest.TestCase):

    def test_clevercsv_import(self):
        """Check that clevercsv can be imported."""
        try:
            import clevercsv  # noqa: F401
        except ImportError:
            self.fail("clevercsv is not installed")

    def test_clevercsv_version(self):
        """Verify clevercsv version."""
        version = importlib.metadata.version("clevercsv")
        assert "0.8.5" in version, f"'0.8.5' not found in version string: {version}"

    def test_detect_comma_delimiter(self):
        """Sniffer should detect comma as delimiter."""
        dialect = clevercsv.Sniffer().sniff(CSV_COMMA, verbose=False)
        self.assertIsNotNone(dialect)
        self.assertEqual(dialect.delimiter, ",")

    def test_detect_semicolon_delimiter(self):
        """Sniffer should detect semicolon as delimiter."""
        dialect = clevercsv.Sniffer().sniff(CSV_SEMICOLON, verbose=False)
        self.assertIsNotNone(dialect)
        self.assertEqual(dialect.delimiter, ";")

    def test_detect_tab_delimiter(self):
        """Sniffer should detect tab as delimiter."""
        dialect = clevercsv.Sniffer().sniff(CSV_TAB, verbose=False)
        self.assertIsNotNone(dialect)
        self.assertEqual(dialect.delimiter, "\t")

    def test_reader_row_count(self):
        """Reader should return all data rows (excluding header)."""
        dialect = clevercsv.Sniffer().sniff(CSV_COMMA, verbose=False)
        reader = clevercsv.reader(io.StringIO(CSV_COMMA), dialect)
        rows = list(reader)
        self.assertEqual(len(rows), 3)  # 1 header + 2 data rows

    def test_dict_reader_fields(self):
        """DictReader should expose correct field names from the header."""
        dialect = clevercsv.Sniffer().sniff(CSV_COMMA, verbose=False)
        reader = clevercsv.DictReader(io.StringIO(CSV_COMMA), dialect=dialect)
        rows = list(reader)
        self.assertEqual(reader.fieldnames, ["name", "age", "city"])
        self.assertEqual(len(rows), 2)

    def test_dict_reader_values(self):
        """DictReader rows should contain correct values."""
        dialect = clevercsv.Sniffer().sniff(CSV_COMMA, verbose=False)
        reader = clevercsv.DictReader(io.StringIO(CSV_COMMA), dialect=dialect)
        rows = list(reader)
        self.assertEqual(rows[0]["name"], "Alice")
        self.assertEqual(rows[0]["age"], "30")

    def test_read_csv_file(self):
        """reader should successfully parse a file with auto-detected dialect."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv",
                                         delete=False, encoding="utf-8") as f:
            f.write(CSV_SEMICOLON)
            tmp_path = f.name
        try:
            with open(tmp_path, newline="", encoding="utf-8") as f:
                file_text = f.read()
            dialect = clevercsv.Sniffer().sniff(file_text, verbose=False)
            with open(tmp_path, newline="", encoding="utf-8") as f:
                rows = list(clevercsv.reader(f, dialect))
            self.assertGreater(len(rows), 0)
            self.assertEqual(rows[0], ["name", "age", "city"])
        finally:
            os.unlink(tmp_path)


if __name__ == "__main__":
    unittest.main()
