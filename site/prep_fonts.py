#!/usr/bin/env python3
"""Premium typefaces: cut-down, renamed copies of two open-licence fonts, written to src/fonts/.

  Poppins (Medium, Bold)       -> prime-display-medium.woff, prime-display-bold.woff   family "Prime Display"   headings
  Inter   (Regular, SemiBold)  -> prime-text-regular.woff,   prime-text-semibold.woff  family "Prime Text"      body text

Both are under the SIL Open Font License 1.1 (texts in src/fonts/OFL-poppins.txt and OFL-inter.txt). A cut-down copy is a changed copy,
so it is renamed. Only the Latin letters, numbers and the punctuation this site uses are kept (see UNICODES).
The source fonts are the ones installed on the build machine (/usr/share/fonts); the finished .woff files are committed, so this
script only needs to run again if the cut or the weights change:   python3 prep_fonts.py
"""
from pathlib import Path
from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "src" / "fonts"
UNICODES = list(range(0x20, 0x7F)) + list(range(0xA0, 0x100)) + [0x2013, 0x2014, 0x2018, 0x2019, 0x201C, 0x201D, 0x2022, 0x2026, 0x2190, 0x2192, 0x2212, 0x00D7]
FEATURES = ["kern", "liga", "calt", "ccmp", "locl", "mark", "mkmk", "tnum", "lnum", "case"]

JOBS = [
    # source file, output name, new family, style, version note
    ("/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf", "prime-display-medium.woff", "Prime Display", "Medium", "Poppins Medium"),
    ("/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf", "prime-display-bold.woff", "Prime Display", "Bold", "Poppins Bold"),
    ("/usr/share/fonts/opentype/inter/Inter-Regular.otf", "prime-text-regular.woff", "Prime Text", "Regular", "Inter Regular"),
    ("/usr/share/fonts/opentype/inter/Inter-SemiBold.otf", "prime-text-semibold.woff", "Prime Text", "SemiBold", "Inter SemiBold"),
]


def rename(font, family, style, note):
    name = font["name"]
    full = f"{family} {style}"
    ps = f"{family.replace(' ', '')}-{style}"
    keep = {0, 13, 14}   # copyright and licence lines stay
    name.names = [n for n in name.names if n.nameID in keep]
    for pid, eid, lid in ((3, 1, 0x409), (1, 0, 0)):
        name.setName(family, 1, pid, eid, lid)
        name.setName(style, 2, pid, eid, lid)
        name.setName(f"{family} subset of {note}", 3, pid, eid, lid)
        name.setName(full, 4, pid, eid, lid)
        name.setName("Version 1.0", 5, pid, eid, lid)
        name.setName(ps, 6, pid, eid, lid)


def main():
    for src, dst, family, style, note in JOBS:
        opts = subset.Options()
        opts.flavor = "woff"
        opts.layout_features = FEATURES
        opts.name_IDs = ["*"]
        opts.notdef_outline = True
        opts.hinting = False
        opts.desubroutinize = True
        font = subset.load_font(src, opts)
        sub = subset.Subsetter(opts)
        sub.populate(unicodes=UNICODES)
        sub.subset(font)
        rename(font, family, style, note)
        subset.save_font(font, str(OUT / dst), opts)
        print(f"{dst}: {(OUT / dst).stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
