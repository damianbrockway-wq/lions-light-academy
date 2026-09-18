import base64, pathlib
from playwright.sync_api import sync_playwright
from pypdf import PdfWriter, PdfReader
B = pathlib.Path("/home/claude/brand"); OUT = pathlib.Path("/home/claude/lla/pdf")
logo = base64.b64encode((B/"logo_gold.png").read_bytes()).decode()
body = (B/"receipt.html").read_text().replace("{logo}", logo)
tmp = B/"_rcpt.html"
tmp.write_text(f"""<!doctype html><html><head><meta charset="utf-8">
<style>
@font-face{{font-family:'Fraunces';src:url('fonts/Fraunces.ttf') format('truetype');font-weight:100 900}}
@font-face{{font-family:'Inter';src:url('fonts/Inter.ttf') format('truetype');font-weight:100 900}}
html{{-webkit-print-color-adjust:exact; print-color-adjust:exact}}
*{{box-sizing:border-box}}
</style></head><body>{body}</body></html>""")
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    pg.goto(f"file://{tmp}", wait_until="networkidle"); pg.emulate_media(media="print")
    pg.pdf(path=str(OUT/"supply-fee-receipt.pdf"), format="Letter", print_background=True,
           margin={"top":"14mm","bottom":"14mm","left":"15mm","right":"15mm"})
    b.close()
tmp.unlink()
print("built", (OUT/"supply-fee-receipt.pdf").stat().st_size//1024, "KB")
