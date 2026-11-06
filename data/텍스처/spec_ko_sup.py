# -*- coding: utf-8 -*-
# 보충(2026-11-05) — OCR 이 놓친 문패·간판·표지판·스토리 소품. spec_ko.py 끝에서 exec 로 읽음(S·B·SPEC·GROUP 공유).
# 이름 읽기는 대사 번역과 같게, 거센소리 규칙. vsize = 원문처럼 한쪽으로 늘린 글자(그 비율로 그린 뒤 상자에 맞춰 늘림)
def N(id_, name, box, mode='dark', **kw):
    S(id_, '보충문패', B(*box, name, font=kw.pop('font', 'gothic'), erase=mode, **kw))
for _id, _nm, _bx, _md, _kw in [
    ('fcb292ff9ea8', '미시마', (8, 8, 60, 58), 'dark', {}), ('6087a12114e1', '류', (2, 10, 62, 54), 'dark', {}),
    ('7202f4cc57d8', '하즈키', (10, 9, 60, 30), 'dark', dict(delta=35)), ('c800bc799c08', '히라노', (6, 8, 60, 56), 'dark', {}),
    ('2b9e98acc998', '타카\n하시', (5, 6, 60, 58), 'dark', {}), ('6bf941d3e829', '나카\n무라', (6, 5, 58, 59), 'light', dict(delta=50)),
    ('62672239471b', '스미야', (8, 8, 56, 56), 'dark', dict(delta=30)), ('bfbbd32a9a71', '스기\n사와', (6, 8, 58, 58), 'light', dict(delta=60)),
    ('811b42a77ffa', '미츠이', (6, 8, 58, 56), 'dark', {}), ('54f76c0bf2b1', '타카\n시마', (6, 6, 60, 58), 'dark', {}),
    ('749228ab3fe0', '사쿠\n라다', (6, 6, 60, 58), 'dark', {}), ('941c1e523491', '노무라', (6, 6, 60, 58), 'dark', {}),
    ('9fc0a7ef991c', '요시\n오카', (6, 4, 60, 60), 'dark', {}), ('1d272cd124c5', '야마\n모토', (6, 4, 60, 60), 'dark', dict(delta=40)),
    ('394694de0b87', '아오\n야마', (4, 6, 60, 58), 'dark', {}), ('537de05b2f3a', '우다\n가와', (4, 8, 62, 56), 'dark', {}),
    ('7b9c3623ee0f', '이토', (6, 6, 58, 58), 'light', dict(delta=50)), ('8815720aa7e8', '아이\n자와', (0, 4, 64, 64), 'dark', {}),
    ('d72158c8d5ef', '아카\n사카', (6, 4, 60, 60), 'dark', {}), ('cb6e6b48897b', '이토이', (6, 5, 58, 60), 'light', dict(delta=60)),
    ('209994407058', '키무라', (4, 6, 60, 56), 'dark', {}), ('a94710f3f51d', '이와타', (4, 6, 60, 56), 'dark', {}),
    ('768c3fe8eb79', '이노\n우에', (4, 2, 62, 56), 'dark', {}), ('999e92f23875', '시라이', (6, 6, 60, 58), 'dark', {}),
    ('f0c4f73a6378', '야마\n기시', (8, 4, 58, 60), 'dark', {}), ('05dde9868fe5', '아즈\n마야', (6, 6, 60, 60), 'dark', {}),
    ('325d9ed5593f', '후쿠\n하라', (10, 6, 58, 60), 'dark', dict(delta=30)), ('4caadc4b596b', '유키', (10, 8, 58, 58), 'dark', {}),
    ('46af07562d12', '유키', (50, 46, 82, 64), 'dark', {}), ('3078d2013d27', '류', (16, 10, 44, 56), 'dark', dict(delta=40)),
    ('09165d2fd487', '타치\n바나', (14, 10, 50, 58), 'light', dict(delta=45)),
    ('cea255b3e10c', '하즈키', (20, 8, 44, 58), 'dark', dict(delta=35, v=True))]:
    N(_id, _nm, _bx, _md, **_kw)
S('9e565de1a410', '보충문패', B(0, 0, 64, 64, '', erase='alpha'), B(1, 2, 63, 28, '메종', font='heavy', fit='box', color=(190, 185, 170)),
  B(1, 32, 63, 61, '이시카와', font='heavy', fit='box', color=(190, 185, 170)))
S('d660d08909a9', '보충문패', B(0, 0, 32, 32, '', erase='alpha'), B(1, 8, 31, 24, '하즈키', font='gothic', fit='box', color=(15, 10, 10)))
S('ed1da07b21a7', '보충문패', B(18, 10, 110, 112, '야마\n노세장', font='gothic', erase='dark', delta=40, fit='box', color=(30, 28, 25)))
S('bb0b09c53bd5', '보충문패', B(30, 26, 52, 106, '니시무라', font='gothic', erase='dark', delta=35, rot=270, fit='box', color=(15, 15, 15)),
  B(66, 0, 126, 128, '', erase='rowprof', cols=[66, 67, 68, 124, 125]),     # 8단 판 전체를 글자 없는 가장자리 명암으로 다시 칠함
  *[B(96 - 14 * len(_nm) // 2, _y0 + 1, 96 + 14 * len(_nm) // 2, _y1, _nm, font='gothic', erase='none', fit='box', spacing=0.02, gain=1.8, color=(0, 0, 0))   # 글자 크기 통일(판 안 가운데)
    for _y0, _y1, _nm in ((0, 15, '야마다'), (16, 32, '하라'), (33, 47, '나카타'), (48, 63, '히라노'), (64, 79, '미카미'), (80, 95, '마츠나가'), (96, 111, '야기'), (112, 127, '니노미야'))])

# ───── 간판 ─────
S('04ea1aa6ba8b', '보충간판', B(0, 0, 64, 64, '', erase='alpha'), B(10, 8, 54, 56, '야오카츠', font='gothic', fit='box', vsize=(44, 14), color=(70, 45, 65)))
S('d4d6d03763eb', '보충간판', B(0, 72, 128, 128, '', erase='alpha'), B(4, 80, 124, 122, '타카라초밥', font='brush', fit='box', color=(10, 10, 110)))
S('4128dac56411', '보충간판', B(0, 0, 64, 64, '', erase='alpha'), B(1, 2, 63, 30, '타카라', font='brush', fit='box', color=(235, 235, 235)), B(1, 34, 63, 62, '초밥', font='brush', fit='box', color=(235, 235, 235)))
S('8e0ff5ab1d69', '보충간판', B(0, 0, 128, 128, '', erase='alpha'), B(6, 10, 126, 70, '우오키치', font='brush', fit='box', color=(10, 10, 10)), B(6, 76, 126, 126, '생선가게', font='brush', fit='box', color=(30, 30, 30)))
for _k, _c, _s in (('371894199a4a', (240, 240, 240), (110, 110, 110)), ('7916aa4cd50e', (185, 185, 185), (45, 45, 45))):
    S(_k, '보충간판', B(0, 0, 128, 128, '', erase='alpha'), B(26, 2, 102, 34, '도자기', font='gothic', fit='box', color=_c, stroke=(_s, 1)),
      B(14, 37, 110, 70, '전문점', font='gothic', fit='box', color=_c, stroke=(_s, 1)), B(2, 78, 126, 124, '로시야', font='gothic', fit='box', color=_c, stroke=(_s, 1)))
S('fe793d4933a2', '보충간판', B(1, 1, 78, 24, '영업시간', font='gothic', fit='box', color=(15, 15, 15)),
  *[B(*_b, _t, font='gothic', fit='box', rot=270, color=(15, 15, 15)) for _b, _t in (((73, 61, 95, 84), '오'), ((73, 85, 95, 105), '전'), ((73, 106, 95, 126), '후'),
                                                                                     ((101, 61, 123, 83), '개'), ((101, 84, 123, 104), '폐'), ((101, 105, 123, 126), '점'))])
_up = (100, 65, 60); _lo = (35, 28, 22)
_e = dict(font='gothic', erase='dark', delta=35, grow=1, fit='box')
S('599c087f46be', '보충간판', B(2, 1, 50, 18, '요금', color=_up, **_e), B(80, 1, 127, 18, '1시간', color=_up, **_e), B(30, 19, 66, 36, '학생', color=_up, **_e),
  B(80, 19, 127, 36, '200엔', color=_up, **_e), B(30, 42, 66, 60, '일반', color=_up, **_e), B(80, 42, 127, 60, '400엔', color=_up, **_e),
  *[B(*_b, _t, v=True, color=_lo, **_e) for _b, _t in (((2, 66, 22, 126), '맥주'), ((26, 66, 50, 127), '안주'), ((52, 66, 74, 122), '주스'), ((78, 66, 100, 122), '라면'), ((104, 66, 127, 108), '컵'))])
S('8a2697a51b4d', '보충간판', B(0, 64, 128, 128, '', erase='alpha'), B(2, 66, 126, 126, '타무라\n정육점', font='heavy', fit='box', color=(140, 35, 40), stroke=((215, 130, 130), 1)))
S('d5b8e94771eb', '보충간판', B(0, 66, 128, 128, '', erase='flat', bg=(125, 42, 42), noise=0.05), B(2, 68, 126, 126, '타무라\n정육점', font='heavy', erase='none', fit='box', color=(225, 150, 150)))
S('bf3236ea9693', '보충간판', B(0, 0, 128, 28, '', erase='alpha'), B(0, 28, 128, 48, '', erase='alpha'),
  B(2, 1, 126, 27, '류 이발소', font='heavy', fit='box', color=(225, 215, 180)), B(2, 30, 126, 47, '커트&파마', font='heavy', fit='box', color=(130, 40, 40)),
  B(4, 92, 124, 120, '류 이발소', font='heavy', erase='dark', delta=50, fit='box', flip='v', color=(25, 20, 20)))
S('e60baa39993a', '보충간판', B(6, 24, 106, 52, '', erase='ink', ink=(70, 40, 10), tol=150, grow=1), B(52, 22, 92, 52, '', erase='ink', ink=(220, 60, 40), tol=130, grow=1),
  B(10, 24, 104, 38, '엄선 밀로 구운', font='heavy', erase='none', fit='box', color=(45, 25, 8)), B(24, 38, 90, 53, '정성 빵', font='heavy', erase='none', fit='box', color=(220, 50, 35)),
  B(0, 76, 128, 128, '', erase='alpha'), B(3, 78, 125, 126, '토마토 마트\n요코스카점', font='gothic', fit='box', color=(25, 25, 30)))
S('d1a431b67fe5', '보충간판', B(0, 12, 128, 50, '', erase='alpha'), B(0, 50, 128, 97, '', erase='alpha'),
  B(12, 16, 94, 50, '수제 빵', font='heavy', fit='box', color=(205, 205, 205)), B(2, 54, 126, 96, '코미네 베이커리', font='heavy', fit='box', color=(205, 205, 205)))
S('050643ba0829', '보충간판', B(0, 6, 64, 30, '', erase='alpha'), B(0, 30, 64, 52, '', erase='alpha'),
  B(8, 9, 56, 29, '수제 빵', font='gothic', fit='box', color=(235, 215, 110)), B(1, 31, 63, 49, '코미네 베이커리', font='gothic', fit='box', color=(235, 215, 110)))
S('dd02b1fc522c', '보충간판', B(4, 6, 128, 60, '신춘 대', font='heavy', erase='light', delta=55, fit='box', color=(225, 225, 225)),
  B(0, 66, 124, 124, '매출', font='heavy', erase='light', delta=55, fit='box', color=(225, 225, 225)))
_inkn = dict(erase='none', fit='box', font='heavy', color=(5, 5, 5))
S('0c568f67d152', '보충간판', B(100, 8, 158, 28, '맛있는', font='gothic', erase='dark', delta=45, grow=1, fit='box', color=(45, 35, 20)),
  *[B(*_b, '', erase='ink', ink=(0, 0, 0), tol=200, grow=1) for _b in ((34, 50, 96, 108), (96, 50, 158, 108), (158, 50, 222, 108))],
  B(44, 60, 86, 100, '도', **_inkn), B(106, 60, 148, 100, '시', **_inkn), B(168, 60, 210, 100, '락', **_inkn))
S('bad202db1f02', '보충간판', B(20, 26, 92, 37, '맛있는', font='gothic', erase='dark', delta=45, grow=1, fit='box', vsize=(40, 11), color=(45, 35, 20)),
  *[B(*_b, '', erase='ink', ink=(0, 0, 0), tol=200, grow=1) for _b in ((20, 46, 86, 70), (20, 70, 86, 94), (20, 94, 86, 118))],
  B(34, 49, 72, 67, '도', vsize=(18, 18), **_inkn), B(34, 73, 72, 91, '시', vsize=(18, 18), **_inkn), B(34, 97, 72, 115, '락', vsize=(18, 18), **_inkn))
S('cee38cf8db57', '보충간판', B(24, 27, 110, 52, '스마일리', font='heavy', erase='light', delta=70, fit='box', color=(245, 245, 245)))
S('17c5e4709eef', '보충간판', B(0, 0, 128, 62, '', erase='alpha'), B(4, 4, 124, 26, '호쿠호쿠', font='heavy', fit='box', color=(150, 30, 30)), B(30, 34, 100, 58, '도시락', font='heavy', fit='box', color=(150, 30, 30)))
S('42c8e591a592', '보충간판', B(0, 0, 64, 64, '', erase='flat'), B(2, 6, 62, 32, '모타비아', font='heavy', erase='none', fit='box', color=(10, 10, 235)), B(10, 34, 54, 60, '교통', font='heavy', erase='none', fit='box', color=(10, 10, 235)))
S('df8f97be6dac', '보충간판', B(16, 84, 76, 112, '', erase='ink', ink=(70, 120, 210), tol=170, grow=1), B(18, 90, 74, 108, '게임센터', font='gothic', erase='none', fit='box', color=(95, 150, 235)))
S('e2e25e2de3df', '보충간판', B(9, 21, 37, 31, '', erase='ink', ink=(50, 70, 190), tol=190, grow=1), B(10, 22, 36, 30, '게임센터', font='gothic', erase='none', fit='box', color=(40, 60, 185)))
S('29ad3d0d2f51', '보충간판', B(12, 34, 58, 58, '', erase='ink', ink=(225, 120, 80), tol=120, grow=1), B(14, 36, 56, 57, '린다', font='gothic', erase='none', fit='box', color=(230, 125, 85)))
for _k in ('a8d1159d0e99', 'f00f9697c56e', '8cbeec177d6e'):
    S(_k, '보충간판', B(84, 2, 102, 80, '당신도 멋지게', v=True, font='gothic', fit='box', color=(190, 150, 50)), B(102, 2, 126, 80, '멋있어!', v=True, font='gothic', fit='box', color=(230, 230, 230)),
      B(2, 82, 52, 102, '커트', font='gothic', fit='box', color=(205, 205, 205)), B(2, 105, 52, 126, '파마', font='gothic', fit='box', color=(205, 205, 205)),
      B(108, 82, 126, 102, '엔', font='gothic', fit='box', color=(205, 205, 205)), B(108, 105, 126, 126, '엔', font='gothic', fit='box', color=(205, 205, 205)))
S('d84106bfaedd', '보충간판', B(1, 24, 63, 37, '어서 오세요', font='gothic', erase='light', delta=45, grow=1, fit='box', color=(205, 205, 195)))

# ───── 표지판 ─────
_h = dict(v=True, font='gaegu', erase='dark', grow=1, fit='box')
S('14460901616c', '보충표지판', B(6, 8, 56, 122, '고장', delta=45, color=(35, 35, 40), **_h), B(74, 8, 116, 110, '고장', delta=45, color=(35, 35, 40), **_h))
S('1467e80b7032', '보충표지판', B(6, 6, 30, 60, '고장', delta=35, color=(70, 50, 35), **_h))
S('f738ca5feef7', '보충표지판', B(6, 14, 60, 50, '화장실', font='gothic', erase='dark', delta=50, fit='box', color=(35, 35, 35)))
S('20f029b6c557', '보충표지판', B(0, 11, 64, 58, '', erase='ink', ink=(40, 40, 40), tol=250, grow=1),   # 잉크 색만(붉은 줄 안 건드림, 획이 줄을 넘어간 곳까지)
  B(8, 13, 46, 31, '제8', font='gaegu', erase='none', fit='box', gain=1.6, color=(40, 40, 40)), B(3, 33, 61, 51, '창고행', font='gaegu', erase='none', fit='box', gain=1.6, color=(40, 40, 40)))
S('de2b6b0376c2', '보충표지판', B(5, 10, 50, 41, '사쿠라\n가오카', font='gothic', erase='light', delta=60, grow=1, fit='box', color=(230, 235, 240)))
S('f96204de8aad', '보충표지판', B(8, 78, 126, 99, '비상시 출입구', font='gothic', erase='ink', ink=(170, 75, 35), tol=130, grow=1, fit='box', color=(160, 65, 30)),
  B(14, 100, 112, 124, '주차 금지', font='gothic', erase='ink', ink=(170, 75, 35), tol=130, grow=1, fit='box', color=(160, 65, 30)))
_addr = dict(font='gothic', erase='none', fit='box', color=(215, 222, 215))
for _k in ('c8f9140ccfe1', 'b9c864d3c08e'):
    S(_k, '보충표지판', B(11, 3, 53, 61, '', erase='flat', bg=(38, 88, 58), noise=0.08), B(12, 8, 52, 32, '야마노세', **_addr), B(14, 34, 50, 56, '3초메', **_addr))
S('a6f84742cdad', '보충표지판', B(11, 3, 53, 61, '', erase='flat', bg=(30, 80, 50), noise=0.08), B(12, 5, 52, 60, '사쿠라\n가오카\n3초메', **_addr))
S('d959617f90c8', '보충표지판', B(26, 2, 104, 127, '야마노세\n상점\n대매출', font='gothic', erase='dark', delta=38, fit='box', color=(50, 30, 25)))
S('362ab1998632', '보충표지판', B(8, 4, 58, 60, '폐\n점', font='heavy', erase='dark', delta=50, fit='box', color=(5, 5, 5)))
S('0f429a0c4d61', '보충표지판', B(9, 7, 56, 122, '', erase='flat', bg=(40, 105, 170), noise=0.05), B(10, 8, 55, 121, '야간\n누름 버튼식', v=True, font='gothic', erase='none', fit='box', color=(235, 238, 240)))
S('a62f30b0ef9b', '보충표지판', B(9, 7, 25, 57, '수행중', v=True, font='gothic', erase='dark', delta=50, grow=1, fit='box', color=(10, 10, 10)))
S('20aa8263d4eb', '보충표지판', B(30, 86, 58, 100, '안전', font='gothic', erase='dark', delta=50, grow=1, fit='box', color=(25, 25, 25)), B(71, 86, 96, 100, '제일', font='gothic', erase='dark', delta=50, grow=1, fit='box', color=(25, 25, 25)))
S('e8793ab775ec', '보충표지판', B(22, 6, 42, 62, '이나리신사', v=True, font='gothic', erase='dark', delta=28, grow=1, fit='box', color=(38, 38, 40)))

# ───── 스토리 소품 ─────
S('ecbb4f8aacf5', '보충스토리', B(0, 0, 128, 128, '', erase='alpha'), B(4, 2, 124, 126, '료 씨에게', v=True, font='mincho', fit='box', vsize=(40, 124), color=(8, 8, 8)))
S('86f8ad80d8ad', '보충스토리', B(0, 0, 64, 64, '', erase='alpha'), B(1, 3, 63, 28, '백록촌', font='mincho', fit='box', color=(40, 40, 48)), B(1, 30, 40, 52, '에서', font='mincho', fit='box', color=(40, 40, 48)))
S('816e0d5c9fdf', '보충스토리', B(0, 0, 93, 128, '', erase='alpha'), B(96, 0, 128, 110, '', erase='alpha'),
  B(2, 8, 92, 120, '홍슈잉\n노사', font='brush', fit='box', color=(8, 8, 8)), B(98, 2, 127, 108, '첸야오원', v=True, font='brush', fit='box', color=(8, 8, 8)))
S('aec55d6748a2', '보충스토리', B(0, 0, 93, 128, '', erase='alpha'), B(96, 0, 128, 110, '', erase='alpha'),
  B(2, 6, 92, 122, '타오\n리샤오\n노사', font='brush', fit='box', color=(8, 8, 8)), B(98, 2, 127, 108, '첸야오원', v=True, font='brush', fit='box', color=(8, 8, 8)))
S('fc26fe43f612', '보충스토리', B(0, 16, 64, 64, '', erase='alpha'), B(14, 20, 50, 62, '귀하', v=True, font='mincho', fit='box', color=(50, 55, 65)))
S('e2de2cd98cf1', '보충스토리', B(24, 26, 224, 96, '팔음팔양', font='brush', erase='dark', delta=50, fit='box', color=(15, 15, 15)))
for _k, _b, _t in (('655b6b1697e0', (117, 6, 205, 45), '할당 8개'), ('660da45d3d31', (98, 10, 186, 50), '할당 10개'), ('3aa1867c9ebb', (75, 16, 161, 55), '할당 8개')):
    S(_k, '보충스토리', B(*_b, _t, font='pen', erase='dark', delta=30, fit='box', color=(200, 40, 40)))
S('9b5bd9fb82c6', '보충스토리', B(0, 0, 30, 64, '', erase='alpha'), B(32, 0, 64, 64, '', erase='alpha'),
  B(2, 6, 28, 58, '꽝', font='heavy', fit='box', vsize=(26, 34), color=(10, 10, 10)), B(34, 2, 62, 62, '특\n등', font='heavy', fit='box', color=(175, 10, 10)))

# ───── 2차 보충(2026-11-05 하스피 실기 스샷 — 글자판 점수 0 이라 후보에서 빠졌던 것) ─────
S('adaa64d5c66c', '보충2',
  B(8, 8, 56, 118, '', erase='light', delta=45, grow=1), B(10, 10, 54, 116, '사쿠라가오카\n공원', v=True, font='gothic', erase='none', fit='box', color=(205, 130, 50)),
  B(70, 2, 124, 126, '', erase='dark', delta=45, grow=1), B(76, 4, 118, 124, '사쿠라가오카\n공원', v=True, font='brush', erase='none', fit='box', gain=1.5, color=(25, 25, 25)))
S('0ed216a24c7c', '보충2', B(4, 10, 62, 56, '카야마', font='gothic', erase='dark', delta=45, fit='box', color=(15, 15, 12)))
S('5757fbdb54c2', '보충2', B(2, 4, 62, 60, '니시다', font='gothic', erase='dark', delta=45, grow=3, fit='box', color=(50, 32, 18)))
S('e94830b894c9', '보충2', B(2, 4, 62, 62, '모토\n야마', font='gothic', erase='dark', delta=45, fit='box', color=(15, 15, 12)))
S('76547d99c6f2', '보충2', B(6, 0, 60, 64, '', erase='rowprof', cols=[1, 2, 3, 61, 62]), B(8, 18, 58, 46, '다지마', font='gothic', erase='none', fit='box', color=(15, 15, 12)))
S('0d4abb065383', '보충2', B(8, 4, 54, 60, '', erase='flat', bg=(32, 78, 48), noise=0.08), B(9, 8, 53, 56, '미도리초\n3초메', font='gothic', erase='none', fit='box', color=(185, 195, 185)))
