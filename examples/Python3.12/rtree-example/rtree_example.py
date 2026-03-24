# main.py
# Robust rtree demo that prints concise test results only.
# Covers:
# - insert/intersection/objects
# - nearest (KNN)
# - bounds (interleaved/deinterleaved)
# - on-disk serialization (custom extensions), unicode path, overwrite (with safe temp dirs)
# - stream loading
# - 3D index (uninterleaved)
# - vectorized APIs (intersection_v/nearest_v) if available
# - duplicate insertion behavior
# - properties round-trip with safe near_minimum_overlap_factor
# - length vs get_size (deprecated)

from rtree import index, core
from rtree.exceptions import RTreeError
import tempfile
import json
import os
import sys
import platform


def build_rect_index(rects):
    """rects: dict[id] = (minx,miny,maxx,maxy)"""
    idx = index.Index()
    for rid, bbox in rects.items():
        idx.add(rid, bbox)
    return idx


def print_env():
    print("=== main: rtree end-to-end demo (resilient) ===\n")
    try:
        print("[env] Python:", sys.version.split()[0], "| Platform:", platform.platform())
    except Exception:
        pass
    try:
        print("[env] libspatialindex version:", core.rt.SIDX_Version().decode())
    except Exception as e:
        print("[env] libspatialindex version lookup failed:", type(e).__name__, str(e))
    try:
        print("[env] core library handle:", getattr(core.rt, "_name", "<unknown>"))
    except Exception:
        pass
    print()


def basic_and_objects_demo():
    # ---------------------------
    # 1) Basic: add + intersection (+ deprecated get_size)
    # ---------------------------
    rects = {
        0: (0.0, 0.0, 10.0, 10.0),
        4: (5.0, 5.0, 15.0, 15.0),
        16: (20.0, 20.0, 30.0, 30.0),
        27: (8.0, 0.0, 12.0, 4.0),
        35: (40.0, 40.0, 50.0, 55.0),
    }
    idx = build_rect_index(rects)
    query = (0.0, 0.0, 12.0, 12.0)
    hits = sorted(idx.intersection(query))

    print("[basic] index size (len):", len(idx))
    if hasattr(idx, "get_size"):
        try:
            print("[basic] index size (get_size - deprecated):", idx.get_size())
        except Exception as e:
            print("[basic] get_size() raised:", type(e).__name__, str(e))
    print("[basic] query bbox:", query)
    print("[basic] intersection ids:", hits)
    print()

    # ---------------------------
    # 2) Insert with payload, objects=True
    # ---------------------------
    payload_id = 4321
    payload_bbox = (34.3776829412, 26.7375853734, 49.3776829412, 41.7375853734)
    payload_obj = {"label": "demo", "meta": [1, "x"]}
    idx.insert(payload_id, payload_bbox, obj=payload_obj)

    hits_obj = list(idx.intersection((0, 0, 60, 60), objects=True))
    item = next(h for h in hits_obj if h.id == payload_id)

    print("[objects] inserted id:", payload_id)
    print("[objects] retrieved id:", item.id)
    print("[objects] retrieved payload:", item.object)
    print("[objects] retrieved bbox (rounded):", [round(t, 6) for t in item.bbox])
    print()

    return rects  # reuse for disk demo


def knn_and_bounds_demo():
    # ---------------------------
    # 3) Nearest (KNN) with points (zero-area boxes)
    # ---------------------------
    pt_idx = index.Index()
    points = {
        1: (0.0, 0.0, 0.0, 0.0),
        2: (2.0, 2.0, 2.0, 2.0),
        3: (-1.0, 1.0, -1.0, 1.0),
        4: (5.0, 1.0, 5.0, 1.0),
        5: (1.0, -3.0, 1.0, -3.0),
    }
    for pid, bbox in points.items():
        pt_idx.add(pid, bbox)

    knn_query = (1.0, 1.0, 1.0, 1.0)
    k = 3
    knn_ids = list(pt_idx.nearest(knn_query, k))

    print("[knn] query point bbox:", knn_query)
    print("[knn] k:", k)
    print("[knn] nearest ids:", knn_ids)
    print()

    # ---------------------------
    # 4) Bounds (interleaved vs. deinterleaved)
    # ---------------------------
    b_idx = index.Index()
    b_idx.add(1, (-1.0, -2.0, 3.0, 4.0))
    b_idx.add(2, (-5.0, -1.0, -4.0, 2.0))
    print("[bounds] interleaved [xmin,ymin,xmax,ymax]:", b_idx.bounds)
    print(
        "[bounds] deinterleaved [xmin,xmax,ymin,ymax]:",
        b_idx.get_bounds(coordinate_interleaved=False),
    )
    print()


def disk_unicodename_and_overwrite_demo(rects):
    # These disk-backed blocks are the ones that can fail in some environments.
    p = index.Property()
    p.idx_extension = "index"
    p.dat_extension = "data"

    # ---------------------------
    # 5) On-disk serialization (custom ext), unicode path, safe temp dir, overwrite
    # ---------------------------
    try:
        with tempfile.TemporaryDirectory() as td:
            base = os.path.join(td, "gilename\u4500abc")  # unicode base

            # Paranoid cleanup (temp dir should be empty anyway)
            for ext in (p.idx_extension, p.dat_extension):
                f = f"{base}.{ext}"
                if os.path.exists(f):
                    os.remove(f)

            # Fresh creation with overwrite=True
            disk_idx = index.Index(base, properties=p, overwrite=True)
            for rid, bbox in rects.items():
                disk_idx.add(rid, bbox)

            before = sorted(disk_idx.intersection((0, 0, 12, 12)))
            del disk_idx

            # Reopen with the same base/properties
            disk_idx2 = index.Index(base, properties=p)
            after = sorted(disk_idx2.intersection((0, 0, 12, 12)))

            print("[disk/unicode] base filename:", base)
            print("[disk/unicode] ids before close:", before)
            print("[disk/unicode] ids after reopen:", after)
            print("[disk/unicode] match:", before == after)
            print()
    except RTreeError as e:
        print("[disk/unicode] disk-backed index not available:", type(e).__name__, str(e))
        print("  → Falling back to an in-memory demonstration for this section.")
        mem_idx = index.Index()
        for rid, bbox in rects.items():
            mem_idx.add(rid, bbox)
        mem_ids = sorted(mem_idx.intersection((0, 0, 12, 12)))
        print("[disk/unicode:FALLBACK] ids (in-memory):", mem_ids)
        print()

    # ---------------------------
    # 6) Overwrite example (safe temp dir)
    # ---------------------------
    try:
        with tempfile.TemporaryDirectory() as td2:
            base2 = os.path.join(td2, "rtree_demo")

            for ext in (p.idx_extension, p.dat_extension):
                f = f"{base2}.{ext}"
                if os.path.exists(f):
                    os.remove(f)

            disk_a = index.Index(base2, properties=p, overwrite=True)
            disk_a.add(99, (0, 0, 1, 1))
            ids_before = sorted(disk_a.intersection((0, 0, 10, 10)))
            del disk_a

            disk_b = index.Index(base2, overwrite=True, properties=p)
            disk_b.add(100, (2, 2, 3, 3))
            ids_after = sorted(disk_b.intersection((0, 0, 10, 10)))

            print("[overwrite] base:", base2)
            print("[overwrite] ids before recreate:", ids_before)
            print("[overwrite] ids after recreate:", ids_after)
            print("[overwrite] recreated cleanly:", ids_after == [100])
            print()
    except RTreeError as e:
        print("[overwrite] disk-backed index not available:", type(e).__name__, str(e))
        print("  → Skipping overwrite demonstration for disk; continuing.")


def stream_and_3d_and_vectorized_and_dups_demo(rects_for_v):
    # ---------------------------
    # 7) Stream loading (generator input)
    # ---------------------------
    def stream():
        # (id, bbox, object)
        for i in range(6):
            yield (1000 + i, (i, i, i + 0.5, i + 0.5), {"i": i})

    s_idx = index.Index(stream())
    s_hits = list(s_idx.intersection((2.0, 2.0, 10.0, 10.0), objects=True))
    print("[stream] total items:", len(s_idx))
    print("[stream] intersection@((2,2)-(10,10)) ids:", sorted(h.id for h in s_hits))
    print("[stream] sample payload for first hit:", json.dumps(s_hits[0].object))
    print()

    # ---------------------------
    # 8) 3D index (dimension=3, uninterleaved)
    # ---------------------------
    prop3 = index.Property()
    prop3.dimension = 3
    idx3d = index.Index(properties=prop3, interleaved=False)
    # For interleaved=False order: (xmin, xmax, ymin, ymax, zmin, zmax)
    idx3d.insert(7, (0, 10, 0, 10, 2, 4))
    q3d = (-1, 5, -1, 5, 1, 3)
    hits3d = list(idx3d.intersection(q3d))
    print("[3d] query (uninterleaved dims):", q3d)
    print("[3d] intersection ids:", hits3d)
    print()

    # ---------------------------
    # 9) Vectorized APIs (only if supported by your lib)
    # ---------------------------
    # Probe availability carefully.
    try:
        mins = [[0, 40], [0, 40]]  # shape: 2 dims x 2 queries
        maxs = [[12, 55], [12, 55]]
        ids_v, counts_v = index.Index().intersection_v(mins, maxs)  # probe callability
        probe_ok = True
    except Exception:
        probe_ok = False

    if probe_ok:
        try:
            v_idx = build_rect_index(rects_for_v)
            ids_v, counts_v = v_idx.intersection_v(mins, maxs)
            print("[intersection_v] ids:", ids_v.tolist())
            print("[intersection_v] counts:", counts_v.tolist())
        except Exception as e:
            print("[intersection_v] failed:", type(e).__name__, str(e))
    else:
        print("[intersection_v] not available in this lib build.")

    try:
        mins_n = [[0, 40], [0, 40]]
        maxs_n = [[12, 55], [12, 55]]
        ret = index.Index().nearest_v(mins_n, maxs_n, num_results=2, return_max_dists=True)  # probe
        probe_ok = isinstance(ret, tuple)
    except Exception:
        probe_ok = False

    if probe_ok:
        try:
            v_idx = build_rect_index(rects_for_v)
            ret = v_idx.nearest_v(mins_n, maxs_n, num_results=2, return_max_dists=True)
            if isinstance(ret, tuple) and len(ret) == 3:
                ids_nv, counts_nv, dists_nv = ret
                print("[nearest_v] ids:", ids_nv.tolist())
                print("[nearest_v] counts:", counts_nv.tolist())
                print("[nearest_v] max_dists:", getattr(dists_nv, "tolist", lambda: dists_nv)())
            else:
                print("[nearest_v] unexpected return:", type(ret).__name__)
        except Exception as e:
            print("[nearest_v] failed:", type(e).__name__, str(e))
    else:
        print("[nearest_v] not available in this lib build.")
    print()

    # ---------------------------
    # 10) Duplicate insertion of same ID
    # ---------------------------
    dup = index.Index()
    dup.add(1, (2, 2))
    dup.add(1, (3, 3))
    dup_hits = list(dup.intersection((0, 0, 5, 5)))
    print("[duplicates] query (0,0,5,5) ids:", dup_hits)
    print()


def properties_demo():
    # ---------------------------
    # 11) Properties round-trip (safe near_minimum_overlap_factor) + Rtree result offset/limit
    # ---------------------------
    p_rt = index.Property()
    # Set capacities first
    p_rt.leaf_capacity = 100
    p_rt.index_capacity = 10

    # near_minimum_overlap_factor MUST be < both capacities.
    # Compute it safely so future edits don't break creation.
    safe_nmo = max(1, min(p_rt.leaf_capacity, p_rt.index_capacity) - 1)
    p_rt.near_minimum_overlap_factor = safe_nmo

    # Other representative properties
    p_rt.fill_factor = 0.5
    p_rt.dimension = 2
    p_rt.idx_extension = "index"
    p_rt.dat_extension = "data"

    # Construct the index with the properties
    prop_idx = index.Index(properties=p_rt)

    # Snapshot properties from the live index
    props = prop_idx.properties
    print("[properties] leaf_capacity:", props.leaf_capacity)
    print("[properties] index_capacity:", props.index_capacity)
    print("[properties] near_minimum_overlap_factor:", props.near_minimum_overlap_factor)
    print("[properties] fill_factor:", props.fill_factor)
    print("[properties] dimension:", props.dimension)
    print("[properties] extensions:", props.idx_extension, "/", props.dat_extension)

    # Rtree-only result offset/limit if lib supports it
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


def main():
    print_env()
    rects = basic_and_objects_demo()
    knn_and_bounds_demo()
    disk_unicodename_and_overwrite_demo(rects)  # robust error handling + fallbacks
    stream_and_3d_and_vectorized_and_dups_demo(
        rects_for_v={
            0: (0.0, 0.0, 10.0, 10.0),
            4: (5.0, 5.0, 15.0, 15.0),
            27: (8.0, 0.0, 12.0, 4.0),
            35: (40.0, 40.0, 50.0, 55.0),
        }
    )
    properties_demo()


if __name__ == "__main__":
    main()
