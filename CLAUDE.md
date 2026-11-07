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
- Module 2: interviews and tickets barely overlap. The 4 interviewees filed 1 ticket between them; the 11 ticket filers weren't interviewed.
  Shift and team handlers (handover notes, second logins, shared consoles) are missing from the research.
- 147 tickets: 30 "quiet" (only 4 responders), 16 "gone before answer" (11 responders), 16 filters, 26 Supply. Only about 98 distinct texts,
  because most non-routing issues appear exactly twice. Consolidated top 3: routing (verify fix), console trust (filters, then alerts), Supply safety.
- Unserved callouts usually had a list of only 1–2 responders, and 27 of 49 since 4.2 involved a miss. That's why v2 adds the second round.
- Open: Halfmoon's drop may be availability time zones (ticket 3050), not routing. Interview Linda Pruitt, Desmond Okafor and Teresa Alvarez next.
- Module 3 (pings + support_tickets): misses land on the 1st ping (3%→21% after 4.2); unserved callouts doubled 5.5%→11.1%. Turn-downs still come at ~22s median, so late answers = alert noticed late, not slow deciding. Answer time for "taken" isn't recorded (ask Wen/Ravi).
- Tickets lag pings: "gone before" tracks the previous day's misses (r 0.70), "quiet" tracks misses 8–14 days earlier (r 0.63). Ping drop vs ticket count r 0.96, but only for handlers who file (Dot, Kip, Halloran file none).
- Ticket hygiene: all 40 pre-4.2 tickets closed; after 4.2, 83 of 107 open, incl. all 45 routing ones. 25 texts filed twice, mostly a closed ticket re-raised by another handler ~29 days later. Several tickets are filed exactly N whole hours after a missed ping. Ask Nadia how filed_at is set.
- What cut responders off wasn't miss order but too few pings to recover: Nightwell fell to 0.44 in release week yet recovered with 18 pings; Vesper (0.68) got 5 and missed 3. The Gale and Nightwell missed as many as Meteor Mite and Vesper (8–9) but earned ~4 points from 51 takes. Misses were ~2/3 of the quiet pair's losses.
- Open: why Nightwell (Midtown) kept getting pinged at a low score. Probably few nearby competitors under proximity 0.60; ask Wen. Charts in this session were inline only, not saved to the repo.
- Module 4 (code): commit `6dcea32` is the code as it ran at 4.2. Scores were in memory, keyed by name; a miss went through `record_declined` (−0.12). Nothing in the code treats responders differently by history or start date.
- Marcus's question (did 4.2 apply to past decliners?): it applied to everyone the same, no responder joined after 12 Aug, and pre-4.2 turn-down rate didn't predict losses (Vantage +31%, Bulwark +16%; Vesper only 15% turn-downs and still −67%). Open for Wen: did the 4.2 deploy restart the service and wipe scores to 0.5? Was the effect on decliners discussed?
- Priya's handoff states the 4.2 goal: stop a distant high-acceptance responder being picked over a nearby one. The roadmap row says only "weight proximity more heavily". Nothing addresses decliners.
- Points back on: only a yes (+0.08) and the drift (0.02/day, and only up to 0.5) happen automatically. A responder at 0 needs ~25 days to reach 0.5, which is still below everyone else's 0.72. That's why the four were restored to pre-4.2 values. Consider a recovery rule that doesn't stop at 0.5.
- The wiki Releases page has no entry for the 24 Oct fix. 4.2's 0.60/0.25 weights are still live and unreviewed (out-of-area pings 17%→39%). Charts and the scoring simulator from this session were inline only, not saved to the repo.
- Module 5: Helen's request (`05-super-speed/director-request.txt`) asks for a one-pager and something clickable, showing what Kip and a quiet responder would notice ("not a setting") and properly answering Wen's 2019 note on score recovery. Story built around Meteor Mite and Kip; no "responder I picked" line existed in CLAUDE.md.
- Built: `brief.md` (plain-language, 8 UX changes, scoring Today vs After, 8 measures incl. backlog and satisfaction), `prototype.html` (both phones locked/unlocked, Kip's console, live ranking, breaks, other-area handoff, Story/Sandbox), and a Claude Design canvas: https://claude.ai/artifact/5ynya6Fcne6Cop1MCSnMDE (private; canvas still shows the brief before the replay was added).
- Proposed score: share of answered pings taken over the last ~30, misses excluded, plus "still free?" check-ins instead of penalties. Recommended over patching points; no classic A/B (16 responders compete for the same callouts, ~9 months to detect +3pts). Use replay, a 2-week background run, then a week-by-week switchback.
- Replay of 1,319 real callouts (`05-super-speed/replay/`): the 90s wait restores acceptance (64%→77%, misses 32→4/wk); the new score protects the quiet four and is more robust than the 24 Oct fix; at 60s it can't recover acceptance. It can't validate Meteor Mite (shares Eastgate with The Gale, no availability data). `callouts.what_happened` holds real incident text (the prototype uses made-up ones).
- Open: label prototype features 4.3 vs Later (lock-screen actions, workload term, turn-down reasons and other-area handoff go beyond the brief); Wen's full replay; Ravi's live data for the 7 Nov check; usability tests with the 4 handlers.
- Module 6: built `.claude/skills/review-checklist/` (4 checks: owner, success measure, scope bounded, problem before fix). Every verdict needs a word-for-word quote that `scripts/validate.py` confirms; `references/examples.md` holds the close calls; `review-log.json` fingerprints briefs so edits since review show as "CHANGED".
- The current briefs are `05-super-speed/brief.md` and `05-super-speed/canvas-brief.dc.html` (a copy of the canvas source; it renders only on the canvas). `fix-brief.md` was deleted. Both now say "Owner: Himanshu Bajaj, PM for Rook Dispatch" and pass all four checks; brief.md's summary and ask now name the new 4.3 score.
- The canvas brief still has no replay section (brief.md does), and the repo copy goes stale whenever the live canvas is edited. Neither brief gives an overall date to check the success measures.
- Classmates' briefs (DianneHulty: 1 flag, no owner; Da1mo: 3 flags, owner, success measure, scope) were reviewed from pasted text only and not saved. All five briefs reviewed lacked a named owner at first; problem-before-fix passed in every one.
