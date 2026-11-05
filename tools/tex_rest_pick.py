# -*- coding: utf-8 -*-
"""전수 눈 검토 후보 정리(2026-11-05, 읽기만) — work/scene_tex/전수/후보_번호.txt(묶음·번호·판독) + ids.tsv → 후보목록.tsv·요약.txt·후보시트/<묶음>_NN.png
  칸 라벨 = 번호·id 앞 8자·판독. 빼기는 EXCLUDE 번호에.
  python tools/tex_rest_pick.py
"""
import os, sys, glob, collections
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, 'work', 'scene_tex'); O = os.path.join(D, '전수'); SH = os.path.join(O, '후보시트'); os.makedirs(SH, exist_ok=True)
for p in glob.glob(os.path.join(SH, '*.png')): os.remove(p)
EXCLUDE = {4016, 4017, 4018, 1859, 2305, 3866, 3889, 701}   # 글자 없는 지도 3 · 읽을 수 없음 5
# 1순위 = 현판·문패·지도·족자·메뉴·간판·표지·옷·주요 소품 / 2순위 = 포스터·게임센터 / 3순위 = 나머지(상품·신문·표·잡동사니)
P1 = {2854, 2954, 2955, 4045, 1823, 3065, 4373, 254, 358, 359, 1005, 1226, 1257, 1543, 2211,
      578, 607, 1522, 1609, 1613, 1623, 1628, 1781, 3472, 4097,
      550, 565, 566, 567, 575, 596, 599, 603, 1100, 1243, 1381, 1715, 1896, 2015, 2027, 2058, 2064, 3952, 4361,
      1619, 1742, 3317, 1704, 253, 304, 615, 1308, 2179, 311, 2228, 2309, 869, 238, 809, 3275, 4288, 4298, 4261, 4289, 4246, 2220, 4142, 2389,
      2095, 2275, 2970, 3167, 3339, 3535, 555, 1391, 2490, 1898, 1947, 594, 2491}
def pri(g, n):
    return 1 if n in P1 else 2 if g in ('포스터', '게임센터') else 3
ids = {}
for l in open(os.path.join(O, 'ids.tsv'), encoding='utf-8').read().splitlines()[1:]:
    c = l.split('\t'); ids[int(c[0])] = c
idx = {l.split('\t')[0]: l.split('\t') for l in open(os.path.join(D, 'index.tsv'), encoding='utf-8').read().splitlines()[1:]}
G = collections.OrderedDict(); seen = set()
for l in open(os.path.join(O, '후보_번호.txt'), encoding='utf-8').read().splitlines():
    if not l or l.startswith('#'): continue
    g, n, t = l.split('\t'); n = int(n)
    if n in EXCLUDE: continue
    if n in seen: print('! 중복', n, t); continue
    seen.add(n); G.setdefault(g, []).append((n, t))
f = ImageFont.truetype('C:/Windows/Fonts/malgun.ttf', 12)
rows = ['순위\t묶음\t번호\tid\t폭\t높이\t사본 수\t판독']; summ = []
C, R, P = 8, 6, 170
for g, its in G.items():
    its.sort()
    summ.append('%-8s %3d장  사본 %4d곳' % (g, len(its), sum(int(idx[ids[n][1]][5]) for n, _ in its)))
    for p in range(0, len(its), C * R):
        ch = its[p:p + C * R]
        sh = Image.new('RGB', (C * (P + 8), ((len(ch) + C - 1) // C) * (P + 36)), (30, 30, 36)); d = ImageDraw.Draw(sh)
        for i, (n, t) in enumerate(ch):
            k = ids[n][1]; rows.append('\t'.join([str(pri(g, n)), g, str(n), k, idx[k][1], idx[k][2], idx[k][5], t]))
            im = Image.open(os.path.join(D, 'png', k + '.png')).convert('RGBA'); w, h = im.size; s = P / max(w, h)
            z = im.resize((int(w * s), int(h * s)), Image.NEAREST if s >= 1 else Image.LANCZOS); bg = Image.new('RGBA', z.size, (128, 128, 128, 255)); bg.alpha_composite(z)
            x, y = (i % C) * (P + 8) + 2, (i // C) * (P + 36)
            d.text((x, y), '%d %s' % (n, k[:8]), font=f, fill=(255, 220, 90)); d.text((x, y + 15), t[:15], font=f, fill=(160, 255, 160))
            sh.paste(bg.convert('RGB'), (x, y + 32))
        sh.save(os.path.join(SH, '%s_%02d.png' % (g, p // (C * R))))
summ.append('합계 %d장' % len(seen))
for q in (1, 2, 3):
    its = [(g, n) for g, v in G.items() for n, _ in v if pri(g, n) == q]
    summ.append('%d순위 %3d장  사본 %4d곳' % (q, len(its), sum(int(idx[ids[n][1]][5]) for _, n in its)))
print('P1 인데 후보에 없음', sorted(P1 - seen))
open(os.path.join(O, '후보목록.tsv'), 'w', encoding='utf-8', newline='\n').write('\n'.join(rows) + '\n')
open(os.path.join(O, '요약.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(summ) + '\n')
sys.stdout.reconfigure(encoding='utf-8'); print('\n'.join(summ)); print(sorted(os.path.basename(p) for p in glob.glob(os.path.join(SH, '*.png'))))
