import unittest
import importlib.metadata
import numpy as np
import simsimd


class TestSimsimdLibrary(unittest.TestCase):

    def test_simsimd_import(self):
        """Check that simsimd can be imported."""
        try:
            import simsimd  # noqa: F401
        except ImportError:
            self.fail("simsimd is not installed")

    def test_simsimd_version(self):
        """Verify simsimd version contains expected major.minor."""
        version = importlib.metadata.version("simsimd")
        assert "6.5.16" in version, f"'6.5.16' not found in version string: {version}"

    def test_cosine_identical_vectors(self):
        """Cosine distance between identical vectors should be 0."""
        a = np.array([1.0, 2.0, 3.0], dtype=np.float32)
        dist = simsimd.cosine(a, a)
        self.assertAlmostEqual(float(dist), 0.0, places=5)

    def test_cosine_orthogonal_vectors(self):
        """Cosine distance between orthogonal unit vectors should be 1."""
        a = np.array([1.0, 0.0, 0.0], dtype=np.float32)
        b = np.array([0.0, 1.0, 0.0], dtype=np.float32)
        dist = simsimd.cosine(a, b)
        self.assertAlmostEqual(float(dist), 1.0, places=5)

    def test_sqeuclidean_known_result(self):
        """Squared Euclidean distance: (0,0,0) vs (1,2,2) should be 9."""
        a = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        b = np.array([1.0, 2.0, 2.0], dtype=np.float32)
        dist = simsimd.sqeuclidean(a, b)
        self.assertAlmostEqual(float(dist), 9.0, places=4)

    def test_dot_orthogonal(self):
        """Inner product distance between orthogonal unit vectors should be 1."""
        a = np.array([1.0, 0.0], dtype=np.float32)
        b = np.array([0.0, 1.0], dtype=np.float32)
        dist = simsimd.dot(a, b)
        self.assertAlmostEqual(float(dist), 1.0, places=5)

    def test_cdist_shape(self):
        """cdist returns the correct shape for pairwise distances."""
        rng = np.random.default_rng(0)
        A = rng.random((3, 16)).astype(np.float32)
        B = rng.random((5, 16)).astype(np.float32)
        result = simsimd.cdist(A, B, metric="cosine")
        self.assertEqual(result.shape, (3, 5))

    def test_hamming_distance(self):
        """Hamming distance between fully flipped bytes should equal number of bits."""
        a = np.array([0b11111111], dtype=np.uint8)
        b = np.array([0b00000000], dtype=np.uint8)
        dist = simsimd.hamming(a, b)
        self.assertEqual(int(dist), 8)


if __name__ == "__main__":
    unittest.main()
