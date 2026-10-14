from gen import *

# XP Pro Thermal blog covers (1920 x 1080), one per feature.
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

# device render geometry (xppro_thermal.png, 450 x 870): front screen's thermal image and its hot breaker
SCREEN_L, SCREEN_T, HOT = 203, 287, (333, 570)

# ---------------------------------------------------------------- 1 · Blending Mode: the device, its MSX screen annotated
dx, dy = 1350, 105
split('blog-blending', 'Blending Mode', WHITE, BLACK, RED, 'See the heat—', 'and exactly where it is.',
      support_line('One view. Full context.', BLACK),
      cutout('Product render', 'xppro_thermal', dx, dy, 450, 870)
      + tag('Thermal over the visible camera', PANEL + 30, dy + SCREEN_T + 150),
      BLACK,
      'Caption: Blending Mode layers thermal over the visible camera, so your crew sees what’s hot and exactly where it is. One view. Full context. sonimtech.com')

# ---------------------------------------------------------------- 2 · Spot Meter: crosshair on the hot breaker in the real capture
s, dx, dy = 1.2, 1250, 30
hx, hy = round(dx + HOT[0] * s), round(dy + HOT[1] * s)
cross = (f'<svg data-name="Spot meter crosshair" width="150" height="150" viewBox="0 0 150 150" class="abs" style="left:{hx - 75}px;top:{hy - 75}px">'
         f'<circle cx="75" cy="75" r="42" fill="none" stroke="{WHITE}" stroke-width="4"/>'
         f'<path d="M75 5v45M75 100v45M5 75h45M100 75h45" stroke="{WHITE}" stroke-width="4"/><circle cx="75" cy="75" r="7" fill="{RED}"/></svg>')
split('blog-spot-meter', 'Spot Meter', BLACK, WHITE, RED, 'Stop estimating heat—', 'measure it to the degree.',
      support_line('The number you need, from a safe distance.', WHITE),
      cutout('Product render', 'xppro_thermal', dx, dy, round(450 * s), round(870 * s)) + cross
      + tag('Spot meter', hx - 330, hy - 26, line_to=330 - 75 - 190),
      GRAY,
      'Caption: Spot Meter gives you an exact, non-contact temperature at any point in the image. The number you need, from a safe distance. sonimtech.com')

# ---------------------------------------------------------------- 3 · IR Scale Lock: use-case photo slot (no accurate image available yet)
slot = box('Image placeholder', l=PANEL + 60, t=60, w=W - PANEL - 120, h=H - 120, cls='group', inner=
           fill('Placeholder fill', WHITE, l=0, t=0, w=W - PANEL - 120, h=H - 120, style={'outline': f'2px dashed {BLACK}'})
           + stack('Placeholder note', [text('Note title', 'Use-case photo', 'h2', BLACK, 34),
                                         text('Note', 'Replace with a real image: a technician scanning a running motor, so a warm motor or hand in frame is the story. Keep it accurate to IR Scale Lock.', 'body', BLACK, 22)],
                   l=48, t=48, w=W - PANEL - 216, gap=12))
split('blog-scale-lock', 'IR Scale Lock', GRAY, BLACK, RED, 'Lock the scale—', 'and every reading stays true.',
      support_line('Consistent from the first reading to the last.', BLACK),
      slot, GRAY,
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

# ---------------------------------------------------------------- 5 · Palette Selector: one capture in nine colour palettes
tw, th, gap = 172, 290, 14
gx, gy = PANEL + (W - PANEL - (3 * tw + 2 * gap)) // 2 + 10, 96
grid = box('Palette grid', l=gx, t=gy, w=3 * tw + 2 * gap, cls='group', inner=''.join(
           photo(f'Palette {i + 1}', f'thermal_p{i + 1}', (i % 3) * (tw + gap), (i // 3) * (th + gap), tw, th) for i in range(9)))
split('blog-palettes', 'Palette Selector', BLACK, WHITE, RED, 'Nine palettes—', 'one clear picture for every job.',
      support_line('Nine color palettes. Same scene, the clearest view for each job.', WHITE),
      grid + text('Grid note', 'One thermal capture shown in nine color palettes', 'small abs', WHITE, 16, {'left': f'{gx}px', 'top': f'{gy + 3 * th + 2 * gap + 14}px'}),
      BLACK,
      'Caption: Every surface, material and light condition shows heat differently. Choose from nine palettes to get the clearest image for the job in front of you. sonimtech.com')
