"""Phase 6: audit preview against Jeff Sackmann's ATP and WTA data.

Question for the preview: what country code does the official-style dataset
give each sample player, and does that code change across years in the
match files?

Source note: the original repos github.com/JeffSackmann/tennis_atp and
tennis_wta returned 404 on 2026-10-28. This script uses the data-only
archival mirror github.com/Aneeshers/tennis-sackmann-archive, pinned to one
commit so the run is repeatable. The mirror says its atp/ and wta/ folders
are snapshots of upstream commits from June 2026. We could not check that
against upstream history, so treat it as a mirror, not the original.

Run from the joy_tennis_nationality folder:
    python scripts/audit_preview.py --download   # first time, fetches ~25 MB
    python scripts/audit_preview.py

Outputs:
    data/audit_preview.csv          one row per player x year x ioc code seen
    data/audit_match_log.csv        how each sample name was matched (or not)
    reports/audit_preview_summary.md  short factual summary, no conclusions
"""

import argparse
import csv
import time
import unicodedata
import urllib.request
from collections import defaultdict
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent.parent
RAW = BASE / "sackmann_raw"
DATA = BASE / "data"
REPORTS = BASE / "reports"

MIRROR = "Aneeshers/tennis-sackmann-archive"
MIRROR_COMMIT = "83733587353df8a41f2fd4f516147d5aa83f5a8d"
YEARS = range(2008, 2027)  # project scope 2008 to 2026

# Sample players with the tour they play on. Aliases cover common
# transliterations so a spelling difference does not look like a missing player.
SAMPLE = [
    ("Elena Rybakina", "wta", ["Elena Rybakina", "Yelena Rybakina"]),
    ("Alexander Bublik", "atp", ["Alexander Bublik", "Aleksandr Bublik"]),
    ("Yulia Putintseva", "wta", ["Yulia Putintseva", "Iuliia Putintseva"]),
    ("Mikhail Kukushkin", "atp", ["Mikhail Kukushkin"]),
    ("Andrey Golubev", "atp", ["Andrey Golubev", "Andrei Golubev"]),
    ("Alexander Shevchenko", "atp", ["Alexander Shevchenko", "Aleksandr Shevchenko"]),
    ("Daria Kasatkina", "wta", ["Daria Kasatkina", "Darya Kasatkina"]),
    ("Natela Dzalamidze", "wta", ["Natela Dzalamidze"]),
    ("Andrey Rublev", "atp", ["Andrey Rublev", "Andrei Rublev"]),
    ("Aryna Sabalenka", "wta", ["Aryna Sabalenka", "Arina Sabalenka"]),
]


def download():
    for tour in ("atp", "wta"):
        (RAW / tour).mkdir(parents=True, exist_ok=True)
        files = [f"{tour}_players.csv"] + [f"{tour}_matches_{y}.csv" for y in YEARS]
        for name in files:
            url = f"https://raw.githubusercontent.com/{MIRROR}/{MIRROR_COMMIT}/{tour}/{name}"
            print("get", url)
            urllib.request.urlretrieve(url, RAW / tour / name)
            time.sleep(1)


def norm(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    return " ".join(s.lower().replace("-", " ").split())


def match_players(players, canonical, aliases):
    """Exact full-name match on any alias. If none, fall back to last name and log it."""
    full = (players["name_first"].fillna("") + " " + players["name_last"].fillna("")).map(norm)
    wanted = {norm(a) for a in aliases}
    hit = players[full.isin(wanted)]
    if len(hit) == 1:
        return hit, "exact"
    if len(hit) > 1:
        return hit, f"ambiguous: {len(hit)} exact name matches"
    last = norm(canonical.split()[-1])
    hit = players[players["name_last"].map(norm) == last]
    return hit, f"no exact match; {len(hit)} last-name matches (not used)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--download", action="store_true")
    args = ap.parse_args()
    if args.download:
        download()

    with (DATA / "players.csv").open(encoding="utf-8") as f:
        switch_facts = {r["player"]: r for r in csv.DictReader(f)}

    out_rows, log_rows = [], []
    summary = []
    for tour in ("atp", "wta"):
        players = pd.read_csv(RAW / tour / f"{tour}_players.csv", dtype=str)
        matches = pd.concat(
            [pd.read_csv(RAW / tour / f"{tour}_matches_{y}.csv", dtype=str,
                         usecols=["tourney_date", "tourney_name", "winner_id", "winner_ioc",
                                  "loser_id", "loser_ioc"])
             for y in YEARS if (RAW / tour / f"{tour}_matches_{y}.csv").exists()],
            ignore_index=True,
        )
        # one row per player appearance, whichever side of the match they were on
        apps = pd.concat([
            matches.rename(columns={"winner_id": "pid", "winner_ioc": "ioc"})[["tourney_date", "tourney_name", "pid", "ioc"]],
            matches.rename(columns={"loser_id": "pid", "loser_ioc": "ioc"})[["tourney_date", "tourney_name", "pid", "ioc"]],
        ])
        apps["year"] = apps["tourney_date"].str[:4]
        apps["ioc"] = apps["ioc"].fillna("(blank)")

        for canonical, ptour, aliases in SAMPLE:
            if ptour != tour:
                continue
            hit, how = match_players(players, canonical, aliases)
            log_rows.append({
                "player": canonical, "tour": tour, "match_method": how,
                "player_ids": "|".join(hit["player_id"]),
                "names_found": "|".join(hit["name_first"].fillna("") + " " + hit["name_last"].fillna("")),
                "players_file_ioc": "|".join(hit["ioc"].fillna("(blank)")),
            })
            if how != "exact":
                summary.append(f"- **{canonical}**: {how}. Left out of the year table.")
                continue
            pid = hit["player_id"].iloc[0]
            pfile_ioc = hit["ioc"].fillna("(blank)").iloc[0]
            mine = apps[apps["pid"] == pid]
            per = mine.groupby(["year", "ioc"]).agg(
                matches=("ioc", "size"),
                first_date=("tourney_date", "min"),
                last_date=("tourney_date", "max"),
            ).reset_index()
            for _, r in per.iterrows():
                out_rows.append({
                    "player": canonical, "tour": tour, "player_id": pid,
                    "players_file_ioc": pfile_ioc, "year": r["year"], "match_ioc": r["ioc"],
                    "matches": r["matches"], "first_tourney_date": r["first_date"],
                    "last_tourney_date": r["last_date"],
                })
            # order the codes by when they first appear, to show any changes
            seq = mine.sort_values("tourney_date").drop_duplicates("ioc")
            codes = ", ".join(f"{c} (first {d[:4]}-{d[4:6]}-{d[6:]})"
                              for c, d in zip(seq["ioc"], seq["tourney_date"]))
            years = sorted(mine["year"].unique())
            span = f"{years[0]} to {years[-1]}" if years else "no main-draw matches in scope"
            line = (
                f"- **{canonical}** ({tour.upper()} id {pid}): players file says `{pfile_ioc}`. "
                f"Match rows {span}, {len(mine)} appearances. Codes in match rows: {codes or 'none'}."
            )
            # compare with the verified switch facts in players.csv
            fact = switch_facts.get(canonical)
            if fact and fact["switch_year"] and len(mine):
                sy = fact["switch_year"]
                if fact["to_nation"] == "NEUTRAL":
                    n = int(((mine["year"] >= sy) & (mine["ioc"] == fact["from_nation"])).sum())
                    line += (f" Appearances from {sy} on (neutral period per players.csv) coded "
                             f"`{fact['from_nation']}`: {n}.")
                else:
                    n = int(((mine["year"] < sy) & (mine["ioc"] == fact["to_nation"])).sum())
                    line += (f" Appearances before {sy} (switch year per players.csv) already coded "
                             f"`{fact['to_nation']}`: {n}.")
            summary.append(line)

    with (DATA / "audit_preview.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["player", "tour", "player_id", "players_file_ioc", "year",
                                          "match_ioc", "matches", "first_tourney_date", "last_tourney_date"])
        w.writeheader()
        w.writerows(out_rows)
    with (DATA / "audit_match_log.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(log_rows[0].keys()))
        w.writeheader()
        w.writerows(log_rows)

    REPORTS.mkdir(exist_ok=True)
    (REPORTS / "audit_preview_summary.md").write_text(
        "# Audit preview summary (auto generated)\n\n"
        f"Source: `{MIRROR}` at commit `{MIRROR_COMMIT[:10]}`, main-draw match files "
        f"{YEARS.start} to {YEARS.stop - 1}. The original Sackmann repos were offline (404) on 2026-10-28.\n\n"
        "What each line shows: the single `ioc` value in the players file, then every distinct "
        "`winner_ioc`/`loser_ioc` value attached to that player in match rows, in the order they first appear.\n"
        "Main-draw singles files only, so Challenger, ITF, qualifying and doubles matches are not counted.\n"
        "`tourney_date` is the tournament start date, not the match date.\n\n"
        + "\n".join(summary) + "\n",
        encoding="utf-8",
    )
    print(f"{len(out_rows)} player-year-code rows -> data/audit_preview.csv")
    print("\n".join(summary))


if __name__ == "__main__":
    main()
