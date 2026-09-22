/* ═══════════════════════════════════════════════════════════════
   BABY SHIB — THE BABYVERSE GATE
   One rAF loop. Transform/opacity only. Stale-not-zero data.
   ═══════════════════════════════════════════════════════════════ */
(() => {
  'use strict';

  const MINT = '5nZMRLSFnA3oWXXswKyyaW5or2FFy34tkTUhtkWPpump';
  const API = 'https://api.dexscreener.com/latest/dex/tokens/' + MINT;
  const $ = s => document.querySelector(s);
  const $$ = s => Array.from(document.querySelectorAll(s));
  const root = document.documentElement;
  const REDUCED = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const FLAT = /(?:\?|&)flat=1/.test(location.search);
  if (FLAT) root.classList.add('flat');

  /* ─────────── toast ─────────── */
  const toastEl = $('#toast');
  let toastT;
  const toast = msg => {
    if (!toastEl) return;
    toastEl.textContent = msg;
    toastEl.classList.add('show');
    clearTimeout(toastT);
    toastT = setTimeout(() => toastEl.classList.remove('show'), 2200);
  };

  /* ─────────── scroll: one passive listener, one job ───────────
     The realm is carried by each section's own class, so there is no global
     state to drive and nothing to strand if a frame never runs. */
  const dock = $('#dock');
  let ticking = false;
  const onScroll = () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => {
      ticking = false;
      if (dock) dock.classList.toggle('up', scrollY > innerHeight * 0.75);
    });
  };
  addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ─────────── live data — stale, never zero ─────────── */
  const fmtMoney = n => {
    if (n == null || isNaN(n)) return null;
    if (n >= 1e9) return '$' + (n / 1e9).toFixed(2) + 'B';
    if (n >= 1e6) return '$' + (n / 1e6).toFixed(2) + 'M';
    if (n >= 1e3) return '$' + (n / 1e3).toFixed(1) + 'K';
    return '$' + n.toFixed(0);
  };
  const fmtPrice = p => {
    const n = parseFloat(p);
    if (!n || isNaN(n)) return null;
    if (n >= 1) return '$' + n.toFixed(3);
    const s = n.toFixed(12).replace(/0+$/, '');
    const m = s.match(/^0\.(0*)(\d{1,4})/);
    if (m && m[1].length >= 3) {
      const sub = '₀₁₂₃₄₅₆₇₈₉';
      return '$0.0' + String(m[1].length).split('').map(d => sub[+d]).join('') + m[2];
    }
    return '$' + n.toPrecision(4).replace(/0+$/, '');
  };
  const pct = v => (v == null || isNaN(v)) ? '' : (v >= 0 ? '+' : '') + v.toFixed(1) + '%';

  let last = null, fails = 0;
  const set = (el, v) => { if (el && v != null) el.textContent = v; };

  function paint(p) {
    last = p;
    const mc = p.marketCap || p.fdv;
    set($('#mPrice'), fmtPrice(p.priceUsd));
    set($('#mMcap'), fmtMoney(mc));
    set($('#mLiq'), fmtMoney(p.liquidity && p.liquidity.usd));
    set($('#mVol'), fmtMoney(p.volume && p.volume.h24));
    const ch = p.priceChange && p.priceChange.h24;
    const chEl = $('#mChange');
    if (chEl && ch != null) {
      chEl.textContent = pct(ch) + ' · 24h';
      chEl.className = 'cell__d mono ' + (ch >= 0 ? 'up' : 'down');
    }
    set($('#dockPrice'), fmtPrice(p.priceUsd));
    $('#liveDot')?.classList.remove('stale');
    set($('#liveNote'), 'live from DexScreener · ' + new Date().toLocaleTimeString());
    paintBoss(ch);
  }

  /* THE FINAL BOSS — bidirectional readout, centred at zero */
  function paintBoss(ch) {
    const bar = $('#bossBar'), st = $('#bossState'), box = $('#boss');
    if (!bar || !st || !box) return;
    if (ch == null || isNaN(ch)) {
      box.classList.add('nodata'); st.textContent = 'NO DATA'; bar.style.width = '0';
      return;
    }
    box.classList.remove('nodata');
    /* Bidirectional readout centred at zero: a red day fills to the right of
       centre, a green day drains to the left. Clamped at +-40% so a spike
       cannot overflow the track, with a 2% floor so a flat day is still
       visible rather than looking broken. */
    const capped = Math.max(-40, Math.min(40, ch));
    const mag = Math.max(2, Math.abs(capped) / 40 * 50);
    if (capped < 0) { bar.style.left = '50%'; bar.style.width = mag + '%'; }
    else { bar.style.left = (50 - mag) + '%'; bar.style.width = mag + '%'; }
    bar.style.background = capped < 0
      ? 'linear-gradient(90deg,#8B0000,#FF3B30)'
      : 'linear-gradient(270deg,#1f7a3a,#2BD96B)';
    st.textContent = capped < 0 ? 'The bear ate today.' : 'The bear is losing ground.';
  }

  function refresh() {
    fetch(API, { cache: 'no-store' })
      .then(r => r.json())
      .then(d => {
        const pairs = (d && d.pairs || []).filter(p => p.chainId === 'solana');
        if (!pairs.length) throw new Error('no pairs');
        pairs.sort((a, b) => ((b.liquidity && b.liquidity.usd) || 0) - ((a.liquidity && a.liquidity.usd) || 0));
        fails = 0;
        paint(pairs[0]);
      })
      .catch(() => {
        fails++;
        if (fails >= 2) {
          $('#liveDot')?.classList.add('stale');
          set($('#liveNote'), last ? 'last updated a moment ago · reconnecting' : 'live data unavailable — see DexScreener');
        }
      });
  }
  refresh();
  setInterval(() => { if (!document.hidden) refresh(); }, 30000);
  document.addEventListener('visibilitychange', () => { if (!document.hidden) refresh(); });

  /* ─────────── copy CA ─────────── */
  const ca = $('#ca');
  function copyCA() {
    const text = $('#caText').textContent.trim();
    const done = () => {
      $('#caBtn').textContent = 'COPIED ✓';
      ca.classList.add('copied');
      toast('Contract address copied 🐾');
      setTimeout(() => { $('#caBtn').textContent = 'COPY'; ca.classList.remove('copied'); }, 1400);
    };
    const fallback = () => {
      const t = document.createElement('textarea');
      t.value = text; t.style.cssText = 'position:fixed;opacity:0';
      document.body.appendChild(t); t.select();
      try { document.execCommand('copy'); done(); } catch (e) { toast('Copy failed — select it manually'); }
      document.body.removeChild(t);
    };
    if (navigator.clipboard && isSecureContext) navigator.clipboard.writeText(text).then(done, fallback);
    else fallback();
  }
  ca?.addEventListener('click', copyCA);
  ca?.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); copyCA(); } });

  /* ─────────── mobile wallet path (feature-detect, no UA sniff) ─────────── */
  if (matchMedia('(pointer: coarse)').matches && !window.solana) {
    const line = $('#phantomLine');
    if (line) {
      line.style.display = 'block';
      line.innerHTML = 'On a phone without a wallet browser? <a href="https://phantom.app/ul/browse/' +
        encodeURIComponent(location.origin + location.pathname) + '" target="_blank" rel="noopener">Open this page inside Phantom ↗</a>';
    }
  }

  /* ─────────── hero video, conditional and post-load ─────────── */
  addEventListener('load', () => {
    if (REDUCED) return;
    const c = navigator.connection;
    if (c && (c.saveData || /2g/.test(c.effectiveType || ''))) return;
    const v = $('#sigilVid');
    if (!v) return;
    v.src = 'assets/sigil.mp4?v=2';
    v.load();
    const go = () => v.play().then(() => v.classList.add('on')).catch(() => {});
    v.readyState >= 2 ? go() : v.addEventListener('loadeddata', go, { once: true });
    const io = new IntersectionObserver(es => es.forEach(e => {
      if (e.isIntersecting) v.play().catch(() => {}); else v.pause();
    }), { threshold: 0.1 });
    io.observe(v);
    document.addEventListener('visibilitychange', () => { document.hidden ? v.pause() : v.play().catch(() => {}); });
  });

  /* ─────────── THE PULL → THE WALL ─────────── */
  const bow = $('#bow'), tension = $('#tension'), string = $('#string');
  const wall = $('#wall'), grid = $('#wallGrid');
  let drawn = 0, dragging = false, fired = false;

  const setDraw = d => {
    drawn = Math.max(0, Math.min(1, d));
    if (tension) tension.style.width = (drawn * 100) + '%';
    if (string) string.setAttribute('x1', String(78 - drawn * 26));
    if (bow) bow.style.transform = `translateX(${-drawn * 5}px)`;
  };

  async function loadWall() {
    if (fired) return;
    fired = true;
    let art = [];
    try { art = await fetch('assets/art.json').then(r => r.json()); } catch (e) { art = []; }
    if (!art.length) { toast('Could not load the wall'); return; }
    wall.classList.add('open');
    $('#wallCount').textContent = art.length + ' originals';
    const cx = innerWidth / 2, cy = innerHeight / 2;
    art.forEach((a, i) => {
      const b = document.createElement('button');
      b.className = 'tile';
      b.type = 'button';
      b.dataset.slug = a.s;
      b.dataset.cap = a.c;
      b.innerHTML = `<img src="assets/art/${a.s}-224.webp" width="224" height="224" loading="lazy" decoding="async" alt="${a.c.replace(/"/g, '&quot;')}">`;
      if (!REDUCED) {
        b.style.setProperty('--dx', (Math.cos(i) * cx * 0.8) + 'px');
        b.style.setProperty('--dy', (Math.sin(i * 1.7) * cy * 0.8) + 'px');
      }
      grid.appendChild(b);
    });
    wall.scrollIntoView({ behavior: REDUCED ? 'auto' : 'smooth', block: 'start' });
    const tiles = $$('.tile');
    tiles.forEach((t, i) => setTimeout(() => t.classList.add('in'), REDUCED ? 0 : (i % 24) * 14 + Math.floor(i / 24) * 260));
    // safety net: a backgrounded tab freezes transitions and would strand tiles invisible
    setTimeout(() => tiles.forEach(t => t.classList.add('in')), 4200);
    document.addEventListener('visibilitychange', () => {
      if (!document.hidden) setTimeout(() => tiles.forEach(t => t.classList.add('in')), 60);
    });
  }

  function release() {
    if (!dragging) return;
    dragging = false;
    bow?.releasePointerCapture?.(0);
    if (drawn < 0.25) { setDraw(0); return; }
    setDraw(0);
    if (REDUCED) return loadWall();
    const fl = $('#flash'), sh = $('#shock'), ar = $('#arrowfly');
    if (ar) {
      ar.style.cssText = 'opacity:1;transform:translate(-50%,-50%) scale(1.4);transition:transform .24s cubic-bezier(.3,0,.7,1),opacity .24s';
      requestAnimationFrame(() => { ar.style.transform = 'translate(60vw,-50%) scale(.6)'; });
      setTimeout(() => { ar.style.opacity = '0'; }, 240);
    }
    setTimeout(() => {
      if (fl) { fl.style.cssText = 'opacity:.9;transition:opacity .06s'; setTimeout(() => { fl.style.opacity = '0'; }, 60); }
      if (sh) {
        sh.style.cssText = 'opacity:1;transform:scale(0);transition:transform .7s cubic-bezier(.2,.7,.3,1),opacity .7s';
        requestAnimationFrame(() => { sh.style.transform = 'scale(26)'; sh.style.opacity = '0'; });
      }
      loadWall();
    }, 240);
  }

  if (bow && !REDUCED) {
    const rect = () => bow.getBoundingClientRect();
    bow.addEventListener('pointerdown', e => {
      dragging = true; bow.setPointerCapture?.(e.pointerId); e.preventDefault();
    });
    bow.addEventListener('pointermove', e => {
      if (!dragging) return;
      const r = rect();
      setDraw((r.left + r.width - e.clientX) / 180);
    });
    bow.addEventListener('pointerup', release);
    bow.addEventListener('pointercancel', release);
    let held = false;
    addEventListener('keydown', e => {
      if ((e.code === 'Space' || e.code === 'Enter') && document.activeElement === document.body && !held) {
        const r = rect();
        if (r.top > innerHeight || r.bottom < 0) return;
        e.preventDefault(); held = true; dragging = true;
        let d = 0;
        const t = setInterval(() => { d += 0.08; setDraw(d); if (d >= 1) clearInterval(t); }, 40);
        bow._t = t;
      }
    });
    addEventListener('keyup', e => {
      if ((e.code === 'Space' || e.code === 'Enter') && held) { held = false; clearInterval(bow._t); release(); }
    });
  } else if (bow) {
    $('#pullHint').textContent = 'Reduced motion is on — use the button below';
  }
  $('#skipPull')?.addEventListener('click', loadWall);

  /* ─────────── lightbox ─────────── */
  const lb = $('#lb');
  grid?.addEventListener('click', e => {
    const t = e.target.closest('.tile');
    if (!t) return;
    const slug = t.dataset.slug, cap = t.dataset.cap;
    $('#lbImg').src = `assets/art/${slug}-900.webp`;
    $('#lbImg').alt = cap;
    $('#lbCap').textContent = cap;
    $('#lbShare').href = 'https://twitter.com/intent/tweet?text=' +
      encodeURIComponent(`"${cap}" — $BABYSHIB 🐶 https://babyshib.lol`);
    lb.classList.add('open');
  });
  const closeLb = () => lb?.classList.remove('open');
  $('#lbX')?.addEventListener('click', closeLb);
  lb?.addEventListener('click', e => { if (e.target === lb) closeLb(); });
  addEventListener('keydown', e => { if (e.key === 'Escape') closeLb(); });

  /* ─────────── reveal, with the frozen-tab safety net ─────────── */
  const rv = $$('.rv');
  if ('IntersectionObserver' in window && !REDUCED) {
    const io = new IntersectionObserver(es => es.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    }), { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });
    rv.forEach((el, i) => { el.style.transitionDelay = (i % 3) * 70 + 'ms'; io.observe(el); });
    const unstick = () => rv.forEach(el => {
      const r = el.getBoundingClientRect();
      if (r.top < innerHeight && r.bottom > 0) { el.style.transitionDelay = '0ms'; el.classList.add('in'); }
    });
    document.addEventListener('visibilitychange', () => { if (!document.hidden) setTimeout(unstick, 60); });
    addEventListener('pageshow', unstick);
    setTimeout(unstick, 2500);
  } else {
    rv.forEach(el => el.classList.add('in'));
  }

  if (FLAT) setTimeout(loadWall, 300);

  const yr = $('#yr');
  if (yr) yr.textContent = new Date().getFullYear();
})();
