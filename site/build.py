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
SRC, DIST = ROOT / "src", ROOT / "dist"
site = json.loads((ROOT / "site.json").read_text(encoding="utf-8"))


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


# ---------- hero: the Premium sample page that builds itself ----------
HERO_MOCK = """\
              <div class="mock mock--premium mock--hero"><div class="m">
                <div class="m-glow"></div>
                <div class="m-nav"><b class="sk" style="--sd:.45s">Your Business</b><span class="on sk" style="--sd:.55s">Home</span><span class="sk" style="--sd:.65s">Services</span><span class="sk" style="--sd:.75s">Contact</span></div>
                <h4><span class="sk" style="--sd:.85s">Your</span><span class="o sk" style="--sd:1s">business.</span></h4>
                <p class="sk" style="--sd:1.15s">A short line about what you do and where you do it.</p>
                <span class="m-btn sk" style="--sd:1.3s">Email us</span>
                <svg class="m-seal" viewBox="0 0 100 100" aria-hidden="true"><defs><path id="seal-path-h" d="M50,50 m-36,0 a36,36 0 1,1 72,0 a36,36 0 1,1 -72,0"/></defs><g class="m-seal__ring"><text><textPath href="#seal-path-h" textLength="222" lengthAdjust="spacing">Made for your trade • Made for your trade •</textPath></text></g><circle cx="50" cy="50" r="6"/></svg>
                <div class="m-stack"><div class="c1" style="--sd:1.5s"><b>Service 1</b><i></i></div><div class="c2" style="--sd:1.65s"><b>Service 2</b><i></i></div><div class="c3" style="--sd:1.8s"><b>Service 3</b><i></i></div></div>
              </div></div>"""


# ---------- sample layouts (samples section) ----------
def sample(s):
    bg, ink, brand, acc = site["themes"][s["theme"]]
    btn_ink = on(brand, bg, ink)
    style = f"--s-bg:{bg};--s-ink:{ink};--s-brand:{brand};--s-acc:{acc};--s-on:{btn_ink}"
    nav = f'<div class="s-nav"><b>{s["brand"]}</b><i></i><i></i><i></i></div>'
    btn = '<span class="s-btn">Email us</span>'
    if s["layout"] == "a":
        inner = (f'{nav}<div class="s-body"><h4>{s["headline"]}</h4><p>{s["sub"]}</p>{btn}</div>'
                 '<div class="s-art"><i></i><i></i></div>')
    elif s["layout"] == "b":
        inner = (f'{nav}<div class="s-body"><h4>{s["headline"]}</h4><p>{s["sub"]}</p>{btn}</div>'
                 '<div class="s-tiles"><i></i><i></i><i></i></div>')
    else:
        inner = (f'<div class="s-photo">{nav}<div class="s-shape"></div></div>'
                 f'<div class="s-body"><h4>{s["headline"]}</h4><p>{s["sub"]}</p>{btn}</div>')
    return (f'        <figure class="sample" tabindex="0">\n'
            f'          <div class="sample__view" aria-hidden="true"><div class="s s--{s["layout"]}" style="{style}">{inner}</div></div>\n'
            f'          <figcaption><strong>{s["trade"]}</strong><span>{s["theme"]} theme</span></figcaption>\n'
            f'        </figure>')


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
    "favicon": favicon, "jsonld": jsonld, "mocks": MOCKS, "hero_mock": HERO_MOCK,
    "samples": "\n".join(sample(s) for s in site["samples"]),
    "price_standard": site["prices"]["standard"], "price_pro": site["prices"]["pro"],
    "price_premium": site["prices"]["premium"],
}


def render(page_kb):
    html = (SRC / "index.html").read_text(encoding="utf-8")
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
for sub in ("css", "js", "fonts"):
    shutil.copytree(SRC / sub, DIST / sub)
if (SRC / "og.png").exists():
    shutil.copy(SRC / "og.png", DIST / "og.png")

page_kb = 0
for _ in range(2):  # the number sits inside the page, so settle it in two passes
    (DIST / "index.html").write_text(render(page_kb), encoding="utf-8")
    total = sum(p.stat().st_size for p in DIST.rglob("*") if p.is_file() and p.suffix in (".html", ".css", ".js", ".woff") and p.name != "artifact.html")
    page_kb = int(math.ceil(total / 1024 / 10.0) * 10)

# ---------- artifact (single file) ----------
css = (SRC / "css" / "styles.css").read_text(encoding="utf-8")
def font_uri(m):
    data = (SRC / "css" / m.group(1)).resolve().read_bytes()
    return "url(data:font/woff;base64," + base64.b64encode(data).decode() + ") format(\"woff\")"
css = re.sub(r'url\(([^)]*?\.woff)\) format\("woff"\)', font_uri, css)
js = (SRC / "js" / "main.js").read_text(encoding="utf-8")

full = (DIST / "index.html").read_text(encoding="utf-8")
head = re.search(r"<head>(.*?)</head>", full, re.S).group(1)
body = re.search(r"<body>(.*)</body>", full, re.S).group(1)
body = re.sub(r'<script src="js/main.js" defer></script>', "", body)
keep_meta = "\n".join(re.findall(r'<meta (?:name="description"|property="og:[^"]+"|name="twitter:card")[^>]*>', head))
ld = re.search(r'<script type="application/ld\+json">.*?</script>', head, re.S).group(0)
art = (f'<title>{site["artifact_title"]}</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n{keep_meta}\n'
       f'<style>\n{css}\n</style>\n{ld}\n{body}\n<script>\n{js}\n</script>\n')
(DIST / "artifact.html").write_text(art, encoding="utf-8")

print(f"dist total ~{page_kb} KB | artifact {len(art.encode())/1024:.0f} KB")
