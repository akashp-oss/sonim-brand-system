from gen import *
import re, base64

# White papers built from the white paper source (whitepaper/src/*.html + assets/sonim-whitepaper.css) are shown in
# the library page for page, so the library, the PDF and the editor can never differ. Each <section class="page">
# becomes one 816 x 1056 artboard; the white paper stylesheet is scoped to `.ab .wpdoc` (more specific than any
# library rule) and library-only properties are reset first. Images become library data-img keys.
WP = ROOT / 'whitepaper/src'
LOGO = open(ROOT / 'brand/logo/sonim-nexa-lockup.svg').read()
ICONS_ALL = json.load(open(ROOT / 'brand/icons/all.json'))
EXTRA_IMG = {}

def _scope_css(css):
    css = re.sub(r'@font-face\s*{[^}]*}', '', css)          # the library embeds the fonts itself
    css = re.sub(r'@page\s*{[^}]*}', '', css)
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    out, i = [], 0
    while i < len(css):
        j = css.find('{', i)
        if j < 0: break
        head = css[i:j].strip()
        if head.startswith('@media'):                          # scope the rules inside, keep the query
            depth, k = 1, j + 1
            while depth:
                depth += css[k] == '{'; depth -= css[k] == '}'; k += 1
            out.append(f'{head}{{{_scope_css(css[j + 1:k - 1])}}}'); i = k; continue
        k = css.index('}', j)
        sels = []
        for sel in head.split(','):
            sel = sel.strip()
            if sel in (':root', 'html', 'body'): sels.append('.ab .wpdoc')
            elif sel == '*': sels.append('.ab .wpdoc, .ab .wpdoc *')
            else: sels.append(f'.ab .wpdoc {sel}')
        out.append(f'{", ".join(sels)}{{{css[j + 1:k]}}}'); i = k + 1
    return '\n'.join(out)

# library classes that share a name with white paper classes: neutralise the library's properties first
_SHARED = ['display', 'h1', 'h2', 'h3', 'label', 'meta', 'stat', 'quote', 'lead', 'body', 'small', 'photo', 'em', 'icon']
RESET = (', '.join(f'.ab .wpdoc .{c}' for c in _SHARED)
         + '{font-family:inherit;font-weight:inherit;line-height:inherit;letter-spacing:inherit;object-fit:fill}'
         '.ab .wpdoc img{display:inline;max-width:100%}.ab .wpdoc svg{display:inline;overflow:hidden}')
PLACE = '.ab .wpdoc .page{margin:0;position:absolute;left:0;top:0}'   # after the white paper rules (they set a screen margin)

def pages(src_name, id_prefix, title, uses):
    html = open(WP / src_name).read().replace('{{LOGO}}', LOGO)
    html = re.sub(r'\{\{icon:([a-z-]+)\}\}', lambda m: ICONS_ALL.get(m.group(1), m.group(0)), html)
    css = open(WP / 'assets/sonim-whitepaper.css').read() + '\n'.join(re.findall(r'<style>(.*?)</style>', html, flags=re.S))
    style = f'<style>{RESET}{_scope_css(css)}{PLACE}</style>'
    def img(m):
        path = m.group(1); key = 'wp_' + re.sub(r'[^a-z0-9]+', '_', path.rsplit('/', 1)[-1].rsplit('.', 1)[0].lower())
        if key not in EXTRA_IMG:                           # downscaled for the library page (print PDF keeps the originals)
            from PIL import Image
            import io
            im = Image.open(WP / path)
            alpha = im.mode in ('RGBA', 'LA', 'P')
            im.thumbnail((500, 500) if alpha else (1400, 1400))   # cutouts are shown ~110 px tall; photos up to page width
            buf = io.BytesIO(); (im.convert('RGBA') if alpha else im.convert('RGB')).save(buf, 'PNG' if alpha else 'JPEG', **({} if alpha else {'quality': 85}))
            EXTRA_IMG[key] = f'data:image/{"png" if alpha else "jpeg"};base64,' + base64.b64encode(buf.getvalue()).decode()
        return f'data-img="{key}"'
    out = []
    for n, sec in enumerate(re.findall(r'<section class="page[^"]*">.*?</section>', html, flags=re.S)):
        sec = re.sub(r'src="(assets/img/[^"]+)"', img, sec)
        aid, name, use = uses[n]
        inner = f'{style if n == 0 else ""}<div class="wpdoc abs" data-name="Page" style="left:0;top:0;width:816px;height:1056px">{sec}</div>'
        out.append(('wp', artboard(f'{id_prefix}-{aid}', f'{title} · {name}', 816, 1056, WHITE, inner, use, 'doc')))
    return out, style

EMS, _style = pages('Sonim_EMS_Whitepaper.html', 'ems', 'EMS white paper', [
    ('opening', 'Opening page', 'US Letter · photo strip, title, challenge and needs callout'),
    ('argument', 'Argument page', 'Interior · comparison table, stats and use cases'),
    ('proof', 'Proof page', 'Interior · two case studies and a quote band'),
    ('solution', 'Solution page', 'Interior · solution stack and a red closing band')])
# the scoped stylesheet must be present wherever any EMS page renders on its own (e.g. Figma view of one set)
EMS = [(s, h.replace('<div class="wpdoc abs"', _style + '<div class="wpdoc abs"', 1) if i else h) for i, (s, h) in enumerate(EMS)]
