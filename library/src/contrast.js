/* Shared by both audits (injected into the page): contrast of each text element against what is painted behind it.
   contrastIssues(textEls, scopeEl) -> ["low contrast 1.0:1 ...", ...]. Text over photos/images is skipped. */
function contrastIssues(textEls, scope, name) {
  const parse = c => { const m = String(c).match(/rgba?\(([^)]+)\)/); if (!m) return null; const v = m[1].split(',').map(parseFloat); return { r: v[0], g: v[1], b: v[2], a: v.length > 3 ? v[3] : 1 }; };
  const lum = c => { const f = x => { x /= 255; return x <= 0.03928 ? x / 12.92 : Math.pow((x + 0.055) / 1.055, 2.4); }; return 0.2126 * f(c.r) + 0.7152 * f(c.g) + 0.0722 * f(c.b); };
  const ratio = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
  const out = [];
  for (const t of textEls) {
    if (t.closest('[data-audit="specimen"]')) continue;   // deliberate examples (e.g. non-approved colour pairs)
    const fg = parse(getComputedStyle(t).color); if (!fg || fg.a < 0.05) continue;
    // check each run of text with its own colour (spans inside the element can differ)
    const runs = [t, ...t.querySelectorAll('*')].filter(e => [...e.childNodes].some(n => n.nodeType === 3 && n.data.trim()));
    for (const e of runs) {
      const c = parse(getComputedStyle(e).color); if (!c) continue;
      const rg = document.createRange(); rg.selectNodeContents(e); const q = [...rg.getClientRects()].find(r => r.width > 2); if (!q) continue;
      e.scrollIntoView({ block: 'center', inline: 'center' });
      const q2 = [...rg.getClientRects()].find(r => r.width > 2);
      const stack = document.elementsFromPoint(q2.left + Math.min(q2.width / 2, 20), (q2.top + q2.bottom) / 2);
      let bg = null, photo = false;
      for (const el of stack) {
        if (!scope.contains(el)) break;
        if (el !== e && e.contains(el)) continue;            // the text's own children; its own box and ancestors count
        if (el.tagName === 'IMG' || el.tagName === 'image' || getComputedStyle(el).backgroundImage !== 'none') { photo = true; break; }
        const b = parse(getComputedStyle(el).backgroundColor); if (b && b.a > 0.5) { bg = b; break; }
      }
      if (photo) continue;
      if (!bg) { const b = parse(getComputedStyle(scope).backgroundColor); bg = b && b.a > 0.5 ? b : { r: 255, g: 255, b: 255, a: 1 }; }
      const r = ratio(c, bg);
      if (r < 2) out.push(`low contrast ${r.toFixed(1)}:1 (text ${getComputedStyle(e).color} on rgb(${bg.r}, ${bg.g}, ${bg.b})): ${name(e)}`);
    }
  }
  return out;
}
