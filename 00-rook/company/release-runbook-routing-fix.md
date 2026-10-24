# Release runbook: routing fix, score restore, 90s ping wait

**Approvals:** Helen Achebe (Director of Product), 24 Oct 2026, for all three changes. Wen Li (staff engineer) reviewed the change and cleared the Dispatch PM to deploy, 24 Oct 2026.
**Code:** `00-rook/code/dispatch-routing/` in this repo (config.py, history.py, offer.py; see CHANGELOG).
**Status:** **shipped 24 Oct 2026** by the Dispatch PM through Rook's release process. The four scores were restored after deploy.
Post-deploy checks are tracked in `post-deploy-checks.md`.

## Before deploy (completed by the Dispatch PM, 24 Oct 2026)
- [x] Marcus Oyelaran told that `config.py` is changing (its header asks for this).
- [x] Wen confirms the **live** scores for Vesper, Meteor Mite, Farlight and The Undertow. Mine are replayed from the ping log.
- [x] Wen confirms how `history.restore()` will run **inside the live routing process**. Scores are held in memory, so a separate script won't reach them.
- [x] Note the time of deploy. Every check below compares before and after it.
- [x] Message 1 sent to Aunt Dot and Kip (`00-rook/feedback/handler-messages.md`), if not already.

## Deploy (in this order)
1. Ship the code: misses scored separately, score decay, and `OFFER_TIMEOUT_SECONDS = 90`.
2. **Then** restore the four scores, in the same window:
   ```python
   history.restore({"Vesper": 0.96, "Meteor Mite": 1.0, "Farlight": 0.84, "The Undertow": 0.88})
   ```
   Never restore before the new rules are live, or misses at 60s can sink them again.
3. Confirm in the live process that the four scores read back as set, and that `OFFER_TIMEOUT_SECONDS` is 90.

## After deploy: first 48 hours
- [ ] A ping that goes unanswered is withdrawn after 90s, not 60.
- [ ] The four responders receive pings again. Expect a few each within 48 hours, in their own areas.
- [ ] No spike in unserved callouts or in time to assign a callout.
- [ ] Nadia watches for new "gone before I could answer" or "phone never goes off" tickets.

## After deploy: two weeks (weekly, `dispatch-guardrail-metrics.md`)
| Check | Expect |
| --- | --- |
| Miss rate | Back to about 1–3% of pings |
| Starved responders | None |
| Pings for the four | About 11–14 a week each (their pre-4.2 level) |
| Local share: Old Town, Uptown, Harborside, Eastgate | Mostly local again (was 7–14% in three of them) |
| Unserved callouts | 4–12 a week |
| Acceptance rate | 75–78%. Read alongside the rows above, not alone. |

When the two-week checks pass: send message 2 to Aunt Dot and Kip, update the release notes (see `wiki-corrections.md`), and mark the roadmap item shipped.

## Rollback
- **Trigger:** unserved callouts above 20 in a week, a sharp rise in time to assign, or new evidence that the change broke dispatch.
- **How:** redeploy the previous routing release. If only the ping wait is the problem, set `OFFER_TIMEOUT_SECONDS` back to 60 and keep the miss fix: the fix protects scores at either setting.
- Restored scores don't need undoing. Under the new rules they drift toward neutral on their own.
- Tell Helen, Marcus and Wen. Hold message 2.
