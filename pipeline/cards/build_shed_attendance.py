#!/usr/bin/env python3
"""Lions Light Academy — fire route attendance, taken at the shed.

Used standing outside, probably in a hurry, possibly in weather. So: big names,
big boxes, alphabetical so a name can be found without reading the whole list,
and the count arithmetic already printed rather than done in someone's head.

The important design decision is the bottom of the page. A tick sheet alone
cannot tell you whether an unticked child is at the dentist or still in the
building, so the two are separated into their own boxes: KNOWN ABSENT, filled
in from the roster before anyone walks out, and UNACCOUNTED FOR, which is the
only list that matters once you are at the shed.

Roster is pulled from build_assignments.STATIONS so it cannot drift from the
cleanup cards.
"""
import base64, pathlib, sys
from playwright.sync_api import sync_playwright
from pypdf import PdfReader, PdfWriter

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import build_assignments as BA

HERE = pathlib.Path(__file__).parent
OUT = HERE / "set"; OUT.mkdir(exist_ok=True)
FONTS = pathlib.Path("/home/claude/brand/fonts")
b64 = lambda p: base64.b64encode(pathlib.Path(p).read_bytes()).decode()
LOGO_WHITE = b64("/home/claude/brand/logo_white.png")
INTER = b64(FONTS / "Inter.ttf")
FRAUNCES = b64(FONTS / "Fraunces.ttf")

ADULTS = ["Damian", "Ginny", "Erika", "Savannah", "Leah", "Jess"]
BLANKS = 3                      # write-in lines: a guest, a sibling, a late arrival
COLS = 3


def roster():
    names = []
    for _, _, _, kids, later in BA.STATIONS:
        for n in kids + later:
            if n not in names:
                names.append(n)
    return sorted(names, key=lambda s: s.lower())


CSS = """
@font-face{font-family:'Inter';src:url(data:font/ttf;base64,%(inter)s) format('truetype');font-weight:100 900}
@font-face{font-family:'Fraunces';src:url(data:font/ttf;base64,%(fraunces)s) format('truetype');font-weight:100 900}
@page{size:Letter portrait;margin:0}
*{box-sizing:border-box;margin:0;padding:0;-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{font-family:'Inter',sans-serif;color:#16232F;background:#fff;
  width:8.5in;height:11in;display:flex;flex-direction:column}

.panel{background:#0A1929;color:#F2F5F8;padding:0.30in 0.55in 0.26in;position:relative}
.lockup{display:flex;align-items:center;gap:8px}
.lockup img{width:0.30in}
.lockup .txt{display:flex;flex-direction:column;line-height:1.15}
.org{font-size:7pt;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:#E6BD63}
.loc{font-size:6.2pt;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:#8FA3B8;margin-top:1px}
h1{font-family:'Fraunces',Georgia,serif;font-size:25pt;font-weight:600;line-height:1.02;margin-top:0.11in}
.where{font-size:9pt;color:#E6BD63;font-weight:700;letter-spacing:.09em;
  text-transform:uppercase;margin-top:5px}
.yr{position:absolute;right:0.55in;top:0.36in;font-size:7.2pt;font-weight:600;
  letter-spacing:.12em;text-transform:uppercase;color:#8FA3B8;text-align:right;line-height:1.6}
.bar{height:0.11in;background:#E6BD63}

.meta{display:flex;gap:0.28in;padding:0.17in 0.55in 0.13in;border-bottom:1px solid #D9D5CB}
.meta .f{flex:1}
.meta .lbl{font-size:6.6pt;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:#6C7784}
.meta .line{border-bottom:1px solid #A8B0B9;height:0.23in}

.body{flex:1;padding:0.16in 0.55in 0}
.hd{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:0.09in}
h2{font-family:'Fraunces',Georgia,serif;font-size:13pt;font-weight:600}
.tally{font-size:8.4pt;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#0A1929}
.tally b{font-size:11pt}
.tally .blank{display:inline-block;width:0.52in;border-bottom:1.4px solid #0A1929}

ul{list-style:none;display:flex;flex-wrap:wrap;margin-bottom:0.10in}
li{width:33.33%%;display:flex;align-items:center;gap:0.14in;
  font-size:14pt;font-weight:500;padding:0.082in 0}
li::before{content:"";flex:0 0 auto;width:17px;height:17px;border:1.7px solid #5A6676;
  border-radius:2px;background:#fff}
li.w{color:#AEB5BD;font-weight:400}
li.w::before{border-color:#AEB5BD}
li .rule{flex:1;border-bottom:1px solid #CFD4D9;height:0.14in}

.adults li{width:33.33%%;font-size:13.4pt}

/* ── the three moments the count actually matters ── */
.steps{display:flex;gap:0.20in;margin:0.20in 0 0.16in}
.step{flex:1;background:#F7F6F2;border-top:2.5px solid #E6BD63;padding:0.12in 0.14in 0.14in}
.step .n{font-family:'Fraunces',Georgia,serif;font-size:10.4pt;font-weight:600;
  color:#0A1929;margin-bottom:3px}
.step .d{font-size:8.6pt;line-height:1.38;color:#3C4756}
.step .d b{color:#0A1929;font-weight:700}

.foot{display:flex;gap:0.22in;padding:0.02in 0.55in 0}
.box{flex:1;border:1.4px solid #B7BCC2;border-radius:3px;padding:0.11in 0.14in 0.13in}
.box.alert{border:2px solid #A32F2F}
.box .t{font-size:7.6pt;font-weight:700;letter-spacing:.11em;text-transform:uppercase;
  color:#6C7784;margin-bottom:2px}
.box.alert .t{color:#A32F2F}
.box .s{font-size:7.4pt;color:#8A94A0;font-style:italic;margin-bottom:0.07in;line-height:1.3}
.box .l{border-bottom:1px solid #C4C9CE;height:0.235in}

.rule2{margin:0.16in 0.55in 0;border-top:2px solid #0A1929}
.last{padding:0.11in 0.55in 0.26in;display:flex;justify-content:space-between;
  align-items:flex-end;gap:0.3in}
.last .big{font-family:'Fraunces',Georgia,serif;font-size:11.4pt;font-weight:600;
  line-height:1.32;max-width:5.1in}
.last .who{font-size:7.4pt;letter-spacing:.09em;text-transform:uppercase;
  color:#8A94A0;font-weight:600;text-align:right;line-height:1.7}
"""

TPL = """<!doctype html><html><head><meta charset="utf-8">
<title>Fire Route Attendance</title><style>%(css)s</style></head><body>

<div class="panel">
  <div class="lockup"><img src="data:image/png;base64,%(logo)s" alt="">
    <div class="txt"><span class="org">Lions Light Academy</span>
    <span class="loc">Winslow, Maine</span></div></div>
  <div class="yr">Fire route<br>Tuesday Co-op 2026&ndash;2027</div>
  <h1>Attendance at the Shed</h1>
  <div class="where">Shed behind the building &middot; nobody goes back inside</div>
</div>
<div class="bar"></div>

<div class="meta">
  <div class="f"><div class="lbl">Date</div><div class="line"></div></div>
  <div class="f"><div class="lbl">Time out</div><div class="line"></div></div>
  <div class="f"><div class="lbl">Count taken by</div><div class="line"></div></div>
  <div class="f"><div class="lbl">Drill or real</div><div class="line"></div></div>
</div>

<div class="body">
  <div class="hd"><h2>Students</h2>
    <div class="tally">On roster <b>%(nkids)d</b> &nbsp;&middot;&nbsp;
      Absent today <span class="blank"></span> &nbsp;&middot;&nbsp;
      Expected here <span class="blank"></span> &nbsp;&middot;&nbsp;
      Counted <span class="blank"></span></div></div>
  <ul>%(kids)s</ul>

  <div class="hd"><h2>Adults</h2>
    <div class="tally">On roster <b>%(nad)d</b> &nbsp;&middot;&nbsp;
      Counted <span class="blank"></span></div></div>
  <ul class="adults">%(adults)s</ul>

  <div class="steps">
    <div class="step"><div class="n">Before you walk out</div>
      <div class="d">Take this sheet. Write today&rsquo;s known absences in the
        box below <b>now</b> &mdash; not at the shed.</div></div>
    <div class="step"><div class="n">At the shed</div>
      <div class="d">Tick every child you can see, then the adults.
        <b>Nobody goes back inside for anything.</b></div></div>
    <div class="step"><div class="n">Before anyone returns</div>
      <div class="d">Damian or Ginny says when &mdash; <b>not the alarm
        stopping</b>, and not because it looks fine.</div></div>
  </div>
</div>

<div class="foot">
  <div class="box">
    <div class="t">Known absent today</div>
    <div class="s">Filled in from the roster <em>before</em> you walk out.</div>
    <div class="l"></div><div class="l"></div>
  </div>
  <div class="box alert">
    <div class="t">Unaccounted for</div>
    <div class="s">Not ticked and not known absent. Say these names out loud.</div>
    <div class="l"></div><div class="l"></div>
  </div>
</div>

<div class="rule2"></div>
<div class="last">
  <div class="big">If a name is unaccounted for, tell Damian or Ginny immediately
    and keep everyone else at the shed.</div>
  <div class="who">Incident lead &middot; Damian &amp; Ginny<br>
    Calls 911 &middot; Erika<br>Contacts parents &middot; Savannah</div>
</div>

</body></html>"""


def build():
    kids = roster()
    items = "".join('<li>%s</li>' % k for k in kids)
    items += "".join('<li class="w"><span class="rule"></span></li>'
                     for _ in range(BLANKS))
    adults = "".join("<li>%s</li>" % a for a in ADULTS)

    src = HERE / "_shed.html"
    src.write_text(TPL % dict(
        css=CSS % dict(inter=INTER, fraunces=FRAUNCES), logo=LOGO_WHITE,
        kids=items, adults=adults, nkids=len(kids), nad=len(ADULTS)))
    raw = HERE / "_sh.pdf"
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
    w.add_metadata({"/Title": "Attendance at the Shed — Lions Light Academy",
                    "/Author": "Lions Light Academy",
                    "/Subject": "Fire route headcount, 2026-2027"})
    f = OUT / "LLA-Shed-Attendance.pdf"
    with open(f, "wb") as fh:
        w.write(fh)
    print("  %s  %d page  %d students + %d adults + %d blanks  %.0f KB"
          % (f.name, len(r.pages), len(kids), len(ADULTS), BLANKS,
             f.stat().st_size / 1024))
    src.unlink(); raw.unlink()


if __name__ == "__main__":
    build()
