# -*- coding: utf-8 -*-
"""텍스처 일부를 확대 + 눈금(텍스처 좌표)으로 — 이름표 위치·각도 재기용.  python tools/tex_crop.py 출력.png id x0 y0 x1 y1 [배율] [new]"""
import os, sys
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out, k, x0, y0, x1, y1 = sys.argv[1], sys.argv[2], *map(int, sys.argv[3:7])
sc = int(sys.argv[7]) if len(sys.argv) > 7 else 6
sub = 'new' if len(sys.argv) > 8 else 'png'
im = Image.open(os.path.join(ROOT, 'work', 'scene_tex', sub, k + '.png')).convert('RGBA').crop((x0, y0, x1, y1))
bg = Image.new('RGBA', im.size, (255, 0, 255, 255)); bg.alpha_composite(im)
big = bg.convert('RGB').resize((im.width * sc, im.height * sc), Image.NEAREST)
o = Image.new('RGB', (big.width + 40, big.height + 24), (30, 30, 36)); o.paste(big, (36, 20)); d = ImageDraw.Draw(o)
f = ImageFont.truetype('C:/Windows/Fonts/malgun.ttf', 11)
for x in range(x0 - x0 % 4, x1 + 1, 4):
    if x < x0: continue
    X = 36 + (x - x0) * sc; d.line([(X, 20), (X, 20 + big.height)], fill=(0, 200, 200) if x % 16 else (255, 255, 0), width=1)
    if x % 16 == 0: d.text((X - 8, 4), str(x), font=f, fill=(255, 255, 0))
for y in range(y0 - y0 % 4, y1 + 1, 4):
    if y < y0: continue
    Y = 20 + (y - y0) * sc; d.line([(36, Y), (36 + big.width, Y)], fill=(0, 200, 200) if y % 16 else (255, 255, 0), width=1)
    if y % 16 == 0: d.text((2, Y - 7), str(y), font=f, fill=(255, 255, 0))
o.save(out)
