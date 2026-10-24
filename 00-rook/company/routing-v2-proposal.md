# Routing v2: proposal for responders and handlers

From the Dispatch PM, for Wen Li, Marcus Oyelaran and Sofia Marino. Then Helen Achebe for prioritisation.
**Status:** "Now" items 1, 5 (re-offer to missers only; widening to neighbouring areas not built) and 12 are **built and tested in the repo, not deployed**. They need Wen's review and Helen's OK. Deploying needs a one-off score import (see CHANGELOG). Everything else is still a proposal. It builds on the 24 Oct fix (misses scored separately, recovery, 90s wait) and goes after what that fix doesn't cover.
Evidence: the routing code in `00-rook/code/dispatch-routing/`, the rook-database (29 Jun–6 Sep), the 4 September interviews and 147 support tickets.

## What the code still gets wrong

| # | In the code | Who it hurts | Evidence |
|---|---|---|---|
| 1 | **Capability is 15% of the score, not a filter.** A responder without the required tags 5 min away (0.66) outranks a capable one 30 min away (0.48). | Safety, responders, handlers | `routing.score`. Glossary implies tags are matched. |
| 2 | **Winner takes all when two responders are close.** First yes wins, so a small score lead takes every callout. | Responders (one starves, one burns out) | Eastgate since 4.2: The Gale 54 pings, Meteor Mite 9. Kip: "Gale's exhausted." |
| 3 | **When the list runs out, the callout is dropped.** Someone who *missed* (not refused) is never asked again. | Incidents, responders | 49 unserved callouts since 4.2; 27 involved a miss. Lists are short (1.1–1.2 pings). |
| 4 | **The answer window is fixed.** Opening the alert doesn't hold it, so a responder can lose it with their thumb on the screen. | Responders | 15 "gone before I could answer" tickets from 11 responders; 3 of 4 interviews. |
| 5 | **No undo on a turn-down,** and it costs −0.12. | Responders | Ticket 3033 ("pressed the wrong button"). |
| 6 | **Strictly one at a time.** Each non-answer adds 90s before the next responder is asked. | Incidents | 90th-percentile time to assign rose from 28s to 62s after 4.2. At 90s it can reach 4.5 min after three non-answers. |
| 7 | **The handler isn't told anything.** The ping goes to the responder only; nothing explains a quiet week. | Handlers | 3 of 4 interviews (alerts); Kip ("nothing… helps me make sense of why"); 30 "is something broken?" tickets. |
| 8 | **Scores live in memory, keyed by name.** They're lost on restart, and two records with the same name would collide. | Everyone | `history._scores`. Two tickets show responders billed twice, which hints at duplicate records. |
| 9 | **Availability follows the handler's time zone,** not the responder's. | Responders who travel | Tickets 3050 (Halfmoon) and 3116 (Stormwrack). |

## The proposal

### For responders: fair, safe, and a fair chance to answer
1. **Make capability a filter.** Only responders with *all* required tags are ranked. If nobody qualifies, fall back to partial matches. The handler sees a "partial match" flag, and the callout counts as a coverage gap. *(Fixes #1. Small change in `routing.rank_for_callout`.)*
2. **Share work in close calls.** Add a light workload term, so near-equal responders take turns:
   `score -= WEIGHT_WORKLOAD × (their pings in last 7 days ÷ area average − 1)`, with `WEIGHT_WORKLOAD = 0.05`, capped at ±0.05.
   This only decides near-ties (about 4 minutes of travel), so it never sends someone far away. *(Fixes #2.)*
3. **"I'm on it" holds the ping.** Opening the alert (a "seen" signal from the phone) adds 30s to the window, once per ping. A seen-but-unanswered ping counts as a miss, not a no. *(Fixes #4.)*
4. **Five-second undo on "no".** The turn-down isn't scored until the undo window closes. *(Fixes #5.)*
5. **A second round before giving up.** If the list runs out, offer the callout once more to anyone who *missed*, not anyone who refused. Then widen to the next ring of areas before the callout is marked unserved. *(Fixes #3. Up to 27 of 49 unserved callouts since 4.2 had someone to re-offer to.)*
6. **Weekly "you're active" note to the responder:** pings and takes this week, and confirmation they're on the list. *(Answers "am I still in the system", tickets 3120 and 3121.)*

### For handlers: see what's live, and why
7. **Handler alert alongside the responder's.** The handler gets "callout offered to [responder]", then the outcome: taken, passed on (and why: missed or refused), or taken by someone else. A different sound per responder. *(Fixes #7. Covers Dot, Ambrose and Kip, plus 2 tickets.)*
8. **"Why quiet" panel per responder.** Shows pings this week against their usual, how many callouts in their area went to others and why (distance, score, not available), and their current standing as low, normal or high. Not raw scores. *(Kip's two cards; the 30 "quiet" tickets.)*
9. **Filters saved per person, and never reset silently.** Save filters to the sign-in, not the computer. If a filter can't be restored, show a warning. Make the active-filter badge prominent, and add "clear all". *(14 tickets since 4.2, plus Ambrose.)*
10. **Time zones and leave fixed.** Availability is set in the *responder's* time zone, and there's an "on leave" status separate from "busy". *(Fixes #9, plus 4 tickets.)*

### Under the hood
11. **Staggered offers when the list has 2 or more people.** The top responder gets the full 90s. If there's no answer after 30s, also offer it to #2, and the first to accept wins. The other sees "taken by another responder" with **no score change**. *(Fixes #6 without shortening anyone's time to answer.)*
12. **Store scores permanently, by responder ID.** Keep them through restarts, and audit for duplicate records (link to the billing tickets). *(Fixes #8.)*
13. **Log the guardrail metrics from the code:** ping share per responder, local share, unserved callouts, seen-but-missed, and time to assign. Ravi then won't have to rebuild them by hand. Also add `answered_at` and `seen_at` to the ping log.

## Order of work

| Phase | Items | Why first | Size (PM estimate; Wen to size) |
|---|---|---|---|
| **Now** (hotfix-sized) | 1 capability filter, 5 second round, 12 store scores | Safety, dropped callouts, data integrity | Small; routing and history only |
| **Next release** | 3 "I'm on it", 4 undo, 2 workload share, 7 handler alert, 9 filters | The top complaints in both interviews and tickets | Medium; needs phone app and console |
| **After** | 8 "why quiet" panel, 6 weekly note, 10 time zones and leave, 11 staggered offers, 13 metrics | Visibility and polish; staggered offers need the most testing | Medium–large |

## Trade-offs and open questions
- **Capability filter:** some callouts that went to a nearby partial match will now go further away or become coverage gaps. That's correct, but coverage-gap numbers will rise. Agree the fallback rule with Wen and Helen.
- **Workload share:** a responder who *wants* more work gets slightly less in close calls. The cap keeps the effect small. Watch The Gale and Meteor Mite after the change.
- **Second round:** it adds up to about 90s more for callouts that would otherwise be dropped. That's a clear gain over dropping them.
- **Staggered offers:** two responders may run for the same callout for a moment. "Taken by another" must withdraw instantly, and must never count against anyone.
- **Supply:** items 10 and 12 touch the availability record and its owners, so tell Supply before changing its shape (`availability.py` says so).
- **Needs data we don't have yet:** "seen" and "answered" times from the phone app, required tags on callouts, and live data from after 24 Oct.

## How we'll know it worked (on top of the post-deploy checks)
- Eastgate split between The Gale and Meteor Mite within 60/40.
- Unserved callouts at 4 a week or fewer, and none where someone only missed.
- No callout taken by a responder missing a required tag, unless flagged as a partial match.
- "Gone before I could answer" tickets and seen-but-missed pings near zero.
- "Is something broken?" tickets near zero.
