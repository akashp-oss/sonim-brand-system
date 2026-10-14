from gen import *

# XP Pro Thermal blog covers (1920 x 1080), one per feature.
# Round 3 (2026-10-14): visuals tied to the articles (Thermal Pro blog content); titles unchanged.
# Round 2 client feedback (Figma): drop the three-icon rows; use images, not illustrations; anything shown must
# mean something and be accurate. The High-Temp cover (stat on Sonim Red + photo) was the favorite, so every
# cover now follows it: a colour panel with the headline and one supporting line, and a meaningful visual.
# Visuals are real: the XP Pro Thermal render and the thermal capture on its screen (an MSX image of a breaker
# panel with one hot breaker), cut from the client's cover. The palette cover shows that same capture in nine
# colour maps (same data, different palette: what the feature does). Copy: client brief.
F = []
SECTION_META_EXTRA = [('blog', 'Blog covers', 'XP Pro Thermal feature covers, 1920 × 1080: a colour panel with the headline and '
                       'one meaningful visual per feature (product, real thermal capture or use-case photo).')]
W, H, M, X = 1920, 1080, 96, 20
PANEL = 1140                    # colour panel width; the visual fills the rest (780 px)
HEAD_SIZE = 84

def flir(color=WHITE, l=M, b=M):
    return stack('Powered by FLIR', [
        box('Powered row', cls='row', style={'gap': '12px', 'align-items': 'center', 'width': '400px'}, inner=
            text('Label', 'Powered by', 'small', color, 16) + fill('Rule', color, style={'position': 'relative', 'flex': '1', 'height': '1px'})),
        text('Partner', 'FLIR', 'h2', color, 34, {'margin-top': '10px'}),
        text('Tech', 'MSX Technology\nLepton 3.5', 'lead', color, 24)], l=l, b=b, w=400, gap=2)

def split(aid, name, panel, ink, em, line2, line3, support, visual, visual_bg, caption):
    """Favourite layout: colour panel (Expanded Notch) with logo, headline, support line, FLIR; visual on the right."""
    inner = (fill('Visual background', visual_bg, l=PANEL, t=0, w=W - PANEL, h=H) + visual
             + xnotch('Expanded notch', 0, 0, PANEL, H, X, panel,
                      logo(220, ink, l=M, t=M)
                      + text('Headline', f'XP Pro Thermal:\n**{line2}** {line3}', 'h1 abs', ink, HEAD_SIZE,
                             {'left': f'{M}px', 'top': '230px', 'width': '1000px', '--em': em, 'line-height': '1.04'})
                      + support
                      + flir(ink), notch_top=2 * X + 210))
    F.append(('blog', artboard(aid, f'Blog cover · {name}', W, H, panel, inner, caption, 'slide')))

def support_line(t, ink, top=600):
    return text('Support', t, 'lead abs', ink, 36, {'left': f'{M}px', 'top': f'{top}px', 'width': '940px'})

def tag(t, l, t_, ink=WHITE, bg=BLACK, line_to=None):
    """Annotation tag; optional leader line to the right, ending at x = line_to."""
    leader = fill('Leader', ink, style={'position': 'relative', 'width': f'{line_to}px', 'height': '2px'}) if line_to else ''
    return box('Annotation', l=l, t=t_, cls='row', style={'gap': '0', 'align-items': 'center'}, inner=
               box('Tag', cls='row', style={'background': bg, 'padding': '12px 18px', 'gap': '10px', 'align-items': 'center'}, inner=
                   fill('Dot', RED, style={'position': 'relative', 'width': '12px', 'height': '12px'}) + text('Tag text', t, 'h3', ink, 22)) + leader)

# ---------------------------------------------------------------- shared visuals, all from the one real capture
# capture = MSX image of a breaker panel (212 x 354) from the device screen; coordinates below are in capture px
CAP_W, CAP_H = 212, 354
SPOTS = [('Sp1', 130, 285), ('Sp2', 110, 200), ('Sp3', 137, 140)]   # hot breaker + two neighbours on the same panel

def crosshair(cx, cy, size=120, color=WHITE):
    h = size // 2
    return (f'<svg data-name="Spot meter" width="{size}" height="{size}" viewBox="0 0 {size} {size}" class="abs" style="left:{cx - h}px;top:{cy - h}px">'
            f'<circle cx="{h}" cy="{h}" r="{h * .55}" fill="none" stroke="{color}" stroke-width="5"/>'
            f'<path d="M{h} 0v{h * .6}M{h} {h * 1.4}v{h * .6}M0 {h}h{h * .6}M{h * 1.4} {h}h{h * .6}" stroke="{color}" stroke-width="5"/>'
            f'<circle cx="{h}" cy="{h}" r="8" fill="{RED}"/></svg>')

def chip(t, l, top, size=26):
    return box('Label', l=l, t=top, cls='row', style={'background': RED, 'padding': '8px 14px'}, inner=text('Label text', t, 'h3', WHITE, size))

# ---------------------------------------------------------------- 1 · Blending Mode: visible edges + thermal = one view
# two input layers stacked on the left feed one large blended view on the right
iw, ih = 180, 300                      # input tiles (capture aspect 0.6)
rw, rh = 420, 700                      # result tile
ix, rx = PANEL + 56, PANEL + 56 + iw + 104
iy1, iy2, ry = 150, 1080 - 150 - ih - 40, (H - rh) // 2
blend = (photo('Visible camera layer', 'edge_layer', ix, iy1, iw, ih) + photo('Thermal layer', 'thermal_layer', ix, iy2, iw, ih)
         + text('Visible label', 'Visible camera', 'h3 abs', WHITE, 22, {'left': f'{ix}px', 'top': f'{iy1 + ih + 10}px'})
         + text('Thermal label', 'Thermal', 'h3 abs', WHITE, 22, {'left': f'{ix}px', 'top': f'{iy2 + ih + 10}px'})
         + text('Plus', '+', 'display abs', RED, 110, {'left': f'{ix + iw // 2 - 32}px', 'top': f'{(iy1 + ih + 40 + iy2) // 2 - 52}px'})
         + text('Equals', '=', 'display abs', RED, 110, {'left': f'{ix + iw + 22}px', 'top': f'{H // 2 - 70}px'})
         + fill('Result frame', RED, l=rx - 8, t=ry - 8, w=rw + 16, h=rh + 16)
         + photo('Blended view', 'thermal_p1', rx, ry, rw, rh)
         + box('Result label', l=rx - 8, t=ry + rh + 8, cls='row', style={'background': RED, 'padding': '8px 14px'}, inner=text('Label text', 'One view', 'h3', WHITE, 24)))
split('blog-blending', 'Blending Mode', WHITE, BLACK, RED, 'See the heat—', 'and exactly where it is.',
      support_line('One view. Full context.', BLACK), blend, BLACK,
      'Caption: Blending Mode layers thermal over the visible camera, so your crew sees what’s hot and exactly where it is. One view. Full context. sonimtech.com')

# ---------------------------------------------------------------- 2 · Spot Meter (electricians): several spot meters on the breaker panel
sc = H / CAP_H
cw = round(CAP_W * sc)
cx0 = PANEL + (W - PANEL - cw) // 2 + 10
spot = photo('Breaker panel capture', 'thermal_p1', cx0, 0, cw, H) + ''.join(
    crosshair(round(cx0 + x * sc), round(y * sc)) + chip(n, round(cx0 + x * sc) + 64, round(y * sc) - 22) for n, x, y in SPOTS)
split('blog-spot-meter', 'Spot Meter', BLACK, WHITE, RED, 'Stop estimating heat—', 'measure it to the degree.',
      support_line('“Looks warm” isn’t a reading.', WHITE), spot, BLACK,
      'Caption: Spot Meter gives you an exact, non-contact temperature at any point in the image. The number you need, from a safe distance. sonimtech.com')

# ---------------------------------------------------------------- 3 · IR Scale Lock (HVAC): the thermal scale itself, locked
bx, by, bw, bh = PANEL + 110, 250, 110, 700
scale = (f'<svg data-name="Thermal color scale" width="{bw}" height="{bh}" viewBox="0 0 {bw} {bh}" class="abs" style="left:{bx}px;top:{by}px">'
         f'<defs><linearGradient id="scaleGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffe0"/><stop offset=".2" stop-color="#ffc000"/>'
         f'<stop offset=".45" stop-color="#ff3000"/><stop offset=".7" stop-color="#a000c0"/><stop offset="1" stop-color="#100040"/></linearGradient></defs>'
         f'<rect width="{bw}" height="{bh}" fill="url(#scaleGrad)"/></svg>')
lock = (f'<svg data-name="Lock" width="150" height="170" viewBox="0 0 150 170" class="abs" style="left:{bx + bw // 2 - 75}px;top:{by - 200}px">'
        f'<path d="M35 75v-25a40 40 0 0 1 80 0v25" fill="none" stroke="{RED}" stroke-width="16"/><rect x="15" y="75" width="120" height="90" fill="{RED}"/>'
        f'<rect x="68" y="105" width="14" height="32" fill="{WHITE}"/></svg>')
span_t, span_b = by + 150, by + 560
lock_ui = (scale + lock
           + fill('Span bracket', WHITE, l=bx + bw + 30, t=span_t, w=6, h=span_b - span_t)
           + fill('Span top', WHITE, l=bx + bw + 14, t=span_t, w=38, h=6) + fill('Span bottom', WHITE, l=bx + bw + 14, t=span_b - 6, w=38, h=6)
           + text('Span label', 'Span', 'h2 abs', WHITE, 34, {'left': f'{bx + bw + 64}px', 'top': f'{span_t - 8}px'})
           + fill('Level marker', RED, l=bx - 40, t=(span_t + span_b) // 2 - 3, w=bw + 80, h=6)
           + text('Level label', 'Level', 'h2 abs', WHITE, 34, {'left': f'{bx + bw + 64}px', 'top': f'{(span_t + span_b) // 2 - 22}px'})
           + text('Scale note', 'Colors stay fixed to the range you set.', 'lead abs', WHITE, 26, {'left': f'{bx + bw + 64}px', 'top': f'{by + bh - 60}px', 'width': '330px'}))
split('blog-scale-lock', 'IR Scale Lock', GRAY, BLACK, RED, 'Lock the scale—', 'and every reading stays true.',
      support_line('A hot motor in the frame shouldn’t change your diagnosis.', BLACK), lock_ui, BLACK,
      'Caption: IR Scale Lock holds the thermal scale steady, so a hot motor or a warm hand never changes what you see. Consistent from the first reading to the last. sonimtech.com')

# ---------------------------------------------------------------- 4 · High-Temp: stat on Sonim Red + photo (client favourite, unchanged)
c4 = (photo('Use-case photo', 'structure_fire', 1140, 0, 780, 1080, '45% 50%')
      + xnotch('Expanded notch', 0, 0, 1140, 1080, X, RED,
               logo(220, WHITE, l=M, t=M)
               + text('Headline', 'XP Pro Thermal:\n**Keep the detail—** even when the heat climbs.', 'h1 abs', WHITE, HEAD_SIZE, {'left': f'{M}px', 'top': '230px', 'width': '1000px', '--em': BLACK})
               + text('Stat', '400°C', 'stat abs', WHITE, 210, {'left': f'{M - 8}px', 'top': '540px'})
               + text('Stat caption', 'Extended display range · 752°F', 'h2 abs', WHITE, 34, {'left': f'{M}px', 'top': '748px'})
               + flir(), notch_top=2 * X + 210))
F.append(('blog', artboard('blog-high-temp', 'Blog cover · High-Temp Measurement', W, H, RED, c4,
          'Caption: When the scene heats up, High-Temp Measurement extends the display range to 400°C (752°F), so the detail stays on screen when it matters most. sonimtech.com', 'slide')))

# ---------------------------------------------------------------- 5 · Palette Selector (pest control): full-bleed mosaic of nine palettes
g = 6
pw, ph = (W - PANEL - 2 * g) // 3, (H - 2 * g) // 3
mosaic = ''.join(photo(f'Palette {i + 1}', f'thermal_p{i + 1}', PANEL + (i % 3) * (pw + g), (i // 3) * (ph + g), pw, ph) for i in range(9))
mosaic += chip('9 color palettes', PANEL + 40, H - 96, 26)
split('blog-palettes', 'Palette Selector', BLACK, WHITE, RED, 'Nine palettes—', 'one clear picture for every job.',
      support_line('Switch in the field to match the job.', WHITE), mosaic, BLACK,
      'Caption: Every surface, material and light condition shows heat differently. Choose from nine palettes to get the clearest image for the job in front of you. sonimtech.com')
