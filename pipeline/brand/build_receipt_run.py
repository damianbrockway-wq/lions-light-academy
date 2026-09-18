#!/usr/bin/env python3
"""Lions Light Academy — a pre-numbered run of supply fee receipts.

receipt.html is already the right form: family copy on top, co-op record
below, cut line between, and the plain statement that this is a participation
fee and not tax-deductible. What it is missing for a real collection day is a
number, and a hand-written number is the one that gets skipped, repeated, or
written on only one of the two halves.

So this prints the number onto both halves before it reaches the table, and
prints a log sheet carrying the same numbers. Money is running through a
personal account until LLA has its own, which makes the paper trail the only
thing separating the co-op's money from Damian's.

    python3 build_receipt_run.py [count] [start]
"""
import base64, pathlib, re, sys
from playwright.sync_api import sync_playwright
from pypdf import PdfReader, PdfWriter

COUNT = int(sys.argv[1]) if len(sys.argv) > 1 else 7
START = int(sys.argv[2]) if len(sys.argv) > 2 else 1
SPARES = 2                     # a misfill on collection day should not stop you

B = pathlib.Path("/home/claude/brand")
OUT = pathlib.Path("/home/claude/lla/pdf")
OUT.mkdir(parents=True, exist_ok=True)

LOGO_GOLD = base64.b64encode((B / "logo_gold.png").read_bytes()).decode()
SRC = (B / "receipt.html").read_text()

# the blank number rule, printed on both halves of every receipt
NUM_CSS = """
.numline{position:relative}
.numline .pre{position:absolute;left:0;right:0;bottom:1px;text-align:center;
  font-weight:800;letter-spacing:.06em;font-size:9.2pt}
"""

HEAD = """<!doctype html><html><head><meta charset="utf-8">
<style>
@font-face{font-family:'Fraunces';src:url('fonts/Fraunces.ttf') format('truetype');font-weight:100 900}
@font-face{font-family:'Inter';src:url('fonts/Inter.ttf') format('truetype');font-weight:100 900}
html{-webkit-print-color-adjust:exact;print-color-adjust:exact}
*{box-sizing:border-box}
%s
</style></head><body>%s</body></html>"""


def numbered(n):
    """One receipt page with its number printed on both halves."""
    tag = '<span class="numline"><span class="pre">%03d</span></span>' % n
    return SRC.replace("{logo}", LOGO_GOLD).replace(
        '<span class="numline"></span>', tag)


def render(body, path, extra_css=""):
    tmp = B / "_run.html"
    tmp.write_text(HEAD % (NUM_CSS + extra_css, body))
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        pg.goto("file://%s" % tmp, wait_until="networkidle")
        pg.emulate_media(media="print")
        pg.pdf(path=str(path), format="Letter", print_background=True,
               margin={"top": "14mm", "bottom": "14mm",
                       "left": "15mm", "right": "15mm"})
        b.close()
    tmp.unlink()


# ── the log sheet ────────────────────────────────────────────────────────────
LOG_CSS = """
body{font-family:'Inter',sans-serif;color:#16232F;margin:0}
.hd{display:flex;align-items:flex-start;justify-content:space-between;gap:10mm}
.lk{display:flex;align-items:center;gap:3mm}
.lk img{width:11mm}
.org{font-size:7.6pt;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:#8A6210}
.loc{font-size:6.6pt;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:#7A838E;margin-top:1px}
h1{font-family:'Fraunces',Georgia,serif;font-size:19pt;font-weight:600;margin:6mm 0 1mm}
.sub{font-size:8.6pt;color:#5A6676;max-width:120mm;line-height:1.4}
.yr{font-size:7.4pt;font-weight:700;letter-spacing:.12em;text-transform:uppercase;
  color:#7A838E;text-align:right;line-height:1.7;white-space:nowrap}
.rule{height:3px;background:#E6BD63;margin:4mm 0 0}

table{width:100%;border-collapse:collapse;margin-top:5mm}
th{font-size:6.9pt;font-weight:700;letter-spacing:.11em;text-transform:uppercase;
  color:#fff;background:#0A1929;padding:2.6mm 2mm;text-align:left}
td{border-bottom:1px solid #C4C9CE;height:11mm}
td.n{font-weight:800;font-size:10pt;color:#0A1929;text-align:center;
  background:#F7F6F2;letter-spacing:.05em}
td.sp{color:#B7BCC2;font-weight:600;font-size:8.4pt;text-align:center;background:#FCFCFB}
tr.tot td{border-bottom:none;border-top:2px solid #0A1929;height:12mm;
  font-size:8pt;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#0A1929}
tr.tot td:nth-child(4){border-bottom:1.6px solid #0A1929}

.note{margin-top:6mm;border-left:3px solid #C08A2E;padding:3mm 4mm;background:#FBF8F1;
  font-size:8.2pt;line-height:1.45;color:#3C4756}
.note b{color:#0A1929}
.foot{margin-top:6mm;display:flex;justify-content:space-between;
  font-size:7pt;letter-spacing:.08em;text-transform:uppercase;color:#9AA3AE;font-weight:600}
"""


def log_html(nums, spares):
    rows = "".join(
        '<tr><td class="n">%03d</td><td></td><td></td><td></td><td></td><td></td></tr>' % n
        for n in nums)
    rows += "".join(
        '<tr><td class="sp">%03d<br>spare</td><td></td><td></td><td></td><td></td><td></td></tr>' % n
        for n in spares)
    return """
<div class="hd">
  <div class="lk"><img src="data:image/png;base64,%(logo)s" alt="">
    <div><div class="org">Lions Light Academy</div>
    <div class="loc">Winslow, Maine</div></div></div>
  <div class="yr">Supply fees<br>2026&ndash;2027</div>
</div>
<h1>Payment Log</h1>
<p class="sub">One line per receipt, filled in as you hand each one over. The numbers
below match the printed receipts &mdash; if a number has no line here, that receipt
has not been accounted for.</p>
<div class="rule"></div>

<table>
  <tr><th style="width:15mm">No.</th><th>Family</th><th style="width:24mm">Date</th>
      <th style="width:24mm">Amount</th><th style="width:30mm">Cash / Check no.</th>
      <th style="width:28mm">Received by</th></tr>
  %(rows)s
  <tr class="tot"><td></td><td style="text-align:right;padding-right:3mm">Total collected</td>
      <td></td><td></td><td colspan="2"></td></tr>
</table>

<div class="note"><b>Check and cash only.</b> No card, no app, no Venmo.<br>
This is a participation fee, not a charitable contribution &mdash; it is
<b>not tax-deductible</b> and should not be claimed as one.<br>
Until Lions Light Academy has its own bank account these funds pass through a
personal account. <b>This sheet and the co-op halves of the receipts are the
only record that they were the co-op&rsquo;s money.</b> Keep them together.</div>

<div class="foot"><div>Lions Light Academy &middot; Tuesday Co-op 2026&ndash;2027</div>
  <div>Sheet ______ of ______</div></div>
""" % dict(logo=LOGO_GOLD, rows=rows)


def main():
    nums = list(range(START, START + COUNT))
    spares = list(range(START + COUNT, START + COUNT + SPARES))

    w = PdfWriter()
    tmp = B / "_one.pdf"

    render(log_html(nums, spares), tmp, LOG_CSS)
    r = PdfReader(str(tmp))
    assert len(r.pages) == 1, "log sheet must be one page, got %d" % len(r.pages)
    w.add_page(r.pages[0])

    for n in nums + spares:
        render(numbered(n), tmp)
        rr = PdfReader(str(tmp))
        assert len(rr.pages) == 1, "receipt %03d ran to %d pages" % (n, len(rr.pages))
        w.add_page(rr.pages[0])
    tmp.unlink()

    w.add_metadata({"/Title": "Supply Fee Receipts %03d-%03d — Lions Light Academy"
                              % (nums[0], spares[-1]),
                    "/Author": "Lions Light Academy",
                    "/Subject": "Pre-numbered supply fee receipts with payment log"})
    f = OUT / ("LLA-Supply-Fee-Receipts-%03d-%03d.pdf" % (nums[0], spares[-1]))
    with open(f, "wb") as fh:
        w.write(fh)

    print("  %s" % f.name)
    print("  %d pages = 1 log + %d receipts + %d spares"
          % (len(PdfReader(str(f)).pages), COUNT, SPARES))
    print("  numbers %03d-%03d, spares %03d-%03d  %.0f KB"
          % (nums[0], nums[-1], spares[0], spares[-1], f.stat().st_size / 1024))


if __name__ == "__main__":
    main()
