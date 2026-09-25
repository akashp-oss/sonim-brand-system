from gen import *

# ============================================================================
# SYSTEM RULES (derived from the whitepaper, brandbook and social guidelines)
#   margin M  ~ 7.4% of the short side (whitepaper: 45pt on 612pt)
#   notch unit X = M / 5 ; notch = X x 18X, on the left edge, top aligned to the label
#   label (red, bold) -> headline (black, bold, tight, red key phrase, ends with a period)
#   logo single colour, bottom-left on the margin (bottom-right allowed when content needs the corner)
#   photography full-bleed, never tinted; product renders on Sonim Gray
# ============================================================================

F = []

# ---------------------------------------------------------------- WHITEPAPER
def doc_head(folio, title='Connected care in motion', dark=False):
    c = WHITE if dark else BLACK
    return stack('Running header', [text('Document title', title, 'meta', c, 9), text('Folio', f'/ {folio:02d}', 'meta', c, 9)], l=None, t=28, r=60, style={'flex-direction': 'row', 'gap': '18px'})

def doc_foot(note):
    return logo(78, BLACK, l=60, b=28) + text('Footnote', note, 'small abs', BLACK, 8, {'right': '60px', 'bottom': '30px', 'width': '380px', 'text-align': 'right'})

X, M = 12, 60
wp1 = (
    box('Hero photos', l=0, t=0, w=816, h=360, cls='group', inner=photo('Photo 1', 'crew', 0, 0, 470, 360, '40% 50%') + photo('Photo 2', 'responder', 473, 0, 343, 360, '50% 30%'))
    + doc_head(1, 'Sonim white paper', dark=True)
    + page_notch(X, 392)
    + stack('Title block', [text('Label', 'White paper · Emergency medical services', 'label', RED, 11),
                            text('Title', 'Connected care\n**in motion.**', 'display', BLACK, 62),
                            text('Subtitle', 'How EMS agencies are replacing legacy communications with mission-critical mobility.', 'lead', BLACK, 17, {'max-width': '520px'})],
            l=M, t=392, w=600, gap=10)
    + stack('Section', [text('Heading', 'The EMS communication challenge', 'h2', BLACK, 20),
                        text('Body', 'Every EMS call runs against the clock. Crews work across hospitals, highways, rural roads, events and disasters, often in one shift, and every call is a chain of conversations.', 'body', BLACK, 12.5),
                        text('Body', 'Legacy land mobile radio has limits. Coverage ends where the towers end, and every expansion means more sites and more capital. Meanwhile, the job now runs on voice, data, video and location together.', 'body', BLACK, 12.5)],
            l=M, t=640, w=380, gap=12)
    + rugged('Callout container', 486, 644, 270, 290, X, GRAY,
             text('Callout heading', 'Today’s EMS teams need:', 'h2', BLACK, 19) +
             '<div class="stack checks" data-name="Checklist" style="gap:9px;margin-top:14px">' +
             ''.join(f'<div class="row" data-name="Item" style="gap:9px;align-items:flex-start">{icon("check", 13, "Tick")}{text("Item text", t, "h3", BLACK, 12.5)}</div>'
                     for t in ['Instant PTT communication', 'Reliable coverage beyond radio range', 'Rugged devices built for frontline use', 'Dispatch integration', 'Secure connectivity and management']) + '</div>')
    + doc_foot('1 Source citation, publication, year. 2 Source citation.')
)
F.append(('wp', artboard('wp-opening', 'Whitepaper · Opening page', 816, 1056, WHITE, wp1, 'US Letter, print and PDF', 'doc')))

wp2 = (
    doc_head(2)
    + page_notch(X, 66)
    + stack('Headline block', [text('Label', 'The shift', 'label', RED, 11),
                               text('Headline', 'Why leading EMS agencies are moving\n**beyond traditional radios.**', 'h1', BLACK, 36)], l=M, t=66, w=690, gap=6)
    + text('Lead', 'EMS leaders are treating communications as an operational mobility platform: nationwide broadband, standards-based push-to-talk and rugged devices that carry voice and data together.', 'lead abs', BLACK, 17, {'left': '60px', 'top': '176px', 'width': '640px'})
    + box('Two columns', l=M, t=270, w=696, cls='row', style={'gap': '20px'}, inner=
          text('Column 1', 'FirstNet, the public safety network built with AT&T, gives first responders priority and preemption and serves about 31,000 agencies.¹ Deployable assets back it up for incidents and planned events.', 'body', BLACK, 12.5, {'flex': '1'}) +
          text('Column 2', 'Mission-critical push-to-talk brings radio-grade group calling to broadband, and gateways connect talkgroups to existing LMR systems, so agencies move at their own pace.', 'body', BLACK, 12.5, {'flex': '1'}))
    + box('Comparison', l=M, t=392, w=696, h=230, cls='group', inner=
          fill('Before fill', GRAY, l=0, t=0, w=330, h=230) + fill('After fill', RED, l=366, t=0, w=330, h=230)
          + fill('After header fill', BLACK, l=366, t=0, w=330, h=40)
          + text('Before header', 'Traditional LMR', 'h3 abs', BLACK, 13, {'left': '16px', 'top': '12px'})
          + text('After header', 'Modern mission-critical mobility', 'h3 abs', WHITE, 13, {'left': '382px', 'top': '12px'})
          + ''.join(text('Before', a, 'body abs', BLACK, 12.5, {'left': '16px', 'top': f'{52+i*36}px'}) + fill('Divider', WHITE, l=0, t=44 + i * 36 - 4, w=330, h=1)
                    + text('Arrow', '→', 'h3 abs', RED, 14, {'left': '341px', 'top': f'{50+i*36}px'})
                    + text('After', b, 'h3 abs', WHITE, 12.5, {'left': '382px', 'top': f'{52+i*36}px'})
                    for i, (a, b) in enumerate([('Coverage limits', 'Nationwide coverage'), ('Voice only', 'Voice + data + video'), ('Costly infrastructure', 'Carrier-powered'), ('Separate devices', 'Consolidated platform'), ('Limited flexibility', 'Rapid deployment')])))
    + fill('Rule', GRAY, l=M, t=650, w=696, h=1)
    + box('Stats', l=M, t=668, w=696, cls='row', style={'gap': '24px'}, inner=''.join(
          f'<div class="stack" data-name="Stat" style="flex:1;gap:6px">{text("Number", n, "stat", RED, 44)}{text("Caption", c, "small", BLACK, 10.5, {"font-weight": "700"})}</div>'
          for n, c in [('18,200+', 'Local EMS agencies answering 911 calls²'), ('28.5M', '911 dispatches a year in 41 reporting states²'), ('~31,000', 'Public safety agencies on FirstNet¹')]))
    + text('Section heading', 'EMS use cases', 'h2 abs', BLACK, 20, {'left': '60px', 'top': '790px'})
    + box('Use cases', l=M, t=828, w=696, cls='row', style={'gap': '16px'}, inner=''.join(
          f'<div class="stack" data-name="{t}" style="flex:1;gap:6px">{icon(k, 36, t)}{text("Title", t, "h3", BLACK, 12.5)}{text("Detail", d, "small", BLACK, 10.5)}</div>'
          for k, t, d in [('ambulance', 'Ambulance operations', 'Crew-to-dispatch from the rig or on foot.'), ('interfacility', 'Interfacility transport', 'Coordination between locations.'),
                          ('events', 'Special events', 'Crowds and mass casualty readiness.'), ('disaster', 'Disaster response', 'Deployable communications.'), ('air-medical', 'Air medical', 'Aircraft tracking and remote connectivity.')]))
    + doc_foot('1 FirstNet.com. 2 NASEMSO, 2020 National EMS Assessment.')
)
F.append(('wp', artboard('wp-argument', 'Whitepaper · Argument page', 816, 1056, WHITE, wp2, 'Interior page: comparison, stats, icons', 'doc')))

wp3 = (
    doc_head(3)
    + page_notch(X, 66)
    + stack('Headline block', [text('Label', 'Customer spotlight', 'label', RED, 11), text('Headline', 'How EMS organizations **use Sonim today.**', 'h1', BLACK, 36)], l=M, t=66, w=696, gap=6)
    + ''.join(
        box(f'Case study {i+1}', l=M + i * 358, t=140, w=338, cls='stack', style={'gap': '6px'}, inner=
            f'<div class="photo-frame" data-name="Photo frame" style="width:338px;height:200px;margin-bottom:10px">{photo("Photo", k, 0, 0, 338, 200, pos)}</div>'
            + text('Label', 'Case study', 'label', RED, 11) + text('Customer', n, 'h2', BLACK, 20) + text('Meta', m, 'small', BLACK, 10.5)
            + text('Subheading', 'Challenge', 'h3', RED, 12.5, {'margin-top': '8px'}) + text('Body', ch, 'body', BLACK, 12.5)
            + text('Subheading', 'Solution', 'h3', RED, 12.5, {'margin-top': '6px'}) + text('Body', so, 'body', BLACK, 12.5)
            + text('Subheading', 'Results', 'h3', RED, 12.5, {'margin-top': '6px'})
            + ''.join(f'<div class="row" data-name="Result" style="gap:8px;align-items:center">{fill("Bar", RED, style={"position": "relative", "width": "4px", "height": "10px"})}{text("Result text", r_, "body", BLACK, 12.5)}</div>' for r_ in rs))
        for i, (k, pos, n, m, ch, so, rs) in enumerate([
            ('heli', '50% 45%', 'Customer name', 'Organisation size · locations · scope', 'One or two sentences on the operational problem.', 'The Sonim products and platform used, in one or two sentences.', ['Result one', 'Result two', 'Result three']),
            ('night', '40% 50%', 'Customer name', 'Organisation size · locations · scope', 'One or two sentences on the operational problem.', 'The Sonim products and platform used, in one or two sentences.', ['Benefit one', 'Benefit two', 'Benefit three'])]))
    + box('Quote band', l=M, t=780, w=696, h=150, cls='group', inner=fill('Band fill', RED, l=0, t=0, w=696, h=150)
          + text('Quote', '“Customer quote in bold white on Sonim Red. Keep it under thirty words and make it specific.”', 'quote abs', WHITE, 21, {'left': '26px', 'top': '26px', 'width': '430px'})
          + text('Attribution', 'Name Surname\nTitle, Organisation', 'small abs', WHITE, 10.5, {'left': '500px', 'bottom': '26px', 'width': '170px', 'font-weight': '700'}))
    + doc_foot('3 Source citation. 4 Source citation.')
)
F.append(('wp', artboard('wp-proof', 'Whitepaper · Proof page', 816, 1056, WHITE, wp3, 'Case studies and a quote band', 'doc')))

# ---------------------------------------------------------------- PRESENTATION 1920x1080
X, M = 24, 120
def slide_head(n, dark=False):
    c = WHITE if dark else BLACK
    return stack('Running header', [text('Deck title', 'Mission-critical mobility for EMS', 'meta', c, 16), text('Folio', f'/ {n:02d}', 'meta', c, 16)], t=56, r=120, style={'flex-direction': 'row', 'gap': '28px'})

s1 = (photo('Hero photo', 'radio', 880, 0, 1040, 1080, '55% 50%')
      + page_notch(X, 290)
      + stack('Title block', [text('Label', 'Sales presentation', 'label', RED, 26),
                              text('Title', 'When the mission\nis critical, the\n**solution is Sonim.**', 'display', BLACK, 86),
                              text('Subtitle', 'Mission-critical mobility for EMS and public safety teams.', 'lead', BLACK, 32, {'max-width': '620px', 'margin-top': '16px'}),
                              text('Meta', 'Presenter name · Month 2027', 'small', BLACK, 22, {'margin-top': '36px'})],
              l=M, t=290, w=740, gap=14)
      + logo(150, BLACK, l=M, b=88))
F.append(('slides', artboard('slide-cover', 'Presentation · Cover', 1920, 1080, WHITE, s1, '16:9 title slide', 'slide')))

s2 = (photo('Section photo', 'team', 960, 0, 960, 1080, '65% 50%')
      + xnotch('Expanded notch 50%', 0, 0, 960, 1080, X, RED,
               text('Section number', '02', 'display abs', WHITE, 240, {'left': '120px', 'top': '220px', '--em': BLACK})
               + text('Section title', 'The shift to\nmission-critical\n**mobility.**', 'h1 abs', WHITE, 88, {'left': '120px', 'top': '500px', 'width': '760px', '--em': BLACK}))
      + logo(150, WHITE, l=M, b=88))
F.append(('slides', artboard('slide-section', 'Presentation · Section divider', 1920, 1080, WHITE, s2, 'Opens a chapter', 'slide')))

s3 = (slide_head(3)
      + page_notch(X, 160)
      + stack('Headline block', [text('Label', 'By the numbers', 'label', RED, 26), text('Headline', 'EMS runs on\n**communication.**', 'h1', BLACK, 96)], l=M, t=160, w=1100, gap=14)
      + text('Lead', 'Every call is a chain of conversations: dispatch, crew, hospital and partner agencies.', 'lead abs', BLACK, 36, {'left': '120px', 'top': '440px', 'width': '1000px'})
      + fill('Rule', WHITE, l=M, t=600, w=1680, h=2)
      + box('Stats', l=M, t=640, w=1680, cls='row', style={'gap': '60px'}, inner=''.join(
          f'<div class="stack" data-name="Stat" style="flex:1;gap:14px">{text("Number", n, "stat", RED, 150)}{text("Caption", c, "h3", BLACK, 26)}{text("Source", s, "small", BLACK, 18)}</div>'
          for n, c, s in [('18,200+', 'Local EMS agencies answer 911 calls.', 'NASEMSO, 2020'), ('28.5M', '911 dispatches a year in 41 reporting states.', 'NASEMSO, 2020'), ('~31,000', 'Public safety agencies on FirstNet.', 'FirstNet.com')]))
      + logo(150, BLACK, l=M, b=88))
F.append(('slides', artboard('slide-stats', 'Presentation · Key numbers', 1920, 1080, GRAY, s3, 'Up to three sourced stats', 'slide')))

s4 = (slide_head(4)
      + text('Model number', 'XP5', 'display abs', RED, 560, {'left': '760px', 'top': '220px', 'letter-spacing': '-0.06em', 'line-height': '0.8'})
      + cutout('Product render', 'xp5', 1130, 150, 420, 800)
      + page_notch(X, 160)
      + stack('Headline block', [text('Label', 'Sonim XP5plus 5G', 'label', RED, 26), text('Headline', 'Radio-style\ncontrol.\n**Broadband reach.**', 'h1', BLACK, 72)], l=M, t=160, w=600, gap=14)
      + stack('Feature callouts', [icon_item(k, t, d, 44, 26, 22, 20) for k, t, d in [('ptt', 'Dedicated PTT', 'Side-mounted key'), ('sos', 'SOS button', 'Top-mounted, programmable'), ('battery', 'Removable battery', 'Up to 25 hours talk time'), ('rugged', 'Ultra-rugged', 'IP68 · MIL-STD-810H')]],
              l=M, t=520, w=560, gap=26)
      + logo(150, BLACK, l=M, b=88))
F.append(('slides', artboard('slide-product', 'Presentation · Product hero', 1920, 1080, GRAY, s4, 'Model number as a graphic, product on Sonim Gray', 'slide')))

s5 = (photo('Quote photo', 'heli', 1200, 0, 720, 1080, '45% 50%')
      + page_notch(X, 250)
      + stack('Quote block', [text('Label', 'Customer voice', 'label', RED, 26),
                              text('Quote', '“With FirstNet, we maintain contact with first responders nationwide during **everyday crises and large disasters.**”', 'quote', BLACK, 68, {'max-width': '940px'}),
                              text('Attribution', 'Jeffrey E. Marani\nNational Director of Field Technologies, Global Medical Response', 'small', BLACK, 22, {'font-weight': '700', 'margin-top': '24px'})],
              l=M, t=250, w=960, gap=18)
      + logo(150, BLACK, l=M, b=88))
F.append(('slides', artboard('slide-quote', 'Presentation · Quote', 1920, 1080, WHITE, s5, 'Customer or analyst quote with source', 'slide')))

s6 = (photo('Closing photo', 'crew', 0, 0, 1920, 1080, '45% 45%')
      + rugged('Contact container', 1160, 160, 600, 700, X, WHITE,
               text('Headline', 'Thank you.', 'display', BLACK, 96) +
               text('Lead', 'For more information, assets or questions.', 'lead', BLACK, 34, {'margin-top': '20px'}) +
               '<div class="stack" data-name="Contact" style="gap:6px;margin-top:auto">' + text('Name', 'Presenter name', 'h3', BLACK, 26) + text('Detail', 'name@sonimtech.com', 'body', BLACK, 24) + text('URL', 'sonimtech.com', 'h3', RED, 24) + '</div>',
               pad=56)
      + logo(150, WHITE, l=M, b=88))
F.append(('slides', artboard('slide-close', 'Presentation · Closing', 1920, 1080, WHITE, s6, 'Thank you and contact', 'slide')))

# ---------------------------------------------------------------- INSTAGRAM POSTS 1080x1350 / 1080x1080
X, M = 16, 80
p1 = (cutout('Product render', 'xp5', 520, 400, 460, 870)
      + page_notch(X, 120)
      + stack('Headline block', [text('Label', 'Sonim XP5plus 5G', 'label', RED, 30), text('Headline', 'Push-to-talk,\n**built in.**', 'display', BLACK, 120)], l=M, t=120, w=920, gap=14)
      + text('Body', 'A dedicated PTT key, 100 dB+ speakers and a removable battery for multi-shift days.', 'lead abs', BLACK, 34, {'left': '80px', 'top': '470px', 'width': '400px'})
      + logo(180, BLACK, l=M, b=80) + text('URL', 'sonimtech.com', 'h3 abs', BLACK, 26, {'right': '80px', 'bottom': '86px'}))
F.append(('ig', artboard('ig-product', 'Instagram post · Product feature', 1080, 1350, GRAY, p1, 'Feed 4:5 · product on Sonim Gray', 'post')))

p2 = (photo('Background photo', 'radio', 0, 0, 1080, 1350, '62% 50%')
      + rugged('Message container', 80, 150, 620, 780, X, WHITE,
               text('Headline', 'Sonim is\ncreating\ndevices to\n**serve those\nwho serve us.**', 'h1', BLACK, 70) + '<div data-name="Spacer" style="flex:1"></div>' + logo(170, BLACK, name='Sonim logo'), pad=48))
F.append(('ig', artboard('ig-message', 'Instagram post · Brand message', 1080, 1350, WHITE, p2, 'Feed 4:5 · Rugged Container over photography', 'post')))

p3 = (page_notch(X, 200)
      + stack('Quote block', [text('Label', 'Quote', 'label', RED, 30),
                              text('Quote', '“Our crews need to reach dispatch the moment it matters, **from anywhere.**”', 'quote', BLACK, 88),
                              text('Attribution', 'Name Surname\nTitle, EMS agency', 'body', BLACK, 30, {'font-weight': '700', 'margin-top': '30px'})], l=M, t=200, w=900, gap=20)
      + logo(180, BLACK, l=M, b=80))
F.append(('ig', artboard('ig-quote', 'Instagram post · Quote', 1080, 1350, GRAY, p3, 'Feed 4:5 · type-only quote', 'post')))

p4 = (page_notch(X, 200, WHITE)
      + stack('Stat block', [text('Label', 'By the numbers', 'label', WHITE, 30),
                             text('Number', '28.5M', 'stat', WHITE, 300, {'margin-top': '10px'}),
                             text('Caption', '911 dispatches a year in\n41 reporting U.S. states.', 'h2', WHITE, 56, {'margin-top': '20px'}),
                             text('Source', 'Source: NASEMSO, 2020 National EMS Assessment.', 'small', WHITE, 24, {'margin-top': '40px'})], l=M, t=200, w=920, gap=0)
      + logo(180, WHITE, l=M, b=80))
F.append(('ig', artboard('ig-stat', 'Instagram post · Stat', 1080, 1350, RED, p4, 'Feed 4:5 · one sourced number on Sonim Red', 'post')))

p5 = (photo('Event photo', 'crowd', 0, 0, 1080, 760, '50% 40%')
      + page_notch(X, 820)
      + stack('Event block', [text('Label', 'Event', 'label', RED, 30), text('Headline', 'Meet us at\n**Event name 2027.**', 'h1', BLACK, 84),
                              text('Details', 'Booth 000 · Month 00–00 · City, ST', 'lead', BLACK, 34, {'margin-top': '16px'})], l=M, t=820, w=920, gap=12)
      + logo(180, BLACK, l=M, b=80) + text('URL', 'sonimtech.com', 'h3 abs', BLACK, 26, {'right': '80px', 'bottom': '86px'}))
F.append(('ig', artboard('ig-event', 'Instagram post · Event', 1080, 1350, WHITE, p5, 'Feed 4:5 · photo over white', 'post')))

p6 = (page_notch(X, 110)
      + stack('Headline block', [text('Label', 'Rugged Performance Standards', 'label', RED, 28), text('Headline', 'Built for the\n**worst days.**', 'h1', BLACK, 88)], l=M, t=100, w=920, gap=12)
      + box('Feature grid', l=M, t=380, w=920, h=500, cls='grid2', style={'gap': '20px'}, inner=''.join(
          f'<div class="stack tile" data-name="{t}" style="background:{WHITE};padding:34px;gap:14px">{icon(k, 64, t)}{text("Title", t, "h3", BLACK, 34)}{text("Detail", d, "body", BLACK, 26)}</div>'
          for k, t, d in [('voice', 'Extra-loud audio', '100 dB+ dual front speakers'), ('battery', 'Multi-shift battery', 'Removable and fast charging'),
                          ('rugged', 'Drop resistant', 'MIL-STD-810H tested'), ('glove', 'Glove-friendly', 'Large, tactile keys')]))
      + logo(160, BLACK, l=M, b=64))
F.append(('ig', artboard('ig-features', 'Instagram post · Feature grid', 1080, 1080, GRAY, p6, 'Square 1:1 · four icon tiles', 'post')))

p7 = (photo('Lifestyle photo', 'night', 0, 0, 1080, 1080, '42% 50%')
      + text('Line', 'Ready when\nit matters most.', 'h1 abs', WHITE, 76, {'left': '80px', 'top': '96px', 'width': '700px'})
      + logo(180, WHITE, l=M, b=80))
F.append(('ig', artboard('ig-lifestyle', 'Instagram post · Lifestyle', 1080, 1080, BLACK, p7, 'Square 1:1 · photo-led, white type', 'post')))

# ---------------------------------------------------------------- INSTAGRAM STORIES 1080x1920
X, M = 16, 80
SAFE_T, SAFE_B = 250, 340
st1 = (photo('Story photo', 'crew', 0, 0, 1080, 1100, '45% 50%')
       + xnotch_h('Expanded notch (rotated)', 0, 1080, 1080, 840, X, RED,
                  stack('Content', [text('Label', 'New white paper', 'label', WHITE, 32),
                                    text('Headline', 'Every call is\na chain of\n**conversations.**', 'h1', WHITE, 96, {'--em': BLACK}),
                                    text('CTA', 'Read it at sonimtech.com  →', 'h3', WHITE, 34, {'margin-top': '14px'})], l=M, t=64, w=920, gap=14))
       + logo(170, WHITE, l=M, t=SAFE_T))
F.append(('stories', artboard('story-photo', 'Instagram story · Photo + red panel', 1080, 1920, WHITE, st1, '9:16 · rotated Expanded Notch', 'story')))

st2 = (text('Model number', 'XP5', 'display abs', RED, 470, {'left': '50px', 'top': '560px', 'letter-spacing': '-0.06em', 'line-height': '0.8'})
       + cutout('Product render', 'xp5', 390, 420, 520, 990)
       + page_notch(X, SAFE_T)
       + stack('Headline block', [text('Label', 'Sonim XP5plus 5G', 'label', RED, 32), text('Headline', 'The fourth\ngeneration is **here.**', 'h1', BLACK, 80)], l=M, t=SAFE_T, w=920, gap=12)
       + text('CTA', 'Available on AT&T and FirstNet.', 'lead abs', BLACK, 38, {'left': '80px', 'top': '1440px', 'width': '900px', 'font-weight': '700'})
       + logo(170, BLACK, l=M, b=SAFE_B + 20))
F.append(('stories', artboard('story-product', 'Instagram story · Product launch', 1080, 1920, GRAY, st2, '9:16 · product on Sonim Gray', 'story')))

st3 = (photo('Story photo', 'heli', 0, 1080, 1080, 840, '50% 50%')
       + page_notch(X, SAFE_T)
       + stack('Stat block', [text('Label', 'Did you know', 'label', RED, 32), text('Number', '~31,000', 'stat', RED, 210),
                              text('Caption', 'public safety agencies\n**use FirstNet.**', 'h1', BLACK, 76, {'margin-top': '10px', '--em': BLACK}),
                              text('Source', 'Source: FirstNet.com', 'small', BLACK, 26, {'margin-top': '24px'})], l=M, t=SAFE_T, w=920, gap=8)
       + logo(170, WHITE, l=M, b=SAFE_B + 20))
F.append(('stories', artboard('story-stat', 'Instagram story · Stat', 1080, 1920, WHITE, st3, '9:16 · type over white, photo base', 'story')))

# ---------------------------------------------------------------- SOCIAL (landscape)
X, M = 12, 64
so1 = (photo('Photo', 'heli', 600, 0, 600, 627, '45% 50%')
       + page_notch(X, 96)
       + stack('Text block', [text('Label', 'White paper', 'label', RED, 20), text('Headline', 'Mission-critical\nmobility **for EMS.**', 'h1', BLACK, 56),
                              text('CTA', 'Download the white paper  →', 'h3', RED, 22, {'margin-top': '16px'})], l=M, t=96, w=500, gap=10)
       + logo(110, BLACK, l=M, b=52))
F.append(('social', artboard('so-link', 'LinkedIn / Facebook · Link post', 1200, 627, WHITE, so1, '1.91:1 shared-link image', 'land')))

X = 16
so2 = (photo('Background photo', 'night', 0, 0, 1600, 900, '60% 50%')
       + rugged('Quote container', 100, 110, 560, 680, X, RED,
                text('Label', 'Customer voice', 'label', WHITE, 24) +
                text('Quote', '“Our crews need to reach dispatch the moment it matters, **from anywhere.**”', 'quote', WHITE, 54, {'margin-top': '14px', '--em': BLACK}) +
                '<div data-name="Spacer" style="flex:1"></div>' + text('Attribution', 'Name Surname · Title, EMS agency', 'small', WHITE, 22, {'font-weight': '700'}), pad=44)
       + logo(140, WHITE, r=90, b=70))
F.append(('social', artboard('so-x', 'X / LinkedIn · Quote card', 1600, 900, BLACK, so2, '16:9 feed image', 'land')))

X = 12
so3 = (photo('Cover photo', 'team', 520, 0, 1064, 396, '55% 50%')
       + xnotch('Expanded notch 33%', 0, 0, 520, 396, X, RED,
                logo(190, WHITE, l=64, t=64) + text('Tagline', 'Built for the extraordinary.\nDesigned to endure.\nTrusted to deliver.', 'h2 abs', WHITE, 26, {'left': '64px', 'top': '176px', 'width': '400px'})))
F.append(('social', artboard('so-cover', 'LinkedIn · Page cover', 1584, 396, WHITE, so3, 'Keep the lower-left clear for the profile image', 'land')))

so4 = (page_notch(X, 88)
       + stack('Text block', [text('Label', 'Webinar', 'label', RED, 20), text('Headline', 'Replacing LMR\nwithout **starting over.**', 'h1', BLACK, 54),
                              text('Details', 'Month 00, 2027 · 11:00 am PT · 45 minutes', 'body', BLACK, 22, {'margin-top': '12px'})], l=M, t=88, w=640, gap=10)
       + box('Speaker', l=770, t=88, w=366, h=452, cls='group', inner=photo('Speaker photo', 'dispatcher', 0, 0, 366, 330, '20% 40%')
             + fill('Name plate', WHITE, l=0, t=330, w=366, h=122)
             + text('Speaker name', 'Speaker name', 'h3 abs', BLACK, 24, {'left': '24px', 'top': '356px'})
             + text('Speaker title', 'Title, Organisation', 'body abs', BLACK, 20, {'left': '24px', 'top': '392px'}))
       + logo(110, BLACK, l=M, b=52))
F.append(('social', artboard('so-webinar', 'LinkedIn / Facebook · Webinar', 1200, 627, GRAY, so4, 'Event or webinar announcement', 'land')))

# ---------------------------------------------------------------- POSTERS
X, M = 20, 96
po1 = (photo('Poster photo', 'rescue', 0, 0, 1200, 980, '50% 40%')
       + cutout('Product render', 'xp5', 850, 700, 270, 515)
       + page_notch(X, 1040)
       + stack('Headline block', [text('Label', 'Sonim XP5plus 5G', 'label', RED, 26), text('Headline', 'Ready when\nit matters\n**most.**', 'display', BLACK, 104)], l=M, t=1040, w=700, gap=14)
       + text('Body', 'Radio-style push-to-talk on AT&T and FirstNet.', 'lead abs', BLACK, 30, {'right': '96px', 'top': '1250px', 'width': '300px'})
       + logo(180, BLACK, l=M, b=M) + text('URL', 'sonimtech.com', 'h3 abs', BLACK, 26, {'right': '96px', 'bottom': '100px'}))
F.append(('posters', artboard('poster-18x24', 'Poster · 18 × 24 in', 1200, 1600, WHITE, po1, '3:4 · photo-led, product breaks the edge', 'poster')))

po2 = (text('Model number', 'XP5', 'display abs', RED, 600, {'left': '70px', 'top': '560px', 'letter-spacing': '-0.06em', 'line-height': '0.8'})
       + cutout('Product render', 'xp5', 560, 420, 460, 875)
       + page_notch(X, M + 30)
       + stack('Headline block', [text('Label', 'The fourth generation', 'label', RED, 26), text('Headline', 'A bold vision\nfor **public safety.**', 'h1', BLACK, 104)], l=M, t=M + 30, w=1000, gap=14)
       + box('Feature callouts', l=M, t=1390, w=1008, cls='row', style={'gap': '28px'}, inner=''.join(
           f'<div style="flex:1">{icon_item(k, t, d, 52, 26, 20, 14)}</div>' for k, t, d in [('ptt', 'Dedicated PTT', 'Side-mounted key'), ('firstnet', 'FirstNet Ready', 'Band 14 certified'), ('rugged', 'Ultra-rugged', 'IP68 · MIL-STD-810H')]))
       + logo(180, BLACK, l=M, b=M))
F.append(('posters', artboard('poster-24x36', 'Poster · 24 × 36 in', 1200, 1800, GRAY, po2, '2:3 · model number as graphic', 'poster')))

# ---------------------------------------------------------------- BANNERS (event + web)
X, M = 12, 56
b1 = (logo_vertical(900, WHITE, 222, 260) + text('URL', 'sonimtech.com', 'h3 abs', WHITE, 26, {'left': '56px', 'bottom': '64px'}))
F.append(('banners', artboard('rollup-logo', 'Roll-up banner · Brand', 660, 1600, RED, b1, '33 × 80 in · vertical logo on Sonim Red', 'rollup')))

b2 = (photo('Banner photo', 'responder', 0, 0, 660, 800, '50% 30%')
      + logo(160, WHITE, l=M, t=M)
      + page_notch(X, 860)
      + stack('Headline block', [text('Label', 'Public safety', 'label', RED, 22), text('Headline', 'A bold\nvision for\n**public\nsafety.**', 'display', BLACK, 96)], l=M, t=860, w=560, gap=12)
      + text('URL', 'sonimtech.com', 'h3 abs', BLACK, 24, {'left': '56px', 'bottom': '64px'}))
F.append(('banners', artboard('rollup-message', 'Roll-up banner · Message', 660, 1600, GRAY, b2, '33 × 80 in · photo over Sonim Gray', 'rollup')))

b3 = (text('Model line 1', 'XP', 'display abs', RED, 400, {'left': '20px', 'top': '420px', 'letter-spacing': '-0.06em', 'line-height': '0.8'})
      + text('Model line 2', '5', 'display abs', RED, 640, {'left': '250px', 'top': '720px', 'letter-spacing': '-0.06em', 'line-height': '0.8'})
      + cutout('Product render', 'xp5', 150, 380, 360, 685)
      + logo(160, BLACK, l=M, t=M)
      + stack('Tagline', [text('Label', 'Sonim XP5plus 5G', 'label', RED, 22), text('Line', 'Radio-style control.\nBroadband reach.', 'h2', BLACK, 40)], l=M, t=1300, w=560, gap=10)
      + text('URL', 'sonimtech.com', 'h3 abs', BLACK, 24, {'left': '56px', 'bottom': '64px'}))
F.append(('banners', artboard('rollup-product', 'Roll-up banner · Product', 660, 1600, GRAY, b3, '33 × 80 in · model number as graphic', 'rollup')))

wb1 = (page_notch(4, 9)
       + text('Headline', 'Mission-critical mobility **for EMS.**', 'h2 abs', BLACK, 24, {'left': '24px', 'top': '31px'})
       + text('CTA', 'Learn more  →', 'h3 abs', RED, 15, {'left': '470px', 'top': '37px'})
       + logo(90, BLACK, r=20, t=29))
F.append(('web', artboard('web-leaderboard', 'Display ad · Leaderboard', 728, 90, GRAY, wb1, '728 × 90', 'web')))

wb2 = (photo('Ad photo', 'radio', 0, 0, 300, 132, '60% 45%')
       + page_notch(5, 146)
       + text('Headline', 'Push-to-talk,\n**built in.**', 'h1 abs', BLACK, 26, {'left': '18px', 'top': '146px', 'width': '260px'})
       + logo(64, BLACK, l=18, b=14) + text('CTA', 'Learn more  →', 'h3 abs', RED, 13, {'right': '16px', 'bottom': '16px'}))
F.append(('web', artboard('web-mpu', 'Display ad · Medium rectangle', 300, 250, WHITE, wb2, '300 × 250', 'web')))

wb3 = (page_notch(6, 30)
       + stack('Text', [text('Label', 'Sonim XP5plus', 'label', RED, 12), text('Headline', 'Ready\nwhen it\nmatters\n**most.**', 'h1', BLACK, 30)], l=16, t=30, w=130, gap=6)
       + cutout('Product render', 'xp5', 30, 220, 100, 190)
       + text('CTA', 'Learn more  →', 'h3 abs', RED, 13, {'left': '16px', 'top': '450px'})
       + logo(64, BLACK, l=16, b=20))
F.append(('web', artboard('web-sky', 'Display ad · Skyscraper', 160, 600, GRAY, wb3, '160 × 600', 'web')))

wb4 = (logo(64, WHITE, l=12, t=14) + text('Headline', 'Built for EMS.', 'h3 abs', WHITE, 14, {'left': '96px', 'top': '17px'})
       + text('CTA', 'Learn more  →', 'h3 abs', WHITE, 12, {'right': '12px', 'top': '18px'}))
F.append(('web', artboard('web-mobile', 'Display ad · Mobile banner', 320, 50, RED, wb4, '320 × 50', 'web')))

X, M = 14, 96
wb5 = (photo('Hero photo', 'paramedics', 700, 0, 740, 640, '50% 50%')
       + page_notch(X, 150)
       + stack('Hero text', [text('Label', 'Emergency medical services', 'label', RED, 20),
                             text('Headline', 'When seconds matter,\n**so does the signal.**', 'h1', BLACK, 64),
                             text('Lead', 'Rugged devices, high-power connectivity and dispatch tools that keep EMS crews connected.', 'lead', BLACK, 22, {'margin-top': '10px', 'max-width': '520px'}),
                             text('CTA', 'Explore EMS solutions  →', 'h3', RED, 20, {'margin-top': '22px'})], l=M, t=150, w=560, gap=12))
F.append(('web', artboard('web-hero', 'Website · Hero', 1440, 640, WHITE, wb5, 'Landing page header', 'web')))

# ---------------------------------------------------------------- OTHER
X, M = 12, 64
ot1 = (photo('Header photo', 'crew', 680, 0, 520, 400, '40% 50%')
       + page_notch(X, 72)
       + stack('Text', [text('Label', 'Sonim newsletter · Month 2027', 'label', RED, 20), text('Headline', 'Connected care\n**in motion.**', 'h1', BLACK, 60)], l=M, t=72, w=580, gap=10)
       + logo(120, BLACK, l=M, b=52))
F.append(('other', artboard('email-header', 'Email · Header', 1200, 400, GRAY, ot1, 'Displays at 600 × 200', 'other')))

ot2 = (logo(420, WHITE, l=315, t=228))
F.append(('other', artboard('card-back', 'Business card · Back', 1050, 600, RED, ot2, '3.5 × 2 in at 300 ppi', 'other')))

ot3 = (page_notch(X, 72)
       + stack('Name block', [text('Name', 'First Last', 'h1', BLACK, 56), text('Title', 'Job title, Department', 'lead', BLACK, 30)], l=M, t=72, w=700, gap=8)
       + stack('Contact', [text('Phone', '+1 000 000 0000', 'body', BLACK, 26), text('Email', 'first.last@sonimtech.com', 'body', BLACK, 26), text('URL', 'sonimtech.com', 'h3', RED, 26)], l=M, b=64, w=600, gap=4)
       + logo(170, BLACK, r=64, b=70))
F.append(('other', artboard('card-front', 'Business card · Front', 1050, 600, WHITE, ot3, '3.5 × 2 in at 300 ppi', 'other')))

ot4 = (fill('Rule', GRAY, l=0, t=0, w=2, h=120, style={'left': '150px', 'top': '20px'})
       + logo(110, BLACK, l=16, t=45)
       + stack('Signature', [text('Name', 'First Last', 'h3', BLACK, 18), text('Title', 'Job title · Sonim, a NEXA company', 'body', BLACK, 14),
                             text('Contact', '+1 000 000 0000 · sonimtech.com', 'body', RED, 14, {'font-weight': '700'})], l=176, t=34, w=400, gap=4))
F.append(('other', artboard('email-signature', 'Email · Signature', 600, 160, WHITE, ot4, 'Export at 2× for retina', 'other')))

X = 24
ot5 = (xnotch('Expanded notch 25%', 0, 0, 480, 1080, X, RED, logo(170, WHITE, l=120, b=88))
       + text('Name', 'First Last', 'h2 abs', BLACK, 34, {'right': '120px', 'top': '96px', 'text-align': 'right'})
       + text('Title', 'Job title', 'body abs', BLACK, 24, {'right': '120px', 'top': '144px', 'text-align': 'right'}))
F.append(('other', artboard('virtual-bg', 'Video call · Virtual background', 1920, 1080, GRAY, ot5, 'Teams / Zoom; the camera image is mirrored in self-view only', 'other')))

SECTION_META = [
    ('wp', 'Whitepapers', 'Long-form print and PDF. The source of the system: 45 pt margins, 12-column grid, notch-anchored headlines.'),
    ('slides', 'Presentation', '16:9 master slides. Same hierarchy scaled up: label, bold headline with a red key phrase, one idea per slide.'),
    ('ig', 'Instagram posts', 'Feed 4:5 and square. Product on Sonim Gray, messages in the Rugged Container, numbers on Sonim Red.'),
    ('stories', 'Instagram stories', '9:16 with platform safe zones: keep type and logo out of the top 250 px and bottom 340 px.'),
    ('social', 'Social media graphics', 'Link posts, quote cards, page covers and event cards for LinkedIn, Facebook and X.'),
    ('posters', 'Posters', 'Print posters. Photography or product carries the page; the headline stays short.'),
    ('banners', 'Banners', 'Roll-up banners for events.'),
    ('web', 'Web and display', 'IAB display ads and a website hero.'),
    ('other', 'Stationery and other', 'Email header and signature, business card, video-call background.'),
]
