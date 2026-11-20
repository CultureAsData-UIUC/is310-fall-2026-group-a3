
# International NBA Players — Individual Milestone 2 Research

## 1. Research Question

How do NBA-affiliated and independent media sources portray international NBA players in relation to national identity, home-country connections, and global audiences?

My individual research examines how international NBA players are represented in sports media, particularly how articles discuss their national identities, relationships with their home countries, and connections to fans around the world.

I also consider how these portrayals differ between institutional sources, such as the NBA and basketball organizations, and independent news outlets.

## 2. Project Scope and Unit of Analysis

My individual dataset contains 25 English-language articles about international NBA players, identified as `NBA001` through `NBA025`.

The unit of analysis is one distinct news article or public interview transcript. Each record represents a media source rather than an individual player, country, or audience.

The articles cover several international NBA players, including Giannis Antetokounmpo, Nikola Jokic, Luka Doncic, Shai Gilgeous-Alexander, Victor Wembanyama, Joel Embiid, and Rui Hachimura.

The inherited shared dataset uses a sampling period of January 1, 2017, through October 22, 2026. My individual analysis focuses on the 25 NBA records selected from that project.

The sample is purposive rather than random, so my findings are intended to identify patterns within these articles rather than represent all NBA media coverage.

## 3. Article Selection Process

The articles were selected based on their relevance to international NBA players and the relationship between sports media, cultural identity, and global audiences.

The selection focused on articles discussing:

- National identity and national-team representation.
- Connections to home countries, hometowns, and cultural heritage.
- Relationships between players and international fan communities.
- International recognition, media visibility, and commercial expansion.

I included both institutional and independent sources to examine different perspectives on international players.

Institutional sources include articles published by organizations such as the NBA, NBA teams, and international basketball organizations. Independent sources include newspapers and other sports media publications.

Because the articles were selected based on their relevance to the research question, the dataset is not a representative sample of all NBA reporting.

## 4. Relationship to the Shared Project

My individual work builds on the shared sports media dataset created for our IS 310 project.

The original file, `data/nba_media_dataset.csv`, contains the article records, source URLs, publication information, provenance, and initial AI-assisted descriptions or classifications.

Rather than replacing the shared dataset, I created a separate individual review log to document my personal examination of the 25 NBA articles.

The individual review log is connected to the inherited dataset through the `item_id` field, which allows each reviewed record to be matched to its original source information.

My contribution focuses on independently reviewing the NBA strand, reconsidering AI-assisted interpretations, and documenting my final cultural-frame and audience-evidence classifications.

## 5. Individual Review and Coding Process

I personally reviewed the 25 articles on November 19, 2026, and recorded my decisions in `reviews/nba_review_log.csv`.

For each article, I examined its portrayal of international NBA players and identified the dominant cultural frame. I also considered what evidence the article provided about fans, audiences, viewership, or public engagement.

The review log contains eight columns:

1. `item_id` — Identifies the article and connects it to the original dataset.
2. `review_date` — Records when I reviewed the article.
3. `source_verified` — Documents whether the source was accessible or required a subscription.
4. `cultural_frame` — Identifies the article's primary cultural portrayal.
5. `audience_evidence` — Classifies the evidence supporting audience-related claims.
6. `evidence_note` — Summarizes the relevant article content in my own words.
7. `coding_decision` — Documents whether I confirmed or revised the AI-assisted interpretation.
8. `review_status` — Indicates whether I personally verified the record.

The definitions and decision rules for these fields are provided in `codebook.md`.

## 6. AI-Assisted Classification Review and Revisions

The original dataset included AI-assisted descriptions and classifications. I used these as starting points, but I reviewed the articles myself before deciding whether to retain or revise the interpretations.

Of the 25 reviewed records:

- 21 AI-assisted classifications were confirmed.
- 4 AI-assisted classifications were revised.
- No classifications were recorded as rejected or left uncertain.

The four revised records were:

- `NBA002` — Revised to emphasize Giannis Antetokounmpo's emotional connection to Greece and his family's citizenship.
- `NBA008` — Revised to emphasize Luka Doncic's connection to both Slovenia and Dallas.
- `NBA018` — Revised to emphasize international promotion and engagement through Victor Wembanyama's superstar identity.
- `NBA025` — Revised to emphasize the recognition and representation of international players across NBA rosters.

The `coding_decision` column in my review log serves as the brief revision log required for my individual work.

## 7. Source Verification and Access Limitations

I recorded the source-access condition for every article.

Most articles were accessible without a subscription. Two Sports Business Journal articles, `NBA010` and `NBA018`, require a subscription for full access.

I was able to access and personally review both articles, so they are marked `student_verified`. However, their `source_verified` values are recorded as `subscription_needed` to make readers aware of potential access restrictions.

These restrictions may make it more difficult for the instructor or another reviewer to independently examine those sources.

## 8. Files and Organization

The individual project uses the following files:

```text
Milestone 2/
├── README.md
├── codebook.md
├── data/
│   └── nba_media_dataset.csv
├── reviews/
│   └── nba_review_log.csv
├── reflection.md
└── audit_plan.md
```

- `README.md` — Explains the individual research question, scope, selection process, and relationship to the shared project.
- `codebook.md` — Defines the eight review-log fields and their classification rules.
- `data/nba_media_dataset.csv` — Contains the inherited article records and source metadata.
- `reviews/nba_review_log.csv` — Contains the 25 personally reviewed records and the individual revision log.
- `reflection.md` — Discusses my research process, interpretive decisions, challenges, AI use, and remaining uncertainties.
- `audit_plan.md` — Describes how the sources, classifications, and review decisions can be independently audited.

## 9. Limitations and Remaining Uncertainties

The dataset includes only 25 purposively selected articles, and several players appear in multiple records. As a result, the sample may emphasize particular athletes, events, or types of media coverage.

Some articles rely on statements from journalists, teams, or leagues rather than direct audience evidence or measured data. I distinguished these evidence types to avoid treating all audience claims as equally supported.

Cultural framing also involves interpretation, so another reviewer might reasonably classify some articles differently. My evidence notes and codebook make these decisions more transparent.

The analysis is descriptive and exploratory. It does not establish that particular media portrayals caused changes in audience interest or behavior.

## 10. AI-Use Disclosure

AI assisted with organizing the initial article descriptions, suggesting classifications, and drafting and refining the review documentation.

I personally reviewed the selected articles and made the final decisions about which AI-assisted classifications to confirm or revise.

The final review log, codebook, and supporting documentation reflect my individual interpretation of the sources. AI assistance is not treated as independent verification of article content.