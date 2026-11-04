# -*- coding: utf-8 -*-
"""처음 추출(extract.py)에서 «잡음»으로 빠졌지만 실제 쓰이는 실행 파일 문자열을 보충한다(2026-11-04 실기: 메모장 「10武館（自宅）」 일본어).
extract.py 를 다시 돌리면 TSV 묶음 경계가 바뀌므로(하스피 번역 파일과 어긋남) 다시 돌리지 않고 «덧붙이기»만 한다 — 여러 번 돌려도 같은 결과.

  · 메모장 구역(0x264000~0x26A100) 문장 → 번역 대상
  · KEEP: 화면에 나오는 낱말(요일 土·날짜 서식·아이템 三塚認定書·舵輪 등)
  · 권법 글꼴(WAZA.FON) 문자열 0x26F4D0~0x26FCA8 — 글자 칸이 재배치된 «붓글씨 기술명·커맨드 기호(偉=→ 등)».
    한글이 덮은 16~40구에 걸린 칸은 build_font extra 로 원본 그림째 옮겨야 하므로 «번역 = 원문 그대로» 행으로 넣는다.
  → work/text/lines.tsv 에 행 덧붙임 + work/text/tsv/sm1_084.tsv + work/text/sm1_084_풀이.tsv(사전 코드 풀이)
"""
import os, sys, re
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import exe_strings, memo_decode

KEEP = {0x25D5A0, 0x262680, 0x26280C, 0x262DC0, 0x262E80, 0x26B6B0, 0x26D614}
WAZA_FONT = (0x26F4D0, 0x26FCA8)
def is_waza_font(t): return WAZA_FONT[0] <= t < WAZA_FONT[1]

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    W = lambda *p: os.path.join(ROOT, 'work', *p)
    lines_p = W('text', 'lines.tsv')
    lines = open(lines_p, encoding='utf-8').read().splitlines()
    have = {l.split('\t')[1] for l in lines}
    add = []
    for t, rf, ln, s, room in exe_strings.main(W('disc1', '1ST_READ.BIN'), W('check', 'exe_strings.tsv')):
        key = 'exe:%06X' % t
        if key in have: continue
        if 0x264000 <= t < 0x26A100 or t in KEEP or is_waza_font(t):
            add.append((key, s, 'room=%d refs=%d' % (room, len(rf))))
    if add:
        with open(lines_p, 'a', encoding='utf-8', newline='\n') as w:
            for key, s, wh in add: w.write('exe\t%s\t\t%s\t%s\n' % (key, s, wh))
    # 번역 묶음 sm1_084 (전체 다시 씀: lines 의 보충 행 = 이 도구가 넣은 것 전부)
    rows = [l.split('\t') for l in open(lines_p, encoding='utf-8').read().splitlines()[1:]]
    orig = set()
    for f in os.listdir(W('text', 'tsv')):
        if f != 'sm1_084.tsv':
            for l in open(W('text', 'tsv', f), encoding='utf-8'):
                c = l.rstrip('\n').split('\t')
                if c[0].startswith(('exe:', 'dict:')): orig.add(c[3])      # 번역 묶음은 «원문 글» 단위 — 같은 글이 이미 있으면 그 번역이 쓰임
    kp = W('text', 'added_keys.txt')
    added = {k for k, *_ in add} | (set(open(kp, encoding='utf-8').read().split()) if os.path.exists(kp) else set())
    open(kp, 'w', encoding='utf-8').write('\n'.join(sorted(added)))
    seen = set(); mine = []
    for r in rows:
        if r[1] in added and r[3] not in orig and r[3] not in seen: seen.add(r[3]); mine.append(r)
    with open(W('text', 'tsv', 'sm1_084.tsv'), 'w', encoding='utf-8', newline='\n') as w:
        w.write('key\tspeaker\tcount\tjp\tko\n')
        for r in mine:
            t = int(r[1][4:], 16)
            w.write('%s\t%s\t1\t%s\t%s\n' % (r[1], '권법글꼴' if is_waza_font(t) else '', r[3], r[3] if is_waza_font(t) else ''))
    with open(W('text', 'sm1_084_풀이.tsv'), 'w', encoding='utf-8', newline='\n') as w:
        w.write('key\tspeaker\tcount\tjp\tjp_풀이\tko\n')
        for r in mine:
            t = int(r[1][4:], 16)
            if is_waza_font(t): continue
            w.write('%s\t\t1\t%s\t%s\t\n' % (r[1], r[3], memo_decode.decode(r[1], r[3])))
    print('lines 덧붙임 %d · sm1_084 %d행(권법 글꼴 %d)' % (len(add), len(mine), sum(1 for r in mine if is_waza_font(int(r[1][4:], 16)))))

if __name__ == '__main__':
    main()
