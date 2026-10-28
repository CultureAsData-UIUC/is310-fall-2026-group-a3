# Codebook

DRAFT for Joy to edit. The examples below come from real items in the dataset, paraphrased. All codes are still provisional until reviewed.

## Dataset fields (`data/tennis_nationality_dataset.csv`)

| Field | What goes in it | Rule |
|---|---|---|
| `item_id` | TEN001, TEN002... | Unique, assigned in order by `precode.py` |
| `player` | Player name as written in the source | Cyrillic stays Cyrillic (e.g. Елена Рыбакина) |
| `from_nation`, `to_nation` | Three-letter codes, or `NEUTRAL` | Copied from `players.csv`, never typed per row |
| `switch_year` | Year of the switch | From `players.csv`, blank if not verified |
| `outlet` | Publication name | Wire services noted in brackets, e.g. NBC New York (AP) |
| `outlet_country` | Two-letter country of the outlet | Where the outlet is based. Exile outlets go by base city (Meduza = LV, The Moscow Times = NL) |
| `url` | Original URL | Must be a full http(s) URL, no duplicates |
| `pub_date` | YYYY-MM-DD | From page metadata. Blank if missing or clearly wrong (see `uncertainty_note`) |
| `access_date` | YYYY-MM-DD | Date `snapshot.py` fetched it |
| `item_type` | `article`, `interview`, `statement`, `profile` | Interview = the piece is mainly the player's answers. Profile = background or explainer piece |
| `language` | ISO 639-1 code | Language of the original text |
| `snapshot_sha256` | Hash of the extracted text | Proves which version of the text was coded |
| `evidence_note` | Short paraphrase plus at most one quote under 15 words | Copyright rule. `check_dataset.py` enforces it |
| `frame_primary` | Main frame, from the list below | Required |
| `frame_secondary` | Second frame or blank | Can't repeat the primary |
| `identities_mentioned` | Pipe separated: `birthplace`, `citizenship`, `residence`, `training_base`, `federation`, `heritage` | Only ones the item actually mentions |
| `money_mentioned` | `yes` / `no` | Any money: federation funding, prize money, earnings |
| `player_voice` | `yes` / `no` | Yes if the player is quoted directly (not just paraphrased) |
| `keyword_flags` | Frames whose keyword lists hit 2+ times | Automatic, from `precode.py`. A pointer, not a code |
| `uncertainty_note` | Free text | Starts with "Provisional AI code." until reviewed. Explains `other`, blank dates, shared items |
| `reviewed_by` | Reviewer's name | Blank until Joy reviews. Only Joy fills this |

### Identity definitions

- **birthplace**: where the player was born (Moscow, Volgograd, Tolyatti...)
- **citizenship**: passport, citizenship or "sporting citizenship"
- **residence**: where they live now or have lived (Vienna, Miami, "doesn't live anywhere")
- **training_base**: where they train or trained (Bra in Italy, Tbilisi, Slovakia and Dubai, Russian tennis school)
- **federation**: a national federation or the tours (KTF, Tennis Australia, RTF, WTA, ITF)
- **heritage**: family origin or roots (Dzalamidze's Georgian father, "respect my roots")

## Frames

Two frames max per item. If nothing fits, use `other` and say why in `uncertainty_note`.

| Code | Meaning | Example from the data |
|---|---|---|
| `opportunity_funding` | Switch framed around federation money, coaching, resources | **TEN027** (Zakon.kz, Kukushkin): he says even as a top Russian junior he got no support or sponsors and had to scrape to save money, and the piece says that pushed him to Kazakhstan in 2008. |
| `pragmatic_career` | Switch framed as a rational career move | **TEN058** (Sports.ru, Dzalamidze): she says at 29 with a career best ranking her prospects are much better in Georgia. |
| `loyalty_betrayal` | Switch framed as abandoning a nation or not belonging | **TEN050** (Meduza, Kasatkina): an exiled outlet reports she was branded a traitor back home after joining Team Australia. |
| `politics_war` | Sanctions, war, neutral status, political pressure | **TEN070** (Free Malaysia Today, Sabalenka): she won't comment on the war after a Ukrainian opponent skips the handshake, and Lukashenko is said to have claimed her win despite the neutral flag. |
| `belonging_homecoming` | New nation framed as real home or identity | **TEN022** (Nur.kz, Putintseva): after a 2026 Australian Open win she thanks Kazakh fans and says she feels Kazakh. |
| `flag_of_convenience` | Nationality framed as purchased or nominal | **TEN023** (Philstar, Kukushkin): a 2008 Davis Cup preview says two Russians changed citizenship just to become eligible for Kazakhstan. |
| `other` | None of the above. Explain in `uncertainty_note` | **TEN031** (Tennishead, Golubev): profile where he calls himself a citizen of the world (Russia, Italy, Kazakhstan). |

Item numbers above match the current build. If `precode.py` reorders rows, check them again.

## Coding rules we used

1. Code the item's framing, not the player's real reasons. If an outlet calls a move "to avoid the ban", that's `flag_of_convenience` even if the player says it was for the Olympics.
2. When a frame comes from someone other than the outlet or player (an interviewer's question, a rival federation, a fan), still code it but say who in `uncertainty_note`.
3. Items that cover several players get filed under the player who is quoted or most central. The others are named in `uncertainty_note`.
4. A neutral player is "switching" only in the sense the tours took the flag away. Items about them almost always land in `politics_war`, which is expected.

## Suggested revisions (for Joy to decide)

The reading pass kept hitting the same gaps:

- **`national_claiming`** (new). Old or home country claiming the player anyway: the Russian federation calling Rybakina "our product", Lukashenko claiming Sabalenka, Sport-Express calling Kukushkin the Volgograd native playing for Kazakhstan, Kommersant naming Sabalenka's country despite the neutral rule. Right now these land in `other` or get squeezed into `politics_war`. About 7 items would move (TEN004, TEN005, TEN008, TEN028, TEN071, TEN072, TEN077).
- **`safety_exile`** (new, or widen `politics_war`). Kasatkina's switch is framed around being unsafe in Russia as a gay woman who opposes the war. `politics_war` covers the war part but not the sexuality and safety part.
- **`multiple_identity`** (new, or a note convention). Golubev ("citizen of the world"), Shevchenko (Rostov, Vienna, Kazakhstan) and Rybakina ("I don't live anywhere") are framed as belonging to several places at once. That's close to the research question about what a single code hides.
- **Federation recruitment without money.** Tennis Australia reaching out to Kasatkina's agent isn't really `opportunity_funding`. Maybe widen that code to "federation recruitment and support".

If any of these get added, update the `FRAMES` set in `check_dataset.py` and the keyword lists in `precode.py`.
