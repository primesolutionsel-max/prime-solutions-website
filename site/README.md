# Prime Solutions website

The Prime Solutions one-page site, built at all three levels from one set of files. Plain HTML, CSS and a small amount of JavaScript. No framework, no build tooling beyond one Python script, nothing loaded from outside the repo.

| Level | Where it is | What it is |
|---|---|---|
| Premium | `index.html` | The front door: a pinned entrance (a stone arch that you walk through, morning to night), then the sheets. |
| Pro | `pro.html` | The same site with the portal picture as the opening, only the swirl turning, layered blocks, scroll reveals and a header that follows you down. Two typefaces. |
| Standard | `standard.html` | The same site, calm and flat. One typeface, one misty-hills picture, a gentle fade on opening. |

Same sections, same words, same prices at every level. Only the treatment changes, so a client can move up a level without starting over.

On `index.html` the Standard and Pro versions also open full screen from the "Three levels" section (`#demo-standard`, `#demo-pro`). The page is built from the same markup in `demos.py`, so the two always match.

## Folder layout

```
site.json            business details, prices, the Forest theme and the six sample layouts
build.py             fills the templates from site.json and writes dist/
demos.py             the Standard and Pro versions (markup), used by build.py for the viewer and for standard.html / pro.html
prep_images.py       turns the pictures in assets_in/ into the small web images in src/img/
assets_in/           the original pictures: trades-sheet.png (six trade photos) and levels-bg.png (misty hills)
src/index.html       the Premium page (uses {{tokens}} from site.json)
src/tier.html        the template for standard.html and pro.html
src/privacy.html     the privacy page template (the text comes from legal/privacy-policy.md)
src/css/styles.css   the Premium page, the demo viewer and the shared rules; the colour theme is at the top
src/css/tiers.css    the Standard (ps-) and Pro (pp-) pages
src/js/intro.js      the entrance
src/js/main.js       scroll, menu, level preview, sample strip, copy address and the demo viewer
src/js/tier.js       the fade-ins and the copy button on standard.html and pro.html
src/img/             portal-far, portal-arch and beyond (the entrance), pro-hero and pro-valley (Pro), levels-bg, six trade photos
src/fonts/           Archivo (headings) and Schibsted Grotesk (body), SIL Open Font License
legal/               privacy-policy.md, the policy text. Fill in the [bracketed] details here
archive/             the earlier plumber sample pages (code and styles), kept in case they are wanted again
dist/                the finished site. Upload this folder to any static host
```

## Build and preview

```
python3 build.py
python3 -m http.server 8000 --directory dist
```

Open http://localhost:8000 (Premium), http://localhost:8000/pro.html or http://localhost:8000/standard.html. Use a local server rather than opening the files directly, because browsers block fonts loaded from file://.

`build.py` needs Python 3 and Pillow (for `prep_images.py`). The site still builds if `assets_in/` is missing: it uses the images already in `src/img/`.

`dist/artifact.html` (Premium), `dist/artifact-standard.html`, `dist/artifact-pro.html` and `dist/prime-solutions-demo.html` are single-file copies with the fonts and pictures embedded, used for quick previews. They are not needed for hosting and are not committed. To link the three previews together, put their addresses in a `preview_links.json` (keys `premium`, `standard`, `pro`) before building.

## Changing things

- Business name, email, prices, description and sample layouts: `site.json`.
- Wording and structure of the Premium page: `src/index.html`. Wording of the Standard and Pro pages: the lists at the top of `demos.py`.
- Colours: the variables at the top of `src/css/styles.css` (theme: Forest). White, black and three greens: Forest, Emerald and Mint. Body text passes 7:1 contrast and the other text pairs pass 4.5:1. The Pro opening and contact text were measured against the pictures.
- Pictures: put new originals in `assets_in/` and run `python3 build.py`. The swirl in the Pro opening is the round copy of the doorway in `pro-hero.webp`; its size and position are the `DOOR` numbers in `build.py`.
- Privacy policy: edit `legal/privacy-policy.md`. Anything in [square brackets] shows highlighted on the page until it is replaced. It is a draft, not legal advice, and needs a South African attorney's review before launch.
- After any change, run `python3 build.py` again.

## Before the domain is known

The pages point the preview image at `og.png` with a relative path. When the live address is decided, change it to the full address (for example `https://example.co.za/og.png`) and add a canonical link.

## Notes

- Fonts are self-hosted copies of the Google Fonts families Archivo and Schibsted Grotesk, subset to Latin. Licences are in `src/fonts/`.
- Motion follows `prefers-reduced-motion`: the entrance is shown open, the swirl does not turn, the fade-ins are off and nothing drifts. The pages store and send no data.
- The pictures are AI-made mood images. The six trade photos stand for trades; they are samples, not client work.
- The Email us buttons are plain `mailto:` links, and the address is also shown as text with a Copy button, so the contact still works where a mail link does nothing.
- Page weight (first load, desktop): Premium about 770 KB, Pro about 490 KB, Standard about 390 KB.
