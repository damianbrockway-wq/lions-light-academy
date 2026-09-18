#!/usr/bin/env python3
"""Rebuild the LLA teacher ID cards at a reduced size.

teacher_id.html hard-codes the card geometry, so rather than touch every
measurement this applies CSS `zoom` to .strip. Unlike `transform: scale`,
zoom shrinks the layout box too, so the three-per-sheet stacking still works.

The rendered card is measured out of the PDF afterwards — not assumed.
"""
import re, sys, pathlib
from playwright.sync_api import sync_playwright
from pypdf import PdfReader, PdfWriter

SCALE = float(sys.argv[1]) if len(sys.argv) > 1 else 0.90
LABEL = sys.argv[2] if len(sys.argv) > 2 else ""

HERE = pathlib.Path("/home/claude/brand")
OUT = pathlib.Path("/home/claude/lla/pdf"); OUT.mkdir(parents=True, exist_ok=True)
SRC = HERE / "teacher_id.html"

html = SRC.read_text()
css = re.search(r"<style>(.*?)</style>", html, re.S).group(1)
strips = re.findall(r'<div class="strip">.*?\n  </div>', html, re.S)
names = [re.search(r'class="name">([^<]+)<', s).group(1) for s in strips]

# zoom shrinks both the painted card and the box it occupies
css_scaled = css + "\n.strip{zoom:%s}\n" % SCALE

PAGE = ('<!doctype html><html><head><meta charset="utf-8"><title>%s</title>'
        '<style>%s</style></head><body><div class="sheet">%s</div></body></html>')


def render(body, title, out_path, meta):
    tmp = HERE / "_scaled.html"
    tmp.write_text(PAGE % (title, css_scaled, body))
    raw = HERE / "_scaled.pdf"
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        pg.goto("file://%s" % tmp.resolve(), wait_until="networkidle")
        pg.emulate_media(media="print")
        pg.pdf(path=str(raw), format="Letter", print_background=True,
               margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
        b.close()
    r = PdfReader(str(raw)); w = PdfWriter()
    for page in r.pages:
        w.add_page(page)
    w.add_metadata(meta)
    with open(out_path, "wb") as fh:
        w.write(fh)
    tmp.unlink(); raw.unlink()
    return len(r.pages)


def measure(pdf_path):
    """Find the navy card block in a rendered page and report its size in inches."""
    import subprocess, tempfile
    from PIL import Image
    dpi = 200
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(["pdftoppm", "-png", "-r", str(dpi), "-f", "1", "-l", "1",
                        str(pdf_path), d + "/p"], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        img = Image.open(next(pathlib.Path(d).glob("*.png"))).convert("RGB")
    px = img.load()
    ink = lambda c: not (c[0] > 245 and c[1] > 245 and c[2] > 245)
    xs, ys = [], []
    for y in range(0, img.height, 2):
        for x in range(0, img.width, 2):
            if ink(px[x, y]):
                xs.append(x); ys.append(y)
    if not xs:
        return None
    # full strip bounding box = front + back side by side
    return (max(xs) - min(xs) + 2) / dpi, (max(ys) - min(ys) + 2) / dpi


if __name__ == "__main__":
    print("Rebuilding teacher IDs at %d%%..." % (SCALE * 100))
    n = render("\n".join(strips), "Lions Light Academy Teacher ID Cards",
               OUT / ("LLA-Teacher-ID-Cards-2026-2027%s.pdf" % LABEL),
               {"/Title": "Lions Light Academy Teacher ID Cards 2026-2027",
                "/Author": "Lions Light Academy",
                "/Subject": "Staff identification cards"})
    print("  full set: %d pages" % n)

    for name, strip in zip(names, strips):
        if "photo filled" not in strip:
            continue
        slug = name.replace(" ", "-")
        f = OUT / ("LLA-Teacher-ID-%s%s.pdf" % (slug, LABEL))
        render(strip, "%s - Lions Light Academy Teacher ID" % name, f,
               {"/Title": "%s — Lions Light Academy Teacher ID" % name,
                "/Author": "Lions Light Academy",
                "/Subject": "Staff identification card, 2026-2027"})
        print("  %-34s %4.0f KB" % (f.name, f.stat().st_size / 1024))

    w, h = measure(OUT / ("LLA-Teacher-ID-Damian-Brockway%s.pdf" % LABEL))
    print("\n  measured strip      : %.3f x %.3f in" % (w, h))
    print("  folded card         : %.3f x %.3f in" % (w / 2, h))
    print("  credit card (CR80)  : 3.370 x 2.125 in")
