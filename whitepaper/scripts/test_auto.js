const { chromium } = require('playwright');
require('fs').mkdirSync(require('path').resolve(__dirname, '../../.qa'), { recursive: true });
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1440, height: 900 }, acceptDownloads: true });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('file://' + require('path').resolve(__dirname, '../dist/Sonim_EMS_Whitepaper_EDITOR.html') + ''); await p.waitForTimeout(400);
  const top = sel => p.evaluate(s => { const pg = fxEditor.pageEl(); const e = pg.querySelector(s); return Math.round((e.getBoundingClientRect().top - pg.getBoundingClientRect().top) / fxEditor.zoom * 0.75 * 10) / 10; }, sel);
  const log = console.log;
  log('flow p1', await p.evaluate(() => fxEditor.flow), await p.textContent('#fx-flow'));
  // P1: move headline block down 20pt with keyboard -> body grid should follow
  const g0 = await top('.grid'), n0 = await top('.notch-anchor'), rh0 = await top('.run-head');
  await p.evaluate(() => fxEditor.select([fxEditor.pageEl().querySelector('.notch-anchor')]));
  await p.keyboard.press('Shift+ArrowDown'); await p.keyboard.press('Shift+ArrowDown');
  log('auto: headline', n0, '->', await top('.notch-anchor'), '| grid', g0, '->', await top('.grid'), '| run-head', rh0, '->', await top('.run-head'), '|', await p.textContent('#fx-flow'));
  // lock the grid and move headline up 10 -> grid stays
  await p.evaluate(() => { fxEditor.select([fxEditor.pageEl().querySelector('.grid')]); fxEditor.toggleLock(); fxEditor.select([fxEditor.pageEl().querySelector('.notch-anchor')]); });
  const g1 = await top('.grid'); await p.keyboard.press('Shift+ArrowUp');
  log('locked grid stays:', g1, '->', await top('.grid'), '| headline ->', await top('.notch-anchor'));
  // canvas click on locked grid should not select it
  await p.evaluate(() => fxEditor.select([]));
  const gb = await p.locator('#fx-stage .page:not(.fx-hidden) .grid .h2').first().boundingBox(); await p.mouse.click(gb.x + 5, gb.y + 5);
  log('click locked ->', await p.evaluate(() => fxEditor.sel.length));
  // auto off: move headline -> grid stays even when unlocked
  await p.evaluate(() => { fxEditor.select([fxEditor.pageEl().querySelector('.grid')]); fxEditor.toggleLock(); fxEditor.setAuto(false); fxEditor.select([fxEditor.pageEl().querySelector('.notch-anchor')]); });
  const g2 = await top('.grid'); await p.keyboard.press('Shift+ArrowDown');
  log('auto off: grid', g2, '->', await top('.grid'));
  await p.evaluate(() => fxEditor.setAuto(true));
  // P4: drag stack row 1 down 60px, story must stay, overflow flagged
  await p.evaluate(() => fxEditor.showPage(3));
  const s0 = await top('.story'), r4 = await p.evaluate(() => { const pg = fxEditor.pageEl(); const r = pg.querySelectorAll('.stack-row')[3]; return Math.round((r.getBoundingClientRect().top - pg.getBoundingClientRect().top) / fxEditor.zoom * .75); });
  const row = p.locator('#fx-stage .page:not(.fx-hidden) .stack-row .num').first(); const bb = await row.boundingBox();
  await p.mouse.move(bb.x + 3, bb.y + 3); await p.mouse.down(); await p.mouse.move(bb.x + 3, bb.y + 60, { steps: 6 }); await p.mouse.up();
  const r4b = await p.evaluate(() => { const pg = fxEditor.pageEl(); const r = pg.querySelectorAll('.stack-row')[3]; return Math.round((r.getBoundingClientRect().top - pg.getBoundingClientRect().top) / fxEditor.zoom * .75); });
  log('p4 sel', await p.evaluate(() => fxEditor.sel.map(e => e.className)), 'row4', r4, '->', r4b, '| story', s0, '->', await top('.story'), '|', await p.textContent('#fx-flow'));
  await p.screenshot({ path: '' + require('path').resolve(__dirname, '../../.qa') + '/auto4.png' });
  // gap control on use-case grid p2
  await p.evaluate(() => { fxEditor.showPage(1); fxEditor.select([fxEditor.pageEl().querySelector('.usecases')]); });
  const hasGap = await p.locator('#fx-props input[data-k="gx"]').count();
  await p.fill('#fx-props input[data-k="gx"]', '24'); await p.press('#fx-props input[data-k="gx"]', 'Enter');
  log('gap field', hasGap, 'columnGap', await p.evaluate(() => fxEditor.pageEl().querySelector('.usecases').style.columnGap));
  await p.keyboard.press('Control+z'); log('undo gap', await p.evaluate(() => fxEditor.pageEl().querySelector('.usecases').style.columnGap));
  log('errors', errs); await b.close();
})();
