## ✅ Program: IBM Granite 3.2 and Granite 4.0-micro Instruct Model Validation Scripts

### Purpose:
This repository provides example scripts to validate the loading, configuration, and basic inference functionality of the **IBM Granite 3.2 2B Instruct** & **IBM Granite 4.0 micro Instruct** model.

---

### Packages Used:
- `torch`  
- `transformers`  
- *(optional)* `bitsandbytes` — for optimized model loading and quantization support

---

### Functionality:

#### **`granite3-example.py` & `granite4-example.py`**
- Loads the **IBM Granite 3.2 2B Instruct** & **IBM Granite 4.0 micro Instruct** model and tokenizer.  
- Demonstrates basic generation tasks:
  1. Explain a concept in simple terms.  
  2. Generate a short Python script.  
- Prints the model name and generated outputs for verification.

#### **`granite3-sub-test.py` & `granite4-sub-test.py`**
- Loads the same model and runs a series of structured inference tasks:
  - **Sentiment classification**
  - **Information extraction with JSON output**
  - **Code explanation**
- Uses controlled sampling parameters (`temperature=0.7`, `top_p=0.9`) for natural text generation.
- Displays prompt–response pairs for easy validation of model behavior.

---

### Example Prompts and Tasks:
| Task | Description | Example Prompt |
|------|--------------|----------------|
| Concept Explanation | Explain a model concept in simple terms | `"Explain IBM Granite 3.0 and 4.0 in simple terms"` |
| Code Generation | Write a basic Python script | `"Write a python script to return sum of two variables"` |
| Sentiment Analysis | Classify sentence sentiment | `"Classify the sentiment of this sentence: 'I absolutely love this phone!'"` |
| Entity Extraction | Extract structured info | `"Extract the person's name and location from this sentence: 'Alice went to New York to attend a tech conference.'"` |
| Code Understanding | Explain code behavior | `"Explain what this Python code does:\nfor i in range(5):\n    print(i * i)"` |

---

### How to Run the Examples:
```bash
# Make the scripts executable 
chmod +x install_test_example.sh
./install_test_example.sh
```

### License: 
It's covered under Apache 2.0 licenses