import tiktoken

def test_model_encodings():
    """Test encoding for specific models"""
    print("=== Testing Model-Specific Encodings ===")
    
    models = [
        "gpt-4",
        "gpt-4-32k",
        "gpt-3.5-turbo",
        "gpt-3.5-turbo-16k",
        "text-davinci-003",
        "text-davinci-002",
    ]
    
    text = "This is a test sentence for model encoding."
    
    for model in models:
        try:
            encoding = tiktoken.encoding_for_model(model)
            tokens = encoding.encode(text)
            decoded = encoding.decode(tokens)
            
            print(f"\nModel: {model}")
            print(f"  Encoding name: {encoding.name}")
            print(f"  Token count: {len(tokens)}")
            print(f"  Decoding matches: {decoded == text}")
            
            assert decoded == text, f"Decoding failed for {model}"
            print(f"  ✓ Test passed")
            
        except Exception as e:
            print(f"  ✗ Error: {e}")

def test_token_limits():
    """Test token counting for context window limits"""
    print("\n=== Testing Token Limits ===")
    
    encoding = tiktoken.get_encoding("cl100k_base")
    
    # Simulate different message lengths
    messages = [
        "Short message.",
        "This is a medium-length message with more content.",
        " ".join(["Word"] * 100),  # 100 words
        " ".join(["Word"] * 1000),  # 1000 words
    ]
    
    for i, msg in enumerate(messages, 1):
        tokens = encoding.encode(msg)
        print(f"\nMessage {i}:")
        print(f"  Character count: {len(msg)}")
        print(f"  Token count: {len(tokens)}")
        print(f"  Chars per token: {len(msg) / len(tokens):.2f}")

def test_encoding_names():
    """Test listing and accessing encoding names"""
    print("\n=== Testing Encoding Names ===")
    
    encoding_names = tiktoken.list_encoding_names()
    print(f"Available encodings: {len(encoding_names)}")
    
    for name in encoding_names:
        try:
            enc = tiktoken.get_encoding(name)
            print(f"  ✓ {name}: Successfully loaded")
        except Exception as e:
            print(f"  ✗ {name}: Error - {e}")

def test_batch_encoding():
    """Test encoding multiple texts"""
    print("\n=== Testing Batch Encoding ===")
    
    encoding = tiktoken.get_encoding("cl100k_base")
    
    texts = [
        "First text to encode.",
        "Second text to encode.",
        "Third text to encode.",
        "Fourth text to encode.",
        "Fifth text to encode.",
    ]
    
    total_tokens = 0
    for i, text in enumerate(texts, 1):
        tokens = encoding.encode(text)
        total_tokens += len(tokens)
        print(f"Text {i}: {len(tokens)} tokens")
    
    print(f"\nTotal tokens across all texts: {total_tokens}")
    print(f"Average tokens per text: {total_tokens / len(texts):.2f}")

if __name__ == "__main__":
    test_model_encodings()
    test_token_limits()
    test_encoding_names()
    test_batch_encoding()
    print("\n=== All Sub-Test 3 Complete ===")


