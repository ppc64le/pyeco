import time
import socket
import select

# Test 1: abseil-py
def test_abseil():
    try:
        from absl import app
        print("[abseil-py] ✅ Import successful")
    except ImportError as e:
        print("[abseil-py] ❌ Import failed:", e)

# Test 2: pycares (c-ares)
def test_pycares():
    try:
        import pycares

        def callback(result, error):
            if error:
                print("[pycares] ❌ DNS Error:", error)
            else:
                print("[pycares] ✅ DNS Result:", result)

        channel = pycares.Channel()
        channel.gethostbyname('google.com', socket.AF_INET, callback)

        timeout = 5.0  # seconds
        start = time.time()
        while True:
            read_fds, write_fds = channel.getsock()

            if not read_fds and not write_fds:
                break

            remaining = max(0, start + timeout - time.time())
            if remaining == 0:
                print("[pycares] ❌ Timeout waiting for DNS response")
                break

            readable, writable, _ = select.select(read_fds, write_fds, [], remaining)

            read_fd = readable[0] if readable else -1
            write_fd = writable[0] if writable else -1

            channel.process_fd(read_fd, write_fd)

    except ImportError as e:
        print("[pycares] ❌ Import failed:", e)

# Run all tests
if __name__ == '__main__':
    print("Running package tests...\n")
    test_abseil()
    test_pycares()
