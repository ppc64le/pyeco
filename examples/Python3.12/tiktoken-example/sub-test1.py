import unittest
import importlib.metadata
import tiktoken

class TestTiktokenLibrary(unittest.TestCase):
    def test_tiktoken_import(self):
        """Check if tiktoken can be imported"""
        try:
            import tiktoken
        except ImportError:
            self.fail("tiktoken is not installed")

    def test_tiktoken_version(self):
        """Verify tiktoken version"""
        version = importlib.metadata.version("tiktoken")
        assert "0.7.0" in version, f"Expected tiktoken 0.7.0, got {version}"

    def test_basic_encoding(self):
        """Test basic encoding functionality"""
        encoding = tiktoken.get_encoding("cl100k_base")
        text = "Hello, world!"
        tokens = encoding.encode(text)
        self.assertIsInstance(tokens, list, "Encoding should return a list")
        self.assertGreater(len(tokens), 0, "Tokens list should not be empty")
        
    def test_encoding_decoding(self):
        """Test that encoding and decoding are reversible"""
        encoding = tiktoken.get_encoding("cl100k_base")
        original_text = "This is a test sentence."
        tokens = encoding.encode(original_text)
        decoded_text = encoding.decode(tokens)
        self.assertEqual(original_text, decoded_text, "Decoded text should match original")

if __name__ == "__main__":
    unittest.main()


