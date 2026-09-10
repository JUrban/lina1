#!/usr/bin/env python3
"""Merge per-student partial JSON files into a single results JSON.

Usage:
    python3 recipes/merge_results.py <parts_dir> <output.json>

Each file in <parts_dir> must contain a JSON object with at least a "student" key
(the student key string) and any number of part keys (e.g. "6a", "6b") mapping to
{"points": N, "comment": "..."}. A "course" key is also collected if present.

Files from the same student are merged; later files overwrite earlier ones for the
same part key (so re-running a single agent overwrites only its parts).
"""
import json, sys, glob, os
from collections import defaultdict

if len(sys.argv) != 3:
    print("Usage: python3 recipes/merge_results.py <parts_dir> <output.json>")
    sys.exit(1)

parts_dir, output = sys.argv[1], sys.argv[2]
SKIP = {"student", "course", "task"}

by_student = defaultdict(dict)

for fpath in sorted(glob.glob(os.path.join(parts_dir, "*.json"))):
    with open(fpath, encoding="utf-8") as f:
        data = json.load(f)
    key = data.get("student")
    if not key:
        print(f"WARNING: {fpath} has no 'student' field — skipping")
        continue
    if "course" in data:
        by_student[key]["course"] = data["course"]
    by_student[key]["student"] = key
    for k, v in data.items():
        if k not in SKIP:
            by_student[key][k] = v

result = dict(sorted(by_student.items()))
with open(output, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"Merged {len(result)} students → {output}")
for k, v in result.items():
    parts = {p: v[p].get("points", "?") if isinstance(v[p], dict) else v[p]
             for p in v if p not in SKIP}
    print(f"  {k}: {parts}")
