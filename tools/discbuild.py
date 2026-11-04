# -*- coding: utf-8 -*-
r"""쉔무 1장 디스크 빌드(2026-11-03) — GD-ROM 3장, 데이터 = Track 3(LBA 45000~, IP.BIN·PVD·디렉터리만, 나머지 0)
   + Track 6(LBA 160046~549150, 파일 전부 빈틈없이, 끝 150섹터 0).

배치 규칙 — ★번역 길이와 무관하게 «원본만으로» 정해진다(빌드마다 같은 LBA; 옛 시험본 스테이트로 이어 해도 안전):
  · 커질 수 있는 파일마다 여유 섹터 RES(파일) 를 원본에서 계산:
      STREAM/*.AFS = SRF 본문 바이트 + PKS 대사 바이트(=두 배까지) + 레코드당 32 B → 섹터 + 2
      번역 그림 .GZ = 원본의 25 % + 1섹터 / MISC/RESUME.DAT = 2섹터 / 1ST_READ.BIN = 마지막 파일이라 뒤 150섹터까지
  · EVICT(HANGON.BIN, 행온 미니게임 롬 5.2 MB) 을 Track 3 빈 구간 고정 자리(LBA 46000~)로 뺀다.
  · Track 6 은 «여유가 있는 첫 파일»부터 끝까지 원래 순서대로 다시 깔며 각 파일 자리 = 원래 섹터 + RES.
  · 실제 새 파일이 자리(원래+RES)를 넘으면 빌드 실패(«여유 초과»).
  · 디렉터리 기록(양 엔디안 LBA·크기) 갱신, 쓴 섹터는 헤더 MSF·모드1·EDC/ECC 새로, 끝에 모든 파일 되읽기 검산.

  python tools/discbuild.py --disc N                 → 배치 계획만(쓰기 없음)
  python tools/discbuild.py --disc N --write         → dist/build/discN/ 에 트랙 사본을 만들어 쓴다 (★하스피 허락 후)
  바꾼 파일 = work/build/discN/<디스크 경로>  (예 work/build/disc1/SCENE/01/STREAM/A0114.AFS) + 세 장 공통 work/build/common/
"""
import os, sys, struct, shutil, argparse, hashlib, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import iso_extract as ie
from gdi import Disc, disc_dir, SEC, USER
from afs import read_afs
from srf import parse_srf
import pks

_sp = importlib.util.spec_from_file_location('cdmode1', r'C:\claude\project\anearth-kr-patch\tools\cdmode1.py')
cdmode1 = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(cdmode1)
SYNC = b'\x00' + b'\xff' * 10 + b'\x00'
def bcd(n): return (n // 10) << 4 | n % 10
def sector(lba, data):
    f = lba + 150
    s = bytearray(SYNC + bytes([bcd(f // 4500), bcd(f // 75 % 60), bcd(f % 75), 1]) + data.ljust(USER, b'\0') + bytes(SEC - 16 - USER))
    return bytes(cdmode1.fix(s))

sec = lambda n: (n + USER - 1) // USER
T3_FREE0 = 46000                     # Track 3: 45000~45144 가 IP.BIN·PVD·디렉터리, 그 뒤 0
EVICT = ['/HANGON/HANGON.BIN']
GFX_GZ = ('/SPRITE/LD', '/SPRITE/LOADNUM', '/SPRITE/TITLE4_', '/SPRITE/OPTION.GZ')

def entries(n):
    ie.D = Disc(n)
    return {full: (lba, size) for full, lba, size, fl in ie.walk() if not fl & 2}

def reserve(n, ents):
    res = {}
    base = os.path.join(ROOT, 'work', 'disc%d' % n)
    for full, (lba, size) in ents.items():
        if '/STREAM/' in full and full.endswith('.AFS'):
            d, es = read_afs(base + full); t = 0
            for nm, o, s in es:
                if nm.upper().endswith('.SRF'): t += sum(r['text_cap'] + 32 for r in parse_srf(d[o:o+s])[0])
                if nm.upper().endswith('.PKS'): t += sum(len(x[1]) for x in pks.strings(d[o:o+s]))
            if t: res[full] = sec(t) + 2
        elif full.startswith(GFX_GZ) and full.endswith('.GZ'):
            res[full] = sec(size // 4) + 1
        elif full == '/MISC/RESUME.DAT':
            res[full] = 2
    # 맵 텍스처(scene_pack)로 다시 압축한 gzip 은 원본보다 커지지 않음(2026-11-05 실측) — 여유 없이, 커지면 «여유 초과»로 실패
    return res

def plan(n):
    ents = entries(n); res = reserve(n, ents)
    t6 = [t for t in ie.D.tracks if t.num == 6][0]; t6_end = t6.start_lba + t6.sectors
    order = sorted(ents, key=lambda f: ents[f][0])
    first = min(ents[f][0] for f in list(res) + EVICT)
    lay = {}; cur = first
    for f in order:
        lba, size = ents[f]
        if lba < first: lay[f] = (lba, sec(size)); continue
        if f in EVICT: continue
        room = sec(size) + res.get(f, 0)
        lay[f] = (cur, room); cur += room
    last = order[-1]; assert last == '/1ST_READ.BIN', last
    # 1ST_READ 는 맨 끝 — 트랙 끝 150섹터 앞까지를 자리로
    l0, r0 = lay[last]; lay[last] = (l0, t6_end - 150 - l0)
    if lay[last][1] < sec(ents[last][1]): raise SystemExit('Track 6 넘침: 1ST_READ 자리 %d < %d' % (lay[last][1], sec(ents[last][1])))
    c3 = T3_FREE0
    for f in EVICT:
        lay[f] = (c3, sec(ents[f][1]) + 64); c3 += lay[f][1]
    t3 = [t for t in ie.D.tracks if t.num == 3][0]
    assert c3 <= t3.start_lba + t3.sectors
    return ents, res, lay, first, t6_end

def changed_files(n):
    out = {}
    for root in (os.path.join(ROOT, 'work', 'build', 'gfx_common'), os.path.join(ROOT, 'work', 'build', 'common'), os.path.join(ROOT, 'work', 'build', 'disc%d' % n),
                 os.path.join(ROOT, 'work', 'build', 'scene_disc%d' % n)):   # 그림(gfx_pack) → 공통 → 장별 → 맵 텍스처(scene_pack)
        if not os.path.isdir(root): continue
        for dp, dn, fn in os.walk(root):
            for f in fn:
                p = os.path.join(dp, f)
                out['/' + os.path.relpath(p, root).replace(os.sep, '/').upper()] = open(p, 'rb').read()
    return out

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--disc', type=int, required=True); ap.add_argument('--write', action='store_true')
    a = ap.parse_args(); sys.stdout.reconfigure(encoding='utf-8')
    n = a.disc
    ents, res, lay, first, t6_end = plan(n)
    moved = sum(1 for f in ents if lay[f][0] != ents[f][0])
    print('장 %d: 파일 %d · 여유 둔 파일 %d (%d섹터) · 다시 까는 시작 LBA %d · 위치 바뀌는 파일 %d · Track 3 로 빼는 파일 %s' %
          (n, len(ents), len(res), sum(res.values()), first, moved, EVICT))
    used = max(l + r for f, (l, r) in lay.items() if l >= 160046)
    print('  Track 6 끝 %d · 사용 끝 %d' % (t6_end, used))
    new = changed_files(n)
    for f, d in new.items():
        if f not in ents: raise SystemExit('디스크에 없는 파일 ' + f)
        if sec(len(d)) > lay[f][1]: raise SystemExit('여유 초과: %s %d섹터 > 자리 %d' % (f, sec(len(d)), lay[f][1]))
    print('  바꾼 파일 %d개 — 전부 자리 안' % len(new))
    if not a.write: return
    src = disc_dir(n); out = os.path.join(ROOT, 'dist', 'build', 'disc%d' % n); os.makedirs(out, exist_ok=True)
    for x in os.listdir(src):
        shutil.copyfile(os.path.join(src, x), os.path.join(out, x))
    D = ie.D
    tr = {t.num: t for t in D.tracks}
    fh = {k: open(os.path.join(out, os.path.basename(t.path)), 'r+b') for k, t in tr.items()}
    def put(lba, data):
        t = next(t for t in tr.values() if t.contains(lba))
        fh[t.num].seek((lba - t.start_lba + t.skip) * SEC); fh[t.num].write(sector(lba, data))
    # 1) 파일 쓰기 — 위치가 바뀌었거나 내용이 바뀐 파일, 자리의 남는 섹터는 0
    for f, (lba, room) in lay.items():
        o_lba, size = ents[f]
        data = new.get(f)
        if data is None and lba == o_lba: continue
        if data is None: data = D.read(o_lba, size)
        for k in range(room):
            put(lba + k, data[k * USER:(k + 1) * USER])
    # 2) 비워진 옛 자리(EVICT 원래 위치 중 새 배치가 덮지 않은 곳)는 0 — 다시 깔기가 덮으므로 Track 6 은 [first, t6_end-150) 전부 덮임
    # 3) 디렉터리 기록
    pvd = D.read(45016, USER); rl, rs = struct.unpack_from('<I', pvd, 158)[0], struct.unpack_from('<I', pvd, 166)[0]
    dirs = {}
    def walk(l, s, pre):
        for k in range(sec(s)):
            b = bytearray(D.read(l + k, USER)); dirs[l + k] = b; i = 0
            while i < USER and b[i]:
                L = b[i]; nm = b[i+33:i+33+b[i+32]]
                if nm not in (b'\0', b'\1'):
                    name = pre + nm.decode('latin1').split(';')[0]
                    el, es_ = struct.unpack_from('<I', b, i+2)[0], struct.unpack_from('<I', b, i+10)[0]
                    if b[i+25] & 2: walk(el, es_, name + '/')
                    else:
                        nl = lay[name][0]; ns = len(new[name]) if name in new else ents[name][1]
                        struct.pack_into('<I', b, i+2, nl); struct.pack_into('>I', b, i+6, nl)
                        struct.pack_into('<I', b, i+10, ns); struct.pack_into('>I', b, i+14, ns)
                i += L
    walk(rl, rs, '/')
    for l, b in dirs.items(): put(l, bytes(b))
    for h in fh.values(): h.close()
    # 4) 되읽기 검산
    G = Disc.__new__(Disc); G.n = n; G.tracks = []
    import gdi
    for t in tr.values():
        G.tracks.append(gdi.Track(os.path.join(out, os.path.basename(t.path)), t.num))
    ie.D = G
    got = {full: (lba, size) for full, lba, size, fl in ie.walk() if not fl & 2}
    for f in ents:
        want = new.get(f) or D.read(*ents[f])
        if got[f][0] != lay[f][0] or G.read(*got[f]) != want: raise SystemExit('되읽기 불일치 ' + f)
    print('✅ 되읽기 %d개 일치 → %s' % (len(ents), out))

if __name__ == '__main__':
    main()
