#!/usr/bin/env python3
"""
test_rake_nltk_v106.py

Version-safe RAKE test script for rake-nltk 1.0.6 (and other 1.x).
- Ensures NLTK resources: 'punkt', 'punkt_tab', 'stopwords'
- Runs RAKE keyword extraction without touching private attributes
- Optionally computes character spans using a simple search (no tokenizer)

Usage:
    pip install rake-nltk nltk
    python test_rake_nltk_v106.py
"""

import argparse
import sys
from pathlib import Path
from typing import List, Tuple

# ---------------------------
# NLTK data management
# ---------------------------

NLTK_RESOURCES = [
    ("tokenizers/punkt", "punkt"),
    ("tokenizers/punkt_tab", "punkt_tab"),
    ("corpora/stopwords", "stopwords"),
]

def ensure_nltk_data(verbose: bool = True) -> dict:
    status = {"punkt": False, "punkt_tab": False, "stopwords": False, "errors": []}
    try:
        import nltk
        for res_path, pkg in NLTK_RESOURCES:
            try:
                nltk.data.find(res_path)
                status[pkg] = True
            except LookupError:
                if verbose:
                    print(f"[INFO] Downloading NLTK resource: {pkg} ...")
                try:
                    nltk.download(pkg, quiet=True)
                    nltk.data.find(res_path)
                    status[pkg] = True
                except Exception as e:
                    status["errors"].append(f"{pkg}: {e}")
                    if verbose:
                        print(f"[WARN] Could not download {pkg}: {e}", file=sys.stderr)
    except Exception as e:
        status["errors"].append(f"nltk-core: {e}")
        if verbose:
            print(f"[WARN] Could not import NLTK: {e}", file=sys.stderr)
    return status

# ---------------------------
# Utilities
# ---------------------------

def load_text_from_file(path: str) -> str:
    p = Path(path)
    if not p.exists() or not p.is_file():
        raise FileNotFoundError(f"File not found: {path}")
    return p.read_text(encoding="utf-8", errors="ignore")

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
            sw = {
                "the","is","and","in","to","of","for","a","an","on","with","by","it","from","as","that",
                "this","be","are","or","at","its"
            }
    if additional:
        sw.update(w.lower() for w in additional)
    return sw

def find_all_spans(text: str, phrase: str) -> List[Tuple[int, int]]:
    """
    Find all non-overlapping case-insensitive occurrences of `phrase` in `text`.
    Returns list of (start, end) character indices. Independent of RAKE internals.
    """
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

# ---------------------------
# RAKE runner
# ---------------------------

def run_rake_v106(
    text: str,
    language: str = "english",
    min_length: int = 1,
    max_length: int = 3,
    ranking_metric: str = "degfreq",
    additional_stopwords: List[str] | None = None,
):
    """
    Execute RAKE with rake-nltk 1.x public API only.
    Returns:
      - ranked_pairs: List[(phrase, score)]
      - span_map: dict phrase -> List[(start, end)] (may have multiple matches)
    """
    from rake_nltk import Rake

    # ranking_metric in rake-nltk: 1 (degree_to_frequency_ratio), 2 (word_frequency)
    if ranking_metric.lower() == "degfreq":
        ranking = 1
    elif ranking_metric.lower() == "freq":
        ranking = 2
    else:
        raise ValueError("ranking_metric must be one of {'degfreq','freq'}")

    sw = build_stopwords(language, additional_stopwords)

    rake = Rake(
        stopwords=sw,
        min_length=min_length,
        max_length=max_length,
        ranking_metric=ranking,
    )
    rake.extract_keywords_from_text(text)

    # Public APIs:
    # - get_ranked_phrases_with_scores() -> [(score, phrase), ...]
    # - get_ranked_phrases() -> [phrase, ...]
    ranked = rake.get_ranked_phrases_with_scores()
    ranked_pairs = [(phrase, float(score)) for score, phrase in ranked]

    # Compute spans independently (case-insensitive exact string match)
    span_map = {phrase: find_all_spans(text, phrase) for phrase, _ in ranked_pairs}

    return ranked_pairs, span_map

# ---------------------------
# CLI & printing
# ---------------------------

def pretty_print_results(
    results: List[Tuple[str, float]],
    span_map: dict[str, List[Tuple[int, int]]],
    top_k: int = 15,
):
    print("\n" + "=" * 80)
    print(f"Top {top_k} Keyword Phrases (score ↓):")
    print("=" * 80)
    for i, (phrase, score) in enumerate(results[:top_k], start=1):
        spans = span_map.get(phrase, [])
        # show first span if present, else (-1, -1)
        span_txt = spans[0] if spans else (-1, -1)
        print(f"{i:>2}. {phrase:<60}  score={score:>8.4f}  span={span_txt}")

def parse_args():
    ap = argparse.ArgumentParser(description="Test rake-nltk (1.x) functionality.")
    src = ap.add_mutually_exclusive_group()
    src.add_argument("--text", type=str, help="Raw text to analyze.")
    src.add_argument("--file", type=str, help="Path to a .txt file to analyze.")
    ap.add_argument("--language", type=str, default="english", help="Stopwords language (default: english).")
    ap.add_argument("--min-length", type=int, default=1, help="Minimum words in a phrase (default: 1).")
    ap.add_argument("--max-length", type=int, default=3, help="Maximum words in a phrase (default: 3).")
    ap.add_argument("--ranking", type=str, default="degfreq", choices=["degfreq", "freq"],
                    help="Ranking metric: 'degfreq' or 'freq'.")
    ap.add_argument("--add-stop", type=str, nargs="*", default=None,
                    help="Additional stopwords to ignore (space-separated).")
    ap.add_argument("--top-k", type=int, default=15, help="How many phrases to print (default: 15).")
    return ap.parse_args()

def main():
    args = parse_args()

    status = ensure_nltk_data(verbose=True)
    have_punkt = status.get("punkt", False)
    have_punkt_tab = status.get("punkt_tab", False)
    have_stop = status.get("stopwords", False)

    print("\n" + "=" * 80)
    print("NLTK Resource Status")
    print("=" * 80)
    print(f"punkt      : {'OK' if have_punkt else 'MISSING'}")
    print(f"punkt_tab  : {'OK' if have_punkt_tab else 'MISSING'}")
    print(f"stopwords  : {'OK' if have_stop else 'MISSING'}")
    if status.get("errors"):
        for e in status["errors"]:
            print(f"[WARN] {e}", file=sys.stderr)

    if args.file:
        text = load_text_from_file(args.file)
    elif args.text:
        text = args.text
    else:
        text = get_sample_text()
        print("\n[INFO] Using built-in sample text. Use --text or --file to test your own input.")

    print("\n" + "=" * 80)
    print("Configuration")
    print("=" * 80)
    print(f"Language      : {args.language}")
    print(f"Min/Max length: {args.min_length}/{args.max_length}")
    print(f"Ranking       : {args.ranking}")
    print(f"Extra stopwords: {args.add_stop or []}")
    print(f"Text length   : {len(text)} chars")

    try:
        results, span_map = run_rake_v106(
            text=text,
            language=args.language,
            min_length=args.min_length,
            max_length=args.max_length,
            ranking_metric=args.ranking,
            additional_stopwords=args.add_stop,
        )
    except Exception as e:
        print("\n[ERROR] RAKE failed:", e, file=sys.stderr)
        print("[HINT] Ensure 'rake-nltk' (1.x) and 'nltk' are installed:", file=sys.stderr)
        print("       pip install rake-nltk nltk", file=sys.stderr)
        sys.exit(1)

    pretty_print_results(results, span_map, top_k=args.top_k)

    print("\n" + "=" * 80)
    print("Sanity Checks")
    print("=" * 80)
    if not results:
        print("[WARN] No phrases extracted. Consider lowering min-length or checking text quality.")
    else:
        top_phrase, top_score = results[0]
        matches = span_map.get(top_phrase, [])
        print(f"[OK] Extracted {len(results)} phrases. Top: '{top_phrase}' (score={top_score:.4f}) spans={matches[:1] or [(-1,-1)]}")

    print("\n[SUCCESS] rake-nltk appears to be working.")

if __name__ == "__main__":
    main()