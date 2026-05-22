import unittest
import importlib.metadata

class TestDoclingParseLibrary(unittest.TestCase):
    def test_docling_parse_import(self):
        """Check if docling-parse can be imported"""
        try:
            import docling_parse
        except ImportError:
            self.fail("docling-parse is not installed")

    def test_docling_parse_version(self):
        """Verify docling-parse version"""
        version = importlib.metadata.version("docling-parse")
        assert "5.8.0" in version, f"Expected docling-parse 5.8.0, got {version}"

    def test_pdf_parser_import(self):
        """Check if pdf_parser_v2 can be imported"""
        try:
            from docling_parse import pdf_parser_v2
            self.assertIsNotNone(pdf_parser_v2, "pdf_parser_v2 should not be None")
        except ImportError as e:
            self.fail(f"Failed to import pdf_parser_v2: {e}")

if __name__ == "__main__":
    unittest.main()

# Made with Bob
