# Prime Solutions website

Premium-level, one-page site for Prime Solutions. Plain HTML, CSS and a small amount of JavaScript. No framework, no build tooling beyond one Python script, nothing loaded from outside the repo.

## Folder layout

```
site.json          business details, prices and the six sample layouts
build.py           fills src/index.html from site.json and writes dist/
src/index.html     page structure and copy (uses {{tokens}} from site.json)
src/privacy.html   privacy page template (the text comes from legal/privacy-policy.md)
legal/             privacy-policy.md, the policy text. Fill in the [bracketed] details here
src/img/           hero-banner.webp, the hero banner from Grokbot (compressed to about 7 KB)
src/css/styles.css all styles, with the colour theme as variables at the top
src/js/main.js     scroll, menu, level preview, endless sample strip and copy-address behaviour
src/fonts/         Archivo (headings) and Schibsted Grotesk (body), SIL Open Font License
src/og.png         preview image for shared links (1200 x 630)
dist/              the finished site. Upload this folder to any static host
```

## Build and preview

```
python3 build.py
python3 -m http.server 8000 --directory dist
```

Open http://localhost:8000. Use a local server rather than opening the file directly, because browsers block fonts loaded from file://.

`dist/artifact.html` is a single-file copy with the fonts embedded, used for quick previews. It is not needed for hosting.

## Changing things

- Business name, email, prices, description and sample layouts: `site.json`.
- Wording and page structure: `src/index.html`.
- Colours: the variables at the top of `src/css/styles.css` (theme: Forest). White, black and three greens: Forest, Emerald and Mint. Contrast was checked for every text and background pair in use.
- Privacy policy: edit `legal/privacy-policy.md`. Anything in [square brackets] shows highlighted on the page until it is replaced. It is a draft, not legal advice, and needs a South African attorney's review before launch.
- After any change, run `python3 build.py` again.

## Before the domain is known

`src/index.html` points the preview image at `og.png` with a relative path. When the live address is decided, change it to the full address (for example `https://example.co.za/og.png`) and add a canonical link.

## Notes

- Fonts are self-hosted copies of the Google Fonts families Archivo and Schibsted Grotesk, subset to Latin. Licences are in `src/fonts/`.
- Motion follows `prefers-reduced-motion`: the strip starts paused, the hero is shown already built and nothing tilts. The page stores and sends no data.
- The sample strip repeats its six samples on both sides and wraps around one set, so it never ends and never jumps. It drifts slowly, slows under the mouse, and carries on in whichever direction it was last pushed (drag, swipe, arrows, sideways wheel or arrow keys). A Pause button stops it.
