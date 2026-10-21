import unittest
import importlib.metadata
import numpy as np
from scipy import sparse

import sknetwork
from sknetwork.data import karate_club, from_edge_list
from sknetwork.ranking import PageRank, HITS
from sknetwork.clustering import Louvain
from sknetwork.embedding import Spectral
from sknetwork.topology import Triangles, CoreDecomposition
from sknetwork.linkpred import JaccardIndex


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
        graph = karate_club()
        adjacency = graph.adjacency
        pagerank = PageRank(damping_factor=0.85)
        scores = pagerank.fit_predict(adjacency)

        self.assertEqual(len(scores), 34)
        self.assertTrue(np.all(scores >= 0))
        self.assertAlmostEqual(float(np.sum(scores)), 1.0, places=4)

    def test_hits(self):
        """Compute HITS authority scores on graph adjacency."""
        graph = karate_club()
        adjacency = graph.adjacency
        hits = HITS()
        scores = hits.fit_predict(adjacency)

        self.assertEqual(len(scores), 34)
        self.assertTrue(np.all(scores >= 0))

    def test_louvain_clustering(self):
        """Perform Louvain community detection."""
        graph = karate_club()
        adjacency = graph.adjacency
        louvain = Louvain()
        labels = louvain.fit_predict(adjacency)

        self.assertEqual(len(labels), 34)
        unique_labels = np.unique(labels)
        self.assertGreaterEqual(len(unique_labels), 2)

    def test_spectral_embedding(self):
        """Compute 2D Spectral embedding of nodes."""
        graph = karate_club()
        adjacency = graph.adjacency
        spectral = Spectral(n_components=2)
        embedding = spectral.fit_transform(adjacency)

        self.assertEqual(embedding.shape, (34, 2))
        self.assertFalse(np.isnan(embedding).any())

    def test_topology_triangles(self):
        """Compute triangle counts for graph nodes."""
        graph = karate_club()
        adjacency = graph.adjacency
        triangles = Triangles()
        counts = triangles.fit_transform(adjacency)

        self.assertEqual(len(counts), 34)
        self.assertTrue(np.all(counts >= 0))
        total_triangles = int(np.sum(counts) / 3)
        self.assertGreater(total_triangles, 0)

    def test_topology_core_decomposition(self):
        """Compute core decomposition."""
        graph = karate_club()
        adjacency = graph.adjacency
        core = CoreDecomposition()
        core_values = core.fit_transform(adjacency)

        self.assertEqual(len(core_values), 34)
        self.assertTrue(np.all(core_values >= 0))

    def test_link_prediction_jaccard(self):
        """Predict link scores using Jaccard Index."""
        graph = karate_club()
        adjacency = graph.adjacency
        jaccard = JaccardIndex()
        jaccard.fit(adjacency)

        test_pairs = [(0, 1), (0, 33)]
        scores = jaccard.predict(test_pairs)
        self.assertEqual(len(scores), 2)
        self.assertTrue(all(0.0 <= s <= 1.0 for s in scores))

    def test_custom_graph_from_edge_list(self):
        """Construct custom graph from edge list and verify adjacency."""
        edges = [(0, 1), (1, 2), (2, 0)]
        graph = from_edge_list(edges, directed=False)
        self.assertEqual(graph.adjacency.shape, (3, 3))
        self.assertEqual(graph.adjacency.nnz, 6)


if __name__ == "__main__":
    unittest.main()
