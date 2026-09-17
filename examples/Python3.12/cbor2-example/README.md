## Purpose: Demonstrates binary serialisation and deserialisation using the cbor2 library, covering basic encode/decode, type fidelity, size comparison with JSON, streaming, and custom semantic tags.

### Packages used:
cbor2

### Functionality:

- Encodes and decodes a mixed-type Python dict using `cbor2.dumps` / `cbor2.loads` and verifies a clean round-trip.
- Demonstrates CBOR's native type fidelity for `bytes`, timezone-aware `datetime`, and `Decimal` values — types that JSON cannot represent without custom handling.
- Compares encoded byte sizes of CBOR vs JSON for the same payload, showing CBOR's compactness.
- Demonstrates streaming (incremental) encode/decode of multiple objects into a single `BytesIO` buffer using `CBOREncoder` and `CBORDecoder`.
- Encodes a value wrapped in a custom `CBORTag` (application-defined semantic tag), then decodes it and inspects the tag number and value.

### How to run the example :
```
chmod +x install_test_example.sh
./install_test_example.sh
```

### License:
It's covered under MIT License.
