"""Import the client's official assets into the formats the builds use. Run after changing Icons/ or Logo/:
    python3 brand/import_client_assets.py

Outputs
  brand/icons/sonim/*.svg, brand/icons/sonim.json   official Sonim icons, cleaned (details below)
  brand/icons/all.json                             THE icon set used everywhere (library + white paper):
      official icons + old keys aliased to official art + the remaining Tabler-based icons restyled
      to the official look (125 grid, same padding, thin 1.67-unit line, square ends, one red detail)
  brand/logo/sonim-nexa-lockup.svg                 official NEXA lockup trimmed to its artwork, single
      colour (fill="currentColor", the NEXA line no longer hard-coded black)

Icon cleaning

- class-based <style> rules are inlined as fill attributes (class names collide once many icons
  sit inline on one page)
- print colours are normalised to the brand hex values (#231F20 & co. -> #000000, #CF202F/#E50019 -> #CF102D)
- XML declarations, comments, ids and fixed width/height are stripped; viewBox is kept
- dated duplicates (…_2024-10-04-…) are skipped; the undated file is the master

"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC, OUT = ROOT / 'Icons', ROOT / 'brand/icons/sonim'
COLOURS = {'#231f20': '#000000', '#241f21': '#000000', '#1a1818': '#000000', '#000': '#000000', '#000000': '#000000',
           '#cf202f': '#CF102D', '#ce202f': '#CF102D', '#cf102d': '#CF102D', '#e50019': '#CF102D', '#fff': '#FFFFFF', '#ffffff': '#FFFFFF'}

def key_for(name):
    k = re.sub(r'^Sonim_Iconography_|^Sonim_|-copy$|-icon-outline$|^icon-', '', name)
    k = k.replace('RPSGeneral', 'rps-general').replace('RPS-', 'rps-').replace('_', '-')
    k = re.sub(r'(?<=[a-z])(?=[A-Z])', '-', k).lower()
    return {'3yr-keyline-cmyk-2c': 'warranty-3yr', 'warranty': 'warranty-2yr', 'xp5plus-turn-to-talk': 'turn-to-talk'}.get(k, k)

def clean(svg):
    svg = re.sub(r'<\?xml[^>]*>|<!--.*?-->', '', svg, flags=re.S)
    styles = {}
    for block in re.findall(r'<style[^>]*>(.*?)</style>', svg, flags=re.S):
        for sels, body in re.findall(r'([^{}]+)\{([^}]*)\}', block):
            for sel in sels.split(','):
                styles.setdefault(sel.strip().lstrip('.'), []).append(body.strip())
    svg = re.sub(r'<defs>\s*<style[^>]*>.*?</style>\s*</defs>|<style[^>]*>.*?</style>', '', svg, flags=re.S)

    def inline(m):
        decl = ';'.join(d for c in m.group(1).split() for d in styles.get(c, []))
        fill = re.search(r'fill:\s*([^;]+)', decl)
        return f'fill="{fill.group(1).strip()}"' if fill else ''
    svg = re.sub(r'class="([^"]*)"', inline, svg)
    svg = re.sub(r'\s(id|data-name)="[^"]*"', '', svg)
    svg = re.sub(r'<path[^>]*stroke="#707070"[^>]*/?>(</path>)?', '', svg)   # Illustrator artboard frame
    m = re.search(r'<svg[^>]*>', svg); tag = m.group(0)
    vb = re.search(r'viewBox="([^"]+)"', tag)
    if not vb:
        w, h = (re.search(fr'{a}="([\d.]+)', tag) for a in ('width', 'height'))
        vb_val = f'0 0 {w.group(1)} {h.group(1)}'
    else:
        vb_val = vb.group(1)
    svg = svg.replace(tag, f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb_val}" fill="none">')
    svg = re.sub(r'(fill|stroke)="(#[0-9a-fA-F]{3,6})"', lambda m: f'{m.group(1)}="{COLOURS.get(m.group(2).lower(), m.group(2))}"', svg)
    # paths without a fill inherit fill="none" from the root: Illustrator's default is black
    svg = re.sub(r'<(path|rect|circle|ellipse|polygon|polyline)(?![^>]*\sfill=)', r'<\1 fill="#000000"', svg)
    return re.sub(r'>\s+<', '><', svg).strip()

OUT.mkdir(parents=True, exist_ok=True)
icons = {}
for f in sorted(SRC.glob('*.svg')):
    if re.search(r'_\d{4}-\d{2}-\d{2}-', f.stem):
        continue
    k = key_for(f.stem)
    icons[k] = clean(f.read_text(encoding='utf-8'))
    (OUT / f'{k}.svg').write_text(icons[k] + '\n')
json.dump(icons, open(OUT.parent / 'sonim.json', 'w'), indent=0)
off = sorted({c for s in icons.values() for c in re.findall(r'(?:fill|stroke)="(#[0-9A-Fa-f]{3,6})"', s)} - {'#000000', '#CF102D', '#FFFFFF'})
print(len(icons), 'icons:', ', '.join(icons), '\noff-palette colours left:', off or 'none')

# ---------------------------------------------------------------- one merged icon set
ALIAS = {'voice': 'rps-audio', 'data': 'data-transfer', 'ptt': 'custom-side-button', 'glove': 'rps-glove',
         'battery': 'battery-general', 'rugged': 'rps-general', 'signal': 'tower', 'coverage': 'tower',
         'software': 'sonim-ware'}

def restyle(svg):
    """Tabler 24-unit icon -> official look: 125 grid, glyph in the same 12.5-112.5 box, 1.67 line, square ends."""
    inner = svg.split('>', 1)[1].rsplit('</svg>', 1)[0]
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 125 125" fill="none">'
            '<g transform="translate(12.5 12.5) scale(4.16667)" stroke="#000000" stroke-width="0.4" '
            f'stroke-linecap="square" stroke-linejoin="miter">{inner}</g></svg>')

tabler = json.load(open(ROOT / 'brand/icons/icons.json'))
merged = dict(icons)
for k, svg in tabler.items():
    merged[k] = icons[ALIAS[k]] if k in ALIAS else restyle(svg)
json.dump(merged, open(ROOT / 'brand/icons/all.json', 'w'), indent=0)
print(len(merged), 'icons in all.json;', 'restyled:', ', '.join(k for k in tabler if k not in ALIAS))

# ---------------------------------------------------------------- NEXA lockup, trimmed + single colour
LOCKUP_VB = '180 222.18 1434.16 620.84'   # artwork bounds of Logo/Sonim_logo_solid_black_1C_NEXA.svg
src = (ROOT / 'Logo/Sonim_logo_solid_black_1C_NEXA.svg').read_text(encoding='utf-8')
paths = re.sub(r'<\?xml[^>]*>|<!--.*?-->', '', src, flags=re.S).split('>', 1)[1].rsplit('</svg>', 1)[0]
paths = re.sub(r'\s(fill|stroke)="#[0-9a-fA-F]{3,6}"', '', paths)
paths = re.sub(r'>\s+<', '><', paths).strip()
(ROOT / 'brand/logo/sonim-nexa-lockup.svg').write_text(
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{LOCKUP_VB}" fill="currentColor" role="img" aria-label="Sonim, a NEXA company">{paths}</svg>\n')
print('wrote brand/logo/sonim-nexa-lockup.svg')
