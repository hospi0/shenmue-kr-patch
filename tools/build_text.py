# -*- coding: utf-8 -*-
"""번역 TSV → 빌드 재료(work/build/common·discN) — 대사(SRF·IDX·AFS 세 장) + NPC 표(HUMANS PKS) + 실행 파일 + 글꼴.

  python tools/build_text.py [TSV 글롭 …]      (기본: "my files/tsv/*.tsv")
  TSV 열: key · speaker · count · jp · ko  (extract.py 가 만든 sm1_NNN.tsv — 원문 «문장» 단위)
  → work/text/lines.tsv 로 «넣을 자리» 전부에 퍼뜨린다(같은 원문 = 같은 번역).

규칙(쓰는 순간 강제)
  · 자막(SRF): 한 줄 19칸(전각 고정폭, 공백도 1칸), 최대 2줄. 번역에 ＆ 가 있고 각 줄 ≤19 면 그대로,
    아니면 ＆ 를 공백으로 풀어 낱말 단위로 다시 접음. 3줄 이상이면 work/build/text_report.tsv 에 «넘침»으로 적고 그대로 넣음(확인용).
  · 반각 공백·영숫자·기호 → 전각(자막 엔진은 2바이트만), 「……」→「…」, 부호 뒤 공백 삭제 (encode.py)
  · PKS: «화자「본문」» 꼴 유지, 줄바꿈 ＆ → 0x0A
  · 실행 파일·메모장 사전: build_exe.py 규칙(토큰·아이템 9자·헬프 줄 20자) 그대로
번역이 비어 있으면 원문 그대로.
"""
import os, sys, glob, re, shutil, subprocess, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from afs import read_afs, build_afs
from srf import split_records, build_srf, parse_srf
from idx import build_idx
from encode import encode, normalize
import pks, build_test

W = lambda *p: os.path.join(ROOT, 'work', *p)
B = W('build')
WIDTH, MAXLINES = 19, 2

def load_tr(paths):
    tr = {}
    for p in paths:
        for i, ln in enumerate(open(p, encoding='utf-8')):
            c = ln.rstrip('\n').split('\t')
            if i == 0 and c[0] == 'key': continue
            if len(c) < 5 or not c[4].strip(): continue
            grp = 'exe' if c[0].startswith(('exe:', 'dict:')) else 'talk'
            tr[(grp, c[3])] = c[4]
    return tr

def prepare_font(texts):
    """번역에 쓰인 «완성형 밖 음절»·«한글 칸(16~40구)에 덮인 한자»를 41구 이후 빈 칸에 넣어 글꼴을 다시 만든다.
    빈 칸 = 원문·번역 어디에도 안 쓰이는 글자 칸."""
    mine = set(''.join(texts)); used = set(mine)
    for l in open(W('text', 'lines.tsv'), encoding='utf-8'):
        c = l.split('\t')
        if len(c) >= 4: used |= set(c[3])
    av = W('font', 'avoid_chars.txt'); open(av, 'w', encoding='utf-8').write(''.join(sorted(used)))
    ex = W('font', 'extra_chars.txt'); open(ex, 'w', encoding='utf-8').write(''.join(sorted(mine)))
    subprocess.run([sys.executable, os.path.join(HERE, 'build_font.py'), '--extra', ''.join(sorted(mine)), '--avoid', av], check=True)
    import encode as _e; _e._EX = None

def wrap(ko):
    ko = normalize(ko)
    parts = ko.split('＆')
    if all(len(p) <= WIDTH for p in parts) and len(parts) <= MAXLINES: return parts
    if len(parts) > MAXLINES and all(len(p) <= WIDTH for p in parts):
        alt = wrap_words(parts)
        return alt if len(alt) <= MAXLINES else parts          # 다시 접어도 3줄이면 하스피가 나눈 대로(보고)
    return wrap_words(parts)

def wrap_words(parts):
    words = ' '.join(p.strip() for p in parts).split(' ')
    lines = ['']
    for w in words:
        cand = (lines[-1] + ' ' + w) if lines[-1] else w
        if len(cand) <= WIDTH: lines[-1] = cand
        elif not lines[-1]: lines[-1] = w            # 한 낱말이 19칸 넘음 — 그대로(보고)
        else: lines.append(w)
    return lines

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    paths = [q for p in (sys.argv[1:] or [os.path.join(ROOT, 'my files', 'tsv', '*.tsv')]) for q in glob.glob(p)]
    tr = load_tr(paths)
    print('번역 TSV %d개 · 번역된 원문 %d' % (len(paths), len(tr)))
    rows = [l.rstrip('\n').split('\t') for l in open(W('text', 'lines.tsv'), encoding='utf-8')][1:]
    srf_tr = collections.defaultdict(dict)    # disc → {(afs, srf, rec): 줄 목록}
    pks_tr = {}; exe_rows = []; report = []
    for kind, key, spk, jp, where in rows:
        grp = 'exe' if kind in ('exe', 'dict') else 'talk'
        ko = tr.get((grp, jp))
        if not ko: continue
        if kind in ('cut', 'free'):
            lines = wrap(ko)
            if len(lines) > MAXLINES or any(len(x) > WIDTH for x in lines):
                report.append('넘침\t%s\t%d줄\t%s' % (key, len(lines), '＆'.join(lines)))
            for w in where.split(','):
                if w == 'pks': pks_tr[key] = ('body', lines); continue
                if w == 'scnf': continue                     # PKS 밖 SCNF(COLD.BIN·MAPINFO) — 아래 scnf_text 가 원문으로 찾아 씀
                n, rest = w.split(':', 1); a, sr = rest.split('/'); s, k = sr.split('#')
                srf_tr[int(n)][(a, s, int(k))] = lines
        elif kind == 'pks':
            pks_tr[key] = ('full', normalize(ko).split('＆'))
        elif kind == 'exe':
            exe_rows.append('%s\t%s\n' % (key, ko))
        elif kind == 'dict':
            exe_rows.append('exe:%s\t%s\n' % (where, ko))
    for d in ('common', 'disc1', 'disc2', 'disc3'):
        if os.path.isdir(os.path.join(B, d)): shutil.rmtree(os.path.join(B, d))
    os.makedirs(os.path.join(B, 'common'), exist_ok=True)
    prepare_font(tr.values())
    build_test.fonts()
    # 1b) PKS 밖 SCNF 대사표(COLD.BIN·COLDINIT.PKS·하즈키 집 MAPINFO) — 원문 본문으로 번역 찾아 제자리에
    import scnf_text, pak
    def scnf_tr(idk, jt):
        spk, body = (jt.split('「', 1) if '「' in jt else ('', jt))
        if spk and body.endswith('」'): body = body[:-1]
        key = body.replace('\n', '＆')
        ko = tr.get(('talk', key)) or tr.get(('talk', key.rstrip('　 '))) or tr.get(('talk', jt.replace('\n', '＆')))
        if not ko: return None
        txt = '\n'.join(wrap(ko))
        if spk: txt = {'ドアの声': '목소리', '涼': '료'}.get(spk, spk) + '「' + txt + '」'   # COLD.BIN SCNF 크기 고정 — 화자도 한글로(8 B 넘침 2026-11-04)
        return b'\n'.join(encode(x) for x in txt.split('\n'))
    nsc = 0; miss = []
    for fn in ('COLD.BIN', 'COLDINIT.PKS'):
        fp = os.path.join(B, 'common', 'MISC', fn)
        raw, dd = pak.load(fp)
        nd, k, seen = scnf_text.patch(dd, scnf_tr); nsc += k
        miss += [(fn, i, t) for i, t in seen if scnf_tr(i, t) is None]
        open(fp, 'wb').write(pak.regzip(raw, nd) if raw[:2] == pak.GZ else nd)
    for n in (1, 2, 3):
        src = W('disc%d' % n, 'SCENE', '0%d' % n, 'JHD0', 'MAPINFO.BIN')
        nd, k, seen = scnf_text.patch(open(src, 'rb').read(), scnf_tr); nsc += k
        miss += [('MAPINFO%d' % n, i, t) for i, t in seen if scnf_tr(i, t) is None]
        dst = os.path.join(B, 'disc%d' % n, 'SCENE', '0%d' % n, 'JHD0', 'MAPINFO.BIN'); os.makedirs(os.path.dirname(dst), exist_ok=True)
        open(dst, 'wb').write(nd)
    print('PKS 밖 SCNF 대사 %d줄 번역 · 번역 없음 %d' % (nsc, len(miss)))
    for x in miss[:20]: print('  번역 없음 %s %s %s' % (x[0], x[1], x[2].replace('\n', '＆')))
    # 1) SRF 세 장
    nsrf = 0
    for n in (1, 2, 3):
        for f in sorted(glob.glob(W('disc%d' % n, 'SCENE', '*', 'STREAM', '*.AFS'))):
            an = os.path.basename(f)[:-4]
            if an == 'HUMANS': continue
            mine = {k: v for k, v in srf_tr[n].items() if k[0] == an}
            if not mine: continue
            d, es = read_afs(f); files = []; newoff = {}
            for si, (nm, o, s) in enumerate(es):
                b = d[o:o+s]
                if nm.upper().endswith('.SRF'):
                    recs, _ = split_records(b); old = [r['off'] for r in parse_srf(b)[0]]
                    nr = []
                    for k, (c1, t, c3) in enumerate(recs):
                        L = mine.get((an, nm[:-4], k))
                        if t is not None and L: t = encode('＆'.join(L)); nsrf += 1
                        nr.append((c1, t, c3))
                    b, offs = build_srf(nr)
                    for a_, c_ in zip(old, offs): newoff[(si, a_)] = c_
                files.append((nm, b))
            rel = os.path.relpath(f, W('disc%d' % n))
            dst = os.path.join(B, 'disc%d' % n, rel); os.makedirs(os.path.dirname(dst), exist_ok=True)
            open(dst, 'wb').write(build_afs(d, files))
            open(dst[:-4] + '.IDX', 'wb').write(build_idx(open(f[:-4] + '.IDX', 'rb').read(), newoff))
    # 2) HUMANS.AFS PKS (세 장 같은 파일 — 장마다 SCENE/0N 경로)
    npks = 0
    if pks_tr:
        src = W('disc1', 'SCENE', '01', 'STREAM', 'HUMANS.AFS'); d, es = read_afs(src); files = []
        for nm, o, s in es:
            b = d[o:o+s]
            if nm.endswith('.PKS'):
                newt = {}
                for idk, t in pks.strings(b):
                    if idk not in pks_tr: continue
                    mode, lines = pks_tr[idk]
                    if mode == 'body':
                        jt = t.decode('euc_jp'); spk = jt.split('「', 1)[0] if '「' in jt else ''
                        body = '\n'.join(lines)
                        txt = spk + '「' + body + '」' if spk else body
                    else:
                        txt = '\n'.join(lines)
                    newt[idk] = b'\n'.join(encode(x) for x in txt.split('\n')); npks += 1
                if newt: b = pks.rebuild(b, newt)
            files.append((nm, b))
        out = build_afs(d, files)
        for n in (1, 2, 3):
            dst = os.path.join(B, 'disc%d' % n, 'SCENE', '0%d' % n, 'STREAM', 'HUMANS.AFS')
            os.makedirs(os.path.dirname(dst), exist_ok=True); open(dst, 'wb').write(out)
    # 3) 실행 파일
    tsv = W('build', 'exe_from_text.tsv')
    open(tsv, 'w', encoding='utf-8', newline='\n').write('key\tko\n' + ''.join(exe_rows))
    if exe_rows:
        import memo_reflow                                   # 메모장 줄 24 B 스택 버퍼 — 넘는 칸은 4줄 안에서 다시 나눔(넘치면 빌드 중단)
        if memo_reflow.main(paths): raise SystemExit('메모장 칸 4줄 넘침 — work/check/memo_overflow.tsv')
        subprocess.run([sys.executable, os.path.join(HERE, 'build_exe.py'), tsv], check=True)
        subprocess.run([sys.executable, os.path.join(HERE, 'verify_exe.py'), tsv], check=True)
        shutil.copyfile(os.path.join(B, '1ST_READ.BIN'), os.path.join(B, 'common', '1ST_READ.BIN'))
    with open(W('build', 'text_report.tsv'), 'w', encoding='utf-8', newline='\n') as w:
        w.write('kind\tkey\tinfo\ttext\n' + ''.join(r + '\n' for r in report))
    print('SRF 줄 %d · PKS %d · 실행 파일 %d · 넘침 보고 %d (work/build/text_report.tsv)' % (nsrf, npks, len(exe_rows), len(report)))

if __name__ == '__main__':
    main()
