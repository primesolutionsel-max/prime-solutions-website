#!/usr/bin/env python3
"""Turn the pictures in assets_in/ into the small web images the site uses (src/img/).

  assets_in/trades-sheet.png   3 x 2 sheet of trade photos  ->  src/img/trade-<key>.webp (six crops)
  assets_in/levels-bg.png      soft landscape               ->  src/img/levels-bg.webp

The site still builds when these are missing: every picture slot has a painted fallback.
"""
from pathlib import Path
from PIL import Image

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


def main():
    derive()
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
            crop.save(OUT / f"trade-{key}.webp", "WEBP", quality=72, method=6)
    bg = IN / "levels-bg.png"
    if bg.exists():
        im = Image.open(bg).convert("RGB")
        if im.width > 1400:
            im = im.resize((1400, round(im.height * 1400 / im.width)), Image.LANCZOS)
        im.save(OUT / "levels-bg.webp", "WEBP", quality=58, method=6)


def derive():
    """small copies of the portal and valley pictures for the Pro and Standard versions"""
    far, beyond = OUT / "portal-far-1680.webp", OUT / "beyond-1680.webp"
    if far.exists():
        im = Image.open(far).convert("RGB").resize((1400, 787), Image.LANCZOS)
        im.save(OUT / "pro-hero.webp", "WEBP", quality=58, method=6)
    if beyond.exists():
        im = Image.open(beyond).convert("RGB").resize((1200, 674), Image.LANCZOS)
        im.save(OUT / "pro-valley.webp", "WEBP", quality=50, method=6)


if __name__ == "__main__":
    main()
