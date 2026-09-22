#!/usr/bin/env python3
"""Generate index.html from assets/art.json. Run locally, commit the output.
The deployed site stays a plain static folder with no toolchain."""
import json, os, html, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
art = json.load(open(ROOT / "assets/art.json"))
by = {a["s"]: a for a in art}

MINT = "5nZMRLSFnA3oWXXswKyyaW5or2FFy34tkTUhtkWPpump"
JUP  = f"https://jup.ag/swap/SOL-{MINT}"
PAIR = "DSiMBS1ueSLmjpt9WB9XKMFeuUjUK1YKcrSn7R2etQDX"
X    = "https://x.com/babyshibhq"
TG   = "https://t.me/Thebabyshibcto"
DEX  = f"https://dexscreener.com/solana/{PAIR.lower()}"
SOL  = f"https://solscan.io/token/{MINT}"

def realm(r, n, skip=()):
    out = [a for a in art if a["r"] == r and a["s"] not in skip]
    return out[:n]

def img(a, sizes_attr, cls="", big=False, lazy=True, w=1254):
    s = a["s"]; have = a["z"]
    srcset = ", ".join(f"assets/art/{s}-{z}.webp {z}w" for z in have)
    base = 900 if 900 in have else have[-1]
    fp = "" if lazy else ' fetchpriority="high"'
    ld = ' loading="lazy"' if lazy else ""
    return (f'<img src="assets/art/{s}-{base}.webp" srcset="{srcset}" sizes="{sizes_attr}"'
            f' width="{w}" height="{w}"{ld} decoding="async"{fp}'
            f' alt="{html.escape(a["c"])}"{f" class=\"{cls}\"" if cls else ""}>')

def cap(a): return html.escape(a["c"])

# ── curation ─────────────────────────────────────────────────────
HERO      = by.get("archer-drawing-crimson-arrow") or art[0]
HERO_BG   = by.get("army-ranks-mushroom-cloud") or art[1]
BOSS      = by.get("storm-field-bear-duel") or art[2]
CLOSE_BG  = by.get("spear-charge-shiba-army") or art[3]
used = {HERO["s"], HERO_BG["s"], BOSS["s"], CLOSE_BG["s"]}

MARCH   = realm("arena", 6, used); used |= {a["s"] for a in MARCH}
LIFE    = realm("life", 14, used); used |= {a["s"] for a in LIFE}
TRENCH  = realm("trench", 8, used); used |= {a["s"] for a in TRENCH}
PACK    = [a for a in art if a["r"] == "pfp"][:6]

march_html = "\n".join(
    f'    <figure class="panel rv">{img(a, "(max-width:700px) 86vw, 32vw")}'
    f'<figcaption>{cap(a)}</figcaption></figure>' for a in MARCH)

life_html = "\n".join(
    f'    <figure class="card rv" style="--r:{(-1.6 if i%2 else 1.4):.1f}deg">'
    f'{img(a, "(max-width:600px) 88vw, (max-width:1100px) 44vw, 27vw")}'
    f'<figcaption>{cap(a)}</figcaption></figure>' for i, a in enumerate(LIFE))

trench_html = "\n".join(
    f'    <figure class="sticker rv">{img(a, "(max-width:600px) 88vw, (max-width:1100px) 44vw, 26vw")}'
    f'<figcaption>{cap(a)}</figcaption></figure>' for a in TRENCH)

pack_html = "\n".join(
    f'      <img src="assets/art/{a["s"]}-224.webp" width="224" height="224" loading="lazy" '
    f'decoding="async" alt="{cap(a)}">' for a in PACK)

PAGE = f"""<!DOCTYPE html>
<html lang="en" data-realm="arena">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>BABY SHIB — Enter the Babyverse</title>
<meta name="description" content="Three realms, one ticker. $BABYSHIB is a community-run Solana memecoin: mint revoked, freeze revoked, 0% tax. Enter the Babyverse.">
<meta name="theme-color" content="#0B0B0B">
<link rel="icon" href="assets/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<link rel="canonical" href="https://babyshib.lol/">
<meta property="og:type" content="website">
<meta property="og:url" content="https://babyshib.lol/">
<meta property="og:title" content="BABY SHIB — Enter the Babyverse">
<meta property="og:description" content="Three realms, one ticker. Community-run Solana memecoin. Mint revoked · Freeze revoked · 0% tax.">
<meta property="og:image" content="https://babyshib.lol/assets/art/{HERO['s']}-900.webp">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@babyshibhq">
<meta name="twitter:title" content="BABY SHIB — Enter the Babyverse">
<meta name="twitter:description" content="Three realms, one ticker. Community-run Solana memecoin.">
<meta name="twitter:image" content="https://babyshib.lol/assets/art/{HERO['s']}-900.webp">
<link rel="preload" as="image" href="assets/art/{HERO['s']}-900.webp" fetchpriority="high">
<link rel="preconnect" href="https://api.dexscreener.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Luckiest+Guy&display=swap">
<link rel="stylesheet" href="styles.css">
</head>
<body>

<header class="nav" id="nav">
  <a class="nav__brand" href="#top"><img src="assets/logo.jpg" alt="" width="34" height="34"><span>BABY SHIB</span><span class="nav__realm" id="realmLabel">THE ARENA</span></a>
  <nav class="nav__links">
    <a href="#loadout">How to buy</a><a href="#march">The March</a><a href="#goodlife">Good Life</a>
    <a href="#trenches">Trenches</a><a href="#wall">The Wall</a><a href="#faq">FAQ</a>
  </nav>
  <a class="buy" data-size="sm" href="{JUP}" target="_blank" rel="noopener">BUY $BABYSHIB</a>
</header>

<main id="top">

<!-- ══ 1 · REALM I — THE ARENA ══ -->
<section class="arena" id="arena">
  <div class="arena__bg">{img(HERO_BG, "100vw", lazy=True)}</div>
  <div class="bolt" id="bolt" aria-hidden="true"></div>
  <div class="arena__inner">
    <div>
      <span class="eyebrow">Realm I · The Arena</span>
      <h1 class="h-xl">BABY<span class="line2">SHIB</span></h1>
      <p class="arena__tag">Just here to continue the legacy and spread the love. <strong>Much Woof!</strong> 🐶</p>
      <div class="arena__cta">
        <a class="buy" data-size="lg" href="{JUP}" target="_blank" rel="noopener">BUY $BABYSHIB</a>
        <a class="ghost" href="#loadout">HOW TO BUY</a>
      </div>
      <div class="ca" id="ca" role="button" tabindex="0" aria-label="Copy the contract address">
        <code id="caText">{MINT}</code><span id="caBtn">COPY</span>
      </div>
      <ul class="proof">
        <li><b>✓</b> Mint revoked</li><li><b>✓</b> Freeze revoked</li><li><b>✓</b> 0% tax</li>
      </ul>
    </div>
    <div>
      <div class="sigil" id="sigil">
        <span class="sigil__ring" aria-hidden="true"></span>
        <img src="assets/sigil-poster.webp" width="900" height="900" alt="Baby Shib drawing a glowing bow" fetchpriority="high">
        <video id="sigilVid" muted playsinline loop preload="none" poster="assets/sigil-poster.webp" aria-hidden="true"></video>
      </div>
    </div>
  </div>
</section>

<!-- ══ 2 · THE TAPE + THE FINAL BOSS ══ -->
<section class="tape" id="tape">
  <div class="wrap">
    <div class="tape__grid">
      <div class="cell"><div class="cell__k">Price</div><div class="cell__v mono" id="mPrice">—</div><div class="cell__d mono" id="mChange">24h</div></div>
      <div class="cell"><div class="cell__k">Market cap</div><div class="cell__v mono" id="mMcap">—</div><div class="cell__d mono">fully diluted</div></div>
      <div class="cell"><div class="cell__k">Liquidity</div><div class="cell__v mono" id="mLiq">—</div><div class="cell__d mono">pooled</div></div>
      <div class="cell"><div class="cell__k">24h volume</div><div class="cell__v mono" id="mVol">—</div><div class="cell__d mono">traded</div></div>
    </div>
    <p class="tape__note"><span class="dot" id="liveDot"></span><span id="liveNote">connecting to DexScreener…</span></p>

    <div class="boss" id="boss">
      <div class="boss__art">{img(BOSS, "170px", w=1821)}</div>
      <div>
        <div class="boss__t"><h2 class="h-md">THE FINAL BOSS</h2><span class="mono" id="bossState">—</span></div>
        <div class="boss__hp"><i id="bossBar"></i><b></b></div>
        <p class="boss__mech">BEAR HP = the live 24h price move from DexScreener, inverted. Green day it drains, red day it refills. That is the whole mechanic.</p>
      </div>
    </div>
  </div>
</section>

<!-- ══ 3 · THE LOADOUT ══ -->
<section class="loadout" id="loadout">
  <div class="wrap">
    <span class="eyebrow">Your loadout</span>
    <h2 class="h-lg">THREE PASSIVES.<br>THREE STEPS.</h2>
    <p class="lead">The passives are on-chain facts you can verify yourself. The steps take about three minutes.</p>

    <div class="passives">
      <article class="pass rv"><div class="pass__i">🔒</div><h3>Mint revoked</h3><p>Mint authority is <code>null</code>. Nobody can print new supply. Ever.</p></article>
      <article class="pass rv"><div class="pass__i">🧊</div><h3>Freeze revoked</h3><p>Freeze authority is <code>null</code>. No one can lock your wallet or block your sell.</p></article>
      <article class="pass rv"><div class="pass__i">🚫</div><h3>0% tax</h3><p>Standard SPL token, no transfer-fee extension. You buy what you pay for.</p></article>
    </div>

    <ol class="steps">
      <li class="step rv"><div class="step__n">01</div><h3>Get a wallet</h3><p>Install <a href="https://phantom.app/" target="_blank" rel="noopener">Phantom</a> or <a href="https://solflare.com/" target="_blank" rel="noopener">Solflare</a>. Save your seed phrase offline, never share it.</p></li>
      <li class="step rv"><div class="step__n">02</div><h3>Fund it with SOL</h3><p>Buy SOL anywhere and send it to your wallet address. Keep ~0.01 SOL spare for network fees.</p></li>
      <li class="step rv"><div class="step__n">03</div><h3>Swap on Jupiter</h3><p>Open Jupiter with the token preloaded, set your amount, confirm. Slippage 3–5% on a moving chart.</p></li>
    </ol>

    <div class="center">
      <a class="buy" data-size="lg" href="{JUP}" target="_blank" rel="noopener">BUY $BABYSHIB</a>
      <p class="lead center" style="margin-top:14px"><a href="{SOL}" target="_blank" rel="noopener">Verify every claim on Solscan ↗</a></p>
      <p class="mono" id="phantomLine" style="display:none;font-size:.8rem;margin-top:10px"></p>
    </div>
  </div>
</section>

<!-- ══ 4 · THE MARCH ══ -->
<section class="march" id="march">
  <div class="wrap">
    <span class="eyebrow">The march</span>
    <h2 class="h-lg">SMALL DOG.<br>BIG MOVES.</h2>
    <p class="lead">Scroll sideways. The army does not stop.</p>
  </div>
  <div class="wrap">
    <div class="march__track">
{march_html}
    </div>
  </div>
</section>

<!-- ══ 5 · GATE I ══ -->
<section class="gate" id="gate1" aria-hidden="true">
  <div class="gate__disc" id="disc1"></div>
  <div class="gate__label" id="lab1">THE GATE OPENS</div>
</section>

<!-- ══ 6 · REALM II — THE GOOD LIFE (no numbers in this realm) ══ -->
<section class="life" id="goodlife">
  <div class="wrap">
    <span class="eyebrow">Realm II · The Good Life</span>
    <h2 class="h-lg">WHAT THE DOG<br>DOES OFF-CHART.</h2>
    <p class="lead">No charts in this realm. Just a small dog having a better day than most portfolios.</p>
    <div class="cards">
{life_html}
    </div>
  </div>
</section>

<!-- ══ 7 · GATE II ══ -->
<section class="gate" id="gate2" aria-hidden="true">
  <div class="gate__blades" id="blades"><i></i><i></i><i></i><i></i></div>
  <div class="gate__slab" id="slab2">YOU ARE NOW IN THE TRENCHES</div>
</section>

<!-- ══ 8 · REALM III — THE TRENCHES ══ -->
<section class="trench" id="trenches">
  <div class="wrap">
    <span class="eyebrow" style="color:#0B0B0B">Realm III · The Trenches</span>
    <h2 class="h-lg">IT'S SO OVER.<br>WE'RE SO BACK.</h2>
    <p class="lead">Where the memes are made and nobody sleeps.</p>
    <div class="stickers">
{trench_html}
    </div>
  </div>
</section>

<!-- ══ 9 · THE PULL → THE WALL ══ -->
<section class="pull" id="pull">
  <div class="wrap center">
    <span class="eyebrow">The pull</span>
    <h2 class="h-lg" style="color:#FFF6E9">DRAW THE BOW.</h2>
    <p class="lead" style="color:#9A9186">Pull the string back and let go. See what the community made.</p>
    <div class="bow" id="bow">
      <img src="assets/art/{HERO['s']}-900.webp" width="900" height="900" loading="lazy" decoding="async" alt="Baby Shib drawing a crimson arrow">
      <svg viewBox="0 0 100 100" aria-hidden="true"><line id="string" x1="78" y1="14" x2="78" y2="86" stroke="#FFF6E9" stroke-width="1.4"/></svg>
    </div>
    <div class="tension"><i id="tension"></i></div>
    <p class="pull__hint" id="pullHint">Drag the string · or press and hold Space</p>
    <button class="skip" id="skipPull">Skip — show me the wall</button>
  </div>
</section>

<section class="wall" id="wall">
  <div class="wrap">
    <div class="wall__hud"><span>The wall · 01 ticker.</span><span id="wallCount"></span></div>
    <div class="wall__grid" id="wallGrid"></div>
    <div class="center" style="margin-top:34px">
      <a class="buy" data-size="lg" href="{JUP}" target="_blank" rel="noopener">BUY $BABYSHIB</a>
    </div>
  </div>
</section>

<!-- ══ 10 · THE ORIGIN GATE (outbound) ══ -->
<section class="origin" id="origin">
  <div class="wrap center">
    <span class="eyebrow">The origin gate</span>
    <h2 class="h-lg" style="color:#FFF6E9">WHERE THE<br>LEGACY BEGAN.</h2>
    <div class="vortex">
      <i></i><i></i><i></i><i></i>
      <svg class="vortex__bolts" viewBox="0 0 400 400" aria-hidden="true">
        <g fill="none" stroke="#F90101" stroke-width="3" stroke-linejoin="round" stroke-linecap="round">
          <polyline points="200,200 214,150 196,140 220,86 200,74 226,16"/>
          <polyline points="200,200 250,186 258,204 314,190 322,208 384,196"/>
          <polyline points="200,200 186,250 204,258 190,314 208,322 196,384"/>
          <polyline points="200,200 150,214 142,196 86,210 78,192 16,204"/>
          <polyline points="200,200 240,164 254,178 296,140 310,154 350,112"/>
          <polyline points="200,200 236,240 222,254 260,296 246,310 288,350"/>
          <polyline points="200,200 160,236 146,222 104,260 90,246 50,288"/>
          <polyline points="200,200 164,160 178,146 140,104 154,90 112,50"/>
        </g>
      </svg>
      <a class="vortex__core" href="https://shib.io" target="_blank" rel="noopener noreferrer"><span>ENTER</span><em>SHIB.IO ↗</em></a>
    </div>
    <p class="origin__dis">This portal opens the official Shiba Inu website in a new tab. We are not affiliated with Shiba Inu or Shibarium — no partnership, no bridge, no connection. We are fans of the dog running a community takeover of a separate Solana token.</p>
  </div>
</section>

<!-- ══ 11 · THE PACK ══ -->
<section class="pack" id="pack">
  <div class="wrap center">
    <span class="eyebrow">The pack</span>
    <h2 class="h-lg">NOBODY HOLDS<br>THIS ALONE.</h2>
    <p class="lead">Memecoins move on attention. Bring one friend and you have already done the work.</p>
    <div class="packgrid">
{pack_html}
    </div>
    <div class="socials">
      <a href="{X}" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" width="19" height="19" aria-hidden="true"><path fill="currentColor" d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>Twitter / X</a>
      <a href="{TG}" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" width="19" height="19" aria-hidden="true"><path fill="currentColor" d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0zm5.01 7.617c.18-.002.578.042.836.252a.91.91 0 0 1 .307.653c.008.19.018.617-.035.95-.194 1.244-.897 5.316-1.253 6.996-.15.711-.447.95-.734.976-.625.058-1.1-.412-1.705-.808-.947-.62-1.482-1.007-2.401-1.612-1.062-.7-.374-1.084.232-1.712.159-.164 2.913-2.67 2.966-2.897.007-.028.013-.134-.05-.19s-.156-.037-.223-.022c-.095.022-1.608 1.022-4.54 3-.429.295-.818.439-1.166.431-.384-.008-1.123-.217-1.672-.396-.673-.219-1.208-.335-1.161-.706.024-.194.29-.392.798-.594 3.127-1.362 5.212-2.26 6.256-2.694 2.978-1.239 3.597-1.454 4-1.461z"/></svg>Telegram</a>
      <a href="{DEX}" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" width="19" height="19" aria-hidden="true"><path fill="currentColor" d="M3 3h2v16h16v2H3zm5 11 3.5-4.5 3 3L20 6l1.5 1.5-6 7-3-3L9 16z"/></svg>Chart</a>
    </div>
  </div>
</section>

<!-- ══ 12 · FAQ — the honesty room ══ -->
<section class="faq" id="faq">
  <div class="narrow">
    <span class="eyebrow">The honesty room</span>
    <h2 class="h-lg">QUESTIONS,<br>ANSWERED STRAIGHT.</h2>
    <div style="margin-top:28px">
      <details><summary>What is $BABYSHIB?</summary><p>A community-run memecoin on Solana carrying the Shiba legacy forward. No utility promises — it is a meme, a culture and a chart, run by the people holding it.</p></details>
      <details><summary>Affiliated with Shiba Inu or Shibarium?</summary><p>No. No partnership, no affiliation, no connection. We are fans who liked the dog. This is a community takeover of a separate Solana token.</p></details>
      <details><summary>Is the portal a real metaverse?</summary><p>No. It is a website with very good art. The gates are page transitions between three art realms — that is the whole trick, and we would rather tell you than let you assume otherwise.</p></details>
      <details><summary>Is the contract safe?</summary><p>Mint authority and freeze authority are both revoked on-chain, and it is a standard SPL token with no transfer tax. That removes the three classic rug levers — but a memecoin is still a high-risk asset. Verify on <a href="{SOL}" target="_blank" rel="noopener">Solscan</a> and never spend what you cannot lose.</p></details>
      <details><summary>Why is my swap failing?</summary><p>Raise slippage to 3–5% and keep ~0.01 SOL for fees. On fast candles a transaction can expire and simply needs a retry.</p></details>
      <details><summary>What does CTO mean?</summary><p>Community Take Over — the original deployer stepped away and holders took the wheel: socials, marketing, memes, this website.</p></details>
      <details><summary>How do I help?</summary><p>Hold, post, raid, bring one friend. Start in the <a href="{TG}" target="_blank" rel="noopener">Telegram</a>.</p>
      <span style="display:block;margin-top:14px"><a class="buy" data-size="sm" href="{JUP}" target="_blank" rel="noopener">BUY $BABYSHIB</a></span></details>
    </div>
  </div>
</section>

<!-- ══ 13 · THE GATE CLOSES ══ -->
<section class="close" id="close">
  <div class="close__bg">{img(CLOSE_BG, "100vw")}</div>
  <div class="close__inner wrap">
    <span class="eyebrow">The gate closes</span>
    <h2 class="h-xl" style="font-size:clamp(2.4rem,7vw,5.4rem)">DON'T BE THE ONE<br>WHO WATCHED.</h2>
    <p class="lead center">Every legend had a moment where it was still small. You are looking at one.</p>
    <div style="margin:32px 0 10px"><a class="buy" data-size="lg" href="{JUP}" target="_blank" rel="noopener">BUY $BABYSHIB</a></div>
    <p class="punch">Behind this portal: a website, a Telegram, and a very small dog.</p>
  </div>
</section>
</main>

<footer class="foot">
  <div class="wrap">
    <div style="display:flex;align-items:center;gap:13px;margin-bottom:16px">
      <img src="assets/logo.jpg" alt="" width="44" height="44" style="border-radius:50%;border:2px solid var(--accent)" loading="lazy">
      <div><strong style="font-family:var(--head);font-size:1.1rem">BABY SHIB</strong>
      <div class="foot__ca">{MINT}</div></div>
    </div>
    <p class="foot__dis">Not affiliated with Shiba Inu or Shibarium. The Babyverse is a website, not a product — the gates are page transitions, nothing more. $BABYSHIB is a meme coin with no intrinsic value, no expectation of financial return and no formal team or roadmap. Nothing here is financial advice. Crypto is volatile and you can lose everything — only spend what you can afford to lose, and always do your own research.</p>
    <p style="opacity:.55;font-size:.78rem;margin:0">© <span id="yr">2026</span> Baby Shib Community · Much Woof 🐶</p>
  </div>
</footer>

<a class="dock" id="dock" href="{JUP}" target="_blank" rel="noopener">
  <span class="dock__p"><b>$BABYSHIB</b><span id="dockPrice">—</span></span>
  <span class="buy" data-size="sm" style="pointer-events:none">BUY NOW</span>
</a>

<div class="flash" id="flash"></div>
<div class="shock" id="shock"></div>
<div class="arrowfly" id="arrowfly">➤</div>
<div class="toast" id="toast"></div>

<div class="lb" id="lb" role="dialog" aria-modal="true" aria-label="Artwork">
  <button class="lb__x" id="lbX" aria-label="Close">×</button>
  <div class="lb__box">
    <img id="lbImg" alt="" width="900" height="900">
    <p class="lb__cap" id="lbCap"></p>
    <div class="lb__act">
      <a class="ghost" id="lbShare" href="#" target="_blank" rel="noopener" style="color:#FFF6E9;border-color:#FFF6E9">SHARE ON X</a>
      <a class="buy" data-size="sm" href="{JUP}" target="_blank" rel="noopener">BUY $BABYSHIB</a>
    </div>
  </div>
</div>

<script src="app.js" defer></script>
</body>
</html>
"""

(ROOT / "index.html").write_text(PAGE)
print(f"index.html ecrit : {len(PAGE)} octets")
print(f"on-page : hero + bg + boss + close + {len(MARCH)} march + {len(LIFE)} life + {len(TRENCH)} trench + {len(PACK)} pfp = {4+len(MARCH)+len(LIFE)+len(TRENCH)+len(PACK)} artworks")
print(f"wall : {len(art)} artworks (lazy, apres le geste)")
