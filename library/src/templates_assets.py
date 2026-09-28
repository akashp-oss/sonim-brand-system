from gen import *

# Reference artboards built from the client's official asset folders:
#   Logo/             -> NEXA lockup (gen.NEXA_PATHS)
#   Icons/            -> official iconography (brand/icons/import_sonim_icons.py -> gen.SONIM_ICONS)
#   Rugged Template/  -> official Rugged Container sizes (gen.RUGGED_SIZES)
F = []
SECTION_META_EXTRA = [('assets', 'Brand assets', 'The official Sonim logo lockup, iconography and Rugged Container sizes, '
                       'taken from the client asset folders. Copy any of them as SVG.')]

X, M = 24, 120
def head(label, headline, top=120):
    return page_notch(X, top) + stack('Headline block', [text('Label', label, 'label', RED, 26), text('Headline', headline, 'h1', BLACK, 72)], l=M, t=top, w=1400, gap=14)

# ---------------------------------------------------------------- logo lockup on every approved background
PANELS = [('On white', WHITE, BLACK), ('On Sonim Gray', GRAY, BLACK), ('On Sonim Red', RED, WHITE), ('On black', BLACK, WHITE)]
pw, ph, gap = 390, 330, 40
a1 = (head('Logo', 'Sonim, **a NEXA company.**')
      + box('Lockup panels', l=M, t=400, w=4 * pw + 3 * gap, cls='row', style={'gap': f'{gap}px'}, inner=''.join(
          f'<div class="stack" data-name="{n}" style="gap:14px;width:{pw}px">'
          + box('Panel', w=pw, h=ph, cls='group', style={'position': 'relative', 'background': bg, 'outline': f'1px solid {GRAY}' if bg == WHITE else None},
                inner=logo(250, fg, l=70, t=round((ph - 250 * NEXA_RATIO) / 2)))
          + text('Caption', n, 'h3', BLACK, 22) + '</div>' for n, bg, fg in PANELS))
      + text('Rule', 'Single colour only: black on light, white on dark, photo or red. Bottom-left on the margin. '
             'Below 100 px wide the wordmark is used without the NEXA line.', 'body abs', BLACK, 22, {'left': f'{M}px', 'top': '860px', 'width': '1300px'})
      + logo(150, BLACK, l=M, b=88))
F.append(('assets', artboard('asset-logo', 'Brand assets · Logo lockup', 1920, 1080, WHITE, a1, 'Official NEXA lockup (Logo/)', 'slide')))

# ---------------------------------------------------------------- official iconography
keys = list(SONIM_ICONS)
cols, cw, rh = 7, 240, 186
rows = -(-len(keys) // cols)
a2 = (head('Iconography', 'Line icons, **one red detail.**')
      + box('Icon grid', l=M, t=330, w=cols * cw, cls='row', style={'flex-wrap': 'wrap', 'row-gap': '26px'}, inner=''.join(
          f'<div class="stack" data-name="{k}" style="width:{cw}px;gap:12px">{icon(k, 96, k)}{text("Name", k, "small", BLACK, 18)}</div>' for k in keys))
      + logo(150, BLACK, l=M, b=88))
H2 = 330 + rows * (96 + 12 + 25 + 26) + 200
F.append(('assets', artboard('asset-icons', 'Brand assets · Iconography', 1920, H2, WHITE, a2, f'{len(keys)} official icons (Icons/), brand colours only', 'slide')))

# ---------------------------------------------------------------- official Rugged Container sizes, drawn to scale
PPI, XS = 60, 7.5                           # 60 px per inch; notch depth 0.125 in, as in the official files
pick = [(3.75, 5), (4.25, 6), (4.75, 7), (5.25, 7.5), (5.75, 8)]
pick = [s for s in pick if s in RUGGED_SIZES] or RUGGED_SIZES[:5]
x0, cells = M, []
for i, (wi, hi) in enumerate(pick):
    W, Hc = wi * PPI, hi * PPI
    cells.append(rugged(f'Container {wi} × {hi} in', x0 + XS, 870 - Hc, W - 2 * XS, Hc, XS, (GRAY, RED)[i % 2], '', pad=0, snap=False)
                 + text('Size', f'{wi} × {hi} in', 'h3 abs', BLACK, 22, {'left': f'{x0}px', 'top': '892px'}))
    x0 += W + 40
a3 = (head('Rugged Container', 'Official sizes, **always taller than wide.**')
      + ''.join(cells)
      + text('Note', f'{len(RUGGED_SIZES)} official sizes from 3.75 × 5 in to 6.25 × 8 in (width includes both notches). '
             'Containers in the library snap to the nearest official proportion.', 'small abs', BLACK, 20, {'left': f'{M}px', 'top': '940px', 'width': '1300px'})
      + logo(150, BLACK, r=M, b=88))
F.append(('assets', artboard('asset-containers', 'Brand assets · Rugged Container sizes', 1920, 1080, WHITE, a3, 'Drawn to scale from Rugged Template/', 'slide')))
