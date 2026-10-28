/* Prime Solutions: the entrance.
   The page opens on the arch of the portal, held still. One swipe, scroll, key press or tap and the rest plays by itself: the camera walks
   into the door, through the light and out into the valley. Nothing is left half done, and once you are inside there is no way back to the
   arch (scrolling up only brings you back to the top of the valley). Then the headline opens and a short scroll carries the plans in.
   Plain JS, no libraries. Only transform and opacity are animated, so the page stays smooth on phones. */
(() => {
  'use strict';

  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
  const sm = (a, b, x) => { x = clamp((x - a) / (b - a)); return x * x * (3 - 2 * x); };

  const stage = $('[data-stage]');
  if (!stage) return;
  const root = document.documentElement;
  const rm = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fine = matchMedia('(hover: hover) and (pointer: fine)').matches;
  const phone = matchMedia('(max-width: 700px)').matches;
  if (rm) root.classList.add('rm');

  const pin = $('[data-pin]');
  const scene = $('[data-scene]');
  const beyond = $('[data-beyond]');
  const far = $('[data-far]');
  const arch = $('[data-arch]');
  const bloom = $('[data-bloom]');
  const shade = $('[data-shade]');
  const cue = $('[data-cue]');
  const side = $('[data-side]');
  const skip = $('[data-skip]');
  const copy = $('.copy', stage);
  const canvas = $('[data-motes]');

  /* ---------- tiny writers: only touch the page when a value really changed ---------- */
  const put = (el, k, v) => { const c = el._c || (el._c = {}); if (c[k] === v) return false; c[k] = v; return true; };
  const op = (el, o, keep) => {
    let v = o < 0.004 ? 0 : o > 0.996 ? 1 : Math.round(o * 1000) / 1000;
    if (keep && v < keep) v = keep;                       // a warm layer: invisible, but already painted
    if (put(el, 'o', v)) el.style.opacity = v;
    const vis = v > 0.002 ? 'visible' : 'hidden';
    if (put(el, 'v', vis)) el.style.visibility = vis;
  };
  const tf = (el, s) => { if (put(el, 't', s)) el.style.transform = s; };

  /* ---------- measuring ---------- */
  let vw = innerWidth, vh = innerHeight, sceneW = 1, panMax = 0, stageTop = 0, W = 1, doorX = 0, doorY = 0;
  function measure() {
    vw = innerWidth; vh = pin.offsetHeight || innerHeight;
    sceneW = scene.offsetWidth;
    const sceneH = scene.offsetHeight;
    panMax = Math.max(0, (sceneW - vw) / 2 - 14);
    W = Math.max(1, stage.offsetHeight - vh);              // the short scroll that carries the valley away (the stage height is set in styles.css)
    stageTop = stage.getBoundingClientRect().top + scrollY;
    // where the door sits on screen: the layers scale around it
    doorX = vw / 2 + (0.5006 - 0.5) * sceneW;
    doorY = vh / 2 + (0.525 - 0.5) * sceneH;
    // phones: how far the valley drifts sideways on its own once you are inside (never further than the picture allows)
    pin.style.setProperty('--drift', Math.max(0, Math.min(panMax * 0.6, sceneW * 0.08)).toFixed(0) + 'px');
    pin.style.setProperty('--dx', doorX.toFixed(1) + 'px');
    pin.style.setProperty('--dy', doorY.toFixed(1) + 'px');
  }

  /* ---------- state ---------- */
  let door = 0;                    // 0 closed, 1 open. Moves with time, not with scroll.
  let anim = null;                 // { from, t0, dur }: the door opening
  let entered = false;             // set by the first swipe; there is no way back
  let ws = 0, wT = 0;              // valley progress (scroll), smoothed and target
  let mx = 0, my = 0, tx = 0, ty = 0, near = 0, nearT = 0;
  let raf = 0, last = 0, isOpen = false, lockTimer = 0, pending = null;

  const OPEN_MS = phone ? 2900 : 3200;
  const S2 = 7;                    // how close the arch gets before the light takes over

  function readScroll() { wT = clamp((scrollY - stageTop) / W); }

  /* ---------- the gate: until the door has opened the page is held still and the first gesture opens it ---------- */
  const stopEv = (e) => { if (e.cancelable) e.preventDefault(); };
  let touchY = null;
  const onWheel = (e) => { stopEv(e); if (!entered && e.deltaY > 1) enter(); };
  const onTouchStart = (e) => { touchY = e.touches.length === 1 ? e.touches[0].clientY : null; };
  const onTouchMove = (e) => {
    stopEv(e);
    if (!entered && touchY !== null && e.touches.length && touchY - e.touches[0].clientY > 12) { touchY = null; enter(); }   // a swipe up
  };
  const onKey = (e) => {
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    const k = e.key;
    const onControl = e.target.closest && e.target.closest('a, button, input, select, textarea, summary');
    if (k === 'ArrowDown' || k === 'PageDown' || k === 'End' || ((k === ' ' || k === 'Spacebar') && !onControl)) { stopEv(e); if (!entered) enter(); }
    else if (k === 'ArrowUp' || k === 'PageUp' || k === 'Home') stopEv(e);
  };
  let gated = false;
  function gate(on) {
    if (on === gated) return;
    gated = on;
    root.classList.toggle('gate', on);
    const m = on ? addEventListener : removeEventListener;
    m.call(window, 'wheel', onWheel, { passive: false });
    m.call(window, 'touchstart', onTouchStart, { passive: true });
    m.call(window, 'touchmove', onTouchMove, { passive: false });
    m.call(window, 'keydown', onKey);
  }
  pin.addEventListener('click', (e) => {                    // a tap or click on the picture goes in too
    if (entered || (e.target.closest && e.target.closest('a, button'))) return;
    enter();
  });

  function syncOpen() {
    const want = door >= 0.62;
    if (want !== isOpen) { isOpen = want; stage.classList.toggle('is-open', want); }
    const st = anim ? 'opening' : (door >= 1 ? 'open' : 'closed');
    if (put(stage, 'st', st)) stage.dataset.state = st;
  }

  function finish() {
    anim = null; door = 1;
    clearTimeout(lockTimer);
    gate(false);
    syncOpen(); readScroll(); ws = wT; render(); kick();
    if (pending) { const f = pending; pending = null; f(); }
  }

  function enter(o = {}) {
    if (entered) return;
    entered = true;
    if (o.instant || rm) { finish(); return; }
    const dur = o.dur || OPEN_MS;
    anim = { from: door, t0: performance.now(), dur };
    clearTimeout(lockTimer);
    lockTimer = setTimeout(() => { if (anim) finish(); }, dur + 900);   // never leave the page stuck
    syncOpen();
    kick();
  }

  /* ---------- the whole film ---------- */
  function render() {
    // the camera walks at the door: starts moving at once, speeds up into the light
    const u = clamp(door / 0.6);
    const sN = Math.exp(Math.log(S2) * (u * (0.35 + 0.65 * u)));
    const sF = Math.pow(sN, 0.36);                           // mountains move slower than the arch: that is the depth
    const closed = door > 0 ? 0 : 1;
    const px = mx * closed, py = my * closed;

    tf(arch, `translate3d(${(-px * 11).toFixed(1)}px,${(-py * 7).toFixed(1)}px,0) scale(${sN.toFixed(3)})`);
    op(arch, 1 - sm(0.5, 0.62, door));
    tf(far, `translate3d(${(-px * 4).toFixed(1)}px,${(-py * 2.5).toFixed(1)}px,0) scale(${sF.toFixed(3)})`);
    op(far, 1 - sm(0.3, 0.52, door));

    // the light. Before the door opens the pointer coaxes it: the nearer you are to the doorway the more it glows.
    const tz = 1 - sm(0, 0.16, door);
    const bo = Math.max(sm(0.16, 0.44, door) * (1 - sm(0.6, 0.92, door)), near * 0.6 * tz);
    const bs = 0.05 + 15 * Math.pow(sm(0.16, 0.7, door), 1.6) + 0.55 * near * tz;
    tf(bloom, `scale(${bs.toFixed(3)})`);
    op(bloom, bo);

    // the valley: comes out of the light, settles, then drifts a little while you scroll
    const out = 1 - Math.pow(1 - sm(0.5, 1, door), 3);
    // wider screens: the camera eases in and slides a little while you scroll. Phones: the valley stays put (it only drifts sideways by
    // itself, see .scene in styles.css), so scrolling down goes straight on to the plans.
    const sB = 1.26 - 0.26 * out + (phone ? 0 : 0.07 * ws);
    const fx = phone ? 0.5 : 0.5 - 0.16 * sm(0.04, 0.4, ws) + 0.42 * sm(0.5, 0.95, ws);
    const pan = clamp((0.5 - fx) * sceneW, -panMax, panMax);
    const bp = sm(0.5, 0.7, door) * (1 - ws);                // inside, the valley leans a little towards the pointer
    tf(beyond, `translate3d(${(-mx * 14 * bp + pan).toFixed(1)}px,${(-my * 8 * bp).toFixed(1)}px,0) scale(${sB.toFixed(3)})`);
    op(beyond, sm(0.5, 0.66, door), 0.003);

    // words
    op(side, 1 - sm(0, 0.22, door));
    tf(side, `translateX(${(-18 * sm(0, 0.22, door)).toFixed(1)}px)`);
    op(cue, 1 - sm(0, 0.1, door));
    op(skip, 1 - sm(0, 0.2, door));
    op(copy, sm(0.55, 0.65, door) * (1 - sm(0.12, 0.62, ws)));   // the headline lifts away within a short scroll, so the next sheet is never far
    tf(copy, `translate3d(0,${(-ws * 36).toFixed(1)}px,0)`);
    op(shade, Math.max(1 - sm(0.1, 0.45, door), sm(0.55, 0.7, door)));

    motes.vis = Math.max(0.22 * closed, 0.36 * sm(0.6, 0.78, door));
    motes.kick();
  }

  /* a still frame: reduced motion, or the scene before any script has run */
  function renderStatic() {
    entered = true; door = 1;
    arch.style.display = 'none'; far.style.display = 'none';
    beyond.style.cssText += ';opacity:1;visibility:visible;transform:scale(1.03)';
    copy.style.cssText += ';opacity:1;visibility:visible';
    stage.classList.add('is-open');
    shade.style.opacity = 1;
  }

  /* ---------- floating motes: a few emerald sparks, only while visible ---------- */
  const motes = (() => {
    const o = { vis: 0, kick() { if (!on && o.vis > 0.02 && visible && !rm) { on = true; lastT = 0; requestAnimationFrame(loop); } } };
    const ctx = canvas.getContext('2d');
    const dpr = Math.min(devicePixelRatio || 1, 1.5);
    const N = phone ? 14 : 34;
    const list = [];
    let W2 = 0, H2 = 0, on = false, visible = true, lastT = 0;
    const sprite = document.createElement('canvas'); sprite.width = sprite.height = 48;
    const sc = sprite.getContext('2d');
    const gr = sc.createRadialGradient(24, 24, 0, 24, 24, 24);
    gr.addColorStop(0, 'rgba(220,255,235,1)'); gr.addColorStop(0.25, 'rgba(90,240,160,.8)'); gr.addColorStop(1, 'rgba(31,174,108,0)');
    sc.fillStyle = gr; sc.fillRect(0, 0, 48, 48);
    for (let i = 0; i < N; i++) list.push({ x: Math.random(), y: Math.random(), s: 5 + Math.random() * 13, v: 0.012 + Math.random() * 0.03, a: 0.3 + Math.random() * 0.6, ph: Math.random() * 6.28, sw: 0.01 + Math.random() * 0.02 });
    const size = () => { W2 = canvas.width = Math.round(pin.clientWidth * dpr); H2 = canvas.height = Math.round(pin.clientHeight * dpr); };
    function loop(t) {
      if (!visible || o.vis < 0.02) { on = false; ctx.clearRect(0, 0, W2, H2); return; }
      const dt = Math.min(0.05, (t - lastT) / 1000 || 0.033);
      if (lastT && t - lastT < 30) { requestAnimationFrame(loop); return; }   // about 30 frames a second is plenty for sparks
      lastT = t;
      ctx.clearRect(0, 0, W2, H2);
      for (const m of list) {
        m.y -= m.v * dt; m.ph += dt * 0.8;
        if (m.y < -0.05) { m.y = 1.05; m.x = Math.random(); }
        ctx.globalAlpha = m.a * o.vis * (0.6 + 0.4 * Math.sin(m.ph * 2));
        const s = m.s * dpr;
        ctx.drawImage(sprite, (m.x + Math.sin(m.ph) * m.sw) * W2 - s / 2, m.y * H2 - s / 2, s, s);
      }
      requestAnimationFrame(loop);
    }
    size(); addEventListener('resize', size);
    new IntersectionObserver((e) => { visible = e[0].isIntersecting; stage.classList.toggle('is-away', !visible); if (visible) o.kick(); }).observe(stage);
    document.addEventListener('visibilitychange', () => { visible = !document.hidden; if (visible) o.kick(); });
    return o;
  })();

  /* ---------- frame loop: runs only while something is moving ---------- */
  function tick(t) {
    raf = 0;
    const dt = Math.min(0.05, (t - last) / 1000 || 0.016); last = t;
    if (anim) {
      const u = clamp((t - anim.t0) / anim.dur);
      door = anim.from + (1 - anim.from) * u;
      syncOpen();
      if (u >= 1) { finish(); return; }
    }
    const k = 1 - Math.exp(-dt * 8);
    ws += (wT - ws) * k; if (Math.abs(wT - ws) < 0.0005) ws = wT;
    const km = 1 - Math.exp(-dt * 5);
    mx += (tx - mx) * km; my += (ty - my) * km;
    near += (nearT - near) * (1 - Math.exp(-dt * 6)); if (Math.abs(nearT - near) < 0.004) near = nearT;
    render();
    if (anim || ws !== wT || Math.abs(tx - mx) > 0.002 || Math.abs(ty - my) > 0.002 || near !== nearT) raf = requestAnimationFrame(tick);
  }
  function kick() { if (!raf) { last = performance.now(); raf = requestAnimationFrame(tick); } }

  /* ---------- scroll ---------- */
  function onScroll() {
    if (!entered) { if (scrollY > 4) enter({ instant: true }); return; }   // something scrolled the page (a link, the back button, a restored position): you are in
    readScroll();
    kick();
  }

  /* ---------- links inside the page ---------- */
  const HEAD = 76;
  const known = ['top', 'main', 'levels', 'samples', 'included', 'process', 'questions', 'contact'];
  function goto(y) {
    const go = () => scrollTo({ top: y, behavior: rm ? 'auto' : 'smooth' });
    if (entered && !anim) { go(); return; }
    if (!entered && y < 4) return;                           // "top" at the arch: nothing to do
    pending = go;
    enter({ dur: 1000 });                                    // a link past the door: through it, quickly, then on to the part
  }
  document.addEventListener('click', (e) => {
    const a = e.target.closest && e.target.closest('a[href^="#"]');
    // (a link inside a demo is the demo's own business; a viewer that has already stopped the browser's default action does not stop this)
    if (!a || e.metaKey || e.ctrlKey || e.shiftKey || e.button || a.closest('.demo')) return;
    const id = a.getAttribute('href').slice(1);
    if (!known.includes(id) && id !== '') return;            // anything else (like the privacy section or a sample page) is left to the browser
    if (location.hash === '#privacy') return;
    const el = id && id !== 'top' ? document.getElementById(id) : null;
    const y = el ? el.getBoundingClientRect().top + scrollY - HEAD : 0;
    e.preventDefault();
    goto(Math.max(0, y));
  });
  skip.addEventListener('click', () => {
    const el = document.getElementById('levels');
    const y = el ? el.getBoundingClientRect().top + scrollY - HEAD : stageTop + W;
    enter({ instant: true });
    scrollTo({ top: Math.max(0, y), behavior: rm ? 'auto' : 'smooth' });
  });

  /* ---------- go ---------- */
  measure();
  if (rm) {
    renderStatic();
  } else {
    const h = location.hash;
    entered = scrollY > 4 || (!!h && h !== '#' && h !== '#top');      // opened with a part of the page in the address, or at a restored position: already inside
    if (entered) door = 1; else gate(true);
    readScroll(); ws = wT;
    syncOpen();
    render();
    addEventListener('scroll', onScroll, { passive: true });
    if (fine) {
      addEventListener('pointermove', (e) => {
        if (stage.classList.contains('is-away') || (entered && !anim && ws >= 0.98)) return;
        tx = (e.clientX / innerWidth - 0.5) * 2; ty = (e.clientY / innerHeight - 0.5) * 2;
        if (!entered) nearT = Math.pow(clamp(1 - Math.hypot(e.clientX - doorX, (e.clientY - doorY) * 0.55) / (0.34 * Math.min(vw, vh * 1.5))), 1.4);
        kick();
      }, { passive: true });
      document.documentElement.addEventListener('mouseleave', () => { tx = ty = 0; nearT = 0; kick(); });
    }
    // have the valley decoded and painted before the door opens, so the crossfade never hitches
    $$('.layer img').forEach((img) => { if (img.decode) img.decode().catch(() => {}); });
  }
  let rt = 0;
  addEventListener('resize', () => {
    clearTimeout(rt);
    rt = setTimeout(() => { measure(); if (!rm) { readScroll(); kick(); } }, 100);
  });
  addEventListener('load', () => { measure(); if (!rm) { readScroll(); kick(); } });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => { measure(); if (!rm) { readScroll(); kick(); } });
})();
