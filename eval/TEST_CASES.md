# Legixo Thinklabs - Test Cases

This document outlines the 23 test cases used to evaluate the Legixo API pipeline.

| ID | Type | Question | Expected Facts | Expected Sources |
|---|---|---|---|---|
| 1 | in_corpus | What notice period applies when Bluecrest or Priya Nambiar ends the employment agreement? | 60 days, written notice, laptops, badges, source code access | 02_employment_agreement_excerpt.md |
| 2 | in_corpus | How long is the non-compete after leaving Bluecrest, and when does it apply? | 12 months, direct competitor, same city, client list | 02_employment_agreement_excerpt.md |
| 3 | in_corpus | What kinds of information are called out as confidential in the Bluecrest excerpt? | pricing sheets, unreleased product roadmaps, customer names, confidential in writing | 02_employment_agreement_excerpt.md |
| 4 | in_corpus | What is the civil suit number and who are the parties in the transport invoice dispute memo? | CV-2024-8812, Arvind Mehta, Northfield Logistics Pvt. Ltd., unpaid invoices, March, June 2024, damaged goods, offsets | 01_matter_memo_arvind_v_northfield.md |
| 5 | in_corpus | Under the memo, what limitation period applies to contract claims under the fictional Riverside Code? | three years, breach date | 01_matter_memo_arvind_v_northfield.md |
| 6 | in_corpus | When is the next hearing in Arvind Mehta v. Northfield, and what is scheduled? | 15 August 2025, witness, plaintiff, billing head | 01_matter_memo_arvind_v_northfield.md |
| 7 | in_corpus | How many clear days before the listed date must parties file written arguments under the hearing notice rules? | seven clear days, late filings, leave of court | 03_hearing_notice_template.md |
| 8 | in_corpus | What time is case CV-2024-8812 listed, and what is it for? | 11:00 a.m., invoice, set-off | 03_hearing_notice_template.md |
| 9 | in_corpus | What happened to case CV-2023-4401 (Lakeview Society v. City Water Board), and what is the next date? | adjourned, 22 September 2025, water supply, interim relief | 03_hearing_notice_template.md |
| 10 | in_corpus | For commercial suits above five lakh fictional rupees, what does Section 14 say about mediation? | mandatory mediation, 30 days, waive in writing | 04_statute_style_excerpt_fictional.md |
| 11 | in_corpus | If a contract fixes no interest rate, what rate may be awarded on admitted dues under Section 22? | 9%, simple interest, date of demand | 04_statute_style_excerpt_fictional.md |
| 12 | in_corpus | What settlement offer did Northfield make in the counsel notes, and what counter-instruction did the client give? | 70%, 85%, counterclaim, 1 August 2025, witness | 05_counsel_notes_settlement.md |
| 13 | in_corpus | Are the settlement talks described in the counsel notes binding? What is the reminder? | without prejudice, term sheet | 05_counsel_notes_settlement.md |
| 14 | in_corpus | Who is the lessor and lessee for Unit 4B at Harbor View Tower, and what is the monthly rent? | Kiran Patel, Harbor Bean Roasters OPC, 45,000 | 06_property_lease_clause.md |
| 15 | in_corpus | What is the security deposit amount, and within how many days must it be refunded after handover? | 1,35,000, 45 days, no damage beyond normal wear | 06_property_lease_clause.md |
| 16 | in_corpus | Is subletting allowed for the Harbor View lease without extra steps? | not allowed, written consent, lessor | 06_property_lease_clause.md |
| 17 | cross_document | In the Arvind Mehta v. Northfield dispute, what is the next hearing date and what settlement offer was made? | 15 August 2025, witness, 70%, 85% | 01_matter_memo_arvind_v_northfield.md, 05_counsel_notes_settlement.md |
| 18 | cross_document | What mediation requirements exist and could they apply to the Arvind Mehta transport invoice case? | mandatory mediation, 30 days, five lakh, CV-2024-8812 | 04_statute_style_excerpt_fictional.md, 01_matter_memo_arvind_v_northfield.md |
| O1 | out_of_corpus | What is the population of Riverside city? |  |  |
| O2 | out_of_corpus | What penalty applies if Priya breaches the non-compete? |  |  |
| O3 | out_of_corpus | Who won case CV-2024-8812? |  |  |
| E1 | edge_case | Hi |  |  |
| E2 | edge_case | Tell me everything about all the documents |  | 01_matter_memo_arvind_v_northfield.md, 02_employment_agreement_excerpt.md, 03_hearing_notice_template.md, 04_statute_style_excerpt_fictional.md, 05_counsel_notes_settlement.md, 06_property_lease_clause.md |
