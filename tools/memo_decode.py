# -*- coding: utf-8 -*-
"""메모장 사전 코드 풀어 보기 — 번역용 TSV 에 «jp_풀이» 열을 더해 work/text/<이름>_풀이.tsv 로.
  메모 문장(0x264000~0x26A100): [1-9A-I][0-9] 두 글자 = 사전(0x27CED0, 159낱말) 번호 첫×10+둘째−10 → 〔낱말〕
                                 0[0-9] = 줄 앞 제어 → ‹0n› (번역에도 그대로 둘 것)
  기술 설명(0x26FFD4~0x271700): 두 자리 숫자 = 사전(0x293980, 00~38) → 〔낱말〕
  python tools/memo_decode.py work/text/tsv/sm1_082.tsv
"""
import os, sys, struct, re
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
B = 0x0C010000
d = open(os.path.join(ROOT, 'work', 'disc1', '1ST_READ.BIN'), 'rb').read()
def table(a, n):
    out = []
    for i in range(n):
        x = struct.unpack_from('<I', d, a + 4 * i)[0]; out.append(d[x-B:x-B+60].split(b'\0')[0].decode('euc_jp', 'replace'))
    return out
MEMO = table(0x27CED0, 159); WAZA = table(0x293980, 39)
def val(c): return int(c) if c.isdigit() else ord(c) - 55
def dec_memo(s):
    out = ''; i = 0
    while i < len(s):
        a = s[i]
        if a in '0123456789ABCDEFGHI' and i + 1 < len(s) and s[i+1].isdigit():
            if a == '0': out += '‹' + s[i:i+2] + '›'
            else:
                n = val(a) * 10 + int(s[i+1]) - 10; out += '〔' + (MEMO[n] if n < len(MEMO) else '?') + '〕'
            i += 2; continue
        out += a; i += 1
    return out
def dec_waza(s):
    return re.sub(r'[0-9]{2}', lambda m: '〔' + WAZA[int(m.group())] + '〕' if int(m.group()) < len(WAZA) else m.group(), s)
def decode(key, jp):
    if not key.startswith('exe:'): return jp
    off = int(key[4:], 16)
    if 0x264000 <= off < 0x26A100: return dec_memo(jp)
    if 0x26FFD4 <= off < 0x271700: return dec_waza(jp)
    return jp
if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    for p in sys.argv[1:]:
        rows = [l.rstrip('\n').split('\t') for l in open(p, encoding='utf-8')]
        out = ['key\tspeaker\tcount\tjp\tjp_풀이\tko']
        for c in rows[1:]: out.append('\t'.join(c[:4] + [decode(c[0], c[3])] + c[4:5]))
        dst = os.path.join(ROOT, 'work', 'text', os.path.basename(p)[:-4] + '_풀이.tsv')
        open(dst, 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n'); print(dst)
