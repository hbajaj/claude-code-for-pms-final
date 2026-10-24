# How Dispatch decides who gets pinged

Written by the Dispatch PM from the code in `00-rook/code/dispatch-routing/`, the Glossary and the Rook Dispatch one-pager.
Priya's handoff noted that no written description existed. **Wen Li (staff engineer) should review this before anyone relies on it.**
Describes routing as of the fix shipped on 24 Oct 2026 (`routing-fix-proposal.md`), with the earlier behaviour noted where it changed.

## The short version
When a callout comes in, Dispatch takes everyone who is available in that area and puts them in order, best match first. It pings the top person's phone.
If they say yes, done. If they say no, or don't answer in time, it pings the next person, and so on down the list.
Every answer feeds back into that responder's score, which affects where they land in the order next time.

## Step by step

**1. Who's on the list** (`availability.available_for`)
- Everyone marked available in the callout's region at that moment. Responders or their handlers set availability in the app. Routing never changes it.
- Availability is a yes/no filter, not part of the score. (The Glossary lists it as a score input, which is wrong.)
- Nobody available is left off. But see step 4: being on the list doesn't mean you'll be asked.

**2. The order** (`routing.score`)
Each responder gets a score. Higher means asked sooner.

| Part | Weight (since 4.2) | Weight (before 4.2) | How it's worked out |
| --- | --- | --- | --- |
| Proximity | 0.60 | 0.45 | Travel-time estimate (since 4.1). 1.0 if they're practically there, falling to 0 at 45 minutes or more. |
| Recent acceptance | 0.25 | 0.40 | The responder's running score, from 0 to 1. See step 5. |
| Capability match | 0.15 | 0.15 | Share of the callout's required tags they have. 1.0 if it needs none. |

A responder with none of the required tags still makes the list, just lower down. Nothing filters on capability.

**3. The ping** (`offer.offer_to`)
The callout goes to the top responder's phone. They have **90 seconds** to answer (4.2 cut it to 60 from 12 Aug; restored to 90 on 24 Oct).
There are three outcomes: **taken**, **turned down**, or **missed** (no answer in time, so the offer is withdrawn from their phone).

**4. Walking the list** (`offer.dispatch`)
- Taken: the callout is assigned, and we stop.
- Turned down or missed: ping the next person.
- If we reach the bottom without a yes, `dispatch` returns nothing. **What happens to the callout then isn't in this code** (ask Wen).
- Because we stop at the first yes, people near the bottom are rarely or never pinged. Over 29 Jun–6 Sep a callout averaged 1.2–1.6 pings.

**5. The recent-acceptance score** (`history.py`)
- Everyone starts at 0.5.
- **Taken: +0.08. Turned down: −0.12.** The score always stays between 0 and 1.
- **Missed:** free, unless it's the 3rd or later miss in a row (−0.12 each). Any answer resets the run.
  *Before 24 Oct, every miss cost −0.12, the same as a turn-down.*
- **Recovery:** scores ease back toward 0.5 by 0.02 a day, even without pings.
  *Before 24 Oct there was no recovery: a score only rose with a take, and a low score meant fewer pings. That trap switched off four responders after 4.2. Their scores were restored to pre-4.2 values on 24 Oct.*
- Scores are kept in memory, keyed by responder name. Whether they survive a restart or deploy is unknown (ask Wen).

## Worked example
A callout needs one tag. Two responders are available and both have that tag.
- **A**: 10 minutes away, score 0.5 (average).
- **B**: 5 minutes away, score 0.1 (several recent misses or turn-downs).

| | Proximity | Since 4.2 | Before 4.2 |
| --- | --- | --- | --- |
| A | 0.78 | 0.60×0.78 + 0.25×0.5 + 0.15 = **0.74** | 0.45×0.78 + 0.40×0.5 + 0.15 = **0.70** |
| B | 0.89 | 0.60×0.89 + 0.25×0.1 + 0.15 = **0.71** | 0.45×0.89 + 0.40×0.1 + 0.15 = **0.59** |

A is still asked first, even though B is closer. 4.2 narrowed the gap, but a low acceptance score still outweighs being twice as close.
If A takes it, B isn't pinged. Before 24 Oct, B's score then could never rise, which is how responders got stuck. Now it drifts back toward 0.5 over time.

## Things that change routing
- **Config ships with the release.** Weights, ping wait and penalties live in `config.py`. Handlers can't adjust them, and changes go out on the monthly train.
  The file asks that Marcus (engineering manager) is told before anything changes.
- **Handler overrides.** A handler can send a callout to someone other than the top pick. Overrides are logged (audit log, 4.0).
  This code doesn't say whether an override affects anyone's score.
- **Bulk callout (4.1)** sends one callout to several responders at once. How it interacts with ranking and scoring isn't in this code.
- **Supply reads the availability record** (`availability.current_record`) to schedule maintenance. Its shape is a contract, so tell Supply before changing it.

## Open questions for Wen
1. What happens to a callout when nobody on the list says yes?
2. Do scores persist across restarts and deploys?
3. Do overrides and bulk callouts change anyone's score?
4. How is "region" defined, and can a responder 45+ minutes away still be in it?
5. ~~Are the proposed miss rule and decay values sensible?~~ Reviewed by Wen; shipped 24 Oct.
