# Event format

Every log line, after parsing, becomes one event with these fields.

| Field      | Meaning                                  | Example                     |
|------------|------------------------------------------|-----------------------------|
| timestamp  | when the event happened                  | 2026-11-15 09:02:15         |
| source     | which system produced the log            | auth-server                 |
| event_type | what kind of event it was                | login_failed                |
| username   | the account involved                     | sara                        |
| source_ip  | where the event came from                | 10.0.0.45                   |
| message    | the original text of the log line        | Invalid password attempt    |

## Rules for the fields
- All field names are lowercase.
- timestamp format: YYYY-MM-DD HH:MM:SS
- event_type values are lowercase (see the list below).
- If a field is missing in a log line, it is stored as an empty value (None).
- Detection rules use only timestamp, event_type, username, source_ip and source.
  They never read the message text.

## Allowed event_type values
- login_success
- login_failed
- privilege_change
- data_request
- access_denied

## Allowed source values
- auth-server
- iam-service
- api-gateway

