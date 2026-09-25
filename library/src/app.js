/* Library app shell: zoom, guides, edit, save, Figma import view, hover copy tools, nav. */
(function(){
  const IMG = JSON.parse(document.getElementById('img-data').textContent);
  const $ = (s,r=document)=>r.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)];
  const MARG = __MARGINS__;
  const isFigma = ()=>document.body.classList.contains('figma');
  function loadImages(){ $$('.ab img[data-img]').forEach(i=>{ const k=i.dataset.img; if(IMG[k] && !i.dataset.custom) i.src=IMG[k]; }); }
  loadImages();

  /* ---------- zoom ---------- */
  let mode = 'fit';
  function layout(){
    const avail = Math.max(240, $('.canvas').clientWidth - parseFloat(getComputedStyle($('.canvas')).paddingLeft)*2);
    $$('.frame').forEach(f=>{
      const ab=$('.ab',f), wr=$('.ab-wrap',f), w=ab.offsetWidth, h=ab.offsetHeight;
      let s = isFigma() ? 1 : mode==='fit' ? Math.min(1, 560/h, avail/w) : Math.min(+mode, mode==='1' ? 1 : avail/w);
      ab.style.transform = s===1?'':`scale(${s})`;
      wr.style.width = w*s+'px'; wr.style.height = h*s+'px';
      f.classList.toggle('tiny', w*s < 250 || h*s < 70);
    });
  }
  window.addEventListener('resize', layout); layout();
  $$('[data-zoom]').forEach(b=>b.onclick=()=>{ mode=b.dataset.zoom; $$('[data-zoom]').forEach(x=>x.classList.toggle('on',x===b)); layout(); });

  /* ---------- guides ---------- */
  let guides=false;
  function drawGuides(){
    $$('.guide').forEach(g=>g.remove()); if(!guides) return;
    $$('.frame').forEach(f=>{
      const ab=$('.ab',f), fmt=f.dataset.fmt, m=MARG[fmt]; const w=ab.offsetWidth,h=ab.offsetHeight;
      if(m && w>2*m && h>2*m){ const g=document.createElement('div'); g.className='guide margin'; Object.assign(g.style,{left:m+'px',top:m+'px',width:(w-2*m)+'px',height:(h-2*m)+'px'}); ab.appendChild(g); }
      if(fmt==='story'){ [[0,250],[h-340,340]].forEach(([t,hh])=>{ const g=document.createElement('div'); g.className='guide safe'; Object.assign(g.style,{left:0,top:t+'px',width:w+'px',height:hh+'px'}); ab.appendChild(g); }); }
    });
  }
  function setGuides(on){ guides=on; $('#btn-guides').classList.toggle('on',on); drawGuides(); }
  $('#btn-guides').onclick=()=>setGuides(!guides);

  /* ---------- edit text + replace images ---------- */
  let editing=false;
  function setEdit(on, quiet){ editing=on; $('#btn-edit').classList.toggle('on',on); document.body.classList.toggle('editing',on);
    $$('.ab .tx').forEach(t=>{ if(on) t.setAttribute('contenteditable','true'); else t.removeAttribute('contenteditable'); });
    if(!quiet) toast(on?'Click any text to edit it. Double-click an image to replace it.':'Editing off'); }
  $('#btn-edit').onclick=()=>setEdit(!editing);
  const picker=document.createElement('input'); picker.type='file'; picker.accept='image/*'; let target=null;
  picker.onchange=()=>{ const f=picker.files[0]; if(!f||!target) return; const r=new FileReader(); r.onload=()=>{ target.src=r.result; target.dataset.custom='1'; toast('Image replaced'); }; r.readAsDataURL(f); picker.value=''; };
  document.addEventListener('dblclick',e=>{ if(!editing) return; const i=e.target.closest('.ab img'); if(i){ target=i; picker.click(); } });

  /* ---------- Figma import view ---------- */
  function setFigma(on){ document.body.classList.toggle('figma',on); $('#btn-figma').classList.toggle('on',on);
    if(on){ setGuides(false); closeNav(); } layout(); if(!on) toast('Figma import view off'); }
  $('#btn-figma').onclick=()=>setFigma(!isFigma());
  if(/[?&#]figma\b/.test(location.href)) setFigma(true);
  document.addEventListener('keydown',e=>{ if(e.key==='Escape'){ if(isFigma()) setFigma(false); closeNav(); } });

  /* ---------- save a self-contained copy ---------- */
  $('#btn-save').onclick=async()=>{
    const wasEdit=editing, wasGuides=guides; if(editing) setEdit(false,true); if(guides) setGuides(false);
    try{
      const doc=document.documentElement.cloneNode(true);
      doc.querySelectorAll('.ab img[data-img]').forEach(i=>{ if(!i.dataset.custom) i.removeAttribute('src'); });
      doc.querySelectorAll('.frame-tools').forEach(t=>t.remove());
      doc.querySelectorAll('.ab').forEach(a=>a.style.transform=''); doc.querySelector('body').className='';
      const blob=new Blob(['<!doctype html>\n'+doc.outerHTML],{type:'text/html'}); const name='Sonim_Brand_Template_Library_edited.html';
      if(window.showSaveFilePicker){
        try{ const h=await showSaveFilePicker({suggestedName:name,types:[{description:'HTML',accept:{'text/html':['.html']}}]}); const w=await h.createWritable(); await w.write(blob); await w.close(); toast('Saved '+h.name); return; }
        catch(err){ if(err.name==='AbortError') return; }
      }
      download(blob, name); toast('Saved to Downloads');
    } finally { if(wasEdit) setEdit(true,true); if(wasGuides) setGuides(true); }
  };

  /* ---------- hover tools: copy SVG / copy for Figma / download SVG ---------- */
  function download(blob, name){ const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download=name; document.body.appendChild(a); a.click(); a.remove(); setTimeout(()=>URL.revokeObjectURL(a.href), 4000); }
  async function copyText(text){
    try{ await navigator.clipboard.writeText(text); return true; }
    catch(e){ const t=document.createElement('textarea'); t.value=text; t.style.cssText='position:fixed;left:-9999px;top:0'; document.body.appendChild(t); t.select();
      let ok=false; try{ ok=document.execCommand('copy'); }catch(_){} t.remove(); return ok; }
  }
  function prep(){ if(editing) setEdit(false,true); const g=guides; if(g) setGuides(false); return ()=>{ if(g) setGuides(true); }; }
  const ACTIONS = {
    svg: async (ab,f)=>{ const done=prep(); try{ return await copyText(sonimExport.toSVG(ab)) ? 'SVG copied. In Figma press Ctrl/⌘ + V.' : 'Copy blocked by the browser. Use Download SVG.'; } finally{ done(); } },
    figma: async (ab,f)=>{ const done=prep(); try{ return await copyText(sonimExport.toFigma(ab)) ? 'Copied for Figma. Run the Sonim template paste plugin and press Ctrl/⌘ + V.' : 'Copy blocked by the browser.'; } finally{ done(); } },
    download: async (ab,f)=>{ const done=prep(); try{ download(new Blob([sonimExport.toSVG(ab)],{type:'image/svg+xml'}), 'Sonim_'+f.id+'.svg'); return 'SVG downloaded'; } finally{ done(); } },
  };
  $$('.frame').forEach(f=>{
    const tools=document.createElement('div'); tools.className='frame-tools';
    tools.innerHTML='<button class="tool" data-act="svg" title="Copy as SVG: paste into Figma as editable vectors and text">Copy SVG</button>'
      +'<button class="tool" data-act="figma" title="Copy with auto layout: paste in Figma with the Sonim template paste plugin">Copy for Figma</button>'
      +'<button class="tool icon" data-act="download" title="Download SVG" aria-label="Download SVG"><svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M8 2v8M4 7l4 4 4-4M2.5 14h11"/></svg></button>';
    $('.ab-wrap',f).appendChild(tools);
    tools.addEventListener('click',async e=>{ const b=e.target.closest('[data-act]'); if(!b) return; e.stopPropagation();
      b.disabled=true; try{ toast(await ACTIONS[b.dataset.act]($('.ab',f),f)); b.classList.add('done'); setTimeout(()=>b.classList.remove('done'),1400); }
      catch(err){ console.error(err); toast('Export failed: '+err.message); } finally{ b.disabled=false; } });
  });

  /* ---------- brand colour chips: click to copy HEX ---------- */
  $$('[data-hex]').forEach(c=>c.onclick=async()=>{ await copyText(c.dataset.hex); toast(c.dataset.hex+' copied'); });

  /* ---------- nav: highlight + mobile drawer ---------- */
  const secs=$$('.lib-section'); const io=new IntersectionObserver(es=>es.forEach(en=>{ if(en.isIntersecting){ $$('.nav-item').forEach(n=>n.classList.toggle('on',n.dataset.sec===en.target.id.slice(4))); } }),{rootMargin:'-40% 0px -55% 0px'});
  secs.forEach(s=>io.observe(s));
  function closeNav(){ document.body.classList.remove('nav-open'); }
  $('#btn-menu').onclick=()=>document.body.classList.toggle('nav-open');
  $('.scrim').onclick=closeNav; $$('.nav-item').forEach(n=>n.addEventListener('click',closeNav));

  function toast(t){ const el=$('#toast'); el.textContent=t; el.classList.add('show'); clearTimeout(toast.t); toast.t=setTimeout(()=>el.classList.remove('show'),2600); }
  window.lib={layout,setFigma};
})();
