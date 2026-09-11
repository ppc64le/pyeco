import unittest
import importlib.metadata
from decimal import Decimal
from datetime import datetime, timezone
from io import BytesIO

import cbor2
from cbor2 import CBOREncoder, CBORDecoder, CBORTag


class TestCbor2Library(unittest.TestCase):

    def test_cbor2_import(self):
        """Check that cbor2 can be imported."""
        try:
            import cbor2  # noqa: F401
        except ImportError:
            self.fail("cbor2 is not installed")

    def test_cbor2_version(self):
        """Verify cbor2 version."""
        version = importlib.metadata.version("cbor2")
        self.assertIn("6.1.4", version, f"'6.1.4' not found in version string: {version}")

    def test_basic_roundtrip(self):
        """Encoding and decoding a dict should recover the original."""
        original = {"key": "value", "num": 42, "flag": True, "empty": None}
        self.assertEqual(cbor2.loads(cbor2.dumps(original)), original)

    def test_bytes_type_preserved(self):
        """CBOR must preserve bytes values exactly."""
        data = {"payload": b"\x00\xff\xde\xad"}
        self.assertEqual(cbor2.loads(cbor2.dumps(data)), data)

    def test_datetime_type_preserved(self):
        """CBOR must preserve timezone-aware datetime objects."""
        dt = datetime(2024, 3, 15, 9, 30, 0, tzinfo=timezone.utc)
        data = {"ts": dt}
        recovered = cbor2.loads(cbor2.dumps(data))
        self.assertEqual(recovered["ts"], dt)

    def test_decimal_type_preserved(self):
        """CBOR must preserve Decimal values without floating-point loss."""
        value = Decimal("1.23456789012345678901234567890")
        data = {"amount": value}
        recovered = cbor2.loads(cbor2.dumps(data))
        self.assertEqual(recovered["amount"], value)

    def test_cbor_smaller_than_json(self):
        """CBOR encoding of a repetitive integer list should be smaller than JSON."""
        import json
        payload = {"ids": list(range(100))}
        cbor_size = len(cbor2.dumps(payload))
        json_size = len(json.dumps(payload).encode("utf-8"))
        self.assertLess(cbor_size, json_size)

    def test_streaming_roundtrip(self):
        """Multiple objects encoded sequentially must decode back in order."""
        records = [{"a": 1}, {"b": 2}, {"c": 3}]
        buf = BytesIO()
        enc = CBOREncoder(buf)
        for r in records:
            enc.encode(r)
        buf.seek(0)
        dec = CBORDecoder(buf)
        recovered = [dec.decode() for _ in records]
        self.assertEqual(recovered, records)

    def test_custom_tag_roundtrip(self):
        """A CBORTag must survive encode/decode with correct tag number and value."""
        tag_num = 9999
        value = {"x": 1, "y": 2}
        encoded = cbor2.dumps(CBORTag(tag_num, value))
        decoded = cbor2.loads(encoded)
        self.assertIsInstance(decoded, CBORTag)
        self.assertEqual(decoded.tag, tag_num)
        self.assertEqual(decoded.value, value)

    def test_empty_dict_roundtrip(self):
        """An empty dict should encode and decode cleanly."""
        self.assertEqual(cbor2.loads(cbor2.dumps({})), {})

    def test_empty_bytes_roundtrip(self):
        """Empty bytes should survive a CBOR round-trip."""
        self.assertEqual(cbor2.loads(cbor2.dumps(b"")), b"")

    def test_nested_structure(self):
        """Deeply nested dicts and lists should round-trip correctly."""
        data = {"level1": {"level2": {"level3": [1, 2, {"deep": True}]}}}
        self.assertEqual(cbor2.loads(cbor2.dumps(data)), data)

    def test_encoded_output_is_bytes(self):
        """cbor2.dumps must return a bytes object."""
        self.assertIsInstance(cbor2.dumps({"ok": True}), bytes)


if __name__ == "__main__":
    unittest.main()
