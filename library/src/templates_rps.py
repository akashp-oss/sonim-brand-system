from gen import *

# Sonim's Rugged Performance Standards · social series (client file Sonim_RPS_social_series.docx, 2026-11-27).
# One 1080 x 1350 (4:5) visual per post. Every line on the artwork is taken from that post's copy (sentence case);
# images in the Word file ignored (brief). The brief has no Post 8; post numbers follow the brief.
#
# Round 3 (client: icons and white tiles looked random and clunky, numbers placed randomly): ONE fixed grid for
# every post, so each element sits in the same place on every artwork.
#   Visual zone   y 0–620    photo, split photo or a diagram of the spec (the only thing that changes)
#   RPS icon      x 920–1000, y 680–760, on the page, no tile; same spot on every post
#   Label         y 680       red, with the page notch
#   Headline      y 722       60 px, up to three lines
#   Spec number   y 950       150 px stat, red, always left-aligned on the margin
#   Spec line     y 1110      32 px, one line, from the copy
#   Footer        logo bottom-left, "Rugged Performance Standards" bottom-right
F = []
SECTION_META_EXTRA = [('rps', 'Rugged Performance Standards · social',
                       'RPS social series, 4:5 (1080 × 1350): an intro post and one post per standard, on one fixed grid: '
                       'a visual of the standard on top, then label, headline, spec number and spec line in the same place on every post.')]
X, M, W, H = 16, 80, 1080, 1350
VIS_H = 620                                   # visual zone height
Y_LABEL, Y_STAT, Y_LINE = 680, 950, 1110
STAT = 150

def post(n, name, visual, key, headline, stat, line, use, stat_size=STAT):
    spec = (text('Spec number', stat, 'stat abs', RED, stat_size, {'left': px(M), 'top': px(Y_STAT)}) if stat else '')
    line_css = {'left': px(M), 'top': px(Y_LINE if stat else Y_STAT), 'width': '920px'}
    inner = (visual
             + page_notch(X, Y_LABEL)
             + stack('Headline block', [text('Label', name, 'label', RED, 30), text('Headline', headline, 'h1', BLACK, 60)], l=M, t=Y_LABEL, w=820, gap=12)
             + box('RPS icon', l=W - M - 80, t=Y_LABEL, w=80, h=80, cls='group', inner=icon(key, 80, key))
             + spec
             + text('Spec line', line, 'h2 abs' if not stat else 'h3 abs', BLACK, 48 if not stat else 32, line_css)
             + logo(170, BLACK, l=M, b=M)
             + text('Series', 'Rugged Performance Standards', 'meta abs', BLACK, 22, {'right': px(M), 'bottom': '92px'}))
    F.append(('rps', artboard(f'rps-{n:02d}', f'RPS · {n:02d} {name}', W, H, WHITE, inner, use, 'post')))

def scene(img, pos):
    return photo('Scene photo', img, 0, 0, W, VIS_H, pos)

# ---------------------------------------------------------------- 1 · intro: the 12 standards as a grid of official icons
RPS = ['rps-drop', 'rps-waterproof', 'rps-dustproof', 'rps-temp', 'rps-shock', 'rps-audio',
       'rps-glove', 'rps-puncture', 'rps-chemical', 'rps-pressure', 'rps-dual-battery', 'rps-general']
IC, COLS, ROWS = 120, 4, 3
gx = [round(M + (920 - IC) * i / (COLS - 1)) for i in range(COLS)]
gy = [round(80 + (VIS_H - 160 - IC) * j / (ROWS - 1)) for j in range(ROWS)]
grid = fill('Visual panel', GRAY, l=0, t=0, w=W, h=VIS_H) + ''.join(
    box(k, l=gx[i % COLS], t=gy[i // COLS], w=IC, h=IC, cls='group', inner=icon(k, IC, k)) for i, k in enumerate(RPS))
post(1, 'Rugged Performance Standards', grid, 'rps-general', 'When the job is mission-critical, **your device can’t be the weak link.**',
     '12', 'Benchmarks for durability and endurance', 'Post 1 · intro: the 12 official RPS icons on an even grid')

# ---------------------------------------------------------------- 2 · waterproof: submersion diagram
wave = (f'<svg data-name="Water surface" width="{W}" height="40" viewBox="0 0 {W} 40" class="abs" style="left:0;top:150px">'
        f'<path d="M0 20 Q 67.5 0 135 20 T 270 20 T 405 20 T 540 20 T 675 20 T 810 20 T 945 20 T 1080 20 V40 H0Z" fill="{GRAY}"/></svg>')
water = (wave + fill('Water', GRAY, l=0, t=188, w=W, h=VIS_H - 188)
         + cutout('XP5plus 5G', 'xp5', 420, 250, 196, 370)
         + fill('Depth line', BLACK, l=760, t=170, w=4, h=450) + fill('Tick top', BLACK, l=740, t=170, w=44, h=4)
         + text('Depth', '6.5 ft', 'h2 abs', BLACK, 40, {'left': '800px', 'top': '370px'}))
post(2, 'Waterproof', water, 'rps-waterproof', 'When severe weather moves in, **the mission doesn’t stop.**',
     'IPX8', 'Freshwater submersion up to 6.5 feet for 30 minutes', 'Post 2 · Waterproof: submersion diagram')

# ---------------------------------------------------------------- 3 · extreme temperatures: cold and heat side by side
split = photo('Cold', 'rescue', 0, 0, W // 2 - 3, VIS_H, '40% 40%') + photo('Heat', 'structure_fire', W // 2 + 3, 0, W // 2 - 3, VIS_H, '50% 50%')
post(3, 'Extreme temperatures', split, 'rps-temp', 'Sonim is built for **the extremes.**',
     '-4°F to 131°F', 'With a 4900mAh Li-Ion quick-charge battery', 'Post 3 · Extreme temperatures: cold and heat photos', stat_size=120)

post(4, 'Glove-friendly', scene('rps_glove', '62% 40%'), 'rps-glove', 'Sonim is designed to work with **the way teams actually work.**',
     None, 'Large, glove-friendly physical keys', 'Post 4 · Glove-friendly: responder in full gear')
post(5, 'Dust-tight', scene('rps_field', '50% 45%'), 'rps-dustproof', 'Sonim is built to **keep the dust out.**',
     'IP6X', 'Completely dust-tight', 'Post 5 · Dust-tight: field crew in smoke and debris')
post(6, 'Drop resistant', scene('electrician', '60% 40%'), 'rps-drop', 'Sonim is built to **take the fall.**',
     '2 m', 'Drops of up to 2 meters (6.5 feet) onto concrete', 'Post 6 · Drop resistant: work from a ladder')
post(7, 'Extra-loud audio', scene('heli', '50% 60%'), 'rps-audio', 'Sonim is built to **cut through the noise.**',
     '100dB+', 'Speaker performance with noise cancellation', 'Post 7 · Extra-loud audio: helicopter noise')
post(9, 'Shock and vibration', scene('paramedics', '50% 55%'), 'rps-shock', 'Sonim is engineered to stay strong **when the job gets rough.**',
     '30G', 'Sudden shocks of up to 30G, vibrations from 5Hz to 500Hz', 'Post 9 · Shock and vibration: vehicles on rough roads')

# ---------------------------------------------------------------- 10 · puncture: lens and housing callouts on the product
PX, PY, PS = 600, 40, 0.48               # render 620 x 1171 -> 298 x 562
pp = lambda ix, iy: (round(PX + ix * PS), round(PY + iy * PS))
lx, ly = pp(150, 560); hx, hy = pp(22, 940)
def leader(title, cy, to_x):
    return (text('Callout', title, 'h3 abs', BLACK, 32, {'left': px(M), 'top': px(cy - 20)})
            + fill('Leader line', BLACK, l=M + 400, t=cy - 1, w=to_x - M - 400, h=3) + fill('Marker', RED, l=to_x - 9, t=cy - 9, w=18, h=18))
puncture = (fill('Visual panel', GRAY, l=0, t=0, w=W, h=VIS_H) + cutout('XP5plus 5G', 'xp5', PX, PY, round(620 * PS), round(1171 * PS))
            + leader('Gorilla Glass lens', ly, lx) + leader('Hardened rubber housing', hy, hx + 6))
post(10, 'Puncture resistant', puncture, 'rps-puncture', 'Sonim is built with **protection where it counts.**',
     '4J', 'Impacts of up to 4J of energy', 'Post 10 · Puncture resistant: lens and housing callouts')

post(11, 'Oil and chemicals', scene('crew', '45% 45%'), 'rps-chemical', 'Sonim is built for **the realities of the job.**',
     None, 'Designed to resist petroleum oils and cleaning solvents', 'Post 11 · Oil and chemicals: cleaning between calls')

# ---------------------------------------------------------------- 12 · pressure: a load pressing down on the device
arrow = lambda x: (fill('Arrow', RED, l=x, t=300, w=14, h=56)
                   + f'<svg data-name="Arrow head" width="40" height="28" viewBox="0 0 40 28" class="abs" style="left:{x - 13}px;top:354px"><path d="M0 0H40L20 28Z" fill="{RED}"/></svg>')
press = (fill('Visual panel', GRAY, l=0, t=0, w=W, h=VIS_H)
         + f'<svg data-name="Load" width="500" height="200" viewBox="0 0 500 200" class="abs" style="left:290px;top:80px"><path d="M190 0H310V36H280V60H220V36H190Z M60 60H440L500 200H0Z" fill="{BLACK}"/></svg>'
         + ''.join(arrow(x) for x in (393, 533, 673))
         + cutout('XP5plus 5G', 'xp5', 482, 400, 116, 220) + fill('Ground', BLACK, l=M, t=VIS_H - 6, w=920, h=6))
post(12, 'Pressure resistant', press, 'rps-pressure', 'Sonim is built to take the pressure. **Literally.**',
     '1 ton', 'Loads of up to one metric ton', 'Post 12 · Pressure resistant: a load pressing on the device')
