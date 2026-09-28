"""Import the official Sonim iconography from Icons/ into brand/icons/sonim/ + sonim.json.

- class-based <style> rules are inlined as fill attributes (class names collide once many icons
  sit inline on one page)
- print colours are normalised to the brand hex values (#231F20 & co. -> #000000, #CF202F/#E50019 -> #CF102D)
- XML declarations, comments, ids and fixed width/height are stripped; viewBox is kept
- dated duplicates (…_2024-10-04-…) are skipped; the undated file is the master

Run: python3 brand/icons/import_sonim_icons.py
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
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
