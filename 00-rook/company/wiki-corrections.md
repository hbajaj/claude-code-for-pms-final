# Wiki corrections — drafts to paste in

From the Dispatch PM. The wiki is read-only from here, so these are ready-to-paste replacements.
Each one gives the page, what it says now, and the replacement text. The routing code README in this repo has already been corrected.

---

## Glossary

**Missed** (currently: "Recorded separately from turned down, though both send the callout onward.")
> Missed — Nobody answered before the ping wait ran out. The ping moves to the next responder. Recorded separately from turned down in the ping log, but until the routing fix ships it costs the responder's recent-acceptance score exactly the same as a turn-down. *Proposed for 4.3: a single miss costs nothing; only a run of three or more does.*

**Routing priority** (currently lists "current availability" as an input, and says turning down or missing "lowers the responder's place in the order for later callouts")
> Routing priority — The score Dispatch uses to order available responders for a callout. Only responders marked available are considered; availability is a filter, not part of the score. The score is proximity (travel-time estimate, zero beyond 45 minutes) weighted 0.60, recent acceptance weighted 0.25, and capability match weighted 0.15 (weights since 4.2). Pings stop at the first yes, so a low place in the order can mean not being pinged at all. See "How Dispatch decides who gets pinged".

**Acceptance rate** (add a caution)
> … Dispatch's headline metric. Read it alongside each responder's share of pings and the number of callouts nobody took: it can rise while some responders are being starved of pings, because their misses drop out of the rate.

**New term: Unserved callout**
> Unserved callout — A callout that was pinged to everyone on its list and nobody took. Different from a coverage gap: there were capable responders, but none said yes in time.

---

## Releases → 4.2

The release notes mention proximity being weighted up but not that acceptance history was weighted down. Add to the first bullet:
> Recent acceptance history now counts for less in the ranking (weight 0.40 → 0.25); proximity counts for more (0.45 → 0.60).

Add a line under the notes:
> Committed for 4.2 but not shipped: Availability Confidence. Status is being reviewed with the Director of Product.

---

## Product briefs

**Bulk Callout** — add at the top:
> **Status: shipped in 4.1 (16 June 2026).** The open questions below are kept for history. Still open: no baseline was taken for time-to-full-coverage, and the "same job, several people" flow hasn't been checked against ranking and scoring.

**Routing Override Audit Log** — add at the top:
> **Status: shipped in 4.0 (7 April 2026).** Overrides appear in the console's activity view.

**Handler Phone App** — replace the "What this solves" paragraph:
> Handlers find out about callouts late because the console is desk-bound. Aunt Dot asked for a notification of her own "so I'm not relying on hearing a buzz through a ceiling". Note: her bigger problem in the interview was Vesper losing pings during the 60-second ping wait, and after 4.2, weeks with no pings at all. A handler app won't fix either of those; the routing fix and the ping-wait decision will.

Owner line: keep "the product designer". The Q3 roadmap should say Sofia Marino, not Priya.

**Requisition Approval Chains** — replace the Problem paragraph and split the proposal:
> Problem: Large requisitions get one quartermaster's sign-off, and Halloran wants a second set of eyes on big-ticket items. Separately, and more urgently from his interview and tickets, approvals are slow: a cracked vest plate waited 11 days, because every requisition sits in one queue and the priority field changes nothing. A second approval step on its own would make urgent items slower.
>
> Phase 1 (4.3): make the priority field actually move urgent requisitions up the queue, and add the second sign-off over $2,000.
> Later, each needing its own brief: 48-hour escalation, a cross-site pending dashboard, handler-visible requisition status, and replacing the gear-cage spreadsheet.

Owner: the Rook Supply team, with a named Supply PM. The Q3 roadmap currently lists Priya.

---

## Rook Dispatch one-pager

Core flow, the "turns it down or missed" bullet — add:
> Pings stop at the first yes, so the order effectively decides who is asked at all.

How we measure it — add:
> Ping share per responder — How evenly pings are spread across available responders, week on week. Watched for anyone who drops sharply.
> Unserved callouts — Callouts that went through the whole list without a yes.

---

## Team directory

Add the new Dispatch PM. Priya's row can stay with "(left 21 August 2026)".
