#!/usr/bin/env python3
"""Lions Light Academy — the opening prayer, one page.

Damian's words, set to be read aloud. Verbatim: nothing added, nothing
rephrased, no Amen appended. The only editorial act is the line breaking,
which follows the natural breath of each sentence so he can look up at the
room between lines and find his place again when he looks back down.

Portrait Letter, exactly one page, same brand system as the rest of the set.
"""
import base64, pathlib
from playwright.sync_api import sync_playwright
from pypdf import PdfReader, PdfWriter

HERE = pathlib.Path(__file__).parent
OUT = HERE / "set"; OUT.mkdir(exist_ok=True)
FONTS = pathlib.Path("/home/claude/brand/fonts")
b64 = lambda p: base64.b64encode(pathlib.Path(p).read_bytes()).decode()
LOGO_WHITE = b64("/home/claude/brand/logo_white.png")
INTER = b64(FONTS / "Inter.ttf")
FRAUNCES = b64(FONTS / "Fraunces.ttf")

# His words. Only "LLA" spelled out, at his request; line breaks otherwise.
PRAYER = [
    ["God I ask that you guide all teachers and students",
     "as well as their families to paths of revelation."],
    ["Help us all to draw closer to you and each other."],
    ["Let us go deeper than we ever have."],
    ["Fill us all with your Spirit."],
    ["Let this be a year of building, encouragement,",
     "prayer and fulfillment."],
    ["We love you Jesus."],
    ["Let Lions Light Academy be blessed in your name!"],
]

HTML = """<!doctype html><html><head><meta charset="utf-8">
<title>Opening Prayer</title><style>
@font-face{font-family:'Inter';src:url(data:font/ttf;base64,%(inter)s) format('truetype');font-weight:100 900}
@font-face{font-family:'Fraunces';src:url(data:font/ttf;base64,%(fraunces)s) format('truetype');font-weight:100 900}
@page{size:Letter portrait;margin:0}
*{box-sizing:border-box;margin:0;padding:0;-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{font-family:'Inter',sans-serif;color:#16232F;background:#F7F6F2;
  width:8.5in;height:11in;display:flex;flex-direction:column}

.panel{background:#0A1929;color:#F2F5F8;padding:0.46in 0.82in 0.40in;position:relative}
.lockup{display:flex;align-items:center;gap:9px}
.lockup img{width:0.38in}
.lockup .txt{display:flex;flex-direction:column;line-height:1.15}
.org{font-size:8pt;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:#E6BD63}
.loc{font-size:7pt;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:#8FA3B8;margin-top:1px}
h1{font-family:'Fraunces',Georgia,serif;font-size:31pt;font-weight:600;
  line-height:1.02;letter-spacing:-.015em;margin-top:0.24in}
.when{position:absolute;right:0.82in;top:0.54in;font-size:7.8pt;font-weight:600;
  letter-spacing:.12em;text-transform:uppercase;color:#8FA3B8;text-align:right;line-height:1.5}
.bar{height:0.14in;background:#E6BD63}

.body{flex:1;padding:0.86in 0.82in 0;display:flex;flex-direction:column;
  justify-content:flex-start}
p{font-family:'Fraunces',Georgia,serif;font-size:19.5pt;font-weight:400;
  line-height:1.44;margin-bottom:0.34in;max-width:6.5in}
p:last-child{margin-bottom:0}
p span{display:block}
p.last{color:#0A1929;font-weight:600}

.mark{margin:0 0.82in;height:2px;width:1.1in;background:#E6BD63}
.foot{margin:0.26in 0.82in 0;padding-bottom:0.46in;
  display:flex;justify-content:space-between;align-items:flex-end;
  font-size:7.6pt;letter-spacing:.09em;text-transform:uppercase;
  color:#8A94A0;font-weight:600}
.foot .r{text-align:right;font-style:normal}
</style></head><body>

<div class="panel">
  <div class="lockup"><img src="data:image/png;base64,%(logo)s" alt="">
    <div class="txt"><span class="org">Lions Light Academy</span>
    <span class="loc">Winslow, Maine</span></div></div>
  <div class="when">First Day<br>15 September 2026</div>
  <h1>Opening Prayer</h1>
</div>
<div class="bar"></div>

<div class="body">
%(prayer)s
</div>

<div class="mark"></div>
<div class="foot">
  <div>Prayed the night before &middot; 14 September 2026</div>
  <div class="r">Tuesday Co-op &middot; 2026&ndash;2027</div>
</div>
</body></html>"""


def build():
    blocks = []
    for i, lines in enumerate(PRAYER):
        cls = ' class="last"' if i == len(PRAYER) - 1 else ""
        blocks.append("  <p%s>%s</p>"
                      % (cls, "".join("<span>%s</span>" % l for l in lines)))
    src = HERE / "_prayer.html"
    src.write_text(HTML % dict(inter=INTER, fraunces=FRAUNCES, logo=LOGO_WHITE,
                               prayer="\n".join(blocks)))
    raw = HERE / "_pr.pdf"
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        pg.goto("file://%s" % src.resolve(), wait_until="networkidle")
        pg.emulate_media(media="print")
        pg.pdf(path=str(raw), width="8.5in", height="11in", print_background=True,
               margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
        b.close()
    r = PdfReader(str(raw))
    assert len(r.pages) == 1, "MUST be one page, got %d" % len(r.pages)
    w = PdfWriter(); w.add_page(r.pages[0])
    w.add_metadata({"/Title": "Opening Prayer — Lions Light Academy",
                    "/Author": "Damian Brockway",
                    "/Subject": "First day opening prayer, 15 September 2026"})
    f = OUT / "LLA-Opening-Prayer.pdf"
    with open(f, "wb") as fh:
        w.write(fh)
    print("  %s  %d page  %.0f KB" % (f.name, len(r.pages), f.stat().st_size / 1024))
    src.unlink(); raw.unlink()


if __name__ == "__main__":
    build()
