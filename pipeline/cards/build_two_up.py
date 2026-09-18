#!/usr/bin/env python3
"""Lions Light Academy — cleanup cards, two to a page.

Each card is normally a full landscape Letter sheet. This renders every card
at 5.5in tall, then stacks two of them on a portrait Letter page so the sheet
cuts cleanly in half across the middle.

Cards are rendered to PDF individually and merged with pypdf rather than being
laid out together in one HTML document — build_set.py and build_assignments.py
define conflicting rules for .card, .panel and h1, so combining their
stylesheets in one page would silently restyle half the set.
"""
import pathlib, re, sys
from playwright.sync_api import sync_playwright
from pypdf import PdfReader, PdfWriter, PageObject, Transformation

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import build_set as BS
import build_assignments as BA
import cutlines as CL

HERE = pathlib.Path(__file__).parent
OUT = HERE / "set"; OUT.mkdir(exist_ok=True)

Z = 5.5 / 8.5                      # scale so a card is exactly half a page tall
CW, CH = 11 * Z, 8.5 * Z           # 7.118 x 5.500 in
PW, PH = 8.5 * 72, 11 * 72         # Letter portrait, points

OVERRIDE = "\n@page{size:%.4fin %.4fin;margin:0}\n.card{zoom:%.7f}\n" % (CW, CH, Z)


def card_html(full_html):
    """Inject the scaled page size and zoom into an already-built card page."""
    return full_html.replace("</style>", OVERRIDE + "</style>", 1)


def render(html, path):
    tmp = HERE / "_2up.html"; tmp.write_text(html)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        pg.goto("file://%s" % tmp.resolve(), wait_until="networkidle")
        pg.emulate_media(media="print")
        pg.pdf(path=str(path), width="%.4fin" % CW, height="%.4fin" % CH,
               print_background=True,
               margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
        b.close()
    tmp.unlink()


def build_pages():
    """Every card, in print order, as a single scaled PDF page each."""
    pages = []

    # 1. the assignments cover
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
    f = HERE / "_p00.pdf"; render(card_html(html), f)
    pages.append(("Assignments", f))

    # 2. the seven station cards
    for i, c in enumerate(BS.CARDS, 1):
        html = BS.TPL % dict(
            css=BS.CSS % dict(inter=BS.INTER, fraunces=BS.FRAUNCES),
            logo=BS.LOGO_WHITE, title=c["title"], role=c["role"], who=c["who"],
            color=c["color"], tag=c["tag"], year=BS.YEAR,
            checklabel=c.get("checklabel", "Checked by"),
            dense=" dense" if len(c["tasks"]) >= 7 else "",
            items="".join("<li>%s</li>" % t for t in c["tasks"]),
            note=('<div class="note">%s</div>' % c["note"]) if c.get("note") else "")
        f = HERE / ("_p%02d.pdf" % i); render(card_html(html), f)
        pages.append((re.sub("&amp;", "&", c["title"]), f))
    return pages


def main():
    pages = build_pages()
    print("rendered %d cards at %.3f x %.3f in" % (len(pages), CW, CH))

    w = PdfWriter()
    card_pt_w, card_pt_h = CW * 72, CH * 72
    x = (PW - card_pt_w) / 2          # centre horizontally
    sheets = 0
    for i in range(0, len(pages), 2):
        sheet = PageObject.create_blank_page(width=PW, height=PH)
        pair = pages[i:i + 2]
        for slot, (title, f) in enumerate(pair):
            pg = PdfReader(str(f)).pages[0]
            y = PH - card_pt_h if slot == 0 else PH - 2 * card_pt_h
            sheet.merge_transformed_page(pg, Transformation().translate(x, y))
        # three cuts: both side trims, and the fold-line between the two cards
        sheet.merge_page(CL.overlay(
            PW, PH,
            vcuts=[x, x + card_pt_w],
            hcuts=[PH - card_pt_h],
            margin_x=x, margin_y=PH - 2 * card_pt_h))
        w.add_page(sheet)
        sheets += 1
        print("  sheet %d: %s" % (sheets, "  +  ".join(t for t, _ in pair)))

    w.add_metadata({"/Title": "LLA Cleanup Cards — Two Per Page",
                    "/Author": "Lions Light Academy",
                    "/Subject": "Assignments cover plus seven station cards, 2 up"})
    out = OUT / "LLA-Cleanup-Cards-TWO-PER-PAGE.pdf"
    with open(out, "wb") as fh:
        w.write(fh)
    for _, f in pages:
        f.unlink()

    r = PdfReader(str(out))
    p0 = r.pages[0]
    print("\n  %s" % out.name)
    print("  %d sheets  %.2f x %.2f in  %d KB"
          % (len(r.pages), float(p0.mediabox.width) / 72,
             float(p0.mediabox.height) / 72, out.stat().st_size / 1024))
    print("  card size: %.3f x %.3f in   cut line at 5.5 in" % (CW, CH))


if __name__ == "__main__":
    main()
