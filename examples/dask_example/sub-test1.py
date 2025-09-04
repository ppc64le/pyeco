import attrs
import yaml
import dask.array as da
import numpy as np
import fsspec
import cloudpickle
import toolz
import wrapt
import tree
from packaging import version
import partd
import locket


# --------------------
# attrs + PyYAML
# --------------------
@attrs.define
class Config:
    scale: int
    values: list


def test_attrs_yaml():
    cfg = Config(scale=2, values=[1, 2, 3])
    dumped = yaml.dump(attrs.asdict(cfg))
    loaded = yaml.safe_load(dumped)
    cfg2 = Config(**loaded)
    assert cfg == cfg2
    print("attrs + PyYAML OK")


# --------------------
# dask + numpy + toolz
# --------------------
def test_dask_numpy_toolz():
    arr = da.from_array(np.array([1, 2, 3, 4]), chunks=2)
    result = arr * 2
    computed = result.compute()
    squared = list(toolz.map(lambda x: x**2, computed))
    assert squared == [4, 16, 36, 64]
    print("dask + numpy + toolz OK")


# --------------------
# fsspec + cloudpickle
# --------------------
def test_fsspec_cloudpickle():
    fs = fsspec.filesystem("file")
    obj = {"a": 1, "b": [1, 2, 3]}
    with fs.open("test.pkl", "wb") as f:
        cloudpickle.dump(obj, f)
    with fs.open("test.pkl", "rb") as f:
        loaded = cloudpickle.load(f)
    assert loaded == obj
    print("fsspec + cloudpickle OK")


# --------------------
# wrapt
# --------------------
@wrapt.decorator
def log_call(wrapped, instance, args, kwargs):
    print(f"[wrapt] {wrapped.__name__} called with {args}")
    return wrapped(*args, **kwargs)


@log_call
def add(a, b):
    return a + b


def test_wrapt():
    result = add(2, 3)
    assert result == 5
    print("wrapt OK")


# --------------------
# dm-tree
# --------------------
def test_dmtree():
    nested = {"a": [1, 2], "b": {"c": 3}}
    flat = tree.flatten(nested)
    rebuilt = tree.unflatten_as(nested, flat)
    assert nested == rebuilt
    print("dm-tree OK")


# --------------------
# packaging
# --------------------
def test_packaging():
    assert version.parse("1.0.0") < version.parse("2.0.0")
    print("packaging OK")


# --------------------
# partd + locket
# --------------------
def test_partd_locket():
    store = partd.File("store")
    lock = locket.lock_file("store/lock")

    with lock:
        store.append({"key": b"123"})   # ✅ must pass dict
        store.append({"key2": b"456"})
        val1 = store.get("key")
        val2 = store.get("key2")

    assert val1 == b"123"
    assert val2 == b"456"
    print("partd + locket OK")


# --------------------
# Main runner
# --------------------
if __name__ == "__main__":
    test_attrs_yaml()
    test_dask_numpy_toolz()
    test_fsspec_cloudpickle()
    test_wrapt()
    test_dmtree()
    test_packaging()
    test_partd_locket()
    print("\n✅ All package tests passed!")
