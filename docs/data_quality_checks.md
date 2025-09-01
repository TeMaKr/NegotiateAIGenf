# Data Quality Checks

## Session 1-4

When comparing with the raw data from session 1 we found that there are 2 files missing in our newly scraped dataset for NegotiateAI3.0. These 2 documents are in-session documents, which means they are not part of the requested data set (see Arbeitspapier).

- <https://apps1.unep.org/resolutions/uploads/proposal_from_saudi_arabia_bahrain_egypt_and_qatar_for_paragraph_2_of_rule_37_of_the_draft_rules_of_procedure.pdf#overlay-context=node/344/revisions/11895/view%3Fq%3Dnode/344/revisions/11895/view>
- <https://wedocs.unep.org/bitstream/handle/20.500.11822/41322/Proposal%20for%20consolidated%20language%20on%20rule%2037%20of%20the%20draft%20Rules%20of%20Procedure.pdf?sequence=3&isAllowed=y>

In sessions 2, 3, and 4, we found that the NegotiateAI3.0 dataset contains all documents present in the NegotiateAI2.0 dataset and also an additional 103 entries that were not present in the NegotiateAI2.0 dataset. This indicates that the new scraping method has successfully captured all data from the NegotiateAI2.0 dataset while adding new entries. For session 3 there is one duplicate which we removed from the new dataset. There is also a contribution for which there is no access to the PDF file. We have not excluded the data from the database, but we have set the documentation to check ‘false’. <https://resolutions.unep.org/resolutions/?q=user/login&destination=uploads/ghana_1.pdf#overlay-context=INC3PlenaryStatements%3Fq%3DINC3PlenaryStatements>

## Session 5

When comparing the raw data from session 5, it initially appears that the NegotiateAI2.0 dataset contains more entries. Further analysis shows that the NegotiateAI2.0 dataset contains 10 duplicate entries, from which it can be concluded that at least 5 entries are missing from the NegotiateAI2.0 dataset. A manual check of the href links, each of which cannot be found in the other dataset, confirms that there are 5 new data entries in the NegotiateAI3.0 dataset:

- <https://resolutions.unep.org/incres/uploads/article_16_0.pdf>
- <https://resolutions.unep.org/incres/uploads/cg2_philippines_text_proposal_on_article_7_emissions_and_releases_1.pdf>
- <https://resolutions.unep.org/incres/uploads/crp_on_moi_submitted_africa_grulac_fiji_cook_island_fsm_26_nov_2024_1_0.pdf>
- <https://resolutions.unep.org/incres/uploads/eums_and_chile_document_on_epr_for_inc5_-_25112024_1_0.pdf>
- <https://resolutions.unep.org/incres/uploads/scope_0.pdf>

At the same time, one data record in the 2.0 data set is no longer valid: <https://resolutions.unep.org/incres/uploads/pan_col_ecu_sal-text_proposal_art_6_production_and_supply.pdf>

Since the NegotiateAI2.0 dataset contains 5 entries that have no href link, and one of these entries was categorized under draft_category “scope”, it is likely that this corresponds to the entry <https://resolutions.unep.org/incres/uploads/scope_0.pdf>.

Thus, the analysis explains the difference of 5 entries between the datasets and confirms that the new scraping method has successfully captured all data from the NegotiateAI2.0 dataset while adding new entries.

## Requested Data (see Arbeitspapier)

| Session | document type                | url                                                                       |
|---------|------------------------------|---------------------------------------------------------------------------|
| 1       | statements                   | https://www.unep.org/inc-plastic-pollution/session-1/statements           |
| 1       | pre session submissions      | https://www.unep.org/inc-plastic-pollution/session-1/submissions          |
| 2       | statements                   | https://www.unep.org/inc-plastic-pollution/session-2/statements           |
| 2       | insession document           | https://www.unep.org/inc-plastic-pollution/session-2/documents/in-session |
| 2       | pre session submissions      | https://www.unep.org/inc-plastic-pollution/session-2/submissions          |
| 3       | statements                   | https://www.unep.org/inc-plastic-pollution/session-3/statements           |
| 3       | insession document           | https://www.unep.org/inc-plastic-pollution/session-3/documents/in-session |
| 3       | pre session submissions      | https://www.unep.org/inc-plastic-pollution/session-3/submissions          |
| 4       | statements                   | https://www.unep.org/inc-plastic-pollution/session-4/statements           |
| 4       | insession document           | https://www.unep.org/inc-plastic-pollution/session-4/documents/in-session |
| 5       | insession document           | https://resolutions.unep.org/resinc/cg1-gs-m-textual-inc5                 |
| 5       | insession document           | https://resolutions.unep.org/resinc/cg2-gs-m-textual-inc5                 |
| 5       | insession document           | https://resolutions.unep.org/resinc/cg3-gs-m-textual-inc5                 |
| 5       | insession document           | https://resolutions.unep.org/resinc/cg4-gs-m-textual-inc5                 |
