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
- Rook sells software to independent masked **responders**, their **handlers** and **quartermasters**.
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
- **Routing priority**: see `00-rook/company/how-routing-works.md`.

### Releases
4.0 (7 Apr): audit log. 4.1 (16 Jun): travel-time proximity, bulk callout. 4.2 (12 Aug): proximity weight
0.45→0.60, **acceptance weight 0.40→0.25** (not in the release notes), **ping wait 90s→60s**, persistent filters.

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
  Halloran all described it in interviews. **Tickets undercount:** the handlers of Vesper and Meteor Mite
  (Aunt Dot, Kip) have never filed one. They only spoke up in interviews.
- **4.2 made routing *less* local, the opposite of its goal.** Pings to responders outside the callout's area went from 17%
  to 39%. Callouts taken locally fell from 100% to 14% in Old Town, 7% in Uptown and 10% in Harborside.
- **The recovery to 73% is misleading.** Acceptance is rising because the starved responders
  no longer get pinged, so their misses drop out of the rate.
  Callouts nobody took rose from 4–12 a week to 14–17 for three weeks, then fell to 7. They aren't tracked anywhere:
  a coverage gap only counts capability mismatches.
- **Answer to Marcus's 14 Aug question.** The config doesn't separate responders who turn jobs down. Lowering the acceptance
  weight actually *helped* them. The harm comes from misses being penalised like turn-downs.
- **Unexplained:** callout volume fell from about 20 a day to about 16 *on release day* and stayed down,
  across every area. It fell most in Northfield and Westbury (−33%), home of the two "halved" responders.
  Check intake and logging, and whether handlers are routing around the console.
- **Possible Supply effect (unverified):** Supply schedules maintenance where callout load is low.
  Starved responders now look low-load. "Maintenance booked on a bad day" tickets started 15 Aug.

### Other contradictions and gaps
- **Roadmap is stale** (last reviewed 30 Jun; all owners still Priya). Availability Confidence is "Committed 4.2" but
  didn't ship. The interviews were for a "console redesign" that isn't on the roadmap.
- **Briefs are stale or misread.** Bulk Callout (shipped 4.1) and Audit Log (shipped 4.0) read as unstarted.
  The Phone App brief misreads Aunt Dot. Approval Chains doesn't fix Halloran's slow single queue.
- **Filter persistence isn't just noise.** Filters reset silently and the active-filter badge is easy to miss,
  so a handler can watch the wrong list.
- **Data caution:** several tickets have word-for-word identical bodies. Check with Nadia before counting them.
- **Data we lack:** availability, capability tags, routing scores, answer times. Team directory doesn't list me.

### Drafts in this repo (all need review; none shared yet)
- `00-rook/company/routing-fix-proposal.md`, with the code change in `00-rook/code/dispatch-routing/`
  (misses scored separately, score decay, `history.reset()`; basic checks pass locally; not reviewed by Wen).
- `00-rook/company/how-routing-works.md`: the missing routing description, for Wen to check.
- `00-rook/company/q3-roadmap-update.md`: corrected roadmap, plus three decisions for Helen.
- `00-rook/company/wiki-corrections.md`: paste-ready fixes for the Glossary, release notes, briefs and one-pager.
- `00-rook/company/dispatch-guardrail-metrics.md`: weekly guardrails and eight data requests.
- `00-rook/company/open-questions.md`: callout drop, Supply impact, filter bugs, local routing, ticket blind spot.
- Note: the repo's routing code holds the *proposed* fix, not what's running in production.

### My to-dos
1. Before the regroup, take the numbers to Marcus, Nadia and Ravi, and get Ravi to confirm them.
2. **Helen approved the routing fix and the pre-4.2 score restore for the four starved responders (24 Oct).**
   Helen also confirmed the ping wait goes back to 90s (in the repo's config).
   Wen reviewed it and cleared me to deploy (24 Oct). Deploy via Rook's release process using
   `release-runbook-routing-fix.md`; this repo can't deploy.
   Send message 1 to Aunt Dot and Kip (`00-rook/feedback/handler-messages.md`); message 2 only once it's live.
3. Take the roadmap decisions to Helen, then paste the wiki corrections in.
4. Send the data requests. Ask Supply what "callout load" means in their scheduler.
