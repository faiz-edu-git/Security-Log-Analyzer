# Weekly Log

Record of weekly progress, decisions, problems and plans. One entry per week.

## Week 1 (17 to 23 November 2026)

### Work completed

#### Alishba Rafaqat
- Created the first dataset, sample_logs.csv, with normal activity and example attacks (17 Nov).
- Extended it to 63 data rows with negative cases, boundary cases (one below, at and above the planned thresholds), and 6 deliberately malformed lines (18 Nov).
- Wrote docs/data_dictionary.md: input fields, validation rules, event types, normalized event schema (19 Nov).
- Clarified that the timestamp is a datetime object inside the program and text when saved (21 Nov).
- Added the proposed detection thresholds for R1 to R5 and the labelling method, with the expected alerts and rejected lines for sample_logs.csv (22 Nov).

#### Faizullah Khan
- Studied the project brief: the five detection rules, the testing types, the evaluation metrics (TP, FP, FN, TN, precision, recall, F1, FPR) and the report structure.
- Agreed the six event fields with Alishba and wrote docs/event_format.md (18 Nov).
- Reviewed the first sample data and gave feedback on gaps: no access_denied events, too few normal and boundary cases, and messages that revealed the expected result (19 Nov).
- Updated docs/event_format.md to match docs/data_dictionary.md (added raw_line_no, the full list of sources, the missing-field rule, and which rule uses each event type) (20 Nov).
- Asked Alishba whether the parser outputs the timestamp as a datetime object or as text, and agreed the rule for alert evidence (see Decisions) (21 Nov).
- Created the src/loganalyzer/ and tests/ folders in the repository (21 Nov).
- Wrote a practice script, scratch/events_practice.py, to work with events as Python dictionaries and datetime values (23 Nov).
- Made a personal 12-week task plan for the detection and evaluation part.

### Decisions
- Log format: CSV with six fields (timestamp, source, event_type, username, source_ip, message).
- Required fields: lines with a missing required field are rejected. Only message may be empty.
- Timestamp: two input formats accepted, one normalized format.
- Rule messages are kept neutral so detection depends on event patterns, not keywords.
- Detection rules use only timestamp, event_type, username and source_ip. They never read the message text. raw_line_no is used as evidence in alerts.
- Timestamps are datetime objects inside the program. In saved files and in alert evidence they are text in the format YYYY-MM-DD HH:MM:SS.
- Proposed thresholds: R1 5 in 120 s, R2 5 failures then success, R3 any privilege change, R4 8 in 60 s, R5 3 in 120 s. To be confirmed by Faizullah.

### Problems and how they were handled
- GitHub shows a warning on the CSV preview because of the malformed lines. These lines are intentional and will be explained in the README.
- The two event format documents did not match (sources, missing-field handling). Fixed by aligning event_format.md with the data dictionary.
- The first sample data did not cover every rule (no access_denied events, few normal cases). More cases were added to the dataset.

### Plan for Week 2 (24 to 30 November)
- config.json with the thresholds (Alishba).
- Design document and architecture diagram (Alishba).
- Threat model: assets, threats, assumptions, ethics (Alishba).
- Literature review: 4 sources each, and a comparison matrix.
- Confirm the thresholds, then write the rule specifications for R1 to R5, the severity table and the alert format (Faizullah).
- Practice the time-window logic with a small script before writing the rules (Faizullah).
- Prepare the D2 package.