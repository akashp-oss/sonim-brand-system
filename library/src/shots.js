const { chromium } = require('playwright');
const QA = require('path').resolve(__dirname, '../../.qa'); require('fs').mkdirSync(QA, { recursive: true });
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1600, height: 1000 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto('file://' + require('path').resolve(__dirname, '../dist/Sonim_Brand_Template_Library.html') + '?figma'); await p.waitForTimeout(800);
  const ids = await p.$$eval('.frame', fs => fs.map(f => f.id));
  const only = process.argv[2] ? process.argv[2].split(',') : null;
  for (const id of ids) { if (only && !only.includes(id)) continue; await p.locator('#' + id + ' .ab').screenshot({ path: `${QA}/${id}.png` }); }
  // overflow check: text boxes that exceed the artboard
  const ov = await p.evaluate(() => [...document.querySelectorAll('.ab')].map(ab => { const r = ab.getBoundingClientRect(); const bad = [...ab.querySelectorAll('.tx')].filter(t => { const q = t.getBoundingClientRect(); return q.right > r.right + 1 || q.bottom > r.bottom + 1 || q.left < r.left - 1; }).map(t => t.dataset.name + ':' + t.textContent.slice(0, 20)); return [ab.dataset.name, bad]; }).filter(x => x[1].length));
  console.log('overflow', JSON.stringify(ov, null, 1)); console.log('errors', errs); await b.close();
})();
