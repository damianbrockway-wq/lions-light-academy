# -*- coding: utf-8 -*-
"""Add a clickable 'Back to Lions Light Academy' link to every page of a PDF.
Preserves the original AcroForm fields by adding URL link annotations
rather than merging content."""
import sys
from pypdf import PdfReader, PdfWriter
from pypdf.annotations import Link
from pypdf.generic import Fit
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from io import BytesIO

SITE_URL = "https://lions-light-academy.pages.dev"


def make_overlay_for_page(width, height):
    """Single-page overlay PDF with just the visible text in the footer."""
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=(width, height))
    c.setFont("Helvetica-Bold", 8.5)
    c.setFillColor(HexColor("#1565C0"))
    text = "← Back to Lions Light Academy"
    x = 0.75 * 72   # 0.75 inch from left
    y = 0.4 * 72    # 0.4 inch from bottom
    c.drawString(x, y, text)
    c.showPage(); c.save()
    buf.seek(0)
    return buf, x, y, c.stringWidth(text, "Helvetica-Bold", 8.5)


def stamp(input_path, output_path):
    # Clone the original (preserves AcroForm, fields, everything)
    writer = PdfWriter(clone_from=input_path)

    # Add visible text + URL annotation on each page
    reader = PdfReader(input_path)
    for i, src_page in enumerate(reader.pages):
        w = float(src_page.mediabox.width)
        h = float(src_page.mediabox.height)
        buf, x, y, tw = make_overlay_for_page(w, h)
        # Merge overlay content into the cloned page
        ov_reader = PdfReader(buf)
        writer.pages[i].merge_page(ov_reader.pages[0])
        # Add a URL link annotation over the text rectangle
        link = Link(
            rect=(x, y - 3, x + tw, y + 13),
            url=SITE_URL,
        )
        writer.add_annotation(page_number=i, annotation=link)

    with open(output_path, "wb") as f:
        writer.write(f)
    print(f"WROTE {output_path}  ({len(reader.pages)} pages stamped)")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: add_back_link.py INPUT OUTPUT"); sys.exit(1)
    stamp(sys.argv[1], sys.argv[2])
