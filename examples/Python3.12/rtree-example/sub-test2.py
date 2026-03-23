# sub-test2.py
# KNN (nearest) + ties + objects=True + duplicate-id behavior
from rtree import index


def main():
    print("=== sub-test2: nearest (KNN), ties, objects, duplicates ===\n")

    # Points as zero-area boxes
    pts = {
        1: (0.0, 0.0, 0.0, 0.0),
        2: (2.0, 2.0, 2.0, 2.0),
        3: (-1.0, 1.0, -1.0, 1.0),
        4: (5.0, 1.0, 5.0, 1.0),
        5: (1.0, -3.0, 1.0, -3.0),
    }
    idx = index.Index()
    for pid, bbox in pts.items():
        idx.add(pid, bbox)

    q = (1.0, 1.0, 1.0, 1.0)
    k = 3
    ids = list(idx.nearest(q, k))
    print("[knn] query:", q)
    print("[knn] k:", k)
    print("[knn] nearest ids:", ids)
    print()

    # Ties: concentric boxes around origin
    small_box = (-10, -10, 10, 10)
    large_box = (-50, -50, 50, 50)
    idx2 = index.Index()
    idx2.insert(0, small_box)
    idx2.insert(1, large_box)
    point = (0, 0)

    res_2 = list(idx2.nearest(point, 2))
    res_1 = list(idx2.nearest(point, 1))
    print("[ties] nearest(2) @ origin:", res_2)
    print("[ties] nearest(1) @ origin:", res_1)
    print()

    # Objects=True with equal distance
    idx3 = index.Index()
    idx3.add(0, (14, 10, 14, 10), obj={"a": 42})
    idx3.add(1, (16, 10, 16, 10), obj={"a": 42})
    hits = sorted(
        (i.id, i.object) for i in idx3.nearest((15, 10, 15, 10), 1, objects=True)
    )
    print("[objects] eq-distance nearest around x=15:", hits)
    print()

    # Duplicate insertion of same ID: expect both entries to be returned
    dup = index.Index()
    dup.add(1, (2, 2))
    dup.add(1, (3, 3))
    dup_hits = list(dup.intersection((0, 0, 5, 5)))
    print("[duplicates] query (0,0,5,5) ids:", dup_hits)


if __name__ == "__main__":
    main()
