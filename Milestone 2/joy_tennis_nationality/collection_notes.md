# Collection notes

DRAFT for Joy to edit. This is the paper trail for how the dataset got built.

## Sampling

**Players (10).** Picked to cover three kinds of switch:

- Kazakhstan wave (6): Rybakina, Bublik, Putintseva, Kukushkin, Golubev, Shevchenko. All Russian-born, all moved to the Kazakhstan Tennis Federation between 2008 and 2024.
- Recent switches (2): Kasatkina (RUS to AUS, 2025), Dzalamidze (RUS to GEO, 2022).
- Neutral flag (2): Rublev and Sabalenka. They didn't switch anything, the tours took their flags away in March 2022. They're in the sample as a contrast: a nationality change done *to* a player instead of *by* one.

**Switch facts.** Every `from_nation`, `to_nation` and `switch_year` in `data/players.csv` has a source URL. Where sources disagreed (month of Rybakina's and Putintseva's switches, Golubev's age, whether Kasatkina is a citizen or a permanent resident) the disagreement is written in `notes` and nothing was picked silently.

**Items.** Target 7 to 8 per player, about 75 total, mixing outlets from the old country (mostly Russian), the new country (mostly Kazakh, Australian) and international (wire services, UK/US tennis sites, Asian and Gulf papers that carry AFP and Reuters).

## How candidates were found

1. Web searches run through the AI assistant (Claude Code's search tool) on 2026-10-28, in English and Russian, plus one Georgian query. Queries mixed the player name with words like switch, citizenship, federation, neutral, flag, and the Russian equivalents (гражданство, переход, федерация, нейтральный флаг). The full list of queries is in `ai-chat-log.md`.
2. Every URL in `data/candidate_seed.csv` came from a search result. No URLs were typed in from memory.
3. `scripts/find_sources.py` cleaned the seed list into `data/candidates.csv` (154 rows).

## Inclusion and exclusion rules

Kept:

- Items where the switch, the nationality or the neutral status is at least part of the story (not just a flag next to a score).
- News reports, interviews, federation or tour statements and profiles.
- English and Russian items, plus a couple in Italian and French. Notes are written in English. The `language` field keeps the original language and the snapshot keeps the original text.

Cut, with the reason recorded in `candidates.csv` or `data/snapshot_log.csv`:

- **Exact duplicate URLs.**
- **Syndicated copies.** When the same AP, AFP or Reuters story ran on several sites, we kept one copy. Groups were listed by hand in `find_sources.py` from the search result titles, and `snapshot.py` also flags any two pages whose extracted text has the same hash.
- **Paywalls and login readers** (PressReader). Not fetched at all.
- **robots.txt.** If a site's robots.txt disallows our user agent, or won't even show us its robots.txt (401/403), we skip it.
- **Pages that came back blocked, broken or nearly empty** at fetch time. Logged, not hidden.
- Content-farm pages that showed up in search (auto-generated bios and the like). Never added to the seed list.
- Pages that turned out to be off topic once read (the nationality angle wasn't really there).

**A bug we caught.** The first robots.txt pass marked 50 candidate URLs as disallowed. That turned out to be Python's `robotparser` fetching robots.txt with its default `Python-urllib` agent, getting a 403 from the CDN and treating that as "disallow everything". After switching to fetching robots.txt with our real user agent, only 1 URL was actually disallowed and 4 sites refused to serve us robots.txt at all.

## Transformation 1: web page to snapshot

`scripts/snapshot.py`

- Polite fetching: a real descriptive user agent (`IS310-CultureAsData-student-research/0.1` plus the repo URL), a 2 second delay between requests, robots.txt checked first, no paywall workarounds.
- For each page it saves the raw HTML and the main text (extracted with trafilatura) into `snapshots/`. That folder is gitignored, so no full article text ends up in the repo.
- It logs every attempt to `data/snapshot_log.csv`: HTTP status, fetch status, access date, SHA256 of the extracted text and the title, site name and date from the page metadata.
- What gets lost here: images, video, captions, comments, page layout, headline placement and ads. The text extractor can also drop pull quotes or grab a related-stories box. The hash pins down *which* text we coded, so if someone re-fetches later and gets different text, it shows.

### Fetch results (2026-10-28)

- 158 candidate URLs in total (154 from the first searches plus 4 from a follow-up Kukushkin search). 10 were excluded before fetching (4 syndicated copies, 1 PressReader paywall, 1 robots.txt disallow, 4 sites that wouldn't serve robots.txt).
- 148 fetched: **133 ok**, 9 HTTP errors (Sportskeeda 405 x4, ATP Tour 403 x2, Tennis Australia 403, two 404s), 1 connection error (Euroradio), 5 too short (under 400 characters of text, mostly JavaScript pages: Deccan Herald x2, Tennis Now, a Tennis.com brief and a Nasha Niva page).
- **Encoding bug.** Five Russian pages (Nur.kz and one Fontanka) came back as mojibake because the site sent no charset and `requests` fell back to Latin-1. Fixed `snapshot.py` to use the detected encoding and refetched them.
- No two ok pages had identical text hashes. But a few were the same wire story with small edits (AAP in Canberra Times, Reuters in Onmanorama, AFP in Infobae), so those were cut by hand at selection.

### Selecting the final 77

From the 133 ok snapshots we picked 7 or 8 per player:

1. The switch, nationality or neutral status has to be part of the story. Cut: match reports where "Kazakhstan" is just a label (Kazinform Olympics result, AP Belgium tie, The National on Hamburg), an extraction that grabbed a sidebar instead of the article (Vechernyaya Moskva) and a Forbes Kazakhstan piece that was about a different player.
2. Near duplicates: keep one per wire story.
3. Mix: try to get old country, new country and international outlets for each player.
4. Kukushkin only had 4 good items after the first round, so a second search added 4 more (Zakon.kz, Sport-Express, The Globe and Mail, Tennis.com). 3 of those made the cut.

Result: 77 items. 50 English, 25 Russian, 1 French, 1 Italian. Outlet countries: 17 KZ, 11 US, 10 GB, 8 RU and the rest spread across 18 other countries (22 total). Only 2 Australian outlets for Kasatkina and 1 Belarusian one for Sabalenka, so the new country side is thin for those two.

**How closely each item was read.** The reading pass used a digest of each snapshot: title, metadata date and the sentences that mention the player next to nationality words (born, citizen, federation, flag, money, war and the Russian equivalents), plus targeted reads where something was unclear (who said a quote, whether money came up). Not every full text was read start to finish. That's a big reason Joy's review matters.

## Transformation 2: snapshot text to structured row

`scripts/precode.py` plus a reading pass.

1. **Keyword pass (automatic).** Regex lists per frame, in English and Russian (with a few Italian and French terms), live at the top of `precode.py` with comments. A frame gets flagged when it has 2 or more hits. These are `keyword_flags`. They show where to look and they aren't the codes.
2. **Reading pass (AI draft, provisional).** The assistant read each selected snapshot and drafted `evidence_note` (paraphrase plus at most one quote under 15 words), `frame_primary`, `frame_secondary`, `identities_mentioned`, `money_mentioned`, `player_voice`, `item_type` and `uncertainty_note`. These live in `data/coding_suggestions.csv` and get merged into the dataset by `precode.py`.
3. **Human review (Joy).** Nothing counts as coded until `reviewed_by` is filled. The review report (`reports/collection_report.html`) has a dropdown per item and exports a CSV that `check_dataset.py --apply-review` reads.

What gets lost here: the whole article shrinks to two frame labels and a short note. Tone, headline vs body differences, how much space the switch gets compared with match results, and who gets quoted are mostly gone. `player_voice` keeps a tiny bit of the last one.

## Failed and skipped sources

See `data/candidates.csv` (status `excluded`) and `data/snapshot_log.csv` (anything not `ok`). A summary is in the fetch results section above.

## Known gaps

- **No Georgian-language items for Dzalamidze.** One Georgian search found nothing about her. Her coverage here is all international or Russian.
- **Few Belarusian outlets for Sabalenka.** The independent Belarusian outlets we found (Nasha Niva, Euroradio) mostly came through in English versions. No Belarusian state media.
- **Kukushkin and Golubev are older and smaller stories,** so their items lean toward match reports where nationality is mentioned in passing.
- **Pub dates come from page metadata** (trafilatura). If the metadata is missing or looks wrong, the date is left blank or the reading pass notes it.
