# Sonim brand system — build targets. Requires Python 3.10+, Node 18+, Playwright (Chromium).
# Akzidenz-Grotesk Pro is embedded from library/src/fonts/ (no system fonts needed).

.PHONY: all assets library whitepaper editor docx icons qa check

all: assets library whitepaper editor check

assets:           ## official client assets (Icons/, Logo/) -> brand/icons/all.json + brand/logo/sonim-nexa-lockup.svg
	python3 brand/import_client_assets.py

icons:            ## regenerate the Tabler-based brand/icons/*.svg + icons.json, then the merged set
	python3 brand/icons/make_icons.py
	python3 brand/import_client_assets.py

library:          ## library/dist/Sonim_Brand_Template_Library.html
	python3 library/src/build.py

whitepaper: library ## PDFs for the white paper, blank template and design system
	# EMS white paper PDF (published as whitepaper.pdf) = the library's ems-* pages, printed
	node library/src/export_pdf.js whitepaper/dist/Sonim_EMS_Whitepaper_Connected_Care_in_Motion.pdf ems-opening,ems-shift,ems-compare,ems-proof,ems-solution,ems-solution-2
	node whitepaper/scripts/render.js whitepaper/src/whitepaper-template.html whitepaper/dist/Sonim_Whitepaper_Template_Blank.pdf
	node whitepaper/scripts/render.js whitepaper/src/design-system.html whitepaper/dist/Sonim_Whitepaper_Design_System.pdf "" .sheet
	rm -f whitepaper/src/*.built.html

editor:           ## whitepaper/dist/Sonim_EMS_Whitepaper_EDITOR.html
	python3 whitepaper/scripts/build_editor.py

docx:             ## clean content-only Word version of the white paper
	node whitepaper/scripts/build_docx.js

qa:               ## screenshots + checks into .qa/
	node library/src/shots.js && node library/src/qa.js
	node whitepaper/scripts/test_editor.js && node whitepaper/scripts/test_auto.js && node whitepaper/scripts/test_save.js

check:            ## layout audit: fails on text < 12 px, bold < 16 px, clipped/covered/overlapping text, crowded footers, margins
	node library/src/audit.js
	node whitepaper/scripts/audit.js
