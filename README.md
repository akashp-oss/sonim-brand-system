# Sonim brand system

Brand template library and white paper system for **Sonim Technologies** (a NEXA company), built in
plain HTML so every template can be edited in the browser and imported into Figma.

**Start with [`CONTEXT.md`](CONTEXT.md)**: the project background, brand rules, file map, build
steps, sourced facts and open items.

## Open the deliverables

| What | File |
|---|---|
| Brand template library: 55 templates across 10 sets | [`library/dist/Sonim_Brand_Template_Library.html`](library/dist/Sonim_Brand_Template_Library.html) |
| EMS white paper (PDF) | [`whitepaper/dist/Sonim_EMS_Whitepaper_Connected_Care_in_Motion.pdf`](whitepaper/dist/) |
| White paper editor (Figma-style, in the browser) | [`whitepaper/dist/Sonim_EMS_Whitepaper_EDITOR.html`](whitepaper/dist/) |
| White paper design system, blank template, Word content | [`whitepaper/dist/`](whitepaper/dist/) |

Download an HTML file and open it in Chrome or Edge. The files are self-contained, with images embedded.

## Copy templates into Figma

Hover any template in the library for three buttons:

| Button | What you get in Figma |
|---|---|
| **Copy SVG** | Press Ctrl/⌘ + V on the canvas. You get editable text, vector logo, notches and icons, and cropped photos, with named layers. No plugin needed. |
| **Copy for Figma** | Native frames **with auto layout** on every stack. Paste with the bundled plugin: [`figma-plugin/`](figma-plugin/README.md) (import `manifest.json` once via Plugins → Development). |
| ↓ | Downloads the SVG file. |

The whole library can still go through an HTML to Figma plugin such as html.to.design: click **Figma import view** (or add `?figma` to the URL), then run the plugin on that tab.

## Hosting on Netlify

`netlify.toml` publishes only a `public/` folder that holds the library (as `index.html`), the white paper editor and the white paper PDF.
Don't publish the repo root. It has no `index.html`, which is why Netlify returns "Page not found", and it would also make the confidential PDFs in `reference/` public.
If you configured the site by hand, clear the publish directory and build command in the Netlify UI so `netlify.toml` takes effect.

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
reference/    client brief, brandbook, social media guideline
figma-plugin/ "Sonim template paste": pastes Copy for Figma output with auto layout
docs/         supporting notes
```

The repo includes the client brand guideline PDFs, so keep it private. Licensed fonts and stock licences are kept outside it; see `CONTEXT.md` §4 and §8.
