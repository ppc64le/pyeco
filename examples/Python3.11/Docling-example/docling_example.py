"""
Docling Package Example - PDF Document Conversion with Granite Docling (local, inline)

This file mirrors the pattern used in the Granite-with-pytorch example:
the model is loaded **locally** using the Hugging Face ``transformers`` library
(AutoModelForImageTextToText + AutoProcessor) — no Ollama server required.

Model:    ibm-granite/granite-docling-258M
Backend:  transformers (InferenceFramework.TRANSFORMERS)
"""

import os
import torch
from docling.datamodel.pipeline_options import VlmPipelineOptions
from docling.datamodel.pipeline_options_vlm_model import (
    InlineVlmOptions,
    InferenceFramework,
    TransformersModelType,
    ResponseFormat,
)

MODEL_REPO_ID = "ibm-granite/granite-docling-258M"


def get_vlm_options() -> InlineVlmOptions:
    """Return inline VLM options to load Granite Docling locally via transformers.

    Mirrors the ``AutoModelForCausalLM.from_pretrained`` pattern used in the
    Granite-with-pytorch example but uses Docling's :class:`InlineVlmOptions`
    wrapper so the VLM pipeline can manage loading, batching, and generation.

    Returns:
        InlineVlmOptions: Ready-to-use inline VLM option object for the pipeline.
    """
    return InlineVlmOptions(
        repo_id=MODEL_REPO_ID,
        prompt="Convert this page to docling.",
        inference_framework=InferenceFramework.TRANSFORMERS,
        transformers_model_type=TransformersModelType.AUTOMODEL_IMAGETEXTTOTEXT,
        response_format=ResponseFormat.DOCTAGS,
        torch_dtype="bfloat16",
        stop_strings=["</doctag>", "<|end_of_text|>"],
        temperature=0.0,
        max_new_tokens=8192,
    )


def get_doc_converter():
    """Build and return a :class:`DocumentConverter` using Granite Docling loaded inline.

    Pipeline:
    - ``VlmPipelineOptions`` with :func:`get_vlm_options` (transformers backend).
    - Page images are generated automatically — required by the VLM pipeline.
    - No separate layout analysis, OCR, or table-structure models are used;
      the VLM understands the document holistically from page renders.

    Returns:
        DocumentConverter: Ready-to-use converter instance.
    """
    from docling.datamodel.base_models import InputFormat
    from docling.document_converter import DocumentConverter, PdfFormatOption
    from docling.pipeline.vlm_pipeline import VlmPipeline

    pipeline_options = VlmPipelineOptions(
        vlm_options=get_vlm_options(),
        generate_page_images=True,
    )

    return DocumentConverter(
        allowed_formats=[InputFormat.PDF],
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_cls=VlmPipeline,
                pipeline_options=pipeline_options,
            )
        },
    )


def create_sample_pdf(path: str = "sample.pdf") -> str | None:
    """Create a sample PDF document with RAG-relevant content at *path*.

    Uses ``reportlab`` when available for rich multi-line content.  Falls back
    to a minimal raw-bytes PDF if ``reportlab`` is not installed.  Skips
    creation if the file already exists.

    Args:
        path (str): Destination file path for the generated PDF.

    Returns:
        str | None: The path that was written, or ``None`` if creation was skipped.
    """
    if os.path.exists(path):
        print(f"PDF already exists at '{path}', skipping creation.")
        return None

    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter

        c = canvas.Canvas(path, pagesize=letter)

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

    except ImportError:
        print("reportlab not available, falling back to minimal PDF.")
        pdf_bytes = (
            b"%PDF-1.4\n"
            b"1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n"
            b"2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj\n"
            b"3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            b"/Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >> endobj\n"
            b"4 0 obj << /Length 44 >>\nstream\n"
            b"BT /F1 12 Tf 100 700 Td (Sample PDF for Docling) Tj ET\n"
            b"endstream\nendobj\n"
            b"5 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj\n"
            b"xref\n0 6\n"
            b"0000000000 65535 f \n"
            b"0000000009 00000 n \n"
            b"0000000058 00000 n \n"
            b"0000000115 00000 n \n"
            b"0000000266 00000 n \n"
            b"0000000360 00000 n \n"
            b"trailer << /Size 6 /Root 1 0 R >>\n"
            b"startxref\n441\n%%EOF\n"
        )
        with open(path, "wb") as f:
            f.write(pdf_bytes)

    print(f"Created sample PDF at '{path}'.")
    return path


def convert_doc(path):
    """Convert a PDF file at *path* and return the ConversionResult.

    Args:
        path (str | Path): Filesystem path to the PDF file.

    Returns:
        ConversionResult: Docling conversion result containing the parsed document.
    """
    doc_converter = get_doc_converter()
    return doc_converter.convert(path)


if __name__ == "__main__":
    print(f"\nModel used: {MODEL_REPO_ID}\n")

    PDF_FILE_PATH = "sample.pdf"
    create_sample_pdf(PDF_FILE_PATH)
    result = convert_doc(PDF_FILE_PATH)
    print(result)
