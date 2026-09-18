#!/usr/bin/env python3
"""Add cut borders and a fold line to the teacher ID cards.

teacher_id.html puts a CSS `outline` around each strip, but it is a single
flat grey — it reads against the cream back face and disappears against the
navy front, which is exactly the edge you need when cutting. This replaces it
with the same alternating light/dark dash used on the cleanup cards, and adds
the fold line down the middle of the strip, which was never marked at all.

Strip positions are detected from a render of each page rather than assumed,
so this keeps working if the cards are rebuilt at a different scale.
"""
import pathlib, subprocess, sys, tempfile
from PIL import Image
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
import io

sys.path.insert(0, "/home/claude/lla-cards")
import cutlines as CL

PDF = pathlib.Path("/home/claude/lla/pdf")
DPI = 150


def strips_on(page_png, pw, ph):
    """Find each card strip on a rendered page. Returns rects in PDF points."""
    img = Image.open(page_png).convert("RGB")
    px = img.load()
    W, H = img.size
    ink = lambda c: not (c[0] > 242 and c[1] > 242 and c[2] > 242)

    rows = []
    for y in range(H):
        rows.append(any(ink(px[x, y]) for x in range(0, W, 3)))

    bands, start = [], None
    for y, on in enumerate(rows + [False]):
        if on and start is None:
            start = y
        elif not on and start is not None:
            if y - start > 20:                 # ignore stray marks
                bands.append((start, y))
            start = None

    rects = []
    for y0, y1 in bands:
        xs = [x for x in range(W)
              if any(ink(px[x, y]) for y in range(y0, y1, 3))]
        if not xs:
            continue
        x0, x1 = min(xs), max(xs) + 1
        # image pixels -> PDF points, flipping the y axis
        rects.append((x0 / W * pw, ph - y1 / H * ph,
                      (x1 - x0) / W * pw, (y1 - y0) / H * ph))
    return rects


def overlay_for(rects, pw, ph):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(pw, ph))
    c.setLineWidth(CL.DASH_W)
    for color, phase in ((CL.DASH_DARK, 0), (CL.DASH_LIGHT, CL.SEG)):
        c.setStrokeColor(color)
        c.setDash([CL.SEG, CL.SEG], phase)
        for x, y, w, h in rects:
            c.rect(x, y, w, h, stroke=1, fill=0)
            c.line(x + w / 2, y, x + w / 2, y + h)   # fold, between the faces
    c.showPage(); c.save()
    buf.seek(0)
    return PdfReader(buf).pages[0]


def stamp(path):
    r = PdfReader(str(path))
    meta = r.metadata
    w = PdfWriter()
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(["pdftoppm", "-png", "-r", str(DPI), str(path), d + "/p"],
                       check=True, stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)
        pngs = sorted(pathlib.Path(d).glob("*.png"))
        for page, png in zip(r.pages, pngs):
            pw, ph = float(page.mediabox.width), float(page.mediabox.height)
            rects = strips_on(png, pw, ph)
            page.merge_page(overlay_for(rects, pw, ph))
            w.add_page(page)
    w.add_metadata(meta or {})
    with open(path, "wb") as fh:
        w.write(fh)
    return len(r.pages), rects


if __name__ == "__main__":
    print("Stamping teacher ID cut lines...")
    for f in sorted(PDF.glob("LLA-Teacher-ID-*.pdf")):
        n, rects = stamp(f)
        sz = ("%.2f x %.2f in" % (rects[0][2] / 72, rects[0][3] / 72)) if rects else "-"
        print("  %-46s %d page  %2d strip(s)  %s" % (f.name, n, len(rects), sz))
