"""The three demo pages: the same sample business (a plumber) built at Standard, Pro and Premium.

Each one opens full screen from the Three levels section (#demo-standard, #demo-pro, #demo-premium).
The markup is plain HTML, the styling lives in src/css/styles.css under the "demo viewer" heading.
Nothing here is a real business, and there are no reviews, figures or forms.
"""

import math

BIZ = "Your Plumbing Co."
MAIL = "hello@yourplumbing.co.za"
HOURS = "Mon to Sat, 07:00 to 17:00"
PHOTO_ALT = "Copper pipes, fittings and wrenches on a workbench"

TIERS = [("standard", "Standard"), ("pro", "Pro"), ("premium", "Premium")]


def swirl():
    """a water swirl: three tapered arms drawn as plain SVG shapes (it turns slowly behind the Pro header photo)"""
    arms = []
    for k, (col, op) in enumerate([("#F0B36A", .95), ("#7FAEF5", .95), ("#FFFFFF", .5)]):
        n = 60
        pts = []
        for i in range(n + 1):
            t = i / n
            th = t * 2.7 * math.pi + k * 2 * math.pi / 3
            r = 12 + t * 84
            pts.append((r * math.cos(th), r * math.sin(th), 5.2 * (1 - t) + .6))   # x, y, half-width (thick near the middle, thin outside)
        left, right = [], []
        for i, (x, y, w) in enumerate(pts):
            x0, y0, _ = pts[max(i - 1, 0)]
            x1, y1, _ = pts[min(i + 1, n)]
            tx, ty = x1 - x0, y1 - y0
            ln = math.hypot(tx, ty) or 1
            nx, ny = -ty / ln, tx / ln
            left.append(f"{x + nx * w:.1f},{y + ny * w:.1f}")
            right.append(f"{x - nx * w:.1f},{y - ny * w:.1f}")
        arms.append(f'<polygon points="{" ".join(left + right[::-1])}" fill="{col}" opacity="{op}"/>')
    return '<svg viewBox="-100 -100 200 200" focusable="false">' + "".join(arms) + "</svg>"


def btn(label="Email us", cls=""):
    return f'<button class="d-btn {cls}" type="button" data-sample>{label}</button>'


def shell(key, label, vars_, inner, price, email, others):
    cur = ' aria-current="true"'
    tabs = "".join(f'<a href="#demo-{k}"{cur if k == key else ""}>{n}</a>' for k, n in TIERS)
    nxt_html = "".join(
        f'<a class="demo__next" href="#demo-{k}">See the {n} demo <span aria-hidden="true">→</span></a>' for k, n in others
    )
    return f"""
<section class="demo" id="demo-{key}" role="dialog" aria-modal="true" aria-label="{label} demo" style="{vars_}">
  <div class="demo__bar">
    <p class="demo__label"><strong>{label} demo</strong><span>Sample page. Not a real business.</span></p>
    <nav class="demo__tabs" aria-label="Choose a demo">{tabs}</nav>
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
          {nxt_html}
        </div>
      </div>
    </div>
  </div>
  <p class="demo__toast" role="status" aria-live="polite"></p>
</section>"""


# ---------------------------------------------------------------- Standard: one typeface, calm and tidy, one photo, light motion
ICON_DROP = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3c3 4 6 7 6 11a6 6 0 0 1-12 0c0-4 3-7 6-11z"/></svg>'
ICON_WRENCH = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>'
ICON_CAL = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M16 3v4M8 3v4M3 10h18M9 15l2 2 4-4"/></svg>'


def standard():
    return f"""
    <div class="d d--standard">
      <header class="ds-head"><div class="ds-wrap">
        <b class="ds-logo">{BIZ}</b>
        <nav aria-label="Sample page"><span>Services</span><span>How we work</span><span>Contact</span></nav>
        {btn()}
      </div></header>
      <section class="ds-hero ds-wrap">
        <div class="ds-hero__copy">
          <h2>Plumbing you can count on.</h2>
          <p>Repairs, installs and maintenance.</p>
          {btn()}
        </div>
        <div class="ds-photo ph ph-plumbing" role="img" aria-label="{PHOTO_ALT}"></div>
      </section>
      <section class="ds-block ds-wrap">
        <h3>What we do</h3>
        <div class="ds-cols">
          <div><span class="ds-ic">{ICON_DROP}</span><h4>Repairs</h4><p>Leaks, blocked drains and burst pipes.</p></div>
          <div><span class="ds-ic">{ICON_WRENCH}</span><h4>Installs</h4><p>Geysers, taps, toilets and basins.</p></div>
          <div><span class="ds-ic">{ICON_CAL}</span><h4>Maintenance</h4><p>Regular checks that stop problems early.</p></div>
        </div>
      </section>
      <section class="ds-block ds-wrap ds-split">
        <div>
          <h3>How we work</h3>
          <ul class="ds-list">
            <li><b>A quote first.</b> You know the price before we start.</li>
            <li><b>A tidy finish.</b> We clean up when we are done.</li>
            <li><b>Plain advice.</b> No pressure, no jargon.</li>
          </ul>
        </div>
        <div class="ds-photo ds-photo--b ph ph-plumbing" role="img" aria-label="{PHOTO_ALT}"></div>
      </section>
      <section class="ds-contact">
        <div class="ds-wrap ds-contact__in">
          <div class="ds-contact__txt">
            <h3>Need a plumber?</h3>
            <p>Email us the problem and your area.</p>
            {btn("Email us", "d-btn--light")}
          </div>
          <div class="ds-card">
            <p class="ds-addr">{MAIL}</p>
            <p class="ds-hours">{HOURS}</p>
          </div>
        </div>
      </section>
      <footer class="ds-foot ds-wrap"><span>© {BIZ}</span><span>Sample page</span></footer>
    </div>"""


# ---------------------------------------------------------------- Pro: two typefaces, photo-led, layered, reveals, a header that follows
def pro():
    return f"""
    <div class="d d--pro">
      <header class="dp-head"><div class="dp-wrap">
        <b class="dp-logo">{BIZ}</b>
        <nav aria-label="Sample page"><span>Services</span><span>How it works</span><span>Contact</span></nav>
        {btn()}
      </div></header>
      <section class="dp-hero">
        <div class="dp-wrap dp-hero__grid">
          <div class="dp-hero__copy d-rv">
            <p class="dp-kicker">Repairs · Installs · Maintenance</p>
            <h2>Plumbing you can count on.</h2>
            <p class="dp-sub">Fast, tidy and honest work, from a dripping tap to a new geyser.</p>
            <div class="dp-cta">{btn("Email us", "d-btn--light")}<span class="dp-more">See what we do ↓</span></div>
          </div>
          <div class="dp-hero__art d-rv" style="--d:.12s">
            <div class="dp-swirl" aria-hidden="true">{swirl()}</div>
            <div class="dp-photo dp-photo--round ph ph-plumbing" role="img" aria-label="{PHOTO_ALT}"></div>
          </div>
        </div>
      </section>
      <section class="dp-cards dp-wrap">
        <article class="dp-card d-rv"><span class="dp-card__n">01</span><h3>Repairs</h3><p>Leaks, blocked drains and burst pipes, sorted the same week.</p></article>
        <article class="dp-card d-rv" style="--d:.1s"><span class="dp-card__n">02</span><h3>Installs</h3><p>Geysers, taps, toilets and basins, fitted neatly.</p></article>
        <article class="dp-card d-rv" style="--d:.2s"><span class="dp-card__n">03</span><h3>Maintenance</h3><p>Regular checks that stop small problems becoming big ones.</p></article>
      </section>
      <section class="dp-split dp-wrap">
        <div class="dp-split__pic d-rv"><div class="dp-photo ph ph-plumbing" role="img" aria-label="{PHOTO_ALT}"></div><i class="dp-block dp-block--c"></i></div>
        <div class="dp-split__txt d-rv" style="--d:.1s">
          <p class="dp-kicker dp-kicker--dark">How we work</p>
          <h3>Tidy work. Plain quotes.</h3>
          <ul class="dp-ticks">
            <li>A quote before work starts</li>
            <li>We clean up when we are done</li>
            <li>Advice without pressure</li>
          </ul>
        </div>
      </section>
      <section class="dp-steps dp-wrap">
        <h3 class="d-rv">From email to fixed</h3>
        <ol class="dp-steps__row">
          <li class="d-rv"><span>1</span><b>Email us</b><p>The problem and your area.</p></li>
          <li class="d-rv" style="--d:.1s"><span>2</span><b>Get a quote</b><p>Plain, in writing.</p></li>
          <li class="d-rv" style="--d:.2s"><span>3</span><b>We fix it</b><p>And leave it tidy.</p></li>
        </ol>
      </section>
      <section class="dp-band">
        <div class="dp-wrap dp-band__in d-rv">
          <div><h3>Need a plumber?</h3><p>Email us the problem and your area.</p></div>
          {btn("Email us", "d-btn--light")}
        </div>
      </section>
      <footer class="dp-foot dp-wrap"><span>© {BIZ}</span><span>{MAIL} · {HOURS}</span></footer>
    </div>"""


# ---------------------------------------------------------------- Premium: big type, depth, choreographed sections, one signature detail
def premium():
    return f"""
    <div class="d d--premium" data-premium>
      <header class="dm-head"><div class="dm-wrap">
        <b class="dm-logo">{BIZ}</b>
        <nav aria-label="Sample page"><span>Services</span><span>How it works</span><span>Contact</span></nav>
        {btn()}
      </div></header>
      <section class="dm-hero">
        <div class="dm-wrap dm-hero__grid">
          <h2 class="dm-h"><span class="dm-l" style="--i:0">Plumbing</span><span class="dm-l" style="--i:1">you can</span><span class="dm-l dm-l--o" style="--i:2">count on.</span></h2>
          <div class="dm-hero__art" data-par>
            <div class="dm-photo ph ph-plumbing" role="img" aria-label="{PHOTO_ALT}"></div>
            <svg class="dm-seal" viewBox="0 0 100 100" aria-hidden="true"><defs><path id="dm-seal-path" d="M50,50 m-36,0 a36,36 0 1,1 72,0 a36,36 0 1,1 -72,0"/></defs><g class="dm-seal__ring"><text><textPath href="#dm-seal-path" textLength="222" lengthAdjust="spacing">Repairs • Installs • Maintenance •</textPath></text></g><circle cx="50" cy="50" r="6"/></svg>
          </div>
          <div class="dm-hero__foot">
            <p>Repairs, installs and maintenance.</p>
            {btn("Email us")}
          </div>
        </div>
      </section>
      <section class="dm-stack dm-wrap" aria-label="What we do">
        <article class="dm-card dm-card--1" data-card><span class="dm-card__n">01</span><div><h3>Repairs</h3><p>Leaks, blocked drains and burst pipes.</p></div></article>
        <article class="dm-card dm-card--2" data-card><span class="dm-card__n">02</span><div><h3>Installs</h3><p>Geysers, taps, toilets and basins.</p></div></article>
        <article class="dm-card dm-card--3" data-card><span class="dm-card__n">03</span><div><h3>Maintenance</h3><p>Regular checks that stop problems early.</p></div></article>
      </section>
      <section class="dm-steps dm-wrap">
        <h3 class="dm-t d-rv">From email to fixed.</h3>
        <div class="dm-steps__list" data-pipe>
          <i class="dm-pipe" aria-hidden="true"></i>
          <i class="dm-drop" aria-hidden="true"></i>
          <div class="dm-step d-rv"><b>Email us</b><p>The problem and your area.</p></div>
          <div class="dm-step d-rv"><b>Get a quote</b><p>Plain, in writing, before we start.</p></div>
          <div class="dm-step d-rv"><b>We fix it</b><p>And leave it tidy.</p></div>
        </div>
      </section>
      <section class="dm-contact">
        <div class="dm-wrap d-rv">
          <h3 class="dm-big">Need a plumber?</h3>
          <p>Email us the problem and your area.</p>
          {btn("Email us", "d-btn--lg")}
          <p class="dm-addr">{MAIL}<span>{HOURS}</span></p>
        </div>
      </section>
      <footer class="dm-foot dm-wrap"><span>© {BIZ}</span><span>Sample page</span></footer>
    </div>"""


def build(site, on):
    bg, ink, brand, acc = site["themes"]["Harbour"]
    base = f"--d-bg:{bg};--d-ink:{ink};--d-brand:{brand};--d-acc:{acc};--d-on:{on(brand, '#FFFFFF', ink)}"
    email = site["email"]
    prices = site["prices"]
    parts = [
        shell("standard", "Standard", base, standard(), prices["standard"], email, [("pro", "Pro"), ("premium", "Premium")]),
        shell("pro", "Pro", base, pro(), prices["pro"], email, [("standard", "Standard"), ("premium", "Premium")]),
        shell("premium", "Premium", base, premium(), prices["premium"], email, [("standard", "Standard"), ("pro", "Pro")]),
    ]
    return "\n".join(parts)
