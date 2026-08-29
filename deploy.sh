#!/usr/bin/env bash
# One-shot deploy of the Baby Shib site to GitHub Pages.
# Requires: gh auth login  (run it once, first)
set -euo pipefail

REPO="IDONTSHOWSYFER/babyshib"
cd "$(dirname "$0")"

gh auth status >/dev/null 2>&1 || { echo "Run 'gh auth login' first."; exit 1; }

if gh repo view "$REPO" >/dev/null 2>&1; then
  echo "→ repo exists, pushing"
  git remote get-url origin >/dev/null 2>&1 || git remote add origin "https://github.com/$REPO.git"
  git push -u origin main
else
  echo "→ creating repo"
  gh repo create "$REPO" --public --source=. --remote=origin --push \
    --description "BABY SHIB (\$BABYSHIB) — community-run Solana memecoin. Live landing page."
fi

echo "→ enabling GitHub Pages"
gh api -X POST "repos/$REPO/pages" -f "source[branch]=main" -f "source[path]=/" >/dev/null 2>&1 \
  || gh api -X PUT "repos/$REPO/pages" -f "source[branch]=main" -f "source[path]=/" >/dev/null

echo
echo "✅ Live in ~1 minute at: https://idontshowsyfer.github.io/babyshib/"
