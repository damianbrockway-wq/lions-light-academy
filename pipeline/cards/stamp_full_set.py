#!/usr/bin/env python3
"""Rebuild the one-per-page cleanup set with card-edge cut borders.

build_set.py alone produces seven station cards; the set that actually ships
is eight pages, with the assignments cover first. That prepend used to be done
by hand — it happens here instead, so the file can be rebuilt from scratch.

Every page gets a dashed border on the card edge. These cards already fill
their whole sheet, so there is nothing to trim on press — but a home printer
scales the sheet to fit Letter with its own margins, and the border scales
with the artwork, so it still marks where the card really ends.
"""
import pathlib, subprocess, sys
from pypdf import PdfReader, PdfWriter

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import cutlines as CL

HERE = pathlib.Path(__file__).parent
OUT = HERE / "set"

for script in ("build_assignments.py", "build_set.py"):
    subprocess.run([sys.executable, str(HERE / script)], check=True,
                   stdout=subprocess.DEVNULL)

ORDER = ["ASSIGNMENTS", "gray-classroom", "yellow-classroom", "main-room-hallways",
         "boys-bathroom", "girls-bathroom", "teacher-lounge-outside",
         "final-walkthrough"]


def bordered(path):
    """Read a PDF and return its pages with the dashed card edge merged on."""
    pages = []
    for page in PdfReader(str(path)).pages:
        pw, ph = float(page.mediabox.width), float(page.mediabox.height)
        page.merge_page(CL.border(pw, ph))
        pages.append(page)
    return pages


print("Stamping cut borders...")

# individual cards, in place
for slug in ORDER:
    f = OUT / ("LLA-Cleanup-%s.pdf" % slug)
    meta = PdfReader(str(f)).metadata
    w = PdfWriter()
    for p in bordered(f):
        w.add_page(p)
    w.add_metadata(meta or {})
    with open(f, "wb") as fh:
        w.write(fh)
    print("  %-44s" % f.name)

# the combined eight-page set, assembled in print order
w = PdfWriter()
for slug in ORDER:
    w.add_page(PdfReader(str(OUT / ("LLA-Cleanup-%s.pdf" % slug))).pages[0])
w.add_metadata({"/Title": "LLA Cleanup Cards — Full Set 2026-2027",
                "/Author": "Lions Light Academy",
                "/Subject": "Assignments cover plus seven station cards, one per page"})
allf = OUT / "LLA-Cleanup-Cards-FULL-SET.pdf"
with open(allf, "wb") as fh:
    w.write(fh)
print("  %-44s %d pages  %.0f KB"
      % (allf.name, len(PdfReader(str(allf)).pages), allf.stat().st_size / 1024))
