import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from receipt import TEXT, make_receipt, verify


class ReceiptTests(unittest.TestCase):
    def test_resolves_and_reports_missing(self):
        receipt = make_receipt([{"alias": "f1", "id": "memory-1", "text": "x"}])
        rows = verify("See f1 and f2; ignore foo1.", receipt)
        self.assertEqual([(r["alias"], r["resolved"]) for r in rows], [("f1", True), ("f2", False)])
        self.assertEqual(len(receipt["aliases"]["f1"]["text_sha256"]), 64)

    def test_duplicate_is_rejected(self):
        with self.assertRaises(ValueError):
            make_receipt([{"alias": "f1", "id": "a"}, {"alias": "f1", "id": "b"}])

    def test_languages(self):
        self.assertEqual(set(TEXT), {"en", "fr", "es"})


if __name__ == "__main__":
    unittest.main()
