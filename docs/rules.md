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

## R2: Success after repeated failures

**Idea:** A password guess probably worked. Failed logins for an
account are followed by a successful login for the same account.

| Item | Value |
|---|---|
| Rule ID | R2 |
| Events used | login_failed, login_success |
| Grouped by | username |
| Condition | 5 or more login_failed within 120 seconds, then a login_success for the same username within 120 seconds after the last of those failures |
| Severity | High |
| Alert text | "Successful login after 5 or more failed logins for the same username" |
| Evidence | the failed-login rows and the success row: raw_line_no, timestamp (text, YYYY-MM-DD HH:MM:SS), source_ip |

**How the rule works (steps):**
1. Keep only login_failed and login_success events.
2. Group them by username and put each group in time order.
3. Find 5 login_failed events in a row (no login_success from the same
   username in between) where the last time minus the first time is
   120 seconds or less.
4. If a login_success for the same username comes after the last of
   those failures, and 120 seconds or less after it, raise one alert.
5. A success that comes before the failures, or after fewer than 5
   failures, does not count.

**Example:** sara has 5 login_failed events between 09:02:15 and
09:03:15, then a login_success at 09:03:45 (30 seconds after the last
failure). This raises one R2 alert, High. R1 also raises its own Medium
alert for the same failures. That is intended: R1 says "someone is
guessing", R2 says "the guess may have worked".

**Test cases:**
| Case | Expected |
|---|---|
| 5 failures within 120 s, success 30 s later | alert (High) |
| 4 failures, then success | no alert (below threshold) |
| 5 failures, success exactly 120 s after the last | alert (edge of gap) |
| 5 failures, success 121 s after the last | no alert |
| 5 failures, no success | no R2 alert (R1 only) |
| success with no failures before it | no alert |
| success before the failures | no alert (order matters) |
| 5 failures for user A, success for user B | no alert (different usernames) |
| 5 failures spread over 10 minutes, then success | no alert |

**Known limitations:**
- The success is not required to come from the same IP address.
- A real user who forgets a password five times and then remembers it
  also triggers R2.
- An attacker who waits more than 120 seconds before the successful
  login is not detected.

## R3: Privileged account change

**Idea:** Someone's privileges were changed, for example a user was
added to an administrators group. This is a common step after an
account is compromised.

| Item | Value |
|---|---|
| Rule ID | R3 |
| Event used | privilege_change |
| Grouped by | nothing (every event is checked on its own) |
| Condition | any privilege_change event |
| Severity | High |
| Alert text | "Privileged account change recorded" |
| Evidence | the event row: raw_line_no, timestamp (text, YYYY-MM-DD HH:MM:SS), username, source_ip, source |

**How the rule works (steps):**
1. Keep only privilege_change events.
2. Raise one alert for each of them.

**Example:** admin has a privilege_change event at 09:10:00 from
192.168.1.5. This raises one R3 alert, High. The message says who was
added, but the rule does not read it. A person reads it in the log line
that raw_line_no points to.

**Test cases:**
| Case | Expected |
|---|---|
| one privilege_change event | one alert (High) |
| only login events, no privilege_change | no alert |
| two privilege_change events, different usernames | two alerts |
| two privilege_change events, same username, 5 s apart | two alerts (no grouping) |
| privilege_change with an empty message | alert (message is not used) |
| login_success by admin, no privilege_change | no alert |

**Known limitations:**
- Every privilege change raises an alert, including legitimate
  administrator work, so false positives are expected.
- The rule cannot tell who received the new privileges, because that is
  only in the message text.

## R4: Unusual request volume

**Idea:** An account makes far more data requests than normal in a
short time, which can mean automated scraping or abuse.

| Item | Value |
|---|---|
| Rule ID | R4 |
| Event used | data_request |
| Grouped by | username |
| Threshold | 8 or more data_request events (inclusive) |
| Time window | 60 seconds (last minus first is 60 s or less) |
| Severity | Medium |
| Alert text | "8 or more data requests for the same username within 60 seconds" |
| Evidence | the request rows: raw_line_no, timestamp (text, YYYY-MM-DD HH:MM:SS), source_ip |

**How the rule works (steps):**
1. Keep only data_request events.
2. Group them by username and put each group in time order.
3. Look at every run of 8 events in a row. If the last time minus the
   first time is 60 seconds or less, raise one alert.
4. If the requests continue (9, 10, 11 in the same burst), keep them in
   the same alert.

**Example:** bilal makes 8 data_request events within 40 seconds. This
raises one R4 alert, Medium.

**Test cases:**
| Case | Expected |
|---|---|
| 7 requests within 60 s | no alert (just below) |
| 8 requests within 60 s | alert (at threshold) |
| 9 requests within 60 s | one alert (above threshold) |
| 8 requests, first to last exactly 60 s | alert (edge of window) |
| 8 requests, first to last 61 s | no alert |
| 8 requests spread over 10 minutes | no alert |
| 5 requests for one user + 5 for another within 60 s | no alert |
| login_failed events mixed in | not counted |

**Known limitations:**
- An attacker who stays under 8 requests per 60 seconds is not detected.
- An attacker who spreads requests across many usernames is not
  detected, because R4 counts per username.
- A legitimate script or heavy user can also trigger R4.

## R5: Repeated access denied

**Idea:** An account keeps trying to reach things it is not allowed to
reach, which can mean probing for permissions.

| Item | Value |
|---|---|
| Rule ID | R5 |
| Event used | access_denied |
| Grouped by | username |
| Threshold | 3 or more access_denied events (inclusive) |
| Time window | 120 seconds (last minus first is 120 s or less) |
| Severity | Medium |
| Alert text | "3 or more access denied events for the same username within 120 seconds" |
| Evidence | the denied rows: raw_line_no, timestamp (text, YYYY-MM-DD HH:MM:SS), source_ip |

**How the rule works (steps):**
1. Keep only access_denied events.
2. Group them by username and put each group in time order.
3. Look at every run of 3 events in a row. If the last time minus the
   first time is 120 seconds or less, raise one alert.
4. If the denials continue, keep them in the same alert.

**Example:** kamran has 3 access_denied events within 90 seconds. This
raises one R5 alert, Medium.

**Test cases:**
| Case | Expected |
|---|---|
| 2 denials within 120 s | no alert (just below) |
| 3 denials within 120 s | alert (at threshold) |
| 4 denials within 120 s | one alert (above threshold) |
| 3 denials, first to last exactly 120 s | alert (edge of window) |
| 3 denials, first to last 121 s | no alert |
| 3 denials spread over 10 minutes | no alert |
| 2 denials for one user + 1 for another within 120 s | no alert |
| login_failed events mixed in | not counted |

**Known limitations:**
- A normal user who clicks a forbidden link a few times can trigger R5.
- Only the username is used, so denials spread across usernames from
  one IP are not detected.

## Severity levels

Severity says how soon a person should look at an alert. It does not
say how sure we are that an attack happened.

| Level | Meaning | What a person should do |
|---|---|---|
| High | Strong sign of a compromise, or a change with high impact | Look at it first |
| Medium | Suspicious pattern that could be an attack or a mistake | Look at it soon |
| Low | Weak signal that is often normal | Look at it when time allows |

| Rule | Severity | Why |
|---|---|---|
| R1 Repeated failed logins | Medium | Could be a guessing attack or a user who forgot a password |
| R2 Success after repeated failures | High | The guess may have worked, so the account may be compromised |
| R3 Privileged account change | High | New privileges give wide access, even if the change is legitimate |
| R4 Unusual request volume | Medium | Could be abuse or a legitimate script |
| R5 Repeated access denied | Medium | Could be probing for permissions or a user's mistake |

Severity is fixed per rule for now. No rule uses Low yet. The level is
kept for rules added later.