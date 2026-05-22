import unittest
from pathlib import Path

class TestReportlabPDFCreation(unittest.TestCase):
    def test_reportlab_import(self):
        """Check if reportlab can be imported"""
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter
        except ImportError:
            self.fail("reportlab is not installed")

    def test_create_simple_pdf(self):
        """Test creating a simple PDF with reportlab"""
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter
            
            pdf_path = "test_document.pdf"
            c = canvas.Canvas(pdf_path, pagesize=letter)
            c.drawString(100, 750, "Test PDF Document")
            c.showPage()
            c.save()
            
            # Verify file was created
            self.assertTrue(Path(pdf_path).exists(), "PDF file was not created")
            
            # Clean up
            Path(pdf_path).unlink()
            
        except Exception as e:
            self.fail(f"Failed to create PDF: {e}")

    def test_pillow_import(self):
        """Check if Pillow can be imported"""
        try:
            from PIL import Image
        except ImportError:
            self.fail("Pillow is not installed")

if __name__ == "__main__":
    unittest.main()

# Made with Bob
