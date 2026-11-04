# -*- coding: utf-8 -*-
"""번역 TSV 검사(빌드 전) — 하스피 번역본을 병합하기 전에 «모든 문제를 한 번에» 모은다(빌드처럼 첫 오류에서 멈추지 않음).

  python tools/check_tr.py <TSV 폴더>     → work/check/check_report.tsv (+ 화면 요약)

검사
  구조   : 원본 work/text/tsv 와 키·화자·횟수·원문 일치, 열 5개
  글자   : encode() 가능(완성형 밖 음절 = extra 후보), 한글이 덮은 JIS 16~40구(+extra 구)에 걸리는 한자·기호(화면에 엉뚱한 한글로 나옴)
           가나 남음(덜 번역), 반각 영숫자(전각으로 바뀜 — 알림만)
  줄     : 자막 19칸×2줄(build_text.wrap 그대로), PKS(NPC 표) 줄 수
  토큰   : 「」『』 개수, 앞뒤 전각 공백, PKS «화자「본문」», 실행 파일 제어 토큰(build_exe.check_tokens) · 헬프 줄 23자 · 아이템 칸 바이트
  통일   : 같은 원문 → 다른 번역
"""
import os, sys, glob, re, collections, struct
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from encode import encode, normalize
import build_text as BT
import build_exe as BE
import exe_strings

KANA = re.compile(r'[\u3041-\u3096\u30a1-\u30fa]')

def jis_row(ch):
    try: b = ch.encode('euc_jp')
    except UnicodeEncodeError: return None
    return b[0] - 0xA0 if len(b) == 2 and b[0] >= 0xA1 else None

def load(folder):
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, 'work', 'text', 'tsv', '*.tsv'))):
        b = os.path.basename(f)[:-4]
        cand = glob.glob(os.path.join(folder, b + '*.tsv'))
        if len(cand) != 1: out.append((b, 0, None, 'FILE', len(cand))); continue
        o = [l.rstrip('\n').split('\t') for l in open(f, encoding='utf-8')]
        u = [l.rstrip('\r\n').split('\t') for l in open(cand[0], encoding='utf-8-sig')]
        for i in range(1, max(len(o), len(u))):
            out.append((os.path.basename(cand[0]), i + 1, o[i] if i < len(o) else None, u[i] if i < len(u) else None))
    return out

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    folder = sys.argv[1]
    rows = load(folder)
    kinds = {}
    for l in open(os.path.join(ROOT, 'work', 'text', 'lines.tsv'), encoding='utf-8'):
        c = l.rstrip('\n').split('\t'); kinds.setdefault(c[1], c[0])
    extra_rows = set()
    ex = os.path.join(ROOT, 'work', 'font', 'extra_map.tsv')
    if os.path.exists(ex):
        for l in open(ex, encoding='utf-8'): extra_rows.add(int(l.split('\t')[1][:2], 16) - 0xA0)
    bad_rows = set(range(16, 41)) | extra_rows
    # 실행 파일 정보
    d = open(BE.SRC, 'rb').read()
    info = {t: (refs, ln, room, s) for t, refs, ln, s, room in exe_strings.main(BE.SRC, os.path.join(ROOT, 'work', 'check', 'exe_strings.tsv'))}
    lim = BE.field_limits(d)
    help_set = {struct.unpack_from('<I', d, p)[0] - BE.BASE for a, b in BE.ORDERED_TABLES for p in range(a, b, 4)}
    rep = []
    def R(sev, f, ln, key, what, jp, ko): rep.append((sev, f, ln, key, what, jp, ko))
    seen = collections.defaultdict(lambda: collections.defaultdict(list))
    for f, ln, o, u in rows:
        if ln == 0: R('오류', f, 0, '', '번역 파일 %d개' % u, '', ''); continue
        if u is None or o is None: R('오류', f, ln, '', '행 수 다름', '', ''); continue
        if len(u) != 5: R('오류', f, ln, u[0], '열 %d개' % len(u), '', '\t'.join(u)); continue
        if u[:4] != o[:4]: R('오류', f, ln, u[0], '키·원문 바뀜', o[3], u[3]); continue
        key, spk, cnt, jp, ko = u
        if not ko.strip():
            if jp.strip(): R('알림', f, ln, key, '번역 비어 있음(원문 그대로 들어감)', jp, ko)
            continue
        kind = kinds.get(key, 'exe' if key.startswith(('exe:', 'dict:')) else '?')
        seen['exe' if kind in ('exe', 'dict') else 'talk'][jp].append((f, ln, ko))
        # 글자
        body = re.sub(r'[\x20-\x7e]', '', ko) if kind in ('exe', 'dict') else ko
        for ch in sorted(set(normalize(body))):
            if '가' <= ch <= '힣':
                if len(ch.encode('euc_kr', 'ignore')) != 2: R('알림', f, ln, key, '완성형 밖 음절 %s → 글꼴 41구 이후 빈 칸에 자동 추가' % ch, jp, ko)
                continue
            r = jis_row(BT.encode.__globals__['to_wide'](ch)) if ch != '＆' else None
            if r is None and ch not in '＆':
                try: encode(ch)
                except ValueError as e: R('오류', f, ln, key, '못 넣는 글자 %r' % ch, jp, ko)
            elif r in bad_rows: R('알림', f, ln, key, '한글 칸(%d구)에 덮인 한자 %s → 원본 글자 그림을 41구 이후 빈 칸으로 옮겨 씀' % (r, ch), jp, ko)
        if KANA.search(ko): R('경고', f, ln, key, '가나 남음: ' + ''.join(KANA.findall(ko)), jp, ko)
        # 괄호·공백
        for a, b in ('「」', '『』'):
            if jp.count(a) != ko.count(a) or jp.count(b) != ko.count(b):
                R('경고' if kind != 'pks' else '오류', f, ln, key, '%s%s 개수 다름' % (a, b), jp, ko)
        lead = lambda s: len(s) - len(s.lstrip('　'))
        trail = lambda s: len(s) - len(s.rstrip('　'))
        if kind not in ('exe', 'dict') and (lead(jp) != lead(ko) or trail(jp) != trail(ko)):
            R('경고', f, ln, key, '앞뒤 전각 공백 다름', jp, ko)
        if re.search(r'  |　　', ko.strip('　')) and kind not in ('exe', 'dict') and not re.search(r'  |　　', jp):
            R('경고', f, ln, key, '공백 두 칸', jp, ko)
        # 줄
        if kind in ('cut', 'free'):
            L = BT.wrap(ko)
            if len(L) > BT.MAXLINES or any(len(x) > BT.WIDTH for x in L):
                R('오류', f, ln, key, '자막 넘침 %d줄/최대 %d칸(19칸×2줄)' % (len(L), max(map(len, L))), jp, '＆'.join(L))
            elif '＆' in ko and '＆'.join(L) != normalize(ko).replace('＆', '＆'):
                if [p for p in normalize(ko).split('＆')] != L:
                    R('알림', f, ln, key, '＆ 줄이 19칸 넘어 다시 접음', jp, '＆'.join(L))
        elif kind == 'pks':
            if jp.count('＆') != ko.count('＆'): R('알림', f, ln, key, 'NPC 표 줄 수 다름(원문 %d / 번역 %d)' % (jp.count('＆') + 1, ko.count('＆') + 1), jp, ko)
            if ('「' in jp) and not re.fullmatch(r'[^「」]*「.*」', ko.replace('＆', '')):
                R('오류', f, ln, key, 'PKS «화자「본문」» 꼴 아님', jp, ko)
        # 실행 파일
        if kind in ('exe', 'dict'):
            off = int(key.split(':')[1], 16) if key.startswith('exe:') else None
            if kind == 'dict': continue
            if off not in info: R('알림', f, ln, key, '가짜 포인터 문자열(빌드에서 건너뜀)', jp, ko); continue
            k2 = BE.prep(info[off][3], ko)
            e = BE.check_tokens(off, info[off][3], k2)
            if e: R('오류', f, ln, key, e, jp, ko); continue
            try: b = BE.enc_mixed(k2)
            except ValueError as x:
                if '완성형 밖' in str(x): b = BE.enc_mixed(k2.replace('슌', '가').replace('푱', '가'))
                else: R('오류', f, ln, key, str(x), jp, ko); continue
            if off in help_set:
                # 헬프 = 조각(0) 격자: 조각 수 원문과 같게 · 한 조각 ≤ 50 B (build_exe 와 같은 규칙, 2026-11-04)
                if info[off][3].count('0') != b.count(b'0'): R('오류', f, ln, key, '헬프 조각 수(0) %d ≠ 원문 %d' % (b.count(b'0'), info[off][3].count('0')), jp, ko)
                for seg in re.split(rb'[0A-Z]', b):
                    n = len(re.sub(rb'[A-Za-z]', b'', seg))
                    if n > 50: R('오류', f, ln, key, '헬프 한 조각 %d B > 50 B' % n, jp, seg.decode('euc_jp', 'replace'))
            if off in lim and len(b) > lim[off]:
                R('오류', f, ln, key, '아이템 칸 %d B > %d B' % (len(b), lim[off]), jp, ko)
    for grp, m in seen.items():
        for jp, v in m.items():
            ks = {normalize(x[2]) for x in v}
            if len(ks) > 1:
                R('경고', v[0][0], v[0][1], grp, '같은 원문 다른 번역 %d가지: ' % len(ks) + ' / '.join('%s:%d' % (x[0][4:7], x[1]) for x in v), jp, ' ‖ '.join(sorted(ks)))
    os.makedirs(os.path.join(ROOT, 'work', 'check'), exist_ok=True)
    out = os.path.join(ROOT, 'work', 'check', 'check_report.tsv')
    with open(out, 'w', encoding='utf-8', newline='\n') as w:
        w.write('sev\tfile\tline\tkey\twhat\tjp\tko\n')
        for r in sorted(rep, key=lambda r: ({'오류': 0, '경고': 1, '알림': 2}[r[0]], r[4].split(' ')[0], r[1], r[2])):
            w.write('\t'.join(map(str, r)) + '\n')
    c = collections.Counter((r[0], re.sub(r'[\d\s:/A-Za-z가-힣%()（）→«»「」『』.,·<>=≤×…]*$', '', re.split(r'[ :(]', r[4])[0])) for r in rep)
    c = collections.Counter((r[0], r[4].split(':')[0].split('(')[0].rstrip('0123456789 ')[:24]) for r in rep)
    for (s, w_), n in sorted(c.items()): print('%s\t%5d\t%s' % (s, n, w_))
    print(out)

if __name__ == '__main__':
    main()
