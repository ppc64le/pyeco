import io
import tempfile
import os
import clevercsv


# ---------------------------------------------------------------------------
# Sample CSV data with intentionally tricky formatting
# ---------------------------------------------------------------------------

# Standard comma-separated with a header
CSV_STANDARD = """\
name,age,city,score
Alice,30,New York,88.5
Bob,25,Los Angeles,91.0
Charlie,35,Chicago,76.3
Diana,28,Houston,95.1
"""

# Semicolon-separated (common in European exports)
CSV_SEMICOLON = """\
name;department;salary;start_date
Eve;Engineering;85000;2021-03-15
Frank;Marketing;72000;2020-07-01
Grace;Engineering;91000;2019-11-20
Heidi;HR;65000;2022-01-10
"""

# Tab-separated with quoted fields that contain commas
CSV_TAB = "product\tprice\tdescription\n" \
          'Laptop\t999.99\t"High performance, slim design"\n' \
          'Phone\t499.99\t"Dual SIM, 5G ready"\n' \
          'Tablet\t349.99\t"Lightweight, long battery"\n'

# Messy CSV: mixed quoting, extra whitespace
CSV_MESSY = """\
"id", "value" , "label"
1 , 42.0 , "alpha"
2 , 17.5 , "beta"
3 , 99.9 , "gamma"
"""


def detect_and_read(csv_text, label):
    """Use clevercsv to detect the dialect and read rows from a CSV string."""
    print(f"\n--- {label} ---")
    dialect = clevercsv.Sniffer().sniff(csv_text, verbose=False)
    if dialect:
        print(f"  Detected delimiter : {repr(dialect.delimiter)}")
        print(f"  Detected quotechar : {repr(dialect.quotechar)}")
    else:
        print("  Could not detect dialect, falling back to default.")

    reader = clevercsv.reader(io.StringIO(csv_text), dialect)
    rows = list(reader)
    header = rows[0] if rows else []
    data_rows = rows[1:] if len(rows) > 1 else []
    print(f"  Header: {header}")
    print(f"  Rows  : {len(data_rows)}")
    if data_rows:
        print(f"  First data row: {data_rows[0]}")
    return header, data_rows


def demo_file_roundtrip(csv_text):
    """Write CSV to a temp file, detect dialect from file, and read it back."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv",
                                     delete=False, encoding="utf-8") as f:
        f.write(csv_text)
        tmp_path = f.name

    try:
        # Detect the dialect from the file contents, then read rows with it
        with open(tmp_path, newline="", encoding="utf-8") as f:
            file_text = f.read()
        dialect = clevercsv.Sniffer().sniff(file_text, verbose=False)
        with open(tmp_path, newline="", encoding="utf-8") as f:
            rows = list(clevercsv.reader(f, dialect))
        print(f"\n--- File Round-trip (reader) ---")
        print(f"  File: {tmp_path}")
        print(f"  Total rows read (incl. header): {len(rows)}")
        if rows:
            print(f"  Header: {rows[0]}")
    finally:
        os.unlink(tmp_path)


def demo_dict_reader(csv_text, label):
    """Use clevercsv DictReader to get rows as dictionaries."""
    dialect = clevercsv.Sniffer().sniff(csv_text, verbose=False)
    reader = clevercsv.DictReader(io.StringIO(csv_text), dialect=dialect)
    rows = list(reader)
    print(f"\n--- DictReader: {label} ---")
    print(f"  Fields: {reader.fieldnames}")
    for row in rows[:2]:
        print(f"  {dict(row)}")


if __name__ == "__main__":
    print("=== CleverCSV Example: Robust CSV Dialect Detection & Parsing ===")

    detect_and_read(CSV_STANDARD, "Standard Comma-Separated")
    detect_and_read(CSV_SEMICOLON, "Semicolon-Separated")
    detect_and_read(CSV_TAB, "Tab-Separated with Quoted Commas")
    detect_and_read(CSV_MESSY, "Messy CSV with Extra Whitespace")

    demo_file_roundtrip(CSV_SEMICOLON)

    demo_dict_reader(CSV_STANDARD, "Employee Records")

    print("\nclevercsv example completed successfully.")
