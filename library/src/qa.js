const { chromium } = require('playwright'); const fs = require('fs');
require('fs').mkdirSync(require('path').resolve(__dirname, '../../.qa'), { recursive: true });
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1600, height: 1000 }, acceptDownloads: true });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('file://' + require('path').resolve(__dirname, '../dist/Sonim_Brand_Template_Library.html') + ''); await p.waitForTimeout(600);
  const r = await p.evaluate(() => {
    const cols = {}, fonts = {}, bgs = {}; let imgs = 0, broken = 0, pseudo = 0, nodes = 0;
    document.querySelectorAll('.ab *').forEach(el => { nodes++; const cs = getComputedStyle(el);
      if (el.classList.contains('tx')) { cols[cs.color] = (cols[cs.color] || 0) + 1; fonts[cs.fontFamily.split(',')[0]] = 1; }
      el.querySelectorAll(':scope > .em').forEach(e => { const c = getComputedStyle(e).color; cols['em ' + c] = (cols['em ' + c] || 0) + 1; });
      if (cs.backgroundColor !== 'rgba(0, 0, 0, 0)') bgs[cs.backgroundColor] = 1;
      if (el.tagName === 'IMG') { imgs++; if (!el.complete || !el.naturalWidth) broken++; }
      ['::before', '::after'].forEach(ps => { const c = getComputedStyle(el, ps).content; if (c && c !== 'none' && c !== 'normal') pseudo++; });
    });
    return { cols, fonts, bgs, imgs, broken, pseudo, nodes, frames: document.querySelectorAll('.ab').length };
  });
  console.log(JSON.stringify(r, null, 1));
  // every artboard exports to SVG and to the Figma plugin JSON without errors
  console.log('exports:', await p.evaluate(() => { const bad = []; let n = 0;
    document.querySelectorAll('.frame').forEach(f => { const ab = f.querySelector('.ab');
      try { const s = sonimExport.toSVG(ab); new DOMParser().parseFromString(s, 'image/svg+xml').querySelector('parsererror') && bad.push(f.id + ' svg-parse');
            JSON.parse(sonimExport.toFigma(ab)); n++; } catch (e) { bad.push(f.id + ' ' + e.message); } });
    return { ok: n, bad }; }));
  console.log('hover tools:', await p.evaluate(() => document.querySelectorAll('.frame-tools').length));
  // figma mode hides chrome
  await p.click('#btn-figma'); await p.waitForTimeout(200);
  console.log('figma chrome visible:', await p.evaluate(() => ['.topbar', '.sidebar', '.sec-head', '.frame-meta', '.frame-tools'].map(s => getComputedStyle(document.querySelector(s)).display)));
  console.log('scale in figma:', await p.evaluate(() => [...document.querySelectorAll('.ab')].filter(a => a.style.transform).length));
  await p.keyboard.press('Escape');
  // edit + save + reopen
  await p.click('#btn-edit'); const t = p.locator('#ig-stat .tx[data-name="Caption"]'); await t.click(); await p.keyboard.press('End'); await p.keyboard.type(' EDITED');
  await p.evaluate(() => { window.showSaveFilePicker = undefined; });
  const [d] = await Promise.all([p.waitForEvent('download'), p.click('#btn-save')]); const out = '' + require('path').resolve(__dirname, '../../.qa/lib_saved.html') + ''; await d.saveAs(out);
  console.log('saved KB', Math.round(fs.statSync(out).size / 1000));
  const p2 = await b.newPage(); p2.on('pageerror', e => errs.push('p2 ' + e.message)); await p2.goto('file://' + out); await p2.waitForTimeout(500);
  console.log('reopen:', await p2.evaluate(() => ({ edited: document.querySelector('#ig-stat .tx[data-name="Caption"]').textContent.includes('EDITED'), broken: [...document.querySelectorAll('.ab img')].filter(i => !i.naturalWidth).length, contenteditable: document.querySelectorAll('[contenteditable]').length, tools: document.querySelectorAll('.frame-tools').length })));
  console.log('errors', errs); await b.close(); })();
