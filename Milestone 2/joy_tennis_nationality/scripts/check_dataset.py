"""Phases 4 and 5: validate the dataset and build the review report.

Standard library only. Checks tennis_nationality_dataset.csv for

  * unique, well formed item_id values (TEN001...)
  * required fields present
  * values that exist in the codebook (frames, item_type, identities, yes/no)
  * date formats (YYYY-MM-DD, real calendar dates)
  * URL format and duplicate URLs
  * snapshot hash format
  * switch facts that match players.csv
  * evidence notes that stay inside the copyright rule (one quote, under 15 words)
  * rows still missing Joy's review

Passing means the file is structurally consistent. It does NOT mean the
codes are correct. Only reading the sources can tell you that.

Writes reports/quality_report.json and rebuilds two copies of the review report:
    reports/collection_report.html                   committed, no snapshot text
    snapshots/collection_report_with_excerpts.html   local only (gitignored), adds excerpts

Run from the joy_tennis_nationality folder:
    python scripts/check_dataset.py
    python scripts/check_dataset.py --apply-review ~/Downloads/review.csv
"""

import argparse
import csv
import datetime as dt
import html
import json
import re
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit

BASE = Path(__file__).resolve().parent.parent
DATASET = BASE / "data" / "tennis_nationality_dataset.csv"
PLAYERS = BASE / "data" / "players.csv"
SNAP = BASE / "snapshots"
REPORTS = BASE / "reports"

FRAMES = {"opportunity_funding", "pragmatic_career", "loyalty_betrayal", "politics_war",
          "belonging_homecoming", "flag_of_convenience", "national_claiming",
          "multiple_identity", "other"}
ITEM_TYPES = {"article", "interview", "statement", "profile"}
IDENTITIES = {"birthplace", "citizenship", "residence", "training_base", "federation", "heritage"}
YES_NO = {"yes", "no"}
REQUIRED = ["item_id", "player_id", "player", "from_nation", "to_nation", "outlet", "outlet_country", "url",
            "access_date", "item_type", "language", "snapshot_sha256", "evidence_note",
            "frame_primary", "money_mentioned", "player_voice"]
QUOTE_RE = re.compile(r"[\"“«]([^\"”»]+)[\"”»]")


def valid_date(s):
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        return False
    try:
        dt.date.fromisoformat(s)
        return True
    except ValueError:
        return False


def check(rows, players):
    problems = []  # (item_id, check, message)

    def bad(row, name, msg):
        problems.append({"item_id": row.get("item_id", "?"), "check": name, "message": msg})

    ids = Counter(r["item_id"] for r in rows)
    urls = Counter(r["url"].strip().rstrip("/").lower() for r in rows)
    for r in rows:
        if not re.fullmatch(r"TEN\d{3}", r["item_id"]):
            bad(r, "id_format", f"item_id '{r['item_id']}' is not TEN + 3 digits")
        if ids[r["item_id"]] > 1:
            bad(r, "id_unique", "item_id used more than once")
        for f in REQUIRED:
            if not r.get(f, "").strip():
                bad(r, "required", f"{f} is blank")

        for f in ("frame_primary", "frame_secondary"):
            v = r.get(f, "")
            if v and v not in FRAMES:
                bad(r, "codebook", f"{f} '{v}' is not a codebook value")
        if r["frame_primary"] and r["frame_primary"] == r["frame_secondary"]:
            bad(r, "codebook", "frame_secondary repeats frame_primary")
        if "other" in (r["frame_primary"], r["frame_secondary"]) and not r["uncertainty_note"].strip():
            bad(r, "codebook", "frame 'other' needs an explanation in uncertainty_note")
        if r["item_type"] and r["item_type"] not in ITEM_TYPES:
            bad(r, "codebook", f"item_type '{r['item_type']}' not allowed")
        for ident in filter(None, r["identities_mentioned"].split("|")):
            if ident not in IDENTITIES:
                bad(r, "codebook", f"identity '{ident}' not allowed")
        for f in ("money_mentioned", "player_voice"):
            if r[f] and r[f] not in YES_NO:
                bad(r, "codebook", f"{f} must be yes or no")
        for f in ("from_nation", "to_nation"):
            if r[f] and not re.fullmatch(r"[A-Z]{3}|NEUTRAL", r[f]):
                bad(r, "nation_code", f"{f} '{r[f]}' is not a 3 letter code or NEUTRAL")

        if r["pub_date"] and not valid_date(r["pub_date"]):
            bad(r, "date_format", f"pub_date '{r['pub_date']}' is not a real YYYY-MM-DD date")
        if r["access_date"] and not valid_date(r["access_date"]):
            bad(r, "date_format", f"access_date '{r['access_date']}' is not a real YYYY-MM-DD date")
        if r["pub_date"] and r["access_date"] and valid_date(r["pub_date"]) \
                and valid_date(r["access_date"]) and r["pub_date"] > r["access_date"]:
            bad(r, "date_order", "pub_date is after access_date")

        parts = urlsplit(r["url"])
        if parts.scheme not in ("http", "https") or not parts.netloc:
            bad(r, "url_format", f"url '{r['url']}' is not a full http(s) URL")
        if urls[r["url"].strip().rstrip("/").lower()] > 1:
            bad(r, "url_duplicate", "same URL appears on another row")
        if r["snapshot_sha256"] and not re.fullmatch(r"[0-9a-f]{64}", r["snapshot_sha256"]):
            bad(r, "hash_format", "snapshot_sha256 is not 64 hex characters")

        p = _find_player(players, r)
        if p and not _written_matches(r):
            bad(r, "player_facts", f"player '{r['player']}' does not look like player_id '{r['player_id']}'")
        if p is None:
            bad(r, "player_facts", f"player_id '{r['player_id']}' not found in players.csv")
        else:
            for f in ("from_nation", "to_nation", "switch_year"):
                if r[f] != p[f]:
                    bad(r, "player_facts", f"{f} '{r[f]}' does not match players.csv '{p[f]}'")

        quotes = QUOTE_RE.findall(r["evidence_note"])
        if len(quotes) > 1:
            bad(r, "copyright", f"evidence_note has {len(quotes)} quotes, max is 1")
        for q in quotes:
            if len(q.split()) >= 15:
                bad(r, "copyright", f"quote is {len(q.split())} words, must be under 15")

        if not r["reviewed_by"].strip():
            bad(r, "review", "not reviewed yet")
    return problems


# 'player' is kept as written in the source, so Russian items use Cyrillic.
# 'player_id' is the canonical Latin name. These surname stems check the two agree.
PLAYER_STEMS = {
    "Elena Rybakina": ["rybakin", "рыбакин"],
    "Alexander Bublik": ["bublik", "бублик"],
    "Yulia Putintseva": ["putintsev", "путинцев"],
    "Mikhail Kukushkin": ["kukushkin", "кукушкин"],
    "Andrey Golubev": ["golubev", "голубев"],
    "Alexander Shevchenko": ["shevchenko", "шевченко"],
    "Daria Kasatkina": ["kasatkin", "касаткин"],
    "Natela Dzalamidze": ["dzalamidze", "дзаламидзе"],
    "Andrey Rublev": ["rublev", "рублев", "рублёв"],
    "Aryna Sabalenka": ["sabalenk", "соболенк", "сабаленк"],
}


def _find_player(players, row):
    """player_id is the canonical Latin name, so it keys straight into players.csv."""
    return players.get(row.get("player_id", ""))


def _written_matches(row):
    """The as-written name should contain one of the player_id's surname stems."""
    written = row["player"].lower()
    return any(s in written for s in PLAYER_STEMS.get(row["player_id"], []))


_SNAP_BY_HASH = None


def excerpt(sha):
    """Opening ~120 words of the local snapshot whose text hash matches."""
    global _SNAP_BY_HASH
    if _SNAP_BY_HASH is None:
        import hashlib
        _SNAP_BY_HASH = {}
        for txt in SNAP.glob("C*.txt"):
            data = txt.read_text(encoding="utf-8")
            _SNAP_BY_HASH[hashlib.sha256(data.encode("utf-8")).hexdigest()] = data
    words = _SNAP_BY_HASH.get(sha, "").split()
    return " ".join(words[:120]) + (" ..." if len(words) > 120 else "")


def build_report(rows, problems, path, with_excerpts):
    by_item = {}
    for p in problems:
        by_item.setdefault(p["item_id"], []).append(p)
    cards = []
    for r in rows:
        probs = [p for p in by_item.get(r["item_id"], []) if p["check"] != "review"]
        reviewed = r["reviewed_by"].strip()
        ex = ""
        if with_excerpts:
            ex_text = excerpt(r["snapshot_sha256"])
            ex = f'<details><summary>Snapshot excerpt</summary><p class="ex">{html.escape(ex_text)}</p></details>' \
                if ex_text else '<p class="muted">no local snapshot found</p>'
        flags = "".join(f'<span class="tag">{html.escape(f)}</span>' for f in r["keyword_flags"].split("|") if f)
        ids = ", ".join(r["identities_mentioned"].split("|")) or "none"
        prob_html = "".join(f"<li>{html.escape(p['message'])}</li>" for p in probs)
        cards.append(f"""
<article class="card" data-id="{html.escape(r['item_id'])}" data-player="{html.escape(r['player_id'] + ' ' + r['player'])}">
  <header>
    <span class="id">{html.escape(r['item_id'])}</span>
    <span class="player">{html.escape(r['player_id'])}</span> <span class="as-written">({html.escape(r['player'])})</span>
    <span class="muted">{html.escape(r['from_nation'])} &rarr; {html.escape(r['to_nation'])} ({html.escape(r['switch_year'] or '?')})</span>
    <span class="status {'done' if reviewed else 'todo'}">{('reviewed by ' + html.escape(reviewed)) if reviewed else 'not reviewed'}</span>
  </header>
  <p><a href="{html.escape(r['url'])}" target="_blank" rel="noopener">{html.escape(r['outlet'])}</a>
     <span class="muted">{html.escape(r['outlet_country'])} &middot; {html.escape(r['language'])} &middot; {html.escape(r['item_type'])} &middot; pub {html.escape(r['pub_date'] or 'unknown')} &middot; accessed {html.escape(r['access_date'])}</span></p>
  <p class="note">{html.escape(r['evidence_note'])}</p>
  {ex}
  <dl>
    <dt>Suggested frames</dt><dd><b>{html.escape(r['frame_primary'])}</b>{(' + ' + html.escape(r['frame_secondary'])) if r['frame_secondary'] else ''}</dd>
    <dt>Keyword flags</dt><dd>{flags or '<span class="muted">none</span>'}</dd>
    <dt>Identities</dt><dd>{html.escape(ids)}</dd>
    <dt>Money / voice</dt><dd>{html.escape(r['money_mentioned'])} / {html.escape(r['player_voice'])}</dd>
    <dt>Uncertainty</dt><dd>{html.escape(r['uncertainty_note'] or '-')}</dd>
  </dl>
  {('<ul class="probs">' + prob_html + '</ul>') if prob_html else ''}
  <div class="review">
    <label>Review <select class="rv-status"><option value="">-</option><option>confirm</option><option>change</option><option>cut</option></select></label>
    <input class="rv-note" placeholder="what to change">
  </div>
</article>""")

    counts = Counter(p["check"] for p in problems)
    n_struct = sum(v for k, v in counts.items() if k != "review")
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Tennis Nationality Review</title>
<style>
:root {{ --bg:#fafaf7; --fg:#1d1d1b; --muted:#6b6b66; --card:#fff; --line:#e3e2dc; --accent:#2a5bd7; --warn:#b4471f; --ok:#2f7a3d; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg:#161614; --fg:#ecebe6; --muted:#9a9a93; --card:#1f1f1c; --line:#33332f; --accent:#8fb0ff; --warn:#f08a62; --ok:#7cc48a; }} }}
body {{ background:var(--bg); color:var(--fg); font:15px/1.5 system-ui, sans-serif; margin:0; padding:16px; }}
main {{ max-width:860px; margin:0 auto; }}
h1 {{ font-size:1.4rem; margin:.2rem 0; }}
.card {{ background:var(--card); border:1px solid var(--line); border-radius:8px; padding:12px 14px; margin:12px 0; }}
.card header {{ display:flex; flex-wrap:wrap; gap:8px; align-items:baseline; }}
.id {{ font-family:ui-monospace, monospace; font-weight:600; }}
.player {{ font-weight:600; }}
.muted {{ color:var(--muted); font-size:.9em; }}
.status {{ margin-left:auto; font-size:.85em; }} .status.todo {{ color:var(--warn); }} .status.done {{ color:var(--ok); }}
.note {{ margin:.4rem 0; }}
.ex {{ color:var(--muted); font-size:.9em; white-space:pre-wrap; }}
dl {{ display:grid; grid-template-columns:max-content 1fr; gap:2px 12px; margin:.4rem 0; }}
dt {{ color:var(--muted); }} dd {{ margin:0; }}
.tag {{ display:inline-block; border:1px solid var(--line); border-radius:4px; padding:0 5px; margin:0 4px 2px 0; font-size:.85em; }}
.probs {{ color:var(--warn); margin:.3rem 0; }}
.review {{ display:flex; flex-wrap:wrap; gap:8px; border-top:1px solid var(--line); padding-top:8px; }}
.review input {{ flex:1; min-width:160px; }}
a {{ color:var(--accent); }}
.bar {{ position:sticky; top:0; background:var(--bg); padding:8px 0; display:flex; flex-wrap:wrap; gap:8px; align-items:center; border-bottom:1px solid var(--line); }}
</style></head><body><main>
<h1>Tennis nationality items: review</h1>
<p class="muted">{len(rows)} items. Codes are AI suggestions until reviewed. {n_struct} structural problems, {counts.get('review', 0)} rows not reviewed.
{'This copy includes snapshot excerpts and stays local.' if with_excerpts else 'This copy has no snapshot text so it can be committed. Run check_dataset.py locally for the version with excerpts.'}</p>
<div class="bar">
  <label>Reviewer <input id="who" size="10" placeholder="Joy"></label>
  <input id="filter" placeholder="filter by player">
  <button id="export">Download review CSV</button>
  <span id="count" class="muted"></span>
</div>
{''.join(cards)}
</main>
<script>
// Review choices are kept in this browser only, then exported as a CSV that
// check_dataset.py --apply-review reads. Nothing is sent anywhere.
const KEY = "tennis-review-v1";
let saved = {{}};
try {{ saved = JSON.parse(localStorage.getItem(KEY) || "{{}}"); }} catch (e) {{}}
const save = () => {{ try {{ localStorage.setItem(KEY, JSON.stringify(saved)); }} catch (e) {{}} }};
const who = document.getElementById("who");
who.value = saved.__who || "";
who.addEventListener("input", () => {{ saved.__who = who.value; save(); }});
document.querySelectorAll(".card").forEach(card => {{
  const id = card.dataset.id, s = card.querySelector(".rv-status"), n = card.querySelector(".rv-note");
  if (saved[id]) {{ s.value = saved[id].status || ""; n.value = saved[id].note || ""; }}
  const upd = () => {{ saved[id] = {{status: s.value, note: n.value}}; save(); tally(); }};
  s.addEventListener("change", upd); n.addEventListener("input", upd);
}});
function tally() {{
  const done = Object.keys(saved).filter(k => k !== "__who" && saved[k].status).length;
  document.getElementById("count").textContent = done + " of {len(rows)} marked";
}}
tally();
document.getElementById("filter").addEventListener("input", e => {{
  const q = e.target.value.toLowerCase();
  document.querySelectorAll(".card").forEach(c => c.style.display = c.dataset.player.toLowerCase().includes(q) ? "" : "none");
}});
document.getElementById("export").addEventListener("click", () => {{
  const esc = v => '"' + String(v).replace(/"/g, '""') + '"';
  const lines = ["item_id,status,note,reviewer"];
  for (const [k, v] of Object.entries(saved)) if (k !== "__who" && v.status) lines.push([k, v.status, v.note, who.value].map(esc).join(","));
  const a = document.createElement("a");
  a.href = URL.createObjectURL(new Blob([lines.join("\\n")], {{type: "text/csv"}}));
  a.download = "review.csv"; a.click();
}});
</script></body></html>"""
    path.write_text(page, encoding="utf-8")


def apply_review(rows, review_path):
    """Fill reviewed_by from the report's exported CSV. Codes are not changed here,
    'change' and 'cut' rows are listed so Joy edits them by hand."""
    with open(review_path, encoding="utf-8") as f:
        review = {r["item_id"]: r for r in csv.DictReader(f)}
    todo = []
    for r in rows:
        rv = review.get(r["item_id"])
        if not rv or not rv["reviewer"].strip():
            continue
        if rv["status"] == "confirm":
            r["reviewed_by"] = rv["reviewer"].strip()
        else:
            todo.append(f"{r['item_id']} {rv['status']}: {rv['note']}")
    return todo


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply-review", help="review.csv exported from the HTML report")
    args = ap.parse_args()

    with DATASET.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames
        rows = list(reader)
    with PLAYERS.open(encoding="utf-8") as f:
        players = {r["player"]: r for r in csv.DictReader(f)}

    if args.apply_review:
        todo = apply_review(rows, args.apply_review)
        with DATASET.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)
        print("reviewed_by filled for confirmed rows. Rows to fix by hand:")
        print("\n".join(todo) or "  none")

    problems = check(rows, players)
    counts = Counter(p["check"] for p in problems)
    structural = [p for p in problems if p["check"] != "review"]
    report = {
        "generated": dt.datetime.now().isoformat(timespec="seconds"),
        "dataset": str(DATASET.relative_to(BASE)),
        "rows": len(rows),
        "players": dict(Counter(r["player_id"] for r in rows)),
        "frame_primary_counts": dict(Counter(r["frame_primary"] for r in rows)),
        "structurally_consistent": not structural,
        "rows_missing_review": counts.get("review", 0),
        "problem_counts": dict(counts),
        "problems": structural,
        "note": "Passing means structurally consistent, not correct. Codes need human review.",
    }
    REPORTS.mkdir(exist_ok=True)
    (REPORTS / "quality_report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False),
                                                 encoding="utf-8")
    build_report(rows, problems, REPORTS / "collection_report.html", with_excerpts=False)
    if SNAP.exists():
        build_report(rows, problems, SNAP / "collection_report_with_excerpts.html", with_excerpts=True)

    print(f"{len(rows)} rows, {len(structural)} structural problems, "
          f"{counts.get('review', 0)} rows missing review")
    for p in structural[:20]:
        print(f"  {p['item_id']} [{p['check']}] {p['message']}")
    return 0 if not structural else 1


if __name__ == "__main__":
    raise SystemExit(main())
