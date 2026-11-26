import unittest
import importlib.metadata
from sudachipy import dictionary, tokenizer


class TestSudachiPyLibrary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tokenizer = dictionary.Dictionary().tokenizer()

    def test_sudachipy_import(self):
        """Check if sudachipy can be imported"""
        try:
            import sudachipy  # noqa: F401
        except ImportError:
            self.fail("sudachipy is not installed")

    def test_sudachipy_version(self):
        """Verify SudachiPy version"""
        version = importlib.metadata.version("SudachiPy")
        assert "0.7.0" in version, f"Expected SudachiPy 0.7.0, got {version}"

    def test_split_modes(self):
        """Mode A should split into units no longer than mode C"""
        text = "国家公務員"
        a = self.tokenizer.tokenize(text, tokenizer.Tokenizer.SplitMode.A)
        c = self.tokenizer.tokenize(text, tokenizer.Tokenizer.SplitMode.C)
        self.assertGreaterEqual(len(a), len(c))
        self.assertEqual("".join(m.surface() for m in a), text)

    def test_dictionary_form(self):
        """Inflected verbs should map back to their dictionary form"""
        tokens = self.tokenizer.tokenize("食べました", tokenizer.Tokenizer.SplitMode.C)
        self.assertEqual(tokens[0].dictionary_form(), "食べる")

    def test_part_of_speech(self):
        """Nouns should be tagged as 名詞"""
        tokens = self.tokenizer.tokenize("東京", tokenizer.Tokenizer.SplitMode.C)
        self.assertEqual(tokens[0].part_of_speech()[0], "名詞")


if __name__ == "__main__":
    unittest.main()
