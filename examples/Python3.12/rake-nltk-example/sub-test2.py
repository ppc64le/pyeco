#!/usr/bin/env python3
"""
rake_batch_eval_standalone.py

Standalone batch test for rake-nltk (1.x):
- Processes a built-in list of documents (no args needed).
- Prints top keyphrases per document.
- Exports combined results to CSV and JSON.

Run:
    python rake_batch_eval_standalone.py
"""

import csv
import json
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
            print(f"[WARN] Could not ensure NLTK data: {e}")

# ---------- Sample corpus ----------

DOCS = [
    ("doc_01_news",
     "The central bank announced a surprise cut in interest rates to stimulate economic growth. "
     "Analysts expect a positive reaction from equity markets, while bond yields may decline."),
    ("doc_02_tech",
     "Large language models have transformed natural language processing. "
     "Developers leverage transformer architectures and fine-tuning techniques for domain-specific tasks."),
    ("doc_03_product",
     "Our new smartwatch features extended battery life, heart-rate monitoring, and improved GPS accuracy. "
     "It integrates seamlessly with popular fitness apps and supports contactless payments."),
]

# ---------- RAKE helpers ----------

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

def run_rake(text: str, language: str = "english", min_length: int = 1, max_length: int = 3,
             ranking_metric: str = "degfreq", additional_stopwords: List[str] | None = None) -> List[Tuple[str, float]]:
    from rake_nltk import Rake
    ranking = 1 if ranking_metric == "degfreq" else 2
    sw = build_stopwords(language, additional_stopwords)
    rake = Rake(stopwords=sw, min_length=min_length, max_length=max_length, ranking_metric=ranking)
    rake.extract_keywords_from_text(text)
    ranked = rake.get_ranked_phrases_with_scores()
    return [(phrase, float(score)) for score, phrase in ranked]

# ---------- Main ----------

def main():
    ensure_nltk_data(verbose=True)
    language = "english"
    min_len, max_len = 1, 3
    ranking = "degfreq"
    top_k = 10

    all_rows = []
    print("\n" + "="*80)
    print("Batch RAKE Test over Built-in Documents")
    print("="*80)

    for name, text in DOCS:
        ranked = run_rake(text, language=language, min_length=min_len, max_length=max_len, ranking_metric=ranking)
        top = ranked[:top_k]

        print("\n" + "-"*80)
        print(f"Document: {name} (len={len(text)} chars) — Top {top_k}")
        print("-"*80)
        for i, (phrase, score) in enumerate(top, start=1):
            print(f"{i:>2}. {phrase:<60}  score={score:>8.4f}")
            all_rows.append({
                "document": name,
                "rank": i,
                "phrase": phrase,
                "score": score,
                "length_chars": len(phrase),
            })

    # Exports
    csv_path = "rake_batch_results.csv"
    json_path = "rake_batch_results.json"
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["document", "rank", "phrase", "score", "length_chars"])
        writer.writeheader()
        writer.writerows(all_rows)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(all_rows, f, ensure_ascii=False, indent=2)

    print(f"\n[OK] Wrote CSV:  {csv_path}")
    print(f"[OK] Wrote JSON: {json_path}")
    print("\n[SUCCESS] Batch RAKE test completed.")

if __name__ == "__main__":
    main()
