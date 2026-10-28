"""The Standard and Pro versions of the Prime Solutions site.

Premium is the page itself (the entrance, the valley, the sheets). These two are the same one-page site built
at the other two levels: the same sections, the same words, the same prices. Only the treatment changes.
All wording comes from site.json ("copy"); nothing is written out here.

Two ways of showing them, from the same markup:
  viewer      full-screen sections on the main page (#demo-standard, #demo-pro), opened from the Three levels section
  standalone  their own pages, standard/index.html and pro/index.html (written by build.py)

The styling is in src/css/tiers.css, the pictures are set by build.py (photo_css). No forms, no invented reviews or figures.
The earlier plumber sample pages are kept in archive/.
"""
import html

TIERS = [("standard", "Standard"), ("pro", "Pro"), ("premium", "Premium")]
PRE = {"standard": "std", "pro": "pro"}


def esc(s):
    return html.escape(str(s), quote=True)


ICONS = {
    "devices": '<rect x="2.5" y="5" width="13" height="9" rx="1.5"/><path d="M6 18h6M9 14v4"/><rect x="17" y="8" width="4.5" height="9" rx="1.2"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="m4 7 8 6 8-6"/>',
    "type": '<path d="M5 6V4.5h14V6M12 4.5v15M9 19.5h6"/>',
    "palette": '<path d="M12 3a9 9 0 1 0 0 18c1.4 0 2-.9 1.6-2-.4-1 .3-2 1.4-2H17a4 4 0 0 0 4-4c0-5-4-10-9-10Z"/><circle cx="7.5" cy="11" r="1"/><circle cx="10" cy="7" r="1"/><circle cx="15" cy="7.5" r="1"/>',
    "search": '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m20 20-4.8-4.8"/>',
    "bolt": '<path d="M13 2.5 5 13.5h6l-1 8 9-12h-6.3L13 2.5Z"/>',
    "code": '<path d="m8 7-5 5 5 5M16 7l5 5-5 5M13.5 5l-3 14"/>',
    "form": '<rect x="4" y="3.5" width="16" height="17" rx="2.5"/><path d="M8 8.5h8M8 12.5h8M8 16.5h4.5"/>',
    "cal": '<rect x="3.5" y="5" width="17" height="15.5" rx="2.5"/><path d="M3.5 10h17M8 3v4M16 3v4"/>',
    "bag": '<path d="M5 8h14l-1.2 11.5a1.5 1.5 0 0 1-1.5 1.3H7.7a1.5 1.5 0 0 1-1.5-1.3L5 8Z"/><path d="M9 8V6.5a3 3 0 0 1 6 0V8"/>',
    "lock": '<rect x="4.5" y="10.5" width="15" height="10" rx="2.5"/><path d="M8 10.5V8a4 4 0 0 1 8 0v2.5"/>',
    "pin": '<path d="M12 21.5s7-6.2 7-11.5a7 7 0 1 0-14 0c0 5.3 7 11.5 7 11.5Z"/><circle cx="12" cy="10" r="2.5"/>',
    "play": '<rect x="3" y="5" width="18" height="14" rx="3"/><path d="m10.5 9.2 4.5 2.8-4.5 2.8V9.2Z"/>',
    "grid": '<rect x="3.5" y="3.5" width="7" height="7" rx="1.5"/><rect x="13.5" y="3.5" width="7" height="7" rx="1.5"/><rect x="3.5" y="13.5" width="7" height="7" rx="1.5"/><rect x="13.5" y="13.5" width="7" height="7" rx="1.5"/>',
}




def ic(name):
    return f'<svg class="d-ic" viewBox="0 0 24 24" aria-hidden="true" focusable="false">{ICONS[name]}</svg>'


def fmt(text, **kw):
    return text.format(**kw)


class Ctx:
    """where the page is shown decides what its links do"""

    def __init__(self, key, viewer, site):
        self.key, self.viewer, self.pre = key, viewer, PRE[key]
        self.site, self.C = site, site["copy"]
        self.name, self.email, self.year = site["name"], site["email"], site["year"]
        self.prices, self.tags = site["prices"], site["price_tag"]
        self.samples = site["samples"]
        self.adv = site.get("mode") == "advertise-only"

    def jump(self, sid):
        """a link that scrolls inside this page"""
        if self.viewer:
            return f'href="#demo-{self.key}" data-goto="{self.pre}-{sid}"'
        return f'href="#{self.pre}-{sid}"'

    def tier(self, kind):
        """a link to one of the three levels"""
        if kind == "premium":
            return 'href="#top" data-premium' if self.viewer else 'href="../"'
        return f'href="#demo-{kind}"' if self.viewer else f'href="../{kind}/"'

    def own_page(self):
        """this level on its own page, from inside the viewer (same domain)"""
        return f'href="{self.key}/"'

    def mail(self, subject=""):
        from urllib.parse import quote
        return f'href="mailto:{self.email}' + (f'?subject={quote(subject, safe="")}' if subject else "") + '"'

    def legal(self, slug):
        return f'href="{slug}/"' if self.viewer else f'href="../{slug}/"'


def email_btn(c, cls="", label=None, subject=""):
    return f'<a class="d-btn {cls}" {c.mail(subject)}>{esc(label or c.C["mail"])}</a>'


def copyrow(c):
    return (f'<span class="d-addr">{c.email}</span>'
            f'<button class="d-copy" type="button" data-copy-demo="{c.email}">{esc(c.C["contact"]["copy"])}</button>')


def tier_tail(c, card):
    """the bottom of a level card: 'This page', or a way to open that level"""
    L, key, name = c.C["levels"], card["key"], card["name"]
    if key == c.key:
        return f'<span class="ps-here">{esc(L["this_page"])}</span>'
    label = L["see_premium"] if key == "premium" else fmt(L["see_demo"], tier=name)
    return f'<a class="d-link" {c.tier(key)}>{esc(label)} <span aria-hidden="true">→</span></a>'


def level_card(c, card, cls, kick):
    key, name = card["key"], card["name"]
    ticks_html = "".join(f"<li>{esc(t)}</li>" for t in card["ticks"])
    here = " is-here" if key == c.key else ""
    mail = f'<p class="plan-cta">{esc(c.C["cta"])} <a {c.mail(fmt(c.C["viewer"]["end_subject"], tier=name))}>{esc(fmt(c.C["plan_mail"], plan=name))}</a></p>'
    return (f'<article class="{cls}{here}">\n'
            f'  <p class="{kick}">{esc(name)}</p>\n  <h4>{esc(card["title"])}</h4>\n  <ul class="ps-ticks">{ticks_html}</ul>\n'
            f'  <p class="ps-price"><strong>{esc(c.prices[key])}</strong><span>{esc(c.tags[key])}</span></p>\n  {tier_tail(c, card)}\n  {mail}\n</article>')


def step_parts(step):
    """a step is a title, or [title, text]"""
    return (step, "") if isinstance(step, str) else (step[0], step[1])


def steps_html(c, numfmt, extra=lambda n: ""):
    out = []
    for n, st in enumerate(c.C["process"]["steps"], 1):
        t, p = step_parts(st)
        out.append(f'<li{extra(n)}><span class="n" aria-hidden="true">{numfmt(n)}</span><h4>{esc(t)}</h4>' + (f"<p>{esc(p)}</p>" if p else "") + "</li>")
    return "".join(out)


def process_notes(c, cls):
    notes = ([c.site["advertise"]["quote"]] if c.adv else []) + [c.C["process"]["note"]]
    return f'<div class="{cls}">' + "".join(f"<p>{esc(n)}</p>" for n in notes) + "</div>"


def pricing_note(c, cls):
    P = c.C["pricing"]
    return f'<div class="{cls}"><p>{esc(P["note"])}</p><p class="d-fine">{esc(P["small"])}</p></div>'


def contact_privacy(c):
    K = c.C["contact"]
    return f'{esc(K["privacy_text"])} <a {c.legal("privacy")}>{esc(K["privacy_link"])}</a>.'


def foot(c, pre):
    """the bottom of the page: the call to action, a link to each legal page, and the advertise-only note"""
    F = c.C["footer"]["legal"]
    links = " · ".join(f'<a {c.legal(slug)}>{esc(F[slug])}</a>' for slug in c.site["legal"]["pages"])
    note = f'<p class="{pre}-foot__note">{esc(c.site["advertise"]["footer"])}</p>' if c.adv else ""
    return (f'<footer class="{pre}-foot {pre}-wrap">\n'
            f'        <p class="{pre}-foot__cta">{esc(c.C["cta"])} <a {c.mail()}>{esc(c.C["mail"])}</a></p>\n'
            f'        <div class="{pre}-foot__row"><span>© {c.year} {esc(c.name)} · {links}</span><a {c.jump("top")}>{esc(c.C["top"])}</a></div>\n'
            f'        {note}\n      </footer>')


def nav_html(c):
    return "".join(f'<a {c.jump(i)}>{esc(t)}</a>' for i, t in c.C["nav"])


def hero_h(c):
    return "".join(f"<span>{esc(t)}</span>" for t in c.C["hero"]["lines"])


def samples_html(c, cls, pic, delay=False):
    out = []
    for i, s in enumerate(c.samples):
        d = f' style="--d:{(i % 3) * .1:.1f}s"' if delay else ""
        out.append(f'<figure class="{cls}"{d}><div class="{pic} ph ph-{s["photo"]}" role="img" aria-label="{esc(c.C["alt"][s["photo"]])}"></div>'
                   f'<figcaption><strong>{esc(s["trade"])}</strong><span>{esc(fmt(c.C["samples"]["caption"], theme=s["theme"]))}</span></figcaption></figure>')
    return "\n".join(out)


# ---------------------------------------------------------------- Standard: one typeface, calm and finished. Soft layered backgrounds, gentle shadows, richer sample cards, a slow fade as each part arrives.
# No portal, no sticky header, nothing that moves on hover or with the scroll: that is what Pro and Premium add.
def samples_std(c):
    out = []
    for i, s in enumerate(c.samples):
        bg, ink, brand, acc = c.site["themes"][s["theme"]]
        sw = "".join(f'<i style="background:{col}"></i>' for col in (brand, acc, bg))
        out.append(f'''<figure class="ps-sample d-rv" style="--d:{(i % 3) * .1:.1f}s">
  <div class="ps-sample__pic ph ph-{s["photo"]}" role="img" aria-label="{esc(c.C["alt"][s["photo"]])}"></div>
  <figcaption><strong>{esc(s["trade"])}</strong><span class="ps-sample__line">{esc(s["headline"])}</span><span class="ps-sample__theme"><span class="ps-sw" aria-hidden="true">{sw}</span>{esc(fmt(c.C["samples"]["caption"], theme=s["theme"]))}</span></figcaption>
</figure>''')
    return "\n".join(out)


def rgb(hexcol):
    h = hexcol.lstrip("#")
    return ",".join(str(int(h[i:i + 2], 16)) for i in (0, 2, 4))


def theme_vars(site):
    """the Standard colours (site.json, standard_theme) as the page's variables. Standard and Pro both use them; they override the shared Forest variables on the page's own frame only."""
    t = site["standard_theme"]
    return (f"--d-bg:{t['paper']};--d-ink:{t['ink']};--d-brand:{t['forest']};--d-deep:{t['forest_deep']};--d-acc:{t['sage_mid']};--d-on:{t['card']};"
            f"--d-mute:{t['mute']};--d-line:rgba(11,15,12,.16);--d-mint:{t['sage']};--d-mint2:{t['sage_soft']};--d-card:{t['card']};--d-paper2:{t['paper_deep']};"
            f"--ps-rgb:{rgb(t['paper'])}")


def std_vars(site):
    """the Standard page also has its own typeface"""
    return theme_vars(site) + ";--f-body:'Prime Serif','Lora',Georgia,'Times New Roman',serif;--f-display:'Prime Serif','Lora',Georgia,'Times New Roman',serif"


def standard(c):
    C = c.C
    levels = "\n".join(level_card(c, k, "ps-level d-rv", "ps-tag").replace('class="ps-level d-rv', f'style="--d:{i * .1:.1f}s" class="ps-level d-rv', 1)
                       for i, k in enumerate(C["levels"]["cards"]))
    samples = samples_std(c)
    feat = "".join(f'<li class="d-rv" style="--d:{(i % 2) * .08:.2f}s"><span class="ps-ic">{ic(f["icon"])}</span><span>{esc(f["text"])}</span></li>' for i, f in enumerate(C["included"]["features"]))
    extras = "".join(f'<li>{ic(e["icon"])}{esc(e["text"])}</li>' for e in C["included"]["extras"])
    steps = steps_html(c, str, lambda n: f' class="d-rv" style="--d:{(n - 1) % 2 * .1:.1f}s"')
    faq = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in C["faq"]["items"])
    I, K = C["included"], C["contact"]
    return f"""
    <div class="d d--standard" id="std-top" style="{std_vars(c.site)}">
      <div class="ps-top">
      <header class="ps-head"><div class="ps-wrap">
        <a class="ps-logo" {c.jump("top")} aria-label="{esc(fmt(C["top_aria"], name=c.name))}">{esc(C["brand"][0])} <span>{esc(C["brand"][1])}</span></a>
        <nav aria-label="{esc(C["viewer"]["page_aria"])}">{nav_html(c)}</nav>
        {email_btn(c)}
        <details class="ps-menu"><summary aria-label="{esc(C["ui"]["menu_open"])}"><span class="ps-burger" aria-hidden="true"><i></i><i></i><i></i></span></summary>
          <div class="ps-menu__panel">{nav_html(c)}</div></details>
      </div></header>
      <section class="ps-hero ps-wrap" aria-labelledby="std-hero-t">
        <div class="ps-hero__copy">
          <p class="ps-eyebrow">{esc(C["hero"]["eyebrow"])}</p>
          <h2 id="std-hero-t">{hero_h(c)}</h2>
          <p class="ps-lead">{esc(C["hero"]["lead"])}</p>
          <div class="ps-cta">{email_btn(c, "d-btn--lg")}<a class="d-link" {c.jump("levels")}>{esc(C["hero"]["see_levels"])}</a></div>
        </div>
      </section>
      </div>
      <section class="ps-band ps-band--soft" id="std-levels" aria-labelledby="std-levels-t"><div class="ps-sky" aria-hidden="true"></div><div class="ps-wrap ps-block">
        <div class="ps-block__head d-rv"><p class="ps-eyebrow">{esc(C["levels"]["eyebrow"])}</p><h3 id="std-levels-t">{esc(C["levels"]["title"])}</h3><p>{esc(C["levels"]["lead"])}</p></div>
        <div class="ps-levels">
{levels}
        </div>
        {pricing_note(c, "ps-note d-rv")}
      </div></section>
      <section class="ps-band ps-band--tint" id="std-samples" aria-labelledby="std-samples-t"><div class="ps-wrap ps-block">
        <div class="ps-block__head d-rv"><p class="ps-eyebrow">{esc(C["samples"]["eyebrow"])}</p><h3 id="std-samples-t">{esc(C["samples"]["title"])}</h3><p>{esc(C["samples"]["lead"])}</p></div>
        <div class="ps-samples">
{samples}
        </div>
      </div></section>
      <section class="ps-band ps-band--gate" id="std-included" aria-labelledby="std-included-t"><div class="ps-wrap ps-block">
        <div class="ps-block__head d-rv"><p class="ps-eyebrow">{esc(I["eyebrow"])}</p><h3 id="std-included-t">{esc(I["title"])}</h3></div>
        <div class="ps-incl">
          <div><p class="ps-sub d-rv">{esc(I["every"])}</p><ul class="ps-feat">{feat}</ul></div>
          <aside class="ps-extras d-rv" style="--d:.1s" aria-labelledby="std-extras-t">
            <p class="ps-sub">{esc(I["extras_tag"])}</p>
            <h4 id="std-extras-t">{esc(I["extras_title"])}</h4>
            <p>{esc(I["extras_sub"])}</p>
            <ul>{extras}</ul>
            {email_btn(c, "", I["extras_button"], I["extras_subject"])}
          </aside>
        </div>
      </div></section>
      <section class="ps-band ps-band--tint" id="std-process" aria-labelledby="std-process-t"><div class="ps-wrap ps-block">
        <div class="ps-block__head d-rv"><p class="ps-eyebrow">{esc(C["process"]["eyebrow"])}</p><h3 id="std-process-t">{esc(C["process"]["title"])}</h3><p>{esc(C["process"]["lead"])}</p></div>
        <ol class="ps-steps">{steps}</ol>
        {process_notes(c, "ps-note d-rv")}
      </div></section>
      <section class="ps-band ps-band--path" id="std-questions" aria-labelledby="std-questions-t"><div class="ps-wrap ps-block">
        <div class="ps-block__head d-rv"><p class="ps-eyebrow">{esc(C["faq"]["eyebrow"])}</p><h3 id="std-questions-t">{esc(C["faq"]["title"])}</h3></div>
        <div class="ps-faq d-rv">{faq}</div>
      </div></section>
      <section class="ps-contact" id="std-contact" aria-labelledby="std-contact-t">
        <div class="ps-contact__bg" aria-hidden="true"></div>
        <div class="ps-wrap ps-contact__in">
          <div class="ps-contact__txt d-rv">
            <p class="ps-eyebrow" style="color:inherit">{esc(K["eyebrow"])}</p>
            <h3 id="std-contact-t">{esc(K["title"])}</h3>
            <p class="ps-lead">{esc(C["cta"])}</p>
            {email_btn(c, "d-btn--lg")}
          </div>
          <div class="ps-card d-rv" style="--d:.1s">{copyrow(c)}<span>{contact_privacy(c)}</span></div>
        </div>
      </section>
      {foot(c, "ps")}
    </div>"""


# ---------------------------------------------------------------- Pro: two typefaces, the portal with only the swirl turning, layered blocks, reveals, a header that follows you down
def pro(c):
    C = c.C
    levels = "\n".join(level_card(c, k, "pp-level d-rv", "pp-kicker").replace('class="pp-level d-rv', f'style="--d:{i * .1:.1f}s" class="pp-level d-rv', 1)
                       for i, k in enumerate(C["levels"]["cards"]))
    samples = samples_html(c, "pp-sample d-rv", "pp-pic", delay=True)
    feat = "".join(f'<li class="d-rv" style="--d:{(i % 2) * .08:.2f}s"><span class="pp-ic">{ic(f["icon"])}</span><span>{esc(f["text"])}</span></li>' for i, f in enumerate(C["included"]["features"]))
    extras = "".join(f'<li>{ic(e["icon"])}{esc(e["text"])}</li>' for e in C["included"]["extras"])
    steps = steps_html(c, lambda n: f"{n:02d}", lambda n: f' class="d-rv" style="--d:{(n - 1) % 3 * .1:.1f}s"')
    faq = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in C["faq"]["items"])
    I, K = C["included"], C["contact"]
    return f"""
    <div class="d d--pro" id="pro-top" style="{theme_vars(c.site)}">
      <header class="pp-head"><div class="pp-wrap">
        <a class="pp-logo" {c.jump("top")} aria-label="{esc(fmt(C["top_aria"], name=c.name))}">{esc(C["brand"][0])} <span>{esc(C["brand"][1])}</span></a>
        <nav aria-label="{esc(C["viewer"]["page_aria"])}">{nav_html(c)}</nav>
        {email_btn(c)}
        <details class="ps-menu"><summary aria-label="{esc(C["ui"]["menu_open"])}"><span class="ps-burger" aria-hidden="true"><i></i><i></i><i></i></span></summary>
          <div class="ps-menu__panel">{nav_html(c)}</div></details>
      </div></header>
      <section class="pp-hero" aria-labelledby="pro-hero-t">
        <div class="pp-hero__pic" role="img" aria-label="{esc(C["alt"]["portal"])}"><div class="pp-scene"><div class="pp-mist" aria-hidden="true"><b></b><b></b><b></b></div></div></div>
        <div class="pp-wrap pp-hero__in">
          <div class="pp-hero__copy d-rv">
            <p class="pp-kicker">{esc(C["hero"]["eyebrow"])}</p>
            <h2 id="pro-hero-t">{hero_h(c)}</h2>
            <p class="pp-sub">{esc(C["hero"]["lead"])}</p>
            <div class="pp-cta">{email_btn(c, "d-btn--light d-btn--lg")}<a class="d-link" {c.jump("levels")}>{esc(C["hero"]["see_levels"])}</a></div>
          </div>
        </div>
      </section>
      <div class="pp-band pp-band--castle"><section class="pp-levels pp-wrap" id="pro-levels" aria-labelledby="pro-levels-t">
        <div class="pp-levels__head d-rv"><p class="pp-kicker">{esc(C["levels"]["lead"].rstrip("."))}</p><h3 id="pro-levels-t">{esc(C["levels"]["title"])}</h3></div>
        <div class="pp-levels__row">
{levels}
        </div>
        {pricing_note(c, "pp-note d-rv")}
      </section></div>
      <section class="pp-sec pp-wrap" id="pro-samples" aria-labelledby="pro-samples-t">
        <div class="pp-sec__head d-rv"><p class="pp-kicker">{esc(C["samples"]["eyebrow"])}</p><h3 id="pro-samples-t">{esc(C["samples"]["title"])}</h3><p>{esc(C["samples"]["lead"])}</p></div>
        <div class="pp-samples">
{samples}
        </div>
      </section>
      <div class="pp-band pp-band--gate"><section class="pp-sec pp-wrap" id="pro-included" aria-labelledby="pro-included-t">
        <div class="pp-sec__head d-rv"><p class="pp-kicker">{esc(I["eyebrow"])}</p><h3 id="pro-included-t">{esc(I["title"])}</h3></div>
        <div class="pp-incl">
          <div><p class="pp-sub2 d-rv">{esc(I["every"])}</p><ul class="pp-feat">{feat}</ul></div>
          <aside class="pp-extras d-rv" style="--d:.1s" aria-labelledby="pro-extras-t">
            <p class="pp-kicker">{esc(I["extras_tag"])}</p>
            <h4 id="pro-extras-t">{esc(I["extras_title"])}</h4>
            <p>{esc(I["extras_sub"])}</p>
            <ul>{extras}</ul>
            {email_btn(c, "", I["extras_button"], I["extras_subject"])}
          </aside>
        </div>
      </section></div>
      <section class="pp-sec pp-wrap" id="pro-process" aria-labelledby="pro-process-t">
        <div class="pp-sec__head d-rv"><p class="pp-kicker">{esc(C["process"]["eyebrow"])}</p><h3 id="pro-process-t">{esc(C["process"]["title"])}</h3><p>{esc(C["process"]["lead"])}</p></div>
        <ol class="pp-steps">{steps}</ol>
        {process_notes(c, "pp-note d-rv")}
      </section>
      <div class="pp-band pp-band--path"><section class="pp-sec pp-wrap" id="pro-questions" aria-labelledby="pro-questions-t">
        <div class="pp-faq__layout">
          <div class="pp-sec__head d-rv"><p class="pp-kicker">{esc(C["faq"]["eyebrow"])}</p><h3 id="pro-questions-t">{esc(C["faq"]["title"])}</h3></div>
          <div class="pp-faq__list d-rv" style="--d:.08s">{faq}</div>
        </div>
      </section></div>
      <section class="pp-contact" id="pro-contact" aria-labelledby="pro-contact-t">
        <div class="pp-contact__bg" aria-hidden="true"></div>
        <div class="pp-wrap d-rv">
          <p class="pp-kicker">{esc(K["eyebrow"])}</p>
          <h3 class="pp-big" id="pro-contact-t">{esc(K["title"])}</h3>
          <p class="pp-sub">{esc(C["cta"])}</p>
          <div class="pp-contact__row">{email_btn(c, "d-btn--lg")}<div class="pp-copyrow">{copyrow(c)}</div></div>
          <p class="pp-sub">{contact_privacy(c)}</p>
        </div>
      </section>
      {foot(c, "pp")}
    </div>"""


PAGES = {"standard": standard, "pro": pro}


def colours(site, on):
    """the Forest theme of the site, as the variables the two pages use"""
    t = site["theme"]
    return (f"--d-bg:{t['bg']};--d-ink:{t['ink']};--d-brand:{t['brand']};--d-acc:{t['accent']};--d-on:{on(t['brand'], '#FFFFFF', t['ink'])};"
            "--d-mute:#44504A;--d-line:rgba(10,15,12,.14);--d-mint:#D6F1E2;--d-mint2:#EAF6EF")


def shell(site, key, name, vars_, inner, others):
    V, adv = site["copy"]["viewer"], site.get("mode") == "advertise-only"
    label = fmt(V["label"], tier=name)
    tabs = []
    for k, n in TIERS:
        if k == "premium":
            tabs.append(f'<a href="#top" data-premium>{esc(n)}</a>')
        else:
            tabs.append(f'<a href="#demo-{k}"{" aria-current=" + chr(34) + "true" + chr(34) if k == key else ""}>{esc(n)}</a>')
    L = site["copy"]["levels"]
    nxt = "".join(
        (f'<a class="demo__next" href="#top" data-premium>{esc(L["see_premium"])} <span aria-hidden="true">→</span></a>' if k == "premium"
         else f'<a class="demo__next" href="#demo-{k}">{esc(fmt(L["see_demo"], tier=n))} <span aria-hidden="true">→</span></a>') for k, n in others)
    from urllib.parse import quote
    price = fmt(V["end_price"], price=site["prices"][key], tag=site["price_tag"][key])
    return f"""
<section class="demo" id="demo-{key}" role="dialog" aria-modal="true" aria-label="{esc(label)}" style="{vars_}">
  <div class="demo__bar">
    <p class="demo__label"><strong>{esc(label)}</strong><span>{esc(fmt(V["sub"], tier=name))}</span></p>
    <nav class="demo__tabs" aria-label="{esc(V["tabs_aria"])}">{"".join(tabs)}</nav>
    <a class="demo__close" href="#levels" data-demo-close>{esc(V["close"])}</a>
  </div>
  <div class="demo__scroll" data-demo-scroll tabindex="-1">
{inner}
    <div class="demo__end">
      <div class="demo__end-in">
        <p class="demo__end-t">{esc(fmt(V["end_title"], tier=name))}</p>
        <p class="demo__end-p">{esc(price)}</p>
        <div class="demo__end-a">
          <a class="btn" href="mailto:{site["email"]}?subject={quote(fmt(V["end_subject"], tier=name), safe="")}">{esc(V["end_mail"])}</a>
          {nxt}
          <a class="demo__own" href="{key}/">{esc(V["own_page"])}</a>
        </div>
      </div>
    </div>
  </div>
</section>"""


def build(site, on):
    """the viewer sections that sit in the main page"""
    base = colours(site, on)
    return "\n".join([
        shell(site, "standard", "Standard", base, standard(Ctx("standard", True, site)), [("pro", "Pro"), ("premium", "Premium")]),
        shell(site, "pro", "Pro", base, pro(Ctx("pro", True, site)), [("standard", "Standard"), ("premium", "Premium")]),
    ])


def page(site, on, key):
    """the same page on its own (standard/index.html, pro/index.html): the markup, and the variables to set on its frame"""
    return PAGES[key](Ctx(key, False, site)), colours(site, on)
