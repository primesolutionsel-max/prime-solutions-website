# Open markers

Written by `build.py` every time it runs. Do not edit by hand. Each line is something that has not been supplied yet.
Fill it in where it says (a legal page, or a field in `site.json`), run `python3 build.py`, and it drops off this list.

Site status: **draft** · Mode: **advertise-only** · Markers open: **4**

| Where | Marker |
|---|---|
| `CREDITS.md` | [TO BE SUPPLIED: where the six trade pictures came from (author or website, and the link) and the licence they are used under (`assets_in/trades-sheet.png`; crops `trade-*.webp`)] |
| `CREDITS.md` | [TO BE SUPPLIED: where the misty-hills picture came from (author or website, and the link) and the licence it is used under (`assets_in/levels-bg.png`; `levels-bg.webp`)] |
| `CREDITS.md` | [TO BE SUPPLIED: where the stone arch and valley pictures came from (author or website, and the link) and the licence they are used under (`portal-arch`, `portal-far`, `pro-hero`, `pro-valley`, `valley-1680`, `beyond-1680`, `rock-1` to `rock-7`, cut by `tools/cut_rocks.py`)] |
| `CREDITS.md` | [TO BE SUPPLIED: the owner's decision on the three Canva AI forest backgrounds (`ps-*`, `pm-*`, made from `assets_in/bg-*.webp`; Canva media ids MAHZSdUTrJs castle, MAHZSaQIOqU gateway, MAHZSbUe3Ho path): replace them with pictures that have a known licence, or keep them with the Canva terms that apply to AI-generated images] |

A marker is any text in square brackets that starts with one of: `[TO BE SUPPLIED`, `[JASON TO SUPPLY`, `[ATTORNEY`, `[VERIFY`, `[CLAUDE INSTRUCTION`, `[TO DECIDE`.
A page, or the site, marked `live` cannot be built while a marker is open in it.
