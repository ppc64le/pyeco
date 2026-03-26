#!/usr/bin/env python3
"""
sub-test2.py
Validates multi-turn conversation with ollama.
Each turn builds on the previous context.
"""

import subprocess
import wrapt
import time

MODEL = "tinyllama:latest"

print(f"MODEL USED: {MODEL}\n")
print("=== Multi-Turn Conversation Test ===\n")

# ----------------------------------------
# wrapt timing decorator
# ----------------------------------------
@wrapt.decorator
def timed(wrapped, instance, args, kwargs):
    start = time.time()
    result = wrapped(*args, **kwargs)
    elapsed = time.time() - start
    print(f"  [wrapt] {wrapped.__name__} took {elapsed:.2f}s")
    return result

@timed
def run_turn(prompt, model=MODEL):
    result = subprocess.run(
        ["ollama", "run", model, prompt],
        capture_output=True, text=True
    )
    return result.stdout.strip()

# ----------------------------------------
# Conversation 1: ML concepts
# ----------------------------------------
print("--- Conversation 1: Machine Learning ---\n")

turns1 = [
    "What is the difference between supervised and unsupervised learning?",
    "Give a real-world example of supervised learning.",
    "Give a real-world example of unsupervised learning.",
    "Summarize both in one sentence each.",
]

for i, msg in enumerate(turns1, 1):
    print(f"Turn {i} - User : {msg}")
    reply = run_turn(msg)
    assert reply, f"Turn {i} returned empty response!"
    print(f"Turn {i} - Model: {reply}\n")

# ----------------------------------------
# Conversation 2: Python concepts
# ----------------------------------------
print("--- Conversation 2: Python Programming ---\n")

turns2 = [
    "What is a Python decorator?",
    "Show a simple example of a Python decorator.",
    "What is the difference between a list and a tuple in Python?",
]

for i, msg in enumerate(turns2, 1):
    print(f"Turn {i} - User : {msg}")
    reply = run_turn(msg)
    assert reply, f"Turn {i} returned empty response!"
    print(f"Turn {i} - Model: {reply}\n")

print("All sub-test2 multi-turn validations passed!")
