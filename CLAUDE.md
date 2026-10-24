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

### Callout journey, with handler complaints mapped (Sept interviews; n = how many of 4 handlers raised it)
1. Callout comes in (handler or intake). No complaint; but volume fell about 20% on release day, unexplained.
2. List who's available in the area. No complaint.
3. Rank by distance + acceptance score + capability. Quiet weeks or lopsided work shows up here (2: Dot, Kip).
4. Ping the top responder's phone. Alerts easy to miss or don't say who they're for (3: Dot, Ambrose, Kip). **Still open.**
5. Wait for an answer (60s from 12 Aug, 90s from 24 Oct). Gone before he could answer (3: Dot, Ambrose, Halloran). Fixed 24 Oct.
6. Taken, or move to the next responder. Stops at the first yes, so a low rank means no pings.
7. Update the acceptance score. Root cause of quiet weeks: a miss counted as a no, with no recovery. Fixed 24 Oct.
8. Handler watches the console. Text too small (2: Dot, Ambrose); too bright at night, coverage view not enough,
   filters reset silently, tag legend buried (1 each); nothing explains why one card is quiet (Kip).
9. Handler reports a problem. Feedback goes nowhere (3: Ambrose, Halloran, Kip).
- Supply: catalog search needs the exact name (1); urgent requisitions stuck in one queue, a safety risk (1);
  failure reports get no reply (1). All Halloran.

### Releases
4.0 (7 Apr): audit log. 4.1 (16 Jun): travel-time proximity, bulk callout. 4.2 (12 Aug): proximity weight
0.45→0.60, **acceptance weight 0.40→0.25** (not in the release notes), **ping wait 90s→60s**, persistent filters.

### 4.2: what the data shows (database covers 29 Jun–6 Sep only)
- **Not seasonal.** Acceptance was 75–78% every week through 3 Aug, fell to 54% in release week, then 66→67→73%.
  Missed pings went from 2–6 a week to 21–38. There's no earlier data to back Priya's "August is always soft".
- **Mechanism (code):** a miss cost −0.12, the same as a turn-down (a take is +0.08); no recovery; floor 0. The 60s wait caused
  misses, misses sank scores, low scores meant no pings, so there was no way back. This contradicted the Glossary and README.
- **Four responders switched off:** Vesper 86→17 pings, Farlight 75→11, The Undertow 75→14, Meteor Mite 70→14. Replayed scores
  hit 0, while everyone else sat at 0.72–1.0. Meteor Mite and The Gale share Eastgate, so distance doesn't explain it.
- **Less local, the opposite of 4.2's goal:** out-of-area pings went from 17% to 39%. Callouts taken locally: Old Town 14%, Uptown 7%, Harborside 10%.
- **Tickets:** 5–8 a week rose to 20–32; ⅔ "phone never goes off", ⅓ "gone before I could answer". They undercount: Dot and Kip
  never file. Several bodies are word-for-word identical, so check with Nadia. The 73% recovery is misleading,
  because starved responders' misses drop out of the rate.
- **Unexplained:** callouts fell from about 20 a day to about 16 *on release day*, in every area, most in Northfield/Westbury (−33%).
  That's where Corporal Ashgrove and Halfmoon lost half their pings despite top scores. Check intake and logging.
- **Possible Supply effect (unverified):** Supply books maintenance where callout load looks low.

### Other gaps
- Roadmap stale (owners all Priya; Availability Confidence dropped quietly). Briefs stale (Bulk Callout, Audit Log already shipped).
- Filters reset silently. Billing listed Halfmoon and The Undertow twice. Handlers share logins. Bulk callout's effect on scores is unknown.
- Data we lack: availability, capability tags, live scores, answer times. The Team directory doesn't list me.

### Shipped 24 Oct 2026, now in two-week monitoring
- Approved by Helen and Wen. Misses scored separately (only 3+ in a row cost), scores recover 0.02 a day, ping wait back to 90s,
  and four scores restored to pre-4.2 values (0.96/1.00/0.84/0.88), not 0.5, which would still have left them last.
- Checks on 26 Oct, 31 Oct and 7 Nov need live data from Ravi (`post-deploy-checks.md`). Watch first for Eastgate flipping
  to Meteor Mite (1.00 vs The Gale 0.96). At week 2: message 2 to Dot and Kip, paste the wiki corrections, close the roadmap item.

### Routing v2 (`routing-v2-proposal.md`)
- Built and tested (14 checks in `test_routing.py`), **not deployed, so the repo is ahead of production**: capability filter,
  second round for missed pings, scores stored by ID. Needs Wen's review and Helen's OK; the deploy needs `history.import_legacy`.

### Files (in `00-rook/company/` unless noted)
routing-fix-proposal, how-routing-works, release-runbook-routing-fix, post-deploy-checks, score-reset-request,
message-to-wen-and-marcus, q3-roadmap-update, wiki-corrections, dispatch-guardrail-metrics, open-questions;
`00-rook/feedback/`: interview-tickets (.md + .csv), handler-messages.

### My to-dos
1. Get Ravi's live data and confirmation of the numbers. Run the post-deploy checks.
2. Next open complaint: alerts easy to miss (step 4). Escalate Halloran's urgent-requisition queue to Supply as a safety issue.
3. Call Linda Pruitt and Desmond Okafor (churn signals). Ask Wen and Marcus to investigate the callout drop.
4. Take the roadmap decisions to Helen; send the data requests; ask Supply what "callout load" means.
