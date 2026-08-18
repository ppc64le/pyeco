## Purpose: Demonstrates SIMD-accelerated similarity and distance calculations using the simsimd library.

### Packages used:
simsimd
numpy

### Functionality:

- Computes cosine distance between float32 vectors (identical, orthogonal, and arbitrary pairs).
- Computes squared Euclidean (L2) distance between vectors.
- Computes inner product distance for unit vectors.
- Runs batch pairwise distance computation (cdist) between a query vector and a set of candidate vectors, as used in vector search workloads.
- Computes Hamming distance between binary uint8 arrays.

### How to run the example :
```
chmod +x install_test_example.sh
./install_test_example.sh
```

### License:
It's covered under Apache 2.0 licenses
