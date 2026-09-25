const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle,
  AlignmentType, LevelFormat, HeadingLevel, Footer, PageNumber } = require('docx');

const RED = 'CF102D', FONT = 'Arial', W = 9360;
// "**bold**" and "^n^" (superscript citation) markup
function runs(s, o = {}) {
  return s.split(/(\*\*[^*]+\*\*|\^[0-9]+\^)/).filter(Boolean).map(p => {
    if (p.startsWith('**')) return new TextRun({ text: p.slice(2, -2), bold: true, font: FONT, ...o });
    if (p.startsWith('^')) return new TextRun({ text: p.slice(1, -1), superScript: true, font: FONT, ...o });
    return new TextRun({ text: p, font: FONT, ...o });
  });
}
const P = (s, o = {}) => new Paragraph({ spacing: { after: 140, line: 288 }, children: runs(s), ...o });
const H1 = s => new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 360, after: 160 }, children: [new TextRun({ text: s, font: FONT })] });
const H2 = s => new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 240, after: 100 }, children: [new TextRun({ text: s, font: FONT })] });
const H3 = s => new Paragraph({ heading: HeadingLevel.HEADING_3, spacing: { before: 160, after: 60 }, children: [new TextRun({ text: s, font: FONT })] });
const B = s => new Paragraph({ numbering: { reference: 'bul', level: 0 }, spacing: { after: 60, line: 276 }, children: runs(s) });
const LEAD = s => new Paragraph({ spacing: { after: 160, line: 300 }, children: runs(s, { size: 24 }) });

const c = [];
// Title
c.push(new Paragraph({ spacing: { after: 80 }, children: [new TextRun({ text: 'White paper · Emergency medical services', font: FONT, bold: true, color: RED, size: 20 })] }));
c.push(new Paragraph({ heading: HeadingLevel.TITLE, spacing: { after: 120 }, children: [new TextRun({ text: 'Connected care in motion', font: FONT })] }));
c.push(LEAD('How EMS agencies are replacing legacy communications with mission-critical mobility.'));

// 1
c.push(H1('The EMS communication challenge'));
c.push(P('**Response times matter.** A study of 1.7 million EMS runs found a median response of about 7 minutes, and about 13 minutes in rural areas, where nearly one call in ten waited close to half an hour.^1^'));
c.push(P('Crews work across hospitals, highways, rural roads, events and disasters, often in one shift. More than 18,200 local EMS agencies answer about 28.5 million 911 dispatches a year.^2^ Every call is a chain of conversations, and **when communication fails, care is delayed.**'));
c.push(P('**Legacy land mobile radio (LMR) has limits.** Coverage ends where the towers end, and every expansion means more sites and more capital. Meanwhile, the job now runs on more than voice:'));
['Voice', 'Data', 'Video', 'GPS location', 'Patient information'].forEach(t => c.push(B(t)));
c.push(H3('Today’s EMS teams need:'));
['Instant PTT communication', 'Reliable coverage beyond radio range', 'Rugged devices built for frontline use', 'Dispatch integration', 'Secure connectivity and management'].forEach(t => c.push(B(t)));

// 2
c.push(H1('Why leading EMS agencies are moving beyond traditional radios'));
c.push(LEAD('EMS leaders are moving away from treating communications as a radio problem and toward an operational mobility platform: nationwide broadband, standards-based push-to-talk and rugged devices that carry voice and data together.'));
c.push(P('FirstNet, the public safety network built with AT&T, covers more than 3 million square miles, gives first responders priority and preemption, and serves about 31,000 agencies. More than 190 deployable assets back it up for incidents and planned events.^3^'));
c.push(P('Mission-critical push-to-talk (MCPTT) brings radio-grade group calling to broadband, and gateways such as FirstNet Fusion Link connect MCPTT talkgroups to existing LMR systems. Agencies can move at their own pace without retiring the radios they already own.^3^'));

const border = { style: BorderStyle.SINGLE, size: 4, color: 'C9D1D4' }, borders = { top: border, bottom: border, left: border, right: border };
const rows = [['Traditional LMR', 'Modern mission-critical mobility'], ['Coverage limits', 'Nationwide coverage'], ['Voice only', 'Voice + data + video'],
  ['Costly infrastructure', 'Carrier-powered'], ['Separate devices', 'Consolidated platform'], ['Limited flexibility', 'Rapid deployment']];
c.push(new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: [W / 2, W / 2], rows: rows.map((r, i) => new TableRow({
  tableHeader: i === 0,
  children: r.map(t => new TableCell({ width: { size: W / 2, type: WidthType.DXA }, borders, margins: { top: 90, bottom: 90, left: 140, right: 140 },
    shading: i === 0 ? { fill: 'E5ECEE', type: ShadingType.CLEAR, color: 'auto' } : undefined,
    children: [new Paragraph({ children: [new TextRun({ text: t, bold: i === 0, font: FONT, size: 21 })] })] })) })) }));
c.push(new Paragraph({ spacing: { after: 120 }, children: [] }));


c.push(B('**18,200+** local EMS agencies answering 911 calls^2^'));
c.push(B('**28.5 million** 911 dispatches a year in 41 reporting states^2^'));
c.push(B('**~31,000** public safety agencies on FirstNet^3^'));

c.push(H2('EMS use cases'));
[['Ambulance operations', 'Crew-to-dispatch communications from the rig or on foot.'],
 ['Interfacility transport', 'Real-time coordination between sending and receiving locations.'],
 ['Special events', 'Large crowds and mass casualty readiness.'],
 ['Disaster response', 'Deployable communications in disrupted environments.'],
 ['Air medical operations', 'Aircraft tracking and remote connectivity. See the Global Medical Response case study.']]
  .forEach(([h, t]) => c.push(B(`**${h}:** ${t}`)));

// 3
c.push(H1('Customer spotlight: how EMS organizations use Sonim today'));
c.push(H2('Global Medical Response (GMR)'));
c.push(P('7,254 ground ambulances · 404 rotor-wing and 114 fixed-wing aircraft · ~5.5 million patient encounters a year^4^', {}));
c.push(H3('Challenge')); c.push(P('Remote aircraft tracking, weak coverage and environmental extremes at air bases and landing zones.'));
c.push(H3('Solution')); c.push(P('Sonim MegaConnect HPUE with FirstNet connectivity: Power Class 1 on Band 14, up to 6x the signal strength and 2x the upload speed of a standard hotspot, with external antenna ports.^5^'));
c.push(H3('Results')); ['Faster deployment', 'Stronger connectivity', 'Improved performance in remote locations', 'Reliable operation in demanding environments'].forEach(t => c.push(B(t)));
c.push(P('GMR has also deployed 1,200 FirstNet-capable Sonim XP8 smartphones to support crisis and disaster response.^3^', { spacing: { before: 120, after: 140, line: 288 } }));

c.push(H2('Star EMS'));
c.push(P('Oakland County, Michigan · 911 and non-emergency transport · in-house 24/7 dispatch center^4^'));
c.push(H3('Challenge')); c.push(P('A costly LMR system with limited scalability. Growing the fleet meant more radio infrastructure.'));
c.push(H3('Solution')); c.push(P('Sonim XP5plus, Kodiak Dispatch and a FirstNet communications platform. Dispatchers make PTT calls, monitor talkgroups and see crew locations from a web console.'));
c.push(H3('Benefits')); ['Rugged frontline communications', 'Improved dispatch coordination', 'Centralized visibility', 'Scalable communications platform'].forEach(t => c.push(B(t)));

c.push(new Paragraph({ spacing: { before: 280, after: 80, line: 320 }, indent: { left: 567, right: 567 },
  border: { left: { style: BorderStyle.SINGLE, size: 24, color: RED, space: 12 } },
  children: [new TextRun({ text: '“With FirstNet, we maintain contact with first responders nationwide during everyday crises and large disasters.”', font: FONT, size: 26, bold: true })] }));
c.push(new Paragraph({ spacing: { after: 200 }, indent: { left: 567 }, border: { left: { style: BorderStyle.SINGLE, size: 24, color: RED, space: 12 } },
  children: runs('— Jeffrey E. Marani, National Director of Field Technologies, Global Medical Response^3^', { size: 20 }) }));

// 4
c.push(H1('The EMS communications ecosystem'));
c.push(LEAD('More than a handset: device, connectivity, accessories and management, working as one system on AT&T and FirstNet.'));
c.push(H2('01  XP5plus 5G'));
c.push(P('Fourth-generation radio-style handset for PTT-first crews. AT&T Enhanced PTT, FirstNet Rapid Response and FirstNet MCPTT.^5^'));
[['Dedicated PTT', 'Side-mounted key'], ['SOS button', 'Top-mounted key'], ['Glove-friendly', 'Large, tactile keys'],
 ['Removable battery', 'Up to 25 hr talk'], ['FirstNet Ready', 'Band 14 certified'], ['Ultra-rugged', 'IP68 · MIL-STD-810H']].forEach(([a, b]) => c.push(B(`**${a}:** ${b}`)));
c.push(H2('02  MegaConnect'));
c.push(P('The first ultra-portable 5G HPUE hotspot, with 2.5 Gbps Ethernet and four external antenna ports.^5^'));
[['Stronger connectivity', 'Up to 6x signal'], ['FirstNet MegaRange', 'HPUE Power Class 1'], ['Mobile deployment', 'Battery-powered'],
 ['Vehicle operations', 'External antennas'], ['Incident command', 'Up to 64 devices']].forEach(([a, b]) => c.push(B(`**${a}:** ${b}`)));
c.push(H2('03  Accessories partners'));
c.push(P('Speaker mics, headsets, chargers, vehicle mounts and carry solutions.'));
c.push(P('RAM Mounts · AdvanceTec · Klein · OTTO · AINA · Stone Mountain'));
c.push(H2('04  Management & services'));
[['Kodiak Dispatch', 'PTT calls, talkgroups, GPS location'], ['Sonim Cloud', 'Remote setup, updates, monitoring'],
 ['SonimWare', 'SafeGuard, Kiosk Mode, SOS app'], ['Support services', 'SonimCare / FirstCare']].forEach(([a, b]) => c.push(B(`**${a}:** ${b}`)));

// Real story
c.push(H1('The real story: no longer a radio problem'));
c.push(P('EMS organizations are treating communications as an operational mobility platform. Devices like the Sonim XP5plus, connectivity such as MegaConnect, and integrated dispatch and management tools improve situational awareness, coverage, coordination and resilience while reducing dependence on traditional radio infrastructure.'));
c.push(P('**Talk to Sonim · sonimtech.com**'));

// Sources
c.push(H2('Sources'));
['Mell HK et al., “Emergency Medical Services Response Times in Rural, Suburban, and Urban Areas,” JAMA Surgery, 2017.',
 'National Association of State EMS Officials (NASEMSO), 2020 National EMS Assessment.',
 'FirstNet.com: EMS solutions; FirstNet Fusion; “Global Medical Response Connects Disaster Teams & Paramedics.”',
 'Global Medical Response, company overview (globalmedicalresponse.com); Star EMS (starems.com).',
 'Sonim Technologies product pages: XP5plus 5G, MegaConnect, SonimWare (sonimtech.com).']
  .forEach(s => c.push(new Paragraph({ numbering: { reference: 'num', level: 0 }, spacing: { after: 60 }, children: [new TextRun({ text: s, font: FONT, size: 18 })] })));

const doc = new Document({
  creator: 'Sonim', title: 'Connected care in motion',
  styles: {
    default: { document: { run: { font: FONT, size: 21 } } },
    paragraphStyles: [
      { id: 'Title', name: 'Title', basedOn: 'Normal', next: 'Normal', run: { font: FONT, size: 56, bold: true, color: '000000' }, paragraph: { spacing: { after: 120 } } },
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: FONT, size: 34, bold: true, color: '000000' }, paragraph: { spacing: { before: 360, after: 160 }, outlineLevel: 0 } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: FONT, size: 27, bold: true, color: '000000' }, paragraph: { spacing: { before: 240, after: 100 }, outlineLevel: 1 } },
      { id: 'Heading3', name: 'Heading 3', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: FONT, size: 21, bold: true, color: RED }, paragraph: { spacing: { before: 160, after: 60 }, outlineLevel: 2 } },
    ],
  },
  numbering: { config: [
    { reference: 'bul', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 360, hanging: 240 } } } }] },
    { reference: 'num', levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 360, hanging: 300 } } } }] }] },
  sections: [{ properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: 'Connected care in motion  ·  ', font: FONT, size: 16, color: '666666' }), new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 16, color: '666666' })] })] }) },
    children: c }],
});
Packer.toBuffer(doc).then(b => fs.writeFileSync(require('path').resolve(__dirname, '../dist/Sonim_EMS_Whitepaper_Connected_Care_in_Motion_Content.docx'), b));
