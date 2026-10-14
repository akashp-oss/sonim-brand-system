from gen import *

# XP Pro Thermal blog covers (1920 x 1080), one per feature. Client feedback (Figma, NEXA file): the covers all
# looked the same, use real use-case images, a new infographic style when the device is shown, different icons
# per cover, and the Sonim, a NEXA company logo. So every cover has its own layout and its own feature icons.
# Copy and captions: client brief. Specs on the FLIR line (MSX, Lepton 3.5) come from the client's Figma cover.
F = []
SECTION_META_EXTRA = [('blog', 'Blog covers', 'XP Pro Thermal feature covers, 1920 × 1080. Five layouts so a series never looks the same twice: '
                       'infographic, use-case photo, comparison, stat on Sonim Red, product with a giant numeral.')]
W, H, M, X = 1920, 1080, 96, 20
HEAD_SIZE = 84

def icon_on(key, size, color, name=None):
    """Official-style icon recoloured for dark backgrounds (black line -> white; the red detail stays)."""
    svg = ICONS[key].replace('#000000', color).replace('<svg ', f'<svg data-name="{esc(name or key)} icon" width="{size}" height="{size}" ', 1)
    return f'<div class="icon" data-name="{esc(name or key)}" style="width:{size}px;height:{size}px;flex:none">{svg}</div>'

def headline(top, line2, line3, color=WHITE, em=RED, w=1100):
    return (page_notch(X, top, RED)
            + text('Headline', f'XP Pro Thermal:\n**{line2}** {line3}', 'h1 abs', color, HEAD_SIZE,
                   {'left': f'{M}px', 'top': f'{top}px', 'width': f'{w}px', '--em': em}))

def callouts(items, top, color=WHITE, w=1100, size=92):
    return box('Feature callouts', l=M, t=top, w=w, cls='row', style={'gap': '44px'}, inner=''.join(
        f'<div class="row" data-name="{t}" style="gap:18px;align-items:center">{icon_on(k, size, color, t)}'
        f'<div class="stack" data-name="Text" style="gap:4px">{text("Label", lab, "lead", color, 24)}{text("Value", t, "h2", color, 34)}</div></div>'
        for k, lab, t in items))

def flir(color=WHITE, l=M, b=M):
    return stack('Powered by FLIR', [
        box('Powered row', cls='row', style={'gap': '12px', 'align-items': 'center', 'width': '400px'}, inner=
            text('Label', 'Powered by', 'small', color, 16) + fill('Rule', color, style={'position': 'relative', 'flex': '1', 'height': '1px'})),
        text('Partner', 'FLIR', 'h2', color, 34, {'margin-top': '10px'}),
        text('Tech', 'MSX Technology\nLepton 3.5', 'lead', color, 24)], l=l, b=b, w=400, gap=2)

def cover(aid, name, bg, inner, caption):
    F.append(('blog', artboard(aid, f'Blog cover · {name}', W, H, bg, inner, caption, 'slide')))

# ---------------------------------------------------------------- 1 · Blending Mode: infographic, no device
venn = (f'<svg data-name="Blend diagram" width="660" height="486" viewBox="0 0 760 560" class="abs" style="left:1168px;top:296px">'
        f'<circle data-name="Visible circle" cx="250" cy="280" r="240" fill="none" stroke="{WHITE}" stroke-width="3"/>'
        f'<circle data-name="Thermal circle" cx="510" cy="280" r="240" fill="none" stroke="{RED}" stroke-width="3"/></svg>')
c1 = (logo(220, WHITE, l=M, t=M)
      + headline(230, 'See the heat—', 'and exactly where it is.', w=1000)
      + callouts([('visible-camera', 'Layer one', 'Visible'), ('thermal-sensor', 'Layer two', 'Thermal'), ('blend-layers', 'Result', 'One view')], 600, w=1000)
      + venn
      + text('Visible label', 'Visible\ncamera', 'h2 abs', WHITE, 30, {'left': '1236px', 'top': '508px'})
      + text('Thermal label', 'Thermal\nimage', 'h2 abs', WHITE, 30, {'right': '160px', 'top': '508px', 'text-align': 'right'})
      + text('Blend label', 'Full\ncontext', 'h2 abs', WHITE, 30, {'left': '1446px', 'top': '508px', 'text-align': 'center', 'width': '100px'})
      + flir())
cover('blog-blending', 'Blending Mode', BLACK, c1,
      'Caption: Blending Mode layers thermal over the visible camera, so your crew sees what’s hot and exactly where it is. One view. Full context. sonimtech.com')

# ---------------------------------------------------------------- 2 · Spot Meter: use-case photo + crosshair
cross = (f'<svg data-name="Spot meter crosshair" width="260" height="260" viewBox="0 0 260 260" class="abs" style="left:1630px;top:640px">'
         f'<circle cx="130" cy="130" r="80" fill="none" stroke="{WHITE}" stroke-width="4"/>'
         f'<path d="M130 10v80M130 170v80M10 130h80M170 130h80" stroke="{WHITE}" stroke-width="4"/>'
         f'<circle cx="130" cy="130" r="9" fill="{RED}"/></svg>')
c2 = (photo('Use-case photo', 'wildfire', 1180, 0, 740, 1080, '100% 50%')
      + cross
      + box('Spot tag', l=1600, t=566, cls='row', style={'background': BLACK, 'padding': '12px 18px', 'gap': '10px', 'align-items': 'center'}, inner=
            fill('Dot', RED, style={'position': 'relative', 'width': '12px', 'height': '12px'}) + text('Tag', 'Spot meter', 'h3', WHITE, 22))
      + logo(220, WHITE, l=M, t=M)
      + headline(230, 'Stop estimating heat—', 'measure it to the degree.', w=1000)
      + callouts([('spot-crosshair', 'Point', 'Exact spot'), ('non-contact', 'Reading', 'Non-contact'), ('thermometer', 'Result', 'To the degree')], 600, w=1040)
      + flir())
cover('blog-spot-meter', 'Spot Meter', BLACK, c2,
      'Caption: Spot Meter gives you an exact, non-contact temperature at any point in the image. The number you need, from a safe distance. sonimtech.com')

# ---------------------------------------------------------------- 3 · IR Scale Lock: comparison infographic on white
def scale_panel(name, l, title, note, locked):
    """A thermal scale drawn in brand colours: six stepped segments, a red marker for the same object.
    Auto scale: the marker sits low because a hotter object stretched the range. Locked: the range holds."""
    steps = [BLACK, BLACK, GRAY, GRAY, WHITE, WHITE] if locked else [BLACK, GRAY, GRAY, WHITE, WHITE, WHITE]
    return box(name, l=l, t=250, w=300, h=640, cls='group', inner=
               fill('Panel fill', GRAY if locked else WHITE, l=0, t=0, w=300, h=640, style={'outline': f'2px solid {GRAY}'})
               + text('Panel title', title, 'h2 abs', BLACK, 30, {'left': '34px', 'top': '40px'})
               + box('Scale bar', l=34, t=110, w=64, h=432, cls='group', style={'outline': f'2px solid {BLACK}'}, inner=''.join(
                     fill('Step', c, l=0, t=i * 72, w=64, h=72) for i, c in enumerate(steps)))
               + box('Marker', l=110, t=182 if locked else 398, cls='row', style={'gap': '10px', 'align-items': 'center'}, inner=
                     fill('Marker line', RED, style={'position': 'relative', 'width': '40px', 'height': '4px'}) + text('Marker text', 'Same object', 'h3', BLACK, 20))
               + text('Note', note, 'body abs', BLACK, 20, {'left': '34px', 'top': '566px', 'width': '240px'}))
c3 = (logo(220, BLACK, l=M, t=M)
      + headline(230, 'Lock the scale—', 'and every reading stays true.', color=BLACK, w=1040)
      + callouts([('scale-lock', 'Thermal scale', 'Locked'), ('consistent', 'Readings', 'Consistent'), ('clear-view', 'On screen', 'No surprises')], 600, color=BLACK, w=1040)
      + scale_panel('Auto scale panel', 1196, 'Auto scale', 'A hot motor enters the frame and the scale shifts.', False)
      + scale_panel('Scale lock panel', 1524, 'Scale lock', 'The scale holds, first reading to last.', True)
      + box('Lock badge', l=1524 + 300 - 100, t=250 + 24, w=80, h=80, cls='group', inner=icon_on('scale-lock', 80, BLACK, 'Scale lock'))
      + flir(BLACK))
cover('blog-scale-lock', 'IR Scale Lock', WHITE, c3,
      'Caption: IR Scale Lock holds the thermal scale steady, so a hot motor or a warm hand never changes what you see. Consistent from the first reading to the last. sonimtech.com')

# ---------------------------------------------------------------- 4 · High-Temp: stat on Sonim Red + photo
c4 = (photo('Use-case photo', 'structure_fire', 1140, 0, 780, 1080, '45% 50%')
      + xnotch('Expanded notch', 0, 0, 1140, 1080, X, RED,
               logo(220, WHITE, l=M, t=M)
               + text('Headline', 'XP Pro Thermal:\n**Keep the detail—** even when the heat climbs.', 'h1 abs', WHITE, HEAD_SIZE, {'left': f'{M}px', 'top': '230px', 'width': '1000px', '--em': BLACK})
               + text('Stat', '400°C', 'stat abs', WHITE, 210, {'left': f'{M - 8}px', 'top': '540px'})
               + text('Stat caption', 'Extended display range · 752°F', 'h2 abs', WHITE, 34, {'left': f'{M}px', 'top': '748px'})
               + flir(), notch_top=2 * X + 210))
cover('blog-high-temp', 'High-Temp Measurement', RED, c4,
      'Caption: When the scene heats up, High-Temp Measurement extends the display range to 400°C (752°F), so the detail stays on screen when it matters most. sonimtech.com')

# ---------------------------------------------------------------- 5 · Palette Selector: product + giant numeral
c5 = (text('Numeral', '9', 'display abs', RED, 980, {'left': '1150px', 'top': '20px', 'line-height': '0.8', 'letter-spacing': '-0.06em'})
      + cutout('Product render', 'xppro_thermal', 1440, 150, 420, 812)
      + logo(220, WHITE, l=M, t=M)
      + headline(230, 'Nine palettes—', 'one clear picture for every job.', w=1040)
      + callouts([('palette-grid', 'Palettes', 'Nine'), ('light-conditions', 'Conditions', 'Any light'), ('clear-view', 'Result', 'Clear image')], 600, w=1040)
      + flir())
cover('blog-palettes', 'Palette Selector', BLACK, c5,
      'Caption: Every surface, material and light condition shows heat differently. Choose from nine palettes to get the clearest image for the job in front of you. sonimtech.com')
