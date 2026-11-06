# -*- coding: utf-8 -*-
r"""쉔무 1장 요코스카 배포 묶음 — dist/Shenmue1_KR_<VER>/ : 장마다 트랙 3·6 xdelta + xdelta.exe + readme.txt(CP949) + 한글패치_적용.bat(CP949) + zip
  (건버드 2 tools/make_dist.py 를 옮김, 2026-11-04) 바뀌는 트랙: 1~3장 각각 트랙 3·6 — 나머지 트랙·cue 는 원본 그대로.
  검증: 원본 트랙 → xdelta 적용 → md5 = 빌드(dist/build/discN) 트랙 md5.
  python tools/make_dist.py   (먼저 빌드: gfx_pack pack → build_resume → build_text → discbuild --disc 1..3 --write)
"""
import hashlib, os, shutil, subprocess, sys, zipfile
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)

VER = 'v0.92'
XDELTA = r'C:\claude\utils\xdelta.exe'
ROM = 'Shenmue - Isshou Yokosuka (Japan) (Disc %d)'
SRC = r'C:\claude\roms\dc'
NAME = 'Shenmue1_KR_' + VER
TITLE = '쉔무 1장 요코스카 (Shenmue, 드림캐스트 일본판 3장) 한글 패치 ' + VER
TRACKS = (3, 6)


def md5(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''):
            h.update(b)
    return h.hexdigest().upper()


README = """{title}
{line}

드림캐스트 일본판 "Shenmue Isshou Yokosuka" 3장(Disc 1~3)의
장마다 트랙 3번과 트랙 6번에 패치하시면 됩니다.

{table}

[ 적용 방법 ]

  1) 원본 트랙 3·6 파일(3장 모두 = 6개)을 이 폴더에 복사
  2) 한글패치_적용.bat 실행 → 이름 끝에 [KR] 이 붙은 파일이 만들어집니다
  3) 만든 파일 이름을 원본 이름으로 바꿔 넣고, 나머지 트랙과 cue 는 원본 그대로 쓰세요
     (장 하나만 있어도 그 장만 패치됩니다)

  직접 적용:
    xdelta.exe -d -s "원본 트랙" "패치 파일" "결과 파일"
  (Delta Patcher 같은 xdelta3 GUI 도구로 적용해도 됩니다. 원본이 다르면 xdelta 가 적용을 거부합니다.)


[ 바뀌는 것 ]

  - 음성 대사 자막 전부, NPC 대화·대화 선택지
  - 메뉴·아이템·도움말·설정·메모장(사전 낱말·줄마다 사건 플래그에 맞춰 조판)
  - 기술 화면(기술 이름·커맨드·설명), 침대 메뉴
  - 혼잣말·문 너머 목소리 등 상주 대사, 이어하기 안내
  - 화면 그림 글자(타이틀·메뉴 등)
  - 마을 간판·문패·표지판·지도·안내판, 아버지 편지·비전서·봉투 등 맵 텍스처 글자
  - 세이브·로드·메모리 카드 안내문, 일시 중단·저장 화면
  - 글꼴: 대사(갈무리), 메모장 손글씨(푸어스토리)


[ 알려진 점 ]

  - 음성은 원본 일본어 그대로입니다.
  - 엔딩 스태프 롤은 원본 그대로입니다.
  - 메모장은 한 줄 9칸 한도라 일부 문장을 줄였습니다.
"""

BAT = r"""@echo off
chcp 949 >nul
set "XD=%~dp0xdelta.exe"
set DONE=0
{body}
if "%DONE%"=="0" echo   [오류] 원본 트랙 파일을 이 폴더에 넣어 주세요 - readme 참고.
pause
"""
BAT_ONE = r"""if exist "%~dp0{bin}" (
  "%XD%" -d -f -s "%~dp0{bin}" "%~dp0{patch}" "%~dp0{kbin}"
  if errorlevel 1 (echo   [오류] Disc {n} 트랙 {t} 패치 실패 - 원본이 다를 수 있습니다) else (echo   완료: Disc {n} 트랙 {t} & set DONE=1)
)
"""   # ⛔ if 블록 안 echo 에 괄호 금지(파일 이름의 (Japan) 이 블록을 닫음)


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    d = os.path.join(ROOT, 'dist', NAME)
    reuse = '--reuse' in sys.argv            # 이미 만들고 검산한 xdelta 재사용(readme·bat·zip 만 다시)
    if os.path.isdir(d) and not reuse:
        shutil.rmtree(d)
    os.makedirs(d, exist_ok=True)
    rows = []; bats = []
    for n in (1, 2, 3):
        rom = ROM % n
        for t in TRACKS:
            b = '%s (Track %d).bin' % (rom, t)
            src = os.path.join(SRC, rom, b); out = os.path.join(ROOT, 'dist', 'build', 'disc%d' % n, b)
            patch = '%s_Disc%d_Track%d.xdelta' % (NAME, n, t); pp = os.path.join(d, patch)
            if reuse and os.path.exists(pp):
                o, want = md5(src), md5(out); got = want
            else:
                subprocess.run([XDELTA, '-e', '-9', '-B', '1073741824', '-f', '-s', src, out, pp], check=True)
                chk = os.path.join(d, '_check.bin')
                subprocess.run([XDELTA, '-d', '-f', '-s', src, pp, chk], check=True)
                o, want, got = md5(src), md5(out), md5(chk)
                os.remove(chk)
            assert got == want, ('패치 적용 결과가 빌드와 다름', b, got, want)
            print('Disc %d 트랙 %d 원본md5 %s → 패치md5 %s · %d B' % (n, t, o, want, os.path.getsize(pp)), flush=True)
            rows.append('  Disc %d 트랙 %d\n    원본md5 : %s\n    패치md5 : %s\n    패치 파일: %s\n' % (n, t, o, want, patch))
            kbin = '%s (Track %d) [KR].bin' % (rom, t)
            bats.append(BAT_ONE.format(bin=b, patch=patch, kbin=kbin, n=n, t=t))
    shutil.copy2(XDELTA, os.path.join(d, 'xdelta.exe'))
    readme = README.format(title=TITLE, line='=' * 60, table='\n'.join(rows))
    open(os.path.join(d, 'readme.txt'), 'wb').write(readme.replace('\n', '\r\n').encode('cp949'))
    open(os.path.join(d, '한글패치_적용.bat'), 'wb').write(BAT.format(body=''.join(bats)).replace('\n', '\r\n').encode('cp949'))
    z = os.path.join(ROOT, 'dist', NAME + '.zip')
    with zipfile.ZipFile(z, 'w', zipfile.ZIP_DEFLATED) as zf:
        for f in sorted(os.listdir(d)):
            zf.write(os.path.join(d, f), NAME + '/' + f)
    print('✅', d)
    for f in sorted(os.listdir(d)):
        print('  %-56s %12d' % (f, os.path.getsize(os.path.join(d, f))))
    print('  zip %s %d B · md5 %s' % (os.path.basename(z), os.path.getsize(z), md5(z)))


if __name__ == '__main__':
    main()
