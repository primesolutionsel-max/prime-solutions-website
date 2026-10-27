"""The Standard and Pro versions of the Prime Solutions site.

Premium is the page itself (the entrance, the valley, the sheets). These two are the same one-page site built
at the other two levels: the same sections, the same words, the same prices. Only the treatment changes.

Two ways of showing them, from the same markup:
  viewer      full-screen sections on the main page (#demo-standard, #demo-pro), opened from the Three levels section
  standalone  their own pages, standard.html and pro.html (written by build.py)

The styling is in src/css/tiers.css, the pictures are set by build.py (photo_css). No forms, no invented reviews or figures.
The earlier plumber sample pages are kept in archive/.
"""

TIERS = [("standard", "Standard"), ("pro", "Pro"), ("premium", "Premium")]
PRE = {"standard": "std", "pro": "pro"}

LEVELS = [
    ("standard", "Standard", "Clean and finished.", ["One typeface", "Calm, tidy layout", "Everything on one page"]),
    ("pro", "Pro", "Photo-led and layered.", ["Everything in Standard", "Second typeface", "Photo-led opening", "Layered blocks, scroll reveals", "Header that follows you down"]),
    ("premium", "Premium", "Crafted and striking.", ["Everything in Pro", "Large editorial type", "Depth and layered surfaces", "Choreographed section transitions", "A signature detail for your trade"]),
]
NAV = [("levels", "Levels"), ("samples", "Samples"), ("included", "What you get"), ("process", "How it works"), ("questions", "Questions")]
FEATURES = [
    ("devices", "A finished one-page site, tested from 375 to 1280 px"),
    ("mail", "An email button as the main contact"),
    ("type", "A text logo, or your own"),
    ("palette", "One colour theme to suit you"),
    ("search", "Search-ready title, description and preview image"),
    ("bolt", "Light pages that load fast"),
    ("code", "The full code, handed over to you"),
]
EXTRAS = [("form", "Contact forms"), ("cal", "Booking"), ("bag", "An online shop"), ("lock", "Logins"), ("pin", "Maps"), ("play", "Embedded video"), ("grid", "Photo galleries")]
STEPS = [
    ("Tell us about your business", "Email your business name, trade and the look you like."),
    ("See a demo first", "A concept before we build. If it is not right, we try another."),
    ("We build your site", "You get a preview."),
    ("You approve it", "Tell us what to adjust."),
    ("Hand-over", "The whole site goes to you. The domain and hosting are yours."),
    ("Fixes later, quoted per job", "Need a change? We quote it, fix it, send it back."),
]
FAQ = [
    ("Is there a monthly fee?", "No. One fee. Domain and hosting costs go to your providers."),
    ("Who owns the website?", "You do. After hand-over we keep no connection to it."),
    ("Can I see it before I decide?", "Yes. A demo first, then a preview."),
    ("What if something breaks later?", "Tell us. We quote the fix."),
    ("Can you add a form, bookings or a shop?", "Yes, as extras quoted per business."),
    ("What if I have no logo?", "We set your name as a text logo."),
    ("Do I have to send photos?", "No. Send what you have."),
    ("Which languages?", "English only, for now."),
]
ALT = {
    "plumbing": "Copper pipes, fittings and wrenches on a workbench",
    "salon": "A bright salon station with a mirror, a chair and plants",
    "cafe": "A coffee machine and a cup of coffee on a café counter",
    "garage": "A car on a lift in a tidy workshop",
    "cleaning": "A basket of cleaning supplies and folded cloths in a living room",
    "firm": "A tidy office desk with law books and a notebook",
}
PORTAL_ALT = "An ancient mossy stone arch with a glowing green portal, in a misty valley"

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


class Ctx:
    """where the page is shown decides what its links do"""

    def __init__(self, key, viewer, site):
        self.key, self.viewer, self.pre = key, viewer, PRE[key]
        self.email, self.prices, self.year = site["email"], site["prices"], site["year"]
        self.samples = site["samples"]

    def jump(self, sid):
        """a link that scrolls inside this page"""
        if self.viewer:
            return f'href="#demo-{self.key}" data-goto="{self.pre}-{sid}"'
        return f'href="#{self.pre}-{sid}"'

    def tier(self, kind):
        """a link to one of the three levels"""
        if kind == "premium":
            return 'href="#top" data-premium' if self.viewer else 'href="index.html"'
        return f'href="#demo-{kind}"' if self.viewer else f'href="{kind}.html"'

    def mail(self, subject=""):
        return f'href="mailto:{self.email}' + (f'?subject={subject}' if subject else "") + '"'

    def privacy(self):
        return 'href="privacy.html"'


def email_btn(c, cls="", label="Email us", subject=""):
    return f'<a class="d-btn {cls}" {c.mail(subject)}>{label}</a>'


def copyrow(c, cls=""):
    return (f'<span class="d-addr">{c.email}</span>'
            f'<button class="d-copy" type="button" data-copy-demo="{c.email}">Copy address</button>')


def tier_tail(c, key, name):
    """the bottom of a level card: 'This page', or a way to open that level"""
    if key == c.key:
        return '<span class="ps-here">This page</span>'
    label = "See it at Premium" if key == "premium" else f"See the {name} demo"
    return f'<a class="d-link" {c.tier(key)}>{label} <span aria-hidden="true">→</span></a>'


def level_card(c, key, name, title, ticks, cls, kick):
    ticks_html = "".join(f"<li>{t}</li>" for t in ticks)
    here = " is-here" if key == c.key else ""
    return (f'<article class="{cls}{here}">\n'
            f'  <p class="{kick}">{name}</p>\n  <h4>{title}</h4>\n  <ul class="ps-ticks">{ticks_html}</ul>\n'
            f'  <p class="ps-price"><strong>{c.prices[key]}</strong><span>once-off</span></p>\n  {tier_tail(c, key, name)}\n</article>')


# ---------------------------------------------------------------- Standard: one typeface, flat and calm, one picture, a gentle fade on opening
def standard(c):
    nav = "".join(f'<a {c.jump(i)}>{t}</a>' for i, t in NAV)
    levels = "\n".join(level_card(c, k, n, t, tk, "ps-level", "ps-tag") for k, n, t, tk in LEVELS)
    samples = "\n".join(
        f'<figure class="ps-sample"><div class="ps-sample__pic ph ph-{s["photo"]}" role="img" aria-label="{ALT[s["photo"]]}"></div>'
        f'<figcaption><strong>{s["trade"]}</strong><span>{s["theme"]} theme</span></figcaption></figure>' for s in c.samples)
    feat = "".join(f'<li><span class="ps-ic">{ic(i)}</span><span>{t}</span></li>' for i, t in FEATURES)
    extras = "".join(f"<li>{ic(i)}{t}</li>" for i, t in EXTRAS)
    steps = "".join(f'<li><span class="n" aria-hidden="true">{n}</span><h4>{t}</h4><p>{p}</p></li>' for n, (t, p) in enumerate(STEPS, 1))
    faq = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in FAQ)
    return f"""
    <div class="d d--standard" id="std-top">
      <header class="ps-head"><div class="ps-wrap">
        <a class="ps-logo" {c.jump("top")} aria-label="Prime Solutions, back to the top">Prime <span>Solutions</span></a>
        <nav aria-label="This page">{nav}</nav>
        {email_btn(c)}
      </div></header>
      <section class="ps-hero ps-wrap" aria-labelledby="std-hero-t">
        <div class="ps-hero__copy">
          <p class="ps-eyebrow">One-page websites</p>
          <h2 id="std-hero-t"><span>Built once.</span><span>Built well.</span><span>Yours to keep.</span></h2>
          <p class="ps-lead">For small businesses in South Africa and beyond.</p>
          <div class="ps-cta">{email_btn(c, "d-btn--lg")}<a class="d-link" {c.jump("levels")}>See the three levels</a></div>
        </div>
        <div class="ps-photo ph-hills" role="img" aria-label="Green hills in morning mist, with the sun coming up"></div>
      </section>
      <section class="ps-block ps-wrap" id="std-levels" aria-labelledby="std-levels-t">
        <div class="ps-block__head"><p class="ps-eyebrow">The three levels</p><h3 id="std-levels-t">Three levels.</h3><p>The same page, three ways.</p></div>
        <div class="ps-levels">
{levels}
        </div>
        <p class="ps-note">Prices are a guide. Your quote confirms them.</p>
      </section>
      <section class="ps-block ps-wrap" id="std-samples" aria-labelledby="std-samples-t">
        <div class="ps-block__head"><p class="ps-eyebrow">Samples</p><h3 id="std-samples-t">What yours could look like.</h3><p>Six trades, six themes. Samples, not client sites.</p></div>
        <div class="ps-samples">
{samples}
        </div>
      </section>
      <section class="ps-block ps-wrap" id="std-included" aria-labelledby="std-included-t">
        <div class="ps-block__head"><p class="ps-eyebrow">What you get</p><h3 id="std-included-t">What is included.</h3></div>
        <div class="ps-incl">
          <div><p class="ps-sub">In every level</p><ul class="ps-feat">{feat}</ul></div>
          <aside class="ps-extras" aria-labelledby="std-extras-t">
            <p class="ps-sub">Add to any level</p>
            <h4 id="std-extras-t">Extras, quoted per business</h4>
            <p>Priced per business.</p>
            <ul>{extras}</ul>
            {email_btn(c, "", "Ask about an extra", "Extras")}
          </aside>
        </div>
      </section>
      <section class="ps-block ps-wrap" id="std-process" aria-labelledby="std-process-t">
        <div class="ps-block__head"><p class="ps-eyebrow">How it works</p><h3 id="std-process-t">From first email to hand-over.</h3><p>Six steps. You see it before it is yours.</p></div>
        <ol class="ps-steps">{steps}</ol>
      </section>
      <section class="ps-block ps-wrap" id="std-questions" aria-labelledby="std-questions-t">
        <div class="ps-block__head"><p class="ps-eyebrow">Common questions</p><h3 id="std-questions-t">Questions we hear first.</h3></div>
        <div class="ps-faq">{faq}</div>
      </section>
      <section class="ps-contact" id="std-contact" aria-labelledby="std-contact-t">
        <div class="ps-wrap ps-contact__in">
          <div class="ps-contact__txt">
            <p class="ps-eyebrow" style="color:inherit">Start here</p>
            <h3 id="std-contact-t">Tell us about your business.</h3>
            <p class="ps-lead">Email us. We reply with a demo.</p>
            {email_btn(c, "d-btn--lg")}
          </div>
          <div class="ps-card">{copyrow(c)}<span>Prices in rand.</span></div>
        </div>
      </section>
      <footer class="ps-foot ps-wrap"><span>© {c.year} Prime Solutions · <a {c.privacy()}>Privacy policy</a></span><a {c.jump("top")}>Back to the top</a></footer>
    </div>"""


# ---------------------------------------------------------------- Pro: two typefaces, the portal with only the swirl turning, layered blocks, reveals, a header that follows you down
def pro(c):
    nav = "".join(f'<a {c.jump(i)}>{t}</a>' for i, t in NAV)
    levels = "\n".join(level_card(c, k, n, t, tk, "pp-level d-rv", "pp-kicker").replace('class="pp-level d-rv', f'style="--d:{i * .1:.1f}s" class="pp-level d-rv', 1)
                       for i, (k, n, t, tk) in enumerate(LEVELS))
    samples = "\n".join(
        f'<figure class="pp-sample d-rv" style="--d:{(i % 3) * .1:.1f}s"><div class="pp-pic ph ph-{s["photo"]}" role="img" aria-label="{ALT[s["photo"]]}"></div>'
        f'<figcaption><strong>{s["trade"]}</strong><span>{s["theme"]} theme</span></figcaption></figure>' for i, s in enumerate(c.samples))
    feat = "".join(f'<li class="d-rv" style="--d:{(i % 2) * .08:.2f}s"><span class="pp-ic">{ic(n)}</span><span>{t}</span></li>' for i, (n, t) in enumerate(FEATURES))
    extras = "".join(f"<li>{ic(i)}{t}</li>" for i, t in EXTRAS)
    steps = "".join(f'<li class="d-rv" style="--d:{(n - 1) % 3 * .1:.1f}s"><span class="n" aria-hidden="true">{n:02d}</span><h4>{t}</h4><p>{p}</p></li>' for n, (t, p) in enumerate(STEPS, 1))
    faq = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in FAQ)
    return f"""
    <div class="d d--pro" id="pro-top">
      <header class="pp-head"><div class="pp-wrap">
        <a class="pp-logo" {c.jump("top")} aria-label="Prime Solutions, back to the top">Prime <span>Solutions</span></a>
        <nav aria-label="This page">{nav}</nav>
        {email_btn(c)}
      </div></header>
      <section class="pp-hero" aria-labelledby="pro-hero-t">
        <div class="pp-hero__pic" role="img" aria-label="{PORTAL_ALT}"><div class="pp-scene"><i class="pp-door" aria-hidden="true"></i></div></div>
        <div class="pp-wrap pp-hero__in">
          <div class="pp-hero__copy d-rv">
            <p class="pp-kicker">One-page websites</p>
            <h2 id="pro-hero-t"><span>Built once.</span><span>Built well.</span><span>Yours to keep.</span></h2>
            <p class="pp-sub">For small businesses in South Africa and beyond.</p>
            <div class="pp-cta">{email_btn(c, "d-btn--light d-btn--lg")}<a class="d-link" {c.jump("levels")}>See the three levels</a></div>
          </div>
        </div>
      </section>
      <section class="pp-levels pp-wrap" id="pro-levels" aria-labelledby="pro-levels-t">
        <div class="pp-levels__head d-rv"><p class="pp-kicker">The same page, three ways</p><h3 id="pro-levels-t">Three levels.</h3></div>
        <div class="pp-levels__row">
{levels}
        </div>
      </section>
      <section class="pp-sec pp-wrap" id="pro-samples" aria-labelledby="pro-samples-t">
        <div class="pp-sec__head d-rv"><p class="pp-kicker">Samples</p><h3 id="pro-samples-t">What yours could look like.</h3><p>Six trades, six themes. Samples, not client sites.</p></div>
        <div class="pp-samples">
{samples}
        </div>
      </section>
      <section class="pp-sec pp-wrap" id="pro-included" aria-labelledby="pro-included-t">
        <div class="pp-sec__head d-rv"><p class="pp-kicker">What you get</p><h3 id="pro-included-t">What is included.</h3></div>
        <div class="pp-incl">
          <div><p class="pp-sub2 d-rv">In every level</p><ul class="pp-feat">{feat}</ul></div>
          <aside class="pp-extras d-rv" style="--d:.1s" aria-labelledby="pro-extras-t">
            <p class="pp-kicker">Add to any level</p>
            <h4 id="pro-extras-t">Extras, quoted per business</h4>
            <p>Priced per business.</p>
            <ul>{extras}</ul>
            {email_btn(c, "", "Ask about an extra", "Extras")}
          </aside>
        </div>
      </section>
      <section class="pp-sec pp-wrap" id="pro-process" aria-labelledby="pro-process-t">
        <div class="pp-sec__head d-rv"><p class="pp-kicker">How it works</p><h3 id="pro-process-t">From first email to hand-over.</h3><p>Six steps. You see it before it is yours.</p></div>
        <ol class="pp-steps">{steps}</ol>
      </section>
      <section class="pp-sec pp-wrap" id="pro-questions" aria-labelledby="pro-questions-t">
        <div class="pp-faq__layout">
          <div class="pp-sec__head d-rv"><p class="pp-kicker">Common questions</p><h3 id="pro-questions-t">Questions we hear first.</h3></div>
          <div class="pp-faq__list d-rv" style="--d:.08s">{faq}</div>
        </div>
      </section>
      <section class="pp-contact" id="pro-contact" aria-labelledby="pro-contact-t">
        <div class="pp-contact__bg" aria-hidden="true"></div>
        <div class="pp-wrap d-rv">
          <p class="pp-kicker">Start here</p>
          <h3 class="pp-big" id="pro-contact-t">Tell us about your business.</h3>
          <p class="pp-sub">Email us. We reply with a demo.</p>
          <div class="pp-contact__row">{email_btn(c, "d-btn--lg")}<div class="pp-copyrow">{copyrow(c)}</div></div>
          <p class="pp-sub">Prices in rand.</p>
        </div>
      </section>
      <footer class="pp-foot pp-wrap"><span>© {c.year} Prime Solutions · <a {c.privacy()}>Privacy policy</a></span><a {c.jump("top")}>Back to the top</a></footer>
    </div>"""


PAGES = {"standard": standard, "pro": pro}


def colours(site, on):
    """the Forest theme of the site, as the variables the two pages use"""
    t = site["theme"]
    return (f"--d-bg:{t['bg']};--d-ink:{t['ink']};--d-brand:{t['brand']};--d-acc:{t['accent']};--d-on:{on(t['brand'], '#FFFFFF', t['ink'])};"
            "--d-mute:#44504A;--d-line:rgba(10,15,12,.14);--d-mint:#D6F1E2;--d-mint2:#EAF6EF")


def shell(key, label, vars_, inner, price, email, others):
    tabs = []
    for k, n in TIERS:
        if k == "premium":
            tabs.append(f'<a href="#top" data-premium>{n}</a>')
        else:
            tabs.append(f'<a href="#demo-{k}"{" aria-current=" + chr(34) + "true" + chr(34) if k == key else ""}>{n}</a>')
    nxt = "".join(
        (f'<a class="demo__next" href="#top" data-premium>See it at Premium <span aria-hidden="true">→</span></a>' if k == "premium"
         else f'<a class="demo__next" href="#demo-{k}">See the {n} demo <span aria-hidden="true">→</span></a>') for k, n in others)
    return f"""
<section class="demo" id="demo-{key}" role="dialog" aria-modal="true" aria-label="{label} demo" style="{vars_}">
  <div class="demo__bar">
    <p class="demo__label"><strong>{label} demo</strong><span>This site, built at {label} level.</span></p>
    <nav class="demo__tabs" aria-label="Choose a level">{"".join(tabs)}</nav>
    <a class="demo__close" href="#levels" data-demo-close>Close</a>
  </div>
  <div class="demo__scroll" data-demo-scroll tabindex="-1">
{inner}
    <div class="demo__end">
      <div class="demo__end-in">
        <p class="demo__end-t">This was the {label} level.</p>
        <p class="demo__end-p">{price}, once-off.</p>
        <div class="demo__end-a">
          <a class="btn" href="mailto:{email}?subject={label}%20level">Email us</a>
          {nxt}
        </div>
      </div>
    </div>
  </div>
</section>"""


def build(site, on):
    """the viewer sections that sit in the main page"""
    base = colours(site, on)
    prices, email = site["prices"], site["email"]
    return "\n".join([
        shell("standard", "Standard", base, standard(Ctx("standard", True, site)), prices["standard"], email, [("pro", "Pro"), ("premium", "Premium")]),
        shell("pro", "Pro", base, pro(Ctx("pro", True, site)), prices["pro"], email, [("standard", "Standard"), ("premium", "Premium")]),
    ])


def page(site, on, key):
    """the same page on its own (standard.html, pro.html): the markup, and the variables to set on its frame"""
    return PAGES[key](Ctx(key, False, site)), colours(site, on)
