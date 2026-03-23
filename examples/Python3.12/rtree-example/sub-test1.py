# sub-test1.py
# Intersection → objects → delete → count → invalid-bounds errors → optional get_size
from rtree import index
import ctypes
from rtree.exceptions import RTreeError


def main():
    print("=== sub-test1: intersection + objects + delete + count + errors ===\n")

    rects = {
        10: (0.0, 0.0, 2.0, 2.0),
        11: (1.0, 1.0, 3.0, 3.0),
        12: (5.0, 5.0, 6.0, 6.0),
    }
    idx = index.Index()
    for rid, bbox in rects.items():
        idx.add(rid, bbox)

    q = (0.5, 0.5, 2.5, 2.5)
    ids_before = sorted(idx.intersection(q))
    count_before = idx.count(q)

    print("[before] query bbox:", q)
    print("[before] ids:", ids_before)
    print("[before] count:", count_before)
    if hasattr(idx, "get_size"):
        try:
            print("[before] get_size (deprecated):", idx.get_size())
        except Exception as e:
            print("[before] get_size raised:", type(e).__name__, str(e))
    print()

    # Insert an object payload and query with objects=True
    idx.insert(4321, (1.5, 1.5, 2.0, 2.0), obj={"tag": "X"})
    with_obj = list(idx.intersection(q, objects=True))
    obj_map = {h.id: h.object for h in with_obj if h.id == 4321}

    print("[objects] ids with objects=True:", sorted(h.id for h in with_obj))
    print("[objects] payload for 4321:", obj_map.get(4321))
    print()

    # Delete one and recheck
    idx.delete(11, rects[11])
    ids_after = sorted(idx.intersection(q))
    count_after = idx.count(q)

    print("[after] ids:", ids_after)
    print("[after] count:", count_after)
    print()

    # ----- Errors (exact messages you requested) -----
    bad_bbox = (0.0, 0.0, -1.0, 1.0)  # minx > maxx

    # add invalid bbox
    try:
        idx.add(None, bad_bbox)
    except RTreeError:
        print("[errors] add invalid bbox -> RTreeError")

    # intersection invalid bbox
    try:
        list(idx.intersection(bad_bbox))
    except RTreeError:
        print("[errors] intersection invalid bbox -> RTreeError")

    # wrong-arity tuple
    try:
        idx.add(None, (1, 1))
    except ctypes.ArgumentError:
        print("[errors] add wrong-arity -> ArgumentError")


if __name__ == "__main__":
    main()
