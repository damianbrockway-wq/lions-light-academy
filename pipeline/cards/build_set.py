#!/usr/bin/env python3
"""Lions Light Academy — Tuesday cleanup card set.

Full brand system: navy panel, gold accents, Fraunces display + Inter body —
the same language as the teacher ID cards and the branded document PDFs.
Each card carries its room's colour as a coded bar under the panel.

Landscape Letter so the cards drop into the existing laminate sleeves.
First names only, no honorifics.
"""
import base64, pathlib, re
from playwright.sync_api import sync_playwright
from pypdf import PdfReader, PdfWriter

HERE = pathlib.Path(__file__).parent
OUT = HERE / "set"; OUT.mkdir(exist_ok=True)
FONTS = pathlib.Path("/home/claude/brand/fonts")

b64 = lambda p: base64.b64encode(pathlib.Path(p).read_bytes()).decode()
LOGO_WHITE = b64("/home/claude/brand/logo_white.png")
INTER = b64(FONTS / "Inter.ttf")
FRAUNCES = b64(FONTS / "Fraunces.ttf")

YEAR = "Tuesday Co-op &middot; 2026&ndash;2027"

CARDS = [
    dict(slug="gray-classroom", title="Gray Classroom", role="Room Lead",
         who="Damian", color="#8E9AA8", tag="High School",
         tasks=["Wipe tables", "Clean whiteboard",
                "Put away extra tables and chairs",
                "All trash picked up", "Trash can emptied",
                "Vacuum floor &mdash; then pass the vacuum to Main Room"]),
    dict(slug="yellow-classroom", title="Yellow Classroom", role="Room Lead",
         who="Erika", color="#E8C54A", tag="Middle School",
         tasks=["Chairs put away", "Tables wiped and put away",
                "Clean whiteboard", "All trash picked up", "Trash can emptied",
                "Vacuum floor &mdash; then pass the vacuum to Gray Classroom"]),
    dict(slug="main-room-hallways", title="Main Room &amp; Hallways", role="Room Leads",
         who="Jess &amp; Ginny", color="#86A96E",
         tag="Elementary &middot; Main room, hallways &amp; entryway",
         tasks=["Chairs put away", "Tables wiped and put away", "Pick up all trash",
                "Sweep floors &mdash; main room, hallways and entryway",
                "Empty large trash into dumpster",
                "Empty entryway mini trash and replace bag",
                "Vacuum entryway rug &mdash; then return the vacuum to the supply closet",
                "Entryway wall cleared &mdash; belongings and students out"]),
    dict(slug="boys-bathroom", title="Boys Bathroom", role="Room Lead",
         who="Damian", color="#6E9BC4", tag="Finishes first &mdash; then help elsewhere",
         tasks=["Flush/Clean toilets", "Pick up trash", "Sweep floor", "Wipe sinks",
                "Check mirrors", "Empty trash"]),
    dict(slug="girls-bathroom", title="Girls Bathroom", role="Room Lead",
         who="Erika", color="#C98BA0", tag="Finishes first &mdash; then help elsewhere",
         tasks=["Flush/Clean toilets", "Pick up trash", "Sweep floor", "Wipe sinks",
                "Check mirrors", "Empty trash"]),
    dict(slug="teacher-lounge-outside", title="Teacher Lounge &amp; Outside", role="Room Lead",
         who="Leah", color="#E0A574", tag="Adult supervision outside",
         tasks=["Wipe lounge surfaces", "Pick up and empty trash", "Sweep lounge",
                "Pick up outdoor toys", "Pick up trash and personal belongings"]),
    dict(slug="final-walkthrough", title="Final Walkthrough", role="Lead",
         who="Damian", color="#E6BD63", tag="Last card of the day", checklabel="Date",
         note="Only after every room card has been checked and approved.",
         tasks=["Supply closet key returned", "All windows locked",
                "All doors closed", "Thermostat set"]),
]

CSS = """
@font-face{font-family:'Inter';src:url(data:font/ttf;base64,%(inter)s) format('truetype');font-weight:100 900}
@font-face{font-family:'Fraunces';src:url(data:font/ttf;base64,%(fraunces)s) format('truetype');font-weight:100 900}
@page{size:Letter landscape;margin:0}
*{box-sizing:border-box;margin:0;padding:0;-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{font-family:'Inter',sans-serif;color:#16232F;background:#fff}
.card{width:11in;height:8.5in;display:flex;flex-direction:column;background:#F7F6F2}

/* ── navy panel ─────────────────────────────── */
.panel{background:#0A1929;color:#F2F5F8;padding:0.52in 0.72in 0.44in;position:relative}
.lockup{display:flex;align-items:center;gap:9px}
.lockup img{width:0.42in;opacity:.97}
.lockup .txt{display:flex;flex-direction:column;line-height:1.16}
.org{font-size:8.4pt;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:#E6BD63}
.loc{font-size:7.2pt;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:#8FA3B8;margin-top:1px}
h1{font-family:'Fraunces',Georgia,serif;font-size:37pt;font-weight:600;line-height:1.02;
   letter-spacing:-.015em;margin-top:0.26in}
.badge{display:inline-block;margin-top:0.19in;background:#E6BD63;color:#0A1929;
   font-size:9.6pt;font-weight:700;letter-spacing:.13em;text-transform:uppercase;
   padding:4px 12px;border-radius:2px}
.tag{position:absolute;top:0.56in;right:0.72in;font-size:8.6pt;font-weight:600;
   letter-spacing:.11em;text-transform:uppercase;color:#8FA3B8;text-align:right}

/* ── room colour bar ────────────────────────── */
.bar{height:0.30in;width:100%%}

/* ── task list ──────────────────────────────── */
.body{flex:1;padding:0.30in 0.72in 0;display:flex;flex-direction:column;justify-content:center}
li{list-style:none;font-size:19pt;line-height:1.26;display:flex;align-items:flex-start;
   gap:0.22in;margin-bottom:0.215in}
li::before{content:"";flex:0 0 auto;width:18px;height:18px;border:1.7px solid #6C7784;
   border-radius:2px;background:#fff;margin-top:5px}
.dense li{font-size:17pt;margin-bottom:0.135in}
.dense li::before{width:16px;height:16px;margin-top:4px}
.note{margin-top:0.24in;font-size:11pt;font-style:italic;color:#5A6676}

/* ── footer ─────────────────────────────────── */
.foot{margin:0 0.72in;padding:0.14in 0 0.34in;border-top:1px solid #D9D5CB;
   display:flex;justify-content:space-between;align-items:flex-end;
   font-size:8.6pt;letter-spacing:.08em;text-transform:uppercase;color:#8A94A0;font-weight:600}
.checked{display:flex;align-items:flex-end;gap:8px}
.checked .rule{display:inline-block;width:2.1in;border-bottom:1px solid #A8B0B9;height:0.20in}
"""

TPL = """<!doctype html><html><head><meta charset="utf-8"><title>%(title)s</title>
<style>%(css)s</style></head><body>
<div class="card">
  <div class="panel">
    <div class="lockup">
      <img src="data:image/png;base64,%(logo)s" alt="">
      <div class="txt"><span class="org">Lions Light Academy</span>
      <span class="loc">Winslow, Maine</span></div>
    </div>
    <div class="tag">%(tag)s</div>
    <h1>%(title)s</h1>
    <div class="badge">%(role)s &middot; %(who)s</div>
  </div>
  <div class="bar" style="background:%(color)s"></div>
  <div class="body%(dense)s"><ul>%(items)s</ul>%(note)s</div>
  <div class="foot">
    <div class="checked"><span>%(checklabel)s</span><span class="rule"></span></div>
    <div>Stewardship in Action &middot; %(year)s</div>
  </div>
</div></body></html>"""


def build(c):
    html = TPL % dict(
        css=CSS % dict(inter=INTER, fraunces=FRAUNCES),
        logo=LOGO_WHITE, title=c["title"], role=c["role"], who=c["who"],
        color=c["color"], tag=c["tag"], year=YEAR,
        checklabel=c.get("checklabel", "Checked by"),
        dense=" dense" if len(c["tasks"]) >= 7 else "",
        items="".join("<li>%s</li>" % t for t in c["tasks"]),
        note=('<div class="note">%s</div>' % c["note"]) if c.get("note") else "",
    )
    src = HERE / ("_%s.html" % c["slug"]); src.write_text(html)
    raw = HERE / "_one.pdf"
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        pg.goto("file://%s" % src.resolve(), wait_until="networkidle")
        pg.emulate_media(media="print")
        pg.pdf(path=str(raw), width="11in", height="8.5in", print_background=True,
               margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
        b.close()
    r = PdfReader(str(raw)); w = PdfWriter(); w.add_page(r.pages[0])
    plain = re.sub("&amp;", "&", c["title"])
    w.add_metadata({"/Title": "%s — LLA Cleanup Card" % plain,
                    "/Author": "Lions Light Academy",
                    "/Subject": "Tuesday co-op cleanup card, 2026-2027"})
    f = OUT / ("LLA-Cleanup-%s.pdf" % c["slug"])
    with open(f, "wb") as fh:
        w.write(fh)
    print("  %-40s %5.0f KB" % (f.name, f.stat().st_size / 1024))
    src.unlink(); raw.unlink()
    return f


if __name__ == "__main__":
    print("Building cleanup card set...")
    files = [build(c) for c in CARDS]
    # one combined file for printing the whole set
    w = PdfWriter()
    for f in files:
        w.add_page(PdfReader(str(f)).pages[0])
    w.add_metadata({"/Title": "LLA Cleanup Cards — Full Set 2026-2027",
                    "/Author": "Lions Light Academy",
                    "/Subject": "All seven Tuesday cleanup cards"})
    allf = OUT / "LLA-Cleanup-Cards-FULL-SET.pdf"
    with open(allf, "wb") as fh:
        w.write(fh)
    print("  %-40s %5.0f KB  (%d pages)" % (allf.name, allf.stat().st_size / 1024, len(files)))
    print("Done ->", OUT)
