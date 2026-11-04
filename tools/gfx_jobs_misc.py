# -*- coding: utf-8 -*-
"""그림 한글화 작업표(4) — 무늬 판·타이틀 로고·엔딩 시·낱칸(円 枚)·도장(練習). 각 항목 (텍스처, 표시용 한글, {'__fn': 렌더러, …인수})"""
POEM1 = ['그 자', '동쪽 먼 나라에서', '바다를 건너', '나타나리라', '젊은이', '숨겨진 힘을', '아직 모르노라',
         '그의 몸을', '멸하는 것도', '그의 소원을', '이루는 것도', '그 자가', '떨쳐 일어설 때']
POEM2 = ['나를 찾으리', '함께', '거친 들판의 길을 가리라', '기다리며 바라라', '해후는 나의', '아득한 옛날부터의', '운명이니',
         '칠흑의 밤이', '펼쳐져도', '샛별은 홀로 빛나고', '긴 이야기는']
POEM3 = ['', '지금', '열리노라']     # 「今 始まれり」— 세로 128 조각이라 4자로(엔딩 글자 크기 통일)
MISC = [
    ('TITLE4_A__13_main', '스타트 메뉴', {'__fn': 'plate', 'kind': 'dark', 'region': (150, 8, 360, 52), 'font': 'button'}),
    ('TITLE4_S__13_main', '스타트 메뉴', {'__fn': 'plate', 'kind': 'dark', 'region': (150, 8, 360, 52), 'font': 'button'}),
    ('MENU__01_main', '메인 메뉴', {'__fn': 'plate', 'kind': 'dark', 'region': (150, 8, 360, 52), 'font': 'button'}),
    ('OPTION__91_yes_r', '예', {'__fn': 'plate', 'kind': 'light', 'region': (30, 12, 115, 52), 'font': 'button', 'text_h': 34}),
    ('OPTION__92_no_r', '아니요', {'__fn': 'plate', 'kind': 'light', 'region': (8, 12, 100, 52), 'font': 'button', 'text_h': 34}),
    ('OPTION__93_yes_h', '예', {'__fn': 'plate', 'kind': 'light', 'region': (30, 12, 115, 52), 'font': 'button', 'text_h': 34}),
    ('OPTION__94_no_h', '아니요', {'__fn': 'plate', 'kind': 'light', 'region': (8, 12, 100, 52), 'font': 'button', 'text_h': 34}),
    ('TITLE4_A__02_tit_main', '쉔무', {'__fn': 'logo', 'font': 'callig', 'keep': (452, 86, 480, 110), 'spread': True}),
    ('TITLE4_S__02_tit_main', '쉔무', {'__fn': 'logo', 'font': 'callig', 'keep': (452, 86, 480, 110), 'spread': True}),
    ('TITLE3__02_tit_main', '쉔무', {'__fn': 'logo', 'font': 'callig', 'keep': (452, 86, 480, 110), 'spread': True}),
    ('TITLE4_A__03_tit_sub', '제1장 요코스카', {'__fn': 'logo', 'font': 'yeonsung'}),
    ('TITLE4_S__03_tit_sub', '제1장 요코스카', {'__fn': 'logo', 'font': 'yeonsung'}),
    ('TITLE3__03_tit_sub', '제1장 요코스카', {'__fn': 'logo', 'font': 'yeonsung'}),
    ('ENDMOJI0__00_ED_C01', ' / '.join(POEM1), {'__fn': 'vcols_fixed', 'columns': POEM1, 'step': 30, 'ink_h': 26}),
    ('ENDMOJI0__01_ED_C02', ' / '.join(POEM2), {'__fn': 'vcols_fixed', 'columns': POEM2, 'step': 30, 'ink_h': 26}),
    ('ENDMOJI0__02_ED_C03', ' / '.join(POEM3), {'__fn': 'vcols_fixed', 'columns': POEM3, 'step': 30, 'ink_h': 26}),
    ('COMICON__04___em_128', '円→엔 · 枚→개 (MISC/TEXTURES.PKS 사본도 같이)', {'__fn': 'cells', 'cells': [((96, 80, 112, 96), '엔'), ((112, 80, 128, 96), '개')]}),
    ('LAPTIME__02_f_sujiw', '円→엔 · 枚→개', {'__fn': 'cells', 'cells': [((16, 48, 32, 64), '엔'), ((32, 48, 48, 64), '개')]}),
    ('COMICON__01_QTE02', '練習→연습', {'__fn': 'stamp', 'box': (30, 82, 100, 110)}),
]
GROUPS = {'08_판로고엔딩기타': MISC}
