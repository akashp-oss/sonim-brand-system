from gen import *

# Healthcare white paper, APPROVED COPY (client file Inova_Whitepaper.docx, approved 2026-10-14).
# Every sentence is the approved text, verbatim. Only allowed edits: headings set in sentence case (brand rule)
# and each "Topic: Headline" heading split into a red label + headline. Do not rewrite; do not add copy.
# Layout: 5 US Letter pages in the EMS paper system, with large official icons on Sonim Gray tiles.
F = []
X, M, W, H = 12, 60, 816, 1056
DOC = 'Healthcare resilience'

def head(folio):
    return stack('Running header', [text('Document title', DOC, 'meta', BLACK, 9), text('Folio', f'/ {folio:02d}', 'meta', BLACK, 9)],
                 t=28, r=M, style={'flex-direction': 'row', 'gap': '18px'})

def foot(note='Sonim, a NEXA company · sonimtech.com', dark=False):
    c = WHITE if dark else BLACK
    return logo(78, c, l=M, b=28, lockup=True) + text('Footnote', note, 'small abs', c, 8, {'right': f'{M}px', 'bottom': '30px', 'width': '420px', 'text-align': 'right'})

def body(t, name='Body', size=12.5, color=BLACK, **k): return text(name, t, 'body', color, size, k or None)
def h2(t, color=BLACK, size=20): return text('Heading', t, 'h2', color, size)

def bullets(items, color=BLACK, bar=RED, size=12.5, bold=False):
    return f'<div class="stack" data-name="List" style="gap:{round(size * 0.5)}px">' + ''.join(
        f'<div class="row" data-name="Item" style="gap:9px;align-items:baseline">'
        f'{fill("Bar", bar, style={"position": "relative", "width": "4px", "height": "10px", "flex": "none"})}'
        f'{text("Item text", i, "h3" if bold else "body", color, size)}</div>' for i in items) + '</div>'

def tiles(items, top, size=56, pad=16, tsize=13.5, dsize=11.5, gap=12, h=None):
    """Sonim Gray tiles: large icon, title, optional detail."""
    return box('Icon tiles', l=M, t=top, w=696, h=h, cls='row', style={'gap': f'{gap}px', 'align-items': 'stretch'}, inner=''.join(
        f'<div class="stack" data-name="{esc((t or d)[:40])}" style="flex:1;gap:8px;background:{GRAY};padding:{pad}px">{icon(k, size, (t or d)[:40])}'
        f'{text("Title", t, "h3", BLACK, tsize, {"margin-top": "4px"}) if t else ""}{text("Detail", d, "body", BLACK, dsize) if d else ""}</div>' for k, t, d in items))

def headline(label, title, top=66):
    return page_notch(X, top) + stack('Headline block', [text('Label', label, 'label', RED, 11), text('Headline', title, 'h1', BLACK, 36)], l=M, t=top, w=696, gap=6)

def lead(t, top, size=17): return text('Lead', t, 'lead abs', BLACK, size, {'left': f'{M}px', 'top': f'{top}px', 'width': '660px'})

def page(aid, name, use, inner, bg=WHITE):
    F.append(('wp', artboard(aid, f'Healthcare white paper · {name}', W, H, bg, inner, use, 'doc')))

# ---------------------------------------------------------------- 1 · title + introduction
p1 = (photo('Hero photo', 'healthcare', 0, 0, W, 340, '50% 30%')
      + head(1)
      + page_notch(X, 372)
      + stack('Title block', [text('Label', 'White paper · Healthcare', 'label', RED, 11),
                              text('Title', 'Enhancing healthcare resilience through **advanced communication infrastructure.**', 'h1', BLACK, 40)],
              l=M, t=372, w=680, gap=10)
      + stack('Introduction', [text('Label', 'Introduction', 'label', RED, 11), h2('When communication fails, care is at risk'),
                               body('In healthcare environments, communication is foundational to patient care—particularly during emergencies and system downtime.'),
                               body('As hospitals modernize and shift toward digital and VoIP-based systems, many have unintentionally introduced new points of failure.'),
                               body('Cyber incidents, power outages, and system maintenance events regularly disrupt hospital operations placing communication systems at risk when they’re needed most.')],
              l=M, t=548, w=390, gap=10)
      + rugged('Callout container', 486, 552, 270, 280, X, GRAY,
               text('Callout heading', 'When communication fails:', 'h2', BLACK, 19)
               + '<div data-name="Spacer" style="height:16px"></div>'
               + bullets(['Care teams become disconnected', 'Critical information is delayed or lost', 'Response times increase', 'Patient safety is placed at risk'], size=13.5, bold=True))
      + fill('Rule', GRAY, l=M, t=882, w=696, h=1)
      + lead('To address this risk, the organization sought a resilient, simple replacement for the traditional hospital “red phone”—a device long relied upon for always‑available communication during critical events.', 898, 15)
      + foot('Photo: sonimtech.com'))
page('hc-opening', 'Opening page', 'US Letter · title, introduction and callout', p1)

# ---------------------------------------------------------------- 2 · a shift in strategy + the system in practice
SOLUTION = [('custom-side-button', 'Sonim XP5plus devices (no knobs)', None),
            ('battery-general', 'Red docking Base Station from AdvanceTec', None),
            ('sonim-ware', 'SonimWare enabled with Kiosk Mode', None)]
p2 = (head(2)
      + headline('A shift in strategy', 'Replacing the traditional **“red phone.”**')
      + lead('Rather than continuing to invest in aging analog infrastructure, the organization made a deliberate shift toward a modern, resilient replacement for the hospital’s traditional red phone.', 134)
      + box('Two columns', l=M, t=222, w=696, cls='row', style={'gap': '20px'}, inner=
            body('At the center of this deployment is the Sonim XP5plus—from Sonim, a NEXA company—selected as a purpose‑built solution to preserve always‑available communication during downtime and emergency events. This deployment represents the organization’s first‑generation use of Sonim devices, focused on solving a clearly defined operational problem rather than introducing unnecessary complexity.', 'Column 1', flex='1')
            + body('The goal was straightforward: replace the legacy red phone with an affordable, fixed‑location device that delivers reliable communication without relying on internal networks or VoIP infrastructure. By maintaining a familiar form factor while modernizing the underlying technology, the organization ensured staff adoption without changing established workflows.', 'Column 2', flex='1'))
      + text('Section heading', 'The solution consists of:', 'h3 abs', BLACK, 13.5, {'left': f'{M}px', 'top': '390px'})
      + tiles(SOLUTION, 416, size=60)
      + fill('Rule', GRAY, l=M, t=574, w=696, h=1)
      + stack('System block', [text('Label', 'The system in practice', 'label', RED, 11), h2('Simple, fixed, and always available'),
                               box('Three columns', cls='row', style={'gap': '20px'}, inner=
                                   body('The Sonim XP5plus operates independently of the hospital’s internal network, ensuring communication remains available when VoIP and IP-based systems are offline.', 'Column 1', flex='1')
                                   + body('Docked in highly visible red AdvanceTec Base Station, the devices are immediately recognizable and accessible, preserving the visual and functional expectations of the traditional red phone.', 'Column 2', flex='1')
                                   + body('No additional accessories were required beyond the red cradle, reinforcing a clean, purpose‑built deployment.', 'Column 3', flex='1'))],
              l=M, t=594, w=696, gap=8)
      + box('System band', l=M, t=790, w=696, h=140, cls='group', inner=fill('Band fill', RED, l=0, t=0, w=696, h=140)
            + text('Band label', 'Together, this creates a system that is:', 'label abs', WHITE, 11, {'left': '24px', 'top': '22px'})
            + box('Qualities', l=24, t=54, w=648, cls='row', style={'gap': '24px'}, inner=''.join(
                text('Quality', q, 'h2', WHITE, 22, {'flex': '1'}) for q in ['Always available', 'Immediately deployable', 'Simple to use under stress'])))
      + foot())
page('hc-strategy', 'Strategy page', 'Interior · solution tiles and a red band', p2)

# ---------------------------------------------------------------- 3 · real-world application + continuity + preparedness
PROVIDERS = [('patient-data', 'Escalate patient concerns without delay', None), ('multiple-users', 'Coordinate treatment plans in real time', None),
             ('command', 'Maintain operational awareness during disruptions', None)]
p3 = (head(3)
      + headline('Real-world application', 'From disruption **to continuity.**')
      + lead('During outages or downtime events, staff simply use the docked Sonim devices to communicate without relying on internal systems.', 134)
      + body('The combination of an affordable device and fixed red cradle delivers reliable communication without the cost or complexity of maintaining analog lines.', 'Body', **{'position': 'absolute', 'left': f'{M}px', 'top': '196px', 'width': '660px'})
      + fill('Rule', GRAY, l=M, t=244, w=696, h=1)
      + stack('Continuity block', [text('Label', 'Protecting what matters most', 'label', RED, 11), h2('Continuity of care'),
                                   body('At its core, this deployment protects continuity of care during moments when communications are most critical.'),
                                   text('Lead-in', 'Providers are able to:', 'h3', BLACK, 13.5)],
              l=M, t=264, w=696, gap=8)
      + tiles(PROVIDERS, 390, size=60)
      + body('By preserving reliable communication, the organization reduces risk linked to delayed or failed coordination.', 'Body', **{'position': 'absolute', 'left': f'{M}px', 'top': '552px', 'width': '660px'})
      + fill('Rule', GRAY, l=M, t=590, w=696, h=1)
      + stack('Preparedness block', [h2('Strengthening emergency preparedness'),
                                     box('Two columns', cls='row', style={'gap': '20px'}, inner=
                                         '<div class="stack" data-name="Column 1" style="flex:1;gap:10px">'
                                         + body('Beyond day-to-day operations, this communication model strengthens the organization’s ability to respond to emergencies.')
                                         + body('While the deployment is primarily focused on replacing the hospital red phone, the fixed‑location Sonim devices support emergency workflows by maintaining reliable communication points during incidents.') + '</div>'
                                         + body('Command centers maintain continuous connectivity with hospitals and departments, enabling real-time situational awareness and coordinated decision-making.', 'Column 2', flex='1'))],
              l=M, t=608, w=696, gap=10)
      + box('Statement band', l=M, t=790, w=696, h=150, cls='group', inner=fill('Band fill', RED, l=0, t=0, w=696, h=150)
            + text('Statement', 'Most importantly, the solution provides a redundant communication option that operates **independently of traditional telephony and IP-based systems.**', 'quote abs', WHITE, 19, {'left': '26px', 'top': '26px', 'width': '420px', '--em': BLACK})
            + text('Detail', 'This eliminates the risk of a single point of failure and ensures that communication remains intact even when primary systems are compromised.',
                   'small abs', WHITE, 10.5, {'left': '476px', 'bottom': '26px', 'width': '196px', 'font-weight': '700'}))
      + foot())
page('hc-continuity', 'Continuity page', 'Interior · icon tiles and a red statement band', p3)

# ---------------------------------------------------------------- 4 · implementation + measurable impact
STEPS = [('multiple-users', None, 'Devices are pre-assigned to departments, eliminating uncertainty during incidents. Docking stations are placed in visible, accessible locations, reinforcing their role as dependable operational tools rather than emergency afterthoughts.'),
         ('user-friendly', None, 'Because the devices mirror the traditional red phone experience, minimal training is required. Familiarity is preserved by design.'),
         ('battery-general', None, 'Basic readiness checks ensure devices remain powered, docked, and available when needed.')]
IMPACT = [('tower', 'Operationally, organizations experience:', ['Reliable communication during telephony or system outages', 'Reduced reliance on aging analog phone infrastructure', 'Simplified device control using SonimWare Kiosk Mode']),
          ('patient-data', 'Clinically, the benefits are clear:', ['Maintained continuity of care', 'Improved response to critical patient events', 'Reduced delays linked to communication failures']),
          ('rps-general', 'From a regulatory perspective, the system supports compliance with:', ['CMS Emergency Preparedness requirements', 'Joint Commission Emergency Management standards', 'National best practices for resilient communication'])]
p4 = (head(4)
      + headline('White paper · Healthcare', 'From implementation **to integration.**')
      + lead('The success of this initiative is rooted not only in the technology, but in how it is implemented.', 134)
      + tiles(STEPS, 190, size=56, dsize=11.5)
      + fill('Rule', GRAY, l=M, t=430, w=696, h=1)
      + stack('Impact intro', [text('Label', 'Demonstrating value', 'label', RED, 11), h2('Measurable impact'),
                               body('The impact of this deployment is both immediate and measurable.')], l=M, t=450, w=696, gap=8)
      + box('Impact columns', l=M, t=548, w=696, cls='row', style={'gap': '20px'}, inner=''.join(
            f'<div class="stack" data-name="{esc(t[:30])}" style="flex:1;gap:10px">{icon(k, 56, t[:30])}{text("Subheading", t, "h3", RED, 12.5)}{bullets(i, size=11.5)}</div>' for k, t, i in IMPACT))
      + lead('More broadly, it strengthens the organization’s position as a high-reliability system, capable of operating effectively under any condition.', 780, 15)
      + foot())
page('hc-impact', 'Impact page', 'Interior · implementation tiles and impact columns', p4)

# ---------------------------------------------------------------- 5 · conclusion
ENSURE = [('multiple-users', 'Teams remain connected', None), ('command', 'Operations remain coordinated', None), ('patient-data', 'Patients continue to receive safe, timely care', None)]
p5 = (box('Conclusion band', l=0, t=0, w=W, h=470, cls='group', inner=fill('Band fill', RED, l=0, t=0, w=W, h=470)
          + stack('Running header', [text('Document title', DOC, 'meta', WHITE, 9), text('Folio', '/ 05', 'meta', WHITE, 9)], t=28, r=M, style={'flex-direction': 'row', 'gap': '18px'})
          + page_notch(X, 96, WHITE)
          + stack('Headline block', [text('Label', 'Conclusion', 'label', WHITE, 11),
                                     text('Headline', 'Redefining communication as a **strategic asset.**', 'h1', WHITE, 40, {'--em': BLACK})], l=M, t=96, w=620, gap=8)
          + stack('Body', [body('In healthcare, resilience is not defined by the absence of disruption, but by the ability to continue operating despite it.', size=15, color=WHITE),
                           body('By replacing the legacy red phone with Sonim XP5plus devices in red AdvanceTec Base Station, the organization modernized a critical communication function without changing how staff work.', size=15, color=WHITE)],
                  l=M, t=250, w=620, gap=12))
      + text('Lead-in', 'By investing in a redundant, resilient communication ecosystem, healthcare organizations ensure that:', 'h3 abs', BLACK, 15, {'left': f'{M}px', 'top': '510px', 'width': '660px'})
      + tiles(ENSURE, 556, size=64, pad=18, tsize=15)
      + lead('Even in the face of system failure, the mission does not stop.', 760)
      + text('Closing line', 'Communication endures. **Care continues.**', 'h1 abs', BLACK, 34, {'left': f'{M}px', 'top': '808px', 'width': '696px'})
      + foot())
page('hc-conclusion', 'Conclusion', 'Closing page · red conclusion band and icon tiles', p5)
