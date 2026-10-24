# Dispatch open questions: callout drop, Supply impact, filter bugs

From the Dispatch PM. Evidence is from the rook-database (29 Jun–6 Sep 2026), the wiki and the handler interviews.
Each section gives the facts, what they suggest, and who can answer it.

## 1. Why did callout volume drop on release day?

**What we see**
- Callouts fell from about 20 a day (1–11 Aug) to about 15.8 a day (12–23 Aug). The drop starts on **12 Aug, release day**: 12 and 13 callouts on 12–13 Aug, against 16–27 on the days before.
- Weekly volume went from about 140 to 110–127 and hasn't returned.
- The drop is spread across **all 15 areas**, from about −3% (Southport) to −20% (Eastgate). Two areas fell much further: **Northfield −33%** and **Westbury −32%**. Those are the home areas of Corporal Ashgrove and Halfmoon, the two responders whose pings roughly halved.
- Every callout in the table has at least one ping. Callouts that never reached routing may not be recorded here at all.

**What it suggests**
Routing can't change how many incidents happen, so something about how callouts are *created or recorded* changed with 4.2. Possibilities to rule in or out:
- An intake or logging change shipped in 4.2 alongside the routing change.
- Handlers enter incidents themselves (Dispatch one-pager). They may be routing around the system after bad experiences, for example calling a responder directly. The Bulk Callout brief describes exactly that behaviour from before. The Northfield and Westbury drops fit this.
- A genuine dip in incidents (Priya's seasonal view). The drop starting on release day makes this unlikely to be the whole story.

**Next step:** Marcus and Wen check what changed in intake and logging in 4.2 (data request #7). Nadia asks the Northfield and Westbury handlers (Yusuf Demir, Simone Fischer) whether they've been handling callouts outside the console.

## 2. Is 4.2 affecting Supply's maintenance scheduling?

**What we see**
- Supply schedules maintenance into "the periods where callout load is lowest" using Dispatch's Responder Availability Record. Changes on Dispatch's side reach Supply without anyone on Supply knowing (Rook Supply one-pager).
- New ticket types appeared after 4.2, with none before:
  - "Maintenance booked on a bad day": suits booked in on city-marathon day. Sgt. Falkirk on 15 Aug, Ironvale on 29 Aug (open).
  - "Maintenance reminder came after the date": Ironvale on 16 Aug, Farlight on 2 Sep (open).
- Against that, Halloran said in his interview on 5 Sep that scheduling has "gotten smarter" and stopped booking into busy stretches.

**What it suggests**
The evidence is weak, but it's worth one question. If Supply's sense of "low callout load" comes from recent pings, then 4.2 changed it. Starved responders like Farlight now look idle, and the overall drop in callouts makes every period look quieter. Neither ticket type obviously follows from the routing change, though. The marathon is a known busy day, and calendar events may simply not be considered.

**Next step:** ask the Supply team what "callout load" means in their scheduler. Is it availability windows, recent pings, or callout history? Did their inputs shift on 12 Aug? Share `routing-fix-proposal.md` with them, because the fix will shift those inputs again. The availability record's shape won't change.

## 3. Filter persistence: real bugs, not noise

Priya's handoff called the 4.2 filter tickets "cosmetic noise". Most are real, and two of them can leave a handler watching the wrong list during a live callout.

| Issue | Tickets | Open | Severity |
| --- | --- | --- | --- |
| Saved filters wiped by updates, silently | 3044, 3064, 3072, 3134, plus Ambrose's interview ("looking at the wrong filter for a quarter of an hour") | 3 | **High**: the handler doesn't know they're seeing a different list |
| Active-filter badge too easy to miss | 3061, 3124 | 1 | **High**: same risk the other way round, a filter is on and the handler forgets |
| Filters saved per computer, not per person (shared machines get a colleague's filters; a second computer has none) | 3042, 3046, 3085, 3115 | 1 | Medium: points to storage in the browser, not the account |
| No "clear all filters" | 3066, 3076 | 0 | Low |
| Thank-yous | 3062, 3100 | — | The feature is valued |

**Likely cause (to confirm with engineering):** filters are saved in the browser rather than on the handler's account, so an update or cache clear wipes them, and a shared machine shares them.

**Proposed fix, for 4.3 or a patch:**
1. Save filters to the handler's sign-in, not the computer.
2. If saved filters can't be restored, show a visible warning. Never fall back to "everyone" silently.
3. Make the active-filter badge prominent, and add "clear all".

Owner: Sofia Marino (console) with Marcus's team.

## Data caution
Several support tickets have **word-for-word identical bodies** from different handlers. For example, 3064 and 3072, 3046 and 3115, and 3054 and 3109. Ask Nadia whether these come from a template, a form default, or duplicated records before counting tickets as independent reports.
