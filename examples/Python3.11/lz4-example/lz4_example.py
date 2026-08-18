import os
import time
import lz4.frame
import lz4.block


def generate_sample_data(size_kb=256):
    """Generate compressible sample text data (~size_kb KB)."""
    line = "The quick brown fox jumps over the lazy dog. " * 10
    repetitions = (size_kb * 1024) // len(line.encode()) + 1
    return (line * repetitions).encode("utf-8")[: size_kb * 1024]


def demo_frame_compress_decompress(data):
    """
    Demonstrate lz4.frame compression and decompression.
    lz4.frame wraps data in a standard LZ4 frame format — interoperable
    with the lz4 CLI tool and other language bindings.
    """
    print("--- LZ4 Frame API ---")
    original_size = len(data)

    t0 = time.perf_counter()
    compressed = lz4.frame.compress(data)
    t_compress = time.perf_counter() - t0

    compressed_size = len(compressed)
    ratio = compressed_size / original_size

    t0 = time.perf_counter()
    decompressed = lz4.frame.decompress(compressed)
    t_decompress = time.perf_counter() - t0

    assert decompressed == data, "Decompressed data does not match original!"

    print(f"  Original size   : {original_size:>10,} bytes")
    print(f"  Compressed size : {compressed_size:>10,} bytes")
    print(f"  Compression ratio: {ratio:.3f}  ({(1 - ratio) * 100:.1f}% reduction)")
    print(f"  Compression time : {t_compress * 1000:.3f} ms")
    print(f"  Decompression time: {t_decompress * 1000:.3f} ms")
    print(f"  Integrity check  : PASSED")


def demo_block_compress_decompress(data):
    """
    Demonstrate lz4.block compression (raw block, no frame header).
    Slightly lower overhead than frame; suitable for in-process use.
    """
    print("\n--- LZ4 Block API ---")
    original_size = len(data)

    compressed = lz4.block.compress(data)
    compressed_size = len(compressed)

    decompressed = lz4.block.decompress(compressed, uncompressed_size=original_size)
    assert decompressed == data, "Block decompressed data does not match original!"

    ratio = compressed_size / original_size
    print(f"  Original size   : {original_size:>10,} bytes")
    print(f"  Compressed size : {compressed_size:>10,} bytes")
    print(f"  Compression ratio: {ratio:.3f}  ({(1 - ratio) * 100:.1f}% reduction)")
    print(f"  Integrity check  : PASSED")


def demo_compression_levels(data):
    """
    Compare lz4.frame compression at different levels.
    Level 0 = fast (LZ4 default), higher levels use LZ4HC (slower, better ratio).
    """
    print("\n--- Compression Level Comparison ---")
    print(f"  {'Level':>7}  {'Comp. Size':>12}  {'Ratio':>7}  {'Time (ms)':>10}")
    for level in [0, 3, 9, 16]:
        t0 = time.perf_counter()
        compressed = lz4.frame.compress(data, compression_level=level)
        elapsed = (time.perf_counter() - t0) * 1000
        ratio = len(compressed) / len(data)
        print(f"  {level:>7}  {len(compressed):>12,}  {ratio:>7.3f}  {elapsed:>10.3f}")


def demo_streaming(data):
    """
    Demonstrate streaming compression using LZ4FrameFile context manager.
    Useful for compressing large files incrementally without loading all into memory.
    """
    print("\n--- Streaming Compression (LZ4FrameFile) ---")
    import tempfile

    with tempfile.NamedTemporaryFile(suffix=".lz4", delete=False) as tmp:
        tmp_path = tmp.name

    try:
        chunk_size = 64 * 1024  # 64 KB chunks
        with lz4.frame.open(tmp_path, "wb") as f:
            for offset in range(0, len(data), chunk_size):
                f.write(data[offset: offset + chunk_size])

        compressed_file_size = os.path.getsize(tmp_path)
        print(f"  Written to     : {tmp_path}")
        print(f"  Compressed file: {compressed_file_size:,} bytes  "
              f"(original: {len(data):,} bytes)")

        # Read back
        with lz4.frame.open(tmp_path, "rb") as f:
            recovered = f.read()
        assert recovered == data, "Streamed decompression mismatch!"
        print(f"  Stream round-trip: PASSED")
    finally:
        os.unlink(tmp_path)


if __name__ == "__main__":
    print("=== LZ4 Example: Fast Compression and Decompression ===\n")

    data = generate_sample_data(size_kb=256)
    print(f"Generated {len(data):,} bytes of sample text data.\n")

    demo_frame_compress_decompress(data)
    demo_block_compress_decompress(data)
    demo_compression_levels(data)
    demo_streaming(data)

    print("\nlz4 example completed successfully.")
