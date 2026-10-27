# Open markers

Written by `build.py` every time it runs. Do not edit by hand. Each line is something that has not been supplied yet.
Fill it in where it says (a legal page, or a field in `site.json`), run `python3 build.py`, and it drops off this list.

Site status: **draft** · Mode: **advertise-only** · Markers open: **11**

| Where | Marker |
|---|---|
| `site.json  domain` | [TO BE SUPPLIED: the live web address, for example https://example.com, no slash at the end] |
| `site.json  legal.host` | [TO BE SUPPLIED: where the website is hosted] |
| `CREDITS.md` | [TO BE SUPPLIED: where the six trade pictures came from (author or website, and the link)] |
| `CREDITS.md` | [TO BE SUPPLIED: the licence they are used under] |
| `CREDITS.md` | [TO BE SUPPLIED: where the misty-hills picture came from (author or website, and the link)] |
| `CREDITS.md` | [TO BE SUPPLIED: the licence it is used under] |
| `CREDITS.md` | [TO BE SUPPLIED: where the stone arch and valley pictures came from (author or website, and the link)] |
| `CREDITS.md` | [TO BE SUPPLIED: the licence they are used under] |
| `legal/privacy.md` | [TO BE SUPPLIED: Cherry's Advertise Only privacy policy (06-privacy-policy-ADVERTISE-ONLY-DRAFT.md). Paste it below the front matter (the lines between the two --- lines at the top), replacing this text. Keep every marker in it exactly as written. If her file has its own Draft banner, change "banner: site" above to "banner: own".] |
| `legal/terms.md` | [TO BE SUPPLIED: Cherry's terms of use / client terms (02-compliance-aligned-website-terms.md). Paste the terms part below the front matter, replacing this text. Keep every marker in it exactly as written.] |
| `legal/refunds.md` | [TO BE SUPPLIED: Cherry's refund, cancellation and cooling-off wording (from 02-compliance-aligned-website-terms.md). Paste it below the front matter, replacing this text. Keep every marker in it exactly as written.] |

A marker is any text in square brackets that starts with one of: `[TO BE SUPPLIED`, `[JASON TO SUPPLY`, `[ATTORNEY`, `[VERIFY`.
A page, or the site, marked `live` cannot be built while a marker is open in it.
