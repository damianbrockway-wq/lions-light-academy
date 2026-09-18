#!/usr/bin/env python3
"""Cut-line overlay for LLA print sheets.

Draws the actual trim guides onto an already-merged sheet: full-bleed dashed
lines on every cut, plus solid crop ticks in the margins so the cut positions
are findable on a guillotine as well as with scissors.

The lines are drawn as a transparent vector overlay merged on top of the page,
so nothing in the card artwork has to move and the cards stay independently
rebuildable.
"""
import io
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

# A single grey dash disappears where it crosses the navy panel. Instead the
# line is drawn twice with opposite dash phases — light segments alternating
# with dark ones — so some part of it always contrasts with what is underneath.
DASH_LIGHT = HexColor("#EDF1F4")
DASH_DARK = HexColor("#5A6676")
DASH_W = 0.7
SEG = 4.5                      # pt, dash segment length
TICK = HexColor("#3C4756")
TICK_LEN = 13                  # pt, crop tick length in the margin


def overlay(pw, ph, vcuts, hcuts, margin_x=0.0, margin_y=0.0):
    """Build a one-page overlay PDF with dashed cuts and margin crop ticks.

    vcuts / hcuts are lists of x / y positions in points.
    margin_x / margin_y say how much white sits outside the artwork, so the
    ticks can be placed there rather than on top of a card.
    """
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(pw, ph))

    # ── full-bleed dashed trim lines ──────────────────────────
    c.setLineWidth(DASH_W)
    for color, phase in ((DASH_DARK, 0), (DASH_LIGHT, SEG)):
        c.setStrokeColor(color)
        c.setDash([SEG, SEG], phase)
        for x in vcuts:
            c.line(x, 0, x, ph)
        for y in hcuts:
            c.line(0, y, pw, y)

    # ── solid crop ticks, in the margins only ─────────────────
    c.setDash()
    c.setStrokeColor(TICK)
    c.setLineWidth(0.9)
    if margin_x > 0:
        for y in hcuts:                       # horizontal cut -> ticks L and R
            c.line(0, y, min(TICK_LEN, margin_x), y)
            c.line(pw - min(TICK_LEN, margin_x), y, pw, y)
    if margin_y > 0:
        for x in vcuts:                       # vertical cut -> ticks top/bottom
            c.line(x, 0, x, min(TICK_LEN, margin_y))
            c.line(x, ph - min(TICK_LEN, margin_y), x, ph)

    c.showPage(); c.save()
    buf.seek(0)
    return PdfReader(buf).pages[0]


def border(pw, ph):
    """Overlay a dashed rectangle on the page edge itself.

    For cards that already fill their whole sheet there is nothing to trim on
    press — but a home printer scales the sheet down to fit Letter with its own
    margins, and the printed card edge then lands wherever the driver put it.
    The border scales with the artwork, so it still marks the true edge.
    """
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(pw, ph))
    i = DASH_W / 2                     # inset so neither half is clipped away
    c.setLineWidth(DASH_W)
    for color, phase in ((DASH_DARK, 0), (DASH_LIGHT, SEG)):
        c.setStrokeColor(color)
        c.setDash([SEG, SEG], phase)
        c.rect(i, i, pw - DASH_W, ph - DASH_W, stroke=1, fill=0)
    c.showPage(); c.save()
    buf.seek(0)
    return PdfReader(buf).pages[0]


def stamp(src, dst, vcuts, hcuts, margin_x=0.0, margin_y=0.0, meta=None):
    """Copy src to dst with the cut overlay merged onto every page."""
    r = PdfReader(str(src))
    w = PdfWriter()
    for page in r.pages:
        pw = float(page.mediabox.width); ph = float(page.mediabox.height)
        page.merge_page(overlay(pw, ph, vcuts, hcuts, margin_x, margin_y))
        w.add_page(page)
    if meta:
        w.add_metadata(meta)
    with open(dst, "wb") as fh:
        w.write(fh)
    return len(r.pages)
