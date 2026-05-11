## ✅ Program : Tiktoken Tokenization Library Test

### Purpose:
Tests the **tiktoken** library, a fast BPE tokenizer for use with OpenAI's models. This example demonstrates various tokenization capabilities including encoding, decoding, model-specific encodings, and token counting.

### Packages used:
tiktoken  
regex  

### Functionality:
- **Basic Tokenization**: Encodes text to tokens and decodes back to verify correctness
- **Multiple Encodings**: Tests different encoding types (gpt2, r50k_base, p50k_base, cl100k_base)
- **Model-Specific Encoding**: Gets appropriate encoding for specific OpenAI models (GPT-4, GPT-3.5-turbo, etc.)
- **Token Counting**: Demonstrates token counting for different text types and lengths
- **Special Tokens**: Shows handling of special tokens in encoding/decoding
- **Special Characters**: Tests encoding of emojis, math symbols, and code
- **Batch Processing**: Encodes multiple texts and calculates token statistics
- **Context Window Limits**: Helps understand token limits for different message lengths

### How to run the example :
```
chmod +x install_test_example.sh
./install_test_example.sh
```

### Example Use Cases:
- **Token Counting**: Calculate tokens before sending to OpenAI API to manage costs
- **Context Management**: Ensure prompts fit within model context windows
- **Text Processing**: Understand how different texts are tokenized
- **Model Selection**: Compare token usage across different model encodings

### Notes:
- Tiktoken is significantly faster than other tokenizers
- Different models use different encodings (e.g., GPT-4 uses cl100k_base)
- Token counts affect API costs and context window limits
- The library supports special tokens used by OpenAI models

### License:
This project is covered under **Apache 2.0 License**.
