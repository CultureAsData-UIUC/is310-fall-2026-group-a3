# Instructor Feedback for Milestone 2

This is a very ambitious and thoughtful project. I really like the question of how media frame tennis players who change national representation and what a single country code hides about citizenship, federation affiliation, birthplace, residence, training, belonging, and political conditions. The comparison between a multilingual media dataset and the Sackmann match data gives the custom dataset and audit a particularly clear relationship.

You have documented the research process in depth. I especially appreciate that you preserve conflicting dates and statuses rather than silently resolving them and distinguish structural validation from interpretive accuracy. The project is already producing an important finding: a single country code can be applied backward across historical match records or remain attached while a player competes without a national flag.

## Initial Custom Dataset

Your research question is strong, but I would be careful with the phrase **nationality switching**. The cases include federation changes, citizenship or residency changes, neutral competitive status, and changes imposed by governing bodies rather than initiated by players.

Your notes already recognize these distinctions. Kasatkina’s Australian representation and permanent residency should not automatically be described as citizenship, while Rublev and Sabalenka did not switch federations when their flags were removed. Consider fields such as:

- `representation_before` and `representation_after`
- `representation_change_type`
- `legal_status`
- `effective_date`, `announcement_date`, and `first_event_under_new_representation`
- `status_source` and `status_uncertainty`

This would prevent `from_nation`, `to_nation`, and `switch_year` from suggesting that every case represents one clear legal change between nationalities.

### Sample and Unit of Analysis

One row represents one media item, which is a sensible unit for studying framing. The ten-player sample is also thoughtfully constructed. However, it is heavily shaped by one geopolitical context: Russian or Belarusian players, Kazakhstan recruitment, and post-2022 neutral status. This is appropriate if the final argument remains focused on these cases rather than becoming a general claim about all tennis players who change representation.

I would keep Rublev and Sabalenka, but identify them as neutral-status comparison cases rather than federation switchers. Seven or eight items per player supports exploratory case comparisons, but not broad claims about how all media frame each player. Analysis by frame, outlet location, language, and case type may be more productive, with individual players used as close examples.

### Collection and Multilingual Evidence

The collection history is one of the strongest parts of the submission. You document searches, exclusions, robots.txt decisions, failed requests, syndication, hashes, duplicate removal, language coverage, and the transformation from web pages into structured records.

The resulting outlet distribution should be interpreted as the shape of the collected sample, not as a measure of the actual distribution of media attention. Gaps in Georgian, Belarusian, and Australian sources are especially important because those perspectives might complicate Russian and international coverage.

Because AI assisted with multilingual reading and translation, either independently check important quotations with a knowledgeable reader where possible or state clearly which translations remain machine-assisted and unverified.

### Framing and Interpretation

The codebook changed in response to the evidence, which is a major strength. Adding `national_claiming` and `multiple_identity`, reducing `other`, and broadening `opportunity_funding` show the data reshaping the categories.

The categories still operate at different analytical levels. `politics_war` describes context, `opportunity_funding` describes a motivation or resource relationship, `loyalty_betrayal` describes an evaluative frame, and `multiple_identity` describes represented belonging. Explain these differences rather than presenting the primary and secondary labels as one simple scale.

The final essay would benefit from concrete examples:

- One straightforward classification
- One classification changed after a full reading
- One event framed differently by old-country and new-country outlets
- One uncertain case that did not fit the categories cleanly

The Putintseva podcast comparison and contrasting responses to Kasatkina appear especially useful.

## Auditing the Sackmann Data

The Sackmann audit is very well connected to the custom dataset. It already identifies that current country codes appear in earlier historical rows, neutral status is not represented, Dzalamidze’s doubles career is largely absent from the singles files, and one code cannot represent citizenship, residence, birthplace, training, federation, and belonging.

The pinned archival mirror is a defensible audit source if you document its provenance, commit, license, and relationship to the unavailable original repositories. Use official ATP, WTA, ITF, federation, or tournament sources to verify consequential dates rather than adding another large dataset only for comparison.

The next important question is why historical rows contain present-day codes. Were the original values recorded at the time of each match, or were historical files later generated by joining matches to a current player table? Until you establish that process, describe this as an observed property of the mirror rather than intentional historical backdating.

### Where Do the Codes Come From?

The provenance of the codes themselves also needs investigation. Your `from_nation` and `to_nation` values are manually entered in `players.csv` and copied into the media dataset. The validator confirms only that they contain three capital letters or equal `NEUTRAL`; it does not confirm that they belong to a documented vocabulary.

Similarly, Sackmann calls its field `ioc`, but that name alone does not establish whether the values originated with the IOC, ATP, WTA, another provider, or Sackmann’s own transformations. The current sample obscures this problem because values such as `RUS`, `KAZ`, `AUS`, `GEO`, and `BLR` overlap across several coding systems.

I would encourage you to investigate the history and institutional purposes of these systems. [ISO 3166](https://www.iso.org/iso-3166-country-codes.html?content_language=English) provides codes for representing country names, while IOC and sporting codes represent National Olympic Committees or competitive delegations. These systems overlap but are not interchangeable. They may also treat territories, historical countries, refugee teams, and neutral competitors differently.

`NEUTRAL` is currently your analytical category rather than a verified source code. Consider separating:

- `source_code`
- `code_system`
- `country_or_delegation`
- `representation_status`
- `normalized_comparison_code`

Preserve the original source value before translating it into your own analytical categories. The history and provenance of the codes could become one of the project’s strongest cultural-data arguments.

## Computation and AI-Assisted Work

The computational workflow is extensive and well documented, and I appreciate the transparency of your AI disclosure. For the final essay, though, I would make your own intellectual contribution visible through examples of decisions you changed, rejected, or left uncertain from working with Claude. The fact that the second pass changed 51 of 77 rows is important methodological evidence about why polished AI classifications still require human review.

There is also an important CSV issue to correct. Extra unquoted commas in `uncertainty_note` cause values to shift into `reviewed_by` and an unnamed field in 44 records. Rewrite the CSV through `csv.DictWriter` or Pandas, check for `None in row`, validate the allowed reviewer names, rerun the reports, and manually inspect several repaired records before analysis.

## Scholarship and Reflection

The scholarship is relevant and explained rather than merely listed. I would prioritize close engagement with these sources over adding many more citations, although scholarship on media framing or tennis-specific national representation could help interpret the outlet comparisons.

## Priorities for the Final Project

To answer your reflection questions:

- The Sackmann mirror is defensible if its provenance and limitations remain explicit.
- Keep Rublev and Sabalenka as neutral-status comparison cases.
- The new framing categories are defensible, but explain their different analytical levels.
- Seven or eight items per player supports exploratory comparison, especially by frame and outlet context.
- Keep the AI disclosure prominent and include concrete examples of your corrections and uncertainties.

As for next steps, I would recommend:

- Repair the malformed CSV and strengthen the validator.
- Distinguish citizenship, legal status, federation affiliation, sporting representation, and neutral status.
- Identify the authority, history, and purpose behind every country-code field.
- Preserve source codes separately from your analytical categories.
- Verify important multilingual quotations and representation-change dates.
- Investigate how Sackmann’s historical match codes were generated.
- Compare frames and outlet contexts while retaining the underlying counts.
- Revise the remaining AI-drafted prose in your own voice and foreground decisions you personally made.

Overall, this is a very strong project with a clear cultural question, transparent provenance, substantial computation, a meaningful audit, and thoughtful reflection on AI-assisted research. The immediate priorities are repairing the CSV and clarifying what the country codes represent, where they came from, and which institutional histories they carry. Addressing those issues should position the project to make a compelling argument about what sports data and media narratives reveal or erase about national belonging.