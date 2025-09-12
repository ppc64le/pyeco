## ✅ Program : Native Dependencies Import and Version Check

### Purpose:
Checks the availability and versions of various native or system-level Python bindings and libraries, reporting which are installed and importable in the current environment.

### Packages checked:
abseilcpp, cares (c-ares), ffmpeg, grpc-cpp, hdf5 (h5py), lame, libprotobuf, libvpx, openblas, openmpi, opus, orc, re2, snappy, thriftcpp, utf8proc

### Functionality:
- Attempts to import each native package.
- Prints success or failure messages.
- Retrieves and displays version information where available, using either common attributes (__version__, version, VERSION) or pkg_resources.
- Gracefully handles missing packages or failures to fetch versions.

### How to run the example :
```
chmod +x install_test_example.sh
./install_test_example.sh
```
### License: 
It's covered under Apache 2.0 licenses
