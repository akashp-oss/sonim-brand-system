from gen import *
from gen import text as _text
import json, re

# Shared white paper design system (Inova healthcare paper, EMS paper): type scale, spacing tokens and
# auto-layout components. Nothing smaller than 12 px; text under 16 px is never bold (gen.text enforces it).
# Every page is one flex column (header, content, footer) of nested stacks and rows, so the HTML to Figma
# import turns each group into auto layout. Only decoration (notches) is absolute.
X, M, W, H = 12, 60, 816, 1056
CFG = {'doc': '', 'name': 'White paper', 'note': 'Sonim, a NEXA company · sonimtech.com'}

# Original EMS icon set (brand/icons/icons.json), as used in the client's EMS white paper layout
EMS_ICONS = {k: re.sub(r'<metadata>.*?</metadata>', '', v, flags=re.S).replace(' xmlns:c2pa="http://c2pa.org/manifest"', '')
             for k, v in json.load(open(ROOT / 'brand/icons/icons.json')).items()}
def ems_icon(key, size, name=None):
    svg = EMS_ICONS[key].replace('<svg ', f'<svg data-name="{esc(name or key)} icon" width="{size}" height="{size}" ', 1)
    return f'<div class="icon" data-name="{esc(name or key)}" style="width:{size}px;height:{size}px;flex:none">{svg}</div>'

def refs(html):
    """[[n]] -> footnote reference (superscript, Sonim Red)."""
    return re.sub(r'\[\[([0-9]+)\]\]', r'<sup class="ref" data-name="Reference" style="color:#CF102D;font-size:.68em;line-height:0;vertical-align:.5em;margin-left:1px">\1</sup>', html)

# ---------------------------------------------------------------- design tokens
#        role       class    size weight line-height letter-spacing
TYPE = {'display': ('display', 56, 700, 1.04, '-0.03em'),
        'title':   ('h1',    40, 700, 1.12, '-0.02em'),
        'stat':    ('stat',  44, 700, 1.0,  '-0.03em'),
        'h1':      ('h1',    32, 700, 1.15, '-0.015em'),
        'h2':      ('h2',    22, 700, 1.25, '-0.01em'),
        'h3':      ('h3',    16, 700, 1.35, '0'),
        'quote':   ('quote', 20, 700, 1.3,  '-0.005em'),
        'lead':    ('lead',  17, 400, 1.5,  '0'),
        'body':    ('body',  14, 400, 1.6,  '0'),
        'label':   ('label', 12, 400, 1.3,  '0.04em'),
        'caption': ('small', 12, 400, 1.4,  '0.01em')}
S = {'none': 0, 'xs': 4, 'sm': 8, 'md': 12, 'lg': 16, 'xl': 24, 'xxl': 32, 'xxxl': 48}

def T(name, content, role, color=BLACK, **extra):
    cls, size, weight, lh, ls = CFG.get('type', TYPE)[role]
    e = {'font-weight': str(weight), 'line-height': str(lh), 'letter-spacing': ls}
    e.update({k.replace('_', '-'): v for k, v in extra.items()})
    return refs(_text(name, content, cls, color, size, e))

def col(name, items, gap='md', **style):
    """Vertical auto layout."""
    s = {'gap': f'{S[gap]}px'}; s.update({k.replace('_', '-'): v for k, v in style.items()})
    return f'<div class="stack" data-name="{esc(name)}" style="{st(s)}">{"".join(items)}</div>'

def row(name, items, gap='xl', **style):
    """Horizontal auto layout; children share the width equally unless they set their own."""
    s = {'gap': f'{S[gap]}px', 'align-items': 'flex-start'}; s.update({k.replace('_', '-'): v for k, v in style.items()})
    return f'<div class="row" data-name="{esc(name)}" style="{st(s)}">{"".join(items)}</div>'

def flex1(name, items, gap='md', **style):
    return col(name, items, gap, flex='1 1 0', min_width='0', **style)

# ---------------------------------------------------------------- components
def header(folio, color=BLACK, doc=None):
    return row('Running header', [T('Document title', doc or CFG['doc'], 'caption', color), T('Folio', f'/ {folio:02d}', 'caption', color)],
               gap='lg', justify_content='flex-end')

def footer(note='Sonim, a NEXA company · sonimtech.com', color=BLACK):
    return row('Footer', [logo(84, color, lockup=True), T('Footnote', note, 'caption', color, text_align='right')],
               gap='xl', justify_content='space-between', align_items='flex-end', margin_top='auto')

def notch(color=RED):
    """Page-edge notch beside a headline (decoration, absolute inside the headline block)."""
    return box('Notch', l=-M, t=2, w=X, h=18 * X, cls='graphic', inner=notch_svg(X, color))

def headline(label, title, role='h1', color=BLACK, label_color=RED, notch_color=RED, em=None):
    extra = {'--em': em} if em else {}
    return col('Headline block', [notch(notch_color), T('Label', label, 'label', label_color), T('Headline', title, role, color, **extra)],
               gap='sm', position='relative')

def section(label, title, items, gap='lg'):
    head = [T('Label', label, 'label', RED)] if label else []
    return col('Section', [col('Section heading', head + [T('Heading', title, 'h2')], gap='sm')] + items, gap=gap)

def body(t, name='Body', color=BLACK): return T(name, t, 'body', color)
def lead(t, name='Lead', color=BLACK): return T(name, t, 'lead', color)
def rule(): return fill('Divider', GRAY, style={'height': '1px', 'flex': 'none'})

def bullets(items, color=BLACK, role='body'):
    _, size, _, lh, _ = CFG.get('type', TYPE)[role]
    bar_top = round((size * lh - 12) / 2)
    return col('List', [row('Item', [fill('Bar', RED, style={'width': '4px', 'height': '12px', 'flex': 'none', 'margin-top': f'{bar_top}px'}),
                                     T('Item text', i, role, color, flex='1 1 0')], gap='md') for i in items], gap='sm')

def tiles(items, size=56, weights=None, pad='xl'):
    """Sonim Gray tiles in a row: icon, title, optional detail. Equal heights; equal widths unless weighted."""
    weights = weights or [1] * len(items)
    return row('Icon tiles', [col((t or d)[:40], [icon(k, size, (t or d)[:40])] + ([T('Title', t, 'h3')] if t else []) + ([body(d, 'Detail')] if d else []),
                                  gap='md', flex=f'{wt} 1 0', min_width='0', background=GRAY, padding=f'{S[pad]}px', align_self='stretch')
                               for (k, t, d), wt in zip(items, weights)], gap='md', align_items='stretch')

def band(name, items, gap='lg', **style):
    return col(name, items, gap, background=RED, padding=f'{S["xl"]}px {S["xl"]}px', **style)

def rugged_box(name, w, h, items, color=GRAY):
    """Rugged Container as auto layout: fixed official proportion, content in a padded stack, notches as decoration."""
    h = rugged_height(w, h, X)
    nh = min(18 * X, h / 2 - 2 * X)
    notches = (box('Right notch', l=w, t=2 * X, w=X, h=nh, cls='graphic', inner=notch_svg(X, color, 'right').replace(f'height="{18 * X}"', f'height="{nh}"'))
               + box('Left notch', l=-X, t=h - 2 * X - nh, w=X, h=nh, cls='graphic', inner=notch_svg(X, color, 'left').replace(f'height="{18 * X}"', f'height="{nh}"')))
    return col(name, [notches] + items, gap='lg', position='relative', background=color, padding=f'{S["xl"]}px',
               width=f'{w}px', height=f'{h}px', flex='none', box_sizing='border-box')

def page(F, aid, name, use, content, folio, bleed='', bg=WHITE, show_header=True, gap='xxl', note=None, tail=None):
    """One page = auto-layout column: optional full-bleed top, then a padded column with header, content, footer.
    tail = a full-bleed block at the bottom that carries its own footer (e.g. a red closing band)."""
    foot = [] if tail else [footer(note or CFG['note'])]
    inner = col('Page content', ([header(folio)] if show_header else [])
                + [col('Content', content, gap, flex='1 1 auto', margin_top=f'{S["lg"]}px' if show_header else '0')]
                + foot, gap='xxl', flex='1 1 auto', padding=f'28px {M}px {S["xxl"] if tail else 32}px', position='relative')
    pg = col('Page', [bleed, inner] + ([tail] if tail else []), gap='none', width=f'{W}px', height=f'{H}px', position='absolute', left='0', top='0')
    F.append(('wp', artboard(aid, f'{CFG["name"]} · {name}', W, H, bg, pg, use, 'doc')))

def bleed_photo(key, h, pos):
    return (f'<img class="photo" data-name="Hero photo" data-img="{key}" alt="Hero photo" '
            f'style="display:block;width:{W}px;height:{h}px;object-fit:cover;object-position:{pos};flex:none">')

