# -*- coding: utf-8 -*-
"""그림 한글화 작업표 — 묶음별 (텍스처, 한글, 옵션). python tools/gfx_jobs.py [묶음…]
일본어 고유명사는 거센소리 표기(か행 ㅋ·た행 ㅌ·つ 츠) — 메모리 규칙. 涼=료, 芭月=하즈키, 横須賀=요코스카."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gfx_kr as G

H = dict(font='brush', fill=(255, 255, 255), stroke=False, sw=0)
V = dict(__fn='vfixed', cell=41, ink_h=35)   # 가장 빠듯한 「사쿠라가오카」(세로 256 텍스처)에 맞춘 한 가지 크기 — 세로 지명: 모두 같은 글자 크기·칸 간격(하스피 «세로글씨 크기 통일»)   # 흰 단색, 굵게(같은 색 테두리 1px)
LD = [
    ('LD4DAYAF__00_0', '4일 후…', V), ('LDABESYO__00_0', '아베상점', V),
    ('LDAJIITI__00_0', '_중화 아지이치', V), ('LDAJIITI__00_LD_aji', '_중화 아지이치', V),
    ('LDASIARK__00_0', '아시아여행사', V), ('LDBARHAR__00_0', '하트비츠', V),
    ('LDBARYKS__00_0', '바 요코스카', V), ('LDBPIZZA__00_0', '밥스 피자', V), ('LDBUNKAD__00_0', '골동품점', V),
    ('LDCHIKA__00_0', '하즈키가 지하', V), ('LDDAISAN__00_0', '다이산겐', V), ('LDDOBUIT__00_0', '도부이타', V),
    ('LDGAMEYU__00_0', '게임센터 유', V), ('LDHAZUKI__00_0', '하즈키가', V), ('LDJIMSYO__00_0', '사무소', V),
    ('LDJYUUTA__00____jyuut', '주택가', V), ('LDKARAOK__00_LD_kpn', '노래방 펍 나나', V), ('LDKITAKU__00_0', '귀가', V),
    ('LDKOUJIG__00_0', '공사현장', V), ('LDKYUKEI__00_LD_kkj', '항만휴게소', V), ('LDKYUSOK__00_LD_sou', '옛창고가', V),
    ('LDLINDA__00_0', '린다', V), ('LDMANPUK__00_0', '만푸쿠켄', V), ('LDNAGAIK__00_0', '나가이흥업', V),
    ('LDOMOYA__00_0', '하즈키가 본채', V), ('LDOPNING__00_LD_opy', '요코스카', V), ('LDRAPISU__00_0', '라피스', V),
    ('LDRIYOMA__00_0', '이발소 마에다', V), ('LDROSIYA__00_0', '도자기점 로시야', V), ('LDRROOMK__00_LD_ryo', '료의 방', V),
    ('LDRYROOM__00_LD_rnh', '료의 방', V), ('LDRYURIH__00_0', '바버 류', V), ('LDSAKURA__00_0', '사쿠라가오카', V),
    ('LDSEKAIR__00_0', '세계여행사', V), ('LDSINYKK__00_0', '신요코스카항', V), ('LDSLOTHO__00_0', '슬롯하우스', V),
    ('LDSOBAYA__00_LD_sob', '소바집 야마지', V), ('LDSYUEIR__00_0', '경비실', V), ('LDTAKARA__00_0', '타카라즈시', V),
    ('LDTATOO__00_0', '타투숍', V), ('LDTOMATO__00_0', '토마토마트', V), ('LDWASYOK__00_LD_rsd', '항만식당', V),
    ('LDYAMANO__00_0', '야마노세', V),
] + [('LDDAI%dSO__00_0' % k, '제%d창고' % k, V) for k in range(1, 10)] \
  + [('LDDAI%dS__00_0' % k, '제%d창고' % k, V) for k in range(10, 19)] + [
    ('LD_0101__00__D_ganta', '설날', H), ('LD_0214__00_LD_vtd', '밸런타인데이', H),
    ('LD_1224__00_LD_ibu', '크리스마스 이브', H), ('LD_1225__00_LD_xmas', '크리스마스', H),
    ('LD_1231__00_LD_oom', '섣달그믐', H),
]
B = dict(__fn='fixed')     # 날짜 낱자: 모두 같은 글자 크기·기준선(하스피 «같은 ui 글자는 크기 통일»)
LOADNUM = [('LOADNUM__10_LD_do', '토', B), ('LOADNUM__11_LD_fun', '분', B), ('LOADNUM__12_LD_gogo', '오후', B),
           ('LOADNUM__13_LD_gozen', '오전', B), ('LOADNUM__14_LD_ji', '시', B), ('LOADNUM__15_LD_ka', '화', B),
           ('LOADNUM__16_LD_kin', '금', B), ('LOADNUM__17_LD_moku', '목', B), ('LOADNUM__18_LD_nen', '년', B),
           ('LOADNUM__19_LD_niti', '일', B), ('LOADNUM__20_LD_sui', '수', B), ('LOADNUM__21_LD_tuki', '월', B)]
GROUPS = {'01_로딩지명': LD, '02_로딩날짜': LOADNUM}
import gfx_jobs_ui
GROUPS.update(gfx_jobs_ui.GROUPS)
import gfx_jobs_para
GROUPS.update(gfx_jobs_para.GROUPS)
import gfx_jobs_misc
GROUPS.update(gfx_jobs_misc.GROUPS)
import gfx_jobs_title
GROUPS.update(gfx_jobs_title.GROUPS)

def run(names):
    for g in names:
        pairs = []
        for name, ko, opt in GROUPS[g]:
            try:
                if '__fn' in opt:
                    o = {k: v for k, v in opt.items() if k != '__fn'}; fn = opt['__fn']
                    if fn == 'fixed': r = G.render_fixed(name, ko, **o)
                    elif fn == 'logo_layer': r = G.render_logo_layer(name, **o)
                    elif fn == 'vshadow': r = G.render_vshadow(name, ko, **o)
                    elif fn == 'vplate': r = G.render_vplate(name, ko, **o)
                    elif fn == 'vfixed': r = G.render_vfixed(name, ko, **o)
                    elif fn == 'plate': r = G.render_plate(name, ko, **o)
                    elif fn == 'logo': r = G.render_logo(name, ko, **o)
                    elif fn == 'vcols': r = G.render_vcols(name, **o)
                    elif fn == 'vcols_fixed': r = G.render_vcols_fixed(name, **o)
                    elif fn == 'cells': r = G.render_cells(name, **o)
                    elif fn == 'stamp': r = G.render_stamp(name, text=ko.split('→')[-1], **o)
                    pairs.append((name, ko, r))
                elif '__para' in opt:
                    o = {k: v for k, v in opt.items() if k != '__para'}
                    pairs.append((name, ' / '.join(x if isinstance(x, str) else str(x) for x in ko), G.render_para(name, ko, **o)))
                else:
                    pairs.append((name, ko, G.render(name, ko, **opt)))
            except FileNotFoundError: print('없음', name)
        for f in [os.path.join(G.PREV, g + '.png')]:
            if os.path.exists(f): os.remove(f)          # 옛 한 장짜리 미리보기
        print(G.preview_grid(g, pairs, scale=2 if g in ('02_로딩날짜', '05_미니게임', '06_권법') else 1), len(pairs))

if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    run(sys.argv[1:] or list(GROUPS))
