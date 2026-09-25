import sys, base64, os, json
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
        f'<div class="frames">{"".join(frames)}</div></section>')

CSS = r"""
:root{--red:#CF102D;--black:#000;--gray:#E5ECEE;--white:#fff;--ui:Arial,"Liberation Sans",Helvetica,sans-serif}
*{box-sizing:border-box}
html,body{margin:0;background:#fff;color:#000;font-family:var(--ui)}
/* ---------- app shell ---------- */
.topbar{position:fixed;top:0;left:0;right:0;height:60px;background:#fff;border-bottom:1px solid var(--gray);display:flex;align-items:center;gap:6px;padding:0 20px 0 0;z-index:20}
.topbar .mark{width:8px;height:44px;background:var(--red);clip-path:polygon(0 0,100% 10%,100% 90%,0 100%);margin-right:20px}
.topbar .brand{display:flex;align-items:center;gap:14px;margin-right:auto}
.topbar .brand svg{height:22px;width:auto;display:block}
.topbar .brand b{font-size:14px;letter-spacing:-.01em}
.topbar .brand span{font-size:12px;border-left:1px solid var(--gray);padding-left:14px}
.btn{font:700 12px var(--ui);color:#000;background:#fff;border:1px solid var(--gray);border-radius:0;padding:8px 12px;cursor:pointer}
.btn:hover{border-color:#000}.btn.on{background:#000;color:#fff;border-color:#000}.btn.red{background:var(--red);border-color:var(--red);color:#fff}
.seg{display:flex}.seg .btn+.btn{border-left:0}
.sep{width:1px;height:26px;background:var(--gray);margin:0 8px}
.sidebar{position:fixed;top:60px;bottom:0;left:0;width:250px;border-right:1px solid var(--gray);background:#fff;overflow:auto;padding:22px 0;z-index:10}
.sidebar h3{font-size:11px;margin:0 22px 10px;color:var(--red)}
.nav-item{display:flex;justify-content:space-between;align-items:center;padding:9px 22px;color:#000;text-decoration:none;font-size:14px;font-weight:700;border-left:4px solid transparent}
.nav-item em{font-style:normal;font-weight:400;font-size:12px}
.nav-item:hover{background:var(--gray)}.nav-item.on{border-left-color:var(--red)}
.sidebar .rules{margin:22px 22px 0;padding-top:18px;border-top:1px solid var(--gray);font-size:12px;line-height:1.5}
.sidebar .rules b{display:block;font-size:11px;color:var(--red);margin-bottom:6px}
.sidebar .rules div{margin-bottom:6px}
.sw{display:inline-block;width:10px;height:10px;margin-right:6px;vertical-align:-1px;border:1px solid var(--gray)}
.canvas{margin:60px 0 0 250px;padding:40px 48px 120px}
.lib-section{margin-bottom:80px}
.sec-head{display:flex;gap:18px;align-items:flex-start;margin:0 0 28px -48px}
.sec-notch{width:8px;height:120px;background:var(--red);clip-path:polygon(0 0,100% 11%,100% 89%,0 100%);flex:none}
.sec-label{font-size:12px;font-weight:700;color:var(--red);margin:0 0 4px 22px}
.sec-head h2{font-size:40px;line-height:1;letter-spacing:-.025em;margin:0 0 10px 22px}
.sec-head p{font-size:14px;line-height:1.45;margin:0 0 0 22px;max-width:680px}
.frames{display:flex;flex-wrap:wrap;gap:40px 36px;align-items:flex-start}
.frame{margin:0}
.frame-meta{display:flex;flex-direction:column;gap:2px;margin-bottom:10px;font-size:12px;line-height:1.35}
.frame-meta b{font-size:13px}
.ab-wrap{position:relative;overflow:hidden;outline:1px solid var(--gray)}
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
.guide.label{font:700 11px var(--ui);color:#00a3ff;background:none;border:0}
.toast{position:fixed;left:50%;bottom:24px;transform:translateX(-50%);background:#000;color:#fff;font:700 12px var(--ui);padding:10px 16px;opacity:0;transition:opacity .2s;z-index:40;pointer-events:none}
/* ---------- Figma import view: true size, no chrome ---------- */
body.figma .topbar,body.figma .toast,body.figma .sidebar,body.figma .sec-head,body.figma .frame-meta{display:none}
body.figma .canvas{margin:0;padding:60px}
body.figma .frames{gap:120px}
body.figma .ab-wrap{outline:0}
@media print{.topbar,.sidebar,.sec-head,.frame-meta{display:none}.canvas{margin:0;padding:0}.frame{break-after:page}}
"""

LOGO_UI = f'<svg viewBox="0 0 152 52" fill="#000">{LOGO_PATHS}</svg>'

JS = r"""
(function(){
  const IMG = JSON.parse(document.getElementById('img-data').textContent);
  const $ = (s,r=document)=>r.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)];
  const MARG = __MARGINS__;
  function loadImages(){ $$('.ab img[data-img]').forEach(i=>{ const k=i.dataset.img; if(IMG[k] && !i.dataset.custom) i.src=IMG[k]; }); }
  loadImages();

  /* zoom */
  let mode = 'fit';
  function layout(){
    const avail = Math.max(320, document.querySelector('.canvas').clientWidth - 96);
    $$('.frame').forEach(f=>{
      const ab=$('.ab',f), wr=$('.ab-wrap',f), w=ab.offsetWidth, h=ab.offsetHeight;
      let s=1;
      if(document.body.classList.contains('figma')) s=1;
      else if(mode==='fit') s=Math.min(1, 560/h, avail/w, (w<400&&h<400)?1:9);
      else s=+mode;
      ab.style.transform = s===1?'':`scale(${s})`;
      wr.style.width = w*s+'px'; wr.style.height = h*s+'px';
    });
  }
  window.addEventListener('resize', layout); layout();
  $$('[data-zoom]').forEach(b=>b.onclick=()=>{ mode=b.dataset.zoom; $$('[data-zoom]').forEach(x=>x.classList.toggle('on',x===b)); layout(); });

  /* guides */
  let guides=false;
  function drawGuides(){
    $$('.guide').forEach(g=>g.remove()); if(!guides) return;
    $$('.frame').forEach(f=>{
      const ab=$('.ab',f), fmt=f.dataset.fmt, m=MARG[fmt]; const w=ab.offsetWidth,h=ab.offsetHeight;
      if(m){ const g=document.createElement('div'); g.className='guide margin'; Object.assign(g.style,{left:m+'px',top:m+'px',width:(w-2*m)+'px',height:(h-2*m)+'px'}); ab.appendChild(g); }
      if(fmt==='story'){ [[0,250],[h-340,340]].forEach(([t,hh])=>{ const g=document.createElement('div'); g.className='guide safe'; Object.assign(g.style,{left:0,top:t+'px',width:w+'px',height:hh+'px'}); ab.appendChild(g); }); }
    });
  }
  $('#btn-guides').onclick=e=>{ guides=!guides; e.currentTarget.classList.toggle('on',guides); drawGuides(); };

  /* edit text + replace images */
  let editing=false;
  $('#btn-edit').onclick=e=>{ editing=!editing; e.currentTarget.classList.toggle('on',editing); document.body.classList.toggle('editing',editing);
    $$('.ab .tx').forEach(t=>{ if(editing) t.setAttribute('contenteditable','true'); else t.removeAttribute('contenteditable'); });
    toast(editing?'Click any text to edit it. Double-click an image to replace it.':'Editing off'); };
  const picker=document.createElement('input'); picker.type='file'; picker.accept='image/*'; let target=null;
  picker.onchange=()=>{ const f=picker.files[0]; if(!f||!target) return; const r=new FileReader(); r.onload=()=>{ target.src=r.result; target.dataset.custom='1'; toast('Image replaced'); }; r.readAsDataURL(f); picker.value=''; };
  document.addEventListener('dblclick',e=>{ if(!editing) return; const i=e.target.closest('.ab img'); if(i){ target=i; picker.click(); } });

  /* figma view */
  function setFigma(on){ document.body.classList.toggle('figma',on); $('#btn-figma').classList.toggle('on',on); if(on&&guides){ guides=false; $('#btn-guides').classList.remove('on'); drawGuides(); } layout();
    if(!on) toast('Figma import view off'); }
  $('#btn-figma').onclick=()=>setFigma(!document.body.classList.contains('figma'));
  if(/[?&#]figma\b/.test(location.href)) setFigma(true);
  document.addEventListener('keydown',e=>{ if(e.key==='Escape'&&document.body.classList.contains('figma')) setFigma(false); });

  /* save */
  $('#btn-save').onclick=async()=>{
    const wasEdit=editing; if(editing) $('#btn-edit').click(); guides&&$('#btn-guides').click();
    const doc=document.documentElement.cloneNode(true);
    doc.querySelectorAll('.ab img[data-img]').forEach(i=>{ if(!i.dataset.custom) i.removeAttribute('src'); });
    doc.querySelectorAll('.ab').forEach(a=>a.style.transform=''); doc.querySelector('body').className='';
    const blob=new Blob(['<!doctype html>\n'+doc.outerHTML],{type:'text/html'}); const name='Sonim_Brand_Template_Library_edited.html';
    try{ if(window.showSaveFilePicker){ const h=await showSaveFilePicker({suggestedName:name,types:[{description:'HTML',accept:{'text/html':['.html']}}]}); const w=await h.createWritable(); await w.write(blob); await w.close(); toast('Saved '+h.name); return; } }catch(err){ if(err.name==='AbortError') return; }
    const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download=name; a.click(); toast('Saved to Downloads');
    if(wasEdit) $('#btn-edit').click();
  };

  /* nav highlight */
  const secs=$$('.lib-section'); const io=new IntersectionObserver(es=>es.forEach(en=>{ if(en.isIntersecting){ $$('.nav-item').forEach(n=>n.classList.toggle('on',n.dataset.sec===en.target.id.slice(4))); } }),{rootMargin:'-40% 0px -55% 0px'});
  secs.forEach(s=>io.observe(s));
  function toast(t){ const el=$('#toast'); el.textContent=t; el.style.opacity=1; clearTimeout(toast.t); toast.t=setTimeout(()=>el.style.opacity=0,2400); }
  window.lib={layout,setFigma};
})();
""".replace('__MARGINS__', json.dumps(MARGINS))

total = len(T.F)
page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sonim brand template library</title>
<style>{CSS}</style>
</head>
<body>
<header class="topbar" data-name="App bar">
  <div class="mark"></div>
  <div class="brand hide-figma">{LOGO_UI}<b>Brand template library</b><span>{total} templates · one system</span></div>
  <div class="seg hide-figma"><button class="btn on" data-zoom="fit">Fit</button><button class="btn" data-zoom="0.25">25%</button><button class="btn" data-zoom="0.5">50%</button><button class="btn" data-zoom="1">100%</button></div>
  <span class="sep hide-figma"></span>
  <button class="btn hide-figma" id="btn-guides" title="Margins and story safe zones">Guides</button>
  <button class="btn hide-figma" id="btn-edit" title="Edit text and replace images">Edit</button>
  <button class="btn hide-figma" id="btn-save">Save file</button>
  <button class="btn red" id="btn-figma" title="True size, no labels: use this view for HTML to Figma import">Figma import view</button>
</header>
<nav class="sidebar" data-name="Sections">
  <h3>Template sets</h3>
  {''.join(nav)}
  <div class="rules">
    <b>System rules</b>
    <div><span class="sw" style="background:#CF102D"></span>Sonim Red · <span class="sw" style="background:#000"></span>Black · <span class="sw" style="background:#E5ECEE"></span>Gray · <span class="sw" style="background:#fff"></span>White. No tints.</div>
    <div>Akzidenz Grotesk Bold / Regular; Arial where it is not installed.</div>
    <div>Sentence case, flush left. Headline in black, key phrase in red, ending with a period.</div>
    <div>Margin ≈ 7.4% of the short side. Notch = X × 18X, X = margin ÷ 5, on the left edge, top aligned to the label.</div>
    <div>Logo single colour, bottom-left on the margin. Min 0.5 in / 50 px.</div>
    <div>No red type on black. No gray type on white. Photography never tinted.</div>
  </div>
</nav>
<main class="canvas" data-name="Canvas">
{''.join(sections_html)}
</main>
<div class="toast" id="toast"></div>
<script id="img-data" type="application/json">{json.dumps(IMG)}</script>
<script>{JS}</script>
</body>
</html>"""
out = HERE.parent / 'dist' / 'Sonim_Brand_Template_Library.html'
open(out, 'w').write(page)
print(round(len(page) / 1e6, 2), 'MB', total, 'templates')
