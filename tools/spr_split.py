# -*- coding: utf-8 -*-
"""SPR(TEXN 묶음) → 낱장 .PVR 로 쪼갠다(읽기 전용, 출력 폴더에만 씀).
TEXN 청크 = 'TEXN' + u32 청크 크기(머리 포함) + 8B 이름 + GBIX…PVRT…  (SCRL 등 다른 청크는 건너뜀)"""
import struct, sys, os, glob
def split(path, outdir):
    d = open(path, 'rb').read(); p = 0; n = 0; base = os.path.splitext(os.path.basename(path))[0]
    while p + 8 <= len(d):
        tag = d[p:p+4]; sz = struct.unpack_from('<I', d, p+4)[0]
        if sz < 8 or p + sz > len(d): break
        if tag == b'TEXN':
            raw = d[p+8:p+16].split(b'\0')[0]
            nm = ''.join(chr(c) if (48 <= c < 58 or 65 <= c < 91 or 97 <= c < 123) else '_' for c in raw) or str(n)
            open(os.path.join(outdir, '%s__%02d_%s.pvr' % (base, n, nm)), 'wb').write(d[p+16:p+sz]); n += 1
        p += sz
    return n
if __name__ == '__main__':
    src, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True); tot = 0
    for f in sorted(glob.glob(os.path.join(src, '*.SPR'))): tot += split(f, out)
    print(tot)
