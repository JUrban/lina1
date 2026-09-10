#!/usr/bin/env python3
"""Check which students are missing results in a parts directory.

Usage:
    python3 recipes/check_progress.py <parts_dir> <expected_keys.json>

<expected_keys.json> must be a JSON file containing either:
  - a list of student key strings, or
  - an object whose keys are student keys (e.g. the merged results file).

Prints which students have no files at all, and which have only partial results.
"""
import json, sys, glob, os
from collections import defaultdict

if len(sys.argv) != 3:
    print("Usage: python3 recipes/check_progress.py <parts_dir> <expected_keys.json>")
    sys.exit(1)

parts_dir, keys_file = sys.argv[1], sys.argv[2]

with open(keys_file, encoding="utf-8") as f:
    raw = json.load(f)
expected = list(raw) if isinstance(raw, (dict,)) else raw

SKIP = {"student", "course", "task"}
found = defaultdict(set)

for fpath in sorted(glob.glob(os.path.join(parts_dir, "*.json"))):
    with open(fpath, encoding="utf-8") as f:
        data = json.load(f)
    key = data.get("student")
    if not key:
        continue
    for k in data:
        if k not in SKIP:
            found[key].add(k)

missing_all = [k for k in expected if k not in found]
partial = [(k, found[k]) for k in expected if k in found]

if missing_all:
    print(f"MISSING ({len(missing_all)} students with no files):")
    for k in missing_all:
        print(f"  {k}")
else:
    print("All expected students have at least one result file.")

all_parts = sorted({p for parts in found.values() for p in parts})
if all_parts and partial:
    incomplete = [(k, ps) for k, ps in partial if ps != set(all_parts)]
    if incomplete:
        print(f"\nINCOMPLETE ({len(incomplete)} students missing some parts, full set is {all_parts}):")
        for k, ps in incomplete:
            missing_parts = sorted(set(all_parts) - ps)
            print(f"  {k}: missing {missing_parts}")
    else:
        print(f"All present students have all parts: {all_parts}")
