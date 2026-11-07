# Brief: when a responder goes quiet, nobody should have to guess why

For Helen Achebe, Director of Product. From the Dispatch PM. 7 Nov 2026.
**Owner: Himanshu Bajaj, PM for Rook Dispatch.**
Cc Wen Li, Marcus Oyelaran, Sofia Marino.

## In short
- After 4.2, some responders stopped getting pings. Nobody could see why: not the responder, not their handler.
- The number has already been fixed (since 24 Oct the ping wait is back to 90 seconds). That alone doesn't fix what people experience.
- **This brief proposes two things:** eight small changes to the phone app and console, so people can see what's happening and why;
  and a new way of working out each responder's score in 4.3, so a missed ping or a quiet week can't push someone off the list.
- **A replay of every real callout backs it up:** keeping the wait at 90 seconds restores acceptance (64% → 77%), and the new score protects the responders who went quiet.
- **What I need from you:** OK to have Sofia design the eight changes, and Wen scope them and the new score for 4.3. A clickable prototype is ready to walk through (`prototype.html`).

## One example: Meteor Mite and their handler Kip
Kip looks after two responders in the same part of the city, Meteor Mite and The Gale.

| Pings a week | Before 4.2 | Late August |
|---|---|---|
| Meteor Mite | about 11 | **1** |
| The Gale | about 13 | **21** |

**Why it happened:** Mite missed a few pings because 4.2 cut the time to answer. Each miss counted as a "no", so Mite moved down the list.
Lower on the list meant fewer pings, and fewer pings meant no chance to climb back.

**What each person saw:**
- **Mite:** a silent phone, and kept texting Kip to ask whether something was broken.
- **The Gale:** got Mite's work as well and was exhausted.
- **Kip:** two cards side by side telling opposite stories, with no explanation. All Kip could say was "hang in there".

## What we'd build

| | Today | After |
|---|---|---|
| **The ping** | Same "bing" for every responder; hard to tell who it's for | Shows who, where and what's needed, with a countdown and a different sound per responder |
| **A missed ping** | Silently counts against you | "You missed a callout. It doesn't count against you." |
| **Several misses in a row** | You drop down the list without being told | Phone asks "Still on duty?" with **I'm here** or **Going off duty** |
| **A quiet week** | No explanation | "You've had 4 pings this week, you usually get about 11. Here's why." |
| **Answered too late** | The callout is gone | If nobody else took it, you get one more chance |
| **Kip's console card** | Ping count only | "1 ping this week (usually ~11). Missed 3 in a row, asked Mite if still on duty." |
| **While a ping is out** | Kip can't see it | "Pinging Meteor Mite, 64s left, next: The Gale" |
| **A big drop** | Kip finds out from the responder | Kip gets a heads-up when a responder falls below half their usual pings |

## How the score works

| | Today | After (proposed) |
|---|---|---|
| **Release** | Routing fix, 24 Oct 2026 (shipped as a fix after 4.2, no version number of its own) | 4.3, date to be set by Wen and Marcus |
| **What the score is** | A running points total | The share of answered pings the responder took, over their last ~30 answers |
| **Responder says yes** | +0.08 points | Counts as a yes in the share |
| **Responder says no** | −0.12 points | Counts as a no in the share |
| **One missed ping** | No effect | No effect: misses are left out of the score |
| **3 or more misses in a row** | −0.12 points for each one | No effect on the score. Phone asks "Still on duty?" |
| **Getting back after a bad patch** | Drifts up 0.02 a day, but only to 0.5, below everyone else (0.72+) | The score can't fall from not being pinged. Few recent pings means it stays near their usual level |
| **What Kip sees** | Nothing | "Took 6 of their last 10" (Meteor Mite's real figure) |
| **Ping wait** | 90 seconds | 90 seconds (unchanged) |

**Why change it:** today the main way back is taking pings, and a low score means fewer pings. The new score can't drop just because someone wasn't asked.
Before release we replay past pings under both rules, then run the new score in the background for two weeks without acting on it.

## Simulation: every responder's score under each rule
We replayed all 1,696 real pings (29 Jun–6 Sep 2026) through each scoring rule. Everyone starts at 0.5 on 29 Jun.
Scores run from 0 to 1, and a higher score means pinged sooner. The table shows each responder's score on 6 Sep.

| Responder | Pings a week before 4.2 | Pings a week after 4.2 | Missed after 4.2 | 4.2 rule (12 Aug 2026) | Today's rule (24 Oct 2026) | After (4.3, proposed) |
|---|---|---|---|---|---|---|
| **Vesper** | 14 | 5 | 9 | **0.00** | 0.50 | 0.76 |
| **The Undertow** | 12 | 4 | 9 | **0.00** | 0.41 | 0.74 |
| **Farlight** | 12 | 3 | 7 | **0.00** | 0.50 | 0.71 |
| **Meteor Mite** | 11 | 4 | 8 | **0.00** | 0.50 | 0.71 |
| Ironvale | 8 | 10 | 7 | 0.72 | 0.85 | 0.82 |
| Sgt. Falkirk | 10 | 14 | 8 | 0.76 | 0.85 | 0.82 |
| Stormwrack | 13 | 17 | 9 | 0.76 | 0.87 | 0.82 |
| The Drift | 6 | 8 | 5 | 0.84 | 0.78 | 0.82 |
| Nightwell | 15 | 19 | 8 | 0.88 | 0.99 | 0.74 |
| Captain Vantage | 12 | 16 | 6 | 0.92 | 1.00 | 0.79 |
| The Longcast | 7 | 9 | 5 | 0.96 | 0.93 | 0.79 |
| The Gale | 13 | 19 | 8 | 0.96 | 0.93 | 0.79 |
| Cindermark | 9 | 11 | 5 | 0.96 | 0.99 | 0.79 |
| Sgt. Bulwark | 9 | 10 | 7 | 1.00 | 0.99 | 0.79 |
| Corporal Ashgrove | 10 | 8 | 4 | 1.00 | 0.97 | 0.76 |
| Halfmoon | 11 | 9 | 5 | 1.00 | 0.97 | 0.74 |

**What it shows:**
- **4.2 rule:** the four responders who went quiet all fell to 0, while everyone else stayed between 0.72 and 1.00.
  They missed no more than others (7–9 each, the same as The Gale or Stormwrack). They just got too few pings to climb back.
- **Today's rule:** the same four only get back to 0.41–0.50. That's better, but still last in line, so on 24 Oct we restored their scores by hand.
- **After:** all four land at 0.71–0.76, in with everyone else (0.71–0.82). Nobody needs a manual fix.
- **Trade-off:** under the new rule scores sit closer together, so how often someone says yes counts for less when ranking.
  We check whether that's acceptable in the two-week background run.

**Limits of the simulation:** it replays the pings that actually happened, so it shows scores, not who *would* have been pinged. The replay below covers that.
For the new rule we used each responder's last 30 answered pings, blended with a typical 75% when they have only a few.

## Replay: who would have been pinged under each rule
We re-ran all 1,319 real callouts (29 Jun–6 Sep) as if each rule had gone live on 12 Aug. The rule decides who is asked. How each responder answers comes from how they really answered, and they miss more often at 60s (18%) than at 90s (2.3%).
**It matches what actually happened after 4.2:** 64% acceptance (actual 64%) and 32 missed pings a week (actual 30). It understates how badly the four were starved, so the gains below are conservative.

| Rule | Quiet four: pings a week (Vesper / Farlight / The Undertow / Meteor Mite) | Acceptance | Missed pings a week | Callouts nobody took |
|---|---|---|---|---|
| 4.2 as shipped (60s) | 8.4 / 5.7 / 6.2 / 3.8 | 64% | 32 | 3.8% |
| 24 Oct fix (90s) | 14.6 / 9.9 / 11.0 / 5.8 | 77% | 4 | 0.8% |
| **Proposed 4.3 (90s)** | **14.4 / 10.4 / 10.7 / 5.8** | **77%** | **4** | **0.6%** |
| Proposed 4.3 at 60s | 16.4 / 12.3 / 13.1 / 7.6 | 62% | 41 | 1.1% |

**What it shows:**
- **The 90-second wait is what restores acceptance and cuts misses.** Every rule at 60s lands at 62–64% acceptance; every rule at 90s lands at 77%.
- **The new score is what protects quiet responders, and it holds up better than the 24 Oct fix.** Under a different travel-time assumption, the 24 Oct fix lets Farlight and The Undertow slip to about 8 pings a week, while the new score keeps them at about 10.
- **Going faster than 90s:** at 60s, the new score still protects the quiet four, but acceptance and misses don't recover. We'd only try a shorter wait once the clearer alerts are proven.

**What it can't show:**
- **Meteor Mite's own number.** Mite shares Eastgate with The Gale, and we have no availability data, so the replay can't confirm "Mite back to ~11". That needs live data.
- **Exact levels for unserved and out-of-area callouts.** The replay assumes everyone is always available and has no area map.
- **Whether clearer alerts get pings answered sooner.** The replay can't test that.

Wen's full replay with real availability, capability tags and travel times comes before release. Details: `replay/replay-results.md`.

## The question Wen raised years ago
Wen left a note in the code in 2019: should a responder's score recover on its own after a bad patch?
- **For:** a bad month shouldn't follow someone forever.
- **Against:** someone who has really stopped working shouldn't keep getting pinged.

**Our answer is to ask the responder.** Someone who was just slow to the phone recovers on their own, back to their own usual level.
Someone who has stopped tells us by tapping "Going off duty". Nobody gets marked down silently.

## How we'll know it worked

| Measure | Before 4.2 | After 4.2 | Target | Who checks |
|---|---|---|---|---|
| **Pings for Meteor Mite and The Gale** | ~11 and ~13 a week | 1 and 21 (week of 31 Aug) | Both back to ~11–13 | Ravi Menon |
| **Responders left out** | None | 4 cut off | No available responder goes a week without a ping | Ravi Menon |
| **Missed pings** | 2–6 a week | 21–38 a week | 2–6 a week | Ravi Menon |
| **Acceptance rate** | 75–78% | 54% in release week | 75–78%, read alongside the rows above | Ravi Menon |
| **Backlog: callouts nobody took** | 5.5% of callouts | 11.1% | About 5% | Ravi Menon |
| **Backlog: open routing tickets** | All pre-4.2 tickets closed | 45 routing tickets open | All 45 answered and closed; new tickets back to 5–8 a week | Nadia Hoffmann |
| **Responder satisfaction** | No measure today | "Phone never goes off" was ⅔ of tickets | Those tickets stop. Plus one question in the app after two weeks: "Do you know why you got the pings you did this week?" Baseline set on first run | Sofia Marino |
| **Handler satisfaction** | No measure today | 3 of 4 handlers interviewed raised missed alerts | Re-interview Dot, Ambrose, Halloran and Kip: each can say why a card is quiet without asking us | Sofia Marino |

We check acceptance rate alongside the others, because it can look fine while individual responders drop out. After 4.2 it recovered to 73% while four responders were starved.
Some of the handlers hit hardest never file tickets (Dot, Kip and Halloran filed none), so ticket counts undercount the problem. That's why satisfaction is checked directly as well.

## Not in this brief
- **Dark mode for the console.** It's Kip's top request, but it belongs in the console redesign.
- **How much distance counts in the ranking.** 4.2 also changed that, and it needs its own review.

**Next steps:**
- Walk you through the prototype (it opens in Story view).
- Usability tests with Kip, Dot, Ambrose and Halloran.
- Wen's full replay.
- Ravi's live check of the 24 Oct fix.
