from gen import *

# Sonim's Rugged Performance Standards · social series (client file Sonim_RPS_social_series.docx, 2026-11-27).
# One 1080 x 1350 (4:5) visual per post; the post copy carries the full text, the visual carries the hook and the spec.
# Every line on the artwork is taken from that post's copy (sentence case); images in the Word file ignored (brief).
# Icons: the official Sonim RPS set (brand/icons/sonim.json). Product: XP5plus render on Sonim Gray.
# The brief has no Post 8; post numbers follow the brief.
F = []
SECTION_META_EXTRA = [('rps', 'Rugged Performance Standards · social',
                       'RPS social series, 4:5 (1080 × 1350): an intro post and one post per standard, each with the '
                       'official RPS icon and the spec, on a scene photo, a red notch panel or a diagram of the spec.')]
X, M, W, H = 16, 80, 1080, 1350
SIGN = lambda c=BLACK: text('Series', 'Rugged Performance Standards', 'meta abs', c, 22, {'right': px(M), 'bottom': '92px'})

def post(n, name, bg, inner, use):
    F.append(('rps', artboard(f'rps-{n:02d}', f'RPS · {n:02d} {name}', W, H, bg, inner, use, 'post')))

# ---------------------------------------------------------------- Post 1 · intro: 12 benchmarks
RPS = ['rps-drop', 'rps-waterproof', 'rps-dustproof', 'rps-temp', 'rps-shock', 'rps-audio',
       'rps-glove', 'rps-puncture', 'rps-chemical', 'rps-pressure', 'rps-dual-battery', 'rps-general']
grid = box('RPS icons', l=M, t=730, w=920, cls='row', style={'flex-wrap': 'wrap', 'gap': '28px 26px', 'background': WHITE, 'padding': '36px 40px', 'box-sizing': 'border-box'}, inner=''.join(
    icon(k, 110, k).replace('height:110px"', 'height:110px;flex:none"', 1) for k in RPS))
c = (page_notch(X, 110, WHITE)
     + stack('Headline block', [text('Label', 'Rugged Performance Standards', 'label', WHITE, 30),
                                text('Headline', 'When the job is mission-critical, **your device can’t be the weak link.**', 'h1', WHITE, 70, {'--em': BLACK})], l=M, t=110, w=920, gap=16)
     + box('Stat row', l=M, t=500, w=920, cls='row', style={'gap': '32px', 'align-items': 'center'}, inner=
           text('Stat', '12', 'stat', WHITE, 230) + text('Caption', 'benchmarks for durability and endurance', 'h2', WHITE, 50, {'max-width': '560px'}))
     + grid
     + logo(170, WHITE, l=M, b=M) + SIGN(WHITE))
post(1, 'Intro', RED, c, 'Post 1 · the 12 benchmarks, with all 12 official RPS icons')

# ---------------------------------------------------------------- Posts 2–12 · one standard each
# Client feedback 2026-11-27: needs variation in images/visuals. Four layouts, each visual chosen to match its copy:
#   photo top   · a scene from the copy (gloved hands, smoke and debris, helicopter noise, cleaning between calls)
#   notch side  · full-height photo with a red Expanded Notch panel (ladder work, rough roads)
#   split       · cold and heat side by side (extreme temperatures)
#   graphic     · a diagram that shows the spec (submersion depth, a 1 ton load, protection callouts)
from templates_social import callout

def spec_row(key, stat, size, cap, ink=BLACK, tile=False):
    """Official RPS icon + the spec + its line from the copy, in one row."""
    ic = icon(key, 100, key).replace('px"', 'px;flex:none"', 1)
    if tile: ic = box('Icon tile', cls='stack', style={'background': WHITE, 'padding': '14px', 'flex': 'none'}, inner=ic)
    txt = ([text('Stat', stat, 'stat', RED if ink == BLACK else WHITE, size)] if stat else []) + [text('Caption', cap, 'h3', ink, 32)]
    return box('Spec', cls='row', style={'gap': '28px', 'align-items': 'center'}, inner=ic + box('Spec text', cls='stack', style={'gap': '8px'}, inner=''.join(txt)))

def head(label, headline, ink=BLACK, t=110, w=920, size=68):
    return stack('Headline block', [text('Label', label, 'label', RED if ink == BLACK else WHITE, 30),
                                    text('Headline', headline, 'h1', ink, size, {'--em': BLACK} if ink == WHITE else None)], l=M, t=t, w=w, gap=14)

def photo_top(n, name, img, pos, key, headline, stat, size, cap):
    c = (photo('Scene photo', img, 0, 0, W, 580, pos)
         + page_notch(X, 640) + head(name, headline, t=640)
         + stack('Spec block', [spec_row(key, stat, size, cap)], l=M, t=930, w=920)
         + logo(170, BLACK, l=M, b=M) + SIGN())
    post(n, name, WHITE, c, f'Post {n} · {name}: scene photo, official RPS icon and the spec')

def notch_side(n, name, img, pos, key, headline, stat, size, cap, extra=None):
    PW = 640
    inner = (head(name, headline, WHITE, t=110, w=PW - M - 40, size=64)
             + stack('Spec block', [box('Icon tile', cls='stack', style={'background': WHITE, 'padding': '16px', 'align-self': 'flex-start'}, inner=icon(key, 96, key)),
                                    text('Stat', stat, 'stat', WHITE, size, {'margin-top': '18px'}),
                                    text('Caption', cap, 'h3', WHITE, 32)] + ([text('Extra', extra, 'body', WHITE, 28, {'margin-top': '14px'})] if extra else []),
                     l=M, t=560, w=PW - M - 40, gap=8)
             + logo(170, WHITE, l=M, b=M))
    c = (photo('Scene photo', img, PW, 0, W - PW, H, pos)
         + xnotch('Expanded notch', 0, 0, PW, H, X, RED, inner, notch_top=2 * X + 94)
         + SIGN(WHITE))
    post(n, name, RED, c, f'Post {n} · {name}: full-height scene photo with a red Expanded Notch panel')

# ---- 2 · Waterproof: submersion diagram (device under 6.5 ft of water, 30 minutes)
wave = (f'<svg data-name="Water surface" width="920" height="40" viewBox="0 0 920 40" class="abs" style="left:{M}px;top:640px">'
        f'<path d="M0 20 Q 57.5 0 115 20 T 230 20 T 345 20 T 460 20 T 575 20 T 690 20 T 805 20 T 920 20 V40 H0Z" fill="{GRAY}"/></svg>')
ruler = (fill('Depth line', BLACK, l=M + 760, t=660, w=4, h=470)
         + fill('Tick top', BLACK, l=M + 740, t=660, w=44, h=4) + fill('Tick bottom', BLACK, l=M + 740, t=1126, w=44, h=4)
         + text('Depth', '6.5 ft', 'stat abs', RED, 88, {'left': f'{M + 520}px', 'top': '820px'})
         + text('Time', 'for 30 minutes', 'h3 abs', BLACK, 32, {'left': f'{M + 520}px', 'top': '920px'}))
c = (page_notch(X, 110) + head('Waterproof', 'When severe weather moves in, **the mission doesn’t stop.**')
     + stack('Spec block', [spec_row('rps-waterproof', 'IPX8', 150, 'Freshwater submersion')], l=M, t=420, w=920)
     + wave + fill('Water', GRAY, l=M, t=678, w=920, h=482)
     + cutout('XP5plus 5G', 'xp5', M + 120, 740, 210, 397) + ruler
     + logo(170, BLACK, l=M, b=M) + SIGN())
post(2, 'Waterproof', WHITE, c, 'Post 2 · Waterproof: submersion diagram, 6.5 ft for 30 minutes')

# ---- 3 · Extreme temperatures: cold and heat, split
half = W // 2
c = (photo('Cold', 'rescue', 0, 0, half - 3, 620, '40% 40%') + photo('Heat', 'structure_fire', half + 3, 0, half - 3, 620, '50% 50%')
     + text('Cold stat', '-4°F', 'stat abs', WHITE, 150, {'left': f'{M}px', 'top': '450px'})
     + text('Heat stat', '131°F', 'stat abs', WHITE, 150, {'left': f'{half + 48}px', 'top': '450px'})
     + page_notch(X, 680) + head('Extreme temperatures', 'Sonim is built for **the extremes.**', t=680)
     + stack('Spec block', [spec_row('rps-temp', None, 0, 'Fully operational from freezing cold to intense heat'),
                            box('Extra', cls='row', style={'gap': '18px', 'align-items': 'center', 'margin-top': '22px'}, inner=
                                icon('battery-general', 64, 'Battery').replace('px"', 'px;flex:none"', 1) + text('Extra text', '4900mAh Li-Ion quick-charge battery', 'body', BLACK, 28))],
             l=M, t=900, w=920)
     + logo(170, BLACK, l=M, b=M) + SIGN())
post(3, 'Extreme temperatures', WHITE, c, 'Post 3 · Extreme temperatures: cold and heat photos side by side')

photo_top(4, 'Glove-friendly', 'rps_glove', '62% 40%', 'rps-glove', 'Sonim is designed to work with **the way teams actually work.**', None, 0, 'Large, glove-friendly physical keys')
photo_top(5, 'Dust-tight', 'rps_field', '50% 45%', 'rps-dustproof', 'Sonim is built to **keep the dust out.**', 'IP6X', 130, 'Completely dust-tight')
notch_side(6, 'Drop resistant', 'electrician', '62% 50%', 'rps-drop', 'Sonim is built to **take the fall.**', '2 m', 190, 'Drops of up to 2 meters (6.5 feet) onto concrete')
photo_top(7, 'Extra-loud audio', 'heli', '50% 60%', 'rps-audio', 'Sonim is built to **cut through the noise.**', '100dB+', 120, 'Speaker performance and noise cancellation')
notch_side(9, 'Shock and vibration', 'paramedics', '48% 50%', 'rps-shock', 'Sonim is engineered to stay strong **when the job gets rough.**', '30G', 190, 'Sudden shocks of up to 30G', 'Vibrations from 5Hz to 500Hz')

# ---- 10 · Puncture resistant: protection callouts on a large product render
PX, PY, PS = 620, 470, 0.6           # render 620 x 1171
pp = lambda ix, iy: (round(PX + ix * PS), round(PY + iy * PS))
gx, gy = pp(140, 560); hx, hy = pp(24, 900)
c = (fill('Product panel', GRAY, l=0, t=300, w=W, h=H - 300)
     + cutout('XP5plus 5G', 'xp5', PX, PY, round(620 * PS), round(1171 * PS))
     + page_notch(X, 110) + head('Puncture resistant', 'Sonim is built with **protection where it counts.**')
     + stack('Spec block', [box('Icon tile', cls='stack', style={'background': WHITE, 'padding': '14px', 'align-self': 'flex-start'}, inner=icon('rps-puncture', 96, 'rps-puncture')),
                            text('Stat', '4J', 'stat', RED, 190, {'margin-top': '14px'}), text('Caption', 'Impacts of up to 4J of energy', 'h3', BLACK, 32)], l=M, t=360, w=420, gap=8)
     + callout('Gorilla Glass lens', 'Protects the display', M, gy, 300, gx, 30, 24)
     + callout('Hardened rubber housing', 'Built for knocks', M, hy, 300, hx + 6, 30, 24)
     + logo(170, BLACK, l=M, b=M) + SIGN())
post(10, 'Puncture resistant', WHITE, c, 'Post 10 · Puncture resistant: callouts on the lens and housing')

photo_top(11, 'Oil and chemicals', 'crew', '45% 45%', 'rps-chemical', 'Sonim is built for **the realities of the job.**', None, 0, 'Designed to resist petroleum oils and cleaning solvents')

# ---- 12 · Pressure resistant: a 1 ton load on the device
c = (page_notch(X, 110) + head('Pressure resistant', 'Sonim is built to take the pressure. **Literally.**')
     + stack('Spec block', [spec_row('rps-pressure', None, 0, 'Loads of up to one metric ton')], l=M, t=420, w=920)
     + fill('Load', BLACK, l=430, t=600, w=520, h=210)
     + text('Load label', '1 ton', 'stat abs', WHITE, 140, {'left': '470px', 'top': '638px'})
     + ''.join(fill('Arrow', RED, l=x, t=830, w=14, h=60) + f'<svg data-name="Arrow head" width="40" height="28" viewBox="0 0 40 28" class="abs" style="left:{x - 13}px;top:888px"><path d="M0 0H40L20 28Z" fill="{RED}"/></svg>' for x in (520, 683, 846))
     + fill('Ground', BLACK, l=M, t=1150, w=920, h=6)
     + cutout('XP5plus 5G', 'xp5', 600, 930, 116, 220)
     + logo(170, BLACK, l=M, b=M) + SIGN())
post(12, 'Pressure resistant', GRAY, c, 'Post 12 · Pressure resistant: a 1 ton load pressing on the device')
