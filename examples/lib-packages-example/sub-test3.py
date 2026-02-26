import time
from thrift.protocol import TBinaryProtocol
from thrift.transport import TTransport

# 1. Test protobuf
try:
    import google.protobuf
    print("protobuf version:", google.protobuf.__version__)
except ImportError:
    print("protobuf is not installed")

# 2. Test OpenBLAS via NumPy
try:
    import numpy as np
    print("NumPy version:", np.__version__)
    size = 1000
    a = np.random.rand(size, size)
    b = np.random.rand(size, size)

    start = time.time()
    c = np.dot(a, b)
    end = time.time()

    print(f"Matrix multiplication time: {end - start:.4f} seconds")
except ImportError:
    print("numpy is not installed")

def test_thrift_cpp():
    # Since you referenced thrift-cpp, but in Python we use thrift package,
    # let's do a basic test of thrift serialization/deserialization
    transport_out = TTransport.TMemoryBuffer()
    protocol_out = TBinaryProtocol.TBinaryProtocol(transport_out)

    # Write a simple string
    test_string = "Hello, Thrift!"
    protocol_out.writeString(test_string)

    transport_in = TTransport.TMemoryBuffer(transport_out.getvalue())
    protocol_in = TBinaryProtocol.TBinaryProtocol(transport_in)

    read_string = protocol_in.readString()
    assert read_string == test_string
    print("Thrift protocol test passed.")

if __name__ == "__main__":
    test_thrift_cpp()