#!/usr/bin/env python3
"""Persist and verify memory citation aliases before their context disappears."""

import argparse
import datetime as dt
import hashlib
import json
import re
import sys
from pathlib import Path

ALIAS = re.compile(r"^[fo][1-9][0-9]*$")
CITATION = re.compile(r"(?<![A-Za-z0-9_])([fo][1-9][0-9]*)(?![A-Za-z0-9_])")
TEXT = {
    "en": {"title": "Memory citation links", "unknown": "unresolved", "known": "resolved", "demo": "Offline fixture. Capture aliases while the source context is still available."},
    "fr": {"title": "Liens des citations de mémoire", "unknown": "introuvable", "known": "résolu", "demo": "Exemple hors ligne. Capturez les alias tant que le contexte source est disponible."},
    "es": {"title": "Enlaces de citas de memoria", "unknown": "sin resolver", "known": "resuelto", "demo": "Ejemplo sin conexión. Capture los alias mientras el contexto de origen esté disponible."},
}


def make_receipt(facts):
    aliases = {}
    for fact in facts:
        alias, identifier = fact["alias"], fact["id"]
        if not ALIAS.fullmatch(alias) or not isinstance(identifier, str) or not identifier:
            raise ValueError("fact requires an fN/oN alias and non-empty id")
        if alias in aliases:
            raise ValueError("duplicate alias: " + alias)
        aliases[alias] = {"id": identifier, "source_url": fact.get("source_url"), "text_sha256": hashlib.sha256(fact.get("text", "").encode()).hexdigest() if "text" in fact else None}
    return {"schema_version": 1, "captured_at": dt.datetime.now(dt.timezone.utc).isoformat(), "aliases": aliases}


def verify(report_text, receipt):
    aliases = receipt.get("aliases", {})
    cited = sorted(set(CITATION.findall(report_text)), key=lambda x: (x[0], int(x[1:])))
    return [{"alias": alias, "resolved": alias in aliases, "id": aliases.get(alias, {}).get("id"), "source_url": aliases.get(alias, {}).get("source_url")} for alias in cited]


def main(argv=None):
    ap = argparse.ArgumentParser(description="Capture and verify short memory citation aliases.")
    ap.add_argument("command", choices=["demo", "build", "verify"])
    ap.add_argument("--lang", choices=TEXT, default="en")
    ap.add_argument("--facts", type=Path, help="JSON array with alias/id and optional source_url/text")
    ap.add_argument("--receipt", type=Path)
    ap.add_argument("--report", type=Path)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    try:
        if args.command == "build":
            if not args.facts or not args.out:
                ap.error("build requires --facts and --out")
            obj = make_receipt(json.loads(args.facts.read_text()))
            args.out.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")
            print(str(args.out))
            return 0
        if args.command == "demo":
            root = Path(__file__).parent / "fixtures"
            receipt = make_receipt(json.loads((root / "facts.json").read_text()))
            report = (root / "report.md").read_text()
        else:
            if not args.receipt or not args.report:
                ap.error("verify requires --receipt and --report")
            receipt = json.loads(args.receipt.read_text())
            report = args.report.read_text()
        rows = verify(report, receipt)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps({"simulated": args.command == "demo", "citations": rows}, ensure_ascii=False, indent=2))
    else:
        print(TEXT[args.lang]["title"])
        if args.command == "demo":
            print(TEXT[args.lang]["demo"])
        for row in rows:
            print(f"{row['alias']}: {row['id'] or '?'} ({TEXT[args.lang]['known'] if row['resolved'] else TEXT[args.lang]['unknown']})")
    return 1 if any(not row["resolved"] for row in rows) else 0


if __name__ == "__main__":
    raise SystemExit(main())
