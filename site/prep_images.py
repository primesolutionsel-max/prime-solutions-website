#!/usr/bin/env python3
"""Turn the pictures in assets_in/ into the small web images the site uses (src/img/).

  assets_in/trades-sheet.png   3 x 2 sheet of trade photos  ->  src/img/trade-<key>.webp (six crops)
  assets_in/levels-bg.png      soft landscape               ->  src/img/levels-bg.webp
  assets_in/bg-gateway.webp    the three forest backgrounds ->  src/img/ps-gateway.webp, ps-castle.webp, ps-path.webp
  assets_in/bg-castle.webp     (Standard only: each is mixed into the page's off-white, so it shows softly behind the text;
  assets_in/bg-path.webp        the strength is "veil" (and "veil_hero" for the castle) in site.json, standard_theme)

  (Pro only)                   a soft cloud texture drawn here, and small copies of the big pictures for phones (name-sm.webp)

The site still builds when these are missing: every picture slot has a painted fallback.
"""
import json
from pathlib import Path
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parent
IN, OUT = ROOT / "assets_in", ROOT / "src" / "img"

# the sheet is 1536 x 1024 with white gutters: columns 508-520 and 1021-1033, rows 505-518
CELLS = {
    "plumbing": (0, 0), "salon": (1, 0), "cafe": (2, 0),
    "garage": (0, 1), "cleaning": (1, 1), "firm": (2, 1),
}
COLS = [(0, 507), (521, 1020), (1034, 1535)]
ROWS = [(0, 504), (519, 1023)]
INSET = 4          # stay clear of the white gutter


def save(im, path, **kw):
    """write a web picture, but leave the file alone when it would come out the same (keeps the git history quiet)"""
    if path.exists():
        old = Image.open(path).convert("RGB")
        if old.size == im.size and ImageChops.difference(old, im.convert("RGB")).getbbox() is None:
            return
    im.save(path, "WEBP", **kw)


def main():
    derive()
    veiled()
    mist()
    sheet = IN / "trades-sheet.png"
    if sheet.exists():
        im = Image.open(sheet).convert("RGB")
        sx, sy = im.width / 1536, im.height / 1024
        for key, (c, r) in CELLS.items():
            x0, x1 = COLS[c]; y0, y1 = ROWS[r]
            box = (round((x0 + INSET) * sx), round((y0 + INSET) * sy), round((x1 - INSET) * sx), round((y1 - INSET) * sy))
            crop = im.crop(box)
            if crop.width > 520:
                crop = crop.resize((520, round(crop.height * 520 / crop.width)), Image.LANCZOS)
            save(crop, OUT / f"trade-{key}.webp", quality=72, method=6)
            save(crop.resize((360, round(crop.height * 360 / crop.width)), Image.LANCZOS), OUT / f"trade-{key}-sm.webp", quality=66, method=6)
    bg = IN / "levels-bg.png"
    if bg.exists():
        im = Image.open(bg).convert("RGB")
        if im.width > 1400:
            im = im.resize((1400, round(im.height * 1400 / im.width)), Image.LANCZOS)
        save(im, OUT / "levels-bg.webp", quality=58, method=6)


def veiled():
    """the Standard backgrounds: the picture mixed into the page's off-white. veil is the share of off-white (0.74 = three parts paper, one part picture)"""
    t = json.loads((ROOT / "site.json").read_text(encoding="utf-8"))["standard_theme"]
    paper = tuple(int(t["paper"].lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
    # the castle valley is the opening's picture and is kept strong ("veil_hero"); the two band pictures stay light ("veil")
    for src, dst, key, size, q in (("bg-gateway", "ps-gateway", "veil", (1440, 809), 62), ("bg-castle", "ps-castle", "veil_hero", (1600, 899), 58),
                                   ("bg-path", "ps-path", "veil", (1440, 809), 62)):
        f = IN / f"{src}.webp"
        if not f.exists():
            continue
        im = Image.open(f).convert("RGB").resize(size, Image.LANCZOS)
        im = Image.blend(im, Image.new("RGB", im.size, paper), float(t.get(key, t["veil"])))
        save(im, OUT / f"{dst}.webp", quality=q, method=6)
        save(im.resize((800, round(im.height * 800 / im.width)), Image.LANCZOS), OUT / f"{dst}-sm.webp", quality=q - 4, method=6)   # for phones


def mist():
    """a soft cloud texture (pale green-white, see-through, fading out toward its edges) for the clouds that swirl into the Pro portal.
    Smoothed random noise, bent into spiral arms around the centre so that turning it while it shrinks reads as a vortex. Fixed seed: same every time."""
    import numpy as np
    n, big = 320, 640
    rng = np.random.default_rng(11)
    f, amp, tot = np.zeros((big, big)), 1.0, 0.0
    for o in range(5):
        g = rng.random((3 * 2 ** o, 3 * 2 ** o))
        f += np.asarray(Image.fromarray((g * 255).astype("uint8")).resize((big, big), Image.BICUBIC), float) / 255 * amp
        tot += amp
        amp *= .55
    f /= tot
    y, x = np.mgrid[0:n, 0:n] / (n - 1)
    dx, dy = (x - .5) * 2, (y - .5) * 2
    r, th = np.sqrt(dx ** 2 + dy ** 2), np.arctan2(dy, dx)
    th2 = th + 3.4 * r                                          # the spiral: the further out, the more the noise is wound
    u = np.clip(((.5 + .5 * r * np.cos(th2)) * (big - 1)).astype(int), 0, big - 1)
    v = np.clip(((.5 + .5 * r * np.sin(th2)) * (big - 1)).astype(int), 0, big - 1)
    d = np.clip((f[v, u] - .35) * 3.0, 0, 1)
    d = d * d * (3 - 2 * d)                                     # smoothstep: soft cloud edges
    fall = np.clip(1 - r, 0, 1)
    fall = fall * fall * (3 - 2 * fall)
    inner = np.clip(r / .16, 0, 1)                              # a clear hole at the very centre, where the light is
    a = np.clip(d * fall * inner * 1.4, 0, .95)
    a = np.clip(a + (rng.random(a.shape) - .5) * .006, 0, 1)    # a whisper of grain so the soft edges do not band
    lo, hi = np.array([140, 224, 180], float), np.array([236, 252, 242], float)
    rgb = lo + (hi - lo) * d[..., None]
    out = np.dstack([rgb, a * 255]).astype("uint8")
    Image.fromarray(out, "RGBA").save(OUT / "pro-mist.webp", "WEBP", quality=70, alpha_quality=80, method=6)


def derive():
    """small copies of the portal and valley pictures for the Pro and Standard versions"""
    # Pro and Standard use the whole valley picture, with its stones in place. (Premium's own copy, beyond-1680.webp,
    # has the stones painted out because they float on their own: see tools/cut_rocks.py.)
    far, valley = OUT / "portal-far-1680.webp", IN / "valley-1680.webp"
    if far.exists():
        im = Image.open(far).convert("RGB").resize((1400, 787), Image.LANCZOS)
        save(im, OUT / "pro-hero.webp", quality=58, method=6)
        save(im.resize((900, round(im.height * 900 / im.width)), Image.LANCZOS), OUT / "pro-hero-sm.webp", quality=54, method=6)
    if valley.exists():
        im = Image.open(valley).convert("RGB").resize((1200, 674), Image.LANCZOS)
        save(im, OUT / "pro-valley.webp", quality=50, method=6)
        save(im.resize((720, round(im.height * 720 / im.width)), Image.LANCZOS), OUT / "pro-valley-sm.webp", quality=46, method=6)


if __name__ == "__main__":
    main()
