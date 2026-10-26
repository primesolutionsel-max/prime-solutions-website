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
  const finePointer = matchMedia('(hover: hover) and (pointer: fine)');

  const header = $('[data-header]');
  const hero = $('[data-hero]');
  const heroInner = $('[data-hero-inner]');
  const glows = $$('.hero__glow');
  const levels = $('#levels');
  const ladder = $('[data-ladder]');
  const stage = $('.ladder__stage');
  const steps = $$('.step');
  const pills = $$('.pill');
  const timeline = $('[data-timeline]');
  const sections = $$('[data-section]');
  const navLinks = $$('.nav a[data-nav]');

  /* ---------- mobile menu ---------- */
  const menuBtn = $('.menu-btn');
  const nav = $('#nav-panel');
  const setMenu = (open) => {
    nav.classList.toggle('is-open', open);
    menuBtn.setAttribute('aria-expanded', String(open));
    $('.menu-btn__label').textContent = open ? 'Close' : 'Menu';
  };
  menuBtn.addEventListener('click', () => setMenu(menuBtn.getAttribute('aria-expanded') !== 'true'));
  nav.addEventListener('click', (e) => { if (e.target.closest('a')) setMenu(false); });
  doc.addEventListener('keydown', (e) => { if (e.key === 'Escape') setMenu(false); });

  /* ---------- hero pinning: only when the hero fits the screen ---------- */
  const measurePin = () => {
    const fits = innerWidth >= 900 && hero.offsetHeight <= innerHeight && !reduce.matches;
    hero.toggleAttribute('data-pin', fits);
  };

  /* ---------- level preview: the same sample page moves up a level, and the section changes colour with it ---------- */
  const setTier = (tier) => {
    if (!ladder || ladder.dataset.tier === tier) return;
    ladder.dataset.tier = tier;
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
    const max = root.scrollHeight - innerHeight;
    header.style.setProperty('--p', max > 0 ? (y / max).toFixed(4) : '0');
    header.classList.toggle('is-stuck', y > 8);

    if (!reduce.matches && hero) {
      const p = clamp(y / Math.max(1, hero.offsetHeight), 0, 1);
      if (y <= hero.offsetHeight) {
        heroInner.style.transform = `translate3d(0, ${(p * -26).toFixed(1)}px, 0) scale(${(1 - p * 0.05).toFixed(4)})`;
        heroInner.style.opacity = (1 - p * 0.85).toFixed(3);
        glows.forEach((g) => { g.style.transform = `translate3d(0, ${(y * Number(g.dataset.depth)).toFixed(1)}px, 0)`; });
      }
    }

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
  const onResize = () => { clearTimeout(resizeTimer); resizeTimer = setTimeout(() => { measurePin(); rail && rail.rebuild(); onScroll(); }, 120); };
  addEventListener('resize', onResize);
  reduce.addEventListener('change', () => { measurePin(); onScroll(); });

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

  /* ---------- hero: the sample page tilts toward the mouse ---------- */
  const hframe = $('[data-hframe]');
  if (hero && hframe && finePointer.matches && !reduce.matches) {
    let raf = 0, nx = 0, ny = 0;
    const apply = () => {
      raf = 0;
      hframe.style.setProperty('--ry', (-5 + nx * 5).toFixed(2) + 'deg');
      hframe.style.setProperty('--rx', (2.5 - ny * 4).toFixed(2) + 'deg');
      hframe.style.setProperty('--gx', (nx * 16).toFixed(1) + 'px');
      hframe.style.setProperty('--gy', (ny * 12).toFixed(1) + 'px');
    };
    hero.addEventListener('pointermove', (e) => {
      const r = hero.getBoundingClientRect();
      nx = clamp(((e.clientX - r.left) / r.width) * 2 - 1, -1, 1);
      ny = clamp(((e.clientY - r.top) / r.height) * 2 - 1, -1, 1);
      if (!raf) raf = requestAnimationFrame(apply);
    });
    hero.addEventListener('pointerleave', () => { nx = 0; ny = 0; apply(); });
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

  measurePin();
  update();
  if (doc.fonts && doc.fonts.ready) doc.fonts.ready.then(() => { measurePin(); update(); if (rail) rail.rebuild(); });
})();
