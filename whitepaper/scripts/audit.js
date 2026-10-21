/* Layout audit for the white paper sources (same checks as library/src/audit.js, adapted to .page documents).
   Usage: node whitepaper/scripts/audit.js [src.html ...]   (default: every src/*.html). Exit 1 on findings. */
const fs = require('fs'), path = require('path'); const { chromium } = require('playwright');
const BRAND = path.resolve(__dirname, '../../brand'), SRC = path.resolve(__dirname, '../src');
const logo = fs.readFileSync(path.join(BRAND, 'logo/sonim-nexa-lockup.svg'), 'utf8');
const icons = JSON.parse(fs.readFileSync(path.join(BRAND, 'icons/all.json'), 'utf8'));
(async () => {
  const files = process.argv.slice(2).length ? process.argv.slice(2) : fs.readdirSync(SRC).filter(f => f.endsWith('.html') && !f.includes('.built')).map(f => path.join(SRC, f));
  const b = await chromium.launch(); let total = 0;
  for (const src of files) {
    const html = fs.readFileSync(src, 'utf8').replaceAll('{{LOGO}}', logo).replace(/\{\{icon:([a-z-]+)\}\}/g, (m, n) => icons[n] || m);
    const tmp = src.replace('.html', '.audit.html'); fs.writeFileSync(tmp, html);
    const p = await b.newPage({ viewport: { width: 1400, height: 1400 } });
    await p.goto('file://' + path.resolve(tmp), { waitUntil: 'networkidle' }); await p.emulateMedia({ media: 'print' });
    await p.addScriptTag({ path: path.resolve(__dirname, '../../library/src/contrast.js') });
    const res = await p.evaluate(() => {
      const out = [];
      const pages = [...document.querySelectorAll('.page, .sheet')];
      const textEls = root => [...root.querySelectorAll('*')].filter(e => [...e.childNodes].some(n => n.nodeType === 3 && n.data.trim()) && getComputedStyle(e).display !== 'none' && getComputedStyle(e).visibility !== 'hidden');
      // line boxes relative to the element's page, so scrolling between measurements doesn't matter
      const lines = e => { const rg = document.createRange(); rg.selectNodeContents(e); const fs = parseFloat(getComputedStyle(e).fontSize), P = e.closest('.page, .sheet').getBoundingClientRect();
        return [...rg.getClientRects()].filter(q => q.width > 1).map(q => { const cy = (q.top + q.bottom) / 2 - P.top; return { l: q.left - P.left, r: q.right - P.left, t: cy - fs / 2, b: cy + fs / 2 }; }); };
      const inter = (a, c) => Math.max(0, Math.min(a.r, c.r) - Math.max(a.l, c.l)) * Math.max(0, Math.min(a.b, c.b) - Math.max(a.t, c.t));
      const opaque = e => { if (e.tagName === 'IMG' || e.closest('svg')) return true; const bg = getComputedStyle(e).backgroundColor; return bg && !/rgba\(0, 0, 0, 0\)|transparent/.test(bg); };
      pages.forEach((pg, i) => {
        const issues = [], P0 = pg.getBoundingClientRect(), P = { left: 0, top: 0, right: P0.width, bottom: P0.height };
        const els = textEls(pg).filter(e => e.closest('.page, .sheet') === pg);
        const nm = e => `${e.tagName.toLowerCase()}${e.className ? '.' + String(e.className).split(' ')[0] : ''} "${e.textContent.trim().slice(0, 30)}"`;
        for (const e of els) {
          const cs = getComputedStyle(e), fs = parseFloat(cs.fontSize), fw = parseInt(cs.fontWeight);
          if (fs < 11.9 && !e.matches('sup.ref')) issues.push(   // footnote reference markers are superscripts by design
            `font ${(fs * 0.75).toFixed(1)}pt (${fs.toFixed(1)}px) < 12px: ${nm(e)}`);
          if (fs < 16 && fw >= 600) issues.push(`bold at ${fs.toFixed(1)}px: ${nm(e)}`);
          const ls = lines(e);
          if (ls.some(q => q.l < P.left - 1 || q.r > P.right + 1 || q.t < P.top - 1 || q.b > P.bottom + 1)) issues.push(`outside page: ${nm(e)}`);
          for (let c = e.parentElement; c && c !== pg; c = c.parentElement) {   // clipped by an overflow:hidden parent
            if (getComputedStyle(c).overflow !== 'visible') { const cr = c.getBoundingClientRect(), Pp = pg.getBoundingClientRect();
              if (ls.some(q => q.b > cr.bottom - Pp.top + 1 || q.r > cr.right - Pp.left + 1)) issues.push(`clipped by ${c.tagName.toLowerCase()}.${c.className}: ${nm(e)}`); break; } }
          // anything painted later that sits over the text (bands, photos) — checked against every opaque later sibling box
          for (const o of pg.querySelectorAll('[class]')) { if (o === e || o.contains(e) || e.contains(o) || !opaque(o) || o.tagName === 'svg') continue;
            if (!(e.compareDocumentPosition(o) & Node.DOCUMENT_POSITION_FOLLOWING)) continue;
            const or = o.getBoundingClientRect(), Pp = pg.getBoundingClientRect(); const R = { l: or.left - Pp.left, r: or.right - Pp.left, t: or.top - Pp.top, b: or.bottom - Pp.top };
            if (getComputedStyle(o).position === 'absolute' && ls.some(q => inter(q, R) > 6)) { issues.push(`text under ${o.tagName.toLowerCase()}.${String(o.className).split(' ')[0]}: ${nm(e)}`); break; } }
          e.scrollIntoView({ block: 'center', inline: 'center' });
          const rg = document.createRange(); rg.selectNodeContents(e);
          outer: for (const q of [...rg.getClientRects()].filter(q => q.width > 4)) for (const fx of [0.08, 0.5, 0.92]) {
            const hit = document.elementFromPoint(q.left + q.width * fx, (q.top + q.bottom) / 2);
            if (!hit || hit === e || e.contains(hit) || hit.contains(e) || !pg.contains(hit) || !opaque(hit)) continue;
            if ([...hit.childNodes].some(n => n.nodeType === 3 && n.data.trim())) continue;
            issues.push(`text covered by ${hit.tagName.toLowerCase()}.${hit.className}: ${nm(e)}`); break outer;
          }
        }
        issues.push(...contrastIssues(els, pg, nm));
        for (let a = 0; a < els.length; a++) { const la = lines(els[a]);
          for (let c = a + 1; c < els.length; c++) { if (els[a].contains(els[c]) || els[c].contains(els[a])) continue;
            const lc = lines(els[c]); if (la.some(x => lc.some(y => inter(x, y) > 6))) issues.push(`text overlaps text: ${nm(els[a])} × ${nm(els[c])}`); } }
        // footer clearance: content must stay 24px clear of the page logo / note
        const feet = [...pg.querySelectorAll('.page-logo, .page-note')];
        for (const f of feet) { const fr = f.getBoundingClientRect();
          for (const e of els) { if (f.contains(e) || e.closest('.page-logo,.page-note,.fullbleed')) continue; const r = e.getBoundingClientRect();   // same scroll state: both measured now
            if (r.bottom <= fr.top + 2 && r.right > fr.left && r.left < fr.right && fr.top - r.bottom < 24) issues.push(`only ${Math.round(fr.top - r.bottom)}px above footer: ${nm(e)}`); } }
        if (issues.length) out.push([i + 1, [...new Set(issues)]]);
      });
      return out;
    });
    fs.unlinkSync(tmp); await p.close();
    for (const [pg, is] of res) { console.log(`\n${path.basename(src)} · page ${pg}`); is.forEach(x => { console.log('  - ' + x); total++; }); }
  }
  console.log(`\n${total} findings`); await b.close(); process.exit(total ? 1 : 0);
})();
