
# Individual Audit Plan — International NBA Players

## 1. Purpose of the Audit

The purpose of this audit is to evaluate the accuracy, consistency, and transparency of my individual review of 25 articles about international NBA players.

My research question is: How do NBA-affiliated and independent media sources portray international NBA players in relation to national identity, home-country connections, and global audiences?

The audit will focus on whether my cultural-frame classifications, audience-evidence categories, and written evidence notes are supported by the original articles. It will also examine whether my revisions to AI-assisted interpretations are documented clearly.

## 2. Files Used for the Audit

The audit will use the following files:

- `data/nba_media_dataset.csv` — Contains the original article records, source URLs, publication information, and provenance.
- `reviews/nba_review_log.csv` — Contains my individual classifications, evidence notes, verification statuses, and revision decisions.
- `codebook.md` — Defines the coding categories and explains the decision rules.
- `README.md` — Explains the research question, selection process, and relationship to the shared project.
- `reflection.md` — Documents my research process, challenges, and remaining uncertainties.

The `item_id` field connects each record in the individual review log to its corresponding article in the original dataset.

## 3. Audit Procedure

An independent reviewer could complete the following steps:

1. **Check Dataset Completeness:** Confirm that the individual review log contains 25 unique records, identified as `NBA001` through `NBA025`, with all eight required columns present.

2. **Verify Source Information:** Match each `item_id` in the review log to the original dataset and check the source URL, publisher, and available publication information.

3. **Review the Original Articles:** Open each accessible article and compare its content with the corresponding `evidence_note`.

4. **Evaluate Cultural Frames:** Use the definitions in `codebook.md` to determine whether the selected `cultural_frame` accurately represents the article's dominant portrayal.

5. **Evaluate Audience Evidence:** Check whether each `audience_evidence` category matches the type of support actually presented in the article.

6. **Review AI-Assisted Decisions:** Examine the `coding_decision` field to identify which interpretations I confirmed and which I revised.

7. **Document Disagreements:** Record any differences between the auditor's interpretation and my classification, including the article ID, the disputed category, and the supporting evidence.

These steps would help determine whether my classifications can be understood and reproduced by someone who did not participate in the original review.

## 4. Priority Records for Review

Although all 25 records can be audited, I would prioritize articles that involve interpretive revisions, source-access limitations, or potentially ambiguous cultural frames.

| Item ID | Reason for Priority Review |
|---|---|
| `NBA002` | Revised classification emphasizing emotional connection to Greece and family citizenship. |
| `NBA008` | Revised classification emphasizing belonging in both Slovenia and Dallas. |
| `NBA010` | Subscription-based source containing international audience and media information. |
| `NBA014` | Discusses Giannis Antetokounmpo's Greek and Nigerian identities, making multiple belonging an important interpretive issue. |
| `NBA017` | Contains NBA-reported audience metrics that should be distinguished from independently verified measurements. |
| `NBA018` | Revised commercial-market classification and potential subscription-access restrictions. |
| `NBA025` | Revised to `international_recognition` rather than treating nationality listings as national representation. |

These records provide useful examples for checking whether the codebook's definitions are applied consistently.

## 5. Source Access and Verification

The original dataset provides source URLs for all 25 articles. The auditor should begin with those URLs rather than relying only on the summaries in my review log.

Most sources were accessible during my review. However, `NBA010` and `NBA018` are Sports Business Journal articles that may require subscriptions.

I personally reviewed both articles, so they remain marked `student_verified` in my individual review log. The `subscription_needed` value indicates a possible limitation for other readers rather than an incomplete student review.

If an auditor cannot access a source, they should record the access limitation and avoid treating the article as independently verified. They should not substitute an AI-generated summary for the original article.

## 6. Coding Consistency and Disagreement Resolution

The auditor should use the definitions in `codebook.md` rather than relying only on personal impressions.

For `cultural_frame`, the reviewer should identify the article's dominant theme and determine whether the selected category reflects that emphasis. Particular attention should be given to distinctions between `national_representative`, `multiple_belonging`, and `international_recognition`.

For `audience_evidence`, the reviewer should distinguish between direct audience quotations, measured data, organizational claims, journalistic inference, and anecdotal observations.

If a disagreement occurs, the auditor should document:

- The article's `item_id`.
- My original classification.
- The auditor's suggested classification.
- The specific article content supporting the alternative interpretation.
- Whether the disagreement can be resolved using the existing codebook.

If the evidence supports more than one reasonable interpretation, the disagreement should remain documented rather than being hidden or automatically treated as an error.

## 7. Audit Criteria and Expected Outcomes

The audit will evaluate the following criteria:

| Criterion | Expected Standard |
|---|---|
| Completeness | All 25 articles appear once in the individual review log. |
| Traceability | Every reviewed record matches an article in the original dataset through `item_id`. |
| Source Support | Evidence notes accurately paraphrase the relevant article content. |
| Coding Consistency | Cultural frames and audience-evidence categories follow the codebook definitions. |
| Revision Transparency | The 21 confirmed and four revised classifications are documented in `coding_decision`. |
| Access Transparency | Subscription restrictions for `NBA010` and `NBA018` are identified. |
| Reproducibility | Another reviewer can understand how classifications were assigned, even if some interpretations differ. |

A successful audit would not require every reviewer to reach exactly the same interpretation. Instead, it would demonstrate that the classifications are supported by identifiable evidence, follow consistent definitions, and are documented transparently.

## 8. Limitations of the Audit

This audit would evaluate the reliability of my individual review process, not the factual accuracy of every claim made by the original publishers.

The 25-article sample is purposive, so auditing the records would not establish whether the findings represent all coverage of international NBA players.

Some cultural frames may remain open to interpretation, and subscription restrictions could limit another reviewer's ability to inspect certain articles.

Despite these limitations, the combination of source URLs, a structured review log, a codebook, and documented revisions provides a clear process for independently evaluating my work.