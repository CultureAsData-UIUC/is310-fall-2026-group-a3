"""Phase 2, transformation 1: web page -> saved snapshot + extracted text.

Reads data/candidates.csv, fetches every row whose status is "candidate"
or "approved", and for each one saves

    snapshots/<candidate_id>.html   raw HTML (gitignored, stays local)
    snapshots/<candidate_id>.txt    main text pulled out with trafilatura

Every attempt, including failures, goes into data/snapshot_log.csv with the
access date, HTTP status, SHA256 of the saved text and whatever title,
site name and publication date the page metadata gives us. Nothing is
silently dropped.

Run from the joy_tennis_nationality folder:
    python scripts/snapshot.py            # skips rows already snapshotted
    python scripts/snapshot.py --refresh  # fetch everything again
"""

import argparse
import csv
import datetime as dt
import hashlib
import time
from pathlib import Path

import requests
import trafilatura

BASE = Path(__file__).resolve().parent.parent
CANDIDATES = BASE / "data" / "candidates.csv"
LOG = BASE / "data" / "snapshot_log.csv"
SNAP = BASE / "snapshots"

USER_AGENT = (
    "IS310-CultureAsData-student-research/0.1 "
    "(UIUC course project; +https://github.com/CultureAsData-UIUC/is310-fall-2026-group-a3)"
)
DELAY = 2          # seconds between requests, per the project rules
MIN_CHARS = 400    # less extracted text than this usually means a block page or a stub

# Phrases that show up on paywall or consent walls. If the extracted text is
# short and contains one of these we mark it paywalled and do not use it.
PAYWALL_HINTS = [
    "subscribe to continue", "subscribe to read", "to continue reading",
    "already a subscriber", "this article is for subscribers",
    "оформите подписку", "доступно только подписчикам",
]

LOG_FIELDS = [
    "candidate_id", "player", "url", "final_url", "http_status", "fetch_status",
    "access_date", "snapshot_sha256", "text_chars", "meta_title", "meta_sitename",
    "meta_pub_date", "duplicate_of", "note",
]


def sha256(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def fetch(row, session):
    entry = {k: "" for k in LOG_FIELDS}
    entry.update(candidate_id=row["candidate_id"], player=row["player"], url=row["url"],
                 access_date=dt.date.today().isoformat())
    try:
        resp = session.get(row["url"], timeout=30, allow_redirects=True)
    except requests.Timeout:
        entry.update(fetch_status="timeout")
        return entry
    except requests.RequestException as e:
        entry.update(fetch_status="request_error", note=type(e).__name__)
        return entry

    entry.update(http_status=resp.status_code, final_url=resp.url)
    if resp.status_code >= 400:
        entry.update(fetch_status="http_error")
        return entry
    if "html" not in resp.headers.get("Content-Type", ""):
        entry.update(fetch_status="not_html", note=resp.headers.get("Content-Type", ""))
        return entry

    # requests falls back to ISO-8859-1 when the header has no charset, which
    # turns Cyrillic pages into mojibake. Use the detected encoding instead.
    if "charset" not in resp.headers.get("Content-Type", "").lower():
        resp.encoding = resp.apparent_encoding
    html = resp.text
    text = trafilatura.extract(html, url=resp.url, include_comments=False,
                               include_tables=False, favor_precision=True) or ""
    meta = trafilatura.extract_metadata(html, default_url=resp.url)

    cid = row["candidate_id"]
    (SNAP / f"{cid}.html").write_text(html, encoding="utf-8")
    (SNAP / f"{cid}.txt").write_text(text, encoding="utf-8")

    entry.update(
        snapshot_sha256=sha256(text),
        text_chars=len(text),
        meta_title=(meta.title or "") if meta else "",
        meta_sitename=(meta.sitename or "") if meta else "",
        meta_pub_date=(meta.date or "") if meta else "",
    )
    low = text.lower()
    if len(text) < MIN_CHARS and any(h in low for h in PAYWALL_HINTS):
        entry.update(fetch_status="paywalled")
    elif len(text) < MIN_CHARS:
        entry.update(fetch_status="too_short", note="extracted text under 400 chars")
    else:
        entry.update(fetch_status="ok")
    return entry


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true", help="refetch rows already logged as ok")
    args = ap.parse_args()

    SNAP.mkdir(exist_ok=True)
    with CANDIDATES.open(encoding="utf-8") as f:
        todo = [r for r in csv.DictReader(f) if r["status"] in ("candidate", "approved")]

    old = {}
    if LOG.exists():
        with LOG.open(encoding="utf-8") as f:
            old = {r["candidate_id"]: r for r in csv.DictReader(f)}

    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT,
                            "Accept-Language": "en,ru;q=0.8,*;q=0.5"})
    log = []
    for i, row in enumerate(todo, 1):
        prev = old.get(row["candidate_id"])
        if prev and prev["fetch_status"] == "ok" and not args.refresh \
                and (SNAP / f"{row['candidate_id']}.txt").exists():
            log.append(prev)
            continue
        entry = fetch(row, session)
        print(f"[{i}/{len(todo)}] {row['candidate_id']} {entry['fetch_status']} "
              f"{entry['http_status']} {entry['text_chars']} chars")
        log.append(entry)
        time.sleep(DELAY)

    # identical extracted text on two URLs = syndicated copy we missed earlier
    first_seen = {}
    for e in log:
        e["duplicate_of"] = ""
        if e["fetch_status"] == "ok":
            h = e["snapshot_sha256"]
            if h in first_seen:
                e["duplicate_of"] = first_seen[h]
            else:
                first_seen[h] = e["candidate_id"]

    with LOG.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=LOG_FIELDS)
        w.writeheader()
        w.writerows(log)

    counts = {}
    for e in log:
        counts[e["fetch_status"]] = counts.get(e["fetch_status"], 0) + 1
    print("done:", counts)


if __name__ == "__main__":
    main()
