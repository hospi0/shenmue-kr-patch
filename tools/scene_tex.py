# -*- coding: utf-8 -*-
"""맵·모델 텍스처 전수 추출(읽기 전용, 2026-11-04 하스피 «마을 집명패·거리 표지판도 뽑았어?»).
work/disc1~3 의 SCENE·MODEL 아래 모든 파일에서 PVRT 를 잘라(gzip·AFS 안까지) 같은 바이트는 하나로 묶고 PNG 로 푼다.
  → work/scene_tex/png/<sha1 앞 12>.png · work/scene_tex/index.tsv (id · 폭 · 높이 · 형식 · 사본 수 · 출처들)
  → work/scene_tex/sheets/sheet_NNN.png (훑어보기용 표: 칸마다 id)
  python tools/scene_tex.py
"""
import os, sys, gzip, struct, hashlib, glob, collections
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, r'C:\claude\utils\dreamcast\PyPVR')
from pypvr import Pypvr
OUT = os.path.join(ROOT, 'work', 'scene_tex')

def blobs(d, where, depth=0):
    """(데이터, 위치 설명) — gzip 풀고 AFS 는 항목별로"""
    if depth > 4: return
    if d[:2] == b'\x1f\x8b':
        try: d = gzip.decompress(d)
        except Exception: return
    yield d, where
    if d[:4] == b'AFS\0':
        n = struct.unpack_from('<I', d, 4)[0]
        for k in range(min(n, 100000)):
            o, s = struct.unpack_from('<II', d, 8 + 8 * k)
            if 0 < o < len(d) and 0 < s <= len(d) - o:
                sub = d[o:o + s]
                if sub[:2] == b'\x1f\x8b' or sub[:4] == b'AFS\0':
                    yield from blobs(sub, '%s#%d' % (where, k), depth + 1)

def carve(d):
    i = 0
    while True:
        i = d.find(b'PVRT', i)
        if i < 0 or i + 16 > len(d): return
        sz = struct.unpack_from('<I', d, i + 4)[0]; w, h = struct.unpack_from('<HH', d, i + 12)
        if 8 <= w <= 1024 and 8 <= h <= 1024 and 16 <= sz and i + 8 + sz <= len(d) + 64:
            st = i - 16 if i >= 16 and d[i - 16:i - 12] == b'GBIX' else i
            yield i, d[st:min(len(d), i + 8 + sz)], w, h, d[i + 8], d[i + 9]
        i += 8

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    os.makedirs(os.path.join(OUT, 'png'), exist_ok=True); os.makedirs(os.path.join(OUT, 'sheets'), exist_ok=True)
    seen = collections.OrderedDict()            # id → [w, h, px, tf, [출처]]
    files = []
    for n in (1, 2, 3):
        for top in ('SCENE', 'MODEL'):
            files += sorted(glob.glob(os.path.join(ROOT, 'work', 'disc%d' % n, top, '**', '*'), recursive=True))
    files = [f for f in files if os.path.isfile(f)]
    print('파일 %d' % len(files), flush=True)
    bad = 0
    for fi, f in enumerate(files):
        rel = os.path.relpath(f, os.path.join(ROOT, 'work')).replace('\\', '/')
        for d, where in blobs(open(f, 'rb').read(), rel):
            for off, pvr, w, h, px, tf in carve(d):
                k = hashlib.sha1(pvr).hexdigest()[:12]
                if k in seen: seen[k][4].append('%s@%X' % (where, off)); continue
                p = os.path.join(OUT, 'png', k + '.png')
                if not os.path.exists(p):
                    try:
                        im = Pypvr.Decode('-buffer -flip -silent -nolog', buff_pvr=pvr).get_image_buffer()
                        im.save(p)
                    except Exception:
                        bad += 1; continue
                seen[k] = [w, h, px, tf, ['%s@%X' % (where, off)]]
        if fi % 200 == 0: print('  %d/%d 텍스처 %d' % (fi, len(files), len(seen)), flush=True)
    with open(os.path.join(OUT, 'index.tsv'), 'w', encoding='utf-8', newline='\n') as w:
        w.write('id\tw\th\tpx\ttf\tcopies\tsources\n')
        for k, (ww, hh, px, tf, src) in seen.items():
            w.write('%s\t%d\t%d\t%d\t%d\t%d\t%s\n' % (k, ww, hh, px, tf, len(src), ' '.join(src[:6])))
    # 훑어보기 표: 칸 160×160 + 이름, 6×5
    font = ImageFont.truetype('C:/Windows/Fonts/malgun.ttf', 12)
    ids = list(seen); C, R, S = 8, 5, 200
    for pg in range(0, len(ids), C * R):
        sh = Image.new('RGB', (C * S, R * (S + 16)), (40, 40, 48)); dr = ImageDraw.Draw(sh)
        for j, k in enumerate(ids[pg:pg + C * R]):
            try: im = Image.open(os.path.join(OUT, 'png', k + '.png')).convert('RGBA')
            except Exception: continue
            im.thumbnail((S - 6, S - 6))
            bg = Image.new('RGBA', im.size, (128, 128, 128, 255)); bg.alpha_composite(im)
            x, y = (j % C) * S, (j // C) * (S + 16)
            sh.paste(bg.convert('RGB'), (x + 3, y + 3)); dr.text((x + 3, y + S), '%s %dx%d' % (k, seen[k][0], seen[k][1]), font=font, fill=(255, 220, 80))
        sh.save(os.path.join(OUT, 'sheets', 'sheet_%03d.png' % (pg // (C * R))))
    print('고유 텍스처 %d · 풀기 실패 %d · 표 %d장 → %s' % (len(seen), bad, (len(ids) + C * R - 1) // (C * R), OUT))

if __name__ == '__main__':
    main()
