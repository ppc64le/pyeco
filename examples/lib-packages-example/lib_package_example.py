import pkg_resources

def get_version(module_name, module=None):
    # Try to get version from common attributes if module is provided
    if module:
        for attr in ('__version__', 'version', 'VERSION'):
            version = getattr(module, attr, None)
            if version:
                if callable(version):
                    try:
                        return version()
                    except Exception:
                        continue
                return version

    # Fallback: try pkg_resources by module_name
    try:
        return pkg_resources.get_distribution(module_name).version
    except Exception:
        return "unknown"


try:
    import abseilcpp
    print("Success: imported package abseilcpp")

except ImportError:
    print("abseil-cpp not importable")

try:
    import cares  # for c-ares
    print("Success: imported package cares")

except ImportError:
    print("c-ares not importable")

try:
    import ffmpeg
    print("Success: imported package ffmpeg")
    print("Version:", get_version("ffmpeg", ffmpeg))
except ImportError:
    print("ffmpeg not importable")

try:
    import grpccpp
    print("Success: imported package grpc")

except ImportError:
    print("grpc-cpp not importable")

try:
    import hdf5  # hdf5 python binding
    print("Success: imported package h5py")
    print("Version:", get_version("hdf5", hdf5))
except ImportError:
    print("hdf5 not importable")

try:
    import lame
    print("Success: imported package lame")
    print("Version:", get_version("lame", lame))
except ImportError:
    print("lame not importable")

try:
    import libprotobuf
    print("Success: imported package libprotobuf")
    print("Version:", get_version("libprotobuf", libprotobuf))
except ImportError:
    print("libprotobuf not importable")

try:
    import libvpx
    print("Success: imported package libvpx")
    print("Version:", get_version("libvpx", libvpx))
except ImportError:
    print("libvpx not importable")

try:
    import openblas
    print("Success: imported package openblas")
    print("Version:", get_version("openblas", openblas))
except ImportError:
    print("openblas not importable")

try:
    import openmpi  # openmpi binding
    print("Success: imported package openmpi")
    print("Version:", get_version("openmpi", openmpi))
except ImportError:
    print("openmpi not importable")

try:
    import opus  # guess for opus
    print("Success: imported package opus")
    print("Version:", get_version("opus", opus))
except ImportError:
    print("opus not importable")

try:
    import orc
    print("Success: imported package orc")
    print("Version:", get_version("orc", orc))
except ImportError:
    print("orc not importable")

try:
    import re2
    print("Success: imported package re2")
    print("Version:", get_version("re2", re2))
except ImportError:
    print("re2 not importable")

try:
    import snappy
    print("Success: imported package snappy")
    print("Version:", get_version("snappy", snappy))
except ImportError:
    print("snappy not importable")

try:
    import thriftcpp  # thrift-cpp → thriftcpp
    print("Success: imported package thriftcpp")

except ImportError:
    print("thrift-cpp not importable")

try:
    import utf8proc
    print("Success: imported package utf8proc")
    print("Version:", get_version("utf8proc", utf8proc))
except ImportError:
    print("utf8proc not importable")
