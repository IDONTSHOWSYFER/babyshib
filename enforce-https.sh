#!/usr/bin/env bash
# Wait for GitHub's DNS check to pass and the Let's Encrypt cert to be issued,
# then turn on Enforce HTTPS. Never rolls anything back: GitHub is already
# serving the domain correctly, only DNS propagation is outstanding.
set -uo pipefail
REPO="IDONTSHOWSYFER/babyshib"
DOMAIN="babyshib.lol"

for i in $(seq 1 120); do   # up to ~2h
  # does GitHub itself now consider the domain healthy?
  if curl -s --max-time 20 --resolve "$DOMAIN:443:185.199.108.153" "https://$DOMAIN/" -o /dev/null 2>/dev/null; then
    if gh api -X PUT "repos/$REPO/pages" -F "https_enforced=true" >/dev/null 2>&1; then
      sleep 5
      STATE=$(gh api "repos/$REPO/pages" 2>/dev/null | python3 -c "import json,sys;print(json.load(sys.stdin).get('https_enforced'))")
      [ "$STATE" = "True" ] && { echo "HTTPS_ENFORCED"; exit 0; }
    fi
  fi
  sleep 60
done
echo "HTTPS_STILL_PENDING"
exit 1
