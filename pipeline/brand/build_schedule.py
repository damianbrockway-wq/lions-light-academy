#!/usr/bin/env python3
"""Lions Light Academy — the Tuesday daily schedule.

schedule_page.html was rendered by hand once in August and never again, which
is most of the reason it sat unpublished with the wrong arrival time on it
while a planning document stood on the website in its place. This makes it
repeatable: edit the HTML, run this, push.

Landscape Letter, one page, asserted. Output goes to lla/pdf under the name
the site already links, so publishing is a copy rather than a rename.
"""
import pathlib, re
from playwright.sync_api import sync_playwright
from pypdf import PdfReader, PdfWriter

B = pathlib.Path("/home/claude/brand")
OUT = pathlib.Path("/home/claude/lla/pdf"); OUT.mkdir(parents=True, exist_ok=True)
SRC = B / "schedule_page.html"

# the site links this name; keep it so families' existing links keep working
SITE_NAME = "coop-day-schedule.pdf"
ARCHIVE_NAME = "LLA-Daily-Schedule-2026-2027.pdf"


def build():
    raw = B / "_sched.pdf"
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        pg.goto("file://%s" % SRC.resolve(), wait_until="networkidle")
        pg.emulate_media(media="print")
        pg.pdf(path=str(raw), width="11in", height="8.5in", print_background=True,
               margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
        b.close()

    r = PdfReader(str(raw))
    assert len(r.pages) == 1, "schedule MUST be one page, got %d" % len(r.pages)

    for name in (SITE_NAME, ARCHIVE_NAME):
        w = PdfWriter(); w.add_page(PdfReader(str(raw)).pages[0])
        w.add_metadata({"/Title": "Co-op Day Schedule — Lions Light Academy",
                        "/Author": "Lions Light Academy",
                        "/Subject": "Tuesday daily schedule, 2026-2027"})
        f = OUT / name
        with open(f, "wb") as fh:
            w.write(fh)
        print("  %-34s %5.0f KB" % (f.name, f.stat().st_size / 1024))
    raw.unlink()

    # the times are the whole point of this document — read them back out
    import subprocess
    txt = subprocess.run(["pdftotext", "-q", str(OUT / SITE_NAME), "-"],
                         capture_output=True, text=True).stdout
    times = re.findall(r"\d{1,2}:\d{2} – \d{1,2}:\d{2}", txt)
    print("  blocks found: %s" % ", ".join(times[:4]))
    assert "8:45 – 9:00" in txt, "arrival block is not 8:45"
    assert "8:30" in txt, "teacher arrival note missing"
    print("  arrival verified: students 8:45, teachers 8:30")


if __name__ == "__main__":
    build()
