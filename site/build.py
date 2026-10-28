#!/usr/bin/env python3
"""Build the Prime Solutions site. Run:  python3 build.py   (see README.md)

Reads   site.json            all wording, prices, contact details, the legal block and the mode
        src/                 templates, styles, scripts, pictures
        legal/*.md           one source file per legal page (privacy, terms, refunds)
        demos.py             the Standard and Pro markup
Writes  dist/                the finished site, one domain:
            index.html            Premium
            standard/index.html   Standard
            pro/index.html        Pro
            privacy/ terms/ refunds/index.html
            css/ js/ fonts/ img/ og.png
        dist/artifact*.html, dist/prime-solutions-demo.html   single-file previews (not committed)
        OPEN-MARKERS.md      every [TO BE SUPPLIED] style marker that is still open, and where it is

The build stops (exit 1) when a page or the site is marked live and still has an open marker.
"""
import base64, html as _html, json, random, re, shutil, sys
from datetime import date
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import demos, prep_images
SRC, DIST, LEGAL = ROOT / "src", ROOT / "dist", ROOT / "legal"
site = json.loads((ROOT / "site.json").read_text(encoding="utf-8"))
C, L = site["copy"], site["legal"]
prep_images.main()          # pictures in assets_in/ become the small web images in src/img/

errors, warnings = [], []


def fail(msg):
    errors.append(msg)


# ---------- small helpers ----------
def esc(s):
    return _html.escape(str(s), quote=True)


def fmt(text, **kw):
    return text.format(**kw)


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


def get(path):
    """site.json value by dotted path, e.g. copy.hero.lines.0"""
    cur = site
    for part in path.split("."):
        try:
            cur = cur[int(part)] if isinstance(cur, list) else cur[part]
        except (KeyError, IndexError, ValueError):
            raise KeyError(f"site.json has no '{path}'")
    return cur


def has_img(name):
    return (SRC / "img" / name).exists()


# ---------- the mode, the domain ----------
ADVERTISE = site.get("mode") == "advertise-only"
DOMAIN_OPEN = site["domain"].lstrip().startswith("[")


def head_social(path):
    """canonical link and absolute og:image. Until the domain is supplied the image link stays relative and nothing is canonical."""
    up = "../" * path.count("/")
    if DOMAIN_OPEN:
        return (f'<meta property="og:image" content="{up}og.png">\n'
                '<!-- the canonical link and the absolute og:image need the "domain" field in site.json -->')
    dom = site["domain"].rstrip("/")
    url = f"{dom}/{path}"
    return (f'<link rel="canonical" href="{url}">\n<meta property="og:url" content="{url}">\n'
            f'<meta property="og:image" content="{dom}/og.png">')


# ---------- the legal pages: legal/<slug>.md -> html ----------
FRONT = re.compile(r"\A---[ \t]*\n(.*?)\n---[ \t]*\n", re.S)
MARKER_WORDS = tuple(L["markers"])


def find_markers(text):
    """the [TO BE SUPPLIED ...] style markers in a text, with nested brackets"""
    found, i = [], 0
    while i < len(text):
        if text[i] == "[" and text[i + 1:].startswith(MARKER_WORDS):
            depth, j = 0, i
            while j < len(text):
                depth += (text[j] == "[") - (text[j] == "]")
                j += 1
                if depth == 0:
                    break
            found.append((i, j))
            i = j
        else:
            i += 1
    return found


def marker_texts(text):
    return [text[a:b] for a, b in find_markers(text)]


def fill_tokens(text, where):
    def one(m):
        try:
            v = get(m.group(1))
        except KeyError as e:
            fail(f"{where}: {e}")
            return m.group(0)
        return str(v)
    return re.sub(r"\{\{\s*([\w.]+)\s*\}\}", one, text)


def strip_internal(md, where):
    """leave the internal 'do not publish' notes out of the page"""
    md = re.sub(r"<!--\s*INTERNAL-START\s*-->.*?<!--\s*INTERNAL-END\s*-->\n?", "", md, flags=re.S | re.I)
    lines, out, i = md.split("\n"), [], 0
    skip_level = None
    for ln in lines:
        h = re.match(r"(#{1,6})\s+(.*)", ln)
        if skip_level is not None:
            if h and len(h.group(1)) <= skip_level:
                skip_level = None
            else:
                continue
        if h and re.search(r"do not publish|internal note|internal only", h.group(2), re.I):
            skip_level = len(h.group(1))
            continue
        out.append(ln)
    md = "\n".join(out)
    # a quoted box whose first line says do not publish
    md = re.sub(r"(?:^>.*do not publish.*\n(?:>.*\n?)*)", "", md, flags=re.I | re.M)
    if re.search(r"do not publish", md, re.I):
        fail(f"{where}: the words 'do not publish' are still in the page. Put the internal notes between "
             "<!-- INTERNAL-START --> and <!-- INTERNAL-END --> so they stay out of the published page.")
    return md


def read_legal(slug):
    p = LEGAL / f"{slug}.md"
    if not p.exists():
        fail(f"legal/{slug}.md is missing (listed in site.json legal.pages)")
        return None
    raw = p.read_text(encoding="utf-8")
    meta, body = {}, raw
    m = FRONT.match(raw)
    if m:
        for ln in m.group(1).splitlines():
            if ":" in ln:
                k, v = ln.split(":", 1)
                meta[k.strip()] = v.strip()
        body = raw[m.end():]
    for k in ("title", "version", "last_updated", "status"):
        if not meta.get(k):
            fail(f"legal/{slug}.md: the front matter needs a '{k}' line")
    body = strip_internal(fill_tokens(body, f"legal/{slug}.md"), f"legal/{slug}.md")
    try:
        d = date.fromisoformat(meta.get("last_updated", ""))
        meta["date_text"] = f"{d.day} {d.strftime('%B %Y')}"
    except ValueError:
        meta["date_text"] = meta.get("last_updated", "")
    meta["slug"], meta["body"] = slug, body
    return meta


LEGAL_PAGES = [x for x in (read_legal(s) for s in L["pages"]) if x]


def inline(t):
    t = _html.escape(t, quote=False)
    stash = []
    spans = find_markers(t)
    for a, b in reversed(spans):
        stash.append(t[a:b])
        t = t[:a] + f"\x00{len(stash) - 1}\x00" + t[b:]
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", t)
    t = re.sub(r"\[([^\]]+)\]\(((?:https?://|mailto:|#|/)[^)\s]*|[\w./-]+/?)\)", r'<a href="\2">\1</a>', t)
    t = re.sub(r"(?<![\"'=>(\w/])(https?://[^\s<)]+)", r'<a href="\1">\1</a>', t)
    t = re.sub(r"(?<![\w/>\"=:.\-])([\w.+-]+@[\w-]+(?:\.[\w-]+)+)", r'<a href="mailto:\1">\1</a>', t)
    t = re.sub(r"\x00(\d+)\x00", lambda m: '<mark class="ph">' + stash[len(stash) - 1 - int(m.group(1))] + "</mark>", t)
    return t


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def md_to_html(md, slug, level=2):
    """plain markdown (headings, paragraphs, lists, tables, quotes, rules, bold, italic, links) -> html"""
    lines = md.splitlines()
    first_h1 = next((i for i, ln in enumerate(lines) if re.match(r"#\s", ln)), None)
    if first_h1 is not None:
        lines[first_h1] = ""            # the page title comes from the front matter
    levels = [len(m.group(1)) for m in (re.match(r"(#{1,6})\s", ln) for ln in lines) if m]
    base = min(levels) if levels else 2
    out, para, items, kind, rows, quote = [], [], [], None, [], []

    def flush():
        nonlocal para, items, kind, rows, quote
        if para:
            out.append("<p>" + " ".join(inline(x) for x in para) + "</p>")
        if items:
            tag = "ol" if kind == "ol" else "ul"
            out.append(f"<{tag}>" + "".join(f"<li>{inline(x)}</li>" for x in items) + f"</{tag}>")
        if rows:
            cells = lambda r: [c.strip() for c in r.strip().strip("|").split("|")]
            head, body = cells(rows[0]), [cells(r) for r in rows[2:]]
            out.append('<div class="table-wrap"><table' + (' class="wide"' if len(head) > 2 else "") + "><thead><tr>" +
                       "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr></thead><tbody>" +
                       "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body) + "</tbody></table></div>")
        if quote:
            out.append("<blockquote><p>" + " ".join(inline(x) for x in quote) + "</p></blockquote>")
        para, items, kind, rows, quote = [], [], None, [], []

    for ln in lines:
        s = ln.rstrip()
        if not s.strip():
            flush(); continue
        h = re.match(r"(#{1,6})\s+(.*)", s)
        if h:
            flush()
            lv = min(level + 2, level + max(0, len(h.group(1)) - base))
            title = h.group(2).strip()
            num = re.match(r"(\d+)\.", title)
            hid = f"{slug}-{num.group(1)}" if num else f"{slug}-{slugify(re.sub(r'<[^>]+>', '', title))[:40]}"
            out.append(f'<h{lv} id="{hid}">{inline(title)}</h{lv}>'); continue
        if re.fullmatch(r"\s*(---+|\*\*\*+|___+)\s*", s):
            flush(); out.append("<hr>"); continue
        if s.startswith("|"):
            if para or items or quote: flush()
            rows.append(s); continue
        if s.startswith(">"):
            if para or items or rows: flush()
            quote.append(s.lstrip("> ").rstrip()); continue
        m_ul, m_ol = re.match(r"\s*[-*•]\s+(.*)", s), re.match(r"\s*\d+[.)]\s+(.*)", s)
        if (m_ul or m_ol) and not s.startswith("**"):
            k = "ol" if m_ol else "ul"
            if para or rows or quote or (items and kind != k): flush()
            kind = k; items.append((m_ol or m_ul).group(1)); continue
        if items and s.startswith((" ", "\t")):
            items[-1] += " " + s.strip(); continue
        if items or rows or quote: flush()
        para.append(s)
    flush()
    return "\n".join(out)


def legal_block(page, level):
    U = C["legal_ui"]
    banner = ""
    if page["status"] == "draft" and page.get("banner", "site") != "own":
        banner = f'<p class="notice"><strong>{esc(U["draft"])}</strong></p>\n'
    meta = (f'<p class="legal__meta">{esc(fmt(U["version"], version=page["version"]))} · '
            f'{esc(fmt(U["updated"], date=page["date_text"]))}</p>\n')
    body = md_to_html(page["body"], page["slug"], level)
    return (f'<div class="wrap legal__wrap">\n<p class="eyebrow">{esc(U["eyebrow"])}</p>\n'
            f'<h{level} class="legal__title" id="{page["slug"]}-title">{esc(page["title"])}</h{level}>\n{meta}{banner}'
            f'<div class="legal__body">\n{body}\n</div>\n</div>')


# ---------- markers: one list, and the live check ----------
def site_markers():
    out = []

    def walk(v, path):
        if isinstance(v, str):
            for m in marker_texts(v):
                out.append((f"site.json  {path}", m))
        elif isinstance(v, dict):
            for k, x in v.items():
                walk(x, f"{path}.{k}" if path else k)
        elif isinstance(v, list):
            for i, x in enumerate(v):
                walk(x, f"{path}.{i}")
    walk(site, "")
    return out


def check_markers():
    rows = site_markers()
    live_site = site.get("status") == "live"
    bad = []
    if live_site:
        bad += [f"{w}: {m}" for w, m in rows]
    credits = ROOT / "CREDITS.md"
    if credits.exists():
        for m in marker_texts(credits.read_text(encoding="utf-8")):
            rows.append(("CREDITS.md", m))
            if live_site:
                bad.append(f"CREDITS.md: {m}")
    for p in LEGAL_PAGES:
        mk = marker_texts(p["body"])
        rows += [(f"legal/{p['slug']}.md", m) for m in mk]
        if p["status"] == "live" and mk:
            bad += [f"legal/{p['slug']}.md is marked live but still has: {m}" for m in mk]
        if live_site and p["status"] != "live":
            warnings.append(f"the site is live but legal/{p['slug']}.md is still marked {p['status']}")
    lines = ["# Open markers", "",
             "Written by `build.py` every time it runs. Do not edit by hand. Each line is something that has not been supplied yet.",
             "Fill it in where it says (a legal page, or a field in `site.json`), run `python3 build.py`, and it drops off this list.",
             "", f"Site status: **{site.get('status')}** · Mode: **{site.get('mode')}** · Markers open: **{len(rows)}**", "",
             "| Where | Marker |", "|---|---|"]
    lines += [f"| `{w.strip()}` | {m.replace('|', '/')} |" for w, m in rows] or ["| (none) | |"]
    lines += ["", "A marker is any text in square brackets that starts with one of: " + ", ".join(f"`[{w}`" for w in MARKER_WORDS) + ".",
              "A page, or the site, marked `live` cannot be built while a marker is open in it.", ""]
    (ROOT / "OPEN-MARKERS.md").write_text("\n".join(lines), encoding="utf-8")
    for b in bad:
        fail("open marker in a page marked live: " + b)
    return rows


MARKER_ROWS = check_markers()


# ---------- the Premium page: sections written from site.json ----------
def nav_items():
    return "\n".join(f'        <li><a href="#{i}" data-nav="{i}">{esc(t)}</a></li>' for i, t in C["nav"])


def hero_lines():
    return "\n".join(f'        <span class="ln" style="--i:{i}"><span>{esc(t)}</span></span>' for i, t in enumerate(C["hero"]["lines"]))


def pills():
    cards = C["levels"]["cards"]
    return "\n".join(f'            <button class="pill" type="button" data-tier="{c["key"]}" aria-pressed="{"true" if i == 0 else "false"}">{esc(c["name"])}</button>'
                     for i, c in enumerate(cards))


def ladder_steps():
    out = []
    for i, c in enumerate(C["levels"]["cards"]):
        key, name, prem = c["key"], c["name"], c["key"] == "premium"
        ticks = "\n".join(f"              <li>{esc(t)}</li>" for t in c["ticks"])
        tail = (f'<p class="step__here">{esc(C["levels"]["here"])}</p>' if prem else
                f'<a class="demolink" href="#demo-{key}">{esc(fmt(C["levels"]["see_demo"], tier=name))} <span aria-hidden="true">→</span></a>')
        subject = quote(fmt(C["viewer"]["end_subject"], tier=name), safe="")
        out.append(f'''          <li class="step{" is-active" if i == 0 else ""}" data-step="{key}">
            <p class="step__tag{" step__tag--premium" if prem else ""}">{esc(name)}</p>
            <h3>{esc(c["title"])}</h3>
            <ul class="ticks">
{ticks}
            </ul>
            <p class="step__price"><strong>{esc(site["prices"][key])}</strong><span>{esc(site["price_tag"][key])}</span></p>
            {tail}
            <p class="step__cta">{esc(C["cta"])} <a href="mailto:{site["email"]}?subject={subject}">{esc(fmt(C["plan_mail"], plan=name))}</a></p>
          </li>''')
    return "\n".join(out)


def open_demo_standard():
    return esc(fmt(C["levels"]["open_demo"], tier=C["levels"]["cards"][0]["name"]))


def pricing_note():
    P = C["pricing"]
    return f'<div class="pricenote reveal"><p>{esc(P["note"])}</p><p class="fine">{esc(P["small"])}</p></div>'


def features():
    F, n = C["included"]["features"], len(C["included"]["features"])
    out = []
    for i, f in enumerate(F):
        d = f' style="--d:{("%g" % (i * .05)).lstrip("0")}s"' if i else ""
        wide = " feat__item--wide" if (i == n - 1 and n % 2) else ""
        out.append(f'            <li class="feat__item{wide} reveal"{d}><div class="feat__card"><span class="feat__ic"><svg class="ic"><use href="#i-{f["icon"]}"/></svg></span><span class="feat__t">{esc(f["text"])}</span></div></li>')
    return "\n".join(out)


def extras():
    return "\n".join(f'            <li><svg class="ic"><use href="#i-{e["icon"]}"/></svg>{esc(e["text"])}</li>' for e in C["included"]["extras"])


def extras_mail():
    return f'mailto:{site["email"]}?subject={quote(C["included"]["extras_subject"], safe="")}'


def timeline():
    out = []
    for n, st in enumerate(C["process"]["steps"], 1):
        t, p = demos.step_parts(st)
        out.append(f'''        <li class="t-step reveal">
          <span class="t-num" aria-hidden="true">{n}</span>
          <div><h3>{esc(t)}</h3>{f"<p>{esc(p)}</p>" if p else ""}</div>
        </li>''')
    return "\n".join(out)


def process_notes():
    notes = ([site["advertise"]["quote"]] if ADVERTISE else []) + [C["process"]["note"]]
    return '<div class="process__notes reveal">' + "".join(f"<p>{esc(n)}</p>" for n in notes) + "</div>"


def faq_list():
    return "\n".join(f"        <details>\n          <summary>{esc(q)}</summary>\n          <p>{esc(a)}</p>\n        </details>" for q, a in C["faq"]["items"])


def contact_privacy(link):
    K = C["contact"]
    return f'{esc(K["privacy_text"])} <a href="{link("privacy")}">{esc(K["privacy_link"])}</a>.'


def footer(link, top_href, top_label):
    """the bottom of the Premium page and of the legal pages: the call to action, a link to every legal page, the mode note"""
    F = C["footer"]["legal"]
    links = " · ".join(f'<a href="{link(s)}">{esc(F[s])}</a>' for s in L["pages"])
    note = f'\n    <p class="footer__note">{esc(site["advertise"]["footer"])}</p>' if ADVERTISE else ""
    return f'''<footer class="site-footer" data-tone="light">
  <div class="wrap footer__bar">
    <p class="footer__name"><strong>{esc(site["name"])}</strong></p>
    <p class="footer__cta">{esc(C["cta"])} <a href="mailto:{site["email"]}">{esc(C["mail"])}</a></p>
    <p class="footer__meta">© {site["year"]} {esc(site["name"])} · {links} · <a href="{top_href}">{esc(top_label)}</a></p>{note}
  </div>
</footer>'''


def ui_json():
    Lv = C["levels"]
    ui = dict(C["ui"])
    ui.update(pause=C["samples"]["pause"], play=C["samples"]["play"], open_demo=Lv["open_demo"], open_premium=Lv["open_premium"],
              note_sample=Lv["note_sample"], note_premium=Lv["note_premium"], tiers={c["key"]: c["name"] for c in Lv["cards"]})
    return '<script type="application/json" id="ui-copy">' + json.dumps(ui, ensure_ascii=False).replace("</", "<\\/") + "</script>"


def mocks():
    m, b = C["levels"]["mock"], None
    e = lambda s: esc(s)
    mail = e(C["mail"])
    nav_s = "".join(f"<span>{e(x)}</span>" for x in m["nav_standard"])
    nav_p = "".join(f'<span{" class=" + chr(34) + "on" + chr(34) if i == 0 else ""}>{e(x)}</span>' for i, x in enumerate(m["nav_pro"]))
    cols = lambda: "".join(f"<div><b>{e(s)}</b><i></i><i></i></div>" for s in m["services"])
    stack = "".join(f'<div class="c{i}"><b>{e(s)}</b><i></i></div>' for i, s in enumerate(m["stack"], 1))
    br = e(m["brand"])
    return f'''              <div class="mock mock--standard"><div class="m">
                <div class="m-nav"><b>{br}</b>{nav_s}</div>
                <div class="m-hero"><h4>{e(m["title"])}</h4><p>{e(m["line"])}</p><span class="m-btn">{mail}</span></div>
                <div class="m-cols">{cols()}</div>
              </div></div>
              <div class="mock mock--pro"><div class="m">
                <div class="m-top">
                  <div class="m-nav"><b>{br}</b>{nav_p}</div>
                  <div class="m-copy"><h4>{e(m["title"])}</h4><p>{e(m["line"])}</p><span class="m-btn">{mail}</span></div>
                  <div class="m-art"><div class="m-blk b1"></div><div class="m-blk b2"></div><div class="m-blk b3"></div></div>
                </div>
                <div class="m-cards">{cols()}</div>
              </div></div>
              <div class="mock mock--premium"><div class="m">
                <div class="m-glow"></div>
                <div class="m-nav"><b>{br}</b>{nav_p}</div>
                <h4><span>{e(m["premium_title"][0])}</span><span class="o">{e(m["premium_title"][1])}</span></h4>
                <p>{e(m["line"])}</p>
                <span class="m-btn">{mail}</span>
                <svg class="m-seal" viewBox="0 0 100 100" aria-hidden="true"><defs><path id="seal-path" d="M50,50 m-36,0 a36,36 0 1,1 72,0 a36,36 0 1,1 -72,0"/></defs><g class="m-seal__ring"><text><textPath href="#seal-path" textLength="222" lengthAdjust="spacing">{e(m["seal"])}</textPath></text></g><circle cx="50" cy="50" r="6"/></svg>
                <div class="m-stack">{stack}</div>
              </div></div>'''


def sample(s):
    bg, ink, brand, acc = site["themes"][s["theme"]]
    btn_ink = on(brand, bg, ink)
    style = f"--s-bg:{bg};--s-ink:{ink};--s-brand:{brand};--s-acc:{acc};--s-on:{btn_ink}"
    nav = f'<div class="s-nav"><b>{esc(s["brand"])}</b><i></i><i></i><i></i></div>'
    btn = f'<span class="s-btn">{esc(C["mail"])}</span>'
    key = s.get("photo")
    ph = bool(key) and has_img(f"trade-{key}.webp")      # without the picture the painted version is used
    body = f'<div class="s-body"><h4>{esc(s["headline"])}</h4><p>{esc(s["sub"])}</p>{btn}</div>'
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
            f'          <figcaption><strong>{esc(s["trade"])}</strong><span>{esc(fmt(C["samples"]["caption"], theme=s["theme"]))}</span></figcaption>\n'
            f'        </figure>')


# ---------- the floating stones ----------
# 1, 2 and 3 are the stones that glow at night (size of the glow as a share of the whole picture)
GLOW = {1: 17, 2: 11, 3: 7}
# how far each stone drifts, as a share of its own height: near stones drift less, far ones a little more, so none look pinned
AMP = {1: 4.2, 2: 5.2, 3: 8, 4: 8.5, 5: 9, 6: 8.5, 7: 9}


def rocks():
    data = json.loads((SRC / "rocks.json").read_text(encoding="utf-8"))
    pw, ph = data["picture"]
    rnd = random.Random(20261027)           # fixed, so the page is the same every build
    out = []
    for r in data["rocks"]:
        n = r["n"]
        dur = rnd.uniform(7.5, 12.5)
        delay = -rnd.uniform(0, dur)
        style = (f"left:{r['x'] / pw * 100:.3f}%;top:{r['y'] / ph * 100:.3f}%;width:{r['w'] / pw * 100:.3f}%;"
                 f"--amp:{AMP.get(n, 8)}%;--dur:{dur:.1f}s;--delay:{delay:.1f}s")
        glow = ""
        if n in GLOW:
            glow = f'<i class="glow" data-glow style="--x:50%;--y:50%;--s:{GLOW[n] / 100 * pw / r["w"] * 100:.0f}%"></i>'
        out.append(f'        <div class="rock" style="{style}"><img src="img/rock-{n}.webp" width="{r["w"]}" height="{r["h"]}" alt="" decoding="async">{glow}</div>')
    return "\n".join(out)


# the swirl in the doorway of pro-hero.webp, as fractions of the picture: d = width of the turning circle, cx / cy = its centre
DOOR = {"d": 0.115, "cx": 0.5000, "cy": 0.5244}


# pictures are background images set by class, so each one is stored once however often it is used
def photo_css():
    out = ["\n/* ---------- pictures (written by build.py from whatever is in src/img) ---------- */"]
    for key in ("plumbing", "salon", "cafe", "garage", "cleaning", "firm"):
        if has_img(f"trade-{key}.webp"):
            out.append(f"html .ph.ph-{key} {{ background-image: url(../img/trade-{key}.webp); background-size: cover; background-position: center; }}")
    if has_img("levels-bg.webp"):
        out.append("html .levels__bg { background-image: url(../img/levels-bg.webp); background-size: cover; background-position: center bottom; }")
        out.append("html .ps-sky { background-image: url(../img/levels-bg.webp); }")   # the soft sunrise sky, Standard
    if has_img("pro-hero.webp"):
        # the Pro opening: the portal picture, and a small round copy of the swirl in its doorway that turns
        d, cx, cy, ar = DOOR["d"], DOOR["cx"], DOOR["cy"], 944 / 1680
        px = (0.5 - cx / d) / (1 - 1 / d) * 100
        py = (0.5 - (ar / d) * cy) / (1 - ar / d) * 100
        out.append("html .pp-scene, html .pp-door { background-image: url(../img/pro-hero.webp); }")
        out.append(f"html .pp-door {{ left: {cx * 100:.2f}%; top: {cy * 100:.2f}%; width: {d * 100:.2f}%; aspect-ratio: 1; "
                   f"background-size: {100 / d:.2f}% auto; background-position: {px:.2f}% {py:.2f}%; }}")
    if has_img("pro-valley.webp"):
        out.append("html .pp-contact__bg, html .ps-contact__bg { background-image: url(../img/pro-valley.webp); background-size: cover; background-position: center; }")
    # the three forest backgrounds of the Standard page (already mixed into the off-white, see prep_images.py)
    for cls, img, pos in (("ps-top", "ps-castle", "70% 22%"), ("ps-band--gate", "ps-gateway", "72% 30%"), ("ps-band--path", "ps-path", "68% 50%")):
        if has_img(f"{img}.webp"):
            out.append(f"html .{cls} {{ background-image: url(../img/{img}.webp); background-size: cover; background-position: {pos}; }}")
            if cls == "ps-top":   # on a phone the tower sits to the right of the writing
                out.append("@media (max-width: 899px) { html .ps-top { background-position: 84% 0; } }")
    return "\n".join(out) + "\n"


# ---------- shared tokens ----------
t = site["theme"]
fav_svg = (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='8' fill='{t['brand']}'/>"
           f"<path d='M10 24V8h7.2a5 5 0 0 1 0 10H14' fill='none' stroke='{t['bg']}' stroke-width='3.2' stroke-linecap='round' stroke-linejoin='round'/></svg>")
favicon = "data:image/svg+xml," + quote(fav_svg, safe="/:=' ")


def jsonld(path=""):
    d = {"@context": "https://schema.org", "@type": site["seo"]["schema_type"],
         "name": site["name"], "description": site["description"], "email": site["email"],
         "areaServed": {"@type": "Country", "name": site["seo"]["area_served"]},
         "serviceType": site["seo"]["service_type"], "knowsLanguage": site["seo"]["language"]}
    if not DOMAIN_OPEN:
        d["url"] = site["domain"].rstrip("/") + "/"
    return json.dumps(d, ensure_ascii=False)


def link_root(slug):
    return f"{slug}/"


def link_sub(slug):
    return f"../{slug}/"


def tokens_for(base="", link=link_root, path=""):
    return {
        "name": esc(site["name"]), "email": site["email"], "mode": site["mode"], "seo_title": esc(site["seo_title"]),
        "description": esc(site["description"]), "year": site["year"], "bg": t["bg"], "base": base,
        "favicon": favicon, "jsonld": jsonld(), "head_social": head_social(path),
        "brand_aria": esc(fmt(C["top_aria"], name=site["name"])),
        "nav_items": nav_items(), "rocks": rocks(), "hero_lines": hero_lines(), "pills": pills(),
        "open_demo_standard": open_demo_standard(), "ladder_steps": ladder_steps(), "pricing_note": pricing_note(),
        "mocks": mocks(), "samples": "\n".join(sample(s) for s in site["samples"]),
        "features": features(), "extras": extras(), "extras_mail": esc(extras_mail()),
        "timeline": timeline(), "process_notes": process_notes(), "faq_list": faq_list(),
        "contact_privacy": contact_privacy(link), "demos": demos.build(site, on),
        "footer": footer(link, "#top", C["top"]), "ui_json": ui_json(),
    }


def render(template, tokens):
    s = (SRC / template).read_text(encoding="utf-8")
    s = re.sub(r"\{\{\s*([\w.]+)\s*\}\}", lambda m: tokens[m.group(1)] if m.group(1) in tokens else (
        esc(get(m.group(1))) if m.group(1).split(".")[0] in site else m.group(0)), s)
    left = re.findall(r"\{\{[^}]*\}\}", s)
    if left:
        sys.exit(f"{template}: unfilled tokens {left}")
    return s


# ---------- dist ----------
if DIST.exists():
    shutil.rmtree(DIST)
for sub in ("css", "js", "fonts", "img"):
    shutil.copytree(SRC / sub, DIST / sub)
CSS_ALL = (SRC / "css" / "styles.css").read_text(encoding="utf-8") + "\n" + (SRC / "css" / "tiers.css").read_text(encoding="utf-8") + photo_css()
(DIST / "css" / "styles.css").write_text(CSS_ALL, encoding="utf-8")
(DIST / "css" / "tiers.css").unlink()   # one stylesheet is shipped


def make_og():
    """the picture shown when the link is shared (og.png). Drawn here from the words in site.json, the Forest colours and the local fonts, so it never carries old wording."""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        warnings.append("Pillow is not installed, so og.png was not drawn")
        return
    W, H, t = 1200, 630, site["theme"]
    im = Image.new("RGB", (W, H), "#FFFFFF")

    def glow(cx, cy, r, col, a):
        g = Image.radial_gradient("L").resize((2 * r, 2 * r)).point(lambda v: max(0, int((255 - v * 1.4143) * a)))   # fades to nothing at the circle's edge
        im.paste(Image.new("RGB", g.size, col), (cx - r, cy - r), g)
    glow(1020, 120, 520, "#1FAE6C", .22)
    glow(80, 470, 460, "#D6F1E2", 1.0)
    d = ImageDraw.Draw(im)
    for r, col in ((250, "#D6F1E2"), (190, "#BFE8D2"), (130, "#1FAE6C"), (70, t["brand"])):   # a doorway: rings of mint, emerald and forest
        d.ellipse((960 - r, 315 - r, 960 + r, 315 + r), fill=col)
    d.ellipse((960 - 26, 315 - 26, 960 + 26, 315 + 26), fill="#FFFFFF")

    def head(size, wght):
        f = ImageFont.truetype(str(SRC / "fonts" / "archivo-display.woff"), size)
        f.set_variation_by_axes([wght, 104])
        return f
    body = ImageFont.truetype(str(SRC / "fonts" / "schibsted-body.woff"), 30)
    body.set_variation_by_axes([400])
    eb = ImageFont.truetype(str(SRC / "fonts" / "schibsted-body.woff"), 22)
    eb.set_variation_by_axes([700])
    x, y = 72, 86
    for ch in C["hero"]["eyebrow"].upper():                      # the small label, with a little space between the letters
        d.text((x, y), ch, font=eb, fill=t["brand"])
        x += eb.getlength(ch) + 3.2
    big = head(104, 800)
    for i, line in enumerate(C["hero"]["lines"]):
        d.text((68, 128 + i * 104), line, font=big, fill=t["brand"] if i == len(C["hero"]["lines"]) - 1 else t["ink"])
    d.text((72, 470), C["hero"]["lead"], font=body, fill="#44504A")
    d.text((72, 546), site["name"], font=head(34, 800), fill=t["brand"])
    im.save(DIST / "og.png", optimize=True)


make_og()


def write(rel, text):
    p = DIST / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


write("index.html", render("index.html", tokens_for("", link_root, "")))

for key, name in demos.TIERS[:2]:
    body, vars_ = demos.page(site, on, key)
    tk = tokens_for("../", link_sub, f"{key}/")
    fonts = ("prime-serif.woff",) if key == "standard" else ("archivo-display.woff", "schibsted-body.woff")   # Standard has its own typeface
    tier_fonts = "\n".join(f'<link rel="preload" href="../fonts/{f}" as="font" type="font/woff" crossorigin>' for f in fonts)
    tk.update(tier_body=body, tier_vars=vars_, tier_title=esc(f"{site['name']} | {name}"), tier_class=f"tier--{key}", tier_fonts=tier_fonts)
    write(f"{key}/index.html", render("tier.html", tk))

for p in LEGAL_PAGES:
    tk = tokens_for("../", link_sub, f"{p['slug']}/")
    tk.update(legal=legal_block(p, 1), legal_title=esc(p["title"]), legal_slug=p["slug"],
              legal_desc=esc(fmt(C["legal_ui"]["desc"], title=p["title"], name=site["name"])),
              footer=footer(link_sub, "../", C["legal_ui"]["back"]),
              back_aria=esc(fmt(C["legal_ui"]["back_aria"], name=site["name"])), back_label=esc(C["legal_ui"]["back"]))
    write(f"{p['slug']}/index.html", render("legal.html", tk))

# ---------- single-file previews ----------
css = CSS_ALL


def font_uri(m):
    data = (SRC / "css" / m.group(1)).resolve().read_bytes()
    return "url(data:font/woff;base64," + base64.b64encode(data).decode() + ") format(\"woff\")"


css = re.sub(r'url\(([^)]*?\.woff)\) format\("woff"\)', font_uri, css)
css = re.sub(r'url\(\.\./img/([^)]*?\.webp)\)', lambda m: "url(data:image/webp;base64," + base64.b64encode((SRC / "img" / m.group(1)).read_bytes()).decode() + ")", css)
js = (SRC / "js" / "intro.js").read_text(encoding="utf-8") + "\n" + (SRC / "js" / "main.js").read_text(encoding="utf-8")

_pl = ROOT / "preview_links.json"
LINKS = json.loads(_pl.read_text(encoding="utf-8")) if _pl.exists() else {}


def inline_images(s):
    return re.sub(r'src="img/([^"]+\.webp)"', lambda m: 'src="data:image/webp;base64,' + base64.b64encode((SRC / "img" / m.group(1)).read_bytes()).decode() + '"', s)


full = (DIST / "index.html").read_text(encoding="utf-8")
head = re.search(r"<head>(.*?)</head>", full, re.S).group(1)
body = re.search(r"<body[^>]*>(.*)</body>", full, re.S).group(1)
body = re.sub(r'<script src="js/(?:intro|main).js" defer></script>\s*', "", body)
body = inline_images(body)
# one file: the legal pages open as sections of the page, and a level's own page is its own preview
for slug in L["pages"]:
    body = body.replace(f'href="{slug}/"', f'href="#{slug}"')
body = re.sub(r'<a class="demo__own" href="(standard|pro)/">.*?</a>',
              lambda m: (f'<a class="demo__own" href="{LINKS[m.group(1)]}" target="_blank" rel="noopener">{esc(C["viewer"]["own_page"])}</a>'
                         if LINKS.get(m.group(1)) else ""), body)
inline_secs = "".join(
    f'<section class="legal legal--inline" id="{p["slug"]}" data-tone="light" aria-labelledby="{p["slug"]}-title">\n{legal_block(p, 2)}\n'
    f'<div class="wrap legal__wrap"><a class="link" href="#top">{esc(C["legal_ui"]["back"])}</a></div>\n</section>\n' for p in LEGAL_PAGES)
assert '<footer class="site-footer"' in body
body = body.replace('<footer class="site-footer"', inline_secs + '<footer class="site-footer"', 1)
keep_meta = "\n".join(re.findall(r'<meta (?:name="description"|property="og:[^"]+"|name="twitter:card")[^>]*>', head))
ld = re.search(r'<script type="application/ld\+json">.*?</script>', head, re.S).group(0)
art = (f'<title>{esc(site["artifact_title"])}</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n{keep_meta}\n'
       f'<script>document.documentElement.classList.add("js")</script>\n<style>\n{css}\n</style>\n{ld}\n{body}\n<script>\n{js}\n</script>\n')
write("artifact.html", art)

# the same page as one complete file (with a doctype) that opens by double-click, offline
demo = ('<!doctype html>\n<html lang="en-ZA">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        f'<title>{esc(site["seo_title"])}</title>\n{keep_meta}\n<meta name="theme-color" content="{t["bg"]}">\n<link rel="icon" href="{favicon}">\n'
        f'<script>document.documentElement.classList.add("js")</script>\n<style>\n{css}\n</style>\n{ld}\n</head>\n<body data-mode="{site["mode"]}">\n{body}\n<script>\n{js}\n</script>\n</body>\n</html>\n')
write("prime-solutions-demo.html", demo)

# Standard and Pro as one file each. Links to the other levels point at their preview pages, listed in
# preview_links.json (made after they are published); without it they stay on the page.
def _out(url):
    return f'href="{url}" target="_blank" rel="noopener"' if url else 'href="#main"'


tjs = (SRC / "js" / "tier.js").read_text(encoding="utf-8")
for key, name in demos.TIERS[:2]:
    page = (DIST / key / "index.html").read_text(encoding="utf-8")
    tb = re.search(r"<body[^>]*>(.*)</body>", page, re.S).group(1)
    tb = re.sub(r'<script src="\.\./js/tier.js" defer></script>\s*', "", tb)
    prem = LINKS.get("premium", "")
    tb = tb.replace('href="../"', _out(prem))
    for other in ("standard", "pro"):
        tb = tb.replace(f'href="../{other}/"', _out(LINKS.get(other, "")))
    for slug in L["pages"]:   # the legal pages open as sections of this file, so the footer links work on their own
        tb = tb.replace(f'href="../{slug}/"', f'href="#{slug}"')
    tb = tb.replace("</footer>", "</footer>\n" + inline_secs.replace('href="#top"', 'href="#main"'), 1) if "</footer>" in tb else tb + inline_secs
    left = re.findall(r'href="\.\./[^"]*"', tb)
    assert not left, left
    tart = (f'<title>{esc(site["artifact_title"] + " " + name)}</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'
            f'<meta name="description" content="{esc(site["description"])}">\n'
            f'<script>document.documentElement.classList.add("js")</script>\n<style>\n{css}\n</style>\n{ld}\n'
            f'<div class="tier-page tier--{key}" data-mode="{site["mode"]}">\n{tb}\n</div>\n<script>\n{tjs}\n</script>\n')
    write(f"artifact-{key}.html", tart)

# ---------- report ----------
total = sum(p.stat().st_size for p in DIST.rglob("*") if p.is_file() and p.suffix in (".html", ".css", ".js", ".woff", ".webp") and not p.name.startswith(("artifact", "prime-solutions")))
open_n = len(MARKER_ROWS)
print(f"built dist/  ({total / 1024:.0f} KB of pages, styles, scripts, fonts and pictures) | mode: {site['mode']} | status: {site['status']}")
print(f"{open_n} marker{'s' if open_n != 1 else ''} still open (see OPEN-MARKERS.md)")
for w in warnings:
    print("WARNING:", w)
if errors:
    print("\nBUILD FAILED:")
    for e in errors:
        print(" -", e)
    sys.exit(1)
