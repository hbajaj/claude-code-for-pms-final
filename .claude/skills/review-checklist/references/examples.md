# Calibration cases

Real calls from earlier reviews. Use them to judge borderline cases the same way every time.
If a new case contradicts one of these, follow the rule here and say so in the note.

## Owner named
| Brief says | Verdict | Why |
|---|---|---|
| "From the Dispatch PM" / "From: Rook Dispatch PM" and nothing else | flag | A role signs it; nobody is named as accountable. |
| A questions table with owners (Wen, Ravi, Marcus) | flag | They own questions, not the brief. |
| "What I need: Helen… Wen… Marcus…" | flag | People being asked for something aren't owners. |
| "Sofia Marino owns the real design" | flag | Owns one part (the screens), not the brief. |
| "Owner: Himanshu Bajaj, PM for Rook Dispatch" | pass | Named person, clear role. |
| "Ends on 'nobody's picked it up yet'" (bulk-callout) | flag | Flagging a future owner isn't naming one. |

## Success measure
| Brief says | Verdict | Why |
|---|---|---|
| Table of measures with before, target and who checks | pass | Measurable, has a target and a checker. |
| "back to about 10 to 12 pings a week within 4 weeks of launch" | pass | Number plus time frame. |
| Only a replay of past data ("Does it work? Replay of all 1,696 pings") | flag | That tests the idea before launch; it doesn't say what we'd watch after. |
| Says what gets logged and where it shows up (audit-log) | flag | Describes output, not how we'd know it works. |
| Targets but no date, or no named checker | pass + note | Mention the gap in the note. |

## Scope stays bounded
| Brief says | Verdict | Why |
|---|---|---|
| Opens "eight small changes", later proposes a new 4.3 score not in the ask | flag | The ask didn't cover the biggest change. Fixed by naming both in the summary and the ask. |
| Opening problem is scoring; table adds a busy window, a status control and delivery reporting for other problems | flag | New features and data for problems the opening never raised. |
| Ask mentions an overlap up front (Availability Confidence) and a "Not in scope" line | pass + note | Stated early, so it's bounded; note the size of the commitment. |
| "that's the whole ask", then four more asks (requisition approval chains) | flag | Classic growth. |
| Items under "Not in this brief", "Later" or "Out of scope" | pass | Clearly fenced off. |

## Problem before fix
| Brief says | Verdict | Why |
|---|---|---|
| First paragraph names who's affected and what goes wrong; asks come after | pass | Problem is set out before any solution. |
| "What I need" comes before the full story, but the opening paragraph already states the problem | pass + note | The problem is set up first, even if briefly. |
| Opens with the app and what it would do; the problem appears in section 2 (handler-phone-app) | flag | Solution first. |
