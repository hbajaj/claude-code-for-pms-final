# Post-deploy checks: routing fix (shipped 24 Oct 2026)

Owner: Dispatch PM, with Ravi Menon (data) and Nadia Hoffmann (support).
What shipped: misses scored separately, score decay, ping wait back to 90s, and scores restored for Vesper, Meteor Mite, Farlight and The Undertow. See `release-runbook-routing-fix.md`.

**Data note:** the rook-database available to this repo stops at 6 Sep 2026 (tickets 7 Sep), with **0 pings since the deploy**.
These checks need live data: Ravi's weekly series, or a refreshed copy of the `pings`, `callouts` and `support_tickets` tables.
The queries below run as-is once that data exists.

## Schedule and results

| Check-in | Date | Status | Notes |
| --- | --- | --- | --- |
| Day 2 | Mon 26 Oct | ☐ | Are the four being pinged again? Any spike in unserved callouts? |
| Week 1 | Sat 31 Oct | ☐ | First full-week read on every check below |
| Week 2 | Sat 7 Nov | ☐ | Pass or fail. On pass: message 2 to Aunt Dot and Kip, release notes, roadmap item closed |

## Pass criteria

| Check | Before 4.2 | After 4.2 (broken) | Pass at week 2 | Roll back if |
| --- | --- | --- | --- | --- |
| Miss rate | 1–3% | 13–22% | ≤ 4% | — |
| Acceptance rate | 75–78% | 54–73% | ≥ 74% | Below 60% |
| Pings for each of the four (per week) | 11–14 | 1–5 | ≥ 8 each | — |
| Starved responders | 0 | 4 | 0 | — |
| Local share: Old Town, Uptown, Harborside | 100% | 7–14% | ≥ 80% | — |
| Unserved callouts (per week) | 4–12 | 7–17 | ≤ 12 | Above 20 |
| "Phone never goes off" tickets (per week) | 0 | 7–13 | 0–1 | — |
| "Gone before I could answer" tickets (per week) | 0 | 1–7 | 0–1 | — |

Rollback: see `release-runbook-routing-fix.md`. Read acceptance rate together with the rows below it, not on its own.

## Queries
Set the deploy time once. Every query compares before and after it.

**1. Weekly miss rate and acceptance since deploy**
```sql
select date_trunc('week', sent_at)::date as week, count(*) as pings,
  round(100.0 * avg((outcome = 'taken')::int), 1) as acceptance_pct,
  round(100.0 * avg((outcome = 'missed')::int), 1) as miss_pct
from pings where sent_at >= '2026-10-24' group by 1 order by 1;
```

**2. The four restored responders: pings and takes per week**
```sql
select responder, date_trunc('week', sent_at)::date as week, count(*) as pings,
  sum((outcome = 'taken')::int) as taken, sum((outcome = 'missed')::int) as missed
from pings
where sent_at >= '2026-10-24'
  and responder in ('Vesper', 'Meteor Mite', 'Farlight', 'The Undertow')
group by 1, 2 order by 1, 2;
```

**3. Starved responders: weekly pings below half their pre-4.2 average**
```sql
with w as (select responder, date_trunc('week', sent_at)::date wk, count(*) n from pings group by 1, 2),
base as (select responder, avg(n) avg_before from w where wk >= '2026-06-29' and wk < '2026-08-10' group by 1),
weeks as (select distinct wk from w where wk >= '2026-10-19'),
grid as (select b.responder, k.wk, coalesce(w.n, 0) n, b.avg_before
         from base b cross join weeks k left join w on w.responder = b.responder and w.wk = k.wk)
select wk, string_agg(responder, ', ') filter (where n < 0.5 * avg_before) as starved
from grid group by wk order by wk;
```

**4. Local share in the four affected areas**
```sql
select c.area, round(100.0 * avg((r.area = c.area)::int)) as pct_taken_locally, count(*) as taken
from pings p join responders r on r.name = p.responder join callouts c using (callout_number)
where p.outcome = 'taken' and p.sent_at >= '2026-10-24'
  and c.area in ('Old Town', 'Uptown', 'Harborside', 'Eastgate')
group by 1 order by 1;
```

**5. Unserved callouts per week**
```sql
with c as (select callout_number, sum((outcome = 'taken')::int) taken from pings group by 1)
select date_trunc('week', k.happened_at)::date week, count(*) filter (where c.taken = 0) unserved
from callouts k join c using (callout_number)
where k.happened_at >= '2026-10-24' group by 1 order by 1;
```

**6. Ticket themes per week**
```sql
select date_trunc('week', filed_at)::date week,
  count(*) filter (where subject ~* '(hardly anything|nothing coming|quiet|has not gone off|still on the list|first one in)') never_goes_off,
  count(*) filter (where subject ~* '(vanished|moved on|gone before|lost one|before he could|before she could)') gone_before_answer
from support_tickets where filed_at >= '2026-10-24' group by 1 order by 1;
```
Remember the blind spot: Aunt Dot and Kip don't file tickets. Ask them directly at week 1.

## Also at week 2
- [ ] Message 2 to Aunt Dot and Kip (`00-rook/feedback/handler-messages.md`)
- [ ] Ask Desmond Okafor (The Undertow) and Linda Pruitt (Farlight) whether things are back to normal. They filed the most tickets.
- [ ] Paste the wiki corrections, including the new "Missed" definition and the 4.2 release note fixes (`wiki-corrections.md`)
- [ ] Close the roadmap item in `q3-roadmap-update.md`
- [ ] Close draft tickets D-01 and D-05 (and D-02, D-08 if the 90s wait fixed them)
