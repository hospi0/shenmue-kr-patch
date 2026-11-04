# -*- coding: utf-8 -*-
"""MISC/RESUME.DAT 다시 쓰기 — 중단·저장 화면(글자판 RESUME00/02 조립용 표 + 문장).

구조(원본 실측): 표0 @0x000(최대 71항목) · 표1 @0x1B0(최대 62항목) · 표2 @0x32A(1항목 IC) · 문장 @0x336~ (NUL 구분 21개)
항목 6 B = 글자 코드 2 B(EUC 바이트를 뒤집어 저장) + x·y·폭·높이 각 1 B, 0×6 으로 끝.
규칙: 표 시작 위치·표2·문장 개수는 그대로, 표 안 «특수 칸»(。、「Cn」？S0~S2 / DISC·숫자·파일 번호 등)은 원본 그대로 두고 한글 낱자 칸을 더함.
  → work/build/gfx_common/MISC/RESUME.DAT   (gfx_resume.py 의 *_table.json 필요)
"""
import os, sys, json, struct
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import gfx_resume as R

SRC = os.path.join(ROOT, 'work', 'disc1', 'MISC', 'RESUME.DAT')
OUT = os.path.join(ROOT, 'work', 'build', 'gfx_common', 'MISC', 'RESUME.DAT')
T0, T1, T2, MSG0 = 0x000, 0x1B0, 0x32A, 0x336
CAP = {T0: 71, T1: 62}
SPACE = (0, 0, 8, 22)        # 전각 공백 = 빈 8px (글자판 맨 아래 빈 줄을 가리킴 — 아래 확인)

def entries(d, p):
    out = []
    while d[p:p+6] != bytes(6):
        out.append((d[p:p+2], d[p+2], d[p+3], d[p+4], d[p+5])); p += 6
    return out

def is_text(code):
    try: c = bytes((code[1], code[0])).decode('euc_jp'); return '぀' <= c <= '鿿'
    except UnicodeDecodeError: return False

def code_of(ch):
    b = ch.encode('euc_kr') if '가' <= ch <= '힣' else ch.encode('euc_jp')
    assert len(b) == 2, ch
    return bytes((b[1], b[0]))

KO = {0: R.MSG0[0], 1: R.MSG0[1], 2: R.MSG0[2], 3: R.MSG0[3], 4: R.MSG0[4], 5: R.MSG0[5],
      8: R.MSG0[0], 9: R.MSG0[1], 10: R.MSG0[2], 11: R.MSG0[4], 12: R.MSG0[5],
      14: R.MSG1[0], 15: R.MSG1[1], 16: R.MSG1[2], 17: R.MSG1[0], 18: R.MSG1[1], 19: R.MSG1[2], 20: R.MSG1[3]}

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    d = bytearray(open(SRC, 'rb').read())
    out = bytearray(d[:MSG0])
    for tp, atlas in ((T0, 'RESUME00__00_re_fix1'), (T1, 'RESUME02__00_re_fix2')):
        old = entries(d, tp)
        keep = [e for e in old if not is_text(e[0])]
        tab = json.load(open(os.path.join(R.G.NEW, atlas + '_table.json'), encoding='utf-8'))
        sp = R.SPEC[atlas]; ax0, ay0, ax1, ay1 = sp['area']
        # 전각 공백: 글자판 낱자 구역 안 빈 곳(낱자가 안 쓴 마지막 줄)
        used_bottom = max(v[1] + v[3] for v in tab.values())
        space = (ax0, used_bottom, 8, 22) if used_bottom + 22 <= ay1 else (ax1 - 8, ay1 - 22, 8, 22)
        new = keep + [(code_of(c), *v) for c, v in tab.items() if c not in ('「', '」', '□')] + [(code_of('　'), *space)]
        if len(new) > CAP[tp]: raise SystemExit('표 @%X 항목 %d > %d' % (tp, len(new), CAP[tp]))
        blob = b''.join(c + bytes(v) for c, *v in new)
        room = (T1 if tp == T0 else T2) - tp
        out[tp:tp + room] = (blob + bytes(room))[:room]
        print('표 @%03X: 특수 %d + 한글 %d + 공백 1 = %d / %d' % (tp, len(keep), len(new) - len(keep) - 1, len(new), CAP[tp]))
    msgs = d[MSG0:].split(b'\0')
    tail_pad = len(d) - MSG0 - len(b'\0'.join(msgs))
    newm = []
    for i, m in enumerate(msgs):
        if i in KO:
            t = R.norm(KO[i]); b = bytearray()
            k = 0
            while k < len(t):
                if t.startswith('Cn', k): b += b'Cn'; k += 2; continue
                c = t[k]; b += c.encode('euc_kr') if '가' <= c <= '힣' else c.encode('euc_jp'); k += 1
            # ★게임 코드가 문장 위치를 «원본 바이트 오프셋»으로 박아 두고 폭을 잰다(폭 함수 0x1402E6 ← 0x140260 등, 상수 0x336+0x187·0x1D7…)
            #  → 문장마다 원래 시작 위치·길이를 지킨다. 남는 바이트는 전각 공백(8px)을 앞뒤 반씩(가운데 정렬 유지) — 2026-11-04 실기 정렬 어긋남
            if len(b) > len(m): raise SystemExit('문장 %d 번역 %d B > 원문 %d B (%s)' % (i, len(b), len(m), KO[i]))
            pad = len(m) - len(b)
            if pad % 2: raise SystemExit('문장 %d 홀수 여백 %d' % (i, pad))
            sp = '　'.encode('euc_jp'); lead = pad // 4; trail = pad // 2 - lead
            newm.append(sp * lead + bytes(b) + sp * trail)
        else: newm.append(m)
    assert [len(x) for x in newm] == [len(x) for x in msgs], '문장 길이·위치가 원본과 다름'
    out += b'\0'.join(newm)
    assert len(out) == len(d), (len(out), len(d))
    os.makedirs(os.path.dirname(OUT), exist_ok=True); open(OUT, 'wb').write(out)
    print('RESUME.DAT %d → %d B, 문장 %d개(그중 한글 %d)' % (len(d), len(out), len(newm), len(KO)))
    # 검산: 모든 한글 문장 글자가 해당 표에 있는가
    for i, t in KO.items():
        tp = T0 if i <= 13 else T1
        codes = {bytes(e[0]) for e in entries(out, tp)}
        miss = [c for c in R.norm(t).replace('Cn', '') if code_of(c) not in codes]
        if miss: raise SystemExit('문장 %d 표에 없는 글자 %s' % (i, miss))
    print('검산: 문장 글자 전부 표에 있음')

if __name__ == '__main__':
    main()
