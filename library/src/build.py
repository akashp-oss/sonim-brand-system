import sys, base64, os, json, re
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from gen import *
import templates as T

IMG = {}
for f in sorted(os.listdir(HERE / 'img')):
    k, ext = f.rsplit('.', 1)
    IMG[k] = f'data:image/{"jpeg" if ext == "jpg" else ext};base64,' + base64.b64encode(open(HERE / 'img' / f, 'rb').read()).decode()

MARGINS = {'doc': 60, 'slide': 120, 'post': 80, 'story': 80, 'land': 64, 'poster': 96, 'rollup': 56, 'other': 64}

sections_html, nav = [], []
for sid, title, intro in T.SECTION_META:
    frames = [h for s, h in T.F if s == sid]
    nav.append(f'<a class="nav-item" href="#sec-{sid}" data-sec="{sid}"><span>{esc(title)}</span><em>{len(frames)}</em></a>')
    sections_html.append(
        f'<section class="lib-section" id="sec-{sid}" data-name="{esc(title)}">'
        f'<header class="sec-head"><div class="sec-notch"></div><div><div class="sec-label">Template set</div><h2>{esc(title)}</h2><p>{esc(intro)}</p></div></header>'
        f'<h2 class="figma-title" data-name="{esc(title)} title">{esc(title)}</h2>'
        f'<div class="frames">{"".join(frames)}</div></section>')

CSS = r"""
:root{--red:#CF102D;--black:#000;--gray:#E5ECEE;--white:#fff;--line:#E5ECEE;--ui:Arial,"Liberation Sans",Helvetica,sans-serif;--top:64px;--side:288px;--bg:#F5F5F5}
*{box-sizing:border-box}
html{scroll-padding-top:calc(var(--top) + 16px)}
html,body{margin:0;background:var(--bg);color:#000;font-family:var(--ui)}
button{font-family:var(--ui)}
:focus-visible{outline:2px solid var(--red);outline-offset:2px}
/* slim scrollbars */
*{scrollbar-width:thin;scrollbar-color:#C4C4C4 transparent}
::-webkit-scrollbar{width:8px;height:8px}::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:#C4C4C4;border:2px solid transparent;background-clip:padding-box}
::-webkit-scrollbar-thumb:hover{background:#8A8A8A;background-clip:padding-box}
/* ---------- app bar ---------- */
.topbar{position:fixed;top:0;left:0;right:0;height:var(--top);background:#000;color:#fff;display:flex;align-items:center;gap:8px;padding:0 16px 0 0;z-index:30}
.topbar .mark{width:8px;height:44px;background:var(--red);clip-path:polygon(0 0,100% 10%,100% 90%,0 100%);flex:none;margin-right:16px}
.topbar .brand{display:flex;align-items:center;gap:14px;margin-right:auto;min-width:0}
.topbar .brand svg{height:22px;width:auto;display:block;flex:none}
.topbar .brand b{font-size:14px;letter-spacing:-.01em;white-space:nowrap}
.topbar .brand span{font-size:12px;border-left:1px solid #333;padding-left:14px;white-space:nowrap}
.btn{font:700 13px/1 var(--ui);color:#fff;background:transparent;border:1px solid #444;border-radius:0;height:38px;padding:0 16px;transition:background .15s,border-color .15s,color .15s;cursor:pointer;white-space:nowrap}
.btn:hover{border-color:#fff}.btn.on{background:#fff;color:#000;border-color:#fff}.btn.red{background:var(--red);border-color:var(--red);color:#fff}
.btn.red:hover,.btn.red.on{background:#fff;border-color:#fff;color:#000}
.seg{display:flex}.seg .btn+.btn{margin-left:-1px}
.sep{width:1px;height:26px;background:#333;margin:0 4px}
#btn-menu{display:none}
/* ---------- sidebar ---------- */
.sidebar{position:fixed;top:var(--top);bottom:0;left:0;width:var(--side);border-right:1px solid #E0E0E0;background:#fff;overflow:auto;padding:28px 0 32px;z-index:20}
.side-h{font-size:11px;font-weight:700;color:var(--red);margin:0 24px 8px}
.nav-item{display:flex;justify-content:space-between;align-items:center;padding:8px 24px 8px 20px;color:#000;text-decoration:none;font-size:14px;font-weight:700;border-left:4px solid transparent}
.nav-item em{font-style:normal;font-weight:400;font-size:12px;min-width:20px;text-align:right}
.nav-item:hover{background:var(--gray)}.nav-item.on{border-left-color:var(--red)}
.rules{margin:24px 0 0;padding:20px 24px 0;border-top:1px solid var(--line)}
.rules .side-h{margin:0 0 12px}
.rule{padding:12px 0;border-top:1px solid var(--line)}
.rule:first-of-type{border-top:0;padding-top:0}
.rule h4{font-size:12px;margin:0 0 8px;font-weight:700}
.rule p,.rule li{font-size:12px;line-height:1.45;margin:0}
.rule ul{list-style:none;margin:0;padding:0;display:grid;gap:4px}
.rule li{display:flex;gap:8px;align-items:baseline}
.rule li i{font-style:normal;font-weight:700;flex:none;width:10px}
.rule li.no i{color:var(--red)}
.chips{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-bottom:8px}
.chip{display:flex;align-items:center;gap:8px;padding:6px;border:1px solid var(--line);background:#fff;cursor:pointer;text-align:left;font:11px/1.2 var(--ui);color:#000}
.chip:hover{border-color:#000}
.chip s{display:block;width:22px;height:22px;flex:none;border:1px solid var(--line)}
.chip b{display:block;font-size:11px}
.sample{font-size:15px;font-weight:700;line-height:1.1;letter-spacing:-.015em;margin:2px 0 8px}
.sample em{font-style:normal;color:var(--red)}
.kv{display:grid;grid-template-columns:auto 1fr;gap:4px 10px;font-size:12px;line-height:1.4}
.kv dt{font-weight:700}.kv dd{margin:0}
.hint{margin:16px 24px 0;padding:12px;background:var(--gray);font-size:12px;line-height:1.45}
.hint b{display:block;margin-bottom:4px}
.scrim{display:none}
/* ---------- canvas ---------- */
.canvas{margin:var(--top) 0 0 var(--side);padding:56px 56px 160px}
.lib-section{margin-bottom:0;padding-bottom:120px}
.lib-section+.lib-section{padding-top:72px;border-top:1px solid #E0E0E0}
.sec-head{display:flex;gap:40px;align-items:flex-start;margin:0 0 40px -56px}
.sec-notch{width:8px;height:112px;background:var(--red);clip-path:polygon(0 0,100% 11%,100% 89%,0 100%);flex:none}
.sec-label{font-size:12px;font-weight:700;color:var(--red);margin:0 0 6px}
.sec-head h2{font-size:40px;line-height:1;letter-spacing:-.025em;margin:0 0 12px}
.sec-head p{font-size:14px;line-height:1.45;margin:0;max-width:680px}
.frames{display:flex;flex-wrap:wrap;gap:64px 48px;align-items:flex-start}
.frame{margin:0;min-width:0}
.frame-meta{display:flex;flex-direction:column;gap:3px;margin-bottom:12px;font-size:12px;line-height:1.35}
.frame-meta b{font-size:13px}
.ab-wrap{position:relative;z-index:0;overflow:hidden;box-shadow:0 1px 2px rgba(0,0,0,.06),0 4px 16px rgba(0,0,0,.06)}
/* hover tools (UI only, never exported) */
.frame-tools{position:absolute;top:8px;right:8px;display:flex;gap:4px;opacity:0;transform:translateY(-4px);transition:opacity .15s,transform .15s;z-index:60}
.ab-wrap:hover .frame-tools,.frame-tools:focus-within{opacity:1;transform:none}
.frame.tiny .ab-wrap{overflow:visible}
.frame.tiny .frame-tools{bottom:auto;top:calc(100% + 6px);right:auto;left:0;opacity:1;transform:none}
.frame.tiny{margin-bottom:34px}
.tool{font:700 12px/1 var(--ui);height:32px;padding:0 14px;border:0;background:var(--red);color:#fff;cursor:pointer;display:flex;align-items:center;gap:6px;white-space:nowrap}
.tool:hover{background:#000}
.tool.icon{padding:0 7px}
.tool.done{background:#000}
.tool:disabled{cursor:progress;opacity:.7}
.ab{position:relative;overflow:hidden;transform-origin:0 0;font-family:Arial,"Liberation Sans",Helvetica,sans-serif;color:#000;--em:#CF102D}
/* ---------- artboard primitives (these become Figma layers) ---------- */
.ab .abs{position:absolute}
.ab .stack{display:flex;flex-direction:column}
.ab .row{display:flex;flex-direction:row}
.ab .grid2{display:grid;grid-template-columns:1fr 1fr;grid-auto-rows:1fr}
.ab .tx{margin:0;white-space:normal}
.ab .em{color:var(--em)}
.ab img{display:block;max-width:none}
.ab .photo{object-fit:cover}
.ab .cutout{object-fit:contain}
.ab svg{display:block;overflow:visible}
.ab .icon svg{width:100%;height:100%}
.ab .photo-frame{position:relative;overflow:hidden;flex:none}
/* type roles: sizes are set per template, roles fix weight, leading and tracking */
.ab .display{font-weight:700;line-height:.94;letter-spacing:-.03em}
.ab .h1{font-weight:700;line-height:1;letter-spacing:-.025em}
.ab .h2{font-weight:700;line-height:1.1;letter-spacing:-.015em}
.ab .h3{font-weight:700;line-height:1.2}
.ab .label{font-weight:700;line-height:1.2}
.ab .lead{font-weight:400;line-height:1.3}
.ab .body{font-weight:400;line-height:1.45}
.ab .small{font-weight:400;line-height:1.35}
.ab .meta{font-weight:700;line-height:1.2}
.ab .stat{font-weight:700;line-height:.92;letter-spacing:-.035em}
.ab .quote{font-weight:700;line-height:1.12;letter-spacing:-.015em}
/* ---------- editing + guides (never exported) ---------- */
body.editing .ab .tx{cursor:text}
body.editing .ab .tx:hover{outline:1px dashed var(--red)}
body.editing .ab img{cursor:copy}
.ab [contenteditable]:focus{outline:2px solid var(--red)}
.guide{position:absolute;pointer-events:none;z-index:50}
.guide.margin{border:1px dashed #00a3ff}
.guide.safe{background:rgba(0,163,255,.12);border-top:1px dashed #00a3ff;border-bottom:1px dashed #00a3ff}
.toast{position:fixed;left:50%;bottom:24px;transform:translate(-50%,8px);background:#000;color:#fff;font:700 12px/1.4 var(--ui);padding:10px 16px;max-width:calc(100vw - 32px);opacity:0;transition:opacity .2s,transform .2s;z-index:80;pointer-events:none}
.toast.show{opacity:1;transform:translate(-50%,0)}
/* ---------- responsive ---------- */
@media (max-width:1180px){.topbar .brand span{display:none}}
@media (max-width:980px){
  #btn-menu{display:block}
  .sidebar{transform:translateX(-100%);transition:transform .2s;z-index:40;width:min(300px,86vw)}
  body.nav-open .sidebar{transform:none}
  body.nav-open .scrim{display:block;position:fixed;inset:var(--top) 0 0 0;background:rgba(0,0,0,.35);z-index:35}
  .canvas{margin-left:0;padding:32px 24px 96px}
  .sec-head{margin-left:-24px;gap:16px}
  .seg,.sep{display:none}
}
@media (max-width:640px){
  .topbar .brand b,#btn-guides,#btn-save{display:none}
  .canvas{padding:24px 16px 80px}.sec-head{margin-left:-16px;gap:8px}.sec-head h2{font-size:30px}
  .frame-tools{opacity:1;transform:none}
}
@media (hover:none){.frame-tools{opacity:1;transform:none}}
/* ---------- Figma import view: true size, no chrome ---------- */
body.figma .topbar,body.figma .sidebar,body.figma .sec-head,body.figma .frame-meta,body.figma .frame-tools,body.figma .scrim{display:none}
body.figma .canvas{margin:0;padding:60px}
body.figma .frames{gap:120px}
body.figma .ab-wrap{box-shadow:none}
body.figma,body.figma .canvas{background:#fff}
body.figma .toast{z-index:95}

/* Figma import view bar: pick a set, exit */
.figma-bar,.figma-title{display:none}
body.figma .figma-bar{display:flex;position:fixed;top:0;left:0;right:0;z-index:90;align-items:center;gap:16px;padding:12px 16px;background:#000;color:#fff;font-size:12px}
.figma-bar b{white-space:nowrap}
.chips-row{display:flex;gap:4px;overflow-x:auto;flex:1;scrollbar-width:thin}
.fchip{font:700 12px/1 var(--ui);height:34px;padding:0 12px;border:1px solid #444;background:transparent;color:#fff;cursor:pointer;white-space:nowrap}
.fchip:hover{border-color:#fff}.fchip.on{background:var(--red);border-color:var(--red)}
.figma-bar kbd{font:400 10px var(--ui);border:1px solid currentColor;padding:1px 4px;margin-left:4px}
body.figma .canvas{padding-top:110px}
body.figma .figma-title{display:block;font-size:40px;line-height:1;letter-spacing:-.025em;margin:0 0 40px}
body.figma .lib-section{margin-bottom:160px;border-top:0;padding-top:0;padding-bottom:0}
@media print{.figma-bar{display:none}.topbar,.sidebar,.sec-head,.frame-meta,.frame-tools{display:none}.canvas{margin:0;padding:0}.frame{break-after:page}}
"""

LOGO_UI = f'<svg viewBox="0 0 152 52" fill="#000" aria-label="Sonim">{LOGO_PATHS}</svg>'
# favicon: the logo's "i" + connectivity lines, white on Sonim Red
_MARK = ''.join(re.findall(r'<rect x="92[^>]*/>|<path d="M(?:108\.505|104\.667|100\.871)[^>]*/>', LOGO_PATHS))
FAVICON = ('data:image/svg+xml,' + __import__('urllib.parse').parse.quote(
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="63 -7 64 64"><rect x="63" y="-7" width="64" height="64" fill="#CF102D"/><g fill="#fff">{_MARK}</g></svg>'))
JS = (open(HERE / 'export.js').read() + '\n' + open(HERE / 'app.js').read()).replace('__MARGINS__', json.dumps(MARGINS))

CHIPS = ''.join(f'<button class="chip" data-hex="{h}" title="Copy {h}"><s style="background:{h}"></s><span><b>{n}</b>{h}</span></button>'
                for n, h in [('Sonim Red', '#CF102D'), ('Black', '#000000'), ('Gray', '#E5ECEE'), ('White', '#FFFFFF')])
RULES = f"""
<div class="rules" data-name="Brand rules">
  <div class="side-h">Brand rules</div>
  <div class="rule"><h4>Colour</h4><div class="chips">{CHIPS}</div><p>Four colours only. No tints, gradients or shadows. Click a chip to copy its HEX.</p></div>
  <div class="rule"><h4>Type</h4>
    <div class="sample">Headline in black, <em>key phrase in red.</em></div>
    <dl class="kv"><dt>Font</dt><dd>Akzidenz Grotesk Bold / Regular. Arial if not installed.</dd><dt>Case</dt><dd>Sentence case, flush left, ends with a period.</dd></dl></div>
  <div class="rule"><h4>Layout</h4>
    <dl class="kv"><dt>Margin</dt><dd>M ≈ 7.4% of the short side</dd><dt>Notch</dt><dd>X × 18X, X = M ÷ 5. Left edge, top aligned to the label.</dd></dl></div>
  <div class="rule"><h4>Logo</h4>
    <dl class="kv"><dt>Colour</dt><dd>Single colour only</dd><dt>Place</dt><dd>Bottom-left, on the margin</dd><dt>Min</dt><dd>50 px / 0.5 in</dd></dl></div>
  <div class="rule"><h4>Never</h4><ul>
    <li class="no"><i>×</i>Red type on black</li><li class="no"><i>×</i>Gray type on white</li>
    <li class="no"><i>×</i>Tinted or filtered photography</li><li class="no"><i>×</i>All caps or Title Case</li></ul></div>
</div>
<div class="hint"><b>Copy to Figma</b>Hover any template and click <b style="display:inline">Copy SVG</b>, then press Ctrl/⌘ + V in Figma. For many at once, use <b style="display:inline">Figma import view</b>: pick a set, then run your HTML to Figma plugin.</div>
"""

total = len(T.F)
page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sonim brand template library</title>
<link rel="icon" type="image/svg+xml" href="{FAVICON}">
<style>{CSS}</style>
</head>
<body>
<header class="topbar" data-name="App bar">
  <div class="mark"></div>
  <button class="btn" id="btn-menu" aria-label="Template sets">Menu</button>
  <div class="brand">{LOGO_UI.replace('fill="#000"','fill="#fff"')}<b>Brand template library</b><span>{total} templates · one system</span></div>
  <div class="seg" role="group" aria-label="Zoom"><button class="btn on" data-zoom="fit">Fit</button><button class="btn" data-zoom="0.25">25%</button><button class="btn" data-zoom="0.5">50%</button><button class="btn" data-zoom="1">100%</button></div>
  <span class="sep"></span>
  <button class="btn" id="btn-guides" title="Show margins and story safe zones">Guides</button>
  <button class="btn" id="btn-edit" title="Edit text and replace images">Edit</button>
  <button class="btn" id="btn-save" title="Save a self-contained copy with your edits">Save file</button>
  <button class="btn red" id="btn-figma" title="True size, no labels: use this view for HTML to Figma import">Figma import view</button>
</header>
<nav class="sidebar" data-name="Sections">
  <div class="side-h">Template sets</div>
  {''.join(nav)}
  {RULES}
</nav>
<div class="scrim"></div>
<div class="figma-bar" data-name="Figma view bar">
  <b>Figma import view</b>
  <div class="chips-row"><button class="fchip on" data-only="">All</button>{''.join(f'<button class="fchip" data-only="{sid}">{esc(t)}</button>' for sid, t, _ in T.SECTION_META)}</div>
  <button class="btn" id="btn-exit-figma">Exit <kbd>Esc</kbd></button>
</div>
<main class="canvas" data-name="Canvas">
{''.join(sections_html)}
</main>
<div class="toast" id="toast" role="status" aria-live="polite"></div>
<script id="img-data" type="application/json">{json.dumps(IMG)}</script>
<script>{JS}</script>
</body>
</html>"""
out = HERE.parent / 'dist' / 'Sonim_Brand_Template_Library.html'
open(out, 'w').write(page)
print(round(len(page) / 1e6, 2), 'MB', total, 'templates')
