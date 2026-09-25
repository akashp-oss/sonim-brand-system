// Sonim template paste: rebuilds a template copied from the brand template library
// ("Copy for Figma") as native Figma layers with auto layout on every flex stack.
figma.showUI(__html__, { width: 320, height: 280 });

const FONT_FAMILIES = ['Akzidenz-Grotesk Pro', 'Arial', 'Inter'];
let FAMILY = null;
async function loadFonts() {
  if (FAMILY) return FAMILY;
  for (const family of FONT_FAMILIES) {
    try {
      await Promise.all([figma.loadFontAsync({ family, style: 'Regular' }), figma.loadFontAsync({ family, style: 'Bold' })]);
      return (FAMILY = family);
    } catch (e) { /* try the next family */ }
  }
  throw new Error('No usable font (Arial or Inter) is available.');
}

function rgb(hex) {
  const n = parseInt(hex.slice(1), 16);
  return { r: ((n >> 16) & 255) / 255, g: ((n >> 8) & 255) / 255, b: (n & 255) / 255 };
}
const solid = hex => (hex ? [{ type: 'SOLID', color: rgb(hex) }] : []);
function bytes(dataUrl) { return figma.base64Decode(dataUrl.slice(dataUrl.indexOf(',') + 1)); }
const imageCache = new Map();
function imageHash(src) {
  if (!imageCache.has(src)) imageCache.set(src, figma.createImage(bytes(src)).hash);
  return imageCache.get(src);
}

function build(n) {
  let node;
  if (n.type === 'TEXT') {
    node = figma.createText();
    node.fontName = { family: FAMILY, style: 'Regular' };
    node.characters = n.chars || ' ';
    node.fontSize = n.size;
    if (n.lh) node.lineHeight = { value: n.lh, unit: 'PIXELS' };
    if (n.ls) node.letterSpacing = { value: n.ls, unit: 'PIXELS' };
    node.textAlignHorizontal = n.align;
    for (const r of n.runs) {
      if (r.end <= r.start) continue;
      node.setRangeFontName(r.start, r.end, { family: FAMILY, style: r.bold ? 'Bold' : 'Regular' });
      node.setRangeFills(r.start, r.end, solid(r.color || '#000000'));
    }
    if (n.autoWidth) node.textAutoResize = 'WIDTH_AND_HEIGHT';
    else { node.textAutoResize = 'HEIGHT'; node.resize(Math.max(1, n.w), Math.max(1, node.height)); }
  } else if (n.type === 'SVG') {
    node = figma.createNodeFromSvg(n.svg);
    node.resize(Math.max(0.01, n.w), Math.max(0.01, n.h));
    node.fills = [];
  } else if (n.type === 'IMAGE') {
    node = figma.createRectangle();
    node.resize(Math.max(0.01, n.w), Math.max(0.01, n.h));
    node.fills = [n.fit === 'FIT'
      ? { type: 'IMAGE', scaleMode: 'FIT', imageHash: imageHash(n.src) }
      : { type: 'IMAGE', scaleMode: 'CROP', imageHash: imageHash(n.src), imageTransform: n.crop }];
  } else if (n.type === 'SPACER') {
    node = figma.createFrame();
    node.fills = [];
    node.resize(Math.max(0.01, n.w || 1), Math.max(0.01, n.h || 1));
    node.setPluginData('spacer', n.w ? 'h' : 'v');
  } else {
    node = figma.createFrame();
    node.fills = solid(n.fill);
    node.clipsContent = !!n.clip;
    node.resize(Math.max(0.01, n.w), Math.max(0.01, n.h));
    const L = n.layout;
    if (L) {
      node.layoutMode = L.mode;
      node.itemSpacing = L.gap || 0;
      [node.paddingTop, node.paddingRight, node.paddingBottom, node.paddingLeft] = L.pad;
      node.primaryAxisAlignItems = L.primary;
      node.counterAxisAlignItems = L.counter === 'MAX' || L.counter === 'CENTER' ? L.counter : 'MIN';
      if (L.wrap) { node.layoutWrap = 'WRAP'; node.counterAxisSpacing = L.rowGap || 0; }
      node.primaryAxisSizingMode = 'FIXED';
      node.counterAxisSizingMode = 'FIXED';
    }
    for (const c of n.children || []) {
      const child = build(c);
      node.appendChild(child);
      if (L) {
        if (c.abs) { child.layoutPositioning = 'ABSOLUTE'; child.x = c.x; child.y = c.y; }
        else {
          if (c.grow) child.layoutGrow = 1;
          if (c.stretch) child.layoutAlign = 'STRETCH';
          if (c.type === 'SPACER') { if (L.mode === 'VERTICAL') child.resize(1, c.h); else child.resize(c.w, 1); }
        }
      } else { child.x = c.x; child.y = c.y; }
    }
    if (L) node.resize(Math.max(0.01, n.w), Math.max(0.01, n.h));
  }
  node.name = n.name || node.name;
  return node;
}

figma.ui.onmessage = async msg => {
  if (msg.type !== 'build') return;
  try {
    await loadFonts();
    const root = build(msg.data.node);
    const c = figma.viewport.center;
    root.x = Math.round(c.x - root.width / 2); root.y = Math.round(c.y - root.height / 2);
    figma.currentPage.appendChild(root);
    figma.currentPage.selection = [root];
    figma.viewport.scrollAndZoomIntoView([root]);
    figma.ui.postMessage({ ok: true, name: root.name });
    figma.notify('Pasted ' + root.name + (FAMILY !== 'Akzidenz-Grotesk Pro' ? ' (set in ' + FAMILY + ')' : ''));
  } catch (e) {
    figma.ui.postMessage({ ok: false, error: String(e && e.message || e) });
  }
};
