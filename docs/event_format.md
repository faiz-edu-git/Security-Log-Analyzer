# Event format (normalized events)

This file describes the events that the rules receive after parsing.
Input validation rules (accepted formats, rejected lines) are in
Alishba's input format document.

| Field       | Meaning                                   | Example                  |
|-------------|-------------------------------------------|--------------------------|
| raw_line_no | line number in the input file             | 12                       |
| timestamp   | when the event happened                   | 2026-11-15 09:02:15      |
| source      | which system produced the log             | auth-server              |
| event_type  | what kind of event it was                 | login_failed             |
| username    | the account involved                      | sara                     |
| source_ip   | where the event came from (IPv4)          | 10.0.0.45                |
| message     | the original text of the log line         | Invalid password attempt |

## Rules for the fields
- All field names are lowercase.
- timestamp is always YYYY-MM-DD HH:MM:SS (the parser converts other
  accepted input formats to this).
- Inside the program timestamp is a Python datetime object. In saved files
  and alert evidence it is text, YYYY-MM-DD HH:MM:SS
- event_type is always lowercase.
- Events are sorted by timestamp after parsing.
- Every field is always present, except message, which may be None.
  Lines with a missing required field are rejected by the parser.
- Detection rules use only timestamp, event_type, username and
  source_ip. They never read the message text. raw_line_no is used
  as evidence in alerts.

## Event types and the rule that uses them
- login_failed: R1, R2
- login_success: R2
- privilege_change: R3
- data_request: R4
- access_denied: R5
Other event types are accepted but no rule uses them.

## Source values
auth-server, web-portal, file-server, iam-service, api-gateway.
Other values are accepted and stored.

## Known limitations
- IPv4 addresses only.
- Timestamps have no time zone.
