/* Prime Solutions: the entrance.
   Scrolling zooms towards the door of an arch. Close to the door the page takes over and plays the rest
   by itself (through the light, into the valley), then the headline opens. Scrolling on carries the
   valley from midday through sunset to night, and the plans follow. Scroll back up and the door closes the same way.
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
  const night = $('[data-night]');
  const dusk = $('[data-dusk]');
  const twilight = $('[data-twilight]');
  const shade = $('[data-shade]');
  const sun = $('[data-sun]');
  const sunset = $('[data-sunset]');
  const moon = $('[data-moon]');
  const starsEl = $('[data-stars]');
  const glows = $$('[data-glow]');
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

  /* ---------- stars: fixed positions, in three groups so only three things twinkle ---------- */
  (function stars() {
    let s = 20261027;
    const rnd = () => { s = (s + 0x6D2B79F5) | 0; let t = Math.imul(s ^ (s >>> 15), 1 | s); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
    const groups = [0, 1, 2].map(() => { const g = document.createElement('div'); g.className = 'sg'; starsEl.appendChild(g); return g; });
    const n = phone ? 24 : 54;
    for (let i = 0; i < n; i++) {
      const el = document.createElement('i');
      const size = 1 + rnd() * 1.6;
      el.style.cssText = `left:${(rnd() * 100).toFixed(2)}%;top:${(rnd() * 100).toFixed(2)}%;width:${size.toFixed(1)}px;height:${size.toFixed(1)}px`;
      groups[i % 3].appendChild(el);
    }
  })();

  /* ---------- measuring ---------- */
  let vw = innerWidth, vh = innerHeight, sceneW = 1, panMax = 0, stageTop = 0, A = 1, W = 1, Wm = 1;
  function measure() {
    vw = innerWidth; vh = pin.offsetHeight || innerHeight;
    sceneW = scene.offsetWidth;
    const sceneH = scene.offsetHeight;
    panMax = Math.max(0, (sceneW - vw) / 2 - 14);
    const hold = vh;                                       // extra scroll for the sky cycle (the stage is 100vh taller for it: see .stage in styles.css)
    const run = Math.max(1, stage.offsetHeight - vh);
    const runOld = Math.max(1, run - hold);
    A = runOld * (70 / 150);                               // scroll that zooms to the door
    Wm = runOld - A;                                       // scroll over which the valley itself drifts, as it always did
    W = Wm + hold;                                         // scroll that carries the sky from midday through sunset to night
    stageTop = stage.getBoundingClientRect().top + scrollY;
    // where the door sits on screen: the layers scale around it
    pin.style.setProperty('--dx', (vw / 2 + (0.5006 - 0.5) * sceneW).toFixed(1) + 'px');
    pin.style.setProperty('--dy', (vh / 2 + (0.525 - 0.5) * sceneH).toFixed(1) + 'px');
  }

  /* ---------- state ---------- */
  let door = 0;                    // 0 closed, 1 open. Moves with time, not with scroll.
  let anim = null;                 // { from, to, t0, dur }
  let as = 0, aT = 0;              // approach progress (scroll), smoothed and target
  let ws = 0, wT = 0;              // valley progress (scroll), smoothed and target
  let mx = 0, my = 0, tx = 0, ty = 0;
  let raf = 0, last = 0;
  let isOpen = false;
  let locked = false, lockY = 0, lockTimer = 0, pending = null;
  let jumping = false, jumpTimer = 0;

  const OPEN_MS = phone ? 2300 : 2500;
  const CLOSE_MS = 1500;

  function readScroll() {
    const rel = scrollY - stageTop;
    aT = clamp(rel / A);
    wT = clamp((rel - A) / W);
    return rel;
  }

  /* ---------- holding the page still while the door plays ---------- */
  const stopEv = (e) => { if (e.cancelable) e.preventDefault(); };
  const stopKey = (e) => { if (['ArrowDown', 'ArrowUp', 'PageDown', 'PageUp', 'Home', 'End', ' ', 'Spacebar'].includes(e.key)) stopEv(e); };
  function lock(on) {
    if (on === locked) return;
    locked = on;
    if (on) {
      lockY = scrollY;
      root.classList.add('is-locked');
      addEventListener('wheel', stopEv, { passive: false });
      addEventListener('touchmove', stopEv, { passive: false });
      addEventListener('keydown', stopKey);
    } else {
      root.classList.remove('is-locked');
      removeEventListener('wheel', stopEv);
      removeEventListener('touchmove', stopEv);
      removeEventListener('keydown', stopKey);
      if (Math.abs(scrollY - lockY) > 1) scrollTo({ top: lockY, behavior: 'instant' });
    }
  }

  function syncOpen() {
    const want = door >= 0.62 && (!anim || anim.to === 1);
    if (want !== isOpen) { isOpen = want; stage.classList.toggle('is-open', want); }
    const st = anim ? (anim.to === 1 ? 'opening' : 'closing') : (door >= 1 ? 'open' : 'closed');
    if (put(stage, 'st', st)) stage.dataset.state = st;
  }

  function endAnim() {
    const a = anim; anim = null;
    door = a.to;
    clearTimeout(lockTimer);
    lock(false);
    syncOpen();
    if (pending) { const f = pending; pending = null; f(); }
  }

  function setDoor(to, o = {}) {
    if (o.instant || rm) {
      anim = null; door = to; clearTimeout(lockTimer); lock(false); syncOpen(); kick();
      if (pending) { const f = pending; pending = null; f(); }
      return;
    }
    const dur = o.dur || (to ? OPEN_MS : CLOSE_MS);
    anim = { from: door, to, t0: performance.now(), dur };
    lock(true);
    clearTimeout(lockTimer);
    lockTimer = setTimeout(() => { if (anim) endAnim(); }, dur + 900);   // never leave the page stuck
    syncOpen();
    kick();
  }

  /* ---------- the whole film ---------- */
  const S1 = 3.3;                  // how close scrolling alone gets you to the door
  const S2 = 7;                    // how close the arch gets before the light takes over
  function render() {
    const asE = as + (1 - as) * sm(0, 0.15, door);          // the camera keeps what scrolling did, then carries on
    const zA = asE * (2 - asE);                              // quick to respond, easing to rest at the door
    const zD = sm(0, 0.64, door);
    const sN = Math.exp(Math.log(S1) * zA + Math.log(S2 / S1) * zD);
    const sF = Math.pow(sN, 0.36);                           // mountains move slower than the arch: that is the depth
    const pw = door > 0 ? 0 : 1 - sm(0, 0.5, as);
    const px = mx * pw, py = my * pw;

    tf(arch, `translate3d(${(-px * 11).toFixed(1)}px,${(-py * 7).toFixed(1)}px,0) scale(${sN.toFixed(3)})`);
    op(arch, 1 - sm(0.5, 0.62, door));
    tf(far, `translate3d(${(-px * 4).toFixed(1)}px,${(-py * 2.5).toFixed(1)}px,0) scale(${sF.toFixed(3)})`);
    op(far, 1 - sm(0.3, 0.52, door));

    // the light
    const bo = sm(0.16, 0.44, door) * (1 - sm(0.6, 0.92, door));
    const bs = 0.05 + 15 * Math.pow(sm(0.16, 0.7, door), 1.6);
    tf(bloom, `scale(${bs.toFixed(3)})`);
    op(bloom, bo);

    // the valley: comes out of the light, settles, then drifts while you scroll
    const out = 1 - Math.pow(1 - sm(0.5, 1, door), 3);
    const wm = clamp(ws * W / Wm);                            // the valley's drift keeps its own pace; the sky cycle below uses the whole run
    const sB = 1.26 - 0.26 * out + 0.07 * wm;
    const fx = 0.5 - 0.16 * sm(0.04, 0.4, wm) + 0.42 * sm(0.5, 0.95, wm);   // on a phone the camera slides across the valley
    const pan = clamp((0.5 - fx) * sceneW, -panMax, panMax);
    const bp = sm(0.5, 0.7, door);
    tf(beyond, `translate3d(${(-mx * 9 * bp + pan).toFixed(1)}px,${(-my * 5 * bp).toFixed(1)}px,0) scale(${sB.toFixed(3)})`);
    op(beyond, sm(0.5, 0.66, door), as > 0.25 || door > 0 ? 0.003 : 0);

    // the sky, in distinct stages: midday (bright, the sun high), sunset (warm light, the sun low), twilight, night (moon, stars, glows)
    const dd = sm(0.6, 0.8, door);                           // only once you are inside the valley
    const md = 1 - sm(0.10, 0.38, ws);
    const ss = sm(0.20, 0.42, ws) * (1 - sm(0.56, 0.74, ws)) * dd;
    const tw = sm(0.50, 0.66, ws) * (1 - sm(0.80, 0.96, ws)) * dd;
    const nt = sm(0.64, 0.92, ws) * dd;
    op(sun, md);
    tf(sun, `translate3d(0,${((1 - md) * 9).toFixed(2)}%,0)`);   // the high sun sinks a little as its light fades
    op(sunset, ss);
    tf(sunset, `translate3d(0,${(-5 + 9 * sm(0.2, 0.62, ws)).toFixed(2)}%,0)`);
    op(dusk, ss * 0.92);
    op(twilight, tw);
    op(night, nt);
    op(moon, sm(0.3, 0.9, nt));
    op(starsEl, sm(0.2, 0.85, nt));
    const g = 0.15 + 0.85 * sm(0.15, 1, nt);
    glows.forEach((el) => op(el, g));

    // words
    const closed = door > 0 ? 0 : 1;
    op(side, (1 - sm(0.05, 0.35, as)) * closed);
    tf(side, `translateX(${(-18 * sm(0.05, 0.35, as)).toFixed(1)}px)`);
    op(cue, (1 - sm(0, 0.12, as)) * closed);
    op(skip, 1 - sm(0, 0.2, door));
    op(copy, sm(0.55, 0.65, door) * (1 - sm(0.03, 0.24, wm)));   // the words leave after a short scroll, so the next sheet is never far
    op(shade, Math.max(1 - sm(0.1, 0.5, as), sm(0.55, 0.7, door)));

    motes.vis = Math.max(0.22 * (1 - sm(0, 0.3, as)) * closed, (0.3 + 0.7 * nt) * sm(0.6, 0.78, door));
    motes.kick();
  }

  /* a still frame: reduced motion, or the scene before any script has run */
  function renderStatic() {
    arch.style.display = 'none'; far.style.display = 'none';
    beyond.style.cssText += ';opacity:1;visibility:visible;transform:scale(1.03)';
    glows.forEach((el) => { el.style.opacity = 0.35; });
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
      door = anim.from + (anim.to - anim.from) * u;
      syncOpen();
      if (u >= 1) endAnim();
    }
    const k = 1 - Math.exp(-dt * 8);
    as += (aT - as) * k; if (Math.abs(aT - as) < 0.0005) as = aT;
    ws += (wT - ws) * k; if (Math.abs(wT - ws) < 0.0005) ws = wT;
    const km = 1 - Math.exp(-dt * 5);
    mx += (tx - mx) * km; my += (ty - my) * km;
    render();
    if (anim || as !== aT || ws !== wT || Math.abs(tx - mx) > 0.002 || Math.abs(ty - my) > 0.002) raf = requestAnimationFrame(tick);
  }
  function kick() { if (!raf) { last = performance.now(); raf = requestAnimationFrame(tick); } }

  /* ---------- scroll rules ---------- */
  function onScroll() {
    if (locked) { if (Math.abs(scrollY - lockY) > 2) scrollTo({ top: lockY, behavior: 'instant' }); return; }
    const rel = readScroll();
    if (jumping) { armJump(160); }
    else if (door === 0 && !anim && rel >= A * 0.96) setDoor(1, rel > A + 0.6 * vh ? { instant: true } : {});
    else if (door === 1 && !anim && rel < A - 0.16 * vh) setDoor(0);
    kick();
  }
  function armJump(ms) { clearTimeout(jumpTimer); jumpTimer = setTimeout(endJump, ms); }
  function endJump() {
    jumping = false;
    const rel = readScroll();
    if (!anim) {
      if (door === 1 && rel < A - 0.16 * vh) setDoor(0);                           // arrived back at the top: close the door
      else if (door === 0 && rel >= A * 0.96) setDoor(1, { instant: true });
    }
    kick();
  }

  /* ---------- links inside the page ---------- */
  const HEAD = 76;
  const known = ['top', 'main', 'levels', 'samples', 'included', 'process', 'questions', 'contact'];
  function goto(y) {
    const go = () => { jumping = true; armJump(1500); scrollTo({ top: y, behavior: rm ? 'auto' : 'smooth' }); };
    if (door === 0 && y - stageTop >= A * 0.96) { pending = go; setDoor(1, { dur: 800 }); } else go();
  }
  document.addEventListener('click', (e) => {
    const a = e.target.closest && e.target.closest('a[href^="#"]');
    if (!a || e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey || e.button) return;
    const id = a.getAttribute('href').slice(1);
    if (!known.includes(id) && id !== '') {                  // anything else (like the privacy section) is left to the browser
      jumping = true; armJump(1500); return;
    }
    if (location.hash === '#privacy') { jumping = true; armJump(1500); return; }
    const el = id && id !== 'top' ? document.getElementById(id) : null;
    const y = el ? el.getBoundingClientRect().top + scrollY - HEAD : 0;
    e.preventDefault();
    goto(Math.max(0, y));
  });
  skip.addEventListener('click', () => {
    const el = document.getElementById('levels');
    goto(el ? el.getBoundingClientRect().top + scrollY - HEAD : stageTop + A + W);
  });

  /* ---------- go ---------- */
  measure();
  if (rm) {
    renderStatic();
  } else {
    const rel = readScroll();
    if (rel >= A * 0.96) { door = 1; }
    as = aT; ws = wT;
    syncOpen();
    render();
    addEventListener('scroll', onScroll, { passive: true });
    if (fine) {
      addEventListener('pointermove', (e) => {
        if (door > 0 || anim || locked) return;
        tx = (e.clientX / innerWidth - 0.5) * 2; ty = (e.clientY / innerHeight - 0.5) * 2; kick();
      }, { passive: true });
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
