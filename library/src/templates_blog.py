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

# ---------------------------------------------------------------- shared: side-by-side comparison + statement hero
# Blending and Scale Lock both teach the feature with the same scene shown twice: without it (left) and with it (right, red frame).
def statement(t, ink, size=60):
    """Hero slot as a short statement from the client's own caption copy (no stat on these two features)."""
    return text('Statement', t, 'h1 abs', ink, size, {'left': f'{M}px', 'top': f'{HERO_T}px', 'width': '980px', 'line-height': '1.1'})

def compare(left, right, tw, th, ty, notes, credit, extra=''):
    tg = 24
    x1 = PANEL + (VW - 2 * tw - tg) // 2
    x2 = x1 + tw + tg
    lab = lambda t, l, red: box('Label', l=l, t=ty - 70, cls='row', style={'background': RED if red else 'transparent', 'padding': '8px 14px' if red else '8px 0'},
                                inner=text('Label text', t, 'h3', WHITE, 30))
    frame = (fill('Frame', RED, l=x2 - 6, t=ty - 6, w=tw + 12, h=6) + fill('Frame', RED, l=x2 - 6, t=ty + th, w=tw + 12, h=6)
             + fill('Frame', RED, l=x2 - 6, t=ty, w=6, h=th) + fill('Frame', RED, l=x2 + tw, t=ty, w=6, h=th))
    out = (lab(left[0], x1, False) + lab(right[0], x2, True)
           + photo(left[0], left[1], x1, ty, tw, th) + photo(right[0], right[1], x2, ty, tw, th) + frame
           + extra.replace('{x1}', str(x1)).replace('{x2}', str(x2)))
    nt = ty + th + (54 if extra else 28)
    out += ''.join(text('Note', n, 'lead abs', WHITE, 24, {'left': f'{x}px', 'top': f'{nt}px', 'width': f'{tw}px'}) for n, x in zip(notes, (x1, x2)))
    return out + text('Credit', credit, 'small abs', WHITE, 14, {'right': f'{M}px', 'bottom': '32px', 'opacity': '.7'})

# ---------------------------------------------------------------- 1 · Blending Mode: FLIR's own thermal-only vs MSX example
# Source: flir.com MSX example (same scene; left thermal only, right blended with visible-camera edges).
cover('blog-blending', 'Blending Mode', WHITE, BLACK, RED, 'See the heat—', 'and exactly where it is.',
      statement('One view.\n**Full context.**', BLACK),
      compare(('Thermal only', 'msx_thermal'), ('Blended', 'msx_blend'), 350, 366, 330,
              ['The heat is there.\nThe details are not.', 'Visible edges on the heat:\nevery cable and bolt.'], 'Thermal image: FLIR MSX example'), BLACK,
      'Caption: Blending Mode layers thermal over the visible camera, so your crew sees what’s hot and exactly where it is. One view. Full context. sonimtech.com')

# ---------------------------------------------------------------- 2 · Spot Meter (electricians): brand book photo of an electrician at the panels
cover('blog-spot-meter', 'Spot Meter', BLACK, WHITE, RED, 'Stop estimating heat—', 'measure it to the degree.',
      hero_icons(['spot-crosshair'], WHITE, 'Exact, non-contact temperature at any point', 200),
      photo('Use-case photo · electrician', 'electrician', PANEL, 0, VW, H, '58% 50%'), BLACK,
      'Caption: Spot Meter gives you an exact, non-contact temperature at any point in the image. The number you need, from a safe distance. sonimtech.com')

# ---------------------------------------------------------------- 3 · IR Scale Lock (HVAC): the article's own example, side by side
# "A hot motor in the frame shouldn't change your diagnosis." Same breaker-panel capture twice: auto-scale lets the motor take
# the range and the hot breaker fades; the locked scale keeps it visible. Built by brand/make_scale_lock.py from the real capture.
bars = ''.join(f'<img class="abs photo" data-name="Color scale" data-img="scale_bar" alt="Color scale" style="left:{{{x}}}px;top:{230 + 568 + 22}px;width:340px;height:14px">' for x in ('x1', 'x2'))
cover('blog-scale-lock', 'IR Scale Lock', GRAY, BLACK, RED, 'Lock the scale—', 'and every reading stays true.',
      statement('Consistent from the first\nreading **to the last.**', BLACK),
      compare(('Auto-scale', 'scale_auto'), ('IR Scale Lock', 'scale_locked'), 340, 568, 230,
              ['A hot motor takes the range.\nThe faulty breaker fades.', 'Range locked to the panel.\nThe fault stays in view.'],
              'Illustration from a real XP Pro Thermal capture', bars), BLACK,
      'Caption: IR Scale Lock holds the thermal scale steady, so a hot motor or a warm hand never changes what you see. Consistent from the first reading to the last. sonimtech.com')

# ---------------------------------------------------------------- 4 · High-Temp: stat on Sonim Red + photo (client favourite, unchanged)
cover('blog-high-temp', 'High-Temp Measurement', RED, WHITE, BLACK, 'Keep the detail—', 'even when the heat climbs.',
      hero_stat('400°C', WHITE, 'Extended display range · 752°F'),
      photo('Use-case photo', 'structure_fire', PANEL, 0, VW, H, '45% 50%'), BLACK,
      'Caption: When the scene heats up, High-Temp Measurement extends the display range to 400°C (752°F), so the detail stays on screen when it matters most. sonimtech.com')

# ---------------------------------------------------------------- 5 · Palette Selector: stat "9" + FLIR's nine palette examples, named
# Source: flir.com "Picking a thermal color palette" (E95 electrical scene; Scout III elk for Black Hot and Graded Fire).
PALETTES = [('Ironbow', '50% 50%'), ('Rainbow', '50% 50%'), ('Rainbow HC', '50% 50%'), ('Arctic', '50% 50%'), ('Lava', '50% 50%'),
            ('White Hot', '50% 50%'), ('Black Hot', '50% 50%'), ('Isotherm', '50% 50%'), ('Graded Fire', '50% 50%')]
g = 6
pw, ph = (VW - 2 * g) // 3, (H - 2 * g) // 3
mosaic = ''.join(photo(f'Palette · {n}', f'flir_pal{i + 1}', PANEL + (i % 3) * (pw + g), (i // 3) * (ph + g), pw, ph, pos)
                 + box('Name', l=PANEL + (i % 3) * (pw + g) + (36 if i % 3 == 0 else 12), t=(i // 3) * (ph + g) + ph - 52, cls='row', style={'background': BLACK, 'padding': '6px 10px'},
                       inner=text('Name text', n, 'h3', WHITE, 20))
                 for i, (n, pos) in enumerate(PALETTES))
cover('blog-palettes', 'Palette Selector', BLACK, WHITE, RED, 'Nine palettes—', 'one clear picture for every job.',
      hero_stat('9', WHITE, 'Color palettes, switchable in the field')
      + text('Credit', 'Palette examples: FLIR', 'small abs', WHITE, 14, {'right': f'{M}px', 'bottom': f'{M}px', 'opacity': '.7'}),
      mosaic, BLACK,
      'Caption: Every surface, material and light condition shows heat differently. Choose from nine palettes to get the clearest image for the job in front of you. sonimtech.com')
