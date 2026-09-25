# Sonim brand system — build targets. Requires Python 3.10+, Node 18+, Playwright (Chromium)
# and the Arial font installed (the brand-approved fallback for Akzidenz Grotesk).

.PHONY: all library whitepaper editor docx icons qa

all: icons library whitepaper editor

icons:            ## regenerate brand/icons/*.svg + icons.json
	python3 brand/icons/make_icons.py

library:          ## library/dist/Sonim_Brand_Template_Library.html
	python3 library/src/build.py

whitepaper:       ## PDFs for the white paper, blank template and design system
	node whitepaper/scripts/render.js whitepaper/src/Sonim_EMS_Whitepaper.html whitepaper/dist/Sonim_EMS_Whitepaper_Connected_Care_in_Motion.pdf
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
