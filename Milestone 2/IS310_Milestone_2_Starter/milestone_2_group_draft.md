# Sports media and national identity across borders

## Milestone 2 initial custom dataset and audit plan

Mason, Drew, and Bob | IS310 | October 22, 2026

**Status:** Proposed group approach with six provisional pilot records. Collection, student verification, and the audit remain incomplete. Future-tense sections describe proposed work, not activities already performed by the group.

## Project focus

Our Milestone 1 theme was how sports become part of national and global culture through television and digital media. We will connect our three interests by studying how public sports coverage describes belonging across national borders. Mason's strand concerns athlete development and relocation, Drew's concerns international NBA players and their connections to audiences outside the United States, and Bob's concerns national allegiance when Formula 1 drivers and teams represent different places.

Our shared research question is: **How do sports media describe the relationship between national identity and cross-border participation through athlete development, international NBA stars, and Formula 1 allegiance?**

We will look for recurring ways of presenting athletes and teams: development opportunities, national representation, hometown connection, global celebrity, and overlapping or competing loyalties. These categories connect the strands without assuming that soccer, basketball, and Formula 1 work identically. Our dataset will document media representations. It will not by itself establish that media exposure causes migration or increases viewership.

## Initial custom dataset

We propose a 75-item dataset with 25 items per strand. One item will be one distinct public article or official interview transcript, rather than one athlete, quotation, or social media reaction. An article that discusses several athletes will remain one record. A syndicated copy of the same story will not count as another item.

The starter currently contains six records: two soccer development articles, two NBA articles, and two Formula 1 items. All six contain real source URLs, retrieval dates, evidence locators, short paraphrases, and provisional coding. No blank rows have been counted toward the target. The pilot is a convenience sample for developing the method and cannot support general claims about sports coverage.

The collection window will cover materials published from January 1, 2017 through October 22, 2026. This period accommodates the historical development and identity stories already present in the pilot. We will record publication dates separately from retrieval dates. Accounts of earlier events can appear in eligible articles, but the article publication date determines eligibility. We will avoid interpreting the collection as a time trend because it does not sample every year evenly.

### Proposed contributions

| Strand | Proposed lead | Planned material | Target |
|---|---|---|---:|
| Athlete development and mobility | Mason | Soccer articles discussing pathways, opportunities, relocation, and domestic alternatives | 25 |
| International NBA players | Drew | Stories about international players, national representation, audience connections, and global visibility | 25 |
| Formula 1 allegiance | Bob | Coverage and transcripts about driver, team, and national identification | 25 |

Each lead would add 23 records beyond the two pilot items in their strand. For NBA coverage, we will include the Milestone 1 examples of Jokic, Antetokounmpo, Doncic, and Gilgeous-Alexander where eligible sources are available. For Formula 1, we will add Antonelli and other cases where driver and team identification differ. For soccer, we will add multiple athletes and keep examples of domestic development so that relocation is not treated as the only path to success.

We propose including at least 10 independent reporting items per strand and no more than 15 items produced by governing bodies, teams, or leagues. Record the actual originator: an Associated Press article hosted by a league remains independent reporting. Aim for at least four focal athletes per strand and cap each focal athlete at eight records. These are sample-design choices, not course requirements. If the pilot or available material makes them impractical, revise and document the change before expanding.

## Selection and exclusion

Include a source when its readable text substantially discusses athlete development, cross-border participation, national identification, or audience belonging relevant to one of the strands. A neutral or contrary example is eligible; a positive statement about national pride is not required. Use English-language sources initially and acknowledge that this excludes important perspectives, particularly Italian coverage of Formula 1 and home-country reporting about NBA players.

Exclude score-only recaps, transfer lists without relevant discussion, rumors lacking an attributable source, unreadable paywalled text, duplicates, and materials outside the publication window. Do not infer an athlete's race, citizenship, ethnicity, or personal motivation from appearance, birthplace, or name. Do not infer fan nationality from the location of a publisher.

For reproducibility, each member will record their searches, dates, candidate URLs, and exclusions in a collection log. Search combinations will pair athlete names with terms such as development, moved, fans, nationality, country, and identity. Search results are a discovery tool; final coding requires reading the relevant original text. Because this is purposive sampling, counts describe our selected corpus rather than all sports media.

## From cultural material to working representation

Our cultural materials are the original articles and interview transcripts, including their wording, speakers, publication context, and intended audiences. We will turn each selected item into a working record containing a source label, URL, date, focal subject, relevant text location, and brief evidence paraphrase.

The pilot retains short paraphrases and locators instead of reproducing full articles. For example, a locator can name a section heading or a speaker's answer. Students will check these locations against the original page and may keep brief private research notes where permitted. The representation loses visual layout, video performance, images, tone, and other surrounding context. An online transcript is a representation of a spoken event; it is not equivalent to watching the original broadcast.

## From working representation to structured data

We will convert the working records to a UTF-8 CSV using a common codebook. Each row has a stable identifier, strand, sport, source provenance, subject, evidence, and codes. The four shared flags are development, national identity, audience connection, and competing allegiance. They are multi-label: a record can receive more than one flag.

Each flag uses `yes`, `no`, or `unclear`. `No` means the feature was not found in the text scope inspected; it does not mean the real-world phenomenon does not exist. `Unclear` is used when the available evidence cannot support a decision. A separate movement field distinguishes relocation discussed, domestic pathway, and not established. Representing a national team or traveling for a match does not automatically count as relocation.

An evidence note supports the code, while a scope field identifies whether the coder inspected an article body or a specific portion. Each record also stores reviewer and review status. The starter's codes were suggested with AI assistance and have not been verified by group members. Students should enter their own names only after review. A second member will independently recode at least five items per strand; the group will discuss disagreements and log changes before finalizing categories.

## Computational process

The accompanying Python program reads the CSV and checks required fields, identifiers, duplicate URLs, dates, allowed categories, and the relationship between review status and reviewer names. It reports the number of records per strand, items still needed to reach the proposed target, and records awaiting review. It also generates an HTML collection page with source links and evidence notes.

This program has been run on the six-row starter. It does not scrape more items, infer nationality, verify quotations, or decide cultural meaning. It demonstrates how computation can help organize and inspect a small custom dataset while leaving interpretation to the group. The code, input CSV, and generated reports should be retained together in the repository.

## Audit and connection plan

We propose auditing **official athlete and team profile collections** against our custom media records. The comparison asks which aspects of national identity and cross-border participation become structured profile fields, which appear only in biographical prose, and which are not represented on a given page.

Starting collections are the [U.S. Soccer player profiles](https://www.ussoccer.com/players/p/christian-pulisic), the [NBA player statistics collection](https://www.nba.com/stats/player/203507//), and [Formula 1 driver profiles](https://www.formula1.com/en/drivers). The [Ferrari team profile](https://www.formula1.com/en/teams/ferrari) provides a separate team context. These are named audit targets, not completed audit observations.

We will select 15 matched comparisons, five per strand, linking one custom item to one official athlete or team profile. An audit row will retain the custom item ID, matched subject, profile URL, access date, exact inspected section, field or concept being checked, and evidence. We will look for nationality or country, current affiliation, development history, migration motivation, audience connection, and allegiance. Birthplace, citizenship, sporting representation, and team base must remain separate concepts.

For each concept, record `structured_field`, `prose_only`, `not_found_in_inspected_scope`, `unclear`, or `not_applicable`. A blocked page is `unclear`, not evidence that a field is missing. We will examine both the page's displayed fields and its biography where accessible, then document the scope. The empty audit CSV in this package is a recording template and contains no findings.

The main comparison will ask whether information that matters in cultural narratives survives the conversion into a player or team profile. We will also check how one country label handles multiple affiliations. Formula 1 needs particular care: a team's base, constructor identity, and driver's nationality do not mean the same thing. An absent audience field is a limit of what a profile can answer, not automatically an error or evidence of bias.

The audit will describe each collection separately before comparing patterns. Different page designs and institutional purposes make raw cross-sport missing-field rankings misleading. Current profiles and historical articles also refer to different moments; changes in club or team should be checked against dates before being labeled inconsistencies. No completed audit is claimed for this milestone starter.

## Scholarly context

**Rowe, D. (2003). Sport and the repudiation of the global. *International Review for the Sociology of Sport, 38*(3), 281-294. https://doi.org/10.1177/10126902030383002**

The available abstract questions whether global sport remains dependent on national cultural difference. This gives us a reason to examine national identification alongside international participation. We will use it to frame a question, rather than assuming that global circulation erases national loyalties. Full-text access was restricted during preparation; the discussion here is based on the publisher's abstract.

**Stead, D., & Maguire, J. (1998). Cricket's global 'finishing school': The migration of overseas cricketers into English county cricket. *European Physical Education Review, 4*(1), 54-69. https://doi.org/10.1177/1356336X9800400106**

The abstract connects sporting migration with development pathways and athletes' motives, drawing on directory analysis and interviews. This supports keeping pathway and motivation as separate ideas in our soccer coding. Its cricket setting also requires caution: we will not transfer its findings directly to soccer, the NBA, or Formula 1. The preparation used the publisher's abstract; the group should read the article before making detailed claims about its results.

**Entman, R. M. (1993). Framing: Toward clarification of a fractured paradigm. *Journal of Communication, 43*(4), 51-58. https://doi.org/10.1111/j.1460-2466.1993.tb01304.x**

This published framing study provides a methodological starting point for distinguishing an event from how a text presents it. We will use that distinction when separating factual affiliations from interpretations about belonging. The bibliographic record was verified during preparation, but full-text access through the publisher was unavailable. The group should read it through the library before refining the framing method or attributing specific arguments to it.

## Initial reflection and feedback needed

At this stage, the strongest connection between our strands is that athletes can belong to several places at once, while media and data systems must decide which connections to emphasize. The shared record format makes the strands comparable without combining their sports-specific details into one nationality label.

The pilot has clear limits. It is too small for conclusions, its NBA strand is concentrated on one athlete, and it contains more institution-hosted material than we want in the expanded collection. The historical examples span different contexts, and the current English-language restriction narrows the perspectives represented. A domestic development case has been kept to challenge the assumption that sporting development always requires international relocation.

We need feedback on whether our shared question is focused enough, whether the instructor expects one 50-100-item group dataset or additional individual datasets, and whether official profile collections are suitable audit targets for this project. We also need to check whether later stages should add a small translated sample. We will not claim that these questions have already been answered.

## Proposed completion schedule

By October 23, review the six starter records, agree on category definitions, and read the scholarly sources. By October 25, aim to add 23 records per strand. By October 26, complete the cross-review, run the checker, revise the reflection, and organize repository links. Aim to submit October 27. If the group uses the extension shown in the assignment screenshots, revise the schedule toward November 3 and state the actual collection status. These are suggested dates, not commitments already agreed to by group members.

## Repository organization

Keep this draft, `codebook.md`, `data/`, `scripts/`, and `reports/` in one milestone folder. Add a link from the repository's main README to this folder's README. The folder contains the initial dataset, explanation of both transformations, computational artifact, named audit targets, reflection, and scholarly context. Collection and student verification remain the main work needed before submission.
