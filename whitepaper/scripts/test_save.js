const { chromium } = require('playwright'); const fs = require('fs');
require('fs').mkdirSync(require('path').resolve(__dirname, '../../.qa'), { recursive: true });
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1440, height: 900 }, acceptDownloads: true });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('file://' + require('path').resolve(__dirname, '../dist/Sonim_EMS_Whitepaper_EDITOR.html') + ''); await p.waitForTimeout(500);
  await p.evaluate(() => { delete window.showSaveFilePicker; window.showSaveFilePicker = undefined; fxEditor.select([fxEditor.pageEl().querySelector('.notch-anchor')]); });
  await p.keyboard.press('Shift+ArrowDown');
  const [d] = await Promise.all([p.waitForEvent('download'), p.click('#fx-save')]);
  fs.mkdirSync('' + require('path').resolve(__dirname, '../../.qa') + '/elsewhere', { recursive: true }); const out = '' + require('path').resolve(__dirname, '../../.qa') + '/elsewhere/' + d.suggestedFilename(); await d.saveAs(out);
  console.log('saved', d.suggestedFilename(), Math.round(fs.statSync(out).size / 1e3) + 'KB');
  const p2 = await b.newPage({ viewport: { width: 1440, height: 900 } }); p2.on('pageerror', e => errs.push('p2 ' + e.message));
  await p2.goto('file://' + out); await p2.waitForTimeout(600);
  console.log(await p2.evaluate(() => ({
    titlePt: parseFloat(getComputedStyle(fxEditor.pageEl().querySelector('.display')).fontSize) * .75,
    imgsOk: [...document.querySelectorAll('#fx-stage img')].filter(i => i.naturalWidth > 0).length + '/' + document.querySelectorAll('#fx-stage img').length,
    moved: fxEditor.pageEl().querySelector('.notch-anchor').style.marginTop, flow: document.querySelector('#fx-flow').textContent,
    editors: document.querySelectorAll('#fx-top').length })));
  await p2.screenshot({ path: '' + require('path').resolve(__dirname, '../../.qa') + '/reopen.png' });
  // save again from the reopened copy -> name should stay _edited
  await p2.evaluate(() => { window.showSaveFilePicker = undefined; });
  const [d2] = await Promise.all([p2.waitForEvent('download'), p2.click('#fx-save')]); console.log('resave name', d2.suggestedFilename());
  await p2.emulateMedia({ media: 'print' }); await p2.pdf({ path: '' + require('path').resolve(__dirname, '../../.qa') + '/reopen.pdf', preferCSSPageSize: true, printBackground: true });
  console.log('errors', errs); await b.close();
})();
