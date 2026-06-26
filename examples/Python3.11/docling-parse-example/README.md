## Purpose: Simple RAG (Retrieval-Augmented Generation) Application with Docling-Parse

### Packages used:
- docling-parse (PDF parsing)
- reportlab (PDF creation for testing)
- Pillow (Image processing support)
- numpy (Numerical operations)

### Functionality:
This example demonstrates a simplified RAG (Retrieval-Augmented Generation) pipeline:

1. **Document Parsing**: Uses docling-parse v2 to extract text from PDF documents
2. **Text Chunking**: Splits extracted text into manageable chunks for retrieval
3. **Keyword-based Retrieval**: Implements simple keyword matching to find relevant chunks
4. **Result Display**: Shows top matching chunks based on query

### RAG Pipeline Steps:
1. Parse PDF document with docling-parse
2. Extract text content from parsed document
3. Create document chunks (configurable size)
4. Perform keyword-based retrieval on chunks
5. Display top relevant results

### Note:
This is a simplified RAG demonstration. Production RAG systems typically use:
- Vector embeddings (e.g., sentence-transformers, OpenAI embeddings)
- Vector databases (e.g., FAISS, Chroma, Pinecone)
- LLM for generation (e.g., vLLM, Ollama, OpenAI GPT)

### How to run the example:
```bash
chmod +x install_test_example.sh
./install_test_example.sh
```

Or manually:
```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install --extra-index-url https://wheels.developerfirst.ibm.com/ppc64le/linux-v2026.06.0 -r requirements.txt
python3.12 docling_parse_example.py [optional_pdf_path]
```

### License:
It's covered under Apache 2.0 licenses
