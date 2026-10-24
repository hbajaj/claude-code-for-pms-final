# Dispatch guardrail metrics and data requests

From the Dispatch PM, for Ravi Menon (data analyst), Wen Li and Nadia Hoffmann.
Why: after 4.2, acceptance rate, the one number everyone watches, was *recovering* (54% → 73%) while four responders were being switched off and unserved callouts doubled.
These metrics sit next to acceptance rate in the weekly report, so that can't happen silently again.
All numbers below are from the rook-database (29 Jun–6 Sep 2026) and still need Ravi to check them.

## Weekly guardrails

Ticket-based measures have a blind spot: the handlers of Vesper and Meteor Mite, two of the four starved responders, have never filed a ticket. Treat the ping-based guardrails as the leading signal.

| Metric | Definition | Alert when | Baseline (before 4.2) | After 4.2 |
| --- | --- | --- | --- | --- |
| **Acceptance rate** (existing) | Pings taken ÷ pings sent | Weekly drop of 5+ points | 75–78% | 54%, 66%, 67%, 73% |
| **Miss rate** | Pings missed ÷ pings sent | Above 5% | 1–3% (2–6 a week) | 13–22% (21–38 a week) |
| **Starved responders** | Available responders whose weekly pings fell below half their own 6-week average | Any, for 2 weeks running | 0 | 4 every week from 17 Aug (Vesper, Farlight, The Undertow, Meteor Mite) |
| **Local share, per area** | Callouts taken by a responder whose home area matches the callout's | Any area below 70% | 100% in every area checked | Old Town 14%, Uptown 7%, Harborside 10% |
| **Unserved callouts** | Callouts pinged to the whole list with no yes | Above 10 a week | 4–12 | 14, 17, 16, 7 |
| **"Phone never goes off" tickets** | Tickets about a responder going quiet (Nadia's tag; rough subject match below) | Any in a week | 0 | 0, 8, 13, 7 |
| **"Gone before I could answer" tickets** | Tickets about a ping moving on mid-answer | Any in a week | 0 | 7, 3, 2, 1 |
| **Time-to-accept** (existing, can't compute yet) | Median seconds from ping to taken | Above half the ping wait (45s at 90s) | — | needs answer times, see data requests |

The starved-responder alert would have fired in the week of 17 Aug, a week before tickets peaked. The acceptance rate alone wouldn't have.

**Read them together:** a rising acceptance rate with a rising starved count means the rate is improving because people stopped being asked, not because they're answering.

## Queries (rook-database)

Miss rate and acceptance by week:
```sql
select date_trunc('week', sent_at)::date as week, count(*) as pings,
  round(100.0 * avg((outcome = 'taken')::int), 1) as acceptance_pct,
  round(100.0 * avg((outcome = 'missed')::int), 1) as miss_pct
from pings group by 1 order by 1;
```

Starved responders (pings below half their own pre-period average):
```sql
with w as (select responder, date_trunc('week', sent_at)::date wk, count(*) n from pings group by 1, 2),
base as (select responder, avg(n) avg_before from w where wk < '2026-08-10' group by 1),
weeks as (select distinct wk from w),
grid as (select b.responder, k.wk, coalesce(w.n, 0) n, b.avg_before
         from base b cross join weeks k left join w on w.responder = b.responder and w.wk = k.wk)
select wk, string_agg(responder, ', ') filter (where n < 0.5 * avg_before) as starved
from grid group by wk order by wk;
```
For an ongoing report, compare each week to the responder's trailing 6 weeks, not a fixed date.

Unserved callouts:
```sql
with c as (select callout_number, sum((outcome = 'taken')::int) taken from pings group by 1)
select date_trunc('week', k.happened_at)::date week, count(*) filter (where c.taken = 0) unserved
from callouts k join c using (callout_number) group by 1 order by 1;
```

Ticket themes: the subject-line match is rough. Nadia's team should tag tickets with a theme when they're filed instead.
```sql
select date_trunc('week', filed_at)::date week,
  count(*) filter (where subject ~* '(hardly anything|nothing coming|quiet|has not gone off|still on the list|first one in)') never_goes_off,
  count(*) filter (where subject ~* '(vanished|moved on|gone before|lost one|before he could|before she could)') gone_before_answer
from support_tickets group by 1 order by 1;
```

## Data requests

| # | Ask | From | Why |
| --- | --- | --- | --- |
| 1 | Official weekly acceptance series, ideally back to 2025 | Ravi | Confirm these numbers, and test Priya's "August is always soft". The database only starts on 29 Jun. |
| 2 | An answer time on each ping (`answered_at`) | Wen / Ravi | Time-to-accept, the headline's companion metric, can't be computed today. Also needed to judge 60s vs 90s. |
| 3 | Availability windows per responder, by day | Wen | Tell "not available" apart from "available but never asked". Starvation should only count available days. |
| 4 | Capability tags on responders, required tags on callouts | Wen | Coverage gap, an official metric, can't be computed today. |
| 5 | A daily snapshot of each responder's recent-acceptance score | Wen | Watch scores sink and recover, and check the fix works. Scores currently live only in memory. |
| 6 | Flags on pings for handler overrides and bulk callouts | Wen | Know whether they distort ping counts and scores. |
| 7 | Where callouts come from (intake source) | Wen / Marcus | Callout volume fell from about 140 a week to 110–127 from release week. Routing shouldn't change how many incidents arrive. |
| 8 | A theme tag on support tickets | Nadia | Replace the rough subject matching above. |
