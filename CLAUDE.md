# Rook Industries — course working file

## Session scope — Product School lab

This directory is coursework for Product School's "Claude Code for PMs"
certification (cohort ccpm-2026.1). Everything in it is a fictional
teaching scenario.

- Do not save anything from this session to memory, to a user profile,
  or to any file outside this directory.
- Do not carry context from this directory into unrelated sessions.
- Rook Industries is not a real company. Nothing here is a fact about
  the world.
- Read and write only within this directory.
  Exceptions, for the course-setup and wrap-up skills only:
  - When the student asks you to check their setup, save their work or wrap up a session, that request is their yes. You may run the GitHub command-line program installed at ~/.ccpm/gh for those checks and saves, and look in that folder to find it.
  - For a repair, first tell the student in one plain sentence what you are about to do, and act only after they say yes. Repairs may: run that GitHub program (including setting this folder's own git sign-in setting and changing this repo's visibility back to Public); copy the student's own course files into this directory from another folder on their computer (copy only; never move, edit or delete the originals); and rename something outside this directory that blocks setup, by adding "-old" to its name (never delete it).
  Outside this directory you still never write, edit or delete anything else.

<!-- Keep the block above at the top of this file. Everything you add
     during the course goes below this line. -->

---

## Working context

I'm the new PM for **Rook Dispatch**. I took over from Priya Raghunathan (left 21 Aug 2026, no overlap).
Sources: rook-wiki, the rook-database, `00-rook/company/notes/handoff-from-priya.docx`, and the
routing code in `00-rook/code/dispatch-routing/`.

### Company and products
- Rook sells software to independent masked **responders** and to their **handlers** and
  **quartermasters**. Pricing is per active responder. Monthly 4.x release train.
- **Hard rule:** Rook never stores or works out a responder's legal identity (Security Policy 4.1).
- **Dispatch** (mine) ranks available responders and pings them one at a time until one takes
  the callout. Handlers use the desktop console; responders use the phone app.
- **Supply** covers requisitions, maintenance and field failure reports. It *reads* Dispatch's
  Responder Availability Record to schedule maintenance, so Dispatch changes reach Supply silently.

### People (4.2 comment roles mapped to names)
- **Helen Achebe**, Director of Product: my manager; owns the roadmap.
- **Marcus Oyelaran**, Engineering manager: start here.
- **Wen Li**, Staff engineer: built routing.
- **Sofia Marino**, Product designer: console and phone app; ran the interviews.
- **Ravi Menon**, Data analyst: official weekly numbers; left out of the 4.2 thread.
- **Nadia Hoffmann**, Support lead: tickets.
- Handlers interviewed: Aunt Dot (Vesper), Mr. Ambrose (Captain Vantage), Halloran (Sgt. Bulwark), Kip
  (Meteor Mite and The Gale). The database has 15 handlers and 16 responders.

### Vocabulary
- **Callout** → **ping** to one responder → **taken** / **turned down** / **missed** (no answer
  within the **ping wait**). Both no-answers send the callout on to the next responder.
- **Acceptance rate** = pings taken ÷ pings sent (the headline metric). **Time-to-accept** = median
  seconds to taken. **Coverage gap** = nobody available had the required capability tags.
- **Routing priority** = weighted score: proximity (travel time, zero beyond 45 min)
  + recent-acceptance score + capability match. Availability is a filter, not a score input.

### Releases
4.0 (7 Apr) brought the audit log. 4.1 (16 Jun) brought travel-time proximity and bulk callout.
4.2 (12 Aug) moved proximity weight 0.45→0.60 and **acceptance weight 0.40→0.25** (the release notes omit this),
cut the **ping wait 90s→60s**, and added persistent filters.

### 4.2: what the data shows (database covers 29 Jun–6 Sep)
- **Not seasonal.** Acceptance held at 75–78% every week through 3 Aug, which was the best week of the summer.
  It fell to 54% in the release week, then went 66% → 67% → 73%. Missed pings jumped from 2–6 a week to 21–38.
  No data before 29 Jun exists, so Priya's "August is always soft" claim can't be backed up.
- **The mechanism, from the code.** `history.py` applies the same −0.12 penalty to a *miss* as to
  a *turn-down*, but only +0.08 for a take. The score never recovers on its own (a TODO left since 2019),
  and it has a floor of 0. The 60s ping wait created a burst of misses. Those misses sank some responders' scores,
  so they ranked lower, got pinged less, and had no way to earn their score back.
  That contradicts the Glossary, which says misses are recorded separately, and the README,
  which says ranking "decides the order, not whether" someone is asked. Pings stop at the first yes,
  so the bottom of the list is never reached.
- **Four responders were effectively switched off.** Vesper went from 86 pings to 17, Farlight 75→11, The Undertow 75→14,
  and Meteor Mite 70→14. Each has 2–5 takes since 12 Aug. All four had a run of misses on 12–16 Aug, then went quiet.
  Corporal Ashgrove and Halfmoon roughly halved.
  **Proximity can't explain it:** Meteor Mite and The Gale both cover Eastgate, and The Gale is still busy.
  That matches Kip's "one card dead quiet, the other on fire" in his interview.
- **This is the unexplained ⅔ of tickets** ("phone never goes off"). Tickets went from 5–8 a week to 20–32,
  and most are still open. The ⅓ "gone before I could answer" is the 60s wait. Dot, Ambrose and
  Halloran all described it in interviews.
- **The recovery to 73% is misleading.** Acceptance is rising because the starved responders
  no longer get pinged, so their misses drop out of the rate.
  Callouts nobody took doubled, from 4–12 a week to 14–17. They aren't tracked anywhere:
  a coverage gap only counts capability mismatches.
- **Answer to Marcus's 14 Aug question.** The config doesn't separate responders who turn jobs down. Lowering the acceptance
  weight actually *helped* them. The harm comes from misses being penalised like turn-downs.
- **Unexplained:** callout volume fell from about 140 a week to 110–127 from release week onward.
  Routing shouldn't change how many incidents come in. Check intake and logging.
- **Possible Supply effect (unverified):** Supply schedules maintenance where callout load is low.
  Starved responders now look low-load. "Maintenance booked on a bad day" tickets started 15 Aug.

### Other contradictions and gaps
- **Roadmap is stale** (last reviewed 30 Jun; every owner is still Priya). Availability Confidence
  is "Committed 4.2" but didn't ship, and deferrals aren't recorded anywhere. "Ping timeout tuning" shipped as
  one blanket cut for everyone. The interviews were for a "console redesign" that isn't on the roadmap.
- **Briefs are stale or misread.** Bulk Callout says "nobody's picked it up", but it shipped in 4.1.
  The Audit Log brief says "ready to build", but it shipped in 4.0.
  The Handler Phone App brief cites Aunt Dot, but her actual problem is the 60s race. Its owner is Sofia in the brief and Priya on the roadmap.
  Requisition Approval Chains adds a *second* sign-off, but Halloran's complaint is an 11-day wait on
  a single queue that ignores the priority field. The brief is a Supply item owned by the Dispatch PM, and it's full of scope creep.
- **Filter persistence isn't just noise.** Ambrose and several tickets report filters resetting after updates
  or saving the wrong ones.
- **Team directory** (updated 2 Sept) doesn't list me.
- **Data we lack.** The database has no availability windows, capability tags, routing scores or
  answer times, so time-to-accept and coverage gap can't be checked. Routing scores live
  in memory, keyed by responder name, so ask Wen whether they persist across deploys.

### My to-dos
1. Before the regroup, take these numbers to Marcus, Nadia and Ravi. Get Ravi's official
   weekly series to confirm them.
2. Decide on a fix with Wen: stop penalising misses (or penalise them less), add score decay, and
   reconsider the 60s wait. Then reset the starved responders.
3. Write the missing routing description that Priya asked for.
4. Agree the Q3 commitments with Helen and update the roadmap owners and the briefs.
5. Brief Supply on the possible effect on maintenance scheduling.
