"""
scikit-network example: Demonstrating graph analytics with sknetwork.
Covers dataset loading, PageRank, HITS ranking, Louvain clustering,
Spectral embedding, topology metrics (triangles & core decomposition),
and link prediction (nearest neighbors in embedding space).
"""

import numpy as np
from sknetwork.data import karate_club, from_edge_list
from sknetwork.ranking import PageRank, HITS
from sknetwork.clustering import Louvain
from sknetwork.embedding import Spectral
from sknetwork.topology import count_triangles, get_core_decomposition
from sknetwork.linkpred import NNLinker


def demo_karate_club():
    """Load and inspect Zachary's Karate Club benchmark graph."""
    print("--- 1. Zachary's Karate Club Dataset ---")
    graph = karate_club(metadata=True)
    adjacency = graph.adjacency
    labels = graph.labels

    print(f"Number of nodes: {adjacency.shape[0]}")
    print(f"Number of edges: {adjacency.nnz // 2}")
    print(f"Ground-truth club affiliations: {labels[:10]}...")
    return graph


def demo_ranking(adjacency):
    """Compute node centrality using PageRank and HITS."""
    print("\n--- 2. Node Ranking & Centrality ---")

    # PageRank
    pagerank = PageRank(damping_factor=0.85)
    pr_scores = pagerank.fit_predict(adjacency)
    top_pr_nodes = np.argsort(pr_scores)[::-1][:5]
    print(f"Top 5 nodes by PageRank: {top_pr_nodes}")
    print(f"Top 5 PageRank scores: {np.round(pr_scores[top_pr_nodes], 4)}")

    # HITS (Hubs and Authorities)
    hits = HITS()
    hits.fit(adjacency)
    top_auth_nodes = np.argsort(hits.scores_)[::-1][:5]
    print(f"Top 5 nodes by HITS authority: {top_auth_nodes}")


def demo_clustering(adjacency):
    """Detect communities using the Louvain algorithm."""
    print("\n--- 3. Community Detection (Louvain) ---")
    louvain = Louvain()
    labels = louvain.fit_predict(adjacency)
    unique_clusters, counts = np.unique(labels, return_counts=True)
    print(f"Number of detected communities: {len(unique_clusters)}")
    for cluster_id, count in zip(unique_clusters, counts):
        print(f"  Community {cluster_id}: {count} members")


def demo_embedding(adjacency):
    """Generate 2D node representations using Spectral Embedding."""
    print("\n--- 4. Node Embedding (Spectral) ---")
    spectral = Spectral(n_components=2)
    embedding = spectral.fit_transform(adjacency)
    print(f"Embedding shape: {embedding.shape}")
    print(f"Sample 2D embedding (node 0): {np.round(embedding[0], 4)}")
    print(f"Sample 2D embedding (node 33): {np.round(embedding[33], 4)}")


def demo_topology(adjacency):
    """Analyze graph topological structure."""
    print("\n--- 5. Graph Topology (Triangles & Core Decomposition) ---")
    total_triangles = count_triangles(adjacency)
    print(f"Total number of triangles in graph: {total_triangles}")

    core_values = get_core_decomposition(adjacency)
    print(f"Max coreness (k-core): {np.max(core_values)}")
    print(f"Node coreness values: {core_values[:10]}...")


def demo_link_prediction(adjacency):
    """Predict link formation using nearest neighbors (cosine similarity)."""
    print("\n--- 6. Link Prediction (NNLinker) ---")
    linker = NNLinker(n_neighbors=5, threshold=0.5)
    links = linker.fit_predict(adjacency)
    print(f"Predicted links matrix shape: {links.shape}")

    test_pairs = [(0, 1), (0, 2), (0, 33), (32, 33)]
    for i, j in test_pairs:
        print(f"  Link score between node {i} and node {j}: {links[i, j]:.4f}")


def demo_custom_graph():
    """Create and analyze a custom graph from an edge list."""
    print("\n--- 7. Custom Graph from Edge List ---")
    edges = [
        (0, 1), (1, 2), (2, 0),
        (2, 3),
        (3, 4), (4, 5), (5, 3)
    ]
    graph = from_edge_list(edges, directed=False, matrix_only=False)
    adjacency = graph.adjacency
    print(f"Custom graph nodes: {adjacency.shape[0]}, edges: {len(edges)}")

    louvain = Louvain()
    labels = louvain.fit_predict(adjacency)
    print(f"Community labels for barbell-like graph: {labels}")


if __name__ == "__main__":
    print("=== scikit-network Example: Graph Analytics & Algorithms ===")
    graph = demo_karate_club()
    adj = graph.adjacency
    demo_ranking(adj)
    demo_clustering(adj)
    demo_embedding(adj)
    demo_topology(adj)
    demo_link_prediction(adj)
    demo_custom_graph()
    print("\nscikit-network example completed successfully.")
