# 비전서 낱장 세로줄 찾기 — 글자 영역(area) 안 어두운 화소 세로 투영으로 열(오른쪽부터) [(x0,x1,y0,y1)]
import numpy as np
from PIL import Image
import os
D = os.path.dirname(os.path.abspath(__file__))
def cols(k, area, gap=4, minw=8, thr=60):
    im = np.array(Image.open(os.path.join(D, 'png', k + '.png')).convert('L')).astype(float)
    x0, y0, x1, y1 = area; r = im[y0:y1, x0:x1]; bg = np.percentile(r, 70)
    ink = r < bg - thr
    on = ink.sum(axis=0) > 2
    runs = []; i = 0
    while i < len(on):
        if on[i]:
            j = i
            while j < len(on) and (on[j] or on[j + 1:j + 1 + gap].any()): j += 1
            if j - i >= minw:
                ys = np.nonzero(ink[:, i:j].any(axis=1))[0]
                runs.append((x0 + i, x0 + j, y0 + int(ys.min()), y0 + int(ys.max()) + 1))
            i = j
        i += 1
    return runs[::-1]
