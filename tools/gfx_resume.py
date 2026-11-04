# -*- coding: utf-8 -*-
"""중단·저장 화면 글자판(RESUME00 / RESUME02) 한글 미리보기 (2026-11-03).

게임은 MISC/RESUME.DAT 의 «글자 → 그림판 좌표(x,y,w,h)» 표로 문장을 조립한다(6 B 항목, 글자 코드 u16 LE).
  표0(@0x000, 71칸) → RESUME00 (중단 화면 0~13번 문장) · 표1(@0x1B0, 62항목) → RESUME02 (저장 화면 14~20번 + 낱말 그림)
여기서는 ① 한글 낱자를 원본 글자 높이(22)로 새 그림판에 채우고 ② 그 낱자로 문장을 조립해 미리보기만 만든다.
RESUME.DAT 표·문장 다시 쓰기와 PVR 재포장은 하스피 확인 뒤.
"""
import os, sys, json
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import gfx_kr as G

MSG0 = ['게임을 일시 중단합니다.', '스타트 메뉴의 「Cn」을 고르면,', '중단한 곳부터 게임을 다시 시작할 수 있습니다.',
        '세이브하고 있습니다.', '메모리 카드를 뽑거나 꽂거나', '전원을 끄지 마세요.']
MSG1 = ['선택해 주세요.', '세이브해도 괜찮습니까?', '덮어써도 괜찮습니까?', '세이브할 파일을']

def norm(m):
    """RESUME 문장은 전부 2바이트 — 반각 공백·부호를 전각으로(「Cn」 은 그대로)"""
    return m.replace(' ', '　').replace('.', '．').replace(',', '，').replace('?', '？').replace('!', '！')

def glyph_set(msgs):
    msgs = [norm(m) for m in msgs]
    return sorted(set(''.join(m.replace('Cn', '') for m in msgs)) - {' ', '　', '「', '」'})   # 「」 는 원본 칸 그대로

# 원본 표에서 읽은 특수 칸(RESUME.DAT) — 낱자 채울 때 피하고, 낱말·문장 그림은 같은 칸에 한글로
SPEC = {
    'RESUME00__00_re_fix1': dict(font='mincho_r', wfont='mincho_r', area=(0, 0, 242, 154), keep=[(154, 66, 241, 88), (242, 0, 256, 154)],
        words=[((0, 154, 255, 187), '세이브했습니다!'), ((0, 187, 255, 220), '게임을 종료해 주세요.'), ((0, 220, 255, 253), '게임을 종료해 주세요.')]),
    'RESUME02__00_re_fix2': dict(font='mincho', wfont='gothic', area=(0, 0, 242, 66), keep=[(242, 0, 256, 66)],
        words=[((70, 66, 124, 88), '게임'), ((143, 66, 191, 88), '일시'), ((0, 88, 66, 110), '스타트'), ((70, 88, 124, 110), '세이브'),
               ((143, 88, 195, 110), '일시'), ((0, 110, 66, 132), '파일'), ((66, 110, 132, 132), '클리어'),
               ((0, 132, 242, 176), '파일이 없습니다.'), ((148, 198, 240, 242), '파일')]),
}

def _clash(x, y, w, h, rects):
    return any(x < r[2] and r[0] < x + w and y < r[3] and r[1] < y + h for r in rects)

def build_atlas(src_name, chars, H=22):
    sp = SPEC[src_name]; font = sp['font']
    src = Image.open(os.path.join(G.ORIG, src_name + '.png')).convert('RGBA')
    ink = sorted([p for p in src.getdata() if p[3] > 200], key=G._lum)
    fill, stroke = ink[-len(ink) // 10 - 1][:3], ink[len(ink) // 20][:3]
    atlas = src.copy()
    ax0, ay0, ax1, ay1 = sp['area']
    atlas.paste((0, 0, 0, 0), (ax0, ay0, ax1, ay1))
    for r in sp['keep']: atlas.alpha_composite(src.crop(r), (r[0], r[1]))
    x, y = ax0, ay0; table = {}
    f = ImageFont.truetype(G.FONTS[font], int(H * 0.86) * 4)
    for c in chars:
        g = Image.new('RGBA', (H * 8, H * 4), (0, 0, 0, 0)); d = ImageDraw.Draw(g)
        bb = f.getbbox('가')
        d.text((8, (H * 4 - (bb[3] - bb[1])) / 2 - bb[1]), c, font=f, fill=fill + (255,), stroke_width=4, stroke_fill=stroke + (255,))
        cw = int(d.textlength(c, font=f) + 16) // 4 + 1
        g = g.resize((H * 2, H), Image.LANCZOS).crop((0, 0, cw, H))
        while True:
            if x + cw > ax1: x = ax0; y += H
            if y + H > ay1: raise SystemExit('%s: 낱자 칸 모자람' % src_name)
            if _clash(x, y, cw, H, sp['keep']): x += 2; continue
            break
        atlas.alpha_composite(g, (x, y)); table[c] = (x, y, cw, H); x += cw
    for (x0, y0, x1, y1), t in sp['words']:            # 낱말·문장 그림 칸: 원본 색으로 한글
        cell = src.crop((x0, y0, x1, y1)); ci = sorted([p for p in cell.getdata() if p[3] > 200], key=G._lum)
        wf, ws = (ci[-len(ci) // 10 - 1][:3], ci[len(ci) // 20][:3]) if ci else (fill, stroke)
        ib = cell.split()[3].getbbox() or (0, 0, x1 - x0, y1 - y0)      # ★칸이 아니라 «칸 안 원본 글자» 높이에 맞춤
        gy0, gh = y0 + ib[1], ib[3] - ib[1]
        atlas.paste((0, 0, 0, 0), (x0, y0, x1, y1))
        img, tw = G.draw_line(t, G.FONTS[sp['wfont']], x1 - x0 - 2, gh, wf, ws, 1)
        atlas.alpha_composite(img.crop((0, 0, min(tw + 2, x1 - x0 - 2), gh)), (x0 + max(1, (x1 - x0 - tw) // 2), gy0))
    return src, atlas, table, y + H

KEEP_GLYPH = {'RESUME00__00_re_fix1': {'「': (242, 44, 13, 22), '」': (242, 66, 14, 22), '□': (154, 66, 87, 22)}}

def compose(atlas, table, msg, H=22):
    w = sum(table[c][2] if c in table else 8 for c in msg.replace('Cn', '□'))
    im = Image.new('RGBA', (w + 4, H), (0, 0, 0, 0)); x = 2
    for c in msg.replace('Cn', '□'):
        if c in table:
            gx, gy, gw, gh = table[c]; im.alpha_composite(atlas.crop((gx, gy, gx + gw, gy + gh)), (x, 0)); x += gw
        else: x += 8
    return im

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    out = []
    for src_name, msgs in (('RESUME00__00_re_fix1', MSG0), ('RESUME02__00_re_fix2', MSG1)):
        chars = glyph_set(msgs)
        src, atlas, table, used_h = build_atlas(src_name, chars)
        atlas.save(os.path.join(G.NEW, src_name + '_glyphs.png'))
        json.dump({c: v for c, v in table.items()}, open(os.path.join(G.NEW, src_name + '_table.json'), 'w', encoding='utf-8'), ensure_ascii=False)
        table.update(KEEP_GLYPH.get(src_name, {}))
        out.append((src_name, src, atlas, [(m, compose(atlas, table, norm(m))) for m in msgs], len(chars)))
        atlas.save(os.path.join(G.NEW, src_name + '.png'))   # gfx_pack 이 넣는 이름
    lab = ImageFont.truetype('C:/Windows/Fonts/malgunbd.ttf', 16)
    W = 1100; H = 40 + sum(260 * 2 + 30 + len(ms) * 50 + 40 for *_, ms, _ in out)
    sh = Image.new('RGB', (W, H), (25, 25, 30)); d = ImageDraw.Draw(sh); y = 8
    for name, src, atlas, ms, n in out:
        d.text((8, y), '%s — 한글 낱자 %d자 (원래 칸 수 안)  왼쪽 원본 글자판 | 오른쪽 한글 글자판' % (name, n), font=lab, fill=(255, 220, 80)); y += 24
        for k, im in enumerate((src, atlas)):
            bg = G.checker(im.size); bg.alpha_composite(im); sh.paste(bg.resize((im.size[0] * 2, im.size[1] * 2), Image.NEAREST).convert('RGB'), (8 + k * 540, y))
        y += src.size[1] * 2 + 10
        d.text((8, y), '조립 미리보기(게임처럼 낱자를 이어 붙임, 「Cn」 자리는 원본 Continue 그림)', font=lab, fill=(150, 220, 255)); y += 24
        for m, im in ms:
            bg = Image.new('RGBA', im.size, (30, 30, 90, 255)); bg.alpha_composite(im)
            sh.paste(bg.resize((im.size[0] * 2, im.size[1] * 2), Image.NEAREST).convert('RGB'), (8, y)); y += im.size[1] * 2 + 6
        y += 20
    sh = sh.crop((0, 0, W, y))
    os.makedirs(G.PREV, exist_ok=True); p = os.path.join(G.PREV, '09_중단저장화면.png'); sh.save(p); print(p)

if __name__ == '__main__':
    main()
