#!/usr/bin/env python3
"""Render one page of a PDF to PNG.

Usage: python3 pdf2png.py <pdf_file> <page> [dpi] [outfile]

  pdf_file  path to a PDF (relative or absolute)
  page      1-based page number
  dpi       resolution in dots per inch (default: 150)
  outfile   optional output path (default: ./<stem>_p<page>.png)

Output: outfile if given, else ./<stem>_p<page>.png (current directory)
"""
import subprocess
import sys
from pathlib import Path

if len(sys.argv) < 3:
    print(__doc__)
    sys.exit(1)

pdf = Path(sys.argv[1]).resolve()
page = int(sys.argv[2])
dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 150

if len(sys.argv) > 4:
    out = Path(sys.argv[4])
    out.parent.mkdir(parents=True, exist_ok=True)
else:
    out = Path(f"{pdf.stem}_p{page:02d}.png")

subprocess.run(
    [
        "gs", "-q", "-dBATCH", "-dNOPAUSE", "-dSAFER",
        "-sDEVICE=png16m", f"-r{dpi}",
        f"-dFirstPage={page}", f"-dLastPage={page}",
        f"-sOutputFile={out}",
        str(pdf),
    ],
    check=True,
)
print(out)
