/* =====================================================================
   Sonim white paper editor — Figma-style, one page at a time.
   Open the HTML file in Chrome or Edge. Everything runs locally.
   ===================================================================== */
(function () {
  if (window.__fx) return; window.__fx = true;
  const PT = 0.75;                        // 1 CSS px = 0.75 pt
  const BRAND = [['Sonim Red', '#CF102D'], ['Sonim Black', '#000000'], ['Sonim Gray', '#E5ECEE'], ['White', '#FFFFFF']];
  const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const round = v => Math.round(v * 10) / 10;

  /* ---------- styles ---------- */
  const st = document.createElement('style'); st.id = 'fx-style';
  st.textContent = `
  html,body{height:100%}
  body.fx{margin:0;overflow:hidden;background:#1e1e1e;font-family:Arial,sans-serif}
  #fx-top{position:fixed;top:0;left:0;right:0;height:44px;background:#2c2c2c;border-bottom:1px solid #111;display:flex;align-items:center;gap:4px;padding:0 10px;z-index:30;color:#eee;font:12px Arial}
  #fx-top .brand{font-weight:700;margin-right:10px}
  .fx-btn{font:12px Arial;color:#eee;background:transparent;border:1px solid transparent;border-radius:4px;padding:5px 8px;cursor:pointer;white-space:nowrap}
  .fx-btn:hover{background:#3a3a3a}.fx-btn.on{background:#CF102D}.fx-btn.primary{background:#CF102D;color:#fff}
  .fx-btn:disabled{opacity:.35;cursor:default;background:transparent}
  .fx-sep{width:1px;height:22px;background:#444;margin:0 6px}
  #fx-zoom{min-width:44px;text-align:center}
  #fx-left,#fx-right{position:fixed;top:44px;bottom:0;background:#2c2c2c;color:#ddd;font:12px/1.35 Arial;overflow:auto;z-index:20}
  #fx-left{left:0;width:230px;border-right:1px solid #111}
  #fx-right{right:0;width:276px;border-left:1px solid #111}
  .fx-h{padding:10px 12px 6px;font-weight:700;color:#fff;font-size:11px;text-transform:none;letter-spacing:.02em;border-top:1px solid #3a3a3a}
  .fx-h:first-child{border-top:0}
  #fx-pages{display:grid;grid-template-columns:1fr 1fr;gap:8px;padding:4px 12px 12px}
  .fx-thumb{cursor:pointer;border:2px solid transparent;border-radius:3px;background:#fff;overflow:hidden;position:relative;height:124px}
  .fx-thumb.on{border-color:#CF102D}.fx-thumb .inner{transform-origin:top left;pointer-events:none;position:absolute;left:0;top:0}
  .fx-thumb span{position:absolute;left:4px;bottom:3px;background:rgba(0,0,0,.7);color:#fff;font-size:10px;padding:1px 4px;border-radius:2px}
  #fx-layers{padding:2px 0 20px}
  .fx-row{display:flex;align-items:center;gap:4px;padding:3px 8px 3px 0;cursor:pointer;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .fx-row:hover{background:#383838}.fx-row.on{background:#4a1a22}
  .fx-row .tw{width:14px;text-align:center;color:#999;flex:none}.fx-row .nm{overflow:hidden;text-overflow:ellipsis;flex:1}
  .fx-row .nm i{color:#888;font-style:normal}.fx-row .eye{color:#888;padding:0 4px;flex:none}.fx-row .eye:hover{color:#fff}
  .fx-row.hid .nm{opacity:.4}
  #fx-canvas{position:fixed;top:44px;left:230px;right:276px;bottom:0;overflow:auto;background:#e6e6e6}
  #fx-wrap{position:relative;margin:40px auto}
  #fx-stage{transform-origin:0 0;position:absolute;left:0;top:0}
  #fx-stage .page{margin:0 !important;box-shadow:0 2px 14px rgba(0,0,0,.18)}
  .fx-hidden{display:none !important}
  #fx-stage img{-webkit-user-drag:none;user-select:none}
  body.fx:not(.fx-editing) #fx-stage{user-select:none}
  #fx-overlay{position:fixed;inset:0;pointer-events:none;z-index:15}
  .fx-box{position:fixed;border:1.5px solid #CF102D;pointer-events:none}
  .fx-box.hover{border:1px solid #CF102D;opacity:.55}
  .fx-box.group{border:1px dashed #CF102D}
  .fx-tag{position:fixed;background:#CF102D;color:#fff;font:10px Arial;padding:1px 5px;border-radius:2px;pointer-events:none;white-space:nowrap}
  .fx-h8{position:fixed;width:8px;height:8px;background:#fff;border:1.5px solid #CF102D;pointer-events:auto;z-index:16}
  .fx-guide{position:fixed;background:#ff2d9b;pointer-events:none}
  .fx-grid{position:fixed;background:rgba(207,16,45,.07);pointer-events:none;border-left:1px solid rgba(207,16,45,.25);border-right:1px solid rgba(207,16,45,.25)}
  .fx-marg{position:fixed;border:1px dashed rgba(207,16,45,.5);pointer-events:none}
  #fx-props{padding:0 12px 20px}
  .fx-empty{padding:14px 12px;color:#999}
  .fx-grp{padding:8px 0;border-bottom:1px solid #3a3a3a}
  .fx-grp>b{display:block;color:#fff;font-size:11px;margin-bottom:6px}
  .fx-f{display:grid;grid-template-columns:repeat(2,1fr);gap:6px}
  .fx-f label{display:flex;align-items:center;gap:6px;background:#383838;border-radius:3px;padding:0 6px}
  .fx-f label span{color:#999;width:16px;flex:none;font-size:11px}
  .fx-f input,.fx-f select{width:100%;background:transparent;border:0;color:#fff;font:12px Arial;padding:5px 0;outline:none}
  .fx-f select option{background:#2c2c2c}
  .fx-icons{display:flex;gap:2px;flex-wrap:wrap}
  .fx-icons button{width:28px;height:26px;background:#383838;border:1px solid transparent;border-radius:3px;color:#ddd;cursor:pointer;display:flex;align-items:center;justify-content:center;padding:0}
  .fx-icons button:hover{border-color:#666}.fx-icons button.on{background:#CF102D;color:#fff}
  .fx-icons svg{width:16px;height:16px}
  .fx-sw{display:flex;gap:6px;align-items:center;flex-wrap:wrap}
  .fx-sw button{width:22px;height:22px;border-radius:3px;border:1px solid #555;cursor:pointer;padding:0}
  .fx-sw button.on{outline:2px solid #fff;outline-offset:1px}
  .fx-sw .none{background:linear-gradient(45deg,transparent 45%,#CF102D 45%,#CF102D 55%,transparent 55%),#fff}
  .fx-warn{margin-top:8px;padding:6px 8px;background:#4a1a22;border-radius:3px;color:#ffb3bf;font-size:11px}
  .fx-ok{margin-top:8px;color:#8fd19e;font-size:11px}
  .fx-acts{display:grid;grid-template-columns:1fr 1fr;gap:6px}
  .fx-acts button{background:#383838;border:0;color:#eee;border-radius:3px;padding:6px;cursor:pointer;font:12px Arial}
  .fx-acts button:hover{background:#474747}
  .fx-row .lk{color:#666;padding:0 2px;flex:none;display:flex}.fx-row .lk svg{width:11px;height:11px}.fx-row .lk:hover{color:#fff}.fx-row .lk.on{color:#f0b429}.fx-row .lk.inh{color:#8a6d1d}
  .fx-row.locked .nm{color:#bbb}
  #fx-flow{font-size:11px;padding:3px 8px;border-radius:10px;background:#383838;color:#9be0a9;white-space:nowrap}
  #fx-flow.over{background:#CF102D;color:#fff}
  .fx-over{position:fixed;background:repeating-linear-gradient(45deg,rgba(207,16,45,.28) 0 6px,rgba(207,16,45,.12) 6px 12px);border-top:1.5px solid #CF102D;pointer-events:none}
  .fx-limit{position:fixed;border-top:1px dashed rgba(207,16,45,.6);pointer-events:none}
  .fx-lockmsg{margin-top:8px;padding:8px;background:#3d3420;border-radius:3px;color:#f0d58a;font-size:11px;display:flex;justify-content:space-between;align-items:center;gap:8px}
  .fx-lockmsg button{background:#f0b429;border:0;border-radius:3px;padding:4px 8px;cursor:pointer;font:11px Arial;color:#111}
  #fx-toast{position:fixed;left:50%;bottom:18px;transform:translateX(-50%);background:#111;color:#fff;padding:8px 14px;border-radius:4px;font:12px Arial;z-index:40;opacity:0;transition:opacity .2s;pointer-events:none}
  #fx-help{position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:50;display:none;align-items:center;justify-content:center}
  #fx-help>div{background:#fff;color:#111;width:560px;max-height:80vh;overflow:auto;border-radius:6px;padding:18px 22px;font:13px/1.5 Arial}
  #fx-help h3{margin:0 0 8px;font-size:16px}#fx-help td{padding:3px 12px 3px 0;vertical-align:top}#fx-help kbd{background:#eee;border:1px solid #ccc;border-radius:3px;padding:0 4px;font:11px monospace}
  [contenteditable="true"]{outline:1.5px solid #CF102D !important;outline-offset:2px;cursor:text}
  @media print{
    #fx-top,#fx-left,#fx-right,#fx-overlay,#fx-toast,#fx-help{display:none !important}
    body.fx{overflow:visible;background:none;height:auto}
    #fx-canvas{position:static;overflow:visible;background:none}
    #fx-wrap{width:auto !important;height:auto !important;margin:0}
    #fx-stage{position:static;transform:none !important}
    #fx-stage .page{box-shadow:none}
    .fx-hidden{display:block !important}
  }`;
  document.head.appendChild(st);

  /* ---------- icons ---------- */
  const I = {
    al: '<svg viewBox="0 0 16 16" fill="currentColor"><rect x="2" y="2" width="1.5" height="12"/><rect x="5" y="4" width="9" height="3"/><rect x="5" y="9" width="5" height="3"/></svg>',
    ac: '<svg viewBox="0 0 16 16" fill="currentColor"><rect x="7.25" y="2" width="1.5" height="12"/><rect x="3" y="4" width="10" height="3"/><rect x="5" y="9" width="6" height="3"/></svg>',
    ar: '<svg viewBox="0 0 16 16" fill="currentColor"><rect x="12.5" y="2" width="1.5" height="12"/><rect x="2" y="4" width="9" height="3"/><rect x="6" y="9" width="5" height="3"/></svg>',
    at: '<svg viewBox="0 0 16 16" fill="currentColor"><rect x="2" y="2" width="12" height="1.5"/><rect x="4" y="5" width="3" height="9"/><rect x="9" y="5" width="3" height="5"/></svg>',
    am: '<svg viewBox="0 0 16 16" fill="currentColor"><rect x="2" y="7.25" width="12" height="1.5"/><rect x="4" y="3" width="3" height="10"/><rect x="9" y="5" width="3" height="6"/></svg>',
    ab: '<svg viewBox="0 0 16 16" fill="currentColor"><rect x="2" y="12.5" width="12" height="1.5"/><rect x="4" y="2" width="3" height="9"/><rect x="9" y="6" width="3" height="5"/></svg>',
    dh: '<svg viewBox="0 0 16 16" fill="currentColor"><rect x="1" y="4" width="3" height="8"/><rect x="6.5" y="4" width="3" height="8"/><rect x="12" y="4" width="3" height="8"/></svg>',
    dv: '<svg viewBox="0 0 16 16" fill="currentColor"><rect x="4" y="1" width="8" height="3"/><rect x="4" y="6.5" width="8" height="3"/><rect x="4" y="12" width="8" height="3"/></svg>',
    tl: '<svg viewBox="0 0 16 16" fill="currentColor"><rect x="2" y="3" width="12" height="1.5"/><rect x="2" y="6.5" width="8" height="1.5"/><rect x="2" y="10" width="12" height="1.5"/><rect x="2" y="13" width="6" height="1.5"/></svg>',
    tc: '<svg viewBox="0 0 16 16" fill="currentColor"><rect x="2" y="3" width="12" height="1.5"/><rect x="4" y="6.5" width="8" height="1.5"/><rect x="2" y="10" width="12" height="1.5"/><rect x="5" y="13" width="6" height="1.5"/></svg>',
    tr: '<svg viewBox="0 0 16 16" fill="currentColor"><rect x="2" y="3" width="12" height="1.5"/><rect x="6" y="6.5" width="8" height="1.5"/><rect x="2" y="10" width="12" height="1.5"/><rect x="8" y="13" width="6" height="1.5"/></svg>',
    tj: '<svg viewBox="0 0 16 16" fill="currentColor"><rect x="2" y="3" width="12" height="1.5"/><rect x="2" y="6.5" width="12" height="1.5"/><rect x="2" y="10" width="12" height="1.5"/><rect x="2" y="13" width="12" height="1.5"/></svg>',
  };

  /* ---------- layout ---------- */
  document.body.classList.add('fx');
  const pagesInit = $$('.page');
  const root = document.createElement('div'); root.id = 'fx-root';
  root.innerHTML = `
  <div id="fx-top">
    <span class="brand">Sonim · White paper editor</span>
    <button class="fx-btn" id="fx-prev" title="Previous page (PgUp)">‹ Prev</button>
    <span id="fx-pnum" style="min-width:64px;text-align:center"></span>
    <button class="fx-btn" id="fx-next" title="Next page (PgDn)">Next ›</button>
    <span class="fx-sep"></span>
    <button class="fx-btn" id="fx-zout" title="Zoom out (Ctrl -)">−</button><span id="fx-zoom"></span><button class="fx-btn" id="fx-zin" title="Zoom in (Ctrl +)">+</button>
    <button class="fx-btn" id="fx-zfit" title="Fit page (Shift 1)">Fit</button><button class="fx-btn" id="fx-z100" title="Actual size (Shift 0)">100%</button>
    <span class="fx-sep"></span>
    <button class="fx-btn" id="fx-gridbtn" title="Show grid and margins (Ctrl ')">Grid</button>
    <button class="fx-btn on" id="fx-autobtn" title="Auto layout: moving an element vertically pushes the content below it (Shift A)">Auto layout</button>
    <span id="fx-flow" title="Space left before the footer zone">…</span>
    <span class="fx-sep"></span>
    <button class="fx-btn" id="fx-undo" title="Undo (Ctrl Z)">Undo</button><button class="fx-btn" id="fx-redo" title="Redo (Ctrl Shift Z)">Redo</button>
    <span style="flex:1"></span>
    <button class="fx-btn" id="fx-helpbtn">Shortcuts</button>
    <button class="fx-btn" id="fx-save" title="Save edited HTML (Ctrl S)">Save file</button>
    <button class="fx-btn primary" id="fx-pdf" title="Save all pages as PDF (Ctrl P)">Export PDF</button>
  </div>
  <div id="fx-left"><div class="fx-h">Pages</div><div id="fx-pages"></div><div class="fx-h">Layers</div><div id="fx-layers"></div></div>
  <div id="fx-canvas"><div id="fx-wrap"><div id="fx-stage"></div></div></div>
  <div id="fx-right"><div class="fx-h">Design</div><div id="fx-props"></div></div>
  <div id="fx-overlay"></div>
  <div id="fx-toast"></div>
  <div id="fx-help"><div><h3>Shortcuts</h3><table>
    <tr><td>Click</td><td>Select (groups first, like Figma)</td></tr>
    <tr><td>Double-click</td><td>Go one level deeper; on text, edit the text</td></tr>
    <tr><td><kbd>Ctrl</kbd>/<kbd>Cmd</kbd> + click</td><td>Select the deepest element directly</td></tr>
    <tr><td><kbd>Shift</kbd> + click</td><td>Add to / remove from selection</td></tr>
    <tr><td>Drag</td><td>Move (snaps to margins and other elements; <kbd>Shift</kbd> locks axis, <kbd>Alt</kbd> disables snapping)</td></tr>
    <tr><td>Drag a handle</td><td>Resize (<kbd>Shift</kbd> keeps proportions)</td></tr>
    <tr><td><kbd>Arrows</kbd> / <kbd>Shift</kbd>+<kbd>Arrows</kbd></td><td>Nudge 1 pt / 10 pt</td></tr>
    <tr><td><kbd>Esc</kbd> / <kbd>Enter</kbd></td><td>Select parent / first child</td></tr>
    <tr><td><kbd>Tab</kbd></td><td>Next sibling (<kbd>Shift</kbd> for previous)</td></tr>
    <tr><td><kbd>Alt</kbd>+<kbd>A</kbd>/<kbd>D</kbd>/<kbd>H</kbd></td><td>Align left / right / centre</td></tr>
    <tr><td><kbd>Alt</kbd>+<kbd>W</kbd>/<kbd>S</kbd>/<kbd>V</kbd></td><td>Align top / bottom / middle</td></tr>
    <tr><td><kbd>Ctrl</kbd>+<kbd>Z</kbd> / <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>Z</kbd></td><td>Undo / redo</td></tr>
    <tr><td><kbd>Ctrl</kbd>+<kbd>D</kbd> · <kbd>Delete</kbd> · <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>H</kbd></td><td>Duplicate · delete · hide</td></tr>
    <tr><td><kbd>Shift</kbd>+<kbd>A</kbd></td><td>Auto layout on/off. When on, moving or resizing an element vertically pushes everything below it; locked items stay put</td></tr>
    <tr><td><kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>L</kbd></td><td>Lock / unlock selection (or use the lock icon in Layers). Header, footnote, logo and closing band start locked</td></tr>
    <tr><td><kbd>PgUp</kbd>/<kbd>PgDn</kbd></td><td>Previous / next page</td></tr>
    <tr><td><kbd>Ctrl</kbd>+scroll, <kbd>Shift</kbd>+<kbd>1</kbd>, <kbd>Shift</kbd>+<kbd>0</kbd></td><td>Zoom, fit, 100%</td></tr>
    <tr><td><kbd>Ctrl</kbd>+<kbd>'</kbd></td><td>Toggle grid (12 columns, margins)</td></tr>
    <tr><td><kbd>Ctrl</kbd>+<kbd>S</kbd> / <kbd>Ctrl</kbd>+<kbd>P</kbd></td><td>Save file / export PDF (Letter, margins None, Background graphics on)</td></tr>
  </table><p style="margin-top:10px;color:#666">Edits are stored as offsets and styles on the elements, so the document stays live HTML. “Save file” downloads a copy you can reopen here or send back to Claude.</p>
  <button class="fx-btn primary" id="fx-helpclose" style="margin-top:6px">Close</button></div></div>`;
  document.body.appendChild(root);
  const stage = $('#fx-stage'), wrap = $('#fx-wrap'), canvas = $('#fx-canvas'), overlay = $('#fx-overlay');
  pagesInit.forEach(p => stage.appendChild(p));
  const pages = () => $$('.page', stage);

  /* ---------- state ---------- */
  let cur = 0, zoom = 1, sel = [], hover = null, showGrid = false, editing = null, autoLayout = true, flow = null;
  const undoS = [], redoS = [];
  const pageEl = () => pages()[cur];
  const scr = () => ({ w: pageEl().offsetWidth, h: pageEl().offsetHeight });

  function toast(t) { const el = $('#fx-toast'); el.textContent = t; el.style.opacity = 1; clearTimeout(toast.t); toast.t = setTimeout(() => el.style.opacity = 0, 1600); }

  /* ---------- history ---------- */
  function snapshot() { return { i: cur, html: pageEl().outerHTML }; }
  function pushUndo(s) { undoS.push(s || snapshot()); if (undoS.length > 150) undoS.shift(); redoS.length = 0; updBtns(); }
  function restore(s, to) {
    to.push(snapshot()); cur = s.i; const old = pages()[s.i];
    const tmp = document.createElement('div'); tmp.innerHTML = s.html; const nw = tmp.firstElementChild;
    old.replaceWith(nw); sel = []; hover = null; showPage(cur, true);
  }
  function undo() { if (undoS.length) { const s = undoS.pop(); restore(s, redoS); toast('Undo'); } updBtns(); }
  function redo() { if (redoS.length) { const s = redoS.pop(); undoS.push(snapshot()); const r = []; restore(s, r); toast('Redo'); } updBtns(); }
  function updBtns() { $('#fx-undo').disabled = !undoS.length; $('#fx-redo').disabled = !redoS.length; }

  /* ---------- pages & zoom ---------- */
  function showPage(i, keep) {
    const ps = pages(); cur = Math.max(0, Math.min(ps.length - 1, i));
    ps.forEach((p, k) => p.classList.toggle('fx-hidden', k !== cur));
    if (!keep) { sel = []; hover = null; }
    $('#fx-pnum').textContent = `Page ${cur + 1} / ${ps.length}`;
    $('#fx-prev').disabled = cur === 0; $('#fx-next').disabled = cur === ps.length - 1;
    checkFlow(); applyZoom(); buildThumbs(); buildLayers(); buildProps(); draw();
  }
  function applyZoom() {
    const { w, h } = scr(); stage.style.transform = `scale(${zoom})`;
    wrap.style.width = w * zoom + 'px'; wrap.style.height = h * zoom + 'px';
    $('#fx-zoom').textContent = Math.round(zoom * 100) + '%'; draw();
  }
  function fit() { const { w, h } = scr(); zoom = Math.min((canvas.clientWidth - 80) / w, (canvas.clientHeight - 80) / h); applyZoom(); }
  function setZoom(z) { zoom = Math.max(.25, Math.min(4, z)); applyZoom(); }
  function buildThumbs() {
    const box = $('#fx-pages'); box.innerHTML = '';
    pages().forEach((p, i) => {
      const t = document.createElement('div'); t.className = 'fx-thumb' + (i === cur ? ' on' : '');
      const inner = p.cloneNode(true); inner.classList.remove('fx-hidden'); inner.classList.add('inner');
      inner.style.transform = 'scale(' + (95 / 816) + ')';
      t.appendChild(inner); const lb = document.createElement('span'); lb.textContent = i + 1; t.appendChild(lb);
      t.onclick = () => showPage(i); box.appendChild(t);
    });
  }

  /* ---------- naming & selectable rules ---------- */
  const NAMES = [['page', 'Page'], ['display', 'Title'], ['h1', 'Headline'], ['h2', 'Heading'], ['h3', 'Subheading'], ['lead', 'Lead'], ['label', 'Label'],
    ['rc', 'Rugged container'], ['xnotch', 'Expanded notch'], ['notch-anchor', 'Headline block'], ['photo', 'Photo'], ['ico', 'Icon'], ['stat', 'Stat'], ['compare', 'Comparison'],
    ['cell', 'Cell'], ['hd', 'Header cell'], ['arrow', 'Arrow'], ['page-logo', 'Logo'], ['run-head', 'Running header'], ['page-note', 'Footnote'], ['grid', 'Grid'],
    ['stack-row', 'Stack row'], ['callouts', 'Callouts'], ['story', 'Closing band'], ['needs', 'Icon row'], ['usecases', 'Use cases'], ['case', 'Case study'],
    ['partners', 'Partner logos'], ['checks', 'Checklist'], ['bars', 'Results list'], ['quote', 'Quote'], ['quote-by', 'Quote credit'], ['shot', 'Product image'],
    ['num', 'Number'], ['meta', 'Meta'], ['fact', 'Fact'], ['cols-2', 'Two columns'], ['p1-hero', 'Hero photos'], ['acc', 'Accessory images'], ['xref', 'Cross-reference']];
  const TAGS = { p: 'Paragraph', li: 'List item', ul: 'List', ol: 'List', img: 'Image', figure: 'Photo', figcaption: 'Caption', h1: 'Heading', h2: 'Heading', h3: 'Heading', article: 'Article', section: 'Section', svg: 'Vector', b: 'Bold', span: 'Text', div: 'Frame', sup: 'Superscript' };
  function nameOf(el) {
    for (const [c, n] of NAMES) if (el.classList && el.classList.contains(c)) return n;
    return TAGS[el.tagName.toLowerCase()] || el.tagName.toLowerCase();
  }
  function snippet(el) { const t = (el.innerText || el.textContent || '').replace(/\s+/g, ' ').trim(); return t.length > 26 ? t.slice(0, 26) + '…' : t; }
  const SKIP_TAGS = new Set(['path', 'rect', 'circle', 'g', 'defs', 'clipPath', 'polygon', 'line', 'br', 'style', 'script']);
  function isNode(el) { return el && el.nodeType === 1 && !SKIP_TAGS.has(el.tagName) && !(el.closest('svg') && el.tagName !== 'svg'); }
  function kids(el) { return [...el.children].filter(isNode); }
  const inPage = el => el && pageEl() && pageEl().contains(el) && el !== pageEl();
  function chainTo(el) { const c = []; while (el && el !== pageEl()) { c.unshift(el); el = el.parentElement; } return c; }  // top-level first
  function normalize(el) { while (el && el.parentElement && (el.closest('svg') && el.tagName !== 'svg')) el = el.parentElement; return el; }
  function pick(target, deep) {
    let el = normalize(target); if (!inPage(el)) return null;
    if (deep) { while (el && ['B', 'STRONG', 'SUP', 'EM', 'I', 'BR'].includes(el.tagName)) el = el.parentElement; return inPage(el) && !isLocked(el) ? el : null; }
    const chain = chainTo(el); if (!chain.length) return null;
    const s = sel[0];
    // Figma logic: start at top-level; if something is selected, go to its sibling level
    let res = chain[0];
    if (s && chain.includes(s)) res = s;
    else if (s) { for (let i = 0; i < chain.length; i++) if (chain[i].parentElement === s.parentElement) { res = chain[i]; break; } }
    return isLocked(res) ? null : res;
  }

  /* ---------- geometry ---------- */
  const R = el => el.getBoundingClientRect();
  function pageRect() { return R(pageEl()); }
  function toPt(px) { return px / zoom * PT; }
  function ptRect(el) { const r = R(el), p = pageRect(); return { l: toPt(r.left - p.left), t: toPt(r.top - p.top), w: toPt(r.width), h: toPt(r.height) }; }
  function getT(el) { const m = (el.style.translate || '').match(/-?[\d.]+/g); return { x: m ? +m[0] : 0, y: m && m[1] ? +m[1] : 0 }; }
  function setT(el, x, y) { x = round(x); y = round(y); el.style.translate = (x || y) ? `${x}pt ${y}pt` : ''; if (getComputedStyle(el).display === 'inline') el.style.display = 'inline-block'; }
  function union(els) {
    const rs = els.map(ptRect); const l = Math.min(...rs.map(r => r.l)), t = Math.min(...rs.map(r => r.t));
    const r = Math.max(...rs.map(r => r.l + r.w)), b = Math.max(...rs.map(r => r.t + r.h)); return { l, t, w: r - l, h: b - t };
  }

  /* ---------- auto layout & locking ---------- */
  const DEFAULT_LOCK = '.run-head,.page-logo,.page-note,.story';
  function initLocks() { $$('.page', stage).forEach(p => $$(DEFAULT_LOCK, p).forEach(el => { if (!el.hasAttribute('data-fx-lock')) el.setAttribute('data-fx-lock', '1'); })); }
  function lockOwner(el) { const l = el && el.closest ? el.closest('[data-fx-lock="1"]') : null; return l && pageEl() && pageEl().contains(l) ? l : null; }
  function isLocked(el) { return !!lockOwner(el); }
  function inFlow(el) { const cs = getComputedStyle(el); return cs.position !== 'absolute' && cs.position !== 'fixed' && cs.display !== 'none'; }
  const pv = v => (parseFloat(v) || 0) * PT;
  function prevFlow(el) { let p = el.previousElementSibling; while (p && (!isNode(p) || !inFlow(p))) p = p.previousElementSibling; return p; }
  function foldMargin(el) {           // turn collapsed margins into one explicit margin-top so moves are predictable
    const par = el.parentElement; if (!par) return; const pd = getComputedStyle(par).display;
    if (getComputedStyle(el).display === 'inline') el.style.display = 'inline-block';
    const prev = prevFlow(el); if (!prev || /grid|flex/.test(pd)) return;
    const pmb = pv(getComputedStyle(prev).marginBottom), mt = pv(getComputedStyle(el).marginTop);
    if (pmb > 0 && mt >= 0) { el.style.marginTop = round(Math.max(pmb, mt)) + 'pt'; prev.style.marginBottom = '0pt'; }
  }
  const usesFlow = el => autoLayout && inFlow(el);
  function lockedAnchors() {
    return $$('[data-fx-lock="1"]', pageEl()).filter(el => inFlow(el) && !sel.some(s => s.contains(el) || el.contains(s))).map(el => ({ el, y: ptRect(el).t }));
  }
  function restoreAnchors(an) { an.forEach(a => { const d = ptRect(a.el).t - a.y; if (Math.abs(d) > 0.05) { foldMargin(a.el); a.el.style.marginTop = round(pv(getComputedStyle(a.el).marginTop) - d) + 'pt'; } }); }
  function withAnchors(fn) { const an = autoLayout ? lockedAnchors() : []; fn(); restoreAnchors(an); }
  function moveY(el, dy) {
    if (!dy) return;
    if (usesFlow(el)) { foldMargin(el); el.style.marginTop = round(pv(getComputedStyle(el).marginTop) + dy) + 'pt'; }
    else { const t = getT(el); setT(el, t.x, t.y + dy); }
  }
  function moveX(el, dx) { if (!dx) return; const t = getT(el); setT(el, t.x + dx, t.y); }
  function checkFlow() {
    const p = pageEl(); if (!p) return; const H = p.offsetHeight * PT; let limit = H - 58, lim = 'footer zone';
    kids(p).forEach(k => { const cs = getComputedStyle(k); if (cs.position === 'absolute' && cs.display !== 'none' && !k.classList.contains('page-logo') && !k.classList.contains('page-note') && !k.classList.contains('run-head')) { const r = ptRect(k); if (r.t > H * .55 && r.t - 8 < limit) { limit = r.t - 8; lim = nameOf(k).toLowerCase(); } } });
    let bottom = 0;
    $$('*', p).forEach(el => {
      if (!isNode(el) || el.closest('svg') && el.tagName !== 'svg') return;
      let a = el, abs = false; while (a && a !== p) { const ps = getComputedStyle(a).position; if (ps === 'absolute' || ps === 'fixed') { abs = true; break; } a = a.parentElement; }
      if (abs) return; const cs = getComputedStyle(el); if (cs.display === 'none' || cs.visibility === 'hidden') return;
      const r = ptRect(el); if (r.h > 0 && r.w > 0) bottom = Math.max(bottom, r.t + r.h);
    });
    flow = { limit, bottom, over: bottom - limit, lim };
    const b = $('#fx-flow'); if (!b) return;
    if (flow.over > 0.5) { b.className = 'over'; b.textContent = `Overflow ${round(flow.over)} pt`; b.title = `Content runs ${round(flow.over)} pt into the ${lim}`; }
    else { b.className = ''; b.textContent = `${Math.max(0, Math.round(-flow.over))} pt free`; b.title = `Space left before the ${lim}`; }
  }

  /* ---------- overlay drawing ---------- */
  function box(r, cls) { const d = document.createElement('div'); d.className = 'fx-box ' + (cls || ''); Object.assign(d.style, { left: r.left + 'px', top: r.top + 'px', width: r.width + 'px', height: r.height + 'px' }); overlay.appendChild(d); return d; }
  function draw(guides) {
    overlay.innerHTML = ''; if (!pageEl()) return; const p = pageRect();
    if (showGrid) {
      const s = zoom / PT, m = 45 * s, gut = 14 * s, cw = (p.width - 2 * m - 11 * gut) / 12;
      const mg = document.createElement('div'); mg.className = 'fx-marg';
      Object.assign(mg.style, { left: p.left + m + 'px', top: p.top + 50 * s + 'px', width: p.width - 2 * m + 'px', height: p.height - 108 * s + 'px' }); overlay.appendChild(mg);
      for (let i = 0; i < 12; i++) { const c = document.createElement('div'); c.className = 'fx-grid'; Object.assign(c.style, { left: p.left + m + i * (cw + gut) + 'px', top: p.top + 'px', width: cw + 'px', height: p.height + 'px' }); overlay.appendChild(c); }
    }
    if (flow && flow.over > 0.5) { const s = zoom / PT; const o = document.createElement('div'); o.className = 'fx-over';
      Object.assign(o.style, { left: p.left + 'px', width: p.width + 'px', top: p.top + flow.limit * s + 'px', height: flow.over * s + 'px' }); overlay.appendChild(o); 
      const t = document.createElement('div'); t.className = 'fx-tag'; t.textContent = `Overflow ${round(flow.over)} pt into the ${flow.lim}`;
      Object.assign(t.style, { left: p.left + 8 + 'px', top: p.top + flow.limit * s - 18 + 'px', background: '#111' }); overlay.appendChild(t); }
    if (flow && (showGrid || (flow.over > -12))) { const s = zoom / PT; const l = document.createElement('div'); l.className = 'fx-limit';
      Object.assign(l.style, { left: p.left + 'px', width: p.width + 'px', top: p.top + flow.limit * s + 'px' }); overlay.appendChild(l); }
    if (hover && !sel.includes(hover) && inPage(hover)) box(R(hover), 'hover');
    sel.filter(inPage).forEach(el => box(R(el), sel.length > 1 ? 'group' : ''));
    if (sel.length) {
      const us = sel.filter(inPage).map(R); if (!us.length) return;
      const u = { left: Math.min(...us.map(r => r.left)), top: Math.min(...us.map(r => r.top)), right: Math.max(...us.map(r => r.right)), bottom: Math.max(...us.map(r => r.bottom)) };
      u.width = u.right - u.left; u.height = u.bottom - u.top;
      if (sel.length > 1) box(u, '');
      const tag = document.createElement('div'); tag.className = 'fx-tag';
      const ur = union(sel.filter(inPage)); tag.textContent = `${round(ur.w)} × ${round(ur.h)} pt`;
      Object.assign(tag.style, { left: u.left + 'px', top: u.bottom + 6 + 'px' }); overlay.appendChild(tag);
      if (!editing) [['nw', 0, 0], ['n', .5, 0], ['ne', 1, 0], ['e', 1, .5], ['se', 1, 1], ['s', .5, 1], ['sw', 0, 1], ['w', 0, .5]].forEach(([k, fx, fy]) => {
        const h = document.createElement('div'); h.className = 'fx-h8'; h.dataset.h = k;
        Object.assign(h.style, { left: u.left + u.width * fx - 4 + 'px', top: u.top + u.height * fy - 4 + 'px', cursor: k + '-resize' });
        h.addEventListener('mousedown', startResize); overlay.appendChild(h);
      });
    }
    (guides || []).forEach(g => { const d = document.createElement('div'); d.className = 'fx-guide'; const s = zoom / PT;
      if (g.x != null) Object.assign(d.style, { left: p.left + g.x * s + 'px', top: p.top + 'px', width: '1px', height: p.height + 'px' });
      else Object.assign(d.style, { top: p.top + g.y * s + 'px', left: p.left + 'px', height: '1px', width: p.width + 'px' });
      overlay.appendChild(d); });
  }
  canvas.addEventListener('scroll', () => draw());
  window.addEventListener('resize', () => draw());

  /* ---------- selection ---------- */
  function select(list, add) {
    list = list.filter(Boolean);
    if (add) { list.forEach(el => { const i = sel.indexOf(el); if (i >= 0) sel.splice(i, 1); else sel.push(el); }); }
    else sel = list;
    buildLayers(); buildProps(); draw();
  }

  /* ---------- snapping ---------- */
  function candidates(excl) {
    const xs = [0, 45, 306, 567, 612], ys = [0, 50, 396, 734, 792];
    $$('*', pageEl()).forEach(el => {
      if (!isNode(el) || excl.some(s => s === el || s.contains(el) || el.contains(s))) return;
      if (el.classList.contains('fx-hidden') || el.closest('.fx-hidden')) return;
      const cs = getComputedStyle(el); if (cs.display === 'none' || cs.display === 'inline') return;
      const r = ptRect(el); if (r.w < 2 || r.h < 2) return;
      xs.push(r.l, r.l + r.w / 2, r.l + r.w); ys.push(r.t, r.t + r.h / 2, r.t + r.h);
    });
    return { xs, ys };
  }
  function snap(b, c, off) {
    const th = toPt(6); let dx = 0, dy = 0, gx = null, gy = null, best = th;
    [b.l, b.l + b.w / 2, b.l + b.w].forEach(v => c.xs.forEach(x => { const d = x - v; if (Math.abs(d) < best) { best = Math.abs(d); dx = d; gx = x; } }));
    best = th;
    [b.t, b.t + b.h / 2, b.t + b.h].forEach(v => c.ys.forEach(y => { const d = y - v; if (Math.abs(d) < best) { best = Math.abs(d); dy = d; gy = y; } }));
    const g = []; if (gx != null && !off) g.push({ x: gx }); if (gy != null && !off) g.push({ y: gy });
    return off ? { dx: 0, dy: 0, g: [] } : { dx, dy, g };
  }

  /* ---------- mouse: select / drag ---------- */
  let drag = null;
  stage.addEventListener('mousemove', e => { if (drag || editing) return; const h = pick(e.target, e.ctrlKey || e.metaKey); if (h !== hover) { hover = h; draw(); } });
  stage.addEventListener('mouseleave', () => { hover = null; draw(); });
  stage.addEventListener('mousedown', e => {
    if (e.button !== 0) return;
    if (editing && editing.contains(e.target)) return;
    if (editing) endEdit();
    const el = pick(e.target, e.ctrlKey || e.metaKey);
    if (!el) { select([]); return; }
    e.preventDefault();
    if (e.shiftKey) { select([el], true); return; }
    if (!sel.includes(el)) select([el]);
    const movable = sel.filter(s => !isLocked(s)); if (!movable.length) return;
    const undo0 = snapshot(), an = autoLayout ? lockedAnchors() : [];
    const items = movable.map(s => { const fl = usesFlow(s); if (fl) foldMargin(s); return { el: s, t: getT(s), fl, mt: pv(getComputedStyle(s).marginTop) }; });
    drag = { start: { x: e.clientX, y: e.clientY }, items, b0: union(movable), moved: false, undo: undo0, an };
  });
  window.addEventListener('mousemove', e => {
    if (!drag || drag.rs) return;
    let dxp = e.clientX - drag.start.x, dyp = e.clientY - drag.start.y;
    if (!drag.moved && Math.hypot(dxp, dyp) < 3) return;
    if (!drag.moved) { drag.moved = true; drag.cand = candidates(sel); }
    if (e.shiftKey) { if (Math.abs(dxp) > Math.abs(dyp)) dyp = 0; else dxp = 0; }
    let dx = toPt(dxp), dy = toPt(dyp);
    const b = { l: drag.b0.l + dx, t: drag.b0.t + dy, w: drag.b0.w, h: drag.b0.h };
    const s = snap(b, drag.cand, e.altKey); dx += s.dx; dy += s.dy;
    drag.items.forEach(it => { if (it.fl) { setT(it.el, it.t.x + dx, it.t.y); it.el.style.marginTop = round(it.mt + dy) + 'pt'; } else setT(it.el, it.t.x + dx, it.t.y + dy); });
    restoreAnchors(drag.an); checkFlow(); draw(s.g); buildProps(true);
  });
  window.addEventListener('mouseup', () => {
    if (!drag || drag.rs) return;
    if (drag.moved) { pushUndo(drag.undo); buildThumbs(); }
    drag = null; checkFlow(); draw();
  });

  /* resize */
  function startResize(e) {
    e.preventDefault(); e.stopPropagation(); if (!sel.length) return;
    const k = e.target.dataset.h, el = sel[0]; if (isLocked(el)) { toast('Locked · unlock to resize'); return; }
    const undo0 = snapshot(), an = autoLayout ? lockedAnchors() : [], fl = usesFlow(el); if (fl) foldMargin(el);
    const r0 = ptRect(el), t0 = getT(el), mt0 = pv(getComputedStyle(el).marginTop);
    drag = { rs: true, moved: false, start: { x: e.clientX, y: e.clientY }, k, el, r0, t0, undo: undo0, ar: r0.w / r0.h };
    const mv = ev => {
      let dx = toPt(ev.clientX - drag.start.x), dy = toPt(ev.clientY - drag.start.y); drag.moved = true;
      let w = r0.w, h = r0.h, tx = t0.x, ty = t0.y;
      if (k.includes('e')) w = r0.w + dx; if (k.includes('w')) { w = r0.w - dx; tx = t0.x + dx; }
      if (k.includes('s')) h = r0.h + dy; if (k.includes('n')) { h = r0.h - dy; ty = t0.y + dy; }
      if (ev.shiftKey && k.length === 2) { h = w / drag.ar; if (k.includes('n')) ty = t0.y + (r0.h - h); }
      w = Math.max(4, w); h = Math.max(4, h);
      if (k !== 'n' && k !== 's') el.style.width = round(w) + 'pt';
      if (k !== 'e' && k !== 'w') el.style.height = round(h) + 'pt';
      if (getComputedStyle(el).display === 'inline') el.style.display = 'inline-block';
      if (fl) { setT(el, tx, t0.y); el.style.marginTop = round(mt0 + (ty - t0.y)) + 'pt'; } else setT(el, tx, ty);
      restoreAnchors(an); checkFlow(); draw(); buildProps(true);
    };
    const up = () => { window.removeEventListener('mousemove', mv); window.removeEventListener('mouseup', up); if (drag && drag.moved) { pushUndo(drag.undo); buildThumbs(); } drag = null; draw(); };
    window.addEventListener('mousemove', mv); window.addEventListener('mouseup', up);
  }

  /* double click: drill in / edit text */
  stage.addEventListener('dblclick', e => {
    const s = sel[0]; const deep = normalize(e.target);
    if (s && s.contains(deep) && s !== deep) { const chain = chainTo(deep); const i = chain.indexOf(s); select([chain[i + 1] || deep]); return; }
    const t = s || deep; if (!t || !inPage(t)) return;
    if (hasText(t)) startEdit(t, e);
  });
  function hasText(el) { return [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()) || (!kids(el).some(k => /^(DIV|UL|OL|FIGURE|ARTICLE|SECTION|IMG)$/.test(k.tagName)) && (el.innerText || '').trim()); }
  function startEdit(el, e) {
    editing = el; el.dataset.fxUndo = '1'; editing._undo = snapshot(); el.setAttribute('contenteditable', 'true'); document.body.classList.add('fx-editing');
    el.focus(); if (e && document.caretRangeFromPoint) { const r = document.caretRangeFromPoint(e.clientX, e.clientY); if (r) { const s = getSelection(); s.removeAllRanges(); s.addRange(r); } }
    draw(); toast('Editing text · Esc to finish');
  }
  function endEdit() {
    if (!editing) return; const el = editing; editing = null; el.removeAttribute('contenteditable'); delete el.dataset.fxUndo; document.body.classList.remove('fx-editing');
    const u = el._undo; if (u && u.html !== snapshot().html) { pushUndo(u); buildThumbs(); }
    buildLayers(); draw();
  }

  /* ---------- actions ---------- */
  function act(fn, label) { if (!sel.length) return; const u = snapshot(); withAnchors(fn); checkFlow(); if (u.html !== snapshot().html) { pushUndo(u); buildThumbs(); if (label) toast(label); } buildLayers(); buildProps(); draw(); }
  const movableSel = () => { const m = sel.filter(el => !isLocked(el)); if (m.length < sel.length) toast('Locked layers were skipped'); return m; };
  function nudge(dx, dy) { act(() => movableSel().forEach(el => { moveX(el, dx); moveY(el, dy); })); }
  function align(mode) {
    act(() => {
      let ref;
      if (sel.length === 1) {
        const el = sel[0], par = el.parentElement;
        if (par === pageEl()) ref = { l: 45, t: 50, w: 522, h: 684 };
        else { const r = ptRect(par), cs = getComputedStyle(par), pl = parseFloat(cs.paddingLeft) * PT, pr = parseFloat(cs.paddingRight) * PT, ptp = parseFloat(cs.paddingTop) * PT, pb = parseFloat(cs.paddingBottom) * PT;
          ref = { l: r.l + pl, t: r.t + ptp, w: r.w - pl - pr, h: r.h - ptp - pb }; }
      } else ref = union(sel);
      movableSel().forEach(el => {
        const r = ptRect(el); let dx = 0, dy = 0;
        if (mode === 'l') dx = ref.l - r.l; if (mode === 'r') dx = ref.l + ref.w - (r.l + r.w); if (mode === 'c') dx = ref.l + ref.w / 2 - (r.l + r.w / 2);
        if (mode === 't') dy = ref.t - r.t; if (mode === 'b') dy = ref.t + ref.h - (r.t + r.h); if (mode === 'm') dy = ref.t + ref.h / 2 - (r.t + r.h / 2);
        moveX(el, dx); moveY(el, dy);
      });
    }, 'Aligned');
  }
  function distribute(axis) {
    if (sel.length < 3) { toast('Select 3 or more to distribute'); return; }
    act(() => {
      const it = sel.map(el => ({ el, r: ptRect(el), t: getT(el) })).sort((a, b) => axis === 'h' ? a.r.l - b.r.l : a.r.t - b.r.t);
      const first = it[0].r, last = it[it.length - 1].r;
      const total = axis === 'h' ? (last.l + last.w - first.l) : (last.t + last.h - first.t);
      const sizes = it.reduce((s, x) => s + (axis === 'h' ? x.r.w : x.r.h), 0); const gap = (total - sizes) / (it.length - 1);
      let pos = axis === 'h' ? first.l : first.t;
      it.forEach(x => { if (isLocked(x.el)) { pos += (axis === 'h' ? x.r.w : x.r.h) + gap; return; }
        const now = ptRect(x.el), cur = axis === 'h' ? now.l : now.t; const d = pos - cur;   // re-measure: auto layout may have pushed it
        if (axis === 'h') moveX(x.el, d); else moveY(x.el, d); pos += (axis === 'h' ? x.r.w : x.r.h) + gap; });
    }, 'Distributed');
  }
  function textAlign(v) {
    act(() => sel.forEach(el => {
      el.style.textAlign = v;
      kids(el).forEach(k => { const cs = getComputedStyle(k); if (cs.display === 'block' && k.getBoundingClientRect().width < el.getBoundingClientRect().width - 2) {
        k.style.marginLeft = v === 'center' || v === 'right' ? 'auto' : ''; k.style.marginRight = v === 'center' ? 'auto' : ''; } });
    }), 'Text aligned ' + v);
  }
  function setStyle(prop, val, label) { act(() => sel.forEach(el => { el.style[prop] = val; if (prop === 'color') $$('*', el).forEach(c => { if (c.style.color) c.style.color = ''; }); }), label); }
  function duplicate() { act(() => { sel = sel.map(el => { const c = el.cloneNode(true); c.removeAttribute('data-fx-lock'); el.after(c); if (!usesFlow(c)) { const t = getT(c); setT(c, t.x + 10, t.y + 10); } return c; }); }, 'Duplicated'); }
  function remove() { const m = sel.filter(el => !isLocked(el)); if (!m.length) { toast('Locked · unlock to delete'); return; } act(() => { m.forEach(el => el.remove()); sel = []; }, 'Deleted'); }
  function toggleLock(els) {
    els = els || sel; if (!els.length) return; const u = snapshot(); const lockIt = !els.every(el => el.getAttribute('data-fx-lock') === '1');
    els.forEach(el => el.setAttribute('data-fx-lock', lockIt ? '1' : '0')); pushUndo(u); toast(lockIt ? 'Locked' : 'Unlocked'); buildLayers(); buildProps(); draw();
  }
  function toggleHide(els) { const u = snapshot(); (els || sel).forEach(el => el.style.display = el.style.display === 'none' ? '' : 'none'); pushUndo(u); buildLayers(); buildProps(); draw(); buildThumbs(); }
  function resetStyles() { act(() => sel.forEach(el => { ['translate', 'width', 'height', 'fontSize', 'lineHeight', 'letterSpacing', 'fontWeight', 'textAlign', 'color', 'backgroundColor', 'opacity', 'marginTop', 'marginBottom', 'padding'].forEach(p => el.style[p] = ''); }), 'Reset'); }

  /* ---------- layers ---------- */
  const LOCK = '<svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.3"><rect x="2" y="5.5" width="8" height="5.5" rx="1" fill="currentColor" stroke="none"/><path d="M3.8 5.5V4a2.2 2.2 0 0 1 4.4 0v1.5"/></svg>', OPEN = '<svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.3"><rect x="2" y="5.5" width="8" height="5.5" rx="1"/><path d="M3.8 5.5V4a2.2 2.2 0 0 1 4.3-.6"/></svg>';
  const open = new WeakSet();
  function buildLayers() {
    const box = $('#fx-layers'); if (!box) return; box.innerHTML = ''; if (!pageEl()) return;
    sel.forEach(s => chainTo(s).forEach(a => open.add(a)));
    const walk = (el, d) => kids(el).forEach(k => {
      const ch = kids(k).length, row = document.createElement('div'); const own = k.getAttribute('data-fx-lock') === '1', inh = !own && isLocked(k);
      row.className = 'fx-row' + (sel.includes(k) ? ' on' : '') + (k.style.display === 'none' ? ' hid' : '') + (own || inh ? ' locked' : '');
      row.style.paddingLeft = 6 + d * 12 + 'px';
      const sn = snippet(k); row.innerHTML = `<span class="tw">${ch ? (open.has(k) ? '▾' : '▸') : ''}</span><span class="nm">${nameOf(k)}${sn && ch < 3 ? ' <i>' + sn.replace(/</g, '&lt;') + '</i>' : ''}</span><span class="lk ${own ? 'on' : inh ? 'inh' : ''}" title="${own ? 'Unlock' : inh ? 'Locked by parent' : 'Lock'}">${own || inh ? LOCK : OPEN}</span><span class="eye" title="Hide / show">${k.style.display === 'none' ? '◌' : '◉'}</span>`;
      row.querySelector('.tw').onclick = ev => { ev.stopPropagation(); open.has(k) ? open.delete(k) : open.add(k); buildLayers(); };
      row.querySelector('.eye').onclick = ev => { ev.stopPropagation(); toggleHide([k]); };
      row.querySelector('.lk').onclick = ev => { ev.stopPropagation(); if (inh) { toast('Locked by a parent layer'); return; } toggleLock([k]); };
      row.onclick = ev => select([k], ev.shiftKey);
      row.onmouseenter = () => { hover = k; draw(); }; row.onmouseleave = () => { hover = null; draw(); };
      box.appendChild(row); if (ch && open.has(k)) walk(k, d + 1);
    });
    walk(pageEl(), 0);
    const on = box.querySelector('.fx-row.on'); if (on) on.scrollIntoView({ block: 'nearest' });
  }

  /* ---------- properties ---------- */
  function hex(c) { const m = c.match(/\d+(\.\d+)?/g); if (!m) return ''; if (m.length === 4 && +m[3] === 0) return 'transparent'; return '#' + m.slice(0, 3).map(v => (+v).toString(16).padStart(2, '0')).join('').toUpperCase(); }
  function field(lbl, val, on, step) { return `<label title="${lbl}"><span>${lbl}</span><input type="number" step="${step || 0.5}" value="${val}" data-k="${on}"></label>`; }
  function flowKids(el) { return kids(el).filter(k => inFlow(k)); }
  function gapFields(el) {
    if (sel.length !== 1) return ''; const fk = flowKids(el); if (fk.length < 2) return '';
    const cs = getComputedStyle(el), gridish = /grid|flex/.test(cs.display);
    let gy, gx = null;
    if (gridish) { gy = cs.rowGap === 'normal' ? 0 : round(pv(cs.rowGap)); gx = cs.columnGap === 'normal' ? 0 : round(pv(cs.columnGap)); }
    else { const a = ptRect(fk[0]), b = ptRect(fk[1]); gy = round(b.t - (a.t + a.h)); }
    return `<div class="fx-grp"><b>Auto layout · spacing between children (pt)</b><div class="fx-f">${field('↕', gy, 'gy')}${gx !== null ? field('↔', gx, 'gx') : ''}</div>
      <div style="color:#888;font-size:10.5px;margin-top:5px">${gridish ? 'Row and column gap of this ' + (cs.display.includes('grid') ? 'grid' : 'row') + '.' : 'Sets equal spacing between the ' + fk.length + ' stacked children.'}</div></div>`;
  }
  function setGap(el, k, v) {
    const cs = getComputedStyle(el), fk = flowKids(el).filter(c => !isLocked(c));
    if (/grid|flex/.test(cs.display)) { if (k === 'gy') el.style.rowGap = v + 'pt'; else el.style.columnGap = v + 'pt'; return; }
    fk.forEach((c, i) => { if (i < fk.length - 1) c.style.marginBottom = '0pt'; if (i > 0) c.style.marginTop = v + 'pt'; });
  }
  function buildProps(liveOnly) {
    const P = $('#fx-props');
    if (!sel.length) { if (!liveOnly) P.innerHTML = `<div class="fx-empty">Click something on the page to select it.<br><br>Double-click to go deeper or edit text. Shift-click to select several, then align or distribute them.</div>`; return; }
    const el = sel[0], cs = getComputedStyle(el), r = sel.length > 1 ? union(sel) : ptRect(el);
    if (liveOnly) { $$('input[data-k]', P).forEach(i => { const k = i.dataset.k; if (k === 'x') i.value = round(r.l); if (k === 'y') i.value = round(r.t); if (k === 'w') i.value = round(r.w); if (k === 'h') i.value = round(r.h); }); return; }
    const fs = round(parseFloat(cs.fontSize) * PT), lh = cs.lineHeight === 'normal' ? '' : round(parseFloat(cs.lineHeight) * PT);
    const ls = cs.letterSpacing === 'normal' ? 0 : Math.round(parseFloat(cs.letterSpacing) / parseFloat(cs.fontSize) * 1000);
    const col = hex(cs.color), bg = hex(cs.backgroundColor), ta = cs.textAlign === 'start' ? 'left' : cs.textAlign;
    const sw = (k, curv, none) => `<div class="fx-sw">${none ? `<button class="none ${curv === 'transparent' ? 'on' : ''}" data-${k}="transparent" title="None"></button>` : ''}${BRAND.map(([n, h]) => `<button style="background:${h}" class="${curv === h ? 'on' : ''}" data-${k}="${h}" title="${n}"></button>`).join('')}<span style="color:#999;font-size:11px">${curv === 'transparent' ? 'None' : (BRAND.find(b => b[1] === curv) || ['Off-brand ' + curv])[0]}</span></div>`;
    const warns = [];
    if (fs < 6.5) warns.push(`Text is ${fs} pt. Brand minimum for print is 6.5 pt.`);
    const txt = (el.innerText || '').replace(/\b(RAM|OTTO|AINA|EMS|LMR|GPS|PTT|SOS|GMR|HPUE|MCPTT|AT&T|IP68|MIL-STD-810H|XP5plus|5G|FirstNet)\b/g, '').trim();
    if (cs.textTransform === 'uppercase' || (txt.length > 6 && txt === txt.toUpperCase() && /[A-Z]{5,}/.test(txt))) warns.push('All caps detected. Brand typography is sentence case.');
    if (col && !BRAND.some(b => b[1] === col) && !/^#(0|F){6}$/i.test(col) && cs.color.indexOf('0.68') < 0) warns.push(`Text colour ${col} is not a brand colour.`);
    if (bg !== 'transparent' && bg && !BRAND.some(b => b[1] === bg)) warns.push(`Fill ${bg} is not a brand colour.`);
    if (ta === 'center' || ta === 'right' || ta === 'justify') warns.push('Brand guidelines prefer flush-left type in most cases.');
    const fam = cs.fontFamily.split(',')[0].replace(/"/g, '');
    P.innerHTML = `
      <div class="fx-grp"><b>${sel.length > 1 ? sel.length + ' layers' : nameOf(el)}</b><div style="color:#999;margin-top:-2px">${sel.length > 1 ? 'Mixed selection' : (snippet(el) || '&nbsp;')}</div>
        ${isLocked(el) ? `<div class="fx-lockmsg"><span>${lockOwner(el) === el ? 'Locked. It stays in place when auto layout pushes content.' : 'Inside a locked layer.'}</span>${lockOwner(el) === el ? '<button data-a="lock">Unlock</button>' : ''}</div>` : ''}</div>
      ${gapFields(el)}
      <div class="fx-grp"><b>Alignment</b><div class="fx-icons">
        <button data-al="l" title="Align left (Alt A)">${I.al}</button><button data-al="c" title="Align horizontal centres (Alt H)">${I.ac}</button><button data-al="r" title="Align right (Alt D)">${I.ar}</button>
        <button data-al="t" title="Align top (Alt W)">${I.at}</button><button data-al="m" title="Align vertical centres (Alt V)">${I.am}</button><button data-al="b" title="Align bottom (Alt S)">${I.ab}</button>
        <button data-ds="h" title="Distribute horizontal spacing">${I.dh}</button><button data-ds="v" title="Distribute vertical spacing">${I.dv}</button></div>
        <div style="color:#888;font-size:10.5px;margin-top:5px">${sel.length > 1 ? 'Aligns the selected layers to each other.' : 'Aligns the layer inside its parent frame.'}</div></div>
      <div class="fx-grp"><b>Position &amp; size (pt)</b><div class="fx-f">
        ${field('X', round(r.l), 'x')}${field('Y', round(r.t), 'y')}${field('W', round(r.w), 'w')}${field('H', round(r.h), 'h')}</div></div>
      <div class="fx-grp"><b>Text</b>
        <div style="color:#999;font-size:11px;margin-bottom:6px">${/Akzidenz/i.test(cs.fontFamily) ? 'Akzidenz Grotesk (uses Arial if not installed)' : fam}</div>
        <div class="fx-f" style="margin-bottom:6px">
          <label title="Weight"><span>Wt</span><select data-k="fw"><option value="400" ${+cs.fontWeight < 600 ? 'selected' : ''}>Regular</option><option value="700" ${+cs.fontWeight >= 600 ? 'selected' : ''}>Bold</option></select></label>
          ${field('Sz', fs, 'fs')}${field('Lh', lh, 'lh')}${field('Tr', ls, 'ls', 5)}</div>
        <div class="fx-icons" style="margin-bottom:8px">
          <button data-ta="left" class="${ta === 'left' ? 'on' : ''}" title="Align text left">${I.tl}</button><button data-ta="center" class="${ta === 'center' ? 'on' : ''}" title="Align text centre">${I.tc}</button>
          <button data-ta="right" class="${ta === 'right' ? 'on' : ''}" title="Align text right">${I.tr}</button><button data-ta="justify" class="${ta === 'justify' ? 'on' : ''}" title="Justify">${I.tj}</button></div>
        ${sw('col', col)}</div>
      <div class="fx-grp"><b>Fill</b>${sw('bg', bg, true)}</div>
      <div class="fx-grp"><b>Spacing (pt)</b><div class="fx-f">
        ${field('↑', round(parseFloat(cs.marginTop) * PT), 'mt')}${field('↓', round(parseFloat(cs.marginBottom) * PT), 'mb')}
        ${field('▣', round(parseFloat(cs.paddingTop) * PT), 'pd')}${field('%', Math.round(parseFloat(cs.opacity) * 100), 'op', 5)}</div>
        <div style="color:#888;font-size:10.5px;margin-top:5px">↑ ↓ margin above / below · ▣ padding · % opacity</div></div>
      <div class="fx-grp"><b>Layer</b><div class="fx-acts">
        <button data-a="parent">Select parent</button><button data-a="child">Select child</button>
        <button data-a="dup">Duplicate</button><button data-a="hide">${el.style.display === 'none' ? 'Show' : 'Hide'}</button>
        <button data-a="reset">Reset edits</button><button data-a="del">Delete</button>
        <button data-a="lock" style="grid-column:1/3">${isLocked(el) && lockOwner(el) === el ? 'Unlock' : 'Lock position'}</button></div>
        ${warns.length ? warns.map(w => `<div class="fx-warn">${w}</div>`).join('') : '<div class="fx-ok">✓ On brand: Arial / Akzidenz, brand colours, sentence case</div>'}</div>`;
    $$('[data-al]', P).forEach(b => b.onclick = () => align(b.dataset.al));
    $$('[data-ds]', P).forEach(b => b.onclick = () => distribute(b.dataset.ds));
    $$('[data-ta]', P).forEach(b => b.onclick = () => textAlign(b.dataset.ta));
    $$('[data-col]', P).forEach(b => b.onclick = () => setStyle('color', b.dataset.col, 'Colour set'));
    $$('[data-bg]', P).forEach(b => b.onclick = () => setStyle('backgroundColor', b.dataset.bg === 'transparent' ? 'transparent' : b.dataset.bg, 'Fill set'));
    $$('[data-a]', P).forEach(b => b.onclick = () => ({ parent: selParent, child: selChild, dup: duplicate, hide: () => toggleHide(), reset: resetStyles, del: remove, lock: () => toggleLock() })[b.dataset.a]());
    $$('input[data-k],select[data-k]', P).forEach(inp => {
      let u = null;
      inp.addEventListener('focus', () => u = snapshot());
      const apply = () => {
        const v = parseFloat(inp.value), k = inp.dataset.k; if (isNaN(v) && k !== 'fw') return;
        if (k === 'gy' || k === 'gx') { withAnchors(() => setGap(sel[0], k, v)); checkFlow(); draw(); return; }
        withAnchors(() => sel.forEach(el => {
          const pr = ptRect(el);
          if ((k === 'x' || k === 'y' || k === 'w' || k === 'h') && isLocked(el)) return;
          if (k === 'x') moveX(el, v - (sel.length > 1 ? union(sel).l : pr.l));
          if (k === 'y') moveY(el, v - (sel.length > 1 ? union(sel).t : pr.t));
          if (k === 'w') el.style.width = v + 'pt'; if (k === 'h') el.style.height = v + 'pt';
          if (k === 'fs') el.style.fontSize = v + 'pt'; if (k === 'lh') el.style.lineHeight = v + 'pt';
          if (k === 'ls') el.style.letterSpacing = (v / 1000) + 'em'; if (k === 'fw') el.style.fontWeight = inp.value;
          if (k === 'mt') el.style.marginTop = v + 'pt'; if (k === 'mb') el.style.marginBottom = v + 'pt';
          if (k === 'pd') el.style.padding = v + 'pt'; if (k === 'op') el.style.opacity = Math.max(0, Math.min(100, v)) / 100;
        }));
        checkFlow(); draw();
      };
      inp.addEventListener('input', () => { if (u) { pushUndo(u); u = null; } apply(); });
      inp.addEventListener('change', () => { apply(); buildThumbs(); buildProps(); });
      inp.addEventListener('keydown', e => { if (e.key === 'Enter') inp.blur(); e.stopPropagation(); });
    });
  }
  function selParent() { if (sel[0] && sel[0].parentElement !== pageEl()) select([sel[0].parentElement]); }
  function selChild() { if (sel[0] && kids(sel[0])[0]) select([kids(sel[0])[0]]); }
  function selSibling(dir) { const s = sel[0]; if (!s) return; const k = kids(s.parentElement); const i = k.indexOf(s); const n = k[(i + dir + k.length) % k.length]; if (n) select([n]); }

  /* ---------- save / export ---------- */
  function saveFile() {
    if (editing) endEdit();
    const doc = document.documentElement.cloneNode(true);
    const body = doc.querySelector('body');
    const script = [...doc.querySelectorAll('script')].pop();
    doc.querySelectorAll('#fx-stage .page').forEach(p => { p.classList.remove('fx-hidden'); body.insertBefore(p, script); });
    doc.querySelectorAll('#fx-root,#fx-style').forEach(n => n.remove());
    doc.querySelectorAll('[contenteditable]').forEach(n => n.removeAttribute('contenteditable'));
    body.classList.remove('fx', 'fx-editing'); if (!body.className) body.removeAttribute('class');
    const blob = new Blob(['<!doctype html>\n' + doc.outerHTML], { type: 'text/html' });
    const base = decodeURIComponent(location.pathname.split(/[\\/]/).pop() || 'whitepaper.html').replace(/\.html$/, '');
    const name = base.replace(/_edited(\(\d+\))?$/, '') + '_edited.html';
    const fallback = () => { const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = name; a.click(); toast('Saved ' + name + ' to your Downloads'); };
    if (window.showSaveFilePicker) {
      window.showSaveFilePicker({ suggestedName: name, types: [{ description: 'HTML page', accept: { 'text/html': ['.html'] } }] })
        .then(async h => { const w = await h.createWritable(); await w.write(blob); await w.close(); toast('Saved ' + h.name); })
        .catch(err => { if (err && err.name !== 'AbortError') fallback(); });
    } else fallback();
  }
  function exportPdf() { if (editing) endEdit(); const s = sel; sel = []; draw(); setTimeout(() => { window.print(); sel = s; draw(); }, 50); }

  /* ---------- keyboard ---------- */
  document.addEventListener('keydown', e => {
    const mod = e.ctrlKey || e.metaKey, tag = (e.target.tagName || '');
    if (editing) { if (e.key === 'Escape') { e.preventDefault(); endEdit(); } return; }
    if (/INPUT|SELECT|TEXTAREA/.test(tag)) return;
    if (mod && e.key.toLowerCase() === 'z') { e.preventDefault(); e.shiftKey ? redo() : undo(); return; }
    if (mod && e.key.toLowerCase() === 'y') { e.preventDefault(); redo(); return; }
    if (mod && e.key.toLowerCase() === 's') { e.preventDefault(); saveFile(); return; }
    if (mod && e.key.toLowerCase() === 'p') { e.preventDefault(); exportPdf(); return; }
    if (mod && e.key.toLowerCase() === 'd') { e.preventDefault(); duplicate(); return; }
    if (mod && e.shiftKey && e.key.toLowerCase() === 'h') { e.preventDefault(); toggleHide(); return; }
    if (mod && e.shiftKey && e.key.toLowerCase() === 'l') { e.preventDefault(); toggleLock(); return; }
    if (!mod && !e.altKey && e.shiftKey && e.key.toLowerCase() === 'a') { e.preventDefault(); setAuto(!autoLayout); return; }
    if (mod && e.key === "'") { e.preventDefault(); showGrid = !showGrid; $('#fx-gridbtn').classList.toggle('on', showGrid); draw(); return; }
    if (mod && (e.key === '=' || e.key === '+')) { e.preventDefault(); setZoom(zoom * 1.25); return; }
    if (mod && e.key === '-') { e.preventDefault(); setZoom(zoom / 1.25); return; }
    if (e.shiftKey && e.code === 'Digit1') { fit(); return; } if (e.shiftKey && e.code === 'Digit0') { setZoom(1); return; }
    if (e.key === 'PageDown') { showPage(cur + 1); return; } if (e.key === 'PageUp') { showPage(cur - 1); return; }
    if (e.altKey && !mod) { const m = { a: 'l', d: 'r', h: 'c', w: 't', s: 'b', v: 'm' }[e.key.toLowerCase()]; if (m) { e.preventDefault(); align(m); return; } }
    if (!sel.length) return;
    const s = e.shiftKey ? 10 : 1, ar = { ArrowUp: [0, -s], ArrowDown: [0, s], ArrowLeft: [-s, 0], ArrowRight: [s, 0] }[e.key];
    if (ar) { e.preventDefault(); nudge(...ar); return; }
    if (e.key === 'Escape') { e.preventDefault(); sel[0].parentElement === pageEl() ? select([]) : selParent(); return; }
    if (e.key === 'Enter') { e.preventDefault(); if (hasText(sel[0]) && !kids(sel[0]).length) startEdit(sel[0]); else selChild(); return; }
    if (e.key === 'Tab') { e.preventDefault(); selSibling(e.shiftKey ? -1 : 1); return; }
    if (e.key === 'Delete' || e.key === 'Backspace') { e.preventDefault(); remove(); return; }
  });
  canvas.addEventListener('wheel', e => { if (e.ctrlKey || e.metaKey) { e.preventDefault(); setZoom(zoom * (e.deltaY < 0 ? 1.1 : 1 / 1.1)); } }, { passive: false });
  canvas.addEventListener('mousedown', e => { if (e.target === canvas || e.target === wrap) { if (editing) endEdit(); select([]); } });

  /* ---------- top bar ---------- */
  $('#fx-prev').onclick = () => showPage(cur - 1); $('#fx-next').onclick = () => showPage(cur + 1);
  $('#fx-zin').onclick = () => setZoom(zoom * 1.25); $('#fx-zout').onclick = () => setZoom(zoom / 1.25);
  $('#fx-zfit').onclick = fit; $('#fx-z100').onclick = () => setZoom(1);
  $('#fx-gridbtn').onclick = () => { showGrid = !showGrid; $('#fx-gridbtn').classList.toggle('on', showGrid); draw(); };
  function setAuto(v) { autoLayout = v; $('#fx-autobtn').classList.toggle('on', v); toast(v ? 'Auto layout on · vertical moves push content below' : 'Auto layout off · elements move freely'); }
  $('#fx-autobtn').onclick = () => setAuto(!autoLayout);
  $('#fx-undo').onclick = undo; $('#fx-redo').onclick = redo; $('#fx-save').onclick = saveFile; $('#fx-pdf').onclick = exportPdf;
  $('#fx-helpbtn').onclick = () => $('#fx-help').style.display = 'flex'; $('#fx-helpclose').onclick = () => $('#fx-help').style.display = 'none';
  window.addEventListener('beforeprint', () => { overlay.innerHTML = ''; });
  window.addEventListener('afterprint', () => draw());

  /* expose for testing */
  window.fxEditor = { setAuto, toggleLock, checkFlow, get flow() { return flow; }, select: els => select(els), align, distribute, textAlign, nudge, undo, redo, showPage, get sel() { return sel; }, get zoom() { return zoom; }, saveFile, pageEl };

  initLocks(); showPage(0); setTimeout(fit, 60); window.addEventListener('load', () => { fit(); buildThumbs(); });
  updBtns();
})();
