# Q3 roadmap — proposed update after 4.2

Draft by the new Dispatch PM, 24 October 2026, for review with Helen Achebe (Director of Product).
The wiki roadmap was last reviewed on 30 June and still shows every 4.2 item as "Committed".
The roadmap says changes to committed items go through Product, so this is a proposal until Helen signs off.
Sources: the Releases database, the 4.2 release page and comments, the dispatch-routing CHANGELOG and config, the product briefs, and Priya's handoff note.

## Roadmap items

| Item | Product | Target | Status (was → proposed) | Owner (was → proposed) | Notes |
| --- | --- | --- | --- | --- | --- |
| Change to who gets pinged | Dispatch | 4.2 | Committed → **Shipped 12 Aug; under review** | Priya → Dispatch PM | Proximity weight 0.45→0.60 and acceptance weight 0.40→0.25. The acceptance cut isn't in the release notes. Acceptance fell after release; see "4.2 follow-up" below. |
| Ping timeout tuning | Dispatch | 4.2 | Committed → **Shipped 12 Aug; under review** | Priya → Dispatch PM | Shipped as one blanket cut, 90s→60s, for everyone. Misses jumped from 2–6 a week to 21–38. |
| Availability Confidence | Dispatch | 4.2 → **TBD** | Committed → **Not shipped (dropped from 4.2)** | Priya → Dispatch PM | Squeezed out when the 4.2 timeline compressed. Not in the release notes, and the deferral was never recorded. **Decision needed:** still a Q3 commitment? It touches the Availability Record that Supply reads. |
| Requisition approval chains | Supply | 4.3 | Committed (unchanged) | Priya → **Supply team (name TBD)** | This is a Supply item, so it shouldn't sit with the Dispatch PM. **Decision needed:** scope. The brief bundles five features. Halloran's interview complaint is an 11-day wait on a single queue that ignores the priority field, and a second sign-off alone won't fix that. |
| Handler phone app | Dispatch | Q4 | Exploring (unchanged) | Priya → **Sofia Marino** | Matches the brief (8 Sep), which names the product designer as owner. Not staffed for a build. |
| Shared cover between responders | Dispatch | Q4 | Exploring (unchanged) | Priya → Dispatch PM | Same as "mutual aid" in the Glossary. No brief yet. |

## Proposed new item

| Item | Product | Target | Status | Owner | Notes |
| --- | --- | --- | --- | --- | --- |
| 4.2 follow-up: routing fairness after the ping-wait cut | Dispatch | Hotfix or 4.3 (engineering to decide) | **Approved by Helen, 24 Oct** | Dispatch PM with Wen Li | Approved: misses scored separately, score decay, and the four starved responders (Vesper, Farlight, The Undertow, Meteor Mite) restored to their pre-4.2 scores. Ping wait back to 90s: decided by the Dispatch PM, Helen to confirm. See routing-fix-proposal.md and score-reset-request.md. |

## Shipped, for reference (from the Releases database)

| Release | Date | What shipped |
| --- | --- | --- |
| 4.2 | 12 Aug 2026 | Change to who gets pinged. Ping wait 90s→60s. Console filters persist (open tickets say they reset after updates). Three defect fixes: duplicate push, capability tag ordering, coverage export time zone. |
| 4.1 | 16 Jun 2026 | Travel-time proximity. Bulk callout. Push delivery reliability. |
| 4.0 | 7 Apr 2026 | Console navigation. Responder profile redesign. Routing override audit log. |

## Briefs to update or mark as shipped

- **Bulk Callout**: the brief says "nobody's picked it up", but it shipped in 4.1. Mark it shipped.
- **Routing Override Audit Log**: the brief says "ready to build", but it shipped in 4.0. Mark it shipped.

## Decisions for Helen

1. Is Availability Confidence still a Q3 commitment, and if so, in which release?
2. Who owns Requisition approval chains on the Supply side, and what's in scope for 4.3?
3. ~~Do we add the 4.2 routing follow-up to 4.3, ahead of new work?~~ Approved 24 Oct. Engineering picks hotfix or 4.3.
