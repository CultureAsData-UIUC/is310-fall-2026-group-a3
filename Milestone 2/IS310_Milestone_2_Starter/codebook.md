# Dataset codebook

Version 0.1 | October 22, 2026 | Proposed shared rules

## Unit and scope

One row represents one distinct public article or official interview transcript. Code only the inspected scope, and record a precise locator for the evidence. Syndicated copies count once. Records may have several flags; flags are not exclusive frames. All initial labels are AI-assisted suggestions awaiting student review.

## Fields

| Field | Definition and allowed values |
|---|---|
| item_id | Stable unique identifier, such as SOC001, NBA001, or F1001 |
| strand | athlete_mobility, nba_global, f1_allegiance |
| sport | soccer, basketball, formula_1; must match strand |
| record_label | Short descriptive label; may abbreviate the original headline |
| source_url | Original readable source, including host if syndicated |
| publisher | Organization hosting the page |
| originator | Authoring organization or named author; distinguish host from originator |
| provenance | institutional or independent; determined by originator |
| published_date | ISO date YYYY-MM-DD; do not substitute an event or retrieval date |
| accessed_date | ISO date the source was inspected |
| subject | Primary athlete or team; do not treat as a citizenship field |
| language | Source language; pilot uses English |
| inspected_scope | article_body or transcript_section |
| evidence_locator | Heading, paragraph context, or speaker identifying the inspected evidence |
| evidence_note | Brief paraphrase supporting the suggested codes; no copied article body |
| development | yes, no, unclear |
| national_identity | yes, no, unclear |
| audience_connection | yes, no, unclear |
| competing_allegiance | yes, no, unclear |
| movement | relocation_discussed, domestic_pathway, not_established |
| review_status | provisional or student_verified |
| reviewer | Blank until a student verifies the source and labels |

## Flag decisions

**Development:** `yes` when text explicitly discusses training, an academy, mentorship, or career development. A match result alone is insufficient.

**National identity:** `yes` when text explicitly foregrounds country, national representation, citizenship, or belonging. A publisher's location alone is insufficient. This broad flag includes national-team representation; it does not imply nationalism or pride. Discuss the particular form in evidence notes.

**Audience connection:** `yes` when the inspected text explicitly describes supporters, fan attachment, viewing, or an athlete's relationship with an audience. Fame or a successful performance alone is insufficient. This flag does not measure audience size or causal growth.

**Competing allegiance:** `yes` when text explicitly describes overlapping, divided, shifting, or competing attachments between an athlete, team, or nation. A nationality mismatch alone is insufficient.

**Movement:** `relocation_discussed` requires explicit discussion of moving for a sporting pathway. `domestic_pathway` identifies an explicitly described home-country development route in the inspected account, not proof the athlete never moved later. `not_established` means no qualifying pathway can be established from that account. International match travel alone is insufficient. Do not infer a physical residential move solely from a new club contract.

Use `no` only after reviewing the recorded scope and finding no qualifying evidence; use `unclear` for incomplete or ambiguous evidence. Absence in a text is not absence in the world. The pilot's provisional flags must be rechecked by the group.

## Review and change log

The strand lead reviews the original source and enters their real name only when setting `student_verified`. A second member independently codes five items per strand. Keep a separate log with item ID, original labels, second labels, disagreement, resolution, date, and participants. Update this codebook and affected records when definitions change. The checker cannot adjudicate these decisions.

## Audit template

Audit rows are separate from custom items and never add to the 75-item count. `availability` uses structured_field, prose_only, not_found_in_inspected_scope, unclear, or not_applicable. Record one checked concept per row, including a linked custom item ID, the profile URL, access date, inspected scope, and evidence. Never prefill an absence finding without inspecting the page. The supplied template is empty.
