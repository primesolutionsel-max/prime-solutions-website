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
