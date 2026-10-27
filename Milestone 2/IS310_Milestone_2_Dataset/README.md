# IS310 sports media dataset

Version 0.2 | Collected October 22, 2026 | Mason, Drew, and Bob

This is an initial custom dataset of 75 distinct public sports articles and interview transcripts, with 25 records for each strand. Each row records a source, an evidence paraphrase, and interpretive codes. It expands the six-row pilot without inventing observations or adding empty records to the count.

## Open the data

- `IS310_Sports_Media_Dataset.xlsx` is the filterable Excel workbook. The Dataset sheet contains every record; the Guide sheet explains fields and limitations.
- `data/sports_media_dataset.csv` is the UTF-8 CSV for the shared repository and computational work.
- `reports/collection_report.html` is a searchable collection page with links to all sources.
- `scripts/check_dataset.py` regenerates the collection page and quality report from the CSV. Run `python scripts/check_dataset.py` from this folder with Python 3. No extra packages are needed.
- `codebook.md` defines the codes, missing values, and review process.
- `collection_notes.md` explains sampling and the relationship to Milestone 2.

The Excel file and CSV contain the same saved observations. Later edits to one do not automatically update the other. The Python program reads the CSV; regenerate the workbook if you later change the CSV.

## What has been completed

All 75 rows have unique IDs and source URLs, access dates, source provenance, evidence notes, and codes. There are 25 soccer development and mobility items, 25 international NBA items, and 25 Formula 1 identity and allegiance items. The dataset meets the proposed size target. The structural checker was run on it.

## Source access and review

56 rows were checked using readable original-page text. 19 use indexed text from the source because direct opening failed or did not expose the article. Indexed text can be incomplete or outdated. The `access_method` and `inspected_scope` columns preserve this distinction; none of the excerpt-based records claim a complete article reading.

Dates were not displayed in the inspected text for NBA004, NBA005, F1009. These dates are deliberately blank. Two additional records use an explicitly labeled updated or edited date. Do not treat those dates as first publication dates or use blank dates as zeroes.

All 75 code assignments remain `provisional`: they were prepared with AI assistance and have not been independently reviewed by the students. Blank reviewer cells do not mean the sources are fictional; they mean no student review has been claimed. Review source passages, revise the flags, and enter actual names only after that work. For indexed-text records, inspect the original source first if possible.

This is a purposive English-language collection, not a representative survey of all coverage or fan opinion. The coding describes how texts frame sport; it does not establish that media caused relocation, fandom, or viewership growth. An organization reporting its own audience figures is recorded as a claim by that organization. Same-event articles can be separate records when their text and focus differ. Syndicated copies are not counted twice.

## What remains for Milestone 2

The dataset and computational artifact are prepared. The group still needs to review the coding, adapt the milestone narrative to the actual collection, read the scholarly sources in full where possible, and upload the files with clear repository navigation. The audit is a later comparison task; this package does not claim that it has been completed. This dataset package supersedes the earlier six-row pilot for collection purposes.
