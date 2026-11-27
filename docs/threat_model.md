# Threat Model

This document states what the Security Log Analyzer protects, which threats it is designed to detect, which threats apply to the tool itself, and what it assumes. The tool is an educational prototype and is not a replacement for a production SIEM.

## 1. System in scope

A Python tool that reads authentication, access and service logs from a file, validates and normalizes them, applies five detection rules (R1 to R5), and stores alerts with evidence for an analyst to review. It does not collect logs from live systems and it does not block or respond to anything.

## 2. Assets

| Asset | Why it matters |
|---|---|
| Log files (input) | They record who did what and from where. They may contain usernames and IP addresses |
| Normalized events and alerts (SQLite, CSV) | The result the analyst relies on. If they are wrong or changed, the analyst is misled |
| Configuration (`config.json`) | Thresholds decide what is detected. A wrong value hides attacks or creates false alarms |
| Detection rules and code | Correct behaviour of the tool depends on them |
| Labels and evaluation results | The evidence for the claims in the report |

## 3. Threats the tool is designed to detect

| Rule | Behaviour detected | Possible meaning | Severity |
|---|---|---|---|
| R1 | Many failed logins for one account in a short time | Password guessing (brute force) | Medium |
| R2 | A successful login right after repeated failures for the same account | A guess may have worked, so the account may be compromised | High |
| R3 | A privilege change | Privilege abuse, often a step after an account is compromised | High |
| R4 | A burst of data requests from one user | Automated or abnormal data access, for example bulk downloading | Medium |
| R5 | Repeated access-denied events for one user | Someone trying resources they are not allowed to use | Medium |

MITRE ATT&CK is used only to give context: R1 relates to Brute Force (T1110), R2 to Valid Accounts (T1078) and R3 to Account Manipulation (T1098). An alert is a lead for an analyst and is not proof that a technique was used. A real user who forgot a password can also trigger R1.

## 4. Threats to the tool itself

| Threat | Example | How the design handles it |
|---|---|---|
| Malformed or hostile input | Bad timestamps, invalid IPs, empty rows, wrong column count, invalid JSON | Lines are validated, rejected with a reason and counted. The program does not crash |
| Misleading log content | Message text written to trigger or hide an alert | Rules never read the `message` field. They use only timestamp, event type, username and IP |
| Out-of-order or duplicated lines | Events arrive in the wrong order | Events are sorted by timestamp before the rules run |
| Tampered logs | An attacker edits or deletes lines before analysis | Out of scope (see section 6). The tool cannot tell if a file was changed before it received it |
| Tampered config or results | Thresholds or the database are edited | Config values are validated when loaded. File protection is left to the operating system |
| Resource exhaustion | A very large file | Processing time is measured on 10,000 lines in the benchmark. Limits are reported honestly |
| Privacy | Real usernames or addresses in the data | Only synthetic data and public sample logs with documented source are used |

## 5. Assumptions

- The input file is authorized data. Only synthetic logs and public samples are used.
- Timestamps are in one local time zone (no zone information is stored).
- Only IPv4 addresses are supported.
- Event types and field names follow `event_format.md` and `data_dictionary.md`.
- The person using the tool is an analyst who reviews each alert.
- The logs reach the tool unchanged.

## 6. Out of scope and known limits

- Live log collection, real-time monitoring and automatic response.
- Detecting tampered logs, or attacks that do not appear in the chosen event types.
- Attacks that stay below the thresholds (for example a few failures spread over a long time), and password spraying across many usernames (R1 counts per username).
- Machine learning and anomaly detection.
- Fixed thresholds on small synthetic data do not prove the same results on real traffic.

## 7. Ethics and responsible use

- Only synthetic data or public sample logs are used. Their source, licence and access date are recorded in `data_sources.md`.
- IP addresses are from private ranges. No real person's data is processed.
- Alerts say "worth checking", not "guilty". A person should never be punished from an alert alone.
- Results are reported honestly, including false positives, false negatives and limitations. No result is invented.
- The tool is for defence and learning. It must not be used on logs the user is not authorized to analyse.
- AI tools were used for planning, drafting and explanation, and this is disclosed in the report. 

