import unittest
from pathlib import Path
import sys

class TestDoclingParseIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Create a test PDF before running tests"""
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter
            
            cls.test_pdf_path = "integration_test.pdf"
            c = canvas.Canvas(cls.test_pdf_path, pagesize=letter)
            c.drawString(100, 750, "Integration Test PDF")
            c.drawString(100, 730, "This document is used for testing docling-parse")
            c.drawString(100, 710, "Line 3 of test content")
            c.showPage()
            c.save()
            
        except Exception as e:
            print(f"Warning: Could not create test PDF: {e}")
            cls.test_pdf_path = None

    @classmethod
    def tearDownClass(cls):
        """Clean up test PDF after tests"""
        if cls.test_pdf_path and Path(cls.test_pdf_path).exists():
            Path(cls.test_pdf_path).unlink()

    def test_parse_pdf_with_docling(self):
        """Test parsing a PDF with docling-parse"""
        if not self.test_pdf_path:
            self.skipTest("Test PDF not available")
        
        try:
            from docling_parse.docling_parse import pdf_parser_v2
            
            # Parse the test PDF
            doc = pdf_parser_v2(self.test_pdf_path)
            
            # Basic assertions
            self.assertIsNotNone(doc, "Parsed document should not be None")
            
            # Check if document has expected attributes
            has_pages = hasattr(doc, 'pages')
            has_text = hasattr(doc, 'text')
            
            # At least one of these should be true for a valid parse
            self.assertTrue(has_pages or has_text, 
                          "Parsed document should have pages or text attribute")
            
        except Exception as e:
            self.fail(f"Failed to parse PDF with docling-parse: {e}")

    def test_docling_parse_error_handling(self):
        """Test error handling for non-existent PDF"""
        try:
            from docling_parse.docling_parse import pdf_parser_v2
            
            # Try to parse a non-existent file
            non_existent_pdf = "this_file_does_not_exist.pdf"
            
            with self.assertRaises(Exception):
                pdf_parser_v2(non_existent_pdf)
                
        except ImportError:
            self.skipTest("docling-parse not available")

if __name__ == "__main__":
    unittest.main()

# Made with Bob
