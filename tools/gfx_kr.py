# -*- coding: utf-8 -*-
"""쉔무 그림 글자 한글화 — 미리보기 생성(2026-11-03, 하스피 «그림한글화 다 해서 마이파일스에 미리보기»)

원본 = work/gfx/orig/<텍스처>.png (PyPVR -flip 으로 푼 RGBA, 똑바로 선 것)
새것 = work/gfx/new/<텍스처>.png  (같은 크기·같은 알파 구조)
미리보기 = my files/그림미리보기/<묶음>.png  (왼쪽 원본 | 오른쪽 한글, 체크 무늬 + 어두운 바탕)

그리는 법(글자만 있는 텍스처): 원본 알파의 «잉크 행 묶음» = 원문 줄 → 한글 줄을 같은 줄 상자에,
  정렬(왼쪽/가운데)·글자 색·테두리 색·테두리 두께·안티 여부를 원본에서 재서 그대로. 세로쓰기는 글자를 세로로 쌓음.
※ 재포장(PVR 인코딩·GZ·디스크)은 하스피 확인 뒤 — 여기선 PNG 만.
"""
import os, sys, glob, re
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
ORIG = os.path.join(ROOT, 'work', 'gfx', 'orig')
NEW = os.path.join(ROOT, 'work', 'gfx', 'new')
PREV = os.path.join(ROOT, 'my files', '그림미리보기')
F = 'C:/claude/utils/font/'
FONTS = {
    'brush': F + 'songmyung/SongMyung-Regular.ttf',          # 로딩 지명·날짜(예서체 느낌)
    'button': F + 'dohyeon/DoHyeon-Regular.ttf',             # 옵션·메뉴 버튼(굵은 고딕 + 테두리)
    'heavy': F + 'blackhansans/BlackHanSans-Regular.ttf',    # 回目·타임오버 등
    'mincho': F + 'gowunbatang/GowunBatang-Bold.ttf',         # 설명 줄(명조)
    'mincho_r': F + 'gowunbatang/GowunBatang-Regular.ttf',    # 중단 화면 글자판(가는 명조)
    'callig': F + 'eastseadokdo/EastSeaDokdo-Regular.ttf',    # 권법 足技 등 붓
    'gothic': F + 'nanum-gothic/NanumGothicExtraBold.ttf',
    'yeonsung': F + 'yeonsung/YeonSung-Regular.ttf',            # 부제 「제1장 요코스카」(하스피 선택 2026-11-04)
}

def ink_rows(a, thr=16):
    """알파에서 잉크 있는 행 묶음 [(y0,y1,x0,x1)]"""
    w, h = a.size; px = a.load(); rows = []
    for y in range(h):
        xs = [x for x in range(w) if px[x, y] > thr]
        rows.append((min(xs), max(xs)) if xs else None)
    segs = []; y = 0
    while y < h:
        if rows[y] is None: y += 1; continue
        y0 = y; x0, x1 = rows[y]
        while y < h and rows[y] is not None:
            x0 = min(x0, rows[y][0]); x1 = max(x1, rows[y][1]); y += 1
        segs.append([y0, y, x0, x1 + 1])
    # 아주 가까운 묶음(탁점·받침 떨어짐)은 합침
    out = []
    for s in segs:
        if out and s[0] - out[-1][1] <= max(1, (out[-1][1] - out[-1][0]) // 6):
            o = out[-1]; o[1] = s[1]; o[2] = min(o[2], s[2]); o[3] = max(o[3], s[3])
        else: out.append(s)
    return out

def colors(im):
    px = [p for p in im.getdata() if p[3] > 200]
    if not px: return (255, 255, 255), None
    lum = lambda p: 0.3 * p[0] + 0.59 * p[1] + 0.11 * p[2]
    px.sort(key=lum)
    dark, light = px[len(px) // 20], px[-len(px) // 20 - 1]
    if lum(light) - lum(dark) < 60:              # 한 색
        return light[:3], None
    nlight = sum(1 for p in px if lum(p) > (lum(light) + lum(dark)) / 2)
    if nlight >= len(px) * 0.35: return light[:3], dark[:3]      # 밝은 글자 + 어두운 테두리
    return dark[:3], light[:3]                                    # 어두운 글자 + 밝은 테두리

def is_binary(im):
    return len(set(p[3] for p in im.getdata())) <= 2

def draw_line(text, font_path, box_w, box_h, fill, stroke, sw, S=4, vertical=False):
    """한 줄을 box 안에 맞춰 그린 RGBA (S배로 그려 줄임)"""
    W, H = box_w * S, box_h * S
    size = int(H * 0.92)
    while True:
        f = ImageFont.truetype(font_path, size)
        if vertical: break
        else:
            bb = f.getbbox(text, stroke_width=sw * S)
            if (bb[2] - bb[0] <= W and bb[3] - bb[1] <= H * 1.05) or size < 8: break
        size = int(size * 0.94)
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dr = ImageDraw.Draw(img)
    if vertical:
        # 칸 = 글자 하나(연속 숫자는 한 칸에 가로로), '_' 로 시작하는 낱말은 작게(0.6), 낱말 사이 0.45칸
        import re as _re
        cells = []
        for wd in text.split(' '):
            small = wd.startswith('_'); wd = wd.lstrip('_')
            if cells: cells.append((' ', 0.45))
            cells += [(c, 0.6 if small else 1.0) for c in _re.findall(r'[0-9]+|.', wd)]
        tot = sum(r for _, r in cells); unit = H / tot
        y = 0
        for c, r in cells:
            if c != ' ':
                fc = ImageFont.truetype(font_path, 400)
                g = Image.new('L', (900, 520), 0); ImageDraw.Draw(g).text((40, 40), c, font=fc, fill=255, stroke_width=sw * 7, stroke_fill=255)
                g = g.crop(g.getbbox())
                tw, th = W * (0.92 if r == 1 else 0.7), unit * r * 0.86
                k = min(tw / g.size[0], th / g.size[1])
                gw, gh = g.size[0] * k, g.size[1] * k
                if gw < tw: gw = min(tw, gw * 1.35)          # 예서체처럼 넓적하게(최대 1.35배)
                g = g.resize((max(1, int(gw)), max(1, int(gh))), Image.LANCZOS)
                col = Image.new('RGBA', g.size, fill + (255,)); col.putalpha(g)
                img.alpha_composite(col, (int((W - g.size[0]) / 2), int(y + (unit * r - g.size[1]) / 2)))
            y += unit * r
    else:
        bb = f.getbbox(text, stroke_width=sw * S)
        dr.text((-bb[0], (H - (bb[3] - bb[1])) / 2 - bb[1]), text, font=f, fill=fill + (255,),
                stroke_width=sw * S, stroke_fill=(stroke or fill) + (255,))
    return img.resize((box_w, box_h), Image.LANCZOS), (f.getbbox(text, stroke_width=sw * S)[2] - f.getbbox(text, stroke_width=sw * S)[0]) // S if not vertical else box_w

def render(name, text, font='button', vertical=False, align=None, keep_aa=None, sw=None, fill=None, stroke=None, light_text=False):
    src = Image.open(os.path.join(ORIG, name + '.png')).convert('RGBA')
    a = src.split()[3]
    segs = ink_rows(a) if not vertical else [list(a.getbbox() or (0, 0, *src.size))]
    if vertical:
        x0, y0, x1, y1 = segs[0]; segs = [[y0, y1, x0, x1]]
    lines = text.split('\n')
    f_col, s_col = colors(src)
    if light_text and s_col is not None and _lum(f_col + (0,)) < _lum(s_col + (0,)):   # 버튼: 언제나 밝은 글자 + 어두운 테두리
        f_col, s_col = s_col, f_col
    fill = fill or f_col; stroke = s_col if stroke is None else (None if stroke is False else stroke)   # False = 테두리 없음
    if sw is None: sw = 0 if stroke is None else max(1, round(min(s[1] - s[0] for s in segs) / 22))
    binary = is_binary(src) if keep_aa is None else not keep_aa
    if len(segs) != len(lines):                     # 줄 수가 다르면 전체 상자를 줄 수로 나눔
        bx = a.getbbox(); hh = (bx[3] - bx[1]) / len(lines)
        segs = [[int(bx[1] + k * hh), int(bx[1] + (k + 1) * hh), bx[0], bx[2]] for k in range(len(lines))]
    lefts = [s[2] for s in segs]
    if align is None: align = 'left' if len(segs) > 1 and max(lefts) - min(lefts) <= 3 else 'center'
    out = Image.new('RGBA', src.size, (0, 0, 0, 0))
    full_x0 = min(s[2] for s in segs); full_x1 = max(s[3] for s in segs)
    for (y0, y1, x0, x1), ln in zip(segs, lines):
        if not ln: continue
        bw = (src.size[0] - 2 * max(2, sw + 2)) if not vertical else (x1 - x0)
        line_img, tw = draw_line(ln, FONTS[font], bw, y1 - y0, fill, stroke, sw, vertical=vertical)
        tw = min(tw + 2, bw)
        if vertical: px = x0
        elif align == 'left': px = full_x0
        else: px = (full_x0 + full_x1) // 2 - tw // 2
        m = max(2, sw + 2); px = max(m, min(px, src.size[0] - tw - m))
        crop = line_img.crop((0, 0, tw, y1 - y0))
        out.alpha_composite(crop, (px, y0))
    if binary:
        r, g, b, al = out.split(); al = al.point(lambda v: 255 if v >= 110 else 0)
        out = Image.merge('RGBA', (r, g, b, al))
        out = Image.composite(Image.new('RGBA', out.size, fill + (255,)), out, out.split()[3].point(lambda v: 0)) if False else out
    os.makedirs(NEW, exist_ok=True)
    out.save(os.path.join(NEW, name + '.png'))
    return src, out

def checker(size, c1=(90, 90, 110), c2=(60, 60, 80), s=8):
    im = Image.new('RGBA', size, c1 + (255,)); d = ImageDraw.Draw(im)
    for y in range(0, size[1], s):
        for x in range(0, size[0], s):
            if (x // s + y // s) % 2: d.rectangle((x, y, x + s - 1, y + s - 1), fill=c2 + (255,))
    return im

def preview(group, pairs, scale=None):
    os.makedirs(PREV, exist_ok=True)
    lab = ImageFont.truetype('C:/Windows/Fonts/malgunbd.ttf', 16)
    tiles = []
    for name, ko, (src, new) in pairs:
        b1 = src.split()[3].getbbox() or (0, 0, *src.size); b2 = new.split()[3].getbbox() or b1
        bb = (min(b1[0], b2[0]), min(b1[1], b2[1]), max(b1[2], b2[2]), max(b1[3], b2[3]))   # 원본·새것 범위 합침
        opq = [p for p in src.getdata() if p[3] > 200]
        dark = bool(opq) and sum(0.3 * p[0] + 0.59 * p[1] + 0.11 * p[2] for p in opq) / len(opq) < 90
        pad = 4; bb = (max(0, bb[0] - pad), max(0, bb[1] - pad), min(src.size[0], bb[2] + pad), min(src.size[1], bb[3] + pad))
        s = scale or max(1, min(4, 360 // max(1, bb[2] - bb[0]), 240 // max(1, bb[3] - bb[1])))
        def show(im):
            c = im.crop(bb); bg = checker(c.size, (225, 215, 190), (200, 190, 165)) if dark else checker(c.size); bg.alpha_composite(c)
            return bg.resize((c.size[0] * s, c.size[1] * s), Image.NEAREST)
        tiles.append((name, ko, show(src), show(new)))
    W = max(a.size[0] + b.size[0] for _, _, a, b in tiles) + 30
    W = max(W, 600); H = sum(max(a.size[1], b.size[1]) + 30 for *_, a, b in tiles) + 10
    sh = Image.new('RGB', (W, H), (25, 25, 30)); d = ImageDraw.Draw(sh); y = 5
    for name, ko, a, b in tiles:
        d.text((6, y), '%s  →  %s' % (name, ko.replace('\n', ' / ')), font=lab, fill=(255, 220, 80)); y += 22
        sh.paste(a.convert('RGB'), (6, y)); sh.paste(b.convert('RGB'), (6 + a.size[0] + 18, y))
        y += max(a.size[1], b.size[1]) + 8
    sh.save(os.path.join(PREV, group + '.png'))
    return os.path.join(PREV, group + '.png')


def runs_in_line(a, y0, y1, gap):
    """한 줄(y0~y1) 안의 잉크 덩어리 [(x0,x1)] — gap 픽셀 이상 비면 나눔"""
    w = a.size[0]; px = a.load()
    cols = [any(px[x, y] > 16 for y in range(y0, y1)) for x in range(w)]
    runs = []; x = 0
    while x < w:
        if not cols[x]: x += 1; continue
        s = x; last = x
        while x < w and (cols[x] or x - last <= gap):
            if cols[x]: last = x
            x += 1
        runs.append((s, last + 1))
    return runs

def _sample(src, pred):
    px = [p for p in src.getdata() if p[3] > 200 and pred(p)]
    if not px: return None
    px.sort(key=lambda p: p[0] + p[1] + p[2]); return px[len(px) // 2][:3]

def draw_rich(dst, x, y0, h, text, font_path, fill, red, stroke, sw, shadow=None, maxw=None):
    """{r}…{/r} 는 빨강. 왼쪽 x 부터 그린다(maxw 넘으면 글자를 줄임). 돌려줌: 끝 x"""
    S = 4
    parts = re.split(r'(\{r\}.*?\{/r\})', text)
    plain = re.sub(r'\{/?r\}', '', text)
    maxw = maxw or (dst.size[0] - x - 2)
    size = int(h * S * 0.95)
    while size > 8 and ImageFont.truetype(font_path, size).getlength(plain) + (sw + (shadow or 0)) * S * 2 > maxw * S:
        size = int(size * 0.95)
    f = ImageFont.truetype(font_path, size)
    canvas = Image.new('RGBA', (dst.size[0] * S, h * S), (0, 0, 0, 0)); d = ImageDraw.Draw(canvas)
    cx = 0
    asc_bb = f.getbbox('가나다')
    for p in parts:
        if not p: continue
        col = red if p.startswith('{r}') else fill
        t = p[3:-4] if p.startswith('{r}') else p
        if shadow:
            d.text((cx + shadow * S, (h * S - (asc_bb[3] - asc_bb[1])) / 2 - asc_bb[1] + shadow * S), t, font=f, fill=(0, 0, 0, 255))
        d.text((cx, (h * S - (asc_bb[3] - asc_bb[1])) / 2 - asc_bb[1]), t, font=f, fill=col + (255,),
               stroke_width=sw * S, stroke_fill=(stroke or col) + (255,))
        cx += d.textlength(t, font=f)
    small = canvas.resize((dst.size[0], h), Image.LANCZOS)
    tw = int(cx / S) + 2
    dst.alpha_composite(small.crop((0, 0, min(tw, dst.size[0] - x), h)), (x, y0))
    return x + tw

def render_para(name, specs, font='gothic', gap=None, shadow=None, sw=0, fill=None, stroke=False, mask=None):
    """specs = 원본 «잉크 줄»마다 하나:
         '문장'                         → 그 줄 가운데에 다시 그림
         ['@keep', '문장', …]           → 원본 덩어리(빈칸 gap 으로 나눔) 위치에 조각별로: '@keep' 은 원본 픽셀 그대로, 문장은 덩어리 왼쪽부터
       문장 안 {r}…{/r} = 빨강(원본에서 빨간 화소를 재서)"""
    src = Image.open(os.path.join(ORIG, name + '.png')).convert('RGBA')
    if mask == 'lum':      # 바탕이 불투명(검정) — 밝기로 글자 찾기, 바탕은 유지
        a = src.convert('L').point(lambda v: 255 if v > 70 else 0)
        base = src.copy()                               # 글자 줄은 바로 위 행을 복사해 메움(바탕 무늬·색 유지)
        for (y0, y1, x0, x1) in ink_rows(a):           # 글자 줄 ±2행까지(옅은 가장자리 찌꺼기 방지)
            row = src.crop((0, max(0, y0 - 4), src.size[0], max(1, y0 - 3)))
            for y in range(max(0, y0 - 2), min(src.size[1], y1 + 2)): base.paste(row, (0, y))
    else:
        a = src.split()[3]; base = Image.new('RGBA', src.size, (0, 0, 0, 0))
    segs = ink_rows(a)
    if len(segs) != len(specs): raise SystemExit('%s: 원본 줄 %d ≠ 지정 %d' % (name, len(segs), len(specs)))
    fill = fill or _sample(src, lambda p: p[0] > 180 and p[1] > 180 and p[2] > 180) or (255, 255, 255)
    red = _sample(src, lambda p: p[0] > 150 and p[1] < 110 and p[2] < 110) or (240, 60, 40)
    stroke = None if stroke is False else stroke
    out = base
    for (y0, y1, x0, x1), sp in zip(segs, specs):
        h = y1 - y0
        if isinstance(sp, str) and '\n' in sp:          # 한 덩어리로 잡힌 여러 줄
            ls = sp.split('\n'); hh = h // len(ls)
            for k, l in enumerate(ls):
                tmp = Image.new('RGBA', src.size, (0, 0, 0, 0))
                end = draw_rich(tmp, 0, y0 + k * hh, hh, l, FONTS[font], fill, red, stroke, sw, shadow)
                cx = (x0 + x1) // 2 - end // 2
                out.alpha_composite(tmp.crop((0, 0, end, src.size[1])), (max(0, min(cx, src.size[0] - end)), 0))
        elif isinstance(sp, str):
            tmp = Image.new('RGBA', src.size, (0, 0, 0, 0))
            end = draw_rich(tmp, 0, y0, h, sp, FONTS[font], fill, red, stroke, sw, shadow)
            cx = (x0 + x1) // 2 - end // 2
            out.alpha_composite(tmp.crop((0, 0, end, src.size[1])), (max(0, min(cx, src.size[0] - end)), 0))
        elif isinstance(sp, tuple) and sp[0] == 'keep':      # ('keep', k, 문장): 앞 덩어리 k개(［ＤＩＳＣ　］)는 원본 그대로, 그 뒤에 문장
            _, k, txt = sp
            runs = runs_in_line(a, y0, y1, max(2, h // 5))
            kx0, kx1 = runs[0][0], runs[k - 1][1]
            out.alpha_composite(src.crop((kx0, y0, kx1, y1)), (kx0, y0))
            draw_rich(out, kx1 + max(2, h // 6), y0, h, txt, FONTS[font], fill, red, stroke, sw, shadow)
        else:
            runs = runs_in_line(a, y0, y1, gap or max(4, h // 2))
            if len(runs) != len(sp): raise SystemExit('%s 줄 y%d: 덩어리 %d ≠ 조각 %d %s' % (name, y0, len(runs), len(sp), runs))
            for (rx0, rx1), piece in zip(runs, sp):
                if piece == '@keep': out.alpha_composite(src.crop((rx0, y0, rx1, y1)), (rx0, y0))
                elif piece: draw_rich(out, rx0, y0, h, piece, FONTS[font], fill, red, stroke, sw, shadow)
    os.makedirs(NEW, exist_ok=True); out.save(os.path.join(NEW, name + '.png'))
    return src, out


def _lum(p): return 0.3 * p[0] + 0.59 * p[1] + 0.11 * p[2]

def render_plate(name, text, font='button', kind='dark', region=None, pad=3, fill=None, stroke=None, sw=2, text_h=None):
    """무늬 판 위 글자: 글자 화소(kind='dark' 검은 글자 / 'light' 흰 글자)의 범위를 찾아 그 칸만
    행마다 좌우 경계 화소로 선형 보간해 지우고, 원본 글자·테두리 색으로 한글을 다시 그림."""
    src = Image.open(os.path.join(ORIG, name + '.png')).convert('RGBA'); W, H = src.size; px = src.load()
    rx0, ry0, rx1, ry1 = region or (0, 0, W, H)
    pts = [(x, y) for y in range(ry0, ry1) for x in range(rx0, rx1) if px[x, y][3] > 200 and
           ((_lum(px[x, y]) < 50) if kind == 'dark' else (_lum(px[x, y]) > 225))]
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    x0, x1, y0, y1 = max(0, min(xs) - pad), min(W - 1, max(xs) + pad), max(0, min(ys) - pad), min(H - 1, max(ys) + pad)
    ink = [px[x, y] for x, y in pts]
    fill = fill or tuple(sorted(ink, key=_lum)[len(ink) // 2][:3])
    if stroke is None:
        ring = [px[x, y] for y in range(y0, y1) for x in range(x0, x1) if px[x, y][3] > 200]
        ring.sort(key=_lum); stroke = (ring[-len(ring) // 30 - 1] if kind == 'dark' else ring[len(ring) // 30])[:3]
    out = src.copy(); op = out.load()
    for y in range(y0, y1 + 1):
        L, R = px[x0 - 1 if x0 > 0 else x0, y], px[x1 + 1 if x1 < W - 1 else x1, y]
        for x in range(x0, x1 + 1):
            t = (x - x0) / max(1, x1 - x0)
            op[x, y] = tuple(int(L[i] * (1 - t) + R[i] * t) for i in range(4))
    if text_h:      # 같은 묶음은 같은 글자 높이(하스피 «예/아니요 선택 시 크기 달라짐»)
        th = text_h; cy = (y0 + y1) // 2
        line, tw = draw_line(text, FONTS[font], W, th, fill, stroke, sw); tw = min(tw + 2, W)
        out.alpha_composite(line.crop((0, 0, tw, th)), ((x0 + x1) // 2 - tw // 2, cy - th // 2))
    else:
        line, tw = draw_line(text, FONTS[font], x1 - x0, y1 - y0, fill, stroke, sw)
        tw = min(tw + 2, x1 - x0)
        out.alpha_composite(line.crop((0, 0, tw, y1 - y0)), ((x0 + x1) // 2 - tw // 2, y0))
    os.makedirs(NEW, exist_ok=True); out.save(os.path.join(NEW, name + '.png'))
    return src, out

def render_logo(name, text, font, keep=None, outline=(170, 170, 180), ow=1, spread=False):
    """질감 로고: 원본 잉크 화소(테두리 안쪽)를 질감으로 따서 한글 모양에 입힘 + 회색 테두리. keep=(x0,y0,x1,y1) 원본 그대로(TM 등)"""
    src = Image.open(os.path.join(ORIG, name + '.png')).convert('RGBA'); W, H = src.size
    a = src.split()[3]; bb = a.getbbox()
    opq = sorted([p for p in src.getdata() if p[3] > 120], key=_lum)
    tex_px = [p for p in opq if _lum(p) < 110] or opq[:max(1, len(opq) // 2)]     # 테두리(밝은 회색) 빼고 안쪽 질감
    import random; rnd = random.Random(1)
    S = 4
    if keep: kx0 = keep[0]
    else: kx0 = bb[2]
    box_w, box_h = (kx0 - bb[0]), (bb[3] - bb[1])
    if spread:                       # 글자를 상자 폭에 고르게 펼침(원본 로고처럼 길게)
        mask = Image.new('L', (box_w, box_h), 0); n = len(text); cw = box_w // n
        fbig = ImageFont.truetype(FONTS[font], 400)
        for k, c in enumerate(text):
            g = Image.new('L', (700, 600), 0); ImageDraw.Draw(g).text((50, 50), c, font=fbig, fill=255); g = g.crop(g.getbbox())
            kk = (box_h * 0.96) / g.size[1]; gw = min(cw * 0.9, g.size[0] * kk * 1.6)   # 높이 꽉, 가로 최대 1.6배
            g = g.resize((max(1, int(gw)), int(box_h * 0.96)), Image.LANCZOS)
            mask.paste(g, (k * cw + (cw - g.size[0]) // 2, int(box_h * 0.02)))
    else:
        m, tw = draw_line(text, FONTS[font], box_w, box_h, (255, 255, 255), None, 0)
        tw = min(box_w, tw + 2)                       # ★원본 범위 가운데에(하스피 «부제가 왼쪽에 쏠림»)
        mask = Image.new('L', (box_w, box_h), 0); mask.paste(m.split()[3].crop((0, 0, tw, box_h)), ((box_w - tw) // 2, 0))
    tex = Image.new('RGBA', (box_w, box_h)); tp = tex.load()
    for y in range(box_h):
        for x in range(box_w): tp[x, y] = tex_px[rnd.randrange(len(tex_px))]
    tex = tex.filter(ImageFilter.SMOOTH)
    glyph = Image.new('RGBA', (box_w, box_h), (0, 0, 0, 0)); glyph.paste(tex, (0, 0), mask.point(lambda v: 255 if v > 100 else 0))
    edge = mask.point(lambda v: 255 if v > 100 else 0).filter(ImageFilter.MaxFilter(1 + 2 * ow))
    ring = Image.new('RGBA', (box_w, box_h), outline + (255,)); ring.putalpha(edge)
    out = Image.new('RGBA', src.size, (0, 0, 0, 0))
    out.alpha_composite(ring, (bb[0], bb[1])); out.alpha_composite(glyph, (bb[0], bb[1]))
    if keep: out.alpha_composite(src.crop(keep), (keep[0], keep[1]))
    os.makedirs(NEW, exist_ok=True); out.save(os.path.join(NEW, name + '.png'))
    return src, out

def vcolumns(a, gap=6):
    """세로쓰기 줄 [(x0,x1,y0,y1)] — 오른쪽부터"""
    W, H = a.size; px = a.load()
    cols = [any(px[x, y] > 40 for y in range(H)) for x in range(W)]
    runs = []; x = 0
    while x < W:
        if not cols[x]: x += 1; continue
        s = x; last = x
        while x < W and (cols[x] or x - last <= gap):
            if cols[x]: last = x
            x += 1
        ys = [y for y in range(H) for xx in range(s, last + 1, 2) if px[xx, y] > 40]
        runs.append((s, last + 1, min(ys), max(ys) + 1))
    return runs[::-1]

def render_vcols(name, columns, font='callig', gap=6, cell=None):
    """세로쓰기 시: 원본 세로줄 위치마다 한글 세로줄(위에서부터). columns = 오른쪽 줄부터 문자열(빈 문자열은 원본 그대로 두지 않고 비움)"""
    src = Image.open(os.path.join(ORIG, name + '.png')).convert('RGBA'); a = src.split()[3]
    runs = vcolumns(a, gap)
    if len(runs) != len(columns): raise SystemExit('%s: 원본 세로줄 %d ≠ 지정 %d %s' % (name, len(runs), len(columns), runs))
    fill = _sample(src, lambda p: _lum(p) > 150) or (230, 230, 230)
    cw = cell or int(sorted(r[1] - r[0] for r in runs)[len(runs) // 2])
    out = Image.new('RGBA', src.size, (0, 0, 0, 0))
    f = ImageFont.truetype(FONTS[font], cw * 4)
    for (x0, x1, y0, y1), col in zip(runs, columns):
        cx = (x0 + x1) // 2; y = y0
        n = len(col); step = cw * 1.02
        if n and y0 + n * step > src.size[1]: step = (src.size[1] - y0) / n
        for c in col:
            if c != ' ':
                g = Image.new('L', (cw * 6, cw * 6), 0); ImageDraw.Draw(g).text((cw, cw), c, font=f, fill=255)
                g = g.crop(g.getbbox()) if g.getbbox() else g
                k = min(cw * 0.95 / g.size[0], step * 0.92 / g.size[1]) if g.size[0] else 1
                g = g.resize((max(1, int(g.size[0] * k)), max(1, int(g.size[1] * k))), Image.LANCZOS)
                colr = Image.new('RGBA', g.size, fill + (255,)); colr.putalpha(g)
                out.alpha_composite(colr, (int(cx - g.size[0] / 2), int(y + (step - g.size[1]) / 2)))
            y += step
    os.makedirs(NEW, exist_ok=True); out.save(os.path.join(NEW, name + '.png'))
    return src, out


def render_cells(name, cells, font='heavy', shear=0.18, sw=1):
    """그림판 낱칸 바꾸기: cells = [((x0,y0,x1,y1), 글자)] — 칸 안 원본 색(가장 밝은=글자, 가장 어두운=테두리)으로 다시 그림, 기울임 shear"""
    src = Image.open(os.path.join(ORIG, name + '.png')).convert('RGBA'); out = src.copy()
    for (x0, y0, x1, y1), ch in cells:
        cell = src.crop((x0, y0, x1, y1))
        ink = sorted([p for p in cell.getdata() if p[3] > 200], key=_lum)
        fill, stroke = ink[-len(ink) // 10 - 1][:3], ink[len(ink) // 10][:3]
        w, h = x1 - x0, y1 - y0
        img, tw = draw_line(ch, FONTS[font], w, h, fill, stroke, sw)
        if shear: img = img.transform(img.size, Image.AFFINE, (1, shear, -shear * h / 2, 0, 1, 0), Image.BICUBIC)
        out.paste((0, 0, 0, 0), (x0, y0, x1, y1))
        out.alpha_composite(img.crop((0, 0, min(w, tw + 3), h)), (x0 + max(0, (w - tw - 3) // 2), y0))
    os.makedirs(NEW, exist_ok=True); out.save(os.path.join(NEW, name + '.png'))
    return src, out

def render_stamp(name, box, text, font='heavy'):
    """도장(練習): 테두리는 두고 안쪽 box 를 지운 뒤 같은 분홍으로 한글"""
    src = Image.open(os.path.join(ORIG, name + '.png')).convert('RGBA'); out = src.copy()
    x0, y0, x1, y1 = box
    col = _sample(src.crop(box), lambda p: p[0] > 150) or (240, 80, 150)
    out.paste((0, 0, 0, 0), box)
    img, tw = draw_line(text, FONTS[font], x1 - x0, y1 - y0, col, None, 0)
    out.alpha_composite(img.crop((0, 0, min(tw + 2, x1 - x0), y1 - y0)), (x0 + max(0, (x1 - x0 - tw) // 2), y0))
    os.makedirs(NEW, exist_ok=True); out.save(os.path.join(NEW, name + '.png'))
    return src, out


def preview_grid(group, pairs, page_w=1600, page_h=1100, scale=1):
    """격자 미리보기: 짝(원본|한글)을 가로로 늘어놓고 page_w×page_h 단위로 쪽을 나눔 → <묶음>_1.png, _2.png …"""
    os.makedirs(PREV, exist_ok=True)
    lab = ImageFont.truetype('C:/Windows/Fonts/malgunbd.ttf', 15)
    tiles = []
    for name, ko, (src, new) in pairs:
        b1 = src.split()[3].getbbox() or (0, 0, *src.size); b2 = new.split()[3].getbbox() or b1
        pad = 4
        bb = (max(0, min(b1[0], b2[0]) - pad), max(0, min(b1[1], b2[1]) - pad), min(src.size[0], max(b1[2], b2[2]) + pad), min(src.size[1], max(b1[3], b2[3]) + pad))
        opq = [p for p in src.getdata() if p[3] > 200]
        dark = bool(opq) and sum(_lum(p) for p in opq) / len(opq) < 90      # 검은 글씨는 밝은 바탕에
        def show(im):
            c = im.crop(bb); bg = checker(c.size, (225, 215, 190), (200, 190, 165)) if dark else checker(c.size); bg.alpha_composite(c)
            return bg.resize((c.size[0] * scale, c.size[1] * scale), Image.NEAREST).convert('RGB')
        a, b = show(src), show(new)
        ko = ko.replace('_', '')
        lw = int(lab.getlength(ko)) + 8
        w = max(a.size[0] + b.size[0] + 10, lw); h = max(a.size[1], b.size[1]) + 24
        t = Image.new('RGB', (w, h), (25, 25, 30)); d = ImageDraw.Draw(t)
        d.text((2, 2), ko, font=lab, fill=(255, 220, 80)); t.paste(a, (0, 22)); t.paste(b, (a.size[0] + 10, 22))
        tiles.append(t)
    pages = []; cur = []; x = y = rowh = 0
    for t in tiles:
        if x + t.size[0] > page_w: x = 0; y += rowh + 12; rowh = 0
        if y + t.size[1] > page_h and cur: pages.append(cur); cur = []; x = y = rowh = 0
        cur.append((t, x, y)); x += t.size[0] + 16; rowh = max(rowh, t.size[1])
    if cur: pages.append(cur)
    for f in glob.glob(os.path.join(PREV, group + '*.png')): os.remove(f)
    out = []
    for k, pg in enumerate(pages, 1):
        W = max(x + t.size[0] for t, x, y in pg); H = max(y + t.size[1] for t, x, y in pg)
        sh = Image.new('RGB', (W + 10, H + 10), (25, 25, 30))
        for t, x, y in pg: sh.paste(t, (x + 5, y + 5))
        p = os.path.join(PREV, '%s_%d.png' % (group, k)); sh.save(p); out.append(p)
    return out


def render_fixed(name, text, font='brush', ink_h=30, stretch=1.4, fill=(255, 255, 255), sw=1, binary=True):
    """같은 UI 낱자는 같은 크기: 기준 글자 「한」의 잉크 높이가 ink_h 가 되는 «한 가지 크기»로 그리고,
    기준선도 「한」 기준으로 칸 가운데(글자마다 자기 잉크로 맞추지 않음). 가로 stretch 배(원본 붓글씨처럼 넓적)."""
    src = Image.open(os.path.join(ORIG, name + '.png')).convert('RGBA'); W, H = src.size
    BIG = 400; f = ImageFont.truetype(FONTS[font], BIG)
    ref = f.getbbox('한'); k = ink_h / (ref[3] - ref[1])
    tw = int(f.getlength(text) + sw * 40) + 40
    g = Image.new('L', (tw, BIG * 2), 0)
    ImageDraw.Draw(g).text((20, BIG // 2), text, font=f, fill=255, stroke_width=sw * 6, stroke_fill=255)
    x0, _, x1, _ = g.getbbox()
    top, bot = BIG // 2 + ref[1], BIG // 2 + ref[3]          # 기준선 = 「한」 위·아래
    g = g.crop((x0, top - int(BIG * 0.15), x1, bot + int(BIG * 0.15)))
    nw, nh = max(1, int(g.size[0] * k * stretch)), max(1, int(g.size[1] * k))
    g = g.resize((nw, nh), Image.LANCZOS)
    if binary: g = g.point(lambda v: 255 if v >= 110 else 0)
    out = Image.new('RGBA', src.size, (0, 0, 0, 0))
    col = Image.new('RGBA', g.size, fill + (255,)); col.putalpha(g)
    out.alpha_composite(col, ((W - nw) // 2, (H - nh) // 2))
    os.makedirs(NEW, exist_ok=True); out.save(os.path.join(NEW, name + '.png'))
    return src, out


def render_vfixed(name, text, font='brush', ink_h=48, cell=56, stretch=1.25, fill=(255, 255, 255), sw=1):
    """세로쓰기 지명: 모든 텍스처에 «같은 글자 크기·같은 칸 간격» (하스피 «세로글씨 크기 통일»).
    글자 크기 = 기준 「한」 잉크 높이 ink_h, 칸 = cell, 낱말 사이 0.45칸, '_' 낱말은 0.6배, 숫자 묶음은 한 칸.
    원본 지명 잉크 범위의 가운데에 세로로 놓음."""
    import re as _re
    src = Image.open(os.path.join(ORIG, name + '.png')).convert('RGBA'); W, H = src.size
    bb = src.split()[3].getbbox(); cx = (bb[0] + bb[2]) // 2; cy = (bb[1] + bb[3]) // 2
    BIG = 400; f = ImageFont.truetype(FONTS[font], BIG); ref = f.getbbox('한'); k = ink_h / (ref[3] - ref[1])
    cells = []
    for wd in text.split(' '):
        small = wd.startswith('_'); wd = wd.lstrip('_')
        if cells: cells.append((' ', 0.45))
        cells += [(c, 0.6 if small else 1.0) for c in _re.findall(r'[0-9]+|.', wd)]
    total = sum(cell * r for _, r in cells)
    y = max(2, min(cy - total / 2, H - total - 2))
    out = Image.new('RGBA', src.size, (0, 0, 0, 0))
    for c, r in cells:
        if c != ' ':
            g = Image.new('L', (int(f.getlength(c)) + 120, BIG * 2), 0)
            ImageDraw.Draw(g).text((40, BIG // 2), c, font=f, fill=255, stroke_width=sw * 7, stroke_fill=255)
            x0, _, x1, _ = g.getbbox()
            top, bot = BIG // 2 + ref[1], BIG // 2 + ref[3]            # 기준선 = 「한」
            g = g.crop((x0, top - int(BIG * 0.12), x1, bot + int(BIG * 0.12)))
            kk = k * r; st = stretch if len(c) == 1 else 1.0               # 두 자리 숫자는 넓히지 않음
            nw, nh = max(1, int(g.size[0] * kk * st)), max(1, int(g.size[1] * kk))
            g = g.resize((nw, nh), Image.LANCZOS)
            col = Image.new('RGBA', g.size, fill + (255,)); col.putalpha(g)
            out.alpha_composite(col, (cx - nw // 2, int(y + (cell * r - nh) / 2)))
        y += cell * r
    os.makedirs(NEW, exist_ok=True); out.save(os.path.join(NEW, name + '.png'))
    return src, out


def render_vcols_fixed(name, columns, step, ink_h, font='callig', gap=6):
    """세로쓰기 시(엔딩): 모든 글자 «같은 크기(기준 「한」 잉크 높이 ink_h)·같은 칸 간격 step·같은 기준선»,
    원본 세로줄 x 가운데 · 원본 줄 윗단(y)부터. 하스피 «세로글씨 엔딩글자 크기가 너무 제각각»(2026-11-04)."""
    src = Image.open(os.path.join(ORIG, name + '.png')).convert('RGBA'); a = src.split()[3]
    runs = vcolumns(a, gap)
    if len(runs) != len(columns): raise SystemExit('%s: 원본 세로줄 %d ≠ 지정 %d' % (name, len(runs), len(columns)))
    fill = _sample(src, lambda p: _lum(p) > 150) or (230, 230, 230)
    BIG = 400; f = ImageFont.truetype(FONTS[font], BIG); ref = f.getbbox('한'); k = ink_h / (ref[3] - ref[1])
    out = Image.new('RGBA', src.size, (0, 0, 0, 0))
    top_all = min(r[2] for r in runs if r[1] - r[0] > 8)
    for (x0, x1, y0, y1), col in zip(runs, columns):
        cx = (x0 + x1) // 2; y = top_all if y0 >= top_all - 10 else y0
        for c in col:
            if c != ' ':
                g = Image.new('L', (int(f.getlength(c)) + 120, BIG * 2), 0)
                ImageDraw.Draw(g).text((40, BIG // 2), c, font=f, fill=255)
                bx = g.getbbox()
                if bx:
                    g = g.crop((bx[0], BIG // 2 + ref[1] - int(BIG * 0.15), bx[2], BIG // 2 + ref[3] + int(BIG * 0.15)))
                    g = g.resize((max(1, int(g.size[0] * k)), max(1, int(g.size[1] * k))), Image.LANCZOS)
                    colr = Image.new('RGBA', g.size, fill + (255,)); colr.putalpha(g)
                    out.alpha_composite(colr, (cx - g.size[0] // 2, int(y + (step - g.size[1]) / 2)))
            y += step if c != ' ' else step * 0.5
    os.makedirs(NEW, exist_ok=True); out.save(os.path.join(NEW, name + '.png'))
    return src, out


def _shadow_spec(src):
    """원본에서 글자색·그림자색·그림자 방향 재기: 가장 많은 두 색 중 글자 마스크를 (dx,dy) 민 자리와 가장 겹치는 쪽이 그림자"""
    from collections import Counter
    cnt = Counter(p[:3] for p in src.getdata() if p[3] > 200).most_common(2)
    (c1, _), (c2, _) = cnt[0], cnt[1]
    W, H = src.size; px = src.load()
    def mask(c): return {(x, y) for y in range(H) for x in range(W) if px[x, y][3] > 200 and px[x, y][:3] == c}
    m1, m2 = mask(c1), mask(c2); best = None
    for txt, sh, mt, ms in ((c1, c2, m1, m2), (c2, c1, m2, m1)):
        for dx in (-2, -1, 0, 1, 2):
            for dy in (-2, -1, 0, 1, 2):
                if dx == dy == 0: continue
                sc = len({(x + dx, y + dy) for x, y in mt} & ms)
                if best is None or sc > best[0]: best = (sc, txt, sh, dx, dy)
    return best[1:]

def render_vshadow(name, text, ink_h=21, cell=28, stretch=1.0, font='heavy'):
    """세로 낱말 + 원본 그림자(색·방향 자동). 같은 묶음은 ink_h·cell 같게 → 같은 크기."""
    src = Image.open(os.path.join(ORIG, name + '.png')).convert('RGBA'); W, H = src.size
    fill, shc, dx, dy = _shadow_spec(src)
    BIG = 400; f = ImageFont.truetype(FONTS[font], BIG); ref = f.getbbox('한'); k = ink_h / (ref[3] - ref[1])
    bb = src.split()[3].getbbox(); cx = (bb[0] + bb[2]) // 2; total = cell * len(text); y = (bb[1] + bb[3]) / 2 - total / 2
    mask = Image.new('L', src.size, 0)
    for c in text:
        g = Image.new('L', (int(f.getlength(c)) + 120, BIG * 2), 0); ImageDraw.Draw(g).text((40, BIG // 2), c, font=f, fill=255)
        bx = g.getbbox(); g = g.crop((bx[0], BIG // 2 + ref[1] - int(BIG * 0.12), bx[2], BIG // 2 + ref[3] + int(BIG * 0.12)))
        g = g.resize((max(1, int(g.size[0] * k * stretch)), max(1, int(g.size[1] * k))), Image.LANCZOS)
        mask.paste(g, (cx - g.size[0] // 2, int(y + (cell - g.size[1]) / 2)), g); y += cell
    mask = mask.point(lambda v: 255 if v >= 110 else 0)
    out = Image.new('RGBA', src.size, (0, 0, 0, 0))
    sh = Image.new('RGBA', src.size, shc + (255,)); sh.putalpha(mask); out.alpha_composite(sh, (dx, dy))
    tx = Image.new('RGBA', src.size, fill + (255,)); tx.putalpha(mask); out.alpha_composite(tx)
    os.makedirs(NEW, exist_ok=True); out.save(os.path.join(NEW, name + '.png'))
    return src, out

def render_vplate(name, text, box, ink_h=11, cell=17, font='heavy', bold=0, pool_x=None):
    """판 위 세로 글자(修行中): box 안 글자(가장 어두운 색)를 세로줄마다 위·아래 판 화소로 보간해 지우고 같은 색으로 세로 한글"""
    src = Image.open(os.path.join(ORIG, name + '.png')).convert('RGBA'); out = src.copy(); op = out.load(); px = src.load()
    x0, y0, x1, y1 = box
    ink = sorted([px[x, y] for y in range(y0, y1) for x in range(x0, x1)], key=_lum); fill = ink[len(ink) // 20][:3]
    # 판 새로 채우기: 같은 높이(±2행) 양옆 금색 띠(글자 없는 x0-4..x0-1, x1..x1+3)의 밝은 화소를 무작위로 뽑아 가운데를 채우고 부드럽게
    import random; rnd = random.Random(7)
    for y in range(y0, y1):
        pool = [px[x, yy] for yy in range(max(0, y - 2), min(src.size[1], y + 3))
                for x in (pool_x or (list(range(x0 - 4, x0)) + list(range(x1, x1 + 4)))) if _lum(px[x, yy]) > 120]
        for x in range(x0, x1):
            if pool: op[x, y] = pool[rnd.randrange(len(pool))]
    patch = out.crop((x0, y0, x1, y1)).filter(ImageFilter.SMOOTH)
    out.paste(patch, (x0, y0)); op = out.load()
    BIG = 400; f = ImageFont.truetype(FONTS[font], BIG); ref = f.getbbox('한'); k = ink_h / (ref[3] - ref[1])
    cx = (x0 + x1) // 2; y = (y0 + y1) / 2 - cell * len(text) / 2
    for c in text:
        g = Image.new('L', (int(f.getlength(c)) + 160, BIG * 2), 0); ImageDraw.Draw(g).text((60, BIG // 2), c, font=f, fill=255, stroke_width=bold, stroke_fill=255)
        bx = g.getbbox(); g = g.crop((bx[0], BIG // 2 + ref[1] - int(BIG * 0.12), bx[2], BIG // 2 + ref[3] + int(BIG * 0.12)))
        g = g.resize((max(1, int(g.size[0] * k)), max(1, int(g.size[1] * k))), Image.LANCZOS).point(lambda v: 255 if v >= 110 else 0)
        col = Image.new('RGBA', g.size, fill + (255,)); col.putalpha(g)
        out.alpha_composite(col, (cx - g.size[0] // 2, int(y + (cell - g.size[1]) / 2))); y += cell
    os.makedirs(NEW, exist_ok=True); out.save(os.path.join(NEW, name + '.png'))
    return src, out


def render_logo_bg(name, items, log=None):
    """배경 그림에 박힌 로고 바꾸기(타이틀 통그림). items = [dict(region=(x0,y0,x1,y1), text, font, sel='dark'|'red', outline=(r,g,b) or None, spread)]
    ① region 안 로고 화소(sel 기준)+테두리를 마스크 ② OpenCV inpaint 로 배경 메움 ③ 원본 로고 질감을 입힌 한글을 region 에."""
    import numpy as np, cv2, random
    src = Image.open(os.path.join(ORIG, name + '.png')).convert('RGBA'); out = src.copy()
    for it in items:
        x0, y0, x1, y1 = it['region']; crop = np.array(out.convert('RGB').crop((x0, y0, x1, y1)))
        r, g, b = crop[..., 0].astype(int), crop[..., 1].astype(int), crop[..., 2].astype(int)
        lum = 0.3 * r + 0.59 * g + 0.11 * b
        if it.get('sel') == 'red': m = (r > g + 18) & (r > b + 18) & (lum < 140)          # 검붉은 로고(파란 하늘 위)
        else: m = lum < it.get('thr', 45)                                                 # 어두운 로고(갈색 배경 위)
        tex = [tuple(crop[y, x]) for y, x in zip(*np.nonzero(m))]
        mm = cv2.dilate(m.astype(np.uint8) * 255, np.ones((5, 5), np.uint8), iterations=1)   # 테두리까지
        bgr = cv2.cvtColor(crop, cv2.COLOR_RGB2BGR)
        filled = cv2.cvtColor(cv2.inpaint(bgr, mm, 6, cv2.INPAINT_TELEA), cv2.COLOR_BGR2RGB)
        patch = Image.fromarray(filled).convert('RGBA')
        # 한글 글자 마스크
        bw, bh = x1 - x0, y1 - y0; mask = Image.new('L', (bw, bh), 0)
        fbig = ImageFont.truetype(FONTS[it.get('font', 'callig')], 400)
        if it.get('spread'):
            n = len(it['text']); cw = bw // n
            for k, c in enumerate(it['text']):
                gl = Image.new('L', (700, 600), 0); ImageDraw.Draw(gl).text((50, 50), c, font=fbig, fill=255); gl = gl.crop(gl.getbbox())
                gw = min(cw * 0.9, gl.size[0] * (bh * 0.9) / gl.size[1] * 1.6)
                gl = gl.resize((max(1, int(gw)), int(bh * 0.9)), Image.LANCZOS); mask.paste(gl, (k * cw + (cw - gl.size[0]) // 2, int(bh * 0.05)))
        else:
            ml, _ = draw_line(it['text'], FONTS[it.get('font', 'brush')], bw, bh, (255, 255, 255), None, 0); mask = ml.split()[3]
        mb = mask.point(lambda v: 255 if v > 100 else 0)
        rnd = random.Random(3); timg = Image.new('RGB', (bw, bh)); tp = timg.load()
        for yy in range(bh):
            for xx in range(bw): tp[xx, yy] = tex[rnd.randrange(len(tex))] if tex else (40, 20, 20)
        timg = timg.filter(ImageFilter.SMOOTH)
        if it.get('outline'):
            ring = Image.new('RGBA', (bw, bh), it['outline'] + (255,)); ring.putalpha(mb.filter(ImageFilter.MaxFilter(3))); patch.alpha_composite(ring)
        glyph = timg.convert('RGBA'); glyph.putalpha(mb); patch.alpha_composite(glyph)
        out.paste(patch, (x0, y0))
    os.makedirs(NEW, exist_ok=True); out.save(os.path.join(NEW, name + '.png'))
    return src, out


def find_layer(feature, layer_name, _unused, scales):
    """로고 레이어(알파 모양)를 통그림에서 찾기: feature(어두움/붉음) 지도와 정규 상관 → (x, y, 배율, 마스크 L)"""
    import numpy as np, cv2
    lay = Image.open(os.path.join(ORIG, layer_name + '.png')).convert('RGBA')
    la = lay.split()[3]; bb = la.getbbox(); la = la.crop(bb)
    best = None
    for s in scales:
        t = la.resize((max(1, int(la.size[0] * s)), max(1, int(la.size[1] * s))), Image.LANCZOS)
        tm = np.array(t, dtype=np.float32) / 255.0
        if tm.shape[0] >= feature.shape[0] or tm.shape[1] >= feature.shape[1]: continue
        r = cv2.matchTemplate(feature, tm, cv2.TM_CCORR_NORMED)
        _, mx, _, loc = cv2.minMaxLoc(r)
        if best is None or mx > best[0]: best = (mx, loc[0], loc[1], s, t)
    return best

def render_logo_layer(name, items):
    """통그림 로고 바꾸기(레이어 맞춤): items=[dict(layer, text, font, feature='dark'|'red', scales, outline, spread, pad)]"""
    import numpy as np, cv2, random
    src = Image.open(os.path.join(ORIG, name + '.png')).convert('RGBA')
    rgb = np.array(src.convert('RGB')).astype(np.float32); alpha = src.split()[3]
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]; lum = 0.3 * r + 0.59 * g + 0.11 * b
    cur = np.array(src.convert('RGB'))
    places = []
    for it in items:
        feat = (np.clip(r - (g + b) / 2, 0, 255) / 255.0).astype(np.float32) if it.get('feature') == 'red' else (np.clip(90 - lum, 0, 90) / 90.0).astype(np.float32)
        sx0, sy0, sx1, sy1 = it.get('search', (0, 0, feat.shape[1], feat.shape[0]))
        mx, x, y, s, t = find_layer(feat[sy0:sy1, sx0:sx1].copy(), it['layer'], None, it.get('scales', [k / 20 for k in range(10, 27)]))
        x += sx0; y += sy0
        mask = np.zeros(lum.shape, np.uint8); tm = (np.array(t) > 40).astype(np.uint8) * 255
        mask[y:y + tm.shape[0], x:x + tm.shape[1]] = tm
        mask = cv2.dilate(mask, np.ones((5, 5), np.uint8), iterations=it.get('pad', 2))
        tex = [tuple(cur[yy, xx]) for yy, xx in zip(*np.nonzero(tm)) if True][:0]
        tex = [tuple(cur[y + yy, x + xx]) for yy, xx in zip(*np.nonzero(np.array(t) > 160))]
        cur = cv2.cvtColor(cv2.inpaint(cv2.cvtColor(cur, cv2.COLOR_RGB2BGR), mask, 7, cv2.INPAINT_TELEA), cv2.COLOR_BGR2RGB)
        places.append((it, x, y, t.size[0], t.size[1], tex, mx, s))
    out = Image.fromarray(cur).convert('RGBA'); out.putalpha(alpha)      # 알파는 원본 그대로
    for it, x, y, bw, bh, tex, mx, s in places:
        mask = Image.new('L', (bw, bh), 0); fbig = ImageFont.truetype(FONTS[it.get('font', 'callig')], 400)
        if it.get('spread'):
            n = len(it['text']); cw = bw // n
            for k, c in enumerate(it['text']):
                gl = Image.new('L', (700, 600), 0); ImageDraw.Draw(gl).text((50, 50), c, font=fbig, fill=255); gl = gl.crop(gl.getbbox())
                gw = min(cw * 0.92, gl.size[0] * (bh * 0.92) / gl.size[1] * it.get('stretch', 1.6))
                gl = gl.resize((max(1, int(gw)), int(bh * 0.92)), Image.LANCZOS); mask.paste(gl, (k * cw + (cw - gl.size[0]) // 2, int(bh * 0.04)))
        else:
            ml, tw = draw_line(it['text'], FONTS[it.get('font', 'brush')], bw, bh, (255, 255, 255), None, 0)
            mask = Image.new('L', (bw, bh), 0); mask.paste(ml.split()[3].crop((0, 0, min(bw, tw + 2), bh)), (max(0, (bw - tw) // 2), 0))   # 가운데
        mb = mask.point(lambda v: 255 if v > 100 else 0)
        rnd = random.Random(3); timg = Image.new('RGB', (bw, bh)); tp = timg.load()
        for yy in range(bh):
            for xx in range(bw): tp[xx, yy] = tex[rnd.randrange(len(tex))] if tex else (60, 30, 30)
        timg = timg.filter(ImageFilter.SMOOTH)
        if it.get('outline'):
            ring = Image.new('RGBA', (bw, bh), it['outline'] + (255,)); ring.putalpha(mb.filter(ImageFilter.MaxFilter(3))); out.alpha_composite(ring, (x, y))
        gly = timg.convert('RGBA'); gly.putalpha(mb); out.alpha_composite(gly, (x, y))
        out.putalpha(alpha)
        print('  %s ← %s 위치 (%d,%d) 배율 %.2f 일치 %.3f' % (name, it['layer'], x, y, s, mx))
    os.makedirs(NEW, exist_ok=True); out.save(os.path.join(NEW, name + '.png'))
    return src, out
