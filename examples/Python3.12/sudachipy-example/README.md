## Program : Japanese Morphological Analysis with SudachiPy (SudachiPy 0.7.0)

### Purpose:
Demonstrates the user-facing Japanese NLP capabilities of **SudachiPy** — a Python port of the Sudachi morphological analyzer — in independent, self-contained sections.

### Packages used:

SudachiPy SudachiDict-core unittest importlib.metadata

### Functionality:
- Tokenizes Japanese text using the three **split modes** (A: short, B: middle, C: named-entity/long unit).
- Prints morpheme details: surface form, reading, dictionary form and part of speech.
- Normalizes orthographic variants (e.g. `附属` / `付属`, half-width kana) with `normalized_form()`.
- Maps inflected verbs back to their **dictionary (lemma) form**.
- Filters tokens by **part of speech** (noun extraction).
- Detects **out-of-vocabulary** (OOV) words.
- `sub-test1.py` verifies the installed version (0.7.0), split modes, lemmatization and POS tagging.

### How to run the example :
```
chmod +x install_test_example.sh
./install_test_example.sh
```

### License:
It's covered under Apache 2.0 licenses
