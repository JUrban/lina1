#!/usr/bin/env python3
"""Render homework attachments into one review image per submission.

Usage:
    /tmp/grading-venv/bin/python sovicka/render_submissions.py \
        sovicka/to_eval/du11_2.json /tmp/review/du11_2

PDF pages are rasterized in source order. Image attachments are EXIF-rotated,
and all pages belonging to one student are stacked vertically with labels.
The script is deliberately presentation-only: it never alters source files.
"""

from __future__ import annotations

import argparse
import io
import json
from pathlib import Path

import pymupdf
from PIL import Image, ImageDraw, ImageFont, ImageOps


MAX_WIDTH = 1600
PDF_DPI = 150
GAP = 18
LABEL_HEIGHT = 44


def normalize(image: Image.Image) -> Image.Image:
    image = ImageOps.exif_transpose(image).convert("RGB")
    if image.width > MAX_WIDTH:
        height = round(image.height * MAX_WIDTH / image.width)
        image = image.resize((MAX_WIDTH, height), Image.Resampling.LANCZOS)
    return image


def attachment_pages(path: Path) -> list[Image.Image]:
    if path.suffix.lower() == ".pdf":
        doc = pymupdf.open(path)
        scale = PDF_DPI / 72
        matrix = pymupdf.Matrix(scale, scale)
        result = []
        for page in doc:
            pix = page.get_pixmap(matrix=matrix, alpha=False)
            result.append(normalize(Image.open(io.BytesIO(pix.tobytes("png")))))
        return result
    if path.suffix.lower() in {".jpg", ".jpeg", ".png"}:
        return [normalize(Image.open(path))]
    return []


def add_label(image: Image.Image, label: str) -> Image.Image:
    canvas = Image.new("RGB", (image.width, image.height + LABEL_HEIGHT), "white")
    canvas.paste(image, (0, LABEL_HEIGHT))
    draw = ImageDraw.Draw(canvas)
    draw.text((12, 12), label, fill="black", font=ImageFont.load_default())
    return canvas


def stack(images: list[Image.Image]) -> Image.Image:
    width = max(image.width for image in images)
    height = sum(image.height for image in images) + GAP * (len(images) - 1)
    canvas = Image.new("RGB", (width, height), "#d8d8d8")
    y = 0
    for image in images:
        canvas.paste(image, ((width - image.width) // 2, y))
        y += image.height + GAP
    return canvas


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_json", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()

    data = json.loads(args.input_json.read_text(encoding="utf-8"))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for student, entry in data.items():
        pages: list[Image.Image] = []
        for message_index, message in enumerate(entry.get("solution", []), start=1):
            attachment = message.get("attachment")
            if not attachment:
                continue
            path = Path(attachment)
            rendered = attachment_pages(path)
            for page_index, image in enumerate(rendered, start=1):
                label = f"student {student} | message {message_index} | {path.name} | page {page_index}/{len(rendered)}"
                pages.append(add_label(image, label))
        if pages:
            stack(pages).save(args.output_dir / f"{student}.jpg", quality=92)


if __name__ == "__main__":
    main()
