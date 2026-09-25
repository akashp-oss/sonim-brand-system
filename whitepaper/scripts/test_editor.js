const { chromium } = require('playwright'); const fs = require('fs');
require('fs').mkdirSync(require('path').resolve(__dirname, '../../.qa'), { recursive: true });
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1440, height: 900 }, acceptDownloads: true });
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto('file://' + require('path').resolve(__dirname, '../dist/Sonim_EMS_Whitepaper_EDITOR.html') + ''); await p.waitForTimeout(400);
  await p.screenshot({ path: '' + require('path').resolve(__dirname, '../../.qa') + '/ed1.png' });
  const log = (...a) => console.log(...a);
  // 1. click on GPS label -> should select top-level grid first
  const gps = p.locator('#fx-stage .needs div').nth(3);
  await gps.click(); log('click1:', await p.evaluate(() => fxEditor.sel.map(e => e.className || e.tagName)));
  await gps.dblclick(); log('dbl1:', await p.evaluate(() => fxEditor.sel.map(e => e.className || e.tagName)));
  await gps.dblclick(); log('dbl2:', await p.evaluate(() => fxEditor.sel.map(e => e.className || e.tagName)));
  await gps.click({ modifiers: ['Control'] }); log('ctrl:', await p.evaluate(() => fxEditor.sel.map(e => (e.className || e.tagName) + ':' + e.textContent.trim())));
  // 2. select all 5 cells and distribute + align top
  await p.evaluate(() => fxEditor.select([...document.querySelectorAll('#fx-stage .needs > div')]));
  const before = await p.evaluate(() => [...document.querySelectorAll('#fx-stage .needs > div')].map(e => Math.round(e.getBoundingClientRect().left)));
  await p.evaluate(() => { const c = document.querySelectorAll('#fx-stage .needs > div')[3]; c.style.translate = '6pt 0pt'; });
  await p.evaluate(() => fxEditor.distribute('h'));
  const after = await p.evaluate(() => [...document.querySelectorAll('#fx-stage .needs > div')].map(e => Math.round(e.getBoundingClientRect().left)));
  log('distribute lefts', before, after, 'gaps', after.slice(1).map((v, i) => v - after[i]));
  // 3. text align center on one cell
  await p.evaluate(() => { fxEditor.select([document.querySelectorAll('#fx-stage .needs > div')[3]]); fxEditor.textAlign('center'); });
  log('textAlign:', await p.evaluate(() => { const d = document.querySelectorAll('#fx-stage .needs > div')[3]; const ic = d.querySelector('.ico'); return [d.style.textAlign, ic.style.marginLeft, Math.round(ic.getBoundingClientRect().left - d.getBoundingClientRect().left)]; }));
  // 4. drag title down 20px
  await p.evaluate(() => fxEditor.select([]));
  const t = p.locator('#fx-stage .display'); const bb = await t.boundingBox();
  await p.mouse.move(bb.x + 40, bb.y + 20); await p.mouse.down(); await p.mouse.move(bb.x + 45, bb.y + 60, { steps: 5 }); await p.mouse.up();
  log('drag sel:', await p.evaluate(() => fxEditor.sel.map(e => e.className)), 'translate', await p.evaluate(() => fxEditor.sel[0].style.translate));
  await p.screenshot({ path: '' + require('path').resolve(__dirname, '../../.qa') + '/ed2.png' });
  // 5. undo
  await p.keyboard.press('Control+z'); log('after undo translate:', await p.evaluate(() => document.querySelector('#fx-stage .notch-anchor').style.translate + '|' + document.querySelector('#fx-stage .display').style.translate));
  // 6. text edit
  await p.evaluate(() => fxEditor.select([]));
  const lead = p.locator('#fx-stage .page:not(.fx-hidden) .lead').first();
  await lead.click(); await lead.dblclick(); await lead.dblclick();
  log('editing?', await p.evaluate(() => !!document.querySelector('[contenteditable=true]')));
  await p.keyboard.press('End'); await p.keyboard.type(' EDITED'); await p.keyboard.press('Escape');
  log('lead text:', (await lead.textContent()).slice(-20));
  // 7. page nav + resize handle
  await p.keyboard.press('PageDown'); await p.keyboard.press('PageDown'); await p.keyboard.press('PageDown');
  log('page', await p.textContent('#fx-pnum'));
  const band = p.locator('#fx-stage .story'); await band.click();
  log('sel p4:', await p.evaluate(() => fxEditor.sel.map(e => e.className)));
  await p.screenshot({ path: '' + require('path').resolve(__dirname, '../../.qa') + '/ed3.png' });
  // 8. save and reopen
  const [d] = await Promise.all([p.waitForEvent('download'), p.keyboard.press('Control+s')]);
  const out = require('path').resolve(__dirname, '../../.qa/_edited_test.html'); await d.saveAs(out);
  const html = fs.readFileSync(out, 'utf8');
  log('saved: fx-root', html.includes('id="fx-root"'), 'pages', (html.match(/class="page/g) || []).length, 'hidden', html.includes('fx-hidden'), 'EDITED', html.includes('EDITED'));
  const p2 = await b.newPage({ viewport: { width: 1440, height: 900 } }); p2.on('pageerror', e => errs.push('p2 ' + e.message));
  await p2.goto('file://' + out); await p2.waitForTimeout(300); log('reopen toolbars', await p2.locator('#fx-top').count(), await p2.textContent('#fx-pnum'));
  // 9. print
  await p2.emulateMedia({ media: 'print' }); await p2.pdf({ path: '' + require('path').resolve(__dirname, '../../.qa') + '/ed_print.pdf', preferCSSPageSize: true, printBackground: true });
  log('errors', errs); await b.close();
})();
