# -*- coding: utf-8 -*-
"""텍스처 좌표 재기용 보기(작업용) — id 여러 개를 칸마다 확대 + 텍스처 화소 눈금(1/8 간격) 표시.
  python tools/tex_grid.py <출력.png> id1 id2 …"""
import os, sys
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
PNG = os.path.join(ROOT, 'work', 'scene_tex', 'png')

def main():
    out, ids = sys.argv[1], sys.argv[2:]
    N = 8
    if ids and ids[0].startswith("-n"): N = int(ids[0][2:]); ids = ids[1:]
    S = 560 if len(ids) > 1 else 1100; C = 3 if len(ids) > 2 else len(ids)
    R = (len(ids) + C - 1) // C
    sh = Image.new('RGB', (C * (S + 40), R * (S + 40)), (30, 30, 36)); d = ImageDraw.Draw(sh)
    f = ImageFont.truetype('C:/Windows/Fonts/malgun.ttf', 13)
    for j, k in enumerate(ids):
        im = Image.open(os.path.join(PNG, k + '.png')).convert('RGBA'); w, h = im.size
        sc = S / max(w, h); im2 = im.resize((int(w * sc), int(h * sc)), Image.NEAREST)
        bg = Image.new('RGBA', im2.size, (255, 0, 255, 255)); bg.alpha_composite(im2)
        x0, y0 = (j % C) * (S + 40) + 34, (j // C) * (S + 40) + 18
        sh.paste(bg.convert('RGB'), (x0, y0))
        for t in range(N + 1):
            gx = x0 + int(w * t / N * sc); gy = y0 + int(h * t / N * sc)
            d.line([(gx, y0), (gx, y0 + int(h * sc))], fill=(0, 255, 255), width=1)
            d.line([(x0, gy), (x0 + int(w * sc), gy)], fill=(0, 255, 255), width=1)
            d.text((gx - 6, y0 - 16), str(w * t // N), font=f, fill=(255, 255, 0))
            d.text((x0 - 32, gy - 7), str(h * t // N), font=f, fill=(255, 255, 0))
        d.text((x0 + 4, y0 + int(h * sc) + 2), '%s %dx%d' % (k, w, h), font=f, fill=(255, 200, 120))
    sh.save(out)

if __name__ == '__main__':
    main()
