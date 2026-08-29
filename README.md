# BABY SHIB — $BABYSHIB

Landing page / sales funnel for **Baby Shib**, a community-run memecoin on Solana.

- **Contract:** `5nZMRLSFnA3oWXXswKyyaW5or2FFy34tkTUhtkWPpump`
- **Chart:** [DexScreener](https://dexscreener.com/solana/dsimbs1ueslmjpt9wb9xkmfeuujuk1ykcrsn7r2etqdx)
- **Buy:** [Jupiter](https://jup.ag/swap/SOL-5nZMRLSFnA3oWXXswKyyaW5or2FFy34tkTUhtkWPpump)
- **X:** [@Babyshibsolana](https://x.com/Babyshibsolana) · **Telegram:** [t.me/Thebabyshibcto](https://t.me/Thebabyshibcto)

## Stack

Static site — no build step, no dependencies. `index.html` + `styles.css` + `app.js` + `assets/`.

Live price / market cap / liquidity / volume are pulled client-side from the public
DexScreener API every 30 seconds, so the numbers on the page are never hard-coded.

## Local preview

```bash
python3 -m http.server 8941
```

Then open http://localhost:8941

## Deploy

Hosted with GitHub Pages from the `main` branch, root folder.

## Editing the essentials

| What | Where |
|---|---|
| Contract address | `index.html` (search `5nZMRL`) + `MINT` in `app.js` |
| Buy link | `index.html`, every `jup.ag/swap` href |
| Chart pair | `index.html`, the DexScreener `<iframe>` src |
| Brand colours | `styles.css`, `:root` (`--red`, `--orange`, `--ink`, `--cream`) |
| Memes | `assets/meme-*.jpg` |
