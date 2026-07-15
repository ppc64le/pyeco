import unittest
import importlib.metadata


class TestDoclingExample(unittest.TestCase):
    """Unit tests for the docling_example module."""

    # ------------------------------------------------------------------
    # Package presence / version
    # ------------------------------------------------------------------

    def test_docling_import(self):
        """Verify that the docling package can be imported."""
        try:
            import docling  # noqa: F401
        except ImportError:
            self.fail("docling is not installed")

    def test_docling_version(self):
        """Verify the installed docling package has a valid version string."""
        version = importlib.metadata.version("docling")
        self.assertIsNotNone(version)
        self.assertGreater(len(version), 0)
        print(f"Docling version: {version}")

    # ------------------------------------------------------------------
    # Module-level function imports
    # ------------------------------------------------------------------

    def test_get_vlm_options_importable(self):
        """Verify get_vlm_options can be imported from docling_example."""
        try:
            from docling_example import get_vlm_options
            self.assertIsNotNone(get_vlm_options)
        except ImportError as e:
            self.fail(f"Failed to import get_vlm_options: {e}")

    def test_get_doc_converter_importable(self):
        """Verify get_doc_converter can be imported from docling_example."""
        try:
            from docling_example import get_doc_converter
            self.assertIsNotNone(get_doc_converter)
        except ImportError as e:
            self.fail(f"Failed to import get_doc_converter: {e}")

    def test_convert_doc_importable(self):
        """Verify convert_doc can be imported from docling_example."""
        try:
            from docling_example import convert_doc
            self.assertIsNotNone(convert_doc)
        except ImportError as e:
            self.fail(f"Failed to import convert_doc: {e}")

    def test_create_sample_pdf_importable(self):
        """Verify create_sample_pdf can be imported from docling_example."""
        try:
            from docling_example import create_sample_pdf
            self.assertIsNotNone(create_sample_pdf)
        except ImportError as e:
            self.fail(f"Failed to import create_sample_pdf: {e}")

    # ------------------------------------------------------------------
    # VLM options construction (inline / transformers)
    # ------------------------------------------------------------------

    def test_get_vlm_options_returns_inline_vlm_options(self):
        """Verify get_vlm_options returns an InlineVlmOptions instance."""
        from docling.datamodel.pipeline_options_vlm_model import InlineVlmOptions
        from docling_example import get_vlm_options

        opts = get_vlm_options()
        self.assertIsNotNone(opts)
        self.assertIsInstance(opts, InlineVlmOptions)

    def test_vlm_options_model_repo_id(self):
        """Verify the Granite Docling model repo_id is set correctly."""
        from docling_example import get_vlm_options, MODEL_REPO_ID

        opts = get_vlm_options()
        self.assertEqual(opts.repo_id, MODEL_REPO_ID)

    def test_vlm_options_inference_framework_transformers(self):
        """Verify the inference framework is set to TRANSFORMERS."""
        from docling.datamodel.pipeline_options_vlm_model import InferenceFramework
        from docling_example import get_vlm_options

        opts = get_vlm_options()
        self.assertEqual(opts.inference_framework, InferenceFramework.TRANSFORMERS)

    def test_vlm_options_model_type_imagetexttotext(self):
        """Verify the transformers model type is AUTOMODEL_IMAGETEXTTOTEXT."""
        from docling.datamodel.pipeline_options_vlm_model import TransformersModelType
        from docling_example import get_vlm_options

        opts = get_vlm_options()
        self.assertEqual(
            opts.transformers_model_type,
            TransformersModelType.AUTOMODEL_IMAGETEXTTOTEXT,
        )

    def test_vlm_options_response_format_doctags(self):
        """Verify response_format is DOCTAGS (required by Granite Docling)."""
        from docling.datamodel.pipeline_options_vlm_model import ResponseFormat
        from docling_example import get_vlm_options

        opts = get_vlm_options()
        self.assertEqual(opts.response_format, ResponseFormat.DOCTAGS)

    # ------------------------------------------------------------------
    # DocumentConverter construction
    # ------------------------------------------------------------------

    def test_get_doc_converter_returns_instance(self):
        """Verify get_doc_converter returns a DocumentConverter instance."""
        from docling.document_converter import DocumentConverter
        from docling_example import get_doc_converter

        converter = get_doc_converter()
        self.assertIsNotNone(converter)
        self.assertIsInstance(converter, DocumentConverter)

    def test_doc_converter_accepts_pdf_format(self):
        """Verify the returned converter has PDF in its allowed formats."""
        from docling.datamodel.base_models import InputFormat
        from docling_example import get_doc_converter

        converter = get_doc_converter()
        self.assertIn(InputFormat.PDF, converter.allowed_formats)

    # ------------------------------------------------------------------
    # Docling core imports (pipeline options, input formats)
    # ------------------------------------------------------------------

    def test_vlm_pipeline_options_importable(self):
        """Verify VlmPipelineOptions is importable from docling."""
        try:
            from docling.datamodel.pipeline_options import VlmPipelineOptions  # noqa: F401
        except ImportError as e:
            self.fail(f"VlmPipelineOptions import failed: {e}")

    def test_inline_vlm_options_importable(self):
        """Verify InlineVlmOptions is importable from docling."""
        try:
            from docling.datamodel.pipeline_options_vlm_model import InlineVlmOptions  # noqa: F401
        except ImportError as e:
            self.fail(f"InlineVlmOptions import failed: {e}")

    def test_input_format_pdf_available(self):
        """Verify InputFormat.PDF is accessible."""
        from docling.datamodel.base_models import InputFormat
        self.assertTrue(hasattr(InputFormat, "PDF"))

    # ------------------------------------------------------------------
    # create_sample_pdf helper
    # ------------------------------------------------------------------

    def test_create_sample_pdf_skips_existing_file(self):
        """Verify create_sample_pdf returns None when the file already exists."""
        import tempfile, os
        from docling_example import create_sample_pdf

        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp_path = tmp.name
        try:
            result = create_sample_pdf(tmp_path)
            self.assertIsNone(result)
        finally:
            os.unlink(tmp_path)

    def test_create_sample_pdf_creates_file(self):
        """Verify create_sample_pdf creates a PDF file and returns its path."""
        import tempfile, os
        from docling_example import create_sample_pdf

        tmp_path = tempfile.mktemp(suffix=".pdf")
        try:
            result = create_sample_pdf(tmp_path)
            self.assertEqual(result, tmp_path)
            self.assertTrue(os.path.exists(tmp_path))
            self.assertGreater(os.path.getsize(tmp_path), 0)
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)


if __name__ == "__main__":
    unittest.main()
