import json
from decimal import Decimal
from datetime import datetime, timezone
from io import BytesIO

import cbor2
from cbor2 import CBOREncoder, CBORDecoder, CBORTag


def demo_basic_roundtrip():
    """
    Demonstrate basic CBOR encode/decode with a mixed-type Python dict.
    cbor2.dumps() produces compact binary bytes; cbor2.loads() recovers the original.
    """
    print("--- Basic Encode / Decode ---")
    original = {
        "name": "Alice",
        "age": 30,
        "score": 98.6,
        "active": True,
        "nickname": None,
        "tags": ["cbor", "binary", "compact"],
    }

    encoded = cbor2.dumps(original)
    decoded = cbor2.loads(encoded)

    assert decoded == original, "Round-trip mismatch!"
    print(f"  Original : {original}")
    print(f"  Encoded  : {len(encoded)} bytes  (hex: {encoded.hex()})")
    print(f"  Decoded  : {decoded}")
    print(f"  Round-trip: PASSED")


def demo_type_fidelity():
    """
    CBOR preserves Python types that JSON cannot represent natively:
    bytes, datetime (timezone-aware), Decimal, and frozenset (via list tag).
    """
    print("\n--- Type Fidelity ---")
    now = datetime(2024, 6, 1, 12, 0, 0, tzinfo=timezone.utc)

    cases = {
        "bytes value": b"\xde\xad\xbe\xef",
        "datetime (UTC)": now,
        "Decimal": Decimal("3.14159265358979"),
        "nested bytes list": [b"\x00\x01", b"\x02\x03"],
    }

    for label, value in cases.items():
        payload = {"data": value}
        encoded = cbor2.dumps(payload)
        decoded = cbor2.loads(encoded)
        assert decoded["data"] == value, f"Type fidelity failed for {label}"
        print(f"  {label:<28} → encoded {len(encoded):>3} bytes  PASSED")


def demo_cbor_vs_json_size():
    """
    Compare encoded size of CBOR vs JSON for the same payload.
    CBOR is typically more compact because it uses binary type tags
    instead of text delimiters and quotes.
    """
    print("\n--- CBOR vs JSON Size Comparison ---")
    payload = {
        "id": 1001,
        "username": "bob_coder",
        "email": "bob@example.com",
        "scores": list(range(50)),
        "metadata": {"created": "2024-01-15", "verified": True, "level": 5},
    }

    cbor_bytes = cbor2.dumps(payload)
    json_bytes = json.dumps(payload).encode("utf-8")

    saving_pct = (1 - len(cbor_bytes) / len(json_bytes)) * 100
    print(f"  JSON size : {len(json_bytes):>6} bytes")
    print(f"  CBOR size : {len(cbor_bytes):>6} bytes")
    print(f"  CBOR is {saving_pct:.1f}% smaller than JSON for this payload")


def demo_streaming():
    """
    Demonstrate streaming (incremental) encode/decode using CBOREncoder and
    CBORDecoder over a BytesIO buffer.  This pattern is useful when encoding
    multiple objects into a single byte stream (e.g. a log file or socket).
    """
    print("\n--- Streaming Encode / Decode ---")
    records = [
        {"event": "login", "user": "alice", "ts": 1_700_000_000},
        {"event": "purchase", "item": "widget", "qty": 3},
        {"event": "logout", "user": "alice", "ts": 1_700_000_120},
    ]

    buf = BytesIO()
    encoder = CBOREncoder(buf)
    for record in records:
        encoder.encode(record)

    buf.seek(0)
    decoder = CBORDecoder(buf)
    recovered = []
    for _ in records:
        recovered.append(decoder.decode())

    assert recovered == records, "Streaming round-trip mismatch!"
    print(f"  Encoded {len(records)} records into {buf.tell()} bytes")
    for i, rec in enumerate(recovered):
        print(f"  Record {i}: {rec}")
    print(f"  Streaming round-trip: PASSED")


def demo_custom_tag():
    """
    CBOR supports semantic tags (integers) that attach extra meaning to a value.
    Here we encode a dict wrapped in a custom application tag (tag 1000),
    decode it back, and inspect the tag number and value.
    """
    print("\n--- Custom CBOR Tag ---")
    TAG_SENSOR_READING = 1000

    reading = {"sensor_id": "T-42", "celsius": 23.7, "humidity": 61.2}
    tagged = CBORTag(TAG_SENSOR_READING, reading)

    encoded = cbor2.dumps(tagged)
    decoded = cbor2.loads(encoded)

    assert isinstance(decoded, CBORTag), "Expected a CBORTag back"
    assert decoded.tag == TAG_SENSOR_READING, "Tag number mismatch"
    assert decoded.value == reading, "Tagged value mismatch"

    print(f"  Tag number : {decoded.tag}")
    print(f"  Tag value  : {decoded.value}")
    print(f"  Encoded    : {len(encoded)} bytes")
    print(f"  Custom tag round-trip: PASSED")


if __name__ == "__main__":
    print("=== cbor2 Example: Binary Serialisation with CBOR ===\n")

    demo_basic_roundtrip()
    demo_type_fidelity()
    demo_cbor_vs_json_size()
    demo_streaming()
    demo_custom_tag()

    print("\ncbor2 example completed successfully.")
