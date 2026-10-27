#!/usr/bin/env python3
"""Build the Prime Solutions site.

Reads site.json and src/, writes:
  dist/            the deployable site (index.html, css/, js/, fonts/)
  dist/artifact.html   one self-contained file for previewing (fonts inlined)
"""
import base64, json, math, re, shutil, sys
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import demos, prep_images
SRC, DIST = ROOT / "src", ROOT / "dist"
site = json.loads((ROOT / "site.json").read_text(encoding="utf-8"))
prep_images.main()          # pictures in assets_in/ become the small web images in src/img/


# ---------- helpers ----------
def lum(hex_):
    h = hex_.lstrip("#")
    r, g, b = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def contrast(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def on(bg, a, b):
    """pick whichever of a, b reads better on bg"""
    return a if contrast(bg, a) >= contrast(bg, b) else b


# ---------- sample page mock-ups (levels section) ----------
MOCKS = """\
              <div class="mock mock--standard"><div class="m">
                <div class="m-nav"><b>Your Business</b><span>About</span><span>Services</span><span>Contact</span></div>
                <div class="m-hero"><h4>Your business name</h4><p>A short line about what you do and where you do it.</p><span class="m-btn">Email us</span></div>
                <div class="m-cols"><div><b>Service one</b><i></i><i></i></div><div><b>Service two</b><i></i><i></i></div><div><b>Service three</b><i></i><i></i></div></div>
              </div></div>
              <div class="mock mock--pro"><div class="m">
                <div class="m-top">
                  <div class="m-nav"><b>Your Business</b><span class="on">Home</span><span>Services</span><span>Contact</span></div>
                  <div class="m-copy"><h4>Your business name</h4><p>A short line about what you do and where you do it.</p><span class="m-btn">Email us</span></div>
                  <div class="m-art"><div class="m-blk b1"></div><div class="m-blk b2"></div><div class="m-blk b3"></div></div>
                </div>
                <div class="m-cards"><div><b>Service one</b><i></i><i></i></div><div><b>Service two</b><i></i><i></i></div><div><b>Service three</b><i></i><i></i></div></div>
              </div></div>
              <div class="mock mock--premium"><div class="m">
                <div class="m-glow"></div>
                <div class="m-nav"><b>Your Business</b><span class="on">Home</span><span>Services</span><span>Contact</span></div>
                <h4><span>Your</span><span class="o">business.</span></h4>
                <p>A short line about what you do and where you do it.</p>
                <span class="m-btn">Email us</span>
                <svg class="m-seal" viewBox="0 0 100 100" aria-hidden="true"><defs><path id="seal-path" d="M50,50 m-36,0 a36,36 0 1,1 72,0 a36,36 0 1,1 -72,0"/></defs><g class="m-seal__ring"><text><textPath href="#seal-path" textLength="222" lengthAdjust="spacing">Made for your trade • Made for your trade •</textPath></text></g><circle cx="50" cy="50" r="6"/></svg>
                <div class="m-stack"><div class="c1"><b>Service 1</b><i></i></div><div class="c2"><b>Service 2</b><i></i></div><div class="c3"><b>Service 3</b><i></i></div></div>
              </div></div>"""


# ---------- sample layouts (samples section) ----------
def has_img(name):
    return (SRC / "img" / name).exists()


def sample(s):
    bg, ink, brand, acc = site["themes"][s["theme"]]
    btn_ink = on(brand, bg, ink)
    style = f"--s-bg:{bg};--s-ink:{ink};--s-brand:{brand};--s-acc:{acc};--s-on:{btn_ink}"
    nav = f'<div class="s-nav"><b>{s["brand"]}</b><i></i><i></i><i></i></div>'
    btn = '<span class="s-btn">Email us</span>'
    key = s.get("photo")
    ph = bool(key) and has_img(f"trade-{key}.webp")      # without the picture the painted version is used
    body = f'<div class="s-body"><h4>{s["headline"]}</h4><p>{s["sub"]}</p>{btn}</div>'
    if s["layout"] == "a":
        art = f'<div class="s-art ph ph-{key}"></div>' if ph else '<div class="s-art"><i></i><i></i></div>'
        inner = nav + body + art
    elif s["layout"] == "b":
        tiles = (f'<div class="s-tiles s-tiles--ph"><i class="ph ph-{key}"></i><i></i></div>' if ph
                 else '<div class="s-tiles"><i></i><i></i><i></i></div>')
        inner = nav + body + tiles
    else:
        head = f'<div class="s-photo{f" ph ph-{key}" if ph else ""}">{nav}<div class="s-shape"></div></div>'
        inner = head + body
    return (f'        <figure class="sample" tabindex="0">\n'
            f'          <div class="sample__view" aria-hidden="true"><div class="s s--{s["layout"]}{" s--ph" if ph else ""}" style="{style}">{inner}</div></div>\n'
            f'          <figcaption><strong>{s["trade"]}</strong><span>{s["theme"]} theme</span></figcaption>\n'
            f'        </figure>')


# the swirl in the doorway of pro-hero.webp, as fractions of the picture: d = width of the turning circle, cx / cy = its centre
DOOR = {"d": 0.115, "cx": 0.5000, "cy": 0.5244}


# pictures are background images set by class, so each one is stored once however often it is used
def photo_css():
    out = ["\n/* ---------- pictures (written by build.py from whatever is in src/img) ---------- */"]
    for key in ("plumbing", "salon", "cafe", "garage", "cleaning", "firm"):
        if has_img(f"trade-{key}.webp"):
            out.append(f"html .ph.ph-{key} {{ background-image: url(../img/trade-{key}.webp); background-size: cover; background-position: center; }}")
    if has_img("levels-bg.webp"):
        out.append("html .levels__bg, html .ps-photo.ph-hills { background-image: url(../img/levels-bg.webp); background-size: cover; background-position: center bottom; }")
        out.append("html .ps-photo.ph-hills { background-position: 66% 64%; }")
    if has_img("pro-hero.webp"):
        # the Pro opening: the portal picture, and a small round copy of the swirl in its doorway that turns
        d, cx, cy, ar = DOOR["d"], DOOR["cx"], DOOR["cy"], 944 / 1680
        px = (0.5 - cx / d) / (1 - 1 / d) * 100
        py = (0.5 - (ar / d) * cy) / (1 - ar / d) * 100
        out.append("html .pp-scene, html .pp-door { background-image: url(../img/pro-hero.webp); }")
        out.append(f"html .pp-door {{ left: {cx * 100:.2f}%; top: {cy * 100:.2f}%; width: {d * 100:.2f}%; aspect-ratio: 1; "
                   f"background-size: {100 / d:.2f}% auto; background-position: {px:.2f}% {py:.2f}%; }}")
    if has_img("pro-valley.webp"):
        out.append("html .pp-contact__bg { background-image: url(../img/pro-valley.webp); background-size: cover; background-position: center; }")
    return "\n".join(out) + "\n"


# ---------- privacy policy: legal/privacy-policy.md -> html ----------
def _ph(text):
    """wrap [placeholders] (nested ones included) in <mark>"""
    out, depth, start = [], 0, 0
    for i, ch in enumerate(text):
        if ch == "[":
            if depth == 0:
                out.append(text[start:i]); start = i
            depth += 1
        elif ch == "]" and depth:
            depth -= 1
            if depth == 0:
                out.append('<mark class="ph">' + text[start:i + 1] + "</mark>"); start = i + 1
    out.append(text[start:])
    return "".join(out)


def _inline(t):
    t = t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    t = _ph(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", t)
    t = re.sub(r"(https?://[^\s<)]+)", r'<a href="\1">\1</a>', t)
    t = re.sub(r"(?<![\w/>\"=:.-])([\w.+-]+@[\w-]+(?:\.[\w-]+)+)", r'<a href="mailto:\1">\1</a>', t)
    return t


def policy_html(md):
    lines, out, para, items, rows = md.splitlines(), [], [], [], []

    def flush():
        nonlocal para, items, rows
        if para:
            out.append("<p>" + "<br>".join(_inline(x) for x in para) + "</p>")
        if items:
            out.append("<ul>" + "".join(f"<li>{_inline(x)}</li>" for x in items) + "</ul>")
        if rows:
            cells = lambda r: [c.strip() for c in r.strip().strip("|").split("|")]
            head, body = cells(rows[0]), [cells(r) for r in rows[2:]]
            out.append('<div class="table-wrap"><table' + (' class="wide"' if len(head) > 2 else '') + '><thead><tr>' + "".join(f"<th>{_inline(c)}</th>" for c in head) +
                       "</tr></thead><tbody>" + "".join("<tr>" + "".join(f"<td>{_inline(c)}</td>" for c in r) + "</tr>" for r in body) +
                       "</tbody></table></div>")
        para, items, rows = [], [], []

    for ln in lines:
        s = ln.rstrip()
        if not s.strip():
            flush(); continue
        if s.startswith("# ") or s.startswith("## ") or s.strip() == "---" or s.startswith("Draft for review only"):
            flush(); continue
        if s.startswith("### "):
            flush()
            title = s[4:].strip()
            num = re.match(r"(\d+)\.", title)
            out.append(f'<h2 id="privacy-{num.group(1) if num else len(out)}">{_inline(title)}</h2>'); continue
        if s.startswith("|"):
            if para or items: flush()
            rows.append(s); continue
        if s.startswith("- "):
            if para or rows: flush()
            items.append(s[2:]); continue
        if items or rows: flush()
        para.append(s)
    flush()
    return "\n".join(out)


def legal_block(level):
    body = policy_html((ROOT / "legal" / "privacy-policy.md").read_text(encoding="utf-8"))
    title = f'<h{level} class="legal__title" id="privacy-title">Privacy policy</h{level}>'
    return (f'<div class="wrap legal__wrap">\n<p class="eyebrow">Privacy</p>\n{title}\n'
            '<p class="notice"><strong>Draft.</strong> The highlighted [brackets] still need filling in, and a South African attorney should review this before launch.</p>\n'
            '<p class="notice notice--plain">This website has no forms, no cookies and no analytics.</p>\n'
            f'<div class="legal__body">\n{body}\n</div>\n</div>')


# ---------- tokens ----------
t = site["theme"]
fav_svg = (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='8' fill='{t['brand']}'/>"
           f"<path d='M10 24V8h7.2a5 5 0 0 1 0 10H14' fill='none' stroke='{t['bg']}' stroke-width='3.2' stroke-linecap='round' stroke-linejoin='round'/></svg>")
favicon = "data:image/svg+xml," + quote(fav_svg, safe="/:=' ")
jsonld = json.dumps({
    "@context": "https://schema.org", "@type": "ProfessionalService",
    "name": site["name"], "description": site["description"], "email": site["email"],
    "areaServed": {"@type": "Country", "name": "South Africa"},
    "serviceType": "One-page website design and build", "knowsLanguage": "en",
}, ensure_ascii=False)

tokens = {
    "name": site["name"], "email": site["email"], "seo_title": site["seo_title"],
    "description": site["description"], "year": site["year"], "bg": t["bg"],
    "favicon": favicon, "jsonld": jsonld, "mocks": MOCKS,
    "samples": "\n".join(sample(s) for s in site["samples"]),
    "demos": demos.build(site, on),
    "price_standard": site["prices"]["standard"], "price_pro": site["prices"]["pro"],
    "price_premium": site["prices"]["premium"],
    "privacy_href": "privacy.html", "legal": legal_block(1),
    "tier_body": "", "tier_vars": "", "tier_title": "", "tier_class": "",
}


def render(page_kb, template="index.html"):
    html = (SRC / template).read_text(encoding="utf-8")
    all_tokens = dict(tokens, page_kb=str(page_kb))
    for k, v in all_tokens.items():
        html = html.replace("{{" + k + "}}", v)
    left = re.findall(r"\{\{\w+\}\}", html)
    if left:
        sys.exit(f"unfilled tokens: {left}")
    return html


# ---------- dist ----------
if DIST.exists():
    shutil.rmtree(DIST)
for sub in ("css", "js", "fonts", "img"):
    shutil.copytree(SRC / sub, DIST / sub)
CSS_ALL = (SRC / "css" / "styles.css").read_text(encoding="utf-8") + "\n" + (SRC / "css" / "tiers.css").read_text(encoding="utf-8") + photo_css()
(DIST / "css" / "styles.css").write_text(CSS_ALL, encoding="utf-8")
(DIST / "css" / "tiers.css").unlink()   # one stylesheet is shipped
if (SRC / "og.png").exists():
    shutil.copy(SRC / "og.png", DIST / "og.png")

page_kb = 0
for _ in range(2):  # the number sits inside the page, so settle it in two passes
    (DIST / "index.html").write_text(render(page_kb), encoding="utf-8")
    (DIST / "privacy.html").write_text(render(page_kb, "privacy.html"), encoding="utf-8")
    for key, name in (("standard", "Standard"), ("pro", "Pro")):
        body, vars_ = demos.page(site, on, key)
        tokens_tier = dict(tier_body=body, tier_vars=vars_, tier_title=f"{site['name']} | {name} level", tier_class=f"tier--{key}")
        tokens.update(tokens_tier)
        (DIST / f"{key}.html").write_text(render(page_kb, "tier.html"), encoding="utf-8")
    total = sum(p.stat().st_size for p in DIST.rglob("*") if p.is_file() and p.suffix in (".html", ".css", ".js", ".woff", ".webp") and p.name != "artifact.html")
    page_kb = int(math.ceil(total / 1024 / 10.0) * 10)

# ---------- artifact (single file) ----------
css = CSS_ALL
def font_uri(m):
    data = (SRC / "css" / m.group(1)).resolve().read_bytes()
    return "url(data:font/woff;base64," + base64.b64encode(data).decode() + ") format(\"woff\")"
css = re.sub(r'url\(([^)]*?\.woff)\) format\("woff"\)', font_uri, css)
css = re.sub(r'url\(\.\./img/([^)]*?\.webp)\)', lambda m: "url(data:image/webp;base64," + base64.b64encode((SRC / "img" / m.group(1)).read_bytes()).decode() + ")", css)
js = (SRC / "js" / "intro.js").read_text(encoding="utf-8") + "\n" + (SRC / "js" / "main.js").read_text(encoding="utf-8")

full = (DIST / "index.html").read_text(encoding="utf-8")
head = re.search(r"<head>(.*?)</head>", full, re.S).group(1)
body = re.search(r"<body>(.*)</body>", full, re.S).group(1)
body = re.sub(r'<script src="js/(?:intro|main).js" defer></script>\s*', "", body)
body = re.sub(r'src="img/([^"]+\.webp)"', lambda m: 'src="data:image/webp;base64,' + base64.b64encode((SRC / "img" / m.group(1)).read_bytes()).decode() + '"', body)
# the preview is one file, so the policy opens as a section of the page instead of privacy.html
body = body.replace('href="privacy.html"', 'href="#privacy"')
inline = ('<section class="legal legal--inline" id="privacy" data-tone="light" aria-labelledby="privacy-title">\n' + legal_block(2) +
          '\n<div class="wrap legal__wrap"><a class="link" href="#top">Back to the site</a></div>\n</section>\n')
assert '<footer class="site-footer"' in body
body = body.replace('<footer class="site-footer"', inline + '<footer class="site-footer"', 1)
keep_meta = "\n".join(re.findall(r'<meta (?:name="description"|property="og:[^"]+"|name="twitter:card")[^>]*>', head))
ld = re.search(r'<script type="application/ld\+json">.*?</script>', head, re.S).group(0)
art = (f'<title>{site["artifact_title"]}</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n{keep_meta}\n'
       f'<script>document.documentElement.classList.add("js")</script>\n<style>\n{css}\n</style>\n{ld}\n{body}\n<script>\n{js}\n</script>\n')
(DIST / "artifact.html").write_text(art, encoding="utf-8")

# the same page as one complete file (with a doctype) that opens by double-click, offline
demo = ('<!doctype html>\n<html lang="en-ZA">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        f'<title>{site["seo_title"]}</title>\n{keep_meta}\n<meta name="theme-color" content="{t["bg"]}">\n<link rel="icon" href="{favicon}">\n'
        f'<script>document.documentElement.classList.add("js")</script>\n<style>\n{css}\n</style>\n{ld}\n</head>\n<body>\n{body}\n<script>\n{js}\n</script>\n</body>\n</html>\n')
(DIST / "prime-solutions-demo.html").write_text(demo, encoding="utf-8")

print(f"dist total ~{page_kb} KB | artifact {len(art.encode())/1024:.0f} KB")
