## ✅ Program: Ollama POWER10 ppc64le Wheel Validation Scripts

## Purpose
This repository provides example scripts to validate the installation, configuration, and inference functionality of the **Ollama Power10-optimized ppc64le wheel**.

---

## Packages Used
- `ollama-python-package==0.13.5+ppc64le1` — Power10-only wheel (bundled Ollama binary + shared libraries)
- `wrapt==1.17.3+ppc64le1` — for logging and timing decorators

---

## Functionality

### `ollama_example.py`
- Lists available models on the Ollama server
- Displays model metadata
- Demonstrates basic inference tasks:
  - Concept explanation
  - Code generation
- Runs a multi-turn conversation
- Uses `wrapt` for logging function calls

---

### `sub-test1.py`
- Runs structured inference tasks using `ollama run`:
  - Sentiment classification
  - Entity extraction (JSON output)
  - Code explanation
  - Code generation
  - Question answering
- Uses `wrapt` timing decorator
- Validates that all responses are non-empty

---

### `sub-test2.py`
- Executes multi-turn conversation validation:
  - Conversation 1: Machine Learning concepts (4 turns)
  - Conversation 2: Python Programming concepts (3 turns)
- Uses `wrapt` timing decorator for each turn
- Ensures valid responses for every interaction

---

## Example Prompts and Tasks

| Task                | Description                                      | Example Prompt |
|---------------------|--------------------------------------------------|----------------|
| Concept Explanation | Explain a concept in simple terms                | "Explain what a large language model is in simple terms" |
| Code Generation     | Generate simple Python code                      | "Write a Python function to return the sum of two numbers" |
| Sentiment Analysis  | Classify sentence sentiment                      | "Classify the sentiment of this sentence: 'I absolutely love this phone!'" |
| Entity Extraction   | Extract structured information (JSON)            | "Extract the person name and location from: 'Alice went to New York to attend a tech conference.'" |
| Code Understanding  | Explain code behavior                            | "Explain what this Python code does:\nfor i in range(5):\n    print(i * i)" |
| Question Answering  | Answer factual questions                         | "What is the capital of France?" |

---

## Supported Architecture

- ✅ IBM Power10 (ppc64le)

---

## How to Run the Examples

```bash
# Make the script executable
chmod +x install_test_example.sh

# Run the validation
./install_test_example.sh
