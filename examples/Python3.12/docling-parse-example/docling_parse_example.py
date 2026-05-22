import sys
from pathlib import Path
from docling_parse.docling_parse import pdf_parser_v2

def parse_pdf_document(pdf_path: str) -> dict:
    """
    Parse a PDF document using docling-parse library.
    
    Args:
        pdf_path: Path to the PDF file to parse
        
    Returns:
        Dictionary containing parsed document information
    """
    try:
        # Parse the PDF document
        doc = pdf_parser_v2(pdf_path)
        
        # Extract basic information
        result = {
            "success": True,
            "num_pages": len(doc.pages) if hasattr(doc, 'pages') else 0,
            "has_text": bool(doc.text) if hasattr(doc, 'text') else False,
            "parser_version": "v2"
        }
        
        # Try to get page count and basic metadata
        if hasattr(doc, 'pages') and doc.pages:
            result["first_page_info"] = {
                "page_num": 1,
                "has_content": bool(doc.pages[0]) if doc.pages else False
            }
        
        return result
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }


def create_sample_pdf():
    """
    Create a simple sample PDF for testing purposes.
    """
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        pdf_path = "sample_document.pdf"
        c = canvas.Canvas(pdf_path, pagesize=letter)
        
        # Add some text content
        c.drawString(100, 750, "Sample PDF Document")
        c.drawString(100, 730, "This is a test document for docling-parse")
        c.drawString(100, 710, "Page 1 of 1")
        
        c.showPage()
        c.save()
        
        print(f"Created sample PDF: {pdf_path}")
        return pdf_path
        
    except ImportError:
        print("reportlab not available, skipping PDF creation")
        return None


if __name__ == "__main__":
    print("=" * 60)
    print("Docling-Parse PDF Parsing Example")
    print("=" * 60)
    
    # Check if a PDF path was provided as argument
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
        print(f"\nParsing provided PDF: {pdf_path}")
    else:
        # Try to create a sample PDF
        pdf_path = create_sample_pdf()
        if not pdf_path:
            print("\nNo PDF provided and couldn't create sample PDF")
            print("Usage: python docling_parse_example.py [path_to_pdf]")
            sys.exit(1)
    
    # Check if file exists
    if not Path(pdf_path).exists():
        print(f"\nError: PDF file not found: {pdf_path}")
        sys.exit(1)
    
    # Parse the PDF
    print(f"\nParsing PDF document...")
    result = parse_pdf_document(pdf_path)
    
    # Display results
    print("\n" + "=" * 60)
    print("Parsing Results:")
    print("=" * 60)
    
    if result["success"]:
        print(f"✓ Successfully parsed PDF")
        print(f"  - Number of pages: {result.get('num_pages', 'N/A')}")
        print(f"  - Has text content: {result.get('has_text', 'N/A')}")
        print(f"  - Parser version: {result.get('parser_version', 'N/A')}")
        
        if "first_page_info" in result:
            print(f"\n  First page information:")
            print(f"    - Page number: {result['first_page_info']['page_num']}")
            print(f"    - Has content: {result['first_page_info']['has_content']}")
    else:
        print(f"✗ Failed to parse PDF")
        print(f"  - Error type: {result.get('error_type', 'Unknown')}")
        print(f"  - Error message: {result.get('error', 'No details available')}")
    
    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)

# Made with Bob
