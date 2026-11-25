# Detection rules

Each rule works only on timestamp, event_type, username and source_ip.
Rules never read the message text.

## R1: Repeated failed logins

**Idea:** Someone is guessing the password of one account.

| Item | Value |
|---|---|
| Rule ID | R1 |
| Event used | login_failed |
| Grouped by | username |
| Threshold | 5 or more failed logins (inclusive) |
| Time window | 120 seconds (last minus first is 120 s or less) |
| Severity | Medium |
| Alert text | "5 or more failed logins for the same username within 120 seconds" |
| Evidence | the failed-login rows: raw_line_no, timestamp (text, YYYY-MM-DD HH:MM:SS), source_ip |

**How the rule works (steps):**
1. Keep only login_failed events.
2. Group them by username.
3. For each username, put the events in time order.
4. Look at every run of 5 events in a row. If the last time minus the
   first time is 120 seconds or less, raise one alert.
5. If the failures continue (6, 7, 8 in the same burst), keep them in the
   same alert instead of raising a new one each time.

**Example:** sara has 5 login_failed events between 09:02:15 and 09:03:15
(60 seconds). This raises one R1 alert, Medium.

**Test cases:**
| Case | Expected |
|---|---|
| 4 failures within 120 s | no alert (just below) |
| 5 failures within 120 s | alert (at threshold) |
| 6 failures within 120 s | one alert (above threshold) |
| 5 failures, first to last exactly 120 s | alert (edge of window) |
| 5 failures, first to last 121 s | no alert |
| 5 failures spread over 10 minutes | no alert |
| 3 failures for one user + 2 for another within 120 s | no alert |
| login_success events mixed between failures | success events are not counted |

**Known limitations:**
- Failures spread across many usernames from one IP (password spraying)
  are not detected, because R1 counts per username.
- An attacker who stays under 5 failures per 120 seconds is not detected.
- Five failures can also be a real user who forgot a password, so R1
  alerts are "worth checking", not proof of an attack.