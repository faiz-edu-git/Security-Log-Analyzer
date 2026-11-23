# Weekly Log

Record of weekly progress, decisions, problems and plans. One entry per week.

## Week 1 (17 to 23 November 2026)

### Work completed
**Alishba Rafaqat**
- Created the first dataset, `sample_logs.csv`, with normal activity and example attacks (17 Nov).
- Extended it to 63 data rows with negative cases, boundary cases (one below, at and above the planned thresholds), and 6 deliberately malformed lines (18 Nov).
- Wrote `docs/data_dictionary.md`: input fields, validation rules, event types, normalized event schema (19 Nov).
- Clarified that the timestamp is a datetime object inside the program and text when saved (21 Nov).
- Added the proposed detection thresholds for R1 to R5 and the labelling method, with the expected alerts and rejected lines for `sample_logs.csv` (22 Nov).

**Faizullah Khan**
to be written by Faiz

### Decisions
- Log format: CSV with six fields (`timestamp, source, event_type, username, source_ip, message`).
- Required fields: lines with a missing required field are rejected. Only `message` may be empty.
- Timestamp: two input formats accepted, one normalized format.
- Rule messages are kept neutral so detection depends on event patterns, not keywords.
- Proposed thresholds: R1 5 in 120 s, R2 5 failures then success, R3 any privilege change, R4 8 in 60 s, R5 3 in 120 s. To be confirmed by Faizullah.

### Problems and how they were handled
- GitHub shows a warning on the CSV preview because of the malformed lines. These lines are intentional and will be explained in the README.
- The two event format documents did not match (sources, missing-field handling). Fixed by aligning `event_format.md` with the data dictionary.

### Plan for Week 2 (24 to 30 November)
- `config.json` with the thresholds (Alishba).
- Design document and architecture diagram (Alishba).
- Threat model: assets, threats, assumptions, ethics (Alishba).
- Literature review: 4 sources each, and a comparison matrix.
- Rule specifications for R1 to R5 and the alert format (Faizullah).
- Prepare the D2 package.
