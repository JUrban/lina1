#!/usr/bin/env python3
"""
Build one sorted PDF per student from <scan_dir>/pages.json.
Output: <scan_dir>/ordered/{copy}_{ascii_name}.pdf

Usage: python3 build_pdfs.py <scan_dir>
"""
import json
import re
import sys
import unicodedata
from pathlib import Path
import fitz

SCAN_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
OUT_DIR = SCAN_DIR / "ordered"
OUT_DIR.mkdir(exist_ok=True)

def to_ascii(s: str) -> str:
    normalized = unicodedata.normalize("NFKD", s)
    ascii_only = normalized.encode("ascii", "ignore").decode("ascii")
    clean = re.sub(r"[^A-Za-z0-9]+", "_", ascii_only)
    return clean.strip("_")


data = json.load(open(SCAN_DIR / "pages.json"))
pages = data["pages"]
students = data["students"]

# Build global_page → (pdf_path, 0-based local index)
pdfs = sorted(SCAN_DIR.glob("*.pdf"))
mapping: dict[int, tuple[Path, int]] = {}
offset = 0
for pdf_path in pdfs:
    n = len(fitz.open(str(pdf_path)))
    for i in range(n):
        mapping[offset + i + 1] = (pdf_path, i)
    offset += n

# Group pages by copy key: copy_key → [(exam_page, global_page), ...]
copy_pages: dict[str, list[tuple[int, int]]] = {}
for global_str, entry in pages.items():
    if entry is None or "duplicate" in entry:
        continue
    key = str(entry["copy"])
    copy_pages.setdefault(key, []).append((entry["page"], int(global_str)))

for key in copy_pages:
    copy_pages[key].sort()

# Sort students: numbered copies first (by int), then VB
def sort_key(item):
    k = item[0]
    return (0, int(k)) if k.isdigit() else (1, k)

missing_students = []
for copy_key, name in sorted(students.items(), key=sort_key):
    pages_list = copy_pages.get(copy_key)
    if not pages_list:
        missing_students.append(copy_key)
        print(f"  SKIP {copy_key} ({name}): no pages found")
        continue

    prefix = f"{int(copy_key):03d}" if copy_key.isdigit() else copy_key
    out_path = OUT_DIR / f"{prefix}_{to_ascii(name)}.pdf"

    out_doc = fitz.open()
    for exam_page, global_page in pages_list:
        pdf_path, page_idx = mapping[global_page]
        src = fitz.open(str(pdf_path))
        out_doc.insert_pdf(src, from_page=page_idx, to_page=page_idx)
        src.close()

    out_doc.save(str(out_path))
    out_doc.close()
    print(f"  {out_path.name}  ({len(pages_list)} pages)")
