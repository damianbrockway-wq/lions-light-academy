#!/usr/bin/env python3
"""Lions Light Academy — Student Pledge, one page.

The Code of Conduct v1.2 rewritten in the student's own voice: a pledge they
read and sign, not a policy they receive. Same brand system as the ID cards
and the cleanup set. Portrait Letter, exactly one page.
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

HTML = """<!doctype html><html><head><meta charset="utf-8">
<title>My Pledge</title><style>
@font-face{font-family:'Inter';src:url(data:font/ttf;base64,%(inter)s) format('truetype');font-weight:100 900}
@font-face{font-family:'Fraunces';src:url(data:font/ttf;base64,%(fraunces)s) format('truetype');font-weight:100 900}
@page{size:Letter portrait;margin:0}
*{box-sizing:border-box;margin:0;padding:0;-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{font-family:'Inter',sans-serif;color:#16232F;background:#fff;
  width:8.5in;height:11in;display:flex;flex-direction:column}

.panel{background:#0A1929;color:#F2F5F8;padding:0.28in 0.62in 0.24in;position:relative}
.lockup{display:flex;align-items:center;gap:8px}
.lockup img{width:0.33in}
.lockup .txt{display:flex;flex-direction:column;line-height:1.15}
.org{font-size:7.2pt;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:#E6BD63}
.loc{font-size:6.4pt;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:#8FA3B8;margin-top:1px}
h1{font-family:'Fraunces',Georgia,serif;font-size:24pt;font-weight:600;line-height:1.02;margin-top:0.10in}
.sub{font-size:8.8pt;color:#AFC0D2;margin-top:5px;line-height:1.38;max-width:5.3in}
.yr{position:absolute;right:0.62in;top:0.38in;font-size:7.8pt;font-weight:600;
  letter-spacing:.12em;text-transform:uppercase;color:#8FA3B8}
.bar{height:0.12in;background:#E6BD63}

.body{flex:1;padding:0.26in 0.62in 0}
h2{font-family:'Fraunces',Georgia,serif;font-size:13.4pt;font-weight:600;
  margin-top:0.22in;margin-bottom:6px}
h2:first-child{margin-top:0}
.rule{height:2px;width:0.62in;background:#E6BD63;margin-bottom:9px}

ul{list-style:none}
li{font-size:10pt;line-height:1.42;margin-bottom:6px;position:relative;padding-left:0.27in}
li::before{content:"";position:absolute;left:0;top:3.5px;width:12px;height:12px;
  border:1.5px solid #8A94A0;border-radius:2px;background:#fff}
li.key::before{border-color:#C08A2E;border-width:2px}
li.key{font-weight:600}
.gloss{display:block;font-weight:400;font-size:8.6pt;font-style:italic;
  color:#8A6210;margin-top:2px}
strong{font-weight:700}
em{font-style:italic}

.strikes{margin:7px 0 8px 0.27in;border-left:2.5px solid #E6BD63;padding-left:0.17in}
.strikes div{font-size:9.6pt;line-height:1.4;margin-bottom:4px;color:#3C4756}
.strikes b{color:#0A1929;font-weight:700}

.sig{margin:0.18in 0.62in 0;border-top:1.5px solid #0A1929;padding-top:0.14in}
.sig .q{font-family:'Fraunces',Georgia,serif;font-size:11pt;line-height:1.3}
.row{display:flex;gap:0.30in;margin-top:0.15in}
.f{flex:1}
.f.d{flex:0 0 1.7in}
.lbl{font-size:7.2pt;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:#6C7784}
.line{border-bottom:1px solid #A8B0B9;height:0.26in}
.note{font-size:8.2pt;color:#8A94A0;margin-top:0.12in;font-style:italic}
.foot{text-align:center;font-size:7.2pt;letter-spacing:.07em;text-transform:uppercase;
  color:#9AA3AE;font-weight:600;padding:0.13in 0 0.20in}
</style></head><body>

<div class="panel">
  <div class="lockup"><img src="data:image/png;base64,%(logo)s" alt="">
    <div class="txt"><span class="org">Lions Light Academy</span>
    <span class="loc">Winslow, Maine</span></div></div>
  <div class="yr">2026&ndash;2027</div>
  <h1>My Pledge</h1>
  <p class="sub">Lions Light Academy is a co-op. My parents teach here, they volunteer here,
  and nobody is paid. Everyone chose to be here &mdash; including me.</p>
</div>
<div class="bar"></div>

<div class="body">
  <h2>What I will do</h2>
  <div class="rule"></div>
  <ul>
    <li class="key">I will do my homework carefully and finish it, even when it&rsquo;s hard.
      <span class="gloss">That is what <em>diligence</em> means.</span></li>
    <li>I will show up ready, and I will try.</li>
    <li>I will follow the adults in this building.</li>
    <li>I will speak and act in a way that respects the people around me.</li>
    <li>I will stay with my group and in the room I belong in.</li>
    <li>I will try the harder version when I&rsquo;m asked.</li>
    <li>I will clean up, and leave every space better than I found it.</li>
  </ul>

  <h2>What I understand</h2>
  <div class="rule"></div>
  <ul>
    <li><strong>Learning is my work.</strong> My teachers teach it and my parents support it,
      but nobody can do it for me.</li>
    <li>If I come without my work, I may be sent to finish it. <strong>The first time is
      not a punishment</strong> &mdash; nothing is written down and I am not in trouble.
      I finish it and I come back. <strong>But twice in a row, without a real reason, is a
      pattern &mdash; and that is a strike.</strong></li>
    <li>Small things get corrected in the moment. Nobody keeps a list.</li>
    <li>Other things are strikes too &mdash; repeating something after I&rsquo;ve been
      corrected, or being disrespectful.</li>
  </ul>
  <div class="strikes">
    <div><b>Strike one</b> &mdash; my parents hear about it, in writing.</div>
    <div><b>Strike two</b> &mdash; the same again.</div>
    <div><b>Strike three</b> &mdash; we all sit down together: me, my parents, my teacher and
      leadership. Not to decide <em>whether</em> I come back. To work out <em>how</em>.</div>
  </div>
  <ul>
    <li>Strikes count across every class and reset each year. If I finish the plan I sign,
      my count goes back to zero.</li>
    <li>Anything unsafe &mdash; hurting someone, threatening someone &mdash; happens
      <strong>immediately</strong>. No warnings, and my parents are called that day.</li>
    <li>If life gets hard, I can tell my teacher. They know me and they have room for that.
      A rough week <em>every</em> week isn&rsquo;t the same thing, and I know the difference.</li>
  </ul>
</div>

<div class="sig">
  <p class="q">I have read this. I understand it. I am choosing to keep it.</p>
  <div class="row">
    <div class="f"><div class="lbl">My name</div><div class="line"></div></div>
    <div class="f"><div class="lbl">My signature</div><div class="line"></div></div>
    <div class="f d"><div class="lbl">Date</div><div class="line"></div></div>
  </div>
  <div class="row">
    <div class="f"><div class="lbl">Parent or guardian &mdash; grade 6 and under</div><div class="line"></div></div>
    <div class="f d"><div class="lbl">Date</div><div class="line"></div></div>
  </div>
  <p class="note">Grade 7 and up sign for themselves.</p>
</div>
<div class="foot">Proverbs 25:2 &middot; Summary of the Lions Light Academy Code of Conduct v1.2</div>
</body></html>"""


def build():
    src = HERE / "_pledge.html"
    src.write_text(HTML % dict(inter=INTER, fraunces=FRAUNCES, logo=LOGO_WHITE))
    raw = HERE / "_pl.pdf"
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
    w.add_metadata({"/Title": "My Pledge — Lions Light Academy Student Code of Conduct",
                    "/Author": "Lions Light Academy",
                    "/Subject": "One-page student pledge, 2026-2027"})
    f = OUT / "LLA-Student-Pledge.pdf"
    with open(f, "wb") as fh:
        w.write(fh)
    print("  %s  %d page  %.0f KB" % (f.name, len(r.pages), f.stat().st_size / 1024))
    src.unlink(); raw.unlink()


if __name__ == "__main__":
    build()
