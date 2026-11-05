# -*- coding: utf-8 -*-
"""글자판 점수에 안 걸려 눈 검토를 안 한 맵 텍스처 전부를 시트로(2026-11-05, 읽기만).
  → work/scene_tex/전수/s_NN.png + ids.tsv(번호→id·첫 출처). 글자 없는 단색 판(표준편차 작음)만 뺌.
  python tools/tex_rest_sheets.py
"""
import os, glob
import numpy as np
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, 'work', 'scene_tex'); O = os.path.join(D, '전수'); os.makedirs(O, exist_ok=True)
for p in glob.glob(os.path.join(O, 's_*.png')): os.remove(p)
tl = {l.split('\t')[1] for l in open(os.path.join(D, 'textlike.tsv'), encoding='utf-8').read().splitlines()}
done = {os.path.basename(p)[:-4] for p in glob.glob(os.path.join(D, 'new', '*.png'))}
idx = {}
for l in open(os.path.join(D, 'index.tsv'), encoding='utf-8').read().splitlines()[1:]:
    c = l.split('\t'); idx[c[0]] = c
def scene(k):
    return idx[k][6].split(' ')[0].split('@')[0].split('/', 1)[1]
rest, flat = [], 0
for k in idx:
    if k in tl or k in done: continue
    a = np.array(Image.open(os.path.join(D, 'png', k + '.png')).convert('L')).astype(float)
    if a.std() < 6: flat += 1; continue
    rest.append(k)
rest.sort(key=lambda k: (scene(k), k))
f = ImageFont.truetype('C:/Windows/Fonts/malgun.ttf', 11)
C, R = 12, 10
rows = ['no\tid\tsource']
for p in range(0, len(rest), C * R):
    sh = Image.new('RGB', (C * 120, R * 132), (32, 32, 38)); d = ImageDraw.Draw(sh)
    for i, k in enumerate(rest[p:p + C * R]):
        im = Image.open(os.path.join(D, 'png', k + '.png')).convert('RGBA'); w, h = im.size
        s = min(116 / w, 116 / h); im = im.resize((max(1, int(w * s)), max(1, int(h * s))), Image.NEAREST if s >= 1 else Image.LANCZOS)
        bg = Image.new('RGBA', im.size, (128, 128, 128, 255)); bg.alpha_composite(im)
        x, y = (i % C) * 120, (i // C) * 132
        d.text((x + 2, y), '%d %s' % (p + i, k[:8]), font=f, fill=(255, 220, 90))
        sh.paste(bg.convert('RGB'), (x + 2, y + 15))
        rows.append('%d\t%s\t%s' % (p + i, k, scene(k)))
    sh.save(os.path.join(O, 's_%02d.png' % (p // (C * R))))
open(os.path.join(O, 'ids.tsv'), 'w', encoding='utf-8', newline='\n').write('\n'.join(rows) + '\n')
print('전체', len(idx), '이미 본 점수 후보', len(tl), '그린 것', len(done), '단색 제외', flat, '이번 대상', len(rest), '시트', (len(rest) + C * R - 1) // (C * R))
