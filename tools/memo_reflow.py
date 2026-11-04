# -*- coding: utf-8 -*-
"""메모장 줄 다시 나누기(2026-11-04 메모장 크래시).

해독 루틴(0x0C0F5090)은 한 줄을 sprintf("%s") 로 «24 B 스택 버퍼»에 복사한다 → 23 B 넘는 줄 = 스택 덮어써 크래시.
원문 한 줄 = 줄 앞 제어(0n) 빼고 최대 18 B(9칸), 펼친(사전 낱말 끼운) 화면 폭도 최대 9칸.
메모 한 칸 = 포인터 4개(16 B, 0 = 빈 줄) 고정 — 표: 어른 0x27DB60~0x27ED20, 어린이 0x27FA00~0x2810C0.

규칙: 칸의 어느 줄이라도 «본문 18 B 초과» 또는 «펼친 폭 9칸 초과»면 그 칸의 줄들을 이어 붙여 낱말(전각 공백) 단위로
     4줄 안에서 다시 나눈다. 각 줄의 줄 앞 제어는 «원래 그 자리 줄의 것»(새로 채우는 빈 줄은 없음).
     4줄에 안 들어가면 그 칸은 손대지 않고 넘침 목록에(빌드 중단 — 줄일 문장은 하스피가 정함).
  → work/build/memo_layout.tsv (표 자리 16진 \t 새 줄 글) · work/check/memo_overflow.tsv
  build_exe.py 가 memo_layout.tsv 를 읽어 새 줄을 빈 자리에 놓고 표 포인터를 바꾼다.
"""
import os, sys, re, struct, glob
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import build_exe as BE
from encode import normalize

TABLES = [(0x27DB60, 0x27ED20), (0x27FA00, 0x2810C0)]
# 쪽 기록표(18 B: 쪽 번호 2 B + 줄 8개 플래그 2 B) — 칸 k 의 줄 j 플래그 = REC + (k//2)*18 + 2 + 2*((k%2)*4 + j).
#   그 사건 플래그가 서야 그 줄이 써진다(0 = 항상). 어른 0x27D150 · 어린이 0x27ED20 (부르는 함수 0x0C0F46C8, 2026-11-04)
#   → 다시 나누기는 «같은 플래그 묶음» 안에서만, 빈 칸을 빌리면 그 칸 플래그도 묶음 값으로(work/build/memo_flags.tsv)
FLAGREC = {0x27DB60: 0x27D150, 0x27FA00: 0x27ED20}
DICT = 0x27CED0
MAXB, MAXB_PRE, MAXW, LINES = 20, 16, 9, 4   # 폭 9칸: 0x0C0F5014 가 줄을 9칸으로 채워 9칸 칸에 그림(10칸이면 옆 칸으로 번짐, 2026-11-04 실기)
B = BE.BASE
PAIR = re.compile(r'[1-9A-I][0-9]')

def load_tr(paths):
    tr = {}
    for p in paths:
        for l in open(p, encoding='utf-8'):
            c = l.rstrip('\n').split('\t')
            if len(c) >= 5 and c[0].startswith(('exe:', 'dict:')) and c[4].strip(): tr[c[3]] = c[4]
    return tr

def main(paths):
    sys.stdout.reconfigure(encoding='utf-8')
    d = open(BE.SRC, 'rb').read()
    tr = load_tr(paths)
    js = lambda o: d[o:].split(b'\0')[0].decode('euc_jp')
    words = []
    for i in range(159):
        w = js(struct.unpack_from('<I', d, DICT + 4 * i)[0] - B)
        words.append(normalize(BE.prep(w, tr.get(w, w))))
    def split_pre(t):
        m = re.match(r'0[0-9]', t); return (t[:2], t[2:]) if m else ('', t)
    def toks(body):
        """(글 조각, 바이트, 화면 폭) — 사전 코드 쌍은 한 덩어리"""
        out = []; i = 0
        while i < len(body):
            if i + 1 < len(body) and PAIR.fullmatch(body[i:i+2]):
                n = int(body[i]) if body[i].isdigit() else ord(body[i]) - 55
                out.append((body[i:i+2], 2, len(words[n * 10 + int(body[i+1]) - 10]))); i += 2
            else:
                out.append((body[i], 1 if ord(body[i]) < 0x80 else 2, 1)); i += 1
        return out
    def measure(body):
        t = toks(body); return sum(x[1] for x in t), sum(x[2] for x in t)
    def fits(body, pre=''):
        """해독 루틴 한계(tools/memo_emu.py): 들여쓰기 0n 줄은 본문 ≤16 B(18 B 이동 한계), 아니면 ≤20 B · 들여쓰기 n + 펼친 폭 ≤ 10칸"""
        b, w = measure(body); n = int(pre[1]) if pre else 0
        return b <= (MAXB_PRE if pre else MAXB) and n + w <= MAXW
    layout = []; over = []; nfix = 0; ndrop = 0
    mp = os.path.join(ROOT, 'work', 'text', 'memo_manual.tsv'); manual = {}
    if os.path.exists(mp):
        for l in open(mp, encoding='utf-8').read().splitlines()[1:]:
            c = l.split('	'); manual[c[0]] = c[1:5]
    flagp = []; ndedup = 0
    exp = lambda s: ''.join(words[(int(x[0]) if x[0].isdigit() else ord(x[0]) - 55) * 10 + int(x[1]) - 10] if PAIR.fullmatch(x) else x for x, _, _ in toks(s))
    nz = lambda s: re.sub(r'[ 　「」『』・＝]', '', exp(s))
    def wrap(text, pre_of):
        """pre_of(i) = 출력 i번째 줄의 줄 앞 제어 — 들여쓰기 칸까지 폭에 넣어 잰다"""
        out = ['']
        for w in [w for w in text.split('　') if w]:
            cand = (out[-1] + '　' + w) if out[-1] else w
            if fits(cand, pre_of(len(out) - 1)): out[-1] = cand; continue
            if out[-1]: out.append('')
            if fits(w, pre_of(len(out) - 1)): out[-1] = w; continue
            for tk in toks(w):                       # 한 낱말이 한 줄보다 김 → 글자 단위(코드 쌍은 안 쪼갬)
                if fits(out[-1] + tk[0], pre_of(len(out) - 1)): out[-1] += tk[0]
                else: out.append(tk[0])
        return out
    def lay_group(glines, pres_at):
        """플래그 묶음 하나의 줄들 → 줄 목록 [(제어, 글)]. pres_at(i) = 놓일 i번째 자리의 원래 줄 앞 제어."""
        if all(fits(b_, p_) for p_, b_ in glines) and all(p_ == pres_at(i) for i, (p_, b_) in enumerate(glines)):
            return list(glines)
        out = []
        for p_, b_ in glines:                                   # ① 하스피 줄 나눔 유지, 넘친 줄만 접기
            if fits(b_, pres_at(len(out))): out.append((pres_at(len(out)), b_)); continue
            k0 = len(out); w = wrap(b_.strip('　'), lambda i: pres_at(k0 + i))
            out += [(pres_at(k0 + i), x) for i, x in enumerate(w)]
        alt = '　'.join(b_.strip('　') for _, b_ in glines if b_.strip('　'))
        w = wrap(alt, pres_at)                                  # ② 이어 붙여 다시
        if len(w) < len(out): out = [(pres_at(i), x) for i, x in enumerate(w)]
        w = wrap(alt, lambda i: '')                             # ③ 들여쓰기 빼고
        if len(w) < len(out): out = [('', x) for x in w]
        return out
    for a0, a1 in TABLES:
        rb = FLAGREC[a0]
        for kk, e in enumerate(range(a0, a1, 16)):
            fa = [rb + (kk // 2) * 18 + 2 + 2 * ((kk % 2) * 4 + j) for j in range(4)]
            flags = [struct.unpack_from('<H', d, x)[0] for x in fa]
            slots = [struct.unpack_from('<I', d, e + 4 * k)[0] for k in range(4)]
            lines = []
            for x in slots:
                if not x: lines.append(None); continue
                j = js(x - B); k = tr.get(j)
                t = normalize(BE.prep(j, k)) if k else j
                lines.append(split_pre(t))
            pre0 = [l[0] if l else '' for l in lines]
            # 원문 읽기 괄호(藍帝（ランテイ）) 가 번역에선 같은 말 → 「란디（란디）」. 괄호 안 말이 같은 칸 앞에 이미 있으면 괄호째 뺀다.
            ded = False
            for li, l in enumerate(lines):
                if l is None: continue
                for m in list(re.finditer(r'（([^（）]*)）', l[1]))[::-1]:
                    inner = nz(m.group(1))
                    before = ''.join(nz(x[1]) for x in lines[:li] if x) + nz(l[1][:m.start()])
                    if len(inner) >= 2 and inner in before:
                        lines[li] = l = (l[0], (l[1][:m.start()] + l[1][m.end():]).strip('　')); ded = True; ndedup += 1
            key = '%06X' % e
            if not ded and key not in manual and all(l is None or fits(l[1], l[0]) for l in lines): continue
            # 플래그 묶음: 빈 줄 아닌 칸을 «잇닿은 같은 플래그»끼리
            groups = []
            for i, l in enumerate(lines):
                if l is None: continue
                if groups and groups[-1][0] == flags[i] and groups[-1][1][-1] == max(j for j in range(i) if lines[j] is not None): groups[-1][1].append(i)
                else: groups.append((flags[i], [i]))
            gl = [[lines[i] for i in g[1] if lines[i][1]] for g in groups]
            if key in manual:
                cells = (manual[key] + [''] * 4)[:4]
                if len(groups) > 1 or any(c.startswith('{') for c in cells):
                    # 자리별 손 교정: 칸 k = 줄 k. 원래 빈 칸에 글을 넣으면 앞 칸 플래그(「{HEX}글」로 지정 가능)
                    row = [''] * LINES; bad = []
                    for k, c in enumerate(cells):
                        fx = None
                        m = re.match(r'\{([0-9A-Fa-f]+)\}', c)
                        if m: fx = int(m.group(1), 16); c = c[m.end():]
                        c = normalize(c.replace(' ', '　'))
                        if not c: continue
                        p_ = pre0[k] if lines[k] is not None and fits(c, pre0[k]) else ''
                        if not fits(c, p_): bad.append(c)
                        row[k] = p_ + c
                        want = fx if fx is not None else (flags[k] if slots[k] else next((flags[j] for j in range(k - 1, -1, -1) if slots[j]), flags[k]))
                        if flags[k] != want: flagp.append((fa[k], want))
                    if bad: over.append('%s\t자리별 손 교정 넘침\t%s' % (key, ' / '.join(bad))); continue
                    nfix += 1
                    for k in range(LINES): layout.append('%06X\t%s' % (e + 4 * k, row[k]))
                    continue
                ml = [normalize(x.replace(' ', '　')) for x in manual[key] if x]
                gl = [[('', x) for x in ml]]
            # 묶음마다 놓을 자리(시작 a, 줄 수 n) 찾기: 자기 원래 칸 + 빈 칸(포인터 0)만, 순서 유지·안 겹침. 빌린 칸 수·이동 최소.
            best = None
            def search(gi, start, acc, cost):
                nonlocal best
                if gi == len(groups):
                    if best is None or cost < best[0]: best = (cost, list(acc))
                    return
                own = set(groups[gi][1])
                for a in range(start, LINES):
                    pa = lambda i, a=a: pre0[a + i] if a + i < LINES and lines[a + i] is not None and (a + i) in own else ''
                    out = lay_group(gl[gi], pa)
                    if key in manual and len(groups) == 1: out = [(('' if not fits(x, pa(i)) else pa(i)), x) for i, (_, x) in enumerate(out)]
                    n = len(out)
                    if a + n > LINES: continue
                    if any(not (s_ in own or slots[s_] == 0) for s_ in range(a, a + n)): continue
                    c = sum(1 for s_ in range(a, a + n) if s_ not in own) * 10 + abs(a - groups[gi][1][0])
                    search(gi + 1, a + n, acc + [(a, out)], cost + c)
            search(0, 0, [], 0)
            if best is None:
                over.append('%s\t%s\t%s' % (key, '플래그 묶음 자리 부족', ' / '.join(l[1] for l in lines if l))); continue
            if any(len(o) == 0 for _, o in best[1]): pass
            if any(not fits(x, p_) for _, o in best[1] for p_, x in o):
                over.append('%s\t%s\t%s' % (key, '줄 넘침', ' / '.join(x for _, o in best[1] for _, x in o))); continue
            row = [''] * LINES
            for (a, out), (f, _) in zip(best[1], groups):
                for i, (p_, x) in enumerate(out):
                    row[a + i] = p_ + x
                    if flags[a + i] != f: flagp.append((fa[a + i], f))
            if not any(l is None or not fits(l[1], l[0]) for l in lines) and [ (l[0] + l[1]) if l else '' for l in lines] == row: continue
            nfix += 1
            if any(p_ == '' and pre0[a + i] for (a, out) in best[1] for i, (p_, x) in enumerate(out)): ndrop += 1
            for k in range(LINES): layout.append('%06X\t%s' % (e + 4 * k, row[k]))
    print('읽기 괄호 겹침 뺌 %d · 빈 줄 자리 빌려 플래그 바꿈 %d' % (ndedup, len(flagp)))
    os.makedirs(os.path.join(ROOT, 'work', 'build'), exist_ok=True)
    open(os.path.join(ROOT, 'work', 'build', 'memo_layout.tsv'), 'w', encoding='utf-8', newline='\n').write('slot\ttext\n' + ''.join(l + '\n' for l in layout))
    open(os.path.join(ROOT, 'work', 'build', 'memo_flags.tsv'), 'w', encoding='utf-8', newline='\n').write('addr\tflag\n' + ''.join('%06X\t%04X\n' % x for x in flagp))
    os.makedirs(os.path.join(ROOT, 'work', 'check'), exist_ok=True)
    open(os.path.join(ROOT, 'work', 'check', 'memo_overflow.tsv'), 'w', encoding='utf-8', newline='\n').write('entry\tlines\ttext\n' + ''.join(l + '\n' for l in over))
    print('메모 칸 다시 나눔 %d (들여쓰기 뺀 칸 %d) · 4줄 넘침 %d (work/check/memo_overflow.tsv)' % (nfix, ndrop, len(over)))
    return len(over)

if __name__ == '__main__':
    main([q for p in sys.argv[1:] for q in glob.glob(p)])
