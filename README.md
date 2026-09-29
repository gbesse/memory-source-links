# Memory Source Links

**Keep short memory citations such as `f3` resolvable after the source context is gone.**

English · [Français](README.fr.md) · [Español](README.es.md)

## See the problem in one command

```sh
python3 receipt.py demo --lang en
```

The fixture resolves `f1` and `o2`, while showing that `f3` has no receipt. Exit code 1 means a citation is unresolved.

**Example output**

```text
Memory citation links
Offline fixture. Capture aliases while the source context is still available.
f1: memory-001 (resolved)
f3: ? (unresolved)
o2: observation-002 (resolved)
```

## Related projects

- [vectorize-io/hindsight](https://github.com/vectorize-io/hindsight/issues/4876) — Reports unresolved `f3/o2` aliases in a mental-model output; the issue motivates durable receipts.
- [Quarktex/citegate](https://github.com/Quarktex/citegate) — Handles broader citation provenance; this CLI only verifies a supplied memory alias map. No affiliation.

## Use it on your data

```sh
python3 receipt.py build --facts fixtures/facts.json --out receipt.json
python3 receipt.py verify --report fixtures/report.md --receipt receipt.json --lang en
```

Capture an explicit `{alias,id,source_url?,text?}` list while constructing a report; `build` stores IDs and optional text hashes, not full source text. `verify` scans a saved report for `fN`/`oN` references and shows missing aliases.

## Scope and limits

Hindsight currently does not expose a complete alias-to-ID table for the reported mental-model case; this CLI requires the caller to provide that mapping at creation time. It cannot reconstruct a lost mapping afterward and claims no automatic Hindsight integration.

## Tests

```sh
python3 -m unittest discover -s tests -v
```

Python 3.11+. MIT. No account or API key is required for the demo.
