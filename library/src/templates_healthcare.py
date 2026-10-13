from gen import *

# Healthcare white paper: Inova replaces the hospital "red phone" (Whitepapers set, ids hc-*).
# Brief: the client's Word file (Inova_Whitepaper.docx). Written with the same flow and writing rules as the
# EMS paper (zate/cc-plugins blog-writer skill: lead with the point, vary rhythm, no AI tells), then a de-AI
# pass. Facts come from the brief or CONTEXT.md §8; no statistics or quotes were invented. Verify before
# publishing: Inova named with approval, the 42 CFR §482.15(c) citation, and the Inova case-study details.
F = []
X, M, W, H = 12, 60, 816, 1056
DOC = 'Care continues'

def head(folio, dark=False):
    c = WHITE if dark else BLACK
    return stack('Running header', [text('Document title', DOC, 'meta', c, 9), text('Folio', f'/ {folio:02d}', 'meta', c, 9)],
                 t=28, r=M, style={'flex-direction': 'row', 'gap': '18px'})

def foot(note):
    return logo(78, BLACK, l=M, b=28, lockup=True) + text('Footnote', note, 'small abs', BLACK, 8, {'right': f'{M}px', 'bottom': '30px', 'width': '420px', 'text-align': 'right'})

def body(t, name='Body', size=12.5, **k): return text(name, t, 'body', BLACK, size, k or None)
def lead_in(bold, rest, size=12.5):
    """Paragraph with a bold black lead-in sentence (EMS paper style)."""
    return f'<div class="tx body" data-name="Body" style="color:{BLACK};font-size:{size}px"><b data-name="Lead-in">{esc(bold)}</b> {esc(rest)}</div>'

def h2(t, color=BLACK, size=20): return text('Heading', t, 'h2', color, size)

def bullets(items, color=BLACK, bar=RED, size=12.5, bold=False):
    return f'<div class="stack" data-name="List" style="gap:{round(size * 0.5)}px">' + ''.join(
        f'<div class="row" data-name="Item" style="gap:9px;align-items:baseline">'
        f'{fill("Bar", bar, style={"position": "relative", "width": "4px", "height": "10px", "flex": "none"})}'
        f'{text("Item text", i, "h3" if bold else "body", color, size)}</div>' for i in items) + '</div>'

def tiles(items, top, size=56, pad=16, tsize=13.5, dsize=10.5, title=None, gap=12):
    """Row of Sonim Gray tiles, each with a large icon, a title and an optional detail line."""
    row = box('Icon tiles', l=M, t=top + (34 if title else 0), w=696, cls='row', style={'gap': f'{gap}px', 'align-items': 'stretch'}, inner=''.join(
        f'<div class="stack" data-name="{t}" style="flex:1;gap:8px;background:{GRAY};padding:{pad}px">{icon(k, size, t)}'
        f'{text("Title", t, "h3", BLACK, tsize, {"margin-top": "4px"})}{text("Detail", d, "small", BLACK, dsize) if d else ""}</div>' for k, t, d in items))
    return (text('Section heading', title, 'h2 abs', BLACK, 20, {'left': f'{M}px', 'top': f'{top}px'}) if title else '') + row

def page(aid, name, use, inner):
    F.append(('wp', artboard(aid, f'Healthcare white paper · {name}', W, H, WHITE, inner, use, 'doc')))

# ---------------------------------------------------------------- 1 · cover + the challenge
p1 = (photo('Hero photo', 'healthcare', 0, 0, W, 372, '50% 30%')
      + head(1)
      + page_notch(X, 404)
      + stack('Title block', [text('Label', 'White paper · Healthcare', 'label', RED, 11),
                              text('Title', 'Care continues\n**when systems don’t.**', 'display', BLACK, 56),
                              text('Subtitle', 'How Inova replaced the hospital red phone with communication that works through downtime.', 'lead', BLACK, 17, {'max-width': '540px', 'margin-top': '4px'})],
              l=M, t=404, w=680, gap=10)
      + stack('Challenge', [h2('The downtime communication gap'),
                            lead_in('Downtime is routine now.', 'Cyber incidents, power outages and planned maintenance take hospital systems offline on a regular basis. Every one of them tests whether care teams can still reach each other.'),
                            lead_in('Modern phones share the network’s weak spots.', 'As hospitals move voice onto VoIP and IP systems, the phone starts depending on the same infrastructure that fails in an outage. When the network goes down, the phones go with it.'),
                            body('For decades the answer was the red phone: one fixed line that worked when nothing else did. Keeping that analog infrastructure alive is getting harder to justify.')],
              l=M, t=636, w=390, gap=12)
      + rugged('Callout container', 486, 640, 270, 280, X, GRAY,
               text('Callout heading', 'When communication fails:', 'h2', BLACK, 19)
               + '<div data-name="Spacer" style="height:16px"></div>'
               + bullets(['Care teams become disconnected', 'Critical information is delayed or lost', 'Response times increase', 'Patient safety is placed at risk'], size=13.5, bold=True))
      + foot('Photo: sonimtech.com.'))
page('hc-opening', 'Opening page', 'US Letter · cover, challenge and callout', p1)

# ---------------------------------------------------------------- 2 · the shift
ROWS = [('A single point of failure', 'Independent of the hospital network'),
        ('Costly analog lines to maintain', 'No analog lines to maintain'),
        ('New system, new training', 'Same red phone workflow'),
        ('Hard to control at scale', 'Locked down with SonimWare Kiosk Mode'),
        ('Unclear ownership in a crisis', 'Pre-assigned to departments')]
USES = [('disaster', 'Cyber incidents', None), ('battery-general', 'Power outages', None), ('sonim-ware', 'Planned maintenance', None),
        ('command', 'Emergency command', None), ('multiple-users', 'Critical escalation', None)]
p2 = (head(2)
      + page_notch(X, 66)
      + stack('Headline block', [text('Label', 'The shift', 'label', RED, 11),
                                 text('Headline', 'Why hospitals are rethinking\n**the red phone.**', 'h1', BLACK, 36)], l=M, t=66, w=690, gap=6)
      + text('Lead', 'The red phone was never about the phone. It was a promise: one place where communication works, every time. Inova kept the promise and replaced the technology underneath it.',
             'lead abs', BLACK, 17, {'left': f'{M}px', 'top': '176px', 'width': '650px'})
      + box('Two columns', l=M, t=262, w=696, cls='row', style={'gap': '20px'}, inner=
            body('Analog red phones depend on copper lines and legacy equipment that hospitals are steadily retiring. Moving them onto VoIP fixes the cost problem and creates a worse one: the phone now fails at the exact moment it is needed, when the network is down.', 'Column 1', flex='1')
            + body('A device that runs independently of the hospital network removes that dependency. Docked in a fixed, recognizable cradle, it keeps the red phone’s role and the way staff use it, while taking it off the hospital’s own infrastructure.', 'Column 2', flex='1'))
      + box('Comparison', l=M, t=376, w=696, h=230, cls='group', inner=
            fill('Before fill', GRAY, l=0, t=0, w=330, h=230) + fill('After fill', RED, l=366, t=0, w=330, h=230)
            + fill('After header fill', BLACK, l=366, t=0, w=330, h=40)
            + text('Before header', 'Network-dependent phones', 'h3 abs', BLACK, 13, {'left': '16px', 'top': '12px'})
            + text('After header', 'Sonim XP5plus as the red phone', 'h3 abs', WHITE, 13, {'left': '382px', 'top': '12px'})
            + ''.join(text('Before', a, 'body abs', BLACK, 12.5, {'left': '16px', 'top': f'{52+i*36}px'}) + fill('Divider', WHITE, l=0, t=44 + i * 36 - 4, w=330, h=1)
                      + text('Arrow', '→', 'h3 abs', RED, 14, {'left': '341px', 'top': f'{50+i*36}px'})
                      + text('After', b, 'h3 abs', WHITE, 12.5, {'left': '382px', 'top': f'{52+i*36}px'}) for i, (a, b) in enumerate(ROWS)))
      + tiles(USES, 640, size=60, pad=14, tsize=12.5, title='Where it matters')
      + fill('Rule', GRAY, l=M, t=846, w=696, h=1)
      + stack('Preparedness', [h2('Built for preparedness requirements', size=16),
                               body('Federal emergency preparedness rules require hospitals to plan for primary and alternate means of communication.¹ A red phone that does not share the network’s failure points gives that plan a physical, testable form: a known device, in a known place, checked on a schedule.')],
              l=M, t=862, w=660, gap=6)
      + foot('1 CMS Emergency Preparedness Rule, 42 CFR §482.15(c). Comparison reflects the Inova deployment on page 3.'))
page('hc-shift', 'Shift page', 'Interior · comparison and use cases', p2)

# ---------------------------------------------------------------- 3 · customer spotlight
CASE_ICONS = {'Challenge': 'disaster', 'Solution': 'sonim-ware', 'Results': 'rps-general'}
CASE = [('Challenge', 'Inova needed a dependable replacement for the hospital red phone: an always-available line for critical events that keeps working through cyber incidents, power outages and system maintenance, without the cost of analog lines or added complexity.'),
        ('Solution', 'Sonim XP5plus devices in a no-knob configuration, docked in red AdvanceTec base stations, with SonimWare Kiosk Mode. Each device is pre-assigned to a department and placed where staff expect the red phone to be. Nothing else was needed.')]
RESULTS = ['Reliable communication during telephony or system outages', 'Less reliance on aging analog phone infrastructure', 'Simpler device control with Kiosk Mode', 'Minimal training: the workflow did not change']
CARE = [('patient-data', 'Escalate patient concerns', 'Without waiting for systems to recover.'), ('multiple-users', 'Coordinate treatment', 'In real time, across departments.'),
        ('command', 'Keep command connected', 'Situational awareness during incidents.')]
p3 = (head(3)
      + page_notch(X, 66)
      + stack('Headline block', [text('Label', 'Customer spotlight', 'label', RED, 11),
                                 text('Headline', 'How Inova keeps care **connected.**', 'h1', BLACK, 36)], l=M, t=66, w=696, gap=6)
      + stack('Case header', [text('Label', 'Case study', 'label', RED, 11), text('Customer', 'Inova', 'h2', BLACK, 22),
                              text('Meta', 'Health system · first-generation Sonim deployment · hospital red phone replacement', 'small', BLACK, 10.5)],
              l=M, t=140, w=696, gap=4)
      + box('Case columns', l=M, t=216, w=696, cls='row', style={'gap': '20px'}, inner=''.join(
            f'<div class="stack" data-name="{t}" style="flex:1;gap:8px">{icon(CASE_ICONS[t], 56, t)}{text("Subheading", t, "h3", RED, 14)}{body(d)}</div>' for t, d in CASE)
            + f'<div class="stack" data-name="Results" style="flex:1;gap:8px">{icon(CASE_ICONS["Results"], 56, "Results")}{text("Subheading", "Results", "h3", RED, 14)}{bullets(RESULTS, size=12.5)}</div>')
      + fill('Rule', GRAY, l=M, t=520, w=696, h=1)
      + stack('Continuity block', [h2('Protecting continuity of care'),
                                   body('This deployment exists for the moments when communication matters most. Because the red phones keep working when other systems stop, providers can still:')],
              l=M, t=540, w=696, gap=8)
      + tiles(CARE, 616, size=64, pad=18)
      + box('Statement band', l=M, t=812, w=696, h=150, cls='group', inner=fill('Band fill', RED, l=0, t=0, w=696, h=150)
            + text('Band label', 'Emergency preparedness', 'label abs', WHITE, 11, {'left': '26px', 'top': '26px'})
            + text('Statement', 'A redundant path that works when telephony and IP systems **don’t.**', 'quote abs', WHITE, 23, {'left': '26px', 'top': '50px', 'width': '400px', '--em': BLACK})
            + text('Detail', 'Fixed-location devices give command centers and departments a communication point that does not share a single point of failure with the hospital’s primary systems.',
                   'small abs', WHITE, 10.5, {'left': '470px', 'bottom': '26px', 'width': '200px', 'font-weight': '700'}))
      + foot('Case study details from Inova deployment brief; confirm before publishing.'))
page('hc-spotlight', 'Customer spotlight', 'Interior · case study, continuity icons, red statement band', p3)

# ---------------------------------------------------------------- 4 · the solution stack + close
STACK = [('01', 'custom-side-button', 'Sonim XP5plus', 'A rugged, loud, simple handset, deployed in a no-knob configuration for fixed use. It runs independently of the hospital’s internal network, so it keeps working when VoIP and IP-based systems are offline.'),
         ('02', 'battery-general', 'Red AdvanceTec base station', 'A red docking base station from accessory partner AdvanceTec keeps each phone in place, powered and instantly recognizable as the red phone. No other accessories were required.'),
         ('03', 'sonim-ware', 'SonimWare Kiosk Mode', 'Locks each device to its job, so the red phone stays a red phone and device control stays simple for IT.'),
         ('04', 'user-friendly', 'Rollout and readiness', 'Devices are pre-assigned to departments, docked in visible spots and checked regularly to make sure they stay powered, docked and ready.')]
p4 = (head(4)
      + page_notch(X, 66)
      + stack('Headline block', [text('Label', 'The solution', 'label', RED, 11),
                                 text('Headline', 'The red phone, **rebuilt.**', 'h1', BLACK, 36)], l=M, t=66, w=696, gap=6)
      + text('Lead', 'Three components and a simple rollout. Familiar on the outside, independent underneath.', 'lead abs', BLACK, 17, {'left': f'{M}px', 'top': '134px', 'width': '650px'})
      + box('Solution grid', l=M, t=198, w=696, h=386, cls='grid2', style={'gap': '12px'}, inner=''.join(
            f'<div class="stack" data-name="{t}" style="background:{GRAY};padding:18px 20px;gap:8px">'
            f'<div class="row" data-name="Header" style="justify-content:space-between;align-items:flex-start">{icon(k, 64, t)}{text("Number", n, "h2", RED, 22)}</div>'
            f'{text("Title", t, "h3", BLACK, 15)}{body(d, size=11.5)}</div>' for n, k, t, d in STACK))
      + text('Compliance', '**Supports compliance with** CMS Emergency Preparedness requirements¹, Joint Commission Emergency Management standards and national best practices for resilient communication.',
             'small abs', BLACK, 10.5, {'left': f'{M}px', 'top': '608px', 'width': '660px', 'font-weight': '700'})
      + box('Closing band', l=0, t=656, w=W, h=400, cls='group', inner=fill('Band fill', RED, l=0, t=0, w=W, h=400)
            + text('Label', 'The real story', 'label abs', WHITE, 11, {'left': f'{M}px', 'top': '36px'})
            + text('Heading', 'Not a phone problem.\n**A continuity problem.**', 'h1 abs', WHITE, 32, {'left': f'{M}px', 'top': '56px', 'width': '420px', '--em': BLACK})
            + text('Body', 'Resilience in healthcare isn’t the absence of disruption. It’s the ability to keep operating through it. By putting Sonim XP5plus devices in red AdvanceTec base stations, Inova modernized a critical communication function without changing how its staff work.',
                   'body abs', WHITE, 12.5, {'left': f'{M}px', 'top': '150px', 'width': '400px'})
            + stack('Ensures', [text('Ensures label', 'Teams stay connected. Operations stay coordinated. Patients keep getting safe, timely care.', 'h3', WHITE, 13.5)],
                    l=500, t=150, w=256)
            + text('Closing line', 'Communication endures. **Care continues.**', 'h2 abs', WHITE, 24, {'left': f'{M}px', 'top': '256px', 'width': '696px', '--em': BLACK})
            + text('CTA', 'Talk to Sonim · sonimtech.com', 'h3 abs', WHITE, 12, {'left': f'{M}px', 'top': '294px'})
            + logo(78, WHITE, l=M, b=28, lockup=True)
            + text('Footnote', '1 CMS Emergency Preparedness Rule, 42 CFR §482.15(c): communication plan, including primary and alternate means of communication.',
                   'small abs', WHITE, 8, {'right': f'{M}px', 'bottom': '30px', 'width': '380px', 'text-align': 'right'})))
page('hc-solution', 'Solution and close', 'Closing page · solution stack and red closing band', p4)
