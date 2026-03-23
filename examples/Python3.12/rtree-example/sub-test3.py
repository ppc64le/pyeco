# sub-test3.py
# Union (&) / Intersection (|) of indices (same interleaving)
# + properties round-trip (safe near_minimum_overlap_factor)
# + vectorized APIs (intersection_v / nearest_v) guarded

from rtree import index, core


def main():
    print("=== sub-test3: union/intersection + properties + vectorized APIs ===\n")

    # Build two indices with the same interleaving (required for & and |)
    a = index.Index(interleaved=True)
    a.insert(1, (3, 3, 5, 5), "a_1")
    a.insert(2, (4, 2, 6, 4), "a_2")

    b = index.Index(interleaved=True)
    b.insert(3, (2, 1, 7, 6), "b_3")
    b.insert(4, (8, 7, 9, 8), "b_4")

    # Intersection (&): only overlapping regions, paired objects
    c_int = a & b
    objs_int = [(h.bbox, h.object) for h in c_int.intersection(c_int.bounds, objects=True)]
    print("[&] interleaved:", c_int.interleaved)
    print("[&] len:", len(c_int))
    print("[&] items (bbox, object):", objs_int)
    print()

    # Union (|): all items from both
    c_union = a | b
    objs_union = sorted((h.id, h.object) for h in c_union.intersection(c_union.bounds, objects=True))
    print("[|] interleaved:", c_union.interleaved)
    print("[|] len:", len(c_union))
    print("[|] items (id, object):", objs_union)
    print()

    # ----- Properties round-trip (safe near_minimum_overlap_factor) -----
    p = index.Property()
    p.leaf_capacity = 100
    p.index_capacity = 10
    # Must be < both capacities:
    p.near_minimum_overlap_factor = max(1, min(p.leaf_capacity, p.index_capacity) - 1)
    p.fill_factor = 0.5
    p.dimension = 2
    p.idx_extension = "index"
    p.dat_extension = "data"

    prop_idx = index.Index(properties=p)
    props = prop_idx.properties
    print("[properties] leaf_capacity:", props.leaf_capacity)
    print("[properties] index_capacity:", props.index_capacity)
    print("[properties] near_minimum_overlap_factor:", props.near_minimum_overlap_factor)
    print("[properties] fill_factor:", props.fill_factor)
    print("[properties] dimension:", props.dimension)
    print("[properties] extensions:", props.idx_extension, "/", props.dat_extension)

    # Rtree-only result offset/limit if supported
    try:
        if hasattr(core.rt, "Index_GetResultSetOffset"):
            r = index.Rtree()
            r.set_result_offset(3)
            print("[properties] Rtree.result_offset:", r.result_offset)
        else:
            print("[properties] Rtree.result_offset not supported by this lib build.")
        if hasattr(core.rt, "Index_GetResultSetLimit"):
            r = index.Rtree()
            r.set_result_limit(44)
            print("[properties] Rtree.result_limit:", r.result_limit)
        else:
            print("[properties] Rtree.result_limit not supported by this lib build.")
    except Exception as e:
        print("[properties] Rtree offset/limit failed:", type(e).__name__, str(e))
    print()

    # ----- Vectorized APIs (best-effort; guard if missing) -----
    # intersection_v
    try:
        mins = [[0, 2], [0, 2]]   # 2 dims x 2 queries
        maxs = [[10, 6], [10, 6]]
        ids_v, counts_v = c_union.intersection_v(mins, maxs)
        print("[intersection_v] ids:", ids_v.tolist())
        print("[intersection_v] counts:", counts_v.tolist())
    except Exception as e:
        print("[intersection_v] not available or failed:", type(e).__name__, str(e))

    # nearest_v
    try:
        mins_n = [[0, 8], [0, 7]]
        maxs_n = [[10, 9], [10, 8]]
        ret = c_union.nearest_v(mins_n, maxs_n, num_results=2, return_max_dists=True)
        if isinstance(ret, tuple) and len(ret) == 3:
            ids_nv, counts_nv, dists_nv = ret
            print("[nearest_v] ids:", ids_nv.tolist())
            print("[nearest_v] counts:", counts_nv.tolist())
            print("[nearest_v] max_dists:", getattr(dists_nv, "tolist", lambda: dists_nv)())
        else:
            print("[nearest_v] unexpected return:", type(ret).__name__)
    except Exception as e:
        print("[nearest_v] not available or failed:", type(e).__name__, str(e))
    print()


if __name__ == "__main__":
    main()
