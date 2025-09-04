import attrs
import yaml
import dask.array as da
import numpy as np
import fsspec
import cloudpickle
import toolz
import wrapt
import tree
from packaging.version import parse as vparse
import partd
import locket
import time


# --------------------
# attrs + PyYAML: nested config
# --------------------
@attrs.define
class ModelConfig:
    name: str
    params: dict


def test_attrs_yaml_nested():
    cfg = ModelConfig(name="demo", params={"lr": 0.01, "epochs": 5})
    dumped = yaml.dump(attrs.asdict(cfg))
    loaded = yaml.safe_load(dumped)
    cfg2 = ModelConfig(**loaded)
    assert cfg == cfg2
    print("attrs + PyYAML nested OK")


# --------------------
# dask + numpy + toolz: matrix ops
# --------------------
def test_dask_numpy_toolz_matrix():
    arr = da.from_array(np.arange(1, 10).reshape(3, 3), chunks=(2, 2))
    doubled = arr * 2
    flattened = doubled.compute().flatten()
    summed = toolz.reduce(lambda x, y: x + y, flattened)
    assert summed == sum(np.arange(1, 10) * 2)
    print("dask + numpy + toolz matrix OK")


# --------------------
# fsspec + cloudpickle: save/load numpy array
# --------------------
def test_fsspec_cloudpickle_numpy():
    fs = fsspec.filesystem("file")
    arr = np.linspace(0, 1, 5)
    with fs.open("array.pkl", "wb") as f:
        cloudpickle.dump(arr, f)
    with fs.open("array.pkl", "rb") as f:
        arr2 = cloudpickle.load(f)
    assert np.allclose(arr, arr2)
    print("fsspec + cloudpickle numpy OK")


# --------------------
# wrapt: timing decorator
# --------------------
@wrapt.decorator
def timing(wrapped, instance, args, kwargs):
    start = time.time()
    result = wrapped(*args, **kwargs)
    elapsed = time.time() - start
    print(f"[wrapt] {wrapped.__name__} took {elapsed:.6f}s")
    return result


@timing
def slow_add(a, b):
    time.sleep(0.1)
    return a + b


def test_wrapt_timing():
    result = slow_add(5, 7)
    assert result == 12
    print("wrapt timing OK")


# --------------------
# dm-tree: nested transformations
# --------------------
def test_dmtree_transform():
    nested = {"x": [1, 2], "y": {"z": [3, 4]}}
    mapped = tree.map_structure(lambda v: v if isinstance(v, list) else v, nested)
    assert mapped["y"]["z"] == [3, 4]
    print("dm-tree transform OK")


# --------------------
# packaging: version sorting
# --------------------
def test_packaging_sort():
    versions = ["1.0.0", "2.0.0", "1.5.0"]
    sorted_versions = sorted(versions, key=vparse)
    assert sorted_versions == ["1.0.0", "1.5.0", "2.0.0"]
    print("packaging sort OK")


# --------------------
# partd + locket: multiple values under same key
# --------------------
def test_partd_locket_multiple():
    store = partd.File("store2")
    lock = locket.lock_file("store2/lock")

    with lock:
        store.append({"numbers": b"1"})
        store.append({"numbers": b"2"})
        val = store.get("numbers")

    # partd concatenates values
    assert val == b"12"
    print("partd + locket multiple OK")


# --------------------
# Runner
# --------------------
if __name__ == "__main__":
    test_attrs_yaml_nested()
    test_dask_numpy_toolz_matrix()
    test_fsspec_cloudpickle_numpy()
    test_wrapt_timing()
    test_dmtree_transform()
    test_packaging_sort()
    test_partd_locket_multiple()
    print("\n✅ All second-round package tests passed!")
