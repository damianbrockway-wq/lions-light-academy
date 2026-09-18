#!/usr/bin/env python3
"""Lions Light Academy — the two record forms the policies already require.

Both documents promise paperwork that did not exist:

  Safety & Emergency Plan v1.3, General Emergency Procedure, step 5 —
    "Document — record what happened and what was done."
  Escalation & Discipline Policy v1.2, Documentation & Review —
    "Every warning goes to the family in writing."

So the wording here is lifted from those documents rather than invented. The
categories on the incident form are the plan's own "Emergency Types Covered";
the concern list on the warning record is the policy's own definition of a
Moderate concern, including the two-sessions-in-a-row rule for work not done.

Both are portrait Letter, exactly one page, and asserted as such.
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

CSS = """
@font-face{font-family:'Inter';src:url(data:font/ttf;base64,%(inter)s) format('truetype');font-weight:100 900}
@font-face{font-family:'Fraunces';src:url(data:font/ttf;base64,%(fraunces)s) format('truetype');font-weight:100 900}
@page{size:Letter portrait;margin:0}
*{box-sizing:border-box;margin:0;padding:0;-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{font-family:'Inter',sans-serif;color:#16232F;background:#fff;
  width:8.5in;height:11in;display:flex;flex-direction:column}

.panel{background:#0A1929;color:#F2F5F8;padding:0.28in 0.55in 0.24in;position:relative}
.lockup{display:flex;align-items:center;gap:8px}
.lockup img{width:0.30in}
.lockup .txt{display:flex;flex-direction:column;line-height:1.15}
.org{font-size:7pt;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:#E6BD63}
.loc{font-size:6.2pt;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:#8FA3B8;margin-top:1px}
h1{font-family:'Fraunces',Georgia,serif;font-size:24pt;font-weight:600;line-height:1.02;margin-top:0.11in}
.src{font-size:7.6pt;color:#AFC0D2;margin-top:4px;max-width:5.4in;line-height:1.4}
.yr{position:absolute;right:0.55in;top:0.34in;font-size:7pt;font-weight:600;
  letter-spacing:.12em;text-transform:uppercase;color:#8FA3B8;text-align:right;line-height:1.6}
.bar{height:0.11in;background:#E6BD63}

.body{flex:1;padding:0.17in 0.55in 0}
h2{font-family:'Fraunces',Georgia,serif;font-size:11.4pt;font-weight:600;
  margin-top:0.16in;margin-bottom:5px}
h2:first-child{margin-top:0}
.hr{border-top:1px solid #D9D5CB;margin-top:0.14in;padding-top:0.12in}

.row{display:flex;gap:0.24in;margin-bottom:0.085in}
.f{flex:1;min-width:0}
.f.sm{flex:0 0 1.25in}
.f.md{flex:0 0 1.9in}
.lbl{font-size:6.4pt;font-weight:700;letter-spacing:.11em;text-transform:uppercase;
  color:#6C7784;white-space:nowrap;overflow:hidden}
.line{border-bottom:1px solid #A8B0B9;height:0.22in}
.line.tall{height:0.26in}

.opts{display:flex;flex-wrap:wrap;gap:0.055in 0.20in;margin:2px 0 0.085in}
.opt{display:flex;align-items:center;gap:6px;font-size:8.6pt;line-height:1.25}
.opt::before{content:"";flex:0 0 auto;width:11px;height:11px;border:1.4px solid #6C7784;
  border-radius:2px;background:#fff}
.opt.k::before{border-color:#C08A2E;border-width:1.9px;background:#FFFDF7}
.opt.k{font-weight:600}
.opt b{font-weight:700}

.write .l{border-bottom:1px solid #C4C9CE;height:0.235in}
.hint{font-size:7.4pt;color:#8A94A0;font-style:italic;margin:-2px 0 4px}

.callout{border-left:3px solid #C08A2E;background:#FBF8F1;padding:0.09in 0.13in;
  font-size:8pt;line-height:1.4;color:#3C4756;margin:0.10in 0 0.02in}
.callout b{color:#0A1929}
.callout.alert{border-color:#A32F2F;background:#FCF6F5}
.callout.alert b{color:#A32F2F}

.foot{border-top:1.4px solid #0A1929;margin:0.10in 0.55in 0;padding:0.11in 0 0.26in}
.fnote{font-size:7.2pt;color:#8A94A0;font-style:italic;margin-top:0.09in;line-height:1.35}
.stamp{display:flex;justify-content:space-between;font-size:6.8pt;letter-spacing:.09em;
  text-transform:uppercase;color:#9AA3AE;font-weight:600;margin-top:0.10in}
"""

SHELL = """<!doctype html><html><head><meta charset="utf-8"><title>%(title)s</title>
<style>%(css)s</style></head><body>
<div class="panel">
  <div class="lockup"><img src="data:image/png;base64,%(logo)s" alt="">
    <div class="txt"><span class="org">Lions Light Academy</span>
    <span class="loc">Winslow, Maine</span></div></div>
  <div class="yr">%(corner)s</div>
  <h1>%(heading)s</h1>
  <p class="src">%(src)s</p>
</div>
<div class="bar"></div>
<div class="body">%(body)s</div>
<div class="foot">%(foot)s
  <div class="stamp"><span>Lions Light Academy &middot; %(stamp)s</span>
  <span>Tuesday Co-op 2026&ndash;2027</span></div>
</div>
</body></html>"""


def lines(n):
    return '<div class="write">%s</div>' % ('<div class="l"></div>' * n)


def opts(items, key=()):
    return '<div class="opts">%s</div>' % "".join(
        '<span class="opt%s">%s</span>' % (" k" if i in key else "", t)
        for i, t in enumerate(items))


def field(label, cls=""):
    return ('<div class="f %s"><div class="lbl">%s</div><div class="line"></div></div>'
            % (cls, label))


def row(*fields):
    return '<div class="row">%s</div>' % "".join(fields)


# ── 1. Incident Report ───────────────────────────────────────────────────────
INCIDENT_BODY = (
    row(field("Date"), field("Time"), field("Location &mdash; room or off-site"))
    + row(field("Completed by &mdash; name"), field("Role"),
          field("Incident Lead on duty"))
    + '<h2>What kind of incident</h2>'
    + opts(["Injury or illness", "Fire, smoke or evacuation",
            "Behavioural crisis posing a safety risk",
            "Facility concern &mdash; power, unsafe condition", "Other"], key=(0, 2))
    + '<h2>Who was involved</h2>'
    + row(field("Student(s)"), field("Age group", "md"))
    + row(field("Adults present"))
    + '<h2>What happened</h2>'
    + '<p class="hint">Facts only, in the order they happened. What was seen, not what was concluded.</p>'
    + lines(4)
    + '<h2>What was done</h2>'
    + '<p class="hint">Every action taken, and by whom.</p>'
    + lines(4)
    + '<div class="hr"></div>'
    + '<h2>Response &mdash; tick every one that applies</h2>'
    + opts(["First aid given", "<b>911 called</b>", "Parents contacted",
            "Attendance taken at the shed", "Student collected by a parent",
            "Student returned to the day", "Transported by ambulance"], key=(1, 2))
    + row(field("911 &mdash; time called", "sm"), field("By whom", "md"),
          field("Parents &mdash; time", "sm"), field("By whom"))
)

INCIDENT_FOOT = (
    row(field("Incident Lead &mdash; signature"), field("Date", "sm"))
    + row(field("Leadership review &mdash; signature"), field("Date", "sm"))
    + '<p class="fnote">Parents are notified following significant incidents, '
      'using clear and factual communication. Leadership reviews incidents to improve '
      'procedures and reduce future risk. Keep this with the student&rsquo;s file and '
      'give the family a copy.</p>'
)


# ── 2. Warning Record ────────────────────────────────────────────────────────
WARNING_BODY = (
    row(field("Student"), field("Date of the concern", "md"), field("Class or room", "md"))
    + row(field("Teacher who raised it"), field("Leadership issuing the warning"))
    + '<h2>Which Moderate concern</h2>'
    + '<p class="hint">Warnings exist only at Moderate. Minor concerns are corrected in the '
      'moment and counted toward nothing.</p>'
    + opts(["Repeated minor issues raised to Moderate",
            "Disrespect toward adults or peers",
            "Disruption that interferes with instruction",
            "Failure to comply after correction",
            "Persistent refusal to take part in instruction",
            "<b>Work not done &mdash; two class sessions in a row</b>"], key=(5,))
    + '<h2>What happened</h2>'
    + '<p class="hint">A short note naming what happened and when is enough. '
      'This is what makes a third concern uncontroversial rather than a fight.</p>'
    + lines(5)
    + '<h2>If raised from repeated minor concerns &mdash; what the pattern was based on</h2>'
    + '<p class="hint">Noted by the teacher at the time, not reconstructed later.</p>'
    + lines(3)
    + '<div class="hr"></div>'
    + '<h2>Before the warning is issued &mdash; leadership check</h2>'
    + opts(["Current warning count for the year confirmed",
            "Checked for an unmet support or accommodation need"], key=(0, 1))
    + '<p class="hint">A check, not a veto.</p>'
    + '<h2>Which warning is this</h2>'
    + opts(["First this school year", "Second this school year",
            "<b>Third &mdash; begins the Reconciliation Process</b>"], key=(2,))
    + '<div class="callout alert"><b>A third Moderate concern does not produce a warning.</b> '
      'It begins the Reconciliation Process: pause, meeting, ownership, repair, a signed '
      're-entry plan, and a four-day review period. Completing it clears the count to zero.</div>'
)

WARNING_FOOT = (
    row(field("Date notified", "sm"), field("How", "md"),
        field("By whom"))
    + row(field("Leadership &mdash; signature"), field("Date", "sm"))
    + '<p class="fnote">Warnings count across all classes, not per teacher, and reset each '
      'school year. Anyone who was the teacher in the incident, is a party to it, or is a '
      'relative of the student steps out of the decision. A family who disagrees may ask '
      'leadership to review it, and leadership answers in writing.</p>'
)


DOCS = [
    dict(slug="Incident-Report", title="Incident Report", heading="Incident Report",
         corner="Safety &amp; Emergency<br>Plan v1.3",
         src="Student Safety &amp; Emergency Plan v1.3 &mdash; General Emergency Procedure, "
             "step 5: <em>Document &mdash; record what happened and what was done.</em>",
         body=INCIDENT_BODY, foot=INCIDENT_FOOT,
         stamp="Incident Report",
         subject="Safety incident record, 2026-2027"),
    dict(slug="Warning-Record", title="Warning Record", heading="Warning Record",
         corner="Escalation &amp; Discipline<br>Policy v1.2.1",
         src="Escalation &amp; Discipline Policy v1.2.1 &mdash; Documentation &amp; Review: "
             "<em>Every warning goes to the family in writing.</em>",
         body=WARNING_BODY, foot=WARNING_FOOT,
         stamp="Warning Record &middot; Moderate concern",
         subject="Documented warning to the family, 2026-2027"),
]


def build(d):
    src = HERE / ("_%s.html" % d["slug"])
    src.write_text(SHELL % dict(
        css=CSS % dict(inter=INTER, fraunces=FRAUNCES), logo=LOGO_WHITE,
        title=d["title"], heading=d["heading"], corner=d["corner"],
        src=d["src"], body=d["body"], foot=d["foot"], stamp=d["stamp"]))
    raw = HERE / "_rec.pdf"
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        pg.goto("file://%s" % src.resolve(), wait_until="networkidle")
        pg.emulate_media(media="print")
        pg.pdf(path=str(raw), width="8.5in", height="11in", print_background=True,
               margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
        b.close()
    r = PdfReader(str(raw))
    assert len(r.pages) == 1, "%s MUST be one page, got %d" % (d["slug"], len(r.pages))
    w = PdfWriter(); w.add_page(r.pages[0])
    w.add_metadata({"/Title": "%s — Lions Light Academy" % d["title"],
                    "/Author": "Lions Light Academy",
                    "/Subject": d["subject"]})
    f = OUT / ("LLA-%s.pdf" % d["slug"])
    with open(f, "wb") as fh:
        w.write(fh)
    print("  %-28s %d page  %4.0f KB" % (f.name, len(r.pages), f.stat().st_size / 1024))
    src.unlink(); raw.unlink()


if __name__ == "__main__":
    for d in DOCS:
        build(d)
