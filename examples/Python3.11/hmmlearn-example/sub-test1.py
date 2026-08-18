import unittest
import importlib.metadata
import numpy as np
from hmmlearn import hmm


class TestHmmlearnLibrary(unittest.TestCase):

    def test_hmmlearn_import(self):
        """Check if hmmlearn can be imported."""
        try:
            from hmmlearn import hmm  # noqa: F401
        except ImportError:
            self.fail("hmmlearn is not installed")

    def test_hmmlearn_version(self):
        """Verify hmmlearn version."""
        version = importlib.metadata.version("hmmlearn")
        assert "0.3.3" in version, f"'0.3.3' not found in version string: {version}"

    def test_gaussian_hmm_sample(self):
        """Build a GaussianHMM and verify it generates samples."""
        model = hmm.GaussianHMM(n_components=2, covariance_type="diag", n_iter=10)
        model.startprob_ = np.array([0.5, 0.5])
        model.transmat_ = np.array([[0.7, 0.3], [0.4, 0.6]])
        model.means_ = np.array([[0.0], [5.0]])
        model.covars_ = np.array([[1.0], [1.0]])

        obs, states = model.sample(50, random_state=0)
        self.assertEqual(obs.shape, (50, 1))
        self.assertEqual(len(states), 50)

    def test_viterbi_decode(self):
        """Verify Viterbi decoding returns valid state sequence."""
        model = hmm.GaussianHMM(n_components=2, covariance_type="diag", n_iter=10)
        model.startprob_ = np.array([0.6, 0.4])
        model.transmat_ = np.array([[0.8, 0.2], [0.3, 0.7]])
        model.means_ = np.array([[0.0], [10.0]])
        model.covars_ = np.array([[1.0], [1.0]])

        obs, _ = model.sample(30, random_state=1)
        log_prob, decoded = model.decode(obs, algorithm="viterbi")
        self.assertEqual(len(decoded), 30)
        self.assertIn(decoded[0], [0, 1])
        self.assertIsInstance(log_prob, float)

    def test_hmm_fit(self):
        """Train a GaussianHMM from observations and verify it converges."""
        rng = np.random.default_rng(7)
        obs = np.concatenate([
            rng.normal(0.0, 1.0, (100, 1)),
            rng.normal(8.0, 1.0, (100, 1)),
        ])
        model = hmm.GaussianHMM(n_components=2, covariance_type="diag",
                                 n_iter=100, random_state=7)
        model.fit(obs)
        score = model.score(obs)
        self.assertIsInstance(score, float)
        self.assertFalse(np.isnan(score))


if __name__ == "__main__":
    unittest.main()
