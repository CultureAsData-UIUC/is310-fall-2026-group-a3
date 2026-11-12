# Instructor Feedback for Milestone 2

I really like the shared question your group developed around how sports media represent national identity and cross-border participation. Bringing together soccer mobility, international NBA players, and Formula 1 allegiance creates a potentially productive comparison without assuming that nationality works identically across the three sports.

The project also contains strong technical infrastructure and I particularly appreciate the distinctions among publisher and originator, publication and update dates, original-page and indexed-text access, and provisional and student-verified coding. These are thoughtful responses to real problems in working with changing web sources.

The shared documentation is also appropriately careful about the limits of the evidence. One row represents one article or interview rather than one athlete or audience, and the dataset records media representations rather than proving that media exposure causes movement, fandom, or audience growth. The purposive sampling strategy and English-language limitations are acknowledged rather than hidden.

However, there are two central issues that need to be addressed before I can evaluate this as three individual Milestone 2 submissions.

First, Milestone 2 was an individual assignment, but the package presents one shared 75-record dataset. The group documents assign 25 soccer records to Mason, 25 NBA records to Drew, and 25 Formula 1 records to Bob, but the repository does not clearly show which records, classifications, documentation, code, or research decisions each student personally completed.

Second, the README states that all 75 classifications were prepared with AI assistance, remain `provisional`, and have not been independently reviewed by the students. Every reviewer field is blank. This project therefore needs substantial revision and potentially resubmission, which I detail below.

## Individual Contributions and Project Directions

### Mason: Soccer Development and Mobility

Mason, your 25-record soccer strand provides a promising way to study how European academies, domestic pathways, national-team choices, passports, family movement, and professional opportunities become part of stories about player development. A question that fits your current evidence might be:

> How do U.S. soccer institutions and independent media frame international movement, domestic development, and national-team choice as pathways to elite opportunity?

Your current strand combines several different processes: moving abroad for development, growing up abroad because of family circumstances, transferring clubs for playing time, holding a passport that facilitates movement, choosing a national team, and developing through a domestic academy. These should not automatically be treated as the same form of mobility. Distinguishing them could become one of your most interesting contributions.

Your source sample also needs careful interpretation. Fourteen records come from U.S. Soccer and seven from *The Guardian*. Twenty-four are coded `development = yes`, all 25 are coded `national_identity = yes`, and only one clearly represents a domestic pathway. These patterns partly reflect the search and selection process rather than demonstrating that nearly all soccer coverage emphasizes development or national identity.

To turn this into a separate individual dataset, you could begin by copying the 25 soccer records into your own CSV and personally reviewing every source, evidence note, and classification. You could then revise the shared fields so that they distinguish academy development, professional transfers, family movement, passport or eligibility pathways, national-team choices, and domestic development. Rather than trying to cover soccer mobility generally, you might construct a focused comparison between U.S. Soccer and independent reporting, or between international and domestic pathways. Selective additional records could make that comparison more balanced, but careful verification and a clearer data model may be more valuable than simply adding rows.

Your revised dataset should also encode some of your own cultural interpretation rather than only recording source metadata and whether identity is mentioned. For example, you might distinguish whether movement is framed as opportunity, necessity, privilege, sacrifice, failure, or an expected route to success; whether agency is attributed to the player, family, club, federation, or passport access; and whether domestic development is treated as a viable alternative or a limitation. These categories should come from your close reading rather than being imposed in advance. Define them in your documentation, allow more than one interpretation or an `unclear` value where necessary, and retain an evidence note showing why you made each decision.

Your group proposed auditing U.S. Soccer player profiles by comparing their structured fields and biographical prose with the media records. I think this is a strong starting point because it asks what happens when a complex development pathway is reduced to a profile. However, the current audit template is empty, and the proposed five matched records should be treated as a pilot rather than a completed individual audit. For your final project, define a systematic set of players or profiles to examine and record what each profile says about birthplace, citizenship or eligibility, academy history, club movement, national-team representation, and development. Because U.S. Soccer also produced many of your custom media records, explain that you are comparing different representational forms within the same institutional ecosystem rather than treating the profiles as an independent or neutral authority. Your audit should identify patterns across the selected profiles and include specific evidence, not only describe what you plan to check.

### Drew: International NBA Players

Drew, your 25-record NBA strand offers a compelling way to connect league globalization, media framing, national representation, and audience relationships without assuming that an athlete belongs neatly to only one place. A question that fits the available evidence might be:

> How do NBA, team, governing-body, and independent media sources frame the relationships among international players, national representation, and audiences?

Your current articles can show how institutions and journalists describe international players and audiences. They cannot by themselves establish that television or digital media caused global NBA growth or increased viewership. If you retain those claims, you would need evidence that directly documents those systems or measurements.

The sample was found partly by pairing player names with terms such as country, identity, fans, and home. That is a reasonable discovery method, but it makes identity and audience frames more likely to enter the dataset. You should clarify whether your dataset compares institutional and independent sources, U.S. and home-country reporting, profiles and event-specific articles, or another clearly defined set of sources. The English-language boundary may exclude precisely the home-country perspectives most relevant to your question.

To turn this into a separate individual dataset, you could copy the 25 NBA records into your own CSV, personally verify them, and redesign the sample around a clearly stated comparison. For example, you might compare how NBA or team sources and independent reporting represent the same players, or compare U.S. coverage with a smaller set of sources connected to players' home countries. Your revised dataset should document the number of records per player, publisher, source type, and event so that repeated coverage of one athlete does not silently receive more analytical weight. You could then audit official NBA player profiles to ask which relationships are preserved as structured data and which appear only in narrative media coverage.

Your revised dataset should move beyond recording that national identity or audiences appear and encode how those relationships are culturally framed. You might distinguish whether a player is presented as a national representative, global celebrity, diasporic connection, commercial market, local hero, or person with several forms of belonging. You could also record whether an audience relationship is measured, quoted directly, asserted by the league, inferred by a journalist, or represented through a single anecdote. Preserve who makes each claim and include uncertainty when an article does not support a confident interpretation. A documented interpretive field of this kind would let you analyze how NBA globalization is narrated rather than simply count country references.

Your group proposed matching the media records to NBA player profiles and statistics pages. This is a productive audit direction because an official profile may reduce a player's relationship to nation and place to one country label while media coverage describes citizenship, family history, national-team representation, audiences, and several forms of belonging. The five proposed comparisons are a useful pilot, but they are not yet a completed individual audit. For your final project, identify a systematic group of players and document the fields, labels, prose, omissions, and access conditions in their official profiles. Be especially careful when comparing current profiles with historically dated articles, since a present-day affiliation may not describe the player at the time of the media record. Your audit should produce a structured file and an analysis of recurring patterns rather than only a set of illustrative profile examples.

### Bob: Formula 1 Allegiance

Bob, your 25-record Formula 1 strand is particularly well suited to studying overlapping forms of national and organizational allegiance. A driver's nationality, a constructor's registration, a team's operational base, a manufacturer's identity, a race location, and an audience's attachments may all point toward different places. A focused question might be:

> How do Formula 1 media sources frame relationships among drivers, constructors, national identities, race locations, and audiences?

The shared cross-sport categories do not yet preserve all the relationships that make Formula 1 distinctive. You might add fields for driver representation, constructor or team identity, team base, manufacturer identity, race or audience location, the object of audience support, and the source making the claim about allegiance. This would avoid compressing support for a driver, team, constructor, manufacturer, or national symbol into one national-identity flag.

Your strand is concentrated in five drivers and English-language sources, including substantial Formula1.com material. That could support a focused institutional-versus-independent comparison, but it should not be presented as representative of global Formula 1 audiences. Claims made by journalists, drivers, teams, or Formula 1 about fan allegiance should also remain distinct from direct evidence supplied by audiences themselves.

To turn this into a separate individual dataset, you could copy the 25 Formula 1 records into your own CSV, personally verify them, and replace the broad cross-sport fields with a Formula 1-specific structure. You might build the dataset around the five existing driver cases while recording the driver, constructor, manufacturer, race location, claimed audience, object of allegiance, and speaker making the claim. This would let you compare institutional Formula1.com narratives with independent reporting without claiming to measure audience attitudes directly. An audit of Formula1.com or FIA driver and constructor profiles could then show how structured platform fields simplify these overlapping identities.

Your revised dataset should also encode how allegiance is being interpreted, not only which national labels appear. You might distinguish whether a source frames allegiance as overlapping, competing, inherited, commercial, event-specific, or explicitly nationalistic; whether support is directed toward a driver, team, constructor, manufacturer, or nation; and whether the evidence comes from a fan quotation, journalist, driver, team representative, or institutional publication. These categories should preserve the possibility that several allegiances coexist in one article. Define the categories through examples, retain the evidence supporting each classification, and use `unclear` rather than forcing ambiguous cases into a single interpretation.

Your group proposed auditing Formula 1 driver and team profiles, including the Ferrari team profile. This is a particularly good fit for your question because the platform must decide how to represent driver nationality, constructor registration, manufacturer identity, team base, and current affiliation. The five proposed comparisons provide a useful pilot, but the template contains no completed observations and does not yet constitute your individual audit. For your final project, define a systematic set of drivers, constructors, or seasons and record which relationships appear as structured labels, which appear only in prose, and which are absent or ambiguous. Since Formula1.com also produced several of your media records, treat this as an audit of different representational forms within the Formula 1 information ecosystem rather than as a neutral external check. Your completed audit should show patterns across profiles and preserve changes over time rather than relying only on current profile values.

## Opportunity to Submit Individual Revisions and Next Steps for Final Projects

You may keep your current provisional Milestone 2 grades or submit individual revisions for reconsideration. Revising Milestone 2 is optional. **Developing three clearly distinct individual projects for the final submission is not optional.** Whether or not you resubmit this milestone, you should begin separating your research questions, datasets, documentation, audits, code, and interpretations now.

You may continue to share the broader group theme and reuse genuinely shared infrastructure such as the schema, validation script, or repository organization. However, the final submission cannot remain one 75-record dataset divided informally among three people. Each student will need an identifiable individual dataset, research question, audit, analysis, reflection, and data essay. The repository and Git history should make it possible to see who completed each part.

The shared profile-audit framework may also be reused, but one collective set of 15 comparisons cannot count as three completed individual audits. Each student should define, carry out, document, and interpret an audit appropriate to their own sport and research question. The five comparisons proposed for each strand can serve as an initial pilot, but the final audit should use a clearly explained scope and produce enough evidence to identify patterns rather than only isolated examples.

If you decide to resubmit, please create clearly labeled individual folders inside `Milestone 2` now:

```text
Milestone 2/mason_soccer_mobility/
Milestone 2/drew_international_nba/
Milestone 2/bob_formula_1_allegiance/
```

Each folder should contain:

- An individual `README.md` explaining the research question, scope, unit of analysis, selection process, and relationship to the shared project.
- A structured data file containing the records the student personally reviewed and intends to claim.
- An individual reflection discussing the process, interpretive decisions, challenges, use of AI, and remaining uncertainties.
- An audit plan specifically connected to the individual strand.
- A brief revision log recording which AI-assisted descriptions or classifications were confirmed, changed, rejected, or left uncertain.
- Any individual code or computational outputs that you created or substantially revised.

Each individual dataset should include at least one clearly documented interpretive field developed through your own reading of the sources. The documentation should explain how the categories were developed, give examples of what qualifies for each value, preserve the evidence supporting each classification, and record disagreement or uncertainty. The goal is not to add subjective labels without explanation, but to make your cultural interpretation transparent, reviewable, and available for analysis.

For every record you claim in your individual dataset, personally inspect the available source, check the evidence note, confirm or revise the classifications, preserve uncertainty, and enter your name in the reviewer field only after completing that work. Your documentation should also explain what you originally contributed to the shared project and what you subsequently changed or developed independently.

Because the group benefited from a shared schema, codebook, validation script, reports, and collection infrastructure, each final project should demonstrate additional individual depth. This might involve better source verification, more appropriate interpretive categories, a clearer comparison, a developed audit, selective additional collection, stronger scholarship, or more transparent documentation of uncertainty. It does not necessarily require collecting 50 entirely new records, but simply copying the existing 25 rows into separate files will not be sufficient.

If you choose to resubmit Milestone 2 for reconsideration, please submit the revision before Fall Break. If you do not resubmit, the current provisional grade will remain or I can drop the grade for Milestone 2 entirely and just weight your grade to final project. Please let me know in Slack which option you would prefer.

Overall, this is a strong collective foundation. The next step is to use that foundation to make each of your individual research and interpretation clearly distinguishable, independently documented, and appropriate for three separate final projects.
