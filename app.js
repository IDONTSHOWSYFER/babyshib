/* ═══════════════════════════════════════════
   BABY SHIB — live site logic
   ═══════════════════════════════════════════ */
(function () {
  'use strict';

  var MINT = '5nZMRLSFnA3oWXXswKyyaW5or2FFy34tkTUhtkWPpump';
  var API  = 'https://api.dexscreener.com/latest/dex/tokens/' + MINT;
  var REFRESH_MS = 30000;

  var $ = function (s) { return document.querySelector(s); };

  /* ─── formatting ─── */
  function money(n) {
    if (n === null || n === undefined || isNaN(n)) return '—';
    if (n >= 1e9) return '$' + (n / 1e9).toFixed(2) + 'B';
    if (n >= 1e6) return '$' + (n / 1e6).toFixed(2) + 'M';
    if (n >= 1e3) return '$' + (n / 1e3).toFixed(1) + 'K';
    return '$' + n.toFixed(0);
  }
  function price(p) {
    var n = parseFloat(p);
    if (!n || isNaN(n)) return '—';
    if (n >= 1) return '$' + n.toFixed(3);
    // compact leading-zero notation: $0.0₄5056
    var s = n.toFixed(12).replace(/0+$/, '');
    var m = s.match(/^0\.(0*)(\d{1,4})/);
    if (m && m[1].length >= 3) {
      var subs = '₀₁₂₃₄₅₆₇₈₉';
      var z = String(m[1].length).split('').map(function (d) { return subs[+d]; }).join('');
      return '$0.0' + z + m[2];
    }
    return '$' + n.toFixed(8).replace(/0+$/, '');
  }
  function pct(v) {
    if (v === null || v === undefined || isNaN(v)) return '';
    return (v >= 0 ? '+' : '') + v.toFixed(1) + '%';
  }

  /* ─── live stats ─── */
  var lastData = null;

  function paint(p) {
    lastData = p;
    var mc = p.marketCap || p.fdv;
    $('#statPrice').textContent = price(p.priceUsd);
    $('#statMcap').textContent  = money(mc);
    $('#statLiq').textContent   = money(p.liquidity && p.liquidity.usd);
    $('#statVol').textContent   = money(p.volume && p.volume.h24);

    var ch = p.priceChange && p.priceChange.h24;
    var el = $('#statChange');
    el.textContent = pct(ch) + ' · 24h';
    el.className = 'stat__d ' + (ch >= 0 ? 'up' : 'down');

    $('#statUpdated').textContent = 'updated ' + new Date().toLocaleTimeString();
    var sticky = $('#stickyPrice');
    if (sticky) sticky.textContent = money(mc) + ' MC';

    buildTicker(p);
  }

  function buildTicker(p) {
    var track = $('#tickerTrack');
    if (!track) return;
    var ch = p && p.priceChange ? p.priceChange.h24 : null;
    var chTag = ch === null ? '' :
      (ch >= 0 ? '<b>' + pct(ch) + '</b>' : '<i>' + pct(ch) + '</i>');
    var bits = [
      '$BABYSHIB <em>' + (p ? price(p.priceUsd) : '—') + '</em> ' + chTag,
      'MUCH WOOF 🐶',
      'MC <em>' + (p ? money(p.marketCap || p.fdv) : '—') + '</em>',
      'MINT REVOKED ✓',
      'FREEZE REVOKED ✓',
      '0% TAX ✓',
      'COMMUNITY TAKEOVER',
      'LIVE ON SOLANA ⛓'
    ];
    var html = '';
    for (var r = 0; r < 3; r++) {
      html += bits.map(function (b) { return '<span>' + b + '</span>'; }).join('<span>·</span>');
      html += '<span>·</span>';
    }
    track.innerHTML = html;
  }

  function refresh() {
    fetch(API, { cache: 'no-store' })
      .then(function (r) { return r.json(); })
      .then(function (d) {
        var pairs = (d && d.pairs) || [];
        if (!pairs.length) throw new Error('no pairs');
        pairs.sort(function (a, b) {
          return ((b.liquidity && b.liquidity.usd) || 0) - ((a.liquidity && a.liquidity.usd) || 0);
        });
        paint(pairs[0]);
      })
      .catch(function () {
        var u = $('#statUpdated');
        if (u && !lastData) u.textContent = 'live data unavailable — see DexScreener';
      });
  }

  buildTicker(null);
  refresh();
  setInterval(refresh, REFRESH_MS);
  document.addEventListener('visibilitychange', function () {
    if (!document.hidden) refresh();
  });

  /* ─── copy contract address ─── */
  var caBox = $('#caBox');
  var toast = $('#toast');
  function showToast(msg) {
    if (!toast) return;
    toast.textContent = msg;
    toast.classList.add('show');
    clearTimeout(showToast._t);
    showToast._t = setTimeout(function () { toast.classList.remove('show'); }, 2200);
  }
  function copyCA() {
    var text = $('#caText').textContent.trim();
    var done = function () {
      $('#caCopy').textContent = 'COPIED!';
      showToast('Contract address copied 🐾');
      setTimeout(function () { $('#caCopy').textContent = 'COPY'; }, 1800);
    };
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(done, fallback);
    } else { fallback(); }
    function fallback() {
      var ta = document.createElement('textarea');
      ta.value = text; ta.style.position = 'fixed'; ta.style.opacity = '0';
      document.body.appendChild(ta); ta.select();
      try { document.execCommand('copy'); done(); } catch (e) { showToast('Copy failed — select it manually'); }
      document.body.removeChild(ta);
    }
  }
  if (caBox) {
    caBox.addEventListener('click', copyCA);
    caBox.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); copyCA(); }
    });
  }

  /* ─── nav shadow on scroll ─── */
  var nav = $('#nav');
  var onScroll = function () {
    if (nav) nav.classList.toggle('is-stuck', window.scrollY > 12);
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ─── floating paws in hero ─── */
  var paws = $('#paws');
  if (paws && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var html = '';
    for (var i = 0; i < 14; i++) {
      var left  = Math.round(Math.random() * 96);
      var delay = (Math.random() * 9).toFixed(2);
      var size  = 16 + Math.round(Math.random() * 22);
      var top   = 20 + Math.round(Math.random() * 70);
      html += '<b style="left:' + left + '%;top:' + top + '%;font-size:' + size +
              'px;animation-delay:-' + delay + 's">🐾</b>';
    }
    paws.innerHTML = html;
  }

  /* ─── scroll reveal ─── */
  var targets = document.querySelectorAll(
    '.story__inner > *, .cards .card, .steps .step, .tok__item, .gallery figure, .road__item, .faq details, .final .h2, .final .lead, .final__cta, .socials, .chart__frame'
  );
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    Array.prototype.forEach.call(targets, function (t, i) {
      t.classList.add('reveal');
      t.style.transitionDelay = (i % 4) * 70 + 'ms';
      io.observe(t);
    });

    /* safety net: a backgrounded tab freezes CSS transitions, which can leave
       revealed blocks stuck at opacity 0. Never let content stay invisible. */
    var unstick = function () {
      Array.prototype.forEach.call(targets, function (t) {
        var r = t.getBoundingClientRect();
        if (r.top < window.innerHeight && r.bottom > 0) {
          t.style.transitionDelay = '0ms';
          t.classList.add('in');
        }
      });
    };
    document.addEventListener('visibilitychange', function () {
      if (!document.hidden) setTimeout(unstick, 60);
    });
    window.addEventListener('pageshow', unstick);
    setTimeout(unstick, 2500);
  } else {
    Array.prototype.forEach.call(targets, function (t) { t.classList.add('in'); });
  }

  /* ─── year ─── */
  var y = $('#year');
  if (y) y.textContent = new Date().getFullYear();
})();
