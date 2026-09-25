# Sonim brand system

Brand template library and white paper system for **Sonim Technologies** (a NEXA company), built in
plain HTML so every template can be edited in the browser and imported into Figma.

**Start with [`CONTEXT.md`](CONTEXT.md)**: the project background, brand rules, file map, build
steps, sourced facts and open items.

## Open the deliverables

| What | File |
|---|---|
| Brand template library: 38 templates across 9 sets | [`library/dist/Sonim_Brand_Template_Library.html`](library/dist/Sonim_Brand_Template_Library.html) |
| EMS white paper (PDF) | [`whitepaper/dist/Sonim_EMS_Whitepaper_Connected_Care_in_Motion.pdf`](whitepaper/dist/) |
| White paper editor (Figma-style, in the browser) | [`whitepaper/dist/Sonim_EMS_Whitepaper_EDITOR.html`](whitepaper/dist/) |
| White paper design system, blank template, Word content | [`whitepaper/dist/`](whitepaper/dist/) |

Download an HTML file and open it in Chrome or Edge. The files are self-contained, with images embedded.

## Import into Figma

1. Open `Sonim_Brand_Template_Library.html` and click **Figma import view** (or add `?figma` to the URL).
2. Run your HTML to Figma plugin (for example html.to.design) on that tab.
3. Each artboard imports as a frame, with text, photos, logo, notches and panels as separate named layers.

## Build

Requires Python 3.10+, Node 18+, Playwright with Chromium (`npm i && npx playwright install chromium`),
and the Arial font installed.

```bash
make library      # library/dist/Sonim_Brand_Template_Library.html
make whitepaper   # white paper, blank template and design-system PDFs
make editor       # self-contained white paper editor
make docx         # content-only Word file
make qa           # screenshots and checks into .qa/
```

## Structure

```
brand/        logo + brand-styled icons (shared)
library/      template library: src/ (generator, templates, images) → dist/
whitepaper/   white paper: src/ (HTML, CSS, images), scripts/ (render, editor, docx) → dist/
reference/    original client brief
docs/         supporting notes
```

Brand guideline PDFs, licensed fonts and stock licences are kept outside this repo; see `CONTEXT.md` §4 and §8.
