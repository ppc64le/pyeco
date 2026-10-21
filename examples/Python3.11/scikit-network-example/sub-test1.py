import unittest
import importlib.metadata
import numpy as np
from scipy import sparse

import sknetwork
from sknetwork.data import karate_club, from_edge_list
from sknetwork.ranking import PageRank, HITS
from sknetwork.clustering import Louvain
from sknetwork.embedding import Spectral
from sknetwork.topology import count_triangles, get_core_decomposition
from sknetwork.linkpred import NNLinker


class TestScikitNetworkLibrary(unittest.TestCase):

    def test_scikit_network_import(self):
        """Check that sknetwork can be imported."""
        try:
            import sknetwork  # noqa: F401
        except ImportError:
            self.fail("scikit-network is not installed")

    def test_scikit_network_version(self):
        """Verify scikit-network version."""
        version = importlib.metadata.version("scikit-network")
        self.assertIn("0.33.5", version, f"'0.33.5' not found in version string: {version}")

    def test_karate_club_dataset(self):
        """Load Zachary's karate club dataset and check structure."""
        graph = karate_club(metadata=True)
        self.assertIsNotNone(graph.adjacency)
        self.assertEqual(graph.adjacency.shape, (34, 34))
        self.assertTrue(sparse.issparse(graph.adjacency))
        self.assertEqual(len(graph.labels), 34)

    def test_pagerank(self):
        """Compute PageRank scores on graph adjacency."""
        adjacency = karate_club()
        pagerank = PageRank(damping_factor=0.85)
        scores = pagerank.fit_predict(adjacency)

        self.assertEqual(len(scores), 34)
        self.assertTrue(np.all(scores >= 0))
        self.assertAlmostEqual(float(np.sum(scores)), 1.0, places=4)

    def test_hits(self):
        """Compute HITS authority scores on graph adjacency."""
        adjacency = karate_club()
        hits = HITS()
        scores = hits.fit_predict(adjacency)

        self.assertEqual(len(scores), 34)
        self.assertTrue(np.all(scores >= 0))

    def test_louvain_clustering(self):
        """Perform Louvain community detection."""
        adjacency = karate_club()
        louvain = Louvain()
        labels = louvain.fit_predict(adjacency)

        self.assertEqual(len(labels), 34)
        unique_labels = np.unique(labels)
        self.assertGreaterEqual(len(unique_labels), 2)

    def test_spectral_embedding(self):
        """Compute 2D Spectral embedding of nodes."""
        adjacency = karate_club()
        spectral = Spectral(n_components=2)
        embedding = spectral.fit_transform(adjacency)

        self.assertEqual(embedding.shape, (34, 2))
        self.assertFalse(np.isnan(embedding).any())

    def test_topology_triangles(self):
        """Count triangles in the graph."""
        adjacency = karate_club()
        total_triangles = count_triangles(adjacency)

        self.assertEqual(total_triangles, 45)

    def test_topology_core_decomposition(self):
        """Compute core decomposition."""
        adjacency = karate_club()
        core_values = get_core_decomposition(adjacency)

        self.assertEqual(len(core_values), 34)
        self.assertTrue(np.all(core_values >= 0))

    def test_link_prediction_nn(self):
        """Predict links using nearest neighbors in embedding space."""
        adjacency = karate_club()
        linker = NNLinker(n_neighbors=5, threshold=0.5)
        links = linker.fit_predict(adjacency)

        self.assertEqual(links.shape, (34, 34))
        self.assertTrue(sparse.issparse(links))
        self.assertTrue(np.all(links.data >= 0.5))

    def test_custom_graph_from_edge_list(self):
        """Construct custom graph from edge list and verify adjacency."""
        edges = [(0, 1), (1, 2), (2, 0)]
        graph = from_edge_list(edges, directed=False, matrix_only=False)
        self.assertEqual(graph.adjacency.shape, (3, 3))
        self.assertEqual(graph.adjacency.nnz, 6)


if __name__ == "__main__":
    unittest.main()
