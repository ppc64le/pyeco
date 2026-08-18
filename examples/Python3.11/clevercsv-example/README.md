## Purpose: Demonstrates robust CSV dialect detection and parsing using the clevercsv library.

### Packages used:
clevercsv

### Functionality:

- Detects CSV dialects (delimiter, quotechar) automatically from raw CSV strings using the CleverCSV Sniffer.
- Parses comma-separated, semicolon-separated, tab-separated, and messy CSV data with inconsistent whitespace.
- Reads rows from in-memory CSV strings using `clevercsv.reader`.
- Reads CSV data as dictionaries using `clevercsv.DictReader`, exposing field names automatically from the header row.
- Reads a CSV file from disk using `clevercsv.read_csv` with auto-detected dialect.

### How to run the example :
```
chmod +x install_test_example.sh
./install_test_example.sh
```

### License:
It's covered under MIT License 
