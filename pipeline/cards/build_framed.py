#!/usr/bin/env python3
"""Lions Light Academy — cleanup cards, full size, framed for lamination.

One card per landscape Letter sheet, no cut lines. The card is scaled slightly
and centred so it sits inside a white margin, with a solid navy rule on its
edge. Nothing is trimmed — the whole sheet goes in the pouch — so the frame is
there to finish the card, and to keep the cream field from bleeding into the
white of the paper.

The margin is wider than any desktop printer's unprintable edge, so the frame
prints whole on all four sides rather than being clipped on one.
"""
import pathlib, re, sys, io
from playwright.sync_api import sync_playwright
from pypdf import PdfReader, PdfWriter, PageObject, Transformation
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import build_set as BS
import build_assignments as BA

HERE = pathlib.Path(__file__).parent
OUT = HERE / "set"; OUT.mkdir(exist_ok=True)

Z = 0.93                           # leaves ~0.385in of white on every side
CW, CH = 11 * Z, 8.5 * Z           # 10.230 x 7.905 in
PW, PH = 11 * 72, 8.5 * 72         # Letter landscape, points

FRAME = HexColor("#0A1929")
FRAME_W = 1.5
# The rule is drawn just OUTSIDE the card rather than on its edge. Drawn on the
# edge it vanishes wherever it meets the navy header — dark on dark — and only
# appears alongside the cream. Held off in the white margin it reads the whole
# way round, and the thin white gap frames the card properly.
FRAME_GAP = 7.0                    # pt of white between card edge and rule

OVERRIDE = "\n@page{size:%.4fin %.4fin;margin:0}\n.card{zoom:%.7f}\n" % (CW, CH, Z)


def render(html, path):
    """Render one already-built card page at the reduced size."""
    tmp = HERE / "_framed.html"
    tmp.write_text(html.replace("</style>", OVERRIDE + "</style>", 1))
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        pg.goto("file://%s" % tmp.resolve(), wait_until="networkidle")
        pg.emulate_media(media="print")
        pg.pdf(path=str(path), width="%.4fin" % CW, height="%.4fin" % CH,
               print_background=True,
               margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
        b.close()
    tmp.unlink()


def frame_overlay(x, y, w, h):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(PW, PH))
    c.setStrokeColor(FRAME)
    c.setLineWidth(FRAME_W)
    g = FRAME_GAP
    c.rect(x - g, y - g, w + 2 * g, h + 2 * g, stroke=1, fill=0)
    c.showPage(); c.save()
    buf.seek(0)
    return PdfReader(buf).pages[0]


def sheet_for(card_pdf):
    """Centre one scaled card on a full landscape page and frame it."""
    cw, ch = CW * 72, CH * 72
    x, y = (PW - cw) / 2, (PH - ch) / 2
    page = PageObject.create_blank_page(width=PW, height=PH)
    page.merge_transformed_page(PdfReader(str(card_pdf)).pages[0],
                                Transformation().translate(x, y))
    page.merge_page(frame_overlay(x, y, cw, ch))
    return page


def build_pages():
    pages = []

    blocks = []
    for name, lead, color, kids, later in BA.STATIONS:
        blocks.append(BA.ST % dict(
            color=color, name=name, lead=lead,
            leadlbl="Room Leads" if "&amp;" in lead else "Room Lead",
            kids=" &middot; ".join(kids),
            later=('<div class="later">+ %s &mdash; after bathroom</div>'
                   % " &middot; ".join(later)) if later else ""))
    html = BA.TPL % dict(css=BA.CSS % dict(inter=BA.INTER, fraunces=BA.FRAUNCES),
                         logo=BA.LOGO_WHITE, stations="".join(blocks))
    f = HERE / "_f00.pdf"; render(html, f)
    pages.append(("ASSIGNMENTS", f))

    for i, c in enumerate(BS.CARDS, 1):
        html = BS.TPL % dict(
            css=BS.CSS % dict(inter=BS.INTER, fraunces=BS.FRAUNCES),
            logo=BS.LOGO_WHITE, title=c["title"], role=c["role"], who=c["who"],
            color=c["color"], tag=c["tag"], year=BS.YEAR,
            checklabel=c.get("checklabel", "Checked by"),
            dense=" dense" if len(c["tasks"]) >= 7 else "",
            items="".join("<li>%s</li>" % t for t in c["tasks"]),
            note=('<div class="note">%s</div>' % c["note"]) if c.get("note") else "")
        f = HERE / ("_f%02d.pdf" % i); render(html, f)
        pages.append((c["slug"], f))
    return pages


def main():
    pages = build_pages()
    print("Framed cleanup cards — %.3f x %.3f in card on %g x %g in sheet"
          % (CW, CH, PW / 72, PH / 72))

    allw = PdfWriter()
    for slug, f in pages:
        page = sheet_for(f)
        allw.add_page(page)

        one = PdfWriter(); one.add_page(sheet_for(f))
        plain = re.sub("&amp;", "&", slug)
        one.add_metadata({"/Title": "%s — LLA Cleanup Card (framed)" % plain,
                          "/Author": "Lions Light Academy",
                          "/Subject": "Tuesday co-op cleanup card, laminate"})
        p = OUT / ("LLA-Cleanup-LAMINATE-%s.pdf" % slug)
        with open(p, "wb") as fh:
            one.write(fh)
        print("  %-46s %5.0f KB" % (p.name, p.stat().st_size / 1024))
        f.unlink()

    allw.add_metadata({"/Title": "LLA Cleanup Cards — Laminate Set 2026-2027",
                       "/Author": "Lions Light Academy",
                       "/Subject": "Eight cards, one per page, framed for lamination"})
    out = OUT / "LLA-Cleanup-Cards-LAMINATE.pdf"
    with open(out, "wb") as fh:
        allw.write(fh)
    r = PdfReader(str(out))
    print("\n  %s\n  %d pages  %.2f x %.2f in  %.0f KB"
          % (out.name, len(r.pages), float(r.pages[0].mediabox.width) / 72,
             float(r.pages[0].mediabox.height) / 72, out.stat().st_size / 1024))
    print("  margin outside the frame: %.3f in" % ((11 - CW) / 2))


if __name__ == "__main__":
    main()
