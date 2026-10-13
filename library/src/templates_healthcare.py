from gen import *

# Healthcare white paper: "Enhancing healthcare resilience through advanced communication infrastructure"
# Content: client Word file (hospital "red phone" replacement with Sonim XP5plus + AdvanceTec base station).
# Copy is the client's own; headings converted to sentence case (brand rule). No statistics, quotes or
# customer name were added: the source has none. US Letter, same system as the EMS white paper (M 60, X 12).
F = []
X, M, W, H = 12, 60, 816, 1056
DOC = 'Healthcare resilience'

def head(folio, dark=False):
    c = WHITE if dark else BLACK
    return stack('Running header', [text('Document title', DOC, 'meta', c, 9), text('Folio', f'/ {folio:02d}', 'meta', c, 9)],
                 t=28, r=M, style={'flex-direction': 'row', 'gap': '18px'})

def foot(note='Sonim, a NEXA company · sonimtech.com'):
    return logo(78, BLACK, l=M, b=28, lockup=True) + text('Footnote', note, 'small abs', BLACK, 8, {'right': f'{M}px', 'bottom': '30px', 'width': '380px', 'text-align': 'right'})

def body(t, name='Body', **k): return text(name, t, 'body', BLACK, 12.5, k or None)
def h2(t, color=BLACK): return text('Heading', t, 'h2', color, 20)

def bullets(items, color=BLACK, bar=RED, size=12.5, bold=False):
    return f'<div class="stack" data-name="List" style="gap:{round(size * 0.6)}px">' + ''.join(
        f'<div class="row" data-name="Item" style="gap:9px;align-items:baseline">'
        f'{fill("Bar", bar, style={"position": "relative", "width": "4px", "height": "10px", "flex": "none"})}'
        f'{text("Item text", i, "h3" if bold else "body", color, size)}</div>' for i in items) + '</div>'

def page(n, aid, name, use, inner, bg=WHITE):
    F.append(('wp', artboard(aid, f'Healthcare white paper · {name}', W, H, bg, inner, use, 'doc')))

# ---------------------------------------------------------------- page 1: cover + introduction
p1 = (photo('Hero photo', 'healthcare', 0, 0, W, 360, '50% 30%')
      + head(1)
      + page_notch(X, 392)
      + stack('Title block', [text('Label', 'White paper · Healthcare', 'label', RED, 11),
                              text('Title', 'Enhancing healthcare resilience through **advanced communication infrastructure.**', 'h1', BLACK, 38),
                              text('Subtitle', 'Replacing the hospital “red phone” with an always-available, purpose-built device.', 'lead', BLACK, 17, {'max-width': '560px', 'margin-top': '4px'})],
              l=M, t=392, w=660, gap=10)
      + stack('Introduction', [h2('Introduction: when communication fails, care is at risk'),
                               body('In healthcare environments, communication is foundational to patient care, particularly during emergencies and system downtime.'),
                               body('As hospitals modernize and shift toward digital and VoIP-based systems, many have unintentionally introduced new points of failure. Cyber incidents, power outages, and system maintenance events regularly disrupt hospital operations, placing communication systems at risk when they’re needed most.'),
                               body('To address this risk, the organization sought a resilient, simple replacement for the traditional hospital “red phone”: a device long relied upon for always-available communication during critical events.')],
              l=M, t=610, w=390, gap=10)
      + rugged('Callout container', 486, 614, 270, 300, X, GRAY,
               text('Callout heading', 'When communication fails:', 'h2', BLACK, 19)
               + '<div data-name="Spacer" style="height:18px"></div>'
               + bullets(['Care teams become disconnected', 'Critical information is delayed or lost', 'Response times increase', 'Patient safety is placed at risk'], size=14, bold=True))
      + foot())
page(1, 'hc-opening', 'Opening page', 'US Letter · cover and introduction', p1)

# ---------------------------------------------------------------- page 2: the shift + the system
SOLUTION = [('custom-side-button', 'Sonim XP5plus', 'Devices in the no-knob configuration.'),
            ('battery-general', 'Red docking base station', 'From accessory partner AdvanceTec.'),
            ('sonim-ware', 'SonimWare', 'Enabled with Kiosk Mode.')]
p2 = (head(2)
      + page_notch(X, 66)
      + stack('Headline block', [text('Label', 'A shift in strategy', 'label', RED, 11),
                                 text('Headline', 'Replacing the traditional **“red phone.”**', 'h1', BLACK, 36)], l=M, t=66, w=696, gap=6)
      + text('Lead', 'Rather than continuing to invest in aging analog infrastructure, the organization made a deliberate shift toward a modern, resilient replacement for the hospital’s traditional red phone.',
             'lead abs', BLACK, 17, {'left': f'{M}px', 'top': '134px', 'width': '660px'})
      + box('Two columns', l=M, t=222, w=696, cls='row', style={'gap': '20px'}, inner=
            body('At the center of this deployment is the Sonim XP5plus, from Sonim, a NEXA company, selected as a purpose-built solution to preserve always-available communication during downtime and emergency events. It is the organization’s first-generation use of Sonim devices, focused on solving a clearly defined operational problem rather than introducing unnecessary complexity.', 'Column 1', flex='1')
            + body('The goal was straightforward: replace the legacy red phone with an affordable, fixed-location device that delivers reliable communication without relying on internal networks or VoIP infrastructure. By maintaining a familiar form factor while modernizing the underlying technology, the organization ensured staff adoption without changing established workflows.', 'Column 2', flex='1'))
      + text('Section heading', 'The solution consists of', 'h3 abs', BLACK, 13, {'left': f'{M}px', 'top': '412px'})
      + box('Solution tiles', l=M, t=440, w=696, cls='row', style={'gap': '12px'}, inner=''.join(
            f'<div class="stack" data-name="{t}" style="flex:1;gap:6px;background:{GRAY};padding:16px 16px 18px">{icon(k, 44, t)}'
            f'{text("Title", t, "h3", BLACK, 13.5, {"margin-top": "4px"})}{text("Detail", d, "small", BLACK, 10.5)}</div>' for k, t, d in SOLUTION))
      + fill('Rule', GRAY, l=M, t=590, w=696, h=1)
      + stack('System block', [h2('The system in practice: simple, fixed and always available'),
                               box('Two columns', cls='row', style={'gap': '20px'}, inner=
                                   body('The Sonim XP5plus operates independently of the hospital’s internal network, ensuring communication remains available when VoIP and IP-based systems are offline.', 'Column 1', flex='1')
                                   + body('Docked in a highly visible red AdvanceTec base station, the devices are immediately recognizable and accessible, preserving the visual and functional expectations of the traditional red phone. No additional accessories were required beyond the red cradle.', 'Column 2', flex='1'))],
              l=M, t=610, w=696, gap=10)
      + box('System band', l=M, t=790, w=696, h=128, cls='group', inner=fill('Band fill', RED, l=0, t=0, w=696, h=128)
            + text('Band label', 'Together, this creates a system that is:', 'label abs', WHITE, 11, {'left': '24px', 'top': '20px'})
            + box('Qualities', l=24, t=52, w=648, cls='row', style={'gap': '24px'}, inner=''.join(
                text('Quality', q, 'h2', WHITE, 21, {'flex': '1'}) for q in ['Always available.', 'Immediately deployable.', 'Simple to use under stress.'])))
      + foot())
page(2, 'hc-strategy', 'Strategy page', 'Interior · solution tiles and a red statement band', p2)

# ---------------------------------------------------------------- page 3: continuity + preparedness
PROVIDERS = [('patient-data', 'Escalate patient concerns without delay'), ('multiple-users', 'Coordinate treatment plans in real time'), ('tower', 'Maintain operational awareness during disruptions')]
p3 = (head(3)
      + page_notch(X, 66)
      + stack('Headline block', [text('Label', 'Real-world application', 'label', RED, 11),
                                 text('Headline', 'From disruption **to continuity.**', 'h1', BLACK, 36)], l=M, t=66, w=696, gap=6)
      + text('Lead', 'During outages or downtime events, staff simply use the docked Sonim devices to communicate without relying on internal systems. The combination of an affordable device and a fixed red cradle delivers reliable communication without the cost or complexity of maintaining analog lines.',
             'lead abs', BLACK, 17, {'left': f'{M}px', 'top': '134px', 'width': '660px'})
      + fill('Rule', GRAY, l=M, t=262, w=696, h=1)
      + stack('Continuity block', [h2('Protecting what matters most: continuity of care'),
                                   body('At its core, this deployment protects continuity of care during moments when communications are most critical. Providers are able to:')],
              l=M, t=284, w=696, gap=10)
      + box('Provider abilities', l=M, t=372, w=696, cls='row', style={'gap': '16px'}, inner=''.join(
            f'<div class="stack" data-name="{t}" style="flex:1;gap:8px">{icon(k, 44, t)}{text("Title", t, "h3", BLACK, 13.5)}</div>' for k, t in PROVIDERS))
      + body('By preserving reliable communication, the organization reduces risk linked to delayed or failed coordination.', 'Body abs', **{'position': 'absolute', 'left': f'{M}px', 'top': '478px', 'width': '660px'})
      + fill('Rule', GRAY, l=M, t=524, w=696, h=1)
      + stack('Preparedness block', [h2('Strengthening emergency preparedness'),
                                     box('Two columns', cls='row', style={'gap': '20px'}, inner=
                                         '<div class="stack" data-name="Column 1" style="flex:1;gap:10px">'
                                         + body('Beyond day-to-day operations, this communication model strengthens the organization’s ability to respond to emergencies.')
                                         + body('While the deployment is primarily focused on replacing the hospital red phone, the fixed-location Sonim devices support emergency workflows by maintaining reliable communication points during incidents.') + '</div>'
                                         + body('Command centers maintain continuous connectivity with hospitals and departments, enabling real-time situational awareness and coordinated decision-making.', 'Column 2', flex='1'))],
              l=M, t=546, w=696, gap=10)
      + box('Statement band', l=M, t=770, w=696, h=160, cls='group', inner=fill('Band fill', RED, l=0, t=0, w=696, h=160)
            + text('Band label', 'Most importantly', 'label abs', WHITE, 11, {'left': '26px', 'top': '24px'})
            + text('Statement', 'A redundant communication option that operates **independently of traditional telephony and IP-based systems.**', 'quote abs', WHITE, 21, {'left': '26px', 'top': '46px', 'width': '420px', '--em': BLACK})
            + text('Detail', 'This eliminates the risk of a single point of failure and ensures that communication remains intact even when primary systems are compromised.', 'small abs', WHITE, 10.5, {'left': '482px', 'bottom': '24px', 'width': '190px', 'font-weight': '700'}))
      + foot())
page(3, 'hc-continuity', 'Continuity page', 'Interior · icon row and a red statement band', p3)

# ---------------------------------------------------------------- page 4: implementation, impact, conclusion
STEPS = [('01', 'Devices are pre-assigned to departments, eliminating uncertainty during incidents.'),
         ('02', 'Docking stations sit in visible, accessible locations: dependable operational tools, not emergency afterthoughts.'),
         ('03', 'Because the devices mirror the traditional red phone experience, minimal training is required.'),
         ('04', 'Basic readiness checks ensure devices remain powered, docked and available when needed.')]
IMPACT = [('Operationally, organizations experience:', ['Reliable communication during telephony or system outages', 'Reduced reliance on aging analog phone infrastructure', 'Simplified device control using SonimWare Kiosk Mode']),
          ('Clinically, the benefits are clear:', ['Maintained continuity of care', 'Improved response to critical patient events', 'Reduced delays linked to communication failures']),
          ('The system supports compliance with:', ['CMS Emergency Preparedness requirements', 'Joint Commission Emergency Management standards', 'National best practices for resilient communication'])]
p4 = (head(4)
      + page_notch(X, 66)
      + stack('Headline block', [text('Label', 'From implementation to integration', 'label', RED, 11),
                                 text('Headline', 'Familiarity, **preserved by design.**', 'h1', BLACK, 36)], l=M, t=66, w=696, gap=6)
      + text('Lead', 'The success of this initiative is rooted not only in the technology, but in how it is implemented.', 'lead abs', BLACK, 17, {'left': f'{M}px', 'top': '134px', 'width': '660px'})
      + box('Steps', l=M, t=198, w=696, cls='row', style={'gap': '16px'}, inner=''.join(
            f'<div class="stack" data-name="Step {n}" style="flex:1;gap:6px">{text("Number", n, "stat", RED, 28)}{text("Text", t, "small", BLACK, 10.5)}</div>' for n, t in STEPS))
      + fill('Rule', GRAY, l=M, t=328, w=696, h=1)
      + stack('Impact intro', [h2('Demonstrating value: measurable impact'),
                               body('The impact of this deployment is both immediate and measurable.')], l=M, t=348, w=696, gap=8)
      + box('Impact columns', l=M, t=420, w=696, cls='row', style={'gap': '20px'}, inner=''.join(
            f'<div class="stack" data-name="{t}" style="flex:1;gap:8px">{text("Subheading", t, "h3", RED, 12.5)}{bullets(i, size=11)}</div>' for t, i in IMPACT))
      + text('Note', 'More broadly, it strengthens the organization’s position as a high-reliability system, capable of operating effectively under any condition.',
             'body abs', BLACK, 12.5, {'left': f'{M}px', 'top': '578px', 'width': '660px'})
      + box('Closing band', l=0, t=632, w=W, h=424, cls='group', inner=fill('Band fill', RED, l=0, t=0, w=W, h=424)
            + text('Label', 'Conclusion', 'label abs', WHITE, 11, {'left': f'{M}px', 'top': '36px'})
            + text('Heading', 'Redefining communication as a **strategic asset.**', 'h1 abs', WHITE, 30, {'left': f'{M}px', 'top': '56px', 'width': '440px', '--em': BLACK})
            + text('Body', 'In healthcare, resilience is not defined by the absence of disruption, but by the ability to continue operating despite it. By replacing the legacy red phone with Sonim XP5plus devices in red AdvanceTec base stations, the organization modernized a critical communication function without changing how staff work.',
                   'body abs', WHITE, 12.5, {'left': f'{M}px', 'top': '160px', 'width': '400px'})
            + stack('Ensures', [text('Ensures label', 'A redundant, resilient ecosystem ensures that:', 'h3', WHITE, 12.5),
                                bullets(['Teams remain connected', 'Operations remain coordinated', 'Patients continue to receive safe, timely care'], WHITE, WHITE, 12.5, True)],
                    l=500, t=160, w=256, gap=10)
            + text('Closing line', 'Communication endures. **Care continues.**', 'h2 abs', WHITE, 24, {'left': f'{M}px', 'top': '296px', 'width': '696px', '--em': BLACK})
            + logo(78, WHITE, l=M, b=28, lockup=True)
            + text('Footnote', 'Sonim, a NEXA company · sonimtech.com', 'small abs', WHITE, 8, {'right': f'{M}px', 'bottom': '30px', 'text-align': 'right'})))
page(4, 'hc-impact', 'Impact and conclusion', 'Closing page · numbered steps, impact columns, red conclusion band', p4)
