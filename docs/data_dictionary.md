# Data Dictionary

This document describes the log format used by the Security Log Analyzer, the validation rules applied to each field, and the normalized event schema produced by the parser.

## 1. Input log format (CSV)

Each line has six comma-separated fields. The first line is a header.

| # | Field | Type | Required | Example | Validation rule |
|---|---|---|---|---|---|
| 1 | `timestamp` | datetime | Yes | `2026-11-15 09:00:01` | Input may be `YYYY-MM-DD HH:MM:SS` or `DD/MM/YYYY HH:MM:SS`. The parser converts both to `YYYY-MM-DD HH:MM:SS`. Anything else is rejected. |
| 2 | `source` | text | Yes | `auth-server` | Must not be empty. |
| 3 | `event_type` | text | Yes | `login_failed` | Must not be empty. Compared in lower case. |
| 4 | `username` | text | Yes | `sara` | Must not be empty. |
| 5 | `source_ip` | IPv4 address | Yes | `10.0.0.45` | Four numbers from 0 to 255 separated by dots. |
| 6 | `message` | text | No | `Authentication event` | May be empty. Kept as free text. Rules do not use it for detection. |

A line with fewer or more than six fields, or with a missing required field, is rejected and reported with its line number and reason.

The normalized output format of each event is described in `event_format.md`. This document adds the input validation rules, the allowed values and the error handling that sit in front of it.

Allowed `source` values: `auth-server`, `web-portal`, `file-server`, `iam-service`, `api-gateway`. Other values are accepted and stored (the rules do not depend on `source`).

**Missing fields:** if any required field (1 to 5) is missing or empty, the line is rejected. Only `message` may be empty, and it is then stored as an empty value (`None`).

## 2. Event types

| `event_type` | Meaning | Used by rule |
|---|---|---|
| `login_success` | A user logged in successfully | R2 |
| `login_failed` | A login attempt failed | R1, R2 |
| `privilege_change` | An account privilege was changed | R3 |
| `data_request` | A request for data from a service | R4 |
| `access_denied` | An access attempt was refused | R5 |

Other event types are accepted and stored but are not used by any rule.

## 3. Normalized event schema (output of the parser)

| Field | Type | Description |
|---|---|---|
| `raw_line_no` | integer | Line number in the input file, used as evidence in alerts |
| `timestamp` | datetime (in memory), text (when stored) | A Python datetime object inside the program, so times can be subtracted. Saved as text `YYYY-MM-DD HH:MM:SS` in SQLite, CSV and alert evidence | 
| `source` | text | Copied from input |
| `event_type` | text | Lower case |
| `username` | text | Copied from input |
| `source_ip` | text | Validated IPv4 address |
| `message` | text | Copied from input |

Events are sorted by `timestamp` after parsing, so out-of-order input does not affect the rules.

## 4. Known limitations of the format
- Only IPv4 addresses are supported.
- Timestamps carry no time zone. All times are treated as one local time.
- Only two date formats are accepted.

## 5. Detection thresholds

All thresholds are stored in `config.json` and can be changed without editing code. The values below are the starting values used for `sample_logs.csv`.

| Rule | Detects | Event type used | Threshold | Group by |
|---|---|---|---|---|
| R1 | Repeated failed logins | `login_failed` | 5 or more within 120 seconds | `username` |
| R2 | Successful login after repeated failures | `login_failed`, then `login_success` | 5 or more failures, within 120 seconds then a success within 120 seconds of the last failure | `username` |
| R3 | Privilege change | `privilege_change` | Any single event | not applicable |
| R4 | Burst of data requests | `data_request` | 8 or more within 60 seconds | `username` |
| R5 | Repeated access denied | `access_denied` | 3 or more within 120 seconds | `username` |

The condition is "greater than or equal to" the threshold, so exactly 5 failed logins in 120 seconds triggers R1 and 4 does not.

## 6. Labelling method

The dataset is labelled by hand before any rule is run, so the labels do not depend on the code that is being  tested.

1. For every planted pattern, decide which rule should fire, using only the thresholds in section 5.
2. Record the expected alert (rule, username, line numbers of the evidence) in `labels.csv`.
3. Lines that should not raise any alert are listed as expected negatives.
4. Malformed lines are listed separately with the line number and the reason for rejection.

Precision, Recall, F1 and false positive rate are computed by comparing the alerts produced by the tool with `labels.csv`.

### Expected results for `sample_logs.csv`

Line numbers count the header as line 1.

| Rule | Expected alert | Evidence |
|---|---|---|
| R1 | `sara` (5 failures in 60 s), `bilal` (6 failures in 75 s) | `sara` lines 15 to 19, `bilal` lines 22 to 27 |
| R2 | `sara` (success after 5 failures) | `sara` lines 15 to 20 |
| R3 | `admin` | line 21 |
| R4 | `tariq` (8 requests in 49 s) | `tariq` lines 30 to 37 |
| R5 | `guest` (5 denied in 40 s) | `guest` lines 47 to 51 |

Boundary and negative cases that must not raise an alert:

| User | Why no alert |
|---|---|
| `nida` | 4 failed logins, one below the R1 threshold. The later success does not trigger R2 |
| `rida` | 7 requests in 48 s, one below the R4 threshold |
| `intern` | 3 access-denied events but over 130 s, outside the 120 s window |
| `kamran` | 5 failed logins spread over 10 minutes, never 5 within 120 s |
| `hina`, `omar` | 1 and 2 failures before a success, below the threshold |
| `ali`, `zainab`, `usman`, `fatima` | Normal activity |

### Malformed lines (it must be rejected, not crash the parser)

| Line | Reason |
|---|---|
| 58 | Invalid timestamp |
| 59 | Missing username |
| 60 | Invalid IP address (`999.999.1.1`) |
| 61 | Missing event type |
| 62 | Empty row |
| 63 | Wrong number of columns (4 instead of 6) |

Expected parser summary: 63 data lines read, 57 accepted, 6 rejected.

Line 56 (`15/11/2026 09:37:00`) is valid and uses the second accepted date format. It appears before line 57 although its time is later, to test sorting.