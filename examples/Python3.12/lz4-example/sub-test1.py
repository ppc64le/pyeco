import unittest
import importlib.metadata
import lz4.frame
import lz4.block


SAMPLE_DATA = b"Hello LZ4! " * 10000


class TestLz4Library(unittest.TestCase):

    def test_lz4_import(self):
        """Check that lz4 can be imported."""
        try:
            import lz4.frame  # noqa: F401
            import lz4.block  # noqa: F401
        except ImportError:
            self.fail("lz4 is not installed")

    def test_lz4_version(self):
        """Verify lz4 version."""
        version = importlib.metadata.version("lz4")
        assert "4.4.5" in version, f"'4.4.5' not found in version string: {version}"

    def test_frame_compress_reduces_size(self):
        """Compressed data should be smaller than the original for repetitive input."""
        compressed = lz4.frame.compress(SAMPLE_DATA)
        self.assertLess(len(compressed), len(SAMPLE_DATA))

    def test_frame_roundtrip(self):
        """Frame compression then decompression should recover original data."""
        compressed = lz4.frame.compress(SAMPLE_DATA)
        decompressed = lz4.frame.decompress(compressed)
        self.assertEqual(decompressed, SAMPLE_DATA)

    def test_block_roundtrip(self):
        """Block compression then decompression should recover original data."""
        compressed = lz4.block.compress(SAMPLE_DATA, store_size=False)
        decompressed = lz4.block.decompress(compressed, uncompressed_size=len(SAMPLE_DATA))
        self.assertEqual(decompressed, SAMPLE_DATA)

    def test_frame_compression_level_0(self):
        """Level 0 (fast) compression should still be decompressible."""
        compressed = lz4.frame.compress(SAMPLE_DATA, compression_level=0)
        decompressed = lz4.frame.decompress(compressed)
        self.assertEqual(decompressed, SAMPLE_DATA)

    def test_frame_compression_level_high(self):
        """High-compression level (9) should produce smaller output than level 0."""
        c0 = lz4.frame.compress(SAMPLE_DATA, compression_level=0)
        c9 = lz4.frame.compress(SAMPLE_DATA, compression_level=9)
        self.assertLessEqual(len(c9), len(c0))

    def test_empty_data_roundtrip(self):
        """Empty bytes should compress and decompress cleanly."""
        compressed = lz4.frame.compress(b"")
        decompressed = lz4.frame.decompress(compressed)
        self.assertEqual(decompressed, b"")

    def test_binary_data_roundtrip(self):
        """Binary data (bytes 0-255) should survive frame compression."""
        binary = bytes(range(256)) * 100
        compressed = lz4.frame.compress(binary)
        decompressed = lz4.frame.decompress(compressed)
        self.assertEqual(decompressed, binary)


if __name__ == "__main__":
    unittest.main()
