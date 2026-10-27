# Credits and licences

Every picture, font and piece of code that is not written for this project is listed here, with where it came from and the licence it is used under.
Nothing is loaded from outside the repository (no Google Fonts, no CDN, no outside scripts or pictures).

Rules for this list: no AI-generated material, no watermarked material, and no picture that suggests a real client unless it is true.
Anything not yet known is a marked field. The build lists every open marker in `OPEN-MARKERS.md`, and refuses to build a site marked `live` while one is open here.

## Fonts (kept in `src/fonts/`, served from the site itself)

| Font | Author | Licence | Used for |
|---|---|---|---|
| Archivo (variable, Latin subset) | The Archivo Project Authors, https://github.com/Omnibus-Type/Archivo | SIL Open Font License 1.1, text in `src/fonts/OFL-archivo.txt` | Headings (Pro and Premium; Standard uses Schibsted Grotesk only) |
| Schibsted Grotesk (variable, Latin subset) | The Schibsted Grotesk Project Authors, https://github.com/schibsted/schibsted-grotesk | SIL Open Font License 1.1, text in `src/fonts/OFL-schibsted.txt` | Body text (all three levels) |

## Libraries and code

None. The site is plain HTML, CSS and a little JavaScript. `build.py` uses Python 3 and Pillow (build time only, nothing from it is shipped).
The small icons are plain SVG shapes written in this project (`ICONS` in `demos.py`, and the page template); no icon library is used.
`og.png` (the picture shown when the link is shared) is drawn by `build.py` from the words in `site.json`, the Forest colours and the fonts above.

## Pictures (`src/img/`, made from the originals in `assets_in/`)

| Pictures | Source | Licence | Notes |
|---|---|---|---|
| `trade-plumbing`, `trade-salon`, `trade-cafe`, `trade-garage`, `trade-cleaning`, `trade-firm` (crops of `assets_in/trades-sheet.png`) | [TO BE SUPPLIED: where the six trade pictures came from (author or website, and the link)] | [TO BE SUPPLIED: the licence they are used under] | Used as sample pictures for six trades. They are samples, not client work, and the page says so. |
| `levels-bg` (from `assets_in/levels-bg.png`) | [TO BE SUPPLIED: where the misty-hills picture came from (author or website, and the link)] | [TO BE SUPPLIED: the licence it is used under] | The hills picture on the Standard opening. |
| `portal-far-1680`, `portal-arch-1680` (the Premium entrance), `pro-hero`, `pro-valley` and `assets_in/valley-1680.webp` (the Pro opening) | [TO BE SUPPLIED: where the stone arch and valley pictures came from (author or website, and the link)] | [TO BE SUPPLIED: the licence they are used under] | |
| `beyond-1680` and `rock-1` to `rock-7` | The same valley picture as above | The same licence | Made here by `tools/cut_rocks.py`: the floating stones are cut out of the valley picture and the gap is filled in. They are a change to that picture, so they follow its licence. |

Before the site goes live, check each row:

- An earlier version of the README described these pictures as AI-made mood images. If that is true for any of them, they break the rule above (no AI-generated material) and need replacing, or the rule needs the owner's decision.
- Check none of them is watermarked and that none suggests a real client.
