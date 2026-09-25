const fs=require('fs'),path=require('path');const {chromium}=require('playwright');
const BRAND=path.resolve(__dirname,'../../brand');
const logo=fs.readFileSync(path.join(BRAND,'logo/sonim-logo.svg'),'utf8');
const icons=JSON.parse(fs.readFileSync(path.join(BRAND,'icons/icons.json'),'utf8'));
(async()=>{const [src,out,png,sel='.page']=process.argv.slice(2);
 let html=fs.readFileSync(src,'utf8').replaceAll('{{LOGO}}',logo).replace(/\{\{icon:([a-z-]+)\}\}/g,(m,n)=>icons[n]||m);
 const tmp=src.replace('.html','.built.html');fs.writeFileSync(tmp,html);
 const b=await chromium.launch();const p=await b.newPage();await p.goto('file://'+path.resolve(tmp),{waitUntil:'networkidle'});
 if(out) await p.pdf({path:out,preferCSSPageSize:true,printBackground:true});
 if(png){await p.emulateMedia({media:'print'});const els=await p.$$(sel);for(let i=0;i<els.length;i++){await els[i].screenshot({path:`${png}-${i+1}.png`});}}
 // overflow check: any element whose bottom exceeds its page's content bottom
 const ov=await p.evaluate(()=>[...document.querySelectorAll('.page')].map((pg,i)=>{const r=pg.getBoundingClientRect();let max=0;pg.querySelectorAll('p,li,div,h1,h2,span').forEach(e=>{if(e.closest('.page-logo,.page-note,.fullbleed'))return;const b=e.getBoundingClientRect().bottom-r.top;if(b>max)max=b});return [i+1,Math.round(max*0.75)]}));
 console.log('content bottom (pt) per page:',JSON.stringify(ov));
 await b.close();})();
