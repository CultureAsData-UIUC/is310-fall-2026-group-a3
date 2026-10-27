# IS310 Milestone 2 group starter

Prepared October 22, 2026 for Mason, Drew, and Bob.

Start with [the group draft](milestone_2_group_draft.md). This package begins the shared project described in Milestone 1. All choices about sample size, sources, roles, and coding are proposals for the group to review.

## What is here

- `milestone_2_group_draft.md`: shared research question, collection plan, transformations, audit plan, reflection, and three scholarly references.
- `codebook.md`: field definitions and coding rules.
- `data/pilot_dataset.csv`: six real source records, two per strand. All coding is provisional and awaits student review.
- `data/audit_template.csv`: empty structure for the later audit; no audit findings are claimed.
- `scripts/check_dataset.py`: Python program that checks records and creates a browsable HTML report using only Python's standard library.
- `reports/quality_report.json` and `reports/collection_report.html`: outputs from running the program on the pilot.

## Current status

Six pilot items have been recorded toward a proposed 75-item dataset. The remaining 69 have not been collected. The existing pilot is deliberately small enough for the group to review its categories before expansion. It is a beginning, not a complete Milestone 2 submission. Two NBA records concern the same athlete, so expanding the range of athletes is especially important.

No repository was provided, and nothing has been uploaded or submitted. Copy this folder into the shared repository, link this README from the repository's main README, and retain the relative folder structure.

## Run the computational artifact

From this folder, run:

```text
python scripts/check_dataset.py
```

Python 3 is required; no extra packages are needed. The program reads `data/pilot_dataset.csv` and rewrites only the two files in `reports/`. Run it again after adding or reviewing records. Open the HTML report in a browser to inspect records and follow source links.

## Before submission

1. Agree on the shared scope and review all six pilot records against their sources. Record the actual reviewer; do not treat AI suggestions as student verification.
2. Collect 23 more eligible records per strand to reach 25 each. If submitting fewer, explain the actual remaining work and completion plan.
3. Read the scholarly sources in full through the library where available, then revise the source discussion. Access limitations are recorded in the draft.
4. Run the checker and resolve errors. Its success establishes structural consistency, not factual or interpretive accuracy.
5. Update the reflection to describe what the group actually did, include any required AI-use disclosure, and add the files to the shared repository with clear navigation.

The screenshots list October 27, 2026 as the due date and November 3 as the automatic extension deadline. Confirm course announcements before submitting.
