#!/usr/bin/env python3
"""
sub-test1.py
Validates ollama inference with structured tasks:
  1. Sentiment classification
  2. Entity extraction (JSON)
  3. Code explanation
  4. Code generation
  5. Question answering
"""

import subprocess
import wrapt

MODEL = "tinyllama:latest"

print(f"MODEL USED: {MODEL}\n")

# ----------------------------------------
# wrapt decorator for timing
# ----------------------------------------
import time

@wrapt.decorator
def timed(wrapped, instance, args, kwargs):
    start = time.time()
    result = wrapped(*args, **kwargs)
    elapsed = time.time() - start
    print(f"  [wrapt] took {elapsed:.2f}s")
    return result

@timed
def run_task(prompt, model=MODEL):
    result = subprocess.run(
        ["ollama", "run", model, prompt],
        capture_output=True, text=True
    )
    return result.stdout.strip()

# ----------------------------------------
# Test cases
# ----------------------------------------
test_cases = [
    {
        "name": "Sentiment Classification",
        "prompt": "Classify the sentiment of this sentence: "
                  "'I absolutely love this phone!' "
                  "Answer with only: Positive, Neutral, or Negative."
    },
    {
        "name": "Entity Extraction",
        "prompt": "Extract the person name and location from: "
                  "'Alice went to New York to attend a tech conference.' "
                  "Return as JSON with keys: name, location."
    },
    {
        "name": "Code Explanation",
        "prompt": "Explain what this Python code does:\n"
                  "for i in range(5):\n"
                  "    print(i * i)"
    },
    {
        "name": "Code Generation",
        "prompt": "Write a Python script to return the sum of two variables."
    },
    {
        "name": "Question Answering",
        "prompt": "What is the capital of France? Answer in one word."
    },
]

print("=== Running Structured Test Cases ===\n")

for i, tc in enumerate(test_cases, 1):
    print(f"Task {i}: {tc['name']}")
    print(f"  Prompt : {tc['prompt']}")
    output = run_task(tc["prompt"])
    assert output, f"Task {i} returned empty response!"
    print(f"  Output : {output}")
    print()

print("All sub-test1 tasks passed!")
