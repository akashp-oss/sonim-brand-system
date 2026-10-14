# Sonim brand template library generator -> one self-contained HTML file.
import base64, json, re, html as H
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]          # repo root

RED, BLACK, GRAY, WHITE = '#CF102D', '#000000', '#E5ECEE', '#FFFFFF'
LOGO_PATHS = re.sub(r'<metadata>.*?</metadata>', '', open(ROOT / 'brand/logo/sonim-logo.svg').read(), flags=re.S).split('>', 1)[1].rsplit('</svg>', 1)[0].strip()
# Official Sonim NEXA lockup ("sonim® / A NEXA Company"), trimmed to its artwork bounds.
# Used for every logo >= NEXA_MIN_W wide; below that the wordmark alone stays legible.
NEXA_SVG = open(ROOT / 'brand/logo/sonim-nexa-lockup.svg').read()   # built by brand/import_client_assets.py
NEXA_PATHS = NEXA_SVG.split('>', 1)[1].rsplit('</svg>', 1)[0]
NEXA_VB = tuple(map(float, re.search(r'viewBox="([^"]+)"', NEXA_SVG).group(1).split()))
NEXA_MIN_W = 100
NEXA_RATIO = NEXA_VB[3] / NEXA_VB[2]

# Official Rugged Container sizes (Rugged Template/, inches incl. both notches): height / width ratios.
_RT = ROOT / 'Rugged Template/PNG versions/Gray'
RUGGED_SIZES = sorted({tuple(map(float, re.search(r'(\d+(?:\.\d+)?) x (\d+(?:\.\d+)?)', f.name).groups())) for f in _RT.glob('*.png')}) if _RT.exists() else []
RUGGED_RATIOS = sorted({round(h / w, 4) for w, h in RUGGED_SIZES}) or [1.04, 1.6]

# Icons: brand/icons/all.json (built by brand/import_client_assets.py) = official Sonim icons, old keys
# aliased to official art, and the remaining icons restyled to the official look. Same set as the white paper.
ICONS = json.load(open(ROOT / 'brand/icons/all.json'))
SONIM_ICONS = json.load(open(ROOT / 'brand/icons/sonim.json'))
ICONS['check'] = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#CF102D" stroke-width="3" stroke-linecap="square"><path d="M4 12.5l5 5L20 6.5"/></svg>'
ICONS['arrow'] = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M3 12h17M14 6l6 6-6 6"/></svg>'

# Akzidenz-Grotesk Pro has no arrow glyph: draw it, sized to the text and in its colour
ARROW = ('<svg data-name="Arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" '
         'style="display:inline-block;width:.9em;height:.9em;vertical-align:-.08em;overflow:visible"><path d="M3 12h17M14 6l6 6-6 6"/></svg>')

def esc(s): return H.escape(s, quote=True)
def st(d): return ';'.join(f'{k}:{v}' for k, v in d.items() if v is not None)
def px(v): return f'{v}px' if isinstance(v, (int, float)) else v

def box(name, l=None, t=None, w=None, h=None, r=None, b=None, cls='', style=None, inner='', tag='div'):
    s = {'left': px(l) if l is not None else None, 'top': px(t) if t is not None else None, 'right': px(r) if r is not None else None,
         'bottom': px(b) if b is not None else None, 'width': px(w) if w is not None else None, 'height': px(h) if h is not None else None}
    s.update(style or {})
    positioned = any(v is not None for v in (l, t, r, b))
    return f'<{tag} class="{"abs " if positioned else ""}{cls}" data-name="{esc(name)}" style="{st(s)}">{inner}</{tag}>'

def fill(name, color, style=None, **k):
    sty = {'background': color}; sty.update(style or {})
    return box(name, cls='shape', style=sty, **k)

MIN_TEXT = 12

def text(name, content, cls, color=None, size=None, extra=None, tag='div'):
    """content supports **red** emphasis marker and \n line breaks"""
    parts = []
    for i, seg in enumerate(content.replace('\u2011', '-').split('**')):
        seg = esc(seg).replace('\n', '<br>').replace('→', ARROW)
        parts.append(f'<span class="em" data-name="Emphasis">{seg}</span>' if i % 2 else seg)
    # type floor for every template: nothing under MIN_TEXT px, and small text (< 16 px) is never bold
    if size and size < MIN_TEXT:
        size = MIN_TEXT
    s = {'color': color, 'font-size': px(size) if size else None}
    s.update(extra or {})
    if size and size < 16:
        s['font-weight'] = '400'
    return f'<{tag} class="tx {cls}" data-name="{esc(name)}" style="{st(s)}">{"".join(parts)}</{tag}>'

def stack(name, items, l=None, t=None, w=None, gap=0, r=None, b=None, style=None, cls=''):
    s = {'gap': px(gap)}; s.update(style or {})
    return box(name, l=l, t=t, w=w, r=r, b=b, cls='stack ' + cls, style=s, inner=''.join(items))

def photo(name, key, l=0, t=0, w=100, h=100, pos='50% 50%', r=None, b=None):
    return (f'<img class="abs photo" data-name="{esc(name)}" data-img="{key}" alt="{esc(name)}" '
            f'style="{st({"left": px(l) if l is not None else None, "top": px(t) if t is not None else None, "right": px(r) if r is not None else None, "bottom": px(b) if b is not None else None, "width": px(w), "height": px(h), "object-position": pos})}">')

def cutout(name, key, l, t, w, h, pos='50% 50%'):
    return (f'<img class="abs cutout" data-name="{esc(name)}" data-img="{key}" alt="{esc(name)}" '
            f'style="{st({"left": px(l), "top": px(t), "width": px(w), "height": px(h), "object-position": pos})}">')

def notch_svg(x, color, direction='right', name='Notch'):
    """Brand notch: 18:1, ends angled 26.5deg (X/2 along the length per X of depth, as in the official containers). direction = side the angled edge faces."""
    pts = '0,0 1,0.5 1,17.5 0,18' if direction == 'right' else '1,0 0,0.5 0,17.5 1,18'
    return (f'<svg class="notch-svg" data-name="{name}" width="{x}" height="{18*x}" viewBox="0 0 1 18" preserveAspectRatio="none">'
            f'<polygon points="{pts}" fill="{color}"/></svg>')

def notch_h_svg(x, color, name='Notch (rotated)'):
    """Notch rotated 90deg: protrudes upward from a panel's top edge."""
    return (f'<svg class="notch-svg" data-name="{name}" width="{18*x}" height="{x}" viewBox="0 0 18 1" preserveAspectRatio="none">'
            f'<polygon points="0,1 0.5,0 17.5,0 18,1" fill="{color}"/></svg>')

def page_notch(x, top, color=RED, left=0):
    return box('Notch', l=left, t=top, w=x, h=18*x, cls='graphic', inner=notch_svg(x, color))

def logo(w, color, l=None, t=None, r=None, b=None, name='Sonim logo', lockup=None):
    """NEXA lockup when w >= NEXA_MIN_W (or lockup=True); the wordmark alone for small sizes."""
    if lockup if lockup is not None else w >= NEXA_MIN_W:
        h = round(w * NEXA_RATIO, 1)
        svg = f'<svg data-name="Logo mark (NEXA lockup)" width="{w}" height="{h}" viewBox="{" ".join(map(str, NEXA_VB))}" fill="{color}">{NEXA_PATHS}</svg>'
    else:
        h = round(w * 52 / 152, 1)
        svg = f'<svg data-name="Logo mark" width="{w}" height="{h}" viewBox="0 0 152 52" fill="{color}">{LOGO_PATHS}</svg>'
    return box(name, l=l, t=t, r=r, b=b, w=w, h=h, cls='logo', inner=svg)

def logo_vertical(h, color, l, t, name='Sonim logo (vertical)'):
    x0, y0, vw, vh = NEXA_VB
    w = round(h * NEXA_RATIO, 1)
    svg = (f'<svg data-name="Logo mark (NEXA lockup)" width="{w}" height="{h}" viewBox="0 0 {vh} {vw}" fill="{color}">'
           f'<g transform="translate({-y0} {vw + x0}) rotate(-90)">{NEXA_PATHS}</g></svg>')
    return box(name, l=l, t=t, w=w, h=h, cls='logo', inner=svg)

def rugged_height(w, h, x):
    """Snap h so the container (width incl. both notches) matches the nearest official size ratio."""
    overall = w + 2 * x
    return round(overall * min(RUGGED_RATIOS, key=lambda r: abs(r - h / overall)))

def rugged(name, l, t, w, h, x, color, content, pad=None, content_style=None, snap=True):
    """Rugged Container: fill + right notch 2X from top + left notch 2X from bottom. Live area inset 2X.
    Height snaps to the official container proportions (Rugged Template/) unless snap=False."""
    if snap:
        h = rugged_height(w, h, x)
    nh = min(18 * x, h / 2 - 2 * x)
    pad = 2 * x if pad is None else pad
    right = box('Right notch', l=w, t=2 * x, w=x, h=nh, cls='graphic', inner=notch_svg(x, color, 'right').replace(f'height="{18*x}"', f'height="{nh}"'))
    left = box('Left notch', l=-x, t=h - 2 * x - nh, w=x, h=nh, cls='graphic', inner=notch_svg(x, color, 'left').replace(f'height="{18*x}"', f'height="{nh}"'))
    cs = {'padding': px(pad)}; cs.update(content_style or {})
    inner = fill('Container fill', color, l=0, t=0, w=w, h=h) + right + left + box('Content', l=0, t=0, w=w, h=h, cls='stack', style=cs, inner=content)
    return box(name, l=l, t=t, w=w, h=h, cls='group', inner=inner)

def xnotch(name, l, t, w, h, x, color, inner='', notch_top=None):
    """Expanded Notch: panel from an edge with the notch protruding from its right edge (2X from top)."""
    nt = 2 * x if notch_top is None else notch_top
    parts = fill('Panel fill', color, l=0, t=0, w=w, h=h) + box('Notch', l=w, t=nt, w=x, h=18 * x, cls='graphic', inner=notch_svg(x, color))
    return box(name, l=l, t=t, w=w, h=h, cls='group', inner=parts + inner)

def xnotch_h(name, l, t, w, h, x, color, inner='', notch_left=None):
    """Expanded Notch rotated 90deg for narrow formats: panel along the bottom, notch protrudes upward."""
    nl = 2 * x if notch_left is None else notch_left
    parts = fill('Panel fill', color, l=0, t=0, w=w, h=h) + box('Notch', l=nl, t=-x, w=18 * x, h=x, cls='graphic', inner=notch_h_svg(x, color))
    return box(name, l=l, t=t, w=w, h=h, cls='group', inner=parts + inner)

def icon(key, size, name=None):
    svg = ICONS[key].replace('<svg ', f'<svg data-name="{esc(name or key)} icon" width="{size}" height="{size}" ', 1)
    return f'<div class="icon" data-name="{esc(name or key)}" style="width:{size}px;height:{size}px">{svg}</div>'

def icon_item(key, title, detail, size, tsize, dsize, gap, color=BLACK, w=None):
    inner = icon(key, size, title) + f'<div class="stack" data-name="Text" style="gap:{round(tsize*0.15)}px">' + \
        text('Title', title, 'h3', color, tsize) + (text('Detail', detail, 'body', color, dsize) if detail else '') + '</div>'
    return f'<div class="row" data-name="{esc(title)}" style="gap:{gap}px;align-items:flex-start;{("width:"+px(w)) if w else ""}">{inner}</div>'

def artboard(aid, name, w, h, bg, inner, use, fmt):
    return (f'<figure class="frame" id="{aid}" data-fmt="{fmt}">'
            f'<figcaption class="frame-meta"><b>{esc(name)}</b><span>{w} × {h} px{"" if use.replace(" ", "") == f"{w}×{h}" else " · " + esc(use)}</span></figcaption>'
            f'<div class="ab-wrap" style="width:{w}px;height:{h}px"><div class="ab" data-name="{esc(name)} · {w}×{h}" style="width:{w}px;height:{h}px;background:{bg}">'
            f'{inner}</div></div></figure>')

SECTIONS = []
def section(sid, title, intro, frames):
    SECTIONS.append((sid, title, intro, frames))
