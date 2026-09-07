#!/usr/bin/env bash
# Deploy the NavigatorLabs landing site to Cloudflare Pages.
#
# Requires in the environment:
#   CLOUDFLARE_API_TOKEN  — token with: Account Settings:Read + Cloudflare Pages:Edit
#                           (add Zone:Read + DNS:Edit on navigators.com if you want
#                            this script to also verify the custom domain attach)
#   CLOUDFLARE_ACCOUNT_ID — the 32-char account id
#
# Usage:
#   bash deploy.sh              # create project (idempotent) + upload current dir
#   bash deploy.sh --attach     # also add custom domain navigators.com (needs Pages + DNS scopes)
set -euo pipefail

PROJECT="navigators-labs"
DOMAIN="navigators.com"

: "${CLOUDFLARE_API_TOKEN:?export CLOUDFLARE_API_TOKEN first}"
: "${CLOUDFLARE_ACCOUNT_ID:?export CLOUDFLARE_ACCOUNT_ID first}"

echo "== 1. Pages project =="
# Create if missing; ignore the "already exists" error.
npx --yes wrangler@latest pages project create "$PROJECT" \
  --production-branch=main 2>&1 | grep -v "already exists" || true

echo "== 2. Upload build =="
npx --yes wrangler@latest pages deploy . \
  --project-name="$PROJECT" --branch=main --commit-dirty=true

echo
echo "Preview/production URL: https://$PROJECT.pages.dev"

if [[ "${1:-}" == "--attach" ]]; then
  echo "== 3. Custom domain $DOMAIN =="
  API="https://api.cloudflare.com/client/v4"
  AUTH=(-H "Authorization: Bearer $CLOUDFLARE_API_TOKEN")
  ACCT="$CLOUDFLARE_ACCOUNT_ID"

  echo "-- adding $DOMAIN to Pages project (must already be a zone in this account) --"
  curl -s "${AUTH[@]}" -X POST \
    "$API/accounts/$ACCT/pages/projects/$PROJECT/domains" \
    -H "Content-Type: application/json" \
    -d "{\"name\":\"$DOMAIN\"}" | python -c "import json,sys; d=json.load(sys.stdin); print('success:', d['success']); print('errors:', d['errors'])"

  echo "-- DNS record for $DOMAIN (CNAME to $PROJECT.pages.dev, proxied) --"
  ZONE_ID=$(curl -s "${AUTH[@]}" "$API/zones?name=$DOMAIN" \
    | python -c "import json,sys; d=json.load(sys.stdin); print(d['result'][0]['id'] if d.get('result') else '')")
  if [[ -z "$ZONE_ID" ]]; then
    echo "!! zone $DOMAIN not visible to this token — add Zone:Read scope, or add the zone to the account first."
    exit 1
  fi
  curl -s "${AUTH[@]}" -X POST "$API/zones/$ZONE_ID/dns_records" \
    -H "Content-Type: application/json" \
    -d "{\"type\":\"CNAME\",\"name\":\"@\",\"content\":\"$PROJECT.pages.dev\",\"proxied\":true}" \
    | python -c "import json,sys; d=json.load(sys.stdin); print('success:', d['success']); print('errors:', d['errors'])"

  echo "NOTE: if $DOMAIN currently points at old hosting (2017 Apache box), the zone's"
  echo "nameservers must already be Cloudflare's for the CNAME to take effect. Verify with:"
  echo "  dig +short navigators.com NS"
fi

echo
echo "== 4. Verify =="
sleep 8
curl -s -o /dev/null -w "pages.dev  -> HTTP %{http_code}\n" "https://$PROJECT.pages.dev/" || true
curl -s -o /dev/null -w "$DOMAIN -> HTTP %{http_code}\n" "https://$DOMAIN/" || true
