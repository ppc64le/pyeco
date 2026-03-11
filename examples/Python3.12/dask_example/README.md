## ✅ Program : Dask Array Processing Mini Pipeline

### Purpose:
Demonstrates a small data processing pipeline using Dask arrays with configuration loading, computation, and result serialization.

### Packages used:
dask numpy absl-py attrs PyYAML fsspec toolz cloudpickle wrapt

### Functionality:
- Loads configuration values from a YAML file.
- Creates a Dask array from input values.
- Scales the array values using a processing function.
- Executes parallel computation using `.compute()`.
- Uses toolz for post-processing of results.
- Saves processed results to a `.pkl` file using cloudpickle.

### How to run the example :

chmod +x install_test_example.sh
./install_test_example.sh


### License:
It's covered under Apache 2.0 licenses
