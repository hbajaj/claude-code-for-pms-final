# Ranking replay: who would have been pinged under each rule

Dispatch PM, 7 Nov 2026. A rough replay from the rook-database. It doesn't replace Wen's full ranking replay.

## What it does
- **Callouts:** re-runs all 1,319 real callouts (29 Jun–6 Sep).
- **Timing:** each rule "goes live" on 12 Aug. Before that, everyone runs the pre-4.2 rules, so all rules start from the same scores.
- **Who gets pinged:** decided by the rule.
- **How each responder answers:** drawn from how that responder actually answered in the database.
  - **Miss rate:** set by the ping wait. It's 2.3% at 90s and 18.0% at 60s.
  - **Take rate when they answer:** 78% on average, using each responder's own rate.
- **Averaging:** 300 random runs per rule.

Run it with `python replay.py data.json 300 5 15`.

## Assumptions (the database has no availability, capability tags or locations)
- **Availability:** everyone is always available and carries the needed tags.
- **Who can be asked:** a responder can be asked about an area only if they were asked about it at least once in the real data.
- **Travel time:** 5 min in their own area, 15 min elsewhere. This was calibrated: it reproduces both periods to within about 2 pings a week per responder. A 10-minute version was also run to check sensitivity.
- **List length:** at most 4 responders per callout, the most the real data shows.

## Does it reproduce what actually happened?
| After 4.2 | Actual | Replay of 4.2 |
|---|---|---|
| Acceptance | 64% | 64% |
| Missed pings a week | 30 | 32 |
| The Gale, pings a week | 18.6 | 19.8 |
| Vesper / Farlight / The Undertow / Meteor Mite | 4.6 / 3.0 / 3.8 / 3.8 | 8.4 / 5.7 / 6.2 / 3.8 |

It reproduces the overall picture and the direction of the starvation, but **underplays how hard three of the quiet four were hit**. Any benefit it shows for a fix is therefore conservative.

## Results (12 Aug–6 Sep, as if each rule had gone live on 12 Aug)
| Rule | Quiet four, pings a week each | The Gale | Acceptance | Misses a week | Unserved | Pings per callout |
|---|---|---|---|---|---|---|
| 4.2 as shipped (60s) | 8.4 / 5.7 / 6.2 / 3.8 | 19.8 | 64% | 32 | 3.8% | 1.49 |
| 24 Oct fix (90s) | 14.6 / 9.9 / 11.0 / 5.8 | 15.6 | 77% | 4 | 0.8% | 1.29 |
| 24 Oct fix at 60s | 13.8 / 9.8 / 10.9 / 5.6 | 18.8 | 63% | 37 | 3.8% | 1.54 |
| **Proposed 4.3 (90s)** | **14.4 / 10.4 / 10.7 / 5.8** | **15.6** | **77%** | **4** | **0.6%** | **1.30** |
| Proposed 4.3 + workload term | 14.1 / 10.6 / 11.1 / 6.4 | 14.8 | 77% | 4 | 0.6% | 1.30 |
| Proposed 4.3 at 60s | 16.4 / 12.3 / 13.1 / 7.6 | 18.1 | 62% | 41 | 1.1% | 1.61 |

Quiet four = Vesper / Farlight / The Undertow / Meteor Mite.

## What it shows
1. **The 90-second wait is what restores acceptance and cuts misses.** Every rule at 60s lands at 62–64% acceptance and 32–41 misses a week. Every rule at 90s lands at 77% and 4.
2. **The scoring change is what protects quiet responders.** At 90s, both the 24 Oct fix and the proposed score bring the quiet four back up.
   - **The proposed score holds up better.** With the 10-minute travel assumption, the 24 Oct fix leaves Farlight and The Undertow at 7.7 and 8.4 a week. The proposed score keeps them at 10.0 and 10.4, and keeps out-of-area pings at 22% against 46%.
3. **At 60s, the proposed score still protects the quiet four** (it gives them the most pings of any rule) **but cannot fix acceptance or misses.** A faster wait would need the alert changes (lock-screen actions, second alert) to work first, and this replay can't test those.
4. **The second round** brings unserved callouts down from 0.8% to 0.6%.
5. **The workload term** evens out The Gale (15.6 → 14.8) and lifts Meteor Mite (5.8 → 6.4), with no cost to acceptance.

## What it can't show
- **Meteor Mite's absolute numbers.** Even with the old rules, the replay gives Mite only about 4 pings a week, against an actual 11 before 4.2. Mite and The Gale share Eastgate, and in reality availability splits the work between them. The database has no availability data, so the brief's "Mite back to ~11" target can only be checked with live data.
- **Unserved and out-of-area levels.** The direction is right, but the levels aren't: everyone is assumed always available, and the replay has no area map.
- **The alert and lock-screen changes.** The replay can't model how quickly a responder notices a ping. That needs usability tests and the answer-time data we don't record yet.

## Next
- Wen's full replay with real availability, tags and travel times.
- Ravi's live data on the 24 Oct fix.
- Usability tests of the prototype.
