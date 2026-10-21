from wpkit import *

# EMS white paper "Connected care in motion": the client's text (client file Ambulance_EMS_Whitepaper_Sonim.pdf =
# whitepaper/dist/Sonim_EMS_Whitepaper_editor-export.pdf), verbatim, in the client's page order.
# Client feedback 2026-10-21: Sonim-branded icons only, and a clean, airy layout; add pages rather than crowd.
# So: the same scale and spacing as the Inova paper (wpkit: body 14 px, sections 32 px apart, tiles 24 px padding),
# official Sonim / Sonim-styled icons (brand/icons/all.json), and 6 pages instead of 4.
# Run-in bold becomes Sonim Red (small text is never bold).
F = []
CFG.update(doc='Connected care in motion', name='EMS white paper')
def page_(*a, **k): return page(F, *a, **k)
def cap(t, color=BLACK, **k): return T('Caption', t, 'caption', color, **k)

# ---------------------------------------------------------------- 1 · opening: photos, title, the challenge
PHOTOS = [('crew', 'Ambulance crew', 318, '45% 50%'), ('dispatcher', 'Dispatch center', 246, '50% 40%'), ('responder', 'Field responder, XP5plus', 252, '50% 30%')]
hero = col('Hero', [
    row('Photos', [f'<div class="stack" data-name="{esc(n)}" style="position:relative;width:{w}px;height:260px;flex:none">'
                   f'<img class="photo" data-name="Photo" data-img="{k}" alt="{esc(n)}" style="display:block;width:{w}px;height:260px;object-fit:cover;object-position:{p}">'
                   + T('Photo caption', n, 'caption', WHITE, position='absolute', left='16px', bottom='14px', **{'--bleed': '1'}) + '</div>' for k, n, w, p in PHOTOS],
        gap='none', justify_content='space-between'),
    box('Header on photo', l=0, t=0, w=W, inner=f'<div style="padding:28px {M}px 0">' + header(1, WHITE, 'Sonim white paper') + '</div>')],
    gap='none', position='relative', flex='none')
JOB = [('voice', 'Voice'), ('data', 'Data'), ('video', 'Video'), ('gps', 'GPS location'), ('patient-data', 'Patient information')]
page_('ems-opening', 'Opening page', 'US Letter · photo strip, title and the challenge', [
    col('Title block', [headline('White paper · Emergency medical services', 'Connected care\n**in motion.**', 'display'),
                        T('Lead', 'How EMS agencies are replacing legacy communications with mission-critical mobility.', 'lead', max_width='560px')], gap='lg'),
    col('Challenge', [T('Heading', 'The EMS communication challenge', 'h2'),
                      body('**Response times matter.** A study of 1.7 million EMS runs found a median response of about 7 minutes, and about 13 minutes in rural areas, where nearly one call in ten waited close to half an hour.[[1]]'),
                      body('Crews work across hospitals, highways, rural roads, events and disasters, often in one shift. More than 18,200 local EMS agencies answer about 28.5 million 911 dispatches a year.[[2]] Every call is a chain of conversations, and **when communication fails, care is delayed.**'),
                      body('**Legacy land mobile radio (LMR) has limits.** Coverage ends where the towers end, and every expansion means more sites and more capital. Meanwhile, the job now runs on more than voice:')], gap='md'),
    row('Job icons', [col(n, [icon(k, 48, n), cap(n)], gap='sm', flex='1 1 0', min_width='0') for k, n in JOB], gap='xl'),
], 1, bleed=hero, show_header=False, gap='xxl', note='1 Mell HK et al., JAMA Surgery, 2017. 2 NASEMSO, 2020 National EMS Assessment.\nPhotos: Pexels (free license), Sonim.')

# ---------------------------------------------------------------- 2 · needs + the shift (the GMR FirstNet quote closes the FirstNet argument)
quote = col('Quote band', [row('Quote row', [T('Quote', '“With FirstNet, we maintain contact with first responders nationwide during everyday crises and large disasters.”', 'quote', WHITE, flex='3 1 0'),
                                              col('Attribution', [T('Name', 'Jeffrey E. Marani', 'body', WHITE),
                                                                  cap('National Director of Field Technologies, Global Medical Response[[3]]', WHITE).replace('color:#CF102D', 'color:#FFFFFF')], gap='xs', flex='2 1 0')],
                                        gap='xxl', align_items='flex-end')], gap='lg', background=RED, padding=f'{S["xxl"]}px')

NEEDS = ['Instant PTT communication', 'Reliable coverage beyond radio range', 'Rugged devices built for frontline use', 'Dispatch integration', 'Secure connectivity and management']
need = lambda n: row('Need', [icon('check', 20, 'Check'), T('Item text', n, 'body', flex='1 1 0')], gap='md', flex='1 1 0', min_width='0')
needs_box = col('Needs callout', [T('Callout heading', 'Today’s EMS teams need:', 'h2'),
                                  row('Needs', [col('Needs column', [need(n) for n in NEEDS[:3]], gap='md', flex='1 1 0'),
                                                col('Needs column', [need(n) for n in NEEDS[3:]], gap='md', flex='1 1 0')], gap='xxl')],
                gap='lg', background=GRAY, padding=f'{S["xxl"]}px')
page_('ems-shift', 'Shift page', 'Interior · needs callout, headline, two columns and a quote band', [
    needs_box,
    col('Opening', [headline('The shift', 'Why leading EMS agencies are moving **beyond traditional radios.**'),
                    lead('EMS leaders are moving away from treating communications as a radio problem and toward an operational mobility platform: nationwide broadband, standards-based push-to-talk and rugged devices that carry voice and data together.')], gap='lg'),
    row('Two columns', [flex1('Column 1', [body('FirstNet, the public safety network built with AT&T, covers more than 3 million square miles, gives first responders priority and preemption, and serves about 31,000 agencies. More than 190 deployable assets back it up for incidents and planned events.[[3]]')]),
                        flex1('Column 2', [body('Mission-critical push-to-talk (MCPTT) brings radio-grade group calling to broadband, and gateways such as FirstNet Fusion Link connect MCPTT talkgroups to existing LMR systems. Agencies can move at their own pace without retiring the radios they already own.[[3]]')])], gap='xxl'),
    quote,
], 2, gap='xxl', note='3 FirstNet.com: EMS solutions; FirstNet Fusion; “Global Medical Response Connects Disaster Teams & Paramedics.”')

# ---------------------------------------------------------------- 3 · comparison, stats, use cases
PAIRS = [('Coverage limits', 'Nationwide coverage'), ('Voice only', 'Voice + data + video'), ('Costly infrastructure', 'Carrier-powered'),
         ('Separate devices', 'Consolidated platform'), ('Limited flexibility', 'Rapid deployment')]
def cmp_row(l, r, head=False):
    pad = f'{S["md"]}px {S["xl"]}px'
    arrow = '' if head else f'<div class="icon" data-name="Arrow" style="width:18px;height:18px;color:{RED}">{ICONS["arrow"]}</div>'
    return row('Comparison row', [col('Traditional', [T('Before', l, 'h3' if head else 'body')], flex='1 1 0', background=GRAY, padding=pad),
                                  col('Arrow cell', [arrow], width='40px', flex='none', align_items='center', justify_content='center', align_self='stretch'),
                                  col('Modern', [T('After', r, 'h3' if head else 'body', WHITE)], flex='1 1 0', background=BLACK if head else RED, padding=pad)],
               gap='none', align_items='stretch')
STATS = [('18,200+', 'Local EMS agencies answering 911 calls[[2]]'), ('28.5M', '911 dispatches a year in 41 reporting states[[2]]'), ('~31,000', 'Public safety agencies on FirstNet[[3]]')]
USES = [('ambulance', 'Ambulance operations', 'Crew-to-dispatch communications from the rig or on foot.'),
        ('interfacility', 'Interfacility transport', 'Real-time coordination between sending and receiving locations.'),
        ('events', 'Special events', 'Large crowds and mass casualty readiness.'),
        ('disaster', 'Disaster response', 'Deployable communications in disrupted environments.'),
        ('air-medical', 'Air medical operations', 'Aircraft tracking and remote connectivity.')]
page_('ems-compare', 'Comparison page', 'Interior · comparison table, stats and use cases', [
    col('Comparison', [cmp_row('Traditional LMR', 'Modern mission-critical mobility', head=True)] + [cmp_row(l, r) for l, r in PAIRS], gap='xs'),
    row('Stats', [flex1(n, [T('Number', n, 'stat', RED), cap(c)], gap='sm') for n, c in STATS], gap='xl'),
    rule(),
    col('Use cases', [T('Heading', 'EMS use cases', 'h2'),
                      row('Use case columns', [flex1(t, [icon(k, 48, t), T('Title', t, 'h3'), cap(d)] + ([cap('See GMR, page 4', RED)] if k == 'air-medical' else []), gap='sm')
                                               for k, t, d in USES], gap='lg')], gap='xl'),
], 3, gap='xxl', note='2 NASEMSO, 2020 National EMS Assessment. 3 FirstNet.com: EMS solutions; FirstNet Fusion.')

# ---------------------------------------------------------------- 4 · customer spotlight
def case(photo_key, pos, name, meta, challenge, solution, out_label, outs, extra=None):
    items = [f'<img class="photo" data-name="Case photo" data-img="{photo_key}" alt="{esc(name)}" style="display:block;width:100%;height:170px;object-fit:cover;object-position:{pos}">',
             col('Case heading', [T('Label', 'Case study', 'label', RED), T('Customer', name, 'h2'), cap(meta)], gap='xs'),
             col('Challenge', [T('Subheading', 'Challenge', 'h3', RED), body(challenge)], gap='xs'),
             col('Solution', [T('Subheading', 'Solution', 'h3', RED), body(solution)], gap='xs'),
             col(out_label, [T('Subheading', out_label, 'h3', RED), bullets(outs)], gap='sm')]
    if extra: items += [rule(), cap(extra)]
    return flex1(name, items, gap='lg')
page_('ems-proof', 'Proof page', 'Interior · two case studies', [
    headline('Customer spotlight', 'How EMS organizations **use Sonim today.**'),
    row('Case studies', [
        case('heli', '50% 45%', 'Global Medical Response (GMR)', '7,254 ground ambulances · 404 rotor-wing and 114 fixed-wing aircraft · ~5.5M patient encounters a year[[4]]',
             'Remote aircraft tracking, weak coverage and environmental extremes at air bases and landing zones.',
             'Sonim MegaConnect HPUE with FirstNet connectivity: Power Class 1 on Band 14, up to 6x the signal strength and 2x the upload speed of a standard hotspot, with external antenna ports.[[5]]',
             'Results', ['Faster deployment', 'Stronger connectivity', 'Improved performance in remote locations', 'Reliable operation in demanding environments'],
             'GMR has also deployed 1,200 FirstNet-capable Sonim XP8 smartphones to support crisis and disaster response.[[3]]'),
        case('night', '40% 50%', 'Star EMS', 'Oakland County, Michigan · 911 and non-emergency transport · in-house 24/7 dispatch center[[4]]',
             'A costly LMR system with limited scalability. Growing the fleet meant more radio infrastructure.',
             'Sonim XP5plus, Kodiak Dispatch and a FirstNet communications platform. Dispatchers make PTT calls, monitor talkgroups and see crew locations from a web console.',
             'Benefits', ['Rugged frontline communications', 'Improved dispatch coordination', 'Centralized visibility', 'Scalable communications platform'])], gap='xxl'),
], 4, gap='xxl', note='3 FirstNet.com, “Global Medical Response Connects Disaster Teams & Paramedics.”\n4 globalmedicalresponse.com; starems.com. 5 sonimtech.com, MegaConnect. Photos: Pexels (free license).')

# ---------------------------------------------------------------- 5–6 · solution stack (quote opens it, closing band ends it)
def callout(k, t, d):
    return row(t, [icon(k, 40, t), col('Callout text', [T('Callout title', t, 'body', RED, line_height='1.35'), cap(d)], gap='xs', flex='1 1 0', min_width='0')],
               gap='md', flex='1 1 0', min_width='0', align_items='center')
def callouts(items, cols=3):
    rows = [items[i:i + cols] for i in range(0, len(items), cols)]
    return col('Callouts', [row('Callout row', [callout(*c) for c in r] + ['<div style="flex:1 1 0"></div>'] * (cols - len(r)), gap='lg') for r in rows], gap='lg')
def img(k, h, name):
    return f'<img class="cutout" data-name="{esc(name)}" data-img="{k}" alt="{esc(name)}" style="display:block;height:{h}px;width:auto;max-width:100%;object-fit:contain">'
def stack_item(n, visual, title, intro, items):
    shot = col('Product image', [visual], width='176px', height='140px', flex='none', background=GRAY, align_items='center', justify_content='center', overflow='hidden')
    return col(f'{n} {title}', [row('Item heading', [T('Number', n, 'h2', RED, width='40px', flex='none'), shot,
                                                     col('Title and intro', [T('Title', title, 'h2')] + ([cap(intro)] if intro else []), gap='sm', flex='1 1 0', min_width='0')],
                                    gap='xl', align_items='center')] + items, gap='lg')
XP5 = stack_item('01', img('xp5', 124, 'XP5plus 5G'), 'XP5plus 5G',
                 'Fourth-generation radio-style handset for PTT-first crews. AT&T Enhanced PTT, FirstNet Rapid Response and FirstNet MCPTT.[[5]]',
                 [callouts([('ptt', 'Dedicated PTT', 'Side-mounted key'), ('sos', 'SOS button', 'Top-mounted key'), ('glove', 'Glove-friendly', 'Large, tactile keys'),
                            ('battery', 'Removable battery', 'Up to 25 hr talk'), ('firstnet', 'FirstNet Ready', 'Band 14 certified'), ('rugged', 'Ultra-rugged', 'IP68 · MIL-STD-810H')])])
MEGA = stack_item('02', img('mega', 104, 'MegaConnect'), 'MegaConnect',
                  'The first ultra-portable 5G HPUE hotspot, with 2.5 Gbps Ethernet and four external antenna ports.[[5]]',
                  [callouts([('signal', 'Stronger connectivity', 'Up to 6x signal'), ('megarange', 'FirstNet MegaRange', 'HPUE Power Class 1'), ('deploy', 'Mobile deployment', 'Battery-powered'),
                             ('vehicle', 'Vehicle operations', 'External antennas'), ('command', 'Incident command', 'Up to 64 devices')])])
ACC = stack_item('03', row('Accessories', [img('rsm', 104, 'Klein VALOR RSM'), img('headset', 104, 'Klein CURL headset'), img('holster', 76, 'Holster')],
                           gap='sm', align_items='center', justify_content='center'),
                 'Accessories partners', 'Speaker mics, headsets, chargers, vehicle mounts and carry solutions.',
                 [col('Partners', [row('Partner row', [col(p, [T('Partner', p, 'body', text_align='center')], flex='1 1 0', border=f'1px solid {GRAY}', padding=f'{S["md"]}px', align_items='center') for p in r], gap='md')
                                   for r in (['RAM Mounts', 'AdvanceTec', 'Klein'], ['OTTO', 'AINA', 'Stone Mountain'])], gap='md')])
MGMT = stack_item('04', f'<img class="photo" data-name="SonimWare dashboard" data-img="sonimware_dash" alt="SonimWare dashboard" style="display:block;width:176px;height:140px;object-fit:cover;object-position:0% 0%">',
                  'Management & services', None,
                  [callouts([('dispatch', 'Kodiak Dispatch', 'PTT calls, talkgroups, GPS location'), ('cloud', 'Sonim Cloud', 'Remote setup, updates, monitoring'),
                             ('software', 'SonimWare', 'SafeGuard, Kiosk Mode, SOS app'), ('support', 'Support services', 'SonimCare / FirstCare')], cols=2)])
page_('ems-solution', 'Solution page', 'Interior · headline and the first two solutions', [
    col('Opening', [headline('The Sonim EMS solution stack', 'The EMS communications **ecosystem.**'),
                    lead('More than a handset: device, connectivity, accessories and management, working as one system on AT&T and FirstNet.')], gap='lg'),
    rule(), XP5, rule(), MEGA,
], 5, gap='xxl', note='5 sonimtech.com: XP5plus 5G, MegaConnect.')

closing = col('Closing band', [
    row('Story', [col('Story heading', [T('Label', 'The real story', 'label', WHITE), T('Heading', 'No longer a **radio problem.**', 'h1', WHITE, **{'--em': BLACK})], gap='sm', width='240px', flex='none'),
                  col('Story text', [T('Body', 'EMS organizations are treating communications as an operational mobility platform. Devices like the Sonim XP5plus, connectivity such as MegaConnect, and integrated dispatch and management tools improve situational awareness, coverage, coordination and resilience while reducing dependence on traditional radio infrastructure.', 'body', WHITE),
                                     T('CTA', 'Talk to Sonim · sonimtech.com', 'h3', WHITE)], gap='lg', flex='1 1 0')], gap='xxl'),
    footer('5 sonimtech.com: SonimWare. Partner logos pending approval.', WHITE)],
    gap='xxxl', background=RED, padding=f'{S["xxxl"]}px {M}px 32px', flex='none')
page_('ems-solution-2', 'Solution page 2', 'Interior · accessories, management and a red closing band', [
    rule(), ACC, rule(), MGMT,
], 6, gap='xxl', tail=closing)
