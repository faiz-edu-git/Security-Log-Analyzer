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
