from absl import app, flags
import attrs
import dask.array as da
import numpy as np
import yaml
import fsspec
import toolz
import cloudpickle
import wrapt

# --------------------
# absl flags
# --------------------
FLAGS = flags.FLAGS
flags.DEFINE_string("config", "config.yaml", "YAML config file")
flags.DEFINE_string("output", "result.pkl", "Pickle output file")

# --------------------
# attrs dataclass
# --------------------
@attrs.define
class Config:
    scale: int
    values: list

# --------------------
# wrapt decorator for logging
# --------------------
@wrapt.decorator
def log_call(wrapped, instance, args, kwargs):
    print(f"[LOG] Calling {wrapped.__name__} with args={args}, kwargs={kwargs}")
    return wrapped(*args, **kwargs)

# --------------------
# Processing function
# --------------------
@log_call
def scale_array(arr, factor):
    return arr * factor

# --------------------
# Main pipeline
# --------------------
def main(argv):
    # --- load YAML config ---
    fs = fsspec.filesystem("file")
    with fs.open(FLAGS.config, "r") as f:
        cfg_dict = yaml.safe_load(f)

    config = Config(**cfg_dict)

    # --- dask + numpy computation ---
    arr = da.from_array(np.array(config.values), chunks=2)
    result = scale_array(arr, config.scale).compute()

    # --- toolz post-processing ---
    squared = list(toolz.map(lambda x: x**2, result))

    print("Original values:", config.values)
    print(f"Scaled by {config.scale}:", result)
    print("Squared (toolz):", squared)

    # --- save result with cloudpickle ---
    with open(FLAGS.output, "wb") as f:
        cloudpickle.dump({"scaled": result.tolist(), "squared": squared}, f)

    print("Result saved to", FLAGS.output)

# --------------------
# Entry
# --------------------
if __name__ == "__main__":
    # Create sample config if missing
    sample_yaml = {"scale": 3, "values": [1, 2, 3, 4]}
    with open("config.yaml", "w") as f:
        yaml.dump(sample_yaml, f)

    app.run(main)
