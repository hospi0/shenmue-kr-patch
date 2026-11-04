# 메모장 해독 루틴(0x0C0F5084) 그대로 흉내 (2026-11-04)
#  · 원줄을 24 B 스택 버퍼로 sprintf → 줄 ≤ 22 B
#  · 줄 앞 0n(들여쓰기 n칸) 떼는 이동은 18 B 까지만 → 들여쓰기 줄 본문 ≥18 B 면 끝 글자 겹침(害害)
#  · 펼친 줄 = 부르는 함수 0x0C0F46C8 의 SP+0x58 버퍼: 원본 20 B(원본 최대 19 B) — build_exe 가 틀을 넓혀 36 B
#  · 버퍼는 앞 20 B 만 지움 → 사전 낱말(strcat)은 20 B 앞에서 시작해야 함
# 판정(OUT_MAX): 펼친 글 ≤ 20 B(10칸) · strcat 시작 < 20 · 의도한 글과 같음
import struct, sys
BASE=0x0C010000; DICT=0x27CED0
OUT_MAX=18   # 펼친 글 ≤ 9칸(18 B) — 0x0C0F5014 가 9칸으로 채워 그림
TABLES=[(0x27DB60,0x27ED20),(0x27FA00,0x2810C0)]
def cs(d,o): return d[o:d.index(0,o)]
def emu(d, line):
    sp=cs(d,0x263A08)
    buf=bytearray(line+b'\0'+b'\xEE'*64)
    R7=0;ind=0
    if buf[0]==0x30 and buf[1]==0x30:
        for k in range(20):
            buf[k]=buf[k+2]
            if buf[k]==0: break
    if buf[0]==0x30:
        R7=1; ind=buf[1]-0x30
        for k in range(18):
            buf[k]=buf[k+2]
            if buf[k]==0: break
    out=bytearray(); late=False
    if R7 and ind>0: out+=sp*ind
    i=0
    while i<20 and buf[i]!=0:
        c=buf[i]-0x30
        if 1<=c<=9: idx=c*10+buf[i+1]-0x30-10; w=True
        elif 0<=buf[i]-65 and buf[i]-64<=9: idx=(buf[i]-65)*10+buf[i+1]-0x30+90; w=True
        else: w=False
        if w and len(out)>=20: late=True
        if w: out+=cs(d,struct.unpack_from('<I',d,DICT+4*idx)[0]-BASE)
        else: out+=buf[i:i+2]
        i+=2
    return bytes(out), late, buf
def naive(d,line):
    s=line
    if s[:2]==b'00': s=s[2:]
    ind=0
    if s[:1]==b'0': ind=s[1]-48; s=s[2:]
    out=cs(d,0x263A08)*ind if ind>0 else b''
    i=0
    while i<len(s):
        c=s[i]-48
        if 1<=c<=9 or 0<=s[i]-65<=9:
            idx=(c*10+s[i+1]-58) if 1<=c<=9 else ((s[i]-65)*10+s[i+1]-48+90)
            out+=cs(d,struct.unpack_from('<I',d,DICT+4*idx)[0]-BASE)
        else: out+=s[i:i+2]
        i+=2
    return out
def scan(path):
    d=open(path,'rb').read(); bad=[]; mx=0
    for a,b in TABLES:
        for e in range(a,b,16):
            for k in range(4):
                p=struct.unpack_from('<I',d,e+4*k)[0]
                if not p: continue
                ln=cs(d,p-BASE); o,late,_=emu(d,ln); n=naive(d,ln); mx=max(mx,len(o)+1)
                if len(o)>OUT_MAX or late or o!=n or len(ln)>22: bad.append((e+4*k,len(ln),len(o)+1,o.decode('euc_jp','replace'),n.decode('euc_jp','replace')))
    return mx,bad
if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    for p in sys.argv[1:]:
        mx,bad=scan(p); print(p,'최대 출력',mx,'B · 문제',len(bad))
        for x in bad[:400]: print('  %06X 원줄 %dB 출력 %dB | %s | 의도 %s'%x)
