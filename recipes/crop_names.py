#!/usr/bin/env python3
"""Crop the name section from cover pages."""
from pathlib import Path
from PIL import Image

# Name row is roughly y=24..38% of the page
copies = [28, 29, 32, 35, 45]
for c in copies:
    files = list(Path("covers").glob(f"copy_{c:02d}_*.png"))
    if not files:
        print(f"copy {c}: not found")
        continue
    img = Image.open(files[0])
    W, H = img.size
    cropped = img.crop((0, int(H*0.14), W, int(H*0.27)))
    out = Path(f"covers/name_{c:02d}.png")
    cropped.save(out)
    print(f"copy {c}: {out}")
