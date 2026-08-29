#!/usr/bin/env bash
# Switch to babyshib.lol only if DNS is stable, and roll back automatically if
# the domain does not actually serve the site. The site must never end up
# unreachable at both addresses again.
set -uo pipefail
cd "$(dirname "$0")"
DOMAIN="babyshib.lol"
REPO="IDONTSHOWSYFER/babyshib"

ok_resolver () {  # $1 = resolver ip
  [ "$(dig +short "$DOMAIN" A @"$1" | grep -c '^185\.199\.1[01][0-9]\.153$')" -ge 4 ]
}

echo "→ waiting for three independent resolvers to agree, three passes in a row"
streak=0
for attempt in $(seq 1 240); do          # up to ~8h, checking every 2 min
  if ok_resolver 1.1.1.1 && ok_resolver 8.8.8.8 && ok_resolver 9.9.9.9; then
    streak=$((streak+1))
    echo "   [$attempt] all three agree (streak $streak/3)"
    [ "$streak" -ge 3 ] && break
  else
    [ "$streak" -gt 0 ] && echo "   [$attempt] streak broken — apex still flapping"
    streak=0
  fi
  sleep 120
done
if [ "$streak" -lt 3 ]; then
  echo "GAVE_UP — apex never stabilised on GitHub's IPs. Site untouched, still on github.io."
  exit 1
fi

echo "→ DNS stable, switching over"
git pull --rebase -q origin main
./golive-domain.sh

echo "→ verifying $DOMAIN actually serves the site (up to 8 min)"
for i in $(seq 1 32); do
  BODY=$(curl -s --max-time 12 "http://$DOMAIN/" | grep -c "BABY SHIB (\$BABYSHIB)" || true)
  if [ "$BODY" -ge 1 ]; then
    echo "SWITCH_OK — $DOMAIN serves the site"
    for j in $(seq 1 30); do
      gh api -X PUT "repos/$REPO/pages" -F "https_enforced=true" >/dev/null 2>&1 && { echo "HTTPS_ENFORCED"; exit 0; }
      sleep 30
    done
    echo "HTTPS_PENDING — certificate not issued yet, enforce it later"
    exit 0
  fi
  sleep 15
done

echo "ROLLBACK — $DOMAIN never served the site, restoring the github.io URL"
git rm -q CNAME
git checkout -- index.html robots.txt sitemap.xml README.md 2>/dev/null
git -c user.name="$(git config --global user.name)" -c user.email="$(git config --global user.email)" \
  commit -q -m "Roll back to the github.io URL: babyshib.lol did not serve the site

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
git push -q origin main
echo "ROLLED_BACK"
exit 1
