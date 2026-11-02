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

All pictures on this website were generated with AI (Canva) and are not photographs of real places, people or businesses. The sample pictures are examples of the kind of pages we make. They are not client work and do not show real clients, people or businesses.

- **Six trade pictures** (plumbing, salon, café, garage, cleaning, firm), used in the six sample layouts. Made with Canva's AI image generator for Prime Solutions (Canva media id MAHZMzPIOmk). Used under Canva's AI Product Terms (https://www.canva.com/policies/ai-product-terms/).
- **Misty hills picture**, a soft wash behind "The three levels" on the Standard page. Made with Canva's AI image generator for Prime Solutions (Canva media id MAHZM9iFw5A). Used under Canva's AI Product Terms (https://www.canva.com/policies/ai-product-terms/).
- **Stone arch and valley pictures, and the floating stones cut from the valley picture**, used in the Premium opening, on the Pro page, and faintly behind the contact part of the Standard page. Made with Canva's AI image generator for Prime Solutions (Canva media ids MAHZMjuWsas arch, MAHZMtrkDek valley). Used under Canva's AI Product Terms (https://www.canva.com/policies/ai-product-terms/).
- **Three forest background pictures** (castle, gateway, path), used behind parts of the Standard, Pro and Premium pages. Made with Canva's AI image generator for Prime Solutions (Canva media ids MAHZSdUTrJs castle, MAHZSaQIOqU gateway, MAHZSbUe3Ho path). Used under Canva's AI Product Terms (https://www.canva.com/policies/ai-product-terms/).

The small copies of these pictures made for phones follow the same source and licence as the picture they were made from. The picture shown when a link to this website is shared is drawn by the site's own build from its words, colours and fonts above.

<!-- INTERNAL-START -->
## Open items before go-live (internal, not published)

Cherry's checklist (file 05) says no AI-generated images. On 2 November 2026 the owner decided to keep the Canva AI pictures (all generated in the Prime Solutions Canva account) under Canva's AI Product Terms, disclosed as AI-generated above. Canva's terms do not allow presenting AI pictures as human-made, so keep that disclosure.

Fonts are kept in `src/fonts/` with each licence text (`OFL-*.txt`) and served from the site itself. Three of them are cut-down, renamed copies made by `prep_fonts.py` (Lora to Prime Serif, Poppins to Prime Display, Inter to Prime Text), renamed because a changed copy may not keep the Reserved Font Name. The icons are plain SVG shapes written in this project (`ICONS` in `demos.py` and the page template); `build.py` uses Python 3 and Pillow at build time only, and nothing from them is shipped.

How the pictures are made: `prep_images.py` turns the originals in `assets_in/` into the small web pictures in `src/img/` (the Standard pages mix each background into the off-white with `standard_theme.veil` and `veil_hero` in `site.json`; the Premium page keeps two of them dark). The originals stay in `assets_in/`.
<!-- INTERNAL-END -->
