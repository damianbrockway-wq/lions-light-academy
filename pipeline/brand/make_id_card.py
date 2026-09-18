#!/usr/bin/env python3
"""Fill one LLA teacher ID card and write a single-card PDF.

    python3 make_id_card.py --html teacher_id.html --name "Leah Mikkonen" \
        --photo leah.jpg --crop 120,80,1300,1535 --out /path/to/out

--crop is optional. Given, it is left,top,right,bottom in the photo's own pixels
and is FORCED to the panel's 0.811 aspect ratio (height wins). Omitted, the photo
is center-cropped to 0.811.

Verify the crop before committing: the script writes <out>/_crop_preview.jpg.
"""
import argparse, base64, io, pathlib, re, sys
from PIL import Image

RATIO = 0.86 / 1.06          # photo panel aspect, ~0.8113
PANEL = (516, 636)           # embedded PNG size


def crop_photo(path, box=None):
    im = Image.open(path).convert("RGB")
    if box:
        l, t, r, b = box
        h = b - t
        w = round(h * RATIO)
        cx = (l + r) / 2
        l, r = round(cx - w / 2), round(cx - w / 2) + w
        l = max(0, min(l, im.width - w)); r = l + w
    else:
        w = min(im.width, round(im.height * RATIO))
        h = round(w / RATIO)
        l = (im.width - w) // 2; t = (im.height - h) // 2
        r, b = l + w, t + h
    c = im.crop((l, t, r, b))
    print(f"  crop {(l, t, r, b)}  {c.size}  ratio {c.width / c.height:.4f}")
    return c


def to_b64(img):
    buf = io.BytesIO()
    img.resize(PANEL, Image.LANCZOS).save(buf, "PNG", optimize=True)
    print(f"  panel png {len(buf.getvalue()) / 1024:.0f} KB")
    return base64.b64encode(buf.getvalue()).decode()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", default="teacher_id.html")
    ap.add_argument("--name", required=True, help="must match the card's .name exactly")
    ap.add_argument("--photo")
    ap.add_argument("--crop", help="left,top,right,bottom in source pixels")
    ap.add_argument("--out", default=".")
    a = ap.parse_args()

    html = pathlib.Path(a.html).read_text()
    css = re.search(r"<style>(.*?)</style>", html, re.S).group(1)
    strips = re.findall(r'<div class="strip">.*?\n  </div>', html, re.S)
    names = [re.search(r'class="name">([^<]+)<', s).group(1) for s in strips]
    if a.name not in names:
        sys.exit(f"no card named {a.name!r}. Found: {names}")
    s = strips[names.index(a.name)]

    if a.photo:
        box = tuple(int(x) for x in a.crop.split(",")) if a.crop else None
        img = crop_photo(a.photo, box)
        outdir = pathlib.Path(a.out); outdir.mkdir(parents=True, exist_ok=True)
        img.save(outdir / "_crop_preview.jpg", quality=90)
        s = re.sub(r'<div class="photo"[^>]*>.*?</div>',
                   '<div class="photo filled"><img src="data:image/png;base64,%s" alt=""></div>'
                   % to_b64(img), s, flags=re.S)

    page = ('<!doctype html><html><head><meta charset="utf-8"><style>%s</style></head>'
            '<body><div class="sheet">%s</div></body></html>' % (css, s))
    tmp = pathlib.Path("_one.html"); tmp.write_text(page)

    from playwright.sync_api import sync_playwright
    from pypdf import PdfReader, PdfWriter
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        pg.goto("file://%s" % tmp.resolve(), wait_until="networkidle")
        pg.emulate_media(media="print")
        pg.pdf(path="_one.pdf", format="Letter", print_background=True,
               margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
        b.close()

    r = PdfReader("_one.pdf"); w = PdfWriter(); w.add_page(r.pages[0])
    w.add_metadata({"/Title": "%s — Lions Light Academy Teacher ID" % a.name,
                    "/Author": "Lions Light Academy",
                    "/Subject": "Staff identification card"})
    f = pathlib.Path(a.out) / ("LLA-Teacher-ID-%s.pdf" % a.name.replace(" ", "-"))
    with open(f, "wb") as fh:
        w.write(fh)
    print(f"  -> {f}  ({f.stat().st_size / 1024:.0f} KB)")
    for t in ("_one.html", "_one.pdf"):
        pathlib.Path(t).unlink(missing_ok=True)


if __name__ == "__main__":
    main()
