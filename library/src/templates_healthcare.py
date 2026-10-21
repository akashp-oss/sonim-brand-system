
# Healthcare white paper, APPROVED COPY (client file Inova_Whitepaper.docx, approved 2026-10-14).
# Every sentence is the approved text, verbatim. Only allowed edits: headings set in sentence case (brand rule)
# and each "Topic: Headline" heading split into a red label + headline. Do not rewrite; do not add copy.
#
# Layout (client request 2026-10-14): a small design system and auto layout throughout.
# - Type scale below; nothing smaller than 12 px; text under 16 px is never bold.
# - Spacing tokens below; every gap and padding uses them.
# - Every page is one flex column (header, content, footer) built from nested flex stacks and rows,
#   so the HTML to Figma import turns each group into auto layout. Only decoration (notches) is absolute.
# - 6 US Letter pages so the approved copy fits at these sizes.
F = []
DOC = 'Healthcare resilience'

from wpkit import *
CFG.update(doc=DOC, name='Healthcare white paper')
_page = page
def page(*a, **k): return _page(F, *a, **k)

# ---------------------------------------------------------------- 1 · title + introduction
page('hc-opening', 'Opening page', 'US Letter · title, introduction and callout', [
    headline('White paper · Healthcare', 'Enhancing healthcare resilience through **advanced communication infrastructure.**', 'title'),
    row('Introduction', [
        flex1('Introduction text', [col('Section heading', [T('Label', 'Introduction', 'label', RED), T('Heading', 'When communication fails, care is at risk', 'h2')], gap='sm'),
                                    body('In healthcare environments, communication is foundational to patient care—particularly during emergencies and system downtime.'),
                                    body('As hospitals modernize and shift toward digital and VoIP-based systems, many have unintentionally introduced new points of failure.'),
                                    body('Cyber incidents, power outages, and system maintenance events regularly disrupt hospital operations placing communication systems at risk when they’re needed most.')]),
        rugged_box('Callout container', 272, 300, [T('Callout heading', 'When communication fails:', 'h3'),
                                                   bullets(['Care teams become disconnected', 'Critical information is delayed or lost', 'Response times increase', 'Patient safety is placed at risk'])])],
        gap='xxl'),
    rule(),
    lead('To address this risk, the organization sought a resilient, simple replacement for the traditional hospital “red phone”—a device long relied upon for always-available communication during critical events.'),
], 1, bleed=bleed_photo('healthcare', 228, '50% 30%'), gap='xl')
F[-1] = (F[-1][0], F[-1][1].replace('Sonim, a NEXA company · sonimtech.com', 'Photo: sonimtech.com', 1))

# ---------------------------------------------------------------- 2 · a shift in strategy
SOLUTION = [('custom-side-button', 'Sonim XP5plus devices (no knobs)', None),
            ('battery-general', 'Red docking Base Station from AdvanceTec', None),
            ('sonim-ware', 'SonimWare enabled with Kiosk Mode', None)]
page('hc-strategy', 'Strategy page', 'Interior · headline, two columns and solution tiles', [
    col('Opening', [headline('A shift in strategy', 'Replacing the traditional **“red phone.”**'),
                    lead('Rather than continuing to invest in aging analog infrastructure, the organization made a deliberate shift toward a modern, resilient replacement for the hospital’s traditional red phone.')], gap='lg'),
    row('Two columns', [
        flex1('Column 1', [body('At the center of this deployment is the Sonim XP5plus—from Sonim, a NEXA company—selected as a purpose-built solution to preserve always-available communication during downtime and emergency events.'),
                           body('This deployment represents the organization’s first-generation use of Sonim devices, focused on solving a clearly defined operational problem rather than introducing unnecessary complexity.')]),
        flex1('Column 2', [body('The goal was straightforward: replace the legacy red phone with an affordable, fixed-location device that delivers reliable communication without relying on internal networks or VoIP infrastructure.'),
                           body('By maintaining a familiar form factor while modernizing the underlying technology, the organization ensured staff adoption without changing established workflows.')])]),
    rule(),
    col('Solution', [T('Section heading', 'The solution consists of:', 'h3'), tiles(SOLUTION, 64)], gap='lg'),
], 2)

# ---------------------------------------------------------------- 3 · the system in practice + real-world application
page('hc-system', 'System page', 'Interior · three columns, red band and a section', [
    headline('The system in practice', 'Simple, fixed, and **always available.**'),
    row('Three columns', [
        flex1('Column 1', [body('The Sonim XP5plus operates independently of the hospital’s internal network, ensuring communication remains available when VoIP and IP-based systems are offline.')]),
        flex1('Column 2', [body('Docked in highly visible red AdvanceTec Base Station, the devices are immediately recognizable and accessible, preserving the visual and functional expectations of the traditional red phone.')]),
        flex1('Column 3', [body('No additional accessories were required beyond the red cradle, reinforcing a clean, purpose-built deployment.')])]),
    band('System band', [T('Band label', 'Together, this creates a system that is:', 'label', WHITE),
                         row('Qualities', [T('Quality', q, 'h2', WHITE, flex='1 1 0') for q in ['Always available', 'Immediately deployable', 'Simple to use under stress']])]),
    rule(),
    section('Real-world application', 'From disruption to continuity', [
        lead('During outages or downtime events, staff simply use the docked Sonim devices to communicate without relying on internal systems.'),
        body('The combination of an affordable device and fixed red cradle delivers reliable communication without the cost or complexity of maintaining analog lines.')]),
], 3)

# ---------------------------------------------------------------- 4 · continuity of care + emergency preparedness
PROVIDERS = [('patient-data', 'Escalate patient concerns without delay', None), ('multiple-users', 'Coordinate treatment plans in real time', None),
             ('command', 'Maintain operational awareness during disruptions', None)]
page('hc-continuity', 'Continuity page', 'Interior · icon tiles, two columns and a red statement band', [
    col('Opening', [headline('Protecting what matters most', 'Continuity **of care.**'),
                    lead('At its core, this deployment protects continuity of care during moments when communications are most critical.')], gap='lg'),
    col('Providers', [T('Lead-in', 'Providers are able to:', 'h3'), tiles(PROVIDERS, 56),
                      body('By preserving reliable communication, the organization reduces risk linked to delayed or failed coordination.')], gap='lg'),
    rule(),
    section(None, 'Strengthening emergency preparedness', [
        row('Two columns', [
            flex1('Column 1', [body('Beyond day-to-day operations, this communication model strengthens the organization’s ability to respond to emergencies.'),
                               body('While the deployment is primarily focused on replacing the hospital red phone, the fixed-location Sonim devices support emergency workflows by maintaining reliable communication points during incidents.')]),
            flex1('Column 2', [body('Command centers maintain continuous connectivity with hospitals and departments, enabling real-time situational awareness and coordinated decision-making.')])])]),
    band('Statement band', [row('Statement row', [
        T('Statement', 'Most importantly, the solution provides a redundant communication option that operates **independently of traditional telephony and IP-based systems.**', 'quote', WHITE, flex='3 1 0', **{'--em': BLACK}),
        T('Detail', 'This eliminates the risk of a single point of failure and ensures that communication remains intact even when primary systems are compromised.', 'body', WHITE, flex='2 1 0')],
        gap='xxl', align_items='flex-end')]),
], 4, gap='xl')

# ---------------------------------------------------------------- 5 · implementation + measurable impact
STEPS = [('multiple-users', None, 'Devices are pre-assigned to departments, eliminating uncertainty during incidents. Docking stations are placed in visible, accessible locations, reinforcing their role as dependable operational tools rather than emergency afterthoughts.'),
         ('user-friendly', None, 'Because the devices mirror the traditional red phone experience, minimal training is required. Familiarity is preserved by design.'),
         ('battery-general', None, 'Basic readiness checks ensure devices remain powered, docked, and available when needed.')]
IMPACT = [('tower', 'Operationally, organizations experience:', ['Reliable communication during telephony or system outages', 'Reduced reliance on aging analog phone infrastructure', 'Simplified device control using SonimWare Kiosk Mode']),
          ('patient-data', 'Clinically, the benefits are clear:', ['Maintained continuity of care', 'Improved response to critical patient events', 'Reduced delays linked to communication failures']),
          ('rps-general', 'From a regulatory perspective, the system supports compliance with:', ['CMS Emergency Preparedness requirements', 'Joint Commission Emergency Management standards', 'National best practices for resilient communication'])]
page('hc-impact', 'Impact page', 'Interior · implementation tiles and impact columns', [
    col('Opening', [headline('White paper · Healthcare', 'From implementation **to integration.**'),
                    lead('The success of this initiative is rooted not only in the technology, but in how it is implemented.')], gap='lg'),
    tiles(STEPS, 40, weights=[1.7, 1.15, 1], pad='lg'),
    rule(),
    section('Demonstrating value', 'Measurable impact', [
        body('The impact of this deployment is both immediate and measurable.'),
        row('Impact columns', [flex1(t[:30], [icon(k, 40, t[:30]), T('Subheading', t, 'h3', RED), bullets(i)], gap='md') for k, t, i in IMPACT], gap='xl'),
        lead('More broadly, it strengthens the organization’s position as a high-reliability system, capable of operating effectively under any condition.')], gap='lg'),
], 5, gap='xl')

# ---------------------------------------------------------------- 6 · conclusion
ENSURE = [('multiple-users', 'Teams remain connected', None), ('command', 'Operations remain coordinated', None), ('patient-data', 'Patients continue to receive safe, timely care', None)]
top_band = col('Conclusion band', [
    header(6, WHITE),
    headline('Conclusion', 'Redefining communication as a **strategic asset.**', 'title', WHITE, WHITE, WHITE, em=BLACK),
    col('Body', [lead('In healthcare, resilience is not defined by the absence of disruption, but by the ability to continue operating despite it.', color=WHITE),
                 lead('By replacing the legacy red phone with Sonim XP5plus devices in red AdvanceTec Base Station, the organization modernized a critical communication function without changing how staff work.', color=WHITE)],
        gap='md', max_width='640px')],
    gap='xl', background=RED, padding=f'28px {M}px {S["xxxl"]}px', flex='none', position='relative')
page('hc-conclusion', 'Conclusion', 'Closing page · red conclusion band and icon tiles', [
    col('Ensure', [T('Lead-in', 'By investing in a redundant, resilient communication ecosystem, healthcare organizations ensure that:', 'h3'), tiles(ENSURE, 56)], gap='lg'),
    col('Closing', [lead('Even in the face of system failure, the mission does not stop.'),
                    T('Closing line', 'Communication endures. **Care continues.**', 'h1')], gap='sm'),
], 6, bleed=top_band, show_header=False)
