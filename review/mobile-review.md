# Review: prime-solutions-website.zip (from fezco-co/prime-solutions-website, read only)

## What's in the zip (469 KB zipped)
```
prime-solutions-website/
  README.md 2.4K   build.py 9.4K   site.json 3.0K   .gitignore
  src/  index.html 13.9K (template)  css/styles.css 36.5K  js/main.js 14.5K  og.png 80K
        fonts/archivo-display.woff 84K  schibsted-body.woff 44K  + 2 licence txt
  dist/ (finished site, same files, index.html 22.1K)
```
Finished page (dist) weighs about 280 KB in total. There are no photos; the heaviest files are the heading font (84 KB) and og.png (80 KB, used only for link previews).

## Verdict
Good quality. It's plain HTML/CSS/JS with no framework, built from site.json by build.py. It's one page, has a working phone menu, and loads nothing from outside the repo. **The phone layout tested well:** nothing scrolls sideways at 375, 390, 768 or 1280 px, even with the page-wide sideways clip turned off. Body text is 17px. All buttons are at least 44px. There are no console errors, and the menu opens, closes and jumps to the section you tap. The "phone not doing well" complaint is about polish, not broken layout. If the owner saw it on an older copy, or by double-clicking the file, that may be why.

## Phone problems found (with fixes)
1. **Small label text, 13px**: `.eyebrow`, `.step__tag`, `.sample figcaption span` (styles.css lines 89, 468). These are uppercase, letter-spaced labels and are hard to read on phones. Fix: use at least `.875rem` (14px) and reduce the letter-spacing to about `.08em` under 700px.
2. **Fake website previews have tiny text**: `.m` / `.m-*` mock text uses `cqw` sizes (lines 359–403). In the hero "browser" at 375px, words like "Service one" are about 6–8px. That's fine as decoration, but it looks blurry and cramped. Fix: hide the small lines on phones (`@media (max-width:600px){.m p,.m-cols,.m-nav span{display:none}}`) or make the mock taller.
3. **Hero is long on phones**: the big heading (54px at 375) plus the preview mock push the level picker well below the first screen. Fix: under 420px use `clamp(2.25rem, 12vw, 3rem)` for `.hero__title` and shrink or hide `.hero__visual`.
4. **Sample strip moves by itself**: `.samples__rail.is-loop` sets `touch-action: pan-y` and keeps drifting. On phones a moving strip is distracting and can fight swipes. Fix: start it paused on touch devices (`matchMedia('(hover: none)')` in main.js) and show the Pause/Play button.
5. **Light borders on outline buttons**: `--line-strong` #76817A on white is 4.05:1 (lines 158, 303, 438, 443). That passes the 3:1 rule for outlines, but the borders look faint in sunlight. Optional fix: darken it to #5F6A64.
6. **Opening by double-click**: no fetch() is used (site.json is baked in at build time), so double-clicking index.html works, and fonts did load in a file:// test in Chromium. The README warns that some browsers block fonts on file://. That's fine, but tell the owner to test on the hosted preview, not a local file.
7. Scroll-reveal sections stay faded until scrolled into view. Real phones are fine, but full-page screenshots show faded blocks, which is expected and not a bug.

## Criteria
| Criterion | Result |
|---|---|
| Static HTML/CSS/small JS, no framework | PASS (no GSAP even) |
| Content from one site.json | PASS (build.py); field names across tiers can't be checked, since this is the only site |
| One page | PASS |
| Header logo / no Prime credit in header | N/A, this is Prime Solutions' own site (text logo) |
| "Website by Prime Solutions" footer credit | N/A for own site (footer shows © 2026 Prime Solutions); needs adding in client templates |
| Email as main contact, no forms | PASS (3 mailto links, copy-address button, no form, no WhatsApp since none supplied) |
| One theme, no dark switch | PASS |
| Contrast: body ink/white 19.3:1; slate muted text 8.4 (white), 7.0 (mint); buttons white/forest 7.95; links forest 7.95; accent emerald on ink 6.75 | PASS (emerald on white would be 2.87, but it's only used on dark) |
| Google Fonts | PASS (self-hosted Archivo + Schibsted Grotesk, OFL) |
| Reduced motion | PASS (0 running animations with reduce on) |
| 375–1280 with no sideways scroll | PASS |
| Light weight | PASS (~280 KB) |
| SEO: title, description, JSON-LD (ProfessionalService), og image, favicon | PASS, but og:image is relative; it needs a full URL and a canonical link once the domain is known |
| No analytics/maps/embeds | PASS |
| No invented reviews | PASS |
| Relative paths / double-click | PASS |

Screenshots in /workspace/review/shots: 375.png, 390.png, 768.png, 1280.png (full page), *-menu.png (open phone menu), 375-screen00..10.png (phone screen-by-screen), strip0/1.png (contact sheets), file-protocol.png.
