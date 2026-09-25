# Sonim template paste (Figma plugin)

Pastes a template from the brand template library into Figma as native layers **with auto layout**
on every stack (headline blocks, rugged-container content, feature rows, grids).

## Install (once)
1. Figma desktop app → **Plugins → Development → Import plugin from manifest…**
2. Pick `figma-plugin/manifest.json` from this repo.

## Use
1. Open `Sonim_Brand_Template_Library.html`, hover a template, click **Copy for Figma**.
2. In Figma: **Plugins → Development → Sonim template paste**, click the box, press Ctrl/⌘ + V.
3. The artboard lands in the middle of the viewport as a frame with named layers.

Text is set in Akzidenz-Grotesk Pro if you have it, otherwise Arial, otherwise Inter.

**No plugin?** Use **Copy SVG** instead and paste straight onto the canvas with Ctrl/⌘ + V. You get
editable vectors, text and images, but no auto layout.
