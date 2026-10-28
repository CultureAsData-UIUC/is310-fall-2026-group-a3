# Reflection (notes for Joy)

These are raw notes on what actually happened while building this. Joy writes the final reflection in his own words.

## What works

- The pipeline runs end to end from the folder: seed list, robots check, snapshots with hashes, keyword flags, merge, checks, report, audit preview. Re-running is cheap because `snapshot.py` skips pages it already has.
- Every switch fact has a source in `players.csv`, and conflicts are written down instead of picked silently.
- Copyright setup holds up: no article text in the repo, evidence notes are checked for quote length, and the committed report has no excerpts.
- The outlet mix actually shows framing differences. Same Putintseva podcast: the Russian portal headline says Russia wouldn't let her train for free, the Kazakh site leads with her praising Kazakhstan. Same Kasatkina switch: Meduza says she's called a traitor, Mail.ru reports it flat, Australian outlets say "welcome".
- The audit preview found something concrete right away. Sackmann's match rows carry the player's current code back in time (Rybakina `KAZ` in 2017, Shevchenko `KAZ` while playing as a neutral), and there's no neutral code at all (315 Rublev rows and 307 Sabalenka rows from 2022 on still say `RUS`/`BLR`).

## What doesn't work (yet)

- **All codes are AI drafts.** 77 of 77 rows still need review. The reading pass used keyword-selected sentences, not full reads of every article.
- **Keyword flags and AI frames agree on only 46 of 77 primary frames.** That's not shocking for crude regex, but it means the flags can't stand in for reading.
- **The codebook is missing codes the data keeps asking for**: national claiming, safety/exile, multiple identity (see `codebook.md`). `other` is doing too much work (8 primary, 2 secondary).
- **Sources are uneven.** Kukushkin and Golubev coverage is older and thinner. No Georgian-language items for Dzalamidze, one Belarusian outlet for Sabalenka, only 2 Australian outlets for Kasatkina.
- **Pub dates from page metadata aren't always right.** Tennishead stamps 2010-era articles with 2018-11-08. We blanked 3 dates, but there could be more evergreen pages (Tennis Majors profile) with update dates instead of publish dates.
- **The Sackmann originals were offline.** The preview uses a mirror we can't fully verify.
- **Switch years are fuzzy.** Shevchenko played Stockholm under the Kazakh flag in October 2022 per a KTF statement, but most outlets say January 2024. A single `switch_year` has the same problem as a single country code.

## Tech problems hit along the way

- Python's `robotparser` sent its own user agent, got 403s and treated 50 URLs as disallowed. Fixed by fetching robots.txt with our real user agent.
- Russian sites with no charset header came back as mojibake. Fixed by using the detected encoding.
- Several sites block scripts outright (Sportskeeda 405, ATP Tour 403), so some good items couldn't be snapshotted at all.

## Feedback I need

- Is a mirror of the Sackmann data OK for the audit, or should we look for another official-style dataset (ITF, Olympics) as a second check?
- Should neutral players stay in the sample? They make the "single code" point really clearly, but they didn't switch anything themselves.
- Should I add the suggested codes (national claiming, safety/exile, multiple identity), or keep the codebook small and lean on `uncertainty_note`?
- Is 7 or 8 items per player enough to say anything per player, or should the analysis be per frame and per outlet country instead?
- How should AI-drafted coding be cited or disclosed in the final writeup beyond `ai-chat-log.md`?

## Use of AI

- Claude Code ran the searches, wrote the scripts, fetched the pages and drafted every code and note. See `ai-chat-log.md`.
- Things it got wrong that got caught: the robots.txt false positives, the encoding bug, and a first set of codebook example IDs that pointed to the wrong rows (fixed by looking them up).
