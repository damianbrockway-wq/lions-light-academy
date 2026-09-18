import base64, pathlib
from playwright.sync_api import sync_playwright
from pypdf import PdfWriter, PdfReader
B = pathlib.Path("/home/claude/brand"); OUT = pathlib.Path("/home/claude/lla/pdf")
logo = base64.b64encode((B/"logo_gold.png").read_bytes()).decode()
body = (B/"form_body.html").read_text()
V = "It is the glory of God to conceal a matter, but the glory of kings is to search it out."
cover = f"""<section class="cover"><div class="cover-body">
<img class="cover-mark" src="data:image/png;base64,{logo}" alt="">
<div class="cover-eyebrow">Lions Light Academy</div>
<h1 class="cover-title">Registration &amp;<br>Enrollment</h1>
<p class="cover-sub">2026&ndash;2027 School Year</p><div class="cover-rule"></div>
<div class="cover-verse">&ldquo;{V}&rdquo;<cite>Proverbs 25:2</cite></div></div>
<div class="cover-foot"><div class="cover-meta">
<div><div class="k">Effective</div><div class="v">September 15, 2026</div></div>
<div class="r"><div class="k">Document</div><div class="v">Form v2</div></div></div></div></section>"""
tmp = B/"_form.html"
tmp.write_text(f"""<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="brand.css"><link rel="stylesheet" href="form.css"></head>
<body>{body.replace("{logo}", logo)}</body></html>""")
FOOT = """<div style="width:100%;font-family:Inter,sans-serif;font-size:7pt;color:#8A94A0;
 padding:0 17mm;display:flex;justify-content:space-between;align-items:center;">
 <span style="letter-spacing:.06em">Registration &amp; Enrollment &middot; 2026&ndash;2027</span>
 <span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span></div>"""
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    pg.goto(f"file://{tmp}", wait_until="networkidle"); pg.emulate_media(media="print")
    pg.pdf(path="_b.pdf", format="Letter", print_background=True,
           display_header_footer=True, header_template="<div></div>", footer_template=FOOT,
           margin={"top":"19mm","bottom":"20mm","left":"17mm","right":"17mm"})
    b.close()
w = PdfWriter()
for x in PdfReader("_b.pdf").pages: w.add_page(x)
w.add_metadata({"/Title":"Registration & Enrollment 2026-2027","/Author":"Lions Light Academy"})
with open(OUT/"registration-enrollment.pdf","wb") as fh: w.write(fh)
pathlib.Path("_b.pdf").unlink()
tmp.unlink()
print("built", (OUT/"registration-enrollment.pdf").stat().st_size//1024, "KB")
