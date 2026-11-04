# -*- coding: utf-8 -*-
"""부하 시험(디스크 쓰기 없음): 세 장 STREAM AFS 의 모든 SRF 대사를 «원문 글자 수 ×2» 길이 한글로 바꿔
SRF·AFS·IDX 를 다시 만든 뒤, 새 IDX 가 가리키는 레코드 본문이 넣은 한글과 같은지 전수 확인."""
import sys, glob, os, random, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from afs import build_afs
from srf import split_records, build_srf, parse_srf
from idx import build_idx, parse_idx
from encode import encode

def afs_entries(b):
    n = struct.unpack_from('<I', b, 4)[0]
    return [struct.unpack_from('<II', b, 8 + i * 8) for i in range(n)]

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    random.seed(1); syl = '가나다라마바사아자차카타파하료는그남자를찾아거리로나섰다'
    ok = bad = 0; grow = 0; bads = []
    for n in (1, 2, 3):
        for f in sorted(glob.glob('../work/disc%d/SCENE/*/STREAM/*.AFS' % n)):
            if f.endswith('HUMANS.AFS'): continue
            d = open(f, 'rb').read(); ents = afs_entries(d)
            names = [None] * len(ents)
            lo, ls = struct.unpack_from('<II', d, ents[0][0] - 8)
            names = [d[lo + i*48:lo + i*48 + 32].split(b'\0')[0].decode() for i in range(len(ents))]
            files = []; newoff = {}; expect = {}
            for si, (o, s) in enumerate(ents):
                b = d[o:o + s]
                if names[si].upper().endswith('.SRF'):
                    recs, _ = split_records(b); old = [r['off'] for r in parse_srf(b)[0]]
                    nrecs = []
                    for k, (c1, t, c3) in enumerate(recs):
                        if t is None: nrecs.append((c1, t, c3)); continue
                        nt = encode(''.join(random.choice(syl) for _ in range(len(t.decode('euc_jp')) * 2)))
                        nrecs.append((c1, nt, c3)); expect[(si, k)] = nt
                    nb, offs = build_srf(nrecs)
                    for k, (a, c) in enumerate(zip(old, offs)): newoff[(si, a)] = c
                    grow += len(nb) - s; b = nb
                files.append((names[si], b))
            na = build_afs(d, files)
            ni = build_idx(open(f[:-4] + '.IDX', 'rb').read(), newoff)
            e2 = afs_entries(na); good = True; cache = {}
            for nm, fi, si, off in parse_idx(ni)[2]:
                if si == 0xFFFF: continue
                if si not in cache:
                    o, s = e2[si]; srf = na[o:o + s]
                    cache[si] = (srf, {r['off']: (k, r) for k, r in enumerate(parse_srf(srf)[0])})
                srf, recs = cache[si]
                if off not in recs: good = False; break
                k, r = recs[off]
                if (si, k) in expect:
                    tp = r['text_off']; raw = srf[tp:srf.index(b'\0', tp)]
                    if raw != expect[(si, k)]: good = False; break
            if good: ok += 1
            else: bad += 1; bads.append(f)
    print('AFS 통과 %d / 실패 %d, SRF 증가 합계 %.1f MB' % (ok, bad, grow / 1e6), bads[:3])

if __name__ == '__main__':
    main()
