/* Artboard exporters (UI only, never part of an artboard).
   toSVG(ab)   -> SVG markup: rects, clipped images, vector logo/notches/icons, live <text>.
                  Paste straight into Figma (Ctrl/Cmd+V) for editable layers.
   toFigma(ab) -> JSON layer tree for the "Sonim template paste" Figma plugin (figma-plugin/),
                  which rebuilds the artboard with auto layout on every flex stack.
   Both measure the artboard at 100% (the zoom transform is lifted while measuring). */
(function () {
  const N = v => Math.round(v * 100) / 100;
  const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  function hex(c) {
    const m = String(c).match(/rgba?\(([^)]+)\)/); if (!m) return c;
    const [r, g, b, a] = m[1].split(',').map(parseFloat);
    if (a === 0) return null;
    return '#' + [r, g, b].map(v => Math.round(v).toString(16).padStart(2, '0')).join('').toUpperCase();
  }
  const visible = el => { const cs = getComputedStyle(el); return cs.display !== 'none' && cs.visibility !== 'hidden'; };
  const skip = el => el.classList && (el.classList.contains('guide') || el.classList.contains('frame-tools'));
  const layerName = el => (el.dataset && el.dataset.name) || (el.tagName === 'IMG' ? 'Image' : 'Group');

  /* measure with the zoom transform removed so every coordinate is in artboard px */
  function measured(ab, fn) {
    const t = ab.style.transform; ab.style.transform = '';
    try { return fn(ab.getBoundingClientRect()); } finally { ab.style.transform = t; }
  }
  const relTo = R => el => { const r = el.getBoundingClientRect(); return { x: r.left - R.left, y: r.top - R.top, w: r.width, h: r.height }; };

  /* image placement for object-fit / object-position (px or %) */
  function imgBox(el, r) {
    const cs = getComputedStyle(el), nw = el.naturalWidth, nh = el.naturalHeight;
    const fit = cs.objectFit;
    const k = fit === 'cover' ? Math.max(r.w / nw, r.h / nh) : fit === 'contain' ? Math.min(r.w / nw, r.h / nh) : fit === 'none' ? 1 : null;
    const dw = k === null ? r.w : nw * k, dh = k === null ? r.h : nh * k;
    const pos = cs.objectPosition.split(' ');
    const off = (v, free) => v.endsWith('%') ? free * parseFloat(v) / 100 : parseFloat(v) || 0;
    return { fit, dw, dh, ox: off(pos[0] || '50%', r.w - dw), oy: off(pos[1] || '50%', r.h - dh) };
  }

  /* inline <svg> re-expressed as a transformed group (Figma keeps it as vectors) */
  function svgInner(el) {
    const color = hex(getComputedStyle(el).color) || '#000000';
    const ser = new XMLSerializer();
    return [...el.childNodes].map(n => ser.serializeToString(n)).join('')
      .replace(/ xmlns="http:\/\/www\.w3\.org\/2000\/svg"/g, '').replace(/currentColor/g, color);
  }
  function svgAttrs(el) {
    const color = hex(getComputedStyle(el).color) || '#000000';
    return ['fill', 'stroke', 'stroke-width', 'stroke-linecap', 'stroke-linejoin', 'fill-rule']
      .filter(a => el.hasAttribute(a)).map(a => `${a}="${esc(el.getAttribute(a).replace('currentColor', color))}"`).join(' ');
  }
  function svgStandalone(el, w, h) {
    const vb = el.getAttribute('viewBox'), par = el.getAttribute('preserveAspectRatio');
    return `<svg xmlns="http://www.w3.org/2000/svg" width="${N(w)}" height="${N(h)}" viewBox="${vb}"${par ? ` preserveAspectRatio="${par}"` : ''} ${svgAttrs(el)}>${svgInner(el)}</svg>`;
  }

  /* text: measure every character, group into runs by line and style, emit exact baselines */
  function textRuns(el, rel) {
    const runs = []; const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT); let n;
    const rg = document.createRange();
    while ((n = walker.nextNode())) {
      const p = n.parentElement, cs = getComputedStyle(p), fs = parseFloat(cs.fontSize);
      const style = { fill: hex(cs.color), weight: cs.fontWeight, size: fs, ls: cs.letterSpacing === 'normal' ? 0 : parseFloat(cs.letterSpacing) };
      for (let i = 0; i < n.data.length; i++) {
        rg.setStart(n, i); rg.setEnd(n, i + 1);
        const b = rg.getClientRects()[0]; if (!b || b.width === 0) continue;
        const r = rel({ getBoundingClientRect: () => b });
        const ch = n.data[i].replace(/\s/, ' ');
        const last = runs[runs.length - 1];
        const baseline = r.y + r.h * 0.905 / 1.117;   // Arial ascent / content-area height
        if (last && last.style === style && Math.abs(last.baseline - baseline) < fs * 0.3) last.text += ch;
        else runs.push({ style, x: r.x, baseline, text: ch });
      }
    }
    return runs.map(r => ({ ...r, text: r.text.replace(/\s+$/, '') })).filter(r => r.text);
  }

  function toSVG(ab) {
    return measured(ab, R => {
      const rel = relTo(R), defs = [], names = new Map(); let clipN = 0;
      const id = el => { const n = layerName(el); const c = (names.get(n) || 0) + 1; names.set(n, c); return esc(c > 1 ? `${n} ${c}` : n); };
      const clip = r => { const c = 'clip' + (++clipN); defs.push(`<clipPath id="${c}"><rect x="${N(r.x)}" y="${N(r.y)}" width="${N(r.w)}" height="${N(r.h)}"/></clipPath>`); return c; };
      function node(el) {
        if (el.nodeType !== 1 || skip(el) || !visible(el)) return '';
        const r = rel(el), cs = getComputedStyle(el);
        if (el.tagName.toLowerCase() === 'svg') {
          const vb = el.viewBox.baseVal; if (!vb || !vb.width) return '';
          let sx = r.w / vb.width, sy = r.h / vb.height, tx = r.x, ty = r.y;
          if (!/none/.test(el.getAttribute('preserveAspectRatio') || '')) { const k = Math.min(sx, sy); tx += (r.w - vb.width * k) / 2; ty += (r.h - vb.height * k) / 2; sx = sy = k; }
          return `<g id="${id(el)}" transform="translate(${N(tx - vb.x * sx)} ${N(ty - vb.y * sy)}) scale(${N(sx * 1e4) / 1e4} ${N(sy * 1e4) / 1e4})" ${svgAttrs(el)}>${svgInner(el)}</g>`;
        }
        if (el.tagName === 'IMG') {
          if (!el.naturalWidth) return '';
          const b = imgBox(el, r);
          const img = `<image xlink:href="${el.src}" x="${N(r.x + b.ox)}" y="${N(r.y + b.oy)}" width="${N(b.dw)}" height="${N(b.dh)}" preserveAspectRatio="none"/>`;
          return b.fit === 'cover' || b.dw > r.w + .5 || b.dh > r.h + .5 ? `<g id="${id(el)}" clip-path="url(#${clip(r)})">${img}</g>` : `<g id="${id(el)}">${img}</g>`;
        }
        let out = '';
        const bg = hex(cs.backgroundColor);
        if (bg) out += `<rect id="${el.classList.contains('shape') ? id(el) : 'Fill'}" x="${N(r.x)}" y="${N(r.y)}" width="${N(r.w)}" height="${N(r.h)}" fill="${bg}"/>`;
        if (el.classList.contains('tx')) {
          const spans = textRuns(el, rel).map(t => `<tspan x="${N(t.x)}" y="${N(t.baseline)}" fill="${t.style.fill}" font-size="${N(t.style.size)}" font-weight="${t.style.weight >= 600 ? 700 : 400}"${t.style.ls ? ` letter-spacing="${N(t.style.ls)}"` : ''}>${esc(t.text)}</tspan>`).join('');
          return out + `<text id="${id(el)}" font-family="Arial, Helvetica, sans-serif" xml:space="preserve">${spans}</text>`;
        }
        const kids = [...el.children].map(node).join('');
        if (el.classList.contains('shape')) return out + kids;
        const clipAttr = cs.overflow === 'hidden' ? ` clip-path="url(#${clip(r)})"` : '';
        return kids ? `<g id="${id(el)}"${clipAttr}>${out}${kids}</g>` : out;
      }
      const W = N(R.width), H = N(R.height), bg = hex(getComputedStyle(ab).backgroundColor) || '#FFFFFF';
      const body = [...ab.children].map(node).join('');
      return `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">`
        + `<defs>${defs.join('')}<clipPath id="artboard"><rect width="${W}" height="${H}"/></clipPath></defs>`
        + `<g id="${esc(ab.dataset.name || 'Artboard')}" clip-path="url(#artboard)"><rect id="Background" width="${W}" height="${H}" fill="${bg}"/>${body}</g></svg>`;
    });
  }

  /* ---------------- Figma layer tree (auto layout) ---------------- */
  const AX = { 'flex-start': 'MIN', start: 'MIN', normal: 'MIN', stretch: 'MIN', center: 'CENTER', 'flex-end': 'MAX', end: 'MAX', 'space-between': 'SPACE_BETWEEN', baseline: 'MIN' };
  function textNode(el, r) {
    const cs = getComputedStyle(el); let chars = ''; const runs = [];
    (function walk(n) {
      for (const c of n.childNodes) {
        if (c.nodeType === 3) {
          const t = c.data.replace(/\s+/g, ' '); if (!t) continue;
          const p = getComputedStyle(c.parentElement);
          runs.push({ start: chars.length, end: chars.length + t.length, color: hex(p.color), bold: +p.fontWeight >= 600 });
          chars += t;
        } else if (c.nodeName === 'BR') chars += '\n';
        else if (c.nodeType === 1) walk(c);
      }
    })(el);
    const lh = cs.lineHeight === 'normal' ? null : parseFloat(cs.lineHeight);
    return {
      type: 'TEXT', name: layerName(el), x: r.x, y: r.y, w: r.w, h: r.h, chars, runs,
      size: parseFloat(cs.fontSize), lh, ls: cs.letterSpacing === 'normal' ? 0 : parseFloat(cs.letterSpacing),
      align: { right: 'RIGHT', end: 'RIGHT', center: 'CENTER' }[cs.textAlign] || 'LEFT',
      autoWidth: cs.position === 'absolute' && !el.style.width && !el.style.maxWidth,
    };
  }
  function toFigma(ab) {
    return measured(ab, R => {
      const rel0 = relTo(R);
      function node(el, parent) {
        if (el.nodeType !== 1 || skip(el) || !visible(el)) return null;
        const a = rel0(el), cs = getComputedStyle(el);
        const r = { x: a.x - parent.x, y: a.y - parent.y, w: a.w, h: a.h };
        const flow = { abs: cs.position === 'absolute', grow: parseFloat(cs.flexGrow) > 0 ? 1 : 0 };
        if (el.tagName.toLowerCase() === 'svg') return { type: 'SVG', name: layerName(el), ...r, ...flow, svg: svgStandalone(el, r.w, r.h) };
        if (el.tagName === 'IMG') {
          if (!el.naturalWidth) return null; const b = imgBox(el, r);
          return { type: 'IMAGE', name: layerName(el), ...r, ...flow, src: el.src, fit: b.fit === 'contain' ? 'FIT' : 'CROP',
            crop: [[r.w / b.dw, 0, -b.ox / b.dw], [0, r.h / b.dh, -b.oy / b.dh]] };
        }
        if (el.classList.contains('tx')) return { ...textNode(el, r), ...flow };
        const f = { type: 'FRAME', name: layerName(el), ...r, ...flow, fill: hex(cs.backgroundColor), clip: cs.overflow === 'hidden', children: [] };
        const kids = [...el.children].map(c => node(c, a)).filter(Boolean);
        const disp = cs.display;
        if (disp === 'flex' || disp === 'grid') {
          const vertical = disp === 'flex' && cs.flexDirection.startsWith('column');
          const pad = ['Top', 'Right', 'Bottom', 'Left'].map(s => parseFloat(cs['padding' + s]) || 0);
          const inflow = kids.filter(k => !k.abs);
          const gapCss = parseFloat(vertical ? cs.rowGap : cs.columnGap) || 0;
          f.layout = { mode: vertical ? 'VERTICAL' : 'HORIZONTAL', gap: gapCss, pad, primary: AX[cs.justifyContent] || 'MIN', counter: AX[cs.alignItems] || 'MIN' };
          if (disp === 'grid') { f.layout.wrap = true; f.layout.rowGap = parseFloat(cs.rowGap) || 0; f.layout.gap = parseFloat(cs.columnGap) || 0; }
          else if (inflow.length > 1 && f.layout.primary !== 'SPACE_BETWEEN') {
            /* margins (e.g. margin-top on a caption) become explicit spacers so the Figma gap stays exact */
            const d = inflow.slice(1).map((k, i) => vertical ? k.y - (inflow[i].y + inflow[i].h) : k.x - (inflow[i].x + inflow[i].w));
            if (d.some(v => Math.abs(v - d[0]) > .75)) {
              f.layout.gap = 0; const seq = [];
              inflow.forEach((k, i) => { if (i && d[i - 1] > .5 && !k.grow && !inflow[i - 1].grow) seq.push({ type: 'SPACER', name: 'Spacer', w: vertical ? 0 : d[i - 1], h: vertical ? d[i - 1] : 0 }); seq.push(k); });
              f.children = seq.concat(kids.filter(k => k.abs));
            } else f.layout.gap = Math.max(0, d[0]);
          }
          const cw = r.w - pad[1] - pad[3];
          inflow.forEach(k => { if (vertical && Math.abs(k.w - cw) < 1) k.stretch = true; });
        }
        if (!f.children.length) f.children = kids;
        return f;
      }
      const root = node(ab, { x: 0, y: 0 });
      Object.assign(root, { x: 0, y: 0, clip: true, fill: hex(getComputedStyle(ab).backgroundColor) || '#FFFFFF', layout: null });
      return JSON.stringify({ sonimFigma: 1, version: 1, node: root });
    });
  }
  window.sonimExport = { toSVG, toFigma };
})();
