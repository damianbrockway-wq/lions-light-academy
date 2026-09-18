#!/usr/bin/env python3
"""Lions Light Academy — cleanup assignments card.

The cover sheet for the seven room cards: where every child goes when the
last class ends. Same brand system, same landscape Letter format.
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

# (station, lead, colour, [names], [names arriving later])
STATIONS = [
    ("Gray Classroom", "Damian", "#8E9AA8",
     ["Cohen", "Nate", "Gideon"], []),
    ("Yellow Classroom", "Erika", "#E8C54A",
     ["Helen", "Noah", "Abi", "Aria", "Savannah H."], ["Abel"]),
    ("Main Room &amp; Hallways", "Jess &amp; Ginny", "#86A96E",
     ["Adalie", "Jack", "Elaine", "Sarah H.", "Madi", "A.J.", "Faith", "Naomi"],
     ["Memphis", "Jaxxson", "Riley"]),
    ("Boys Bathroom", "Damian", "#6E9BC4",
     ["Abel", "Jaxxson"], []),
    ("Girls Bathroom", "Erika", "#C98BA0",
     ["Memphis", "Riley"], []),
    ("Teacher Lounge &amp; Outside", "Leah", "#E0A574",
     ["Tirzah", "Sarah F.", "Grace"], []),
]

CSS = """
@font-face{font-family:'Inter';src:url(data:font/ttf;base64,%(inter)s) format('truetype');font-weight:100 900}
@font-face{font-family:'Fraunces';src:url(data:font/ttf;base64,%(fraunces)s) format('truetype');font-weight:100 900}
@page{size:Letter landscape;margin:0}
*{box-sizing:border-box;margin:0;padding:0;-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{font-family:'Inter',sans-serif;color:#16232F}
.card{width:11in;height:8.5in;display:flex;flex-direction:column;background:#F7F6F2}

.panel{background:#0A1929;color:#F2F5F8;padding:0.34in 0.60in 0.32in;position:relative}
.lockup{display:flex;align-items:center;gap:9px}
.lockup img{width:0.36in}
.org{font-size:7.8pt;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:#E6BD63}
.loc{font-size:6.8pt;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:#8FA3B8;margin-top:1px}
.lockup .txt{display:flex;flex-direction:column;line-height:1.16}
h1{font-family:'Fraunces',Georgia,serif;font-size:27pt;font-weight:600;line-height:1.05;margin-top:0.15in}
.steps{position:absolute;right:0.60in;top:0.40in;text-align:right;font-size:9.2pt;
  line-height:1.62;color:#C6D2DF}
.steps b{color:#E6BD63;font-weight:700}

.grid{flex:1;display:grid;grid-template-columns:repeat(3,1fr);gap:0.24in 0.17in;
  grid-auto-rows:min-content;align-content:center;padding:0.10in 0.60in}
.st{background:#fff;border:1px solid #E3E0D8;border-radius:3px;overflow:hidden;
  display:flex;flex-direction:column}
.st .chip{height:0.155in}
.st .in{padding:0.15in 0.18in 0.18in}
.st h2{font-family:'Fraunces',Georgia,serif;font-size:14.4pt;font-weight:600;line-height:1.1}
.st .lead{font-size:7.4pt;font-weight:700;letter-spacing:.12em;text-transform:uppercase;
  color:#8A6210;margin-top:4px}
.st .kids{font-size:12.4pt;line-height:1.48;margin-top:8px;color:#22303F}
.st .later{font-size:10pt;line-height:1.4;margin-top:6px;color:#6C7784;font-style:italic}

.foot{background:#0A1929;color:#C6D2DF;padding:0.22in 0.60in 0.24in;display:flex;gap:0.5in;
  align-items:flex-start}
.foot .ste{flex:1.55;font-size:9.6pt;line-height:1.52}
.foot .ste b{color:#E6BD63}
.foot .vac{flex:1;font-size:9pt;line-height:1.5;border-left:1px solid #24384F;padding-left:0.42in}
.foot .vac .h{font-size:7.4pt;font-weight:700;letter-spacing:.13em;text-transform:uppercase;
  color:#E6BD63;display:block;margin-bottom:4px}
.foot .vac code{font-family:'Inter',sans-serif;color:#F2F5F8;font-weight:600}
"""

TPL = """<!doctype html><html><head><meta charset="utf-8">
<title>Cleanup Assignments</title><style>%(css)s</style></head><body>
<div class="card">
  <div class="panel">
    <div class="lockup"><img src="data:image/png;base64,%(logo)s" alt="">
      <div class="txt"><span class="org">Lions Light Academy</span>
      <span class="loc">Winslow, Maine</span></div></div>
    <div class="steps">
      <b>1.</b> Belongings neatly along the entryway wall<br>
      <b>2.</b> Go straight to your cleaning station<br>
      <b>3.</b> Stay with your Room Lead until told otherwise
    </div>
    <h1>Where do I go after my last class?</h1>
  </div>
  <div class="grid">%(stations)s</div>
  <div class="foot">
    <div class="ste"><b>Stewardship.</b> This building isn&rsquo;t ours. The rooms, the tables,
      the floors we just learned on &mdash; all of it was lent to us. Cleaning well is how we
      say thank you, and how we look after whoever walks in after we leave.
      <b>Leave every space better than we found it.</b></div>
    <div class="vac"><span class="h">Vacuum &mdash; one route, no waiting</span>
      <code>Yellow</code> &rarr; <code>Gray</code> &rarr; <code>Main Room</code> (entryway rug)
      &rarr; supply closet.<br>Floors elsewhere are swept, not vacuumed.</div>
  </div>
</div></body></html>"""

ST = """<div class="st"><div class="chip" style="background:%(color)s"></div>
<div class="in"><h2>%(name)s</h2><div class="lead">%(leadlbl)s &middot; %(lead)s</div>
<div class="kids">%(kids)s</div>%(later)s</div></div>"""


def build():
    blocks = []
    for name, lead, color, kids, later in STATIONS:
        blocks.append(ST % dict(
            color=color, name=name, lead=lead,
            leadlbl="Room Leads" if "&amp;" in lead else "Room Lead",
            kids=" &middot; ".join(kids),
            later=('<div class="later">+ %s &mdash; after bathroom</div>'
                   % " &middot; ".join(later)) if later else "",
        ))
    html = TPL % dict(css=CSS % dict(inter=INTER, fraunces=FRAUNCES),
                      logo=LOGO_WHITE, stations="".join(blocks))
    src = HERE / "_assign.html"; src.write_text(html)
    raw = HERE / "_assign.pdf"
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        pg.goto("file://%s" % src.resolve(), wait_until="networkidle")
        pg.emulate_media(media="print")
        pg.pdf(path=str(raw), width="11in", height="8.5in", print_background=True,
               margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
        b.close()
    r = PdfReader(str(raw)); w = PdfWriter(); w.add_page(r.pages[0])
    w.add_metadata({"/Title": "Cleanup Assignments — Where Do I Go After My Last Class",
                    "/Author": "Lions Light Academy",
                    "/Subject": "Tuesday co-op cleanup assignments, 2026-2027"})
    f = OUT / "LLA-Cleanup-ASSIGNMENTS.pdf"
    with open(f, "wb") as fh:
        w.write(fh)
    print("  %-40s %5.0f KB" % (f.name, f.stat().st_size / 1024))
    src.unlink(); raw.unlink()

    total = len({n for _, _, _, k, l in STATIONS for n in k + l})
    print("  unique children on the card:", total)


if __name__ == "__main__":
    build()
