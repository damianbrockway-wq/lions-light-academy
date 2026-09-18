#!/usr/bin/env python3
"""Lions Light Academy — first day run sheet.

One thing to carry and tick all day. Ordered by the clock rather than by
topic, because the question being asked at 9:02 is never "what category is
this" but "what is next." Admin that has no natural time — chasing paperwork,
checking Classroom access — is parked in its own block so it does not pretend
to be scheduled.

The last block is deliberately after dismissal: things that matter this week
and must not be done today.
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

BL = "&#95;" * 26          # a line to write on, on the blank template

# a few headings read differently when nothing is filled in yet
TMPL_TITLE = {"Class 1 &middot; 50 min": "Class 1",
              "Class 2 &middot; 55 min": "Class 2",
              "Class 3 &middot; 45 min": "Class 3"}
TMPL_HINT = {"10:00": "Short blocks on the first day &mdash; the opening hour replaces first period",
             "10:50": "Ten minutes &mdash; then move",
             "12:00": "Whole school together",
             "This week": "Write it down before you leave the building"}     # page 1 ends once the normal schedule starts

CORNER = {False: "First day<br>Tuesday 15 September 2026",
          True:  "First day<br>Date &#95;&#95;&#95;&#95;&#95;&#95;&#95;&#95;&#95;&#95;"}
SUB = {False: ("Teachers 8:30 &middot; students 8:45 &middot; opening 8:50. Today is not a normal "
               "Tuesday: the opening hour replaces first period, then <b>three short classes</b> "
               "and lunch at noon."),
       True:  ("The first day runs the same way every year. Fill in the blanks, print it, carry it. "
               "The opening hour replaces first period, so classes start late and run short.")}

K = "key"          # the ones that matter most — gold checkbox, bold
N = None

BLOCKS = [
 ("8:30", "Teachers arrive", "Fifteen minutes before students &mdash; work down this list in order", [
   ("Unlock, lights on, thermostat set", N, N),
   ("Walk the building together &mdash; every adult sees where the first aid kit is",
    "Not &ldquo;it&rsquo;s in the office.&rdquo; Walk them to it.", K),
   ("Name the adult who walks at the <b>back</b> of the group on the fire route",
    "One person, named out loud, so it is not decided at 9:00.", K),
   ("Say the furniture staging spot &mdash; <b>one</b> place",
    "The cards currently disagree: Main and Yellow say by the H.S. classroom, Gray says main room. Pick one.", K),
   ("Cleanup cards to the room leads &mdash; Damian, Erika, Jess &amp; Ginny, Leah", N, N,
    "Cleanup cards handed to each room lead", "Room leads: %s" % BL),
   ("Shed attendance sheet and first aid kit staged by the door", N, N),
   ("Erika confirms she calls 911. Savannah confirms she contacts parents.", N, N,
    "<b>Say the emergency roles out loud</b>",
    "Incident Lead %s &middot; Calls 911 %s &middot; Contacts parents %s" % (BL, BL, BL)),
   ("Registration, Code of Conduct and pledge paperwork out on a table",
    "Five families still owe registration and Code of Conduct.", N,
    "Registration, Code of Conduct and pledge paperwork out on a table",
    "Families still owing paperwork: %s" % BL),
 ]),
 ("8:45", "Students arrive", "Decided &mdash; 8:45, matching what families have already been given", [
   ("Belongings neatly along the entryway wall", N, N),
   ("Straight to the Main Room", N, N),
 ]),
 ("8:50", "Opening", "Everyone in the Main Room", [
   ("<b>Open with prayer over the year</b>",
    "Before anything else. This is the first thing that happens at Lions Light Academy.", K),
   ("Worship", N, N),
   ("Welcome &mdash; every adult stands and is named", N, N),
   ("<b>Lunch today is on us</b>", "From next week, families bring their own.", K,
    "<b>Say whether lunch today is provided</b>",
    "And when families start bringing their own."),
 ]),
 ("9:00", "Fire drill &mdash; walk the route", "On foot, the whole way, before anyone is tired or distracted", [
   ("Walk the fire route to the shed &mdash; everyone, on foot", N, K),
   ("<b>Take attendance at the shed</b>",
    "Known absences written in <em>before</em> you walk out. Unaccounted names said out loud.", K),
   ("Nobody goes back inside until Damian or Ginny says so",
    "Not the alarm stopping. Not because it looks fine.", K),
   ("On the way back, ask students: <b>&ldquo;Where do we go?&rdquo;</b>", N, N),
 ]),
 ("9:20", "Expectations", "Same talk for every age", [
   ("Code of Conduct &mdash; the short version, in your own words", N, N),
   ("<b>Hand out the student pledge</b>",
    "Grade 7 and up sign it in the room, on paper. Grade 6 and under take it home for a parent.", K),
   ("Three strikes &mdash; and what is <em>not</em> a strike",
    "Coming without your work once is not a strike. Twice in a row without a reason is.", N),
   ("Homework is your work. Nobody can do it for you.", N, N),
   ("Collect the pledges that get signed in the room", N, N),
 ]),
 ("9:40", "Split by age group", "Fifteen minutes each", [
   ("Elementary &middot; Middle &middot; High School", N, N),
 ]),
 ("10:00", "Class 1 &middot; 50 min", "Short blocks today &mdash; 50 / 55 / 45, not the usual 80 and 60", [
   ("<b>HS Chemistry</b> &mdash; Ginny &mdash; Gray Room", N, N,
    "<b>High School</b> &mdash; %s" % BL),
   ("<b>MS Art</b> &mdash; Erika &mdash; Main Room", N, N,
    "<b>Middle School</b> &mdash; %s" % BL),
   ("<b>E History</b> &mdash; Leah &mdash; Yellow Room", N, N,
    "<b>Elementary</b> &mdash; %s" % BL),
   ("Rosters on paper in every room &mdash; <b>not on a phone</b>", N, K),
   ("MS Science and E Art do not run today",
    "Cut so that every teacher still teaches at least once on the first day.", N,
    "Classes that do <b>not</b> run today: %s" % BL,
    "Cut so that every teacher still teaches at least once on the first day."),
 ]),
 ("10:50", "Break + snack", "Ten minutes &mdash; then move", [
   ("Snack, then straight to the Class 2 rooms", N, N),
 ]),
 ("11:00", "Class 2 &middot; 55 min", N, [
   ("<b>HS Computer Science</b> &mdash; Damian &mdash; Gray Room", N, N,
    "<b>High School</b> &mdash; %s" % BL),
   ("<b>MS History</b> &mdash; Leah &mdash; Yellow Room", N, N,
    "<b>Middle School</b> &mdash; %s" % BL),
   ("<b>E Science</b> &mdash; Jess &mdash; Main Room", N, N,
    "<b>Elementary</b> &mdash; %s" % BL),
   ("11:55 &mdash; everyone moves to the Main Room", N, N),
 ]),
 ("12:00", "Lunch &mdash; whole school", "Main Room, forty minutes", [
   ("<b>Say again that lunch today is on us</b>",
    "And that from next week families bring their own. Say it to the room, not to individuals.", K),
 ]),
 ("12:45", "Class 3 &middot; 45 min", "Last class of the day", [
   ("<b>HS Real World Ready</b> &mdash; Damian &mdash; Gray Room", N, N,
    "<b>High School</b> &mdash; %s" % BL),
   ("<b>Drama &amp; Public Speaking</b> &mdash; Savannah &mdash; Main Room",
    "Middle School and Elementary combined.", N,
    "<b>Middle School + Elementary</b> &mdash; %s" % BL),
   ("Cleanup at <b>1:30 sharp</b> &mdash; warn the rooms at 1:25", N, N),
 ]),
 ("Any time", "Admin &mdash; catch people while they are in front of you", "None of this is scheduled; all of it is easier today than by email", [
   ("Five families: registration and Code of Conduct",
    "Completed paperwork goes to lionslightacademy2025@gmail.com &mdash; not Damian&rsquo;s personal mail.", K,
    "<b>Chase the outstanding registration and Code of Conduct</b>",
    "Completed paperwork goes to lionslightacademy2025@gmail.com &mdash; not a personal inbox."),
   ("<b>Leah and Savannah &mdash; can they actually see their Google Classroom?</b>",
    "Invitations went to leahyoga33@gmail.com and savannahbox86@gmail.com, but the teacher threads use leah.mikkonen@icloud.com and ssbox@att.net. A Classroom invitation only ever lives in email.", K,
    "<b>Ask every teacher to open Classroom while you watch</b>",
    "An invitation lives only in email and is easy to miss. Check the address it was sent to is the address they actually read."),
   ("Every teacher has accepted their Classroom invitation and can see their class", N, N),
   ("Show teachers the website and where every document lives",
    "lions-light-academy.pages.dev &mdash; everything is there, nothing has to be emailed around.", N),
   ("Classes are owned by lionslightacademy2025@gmail.com, not a personal account",
    "If Classroom looks wrong, check which Google account the browser is signed into.", N),
   ("<b>Supply fees &mdash; check or cash only</b>",
    "No card, no app, no Venmo. If someone asks, that is the answer.", K),
   ("<b>Write a receipt for every single payment, on the spot</b>",
    "Supply Fee Receipt form is on the site. Money is going through a personal account until LLA has its own &mdash; the receipt is the only record that it was LLA&rsquo;s money and not Damian&rsquo;s.", K),
   ("Keep one written list of who paid, what, and when",
    "Not in your head, not in a text thread. One page that goes home with you.", K),
 ]),
 ("1:30", "Cleanup", "Explain the cards <em>before</em> releasing anyone", [
   ("Hold up the assignments card: <b>&ldquo;Where do I go after my last class?&rdquo;</b>", N, K),
   ("Room leads take their card and keep their group together", N, N),
   ("Vacuum route &mdash; <b>Yellow &rarr; Gray &rarr; Main Room</b> (entryway rug) &rarr; supply closet",
    "One route, no waiting. Everywhere else is swept, not vacuumed.", N),
   ("Stewardship &mdash; say why: the building is lent to us. Leave it better than we found it.", N, K),
   ("Each room lead checks and signs their card, and hands it to Damian", N, N),
 ]),
 ("1:45", "Dismissal", N, [
   ("Closing prayer", N, K),
   ("Ask one last time: <b>&ldquo;Where do we go if there&rsquo;s a fire?&rdquo;</b>", N, N),
 ]),
 ("Last out", "Final walkthrough &mdash; Damian", "Only after every room card has been checked and approved", [
   ("Supply closet key returned", N, N),
   ("All windows locked", N, N),
   ("All doors closed", N, N),
   ("Thermostat set", N, N),
   ("Collect all eight cleanup cards", N, N),
 ]),
 ("This week", "Not today", "Write it down now so it stops rattling around", [
   ("Fix the unpublished schedule to say <b>8:45</b>, then publish it",
    "It is the only document still saying 8:30. Everything families can see already says 8:45.", N, ""),
   ("Push the site: the unlisted /kit/ folder and the tidied docs/", N, N,
    "Publish anything that changed today", "Schedule, rosters, class lists."),
   ("Enrollment form is still titled <b>2025&ndash;2026</b>", N, N,
    "Check every document still says the right school year"),
   ("Insurance from the host church &mdash; <b>in writing</b>",
    "LLA is an unaffiliated outside group. Assume nothing.", N,
    "Insurance from the host church &mdash; <b>in writing</b>, current year",
    "LLA is an unaffiliated outside group. Assume nothing."),
   ("ID photos for Leah and Jess", N, N, "ID photos for any teacher still without one"),
   ("Retire the old cleanup sheets so nobody prints last year&rsquo;s", N, N,
    "Retire last year&rsquo;s printables so nobody prints them by mistake"),
   ("Maine nonprofit filing, then EIN, then a bank account",
    "Until that exists every supply fee runs through a personal account. The receipts are what keeps it clean.", N, ""),
   ("Reconcile today&rsquo;s receipts against what actually came in", N, N),
 ]),
]

TEMPLATE = False
BREAK_AFTER = None

CSS = """
@font-face{font-family:'Inter';src:url(data:font/ttf;base64,%(inter)s) format('truetype');font-weight:100 900}
@font-face{font-family:'Fraunces';src:url(data:font/ttf;base64,%(fraunces)s) format('truetype');font-weight:100 900}
@page{size:Letter portrait;margin:0}
*{box-sizing:border-box;margin:0;padding:0;-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{font-family:'Inter',sans-serif;color:#16232F;background:#fff}

.panel{background:#0A1929;color:#F2F5F8;padding:0.26in 0.58in 0.22in;position:relative}
.lockup{display:flex;align-items:center;gap:8px}
.lockup img{width:0.31in}
.lockup .txt{display:flex;flex-direction:column;line-height:1.15}
.org{font-size:7.2pt;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:#E6BD63}
.loc{font-size:6.4pt;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:#8FA3B8;margin-top:1px}
h1{font-family:'Fraunces',Georgia,serif;font-size:23pt;font-weight:600;line-height:1.02;margin-top:0.12in}
.sub{font-size:8.2pt;color:#AFC0D2;margin-top:5px}
.yr{position:absolute;right:0.62in;top:0.40in;font-size:7.2pt;font-weight:600;
  letter-spacing:.12em;text-transform:uppercase;color:#8FA3B8;text-align:right;line-height:1.6}
.bar{height:0.11in;background:#E6BD63}

.body{padding:0 0.58in 0.22in}
/* thead repeats on every printed page, so this spacer does too */
table.flow{width:100%%;border-collapse:collapse}
table.flow th.sp{height:0.46in;padding:0;border:0}
table.flow td{padding:0;border:0;vertical-align:top;break-inside:avoid}

.blk{display:flex;gap:0.20in;margin-bottom:0.145in;break-inside:avoid}
.when{flex:0 0 0.78in;text-align:right;padding-top:1px}
.when .t{font-family:'Fraunces',Georgia,serif;font-size:12.8pt;font-weight:600;
  color:#0A1929;line-height:1.05}
.when .t.sm{font-size:9.6pt;letter-spacing:.02em}
.col{flex:1;border-left:2px solid #E6BD63;padding-left:0.17in}
h2{font-family:'Fraunces',Georgia,serif;font-size:12.4pt;font-weight:600;line-height:1.15}
.hint{font-size:7.9pt;color:#7A838E;font-style:italic;margin-top:2px;margin-bottom:5px}
.col.nohint h2{margin-bottom:5px}

ul{list-style:none}
li{font-size:9.8pt;line-height:1.36;margin-bottom:4.4px;position:relative;padding-left:0.25in}
li::before{content:"";position:absolute;left:0;top:2.5px;width:11px;height:11px;
  border:1.5px solid #8A94A0;border-radius:2px;background:#fff}
li.key::before{border-color:#C08A2E;border-width:2px;background:#FFFDF7}
li.key{font-weight:600}
li b{font-weight:700}
li em{font-style:italic}
.note{display:block;font-weight:400;font-size:8.2pt;line-height:1.34;
  color:#6C7784;margin-top:1px}
li.key .note{color:#8A6210}

.foot{border-top:1px solid #D9D5CB;margin:0.06in 0.62in 0;padding:0.12in 0 0.30in;
  display:flex;justify-content:space-between;align-items:flex-end;
  font-size:7.4pt;letter-spacing:.08em;text-transform:uppercase;color:#8A94A0;font-weight:600}
.brk{break-after:page}
"""

TPL = """<!doctype html><html><head><meta charset="utf-8">
<title>First Day Run Sheet</title><style>%(css)s</style></head><body>
<div class="panel">
  <div class="lockup"><img src="data:image/png;base64,%(logo)s" alt="">
    <div class="txt"><span class="org">Lions Light Academy</span>
    <span class="loc">Winslow, Maine</span></div></div>
  <div class="yr">%(corner)s</div>
  <h1>Run Sheet</h1>
  <p class="sub">%(sub)s</p>
</div>
<div class="bar"></div>
<div class="body"><table class="flow"><thead><tr><th class="sp"></th></tr></thead><tbody>%(blocks)s</tbody></table></div>
<div class="foot">
  <div>Lions Light Academy &middot; Tuesday Co-op 2026&ndash;2027</div>
  <div>Incident lead &middot; Damian &amp; Ginny</div>
</div>
</body></html>"""


def build():
    global TEMPLATE
    out = []
    for when, title, hint, items in BLOCKS:
        lis = []
        for item in items:
            text, note, flag = item[0], item[1], item[2]
            if TEMPLATE and len(item) > 3 and item[3] is not None:
                if item[3] == "":
                    continue                      # dated edition only
                text, note = item[3], (item[4] if len(item) > 4 else None)
            cls = ' class="key"' if flag == K else ""
            n = ('<span class="note">%s</span>' % note) if note else ""
            lis.append("<li%s>%s%s</li>" % (cls, text, n))
        if not lis:
            continue
        if TEMPLATE:
            title = TMPL_TITLE.get(title, title)
            hint = TMPL_HINT.get(when, hint)
        sm = " sm" if len(when) > 5 else ""
        nohint = "" if hint else " nohint"
        hint_html = ('<div class="hint">%s</div>' % hint) if hint else ""
        brk = " brk" if when == BREAK_AFTER else ""
        out.append(
            '<tr><td><div class="blk%s"><div class="when"><div class="t%s">%s</div></div>'
            '<div class="col%s"><h2>%s</h2>%s<ul>%s</ul></div></div></td></tr>'
            % (brk, sm, when, nohint, title, hint_html, "".join(lis)))

    src = HERE / "_run.html"
    src.write_text(TPL % dict(css=CSS % dict(inter=INTER, fraunces=FRAUNCES),
                              logo=LOGO_WHITE, blocks="".join(out),
                              corner=CORNER[TEMPLATE], sub=SUB[TEMPLATE]))
    raw = HERE / "_rn.pdf"
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        pg.goto("file://%s" % src.resolve(), wait_until="networkidle")
        pg.emulate_media(media="print")
        pg.pdf(path=str(raw), width="8.5in", height="11in", print_background=True,
               margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
        b.close()
    r = PdfReader(str(raw))
    assert len(r.pages) <= 4, "expected at most 4 pages, got %d" % len(r.pages)
    w = PdfWriter()
    for p_ in r.pages:
        w.add_page(p_)
    w.add_metadata({"/Title": ("First Day Run Sheet — Template" if TEMPLATE
                               else "First Day Run Sheet") + " — Lions Light Academy",
                    "/Author": "Lions Light Academy",
                    "/Subject": ("Reusable first-day template" if TEMPLATE
                                 else "15 September 2026")})
    f = OUT / ("LLA-First-Day-Run-Sheet-TEMPLATE.pdf" if TEMPLATE
               else "LLA-First-Day-Run-Sheet.pdf")
    with open(f, "wb") as fh:
        w.write(fh)
    n = sum(len(i) for _, _, _, i in BLOCKS)
    print("  %s  %d pages  %d blocks  %d items  %.0f KB"
          % (f.name, len(r.pages), len(BLOCKS), n, f.stat().st_size / 1024))
    src.unlink(); raw.unlink()


if __name__ == "__main__":
    build()
    TEMPLATE = True
    build()
