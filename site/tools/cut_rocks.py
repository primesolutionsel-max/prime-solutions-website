#!/usr/bin/env python3
"""Cut the floating rocks out of the valley picture so they can drift on their own.

One-off tool (needs opencv-python-headless, numpy and Pillow). The normal build does NOT need it:
its results are committed. Run it only if the valley picture changes.

  reads    assets_in/valley-1680.webp        the original valley picture, rocks painted in
  writes   src/img/rock-<n>.webp             each rock on its own, with soft transparent edges
           src/img/beyond-1680.webp          the valley with the rocks painted out of the sky behind them
           src/rocks.json                    where each rock sits (as % of the picture) and how it floats

Pro and Standard keep using the original picture (prep_images.py makes pro-valley.webp from it).
"""
import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC_IMG = ROOT / "assets_in" / "valley-1680.webp"
OUT = ROOT / "src" / "img"

# a generous box around each floating rock, in picture pixels (x0, y0, x1, y1), and how far to grow the hole that is filled
ROCKS = [
    ("big",   (1195, 190, 1395, 445), 16),
    ("left",  (440, 345, 560, 490), 12),
    ("mid",   (622, 440, 672, 500), 8),
    ("far-a", (1112, 448, 1158, 500), 8),
    ("far-b", (1165, 345, 1205, 392), 8),
    ("far-c", (1402, 445, 1450, 495), 8),
    ("far-d", (358, 484, 392, 528), 8),
]
MARGIN = 6   # transparent space kept around each cut-out


def cut(img, box):
    """grabCut inside the box: the rock is darker and mossier than the cloud and mountain behind it"""
    h, w = img.shape[:2]
    x0, y0, x1, y1 = box
    pad = 18
    X0, Y0, X1, Y1 = max(0, x0 - pad), max(0, y0 - pad), min(w, x1 + pad), min(h, y1 + pad)
    crop = img[Y0:Y1, X0:X1].copy()
    m = np.full(crop.shape[:2], cv2.GC_BGD, np.uint8)
    bx0, by0, bx1, by1 = x0 - X0, y0 - Y0, x1 - X0, y1 - Y0
    m[by0:by1, bx0:bx1] = cv2.GC_PR_FGD
    kx, ky = int((bx1 - bx0) * .3), int((by1 - by0) * .3)
    m[by0 + ky:by1 - ky, bx0 + kx:bx1 - kx] = cv2.GC_FGD
    cv2.grabCut(crop, m, None, np.zeros((1, 65)), np.zeros((1, 65)), 8, cv2.GC_INIT_WITH_MASK)
    fg = ((m == cv2.GC_FGD) | (m == cv2.GC_PR_FGD)).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(fg)
    if n > 1:
        fg = (lab == 1 + np.argmax(st[1:, cv2.CC_STAT_AREA])).astype(np.uint8)
    cnts, _ = cv2.findContours(fg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    fill = np.zeros_like(fg)
    cv2.drawContours(fill, cnts, -1, 1, -1)
    fill = cv2.morphologyEx(fill, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    full = np.zeros((h, w), np.uint8)
    full[Y0:Y1, X0:X1] = fill
    return full


def main():
    bgr = cv2.cvtColor(np.array(Image.open(SRC_IMG).convert("RGB")), cv2.COLOR_RGB2BGR)
    H, W = bgr.shape[:2]
    hole = np.zeros((H, W), np.uint8)
    info = []
    for n, (name, box, grow) in enumerate(ROCKS, 1):
        mask = cut(bgr, box)
        ys, xs = np.nonzero(mask)
        x0, x1, y0, y1 = max(0, xs.min() - MARGIN), min(W, xs.max() + 1 + MARGIN), max(0, ys.min() - MARGIN), min(H, ys.max() + 1 + MARGIN)
        m = mask[y0:y1, x0:x1]
        crop = bgr[y0:y1, x0:x1]
        # colours at the very edge are mixed with the sky, so pull them in from the inside of the rock
        inner = cv2.erode(m, np.ones((3, 3), np.uint8), iterations=2)
        pure = cv2.inpaint(crop, (1 - inner).astype(np.uint8) * 255, 3, cv2.INPAINT_TELEA)
        rgb = np.where(inner[..., None] > 0, crop, pure)
        alpha = cv2.GaussianBlur(cv2.erode(m, np.ones((3, 3), np.uint8)).astype(np.float32), (0, 0), 0.8)
        sprite = np.dstack([cv2.cvtColor(rgb, cv2.COLOR_BGR2RGB), (alpha * 255).astype(np.uint8)])
        Image.fromarray(sprite, "RGBA").save(OUT / f"rock-{n}.webp", "WEBP", quality=88, method=6)
        hole |= cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (grow * 2 + 1, grow * 2 + 1)))
        info.append({"n": n, "name": name, "x": int(x0), "y": int(y0), "w": int(x1 - x0), "h": int(y1 - y0)})
        print(f"rock-{n} ({name}): {x1 - x0}x{y1 - y0} at {x0},{y0}")
    clean = cv2.inpaint(bgr, hole * 255, 6, cv2.INPAINT_TELEA)
    Image.fromarray(cv2.cvtColor(clean, cv2.COLOR_BGR2RGB)).save(OUT / "beyond-1680.webp", "WEBP", quality=82, method=6)
    (ROOT / "src" / "rocks.json").write_text(json.dumps({"picture": [int(W), int(H)], "rocks": info}, indent=1) + "\n")


if __name__ == "__main__":
    main()
