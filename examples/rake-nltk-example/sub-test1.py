#!/usr/bin/env python3
"""
test_rake_nltk_v106.py

Standalone basic functionality test for rake-nltk (1.x).
- Ensures NLTK data ('punkt', 'punkt_tab', 'stopwords').
- Extracts keyphrases from built-in text.
- Computes simple case-insensitive character spans (no private attributes).

Run:
    python test_rake_nltk_v106.py
"""

import sys
from typing import List, Tuple

# ---------- NLTK resource handling ----------

NLTK_RESOURCES = [
    ("tokenizers/punkt", "punkt"),
    ("tokenizers/punkt_tab", "punkt_tab"),
    ("corpora/stopwords", "stopwords"),
]

def ensure_nltk_data(verbose: bool = True) -> None:
    try:
        import nltk
        for res_path, pkg in NLTK_RESOURCES:
            try:
                nltk.data.find(res_path)
            except LookupError:
                if verbose:
                    print(f"[INFO] Downloading NLTK resource: {pkg} ...")
                nltk.download(pkg, quiet=True)
    except Exception as e:
        if verbose:
            print(f"[WARN] Could not ensure NLTK data: {e}", file=sys.stderr)

# ---------- Helpers ----------

def get_sample_text() -> str:
    return (
        "Rapid Automatic Keyword Extraction (RAKE) is an algorithm for extracting key phrases "
        "from individual documents. It uses stopword lists and phrase delimiters to identify "
        "candidate keywords, then scores them based on word frequency and co-occurrence degree. "
        "RAKE is especially useful for quick keyword extraction in scenarios like summarization, "
        "topic exploration, and search indexing."
    )

def build_stopwords(language: str = "english", additional: List[str] | None = None) -> set:
    from nltk.corpus import stopwords
    try:
        sw = set(stopwords.words(language))
    except LookupError:
        try:
            sw = set(stopwords.words("english"))
        except LookupError:
            sw = {"the","is","and","in","to","of","for","a","an","on","with","by","it","from","as","that","this","be","are","or","at","its"}
    if additional:
        sw.update(w.lower() for w in additional)
    return sw

def find_all_spans(text: str, phrase: str) -> List[Tuple[int, int]]:
    spans = []
    if not phrase:
        return spans
    lt = text.lower()
    lp = phrase.lower()
    start = 0
    while True:
        idx = lt.find(lp, start)
        if idx == -1:
            break
        spans.append((idx, idx + len(phrase)))
        start = idx + len(phrase)
    return spans

# ---------- RAKE runner ----------

def run_rake_basic(text: str) -> List[Tuple[str, float]]:
    from rake_nltk import Rake
    sw = build_stopwords("english", additional=None)
    # ranking_metric: 1 (degree-to-frequency ratio), 2 (word frequency)
    rake = Rake(stopwords=sw, min_length=1, max_length=3, ranking_metric=1)
    rake.extract_keywords_from_text(text)
    ranked = rake.get_ranked_phrases_with_scores()  # [(score, phrase)]
    return [(phrase, float(score)) for score, phrase in ranked]

# ---------- Main ----------

def main():
    ensure_nltk_data(verbose=True)
    text = get_sample_text()
    print("\n" + "="*80)
    print("RAKE Basic Functionality Test")
    print("="*80)
    print(f"Text length: {len(text)} chars")

    try:
        results = run_rake_basic(text)
    except Exception as e:
        print(f"\n[ERROR] RAKE failed: {e}", file=sys.stderr)
        print("Make sure 'rake-nltk' and 'nltk' are installed: pip install rake-nltk nltk", file=sys.stderr)
        sys.exit(1)

    # Compute spans independently
    span_map = {phrase: find_all_spans(text, phrase) for phrase, _ in results}

    top_k = 15
    print("\nTop keyword phrases (score ↓):")
    print("-"*80)
    for i, (phrase, score) in enumerate(results[:top_k], start=1):
        spans = span_map.get(phrase, [])
        show = spans[0] if spans else (-1, -1)
        print(f"{i:>2}. {phrase:<60}  score={score:>8.4f}  span={show}")

    print("\nSanity check:")
    if results:
        print(f"[OK] Extracted {len(results)} phrases. Top: {results[0][0]} (score={results[0][1]:.4f})")
    else:
        print("[WARN] No phrases extracted.")

    print("\n[SUCCESS] rake-nltk basic test completed.")

if __name__ == "__main__":
    main()
