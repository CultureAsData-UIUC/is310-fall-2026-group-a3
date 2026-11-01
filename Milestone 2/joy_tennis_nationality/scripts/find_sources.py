"""Phase 1: turn the hand-built seed list into data/candidates.csv.

The web searching itself was done with an AI search tool (see ai-chat-log.md
and collection_notes.md). This script does the repeatable part:

  * normalizes URLs and drops exact duplicates
  * flags known syndicated copies (same wire story on several sites)
  * checks robots.txt for our user agent on every domain
  * writes candidates.csv with a status column for Joy to approve or cut

Run from the joy_tennis_nationality folder:
    python scripts/find_sources.py
"""

import csv
import time
import urllib.robotparser
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

import requests

BASE = Path(__file__).resolve().parent.parent
SEED = BASE / "data" / "candidate_seed.csv"
OUT = BASE / "data" / "candidates.csv"

USER_AGENT = (
    "IS310-CultureAsData-student-research/0.1 "
    "(UIUC course project; +https://github.com/CultureAsData-UIUC/is310-fall-2026-group-a3)"
)
DELAY = 2  # seconds between robots.txt requests

# Same wire story on several sites. The first URL in each group is kept,
# the rest are marked as syndicated copies. Grouped by reading the search
# result titles; snapshot.py also checks for identical text afterwards.
SYNDICATED = [
    [
        "https://www.gulftoday.ae/sport/2026/01/31/elena-rybakina-kazakhstans-moscow-born-melbourne-tennis-champion",
        "https://www.thenews.pk/print/1396446-elena-rybakina-kazakhstan-s-moscow-born-melbourne-champion",
        "https://supersport.com/tennis/news/67db111e-85f0-42ac-b34f-c188a6af852c/elena-rybakina-kazakhstans-moscow-born-melbourne-champion",
    ],
    [
        "https://www.nbcnewyork.com/news/sports/russia-claims-credit-for-elena-rybakinas-wimbledon-title",
        "https://www.clickondetroit.com/sports/2022/07/10/russia-claims-credit-for-elena-rybakinas-wimbledon-title",
    ],
    [
        "https://www.flashscore.com/news/tennis-rome-wta-singles-aryna-sabalenka-hoping-to-compete-under-belarus-flag-after-ioc-ruling-lifts-olympic-ban/Wxl7D0Bb",
        "https://citizen.digital/article/sabalenka-hopes-to-compete-under-belarus-flag-after-ioc-ruling-n382303",
    ],
]

# Domains where search snippets or the URL itself show a paywall or a
# reader app that needs a login. We skip these instead of trying to get around them.
PAYWALLED = {"www.pressreader.com"}


def normalize(url):
    """Lowercase the host, drop fragments and trailing slashes so dups match."""
    parts = urlsplit(url.strip())
    path = parts.path.rstrip("/") or "/"
    return urlunsplit((parts.scheme, parts.netloc.lower(), path, parts.query, ""))


def robots_allows(url, cache):
    # RobotFileParser.read() fetches with the default Python-urllib agent,
    # which many CDNs block with a 403, and a 403 makes the parser treat the
    # whole site as disallowed. So we fetch robots.txt ourselves with our real
    # user agent and only hand the text to the parser.
    host = urlsplit(url).netloc
    if host not in cache:
        rp = urllib.robotparser.RobotFileParser()
        try:
            resp = requests.get(f"https://{host}/robots.txt",
                                headers={"User-Agent": USER_AGENT}, timeout=20)
            if resp.status_code in (401, 403):
                cache[host] = f"robots.txt returned {resp.status_code}"
            elif resp.status_code >= 400:
                rp.parse([])  # no robots.txt means no rules
                cache[host] = rp
            else:
                rp.parse(resp.text.splitlines())
                cache[host] = rp
        except requests.RequestException as e:
            cache[host] = f"robots_error: {type(e).__name__}"
        time.sleep(DELAY)
    rp = cache[host]
    if isinstance(rp, str):
        return None, rp
    return rp.can_fetch(USER_AGENT, url), ""


def main():
    with SEED.open(encoding="utf-8") as f:
        seed = list(csv.DictReader(f))

    syndicated_copy = {}
    for group in SYNDICATED:
        keep = normalize(group[0])
        for u in group[1:]:
            syndicated_copy[normalize(u)] = keep

    seen = set()
    robots_cache = {}
    rows = []
    for i, r in enumerate(seed, start=1):
        url = r["url"].strip()
        norm = normalize(url)
        status, reason = "candidate", ""
        if norm in seen:
            status, reason = "excluded", "duplicate URL"
        elif norm in syndicated_copy:
            status, reason = "excluded", f"syndicated copy of {syndicated_copy[norm]}"
        elif urlsplit(url).netloc.lower() in PAYWALLED:
            status, reason = "excluded", "paywall or login reader"
        seen.add(norm)

        allowed, note = (None, "")
        if status == "candidate":
            allowed, note = robots_allows(url, robots_cache)
            if allowed is False:
                status, reason = "excluded", "robots.txt disallows our user agent"
            elif note.startswith("robots.txt returned"):
                # site refuses to even show its rules to us, so we stay out
                status, reason = "excluded", note

        rows.append({
            "candidate_id": f"C{i:03d}",
            "player": r["player"],
            "url": url,
            "outlet": r["outlet"],
            "outlet_country": r["outlet_country"],
            "language": r["language"],
            "why_relevant": r["why_relevant"],
            "robots_allowed": "" if allowed is None else str(allowed).lower(),
            "robots_note": note,
            "status": status,
            "exclude_reason": reason,
        })

    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    kept = sum(r["status"] == "candidate" for r in rows)
    print(f"wrote {len(rows)} rows to {OUT.name}: {kept} candidates, {len(rows) - kept} excluded")


if __name__ == "__main__":
    main()
