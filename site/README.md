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

Premium shows Standard and Pro in its "Three levels" section, and every level links to the others. Same sections, same words at every level. The site shows no prices. Only the treatment changes (Premium is richer than Pro, and Pro is richer than Standard).

The legal pages are at `/privacy-policy/`, `/terms-of-use/` and `/how-it-works/` (Cherry's file names), and every page links to all three from its footer. `/credits/` is the credits page, built from `CREDITS.md` and linked from the terms.

## Where things live

```
site.json            ALL the wording (copy), contact email, mode, status, the legal block (name, owner, location, the WhatsApp number, footer and enquiry texts, domain, date, version), the Forest theme, the six sample layouts
legal/privacy-policy.md   the privacy policy      one source file per legal page, each with its own last-updated line
legal/terms-of-use.md     the website terms of use (version 1.0)
legal/how-it-works.md     how it works, refunds and cancellation (version 1.0)
CREDITS.md           the source and licence of every picture and font; also published as /credits/
OPEN-MARKERS.md      the one list of everything still to be supplied (written by the build; do not edit)
build.py             fills the templates from site.json and legal/, writes dist/, runs the checks below
texts.py             draws the footer, contact block and enquiry notice from site.json (the words are never changed there)
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

- **Any wording or the contact email:** `site.json` (`copy` for the words, `email`). Do not type wording into the templates or `demos.py`; the build reads it from `site.json`. The contact email has one source, `email`: the legal pages take it from there with `{{legal.email}}`, and the build fails if any page shows a different address.
- **No prices.** The site shows no price of any kind: no rand figure, range, "from" price or price anchor, on any page, plan card, meta tag, structured-data block or alt text, and no "one-off fee, no monthly charges" wording. The plans show their names and what each includes, under the label "Plans and what they include." (`copy.pricing.label`). The only price wording is one note (`copy.pricing.note`): "Your price is set out in a written quote before any work starts, based on what you need. Extra features are quoted before we start. Prime Solutions EL is not VAT registered, so no VAT is added. Hosting and your domain name are your own cost unless your quote says otherwise." The terms and the how-it-works page take that note from `site.json` with `{{copy.pricing.note}}`. Nothing is sold on the site: the first step is an email or a WhatsApp message, then a written quote and agreement. The turnaround is agreed in the quote. The four steps are `copy.process.steps`; `copy.process.one_line` is the one-line version of them, kept for use as a summary (it is not shown today). If prices are ever to be shown again, that is a decision for the owner, and the build checks, the terms, the how-it-works page, the quotes and the privacy page change with it.
- **Who we are, where, and how to get in touch.** The owner line (HAMZA KHAN, a sole proprietor), the location ("East London, South Africa" and nothing more specific: no street, suburb, postal code or map) and the one WhatsApp number are in the `legal` block of `site.json` (`owner`, `location`, `whatsapp`). The email is the top-level `email`. The WhatsApp number is the only phone-type contact: a plain link to `https://wa.me/27718634356` (new tab, `rel="noopener"`, no script, no widget, no prefilled text), shown only in the contact block, the footer and the privacy page. There is no `tel:` link and no other number. The three texts that carry these are `legal.footerNotice` (every page's footer), `copy.contact.block` (the contact part of every level) and `legal.enquiryNotice` (next to every email prompt); all three are shown word for word, and the build checks that.
- **The address of the live site:** `legal.domain` in `site.json` (primesolutionsgroup.co.za, as Cherry spelled it). The build makes the `https://` address from it, and every page gets an absolute `og:image` and a canonical link (these are not requests the page makes).
- **The enquiry notice** ("When you email us or message us on WhatsApp, we use your details only to reply, quote and, if you go ahead, build your site...", `legal.enquiryNotice`) sits next to the email calls to action: the opening, the plans, the extras, the contact part, the footer of every page and the end of each full-screen demo. The sticky header button has no room for it and opens the same email as the opening button.
- **Colours:** the Forest theme (forest green `#0B5D3B`, white, mint `#D6F1E2`, emerald `#1FAE6C`) is the `theme` block in `site.json` and the variables at the top of `src/css/styles.css`.
- **Pictures:** put new originals in `assets_in/`, run `python3 build.py`, and update `CREDITS.md`.
- **After any change,** run `python3 build.py` again and upload `dist/`.

## The legal pages

Each page has its own source file in `legal/` (`privacy-policy.md`, `terms-of-use.md`, `how-it-works.md`), and `/credits/` is built from `CREDITS.md`. A file starts with a few lines between two `---` lines (`title`, `slug`, `status`, `banner`, and `last_updated` or `version` only if a page needs its own) and then the text. Every page shows "Last updated: <date> · Version 1.0". Both default to `legal.last_updated` and `legal.version` in `site.json`, so the go-live date is one edit there (set it to the day the site really goes live).

- **Where the text came from.** The privacy page is the full text in Cherry's file of 29 October 2026 ("address and disclosures", section 4A), word for word, with the Information Regulator's details as on the Regulator's own contact page. The terms and how-it-works pages are her package text (files 02 and 03) with that file's changes: no prices, the price note above, a Complaints section in the terms and a new "Questions or complaints" section in how-it-works. Her STATUS lines and instructions to Claude are not published. The email address, the owner, the location and the WhatsApp number inside them are `{{legal.email}}`, `{{legal.owner}}`, `{{legal.location}}` and `{{legal.whatsapp.number}}`, so each has one source in `site.json`. The WhatsApp number is a link on the privacy page and plain text on the terms and how-it-works pages. A link such as `[credits](credits)` or `[Privacy Policy](privacy-policy)` goes to that page wherever the page is shown.
- **To publish a different version of a page,** replace the text below the `---` lines with the new text, update `legal.last_updated` and `legal.version` in `site.json`, and run `python3 build.py`. Do not edit anything in `dist/`.
- **The words common to all pages** (the trading name, the owner, the location, the WhatsApp number, the domain, the date and version) are one block in `site.json` (`legal`). A source file can use them as `{{legal.email}}`, `{{legal.name}}` (Prime Solutions EL), `{{legal.owner}}`, `{{legal.location}}`, `{{legal.whatsapp.number}}` and `{{legal.whatsapp.url}}`. No legal wording is written into the templates or the scripts. The owner's name appears only as the owner line and as the responsible party in the privacy policy. No street address, postal address or other phone number is shown anywhere (the owner's decision); the one street line on the site is the Information Regulator's own address in the privacy policy.
- **The Draft notice.** Until a page is final it carries a "Draft. This page is not final." notice. `banner: site` shows the site's notice; `banner: own` is for a file that already has its own Draft banner. The site never says a page is final or legally approved. Cherry's package is draft, not legal advice, and it says to re-paper everything with a lawyer when a company is registered or before the first paying client.
- **Text kept internal.** If a source file has an internal "do not publish" box, fence it with `<!-- INTERNAL-START -->` and `<!-- INTERNAL-END -->` (or leave it as a heading or quote that says "do not publish" or "internal") and the build leaves it out of the published page. The build refuses to finish if "do not publish" text is still in a published page. `CREDITS.md` keeps its open items this way.
- **The privacy page and the site must stay in step.** The policy says the site has no forms, cookies, local storage, analytics, payments or outside requests, and that the copy buttons only copy to the clipboard. The build checks this on every build (see "What the build checks"); if any of it must change, change the policy first. The policy says only "our web host" and never names a company. HostAfrica is the domain registrar only and is not named. If the site is deployed to a named host and the owner wants it named, that is a change to the policy first.
- **The entrance plays once per visit** and is remembered only in a variable inside the open page (`entered` in `src/js/intro.js`), so it starts again when the visitor leaves and comes back. It is never kept in a cookie, browser storage or the address.

## What the build checks

`python3 build.py` stops (exit 1) when a finished page:

- contains a placeholder marker (`[TO BE SUPPLIED ...]` and the like);
- uses a banned word from Cherry's list (buy, order, pay, payment, book now, subscribe, sign up, guaranteed, fixed price, "trusted by", "#1", "best in South Africa", Pty Ltd, ...) outside a sentence that says nothing can be ordered or paid for;
- shows an email address other than the one in `site.json` (the Information Regulator's address, in the privacy text, is the one listed exception: `legal.other_emails`);
- has a form field, an embed (iframe, video, audio), or a `tel:`, `sms:` or `whatsapp:` link;
- has a WhatsApp link other than exactly `https://wa.me/27718634356` (new tab, `rel="noopener"`, the number as its text), or has it anywhere except the contact block, the footer and the privacy page;
- shows a price or fee wording (a rand or dollar figure, "from R...", "once-off", "per month" and the like), a street or postal address (the Information Regulator's own street line on the privacy page is the one exception), or any phone-looking number other than the WhatsApp number (and the Regulator's, on the privacy page);
- has a price, offer, phone number or address in its structured data;
- does not show the footer, the enquiry notice (every page) and the contact block (the three level pages) word for word as written in `site.json`;
- has an internal link that goes nowhere;
- uses `localStorage`, `sessionStorage`, IndexedDB, cookies, `fetch`, XMLHttpRequest, WebSocket, a beacon or a service worker in its scripts;
- loads anything from another website (a script, picture, font, stylesheet or frame).

It also refuses a site or page marked `live` while any marker is open anywhere, including the internal notes in `CREDITS.md`.

## Markers: what is still to be supplied

A marker is any text in square brackets that starts with `[TO BE SUPPLIED`, `[JASON TO SUPPLY`, `[ATTORNEY`, `[VERIFY`, `[CLAUDE INSTRUCTION` or `[TO DECIDE` (the list is `legal.markers` in `site.json`). The words CLAUDE INSTRUCTION, TO DECIDE, PENDING and TBC may not appear in a finished page at all, bracketed or not. It is shown on the page, highlighted, until it is replaced.

- Every run of `python3 build.py` writes **`OPEN-MARKERS.md`**: the one list of every open marker, with the file and field it is in.
- Set `"status": "live"` in `site.json` only when the list is empty. A site marked `live` will not build while any marker is open in `site.json`, `CREDITS.md` (its internal notes too) or a legal page. A legal page can also be marked `status: live` by itself, and will not build with a marker in it. Draft pages and the draft site only warn. No finished page may contain a marker at all (see "What the build checks"): open items that are not for visitors, such as the picture licences, are kept inside the internal block of `CREDITS.md`.

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
- **Switching levels:** the Standard / Pro / Premium buttons beside the sample page pin the level they were pressed for while the page scrolls to it (before, the page flipped back through the levels it passed on the way, so the sample page flickered); any scroll, touch or key by the visitor lets go of the pin. Inside the full-screen demo, a tab tapped (Standard, Pro, Premium, or the links at the end of the page) is followed by the page itself and does **not** write to the page address at all, because the viewer that hosts the page watches the address and can send an older one back a moment later, which undid the tap. For the same reason an address that asks for a demo in the two seconds after a tap is ignored, a close that is still waiting cannot shut a demo opened after it, and the address is caught up (a `replaceState`) once things are quiet. With the script running, only `is-open` decides which demo shows (`:target` is used only when the script has not run, so without JavaScript the `#demo-…` links still work). The Standard demo's phone menu is shut again when you come back to it.
- The rest of the plans and demo part ("Three levels", the demo viewer) is as before. The "Back to the entrance" button only scrolls up to the top of the valley.

## Notes

- Motion follows `prefers-reduced-motion`: the entrance is shown open, the stones and swirl hold still, the pointer effects are off, the fade-ins are off. The pages store and send no data.
- The Email us buttons are plain `mailto:` links, and the address is also shown as text with a Copy button, so the contact still works where a mail link does nothing.
- Pictures and fonts: see `CREDITS.md`. Its sources are not all filled in yet.
