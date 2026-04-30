import tiktoken

def demonstrate_tiktoken():
    """
    Demonstrates tiktoken tokenization capabilities with various encodings.
    """
    print("=== 1. Basic Tokenization Test ===")
    
    # Get encoding for GPT-4
    encoding = tiktoken.get_encoding("cl100k_base")
    
    # Sample text
    text = "Hello, world! This is a test of the tiktoken library."
    
    # Encode text to tokens
    tokens = encoding.encode(text)
    print(f"Original text: {text}")
    print(f"Encoded tokens: {tokens}")
    print(f"Number of tokens: {len(tokens)}")
    
    # Decode tokens back to text
    decoded_text = encoding.decode(tokens)
    print(f"Decoded text: {decoded_text}")
    print()
    
    print("=== 2. Different Encoding Models ===")
    
    # Test different encodings
    encodings_to_test = ["gpt2", "r50k_base", "p50k_base", "cl100k_base"]
    test_text = "The quick brown fox jumps over the lazy dog."
    
    for enc_name in encodings_to_test:
        try:
            enc = tiktoken.get_encoding(enc_name)
            tokens = enc.encode(test_text)
            print(f"{enc_name}: {len(tokens)} tokens")
        except Exception as e:
            print(f"{enc_name}: Error - {e}")
    print()
    
    print("=== 3. Model-Specific Encoding ===")
    
    # Get encoding for specific models
    models_to_test = ["gpt-4", "gpt-3.5-turbo", "text-davinci-003"]
    
    for model_name in models_to_test:
        try:
            enc = tiktoken.encoding_for_model(model_name)
            tokens = enc.encode(test_text)
            print(f"{model_name}: {len(tokens)} tokens (encoding: {enc.name})")
        except Exception as e:
            print(f"{model_name}: Error - {e}")
    print()
    
    print("=== 4. Token Counting for Different Text Types ===")
    
    texts = [
        "Short text.",
        "This is a medium-length sentence with some punctuation!",
        "A longer paragraph with multiple sentences. It contains various words and punctuation marks. This helps demonstrate how tiktoken handles different text lengths and complexities.",
        "Code example: def hello_world():\n    print('Hello, World!')",
        "Special characters: @#$%^&*()_+-=[]{}|;:',.<>?/~`",
    ]
    
    encoding = tiktoken.get_encoding("cl100k_base")
    
    for i, text in enumerate(texts, 1):
        tokens = encoding.encode(text)
        print(f"Text {i}: {len(tokens)} tokens")
        print(f"  Preview: {text[:50]}{'...' if len(text) > 50 else ''}")
    print()
    
    print("=== 5. Encoding and Decoding with Special Tokens ===")
    
    # Test with special tokens
    text_with_special = "Hello <|endoftext|> World"
    
    # Encode with special tokens disallowed (treat as normal text)
    tokens_normal = encoding.encode(text_with_special, disallowed_special=())
    print(f"Normal encoding (special tokens as text): {tokens_normal}")
    
    # Encode with special tokens allowed
    tokens_special = encoding.encode(text_with_special, allowed_special="all")
    print(f"With special tokens: {tokens_special}")
    
    # Decode both
    decoded_normal = encoding.decode(tokens_normal)
    decoded_special = encoding.decode(tokens_special)
    print(f"Decoded normal: {decoded_normal}")
    print(f"Decoded special: {decoded_special}")
    print()
    
    print("=== 6. List Available Encodings ===")
    
    # List all available encodings
    print("Available encodings:")
    for enc_name in tiktoken.list_encoding_names():
        print(f"  - {enc_name}")
    print()
    
    print("=== Script Complete ===")


if __name__ == "__main__":
    demonstrate_tiktoken()


