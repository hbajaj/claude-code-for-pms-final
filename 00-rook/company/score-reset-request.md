# Request: restore the scores of four responders hurt by 4.2

From the Dispatch PM to Wen Li (staff engineer), copying Marcus Oyelaran. Needs Helen Achebe's OK, because it changes who gets pinged.
Related: `routing-fix-proposal.md` and `how-routing-works.md`.

## What we're asking
Put these four responders' recent-acceptance scores back to where they were **before 4.2** (12 Aug 2026):

| Responder | Handler | Area | Score before 4.2* | Score now* | Restore to |
| --- | --- | --- | --- | --- | --- |
| Vesper | Aunt Dot | Old Town | 0.96 | 0 | 0.96 |
| Meteor Mite | Kip | Eastgate | 1.00 | 0 | 1.00 |
| Farlight | Linda Pruitt | Uptown | 0.84 | 0 | 0.84 |
| The Undertow | Desmond Okafor | Harborside | 0.88 | 0 | 0.88 |

\*Replayed from the ping log (29 Jun–6 Sep) using the current scoring rules, starting everyone at 0.5 on 29 Jun. **Wen: please check the live values first.** Scores live in memory, keyed by name, so the real numbers may differ (for example, if a deploy wiped them).

No other responder needs this. In the same replay everyone else is between 0.72 and 1.0. Corporal Ashgrove and Halfmoon had their pings roughly halve but are at 1.0. Their drop has another cause; see the callout drop in open-questions.md.

## Why pre-4.2 scores, not neutral (0.5)
Neutral would still leave all four below every competitor (0.72–1.0). Meteor Mite would keep losing every Eastgate callout to The Gale (0.96), so nothing would change for Kip.
The drop came from a defect (misses scored as turn-downs), not from their behaviour, so putting them back where they were is the fair correction.
If Helen prefers a more cautious option, use 0.8: near the middle of the active responders, and above neutral.

## How
`history.py` in the repo now has both functions (basic checks pass locally):
```python
history.restore({"Vesper": 0.96, "Meteor Mite": 1.0, "Farlight": 0.84, "The Undertow": 0.88})
# or, for neutral:
history.reset(["Vesper", "Meteor Mite", "Farlight", "The Undertow"])
```
They have to run **inside the live routing process**, because scores are held in its memory. A separate script won't affect it. Wen to decide how: an admin hook, or as part of the deploy.

## Order of operations
1. **Ship the miss-rule fix first, or at the same time.** Restoring scores under the old rule won't stick: one bad evening of misses at 60s would sink them again.
2. Restore the four scores.
3. Watch for two weeks. Each should get back to roughly their pre-4.2 weekly pings (about 11–14 a week), and the local share in Old Town, Uptown, Harborside and Eastgate should return to mostly local. Use the starved-responder and local-share checks in `dispatch-guardrail-metrics.md`.
4. Let the handlers know (drafts in `00-rook/feedback/handler-messages.md`).
