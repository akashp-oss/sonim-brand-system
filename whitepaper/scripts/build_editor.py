"""Build the self-contained, Figma-style editor for the EMS white paper.

Inlines the stylesheet and every image of src/Sonim_EMS_Whitepaper.html as data URIs
and appends scripts/editor2.js, so the output opens and saves from any folder.
Usage: python3 whitepaper/scripts/build_editor.py
"""
import base64, re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / 'src'
DIST = HERE.parent / 'dist'
MIME = {'jpg': 'image/jpeg', 'jpeg': 'image/jpeg', 'png': 'image/png', 'webp': 'image/webp'}

html = (SRC / 'Sonim_EMS_Whitepaper.html').read_text()
css = (SRC / 'assets/sonim-whitepaper.css').read_text()
# embed the brand font files referenced by the stylesheet so the editor stays self-contained
import base64, re as _re
css = _re.sub(r'url\("\.\./\.\./\.\./(library/src/fonts/[^"]+\.otf)"\)',
              lambda m: 'url(data:font/otf;base64,' + base64.b64encode((SRC.parents[1] / m.group(1)).read_bytes()).decode() + ')', css)
html = html.replace('<link rel="stylesheet" href="assets/sonim-whitepaper.css">', '<style id="wp-base">\n' + css + '\n</style>')

def embed(m):
    p = SRC / m.group(1)
    return 'src="data:%s;base64,%s"' % (MIME[p.suffix[1:].lower()], base64.b64encode(p.read_bytes()).decode())

html = re.sub(r'src="(assets/img/[^"]+)"', embed, html)
assert 'assets/' not in html, 'a relative asset reference is still in the page'
html = html.replace('</body>', '<script>\n' + (HERE / 'editor2.js').read_text() + '\n</script>\n</body>')
out = DIST / 'Sonim_EMS_Whitepaper_EDITOR.html'
out.write_text(html)
print(out, round(len(html) / 1e6, 2), 'MB')
