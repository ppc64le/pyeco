import sys
from pathlib import Path
from typing import List, Dict
from docling_parse.pdf_parser import DoclingPdfParser

def parse_pdf_with_docling(pdf_path: str) -> str:
    """
    Parse a PDF document using docling-parse and extract text content.
    
    Args:
        pdf_path: Path to the PDF file to parse
        
    Returns:
        Extracted text content from the PDF
    """
    try:
        # Create parser instance and parse the PDF document
        parser = DoclingPdfParser()
        doc = parser.parse(pdf_path)
        
        # Extract text content from pages
        text_content = ""
        
        if hasattr(doc, 'pages') and doc.pages:
            for page in doc.pages:
                # Extract text from cells in the page
                if hasattr(page, 'cells'):
                    for cell in page.cells:
                        if hasattr(cell, 'text'):
                            text_content += cell.text + " "
                    text_content += "\n"
        
        return text_content.strip() if text_content else "No text content extracted"
        
    except Exception as e:
        return f"Error parsing PDF: {str(e)}"


def create_document_chunks(text: str, chunk_size: int = 500) -> List[str]:
    """
    Split document text into smaller chunks for RAG processing.
    
    Args:
        text: Full document text
        chunk_size: Size of each chunk in characters
        
    Returns:
        List of text chunks
    """
    # Simple chunking by character count
    chunks = []
    words = text.split()
    current_chunk = []
    current_size = 0
    
    for word in words:
        word_size = len(word) + 1  # +1 for space
        if current_size + word_size > chunk_size and current_chunk:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
            current_size = word_size
        else:
            current_chunk.append(word)
            current_size += word_size
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks


def simple_keyword_search(chunks: List[str], query: str) -> List[Dict[str, any]]:
    """
    Simple keyword-based retrieval (mock RAG retrieval).
    In a real RAG system, this would use embeddings and vector search.
    
    Args:
        chunks: List of document chunks
        query: Search query
        
    Returns:
        List of relevant chunks with scores
    """
    results = []
    query_lower = query.lower()
    query_words = set(query_lower.split())
    
    for idx, chunk in enumerate(chunks):
        chunk_lower = chunk.lower()
        # Simple scoring: count matching words
        matches = sum(1 for word in query_words if word in chunk_lower)
        
        if matches > 0:
            results.append({
                "chunk_id": idx,
                "text": chunk,
                "score": matches,
                "preview": chunk[:200] + "..." if len(chunk) > 200 else chunk
            })
    
    # Sort by score (descending)
    results.sort(key=lambda x: x["score"], reverse=True)
    return results


def create_sample_pdf():
    """
    Create a sample PDF document with RAG-relevant content.
    """
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        pdf_path = "rag_sample_document.pdf"
        c = canvas.Canvas(pdf_path, pagesize=letter)
        
        # Add content about AI and machine learning
        y_position = 750
        content = [
            "Introduction to Artificial Intelligence",
            "",
            "Artificial Intelligence (AI) is the simulation of human intelligence",
            "processes by machines, especially computer systems. These processes",
            "include learning, reasoning, and self-correction.",
            "",
            "Machine Learning is a subset of AI that provides systems the ability",
            "to automatically learn and improve from experience without being",
            "explicitly programmed. Deep learning is a subset of machine learning.",
            "",
            "Natural Language Processing (NLP) is a branch of AI that helps",
            "computers understand, interpret and manipulate human language.",
            "NLP draws from many disciplines, including computer science and",
            "computational linguistics.",
        ]
        
        for line in content:
            c.drawString(50, y_position, line)
            y_position -= 20
        
        c.showPage()
        c.save()
        
        print(f"✓ Created sample PDF: {pdf_path}")
        return pdf_path
        
    except ImportError:
        print("✗ reportlab not available, skipping PDF creation")
        return None


if __name__ == "__main__":
    print("=" * 70)
    print("Simple RAG Application with Docling-Parse")
    print("=" * 70)
    
    # Step 1: Get or create PDF document
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
        print(f"\n[1/5] Using provided PDF: {pdf_path}")
    else:
        print("\n[1/5] Creating sample PDF document...")
        pdf_path = create_sample_pdf()
        if not pdf_path:
            print("\n✗ No PDF provided and couldn't create sample PDF")
            print("Usage: python docling_parse_example.py [path_to_pdf]")
            sys.exit(1)
    
    # Check if file exists
    if not Path(pdf_path).exists():
        print(f"\n✗ Error: PDF file not found: {pdf_path}")
        sys.exit(1)
    
    # Step 2: Parse PDF with docling-parse
    print("\n[2/5] Parsing PDF with docling-parse...")
    document_text = parse_pdf_with_docling(pdf_path)
    print(f"✓ Extracted {len(document_text)} characters")
    
    # Step 3: Create document chunks
    print("\n[3/5] Creating document chunks for RAG...")
    chunks = create_document_chunks(document_text, chunk_size=300)
    print(f"✓ Created {len(chunks)} chunks")
    
    # Step 4: Demonstrate retrieval
    print("\n[4/5] Performing keyword-based retrieval...")
    query = "machine learning"
    print(f"Query: '{query}'")
    
    results = simple_keyword_search(chunks, query)
    print(f"✓ Found {len(results)} relevant chunks")
    
    # Step 5: Display results
    print("\n[5/5] Top Retrieved Chunks:")
    print("=" * 70)
    
    for i, result in enumerate(results[:3], 1):  # Show top 3
        print(f"\nChunk #{result['chunk_id']} (Score: {result['score']})")
        print("-" * 70)
        print(result['preview'])
    
    print("\n" + "=" * 70)
    print("RAG Example completed successfully!")
    print("=" * 70)
    print("\nNote: This is a simplified RAG demonstration.")
    print("Production RAG systems would use:")
    print("  - Vector embeddings (e.g., sentence-transformers)")
    print("  - Vector databases (e.g., FAISS, Chroma)")
    print("  - LLM for generation (e.g., vLLM, Ollama)")
    print("=" * 70)

# Made with Bob
