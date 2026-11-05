# -*- coding: utf-8 -*-
"""스샷의 글자 구역 → 맵 텍스처 찾기(2026-11-05, 읽기만). 스샷을 잘라 8방향(회전·뒤집기)·여러 크기로 전체 텍스처와 정규화 상관 대조.
  python tools/tex_find_shot.py <스샷.png> x0 y0 x1 y1 [출력 이름]
  → 상위 후보 출력 + work/scene_tex/보충시트/find_<이름>.png (왼쪽 위 = 자른 곳, 칸마다 점수·방향·id·새것 있음 표시)
"""
import os, sys, glob
from concurrent.futures import ProcessPoolExecutor
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, 'work', 'scene_tex')
HS = (20, 24, 28, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256)
ASP = (0.75, 1.0, 1.3)

def orients(c):
    out = []
    for r in range(4):
        x = np.rot90(c, r)
        out += [(r * 90, False, x), (r * 90, True, x[:, ::-1])]
    return out

CROP = None
def work(p):
    k = os.path.basename(p)[:-4]
    im = Image.open(p).convert('RGBA'); bg = Image.new('RGBA', im.size, (128, 128, 128, 255)); bg.alpha_composite(im)
    g = np.array(bg.convert('L')); H, W = g.shape
    best = (-1, 0, False)
    for rot, fl, c in orients(CROP):
        ch, cw = c.shape
        for hh in HS:                                   # 잘라 낸 구역의 긴 변이 텍스처에서 몇 화소인가
            s = hh / max(ch, cw); th0, tw0 = ch * s, cw * s
            for a in ASP:
                th, tw = (int(th0), int(tw0 * a)) if ch >= cw else (int(th0 * a), int(tw0))
                if th < 6 or tw < 6 or th > H or tw > W: continue
                t = cv2.resize(c, (tw, th), interpolation=cv2.INTER_AREA)
                if t.std() < 5: continue
                v = cv2.minMaxLoc(cv2.matchTemplate(g, t, cv2.TM_CCOEFF_NORMED))[1]
                if v > best[0]: best = (float(v), rot, fl)
    return best + (k,)

def init(c):
    global CROP
    CROP = c

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    shot, x0, y0, x1, y1 = sys.argv[1], *map(int, sys.argv[2:6]); name = sys.argv[6] if len(sys.argv) > 6 else 'x'
    crop = np.array(Image.open(shot).convert('L'))[y0:y1, x0:x1]
    crop = cv2.normalize(crop, None, 0, 255, cv2.NORM_MINMAX)
    files = glob.glob(os.path.join(D, 'png', '*.png'))
    with ProcessPoolExecutor(initializer=init, initargs=(crop,)) as ex:
        res = sorted(ex.map(work, files, chunksize=64), reverse=True)
    f = ImageFont.truetype('C:/Windows/Fonts/malgun.ttf', 12)
    sh = Image.new('RGB', (6 * 200, 3 * 225), (28, 28, 34)); d = ImageDraw.Draw(sh)
    c = Image.fromarray(crop); c.thumbnail((196, 205)); sh.paste(c.convert('RGB'), (2, 18)); d.text((2, 2), '스샷 자른 곳', font=f, fill=(120, 255, 120))
    for i, (v, rot, fl, k) in enumerate(res[:17], 1):
        im = Image.open(os.path.join(D, 'png', k + '.png')).convert('RGBA'); w, h = im.size; s = 196 / max(w, h)
        z = im.resize((int(w * s), int(h * s)), Image.NEAREST if s >= 1 else Image.LANCZOS); bg = Image.new('RGBA', z.size, (128, 128, 128, 255)); bg.alpha_composite(z)
        x, y = (i % 6) * 200 + 2, (i // 6) * 225
        done = os.path.exists(os.path.join(D, 'new', k + '.png'))
        d.text((x, y + 2), '%.2f %s %d%s%s' % (v, k[:8], rot, 'F' if fl else '', ' 있음' if done else ''), font=f, fill=(120, 255, 120) if done else (255, 220, 90))
        sh.paste(bg.convert('RGB'), (x, y + 18))
    out = os.path.join(D, '보충시트', 'find_%s.png' % name); sh.save(out); print(out)
    for v, rot, fl, k in res[:17]:
        print('%.3f %s rot%d%s %s' % (v, k, rot, 'F' if fl else '', '있음' if os.path.exists(os.path.join(D, 'new', k + '.png')) else ''))

if __name__ == '__main__':
    main()
