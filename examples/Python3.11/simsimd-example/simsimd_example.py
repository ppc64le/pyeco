import numpy as np
import simsimd


def demo_cosine_similarity():
    """
    Compute cosine similarity between two float32 vectors.
    Cosine similarity measures the angle between two vectors (1.0 = identical direction).
    """
    a = np.array([1.0, 2.0, 3.0, 4.0], dtype=np.float32)
    b = np.array([4.0, 3.0, 2.0, 1.0], dtype=np.float32)

    cos_sim = simsimd.cosine(a, b)
    print(f"Vector A: {a.tolist()}")
    print(f"Vector B: {b.tolist()}")
    print(f"Cosine distance:    {cos_sim:.6f}")
    print(f"Cosine similarity:  {1.0 - cos_sim:.6f}")


def demo_euclidean_distance():
    """
    Compute squared Euclidean (L2) distance between two float32 vectors.
    """
    a = np.array([0.0, 0.0, 0.0], dtype=np.float32)
    b = np.array([1.0, 2.0, 2.0], dtype=np.float32)

    dist = simsimd.sqeuclidean(a, b)
    print(f"\nVector A: {a.tolist()}")
    print(f"Vector B: {b.tolist()}")
    print(f"Squared Euclidean distance: {dist:.6f}  (expected 9.0)")


def demo_inner_product():
    """
    Compute the raw dot (inner) product between two unit vectors.
    """
    a = np.array([1.0, 0.0, 0.0], dtype=np.float32)
    b = np.array([0.0, 1.0, 0.0], dtype=np.float32)

    dot_product = simsimd.dot(a, b)
    print(f"\nUnit vector A: {a.tolist()}")
    print(f"Unit vector B: {b.tolist()}")
    print(f"Dot product: {dot_product:.6f}  (expected 0.0 for orthogonal)")


def demo_batch_distances():
    """
    Compute distances from one query vector against a batch of database vectors.
    Demonstrates the cdist / pairwise use-case common in vector search.
    """
    rng = np.random.default_rng(42)
    query = rng.random(128).astype(np.float32)
    # Normalise query to unit length
    query /= np.linalg.norm(query)

    # 5 candidate vectors, also normalised
    candidates = rng.random((5, 128)).astype(np.float32)
    candidates /= np.linalg.norm(candidates, axis=1, keepdims=True)

    distances = np.array(simsimd.cdist(query[np.newaxis, :], candidates, metric="cosine"))
    print("\nBatch cosine distances (query vs 5 candidates):")
    for i, d in enumerate(distances[0]):
        print(f"  candidate[{i}]: {d:.6f}")


def demo_hamming_distance():
    """
    Compute Hamming distance between two binary (uint8) byte arrays.
    The `dtype="b8"` override tells simsimd to treat each byte as 8 packed bits.
    """
    a = np.array([0b10101010, 0b11001100, 0b11110000], dtype=np.uint8)
    b = np.array([0b01010101, 0b00110011, 0b00001111], dtype=np.uint8)

    ham = simsimd.hamming(a, b, dtype="b8")
    print(f"\nBinary array A: {[bin(x) for x in a]}")
    print(f"Binary array B: {[bin(x) for x in b]}")
    print(f"Hamming distance: {ham}")


if __name__ == "__main__":
    print("=== SimSIMD Example: SIMD-Accelerated Similarity & Distance ===\n")

    print("--- 1. Cosine Similarity ---")
    demo_cosine_similarity()

    print("\n--- 2. Squared Euclidean Distance ---")
    demo_euclidean_distance()

    print("\n--- 3. Inner Product Distance ---")
    demo_inner_product()

    print("\n--- 4. Batch Distances (cdist) ---")
    demo_batch_distances()

    print("\n--- 5. Hamming Distance ---")
    demo_hamming_distance()

    print("\nSimSIMD example completed successfully.")
