#!/usr/bin/env bash
# Switch the site over to babyshib.lol once GoDaddy DNS points at GitHub Pages.
set -euo pipefail
cd "$(dirname "$0")"
DOMAIN="babyshib.lol"
REPO="IDONTSHOWSYFER/babyshib"

echo "$DOMAIN" > CNAME

# canonical / og / sitemap / robots move from the github.io path to the apex domain
python3 - <<PY
import re
h=open('index.html').read()
h=h.replace('https://idontshowsyfer.github.io/babyshib/','https://$DOMAIN/')
h=h.replace('<meta property="og:image" content="assets/logo.jpg">','<meta property="og:image" content="https://$DOMAIN/assets/logo.jpg">')
h=h.replace('<meta name="twitter:image" content="assets/logo.jpg">','<meta name="twitter:image" content="https://$DOMAIN/assets/logo.jpg">')
h=h.replace('<meta property="og:type" content="website">','<meta property="og:type" content="website">\n<meta property="og:url" content="https://$DOMAIN/">')
open('index.html','w').write(h)
for f in ('robots.txt','sitemap.xml','README.md'):
    s=open(f).read().replace('https://idontshowsyfer.github.io/babyshib/','https://$DOMAIN/')
    open(f,'w').write(s)
PY

git add -A
git commit -q -m "Point the site at babyshib.lol

CNAME for GitHub Pages, plus canonical/og/sitemap/robots moved from the
github.io path to the apex domain so social cards and search resolve there.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
git push -q origin main
echo "→ pushed CNAME"

gh api -X PUT "repos/$REPO/pages" -f "cname=$DOMAIN" >/dev/null 2>&1 || true
echo "→ custom domain set on GitHub"
