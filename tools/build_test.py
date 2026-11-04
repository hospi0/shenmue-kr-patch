# -*- coding: utf-8 -*-
"""시험 빌드용 바꾼 파일 만들기(2026-11-03) → work/build/common/·disc1/ (discbuild.py 입력)
  · 글꼴 3종(work/font/*.FON — build_font.py 결과)
  · 1장 오프닝 A0114.AFS/IDX: 대표 줄은 시험 번역, 나머지 줄은 «시험 자막 N번»
  · 1ST_READ.BIN: 時計·コイン·はい·いいえ + 덧붙임 구역 확인용 긴 문자열(時計 자리를 길게) — build_exe.py 로
"""
import os, sys, shutil, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from afs import read_afs, build_afs
from srf import split_records, build_srf, parse_srf
from idx import build_idx
from encode import encode

B = os.path.join(ROOT, 'work', 'build')
LINES = {   # A0114.SRF 레코드 번호 → 시험 번역(＆ 줄바꿈)  값이 (문장, 반각공백, 반각영숫자) 꼴이면 그 설정으로
    2: '앗! 이네 씨…',
    # 3차 시험: 반각 공백·반각 영숫자는 자막 엔진이 못 그림(위치 따라 사라지거나 찌꺼기) → 전각만 씀
    6: '전각 영숫자 ABC 123!?＆6번 확인',
    51: '덤벼라!＆…무술가답게 죽여 주마',
    62: '무, 무슨 말이야, 아버지…',
    63: '아버지!',
    66: '아버지?…아버지!…아버지!',
}

def opening():
    src = os.path.join(ROOT, 'work', 'disc1', 'SCENE', '01', 'STREAM', 'A0114')
    d, es = read_afs(src + '.AFS'); files = []; newoff = {}
    for si, (nm, o, s) in enumerate(es):
        b = d[o:o+s]
        if nm.upper().endswith('.SRF'):
            recs, _ = split_records(b); old = [r['off'] for r in parse_srf(b)[0]]
            nr = []
            for k, (c1, t, c3) in enumerate(recs):
                if t is None: nr.append((c1, t, c3)); continue
                v = LINES.get(k, '시험 자막 %d번＆한글 표시 확인' % k)
                nr.append((c1, encode(*v) if isinstance(v, tuple) else encode(v), c3))
            b, offs = build_srf(nr)
            for a, c in zip(old, offs): newoff[(si, a)] = c
        files.append((nm, b))
    dst = os.path.join(B, 'disc1', 'SCENE', '01', 'STREAM'); os.makedirs(dst, exist_ok=True)
    open(os.path.join(dst, 'A0114.AFS'), 'wb').write(build_afs(d, files))
    open(os.path.join(dst, 'A0114.IDX'), 'wb').write(build_idx(open(src + '.IDX', 'rb').read(), newoff))

def exe():
    tsv = os.path.join(ROOT, 'work', 'test', 'exe_test.tsv')
    # 덧붙임 구역 시험은 «화면에 바로 그리는» 헬프 문장으로(아이템 이름은 고정 버퍼 — 길면 멈춤)
    rows = {'261324': '시계',
            '25DA88': '【메모장】A이 도움말은 파일 끝 뒤에00덧붙인 자리에서 읽습니다.0000페이지 넘기기0돌아가기0첫 페이지00최신 페이지0',
            '262E28': '코인', '26D734': '예', '26D744': '아니요'}
    open(tsv, 'w', encoding='utf-8', newline='\n').write('key\tko\n' + ''.join('exe:%s\t%s\n' % kv for kv in rows.items()))
    subprocess.run([sys.executable, os.path.join(HERE, 'build_exe.py'), tsv], check=True)
    subprocess.run([sys.executable, os.path.join(HERE, 'verify_exe.py'), tsv], check=True)
    shutil.copyfile(os.path.join(B, '1ST_READ.BIN'), os.path.join(B, 'common', '1ST_READ.BIN'))

def overlay(base, built, orig):
    """묶음 안 글꼴(base) 에서 «우리가 바꾼 칸»(원본 MISC 글꼴과 built 가 다른 칸)만 built 로 덮는다 — 묶음 판의 다른 칸은 보존."""
    b = bytearray(base)
    for i in range(len(orig) // 45):
        s = slice(i * 45, i * 45 + 45)
        if built[s] != orig[s]: b[s] = built[s]
    return bytes(b)

def fonts():
    import pak
    dst = os.path.join(B, 'common', 'MISC'); os.makedirs(dst, exist_ok=True)
    built = {}; orig = {}
    for f in ('DC_KANJI', 'RYOU', 'WAZA'):
        shutil.copyfile(os.path.join(ROOT, 'work', 'font', f + '.FON'), os.path.join(dst, f + '.FON'))
        built[f] = open(os.path.join(ROOT, 'work', 'font', f + '.FON'), 'rb').read()
        orig[f] = open(os.path.join(ROOT, 'work', 'disc1', 'MISC', f + '.FON'), 'rb').read()
    # ★게임이 실제로 쓰는 글꼴 = COLD.BIN·COLDINIT.PKS(gzip) 안 IPAC 항목
    for fn in ('COLD.BIN', 'COLDINIT.PKS'):
        raw, d = pak.load(os.path.join(ROOT, 'work', 'disc1', 'MISC', fn))
        ents = pak.entries(d)
        repl = {n: overlay(d[ents[n][0]:ents[n][0] + ents[n][1]], built[n], orig[n]) for n in ('DC_KANJI', 'RYOU') if n in ents}
        nd = pak.replace_same_size(d, repl)
        out = pak.regzip(raw, nd) if raw[:2] == pak.GZ else nd
        open(os.path.join(dst, fn), 'wb').write(out)
        print(fn, len(raw), '→', len(out), '항목', list(repl))

if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    for d in ('common', 'disc1'):
        p = os.path.join(B, d)
        if os.path.isdir(p): shutil.rmtree(p)
    os.makedirs(os.path.join(B, 'common'), exist_ok=True)
    fonts(); opening(); exe()
    print('준비 끝')
