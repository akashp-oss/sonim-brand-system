from gen import *
from templates_social import counter, swipe, item

# Radio replacement blog · LinkedIn set (client brief 2026-11-24). Every artwork is 1080 x 1350 (4:5 portrait,
# LinkedIn feed and document-carousel size). Copy is the client's, verbatim; headings in sentence case (brand rule).
# No URL on artwork (the post text carries the link). Carrier names as text, no third-party logos.
# Devices: XP5plus (radio-style PTT) and XP Pro (img/xppro_ptt.png = brand/make_xppro_ptt.py: the client's render
# with a generic PTT screen). Product renders on Sonim Gray (brand rule). Photography only where it fits the story.
F = []
SECTION_META_EXTRA = [('radio', 'Radio replacement · LinkedIn',
                       'Radio replacement blog, LinkedIn 4:5 (1080 × 1350): a 6-slide carousel, a stat card, '
                       'myth vs. fact (an 8-slide reveal carousel, or three single cards) and a listicle. Upload the carousel as a PDF document post.')]
X, M, W, H = 16, 80, 1080, 1350

def post(aid, name, bg, inner, use):
    F.append(('radio', artboard(aid, name, W, H, bg, inner, use, 'post')))

def devices(l, t, h, name='Devices'):
    """XP5plus in front of the XP Pro, bottoms aligned. h = height of the taller device."""
    pw, ph = round(h * 450 / 870), h
    xw, xh = round(h * 0.86 * 620 / 1171), round(h * 0.86)
    return box(name, l=l, t=t, w=pw + xw - 40, h=h, cls='group', inner=
               cutout('XP Pro', 'xppro_ptt', 0, 0, pw, ph) + cutout('XP5plus 5G', 'xp5', pw - 40, h - xh, xw, xh))

# ================================================================ 1 · CAROUSEL "$130K or a smarter option?"
n_ = 6
c = (photo('Cover photo', 'radio', 0, 0, W, 520, '40% 45%')
     + page_notch(X, 580)
     + stack('Headline block', [text('Label', 'Radio replacement', 'label', RED, 30),
                                text('Stat', '$130K', 'stat', RED, 210, {'margin-top': '8px'}),
                                text('Headline', 'for two repeaters?\n**There’s a smarter way.**', 'h1', BLACK, 74)], l=M, t=580, w=920, gap=10)
     + logo(170, BLACK, l=M, b=M) + swipe(RED, M, 88))
post('rr-car-1', 'Radio carousel · 1 Cover', WHITE, c, f'Slide 1 of {n_} · the hook')

tower_tile = box('Quote tile', l=M, t=620, w=920, cls='stack', style={'background': WHITE, 'padding': '48px', 'gap': '28px'}, inner=
                 box('Repeaters', cls='row', style={'gap': '24px', 'align-items': 'center'}, inner=
                     icon('tower', 132, 'Repeater 1') + icon('tower', 132, 'Repeater 2')
                     + text('Plus', '+ radios', 'h2', BLACK, 48, {'margin-left': '12px'}))
                 + text('Number', '$130,000+', 'stat', RED, 150)
                 + text('Caption', 'Quoted to expand the radio system', 'body', BLACK, 30))
c = (page_notch(X, 120)
     + stack('Text block', [text('Label', 'The quote', 'label', RED, 30),
                            text('Body', 'A Midwest school bus fleet was quoted **$130,000+** to expand its radio system with just two repeaters and radios.', 'h2', BLACK, 56)],
             l=M, t=120, w=920, gap=16)
     + tower_tile
     + logo(170, BLACK, l=M, b=M) + counter(f'2 / {n_}', BLACK, M, 88))
post('rr-car-2', 'Radio carousel · 2 The quote', GRAY, c, f'Slide 2 of {n_} · the $130K radio quote')

c = (page_notch(X, 120)
     + stack('Headline block', [text('Label', 'The switch', 'label', RED, 30),
                                text('Headline', 'Instead, they switched to **rugged 5G phones** with push-to-talk over cellular.', 'h1', BLACK, 66)], l=M, t=120, w=920, gap=16)
     + fill('Product panel', GRAY, l=M, t=520, w=920, h=640)
     + devices(M + 210, 560, 560)
     + logo(170, BLACK, l=M, b=M) + counter(f'3 / {n_}', BLACK, M, 88))
post('rr-car-3', 'Radio carousel · 3 The switch', WHITE, c, f'Slide 3 of {n_} · XP Pro and XP5plus on Sonim Gray')

GAINS = [('lock', 'Encrypted communications'), ('gps', 'GPS location'), ('multiple-users', 'Multi-channel talk groups'),
         ('cloud', 'Cloud device management'), ('coverage', 'Coverage beyond radio range')]
c = (page_notch(X, 120)
     + stack('Headline block', [text('Label', 'The outcome', 'label', RED, 30),
                                text('Headline', 'What they **gained:**', 'h1', BLACK, 84)], l=M, t=120, w=920, gap=16)
     + stack('Gains', [item(k, t_, None, 112, 46, 0, 40).replace('align-items:flex-start', 'align-items:center') for k, t_ in GAINS], l=M, t=380, w=920, gap=48)
     + logo(170, BLACK, l=M, b=M) + counter(f'4 / {n_}', BLACK, M, 88))
post('rr-car-4', 'Radio carousel · 4 What they gained', WHITE, c, f'Slide 4 of {n_} · five gains with Sonim icons')

c = (page_notch(X, 440, WHITE)
     + stack('Headline block', [text('Label', 'The result', 'label', WHITE, 30),
                                text('Headline', '**Tens of thousands** saved in upfront infrastructure costs.', 'display', WHITE, 112, {'--em': BLACK})],
             l=M, t=440, w=920, gap=16)
     + logo(180, WHITE, l=M, b=M) + counter(f'5 / {n_}', WHITE, M, 88))
post('rr-car-5', 'Radio carousel · 5 The result', RED, c, f'Slide 5 of {n_} · the result on Sonim Red')

c = (page_notch(X, 160)
     + stack('Headline block', [text('Label', 'Your next step', 'label', RED, 30),
                                text('Headline', 'Go beyond\n**LMR.**', 'display', BLACK, 150),
                                text('CTA', 'Talk to our team.', 'h2', BLACK, 60, {'margin-top': '28px'})], l=M, t=160, w=920, gap=14)
     + devices(470, 620, 540)
     + logo(180, BLACK, l=M, b=M) + counter(f'6 / {n_}', BLACK, M, 88))
post('rr-car-6', 'Radio carousel · 6 End slide', GRAY, c, f'Slide 6 of {n_} · call to action, no URL (link in the post)')

# ================================================================ 2 · STAT CARD "$2,600 per device"
c = (page_notch(X, 120)
     + stack('Stat block', [text('Label', 'Per device', 'label', RED, 30),
                            text('Stat', '$2,600', 'stat', RED, 230, {'margin-top': '6px'}),
                            text('Subhead', 'Saved per device by switching from rented radios to **rugged push-to-talk phones.**', 'h2', BLACK, 52, {'margin-top': '12px'})],
             l=M, t=120, w=920, gap=10)
     + devices(560, 640, 520)
     + text('Footnote', 'Based on a customer’s own cost analysis.', 'small abs', BLACK, 22, {'left': px(M), 'top': '1100px', 'width': '420px'})
     + logo(170, BLACK, l=M, b=M))
post('rr-stat', 'Radio · Stat card $2,600', GRAY, c, 'Stat card · devices on Sonim Gray, footnote as sourced in the brief')

# ================================================================ 3 · MYTH VS. FACT
# Client feedback 2026-11-24: the struck-through cards didn't land. Research (LinkedIn carousel guides: one idea per
# slide, a hook cover, myth-per-page PDF carousels, "swipe to reveal" pacing) -> show each fact as a visual proof,
# not a second block of text. Two ways to post it, same visuals:
#   A · rr-mf-*  : one 8-slide carousel. Cover, then each myth as a "true or false?" slide and its fact as the reveal.
#   B · rr-myth-*: three single cards, myth small on top, the fact and its visual proof as the hero.
MYTHS = [('Going broadband means ripping out your radios.', 'Broadband push-to-talk connects with **virtually any LMR system.**'),
         ('Upgrading communications means a massive infrastructure bill.', 'One fleet avoided a **$130K+ radio expansion.**'),
         ('Push-to-talk over cellular only works on one network.', 'It works across **AT&T FirstNet, Verizon Frontline and T-Mobile T-Priority.**')]

def proof_interop(t, h):
    """Myth 1: the LMR system and broadband PTT, linked (no claim beyond the fact line)."""
    cw = 360
    side = lambda name, inner, cap: box(name, cls='stack', style={'width': f'{cw}px', 'height': f'{h}px', 'background': GRAY, 'align-items': 'center', 'justify-content': 'center', 'gap': '20px', 'flex': 'none'},
                                        inner=inner + text('Caption', cap, 'h3', BLACK, 30, {'text-align': 'center'}))
    lmr = side('LMR system', icon('tower', 170, 'LMR tower') , 'Your LMR system')
    bb = side('Broadband PTT', box('Devices', cls='row', style={'gap': '0', 'align-items': 'flex-end', 'height': f'{h - 150}px'}, inner=
              f'<img class="cutout" data-name="XP Pro" data-img="xppro_ptt" alt="XP Pro" style="display:block;height:{h - 170}px;width:auto">'
              f'<img class="cutout" data-name="XP5plus 5G" data-img="xp5" alt="XP5plus" style="display:block;height:{round((h - 170) * .86)}px;width:auto;margin-left:-24px">'), 'Broadband push-to-talk')
    link = box('Link', cls='row', style={'flex': '1', 'align-items': 'center', 'gap': '0', 'height': f'{h}px'}, inner=
               fill('Line', BLACK, style={'flex': '1', 'height': '4px'}) + fill('Node', RED, style={'width': '36px', 'height': '36px', 'flex': 'none'}) + fill('Line', BLACK, style={'flex': '1', 'height': '4px'}))
    return box('Proof · interop', l=M, t=t, w=920, h=h, cls='row', style={'gap': '0', 'align-items': 'center'}, inner=lmr + link + bb)

def proof_cost(t, h):
    """Myth 2: the $130K+ expansion, crossed out."""
    return box('Proof · cost', l=M, t=t, w=920, h=h, cls='stack', style={'background': GRAY, 'align-items': 'center', 'justify-content': 'center', 'gap': '24px'}, inner=
               box('Crossed figure', cls='row', style={'position': 'relative', 'align-items': 'center'}, inner=
                   text('Figure', '$130K+', 'stat', BLACK, 220, {'--bleed': '1'})
                   + fill('Strike', RED, style={'position': 'absolute', 'left': '-16px', 'right': '-16px', 'top': '50%', 'height': '16px', 'transform': 'rotate(-8deg)'}))
               + box('Tag', cls='row', style={'background': RED, 'padding': '12px 22px', 'gap': '14px', 'align-items': 'center'}, inner=
                     text('Tag text', 'Radio expansion avoided', 'h3', WHITE, 34)))

def proof_networks(t, h):
    """Myth 3: one PTT service, three carrier networks (names as text, no logos)."""
    nets = ['AT&T FirstNet', 'Verizon Frontline', 'T-Mobile T-Priority']
    tile = lambda n: box(n, cls='row', style={'background': GRAY, 'padding': '0 32px', 'gap': '24px', 'align-items': 'center', 'flex': '1'}, inner=
                         icon('signal', 64, n) + text('Network', n, 'h2', BLACK, 44))
    return box('Proof · networks', l=M, t=t, w=920, h=h, cls='stack', style={'gap': '14px'}, inner=''.join(tile(n) for n in nets))

PROOFS = [proof_interop, proof_cost, proof_networks]

# ---------------------------------------------------------------- A · 8-slide reveal carousel
n_ = 8
c = (page_notch(X, 360, WHITE)
     + stack('Headline block', [text('Label', 'Radio replacement', 'label', WHITE, 30),
                                text('Headline', 'Myth vs.\n**fact.**', 'display', WHITE, 190, {'--em': BLACK}),
                                text('Body', '3 myths, swipe for the facts.', 'h2', WHITE, 48, {'margin-top': '28px'})], l=M, t=360, w=920, gap=12)
     + logo(180, WHITE, l=M, b=M) + swipe(WHITE, M, 88))
post('rr-mf-1', 'Radio myth vs. fact · 1 Cover', RED, c, f'Carousel A, slide 1 of {n_} · cover on Sonim Red')
for i, (myth, fact) in enumerate(MYTHS, 1):
    s = 2 * i
    c = (text('Quote mark', '“', 'display abs', RED, 300, {'left': f'{M - 10}px', 'top': '40px', 'line-height': '1'})
         + page_notch(X, 380)
         + stack('Myth block', [text('Label', f'Myth {i} of 3', 'label', RED, 30), text('Myth', myth, 'h1', BLACK, 84)], l=M, t=380, w=920, gap=18)
         + text('Prompt', 'True or **false?**', 'h1 abs', BLACK, 72, {'left': f'{M}px', 'top': '960px'})
         + logo(170, BLACK, l=M, b=M) + swipe(RED, M, 88))
    post(f'rr-mf-{s}', f'Radio myth vs. fact · {s} Myth {i}', GRAY, c, f'Carousel A, slide {s} of {n_} · the myth, swipe to reveal')
    c = (page_notch(X, 120)
         + stack('Fact block', [box('Verdict', cls='row', style={'gap': '14px', 'align-items': 'center'}, inner=
                                    text('Verdict', 'False', 'label', WHITE, 30, {'background': RED, 'padding': '6px 14px'}) + text('Label', f'Fact {i} of 3', 'label', RED, 30)),
                                text('Fact', fact, 'h1', BLACK, 64)], l=M, t=120, w=920, gap=18)
         + PROOFS[i - 1](560, 560)
         + logo(170, BLACK, l=M, b=M) + counter(f'{s + 1} / {n_}', BLACK, M, 88))
    post(f'rr-mf-{s + 1}', f'Radio myth vs. fact · {s + 1} Fact {i}', WHITE, c, f'Carousel A, slide {s + 1} of {n_} · the fact, with a visual proof')
c = (page_notch(X, 360)
     + stack('Headline block', [text('Label', 'Your next step', 'label', RED, 30),
                                text('Headline', 'Go beyond\n**LMR.**', 'display', BLACK, 150),
                                text('CTA', 'Talk to our team.', 'h2', BLACK, 60, {'margin-top': '28px'})], l=M, t=360, w=920, gap=14)
     + logo(180, BLACK, l=M, b=M) + counter(f'{n_} / {n_}', BLACK, M, 88))
post(f'rr-mf-{n_}', f'Radio myth vs. fact · {n_} End slide', GRAY, c, f'Carousel A, slide {n_} of {n_} · call to action')

# ---------------------------------------------------------------- B · three single cards
for i, (myth, fact) in enumerate(MYTHS, 1):
    c = (box('Myth strip', l=0, t=0, w=W, h=300, cls='group', inner=fill('Strip fill', GRAY, l=0, t=0, w=W, h=300)
             + stack('Myth block', [text('Label', 'Myth', 'label', RED, 30), text('Myth', f'“{myth}”', 'h2', BLACK, 46)], l=M, t=80, w=920, gap=12))
         + page_notch(X, 360)
         + stack('Fact block', [box('Verdict', cls='row', style={'gap': '14px', 'align-items': 'center'}, inner=
                                    text('Verdict', 'False', 'label', WHITE, 30, {'background': RED, 'padding': '6px 14px'}) + text('Label', 'Fact', 'label', RED, 30)),
                                text('Fact', fact, 'h1', BLACK, 60)], l=M, t=360, w=920, gap=18)
         + PROOFS[i - 1](700, 440)
         + logo(170, BLACK, l=M, b=M) + counter(f'{i} / 3', BLACK, M, 88))
    post(f'rr-myth-{i}', f'Radio · Myth vs. fact card {i}', WHITE, c, f'Option B, card {i} of 3 · myth on top, the fact and its visual proof as the hero')

# ================================================================ 4 · LISTICLE "5 things to know" (type and graphics)
THINGS = [('tower', 'Keep your LMR', 'Add broadband PTT without ripping out your existing radio system.'),
          ('video', 'Go beyond voice', 'Add messaging, GPS, images, video and more.'),
          ('cost-down', 'Cut the cost', 'Avoid expensive LMR infrastructure, upgrades and rental costs.'),
          ('signal', 'Extend your reach', 'Use cellular coverage beyond traditional radio boundaries.'),
          ('ptt', 'Keep push-to-talk simple', 'Familiar PTT on rugged Sonim XP Series devices.')]
def thing(n, k, t_, d):
    return box(t_, cls='row', style={'gap': '28px', 'align-items': 'center', 'padding': '22px 0', 'border-top': f'2px solid {GRAY}'}, inner=
               text('Number', f'{n:02d}', 'h2', RED, 40, {'width': '56px', 'flex': 'none'}) + icon(k, 72, t_).replace('height:72px"', 'height:72px;flex:none"', 1)
               + box('Text', cls='stack', style={'gap': '6px'}, inner=text('Title', t_, 'h3', BLACK, 36) + text('Detail', d, 'body', BLACK, 26)))
c = (page_notch(X, 110)
     + stack('Headline block', [text('Label', 'Radio replacement', 'label', RED, 30),
                                text('Headline', '5 things to know about **radio replacement.**', 'h1', BLACK, 64)], l=M, t=110, w=920, gap=14)
     + stack('List', [thing(i, *t) for i, t in enumerate(THINGS, 1)], l=M, t=330, w=920, gap=0)
     + text('Tagline', 'Radio simplicity. Broadband capability. **One rugged device.**', 'h2 abs', BLACK, 34, {'left': px(M), 'top': '1060px', 'width': '920px'})
     + logo(170, BLACK, l=M, b=M))
post('rr-list', 'Radio · 5 things to know', WHITE, c, 'Listicle · type and Sonim icons, no imagery')
