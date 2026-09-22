# BABY SHIB — babyshib.lol

**THE BABYVERSE GATE.** Three art realms, one ticker.

Landing page / sales funnel for **$BABYSHIB**, a community-run memecoin on Solana.

- **Contract:** `5nZMRLSFnA3oWXXswKyyaW5or2FFy34tkTUhtkWPpump`
- **Buy:** [Jupiter](https://jup.ag/swap/SOL-5nZMRLSFnA3oWXXswKyyaW5or2FFy34tkTUhtkWPpump) · **Chart:** [DexScreener](https://dexscreener.com/solana/dsimbs1ueslmjpt9wb9xkmfeuujuk1ykcrsn7r2etqdx)
- **X:** [@babyshibhq](https://x.com/babyshibhq) · **Telegram:** [t.me/Thebabyshibcto](https://t.me/Thebabyshibcto)

## The idea

The 93 original artworks sort into three visual worlds, so the page *becomes* three worlds.
Scrolling changes realm — palette, type colour, shadow language and radius all swap, twice.
The only element identical across all three is the BUY button. That invariance is the argument.

| Realm | Look | Art |
|---|---|---|
| **I · The Arena** | ink + red lightning | epic anime, battle, the bear |
| **II · The Good Life** | cream + sunset, no numbers anywhere | slice-of-life |
| **III · The Trenches** | flat sticker red, borderless | meme cartoons |

Signature moments: the two **gates** (a red disc swallows the page, then four blades slam in),
**the pull** (drag the bow, release, the explosion becomes the wall of all 93 originals),
and **the final boss** (a bear whose HP is the live 24h price move, inverted — mechanic printed in plain text).

## Honesty

Not affiliated with Shiba Inu or Shibarium. The Babyverse is a website, not a product — the gates are
page transitions. The origin portal is an outbound link to shib.io, nothing more. Only facts verifiable
on Solscan or DexScreener are stated as facts; everything else reads unmistakably as a joke.

## Stack

Static. No build step, no framework, no npm, no tracking. `index.html` + `styles.css` + `app.js` + `assets/`.
Live price / market cap / liquidity / volume come client-side from the DexScreener API every 30s,
stale-not-zero on failure.

## Local

```bash
python3 -m http.server 8941
```

Append `?flat=1` to flatten the full-height sections and reveal everything — used for screenshot QA.

## Regenerating the page

`index.html` is generated from `assets/art.json` (the artwork manifest):

```bash
python3 tools/build-page.py
```

Edit copy and structure in `tools/build-page.py`, never in `index.html` directly.

## Assets

93 artworks, each encoded to WebP at 224 / 400 / 900 px (plus 1600 for the strongest pieces).
Source library was 129 MB of PNG/JPEG; shipped as ~14 MB. The hero video is a 365 KB loop
(the 17 MB master is not in the repo). Filenames are semantic — `storm-field-bear-duel-900.webp`.
