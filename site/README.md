# Prime Solutions website

**This repository (`prime-solutions-website`) is the master.** The Premium, Pro and Standard pages, the legal pages and all wording live here and only here. A copy of any of them kept somewhere else is out of date the moment this one changes: change it here, run `python3 build.py`, and upload `dist/`.

**Mode: Advertise Only.** The site tells people what Prime Solutions offers and how to get in touch by email. Nothing is bought, booked, paid for or signed up for on the site. It has no forms, no payments, no sign-ups, no analytics, no cookies and no tracking, and it makes no request to any outside server. The mode is one setting, `"mode": "advertise-only"` in `site.json`. It is shown in the footer of every page.

Plain HTML, CSS and a small amount of JavaScript. No framework, no build tooling beyond one Python script, nothing loaded from outside the repository.

## The three levels, on one address

| Level | Address | What it is |
|---|---|---|
| Premium | `/` (the main address) | The front door: a pinned entrance (a stone arch you walk through with one swipe, with the stones floating gently), then the sheets. Poppins headings and Inter text (renamed Prime Display and Prime Text), the three forest pictures behind the samples, "How it works" and contact, and light pointer effects on top. |
| Pro | `/pro/` | The same site with the dark portal picture as the opening, and the swirl in its doorway turning like a vortex around the white light. Below it the Standard colours (off-white, black, pastel and forest green), the same three forest pictures behind its bands (they melt into the page at their edges), layered blocks, scroll reveals and cards that lift on hover. The header follows you down: clear over the opening, a soft off-white veil below it, links in the middle, a burger on phones, and the link of the part you are reading underlined. Two typefaces. Less rich than Premium. No zoom-in opening. |
| Standard | `/standard/` | The same site, calm and finished, in its own look: off-white (the main colour), black, pastel green and forest green, set in one serif typeface (Prime Serif, a cut-down copy of Lora). The opening has no portal: the castle-and-tower valley picture sits strong behind it and fades out as "The three levels" begins. Two more forest pictures sit lightly behind two bands, and the sunrise sky and the valley appear faintly. The header has no bar: links sit in the middle and a burger menu takes over on phones. A slow fade as each part arrives, nothing on hover. |

Premium shows Standard and Pro in its "Three levels" section, and every level links to the others. Same sections, same words, same prices at every level. Only the treatment changes (Premium is richer than Pro, and Pro is richer than Standard).

The legal pages are at `/privacy/`, `/terms/` and `/refunds/`, and every page links to all three from its footer.

## Where things live

```
site.json            ALL the wording (copy), prices, contact email, mode, status, the domain, the Forest theme, the six sample layouts
legal/privacy.md     the privacy policy      one source file per legal page, each with its own version and last-updated line
legal/terms.md       the terms
legal/refunds.md     the refund and cancellation page
CREDITS.md           the source and licence of every picture and font
OPEN-MARKERS.md      the one list of everything still to be supplied (written by the build; do not edit)
build.py             fills the templates from site.json and legal/, writes dist/, checks the markers
demos.py             the markup of the Standard and Pro pages (no wording in it: it reads site.json)
prep_images.py       turns the originals in assets_in/ into the small web images in src/img/
prep_fonts.py        cuts down and renames the Premium fonts (Poppins, Inter) into src/fonts/ (run only if the cut or the weights change)
tools/cut_rocks.py   cuts the floating stones out of the valley picture (run only if that picture changes)
assets_in/           the original pictures
src/index.html       the Premium page template ({{tokens}} filled from site.json)
src/tier.html        the template for the Standard and Pro pages
src/legal.html       the template for the legal pages
src/css, src/js      styles and scripts (styles.css, tiers.css, intro.js, main.js, tier.js)
src/img, src/fonts   web pictures and the local fonts (Poppins and Inter for Premium, Archivo and Schibsted Grotesk for Pro, Lora for Standard; all SIL Open Font License)
archive/             old files kept only so nothing is lost; do not use or publish them
dist/                the finished site. Upload this folder to any static host
```

## Build and preview

```
python3 build.py
python3 -m http.server 8000 --directory dist
```

Open http://localhost:8000 (Premium), http://localhost:8000/pro/ and http://localhost:8000/standard/. Use a local server rather than opening the files, because browsers block fonts loaded from file://.

`build.py` needs Python 3 and Pillow (also used to draw `og.png`). The site still builds if `assets_in/` is missing: it uses the pictures already in `src/img/`.

`dist/artifact*.html` and `dist/prime-solutions-demo.html` are single-file copies with the fonts and pictures embedded, for quick previews. They are not needed for hosting. To link the three previews together, put their addresses in a `preview_links.json` (keys `premium`, `standard`, `pro`) before building.

## Changing things

- **Any wording, price or the contact email:** `site.json` (`copy` for the words, `prices`, `email`). Do not type wording into the templates or `demos.py`; the build reads it from `site.json`.
- **Estimates only:** prices are shown as estimates ("estimated", "from"), never fixed or final. There is no VAT because Prime Solutions is not VAT registered. The one fee excludes extras; hosting and the domain are the client's own cost; there is no monthly fee. Buying is by email only ("Email first, we talk, then we build"). The turnaround is agreed in the quote.
- **The address of the live site:** the `domain` field in `site.json` (for example `https://example.com`, no slash at the end). Until it is filled in, the canonical link is left out and the share picture (`og:image`) uses a relative address. Once it is set, every page gets an absolute `og:image` and a canonical link.
- **Colours:** the Forest theme (forest green `#0B5D3B`, white, mint `#D6F1E2`, emerald `#1FAE6C`) is the `theme` block in `site.json` and the variables at the top of `src/css/styles.css`.
- **Pictures:** put new originals in `assets_in/`, run `python3 build.py`, and update `CREDITS.md`.
- **After any change,** run `python3 build.py` again and upload `dist/`.

## The legal pages

Each page has its own source file in `legal/`: `privacy.md`, `terms.md`, `refunds.md`. A file starts with a few lines between two `---` lines (`title`, `version`, `last_updated`, `status`, `banner`) and then the text. The page shows its version and "last updated" line from those, so a change is a one-file edit.

- **To publish a different version of a page,** replace the text below the `---` lines with the new text, update `version` and `last_updated`, and run `python3 build.py`. Do not edit anything in `dist/`.
- **The words common to all three pages** (the name, the email, where the site is hosted) are one block in `site.json` (`legal`). A source file can use them as `{{legal.email}}`, `{{legal.name}}` and `{{legal.host}}`. No legal wording is written into the templates or the scripts.
- **The Draft notice.** Until a page is final it carries a "Draft. This page is not final." notice. `banner: site` shows the site's notice; `banner: own` is for a file that already has its own Draft banner. The site never says a page is final or legally approved.
- **Text kept internal.** If a source file has an internal "do not publish" box, fence it with `<!-- INTERNAL-START -->` and `<!-- INTERNAL-END -->` (or leave it as a heading or quote that says "do not publish" or "internal") and the build leaves it out of the published page. The build refuses to finish if "do not publish" text is still in a published page.
- **Right now** each file holds one marked placeholder naming the file it is waiting for. The real wording has not been supplied, and nothing here has been written in its place.
- `archive/legal/` holds older policy drafts that do not fit Advertise Only. They are not used and must not be published.

## Markers: what is still to be supplied

A marker is any text in square brackets that starts with `[TO BE SUPPLIED`, `[JASON TO SUPPLY`, `[ATTORNEY` or `[VERIFY` (the list is `legal.markers` in `site.json`). It is shown on the page, highlighted, until it is replaced.

- Every run of `python3 build.py` writes **`OPEN-MARKERS.md`**: the one list of every open marker, with the file and field it is in.
- Set `"status": "live"` in `site.json` only when the list is empty. A site marked `live` will not build while any marker is open in `site.json`, `CREDITS.md` or a legal page. A legal page can also be marked `status: live` by itself, and will not build with a marker in it. Draft pages and the draft site only warn.

## The Standard look

- Colours and softness are in `site.json` under `standard_theme` (`paper`, `card`, `sage`, `forest`, `ink` and the rest). `demos.py` (`std_vars`) turns them into the page's variables, so the Standard page has its own palette without touching Pro or Premium.
- The three background pictures (`src/img/ps-castle.webp`, `ps-gateway.webp`, `ps-path.webp`) are the originals in `assets_in/bg-*.webp` mixed into the off-white. `standard_theme.veil` (0 to 1) says how much off-white goes over the two band pictures, and `veil_hero` how much goes over the castle picture in the opening (kept low, so it stays strong): higher is lighter. To change either, edit it and run `python3 prep_images.py`, then `python3 build.py`. The fade of the castle picture into "The three levels" is in `src/css/tiers.css` (`.ps-top`, `--ps-run`).
- The typeface is `src/fonts/prime-serif.woff` (Lora cut down and renamed, see `CREDITS.md`). Only that one font file loads on the Standard page.
- The three background pictures are AI-made, which the build rules for this project do not allow. They are marked in `CREDITS.md` for the owner to decide.

## The Pro look

- The swirl in the portal's doorway turns clockwise around the white light: the whole doorway slowly, its middle faster, so it reads as a vortex. It is the doorway's own picture that turns (`pro-hero.webp`), not something added on top: the swirl is squashed to a circle, turned, and stretched back, so the stones stay still (`DOOR` in `build.py`, `@keyframes pp-turn` in `src/css/tiers.css`). It holds still with reduced motion.
- Pro uses the Standard colours from `site.json` (`standard_theme`), and its own two typefaces. The castle, gateway and path pictures sit behind its bands under a veil written in `tiers.css` (`--pp-veil-*`).
- The header's clear and veil states are switched by a few lines in `src/js/tier.js` (and `main.js`, for the Pro demo inside Premium). Without the script it stays the soft veil.
- Phones get smaller copies of the big pictures (`*-sm.webp`, made by `prep_images.py`), so Pro loads under 450 KB on a phone and about 600 KB on a desktop.
- Harvey's brief said the Pro header must stay as it was. Hamza asked for it to be invisible with the links in the middle (as on Standard), so it was changed on his instruction.

## The entrance and the look of Premium

- **One swipe in.** The page opens locked on the entrance. One scroll down, one swipe up, one tap on the doorway or one press of the arrow, space or page-down key starts a timed walk through the portal (about 3 seconds, a little less on phones). It runs by itself, so there is no half-way stop, and once you are through the page never closes the door again (scrolling back up stays in the valley). Links to a part of the page, and the "skip" link, take you straight in. A visitor who arrives part-way down (a link with `#levels`, or a reload) is let in at once. With reduced motion the finished valley is shown straight away.
- **No day-to-night.** The sky cycle is gone, so the plans are about one screen of scrolling below the headline. The stones still float.
- The seven stones are cut-outs (`src/img/rock-1..7.webp`), placed by the percentages in `src/rocks.json` and drifted slowly up and down with CSS transforms, each with its own random delay and speed; their glow breathes. They stop for `prefers-reduced-motion`.
- The valley picture without the stones is `src/img/beyond-1680.webp`. If the original valley picture changes, run `python3 tools/cut_rocks.py` and then `python3 prep_images.py`. Pro and Standard use the valley picture as it is, without the floating stones.
- **Pictures.** The samples part sits on the stone gateway, "How it works" on the castle valley (mixed into white) and contact on the mossy path. They are made by `premium()` in `prep_images.py` (small copies for phones), load only when their part is close to the screen, and drift a little as you scroll. They are the AI-made Canva backgrounds, so the same owner decision as in `CREDITS.md` applies.
- **Fonts.** Poppins (headings) and Inter (text), cut down and renamed "Prime Display" and "Prime Text" by `prep_fonts.py`. Pro and Standard keep their own typefaces (the Pro sample inside Premium shows Pro's).
- **Interaction.** The doorway glows as the pointer comes near it; the valley leans slightly with the pointer; the samples part and contact have a soft light that follows the pointer (mouse only, off on touch); the "What you get" cards light up under the pointer; the questions open smoothly. All of it is light, stops for reduced motion and stores nothing.
- **On phones** (under 700 px for the valley, under 900 px for the plans): after the portal the valley stays still while you scroll (no zoom, no sliding) and only drifts slowly from side to side by itself, so scrolling goes straight on to the plans. In "Three levels" the pinned sample box is gone: each level carries its own sample page (`step_box()` in `build.py`) right above its writing, and the two scroll down together. Laptops and PCs keep the pinned box and the level buttons.
- **The demo buttons** ("See the Standard demo", "See the Pro demo", and the open-demo button beside the sample page) open the Standard or Pro version full screen over the page. The page follows these links itself and only keeps the address (`#demo-standard`, `#demo-pro`) in step, so they still work in a viewer that holds links or the address still (a link-swallowing viewer was the cause of "nothing happens"). Back, Escape, the Close button and a shared `#demo-pro` link all still work, and the nav links work in such a viewer too.
- **Switching levels:** the Standard / Pro / Premium buttons beside the sample page pin the level they were pressed for while the page scrolls to it (before, the page flipped back through the levels it passed on the way, so the sample page flickered); any scroll, touch or key by the visitor lets go of the pin. Inside the full-screen demo, switching between Standard and Pro ignores an older address that comes back a moment late, a close that is still waiting cannot shut the page opened after it, and only the open demo is ever shown (a stale `#demo-…` address cannot show a second one). The Standard demo's phone menu is shut again when you come back to it.
- The rest of the plans and demo part ("Three levels", the demo viewer) is as before. The "Back to the entrance" button only scrolls up to the top of the valley.

## Notes

- Motion follows `prefers-reduced-motion`: the entrance is shown open, the stones and swirl hold still, the pointer effects are off, the fade-ins are off. The pages store and send no data.
- The Email us buttons are plain `mailto:` links, and the address is also shown as text with a Copy button, so the contact still works where a mail link does nothing.
- Pictures and fonts: see `CREDITS.md`. Its sources are not all filled in yet.
