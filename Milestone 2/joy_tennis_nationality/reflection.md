# Reflection

## What works

The whole pipeline runs from inside my folder with five Python scripts. It starts from a hand-built seed list, checks robots.txt, snapshots each page with a hash, adds keyword flags, merges everything into the dataset and builds the review report. Then the audit preview compares my players against the Sackmann data. Rerunning it is cheap because `snapshot.py` skips pages it already has.

Every switch fact in `players.csv` has a source URL. When sources disagreed, like the month Rybakina switched or whether Kasatkina is a citizen or a permanent resident, the conflict went into the notes instead of getting quietly picked. The copyright setup held up too. There's no article text in the repo, `check_dataset.py` makes sure each evidence note has at most one short quote and the report I committed has no excerpts.

The best part is that the outlet mix shows framing differences I can actually point to. Putintseva gave one podcast interview, and the Russian portal's headline says Russia wouldn't let her train for free while the Kazakh site leads with her praising Kazakhstan. With Kasatkina's switch, Meduza says people back home are calling her a traitor, Mail.ru just reports it and the Australian outlets are all "welcome to the family".

The audit preview found something concrete right away. Sackmann's match rows carry a player's current country code back in time. Rybakina is `KAZ` in 2017, a year before she switched, and Shevchenko is `KAZ` in 36 matches from 2022 and 2023 when he was playing as a neutral. There's no neutral code at all either: Rublev has 315 rows and Sabalenka 307 rows from 2022 on that still say `RUS` and `BLR`. That's basically my research question showing up in the data, since one code per row can't show when someone switched or that they had no flag for years.

## What doesn't work yet

The coding still isn't mine. Claude drafted every code, and the first pass only worked from key sentences pulled out of each article. A second pass read all 77 articles in full and changed 51 rows. It caught real mistakes, like Ovechkin's words being credited to Rublev, a journalist described as American when nothing in the text says that and three Tennishead dates left blank even though they were printed right on the page. That's a lot of fixes for something that looked finished, so I need to go through every row myself before I fill in `reviewed_by`. Right now it's blank on all 77.

The keyword flags match the primary frame on only 51 of 77 items (46 before the full read and the new codes). For crude regex that's not shocking, but it means the flags are good for finding things and useless as a replacement for reading.

The original codebook was missing frames the data kept needing. It now has `national_claiming` for when the old country claims the player anyway, like the Russian federation calling Rybakina "our product", and `multiple_identity` for players framed as belonging to several places, like Golubev calling himself a citizen of the world. `opportunity_funding` also covers a federation recruiting someone now. There's no safety code, so Kasatkina being unsafe in Russia goes under `politics_war` with a note. Items coded `other` went from 8 to 5.

Sources are uneven. Kukushkin and Golubev coverage is older and thinner. I found no Georgian-language items for Dzalamidze, and there's only one Belarusian outlet for Sabalenka and two Australian outlets for Kasatkina.

Page metadata dates aren't reliable. Tennishead stamps its 2010 and 2012 articles with 2018-11-08, which looks like a site migration date. For those three I used the "originally published" date printed in the text, but evergreen pages like the Tennis Majors profile might show an update date and I can't always tell.

The Sackmann repos were offline (both returned 404), so the audit preview uses an archived mirror pinned to one commit. I couldn't check it against the originals.

Switch years are fuzzy too. A Stockholm results graphic showed Shevchenko with a Kazakh flag in October 2022, but the federation only had his request under review then and he started playing for Kazakhstan in January 2024, so `players.csv` keeps 2024. A single `switch_year` has the same problem as a single country code.

## Tech problems

Python's `robotparser` sent its own user agent, got 403s and marked 50 URLs as off limits, so the script had to fetch robots.txt with our real user agent instead. Russian sites with no charset header came back as garbled text until the script switched to the detected encoding. Some sites block scripts outright (Sportskeeda gave a 405 and ATP Tour a 403), so a few good items never got snapshotted.

## Feedback I need

- Is the Sackmann mirror OK for the audit, or should I add another official dataset like ITF or Olympics data as a second check?
- Should the neutral players stay in the sample? Rublev and Sabalenka make the single code point really clearly, but they didn't switch anything themselves.
- Are the two new codes OK, or should my codebook stay closer to the group's shared one?
- Is 7 or 8 items per player enough to say anything per player, or should I analyze by frame and outlet country instead?
- How should I disclose the AI-drafted coding in the final writeup beyond `ai-chat-log.md`?

## Use of AI

I used Claude Code for most of the build. It ran the searches, wrote the scripts, fetched the pages and drafted every code and evidence note. When I asked, it also made the calls on the new codes and on Shevchenko and Kasatkina, and I'm going with those for now. It wrote the first draft of this reflection from notes on what happened. Everything is logged in `ai-chat-log.md`.

It got things wrong along the way. Besides the coding errors above, there were the robots.txt false positives, the encoding bug and a set of codebook example IDs that pointed to the wrong rows. It caught all of those itself when it went back and checked its own work, which is reassuring and also kind of the problem. The review and the final say on every code are still on me.
