# -*- coding: utf-8 -*-
"""맵·모델 텍스처 한글판 재포장(2026-11-05) — work/scene_tex/new/<id>.png → 원본과 같은 PVR 형식으로 인코딩 →
3장 SCENE·MODEL 안 «모든 사본»(PKF gzip 안·MT5·AFS 날 데이터)을 제자리 교체 → work/build/scene_discN/<경로>(discbuild 가 마지막에 덮음).
  · id = 원본 PVR 바이트 sha1 앞 12(tools/scene_tex.py 와 같은 잘라내기) — 사본은 바이트가 같아서 전부 잡힘
  · 인코딩 크기 ≠ 원본이면 그 텍스처는 건너뜀(보고)
  · 이미 빌드된 파일(build_text 결과)이 있으면 그 위에 덮음 → ★build_text 다음에 돌릴 것
  · 다시 압축한 gzip 파일 목록 → work/build/scene_tex_touched_discN.txt (discbuild 가 여유 섹터를 둠)
  python tools/scene_pack.py
"""
import os, sys, gzip, glob, hashlib, struct
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import gfx_pack as G, pak

D = os.path.join(ROOT, 'work', 'scene_tex')

def carve(d):
    i = 0
    while True:
        i = d.find(b'PVRT', i)
        if i < 0 or i + 16 > len(d): return
        sz = struct.unpack_from('<I', d, i + 4)[0]; w, h = struct.unpack_from('<HH', d, i + 12)
        if 8 <= w <= 1024 and 8 <= h <= 1024 and 16 <= sz and i + 8 + sz <= len(d) + 64:
            st = i - 16 if i >= 16 and d[i - 16:i - 12] == b'GBIX' else i
            yield st, min(len(d), i + 8 + sz)
        i += 8

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    ids = {os.path.basename(p)[:-4] for p in glob.glob(os.path.join(D, 'new', '*.png'))}
    cache, bad = {}, set()
    tot = 0
    for n in (1, 2, 3):
        src = os.path.join(ROOT, 'work', 'disc%d' % n); bt = os.path.join(ROOT, 'work', 'build', 'disc%d' % n)
        dst = os.path.join(ROOT, 'work', 'build', 'scene_disc%d' % n)          # 따로 두는 출력(다시 돌려도 원본·build_text 결과에서 새로)
        import shutil
        if os.path.isdir(dst): shutil.rmtree(dst)
        touched = []
        files = [f for top in ('SCENE', 'MODEL') for f in glob.glob(os.path.join(src, top, '**', '*'), recursive=True) if os.path.isfile(f)]
        for f in files:
            rel = os.path.relpath(f, src)
            built = os.path.join(dst, rel); bsrc = os.path.join(bt, rel)
            raw = open(bsrc if os.path.exists(bsrc) else f, 'rb').read()
            gz = raw[:2] == b'\x1f\x8b'
            try: d = bytearray(gzip.decompress(raw) if gz else raw)
            except Exception: continue
            hit = 0
            for a, b in list(carve(bytes(d))):
                k = hashlib.sha1(bytes(d[a:b])).hexdigest()[:12]
                if k not in ids or k in bad: continue
                if k not in cache:
                    pvr = bytes(d[a:b]); px, df, w, h = G.pvr_info(pvr)
                    try:
                        e = G.encode(os.path.join(D, 'new', k + '.png'), px, df, G.gbix_of(pvr))
                    except Exception as ex:
                        print('! 인코딩 실패', k, ex); bad.add(k); continue
                    if len(e) != b - a:
                        print('! 크기 다름', k, len(e), b - a); bad.add(k); continue
                    cache[k] = e
                d[a:b] = cache[k]; hit += 1
            if not hit: continue
            out = pak.regzip(raw, bytes(d)) if gz else bytes(d)
            os.makedirs(os.path.dirname(built), exist_ok=True); open(built, 'wb').write(out)
            if gz: touched.append('/' + rel.replace(os.sep, '/').upper())
            tot += hit
            print('장%d %-40s 텍스처 %d · %d → %d B' % (n, rel, hit, len(raw), len(out)), flush=True)
        open(os.path.join(ROOT, 'work', 'build', 'scene_tex_touched_disc%d.txt' % n), 'w', encoding='utf-8').write('\n'.join(touched) + '\n')
    print('교체 %d곳 · 인코딩 %d장 · 실패 %d %s' % (tot, len(cache), len(bad), sorted(bad)))
    miss = ids - set(cache) - bad
    if miss: print('디스크에서 못 찾은 id', sorted(miss))

if __name__ == '__main__':
    main()
