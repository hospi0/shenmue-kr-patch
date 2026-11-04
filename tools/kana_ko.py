# -*- coding: utf-8 -*-
"""가나 → 한글 근사 표기(하스피 규칙: か행 ㅋ·た행 ㅌ·つ 츠, 장음 생략) — 이름 표기 검사용."""
import re

def _h(ch):
    return chr(0x3041 + ord(ch) - 0x30A1) if 'ァ' <= ch <= 'ヶ' else ch

T = {}
def _row(cons, vs):
    for k, v in zip(cons, vs): T[k] = v
_row('あいうえお', ['아', '이', '우', '에', '오'])
_row('かきくけこ', ['카', '키', '쿠', '케', '코']); _row('がぎぐげご', ['가', '기', '구', '게', '고'])
_row('さしすせそ', ['사', '시', '스', '세', '소']); _row('ざじずぜぞ', ['자', '지', '즈', '제', '조'])
_row('たちつてと', ['타', '치', '츠', '테', '토']); _row('だぢづでど', ['다', '지', '즈', '데', '도'])
_row('なにぬねの', ['나', '니', '누', '네', '노']); _row('はひふへほ', ['하', '히', '후', '헤', '호'])
_row('ばびぶべぼ', ['바', '비', '부', '베', '보']); _row('ぱぴぷぺぽ', ['파', '피', '푸', '페', '포'])
_row('まみむめも', ['마', '미', '무', '메', '모']); _row('やゆよ', ['야', '유', '요'])
_row('らりるれろ', ['라', '리', '루', '레', '로']); _row('わを', ['와', '오'])
Y = {'ゃ': 'ㅑ', 'ゅ': 'ㅠ', 'ょ': 'ㅛ'}
JUNG = 'ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ'
CHO = 'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ'

def _dec(s):
    o = ord(s) - 0xAC00; return o // 588, (o % 588) // 28, o % 28
def _comp(c, j, t=0): return chr(0xAC00 + c * 588 + j * 28 + t)

def to_ko(kana):
    s = [_h(c) for c in kana]
    out = []
    i = 0
    while i < len(s):
        c = s[i]
        if c in 'ゃゅょ' and out:
            ch, ju, jo = _dec(out[-1]); out[-1] = _comp(ch, JUNG.index(Y[c])); i += 1; continue
        if c == 'ん' and out:
            ch, ju, jo = _dec(out[-1]); out[-1] = _comp(ch, ju, 4); i += 1; continue
        if c == 'っ' and out:
            ch, ju, jo = _dec(out[-1]); out[-1] = _comp(ch, ju, 19); i += 1; continue
        if c == 'ー': i += 1; continue
        if c in 'ぁぃぅぇぉ' and out:
            v = {'ぁ': 'ㅏ', 'ぃ': 'ㅣ', 'ぅ': 'ㅜ', 'ぇ': 'ㅔ', 'ぉ': 'ㅗ'}[c]
            ch, ju, jo = _dec(out[-1]); out[-1] = _comp(ch, JUNG.index(v)); i += 1; continue
        if c in T: out.append(T[c])
        else: return None
        i += 1
    # 장음 생략: 오우→오, 에이→에(이름 관행), 우우→우
    r = ''.join(out)
    return r

def variants(ko):
    """규칙 위반 꼴: 첫 글자 ㅋ→ㄱ·ㅌ→ㄷ, 츠→쓰/즈/쯔"""
    out = set()
    if ko and '가' <= ko[0] <= '힣':
        ch, ju, jo = _dec(ko[0])
        if CHO[ch] == 'ㅋ': out.add(_comp(CHO.index('ㄱ'), ju, jo) + ko[1:])
        if CHO[ch] == 'ㅌ': out.add(_comp(CHO.index('ㄷ'), ju, jo) + ko[1:])
    if '츠' in ko:
        for v in ('쓰', '쯔', '즈'): out.add(ko.replace('츠', v))
    return out - {ko}
