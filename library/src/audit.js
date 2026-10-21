/* Layout audit for every artboard in the built library. Fails (exit 1) on any finding.
   Checks: text outside the artboard, text clipped by its box or a clipping parent, text overlapping other
   text / logos / icons, text below 12 px, bold text under 16 px, content crowding the footer or logo,
   text outside the format's margins, broken images.
   Usage: node library/src/audit.js [id,id,...]  */
const { chromium } = require('playwright');
const path = require('path');
const MARG = { web: 12, blog: 96, doc: 60, slide: 120, post: 80, story: 80, land: 64, poster: 96, rollup: 56, other: 64 };
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 2200, height: 2000 } });
  await p.goto('file://' + path.resolve(__dirname, '../dist/Sonim_Brand_Template_Library.html') + '?figma'); await p.waitForTimeout(800);
  await p.addScriptTag({ path: path.join(__dirname, 'contrast.js') });
  const only = process.argv[2] ? process.argv[2].split(',') : null;
  const res = await p.evaluate(({ MARG, only }) => {
    const out = [];
    const R = (e, ab) => { const r = e.getBoundingClientRect(), a = ab.getBoundingClientRect(); return { l: r.left - a.left, t: r.top - a.top, r: r.right - a.left, b: r.bottom - a.top, w: r.width, h: r.height }; };
    const inter = (a, c) => Math.max(0, Math.min(a.r, c.r) - Math.max(a.l, c.l)) * Math.max(0, Math.min(a.b, c.b) - Math.max(a.t, c.t));
    // tight box of the actual glyph lines (not the full-width block)
    // each text line as its line box (font content area trimmed to the line height), so tight leading isn't an overlap
    const lines = (e, ab) => { const rg = document.createRange(); rg.selectNodeContents(e); const a = ab.getBoundingClientRect();
      const cs = getComputedStyle(e), fs = parseFloat(cs.fontSize), lh = cs.lineHeight === 'normal' ? fs * 1.2 : parseFloat(cs.lineHeight);
      const ink = Math.min(lh, fs * 1.0);   // cap height + descenders sit inside ~1em
      return [...rg.getClientRects()].filter(q => q.width > 1).map(q => { const cy = (q.top + q.bottom) / 2 - a.top;
        return { l: q.left - a.left, t: cy - ink / 2, r: q.right - a.left, b: cy + ink / 2 }; }); };
    for (const f of document.querySelectorAll('.frame')) {
      if (only && !only.includes(f.id)) continue;
      const ab = f.querySelector('.ab'), W = ab.offsetWidth, H = ab.offsetHeight, m = MARG[f.dataset.fmt] || 60;
      const issues = [];
      const txs = [...ab.querySelectorAll('.tx')].filter(t => t.textContent.trim() && getComputedStyle(t).visibility !== 'hidden');
      const name = t => `${t.dataset.name} "${t.textContent.trim().slice(0, 28)}"`;
      for (const t of txs) {
        const cs = getComputedStyle(t), fs = parseFloat(cs.fontSize), fw = parseInt(cs.fontWeight);
        const r = R(t, ab), ls = lines(t, ab);
        if (fs < 12) issues.push(`font ${fs}px < 12: ${name(t)}`);
        // bold under 16 px; inline emphasis spans inherit, so check the element and its spans
        if (fs < 16 && fw >= 600) issues.push(`bold at ${fs}px: ${name(t)}`);
        for (const q of ls) if (q.l < -1 || q.t < -1 || q.r > W + 1 || q.b > H + 1) { issues.push(`outside artboard: ${name(t)}`); break; }
        if ((cs.overflow !== 'visible' || t.style.height) && (t.scrollHeight > t.clientHeight + 2 || t.scrollWidth > t.clientWidth + 2)) issues.push(`clipped by own box: ${name(t)}`);
        if (ls.some(q => q.r > r.r + 2)) issues.push(`runs past its box: ${name(t)}`);
        for (let a = t.parentElement; a && a !== ab; a = a.parentElement) {
          if (getComputedStyle(a).overflow === 'hidden') { const ar = R(a, ab); if (ls.some(q => q.b > ar.b + 1 || q.r > ar.r + 1 || q.t < ar.t - 1)) issues.push(`clipped by ${a.dataset.name}: ${name(t)}`); break; }
        }
        // glyphs outside the format margin (decorative full-bleed elements don't carry text)
        const sb = parseFloat(cs.fontSize) >= 120 ? parseFloat(cs.fontSize) * 0.06 : 0;   // big numerals hang into the margin by their side bearing
        if (ls.some(q => q.l < m - 2 - sb || q.r > W - m + 2 || q.t < Math.min(m, 24) - 2 || q.b > H - Math.min(m, 24) + 2)) {
          if (!t.style.getPropertyValue('--bleed')) issues.push(`outside ${m}px margin: ${name(t)}`);
        }
      }
      // text hidden under something painted on top of it (photo, panel, shape): sample points along each line
      const opaque = e => { if (e.tagName === 'IMG' || e.closest('svg')) return true; const bg = getComputedStyle(e).backgroundColor;
        return bg && !/rgba\(0, 0, 0, 0\)|transparent/.test(bg); };
      for (const t of txs) {
        if (t.style.getPropertyValue('--bleed')) continue;   // deliberate: product render over the model number
        t.scrollIntoView({ block: 'center', inline: 'center' });
        const rg = document.createRange(); rg.selectNodeContents(t);
        outer: for (const q of [...rg.getClientRects()].filter(q => q.width > 4)) {
          for (const fx of [0.08, 0.5, 0.92]) {
            const hit = document.elementFromPoint(q.left + q.width * fx, (q.top + q.bottom) / 2);
            if (!hit || hit === t || t.contains(hit) || !ab.contains(hit) || hit.classList.contains('guide')) continue;
            if (hit.closest('.tx') || !opaque(hit)) continue;      // other text: overlap check; transparent layout boxes
            issues.push(`text covered by ${hit.dataset.name || hit.closest('[data-name]')?.dataset.name || hit.tagName}: ${name(t)}`); break outer;
          }
        }
      }
      issues.push(...contrastIssues(txs.filter(t => !t.style.getPropertyValue('--bleed')), ab, t => `${(t.closest('.tx') || t).dataset.name} "${t.textContent.trim().slice(0, 28)}"`));
      // text on text / text on logo or icon
      const marks = [...ab.querySelectorAll('.logo, .icon')];
      for (let i = 0; i < txs.length; i++) {
        const li = lines(txs[i], ab);
        for (let j = i + 1; j < txs.length; j++) {
          if (txs[i].contains(txs[j]) || txs[j].contains(txs[i])) continue;
          if (txs[i].style.getPropertyValue('--bleed') && txs[j].style.getPropertyValue('--bleed')) continue;
          const lj = lines(txs[j], ab);
          if (li.some(a => lj.some(c => inter(a, c) > 6))) issues.push(`text overlaps text: ${name(txs[i])} × ${name(txs[j])}`);
        }
        for (const mk of marks) { const mr = R(mk, ab); if (li.some(a => inter(a, mr) > 6)) issues.push(`text overlaps ${mk.dataset.name}: ${name(txs[i])}`); }
      }
      // footer / bottom logo clearance: nothing within C px above it in its column
      const C = Math.round(m * 0.4);
      const feet = [...ab.querySelectorAll('[data-name="Footer"], .logo')].filter(e => R(e, ab).t > H * 0.75);
      const content = [...ab.querySelectorAll('.tx, .icon, .shape, .photo, .rugged, [data-name="Icon tiles"]')];
      for (const ft of feet) {
        const fr = R(ft, ab);
        for (const c of content) {
          if (ft.contains(c) || c.contains(ft) || c.closest('[data-name="Footer"]')) continue;
          const cr = R(c, ab);
          if (cr.w >= W - 2 && cr.h >= H - 2) continue;                     // full-artboard backgrounds
          if (cr.b > fr.t + 2 || cr.r < fr.l || cr.l > fr.r) continue;       // not above it / not in its column
          if (c.classList.contains('shape') && (cr.h < 3 || cr.t < fr.t - H * 0.6)) continue;   // hairlines, big panels the footer sits on
          if (c.classList.contains('photo') || c.closest('.group') && !c.classList.contains('tx')) continue;
          const gap = fr.t - cr.b;
          if (gap < C) issues.push(`only ${Math.round(gap)}px above ${ft.dataset.name} (min ${C}): ${c.classList.contains('tx') ? name(c) : c.dataset.name}`);
        }
      }
      // logos and icons sit inside the margin (logos) / the artboard (icons)
      for (const lg of ab.querySelectorAll('.logo')) { const q = R(lg, ab), mm = Math.min(m, 24);
        if (q.l < Math.min(m, 40) - 2 || q.r > W - Math.min(m, 40) + 2 || q.t < mm - 2 || q.b > H - mm + 2) issues.push(`logo outside margin at ${Math.round(q.l)},${Math.round(q.t)}`); }
      for (const ic of ab.querySelectorAll('.icon')) { const q = R(ic, ab); if (q.l < 0 || q.t < 0 || q.r > W || q.b > H) issues.push(`icon outside artboard: ${ic.dataset.name}`); }
      for (const im of ab.querySelectorAll('img')) if (!im.complete || !im.naturalWidth) issues.push(`broken image: ${im.dataset.name}`);
      if (issues.length) out.push([f.id, [...new Set(issues)]]);
    }
    return out;
  }, { MARG, only });
  let n = 0; for (const [id, is] of res) { console.log(`\n${id}`); for (const i of is) { console.log('  - ' + i); n++; } }
  console.log(`\n${n} findings in ${res.length} artboards`); await b.close(); process.exit(n ? 1 : 0);
})();
