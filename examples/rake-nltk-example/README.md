## Program : RAKE Keyword Extraction Test with NLTK (rake-nltk 1.x)

### Purpose:
Tests the functionality of the RAKE (Rapid Automatic Keyword Extraction) algorithm using **rake-nltk** with proper NLTK resource handling. The script extracts keyword phrases from input text or a file, ranks them, and displays their character spans in the original text.

### Packages used:

rake-nltk nltk argparse pathlib typing sys

### Functionality:
- Ensures required **NLTK resources** (`punkt`, `punkt_tab`, `stopwords`) are available and downloads them if missing.
- Accepts input text via:
  - command-line argument (`--text`)
  - a text file (`--file`)
  - or uses a built-in sample text.
- Builds stopword lists using NLTK with optional additional stopwords.
- Runs the **RAKE keyword extraction algorithm** using the public API of `rake-nltk`.
- Ranks extracted keyword phrases using configurable metrics (`degfreq` or `freq`).
- Finds character span locations of extracted phrases within the original text.
- Prints the **top ranked keyword phrases with scores and text spans**.
- Displays configuration information such as language, phrase length limits, and ranking metric.
- Performs sanity checks to confirm that keyword extraction completed successfully.

### How to run the example :
```
chmod +x install_test_example.sh
./install_test_example.sh
```

### License:
It's covered under Apache 2.0 licenses