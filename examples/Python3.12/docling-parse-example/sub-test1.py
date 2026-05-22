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
        """Check if DoclingPdfParser can be imported"""
        try:
            from docling_parse.pdf_parser import DoclingPdfParser
            self.assertIsNotNone(DoclingPdfParser, "DoclingPdfParser should not be None")
        except ImportError as e:
            self.fail(f"Failed to import DoclingPdfParser: {e}")

    def test_pdf_parser_instantiation(self):
        """Check if DoclingPdfParser can be instantiated"""
        try:
            from docling_parse.pdf_parser import DoclingPdfParser
            parser = DoclingPdfParser()
            self.assertIsNotNone(parser, "Parser instance should not be None")
        except Exception as e:
            self.fail(f"Failed to instantiate DoclingPdfParser: {e}")

if __name__ == "__main__":
    unittest.main()

