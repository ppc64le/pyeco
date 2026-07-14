## Purpose: Demonstrates core Docling PDF document-conversion using the IBM Granite Docling model loaded **locally via the `transformers` library** — mirroring the Granite-with-pytorch example pattern.

### Model used:
- **ibm-granite/granite-docling-258M**
- Backend: `transformers` (`AutoModelForImageTextToText`) via Docling's `InlineVlmOptions`
- No Ollama server required — model weights are loaded directly into Python, just like `AutoModelForCausalLM.from_pretrained(...)` in the Granite-with-pytorch example

### Packages used:
- docling==2.74.0
- docling-parse==5.3.2
- torch==2.9.1
- torchvision==0.24.1
- transformers==4.57.1

### Python Version:
- Python 3.12

### Main Example File: `docling_example.py`

This file contains four functions that together demonstrate the full Docling VLM PDF-conversion pipeline:

#### `get_vlm_options()`
Builds and returns an `InlineVlmOptions` object that loads `ibm-granite/granite-docling-258M`
locally using the `transformers` framework (`AUTOMODEL_IMAGETEXTTOTEXT`), with:
- `torch_dtype="bfloat16"` — matches the `dtype=torch.bfloat16` pattern from the pytorch example
- `response_format=DOCTAGS` — the structured markup format that Granite Docling produces
- `inference_framework=InferenceFramework.TRANSFORMERS` — no external server needed

#### `get_doc_converter()`
Builds a fully-configured `DocumentConverter` for PDF input with:
- **`VlmPipelineOptions`** wired to the inline Granite Docling model via `get_vlm_options()`.
- **Page image generation** enabled — required by the VLM pipeline.
- No separate OCR, layout analysis, or table-structure models; the VLM handles everything from page renders.

#### `create_sample_pdf(path)`
Creates a sample PDF with RAG-relevant content at the given path using `reportlab`. Falls back to a minimal raw-bytes PDF if `reportlab` is not available. Skips creation silently if the file already exists.

#### `convert_doc(path)`
Accepts a filesystem path to a PDF file, invokes the converter, and returns the `ConversionResult`.

### How to run the example:
```bash
chmod +x install_test_example.sh
./install_test_example.sh
```

> **Note:** A sample PDF (`sample.pdf`) is automatically generated in the working directory on first run — no manual file setup is required. Model weights are downloaded automatically from HuggingFace on first run and cached locally (same behaviour as the Granite-with-pytorch example).

### How to run only the tests:
```bash
python3.12 sub-test1.py
```

### License:
It's covered under Apache 2.0 licenses
