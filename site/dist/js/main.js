/* Prime Solutions: small, dependency-free enhancements.
   Everything on the page is readable without this file. */
(() => {
  const doc = document;
  const root = doc.documentElement;
  root.classList.add('js');

  const $ = (s, c = doc) => c.querySelector(s);
  const $$ = (s, c = doc) => Array.from(c.querySelectorAll(s));
  const clamp = (n, a, b) => Math.min(b, Math.max(a, n));
  const reduce = matchMedia('(prefers-reduced-motion: reduce)');

  const header = $('[data-header]');
  const levels = $('#levels');
  const ladder = $('[data-ladder]');
  const stage = $('.ladder__stage');
  const steps = $$('.step');
  const pills = $$('.pill');
  const timeline = $('[data-timeline]');
  const sections = $$('[data-section]');
  const navLinks = $$('.nav a[data-nav]');
  const toneEls = $$('[data-tone]').filter((el) => el.dataset.tone);

  /* ---------- mobile menu (burger) ---------- */
  const menuBtn = $('.burger');
  const nav = $('#nav-panel');
  const setMenu = (open) => {
    nav.classList.toggle('is-open', open);
    header.classList.toggle('menu-open', open);
    menuBtn.setAttribute('aria-expanded', String(open));
    menuBtn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    doc.body.style.overflow = open ? 'hidden' : '';
    if (open) { const first = $('a', nav); if (first) first.focus(); }
  };
  if (menuBtn && nav) {
    menuBtn.addEventListener('click', () => setMenu(menuBtn.getAttribute('aria-expanded') !== 'true'));
    nav.addEventListener('click', (e) => { if (e.target.closest('a')) setMenu(false); });
    doc.addEventListener('keydown', (e) => { if (e.key === 'Escape') setMenu(false); });
  }

  /* ---------- the invisible header: its text turns white or ink to suit what is behind it ---------- */
  let tone = '';
  const BAND = { stage: '#0A0F0C', ink: '#0A0F0C', light: '#FFFFFF' };
  const updateTone = () => {
    let t = 'stage';
    for (const el of toneEls) {
      const r = el.getBoundingClientRect();
      if (r.top <= 38 && r.bottom > 38) t = el.dataset.tone;
    }
    if (t === tone) return;
    tone = t;
    header.dataset.tone = t;
    root.style.setProperty('--band', BAND[t] || BAND.light);
  };

  /* ---------- level preview: the same sample page moves up a level, and the section changes colour with it ---------- */
  const demoBtn = $('[data-demo-open]');
  const demoLabel = $('[data-demo-label]');
  const demoNote = $('.stage__note');
  const TIER_NAME = { standard: 'Standard', pro: 'Pro', premium: 'Premium' };
  const setTier = (tier) => {
    if (!ladder || ladder.dataset.tier === tier) return;
    ladder.dataset.tier = tier;
    const prem = tier === 'premium';
    if (demoBtn) demoBtn.setAttribute('href', prem ? '#top' : '#demo-' + tier);
    if (demoLabel) demoLabel.textContent = prem ? 'Back to the entrance' : 'Open the ' + TIER_NAME[tier] + ' demo';
    if (demoNote) demoNote.textContent = prem ? 'You are on a Premium page now.' : 'Sample page. Opens full screen.';
    if (levels) levels.dataset.tier = tier;
    pills.forEach((p) => p.setAttribute('aria-pressed', String(p.dataset.tier === tier)));
    steps.forEach((s) => s.classList.toggle('is-active', s.dataset.step === tier));
  };
  const updateLadder = () => {
    if (!ladder) return;
    const wide = innerWidth >= 900;
    const sb = stage.getBoundingClientRect().bottom;
    const line = wide ? innerHeight * 0.5 : sb + (innerHeight - sb) * 0.4;
    let best = steps[0], bestD = Infinity;
    steps.forEach((s) => {
      const r = s.getBoundingClientRect();
      const d = Math.abs((r.top + r.bottom) / 2 - line);
      if (d < bestD) { bestD = d; best = s; }
    });
    setTier(best.dataset.step);
  };
  pills.forEach((p) => p.addEventListener('click', () => {
    const step = steps.find((s) => s.dataset.step === p.dataset.tier);
    setTier(p.dataset.tier);
    if (!step) return;
    const wide = innerWidth >= 900;
    const r = step.getBoundingClientRect();
    const sb = stage.getBoundingClientRect().bottom;
    const top = wide ? r.top + scrollY - (innerHeight - r.height) / 2 : r.top + scrollY - sb - 6;
    scrollTo({ top, behavior: reduce.matches ? 'auto' : 'smooth' });
  }));

  /* ---------- scroll loop ---------- */
  let ticking = false;
  const update = () => {
    ticking = false;
    const y = scrollY;
    updateTone();

    updateLadder();

    if (timeline) {
      const r = timeline.getBoundingClientRect();
      timeline.style.setProperty('--p', clamp((innerHeight * 0.72 - r.top) / r.height, 0, 1).toFixed(3));
    }

    let current = null;
    sections.forEach((s) => { if (s.getBoundingClientRect().top <= innerHeight * 0.4) current = s.id; });
    navLinks.forEach((a) => a.classList.toggle('is-active', a.dataset.nav === current));
  };
  const onScroll = () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } };
  addEventListener('scroll', onScroll, { passive: true });
  let resizeTimer;
  const onResize = () => { clearTimeout(resizeTimer); resizeTimer = setTimeout(() => { rail && rail.rebuild(); onScroll(); }, 120); };
  addEventListener('resize', onResize);
  reduce.addEventListener('change', onScroll);

  /* ---------- reveal on scroll ---------- */
  const reveals = $$('.reveal');
  if (reduce.matches || !('IntersectionObserver' in window)) {
    reveals.forEach((el) => el.classList.add('in'));
  } else {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
    reveals.forEach((el) => io.observe(el));
  }

  /* ---------- the endless sample strip ----------
     The samples sit in a track that is repeated on both sides. The position (phase) wraps around one
     set, so the strip never ends and never jumps. It drifts on its own. Whichever way you push it
     (drag, swipe, arrows, sideways wheel, arrow keys) it carries on drifting that way. */
  const rail = (() => {
    const el = $('[data-rail-el]');
    if (!el) return null;
    const originals = $$('.sample', el);
    if (!originals.length) return null;

    const track = doc.createElement('div');
    track.className = 'samples__track';
    originals.forEach((o) => track.appendChild(o));
    el.appendChild(track);
    el.classList.add('is-loop');
    el.removeAttribute('tabindex');

    const SPEED = 38;           // px per second, drifting
    const toggleBtn = $('[data-rail-toggle]');
    let k = 1, P = 1, railW = 0, phase = 0;
    let v = 0, dir = 1, last = 0, raf = 0, target = null;
    let paused = reduce.matches, hovering = false, focused = false, dragging = false, visible = true;

    const wrap = (n) => ((n % P) + P) % P;
    const render = () => { track.style.transform = `translate3d(${(-(k * P + phase)).toFixed(2)}px,0,0)`; };

    const clone = (n) => {
      const c = n.cloneNode(true);
      c.removeAttribute('tabindex');
      c.setAttribute('aria-hidden', 'true');
      c.classList.add('is-clone');
      return c;
    };
    const rebuild = () => {
      $$('.is-clone', track).forEach((n) => n.remove());
      railW = el.clientWidth;
      const gap = parseFloat(getComputedStyle(track).columnGap) || 0;
      const first = originals[0], lastEl = originals[originals.length - 1];
      P = Math.max(1, lastEl.offsetLeft + lastEl.offsetWidth + gap - first.offsetLeft);
      k = Math.max(1, Math.ceil(railW / P));
      const before = doc.createDocumentFragment(), after = doc.createDocumentFragment();
      for (let i = 0; i < k; i++) originals.forEach((o) => { before.appendChild(clone(o)); after.appendChild(clone(o)); });
      track.insertBefore(before, originals[0]);
      track.appendChild(after);
      phase = wrap(phase);
      render();
    };

    const needs = () => visible && (dragging || target !== null || Math.abs(v) > 0.05 || !(paused || focused));
    const frame = (t) => {
      raf = 0;
      const dt = Math.min(0.05, (t - last) / 1000 || 0);
      last = t;
      if (!dragging) {
        if (target !== null) {
          let d = target - phase;
          d -= P * Math.round(d / P);
          if (Math.abs(d) < 0.5) { phase = wrap(target); target = null; }
          else phase = wrap(phase + d * (1 - Math.exp(-dt * 8)));
          v = 0;
        } else {
          const stopped = paused || focused;
          const goal = stopped ? 0 : dir * SPEED * (hovering ? 0.3 : 1);   // over the strip it slows, but keeps its direction
          v += (goal - v) * (1 - Math.exp(-dt * (stopped ? 5 : 2.2)));
          phase = wrap(phase + v * dt);
        }
        render();
      }
      if (needs()) raf = requestAnimationFrame(frame);
      else if (!dragging && target === null && (paused || focused)) v = 0;
    };
    const kick = () => {
      if (raf || !visible) return;
      last = performance.now();
      raf = requestAnimationFrame(frame);
    };

    const setPaused = (p) => {
      paused = p;
      if (toggleBtn) toggleBtn.textContent = p ? 'Play' : 'Pause';
      kick();
    };
    if (toggleBtn) {
      toggleBtn.textContent = paused ? 'Play' : 'Pause';
      toggleBtn.addEventListener('click', () => setPaused(!paused));
    }

    /* arrows: a push that carries on in that direction */
    const push = (d) => {
      dir = d;
      target = null;
      if (reduce.matches) {
        const step = originals[0].offsetWidth + 18;
        phase = wrap(phase + d * step);
        render();
        return;
      }
      v = clamp(v + d * 520, -900, 900);
      kick();
    };
    $$('[data-rail]').forEach((b) => b.addEventListener('click', () => push(Number(b.dataset.rail))));

    /* drag or swipe, with a flick that carries on */
    let pid = null, startX = 0, startPhase = 0, lastX = 0, lastT = 0, vx = 0;
    el.addEventListener('pointerdown', (e) => {
      if (e.pointerType === 'mouse' && e.button !== 0) return;
      dragging = true; pid = e.pointerId;
      startX = lastX = e.clientX; startPhase = phase; lastT = e.timeStamp; vx = 0; target = null;
      try { el.setPointerCapture(pid); } catch (err) { /* ignore */ }
      el.classList.add('is-dragging');
      kick();
    });
    el.addEventListener('pointermove', (e) => {
      if (!dragging || e.pointerId !== pid) return;
      phase = wrap(startPhase - (e.clientX - startX));
      const dt = (e.timeStamp - lastT) / 1000;
      if (dt > 0) vx = vx * 0.6 + (-(e.clientX - lastX) / dt) * 0.4;
      lastX = e.clientX; lastT = e.timeStamp;
      render();
    });
    const endDrag = (e) => {
      if (!dragging || (e.pointerId !== undefined && e.pointerId !== pid)) return;
      dragging = false;
      el.classList.remove('is-dragging');
      try { el.releasePointerCapture(pid); } catch (err) { /* ignore */ }
      if (e.timeStamp - lastT > 90) vx = 0;
      if (reduce.matches) { v = 0; return; }
      v = clamp(vx, -2200, 2200);
      if (Math.abs(v) > 60) dir = Math.sign(v);
      kick();
    };
    el.addEventListener('pointerup', endDrag);
    el.addEventListener('pointercancel', endDrag);

    /* sideways wheel or trackpad swipe */
    el.addEventListener('wheel', (e) => {
      if (Math.abs(e.deltaX) <= Math.abs(e.deltaY)) return;
      e.preventDefault();
      phase = wrap(phase + e.deltaX);
      dir = Math.sign(e.deltaX) || dir;
      target = null;
      render();
      kick();
    }, { passive: false });

    /* mouse over the strip slows it (it still carries on the same way) so a sample can be looked at */
    el.addEventListener('pointerenter', (e) => { if (e.pointerType === 'mouse') { hovering = true; kick(); } });
    el.addEventListener('pointerleave', (e) => { if (e.pointerType === 'mouse') { hovering = false; kick(); } });

    /* keyboard: a sample in focus is brought to the middle and the drift waits */
    const phaseFor = (n) => n.offsetLeft - k * P + n.offsetWidth / 2 - railW / 2;
    track.addEventListener('focusin', (e) => {
      const s = e.target.closest('.sample');
      if (!s || s.classList.contains('is-clone') || !s.matches(':focus-visible')) return;
      focused = true;
      if (reduce.matches) { phase = wrap(phaseFor(s)); render(); } else { target = wrap(phaseFor(s)); }
      kick();
    });
    track.addEventListener('focusout', () => { focused = false; kick(); });
    el.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowRight') { e.preventDefault(); push(1); }
      if (e.key === 'ArrowLeft') { e.preventDefault(); push(-1); }
    });
    el.addEventListener('scroll', () => { if (el.scrollLeft) el.scrollLeft = 0; });

    /* only run while the strip is on screen */
    if ('IntersectionObserver' in window) {
      new IntersectionObserver((entries) => {
        visible = entries[entries.length - 1].isIntersecting;
        if (visible) kick();
      }).observe(el);
    }

    rebuild();
    kick();
    return { rebuild: () => { if (!dragging) rebuild(); }, kick };
  })();

  /* ---------- copy the email address ---------- */
  const copyBtn = $('[data-copy]');
  const status = $('[data-copy-status]');
  if (copyBtn) {
    copyBtn.addEventListener('click', async () => {
      let ok = false;
      try { await navigator.clipboard.writeText(copyBtn.dataset.copy); ok = true; } catch (err) {
        const el = $('#addr');
        const range = doc.createRange();
        range.selectNodeContents(el);
        const sel = getSelection();
        sel.removeAllRanges();
        sel.addRange(range);
      }
      status.textContent = ok ? 'Address copied.' : 'Address selected. Copy it from your keyboard or menu.';
      copyBtn.textContent = ok ? 'Copied' : 'Selected';
      setTimeout(() => { copyBtn.textContent = 'Copy address'; }, 2200);
    });
  }

  /* ---------- the Standard and Pro pages: #demo-standard, #demo-pro ----------
     They open full screen over the site (the Premium level is this page itself). The address (hash) says which one is
     open, so the back button closes them, a shared link opens them, and without this script the same links still work (:target). */
  (() => {
    const list = $$('.demo');
    if (!list.length) return;
    let openEl = null, opener = null, depth = 0, scroller = null, io = null;

    const idNow = () => { const m = /^#demo-(standard|pro)$/.exec(location.hash); return m ? 'demo-' + m[1] : ''; };

    const teardown = () => {
      if (!openEl) return;
      if (io) io.disconnect();
      io = null; scroller = null;
      openEl.classList.remove('is-open');
      openEl = null;
    };

    const open = (el) => {
      const fresh = !openEl;
      if (fresh) opener = doc.activeElement && doc.activeElement !== doc.body ? doc.activeElement : null;
      teardown();
      openEl = el;
      el.classList.add('is-open');
      root.classList.add('demo-open');
      scroller = $('[data-demo-scroll]', el);
      scroller.scrollTop = 0;
      scroller.focus({ preventScroll: true });

      const rv = $$('.d-rv', el);
      rv.forEach((n) => n.classList.remove('in'));
      if (reduce.matches || !('IntersectionObserver' in window)) rv.forEach((n) => n.classList.add('in'));
      else {
        io = new IntersectionObserver((entries) => {
          entries.forEach((en) => { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
        }, { root: scroller, threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
        rv.forEach((n) => io.observe(n));
      }
    };

    const close = () => {
      if (depth > 0) history.back(); else location.replace('#levels');
    };

    const sync = (fromEvent) => {
      const id = idNow();
      const el = id ? doc.getElementById(id) : null;
      if (el === openEl) return;
      if (el) {
        depth = fromEvent && !openEl ? 1 : (openEl ? depth : 0);
        open(el);
      } else {
        depth = 0;
        const back = opener;
        teardown();
        root.classList.remove('demo-open');
        if (back && back.focus) { try { back.focus({ preventScroll: true }); } catch (err) { /* ignore */ } }
        opener = null;
      }
    };
    addEventListener('hashchange', () => sync(true));

    const copyAddress = async (btn) => {
      let ok = false;
      try { await navigator.clipboard.writeText(btn.dataset.copyDemo); ok = true; } catch (err) {
        const el = btn.parentNode.querySelector('.d-addr');
        if (el) { const r = doc.createRange(); r.selectNodeContents(el); const sel = getSelection(); sel.removeAllRanges(); sel.addRange(r); }
      }
      btn.textContent = ok ? 'Copied' : 'Selected';
      setTimeout(() => { btn.textContent = 'Copy address'; }, 2200);
    };

    doc.addEventListener('click', (e) => {
      const t = e.target;
      if (!t.closest || !openEl) return;
      const plain = e.metaKey || e.ctrlKey || e.shiftKey;
      const closeLink = t.closest('[data-demo-close]');
      if (closeLink) { e.preventDefault(); close(); return; }
      const copy = t.closest('[data-copy-demo]');
      if (copy) { copyAddress(copy); return; }
      const jump = t.closest('[data-goto]');
      if (jump && !plain) {
        e.preventDefault();
        const to = doc.getElementById(jump.dataset.goto);
        if (to) to.scrollIntoView({ behavior: reduce.matches ? 'auto' : 'smooth', block: 'start' });
        return;
      }
      const prem = t.closest('[data-premium]');
      if (prem && !plain) { e.preventDefault(); location.replace('#top'); return; }
      const a = t.closest('.demo a[href^="#demo-"]');
      if (a && !plain) { e.preventDefault(); location.replace(a.getAttribute('href')); }
    });

    doc.addEventListener('keydown', (e) => {
      if (!openEl) return;
      if (e.key === 'Escape') { e.preventDefault(); close(); return; }
      if (e.key !== 'Tab') return;
      const f = $$('a[href], button:not([disabled]), summary, [tabindex]:not([tabindex="-1"])', openEl).filter((n) => n.getClientRects().length);
      if (!f.length) return;
      const first = f[0], last = f[f.length - 1];
      if (e.shiftKey && (doc.activeElement === first || doc.activeElement === scroller)) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && doc.activeElement === last) { e.preventDefault(); first.focus(); }
    });

    sync(false);
  })();

  update();
  if (doc.fonts && doc.fonts.ready) doc.fonts.ready.then(() => { update(); if (rail) rail.rebuild(); });
})();
