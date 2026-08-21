## Purpose: Demonstrates fast compression and decompression using the lz4 library with both the frame and block APIs.

### Packages used:
lz4

### Functionality:

- Compresses and decompresses data using the LZ4 frame API (`lz4.frame`), which produces standard interoperable LZ4 frames.
- Compresses and decompresses data using the LZ4 block API (`lz4.block`), with lower overhead for in-process use.
- Compares compression ratios and compression times across LZ4 compression levels (0, 3, 9, 16), where level 0 is fastest and higher levels use LZ4HC for better ratios.
- Demonstrates streaming file compression and decompression in chunks using `lz4.frame.open`.

### How to run the example :
```
chmod +x install_test_example.sh
./install_test_example.sh
```

### License:
It's covered under BSD License.
