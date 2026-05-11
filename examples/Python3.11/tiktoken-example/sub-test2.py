import tiktoken

def test_multiple_encodings():
    """Test different encoding types"""
    print("=== Testing Multiple Encodings ===")
    
    text = "The quick brown fox jumps over the lazy dog."
    encodings = ["gpt2", "r50k_base", "p50k_base", "cl100k_base"]
    
    for enc_name in encodings:
        try:
            encoding = tiktoken.get_encoding(enc_name)
            tokens = encoding.encode(text)
            decoded = encoding.decode(tokens)
            
            print(f"\nEncoding: {enc_name}")
            print(f"  Token count: {len(tokens)}")
            print(f"  First 5 tokens: {tokens[:5]}")
            print(f"  Decoding matches: {decoded == text}")
            
            assert decoded == text, f"Decoding failed for {enc_name}"
            print(f"  ✓ Test passed for {enc_name}")
            
        except Exception as e:
            print(f"  ✗ Error with {enc_name}: {e}")

def test_special_characters():
    """Test encoding of special characters"""
    print("\n=== Testing Special Characters ===")
    
    encoding = tiktoken.get_encoding("cl100k_base")
    
    special_texts = [
        "Hello, World! 123",
        "Émojis: 😀 🎉 🚀",
        "Math: ∑ ∫ √ π",
        "Code: def func(): return True",
        "Symbols: @#$%^&*()",
    ]
    
    for text in special_texts:
        tokens = encoding.encode(text)
        decoded = encoding.decode(tokens)
        print(f"\nText: {text}")
        print(f"  Tokens: {len(tokens)}")
        print(f"  Match: {decoded == text}")

def test_long_text():
    """Test encoding of longer text"""
    print("\n=== Testing Long Text ===")
    
    encoding = tiktoken.get_encoding("cl100k_base")
    
    long_text = " ".join(["This is sentence number {}.".format(i) for i in range(100)])
    
    tokens = encoding.encode(long_text)
    decoded = encoding.decode(tokens)
    
    print(f"Original length: {len(long_text)} characters")
    print(f"Token count: {len(tokens)}")
    print(f"Decoding matches: {decoded == long_text}")
    
    assert decoded == long_text, "Long text decoding failed"
    print("✓ Long text test passed")

if __name__ == "__main__":
    test_multiple_encodings()
    test_special_characters()
    test_long_text()
    print("\n=== All Sub-Test 2 Complete ===")


