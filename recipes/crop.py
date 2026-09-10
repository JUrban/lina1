#!/usr/bin/env python3
"""Crop a region from a PNG image using percentage coordinates.

Usage: python3 crop.py <png_file> <x%> <y%> <w%> <h%>

  png_file  path to input PNG
  x%        left edge, 0-100 (percent of image width)
  y%        top edge, 0-100 (percent of image height)
  w%        crop width, 1-100 (percent of image width)
  h%        crop height, 1-100 (percent of image height)

Output: ./<stem>_crop.png  (in the current working directory)

Examples:
  Top half of page:     python3 crop.py page.png 0 0 100 50
  Bottom half:          python3 crop.py page.png 0 50 100 50
  Top-right quarter:    python3 crop.py page.png 50 0 50 50
  Middle strip (30-70%): python3 crop.py page.png 0 30 100 40
"""
import sys
from pathlib import Path
from PIL import Image

if len(sys.argv) != 6:
    print(__doc__)
    sys.exit(1)

src = Path(sys.argv[1])
x_pct = float(sys.argv[2])
y_pct = float(sys.argv[3])
w_pct = float(sys.argv[4])
h_pct = float(sys.argv[5])

img = Image.open(src)
W, H = img.size

left   = int(W * x_pct / 100)
top    = int(H * y_pct / 100)
right  = int(W * (x_pct + w_pct) / 100)
bottom = int(H * (y_pct + h_pct) / 100)

cropped = img.crop((left, top, right, bottom))
out = Path(f"{src.stem}_crop.png")
cropped.save(out)
print(out)
