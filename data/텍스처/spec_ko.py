# -*- coding: utf-8 -*-
# 맵 텍스처 한글화 스펙(tools/tex_kr.py) — box = 원본 텍스처 화소 좌표(대강 상자 → 안에서 원문 글자 잉크 범위를 재서 그 안에만 한글)
# 이름 읽기: 대사 번역에 있으면 그대로(곤도·야다·노구치·아베·마에다·나가이·오카야마·핫토리·아이다·류), 없으면 거센소리 규칙
SPEC = {}
GROUP = {}
def S(id_, group, *items):
    SPEC[id_] = list(items); GROUP[id_] = group
def B(x0, y0, x1, y1, t, **kw):
    d = dict(box=(x0, y0, x1, y1), t=t); d.update(kw); return d

# ───────── 문패 ─────────
_n = [('야다', '신자토'), ('무라오카', '카야마'), ('니무라', '이시다'), ('스나가', '미치이')]
S('856c75548722', '문패', B(0, 0, 64, 64, '', erase='alpha'), *[B(x0, y0, x1, y1, _n[r][c], font='gothic', fit='box')
                           for r, (y0, y1) in enumerate([(4, 16), (18, 30), (32, 44), (46, 58)])
                           for c, (x0, x1) in enumerate([(3, 29), (36, 62)])])
S('d6d8b8243b31', '간판',
  B(0, 0, 256, 100, '', erase='alpha'), B(100, 118, 199, 156, '', erase='alpha'), B(100, 160, 256, 230, '', erase='alpha'),
  B(2, 6, 210, 24, '행온 1코인 클리어', font='heavy', align='l'),
  B(2, 28, 254, 48, '스페이스 해리어 1코인 클리어', font='heavy', align='l'),
  B(2, 52, 172, 74, '메달 10000개 획득', font='heavy', align='l'),
  B(2, 76, 172, 98, '메달 50000개 획득', font='heavy', align='l'),
  B(104, 122, 198, 154, '게임센터', font='heavy'),
  B(108, 166, 254, 222, '슬롯 하우스', font='heavy', color=(12, 12, 12), stroke=((90, 30, 60), 1)))
S('b8eda874cd03', '문패', B(8, 10, 60, 56, '시라이', font='gothic'))
S('b6682268cd99', '문패', B(6, 12, 60, 56, '키타자와', font='gothic'))
S('88934365da6b', '문패', B(0, 4, 64, 58, '이와사키', font='gothic'))
S('77bcb4a551bd', '문패', B(6, 14, 60, 56, '모리노', font='gothic'))
S('60d060846ab6', '문패', B(4, 14, 62, 60, '사토', font='gothic'))
S('56f1c8b69755', '문패', B(6, 14, 62, 60, '곤도', font='gothic'))
S('ffb610bd301f', '문패', B(58, 15, 113, 40, '야마시타', font='gothic'))
S('13f20273b340', '문패', B(0, 0, 64, 64, '', erase='alpha'), B(2, 6, 62, 28, '코포', font='gothic', fit='box'), B(2, 34, 62, 58, '와카바', font='gothic', fit='box'))
S('61b1e371ee13', '문패', B(0, 0, 64, 64, '', erase='alpha'), B(2, 6, 62, 28, '코포', font='gothic', fit='box'), B(2, 34, 62, 58, '츠쿠시', font='gothic', fit='box'))
S('2fc377fb1254', '문패', B(0, 0, 64, 64, '', erase='alpha'), B(2, 6, 62, 28, '코포', font='gothic', fit='box'), B(2, 34, 62, 58, '츠쿠시', font='gothic', fit='box'))
S('de0fa6ecc86b', '문패', B(0, 0, 128, 128, '', erase='alpha'), B(14, 12, 114, 50, '모치즈키장', font='gothic', fit='box'),
  B(14, 54, 114, 82, '코포', font='gothic', fit='box'), B(14, 84, 114, 120, '오이와', font='gothic', fit='box'))
S('f17a9829774c', '문패', B(12, 12, 54, 38, '오카야마'), B(12, 38, 54, 56, '하이츠'))
S('cc5c66a41467', '문패', B(0, 0, 64, 64, '', erase='alpha'), B(4, 8, 62, 38, '오카야마', fit='box'), B(4, 40, 62, 60, '하이츠', fit='box'))
S('ac585e15e4b9', '문패', B(10, 16, 70, 56, '하이츠', font='gaegu'), B(22, 56, 112, 116, '사쿠라', font='gaegu'))
S('5252e36f7710', '간판', B(0, 0, 64, 64, '', erase='alpha'), B(2, 2, 62, 30, '나가이', font='gothic', fit='box', color=(255, 255, 255)),
  B(2, 34, 62, 62, '흥업', font='gothic', fit='box', color=(255, 255, 255)))
S('205c97db7f9e', '간판', B(0, 4, 128, 40, '', erase='alpha'), B(0, 42, 128, 76, '', erase='alpha'),
  B(4, 6, 124, 40, '만푸쿠켄', font='heavy', fit='box', color=(20, 20, 20)), B(4, 42, 124, 76, '나가이 흥업', font='gothic', fit='box'))
S('76f7b04fbe01', '간판', B(22, 24, 52, 110, '나가이흥업', v=True, font='brush'), B(86, 24, 116, 110, '나가이흥업', v=True, font='brush'))
S('5459686e863c', '간판', B(2, 22, 56, 41, '', erase='alpha'), B(2, 43, 56, 61, '', erase='alpha'),
  B(2, 22, 56, 41, '사이토', fit='box', color=(110, 20, 70)), B(2, 43, 56, 61, '교통', fit='box', color=(110, 20, 70)))
def _uranai(id_, ys):
    a, b, c, d, e, f = ys
    S(id_, '간판', B(0, a[0], 128, a[1], '', erase='alpha'), B(0, b[0], 128, b[1], '', erase='alpha'), B(0, c[0], 128, c[1], '', erase='alpha'),
      B(0, d[0], 128, d[1], '', erase='alpha'), B(0, e[0], 82, e[1], '', erase='alpha'), B(0, f[0], 82, f[1], '', erase='alpha'),
      B(0, a[0], 128, a[1], '점술의 집', font='heavy', fit='box', color=(40, 40, 40)),
      B(0, b[0], 128, b[1], '라피스', font='heavy', fit='box', color=(150, 50, 40)),
      B(0, c[0], 128, c[1], '당신의 고민을 풀어 드립니다', font='gothic', fit='box', color=(110, 90, 40)),
      B(0, d[0], 128, d[1], '행복해집시다!', font='gothic', fit='box', color=(200, 160, 60)),
      B(0, e[0], 82, e[1], '당신의 미래를', font='gothic', fit='box', color=(150, 150, 150), align='l'),
      B(0, f[0], 82, f[1], '점쳐 드립니다', font='gothic', fit='box', color=(150, 150, 150), align='l'))
_uranai('b1c8fa2c8083', [(2, 28), (30, 58), (60, 76), (78, 92), (92, 107), (107, 123)])
_uranai('34a10b6d7678', [(4, 27), (28, 56), (60, 76), (77, 93), (94, 109), (109, 124)])
S('d0dcf0db6031', '간판', B(20, 30, 236, 90, '', erase='alpha'), B(20, 100, 236, 160, '', erase='alpha'), B(20, 170, 236, 232, '', erase='alpha'),
  B(36, 40, 220, 80, '행운의 열쇠', font='mincho', fit='box', color=(235, 210, 150), stroke=((70, 35, 80), 1)),
  B(36, 110, 220, 150, '운명의 실', font='mincho', fit='box', color=(235, 210, 150), stroke=((70, 35, 80), 1)),
  B(36, 180, 220, 222, '승리의 문', font='mincho', fit='box', color=(235, 210, 150), stroke=((70, 35, 80), 1)))
S('cc5f0d2a20b6', '간판', B(0, 0, 44, 128, '', erase='alpha'), B(2, 2, 42, 126, '타카라초밥', v=True, font='brush', fit='box', color=(10, 10, 10)),
  B(95, 63, 128, 128, '혼자서도\n놀 수 있어요', v=True, font='gothic', spacing=0.02, erase='box', color=(30, 25, 20)))
S('09da441ef240', '간판', B(0, 0, 46, 128, '', erase='alpha'), B(2, 2, 44, 126, '타카라초밥', v=True, font='brush', fit='box', color=(10, 10, 10)),
  B(94, 63, 128, 128, '혼자서도\n놀 수 있어요', v=True, font='gothic', spacing=0.02, erase='box', color=(30, 25, 20)))
S('c79502b9a2be', '간판', B(12, 74, 120, 118, '', erase='auto', grow=1), B(14, 76, 118, 116, '남은 코인은,\n카운터에서\n맡아 드립니다', font='gothic', fit='box', erase='none', color=(170, 165, 150)))
S('2d6a484d8b13', '간판', B(14, 6, 48, 58, '보험조제', v=True, font='gothic'), B(14, 66, 31, 127, '처방전접수', v=True, font='gothic'),
  B(33, 66, 47, 114, '있음', v=True, font='gothic'), B(47, 66, 60, 124, '일용잡화', v=True, font='gothic'),
  B(96, 3, 121, 122, '한방이니까', v=True, font='brush'), B(70, 6, 90, 56, '잘들어', v=True, font='brush'))
S('f1e17fb6cca9', '간판', B(4, 10, 126, 50, '핫토리 스포츠', font='gothic'), B(36, 66, 108, 89, '월정액', font='heavy'),
  B(4, 89, 124, 107, '혼마치 유료 주차장', font='heavy', erase='box', color=(25, 20, 15)), B(4, 106, 124, 125, '', erase='dark', delta=35, grow=1), B(10, 108, 118, 123, '무단 주차 금지!', font='gothic', erase='none', fit='box', color=(40, 35, 30)))
S('1cde6d9015ff', '간판', B(3, 20, 62, 47, '핫토리 스포츠', font='gothic'))
S('8f92d05f3c73', '간판', B(10, 5, 120, 21, '', erase='alpha'), B(10, 22, 120, 54, '', erase='alpha'),
  B(20, 5, 108, 21, '플라워 센터', font='heavy', fit='box'), B(24, 22, 104, 54, '아이다', font='heavy', fit='box'))
S('38bf6e6abf3e', '간판', B(6, 5, 116, 21, '', erase='alpha'), B(8, 22, 112, 54, '', erase='alpha'),
  B(20, 5, 108, 21, '플라워 센터', font='heavy', fit='box'), B(24, 22, 104, 54, '아이다', font='heavy', fit='box'))
S('61a14eab5e1f', '간판', B(0, 0, 128, 30, '', erase='alpha'), B(0, 30, 128, 48, '', erase='alpha'),
  B(2, 1, 126, 29, '류 이발소', font='heavy', fit='box'), B(2, 31, 126, 47, '커트&파마', font='heavy', fit='box'),
  B(2, 90, 126, 122, '류 이발소', font='heavy', flip='v'))
for _k, _y in (('e728bf825e8d', (20, 48)), ('0c0f71e9e4f9', (24, 54)), ('49e3f97dba9e', (24, 54))):
    S(_k, '간판', B(0, _y[0] - 8, 128, _y[1] + 4, '', erase='alpha'), B(0, _y[0], 128, _y[1], '신요코스카 명화극장', font='gothic', fit='box'))
S('e5856ddc7824', '간판', B(6, 18, 124, 52, '아시아 여행사', font='gothic'))
# 항만식당(진한 색)·항만휴게소(밝은 색) — 원문처럼 3×3 칸에 한 글자씩, 모든 글자 같은 크기
_hc = [(4, 42), (45, 83), (86, 124)]; _hr = [(5, 43), (46, 84), (87, 125)]
_dark, _light = (40, 40, 40), (175, 175, 175)
S('a2a5cae59721', '간판', B(0, 0, 128, 128, '', erase='alpha'),
  *[B(_hc[c][0], _hr[r][0], _hc[c][1], _hr[r][1], ch, font='gothic', fit='box', color=col)
    for (r, c, ch, col) in ((0, 0, '항', _dark), (0, 1, '만', _dark), (0, 2, '식', _dark), (1, 0, '당', _dark),
                            (1, 1, '항', _light), (1, 2, '만', _light), (2, 0, '휴', _light), (2, 1, '게', _light), (2, 2, '소', _light))])
S('aea1e577c8c5', '간판', B(2, 4, 126, 42, '', erase='alpha'), B(2, 42, 126, 73, '', erase='alpha'),
  B(2, 4, 126, 42, '노구치 공무점', font='gothic', fit='box', color=(0, 0, 0)), B(14, 42, 120, 73, '운송 코조', font='gothic', fit='box', color=(0, 0, 0)))
S('7e3de3a4e0cb', '간판', B(4, 8, 124, 26, '', erase='alpha'), B(2, 26, 126, 58, '', erase='alpha'),
  B(10, 8, 120, 26, '와펜·자수', font='heavy', fit='box'), B(4, 27, 124, 57, '마리 상회', font='heavy', fit='box'))
S('d4e11161bf53', '간판', B(4, 8, 116, 26, '', erase='alpha'), B(2, 26, 120, 60, '', erase='alpha'),
  B(10, 8, 110, 26, '와펜·자수', font='heavy', fit='box'), B(4, 28, 118, 58, '마리 상회', font='heavy', fit='box'))
S('0d999ba9f27c', '간판', B(30, 34, 114, 68, '린다', font='heavy', erase='box', color=(215, 110, 70)), B(30, 94, 114, 126, '린다', font='heavy', erase='box', color=(160, 90, 70)))
S('0a0e2d83cc8e', '간판', B(0, 0, 64, 64, '', erase='alpha'), B(2, 6, 62, 32, '호쿠호쿠', font='heavy', fit='box'), B(10, 36, 54, 60, '도시락', font='heavy', fit='box'))
S('448a9ba5bdf1', '간판', B(0, 0, 128, 128, '', erase='alpha'), B(4, 4, 124, 28, '호쿠호쿠', font='heavy', fit='box'),
  B(30, 30, 110, 52, '도시락', font='heavy', fit='box'), B(2, 60, 126, 126, '영업시간', font='gothic', fit='box'))
S('b276d6492eea', '간판', B(0, 0, 128, 128, '', erase='alpha'), B(6, 10, 126, 70, '우오키치', font='brush', fit='box', color=(10, 10, 10)),
  B(6, 76, 126, 126, '생선가게', font='brush', fit='box', color=(10, 10, 10)))
S('969c07346c25', '간판', B(58, 14, 125, 42, '담배·과자', font='gothic', erase='box', color=(30, 30, 30)), B(60, 58, 126, 126, '아베 상점', font='heavy', erase='box', color=(15, 15, 15)))
for _k in ('3cb333152296', '3943833e9b0c'):
    S(_k, '간판', B(4, 2, 62, 18, '영업시간', font='pen'), B(3, 19, 64, 34, '오전 9시부터', font='pen'),
      B(3, 34, 64, 49, '오후 7시까지', font='pen'), B(26, 47, 64, 64, '아베 상점', font='pen', erase='dark', delta=35, grow=1, fit='box', color=(40, 35, 30)))
S('c58f2585e183', '간판', B(2, 35, 64, 58, '세가 건설', font='heavy', stroke=((235, 210, 60), 1)))
S('ba76b275b913', '간판', B(0, 0, 64, 64, '', erase='alpha'), B(2, 6, 62, 34, '데조리스', font='heavy', fit='box'), B(10, 36, 56, 62, '제빙', font='heavy', fit='box'))
for _k in ('baf2a5dbdfc3', '041b7ccfab76'):
    S(_k, '간판', B(0, 0, 128, 128, '', erase='alpha'), B(2, 2, 126, 62, '알파', font='heavy', fit='box'), B(2, 66, 126, 126, '무역', font='heavy', fit='box'))
S('857b131b3858', '간판', B(20, 94, 122, 124, '세계 여행사', font='gothic'))
for _k, _c in (('7bb95dfb07ba', (250, 250, 250)), ('f922c3f64423', (200, 150, 190))):
    S(_k, '간판', B(0, 96, 58, 128, '', erase='alpha'), B(72, 96, 128, 128, '', erase='alpha'),
      B(2, 98, 54, 127, '혼다', font='gothic', fit='box', color=_c), B(74, 98, 127, 127, '약국', font='gothic', fit='box', color=_c))
S('e9de3449a894', '간판', B(6, 104, 74, 122, '이용원 마에다', font='heavy', erase='dark', delta=50, grow=1, fit='box', color=(20, 20, 20)))
S('9b3d6181fb67', '간판', B(0, 0, 80, 128, '', erase='alpha'), B(2, 4, 78, 124, '골동\n문화당', v=True, font='heavy', fit='box', color=(10, 10, 10)))
S('190f4517a9ae', '간판', B(14, 22, 52, 56, '', erase='auto', grow=1), B(17, 24, 48, 54, '구룡', font='gothic', fit='box', erase='none', color=(235, 235, 235)))
for _k in ('dfa17865c7b7', 'b5805ebbded8'):
    S(_k, '간판', B(32, 70, 76, 86, '소바집', font='heavy'), B(78, 70, 120, 86, '야마지', font='heavy'))
S('e441e993daf5', '간판', B(102, 4, 127, 100, '소바집', v=True, font='brush', erase='dark', delta=60, grow=1, fit='box', color=(20, 20, 20)), B(68, 24, 100, 124, '야마지', v=True, font='brush', erase='dark', delta=60, grow=1, fit='box', color=(20, 20, 20)))
S('c9a5fdbbeca6', '간판', B(2, 2, 31, 62, '야마지', v=True, font='brush', erase='dark', delta=60, grow=1, fit='box', color=(25, 25, 25)))
S('d8aad98033ba', '간판', B(0, 0, 64, 64, '', erase='alpha'), B(38, 0, 64, 64, '스즈메', v=True, font='brush', fit='box', color=(20, 20, 20)),
  B(2, 12, 34, 60, '공원', v=True, font='brush', fit='box', color=(20, 20, 20)))
# 글자판(시간 표시 조각) — 누운 글자 낱자마다 원래 칸에(270° = 시계 방향 90°)
S('a4ffdf3519ff', '간판', B(0, 0, 80, 24, '', erase='alpha'), B(2, 1, 80, 23, '영업시간', font='gothic', fit='box', color=(255, 255, 255)),
  *[x for ch, box in (('오', (72, 62, 94, 84)), ('전', (72, 84, 94, 105)), ('후', (72, 105, 94, 126)),
                      ('개', (102, 62, 124, 83)), ('폐', (102, 83, 124, 105)), ('점', (102, 105, 124, 126)))
    for x in (B(*box, '', erase='alpha'), B(*box, ch, font='gothic', fit='box', rot=270, color=(255, 255, 255)))])
# ───────── 표지판 ─────────
S('2d0361ce81a5', '표지판', B(4, 6, 60, 31, '화장실', font='gothic'), B(4, 35, 60, 60, '사무실', font='gothic'))
S('e4a6d904f05b', '표지판', B(6, 6, 126, 58, '직원 외', font='gothic', erase='dark', delta=50, grow=1, color=(110, 40, 40)), B(6, 66, 126, 122, '출입 금지', font='gothic', erase='dark', delta=50, grow=1, color=(110, 40, 40)))
S('1c51625af2de', '표지판', B(6, 93, 122, 121, '창고 내 금연', font='gothic', erase='dark', delta=40, grow=1, color=(110, 40, 50)))
S('52e8f9ccc3b1', '표지판', B(3, 46, 61, 61, '창고 내 금연', font='gothic', erase='dark', delta=40, grow=1, color=(110, 40, 50)))
S('6d0390599039', '표지판', B(8, 12, 120, 58, '화기엄금', font='gothic', erase='box', color=(225, 190, 160)))
S('4e494fad44b8', '표지판', B(8, 12, 120, 58, '화기엄금', font='gothic', erase='box', color=(225, 190, 160)))
S('07700458a1b2', '표지판', B(4, 3, 62, 15, '안전제일', font='heavy', erase='dark', delta=40, grow=1, fit='box', color=(30, 30, 30)), B(48, 16, 126, 33, '지적 확인', font='heavy', erase='dark', delta=40, grow=1, fit='box', color=(30, 30, 30)))
S('aa8204e35492', '표지판', B(28, 24, 74, 122, '', erase='dark', delta=40, grow=1), B(66, 2, 126, 38, '', erase='auto', grow=1), B(38, 26, 72, 118, '전원참가로', v=True, font='heavy', erase='dark', delta=40, grow=1, fit='box', color=(40, 30, 15)), B(5, 52, 32, 124, '지적호칭', v=True, font='heavy', erase='dark', delta=40, grow=1, fit='box', color=(40, 30, 15)), B(80, 6, 124, 34, '머리\n조심!!', font='heavy', erase='auto', grow=1, fit='box', color=(240, 230, 210)))
S('2f0219ca0eae', '표지판', B(6, 4, 124, 15, '계약차 외 무단 출입 금지', font='gothic', erase='dark', delta=40, grow=1, fit='box', color=(70, 40, 40)), B(4, 72, 38, 120, '주차\n금지', font='heavy', erase='dark', delta=40, grow=1, fit='box', color=(170, 30, 40)), B(46, 66, 62, 114, '계약차외', v=True, font='heavy', erase='dark', delta=40, grow=1, fit='box', color=(40, 50, 120)), B(110, 60, 126, 124, '계약차외의', v=True, font='gothic', erase='dark', delta=40, grow=1, fit='box', color=(130, 40, 50)), B(90, 62, 108, 124, '주차를엄금합', v=True, font='gothic', erase='dark', delta=40, grow=1, fit='box', color=(130, 40, 50)), B(76, 62, 90, 84, '니다', v=True, font='gothic', erase='dark', delta=40, grow=1, fit='box', color=(130, 40, 50)))
for _k in ('b4b8d2f0771d', '219095552e00'):
    S(_k, '표지판', B(3, 38, 62, 50, '비상 출입구', font='heavy'), B(3, 50, 62, 61, '주차 금지', font='heavy'))
S('efb53edc7e98', '표지판', B(4, 50, 126, 110, '이 부근에서 서서 잡담,\n주저앉기, 음식 섭취 등을\n하지 않도록 부탁드립니다.', font='gothic', erase='box', color=(110, 125, 165)))
S('b7fc60e7b490', '표지판', B(86, 2, 127, 21, '경고', font='heavy'), B(4, 42, 126, 60, '허가받은 사람만 출입 가능', font='heavy', erase='box', color=(70, 30, 30)),
  B(46, 78, 124, 106, '버추어 파이터', font='heavy'))
for _k in ('5b206201ade8', '2d6760fcc398'):
    S(_k, '표지판', B(58, 80, 120, 118, '', erase='dark', delta=50, grow=2), B(64, 86, 110, 112, '금연', font='heavy', erase='none', fit='box', color=(125, 45, 55)))
S('da3a9c03e415', '표지판', B(64, 97, 94, 127, '', erase='dark', delta=45, grow=1), B(66, 99, 92, 111, '입구', font='heavy', erase='none', fit='box', color=(25, 25, 25)), B(66, 114, 92, 126, '출구', font='heavy', erase='none', fit='box', color=(25, 25, 25)), B(13, 46, 53, 60, '', erase='dark', delta=50, grow=1), B(15, 48, 51, 58, '임항순환', font='heavy', erase='none', fit='box', color=(40, 40, 40)))
S('8ab52b9979e0', '표지판', B(6, 28, 62, 44, '자외선 소독', font='gothic', erase='box', color=(190, 160, 210)))
S('68caaf7d0af1', '표지판', B(11, 6, 53, 123, '', erase='light', delta=60, grow=2), B(14, 8, 50, 121, '야간누름버튼식', v=True, font='gothic', erase='none', fit='box', color=(235, 240, 250)))
# ───────── 현수막(위·아래 두 쪽이 한 현수막) ─────────
S('4afa23f05d6f', '현수막', B(16, 18, 124, 52, '요코스카', font='gothic'), B(4, 76, 112, 116, '감사 세일', font='gothic'))
S('e3503631680d', '현수막', B(16, 18, 128, 52, '요코스카', font='gothic'), B(2, 76, 112, 116, '연말 세일', font='gothic'))
S('6c68aa6566a6', '현수막', B(10, 20, 98, 56, '요코스카', font='gothic'), B(33, 82, 116, 116, '', erase='dark', delta=50, grow=1), B(42, 84, 110, 114, '세일', font='gothic', erase='none', fit='box', color=(45, 45, 45)))
S('3f0c251565e7', '현수막', B(10, 20, 98, 56, '요코스카', font='gothic'), B(33, 82, 116, 116, '', erase='dark', delta=50, grow=1), B(42, 84, 110, 114, '세일', font='gothic', erase='none', fit='box', color=(45, 45, 45)))
S('0e18e6bf04ed', '현수막', B(0, 6, 128, 64, '', erase='light', delta=50, grow=2), B(14, 8, 128, 62, '신춘 대', font='heavy', erase='none', color=(230, 215, 215), fit='box'),
  B(0, 64, 128, 126, '', erase='light', delta=50, grow=2), B(0, 66, 120, 124, '바겐세일', font='heavy', erase='none', color=(230, 215, 215), fit='box'))
# ───────── 표지판(길 안내·정류장) ─────────
S('541d1488fd9d', '표지판', B(6, 6, 106, 41, '', erase='light', delta=35, grow=2), B(6, 66, 106, 102, '', erase='light', delta=35, grow=2), B(12, 10, 98, 36, '야마노세', font='gothic', erase='none', fit='box', color=(225, 230, 235)), B(12, 71, 98, 97, '도부이타', font='gothic', erase='none', fit='box', color=(225, 230, 235)))
S('8220040a0b9d', '표지판', B(10, 62, 126, 106, '', erase='alpha'), B(12, 64, 124, 104, '사쿠라가오카', font='gothic', fit='box', color=(255, 255, 255)))
S('1545f64f9529', '표지판', B(28, 15, 46, 32, '요코', font='gothic', erase='light', delta=50, grow=1, fit='ink', color=(225, 230, 240)), B(72, 15, 104, 32, '계통', font='gothic', erase='light', delta=50, grow=1, fit='ink', color=(225, 230, 240)), B(12, 45, 110, 69, '혼마치 1초메', font='gothic', erase='dark', delta=50, grow=1, fit='ink', color=(30, 30, 30)), B(20, 74, 106, 93, '다음은 시오이리역 앞', font='gothic', erase='dark', delta=50, grow=1, fit='ink', color=(30, 30, 30)), B(28, 95, 60, 120, '임해', font='gothic', erase='dark', delta=50, grow=1, fit='ink', color=(40, 40, 40)), B(68, 95, 100, 120, '순환', font='gothic', erase='dark', delta=50, grow=1, fit='ink', color=(40, 40, 40)))
S('abc53e1538c7', '표지판', B(15, 7, 22, 15, '요코', font='gothic', erase='light', delta=50, grow=1, fit='ink', color=(225, 230, 240)), B(36, 7, 49, 15, '계통', font='gothic', erase='light', delta=50, grow=1, fit='ink', color=(225, 230, 240)), B(10, 22, 53, 35, '', erase='dark', delta=35, grow=1), B(10, 24, 50, 33, '아미하마미나토초', font='gothic', erase='none', fit='box', color=(20, 20, 20)), B(7, 39, 57, 49, '', erase='dark', delta=40, grow=1), B(7, 40, 57, 48, '다음은 아미하마 4초메', font='gothic', erase='none', fit='box', color=(20, 20, 20)), B(13, 50, 29, 61, '임해', font='gothic', erase='dark', delta=50, grow=1, fit='ink', color=(40, 40, 40)), B(35, 50, 51, 61, '순환', font='gothic', erase='dark', delta=50, grow=1, fit='ink', color=(40, 40, 40)))
def _tt(id_, title, co):
    # 낱말마다 원문 잉크 범위(erase='dark' → fit='ink') 안에만 — 표 선을 넘지 않게 칸 안쪽 상자
    W = dict(erase='dark', delta=60, grow=1, fit='ink', font='mincho', color=(45, 40, 35))
    S(id_, '안내판', B(*title, '임항순환버스', **W), B(*co, '요코스카 교통', **W),
      B(4, 58, 22, 76, '시', **W), B(30, 58, 96, 76, '평일', **W),
      B(106, 58, 172, 76, '토요일', **W), B(180, 58, 250, 76, '일요일·공휴일', **W))
_tt('75d8b2385077', (8, 20, 134, 46), (142, 20, 250, 46))
_tt('9a6e2b6ee255', (24, 18, 154, 46), (158, 24, 234, 44))
for _k in ('5655b56d6cbb', '103c26d582b4'):
    S(_k, '안내판', B(8, 218, 248, 238, '도로 정체로 예정대로 운행하지 못할 수 있으니 양해 바랍니다.', font='gothic', erase='dark', delta=50, grow=1, fit='ink', color=(50, 45, 40)))
# 아미하마초 안내판 글자판(낱말마다 따로 잘라 씀) — 낱말 영역마다 원문 잉크 범위를 재서 그 안에만, 색은 원문 글자 색
_AMI = [((4, 2, 164, 50), '아미하마초', 'mincho'), ((186, 10, 252, 34), '현재 위치', 'gothic'),
        ((2, 50, 206, 92), '신요코스카항', 'mincho'), ((2, 92, 132, 112), '미군기지 시설', 'gothic'),
        ((156, 92, 224, 112), '주차장', 'gothic'), ((2, 113, 88, 134), '중앙 부두', 'gothic'),
        ((128, 113, 214, 134), '아미하마 부두', 'gothic'), ((2, 135, 88, 158), '카노 물산', 'gothic'),
        ((88, 135, 140, 158), '(주)', 'gothic'), ((140, 135, 246, 158), '알파 무역', 'gothic')]
def _ami(id_, extra):
    its = []
    for box, t, f in _AMI + extra:
        its.append(B(*box, t, font=f, erase='alpha', fit='ink', spacing=0.02, amul=True, **({'v': True} if t == '식당' else {})))
    S(id_, '안내판', *its)
_ami('ecb187f748b6', [((222, 80, 254, 134), '식당', 'gothic'), ((120, 222, 256, 256), '항만 휴게소', 'mincho')])
_ami('263ffea1f5ee', [])
# ───────── 지도 ─────────
_sk = [((110, 24, 224, 75), '사쿠라가오카', {}), ((256, 34, 287, 68), '이와타', {}), ((77, 108, 121, 141), '스미야', {}),
       ((138, 127, 175, 159), '타카시마', {}), ((193, 150, 211, 178), '류', {}), ((258, 124, 287, 145), '노무라', {}),
       ((314, 100, 387, 120), '사쿠라가오카 공원', {}), ((254, 187, 288, 208), '야마모토', {}), ((83, 224, 106, 248), '타치\n바나', {}),
       ((132, 229, 170, 255), '스기사와', {}), ((217, 214, 238, 271), '타카하시', dict(v=True)), ((254, 224, 288, 250), '미츠이', {}),
       ((250, 271, 288, 297), '아카사카', {}), ((316, 249, 350, 271), '곤도', {}), ((356, 249, 388, 271), '히라노', {}),
       ((314, 304, 363, 334), '아베 상점', {}), ((332, 352, 351, 378), '류', {}), ((350, 397, 387, 420), '니시다', {}),
       ((290, 450, 326, 471), '야마기시', {}), ((222, 338, 240, 392), '미시마', dict(v=True)), ((252, 338, 289, 371), '타지마', {}),
       ((252, 378, 289, 406), '이토', {}), ((140, 348, 190, 420), '하이츠\n사쿠라', {}),
       ((409, 10, 429, 150), '도부이타거리방면', dict(v=True)), ((96, 466, 161, 487), '야마노세 방면', {})]
def C(x, y, t, **kw):
    d = dict(cell=(x, y), t=t); d.update(kw); return d
# 사쿠라가오카 지도 — 칸 밖 제목·방면 표시는 글자 화소만 지우고, 집 이름은 칸 통째로(칸 색 한 가지 + 그 안에만 한글)
_SK_OUT = ('사쿠라가오카', '사쿠라가오카 공원', '도부이타거리방면', '야마노세 방면')
S('13064aa79400', '지도', *[B(*b, t, font='gothic', erase='dark', delta=45, grow=1, fit='box', color=(35, 30, 28), **kw) if t in _SK_OUT
                           else C((b[0] + b[2]) // 2, (b[1] + b[3]) // 2, t, color=(35, 30, 28), thr=150, net=1, line=120, maxa=12000, r=2, csize=16, upright=1, **kw) for b, t, kw in _sk])
# 도부이타 지도 — 이름표 칸마다 칸 안 한 점(칸 전체를 칸 색으로 칠하고 그 안에만 한글)
_db = [C(150, 298, '야마지'), C(223, 311, '공원'), C(214, 352, '타무라\n정육점'), C(266, 352, '데조리스'),
       C(234, 402, '코인'), C(166, 401, '이용원 마에다'), C(321, 427, '와펜\n마리 상회'), C(410, 200, '모치즈키\n장'),
       C(466, 299, '요코스카\n명화극장'), C(468, 370, '우오키치'),
       C(241, 185, '류 이발소'), C(131, 457, '스마일리'), C(43, 452, '히라타 상점'), C(362, 396, '쿠리타'), C(408, 395, '세계여행사')]
S('d3cbf24ec345', '지도', B(212, 44, 376, 82, '사쿠라가오카 방면', font='gothic', erase='dark', grow=2, fit='box', color=(25, 25, 25)),
  B(338, 430, 512, 500, '현재', font='heavy', erase='dark', grow=2, fit='box', color=(25, 25, 25)), *_db)
SPEC['72e9accd66d2'] = list(SPEC['d3cbf24ec345']); GROUP['72e9accd66d2'] = '지도'
# 도부이타 상점가 지도 오른쪽 절반(왼쪽 절반 «현재»와 이어짐 → «현재|지») — 비스듬한 이름표(오카야마 하이츠·만푸쿠켄·아지이치·혼다 약국·핫토리 스포츠·문화당 등)는 미처리
for _k in ('60998e4d41cc', '84d9a3b935d0'):
    S(_k, '지도', C(112, 231, '아이다'), C(112, 249, '타카라초밥'), C(181, 239, '야오카츠'), C(14, 254, '로시야'),
      B(175, 406, 417, 445, '도부이타', font='heavy', erase='dark', grow=2, fit='box', color=(25, 25, 25)),
      B(243, 452, 504, 495, '상점가', font='heavy', erase='dark', grow=2, fit='box', color=(25, 25, 25)),
      B(3, 440, 96, 500, '지', font='heavy', erase='dark', grow=2, fit='box', color=(25, 25, 25)),
      C(309, 92, '오카야마\n하이츠'), C(393, 83, '만푸쿠켄'), C(369, 145, '요코스카'), C(289, 228, '아지이치'),
      C(291, 285, '혼다\n약국'), C(337, 266, '핫토리\n스포츠'), C(94, 350, '문화당'), C(62, 360, '워터\n드래곤'))
S('eab812e33806', '지도', *[B(*b, t, font='heavy', erase='dark', fit='box', color=(25, 25, 25)) for b, t in (
    ((86, 101, 118, 113), '도부이타'), ((94, 113, 128, 125), '상점가'), ((42, 111, 77, 123), '현재지'))])
S('fa0f71786162', '지도', *[B(*b, t, font='heavy', erase='dark', fit='box', color=(25, 25, 25)) for b, t in (
    ((85, 101, 118, 112), '도부이타'), ((94, 113, 128, 125), '상점가'), ((43, 111, 76, 123), '현재지'), ((27, 11, 49, 19), '사쿠라가오카 방면'))])
S('9a45a6ba8c7a', '지도', *[B(*b, t, font='heavy', erase='dark', fit='box', color=(25, 25, 25)) for b, t in (
    ((42, 50, 59, 56), '도부이타'), ((46, 56, 64, 63), '상점가'), ((21, 54, 35, 61), '현재지'))])
# ───────── 스토리 소품 ─────────
def _cols(id_, cols, font='gaegu', color=(10, 5, 10)):
    S(id_, '스토리', B(0, 0, 128, 128, '', erase='alpha'), *[B(*b, t, v=True, font=font, fit='box', color=color) for b, t in cols])
_cols('3ceb43364698', [((102, 2, 126, 126), '용돈'), ((72, 2, 100, 126), '료에게'), ((42, 2, 70, 126), '제8창고'), ((6, 2, 36, 80), '자료')])
_cols('ecb5f3b042ea', [((102, 2, 126, 126), '용돈'), ((72, 2, 100, 126), '료에게'), ((42, 2, 70, 126), '제8창고'), ((6, 2, 36, 80), '자료')])
_cols('379509c682f5', [((102, 2, 126, 126), '구창고가'), ((74, 2, 100, 126), '제8창고'), ((44, 2, 70, 70), '귀중'), ((6, 2, 36, 112), '월급봉투')])
S('eeb3fb3074cb', '스토리', B(40, 46, 184, 82, '하즈키 이와오 님', font='brush', erase='dark', fit='box', color=(25, 25, 25)))
S('10e9c88c2a0c', '스토리', B(222 - 182, 46, 222, 82, '하즈키 이와오 선생님', font='brush', erase='dark', fit='box', color=(25, 25, 25)),
  B(166, 204, 216, 232, '주위안다', font='brush', erase='dark', fit='box', color=(25, 25, 25)))
S('ffe157643a1a', '스토리', B(146, 8, 232, 46, '할당 10개', font='pen', erase='dark', delta=30, fit='box', color=(200, 40, 40)))
S('738004877321', '스토리', B(2, 206, 96, 242, '할당 8개', font='pen', erase='dark', delta=30, fit='box', color=(200, 40, 40)))
S('50f3053f5651', '스토리', B(0, 0, 103, 27, '', erase='alpha'), B(0, 73, 128, 128, '', erase='alpha'),
  B(0, 1, 102, 26, '치바 히로타카', font='heavy', fit='box', color=(20, 0, 20)),
  B(0, 80, 128, 104, '신창고가', font='heavy', fit='box', color=(20, 0, 20)), B(0, 106, 128, 128, '경비 스케줄', font='heavy', fit='box', color=(20, 0, 20)))
S('2145c823556f', '스토리', B(0, 0, 128, 104, '', erase='alpha'), B(40, 103, 128, 128, '', erase='alpha'),
  B(2, 1, 126, 26, '종합계좌', font='gothic', fit='box', color=(190, 190, 190)), B(2, 28, 126, 52, '통장', font='gothic', fit='box', color=(190, 190, 190)),
  B(2, 54, 126, 72, '보통·정기 예금', font='gothic', fit='box', color=(190, 190, 190)), B(2, 74, 126, 102, '하즈키 료', font='gothic', fit='box', color=(205, 205, 205)),
  B(52, 106, 126, 127, '스미토모 은행', font='gothic', fit='box', color=(235, 235, 235)))
# 아미하마초 안내 지도(세 가지 판) — 비스듬한 부두 칸 이름은 미처리
def _ami2(k, base, park):
    S(k, '지도', B(176, 16, 228, 44, '아미하마초', font='mincho', erase='dark', fit='box', color=(40, 40, 40)),
      B(106, 78, 162, 98, '신요코스카항', font='mincho', erase='dark', delta=25, fit='box', color=(70, 80, 120)),
      B(*base[0], '미군기지 시설', font='gothic', erase='dark', delta=base[1], fit='box', color=base[2]),
      *[B(*b, '주차장', font='gothic', erase='dark', delta=25, fit='box', color=(40, 40, 40)) for b in park])
_ami2('41f4e6d80be7', ((28, 6, 82, 20), 20, (200, 80, 130)), [(46, 204, 64, 220), (70, 204, 90, 220)])
_ami2('2e63b6e2abc3', ((8, 4, 86, 20), 25, (40, 40, 40)), [(44, 212, 66, 228), (68, 212, 92, 228)])
_ami2('20574003fc67', ((12, 24, 64, 40), 20, (200, 80, 130)), [(46, 211, 67, 225)])
DERIVE = {'6bb3a2425c97': '13064aa79400'}     # 사쿠라가오카 지도 축소판
# 비전서 표지(기술 이름 = 대사 번역 그대로)
for _k, _t in (('bdd51a1bc542', '비연연예'), ('d3f763099aa3', '쌍인'), ('6f20482de85a', '호신붕'), ('1741a7c9f339', '땅거미')):
    S(_k, '스토리', B(106, 4, 126, 124, _t, v=True, font='brush', erase='dark', fit='box', color=(20, 20, 20)))
# 국도 16호 방향 표지 — 낱말마다 따로 잘라 붙이는 글자판(낱말 범위 = 원문 글자 칸 그대로, 넘지 않게)
_r16 = [((0, 0, 128, 32), '요코스카항'), ((128, 0, 256, 32), '미군기지'),
        ((0, 32, 64, 64), '나가우라'), ((64, 32, 128, 64), '요코하마'), ((128, 32, 160, 64), '역'), ((160, 32, 192, 64), '초'),
        ((0, 64, 64, 96), '혼초'), ((64, 64, 192, 96), '야마나카 도로'),
        ((0, 96, 128, 128), '히노데초'), ((128, 96, 192, 128), '헨미'),
        ((0, 128, 96, 160), '미도리가오카'), ((96, 128, 160, 160), '시오이리'),
        ((0, 160, 96, 192), '쿠리하마'), ((96, 160, 192, 192), '칸논자키')]
S('a912fe7907aa', '표지판', B(0, 0, 200, 192, '', erase='alpha'), B(192, 0, 256, 32, '', erase='alpha'),
  *[B(*b, t, font='gothic', erase='alpha', fit='ink', color=(255, 255, 255)) for b, t in _r16])
# 국도 16 표지: 낱말 글자 범위를 먼저 잰 뒤(위) 빈 곳에 남은 원문 획 정리 — 아래 _r16clean 에서

# 아버지 편지(세로쓰기, 오른쪽부터) — 둘째 편지는 음성 자막 번역(01LETB001~006) 그대로, 첫째는 새 번역
def _letter(id_, area, cols, w, y0, y1, font='gaegu', cell=None):
    items = [B(*area, '', erase='dark', delta=40, grow=1)]
    for cx, t in cols:
        items.append(B(int(cx - w / 2), y0 if not t.startswith('@') else y0 + 40, int(cx + w / 2), y1, t.lstrip('@'),
                       v=True, font=font, fit='box', align='l', color=(25, 25, 30), erase='none', spacing=0.02, cell=cell, gain=1.8))
    S(id_, '스토리', *items)
_letter('702d6d412594', (20, 20, 492, 500), [
    (451, '@료에게'), (398, '팔음팔양이란 음양의 변화를 나타낸 말이다.'), (353, '세상 모든 것에는 음과 양,'),
    (302, '즉 빛과 그림자가 존재한다.'), (261, '내가, 그리고 네가 배우는 권법에 비유하면'), (220, '그것은 공격과 수비에 해당한다.'),
    (170, '알겠느냐 료. 양인 공격과 음인'), (124, '방어를 극에 이르게 하라. 너라면 할 수 있다.'), (65, '무슨 일이 일어나더라도')], 36, 36, 494, cell=22)
_letter('c7416a33dbe2', (16, 10, 248, 246), [
    (233, '@료에게'), (204, '무술의 길을 걷는 자는'), (181, '자신의 신념을 완수하기 위해'), (158, '죽음도'),
    (138, '각오해야 한다.'), (112, '신념에 살고, 신념에 죽는다.'), (85, '그것이 내 삶의 방식이다.'),
    (58, '료, 너도 네 신념을 가슴에 품고'), (36, '길을 걸어라. 그리고 극에 이르러라.')], 19, 18, 244, cell=12)
# ───────── 비전서 낱장(세로쓰기 붓글씨, 오른쪽부터) — 열 위치는 원문 잉크로 찾음(scroll_cols.py), 글은 새 번역 ─────────
import sys as _sys, os as _os
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import scroll_cols as _C
def _scroll(id_, area, lines, font='brush2', bottoms=None):
    cs = _C.cols(id_, area)
    if bottoms: cs = [(a, b, c, max(d, bt)) for (a, b, c, d), bt in zip(cs, bottoms)]
    assert len(cs) == len(lines), (id_, len(cs), len(lines))
    pitch = min(c[1] - c[0] for c in cs) + 4
    items = [B(c[0] - 3, c[2] - 3, c[1] + 3, c[3] + 3, '', erase='dark', delta=55, grow=1) for c in cs]
    for (x0, x1, y0, y1), t in zip(cs, lines):
        cx = (x0 + x1) // 2; w = pitch
        items.append(B(cx - w // 2, y0, cx + w // 2 + 1, max(area[3], y1), t, v=True, font=font, fit='box', align='l',
                       color=(20, 15, 10), erase='none', spacing=0.0, cell=pitch + 1, gain=1.6))
    S(id_, '스토리', *items)
_scroll('7da8071b25d9', (240, 25, 490, 492), ['무의 경지에 이르는 것은', '주먹도 아니요 다리도 아니요, 오체를 쓰는 것이라',
        '어깨와 등을 써서 공격함 또한 무라', '허를 찔러 물러서고, 공격하며 나아가기를 두 번',
        '목치기로 들어가 어깨치기에 이르니', '그 격렬한 모습이 마치 범과 같다'])
_scroll('c50bf20ca0c2', (20, 15, 500, 335), bottoms=[302, 324, 348, 308, 138, 424, 476], lines=['쌍인은 실로 진전으로 전해진다', '물러서서 적을 속이기를 한 박자',
        '돌아서 간격을 좁히기를 두 박자', '상대의 목에 두 손날을 내리쳐', '숨을 끊는다', '숙달되면 한 손 한 칼로 베리라',
        '살리고 죽임이 자유자재하여 찰나에 생사를 쥐리라'])
_scroll('5a089d099614', (230, 15, 500, 375), bottoms=[380, 492, 478, 380, 380, 462, 380], lines=['붙잡아 제압하는 기술, 이를 몽롱이라 한다', '때에 따라 던지고 변화에 응해 관절을 꺾으라',
        '신법 또한 변화무쌍하여 적에게 다가서기를 한 박자', '물러서기를 두 박자로 붙잡으라', '숙달되어 묘리를 깨우치면',
        '그 기술은 흐르는 물처럼 멈출 수 없으니', '몽롱을 극한 자는 무쌍이 되리라'])
_scroll('8865590b10c6', (40, 30, 500, 300), bottoms=[300, 318, 300, 300, 300, 300, 318, 318], lines=['태조로부터 전해지는 권타라', '하지의 힘으로 오른손을 돌려', '주먹이 꿈틀거림은',
        '용이 승천하는 듯하다', '엎드려 땅에서 내뻗고', '뻗어 하늘을 꿰뚫는다', '발놀림은 물결과도 같아', '한 번 다가서고 두 번 물러서리'])
_scroll('5875172e8f79', (60, 25, 500, 290), bottoms=[305, 270, 230, 140, 230, 160, 230, 230, 300, 280], lines=['비연연예는 비전의 퇴법이라', '신법은 민첩함을 으뜸으로 삼으니', '첫째로 물러서서',
        '적을 꾀어내고', '둘째로 나아가', '적을 치리라', '오르는 발로 하늘을 찌르고', '내리는 발로 땅을 꿰뚫는다',
        '오르는 발에 일섬의 음양이 있어', '맞서는 자는 막기 어렵다'])
_scroll('9187fac4718b', (110, 20, 500, 275), bottoms=[300, 200, 200, 300, 220, 220, 300, 300, 220], lines=['땅거미는 허의 기법이라', '한 번 물러서', '기세를 흘리고',
        '두 번 나아가 몸을 엎드려', '내뻗은 다리로', '낭심을 치리라', '낮게 이르기는 쉬우나', '막힘없이 쳐 넣는 것',
        '이야말로 긴요하다'])
_scroll('aa4e6a8bd81a', (60, 15, 500, 290), bottoms=[300, 200, 240, 290, 200, 240, 150, 290, 405], lines=['그림자사냥은 하지의 기법이라.', '태조로부터 전해진다.', '촌보로 자세를 낮추고',
        '나아가 공격하니 그 움직임이', '질풍과 같다.', '발날로 정강이를 베고', '무릎을 벤다.', '한 번 번뜩이면',
        '땅에 떨어지는 적의 그림자를 사냥하는 듯하다.'])
_scroll('a303c07dcce2', (50, 20, 500, 300), bottoms=[310, 325, 240, 310, 280, 320, 200, 325], lines=['선풍은 다리 후리기 기술이라', '신법은 나아감과 물러남을 쓰고', '자세를 낮추어 몸을 돌려',
        '좌우 발뒤꿈치로 쓸기를 단숨에', '적의 다리를 봉하는 것이라', '도는 것이 팽이와 같고', '몸은 기울지 않으며',
        '움직임을 옮겨 다리를 죽이는 것이라'])
# ───────── 지도 기울어진 이름표(색칸) — 칸 안 한 점(seed) → 같은 색 영역·각도 자동, 칸 밖으로 안 나감 ─────────
def R(x, y, t, **kw):
    d = dict(seed=(x, y), t=t); d.update(kw); return d
_dbslant = [R(0, 0, '류 이발소', poly=[(203, 189), (268, 163), (280, 182), (212, 206)]),
            R(0, 0, '스마일리', poly=[(106, 456), (117, 442), (156, 457), (144, 471)]),
            R(0, 0, '히라타 상점', poly=[(12, 450), (24, 434), (75, 456), (63, 471)]),
            R(0, 0, '쿠리타', poly=[(344, 392), (372, 380), (384, 398), (352, 411)]),
            R(0, 0, '세계여행사', poly=[(386, 372), (436, 404), (410, 420), (380, 392)], ang=52, tsize=(50, 18))]
# 도부이타 상점가 지도(오른쪽 판) 기울어진 이름표 — 네 모서리 실측
_shslant = [R(0, 0, '오카야마 하이츠', poly=[(254, 90), (300, 54), (364, 96), (318, 128)], ang=30, tsize=(80, 22), shrink=1),
            R(0, 0, '만푸쿠켄', poly=[(369, 95), (393, 57), (416, 72), (393, 109)], ang=-57, tsize=(44, 18), shrink=1),
            R(0, 0, '요코스카', poly=[(344, 140), (362, 126), (394, 152), (374, 164)], ang=40, tsize=(38, 14)),
            R(0, 0, '아지이치', poly=[(262, 224), (284, 206), (316, 234), (296, 250)], ang=40, tsize=(40, 16)),
            R(0, 0, '혼다\n약국', poly=[(262, 268), (298, 262), (322, 296), (276, 306)], ang=-12, tsize=(34, 30)),
            R(0, 0, '핫토리\n스포츠', poly=[(302, 262), (350, 240), (372, 268), (322, 292)], ang=-25, tsize=(48, 28)),
            R(0, 0, '문화당', poly=[(70, 340), (95, 328), (117, 360), (90, 370)], ang=54, tsize=(36, 22), shrink=0, bg=(255, 198, 148)),
            R(0, 0, '워터\n드래곤', poly=[(43, 353), (65, 343), (84, 370), (55, 375)], ang=54, tsize=(30, 22), shrink=1, bg=(255, 186, 189))]
# 아미하마초 안내 지도 부두 이름(분홍 작은 글자, 부두 방향으로 기울어짐)
_amipier = [B(118, 126, 152, 176, '', erase='ink', ink=(200, 110, 150), tol=60, grow=1),
            B(158, 126, 194, 168, '', erase='ink', ink=(200, 110, 150), tol=60, grow=1),
            B(84, 156, 122, 172, '', erase='ink', ink=(200, 110, 150), tol=60, grow=1),
            B(120, 128, 152, 174, '중앙 부두', font='gothic', erase='none', rot=55, tsize=(44, 8), color=(205, 95, 140)),
            B(160, 128, 194, 166, '아미하마 부두', font='gothic', erase='none', rot=55, tsize=(44, 8), color=(205, 95, 140)),
            B(86, 158, 120, 170, '항만 휴게소', font='gothic', erase='none', fit='box', color=(205, 95, 140))]
for _k in ('41f4e6d80be7', '2e63b6e2abc3'):
    SPEC[_k] = SPEC[_k] + _amipier
SPEC['20574003fc67'] = SPEC['20574003fc67'] + [
    B(124, 120, 158, 160, '', erase='ink', ink=(200, 110, 150), tol=60, grow=1),
    B(162, 120, 190, 160, '', erase='ink', ink=(200, 110, 150), tol=60, grow=1),
    B(124, 122, 158, 158, '중앙 부두', font='gothic', erase='none', rot=55, tsize=(40, 8), color=(205, 95, 140)),
    B(162, 120, 190, 158, '아미하마 부두', font='gothic', erase='none', rot=55, tsize=(40, 8), color=(205, 95, 140))]
# 사본 판(칸 배치가 원본과 조금 다름): 칸 이름표는 원본 판에서 칸 모양을 찾아 짚는 점을 옮김
def _copy(src, dst):
    SPEC[dst] = [dict(it, **{'from': src}) if isinstance(it.get('cell'), tuple) else it for it in SPEC[src]]
_copy('d3cbf24ec345', '72e9accd66d2'); _copy('60998e4d41cc', '84d9a3b935d0')
SPEC['84d9a3b935d0'] = [dict(cell=(272, 292), t=it['t']) if it.get('t') == '혼다\n약국' else it for it in SPEC['84d9a3b935d0']]

# 보충(2026-11-05) — OCR 이 놓친 문패·간판·표지판·스토리 소품 → spec_ko_sup.py
import os as _os
exec(open(_os.path.join(_os.path.dirname(__file__), "spec_ko_sup.py"), encoding="utf-8").read())
exec(open(_os.path.join(_os.path.dirname(__file__), "spec_ko_sup3.py"), encoding="utf-8").read())
