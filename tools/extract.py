# -*- coding: utf-8 -*-
"""쉔무1 번역 원문표 추출 (읽기 전용 → work/text/).

키 규칙
  - SRF 대사 : IDX 가 가리키면 «음성 이름»(예 F1015B002, A0114A002), 아니면 «AFS/SRF#레코드»(예 FREE01/F1061#3)
               → 세 장에서 (키, 원문)이 같으면 한 줄로 합치고 나온 곳을 전부 적는다.
  - PKS(HUMANS) : 같은 음성 이름이 SRF 에 있으면 그 줄에 «pks» 표시만, 없으면 따로 한 줄.
  - 실행 파일 : exe:<오프셋16진> (exe_strings.py 결과), 메모장 사전 = dict:<번호>

출력
  work/text/lines.tsv       전체 (kind, key, speaker, jp, where)
  work/text/tsv/sm1_NNN.tsv 18KB 단위 번역용 (key, speaker, jp, ko)
"""
import sys, os, glob, re, struct, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from afs import read_afs
from srf import parse_srf
from idx import parse_idx
import exe_strings

SPLIT = 18 * 1024
W = lambda *p: os.path.join(ROOT, 'work', *p)


def write_split(folder, stem, head, lines):
    os.makedirs(folder, exist_ok=True)
    for f in glob.glob(os.path.join(folder, stem + '_*.tsv')): os.remove(f)
    chunks = []; cur = []; size = len(head.encode('utf-8'))
    for ln in lines:
        n = len(ln.encode('utf-8'))
        if cur and size + n > SPLIT: chunks.append(cur); cur = []; size = len(head.encode('utf-8'))
        cur.append(ln); size += n
    if cur: chunks.append(cur)
    for i, c in enumerate(chunks, 1):
        with open(os.path.join(folder, '%s_%03d.tsv' % (stem, i)), 'w', encoding='utf-8', newline='\n') as w:
            w.write(head + ''.join(c))
    return len(chunks)


def srf_lines():
    rows = collections.OrderedDict()   # (key, jp) -> [speaker, kind, wheres]
    for n in (1, 2, 3):
        for f in sorted(glob.glob(W('disc%d' % n, 'SCENE', '*', 'STREAM', '*.AFS'))):
            ip = f[:-4] + '.IDX'
            if f.endswith('HUMANS.AFS') or not os.path.exists(ip): continue
            an = os.path.basename(f)[:-4]
            d, es = read_afs(f)
            _, _, ents, _ = parse_idx(open(ip, 'rb').read())
            ref = {(si, off): nm.upper() for nm, fi, si, off in ents if si != 0xFFFF}
            kind = 'free' if an.startswith('FREE') else 'cut'
            for si, (sn, so, ss) in enumerate(es):
                if not sn.upper().endswith('.SRF'): continue
                for k, r in enumerate(parse_srf(d[so:so + ss])[0]):
                    if not r['text']: continue
                    if '\t' in r['text'] or '\n' in r['text']: raise SystemExit('탭/줄바꿈 원문 %s %s' % (f, sn))
                    key = ref.get((si, r['off'])) or '%s/%s#%d' % (an, sn[:-4], k)
                    e = rows.setdefault((key, r['text']), [r['name'], kind, []])
                    e[2].append('%d:%s/%s#%d' % (n, an, sn[:-4], k))
    return rows


def pks_lines():
    d, es = read_afs(W('disc1', 'SCENE', '01', 'STREAM', 'HUMANS.AFS'))
    out = collections.OrderedDict()
    for nm, o, s in es:
        if not nm.endswith('.PKS'): continue
        for m in re.finditer(rb'([A-Z][0-9A-Z]{8})\x00([\xa1-\xfe][^\x00]*)\x00', d[o:o + s]):
            try: t = m.group(2).decode('euc_jp')
            except UnicodeDecodeError: continue
            out.setdefault(m.group(1).decode(), (nm[:-4], t))
    return out


def memo_dict(exe):
    B = 0x0C010000; out = []; i = 0x27CED0
    while True:
        v = struct.unpack_from('<I', exe, i)[0]
        if not (B + 0x250000 <= v < B + 0x270000): break
        o = v - B; out.append((len(out), o, exe[o:exe.find(b'\0', o)].decode('euc_jp'))); i += 4
    return out


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    os.makedirs(W('text'), exist_ok=True)
    srf = srf_lines(); pks = pks_lines()
    keys_srf = {k for k, _ in srf}
    lines = []
    for (key, jp), (spk, kind, wh) in srf.items():
        lines.append((kind, key, spk, jp, ','.join(wh) + (',pks' if key in pks else '')))
    pk_only = 0
    for key, (who, t) in pks.items():
        if key in keys_srf: continue
        pk_only += 1
        lines.append(('pks', key, who, t.replace('\n', '＆'), 'HUMANS/%s.PKS' % who))
    exe_path = W('disc1', '1ST_READ.BIN'); exe = open(exe_path, 'rb').read()
    talk = set(''.join(r[3] for r in lines))
    def noise(s):
        # 대사에 한 번도 안 나온 글자가 있고 가나가 없으면 코드·데이터를 문자열로 잘못 본 것(「膀」「廚援頼慢瑛咳」)
        odd = [c for c in s if c not in talk and ord(c) >= 0x80 and not ('０' <= c <= 'ｚ')]
        kana = any('぀' <= c <= 'ヿ' for c in s)
        return bool(odd) and not kana
    dropped = 0
    for t, rf, ln, s, room in exe_strings.main(exe_path, W('exe_strings.tsv')):
        if noise(s): dropped += 1; continue
        lines.append(('exe', 'exe:%06X' % t, '', s.replace('\n', '\\n'), 'room=%d refs=%d' % (room, len(rf))))
    for k, o, s in memo_dict(exe):
        lines.append(('dict', 'dict:%d' % k, '', s, '%06X' % o))
    with open(W('text', 'lines.tsv'), 'w', encoding='utf-8', newline='\n') as w:
        w.write('kind\tkey\tspeaker\tjp\twhere\n')
        for r in lines: w.write('\t'.join(r) + '\n')
    c = collections.Counter(r[0] for r in lines)
    ch = collections.Counter()
    for r in lines: ch[r[0]] += len(r[3])
    print('줄:', dict(c)); print('글자:', dict(ch)); print('PKS 전용:', pk_only, '/ 실행 파일 잡음 제외:', dropped)
    dup_keys = collections.Counter(k for k, _ in srf)
    print('같은 키·다른 원문:', sum(1 for v in dup_keys.values() if v > 1))
    # 번역용은 «원문 문장» 단위로 한 번만(대사끼리 / 실행 파일·사전은 따로 묶음 — 같은 글이라도 조판이 다르다)
    uniq = collections.OrderedDict()
    for r in lines:
        grp = 'exe' if r[0] in ('exe', 'dict') else 'talk'
        e = uniq.setdefault((grp, r[3]), [r[1], r[2], 0]); e[2] += 1
    tl = ['%s\t%s\t%d\t%s\t\n' % (k, spk, cnt, jp) for (g, jp), (k, spk, cnt) in uniq.items()]
    print('번역할 문장(중복 제거):', len(uniq), '글자', sum(len(jp) for g, jp in uniq))
    n = write_split(W('text', 'tsv'), 'sm1', 'key\tspeaker\tcount\tjp\tko\n', tl)
    print('TSV 묶음', n, '개 (18KB)')


if __name__ == '__main__':
    main()
