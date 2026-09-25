SONIM WHITE PAPER SYSTEM  v1.0
==============================

Open in a browser (Chrome/Edge):
  design-system.html       Design system spec (10 pages, landscape)
  whitepaper-template.html Blank masters T1-T5 (US Letter)
  Sonim_EMS_Whitepaper.html  Filled EMS white paper (4 pages), built from the template

Icons and the logo are already inlined; to rebuild the PDF:
  node render.js Sonim_EMS_Whitepaper.html out.pdf

To save as PDF from the browser (template and design system): Print > Save as PDF, paper Letter, margins None,
"Background graphics" ON.

Files
  assets/sonim-whitepaper.css  Tokens (colors, type scale, grid, notch) + components
  assets/sonim-logo.svg        Single-color logo (inherits text color)
  assets/img/                  Photography used in the EMS paper
  assets/thumbs/               Page previews used in the design system
  assets/icons/                Brand-styled line icons (Tabler Icons, MIT license): black line, one red detail
  assets/img/S*.jpg            Stock photos from Pexels (free license, no attribution required)
  render.js                    Optional: node render.js <file.html> <out.pdf>
                               (needs Node + Playwright)

Fonts
  Built for Akzidenz Grotesk (Bold/Regular). If it isn't installed, the files fall
  back to Arial, the brand's approved system font.

New white paper
  1. Copy whitepaper-template.html and rename it.
  2. Replace the placeholder text and gray image slots, page by page.
  3. Keep one notch headline per page, sentence case, one red key phrase.
  4. Export to PDF and check each page for overflow.
