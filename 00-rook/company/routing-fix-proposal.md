# Proposal: stop scoring missed pings as turn-downs

From the Dispatch PM, for Wen Li (staff engineer) and Marcus Oyelaran (engineering manager), with Helen Achebe for the release decision.
Status: **draft**. The code change is in `00-rook/code/dispatch-routing/`. It has passed basic checks on the PM's machine (miss rule, decay, reset, and misses vs turn-downs in `dispatch`), but Wen hasn't reviewed it and it hasn't been run against real routing.

## The problem
- When a ping goes unanswered, `offer.dispatch()` records it with `history.record_declined()`. That is the same −0.12 penalty as a responder saying no.
  This contradicts the Glossary, which says missed pings are "recorded separately".
- 4.2 cut the ping wait from 90s to 60s. Missed pings went from 2–6 a week to 21–38.
  Every one of them lowered the responder's score, so they ranked lower and got pinged less.
- Scores never recovered on their own (the open TODO from 2019), and a responder can only earn points back by taking a ping. The responders who sank were stuck.
- Result, from the rook-database (29 Jun–6 Sep): Vesper, Farlight, The Undertow and Meteor Mite fell from 70–86 pings before 4.2 to 11–17 after, with 2–5 taken each.
  Callouts that nobody took rose from 4–12 a week to 14–17 for the three weeks after release, then fell to 7 in the week of 31 Aug. Support tickets went from 5–8 a week to 20–32. About ⅔ of them say "phone never goes off".

## The change (in the repo, proposed for 4.3)
1. **Misses are scored separately** (`offer.py`, `history.record_missed`). A single miss costs nothing.
   The 3rd miss in a row, and each one after it, costs the turn-down penalty, so a responder whose phone is genuinely off still drops.
   Any answer, yes or no, resets the run.
2. **Scores ease back toward neutral**, by 0.02 a day (`SCORE_DECAY_PER_DAY`). A responder at the floor gets back to neutral in about 25 days even if they aren't pinged.
3. **One-off reset** (`history.reset()`): puts the responders hurt by 4.2 back to neutral when the fix ships.
4. **Ping wait back to 90s** (`OFFER_TIMEOUT_SECONDS`). Decided by the Dispatch PM on 24 Oct; Helen still to confirm, since her approval covered items 1–3.
   At 90s, misses were 1–3% of pings; at 60s they're 13–22%. This removes the trigger for the miss spiral and the "gone before I could answer" third of tickets.
   Cost: up to 30s more per unanswered ping, and most callouts take 1–2 pings. Shipping it with the miss fix restores known behaviour.
   A 90s-first, 60s-after split can be tested later as its own change.

## Evidence it targets the right thing
- Replaying the miss rule over the pings in the database: since 4.2 there were **110 misses, and all of them were penalised**.
  Under the new rule **only 6 would be**. The longest run of misses was 4 in a row.
- Before 4.2 there were 25 misses and none came in a run, so the rule changes nothing about pre-4.2 behaviour.

## Before shipping
- [ ] Wen reviews the code, and the penalty and decay values. The values are a PM's starting point, not tuned numbers.
- [ ] Wen confirms how scores are stored. The code keeps them in memory, keyed by responder name, so do they survive a deploy? The reset approach depends on this.
- [ ] Full replay of the ranking with old vs new rules (Wen or Ravi). Expected result: the four starved responders keep getting pinged.
- [ ] Ravi confirms the acceptance and ping numbers against the official weekly series.
- [x] Helen approved the fix and the score restore (24 Oct 2026). Wen and Marcus pick hotfix or 4.3. Marcus is told before `config.py` changes, as its header asks.
- [ ] Glossary, README and the routing description are updated to match.

## How we'll know it worked
- Each responder's share of pings returns to its pre-4.2 range. No responder goes a week without a ping while available.
- Callouts nobody took fall back to about 4–12 a week.
- "Phone never goes off" tickets stop arriving.
- Acceptance rate is watched *alongside* these. On its own it went up while the problem got worse.
