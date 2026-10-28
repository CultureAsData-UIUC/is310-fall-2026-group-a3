# Tennis nationality switching (Joy's Milestone 2 strand)

DRAFT for Joy to edit.

Part of Group A3's project on how sports become part of national and global culture through TV and digital media. This strand asks:

> How do media frame tennis players who switch national federations, and what does an official dataset's single country code hide about those identities?

Scope: 2008 to 2026, 10 players (6 Russian-born players who moved to Kazakhstan, Kasatkina to Australia, Dzalamidze to Georgia, and Rublev and Sabalenka as neutral athletes).

## Status

As of 2026-10-28:

- [x] `players.csv`: 10 players, each switch fact with a source URL. Shevchenko's year (2024) and Kasatkina's status (permanent residency, plays as AUS) decided 2026-10-28, see notes
- [x] 158 candidates found, 148 fetched, 133 snapshots ok
- [x] **75 items** in the dataset, 7 or 8 per player (2 near duplicates cut in review, IDs kept stable)
- [x] Keyword flags plus AI-drafted provisional codes for every item, checked again in a full read of every article (2026-10-28)
- [x] `check_dataset.py`: 0 structural problems, **75 of 75 rows still need Joy's review**
- [x] Audit preview against Sackmann data (mirror, see `audit_plan.md`)
- [ ] Joy reviews all 75 items and fills `reviewed_by`
- [x] Codebook changes: added `national_claiming` and `multiple_identity`, widened `opportunity_funding` (`codebook.md`)
- [ ] Joy edits the reflection and checks the references through the UIUC library

## File map

| Path | What it is |
|---|---|
| `data/players.csv` | One row per player: from, to, switch year, the source that verifies it, notes on conflicts |
| `data/candidate_seed.csv` | Hand-built list of candidate URLs from web searches |
| `data/candidates.csv` | Seed list after dedupe, syndication and robots.txt checks, with status and reasons |
| `data/snapshot_log.csv` | Every fetch attempt: status, access date, SHA256, page metadata |
| `data/coding_suggestions.csv` | AI-drafted provisional codes and notes per selected item |
| `data/precode_flags.csv` | Keyword hit counts per frame per item |
| `data/tennis_nationality_dataset.csv` | **The dataset.** Schema in `codebook.md` |
| `data/audit_preview.csv` | Sackmann `ioc` codes per player per year |
| `data/audit_match_log.csv` | How each player name matched in the Sackmann players files |
| `snapshots/` | Raw HTML and extracted text. **Gitignored**, stays on your laptop |
| `sackmann_raw/` | Downloaded Sackmann files. **Gitignored**, re-download with the script |
| `scripts/` | The five scripts below |
| `reports/collection_report.html` | Review cards, one per item (no article text, safe to commit) |
| `reports/quality_report.json` | Output of the checks |
| `reports/audit_preview_summary.md` | Auto-written summary of the audit preview |
| `codebook.md` | Fields, frames, examples |
| `collection_notes.md` | Sampling, inclusion and exclusion, both transformations, failures |
| `audit_plan.md` | Sackmann audit and connection plan, timeline to Dec 11 |
| `reflection.md` | Notes for the reflection (Joy writes the final version) |
| `references.md` | Scholarly sources |
| `ai-chat-log.md` | Log of AI-assisted steps (course requirement) |

## How to run

From the repo root, set up the environment once:

```bash
python3 -m venv .venv
.venv/bin/pip install requests beautifulsoup4 pandas trafilatura
```

Then from this folder (`Milestone 2/joy_tennis_nationality/`), using the venv's Python:

```bash
python scripts/find_sources.py      # seed list -> data/candidates.csv (checks robots.txt, ~2 min)
python scripts/snapshot.py          # fetch pages -> snapshots/ + data/snapshot_log.csv (~6 min, skips ones already done)
python scripts/precode.py           # keyword flags + merge suggestions -> data/tennis_nationality_dataset.csv
python scripts/check_dataset.py     # checks -> reports/quality_report.json + reports/collection_report.html
python scripts/audit_preview.py --download   # first time only, fetches Sackmann files (~25 MB)
python scripts/audit_preview.py     # -> data/audit_preview.csv + reports/audit_preview_summary.md
```

To review: open `snapshots/collection_report_with_excerpts.html` (local, has article excerpts) or `reports/collection_report.html`. Mark each card confirm, change or cut, hit **Download review CSV**, then:

```bash
python scripts/check_dataset.py --apply-review ~/Downloads/review.csv
```

That fills `reviewed_by` for confirmed rows and lists the change and cut rows for you to fix by hand in the CSV.

`check_dataset.py` exits with code 1 while there are structural problems. Missing reviews alone don't make it fail, they're counted separately.

## Limits

- **Passing `check_dataset.py` means the file is structurally consistent, not that it's correct.** It checks formats, codebook values and duplicates. It can't tell whether a frame actually fits an article. Only reading can.
- All frame codes are AI suggestions until Joy reviews them (`reviewed_by` blank = not reviewed).
- Keyword flags are crude regex counts in two main languages. They're a pointer, not a measurement.
- Search results depend on the search tool and date (2026-10-28). Another search on another day would turn up a different set.
- Russian-language items were read and paraphrased by the AI assistant. Joy should spot-check them with a translation tool.
- The Sackmann originals were offline when we checked, so the audit preview uses a mirror (details in `audit_plan.md`).
- Snapshots stay local because of copyright, so someone cloning the repo has to re-run `snapshot.py`. Pages may have changed, and the hash will show it.
