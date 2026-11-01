# Audit and connection plan

DRAFT for Joy to edit.

## The existing dataset

Jeff Sackmann's ATP and WTA match and player data (`tennis_atp`, `tennis_wta`, CC BY-NC-SA 4.0). It's the most used open tennis dataset out there, so a lot of tennis analysis inherits whatever it does with nationality.

**Heads up on access.** On 2026-10-28 both original repos (`github.com/JeffSackmann/tennis_atp` and `tennis_wta`) returned 404. For the preview we used a data-only archival mirror, `github.com/Aneeshers/tennis-sackmann-archive`, pinned to commit `8373358735`. The mirror says its ATP and WTA folders come from upstream commits made in June 2026 and it keeps Sackmann's original READMEs. We can't check that against upstream git history because the mirror is a single commit. For the full audit we need to either find out if Sackmann moved the repos or say clearly in the writeup that we audited a mirror.

## What it measures

Files we used (column names confirmed from the actual files, not from memory):

- `atp_players.csv`, `wta_players.csv`: `player_id, name_first, name_last, hand, dob, ioc, height, wikidata_id`. One `ioc` value per player.
- `atp_matches_YYYY.csv`, `wta_matches_YYYY.csv` (2008 to 2026): one row per main draw singles match, with `tourney_date`, `winner_id`, `winner_name`, `winner_ioc`, `loser_id`, `loser_name`, `loser_ioc` and lots of stats we don't need.

So nationality is one three-letter code per player in the players file, plus one code per match appearance. No field for birthplace, citizenship, residence, training base or neutral status.

## How it joins to my dataset

- **Key:** player name to `name_first + name_last` (normalized, with a short alias list for spellings like Andrey/Andrei). All 10 sample players matched exactly one id. The match log is in `data/audit_match_log.csv`.
- **Time:** my `switch_year` and item `pub_date` against `tourney_date` in the match files.
- Long term the cleaner key is `wikidata_id`, which is in the players file and would also let us pull birthplace and citizenship from Wikidata for comparison.

## What the preview found (facts only, see `reports/audit_preview_summary.md`)

- **Players file:** one code each. Kazakhstan wave all `KAZ`. Kasatkina `AUS`. Rublev `RUS`, Sabalenka `BLR`. Dzalamidze `RUS` even though she has played for Georgia since June 2022.
- **Codes backdated in match rows.** For most switchers the match rows use the current code even before the switch. Examples: Rybakina is `KAZ` at Moscow in October 2017 (switch 2018). Shevchenko is `KAZ` in 36 appearances in 2022 and 2023, when he was playing as a neutral (his official switch is January 2024, see `players.csv`). Kasatkina is the one player whose code changes in the match rows: `RUS` through the end of 2024, then `AUS` from Brisbane (tourney date 2024-12-30), which is three months before her March 2025 announcement.
- **No neutral code.** Rublev has 315 appearances from 2022 on coded `RUS` and Sabalenka has 307 coded `BLR`, though neither played under a flag in that period.
- **Coverage gap.** Dzalamidze has zero main draw singles matches in scope because she's mostly a doubles player, so this dataset barely sees her at all.

These are observations from one mirror snapshot. We haven't yet figured out why the codes look like this (for example, whether the files get rebuilt with the latest code each season).

## What to investigate in the full audit

1. **Switch history.** For every switch, find the exact first event under the new flag (from ATP or WTA profiles and news), then count match rows before that date that already carry the new code. That needs date-level switch dates, not just years.
2. **Neutral players.** How many 2022 to 2026 match rows for Russian and Belarusian players carry `RUS`/`BLR`? Compare with what was shown on TV and scoreboards (no flag).
3. **Single code vs multiple identities.** For each player, lay the one `ioc` code next to what my media items mention (birthplace, citizenship, residence, training base, federation, heritage). The `identities_mentioned` field is built for this.
4. **Doubles and lower levels.** Check whether the doubles, qualifying and Challenger files exist in the mirror and whether Dzalamidze shows up there.
5. **Expand the sample.** Use the players file to find every player whose match rows carry two different codes in 2008 to 2026. That's a cheap way to find switchers we missed (Kasatkina showed up that way).

## How to verify against ATP and WTA profiles

For each sample player, open the ATP or WTA profile and note the current flag. Then use the activity or results pages and news items to find the first tournament under the new flag. Record the source URL and access date in `players.csv` (new columns `first_event_new_flag` and `first_event_source`). ATP Tour pages are allowed in robots.txt for our user agent, but some pages load by JavaScript, so this might need to be manual.

## Timeline to Dec 11

| Dates | Work |
|---|---|
| Nov 3 | Milestone 2 in (this folder) |
| Nov 4 to 10 | Joy reviews all items, fixes frames, edits codebook. Try to locate original Sackmann repos |
| Nov 11 to 17 | Date-level switch dates for all 10 players from profiles and news |
| Nov 18 to 24 | Full audit script: pre-switch rows, neutral period rows, multi-code players across the whole files |
| Nov 25 to Dec 1 | Thanksgiving break buffer. Wikidata join for birthplace and citizenship |
| Dec 2 to 8 | Write up findings, tie back to frames, group sync |
| Dec 11 | Final due |
