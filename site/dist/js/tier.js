/* Prime Solutions: the Standard and Pro pages on their own (standard/index.html, pro/index.html).
   Everything is readable without this file; it only adds the fade-ins and the copy button. */
(() => {
  const doc = document;
  const $$ = (s, c = doc) => Array.from(c.querySelectorAll(s));
  const reduce = matchMedia('(prefers-reduced-motion: reduce)');
  /* the words come from site.json, through the #ui-copy block that build.py writes into the page */
  const UI = (() => { try { return JSON.parse(doc.getElementById('ui-copy').textContent); } catch (err) { return {}; } })();
  const setText = (el, key) => { if (el && UI[key]) el.textContent = UI[key]; };

  const rv = $$('.d-rv');
  if (reduce.matches || !('IntersectionObserver' in window)) rv.forEach((n) => n.classList.add('in'));
  else {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
    rv.forEach((n) => io.observe(n));
  }

  /* Pro: the header is clear over the dark opening and becomes a soft off-white veil once the opening is behind it;
     the link of the part you are reading is underlined. Without this the header simply stays the soft veil. */
  const head = doc.querySelector('.pp-head'), hero = doc.querySelector('.pp-hero');
  if (head && hero && 'IntersectionObserver' in window) {
    head.classList.add('on-hero');
    new IntersectionObserver(([en]) => head.classList.toggle('on-hero', en.isIntersecting), { rootMargin: '-72px 0px 0px 0px' }).observe(hero);
    const links = $$('.pp-head a[href^="#"]'), key = (a) => a.dataset.goto || (a.getAttribute('href') || '').slice(1);
    const spy = new IntersectionObserver((entries) => entries.forEach((en) => {
      if (en.isIntersecting) links.forEach((a) => (key(a) === en.target.id ? a.setAttribute('aria-current', 'true') : a.removeAttribute('aria-current')));
    }), { rootMargin: '-40% 0px -55% 0px' });
    $$('.pp-head nav a').map((a) => doc.getElementById(key(a))).filter(Boolean).forEach((n) => spy.observe(n));
  }

  /* the phone menu is a plain <details>: close it after a tap on a link, or on Escape */
  $$('.ps-menu').forEach((m) => {
    m.addEventListener('click', (e) => { if (e.target.closest && e.target.closest('.ps-menu__panel a')) m.removeAttribute('open'); });
    doc.addEventListener('keydown', (e) => { if (e.key === 'Escape' && m.open) { m.removeAttribute('open'); m.querySelector('summary').focus(); } });
  });

  $$('[data-copy-demo]').forEach((btn) => btn.addEventListener('click', async () => {
    let ok = false;
    try { await navigator.clipboard.writeText(btn.dataset.copyDemo); ok = true; } catch (err) {
      const el = btn.parentNode.querySelector('.d-addr');
      if (el) { const r = doc.createRange(); r.selectNodeContents(el); const s = getSelection(); s.removeAllRanges(); s.addRange(r); }
    }
    setText(btn, ok ? 'copied' : 'selected');
    setTimeout(() => { setText(btn, 'copy'); }, 2200);
  }));
})();
