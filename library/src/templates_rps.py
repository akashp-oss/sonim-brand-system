from gen import *

# Sonim's Rugged Performance Standards · social series (client file Sonim_RPS_social_series.docx, 2026-11-27).
# One 1080 x 1350 (4:5) visual per post; the post copy carries the full text, the visual carries the hook and the spec.
# Every line on the artwork is taken from that post's copy (sentence case); images in the Word file ignored (brief).
# Icons: the official Sonim RPS set (brand/icons/sonim.json). Product: XP5plus render on Sonim Gray.
# The brief has no Post 8; post numbers follow the brief.
F = []
SECTION_META_EXTRA = [('rps', 'Rugged Performance Standards · social',
                       'RPS social series, 4:5 (1080 × 1350): an intro post and one post per standard, each with the '
                       'official RPS icon, the spec as the hero and the XP5plus on Sonim Gray.')]
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
#  n, name, icon, headline (from the copy), stat (or None), stat size, caption, extra (icon, line) or None
SPECS = [
    (2, 'Waterproof', 'rps-waterproof', 'When severe weather moves in, **the mission doesn’t stop.**',
     'IPX8', 190, 'Freshwater submersion up to 6.5 feet for 30 minutes', None),
    (3, 'Extreme temperatures', 'rps-temp', 'Sonim is built for **the extremes.**',
     '-4°F to 131°F', 120, 'Fully operational from freezing cold to intense heat', ('battery-general', '4900mAh Li-Ion quick-charge battery')),
    (4, 'Glove-friendly', 'rps-glove', 'Sonim is designed to work with **the way teams actually work.**',
     None, 0, 'Large, glove-friendly physical keys', None),
    (5, 'Dust-tight', 'rps-dustproof', 'Sonim is built to **keep the dust out.**',
     'IP6X', 190, 'Completely dust-tight', None),
    (6, 'Drop resistant', 'rps-drop', 'Sonim is built to **take the fall.**',
     '2 m', 210, 'Drops of up to 2 meters (6.5 feet) onto concrete', None),
    (7, 'Extra-loud audio', 'rps-audio', 'Sonim is built to **cut through the noise.**',
     '100dB+', 134, 'Speaker performance and noise cancellation', None),
    (9, 'Shock and vibration', 'rps-shock', 'Sonim is engineered to stay strong **when the job gets rough.**',
     '30G', 210, 'Sudden shocks of up to 30G', (None, 'Vibrations from 5Hz to 500Hz')),
    (10, 'Puncture resistant', 'rps-puncture', 'Sonim is built with **protection where it counts.**',
     '4J', 210, 'Impacts of up to 4J of energy', (None, 'Gorilla Glass lens and hardened rubber housing')),
    (11, 'Oil and chemicals', 'rps-chemical', 'Sonim is built for **the realities of the job.**',
     None, 0, 'Designed to resist petroleum oils and cleaning solvents', None),
    (12, 'Pressure resistant', 'rps-pressure', 'Sonim is built to take the pressure. **Literally.**',
     '1 ton', 190, 'Loads of up to one metric ton', None),
]
COL = 520          # left column (spec); the product sits in the right column
for n, name, key, head, stat, size, cap, extra in SPECS:
    spec = [icon(key, 200 if stat is None else 128, name).replace('px"', 'px;flex:none"', 1)]
    if stat:
        spec.append(text('Stat', stat, 'stat', RED, size, {'margin-top': '12px'}))
        spec.append(text('Caption', cap, 'h3', BLACK, 34, {'margin-top': '8px'}))
    else:
        spec.append(text('Caption', cap, 'h2', BLACK, 52, {'margin-top': '20px'}))
    if extra:
        spec.append(box('Divider', cls='shape', style={'background': WHITE, 'height': '3px', 'margin': '20px 0 4px'}))
        spec.append(box('Extra', cls='row', style={'gap': '18px', 'align-items': 'center'}, inner=
                        (icon(extra[0], 64, extra[1]).replace('px"', 'px;flex:none"', 1) if extra[0] else fill('Bar', RED, style={'width': '6px', 'height': '34px', 'flex': 'none'}))
                        + text('Extra text', extra[1], 'body', BLACK, 28)))
    c = (page_notch(X, 110)
         + stack('Headline block', [text('Label', name, 'label', RED, 30), text('Headline', head, 'h1', BLACK, 70)], l=M, t=110, w=920, gap=16)
         + stack('Spec', spec, l=M, t=470, w=COL, gap=4)
         + cutout('XP5plus 5G', 'xp5', 650, 470, 352, 665)
         + logo(170, BLACK, l=M, b=M) + SIGN())
    post(n, name, GRAY, c, f'Post {n} · {name}: official RPS icon, spec from the copy, XP5plus on Sonim Gray')
