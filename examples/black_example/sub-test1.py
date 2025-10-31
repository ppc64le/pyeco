import unittest
import importlib.metadata
import black

class TestBlackLibrary(unittest.TestCase):
    def test_black_import(self):
        """Check if black can be imported"""
        try:
            import black
        except ImportError:
            self.fail("black is not installed")

    def test_black_version(self):
        """Verify black version"""
        version = importlib.metadata.version("black")
        self.assertEqual(version, "22.12.0", f"Expected black 22.12.0, got {version}")

    def test_black_formatting(self):
        """Use black.format_str to format Python code"""
        source_code = "x=  1+2"
        formatted = black.format_str(source_code, mode=black.FileMode())
        self.assertEqual(formatted, "x = 1 + 2\n", "Black did not format code as expected")

if __name__ == "__main__":
    unittest.main()
