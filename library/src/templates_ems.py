from wpkit import *

# EMS white paper "Connected care in motion": the client's latest 4-page layout
# (client file Ambulance_EMS_Whitepaper_Sonim.pdf = whitepaper/dist/Sonim_EMS_Whitepaper_editor-export.pdf).
# Copy is the client's text, verbatim; layout follows the client pages on the shared white paper design system
# (wpkit: Akzidenz-Grotesk Pro, 12 px minimum, small text regular, auto layout). Icons: the original EMS set
# (brand/icons/icons.json) used in the client's layout. Run-in bold becomes Sonim Red (small text is never bold).
F = []
CFG.update(doc='Connected care in motion', name='EMS white paper')
# Denser scale than the Inova paper so the client's 4 pages keep their 4 pages; same floor (12 px, small text regular).
CFG['type'] = dict(TYPE, display=('display', 52, 700, 1.04, '-0.03em'), h1=('h1', 30, 700, 1.12, '-0.015em'), h2=('h2', 20, 700, 1.2, '-0.01em'),
                   stat=('stat', 40, 700, 1.0, '-0.03em'), quote=('quote', 19, 700, 1.28, '-0.005em'), lead=('lead', 16, 400, 1.45, '0'),
                   body=('body', 13, 400, 1.5, '0'), caption=('small', 12, 400, 1.35, '0.01em'))
def page_(*a, **k): return page(F, *a, **k)
def cap(t, color=BLACK, **k): return T('Caption', t, 'caption', color, **k)

# ---------------------------------------------------------------- 1 · opening: photos, title, challenge, needs
PHOTOS = [('crew', 'Ambulance crew', 318, '45% 50%'), ('dispatcher', 'Dispatch center', 246, '50% 40%'), ('responder', 'Field responder, XP5plus', 252, '50% 30%')]
hero = col('Hero', [
    row('Photos', [f'<div class="stack" data-name="{esc(n)}" style="position:relative;width:{w}px;height:300px;flex:none">'
                   f'<img class="photo" data-name="Photo" data-img="{k}" alt="{esc(n)}" style="display:block;width:{w}px;height:300px;object-fit:cover;object-position:{p}">'
                   + T('Photo caption', n, 'caption', WHITE, position='absolute', left='12px', bottom='12px', **{'--bleed': '1'}) + '</div>' for k, n, w, p in PHOTOS], gap='none', justify_content='space-between'),
    box('Header on photo', l=0, t=0, w=W, inner=f'<div style="padding:28px {M}px 0">' + header(1, WHITE, 'Sonim white paper') + '</div>')],
    gap='none', position='relative', flex='none')

NEEDS = ['Instant PTT communication', 'Reliable coverage beyond radio range', 'Rugged devices built for frontline use', 'Dispatch integration', 'Secure connectivity and management']
needs_list = col('Checklist', [row('Item', [icon('check', 18, 'Check'), T('Item text', n, 'body', flex='1 1 0')], gap='sm', align_items='flex-start') for n in NEEDS], gap='sm')
JOB = [('voice', 'Voice'), ('data', 'Data'), ('video', 'Video'), ('gps', 'GPS location'), ('patient-data', 'Patient information')]
page_('ems-opening', 'Opening page', 'US Letter · photo strip, title, challenge and needs callout', [
    col('Title block', [headline('White paper · Emergency medical services', 'Connected care\n**in motion.**', 'display'),
                        T('Lead', 'How EMS agencies are replacing legacy communications with mission-critical mobility.', 'lead', max_width='560px')], gap='lg'),
    row('Challenge', [
        flex1('Challenge text', [T('Heading', 'The EMS communication challenge', 'h2'),
                                 body('**Response times matter.** A study of 1.7 million EMS runs found a median response of about 7 minutes, and about 13 minutes in rural areas, where nearly one call in ten waited close to half an hour.[[1]]'),
                                 body('Crews work across hospitals, highways, rural roads, events and disasters, often in one shift. More than 18,200 local EMS agencies answer about 28.5 million 911 dispatches a year.[[2]] Every call is a chain of conversations, and **when communication fails, care is delayed.**'),
                                 body('**Legacy land mobile radio (LMR) has limits.** Coverage ends where the towers end, and every expansion means more sites and more capital. Meanwhile, the job now runs on more than voice:'),
                                 rule(),
                                 row('Job icons', [col(n, [ems_icon(k, 36, n), cap(n)], gap='sm', flex='1 1 0', min_width='0', align_items='flex-start') for k, n in JOB], gap='md')], gap='md'),
        rugged_box('Needs container', 250, 330, [T('Callout heading', 'Today’s EMS teams need:', 'h3'), needs_list])],
        gap='xxl'),
], 1, bleed=hero, show_header=False, gap='xl', note='1 Mell HK et al., JAMA Surgery, 2017. 2 NASEMSO, 2020 National EMS Assessment.\nPhotos: Pexels (free license), Sonim.')

# ---------------------------------------------------------------- 2 · the shift: comparison, stats, use cases
PAIRS = [('Coverage limits', 'Nationwide coverage'), ('Voice only', 'Voice + data + video'), ('Costly infrastructure', 'Carrier-powered'),
         ('Separate devices', 'Consolidated platform'), ('Limited flexibility', 'Rapid deployment')]
def cmp_row(l, r, head=False):
    pad = f'{S["sm"]}px {S["lg"]}px'
    lc = T('Before', l, 'h3' if head else 'body', BLACK)
    rc = T('After', r, 'h3' if head else 'body', WHITE)
    arrow = '' if head else f'<div class="icon" data-name="Arrow" style="width:16px;height:16px;color:{RED}">{ICONS["arrow"]}</div>'
    return row('Comparison row', [col('Traditional', [lc], flex='1 1 0', background=GRAY, padding=pad),
                                  col('Arrow cell', [arrow], width='32px', flex='none', align_items='center', justify_content='center', align_self='stretch'),
                                  col('Modern', [rc], flex='1 1 0', background=BLACK if head else RED, padding=pad)], gap='none', align_items='stretch')
STATS = [('18,200+', 'Local EMS agencies answering 911 calls[[2]]'), ('28.5M', '911 dispatches a year in 41 reporting states[[2]]'), ('~31,000', 'Public safety agencies on FirstNet[[3]]')]
USES = [('ambulance', 'Ambulance operations', 'Crew-to-dispatch communications from the rig or on foot.'),
        ('interfacility', 'Interfacility transport', 'Real-time coordination between sending and receiving locations.'),
        ('events', 'Special events', 'Large crowds and mass casualty readiness.'),
        ('disaster', 'Disaster response', 'Deployable communications in disrupted environments.'),
        ('air-medical', 'Air medical operations', 'Aircraft tracking and remote connectivity.')]
page_('ems-argument', 'Argument page', 'Interior · comparison table, stats and use cases', [
    col('Opening', [headline('The shift', 'Why leading EMS agencies are moving **beyond traditional radios.**'),
                    lead('EMS leaders are moving away from treating communications as a radio problem and toward an operational mobility platform: nationwide broadband, standards-based push-to-talk and rugged devices that carry voice and data together.')], gap='lg'),
    row('Two columns', [flex1('Column 1', [body('FirstNet, the public safety network built with AT&T, covers more than 3 million square miles, gives first responders priority and preemption, and serves about 31,000 agencies. More than 190 deployable assets back it up for incidents and planned events.[[3]]')]),
                        flex1('Column 2', [body('Mission-critical push-to-talk (MCPTT) brings radio-grade group calling to broadband, and gateways such as FirstNet Fusion Link connect MCPTT talkgroups to existing LMR systems. Agencies can move at their own pace without retiring the radios they already own.[[3]]')])]),
    col('Comparison', [cmp_row('Traditional LMR', 'Modern mission-critical mobility', head=True)] + [cmp_row(l, r) for l, r in PAIRS], gap='xs'),
    row('Stats', [flex1(n, [T('Number', n, 'stat', RED), cap(c)], gap='sm') for n, c in STATS], gap='xl'),
    col('Use cases', [T('Heading', 'EMS use cases', 'h2'),
                      row('Use case columns', [flex1(t, [ems_icon(k, 36, t), T('Title', t, 'h3'), cap(d)] + ([cap('See GMR, page 3', RED)] if k == 'air-medical' else []), gap='sm')
                                               for k, t, d in USES], gap='lg')], gap='lg'),
], 2, gap='lg', note='2 NASEMSO, 2020 National EMS Assessment. 3 FirstNet.com: EMS solutions; FirstNet Fusion.')

# ---------------------------------------------------------------- 3 · customer spotlight: two case studies + quote
def case(photo_key, pos, name, meta, challenge, solution, out_label, outs, extra=None):
    items = [f'<img class="photo" data-name="Case photo" data-img="{photo_key}" alt="{esc(name)}" style="display:block;width:100%;height:150px;object-fit:cover;object-position:{pos}">',
             col('Case heading', [T('Label', 'Case study', 'label', RED), T('Customer', name, 'h2'), cap(meta)], gap='xs'),
             col('Challenge', [T('Subheading', 'Challenge', 'h3', RED), body(challenge)], gap='xs'),
             col('Solution', [T('Subheading', 'Solution', 'h3', RED), body(solution)], gap='xs'),
             col(out_label, [T('Subheading', out_label, 'h3', RED), bullets(outs)], gap='sm')]
    if extra: items += [rule(), cap(extra)]
    return flex1(name, items, gap='md')
page_('ems-proof', 'Proof page', 'Interior · two case studies and a quote band', [
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
             'Benefits', ['Rugged frontline communications', 'Improved dispatch coordination', 'Centralized visibility', 'Scalable communications platform'])], gap='xl'),
    band('Quote band', [row('Quote row', [T('Quote', '“With FirstNet, we maintain contact with first responders nationwide during everyday crises and large disasters.”', 'quote', WHITE, flex='3 1 0'),
                                          col('Attribution', [T('Name', 'Jeffrey E. Marani', 'body', WHITE), cap('National Director of Field Technologies, Global Medical Response[[3]]', WHITE).replace('color:#CF102D', 'color:#FFFFFF')], gap='xs', flex='2 1 0')],
                                    gap='xl', align_items='flex-end')]),
], 3, gap='lg', note='3 FirstNet.com, “Global Medical Response Connects Disaster Teams & Paramedics.” 4 globalmedicalresponse.com; starems.com.\n5 sonimtech.com, MegaConnect. Photos: Pexels (free license).')

# ---------------------------------------------------------------- 4 · solution stack + closing band
def callout(k, t, d):
    return row(t, [ems_icon(k, 24, t), col('Callout text', [T('Callout title', t, 'body', RED, line_height='1.3'), cap(d)], gap='none', flex='1 1 0', min_width='0')], gap='sm', flex='1 1 0', min_width='0')
def callouts(items, cols=3):
    rows = [items[i:i + cols] for i in range(0, len(items), cols)]
    return col('Callouts', [row('Callout row', [callout(*c) for c in r] + ['<div style="flex:1 1 0"></div>'] * (cols - len(r)), gap='md') for r in rows], gap='sm')
def shot(inner):
    return col('Product image', [inner], width='140px', height='92px', flex='none', background=GRAY, align_items='center', justify_content='center', overflow='hidden')
def img(k, h, name):
    return f'<img class="cutout" data-name="{esc(name)}" data-img="{k}" alt="{esc(name)}" style="display:block;height:{h}px;width:auto;max-width:100%;object-fit:contain">'
def stack_row(n, visual, title, items):
    return row(f'{n} {title}', [T('Number', n, 'h2', RED, width='36px', flex='none'), shot(visual), flex1('Details', [T('Title', title, 'h2')] + items, gap='sm')], gap='lg')
STACK = [
    ('01', img('xp5', 84, 'XP5plus 5G'), 'XP5plus 5G', [cap('Fourth-generation radio-style handset for PTT-first crews. AT&T Enhanced PTT, FirstNet Rapid Response and FirstNet MCPTT.[[5]]'),
            callouts([('ptt', 'Dedicated PTT', 'Side-mounted key'), ('sos', 'SOS button', 'Top-mounted key'), ('glove', 'Glove-friendly', 'Large, tactile keys'),
                      ('battery', 'Removable battery', 'Up to 25 hr talk'), ('firstnet', 'FirstNet Ready', 'Band 14 certified'), ('rugged', 'Ultra-rugged', 'IP68 · MIL-STD-810H')])]),
    ('02', img('mega', 76, 'MegaConnect'), 'MegaConnect', [cap('The first ultra-portable 5G HPUE hotspot, with 2.5 Gbps Ethernet and four external antenna ports.[[5]]'),
            callouts([('signal', 'Stronger connectivity', 'Up to 6x signal'), ('megarange', 'FirstNet MegaRange', 'HPUE Power Class 1'), ('deploy', 'Mobile deployment', 'Battery-powered'),
                      ('vehicle', 'Vehicle operations', 'External antennas'), ('command', 'Incident command', 'Up to 64 devices')])]),
    ('03', row('Accessories', [img('rsm', 76, 'Klein VALOR RSM'), img('headset', 76, 'Klein CURL headset'), img('holster', 56, 'Holster')], gap='xs', align_items='center', justify_content='center'),
     'Accessories partners', [cap('Speaker mics, headsets, chargers, vehicle mounts and carry solutions.'),
            col('Partners', [row('Partner row', [col(p, [cap(p, text_align='center')], flex='1 1 0', border=f'1px solid {GRAY}', padding='6px 8px', align_items='center') for p in r], gap='sm')
                             for r in (['RAM Mounts', 'AdvanceTec', 'Klein'], ['OTTO', 'AINA', 'Stone Mountain'])], gap='sm')]),
    ('04', f'<img class="photo" data-name="SonimWare dashboard" data-img="sonimware_dash" alt="SonimWare dashboard" style="display:block;width:140px;height:92px;object-fit:cover;object-position:0% 0%">',
     'Management & services', [callouts([('dispatch', 'Kodiak Dispatch', 'PTT calls, talkgroups, GPS location'), ('cloud', 'Sonim Cloud', 'Remote setup, updates, monitoring'),
                                         ('software', 'SonimWare', 'SafeGuard, Kiosk Mode, SOS app'), ('support', 'Support services', 'SonimCare / FirstCare')], cols=2)])]
closing = col('Closing band', [
    row('Story', [col('Story heading', [T('Label', 'The real story', 'label', WHITE), T('Heading', 'No longer a **radio problem.**', 'h2', WHITE, **{'--em': BLACK})], gap='xs', width='170px', flex='none'),
                  col('Story text', [T('Body', 'EMS organizations are treating communications as an operational mobility platform. Devices like the Sonim XP5plus, connectivity such as MegaConnect, and integrated dispatch and management tools improve situational awareness, coverage, coordination and resilience while reducing dependence on traditional radio infrastructure.', 'body', WHITE),
                                     T('CTA', 'Talk to Sonim · sonimtech.com', 'h3', WHITE)], gap='sm', flex='1 1 0')], gap='xl'),
    footer('5 sonimtech.com: XP5plus 5G, MegaConnect, SonimWare. Partner logos pending approval.', WHITE)],
    gap='xl', background=RED, padding=f'{S["lg"]}px {M}px 28px', flex='none')
page_('ems-solution', 'Solution page', 'Interior · solution stack and a red closing band', [
    col('Opening', [headline('The Sonim EMS solution stack', 'The EMS communications **ecosystem.**'),
                    lead('More than a handset: device, connectivity, accessories and management, working as one system on AT&T and FirstNet.')], gap='lg'),
    col('Stack', sum([[rule(), stack_row(n, v, t, items)] for n, v, t, items in STACK], []), gap='sm'),
], 4, gap='lg', tail=closing)

CFG.pop('type')
