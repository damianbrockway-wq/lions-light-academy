#!/usr/bin/env python3
"""Build branded Lions Light Academy PDFs from markdown."""
import re, sys, base64, pathlib
import markdown
from playwright.sync_api import sync_playwright

BRAND = pathlib.Path("/home/claude/brand")
SRC   = pathlib.Path("/home/claude/lla")
OUT   = pathlib.Path("/home/claude/lla/pdf"); OUT.mkdir(exist_ok=True)
LOGO  = pathlib.Path("/home/claude/brand/logo_gold.png")

LOGO_B64 = base64.b64encode(LOGO.read_bytes()).decode()

DOCS = [
    dict(src="DRAFT_Code_of_Conduct_v1.2.md",
         out="code-of-conduct.pdf",
         eyebrow="Lions Light Academy",
         title="Code of Conduct",
         sub="Faith-Based Expectations for Students and Families",
         version="Version 1.2", effective="September 15, 2026",
         footer="Code of Conduct · v1.2"),
    dict(src="DRAFT_HS_Credit_Summary_v1.0.md",
         out="hs-credit-summary.pdf",
         eyebrow="Lions Light Academy",
         title="High School Credit Summary",
         sub="Parent submission sheet",
         version="Version 1.0", effective="September 2026",
         footer="HS Credit Summary &middot; 2026&ndash;2027"),
    dict(src="DRAFT_Maine_Homeschool_Checklist_v1.0.md",
         out="maine-homeschool-checklist.pdf",
         eyebrow="Lions Light Academy",
         title="Maine Homeschool Documentation Checklist",
         sub="What to keep, and what the co-op covers",
         version="Version 1.0", effective="September 2026",
         footer="Maine Homeschool Checklist &middot; 2026&ndash;2027"),
    dict(src="LLA_HANDBOOK_Where_Everything_Lives.md",
         out="where-everything-lives.pdf",
         eyebrow="Lions Light Academy",
         title="Where Everything Lives",
         sub="The handover map &mdash; files, backups, and how to change anything",
         version="Updated 18 September 2026", effective="September 2026",
         footer="Where Everything Lives &middot; LLA handover map"),
    dict(src="DRAFT_Teacher_Absence_Plan_v1.0.md",
         out="teacher-absence-plan.pdf",
         eyebrow="Lions Light Academy",
         title="When You Can&rsquo;t Be There",
         sub="Teacher absence and cover",
         version="Version 1.0", effective="September 2026",
         footer="Teacher Absence &amp; Cover &middot; 2026&ndash;2027"),
    dict(src="DRAFT_Your_First_Day_v1.0.md",
         out="your-first-day.pdf",
         eyebrow="Lions Light Academy",
         title="Your First Day",
         sub="What the first Tuesday actually looks like",
         version="Version 1.0", effective="September 2026",
         footer="Your First Day &middot; 2026&ndash;2027"),
    dict(src="DRAFT_Supply_List_v1.0.md",
         out="supply-list.pdf",
         eyebrow="Lions Light Academy",
         title="Supply List",
         sub="What to bring on the first day",
         version="Version 1.0", effective="September 2026",
         footer="Supply List &middot; 2026&ndash;2027"),
    dict(src="DRAFT_Classroom_Family_Guide_v1.0.md",
         out="classroom-family-guide.pdf",
         eyebrow="Lions Light Academy",
         title="Google Classroom &mdash; A Guide for Families",
         sub="Getting in, staying in, and the three days that matter",
         version="Version 1.0", effective="September 2026",
         footer="Google Classroom &middot; A Guide for Families"),
    dict(src="DRAFT_Escalation_Discipline_Policy_v1.2.md",
         out="discipline-policy.pdf",
         eyebrow="Lions Light Academy",
         title="Escalation &amp; Discipline Policy",
         sub="Clear Authority, Order, and Restoration",
         version="Version 1.2.1", effective="September 15, 2026",
         footer="Escalation &amp; Discipline Policy · v1.2.1"),
    dict(src="Teacher_Guidebook_2026_DRAFT.md",
         out="teacher-guidebook.pdf",
         eyebrow="Lions Light Academy",
         title="Teacher &amp; Mentor Guidebook",
         sub="A companion for teaching, mentoring, and keeping a room where wonder is possible",
         version="Version 2.0 · 2026 Edition", effective="September 15, 2026",
         footer="Teacher &amp; Mentor Guidebook · v2.0"),
    dict(src="DRAFT_Teacher_Volunteer_Expectations_v2.0.md",
         out="teacher-volunteer-expectations.pdf",
         eyebrow="Lions Light Academy",
         title="Teacher &amp; Volunteer Expectations",
         sub="Authority, Clarity, and Support",
         version="Version 2.0", effective="September 15, 2026",
         footer="Teacher &amp; Volunteer Expectations · v2.0"),
    dict(src="DRAFT_Safety_Emergency_Plan_v1.3.md",
         out="safety-emergency-plan.pdf",
         eyebrow="Lions Light Academy",
         title="Student Safety &amp; Emergency Plan",
         sub="Preparedness, Clarity, and Calm Response",
         version="Version 1.3", effective="September 15, 2026",
         footer="Student Safety &amp; Emergency Plan · v1.3"),
    dict(src="DRAFT_Parent_Packet_v3.md",
         out="parent-packet.pdf",
         eyebrow="Lions Light Academy",
         title="Parent Packet",
         sub="Welcome, Vision, and How the Co-op Works",
         version="Version 3.1 · 2026\u20132027", effective="September 17, 2026",
         footer="Parent Packet · v3.1 · 2026\u20132027"),
    dict(src="DRAFT_Supervision_SOP_v1.1.md",
         out="supervision-sop.pdf",
         eyebrow="Lions Light Academy",
         title="Supervision &amp; Room Operations SOP",
         sub="Operational Clarity for Co-op Days",
         version="Version 1.1", effective="September 15, 2026",
         footer="Supervision &amp; Room Operations SOP · v1.1"),
    dict(src="DRAFT_First_Day_Run_Through.md",
         out="first-day-run-through.pdf",
         eyebrow="Lions Light Academy",
         title="First Day Run-Through",
         sub="What to cover with every student, in order",
         version="2026\u20132027", effective="September 15, 2026",
         footer="First Day Run-Through · 2026\u20132027"),
    dict(src="DRAFT_Classroom_Setup_Guide.md",
         out="classroom-setup-guide.pdf",
         eyebrow="Lions Light Academy",
         title="Setting Up Your Google Classroom",
         sub="A three-minute job for leadership, and the rest is yours",
         version="Version 1.3", effective="September 17, 2026",
         footer="Google Classroom Setup · v1.3"),
    dict(src="DRAFT_Technical_Operations.md",
         out="technical-operations.pdf",
         eyebrow="Lions Light Academy",
         title="Technical Operations Handbook",
         sub="How the website and the Google backend actually work",
         version="Version 1.1", effective="September 7, 2026",
         footer="Technical Operations Handbook \u00b7 v1.1"),
]

VERSE = ("It is the glory of God to conceal a matter, "
         "but the glory of kings is to search it out.")

COVER = """
<section class="cover">
  <div class="cover-body">
    <img class="cover-mark" src="data:image/png;base64,{logo}" alt="">
    <div class="cover-eyebrow">{eyebrow}</div>
    <h1 class="cover-title">{title}</h1>
    <p class="cover-sub">{sub}</p>
    <div class="cover-rule"></div>
    <div class="cover-verse">&ldquo;{verse}&rdquo;<cite>Proverbs 25:2</cite></div>
  </div>
  <div class="cover-foot">
    <div class="cover-meta">
      <div><div class="k">Effective</div><div class="v">{effective}</div></div>
      <div class="r"><div class="k">Document</div><div class="v">{version}</div></div>
    </div>
  </div>
</section>
"""

SIG_HTML = """
<div class="sig">
  <div class="row"><div class="lbl">Student Name</div><div class="line"></div></div>
  <div class="row"><div class="lbl">Parent / Guardian Name</div><div class="line"></div></div>
  <div class="row split">
    <div><div class="lbl">Signature</div><div class="line"></div></div>
    <div class="date"><div class="lbl">Date</div><div class="line"></div></div>
  </div>
</div>
"""

FOOTER_TPL = """
<div style="width:100%;font-family:Inter,sans-serif;font-size:7pt;color:#8A94A0;
     padding:0 17mm;display:flex;justify-content:space-between;align-items:center;">
  <span style="letter-spacing:.06em">{footer}</span>
  <span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span>
</div>
"""

def strip_front(md: str) -> str:
    """Remove the markdown title block; the cover carries it.

    Callout blockquotes in the front matter (version supersession notices,
    'works alongside' lines) sit BEFORE the first rule and were being
    stripped with the title. Preserve them and re-attach after the rule.

    Blank lines BETWEEN kept callouts must survive too. Without them,
    markdown merges two adjacent blockquotes into a single callout box and
    the sentences run together mid-paragraph.
    """
    def is_callout(x):
        return (x.lstrip().startswith(">") or
                (x.strip().startswith("*") and "Aligned with" in x) or
                x.strip().startswith("Works alongside"))

    lines = md.split("\n")
    for i, l in enumerate(lines):
        if l.strip() == "---" and i > 2:
            front = lines[:i]
            kept = []
            for x in front:
                if x.strip() == "":
                    if kept and kept[-1] != "":
                        kept.append("")          # separator, collapsed to one
                elif is_callout(x):
                    kept.append(x)
            while kept and kept[-1] == "":
                kept.pop()
            while kept and kept[0] == "":
                kept.pop(0)
            body = lines[i+1:]
            if kept:
                return "\n".join(kept + [""] + body)
            return "\n".join(body)
    return md

def build_signature(html: str) -> str:
    """Replace the plain-text signature lines with a designed block."""
    pat = re.compile(
        r"<p>Student Name:.*?Date: _+</p>", re.S)
    if pat.search(html):
        return pat.sub(SIG_HTML, html)
    # fallback: individual paragraphs
    pat2 = re.compile(r"<p>Student Name:.*?</p>\s*<p>Parent/Guardian Name:.*?</p>\s*<p>Signature:.*?</p>", re.S)
    return pat2.sub(SIG_HTML, html)

def mark_verses(html: str) -> str:
    """Blockquotes that are a single italic scripture line get the verse treatment."""
    def rep(m):
        inner = m.group(1)
        if "—" in inner and len(re.sub("<[^>]+>", "", inner)) < 220 and "supersedes" not in inner:
            return '<blockquote class="verse">%s</blockquote>' % inner
        return m.group(0)
    return re.sub(r"<blockquote>(.*?)</blockquote>", rep, html, flags=re.S)

def render(doc):
    md_text = strip_front((SRC / doc["src"]).read_text())
    body = markdown.markdown(
        md_text,
        # fenced_code is required. Without it a ``` block is not turned into a
        # <pre>, its newlines collapse, and the fence's language label ("bash")
        # is glued to the first line. The verify-before-push script shipped that
        # way in Technical Operations v1.0 and could not be pasted and run.
        extensions=["tables", "sane_lists", "attr_list", "fenced_code"],
    )
    body = mark_verses(body)
    body = build_signature(body)

    html = f"""<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="brand.css"></head><body>
{COVER.format(logo=LOGO_B64, verse=VERSE, **doc)}
<main class="doc">{body}</main>
</body></html>"""

    tmp = BRAND / f"_{doc['out']}.html"
    tmp.write_text(html)

    cover_pdf = BRAND / "_cover.pdf"
    body_pdf  = BRAND / "_body.pdf"

    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        pg.goto(f"file://{tmp}", wait_until="networkidle")
        pg.emulate_media(media="print")
        common = dict(format="Letter", print_background=True)
        # cover: no footer, no margins
        pg.pdf(path=str(cover_pdf), page_ranges="1", **common,
               margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
        # body: footer with page numbers, numbered within the whole document
        pg.pdf(path=str(body_pdf), page_ranges="2-", **common,
               display_header_footer=True,
               header_template="<div></div>",
               footer_template=FOOTER_TPL.format(footer=doc["footer"]),
               margin={"top": "19mm", "bottom": "20mm", "left": "17mm", "right": "17mm"})
        b.close()

    from pypdf import PdfWriter, PdfReader
    w = PdfWriter()
    for f in (cover_pdf, body_pdf):
        for page in PdfReader(str(f)).pages:
            w.add_page(page)
    w.add_metadata({"/Title": re.sub("&amp;", "&", doc["title"]),
                    "/Author": "Lions Light Academy",
                    "/Subject": re.sub("&amp;", "&", doc["sub"])})
    with open(OUT / doc["out"], "wb") as fh:
        w.write(fh)

    tmp.unlink(); cover_pdf.unlink(); body_pdf.unlink()
    size = (OUT / doc["out"]).stat().st_size
    print(f"  {doc['out']:26} {size/1024:7.0f} KB")

if __name__ == "__main__":
    print("Building branded PDFs...")
    for d in DOCS:
        render(d)
    print("Done ->", OUT)
