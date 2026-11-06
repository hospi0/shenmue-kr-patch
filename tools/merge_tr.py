# -*- coding: utf-8 -*-
"""하스피 번역 TSV 병합 + 자동 교정 → work/text/ko/*.tsv (빌드 입력) + work/text/ko/merge_log.tsv(바꾼 것 전부)

  python tools/merge_tr.py "<번역 폴더>" [--skip sm1_082]

자동 교정(쓰는 순간 강제 — 바꾼 줄은 전부 merge_log 에)
  1) 이름 표기 통일(GLOSSARY: 원문에 그 이름이 있을 때만, 뒤 조사 받침 맞춤) — 거센소리 규칙(か=카·た=타·つ=츠)
  2) 반각 따옴표 ' " → 원문 괄호(원문 『』 면 『』, 아니면 「」) — 전각 ＇＂ 는 EUC 밖(IBM 확장)이라 못 넣음
  3) 원문 괄호가 『』 뿐인데 번역이 「」 뿐이면 『』 로
  4) 메모장·기술 설명(사전 코드 구역): 코드가 아닌 반각 숫자·영문 → 전각(반각 두 글자는 사전 코드로 읽힌다)
  5) 실행 파일 설명 글: 원문 «꽉 찬 줄의 자동 줄바꿈(0)»을 그대로 베낀 낱말 중간 0 은 지우고, 폭 넘는 줄은 띄어쓰기에서 0 으로 다시 접음
  6) FIXES: 손으로 고친 줄(아이템 칸 바이트·버튼 자리·표 맞춤) — 이유와 함께
"""
import os, sys, re, glob, struct, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import build_exe as BE
import exe_strings
from encode import to_wide

OUT = os.path.join(ROOT, 'work', 'text', 'ko')

# (원문에 있어야 할 글자, 틀린 꼴, 바른 꼴, 짧은 낱말이라 앞뒤 경계 필요?)
GLOSSARY = [
    ('稲', '이나', '이네', True), ('陳', '진', '첸', True), ('陳', '천', '첸', True), ('劉', '유', '류', True),
    ('大石', '오오이시', '오이시', False), ('矢田', '야타', '야다', False),
    ('クリタ', '구리타', '쿠리타', False), ('栗田', '구리타', '쿠리타', False),
    ('明田川', '아케다가와', '아케타가와', False), ('竹内', '다케우치', '타케우치', False),
    ('辰巳', '다쓰미', '타츠미', False), ('辰巳', '타쓰미', '타츠미', False), ('タツミ', '타쓰미', '타츠미', False),
    ('住谷', '스미타니', '스미야', False), ('鶴岡', '쓰루오카', '츠루오카', False), ('ツルオカ', '쓰루오카', '츠루오카', False),
    ('コミネ', '고미네', '코미네', False), ('小峰', '고미네', '코미네', False), ('秀玉', '슈교쿠', '수옥', False),
    ('貴章', '키쇼', '귀장', False), ('貴章', '다카아키', '귀장', False), ('藍帝', '남제', '란디', True),
    ('原崎', '하라자키', '하라사키', False), ('八百勝', '야오카쓰', '야오카츠', False), ('勝', '가쓰', '카츠', True),
    ('つくし', '쓰쿠시', '츠쿠시', False), ('土蜘蛛', '쓰치구모', '츠치구모', False), ('松山', '마쓰야마', '마츠야마', False),
    ('小松菜', '고마쓰나', '코마츠나', False), ('イシマツ', '이시마쓰', '이시마츠', False), ('こたつ', '고타쓰', '코타츠', False),
    ('草津', '쿠사쓰', '쿠사츠', False), ('残月', '잔게쓰', '잔게츠', False), ('ミツヅカ', '미쓰즈카', '미츠즈카', False),
    ('はつてん', '하쓰텐', '하츠텐', False), ('シュゲンタツ', '슈겐타쓰', '슈겐타츠', False),
    ('リュウサツ', '류사쓰', '류사츠', False),
    ('トキ', '도키', '토키', True), ('シェンムー', '션무', '쉔무', False),
    # 중국인 이름 = 중국어 발음(하스피 2026-11-04 «중국인 이름은 중국어 발음으로»)
    ('陶', '도', '타오', True), ('チンタイジン', '천', '첸', True),
    ('貴章', '귀장', '구이장', False), ('貴章', '타카아키', '구이장', False), ('秀玉', '하수옥', '샤슈위', False), ('秀玉', '수옥', '슈위', False),
    ('朱元達', '주원달', '주위안다', False), ('朱元達', '朱元達', '주위안다', False), ('シュゲンタツ', '슈겐타츠', '주위안다', False),
    ('高文', '타카후미', '가오원', False), ('高文', '코타', '가오원', True), ('コウブン', '高文', '가오원', False),
    ('趙孫明', '조손명', '자오쑨밍', False), ('趙', '조', '자오', True),
    ('桂林', '구이린', '계림', False),   # 자막 표기로 통일(하스피 2026-11-06)
    ('玲莎花', '링샤화', '링션화', False),   # 게임 이름 シェンファ·Shenhua (하스피 2026-11-06 «션화 ㄱ»)
    ('桃李少', '도리소', '타오리샤오', False), ('桃李少', '桃李少', '타오리샤오', False), ('かよこ', '가요코', '카요코', False), ('タムラ', '다무라', '타무라', False),
]

# 손으로 고친 줄: 키 → (바뀐 번역, 이유)
FIXES = {
    'exe:2612E8': ('미니 카세트', '아이템 이름 칸 18 B(9자) — «미니 라디오 카세트» 20 B'),
    'exe:261300': ('아버지 앞 편지', '아이템 이름 칸 18 B — «아버지 앞으로 온 편지» 24 B'),
    'exe:2614CC': ('그림자사냥 비급', '아이템 이름 칸 18 B · 기술 이름 통일(하스피 2026-11-05 «기존번역으로»)'),
    'exe:2614DC': ('그림자사냥의 기술서', '기술 이름 통일'),
    'exe:2614F8': ('갑옷꿰기 기술서', '아이템 이름 칸 18 B · 기술 이름 통일'),
    'exe:261504': ('갑옷꿰기의 기술서', '기술 이름 통일'),
    'exe:2615B0': ('선풍의 기술서', '기술 이름 통일(회오리→선풍)'),
    'exe:2615BC': ('선풍의 기술서', '기술 이름 통일(회오리→선풍)'),
    'exe:26160C': ('몽롱무쌍 비급', '아이템 이름 칸 18 B · 기술 이름 통일'),
    'exe:26161C': ('몽롱무쌍의 기술서', '기술 이름 통일'),
    'E1018A146': ('그림자사냥…', '기술 이름 통일'),
    'SA1108B003': ('갑옷꿰기(鎧通)는 몸놀림으로＆장(掌)을 내뻗는 기술이니라', '기술 이름 통일'),
    'exe:26B868': ('하즈키 가 현관에서 상황에 따라,', '하스피 «현관에서 뒤 쉼표는 빼고»'),
    'exe:26B8DC': ('「１０세」 이하용으로 메모, 도움말', '설정 설명 줄 38 B 한도(40 B)'),
    'exe:26B948': ('「하즈키 가 현관」에서 경우에 따라', '설정 설명 줄 38 B 한도(40 B)'),
    'exe:26165C': ('수수께끼 두루마리', '아이템 이름 칸 18 B — «의» 빼기'),
    # 기술 화면 도움말: 줄마다 «본문(0칸~) 0 꼬리(19칸~) 0» · R 아이콘은 원문 자리(3줄 7~8칸째)에 고정으로 그려짐(2026-11-04 실기 겹침)
    'exe:25CF00': ('A막대그래프는　「숙련도」를　나타냅니다0．0빨간　틀은　중점적으로　수행하는　기술0．0초록　틀은，　　에　등록된　기술입니다0．0커맨드는　료가　오른쪽을　향한　경우0．0',
                   '기술 화면 도움말 — 줄 19칸 + 꼬리, 버튼 그림 자리를 원문 칸(3줄 7칸째)에'),
    'exe:25CFAC': ('B막대그래프는　「숙련도」를　나타냅니다0．0빨간　틀은　중점적으로　수행하는　기술0．0초록　틀은　등록되어　있는　기술0．0커맨드는　료가　오른쪽을　향한　경우0．0',
                   '기술 화면 도움말(어린이판) — 줄 19칸 + 꼬리'),
    # COLDINIT.PKS SCNF(크기 고정) 28 B 넘침 → 혼잣말 몇 줄 다듬기(자막 SRF 도 같은 문장, 2026-11-04)
    'SY07A006': ('이네 씨가 신경 쓰겠지.＆돌아갈까…', 'COLDINIT SCNF 크기 고정 — 짧게'),
    'SY08A004': ('이네 씨가 신경 쓰겠지.＆이만 갈까…', 'COLDINIT SCNF 크기 고정 — 짧게'),
    'SY07A007': ('벌써 이런 시간인가…＆오늘은 일찍 가야지…', 'COLDINIT SCNF 크기 고정 — 짧게'),
    'SY08A005': ('이네 씨가 걱정하겠지.＆돌아갈까…', 'COLDINIT SCNF 크기 고정 — 짧게'),
    'SY07A005': ('이네 씨가 걱정할라.＆슬슬 돌아갈까…', 'COLDINIT SCNF 크기 고정 — 짧게'),
    'SY08A006': ('이네 씨가 걱정할라.＆슬슬 돌아갈까…', 'COLDINIT SCNF 크기 고정 — 짧게'),
    # 도움말 = 조각(0) 격자(줄 i//2, 칸 (i%2)×19) · 조각 수 원문과 같게 · 버튼 그림 자리 원문 칸 · 한 조각 ≤50 B(52 B 줄 버퍼)
    'exe:25CBF0': ('B다이얼하고　싶은　번호에　손끝을　맞추0고，0　　버튼을　눌러　주세요．00전화를　걸　수　있습니다．',
                   '도움말 조각 수 원문(4)대로 · 버튼 자리 2줄 첫 칸'),
    'exe:25E70C': ('【다트　세븐】A１게임　１００엔이고，　　로　던집니다0．0１２０점을　넘으면　２ｎｄ　스테이지로，00２ｎｄ　스테이지에서　２４０점을　넘으면00３ｒｄ　스테이지로　진행할　수　있습니다．0000　중앙의　빨간　원　　　　　：５０점00　중앙　주변　　　　　　　　：２５점00　바깥쪽　빨강·초록　라인　：２배00　안쪽　빨강·초록　라인　　：３배0',
                   '도움말 조각 수 원문(17)대로 · 버튼 자리 1줄 12칸째 · 첫 조각 50 B 넘음 · ：줄 맞춤'),
    'exe:25ED18': ('【전　기술　두루마리】A여기　적힌　커맨드는　료가　오른쪽을00보고　상대가　오른쪽에　있을　때입니다．00료의　방향이　반대면　커맨드도　반대가0됩니다．0초록　틀은，　　에　등록　중인　기술．0000선택0료　줌0기술　해설0료　회전000표시　전환0뒤로0',
                   '도움말 조각 수 원문(18)대로 · 버튼 자리 4줄 7칸째 · 조각 50 B 넘음'),
    'exe:25EE00': ('【컬렉션】A입수한　컬렉션　아이템을00볼　수　있습니다．00컬렉션이　８５개　이상이　되면00　　　　로　창을　전환할　수　있습니다0．000커서　이동0　　보기0000　　뒤로0',
                   '도움말 조각 수 원문(16)대로 · 버튼 자리 원문 칸 · 조각 50 B 넘음'),
}
# 자막 3줄 → 2줄(19칸) 다듬기 — 하스피 «자막 2줄로 적당히 줄이고»(2026-11-04)
_SUB2 = {
    '01195010033': '음…그걸로 됐다. 부모가 부모이듯,＆친구 또한 친구일 뿐이다',
    'E1017B053': '선생님은 늘 이 수월 찌르기가＆기본이고 제일 중요하다셨죠',
    'F1041A125': '아뇨, 이발하러 가는 게 아니에요.＆잠깐 볼일이 있을 뿐이에요…',
    'F1041B239': '쿠리타 씨랑 한잔하고 오는 길에＆『여기 내 아파트야』라길래…',
    'F1050C042': '만푸쿠켄은 우리 집 나가서 왼쪽,＆오토바이 가게 지나서예요',
    'F1101B052': '사나이라면 겉모양부터 따지지 마라.＆문신 따위 그저 장식일 뿐이다',
    'F1133B031': '적어도, 이 현장 관계자 중엔＆중국어를 읽을 사람이 없네요',
    'F1143B083': '있었나, 문신 가게 같은 게?＆아니, 어디서 들은 것 같은데…',
    'F1225A096': '이 근처에서 중국 사람에 대해＆누구한테 묻는 게 제일 좋을까?',
    'F1252B176': '어깨 부딪히면 치료비 내놓으라느니,＆밥이 맛없으면 식중독이라느니…',
    'F1252B243': '좋아하는 Ｇｌｏｏｍｙ　Ｃｉｔｙ를＆그런 싸구려 술집에선 듣기 싫어…',
    'F1274B149': '정규 입국 절차를 안 밟아도＆항구를 거점으로 세를 넓히니까',
    '01KEIB006': '옛날 중국에선 돌거울을 만들었지요.＆그건 그렇고 훌륭하군요',
    'A0132B002': '나비 부인의 특별 주문품입니다.＆자, 마담 버터플라이. 아시죠',
    'F1022B065': '대륙에서 짐짝처럼 귀환선을 타서＆배라면 이제 지긋지긋하다니까',
    'F1033B287': '아, 그 편의점 옆 가게 말이지.＆좋은 거 있긴 한데, 비싸단 말야',
    'F1105B014': '나가서 오른쪽으로 돌면 바다니까＆해안 따라 왼쪽으로 쭉 가야 해',
    'F1119B222': '아시아 여행사란 데가 있어.＆전에 항구서 거기까지 손님 태웠거든',
    'A0174B005': '야반도주하려고 준비해 둔 겁니다.＆보시다시피 부도 내고 망했어요',
    'E1063B052': '다음은 좌우로 한 걸음 옮기며＆곧바로 피하기와 던지기에 드는 걸세',
    'F1024B020': '젊을 땐 센 척하는 것도 좋지만,＆정신 차려 보면 주변은 적투성이…',
    'F1106B028': '아니면 차라리 연예인 노려 볼래?＆너라면 분명 통할 거야',
    'F1106B029': '여기서 나가서 반대편이야.＆좌우 어느 쪽으로 돌아가도 돼',
    'F1288B020': '아까 고등학생 같은 사람이 있었지.＆그 사람도 알바를 찾았나?',
}
for _k, _v in _SUB2.items(): FIXES[_k] = (_v, '자막 3줄 → 2줄로 다듬음(19칸)')
# 권법 글꼴(WAZA.FON 재배치 칸) 문자열 — 글자 그림으로 읽은 원문(work/text/waza_font_ko.tsv, 2026-11-04 기술 화면·침대 메뉴 실기)
_WK = os.path.join(ROOT, 'work', 'text', 'waza_font_ko.tsv')
if os.path.exists(_WK):
    for _l in open(_WK, encoding='utf-8').read().splitlines()[1:]:
        _k, _j, _v = _l.split('	')
        if _v: FIXES[_k] = (_v, '권법 글꼴 문자열(원문 %s)' % _j)
# 저장 안내 사전(0x26E890~, 매크로 A~z): 일본어 조각 매크로(ません·ています…)는 한국어 어순에 안 맞음 → 매크로를 펼친 완성 문장으로(H 예/아니오 상자·9X 코드만 유지)
# (2026-11-04 실기 «진행되않습니다 않았습니다»·«종료했습니다») — work/text/save_dict_ko.tsv
SAVE_LO, SAVE_HI = 0x26E890, 0x26F400
_SK = os.path.join(ROOT, 'work', 'text', 'save_dict_ko.tsv')
if os.path.exists(_SK):
    for _l in open(_SK, encoding='utf-8').read().splitlines()[1:]:
        _c = _l.split('	')
        if len(_c) > 1 and _c[1]: FIXES[_c[0]] = (_c[1], '저장 안내 — 매크로 펼친 완성 문장')

LINE_EDITS = {   # 키 → [(바꿀 것, 새 것)], 이유 — 버튼 그림 자리(　)·표 맞춤
    'exe:25E1D8': ([('000　　　 버튼으로', '000　　　버튼으로'), ('00　 또는　 버튼을 눌러 주세요.', '00　나　를 눌러 주세요.')],
                   '버튼 그림 자리(　) 위치를 원문 칸과 같게'),
    'exe:25F7C0': ([('　잠자기　　　：', '　잠자기　　：')], '표 맞춤 — «：» 줄 맞춤 칸 수를 원문과 같게'),
    'exe:260798': ([('　중앙의 빨간 원　　　：', '　중앙의 빨간 원　　　　：'), ('　중앙의 주위　　　　：', '　중앙의 주위　　　　　　：'),
                    ('　안쪽 빨강·초록 라인：', '　안쪽 빨강·초록 라인　：')], '표 맞춤 — «：» 줄 맞춤'),
    'exe:260B9C': ([('　행운의 열쇠　：', '　행운의 열쇠　　：'), ('　운명의 실　　：', '　운명의 실　　　：'), ('　승리의 문　　：', '　승리의 문　　　：')],
                   '표 맞춤 — «：» 줄 맞춤'),
    # 버튼 아이콘 앞 글이 원문 칸보다 길어 아이콘이 글자를 덮던 곳(2026-11-04 실기) — 앞 글만 짧게, 칸은 align_icons 가 맞춤
    'exe:25DF6C': ([('물건 뒤나 모퉁이에서', '그늘·모퉁이에서')], '버튼 아이콘 앞 글 9칸 이내'),
    'exe:25E4F8': ([('물건 뒤나 모퉁이에서', '그늘·모퉁이에서'), ('확인할 수 있으며,', '확인하고,')], '버튼 아이콘 앞 글 9칸 이내 · 아이콘 칸 맞춘 줄 폭 19칸'),
    'exe:25E334': ([('오른쪽 아래에', '우하단')], '버튼 아이콘 앞 글 3칸 이내'),
    'exe:25E4AC': ([('오른쪽 아래에', '우하단')], '버튼 아이콘 앞 글 3칸 이내'),
    'exe:260454': ([('오른쪽 아래에', '우하단에')], '버튼 아이콘 앞 글 5칸 이내'),
    'exe:2604BC': ([('오른쪽 아래에', '우하단에')], '버튼 아이콘 앞 글 5칸 이내'),
    'exe:25E674': ([('물건에 대해', '물건에다')], '버튼 아이콘 앞 글 5칸 이내'),
    'exe:25E95C': ([('타이틀 화면에서', '제목 화면에서')], '버튼 아이콘 앞 글 7칸 이내'),
    'exe:25EA2C': ([('타이틀 화면에서', '제목 화면에서')], '버튼 아이콘 앞 글 7칸 이내'),
    # 어른이 청년(료)을 부르는 お兄さん/お兄ちゃん = 총각·손님(2026-11-04 하스피: 애매한 아이는 오빠 유지, 어른은 총각·학생·손님)
    'F1102B003': ([('아, 오빠', '아, 손님')], '가게 점원 お兄さん → 손님'),
    'F1229B098': ([('무섭게 생긴 오빠들이', '무섭게 생긴 총각들이')], '어른 화자 お兄さん → 총각'),
    'F1105B096': ([('오빠가 데루이 씨를', '총각이 데루이 씨를')], '아주머니 화자 お兄ちゃん → 총각'),
    'exe:270714': ([('초승달차기　　　', '초승달차기')], '뒤 전각 공백(버튼 자리 아님) 빼기'),
}

def jong(ch):
    o = ord(ch) - 0xAC00
    return (o % 28) if 0 <= o < 11172 else None
JOSA = [('이에요', '예요'), ('이야', '야'), ('이랑', '랑'), ('이나', '나'), ('으로', '로'), ('은', '는'), ('을', '를'), ('과', '와'), ('이', '가')]
_JR = '|'.join(sorted({x for p in JOSA for x in p}, key=len, reverse=True))
def fit(word, jo):
    j = jong(word[-1])
    for c, v in JOSA:
        if jo in (c, v):
            if c == '으로': return '로' if j in (0, 8) else '으로'
            return v if j == 0 else c
    return jo

MALE_SPK = {'YUKK', 'HINA', 'AKIR'}   # お兄ちゃん 을 부르는 남자 화자(YUKK 실기 확인 · HINA 남자 말투 «頼まねえよ» · AKIR=료)

def replace_term(t, a, b, strict):
    pre = r'(?<![가-힣])' if strict else ''
    def sub(m):
        jo, nx = m.group(1), m.group(2)
        if strict and nx and jong(nx) is not None and not jo and nx not in '의에한랑께씨네만': return m.group(0)      # 뒤가 한글(조사 아님) → 다른 낱말
        if jo is None: return b
        if jo in ('이', '가', '이야', '야') and nx and jong(nx) is not None: return b + jo
        return b + fit(b, jo)
    t = re.sub(pre + re.escape(a) + '(' + _JR + ')?(?=(.?))', sub, t)
    if jong(b[-1]) and not jong(a[-1]):                       # 받침 생김: 서술격 «냐·라는…» 앞에 «이» (키쇼냐→귀장이냐)
        t = re.sub(re.escape(b) + '(?=냐|라는|라고|라면|란|라서|였|예요|여서)', b + '이', t)
    if jong(a[-1]) and not jong(b[-1]):                       # 받침 사라짐: «주원달이라는» → «주위안다라는»
        t = re.sub(re.escape(b) + '이(?=냐|라는|라고|라면|란|라서|었|에요|여서)', b, t)
    return t

def fix_quotes(jp, ko):
    if "'" not in ko and '"' not in ko: return ko
    o, c = ('『', '』') if '『' in jp else ('「', '」')
    for q in ("'", '"'):
        parts = ko.split(q)
        if len(parts) % 2 == 1:
            ko = ''.join(p + ((o if i % 2 == 0 else c) if i < len(parts) - 1 else '') for i, p in enumerate(parts))
    return ko

WAZA_LO, WAZA_HI = 0x26FFD4, 0x271700
def dict_region(off): return BE.MEMO_LO <= off < BE.MEMO_HI or WAZA_LO <= off < WAZA_HI

def widen_literals(jp, ko, memo=False):
    """사전 코드 구역: 원문에 있던 코드 쌍만 반각으로 남기고 나머지 반각 영숫자는 전각.
    메모장은 «영문자로 시작하는 코드(A0~G8)»는 하스피가 다른 줄로 옮겨 쓴 사전 낱말로 보고 그대로 둔다(C0 = 히사카, 2026-11-04)."""
    pool = collections.Counter(p for run in re.findall(r'[\x21-\x7e]+', jp) for p in (run[i:i+2] for i in range(0, len(run) - 1, 2)))
    def run_fix(m):
        r = m.group(); i = 0; out = ''
        while i + 1 < len(r) and (pool[r[i:i+2]] > 0 or (memo and re.fullmatch(r'[A-F][0-9]|G[0-8]', r[i:i+2]))):
            pool[r[i:i+2]] -= 1; out += r[i:i+2]; i += 2
        return out + ''.join(to_wide(ch) for ch in r[i:])
    return re.sub(r'[0-9A-Za-z]+', run_fix, ko)

ENDS = set('을를은는이가에의고며서로도와과께게다요면나지만해때수')
def lines_of(s): return re.split(r'0+', s)
def width(seg): return len(re.sub(r'[A-Za-z0-9]', '', seg))

def reflow(off, jp, ko, W):
    """원문의 «폭이 차서 생긴 낱말 중간 0» 을 베낀 곳은 지우고, 폭 W 넘는 줄은 마지막 띄어쓰기에서 0 으로 접는다."""
    # ① 낱말 중간 0: 한글/부호 사이 홑 0, 원문 같은 순번의 홑 0 앞줄이 폭 W-2 이상(=자동 줄바꿈)이었을 때
    jp_soft = []
    for m in re.finditer(r'(?<!0)0(?!0)', jp):
        prev = jp[:m.start()].rsplit('0', 1)[-1]
        jp_soft.append(width(re.sub(r'^【[^】]*】[A-Z]?', '', prev)) >= W - 3)
    out = []; k = 0; i = 0
    for m in re.finditer(r'0+', ko):
        out.append(ko[i:m.start()]); z = m.group()
        if z == '0':
            soft = k < len(jp_soft) and jp_soft[k]; k += 1
            a, b = ko[m.start() - 1:m.start()], ko[m.end():m.end() + 1]
            if soft and re.match(r'[가-힣]', a) and re.match(r'[.,!?．，。、]', b): z = ''          # 「점칩니다0.」
            elif soft and re.match(r'[가-힣]', a) and re.match(r'[가-힣]', b):
                z = '　' if a in ENDS else ''        # 조사·어미 뒤 = 낱말 경계(띄어쓰기로) / 그 밖 = 낱말 중간(붙임: 던0집니다)
        else: k += 0
        out.append(z); i = m.end()
    out.append(ko[i:]); ko = ''.join(out)
    # ② 긴 줄 접기
    parts = re.split(r'(0+)', ko); res = []
    for p in parts:
        if not p or p[0] == '0': res.append(p); continue
        head = re.match(r'^(【[^】]*】[A-Z]?|[A-Z][^】]*】[A-Z])', p)
        h = head.group() if head else ''; body = p[len(h):]
        segs = ['']
        for w in re.split(r'(?<=[ 　])', body):
            if width(segs[-1] + w.rstrip(' 　')) > W and segs[-1].strip(' 　'): segs[-1] = segs[-1].rstrip(' 　'); segs.append(w)
            else: segs[-1] += w
        res.append(h + '0'.join(segs))
    return ''.join(res)

SLOT_WARN = []
HELP_WARN = []
HELP_SHORT = collections.defaultdict(list)
_HS = os.path.join(ROOT, 'work', 'text', 'help_short.tsv')
if os.path.exists(_HS):
    for _l in open(_HS, encoding='utf-8').read().splitlines()[1:]:
        _c = _l.split('\t')
        HELP_SHORT[_c[0]].append((int(_c[1]), _c[2], _c[3]))
ICON_RUN = re.compile(r'(?<!　)　　(?![　：])')          # 원문 버튼 그림 자리 = 딱 전각 공백 둘(표 맞춤 «　：» 제외)
KO_RUN = re.compile(r'　{2,}(?!：)')
def align_icons(jp, ko):
    """버튼 아이콘은 원문 조각의 «전각 공백 둘» 칸에 고정으로 그려진다(2026-11-04 실기 R·A 아이콘이 글자를 덮음).
    번역 조각의 공백 줄(같은 순번)을 원문 칸 c..c+1 을 정확히 덮도록 늘리고 줄인다. 앞 글이 c 칸을 넘으면 알림.
    돌려줌: (새 글, 알림 목록)"""
    notes = []
    h = HEAD.match(ko); head = h.group() if h else ''; ps = ko[len(head):].split('0')
    jh = HEAD.match(jp); jps = (jp[len(jh.group()):] if jh else jp).split('0')
    for i, jpp in enumerate(jps):
        targets = [width(jpp[:m.start()]) for m in ICON_RUN.finditer(jpp)]
        if not targets or i >= len(ps): continue
        runs = list(KO_RUN.finditer(ps[i]))
        if len(runs) != len(targets):
            notes.append('조각 %d 버튼 자리 %d ≠ 원문 %d' % (i, len(runs), len(targets))); continue
        p = ps[i]
        for m, c in reversed(list(zip(runs, targets))):
            s = width(p[:m.start()])
            if s > c: notes.append('조각 %d 버튼 자리 앞 글 %d칸 > 원문 %d칸' % (i, s, c)); continue
            p = p[:m.start()] + '　' * (c + 2 - s) + p[m.end():]
        ps[i] = p
    return head + '0'.join(ps), notes

def help_fit(jp, ko):
    """도움말 그리기(0x0C0E2514): 0 마다 조각 하나를 52 B 줄 버퍼에 모아 그림 — 조각 i 는 줄 i//2, 칸 (i%2)×19 격자.
    조각 배열은 20칸(매크로 펼친 뒤 합계)·버튼 안내/아이콘은 원문 격자에 고정 → 조각 수는 원문과 같아야 한다.
    여기선 «19칸 넘는 짝수 조각 + 바로 뒤 홀수 조각이 빔» 이면 19칸 뒤를 홀수 조각으로 옮긴다(화면 모양 같음, 버퍼 안전)."""
    notes = []
    h = HEAD.match(ko); head = h.group() if h else ''; body = ko[len(head):]
    jh = HEAD.match(jp); jbody = jp[len(jh.group()):] if jh else jp
    ps = body.split('0'); jn = jbody.count('0')
    if len(ps) - 1 != jn: notes.append('조각 수 %d ≠ 원문 %d' % (len(ps) - 1, jn))
    for i in range(0, len(ps) - 1, 2):
        if width(ps[i]) > ROW_W and ps[i + 1] == '':
            ps[i], ps[i + 1] = ps[i][:ROW_W], ps[i][ROW_W:]
    for i, p in enumerate(ps):
        if len(p.encode('utf-8')) and len(p) > 25: notes.append('조각 %d 이 %d칸(50 B 넘음 — 줄 버퍼 크래시)' % (i, len(p)))
    jps = jbody.split('0')
    rw = lambda L, i: ((ROW_W + width(L[i + 1])) if i + 1 < len(L) and L[i + 1] else width(L[i])) if i < len(L) else 0
    for i in range(0, len(ps), 2):
        lim = max(21, rw(jps, i))                                  # 원문 줄 폭(꼬리 포함)까지는 원래 화면 그대로
        if rw(ps, i) > lim: notes.append('줄 %d 폭 %d칸 > %d' % (i // 2, rw(ps, i), lim))
    return head + '0'.join(ps), notes
HEAD = re.compile(r'^(【[^】]*】[A-Z]?|[A-Z])')
ROW_W, TAIL_W = 19, 2
SENT_END = set('．。.!?！？…」』）)')
def pair_rows(body):
    """도움말 글 그리기 규칙(2026-11-04 기술 화면 실기): 0 으로 나눈 조각을 둘씩 한 줄 — 짝수 조각은 0칸, 홀수 조각은 19칸부터."""
    ps = body.split('0')
    return [(ps[i], ps[i + 1] if i + 1 < len(ps) else '') for i in range(0, len(ps), 2)]
def pair_model(jp):
    """원문이 «짝 조각» 꼴인지 — 홀수 조각(꼬리)이 전부 4칸 이하"""
    h = HEAD.match(jp); body = jp[len(h.group()):] if h else jp
    return all(width(t) <= 4 for _, t in pair_rows(body))
def pair_ok(ko):
    h = HEAD.match(ko); body = ko[len(h.group()):] if h else ko
    return all(width(r) <= ROW_W and width(t) <= TAIL_W for r, t in pair_rows(body))
def slot_pos(s):
    """버튼 그림 자리(전각 공백 둘) 의 (줄, 칸) 목록 — 꼬리 조각은 19칸부터"""
    h = HEAD.match(s); body = s[len(h.group()):] if h else s; out = []
    for i, (r, t) in enumerate(pair_rows(body)):
        for j, piece in ((0, r), (ROW_W, t)):
            for m in re.finditer(r'　{2,}', piece): out.append((i, j + m.start()))
    return out
SLOT = ''
def help_layout(ko, targets=None):
    """번역 글을 «줄 19칸 · 줄 끝 00 · 문장 끝 1~2글자는 꼬리»로 다시 짠다.
    홑 0: 앞이 문장 끝 부호면 줄 끝, 아니면 원문 자동 줄바꿈 자리(이어 씀) · 0 여러 개(k) = 줄 끝 k//2 번(빈 줄 유지).
    targets = 원문 버튼 그림 자리 (줄, 칸) — 아이콘이 원문 자리에 고정으로 그려지므로 번역의 전각 공백 둘(이상)을 그 자리에 맞춘다.
    돌려줌: (새 글, 맞춤 실패 사유 또는 '')"""
    h = HEAD.match(ko); head = h.group() if h else ''; body = ko[len(head):]
    body = re.sub(r' ?　(?: ?　)+ ?', SLOT, body)                 # 전각 공백 둘 이상 = 버튼 그림 자리
    nslot = body.count(SLOT)
    if targets is not None and nslot != len(targets): return None, '버튼 자리 수 %d ≠ 원문 %d' % (nslot, len(targets))
    lines = [['', None]]                                     # [본문, 꼬리(19칸~) 또는 None]
    def end_row(): lines.append(['', None])
    for p in re.split(r'(0+)', body):
        if not p: continue
        cur = lines[-1]
        if p[0] != '0':
            if cur[1] is not None: cur[1] += p
            else: cur[0] += p
            continue
        if len(p) == 1:
            prev = cur[0][-1:]
            if cur[1] is not None: end_row()                     # 꼬리 뒤 0 = 줄 끝
            elif not prev or prev in SENT_END: end_row()
            elif width(cur[0].replace(SLOT, '　　')) >= 12:          # 원문 자동 줄바꿈 자리를 베낀 0 → 이어 씀
                if prev not in ' 　' + SLOT: cur[0] += '　' if prev in ENDS else ''
            else: cur[1] = ''                                    # 짧은 조각 뒤 0 = 19칸으로(버튼 안내 두 칸 목록)
        else:
            end_row()
            for _ in range(len(p) // 2 - 1): end_row()
    while lines and lines[-1] == ['', None]: lines.pop()
    W_ = lambda x: width(x.replace(SLOT, '　　'))
    rows = []; si = 0; err = ''
    for ln, ltail in lines:
        ln = ln.strip(' 　')
        rows.append(['', '']); start = len(rows) - 1
        if not ln and not ltail: continue
        toks = []
        for w in [w for w in re.split(r'[ 　]', ln) if w]:
            for k, piece in enumerate(re.split('(' + SLOT + ')', w)):
                if piece: toks.append((piece, k == 0))
        for piece, sp in toks:
            r = rows[-1]; side = 1 if r[1] else 0
            if piece == SLOT:
                tr, tc = targets[si] if targets else (len(rows) - 1, None); si += 1
                while len(rows) - 1 < tr: rows.append(['', ''])
                if len(rows) - 1 != tr: err = err or '버튼 자리 줄 %d → 번역은 %d줄째에야' % (tr, len(rows) - 1); tc = None
                r = rows[-1]
                if tc is None: r[side] += ('　' if sp and r[side] else '') + SLOT; continue
                if tc >= ROW_W:
                    if W_(r[1]) > tc - ROW_W or W_(r[0]) > ROW_W: err = err or '꼬리 버튼 자리 칸 %d 넘침' % tc
                    r[1] += '　' * max(0, tc - ROW_W - W_(r[1])) + SLOT
                else:
                    if W_(r[0]) > tc: err = err or '버튼 자리 (%d,%d) 앞 글이 %d칸' % (tr, tc, W_(r[0]))
                    r[0] += '　' * max(0, tc - W_(r[0])) + SLOT
                continue
            cur = r[side]; glue = (not sp) or cur.endswith(SLOT) or not cur
            cand = cur + ('' if glue else '　') + piece
            lim = ROW_W if side == 0 else 99
            if W_(cand) <= lim: r[side] = cand; continue
            rows.append(['', piece])  if False else rows.append([piece, ''])
            while W_(rows[-1][0]) > ROW_W: x = rows[-1][0]; rows[-1][0] = x[:ROW_W]; rows.append([x[ROW_W:], ''])
        if ltail is not None:
            rows[-1][1] += ltail.strip(' ')
            continue
        last = rows[-1]
        if len(rows) - 1 > start and not last[1] and W_(last[0]) <= TAIL_W and all(c in SENT_END for c in last[0]):
            rows.pop(); rows[-1][1] = last[0]
        elif not last[1] and W_(last[0]) == ROW_W and last[0][-1] in SENT_END: last[0], last[1] = last[0][:-1], last[0][-1]
    if targets is not None and si != len(targets): err = err or '버튼 자리 일부 못 놓음'
    out = head + ''.join(a + '0' + b + '0' for a, b in rows)
    return out.replace(SLOT, '　　'), err

def _jong(ch): return '가' <= ch <= '힣' and (ord(ch) - 0xAC00) % 28 != 0
def _jong_l(ch): return '가' <= ch <= '힣' and (ord(ch) - 0xAC00) % 28 == 8
JOSA_PAIRS = [('이', '가'), ('을', '를'), ('은', '는'), ('과', '와')]
def josa_after_codes(d):
    """사전 코드·매크로(메모장 0x27CED0 · 기술 설명 0x293980 · 저장 안내 0x2932F8) 뒤 조사를 «펼친 낱말» 받침에 맞춤.
    (2026-11-04 실기 «파일가»·«가능성가» → 전수 검사에서 톰가·찰리은·첸 대인와·문신를 등 발견) 출력 TSV 를 고쳐 쓰고 로그 줄을 돌려줌."""
    files = sorted(glob.glob(os.path.join(OUT, 'sm1_*.tsv')))
    rows = {}
    for f in files:
        for ln in open(f, encoding='utf-8').read().splitlines()[1:]:
            c = ln.split('\t')
            if len(c) > 4: rows[c[0]] = c[4]
    def ptab(a, n):
        return [rows.get('exe:%06X' % (struct.unpack_from('<I', d, a + 4 * i)[0] - BE.BASE)) or '' for i in range(n)]
    SAVE = dict(zip([chr(65 + i) for i in range(26)] + [chr(97 + i) for i in range(26)], ptab(0x2932F8, 52)))
    MEMO = ptab(0x27CED0, 159); WAZA = ptab(0x293980, 39)
    val = lambda c: int(c) if c.isdigit() else ord(c) - 55
    def last_char(w, depth=0):            # 펼친 낱말의 마지막 한글(저장 매크로는 안쪽까지)
        w = w.rstrip('　 ')
        if depth < 4 and w and w[-1] in SAVE and SAVE[w[-1]]: return last_char(SAVE[w[-1]], depth + 1)
        w = w.rstrip('」』］）')
        return w[-1] if w else ''
    def code_re(off):
        if 0x26E890 <= off < 0x26F400: return re.compile(r'(?<!9)([A-Za-z])'), lambda m: SAVE.get(m.group(1), '')
        if 0x264000 <= off < 0x26A100: return re.compile(r'(?=[1-9A-I])([0-9A-I][0-9])|0[0-9]'), lambda m: MEMO[val(m.group(1)[0]) * 10 + int(m.group(1)[1]) - 10] if val(m.group(1)[0]) * 10 + int(m.group(1)[1]) - 10 < 159 else ''
        if 0x26FFD4 <= off < 0x271700: return re.compile(r'([0-9]{2})'), lambda m: WAZA[int(m.group(1))] if int(m.group(1)) < 39 else ''
        return None, None
    log = []
    for f in files:
        lines = open(f, encoding='utf-8').read().splitlines(); ch = False
        for i, ln in enumerate(lines[1:], 1):
            c = ln.split('\t')
            if len(c) < 5 or not c[0].startswith('exe:') or not c[4]: continue
            rx, word = code_re(int(c[0][4:], 16))
            if not rx: continue
            ko = c[4]; out = []; pos = 0
            for m in rx.finditer(ko):
                if m.group(1) is None: continue        # 0n = 줄 앞 제어
                w = word(m)
                if not w: continue
                k = m.end(); br = ''
                while k < len(ko) and ko[k] in '」』］）': br += ko[k]; k += 1
                p = last_char(w)
                if not ('가' <= p <= '힣'): continue
                for a, b in JOSA_PAIRS:
                    for cur, want in ((b, a), (a, b)):
                        if ko.startswith(cur, k) and (k + 1 >= len(ko) or not ('가' <= ko[k + 1] <= '힣')):
                            right = a if _jong(p) else b
                            if cur != right: out.append((k, cur, right))
                if ko.startswith('로', k) and _jong(p) and not _jong_l(p): out.append((k, '로', '으로'))
                if ko.startswith('으로', k) and (not _jong(p) or _jong_l(p)): out.append((k, '으로', '로'))
            if not out: continue
            n = ko
            for k, cur, right in sorted(set(out), reverse=True): n = n[:k] + right + n[k + len(cur):]
            log.append('%s\t%s\t사전 코드 뒤 조사 받침 맞춤\t%s\t%s' % (os.path.basename(f)[:-4], c[0], ko, n))
            c[4] = n; lines[i] = '\t'.join(c); ch = True
        if ch: open(f, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines) + '\n')
    print('사전 코드 뒤 조사 맞춤 %d줄' % len(log))
    return log

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    src = sys.argv[1]; skip = set(sys.argv[3:]) if len(sys.argv) > 2 and sys.argv[2] == '--skip' else set()
    d = open(BE.SRC, 'rb').read()
    info = {t: (refs, ln, room, s) for t, refs, ln, s, room in exe_strings.main(BE.SRC, os.path.join(ROOT, 'work', 'check', 'exe_strings.tsv'))}
    help_set = {struct.unpack_from('<I', d, p)[0] - BE.BASE for a, b in BE.ORDERED_TABLES for p in range(a, b, 4)}
    os.makedirs(OUT, exist_ok=True)
    for f in glob.glob(os.path.join(OUT, '*.tsv')): os.remove(f)
    log = ['file\tkey\twhy\tbefore\tafter']
    for f in sorted(glob.glob(os.path.join(ROOT, 'work', 'text', 'tsv', '*.tsv'))):
        base = os.path.basename(f)[:-4]
        if base in skip:
            open(os.path.join(OUT, base + '.tsv'), 'w', encoding='utf-8', newline='\n').write(open(f, encoding='utf-8').read())
            log.append('%s\t-\t건너뜀(하스피 다시 줌)\t\t' % base); continue
        cand = sorted(glob.glob(os.path.join(src, base + '*.tsv')), key=lambda p: ('_풀이' not in p, p))   # 풀이판(사전 코드 풀어 쓴 꼴)이 있으면 그것
        u = cand[0] if cand else f            # 하스피 파일이 아직 없는 묶음(보충 sm1_084: 초안 번역·권법 글꼴 원문 그대로) → 원본 묶음 그대로
        lines = [l.rstrip('\r\n') for l in open(u, encoding='utf-8-sig')]
        decoded = lines[0].split('\t')[4:5] == ['jp_풀이']
        out = ['key\tspeaker\tcount\tjp\tko'] if decoded else [lines[0]]
        for ln in lines[1:]:
            c = ln.split('\t')
            jp_rule = c[3]
            if decoded:                       # ‹0n› → 0n(줄 앞 제어 그대로) · 〔낱말〕 → 낱말(풀어 쓴 번역)
                jp_rule = c[4]
                ko = re.sub(r'‹(0[0-9])›', r'\1', c[5]); ko = re.sub(r'〔([^〕]*)〕', r'\1', ko)
                assert '‹' not in ko and '〔' not in ko, (c[0], ko)
                c = c[:4] + [ko]
            key, jp, ko = c[0], c[3], c[4]
            before = ko; why = []
            if not ko.strip() and key in FIXES: ko = FIXES[key][0]         # 빈 번역에도 손 교정(권법 글꼴 등) 적용
            if ko.strip():
                if c[1] in MALE_SPK and '오빠' in ko:            # お兄ちゃん = 남자 화자면 «형»(2026-11-04 하스피 실기 «오빠 아니고 형이야»)
                    n = replace_term(ko, '오빠', '형', False)
                    n = re.sub(r'형(?=다[.!?…~,]|다$)', '형이', n)
                    if n != ko: ko = n; why.append('남자 화자 오빠→형')
                for trig, a, b, strict in GLOSSARY:
                    if (trig in jp or trig in jp_rule) and a in ko:
                        n = replace_term(ko, a, b, strict)
                        if n != ko: ko = n; why.append('이름 %s→%s' % (a, b))
                n = fix_quotes(jp, ko)
                if n != ko: ko = n; why.append('반각 따옴표→원문 괄호')
                if '『' in jp and '「' not in jp and '『' not in ko and ko.count('「') == jp.count('『'):
                    ko = ko.replace('「', '『').replace('」', '』'); why.append('「」→원문 『』')
                if key.startswith('exe:') and 0x26E890 <= int(key[4:], 16) < 0x26F400:   # 저장 안내 사전(포인터 표 0x2932F8, A~z 매크로)
                    n = re.sub(r'D(］?)([가는를와])', lambda m: 'D' + m.group(1) + {'가': '이', '는': '은', '를': '을', '와': '과'}[m.group(2)], ko)
                    if n != ko: ko = n; why.append('매크로 D=파일 뒤 조사 받침(파일가→파일이, 2026-11-04 실기)')
                if key in FIXES: ko, r = FIXES[key]; why.append(r)
                if key in LINE_EDITS:
                    eds, r = LINE_EDITS[key]
                    for a_, b_ in eds:
                        assert a_ in ko, (key, a_); ko = ko.replace(a_, b_)
                    why.append(r)
                if key.startswith('exe:'):
                    off = int(key[4:], 16)
                    if off in info:
                        k2 = BE.prep(info[off][3], ko); k0 = k2
                        if '　　' in info[off][3] and key not in FIXES:          # 손 교정은 칸을 맞춰 썼음
                            n = re.sub(r'(?<=　　)　(?=[^　])', '', k2) if '　　　' not in info[off][3] else k2
                            if n != k2: why.append('버튼 그림 자리 옆 띄어쓰기 빼기'); k2 = n
                        if dict_region(off):
                            n = widen_literals(info[off][3], k2, BE.MEMO_LO <= off < BE.MEMO_HI)
                            if n != k2: why.append('사전 코드 구역 반각 숫자·영문→전각')
                            k2 = n
                        elif not re.search(r'[0-9A-Za-z]', info[off][3]) and re.search(r'[0-9A-Za-z]', k2):
                            k2 = re.sub(r'[0-9A-Za-z]', lambda m: to_wide(m.group()), k2); why.append('원문에 반각 영숫자 없음 → 전각')
                        elif off in help_set and '0' in info[off][3]:
                            n, notes = help_fit(info[off][3], k2)
                            if n != k2: why.append('도움말 19칸 넘는 줄 뒤를 19칸 조각으로(조각 수·위치 원문대로)'); k2 = n
                            if key in HELP_SHORT:                  # 줄인 줄(work/text/help_short.tsv, 하스피 «문장줄여줘» 2026-11-04)
                                h_ = HEAD.match(k2); hd = h_.group() if h_ else ''; ps = k2[len(hd):].split('0')
                                for r, m_, t_ in HELP_SHORT[key]: ps[2 * r] = m_; ps[2 * r + 1] = t_
                                k2 = hd + '0'.join(ps); why.append('도움말 넓은 줄 줄임(%d줄)' % len(HELP_SHORT[key]))
                            n, an = align_icons(info[off][3], k2)      # 버튼 아이콘 칸 = 원문 칸(2026-11-04 실기)
                            if n != k2: why.append('버튼 그림 자리를 원문 칸에'); k2 = n
                            k2, notes = help_fit(info[off][3], k2); notes = an + notes
                            for x in notes: HELP_WARN.append('%s	%s	%s' % (key, x, k2))
                        elif '0' in info[off][3] and re.match(r'^(【|[A-Z])', info[off][3]):
                            jl = [width(re.sub(r'^【[^】]*】[A-Z]?', '', x)) for x in lines_of(info[off][3])]
                            W = 20 if off in help_set else max(20, max(jl))
                            n = reflow(off, info[off][3], k2, W)
                            if n != k2: why.append('줄 다시 접기(폭 %d)' % W)
                            k2 = n
                        if k2 != k0: ko = k2          # 실행 파일 쪽 교정이 있을 때만 전각화된 꼴로 씀(아니면 하스피 원문 그대로)
            if ko != before: log.append('%s\t%s\t%s\t%s\t%s' % (base, key, ' · '.join(why), before, ko))
            c[4] = ko; out.append('\t'.join(c))
        open(os.path.join(OUT, base + '.tsv'), 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
    log += josa_after_codes(d)
    open(os.path.join(OUT, 'merge_log.tsv'), 'w', encoding='utf-8', newline='\n').write('\n'.join(log) + '\n')
    open(os.path.join(ROOT, 'work', 'check', 'help_fit.tsv'), 'w', encoding='utf-8', newline='\n').write('key\tnote\ttext\n' + ''.join(x + '\n' for x in HELP_WARN))
    print('도움말 알림 %d (work/check/help_fit.tsv)' % len(HELP_WARN))
    c = collections.Counter(w.split(' ')[0] if w.startswith('이름') else w for l in log[1:] for w in l.split('\t')[2].split(' · '))
    for k, n in c.most_common(): print('%5d  %s' % (n, k))
    print('바꾼 줄 %d → %s' % (len(log) - 1, OUT))

if __name__ == '__main__':
    main()
