# Credits and licences

Every picture, font and piece of code that is not written for this project is listed here, with where it came from and the licence it is used under.
Nothing is loaded from outside the repository (no Google Fonts, no CDN, no outside scripts or pictures).

Rules for this list: no AI-generated material, no watermarked material, and no picture that suggests a real client unless it is true.
The three Standard background pictures below were made with an AI image tool (the Canva connector), so they break the first rule. They are in the draft so the Standard look can be judged, and they are marked below for the owner to decide: keep them, or replace them with licensed or own pictures.
Anything not yet known is a marked field. The build lists every open marker in `OPEN-MARKERS.md`, and refuses to build a site marked `live` while one is open here.

## Fonts (kept in `src/fonts/`, served from the site itself)

| Font | Author | Licence | Used for |
|---|---|---|---|
| Archivo (variable, Latin subset) | The Archivo Project Authors, https://github.com/Omnibus-Type/Archivo | SIL Open Font License 1.1, text in `src/fonts/OFL-archivo.txt` | Headings (Pro and Premium) |
| Schibsted Grotesk (variable, Latin subset) | The Schibsted Grotesk Project Authors, https://github.com/schibsted/schibsted-grotesk | SIL Open Font License 1.1, text in `src/fonts/OFL-schibsted.txt` | Body text (Pro and Premium) |
| Prime Serif (variable, Latin subset): Lora 3.008 cut down and renamed | The Lora Project Authors, https://github.com/cyrealtype/Lora-Cyrillic | SIL Open Font License 1.1, text and the rename note in `src/fonts/OFL-lora.txt` | The only typeface on the Standard page (headings and text). Renamed because a changed copy may not keep the Reserved Font Name "Lora". |

## Libraries and code

None. The site is plain HTML, CSS and a little JavaScript. `build.py` uses Python 3 and Pillow (build time only, nothing from it is shipped).
The small icons are plain SVG shapes written in this project (`ICONS` in `demos.py`, and the page template); no icon library is used.
`og.png` (the picture shown when the link is shared) is drawn by `build.py` from the words in `site.json`, the Forest colours and the fonts above.

## Pictures (`src/img/`, made from the originals in `assets_in/`)

| Pictures | Source | Licence | Notes |
|---|---|---|---|
| `trade-plumbing`, `trade-salon`, `trade-cafe`, `trade-garage`, `trade-cleaning`, `trade-firm` (crops of `assets_in/trades-sheet.png`) | [TO BE SUPPLIED: where the six trade pictures came from (author or website, and the link)] | [TO BE SUPPLIED: the licence they are used under] | Used as sample pictures for six trades. They are samples, not client work, and the page says so. |
| `levels-bg` (from `assets_in/levels-bg.png`) | [TO BE SUPPLIED: where the misty-hills picture came from (author or website, and the link)] | [TO BE SUPPLIED: the licence it is used under] | The sunrise hills picture, shown as a soft wash behind "The three levels" on the Standard page. |
| `portal-far-1680`, `portal-arch-1680` (the Premium entrance), `pro-hero`, `pro-valley` and `assets_in/valley-1680.webp` (the Pro opening; the Standard page also uses `pro-hero` still, in a frame, and `pro-valley` faintly behind its contact part) | [TO BE SUPPLIED: where the stone arch and valley pictures came from (author or website, and the link)] | [TO BE SUPPLIED: the licence they are used under] | |
| `beyond-1680` and `rock-1` to `rock-7` | The same valley picture as above | The same licence | Made here by `tools/cut_rocks.py`: the floating stones are cut out of the valley picture and the gap is filled in. They are a change to that picture, so they follow its licence. |

| `ps-castle`, `ps-gateway`, `ps-path` (made from `assets_in/bg-castle.webp`, `bg-gateway.webp`, `bg-path.webp`) | AI-generated with Canva's image generator (Canva media ids MAHZSdUTrJs castle, MAHZSaQIOqU gateway, MAHZSbUe3Ho path) and supplied by the project owner. [TO BE SUPPLIED: the owner's decision to keep them, with the Canva terms that apply to AI-generated images, or the replacement pictures and their sources] | [TO BE SUPPLIED: the licence they are used under] | The three soft forest backgrounds on the Standard page (the castle valley behind the opening, the stone gateway behind "What is included", the mossy path behind "Questions"). `prep_images.py` mixes each into the off-white (`standard_theme.veil` in `site.json`) so they stay light, and saves it small. The originals are kept in `assets_in/`. |

Before the site goes live, check each row:

- An earlier version of the README described these pictures as AI-made mood images. If that is true for any of them, they break the rule above (no AI-generated material) and need replacing, or the rule needs the owner's decision.
- Check none of them is watermarked and that none suggests a real client.
