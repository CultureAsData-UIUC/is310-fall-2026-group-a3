
# International NBA Players — Individual Coding Codebook

**Version:** 1.0 (applied to the final individual review log, November 19, 2026)  
**Project:** IS 310 Milestone 2 — Individual NBA Revision  
**Research Question:** How do NBA-affiliated and independent media sources portray international NBA players in relation to national identity, home-country connections, and global audiences?

## 1. Purpose and Unit of Analysis

Each record represents **one distinct English-language news article or public interview transcript**, not one player, country, or audience. The individual strand includes **25 records (`NBA001`–`NBA025`)**. I reviewed the articles and recorded interpretations in `reviews/nba_review_log.csv`, using initial AI-assisted descriptions and classifications as starting points rather than as unquestioned findings.

The broader comparison concerns **institutional** sources (such as NBA, team, or basketball governing-body publications) and **independent** editorial sources. Source type is determined by the originating organization, not solely the website hosting an item. The sample is purposive and theme-based; it is not a random or representative sample of NBA coverage. The inherited shared dataset uses a sampling window of January 1, 2017–October 22, 2026.

## 2. Relationship to the Shared Dataset

The inherited `data/nba_media_dataset.csv` contains article metadata, source URLs, provenance, and earlier AI-assisted classifications. Its original fields remain governed by the shared project's definitions, including `shared_codebook_reference.md` where applicable. The individual review log is a **separate eight-column file**, linked to the inherited data by `item_id`.

The review log does not repeat source URLs, publication dates, publisher names, or all inherited flags. These are obtained by matching each `item_id` to the main dataset. It also functions as the **brief individual revision log** through its `coding_decision` field.

## 3. Individual Review Log Fields

The CSV columns must appear in this order:

```csv
item_id,review_date,source_verified,cultural_frame,audience_evidence,evidence_note,coding_decision,review_status
```

| Field | Definition and Allowed Values |
|---|---|
| `item_id` | Unique identifier matching the inherited dataset; `NBA001` through `NBA025`. |
| `review_date` | Date I reviewed the source, formatted `YYYY-MM-DD`. The final log records `2026-11-19` for all 25 items. |
| `source_verified` | Source access condition: `yes` = original source accessible and personally inspected; `subscription_needed` = I accessed and inspected the article, but other readers may need a subscription; `no` = original source could not be verified. |
| `cultural_frame` | One primary portrayal category from Section 4. |
| `audience_evidence` | The type of support for the article's main audience-related claim, from Section 5. |
| `evidence_note` | Concise paraphrase identifying the textual basis for the assigned categories (written by me). |
| `coding_decision` | Brief description of whether an AI-assisted classification was `confirmed`, `revised`, `rejected`, or `left uncertain`, and the reason or emphasis. The final log contains confirmed and revised decisions. |
| `review_status` | `student_verified` when I reviewed sufficient original material to support the recorded classifications; `provisional` when further review is necessary. |

**Access Note:** `subscription_needed` does **not** mean I failed to review the article. `NBA010` and `NBA018` are Sports Business Journal articles that I accessed and reviewed; readers without subscriptions may encounter restrictions. Both are recorded as `student_verified`.

## 4. Cultural Frame Definitions

Choose one dominant cultural frame based on the article's central emphasis, rather than a passing mention of nationality.

| Value | Decision Rule |
|---|---|
| `national_representative` | The player is portrayed as representing a nation, national team, or national sporting identity. Merely listing nationality is insufficient. |
| `global_celebrity` | The focus is worldwide visibility, transnational fame, or a player's international public profile. NBA stardom alone is insufficient. |
| `diasporic_connection` | The article explicitly connects the player to communities, heritage, or audiences maintaining ties across national borders. Do not infer a diaspora solely from birthplace. |
| `commercial_market` | Marketing, sponsorship, media rights, international fan development, or commercial expansion is the central frame. |
| `local_hero` | The player is especially meaningful to a particular hometown, local community, or named local fan base. |
| `multiple_belonging` | The article emphasizes the player's connections to, or negotiation of, multiple national, cultural, or community identities. |
| `international_recognition` | The article highlights international players collectively, their countries of origin, or their representation across the league without chiefly portraying an individual as a national representative or global celebrity. |

**Selection Rule:** Consider the headline, opening, and repeated themes. If an article contains several frames, select the one most central to the source and explain the choice in `evidence_note`. Do not use `multiple_belonging` simply because two countries are mentioned; belonging must be part of the discussion.

**Distinction for NBA025:** A league roster listing countries of origin is not automatically evidence that players are framed as national representatives. The final review log uses `international_recognition` to capture the collective international presence emphasized by this article.

## 5. Audience Evidence Definitions

Choose the evidence type that best supports the article's **main claim about fans, audiences, viewership, or public connection**. This describes the evidence presented, not whether the claim is objectively true.

| Value | Decision Rule |
|---|---|
| `measured_data` | Quantitative evidence such as viewership, audience counts, engagement, or reach is presented. Note limitations if the source or method is unclear. |
| `direct_audience_quote` | A fan or audience member is directly quoted describing their response or connection. |
| `player_or_coach_quote` | A player, coach, or comparable participant is quoted about audience or community connection. |
| `league_or_team_claim` | The league, a team, or another governing organization asserts audience interest or connection without independent measurement presented. |
| `journalist_inference` | The journalist interprets audience interest or connection without directly supporting it with audience quotations or measured data. |
| `anecdotal_observation` | An observed celebration, reception, or individual example suggests audience interest but does not establish broader behavior. |
| `no_audience_claim` | The article makes no substantive claim about audience response, interest, or engagement. |

When multiple types occur, use the type most relevant to the main audience claim. An anecdote should not be treated as representative data, and an organizational assertion should not be described as independently measured audience growth.

## 6. Evidence Notes and Coding Decisions

The `evidence_note` is a short, original paraphrase of what the reviewed article supports. It should connect the chosen cultural frame and, where applicable, the audience evidence to specific article content. It should avoid unsupported assumptions and extensive copying from sources.

The `coding_decision` documents how my review relates to the earlier AI-assisted suggestion:

- **`confirmed`** — I retained the AI-assisted interpretation after reviewing the source.
- **`revised`** — I adjusted or sharpened the earlier interpretation after reviewing the source.
- **`rejected`** — I found that an earlier suggested interpretation was not supported.
- **`left uncertain`** — I could not confidently resolve an interpretation with the available evidence.

These are **descriptive phrases**, not separate CSV columns. The final log documents **21 confirmed** and **4 revised** decisions. The revised items are `NBA002`, `NBA008`, `NBA018`, and `NBA025`; none are recorded as rejected or left uncertain.

## 7. Review Workflow and Verification Standard

For each article, I:

1. Opened the source and considered the material available for personal review.
2. Matched the article to its `item_id` and inherited source metadata.
3. Reconsidered the AI-assisted interpretation using the cultural-frame and audience-evidence definitions.
4. Recorded a paraphrased `evidence_note`, the review date, and the outcome in `coding_decision`.
5. Used `student_verified` only for material personally reviewed sufficiently to support the recorded decisions.

The review log documents **interpretive verification**, not independent fact-checking of every statement made by a publisher. A second reviewer or formal disagreement-resolution process is not claimed. Any automated checks can validate field names, permitted values, and completeness, but cannot independently confirm interpretive judgments.

## 8. Comparison, Limitations, and Audit Considerations

The individual analysis can compare cultural frames and audience-evidence categories across institutional and independent sources using `provenance` from the inherited dataset. Counts should be reported with their denominators, and contrasting examples should be examined closely.

The **25-item purposive sample** cannot establish how all NBA media portray international players. Some players and events recur, and publisher types may differ in how they discuss audiences. The two subscription-based articles may be difficult for the professor or other readers to access. A source's claim about fan interest is not proof of broad audience behavior or a causal effect.

An audit can match `item_id` to `source_url` in the inherited dataset, reopen available sources, compare their content with `evidence_note`, and check the category definitions and `coding_decision` wording. The separate individual audit plan should specify which cases to prioritize and how disagreements or access limitations would be handled.

## 9. Versioning and Change Management

- **Version 0.1:** Proposed framework containing additional interpretive fields not adopted in the final review log.
- **Version 1.0 (November 19, 2026):** Updated to match the eight-column individual review log and its completed review decisions. Removed unused proposed columns, including `secondary_cultural_frame`, `identity_connection_type`, `interpretive_evidence`, and `coding_uncertainty`; renamed the primary coding concept to `cultural_frame` and the audience field to `audience_evidence`; added `international_recognition`; and documented subscription access and revision outcomes.

Retain the shared codebook separately for definitions governing inherited fields. Future changes to the individual log should be reflected consistently in this codebook and the README.

## 10. AI-Use Disclosure

AI assisted with organizing the initial dataset descriptions, suggesting classifications, and drafting and refining the codebook. I personally reviewed the selected sources, confirmed or revised the AI-assisted interpretations, and remain responsible for the final classifications and evidence notes. AI assistance is not presented as independent source verification or as a substitute for my judgment.