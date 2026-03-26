#!/usr/bin/env python3
"""
ollama_example.py
Demonstrates basic ollama usage:
  1. List available models
  2. Show model metadata
  3. Single prompt generation
  4. Multi-turn conversation
"""

import subprocess
import wrapt

MODEL = "tinyllama:latest"

print(f"MODEL USED: {MODEL}\n")

# ----------------------------------------
# wrapt decorator for logging
# ----------------------------------------
@wrapt.decorator
def log_call(wrapped, instance, args, kwargs):
    print(f"[wrapt] Calling: {wrapped.__name__}")
    result = wrapped(*args, **kwargs)
    print(f"[wrapt] {wrapped.__name__} completed")
    return result

# ----------------------------------------
# Helper: run ollama command
# ----------------------------------------
def ollama_run(prompt, model=MODEL):
    result = subprocess.run(
        ["ollama", "run", model, prompt],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

# ----------------------------------------
# 1. List available models
# ----------------------------------------
print("=== 1. List Available Models ===")
result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
print(result.stdout.strip())

# ----------------------------------------
# 2. Show model metadata
# ----------------------------------------
print(f"\n=== 2. Show Model Metadata ({MODEL}) ===")
result = subprocess.run(
    ["ollama", "show", "--modelinfo", MODEL],
    capture_output=True, text=True
)
print(result.stdout.strip())

# ----------------------------------------
# 3. Single prompt — concept explanation
# ----------------------------------------
print("\n=== 3. Single Prompt ===")
prompt1 = "Explain what a large language model is in simple terms."
print(f"Prompt: {prompt1}")
print(f"Response: {ollama_run(prompt1)}")

# ----------------------------------------
# 4. Single prompt — code generation
# ----------------------------------------
print("\n=== 4. Code Generation ===")
prompt2 = "Write a Python function to return the sum of two numbers."
print(f"Prompt: {prompt2}")
print(f"Response: {ollama_run(prompt2)}")

# ----------------------------------------
# 5. Multi-turn conversation
# ----------------------------------------
print("\n=== 5. Multi-Turn Conversation ===")

@log_call
def run_turn(turn_num, user_msg, model=MODEL):
    print(f"\nTurn {turn_num} - User : {user_msg}")
    response = ollama_run(user_msg, model)
    print(f"Turn {turn_num} - Model: {response}")
    return response

conversation = [
    "What is supervised learning?",
    "Give a simple real world example.",
    "Summarize in one sentence.",
]

for i, msg in enumerate(conversation, 1):
    run_turn(i, msg)

print("\n=== ollama_example.py Complete ===")
