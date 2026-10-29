# Credits and licences

Every picture, font and piece of code on this website that was not written for it is listed here, with where it came from and the licence it is used under. Nothing is loaded from other websites: fonts, pictures, scripts and styles are all served from this site.

## Fonts

All five typefaces are used under the SIL Open Font License 1.1. The licence text of each is kept with the font files on this site.

- **Archivo** (variable, Latin subset). By the Archivo Project Authors. Source: https://github.com/Omnibus-Type/Archivo · Licence text: fonts/OFL-archivo.txt on this site. Used for headings on the Pro page, and on the Pro sample inside the Premium page.
- **Schibsted Grotesk** (variable, Latin subset). By the Schibsted Grotesk Project Authors. Source: https://github.com/schibsted/schibsted-grotesk · Licence text: fonts/OFL-schibsted.txt on this site. Used for body text on the Pro page, and on the Pro sample inside the Premium page.
- **Prime Serif**, a cut-down, renamed copy of Lora 3.008 (variable, Latin subset). By the Lora Project Authors. Source: https://github.com/cyrealtype/Lora-Cyrillic · Licence text: fonts/OFL-lora.txt on this site. The only typeface on the Standard page. It is renamed because a changed copy may not keep the font's Reserved Font Name.
- **Prime Display**, a cut-down, renamed copy of Poppins Medium and Bold (Latin subset). By the Poppins Project Authors. Source: https://github.com/itfoundry/poppins · Licence text: fonts/OFL-poppins.txt on this site. Used for headings on the Premium page and its legal pages.
- **Prime Text**, a cut-down, renamed copy of Inter Regular and SemiBold (Latin subset). By the Inter Project Authors. Source: https://github.com/rsms/inter · Licence text: fonts/OFL-inter.txt on this site. Used for body text on the Premium page and its legal pages.

## Code

The website is plain HTML, CSS and a little JavaScript written for it. It uses no library and no framework, and loads no code from other companies. The small icons are plain shapes drawn for this site.

## Pictures

The sample pictures on this website are examples of the kind of pages we make. They are not client work and do not show real clients, people or businesses.

- **Six trade pictures** (plumbing, salon, café, garage, cleaning, firm), used in the six sample layouts. Source: not yet recorded. Licence: not yet recorded.
- **Misty hills picture**, a soft wash behind "The three levels" on the Standard page. Source: not yet recorded. Licence: not yet recorded.
- **Stone arch and valley pictures, and the floating stones cut from the valley picture**, used in the Premium opening, on the Pro page, and faintly behind the contact part of the Standard page. Source: not yet recorded. Licence: not yet recorded.
- **Three forest background pictures** (castle, gateway, path), used behind parts of the Standard, Pro and Premium pages. Made with Canva's AI image generator for Prime Solutions. Licence: not yet recorded (Canva's terms for AI-generated images apply).

The small copies of these pictures made for phones follow the same source and licence as the picture they were made from. The picture shown when a link to this website is shared is drawn by the site's own build from its words, colours and fonts above.

<!-- INTERNAL-START -->
## Open items before go-live (internal, not published)

Cherry's checklist (file 05) says: no AI-generated images; no picture with an unknown licence; none that implies a real client. Today every picture on the site falls under the first two. They are kept in this draft so the three looks can be judged, and each is a marked item below. The build lists them in `OPEN-MARKERS.md` and refuses to build a site marked `live` while one is open.

- [TO BE SUPPLIED: where the six trade pictures came from (author or website, and the link) and the licence they are used under (`assets_in/trades-sheet.png`; crops `trade-*.webp`)]
- [TO BE SUPPLIED: where the misty-hills picture came from (author or website, and the link) and the licence it is used under (`assets_in/levels-bg.png`; `levels-bg.webp`)]
- [TO BE SUPPLIED: where the stone arch and valley pictures came from (author or website, and the link) and the licence they are used under (`portal-arch`, `portal-far`, `pro-hero`, `pro-valley`, `valley-1680`, `beyond-1680`, `rock-1` to `rock-7`, cut by `tools/cut_rocks.py`)]
- [TO BE SUPPLIED: the owner's decision on the three Canva AI forest backgrounds (`ps-*`, `pm-*`, made from `assets_in/bg-*.webp`; Canva media ids MAHZSdUTrJs castle, MAHZSaQIOqU gateway, MAHZSbUe3Ho path): replace them with pictures that have a known licence, or keep them with the Canva terms that apply to AI-generated images]

Fonts are kept in `src/fonts/` with each licence text (`OFL-*.txt`) and served from the site itself. Three of them are cut-down, renamed copies made by `prep_fonts.py` (Lora to Prime Serif, Poppins to Prime Display, Inter to Prime Text), renamed because a changed copy may not keep the Reserved Font Name. The icons are plain SVG shapes written in this project (`ICONS` in `demos.py` and the page template); `build.py` uses Python 3 and Pillow at build time only, and nothing from them is shipped.

How the pictures are made: `prep_images.py` turns the originals in `assets_in/` into the small web pictures in `src/img/` (the Standard pages mix each background into the off-white with `standard_theme.veil` and `veil_hero` in `site.json`; the Premium page keeps two of them dark). The originals stay in `assets_in/`.
<!-- INTERNAL-END -->
