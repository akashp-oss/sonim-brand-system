from gen import *
import re

# XP Pro Thermal blog covers (1920 x 1080), one per feature.
# Round 4 (2026-10-14): every cover now follows the client favourite (High-Temp) exactly: a colour panel with
# logo, headline, ONE hero element in the stat slot, and the FLIR block; a meaningful visual on the right.
# No floating one-liners. Hero element = the feature's number where there is one (400°C, 9 palettes),
# otherwise the feature drawn as large brand icons. Visuals: Sonim brand book photography for the use case
# (electrician, technician), the XP Pro Thermal product, or the real capture in nine palettes.
# Titles and captions: client brief, unchanged.
F = []
SECTION_META_EXTRA = [('blog', 'Blog covers', 'XP Pro Thermal feature covers, 1920 × 1080: a colour panel with the headline and '
                       'one hero element (stat or feature icon), plus a use-case photo, the product or a real capture.')]
W, H, M, X = 1920, 1080, 96, 20
PANEL = 1140                    # colour panel width; the visual fills the rest (780 px)
VW = W - PANEL
HEAD_SIZE = 84
HERO_T, CAP_T = 540, 748        # stat slot and its caption, as on the High-Temp cover

def flir(color=WHITE, l=M, b=M):
    return stack('Powered by FLIR', [
        box('Powered row', cls='row', style={'gap': '12px', 'align-items': 'center', 'width': '400px'}, inner=
            text('Label', 'Powered by', 'small', color, 16) + fill('Rule', color, style={'position': 'relative', 'flex': '1', 'height': '1px'})),
        text('Partner', 'FLIR', 'h2', color, 34, {'margin-top': '10px'}),
        text('Tech', 'MSX Technology\nLepton 3.5', 'lead', color, 24)], l=l, b=b, w=400, gap=2)

def big_icon(key, size, ink, name=None):
    """Brand icon at hero size: line in the panel ink (black or white), detail stays Sonim Red, stroke weighted up to read at size."""
    svg = re.sub(r'"#000(000)?"', f'"{ink}"', ICONS[key]).replace('stroke-width="0.4"', 'stroke-width="0.62"')
    svg = svg.replace('<svg ', f'<svg data-name="{esc(name or key)} icon" width="{size}" height="{size}" ', 1)
    return f'<div class="icon" data-name="{esc(name or key)}" style="width:{size}px;height:{size}px">{svg}</div>'

def hero_icons(parts, ink, caption, size=170):
    """Icons (and + / = signs) in a row in the stat slot, with a caption below."""
    inner = ''.join(big_icon(p, size, ink) if p in ICONS else text('Sign', p, 'display', RED, 120, {'line-height': '1'}) for p in parts)
    return (box('Hero', l=M - 14 - (size - 170) // 8, t=HERO_T - (size - 170) // 2, cls='row', style={'gap': '28px', 'align-items': 'center', 'height': f'{size}px'}, inner=inner)
            + text('Hero caption', caption, 'h2 abs', ink, 34, {'left': f'{M}px', 'top': f'{CAP_T}px', 'width': '980px'}))

def hero_stat(stat, ink, caption):
    return (text('Stat', stat, 'stat abs', ink, 210, {'left': f'{M - 8}px', 'top': f'{HERO_T}px'})
            + text('Stat caption', caption, 'h2 abs', ink, 34, {'left': f'{M}px', 'top': f'{CAP_T}px'}))

def cover(aid, name, panel, ink, em, line2, line3, hero, visual, visual_bg, caption):
    inner = (fill('Visual background', visual_bg, l=PANEL, t=0, w=VW, h=H) + visual
             + xnotch('Expanded notch', 0, 0, PANEL, H, X, panel,
                      logo(220, ink, l=M, t=M)
                      + text('Headline', f'XP Pro Thermal:\n**{line2}** {line3}', 'h1 abs', ink, HEAD_SIZE,
                             {'left': f'{M}px', 'top': '230px', 'width': '1000px', '--em': em})
                      + hero + flir(ink), notch_top=2 * X + 210))
    F.append(('blog', artboard(aid, f'Blog cover · {name}', W, H, panel, inner, caption, 'blog')))

# ---------------------------------------------------------------- 1 · Blending Mode: thermal + visible in one view
# hero: the feature in type ("Thermal + visible", as loud as 400°C); visual: brand book photo where heat is the job (foundry pour)
def hero_type(t, ink, caption, size=110):
    return (text('Hero', t, 'stat abs', ink, size, {'left': f'{M}px', 'top': f'{HERO_T + 40}px', 'white-space': 'nowrap', 'letter-spacing': '-0.03em'})
            + text('Hero caption', caption, 'h2 abs', ink, 34, {'left': f'{M}px', 'top': f'{CAP_T}px'}))

cover('blog-blending', 'Blending Mode', WHITE, BLACK, RED, 'See the heat—', 'and exactly where it is.',
      hero_type('Thermal **+** visible', BLACK, 'Two cameras, blended into one view'),
      photo('Use-case photo · foundry', 'foundry', PANEL, 0, VW, H, '76% 50%'), BLACK,
      'Caption: Blending Mode layers thermal over the visible camera, so your crew sees what’s hot and exactly where it is. One view. Full context. sonimtech.com')

# ---------------------------------------------------------------- 2 · Spot Meter (electricians): brand book photo of an electrician at the panels
cover('blog-spot-meter', 'Spot Meter', BLACK, WHITE, RED, 'Stop estimating heat—', 'measure it to the degree.',
      hero_icons(['spot-crosshair'], WHITE, 'Exact, non-contact temperature at any point', 200),
      photo('Use-case photo · electrician', 'electrician', PANEL, 0, VW, H, '58% 50%'), BLACK,
      'Caption: Spot Meter gives you an exact, non-contact temperature at any point in the image. The number you need, from a safe distance. sonimtech.com')

# ---------------------------------------------------------------- 3 · IR Scale Lock (HVAC): the article's own example, side by side
# "A hot motor in the frame shouldn't change your diagnosis." Same breaker-panel capture twice: auto-scale lets the motor take
# the range and the hot breaker fades; the locked scale keeps it visible. Built by brand/make_scale_lock.py from the real capture.
tw, th, tg = 340, 568, 24
tx1 = PANEL + (VW - 2 * tw - tg) // 2
tx2, ty = tx1 + tw + tg, 230
def col_label(t, l, red):
    return box('Label', l=l, t=ty - 70, cls='row', style={'background': RED if red else 'transparent', 'padding': '8px 14px' if red else '8px 0', 'gap': '10px', 'align-items': 'center'},
               inner=text('Label text', t, 'h3', WHITE, 30))
def bar(l):
    return f'<img class="abs photo" data-name="Color scale" data-img="scale_bar" alt="Color scale" style="left:{l}px;top:{ty + th + 22}px;width:{tw}px;height:14px">'
compare = (col_label('Auto-scale', tx1, False) + col_label('IR Scale Lock', tx2, True)
           + photo('Auto-scale capture', 'scale_auto', tx1, ty, tw, th) + photo('Locked-scale capture', 'scale_locked', tx2, ty, tw, th)
           + fill('Locked frame', RED, l=tx2 - 6, t=ty - 6, w=tw + 12, h=6) + fill('Locked frame', RED, l=tx2 - 6, t=ty + th, w=tw + 12, h=6)
           + fill('Locked frame', RED, l=tx2 - 6, t=ty, w=6, h=th) + fill('Locked frame', RED, l=tx2 + tw, t=ty, w=6, h=th)
           + bar(tx1) + bar(tx2)
           + text('Note', 'A hot motor takes the range.\nThe faulty breaker fades.', 'lead abs', WHITE, 24, {'left': f'{tx1}px', 'top': f'{ty + th + 54}px', 'width': f'{tw}px'})
           + text('Note', 'Range locked to the panel.\nThe fault stays in view.', 'lead abs', WHITE, 24, {'left': f'{tx2}px', 'top': f'{ty + th + 54}px', 'width': f'{tw}px'})
           + text('Credit', 'Illustration from a real XP Pro Thermal capture', 'small abs', WHITE, 14, {'right': f'{M}px', 'bottom': '32px', 'opacity': '.7'}))
cover('blog-scale-lock', 'IR Scale Lock', GRAY, BLACK, RED, 'Lock the scale—', 'and every reading stays true.',
      hero_type('Level **+** span', BLACK, 'Locked to the range you set'),
      compare, BLACK,
      'Caption: IR Scale Lock holds the thermal scale steady, so a hot motor or a warm hand never changes what you see. Consistent from the first reading to the last. sonimtech.com')

# ---------------------------------------------------------------- 4 · High-Temp: stat on Sonim Red + photo (client favourite, unchanged)
cover('blog-high-temp', 'High-Temp Measurement', RED, WHITE, BLACK, 'Keep the detail—', 'even when the heat climbs.',
      hero_stat('400°C', WHITE, 'Extended display range · 752°F'),
      photo('Use-case photo', 'structure_fire', PANEL, 0, VW, H, '45% 50%'), BLACK,
      'Caption: When the scene heats up, High-Temp Measurement extends the display range to 400°C (752°F), so the detail stays on screen when it matters most. sonimtech.com')

# ---------------------------------------------------------------- 5 · Palette Selector: stat "9" + the real capture in all nine palettes
g = 6
pw, ph = (VW - 2 * g) // 3, (H - 2 * g) // 3
mosaic = ''.join(photo(f'Palette {i + 1}', f'thermal_p{i + 1}', PANEL + (i % 3) * (pw + g), (i // 3) * (ph + g), pw, ph) for i in range(9))
cover('blog-palettes', 'Palette Selector', BLACK, WHITE, RED, 'Nine palettes—', 'one clear picture for every job.',
      hero_stat('9', WHITE, 'Color palettes, switchable in the field'),
      mosaic, BLACK,
      'Caption: Every surface, material and light condition shows heat differently. Choose from nine palettes to get the clearest image for the job in front of you. sonimtech.com')
