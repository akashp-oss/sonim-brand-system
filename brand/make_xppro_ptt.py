# XP Pro render with a push-to-talk screen (radio replacement posts). Run from the repo root:
#   python3 brand/make_xppro_ptt.py  ->  library/src/img/xppro_ptt.png
# Source: brand/xppro_source.png (the client's XP Pro cutout); the thermal app on its screen is replaced
# by a generic PTT screen drawn in the brand font and colours.
from PIL import Image, ImageDraw, ImageFont
S = 4                                    # draw the screen at 4x, then scale down
src = Image.open('brand/xppro_source.png').convert('RGBA')
L, T, R, B = 204, 234, 416, 801          # front screen in source px
W, H = (R - L) * S, (B - T) * S
F = lambda w, s: ImageFont.truetype(f'library/src/fonts/AkzidenzGroteskPro-{w}.otf', s * S)
scr = Image.new('RGBA', (W, H), (14, 15, 16, 255)); d = ImageDraw.Draw(scr)
RED, GRAY, WHITE, MID = (207, 16, 45), (229, 236, 238), (255, 255, 255), (120, 128, 132)
d.text((10 * S, 8 * S), '9:41', font=F('Bold', 9), fill=WHITE)
d.text((W - 34 * S, 8 * S), '5G', font=F('Bold', 9), fill=WHITE)
d.text((14 * S, 34 * S), 'Talk group', font=F('Regular', 10), fill=MID)
d.text((14 * S, 48 * S), 'Fleet · North', font=F('Bold', 17), fill=WHITE)
for i, (n, on) in enumerate([('Dispatch', True), ('Bus 14', True), ('Bus 22', False), ('Bus 31', True)]):
    y = (84 + i * 28) * S
    d.ellipse((14 * S, y + 3 * S, 22 * S, y + 11 * S), fill=(RED if on else MID))
    d.text((30 * S, y), n, font=F('Regular', 12), fill=WHITE)
    d.line((14 * S, y + 21 * S, W - 14 * S, y + 21 * S), fill=(40, 42, 44), width=S)
cx, cy, r = W // 2, 330 * S, 62 * S                    # PTT button
d.ellipse((cx - r - 8 * S, cy - r - 8 * S, cx + r + 8 * S, cy + r + 8 * S), outline=(90, 20, 30), width=3 * S)
d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=RED)
d.text((cx, cy), 'PTT', font=F('Bold', 26), fill=WHITE, anchor='mm')
d.text((cx, cy + r + 26 * S), 'Hold to talk', font=F('Regular', 11), fill=MID, anchor='mm')
d.text((cx, H - 24 * S), 'GPS on  ·  Encrypted', font=F('Regular', 9), fill=MID, anchor='mm')
mask = Image.new('L', (W, H), 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, W, H), radius=12 * S, fill=255)
scr.putalpha(mask)
scr = scr.resize((R - L, B - T), Image.LANCZOS)
out = src.copy(); out.alpha_composite(scr, (L, T))
out.save('library/src/img/xppro_ptt.png')
print('library/src/img/xppro_ptt.png', out.size)
