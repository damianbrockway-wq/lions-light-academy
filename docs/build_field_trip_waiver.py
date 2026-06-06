# -*- coding: utf-8 -*-
"""Build the LLA Field Trip Waiver — simplified per-trip form.
Assumes the family has already signed the enrollment Liability Release,
Photo/Media Preference, and Medical Emergency Consent."""
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.units import inch
import os

NAVY     = HexColor("#1A2E5C")
GREY     = HexColor("#5A6B7B")
ACCENT   = HexColor("#1565C0")
BORDER   = HexColor("#A8B5C2")
FIELDBG  = HexColor("#F5F8FB")
RULE     = HexColor("#D6DEE6")
NOTEBG   = HexColor("#EFF4FA")

PAGE_W, PAGE_H = letter
LM, RM = 0.75*inch, 0.75*inch
TM, BM = 0.7*inch, 0.7*inch
CW = PAGE_W - LM - RM

LOGO = "/sessions/serene-practical-davinci/mnt/outputs/lla-logo-trans.png"
OUT  = "/sessions/serene-practical-davinci/mnt/LLA-site/docs/field-trip-waiver.pdf"

c = canvas.Canvas(OUT, pagesize=letter)
c.setTitle("Lions Light Academy — Field Trip Waiver")
form = c.acroForm
state = {"y": PAGE_H - TM, "page": 1, "fid": 0}

def fid(prefix):
    state["fid"] += 1
    return f"{prefix}_{state['fid']}"

SITE_URL = "https://lions-light-academy.pages.dev"

def footer():
    c.setFont("Helvetica", 8)
    c.setFillColor(GREY)
    c.drawCentredString(PAGE_W/2, 0.4*inch,
        "Lions Light Academy  •  Field Trip Waiver  •  Fall 2026 — v1.0")
    c.drawRightString(PAGE_W - RM, 0.4*inch, f"Page {state['page']}")
    # Clickable back-to-site link in the footer (left side)
    c.setFillColor(ACCENT)
    c.setFont("Helvetica-Bold", 8.5)
    back_text = "← Back to Lions Light Academy"
    c.drawString(LM, 0.4*inch, back_text)
    tw = c.stringWidth(back_text, "Helvetica-Bold", 8.5)
    c.linkURL(SITE_URL, (LM, 0.36*inch, LM + tw, 0.55*inch), relative=0)

def new_page():
    footer()
    c.showPage()
    state["page"] += 1
    state["y"] = PAGE_H - TM
    c.setFont("Helvetica", 10)
    draw_header_small()

def need(h):
    if state["y"] - h < BM + 0.4*inch:
        new_page()

def draw_header_full():
    if os.path.exists(LOGO):
        c.drawImage(LOGO, LM, PAGE_H - TM - 0.95*inch, width=1.0*inch, height=1.0*inch,
                    mask='auto', preserveAspectRatio=True)
    tx = LM + 1.15*inch
    c.setFont("Helvetica-Bold", 10); c.setFillColor(NAVY)
    c.drawString(tx, PAGE_H - TM - 0.30*inch, "Lions Light Academy")
    c.setFont("Helvetica", 10); c.setFillColor(black)
    c.drawString(tx, PAGE_H - TM - 0.48*inch, "Field Trip Waiver")
    state["y"] = PAGE_H - TM - 1.15*inch
    c.setFont("Helvetica-Bold", 22); c.setFillColor(NAVY)
    c.drawString(LM, state["y"], "Field Trip Waiver & Permission")
    state["y"] -= 0.24*inch
    c.setFont("Helvetica", 10); c.setFillColor(GREY)
    c.drawString(LM, state["y"], "Per-Trip Authorization for Co-Op Activities")
    state["y"] -= 0.18*inch
    c.setFont("Helvetica", 9.5); c.setFillColor(black)
    c.drawCentredString(PAGE_W/2, state["y"] - 0.10*inch, "Effective: Fall 2026  |  Version 1.0")
    state["y"] -= 0.40*inch

def draw_header_small():
    if os.path.exists(LOGO):
        c.drawImage(LOGO, LM, PAGE_H - TM - 0.55*inch, width=0.55*inch, height=0.55*inch,
                    mask='auto', preserveAspectRatio=True)
    c.setFont("Helvetica-Bold", 9.5); c.setFillColor(NAVY)
    c.drawString(LM + 0.70*inch, PAGE_H - TM - 0.22*inch, "Lions Light Academy")
    c.setFont("Helvetica", 9.5); c.setFillColor(black)
    c.drawString(LM + 0.70*inch, PAGE_H - TM - 0.38*inch, "Field Trip Waiver")
    state["y"] = PAGE_H - TM - 0.85*inch

def h_section(title):
    need(0.45*inch)
    state["y"] -= 0.06*inch
    c.setFont("Helvetica-Bold", 12.5); c.setFillColor(NAVY)
    c.drawString(LM, state["y"], title)
    state["y"] -= 0.05*inch
    c.setStrokeColor(RULE); c.setLineWidth(0.8)
    c.line(LM, state["y"], LM+CW, state["y"])
    state["y"] -= 0.20*inch

def para(text, size=10, color=None, gap=0.06*inch):
    words = text.split(); line = ""
    for w in words:
        c.setFont("Helvetica", size)
        if c.stringWidth(line+" "+w,"Helvetica",size) > CW:
            need(0.2*inch)
            c.setFont("Helvetica", size); c.setFillColor(color or black)
            c.drawString(LM, state["y"], line)
            state["y"] -= 0.17*inch
            line = w
        else:
            line = (line+" "+w).strip()
    if line:
        need(0.2*inch)
        c.setFont("Helvetica", size); c.setFillColor(color or black)
        c.drawString(LM, state["y"], line)
        state["y"] -= 0.17*inch
    state["y"] -= gap

FH = 0.26*inch
LBLH = 0.155*inch

def textfield(label, x, y, w, multiline=False, h=None):
    c.setFont("Helvetica", 8); c.setFillColor(GREY)
    c.drawString(x+0.02*inch, y, label)
    fh = h if h else FH
    form.textfield(name=fid("f"), x=x, y=y-LBLH-fh, width=w, height=fh,
                   borderWidth=0.75, borderColor=BORDER, fillColor=FIELDBG,
                   forceBorder=True, fontName="Helvetica", fontSize=10,
                   fieldFlags=("multiline" if multiline else ""))
    return y - LBLH - fh

def row(fields, gap=0.14*inch):
    need(FH + LBLH + 0.12*inch)
    total_w = CW - gap*(len(fields)-1)
    weights = sum(f[1] for f in fields)
    base = state["y"]; miny = base
    x = LM
    for (label, wt, *rest) in fields:
        ml = rest[0] if rest else False
        w = total_w * wt/weights
        endy = textfield(label, x, base, w, multiline=ml)
        miny = min(miny, endy)
        x += w + gap
    state["y"] = miny - 0.16*inch

def bigfield(label, h=0.5*inch):
    need(h + LBLH + 0.12*inch)
    endy = textfield(label, LM, state["y"], CW, multiline=True, h=h)
    state["y"] = endy - 0.16*inch

def agree(text):
    size = 11
    tw = CW - (size+6)
    c.setFont("Helvetica", 9.5)
    words = text.split(); lines = []; line = ""
    for w in words:
        if c.stringWidth(line+" "+w,"Helvetica",9.5) > tw:
            lines.append(line); line = w
        else:
            line = (line+" "+w).strip()
    if line: lines.append(line)
    need(0.17*inch*len(lines) + 0.2*inch)
    top = state["y"]
    form.checkbox(name=fid("cb"), x=LM, y=top-size+1, size=size,
                  borderWidth=0.75, borderColor=BORDER, fillColor=white, forceBorder=True)
    tx = LM + size + 6
    c.setFont("Helvetica", 9.5); c.setFillColor(black)
    yy = top - size + 3
    for ln in lines:
        c.drawString(tx, yy, ln)
        yy -= 0.165*inch
    state["y"] = yy - 0.10*inch

# ─── BUILD ───
draw_header_full()

# A simple intro note explaining what this is (and what it isn't)
about = ("This form gives permission for your child to attend a specific LLA field trip. The Liability Release, Medical Emergency "
         "Consent, and Photo/Media Preference you signed at enrollment remain in effect — not duplicated here. "
         "To fill on screen: download this file and open it in Preview (Mac), Files / Adobe Acrobat (iPhone or Android), "
         "or Acrobat Reader (Windows). Browser PDF viewers usually don't show form fields. You can also print and fill by hand.")
# Pre-wrap to get line count
c.setFont("Helvetica", 9.5)
tw = CW - 0.30*inch
words = about.split(); about_lines = []; line = ""
for w in words:
    if c.stringWidth(line+" "+w,"Helvetica",9.5) > tw:
        about_lines.append(line); line = w
    else:
        line = (line+" "+w).strip()
if line: about_lines.append(line)
box_h = 0.30*inch + 0.16*inch*len(about_lines) + 0.10*inch  # header + lines + bottom padding
need(box_h + 0.20*inch)
top = state["y"]
c.setStrokeColor(BORDER); c.setLineWidth(0.75)
c.setFillColor(NOTEBG)
c.roundRect(LM, top-box_h, CW, box_h, 5, fill=1, stroke=1)
c.setFillColor(NAVY); c.setFont("Helvetica-Bold", 9.5)
c.drawString(LM+0.12*inch, top-0.18*inch, "About this form  —  How to fill it out")
c.setFillColor(black); c.setFont("Helvetica", 9.5)
yy = top - 0.36*inch
for ln in about_lines:
    c.drawString(LM+0.12*inch, yy, ln)
    yy -= 0.16*inch
state["y"] = top - box_h - 0.14*inch

# ─── 1. Trip ───
h_section("1. Trip Information  (completed by leadership)")
row([("Trip Name / Destination", 2)])
row([("Trip Date", 1), ("Departure Time", 1), ("Return Time", 1)])
row([("Departure Location", 1), ("Return Location", 1)])
row([("Lead Teacher / Trip Supervisor", 1.6), ("Phone During Trip", 1)])
bigfield("Brief Description of Activities & Any Trip-Specific Notes", h=0.55*inch)

# ─── 2. Student & Family ───
h_section("2. Student & Family")
row([("Student Full Name", 2), ("Grade", 0.6)])
row([("Parent / Guardian — Full Name", 1.8), ("Best Phone During Trip", 1)])

# ─── 3. Updates ───
h_section("3. Anything Leadership Should Know for This Trip")
bigfield("Allergies, medications, or special considerations specific to this day (leave blank if none change)", h=0.5*inch)

# ─── 4. Permission ───
h_section("4. Permission")
agree("I give my child permission to attend and participate in the field trip described above. "
      "I understand that the Liability Release, Medical Emergency Consent, and Photo/Media Preference "
      "I signed at enrollment remain in effect during this trip.")

# ─── 5. Signature ───
h_section("5. Signature")
row([("Parent / Guardian Signature (typed name)", 2.2), ("Date", 1)])

# ─── OFFICE USE ───
need(0.95*inch)
state["y"] -= 0.08*inch
top = state["y"]
c.setStrokeColor(BORDER); c.setLineWidth(0.75)
c.setFillColor(NOTEBG)
c.roundRect(LM, top-0.92*inch, CW, 0.92*inch, 5, fill=1, stroke=1)
c.setFillColor(NAVY); c.setFont("Helvetica-Bold", 9.5)
c.drawString(LM+0.12*inch, top-0.20*inch, "FOR OFFICE USE ONLY")
state["y"] -= 0.36*inch
row([("Received by", 1), ("Date Received", 1), ("Verified by Supervisor", 1)])

footer()
c.save()

from pypdf import PdfReader
r = PdfReader(OUT)
flds = r.get_fields() or {}
print(f"WROTE {OUT}")
print(f"Pages: {len(r.pages)}  Fillable fields: {len(flds)}")
import os
print(f"Size: {os.path.getsize(OUT):,} bytes")
