# -*- coding: utf-8 -*-
"""그림 한글화 작업표(2) — 옵션·메뉴 버튼, 설명 줄, 미니게임, 권법. gfx_jobs.py 가 불러 GROUPS 에 더한다."""

# ── 옵션·메뉴 버튼(굵은 고딕 + 원본 테두리 색 자동) ──
BT = dict(font='button', light_text=True, sw=1)   # 버튼 전부: 밝은 글자 + 어두운 테두리, 테두리 두께 1px 통일(하스피 «테두리 제각각 통일»)
BTN = [
    ('OPTION__17_child', '어린이 모드', BT), ('OPTION__18_voice', '음성과 자막', BT), ('OPTION__19_set', '설 정', BT),
    ('OPTION__20_70', '70인 프리배틀\n타임어택', BT), ('OPTION__21_child_c', '어린이 모드', BT), ('OPTION__22_voice_c', '음성과 자막', BT),
    ('OPTION__23_set_c', '설정', BT), ('OPTION__24_amode', '어른', BT), ('OPTION__25_cmode', '어린이', BT),
    ('OPTION__26_cinema', '시네마 모드\n음성:있음\n자막:없음', BT), ('OPTION__27_shen', '쉔무 모드\n음성:있음\n자막:있음', BT),
    ('OPTION__28_game', '게임 모드\n음성:있음\n자막:있음', BT), ('OPTION__29_text', '텍스트 모드\n음성:없음\n자막:있음', BT),
    ('OPTION__30_game_c', '게임 모드\n음성:있음\n자막:있음', BT),
    ('OPTION__41_sound', '사운드', BT), ('OPTION__42_ej', '에리어\n점프', BT), ('OPTION__43_lr', '달리기 버튼\n변경', BT),
    ('OPTION__44_mw', '매직\n웨더', BT), ('OPTION__45_se', '설정', BT), ('OPTION__46_se_c', '설정', BT),
    ('OPTION__47_mono', '모노', BT), ('OPTION__48_stereo', '스테레오', BT), ('OPTION__49_on', '온', BT), ('OPTION__50_off', '오프', BT),
    ('OPTION__51_lmode', 'L:달리기\nR:줌', BT), ('OPTION__52_rmode', 'L:줌\nR:달리기', BT),
    ('OPTION__53_sw', '쉔무\n데이터', BT), ('OPTION__54_kw', '기상대\n데이터', BT),
    ('OPTION__55_lmode_c', 'L:달리기\nR:줌', BT), ('OPTION__56_rmode_c', 'L:줌\nR:달리기', BT), ('OPTION__57_kw_c', '기상대\n데이터', BT),
    ('OPTION__68_file01', '파일1', BT), ('OPTION__69_file02', '파일2', BT), ('OPTION__70_file03', '파일3', BT),
    ('OPTION__71_me_text', 'DISC\n게임 일시\n세이브 일시', BT), ('OPTION__72__e_text_', 'DISC\n게임 일시\n세이브 일시', BT),
    ('OPTION__73_nofile', '파일이 없습니다.', BT), ('OPTION__96_cl_txt', '클리어 파일', BT), ('OPTION__97_lr_c', '달리기 버튼\n변경', BT),
    ('OPTION__104_sd_txt', '스타트 파일', BT),
    ('OPTION1__07_sound', '사운드', BT), ('OPTION1__08_config', '컨피그', BT), ('OPTION1__09_child', '어린이 모드', BT),
    ('OPTION1__10_voice', '음성과 자막', BT), ('OPTION1__11_voice_c', '음성과 자막', BT),
    ('OPTION2__00_mono', '모노', BT), ('OPTION2__01_stereo', '스테레오', BT),
    ('OPTION2__02_lmode', 'L모드\nL:달리기\nR:줌', BT), ('OPTION2__03_lmode_c', 'L모드\nL:달리기\nR:줌', BT),
    ('OPTION2__04_rmode', 'R모드\nL:줌\nR:달리기', BT), ('OPTION2__05_rmode_c', 'R모드\nL:줌\nR:달리기', BT),
    ('OPTION2__06_amode', '어른', BT), ('OPTION2__07_cmode', '어린이', BT),
    ('OPTION2__08_cinema', '시네마 모드\n음성:있음\n자막:없음', BT), ('OPTION2__09_game', '게임 모드\n음성:있음\n자막:있음', BT),
    ('OPTION2__10_game_c', '게임 모드\n음성:있음\n자막:있음', BT), ('OPTION2__11_shen', '쉔무 모드\n음성:있음\n자막:있음', BT),
    ('OPTION2__12_text', '텍스트 모드\n음성:없음\n자막:있음', BT),
]

# ── 설명 줄(검은 명조, 왼쪽 정렬 자동) — 어린이판(히라가나)도 같은 한글 ──
MC = dict(font='mincho', fill=(20, 20, 20), stroke=False, sw=0, align='left')   # 원본: 검은 명조, 왼쪽에서 시작
d_start = '새로 게임을 시작합니다.'
d_cont = '중단한 곳부터\n게임을 다시 시작합니다.'
d_read_s = '세이브 파일을 불러옵니다.'
d_read_d = '세이브 데이터를 불러옵니다.'
d_opt = '게임 설정을 변경합니다.'
DESC = [
    ('MENU__12_start_t', d_start, MC), ('MENU__13___ntinue', d_cont, MC), ('MENU__14_read_t', d_read_d, MC), ('MENU__15_option_t', d_opt, MC),
    ('MENU__16_choice', '선택', MC), ('MENU__17_fix', '결정', MC), ('MENU__18_back', '뒤로', MC),
    ('MENU__19_start_ct', d_start, MC), ('MENU__20_read_ct', d_read_d, MC), ('MENU__21__ption_c', d_opt, MC), ('MENU__22____tinue', d_cont, MC),
]
for p in ('TITLE4_A__', 'TITLE4_S__'):
    for s, t in (('24_start_t', d_start), ('25___ntinue', d_cont), ('26_read_t', d_read_s), ('27_option_t', d_opt),
                 ('28_start_ct', d_start), ('29_read_ct', d_read_s), ('30__ption_c', d_opt), ('31____tinue', d_cont),
                 ('32__t_nofil', '파일이 없습니다.')):
        DESC.append((p + s, t, MC))
DESC += [
    ('OPTION2__13_sound_t', '소리 설정을 변경합니다.', MC), ('OPTION2__14_sound_ct', '소리 설정을 변경합니다.', MC),
    ('OPTION2__15_lr_t', '달리기 버튼을 바꿉니다.', MC), ('OPTION2__16_lr_ct', '달리기 버튼을 바꿉니다.', MC),
    ('OPTION2__17_child_t', '쉬운 말을 중심으로\n게임을 진행합니다.', MC),
    ('OPTION2__18_child_ct', '어린이 모드에서는 쉬운 말을\n중심으로 게임을 진행합니다.', MC),
    ('OPTION2__19_voice_t', '음성과 자막 설정을 변경합니다.', MC),
    ('OPTION2__20_voice_st', '쉔무 모드에서는\n건너뛸 때 자막이 표시됩니다.', MC),
    ('OPTION2__21_voice_ct', '어린이 모드에서는 게임 모드로\n고정됩니다.', MC),
    ('OPTION__100_ryodat', '세이브 파일을 선택해 주세요.', MC), ('OPTION__101_ryodat_c', '세이브 파일을 선택해 주세요.', MC),
    ('OPTION__102_novms', '메모리 카드를 【포트A・슬롯1】에\n꽂아 주세요.', MC),
    ('OPTION__103_novms_c', '메모리 카드를 【포트A・슬롯1】에\n꽂아 주세요.', MC),
    ('OPTION__31_c_t', '10세 이하를 위해 메모, 도움말\n등을 쉬운 말로 바꿉니다.', MC),
    ('OPTION__32_cinema_t', '음성만으로 게임을 진행합니다.', MC),
    ('OPTION__33_shen_t', '음성과 자막으로 게임을 진행합니다.\n건너뛸 때 자막이 표시됩니다.', MC),
    ('OPTION__34_game_t', '음성과 자막으로 게임을 진행합니다.', MC),
    ('OPTION__35_text_t', '자막만으로 게임을 진행합니다.', MC),
    ('OPTION__36_set_t', '그 밖의 설정을 변경합니다.', MC),
    ('OPTION__37_t_t', '타임어택 모드입니다.(DISC 3)\n쉔무 패스포트에서 순위가 매겨집니다.', MC),
    ('OPTION__38_c_ct', '10세 이하를 위해 메모, 도움말\n등을 쉬운 말로 바꿉니다.', MC),
    ('OPTION__39_game_ct', '음성과 자막으로\n게임을 진행합니다.', MC),
    ('OPTION__40_set_ct', '그 밖의 설정을 변경합니다.', MC),
    ('OPTION__58_s_t', '모노와 스테레오를\n전환합니다.', MC), ('OPTION__63_s_ct', '모노와 스테레오를\n전환합니다.', MC),
    ('OPTION__59_j_t', '하즈키가 현관에서 상황에 따라\n목적지로 바로 이동할 수 있습니다.', MC),
    ('OPTION__64_j_ct', '하즈키가 현관에서 상황에 따라\n목적지로 바로 이동할 수 있습니다.', MC),
    ('OPTION__60_l_t', '달리기 버튼과 줌 버튼의\n기능을 바꿉니다.', MC),
    ('OPTION__65_l_ct', '달리기 버튼과 줌 버튼의\n기능을 바꿉니다.', MC),
    ('OPTION__61_sw_t', '쉔무 기상대 데이터', MC), ('OPTION__66_sw_ct', '쉔무 기상대 데이터', MC),
    ('OPTION__62_kw_t', '86년 요코하마 지방 기상대\n발표 데이터', MC),
    ('OPTION__67_kw_ct', '86년 요코하마 지방 기상대\n발표 데이터', MC),
    ('OPTION__74_re_t', '불러올 파일을\n선택해 주세요.', MC), ('OPTION__75_re_ct', '불러올 파일을\n선택해 주세요.', MC),
    ('OPTION__95_load_t', '불러와도 괜찮습니까?', MC),
    ('OPTION__98___ntinue', d_cont, MC), ('OPTION__99____tinue', d_cont, MC),
]

# ── 미니게임 ──
HV = dict(font='heavy')
MINI = [('TNRETRY0__02_kaime', '번째', HV), ('TNRETRY1__02_kaime_c', '번째', HV),
        ('TNTMOV01__00_time_c', '타임 오버', HV), ('TNGMOV01__00_game_c', '게임 오버', HV)]

# ── 권법 화면 ──
CG = dict(font='callig')
CGV = dict(__fn='vshadow')                       # 中級·上級·修得: 같은 크기 + 원본 그림자(하스피 «그림자좀»)
TAN = dict(__fn='vplate', box=(6, 7, 23, 57), ink_h=14, cell=16, font='gothic', bold=5, pool_x=[5, 23, 24, 25])   # 왼쪽 찌꺼기까지(x6~)·조금 굵게   # 판 금색 x5~25, 글자 x9~21     # 修行中: 금색 판은 살리고 글자만
WAZA = [('SYUGYOU__00_ashi', '발기술', CG), ('SYUGYOU__01_ashi_a', '발기술', CG), ('SYUGYOU__07_nage', '던지기', CG),
        ('SYUGYOU__08_nage_a', '던지기', CG), ('SYUGYOU__15_te', '손기술', CG), ('SYUGYOU__16_te_a', '손기술', CG),
        ('SYUGYOU__18_zen', '모든 기술', CG), ('SYUGYOU__19_zen_a', '모든 기술', CG),
        ('SYUGYOU__02_chu', '중급', CGV), ('SYUGYOU__03_jyo', '상급', CGV), ('SYUGYOU__13_syu', '습득', CGV),
        ('SYUGYOU__14_tan', '수행중', TAN),
        ('WAZAHYOU__00_chu', '중급', CGV), ('WAZAHYOU__01_jyo', '상급', CGV), ('WAZAHYOU__07_syu', '습득', CGV),
        ('WAZAHYOU__08_tan', '수행중', TAN)]

GROUPS = {'03_옵션메뉴버튼': BTN, '04_설명줄': DESC, '05_미니게임': MINI, '06_권법': WAZA}
