/* Prime Solutions: the Standard and Pro pages on their own (standard.html, pro.html).
   Everything is readable without this file; it only adds the fade-ins and the copy button. */
(() => {
  const doc = document;
  const $$ = (s, c = doc) => Array.from(c.querySelectorAll(s));
  const reduce = matchMedia('(prefers-reduced-motion: reduce)');

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
    btn.textContent = ok ? 'Copied' : 'Selected';
    setTimeout(() => { btn.textContent = 'Copy address'; }, 2200);
  }));
})();
