from gen import *

# ============================================================================
# SOCIAL VARIATIONS — post types informed by competitor research
# (docs/competitor-social-research.md): spec callout, durability proof, numbered
# list, testimonial with portrait, partner lockup, launch teaser, lineup, how-to,
# hiring, carousel (cover + inner + end), countdown and poll stories, customer
# proof card, LinkedIn document cover.
# Same system as templates.py: one notch per artboard (page notch OR Rugged
# Container OR Expanded Notch), label -> headline -> body -> logo on the margin.
# Facts only from CONTEXT.md §8 with their source; everything else is a placeholder.
# ============================================================================

F = []
SECTION_META_EXTRA = [
    ('carousel', 'Carousels', 'Swipeable 4:5 sets for Instagram and LinkedIn: a cover that hooks, one idea per inner slide, an end slide with the call to action.'),
]


def hairline(name='Hairline', color=GRAY, h=2):
    return box(name, cls='shape', style={'background': color, 'height': px(h), 'flex': 'none', 'align-self': 'stretch'})


def spacer(h=None):
    return box('Spacer', style={'flex': '1' if h is None else 'none', 'height': px(h) if h else None})


def callout(title, detail, l, cy, w, px_to, size=32, dsize=24):
    """Spec callout: text block on the left, leader line running right to a red marker on the product."""
    blk_h = round(size * 1.2 + dsize * 1.45 + 6)
    t = cy - round(size * 0.6)
    txt = stack(f'{title} text', [text('Title', title, 'h3', BLACK, size), text('Detail', detail, 'body', BLACK, dsize)], l=l, t=t, w=w, gap=6)
    line_l = l + w + 16
    line = fill('Leader line', BLACK, l=line_l, t=cy - 1, w=px_to - line_l, h=3)
    mark = fill('Marker', RED, l=px_to - 9, t=cy - 9, w=18, h=18)
    return box(f'Callout · {title}', l=0, t=0, w=1, h=1, cls='group', inner=txt + line + mark)


def item(key, title, detail, size, tsize, dsize, gap):
    """icon_item with a non-shrinking icon so text columns align."""
    return icon_item(key, title, detail, size, tsize, dsize, gap).replace(f'style="width:{size}px;height:{size}px"', f'style="width:{size}px;height:{size}px;flex:none"', 1)


def counter(label, color, r, b, size=24):
    return text('Slide counter', label, 'meta abs', color, size, {'right': px(r), 'bottom': px(b)})


def swipe(color, r, b, size=28):
    return box('Swipe cue', r=r, b=b, cls='row', style={'gap': '12px', 'align-items': 'center', 'color': color},
               inner=text('Swipe', 'Swipe', 'h3', color, size) + box('Arrow', cls='icon', w=size + 6, h=size + 6, inner=ICONS['arrow'].replace('<svg ', '<svg data-name="Arrow icon" ', 1)))


# ---------------------------------------------------------------- INSTAGRAM POSTS
X, M = 16, 80

# 1 · Spec callout with leader lines (Zebra / Honeywell / Samsung "feature annotation" posts)
PL, PT, PS = 600, 300, 0.74          # product render position and scale (render is 620 x 1171)
def pp(ix, iy): return round(PL + ix * PS), round(PT + iy * PS)
sx, sy = pp(320, 196); tx_, ty = pp(97, 473); hx, hy = pp(100, 750); kx, ky = pp(205, 993)
a = (cutout('Product render', 'xp5', PL, PT, round(620 * PS), round(1171 * PS))
     + page_notch(X, 110)
     + stack('Headline block', [text('Label', 'Sonim XP5plus 5G', 'label', RED, 30), text('Headline', 'Every detail\n**has a job.**', 'h1', BLACK, 92)], l=M, t=110, w=560, gap=12)
     + callout('100 dB+ speakers', 'Dual, front facing', M, sy, 380, sx)
     + callout('Side push-to-talk', 'AT&T Enhanced PTT ready', M, ty, 380, tx_)
     + callout('Rugged housing', 'IP68, IPx9K, MIL-STD-810H', M, hy, 380, hx)
     + callout('Glove-friendly keypad', 'Large, tactile keys', M, ky, 380, kx)
     + logo(170, BLACK, l=M, b=M) + text('Source', 'Source: sonimtech.com', 'small abs', BLACK, 22, {'right': px(M), 'bottom': '86px'}))
F.append(('ig', artboard('ig-spec', 'Instagram post · Spec callout', 1080, 1350, GRAY, a, 'Feed 4:5 · product with leader-line annotations', 'post')))

# 2 · Durability proof (Kyocera / Cat / Crosscall torture-test posts, told with ratings instead of stunts)
rows = [('IP68', 'Dust tight and protected against continuous immersion.'),
        ('IPx9K', 'Protected against high-pressure, high-temperature water jets.'),
        ('MIL-STD-810H', 'U.S. Department of Defense environmental test standard.')]
rating_items = []
for i, (k, d) in enumerate(rows):
    rating_items.append(stack(k, [text('Rating', k, 'stat', RED, 116), text('Meaning', d, 'body', BLACK, 30)], gap=14))
    if i < len(rows) - 1:
        rating_items.append(hairline('Hairline', WHITE, 3))
a = (cutout('Product render', 'xp5', 790, 110, 210, 397)
     + page_notch(X, 120)
     + stack('Headline block', [text('Label', 'Designed to endure', 'label', RED, 30), text('Headline', 'Tested so your crew\n**doesn’t have to.**', 'h1', BLACK, 76)], l=M, t=120, w=700, gap=12)
     + stack('Ratings', rating_items, l=M, t=420, w=920, gap=38)
     + logo(170, BLACK, l=M, b=M) + text('Source', 'XP5plus 5G ratings. Source: sonimtech.com', 'small abs', BLACK, 22, {'right': px(M), 'bottom': '86px'}))
F.append(('ig', artboard('ig-durability', 'Instagram post · Durability proof', 1080, 1350, GRAY, a, 'Feed 4:5 · certifications as proof, product on Sonim Gray', 'post')))

# 3 · Numbered list "3 reasons" (the most common B2B list post)
reasons = [('01', 'Push-to-talk, built in.', 'A side PTT key with AT&T Enhanced PTT, FirstNet Rapid Response and FirstNet MCPTT via Fusion.'),
           ('02', 'Power you can swap.', 'A removable 3,500 mAh battery with up to 25 hours of talk time.'),
           ('03', 'Heard over the noise.', '100 dB+ dual front speakers and a glove-friendly keypad.')]
items = []
for i, (n, t_, d) in enumerate(reasons):
    items.append(hairline())
    items.append(box(f'Reason {n}', cls='row', style={'gap': '36px', 'align-items': 'flex-start'},
                     inner=text('Number', n, 'stat', RED, 88, {'width': '130px', 'flex': 'none'})
                     + stack('Text', [text('Title', t_, 'h2', BLACK, 48), text('Detail', d, 'body', BLACK, 30)], gap=12, style={'flex': '1'})))
a = (page_notch(X, 110)
     + stack('Headline block', [text('Label', 'Sonim XP5plus 5G', 'label', RED, 30), text('Headline', 'Three reasons it\n**belongs on shift.**', 'h1', BLACK, 84)], l=M, t=110, w=920, gap=12)
     + stack('Reasons', items, l=M, t=390, w=920, gap=44)
     + logo(170, BLACK, l=M, b=M) + text('Source', 'Source: sonimtech.com', 'small abs', BLACK, 22, {'right': px(M), 'bottom': '86px'}))
F.append(('ig', artboard('ig-reasons', 'Instagram post · Three reasons', 1080, 1350, WHITE, a, 'Feed 4:5 · numbered list on white', 'post')))

# 4 · Testimonial with portrait (FirstNet / Getac / Motorola customer voices)
a = (photo('Portrait photo', 'responder', M, M, 440, 560, '40% 30%')
     + stack('Attribution', [text('Name', 'Name Surname', 'h2', BLACK, 40), text('Title', 'Title, Organisation\nCity, ST', 'body', BLACK, 28)], l=560, b=1350 - M - 560, w=440, gap=8)
     + page_notch(X, 710)
     + stack('Quote block', [text('Label', 'Customer story', 'label', RED, 30),
                             text('Quote', '“Customer quote in one or two short sentences, with the **key phrase in red.**”', 'quote', BLACK, 70)], l=M, t=710, w=920, gap=18)
     + logo(170, BLACK, l=M, b=M) + text('CTA', 'Read the story at sonimtech.com', 'h3 abs', BLACK, 26, {'right': px(M), 'bottom': '86px'}))
F.append(('ig', artboard('ig-testimonial', 'Instagram post · Testimonial with portrait', 1080, 1350, GRAY, a, 'Feed 4:5 · replace portrait, quote and name; get written approval', 'post')))

# 5 · Partner announcement with lockup (Motorola / Panasonic / Samsung partner posts)
lock = box('Partner lockup', l=M, b=M, cls='row', style={'gap': '36px', 'align-items': 'center'},
           inner=logo(180, WHITE) + fill('Divider', WHITE, w=3, h=72, style={'flex': 'none'})
           + box('Partner logo', cls='stack', w=220, h=72, style={'border': '3px solid #FFFFFF', 'justify-content': 'center', 'padding': '0 20px', 'flex': 'none'},
                 inner=text('Partner logo placeholder', 'Partner logo', 'h3', WHITE, 26)))
a = (page_notch(X, 120, WHITE)
     + stack('Headline block', [text('Label', 'Partnership', 'label', WHITE, 30),
                                text('Headline', 'Now working\ntogether with\n**Partner name.**', 'h1', WHITE, 112, {'--em': BLACK}),
                                text('Body', 'One sentence on what the partnership means for crews in the field.', 'lead', WHITE, 38, {'margin-top': '26px', 'max-width': '800px'})], l=M, t=120, w=920, gap=14)
     + lock)
F.append(('ig', artboard('ig-partner', 'Instagram post · Partner announcement', 1080, 1080, RED, a, 'Square 1:1 · Sonim + partner lockup, both single colour', 'post')))

# 6 · Launch teaser (partial product reveal + date)
a = (cutout('Product render (cropped)', 'xp5', 560, 860, 460, 869)
     + page_notch(X, 120)
     + stack('Headline block', [text('Label', 'Coming soon', 'label', RED, 30),
                                text('Headline', 'Something\nnew is\n**on its way.**', 'display', BLACK, 150),
                                text('Date', 'Month 00, 2027', 'h2', BLACK, 52, {'margin-top': '28px'})], l=M, t=120, w=920, gap=14)
     + logo(170, BLACK, l=M, b=M))
F.append(('ig', artboard('ig-teaser', 'Instagram post · Launch teaser', 1080, 1350, GRAY, a, 'Feed 4:5 · partial product reveal, cropped by the frame', 'post')))

# 7 · Product lineup (portfolio posts)
lineup = [('xp5', 'XP5plus 5G', 'Rugged 5G phone with side push-to-talk.'),
          ('mega', 'MegaConnect', 'Ultra-portable 5G HPUE hotspot.'),
          ('rsm', 'Klein VALOR RSM', 'Remote speaker mic from accessory partner Klein.')]
tiles = ''.join(
    f'<div class="stack" data-name="{n}" style="background:{WHITE};padding:28px;gap:10px;width:293px;flex:none">'
    f'<div class="photo-frame" data-name="Product frame" style="width:237px;height:420px">{cutout("Product render", k, 0, 0, 237, 420)}</div>'
    f'{text("Name", n, "h3", BLACK, 30, {"margin-top": "14px"})}{text("Detail", d, "body", BLACK, 23)}</div>'
    for k, n, d in lineup)
a = (page_notch(X, 110)
     + stack('Headline block', [text('Label', 'The lineup', 'label', RED, 30), text('Headline', 'One system for\n**the whole shift.**', 'h1', BLACK, 84)], l=M, t=110, w=920, gap=12)
     + box('Product tiles', l=M, t=400, w=920, cls='row', style={'gap': '20px', 'align-items': 'stretch'}, inner=tiles)
     + logo(170, BLACK, l=M, b=M) + text('URL', 'sonimtech.com', 'h3 abs', BLACK, 26, {'right': px(M), 'bottom': '86px'}))
F.append(('ig', artboard('ig-lineup', 'Instagram post · Product lineup', 1080, 1350, GRAY, a, 'Feed 4:5 · three products in white tiles', 'post')))

# 8 · How-to / tip (software explainer posts)
steps = [('cloud', 'SonimWare Cloud', 'Remote setup, updates and monitoring.'),
         ('software', 'SonimWare SCOUT', 'SafeGuard, Kiosk Mode, MDM Helper and App Updater.'),
         ('dispatch', 'Kodiak dispatch', 'Web console, push-to-talk, talkgroups and GPS.')]
a = (page_notch(X, 100)
     + stack('Headline block', [text('Label', 'How to', 'label', RED, 28), text('Headline', 'Manage every\ndevice **remotely.**', 'h1', BLACK, 80)], l=M, t=100, w=920, gap=12)
     + stack('Steps', sum([[hairline(), item(k, t_, d, 80, 40, 30, 36)] for k, t_, d in steps], []), l=M, t=380, w=920, gap=34)
     + logo(160, BLACK, l=M, b=M) + text('Source', 'Source: sonimtech.com; Kodiak', 'small abs', BLACK, 20, {'right': px(M), 'bottom': '86px'}))
F.append(('ig', artboard('ig-howto', 'Instagram post · How-to', 1080, 1080, WHITE, a, 'Square 1:1 · three icon steps on white', 'post')))

# 9 · Hiring / culture (Motorola / Zebra "join the team" posts)
roles = []
for r_ in ['Job title · City, ST', 'Job title · City, ST', 'Job title · Remote']:
    roles.append(hairline())
    roles.append(box('Role', cls='row', style={'justify-content': 'space-between', 'align-items': 'center'},
                     inner=text('Role', r_, 'h3', BLACK, 32) + box('Arrow', cls='icon', w=34, h=34, inner=ICONS['arrow'].replace('<svg ', '<svg data-name="Arrow icon" style="color:#CF102D" ', 1))))
a = (photo('Team photo', 'team', 0, 0, 1080, 560, '50% 40%')
     + page_notch(X, 620)
     + stack('Headline block', [text('Label', 'We’re hiring', 'label', RED, 30), text('Headline', 'Build tools for\n**those who serve.**', 'h1', BLACK, 80)], l=M, t=620, w=920, gap=12)
     + stack('Open roles', roles, l=M, t=880, w=920, gap=22)
     + logo(170, BLACK, l=M, b=M) + text('CTA', 'Apply at sonimtech.com', 'h3 abs', BLACK, 26, {'right': px(M), 'bottom': '86px'}))
F.append(('ig', artboard('ig-hiring', 'Instagram post · Hiring', 1080, 1350, WHITE, a, 'Feed 4:5 · team photo with open roles; replace with your own team', 'post')))

# ---------------------------------------------------------------- CAROUSEL (4 slides, 1080 x 1350)
c = (photo('Cover photo', 'paramedics', 0, 0, 1080, 640, '50% 55%')
     + page_notch(X, 700)
     + stack('Headline block', [text('Label', 'White paper highlights', 'label', RED, 30),
                                text('Headline', 'Connected care\n**in motion.**', 'display', BLACK, 118),
                                text('Body', 'What changes when EMS treats communications as a mobility platform.', 'lead', BLACK, 34, {'margin-top': '14px', 'max-width': '760px'})], l=M, t=700, w=920, gap=12)
     + logo(170, BLACK, l=M, b=M) + swipe(RED, M, 88))
F.append(('carousel', artboard('carousel-cover', 'Carousel · 1 Cover', 1080, 1350, WHITE, c, 'Slide 1 of 4 · hook with photo and swipe cue', 'post')))

stat_tile = lambda n, cap, w: (f'<div class="stack" data-name="{esc(cap)}" style="background:{WHITE};padding:44px 36px;gap:18px;width:{w}px;flex:none">'
                               + text('Number', n, 'stat', RED, 104) + text('Caption', cap, 'body', BLACK, 30) + '</div>')
c = (page_notch(X, 110)
     + stack('Headline block', [text('Label', 'The challenge', 'label', RED, 30), text('Headline', 'Distance still\n**decides the wait.**', 'h1', BLACK, 92)], l=M, t=110, w=920, gap=12)
     + stack('Comparison', [
           box('Stat pair', cls='row', style={'gap': '20px'},
               inner=stat_tile('~7 min', 'Median EMS response time across 1.7M runs.', 450) + stat_tile('~13 min', 'Median EMS response time in rural areas.', 450)),
           box('Callout tile', cls='stack', style={'background': WHITE, 'padding': '44px 36px', 'gap': '10px'},
               inner=text('Callout', 'About **1 in 10** rural calls waited around 30 minutes.', 'h2', BLACK, 58)),
           text('Source', 'Source: Mell HK et al., JAMA Surgery, 2017.', 'small', BLACK, 22, {'margin-top': '16px'})], l=M, t=440, w=920, gap=24)
     + logo(170, BLACK, l=M, b=M) + counter('2 / 4', BLACK, M, 88))
F.append(('carousel', artboard('carousel-compare', 'Carousel · 2 Comparison', 1080, 1350, GRAY, c, 'Slide 2 of 4 · two sourced numbers side by side', 'post')))

stack_items = [('devices', 'XP5plus 5G', 'Rugged 5G phone with side PTT and a top SOS key.'),
               ('megarange', 'MegaConnect', '5G HPUE hotspot: Power Class 1 on Band 14, up to 64 Wi-Fi devices.'),
               ('cloud', 'SonimWare', 'Remote setup, updates and monitoring for the fleet.')]
c = (page_notch(X, 110)
     + stack('Headline block', [text('Label', 'The shift', 'label', RED, 30), text('Headline', 'From a radio problem\nto a **mobility platform.**', 'h1', BLACK, 76)], l=M, t=110, w=920, gap=12)
     + stack('Solution stack', [item(k, t_, d, 96, 44, 32, 36) for k, t_, d in stack_items], l=M, t=410, w=920, gap=64)
     + text('Source', 'Source: sonimtech.com; firstnet.com', 'small abs', BLACK, 22, {'left': px(M), 'top': '1030px'})
     + logo(170, BLACK, l=M, b=M) + counter('3 / 4', BLACK, M, 88))
F.append(('carousel', artboard('carousel-points', 'Carousel · 3 Key points', 1080, 1350, WHITE, c, 'Slide 3 of 4 · one idea, three icon points', 'post')))

c = (page_notch(X, 360, WHITE)
     + stack('Headline block', [text('Label', 'Read more', 'label', WHITE, 30),
                                text('Headline', 'Get the full\n**white paper.**', 'display', WHITE, 130, {'--em': BLACK}),
                                text('Body', 'Case studies, use cases and the complete EMS solution stack.', 'lead', WHITE, 36, {'margin-top': '22px', 'max-width': '760px'}),
                                text('CTA', 'sonimtech.com', 'h2', WHITE, 52, {'margin-top': '40px'})], l=M, t=360, w=920, gap=14)
     + logo(180, WHITE, l=M, b=M) + counter('4 / 4', WHITE, M, 88))
F.append(('carousel', artboard('carousel-end', 'Carousel · 4 End slide', 1080, 1350, RED, c, 'Slide 4 of 4 · call to action on Sonim Red', 'post')))

# ---------------------------------------------------------------- STORIES 1080 x 1920
X, M = 16, 80
SAFE_T, SAFE_B = 250, 340

s = (page_notch(X, SAFE_T, WHITE)
     + stack('Countdown block', [text('Label', 'Countdown', 'label', WHITE, 34),
                                 text('Number', '3', 'stat', WHITE, 520, {'margin-top': '10px'}),
                                 text('Unit', 'days to go.', 'h1', WHITE, 110, {'margin-top': '-10px'}),
                                 text('Headline', 'Meet us at\n**Event name 2027.**', 'h1', WHITE, 76, {'margin-top': '60px', '--em': BLACK}),
                                 text('Details', 'Booth 000 · Month 00–00 · City, ST', 'lead', WHITE, 36, {'margin-top': '20px'})], l=M, t=SAFE_T, w=920, gap=8)
     + logo(170, WHITE, l=M, b=SAFE_B + 20))
F.append(('stories', artboard('story-countdown', 'Instagram story · Event countdown', 1080, 1920, RED, s, '9:16 · change the number daily; add the countdown sticker in the app', 'story')))

opt = lambda k, t_, n: (f'<div class="stack" data-name="Option {n}" style="background:{GRAY};padding:36px;gap:22px;width:450px;flex:none">'
                        + icon(k, 88, t_) + text('Option', t_, 'h2', BLACK, 44) + '</div>')
s = (photo('Story photo', 'radio', 0, 0, 1080, 820, '55% 50%')
     + page_notch(X, 880)
     + stack('Headline block', [text('Label', 'Your call', 'label', RED, 32), text('Headline', 'What matters most\n**on a long shift?**', 'h1', BLACK, 80)], l=M, t=880, w=920, gap=12)
     + box('Options', l=M, t=1130, w=920, cls='row', style={'gap': '20px'}, inner=opt('battery', 'Battery life', 'A') + opt('voice', 'Loud, clear audio', 'B'))
     + logo(170, BLACK, l=M, b=SAFE_B + 20))
F.append(('stories', artboard('story-poll', 'Instagram story · This or that poll', 1080, 1920, WHITE, s, '9:16 · add the poll sticker in the clear space below the options', 'story')))

# ---------------------------------------------------------------- SOCIAL (landscape + LinkedIn document)
X, M = 12, 64
so = (photo('Background photo', 'team', 0, 0, 1200, 627, '60% 45%')
      + rugged('Proof container', M, 56, 340, 515, X, RED,
               text('Label', 'Customer proof', 'label', WHITE, 20)
               + text('Number', '1,200', 'stat', WHITE, 104, {'margin-top': '14px'})
               + text('Caption', 'FirstNet-capable Sonim XP8 phones deployed by Global Medical Response for crisis response.', 'body', WHITE, 24, {'margin-top': '14px'})
               + spacer()
               + text('Source', 'Source: firstnet.com', 'small', WHITE, 15), pad=30)
      + logo(120, WHITE, r=M, b=M))
F.append(('social', artboard('so-proof', 'LinkedIn / Facebook · Customer proof', 1200, 627, BLACK, so, '1.91:1 · sourced number in a Rugged Container over photography', 'land')))

X, M = 16, 80
so = (photo('Side photo', 'heli_red', 810, 0, 270, 1350, '62% 50%')
      + xnotch('Expanded notch 75%', 0, 0, 810, 1350, X, RED,
               stack('Headline block', [text('Label', 'Guide · PDF', 'label', WHITE, 30),
                                        text('Headline', 'Replacing LMR\nwithout\n**starting over.**', 'display', WHITE, 88, {'--em': BLACK}),
                                        text('Body', 'A practical guide for public safety leaders planning the move to mission-critical mobility.', 'lead', WHITE, 34, {'margin-top': '24px', 'max-width': '620px'}),
                                        text('Meta', '00 pages · Month 2027', 'h3', WHITE, 28, {'margin-top': '30px'})], l=M, t=330, w=650, gap=14)
               + logo(180, WHITE, l=M, b=M), notch_top=330))
F.append(('social', artboard('so-doc-cover', 'LinkedIn · Document cover', 1080, 1350, WHITE, so, '4:5 PDF carousel cover · red Expanded Notch 75%', 'post')))
