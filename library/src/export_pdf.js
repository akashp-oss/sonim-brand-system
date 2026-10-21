/* Print library artboards to a PDF, one artboard per page at its own size (US Letter artboards = Letter pages).
   Usage: node library/src/export_pdf.js out.pdf id1,id2,...   (fonts and images come from the built library) */
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [out, list] = process.argv.slice(2);
  const ids = list.split(',');
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file://' + path.resolve(__dirname, '../dist/Sonim_Brand_Template_Library.html') + '?figma'); await p.waitForTimeout(800);
  const size = await p.evaluate(ids => {
    const abs = ids.map(id => { const a = document.querySelector(`#${id} .ab`); if (!a) throw new Error('no artboard ' + id); return a; });
    const { offsetWidth: w, offsetHeight: h } = abs[0];
    const style = [...document.querySelectorAll('style')].map(s => s.outerHTML).join('');
    const pages = abs.map(a => { const c = a.cloneNode(true); c.style.transform = ''; c.querySelectorAll('.guide,.frame-tools').forEach(x => x.remove());
      return `<div class="pdf-page">${c.outerHTML}</div>`; }).join('');
    document.documentElement.innerHTML = `<head>${style}<style>@page{size:${w}px ${h}px;margin:0}html,body{margin:0;padding:0;background:#fff}
      .pdf-page{width:${w}px;height:${h}px;overflow:hidden;break-after:page;page-break-after:always}.pdf-page:last-child{break-after:auto}</style></head><body>${pages}</body>`;
    return { w, h };
  }, ids);
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({ path: out, width: size.w + 'px', height: size.h + 'px', printBackground: true, preferCSSPageSize: true });
  console.log(out, ids.length, 'pages');
  await b.close();
})();
