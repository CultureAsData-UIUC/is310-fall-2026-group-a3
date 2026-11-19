# International NBA Players — Individual Coding Codebook

**Version:** 0.1 (proposed coding framework; not yet applied)  
**Project:** IS 310 Milestone 2 individual NBA revision  
**Research question:** How do NBA-affiliated and independent media sources portray international NBA players in relation to national identity, home-country connections, and global audiences?

## 1. Purpose and Unit of Analysis

Each record is **one distinct English-language news article or public interview transcript**, not one player, country, or audience. The existing dataset has 25 NBA records (`NBA001`–`NBA025`). This codebook specifies how the student will conduct **close, human review** of those records. The existing classifications are provisional AI-assisted suggestions and are **not** independently verified.

The primary comparison is between **institutional** sources (league, team, or governing-body originators) and **independent** sources (news or other editorial originators). Classify by **originator**, not merely the website hosting the item. Source type is not proof of a particular framing. Repeated athletes and events may affect the distribution of frames.

The shared dataset's sampling period is January 1, 2017–October 22, 2026; undated items remain flagged. The corpus is purposive, English-language, and theme-searched; it is not a representative or random sample of NBA media.

## 2. Preserve the Inherited Fields

The original `data/nba_media_dataset.csv` needs to remain unchanged until an individual review begins. The shared codebook's fields and meanings stay the same, particularly:

- **Source and provenance:** `item_id`, `strand`, `sport`, `record_label`, `source_url`, `publisher`, `originator`, `provenance`, `source_date`, `date_basis`, `date_note`, `accessed_date`, `subject`, `language`.
- **Evidence and access:** `inspected_scope`, `access_method`, `evidence_locator`, `evidence_note`.
- **Existing flags:** `development`, `national_identity`, `audience_connection`, `competing_allegiance` (`yes`, `no`, `unclear`); `movement` (`relocation_discussed`, `domestic_pathway`, `not_established`). Use the definitions in `shared_codebook_reference.md`.
- **Review status:** `review_status` (`provisional`, `student_verified`) and `reviewer` (blank until the student personally inspects and codes the item).

Do not treat an `article_excerpt` or `indexed_text` as proof of having reviewed the full article. If the original article cannot be accessed, retain the limited scope, explain the access issue, and do not mark the record `student_verified` as a fully reviewed article.

## 3. New interpretive fields (proposed)

The fields below are not yet columns in the CSV. They will be added in the next dataset-preparation stage, before individual article review. Use the exact values listed so the validator can check them later.

### `primary_cultural_frame`

The **dominant portrayal** of the international player in the inspected text. Choose one value only if there is explicit support:

| Value | Decision rule |
|---|---|
| `national_representative` | The player is framed chiefly as representing a nation, national team, or national sporting identity. Merely listing nationality is insufficient. |
| `global_celebrity` | The emphasis is on worldwide visibility, transnational fame, or broad international recognition. Being an NBA star alone is insufficient. |
| `diasporic_connection` | The article explicitly connects the player to a diaspora or community with ties across countries. Do not infer diaspora from birthplace alone. |
| `commercial_market` | The player is framed primarily through marketing, sponsorship, media rights, merchandise, or international business expansion. |
| `local_hero` | The player is portrayed as especially meaningful to a named home community, hometown, or local fan base. A country name alone is insufficient. |
| `multiple_belonging` | The main theme is negotiating or combining more than one national, cultural, or community affiliation. |
| `sporting_performance` | Performance, tactics, statistics, or competition dominate without a substantiated cultural frame. |
| `other` | A clear dominant portrayal does not fit the listed frames; explain in the evidence note. |
| `not_established` | The inspected material does not provide enough evidence to identify a dominant portrayal. |

**Tie rule:** Choose the frame most central to the headline, lead, and repeated discussion *within the actually inspected scope*. If frames are equally prominent, choose `multiple_belonging` **only when belonging itself is the theme**; otherwise record the tie as uncertainty and explain the decision. Do not force every record into a national-identity category.

### `secondary_cultural_frame`

Use one of the same values as `primary_cultural_frame`, or `none`. Assign a secondary frame only when separately supported by the text; it must differ from the primary frame. `none` means no second frame is supported in the inspected material, not that none exists in the full article.

### `identity_connection_type`

How national or cultural identity is *explicitly* discussed:

| Value | Decision rule |
|---|---|
| `national_team` | Playing for, choosing, or representing a national team is discussed. |
| `citizenship_or_eligibility` | Citizenship, nationality eligibility, naturalization, or legal national status is discussed. |
| `heritage_or_family` | Family heritage, ancestry, or cultural upbringing is connected to identity. |
| `home_country_attachment` | Explicit personal or community ties to a home country are discussed outside merely listing nationality. |
| `multiple_affiliations` | Two or more affiliations are explicitly compared or negotiated as an identity issue. |
| `none_explicit` | No qualifying identity discussion appears in the inspected material. |
| `unclear` | The text suggests identity but does not clearly establish its type. |

**Multiple types:** Select the type most important to the article and note additional types in `interpretive_evidence`. Do not infer citizenship from a national-team appearance or equate birthplace, ethnicity, and nationality.

### `audience_evidence_type`

What **kind of evidence**, if any, supports a claim about fans, reach, viewing, or audience connection:

| Value | Decision rule |
|---|---|
| `measured_data` | A specified metric (e.g., audience count, viewership, sales, followers) with an identifiable source or method appears. A number without provenance should be noted as limited. |
| `direct_audience_quote` | A fan or audience member is directly quoted about their experience or connection. |
| `player_or_coach_quote` | A player, coach, or similarly situated participant makes an audience-related claim. |
| `league_or_team_claim` | A league, team, or governing-body representative makes the claim without independent measurement presented in the inspected material. |
| `journalist_inference` | The author asserts or interprets audience connection without direct supporting data or audience quotation. |
| `anecdotal_observation` | An observed fan event or isolated example is described, but cannot establish general audience behavior. |
| `no_audience_claim` | The inspected text makes no qualifying audience claim. |
| `unclear` | The basis of the audience claim cannot be determined from the inspected scope. |

If multiple evidence types appear, record the **strongest evidence actually presented for the article's main audience claim**, and describe any other types in `interpretive_evidence`. Do not interpret an organizational assertion as measured audience growth, or correlation as causation.

### `interpretive_evidence`

A short **student-written paraphrase** (typically 1–3 sentences) explaining the selected frame(s), identity type, and audience-evidence type. Include a precise paragraph, heading, or speaker locator and distinguish **what the text states** from **your interpretation**. Avoid copying substantial article text. If a source is inaccessible, describe that limitation rather than inventing evidence.

### `coding_uncertainty`

| Value | Decision rule |
|---|---|
| `low` | The inspected text clearly supports the selected categories and relevant locators are recorded. |
| `medium` | More than one plausible interpretation, incomplete context, or a borderline category remains; explain the issue. |
| `high` | Material is missing, inaccessible, contradictory, or too thin for a confident interpretive classification; use `not_established` / `unclear` where appropriate. |

This field describes **coding confidence**, not the truth of the article's factual claims. A `low` value does not establish factual accuracy.

## 4. Review Workflow and Verification Standard

For each item (`NBA001`–`NBA025`):

1. Open the original `source_url`; record the date of your review and whether the full article, a section, or an excerpt was accessible.
2. Check the title/record label, author or originator, publication date, provenance, and evidence locator against the source; note discrepancies.
3. Independently reconsider the inherited flags using the shared codebook, rather than accepting the AI-assisted values automatically.
4. Assign the new interpretive fields **only from material you personally inspected**. Write your own evidence paraphrase and record uncertainty.
5. Log the original and revised decisions, source access, reason for change or confirmation, and review date in a separate revision log.
6. Set `review_status=student_verified` and enter your actual reviewer name **only if you personally inspected sufficient original source material to validate the recorded scope and classifications**. If not, retain `provisional` and explain why.

A second reviewer or a disagreement-resolution log should only be reported if it actually happens. Computational validation can check allowed values, missing fields, and record counts; it **cannot** verify cultural interpretations.

## 5. Comparison and Analysis Plan

After human review, summarize frame frequencies and audience-evidence types by `provenance` (institutional versus independent), including denominators and missing/uncertain values. Read contrasting examples closely and explain exceptions. Because the sample has only 25 purposively selected records (9 institutional and 16 independent initially), treat comparisons as **descriptive and exploratory**, not representative estimates or causal findings. Do not claim that a frame caused audience growth.

## 6. Versioning and Change Management

- **v0.1:** Proposed individual coding definitions only; no articles independently reviewed and no new interpretive labels assigned.
- Keep `shared_codebook_reference.md` as the unmodified inherited reference.
- When the student and assistant refine a definition, record the change and date before applying it consistently to records.
- The original 50–100-item requirement remains to be resolved in the revision plan; this codebook does not claim that 25 items alone satisfy it.

## 7. AI-Use Disclosure

AI assisted in drafting this proposed codebook and organizing possible categories. These definitions require my personal judgment during application. AI does not independently verify the 25 articles, assign reviewed cultural frames, or resolve issues without proper oversight.
