# -*- coding: utf-8 -*-
"""그림 한글화 작업표(5) — 타이틀 통그림 로고(하스피 «타이틀 쉔무 큰글자 안 했으면 ㄱ», 2026-11-04).
배경에 박힌 로고를 TITLE3 로고 레이어 모양으로 찾아 지우고(OpenCV inpaint), 원본 로고 질감으로 한글. 鈴木(스즈키 유 서명)은 그대로."""
T = [
    ('TITLE__00_TITLE03', '쉔무 / 제1장 요코스카', {'__fn': 'logo_layer', 'items': [
        dict(layer='TITLE3__02_tit_main', text='쉔무', feature='red', outline=(170, 170, 180), spread=True, stretch=1.9, pad=1),
        dict(layer='TITLE3__03_tit_sub', text='제1장 요코스카', font='yeonsung', feature='red', outline=(170, 170, 180), pad=1,
             search=(100, 260, 560, 350), scales=[1.0])]}),
    ('TITLE2__00_TIT_1207', '쉔무', {'__fn': 'logo_layer', 'items': [
        dict(layer='TITLE3__02_tit_main', text='쉔무', feature='dark', spread=True, stretch=1.9, pad=1)]}),
]
GROUPS = {'10_타이틀통그림': T}
