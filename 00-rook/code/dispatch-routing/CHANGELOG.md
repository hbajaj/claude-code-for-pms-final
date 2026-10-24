# Dispatch routing — changelog

## Routing v2, "Now" items — built and tested, NOT deployed (needs staff engineer review and Director of Product OK)
- Capability is a filter: only responders with every required tag are
  offered a callout. If none, fall back to partial matches and flag the
  callout to the handler (`offer.flag_partial_match`, stub). Nobody with
  none of the tags is offered it; an empty list is a coverage gap.
- Second round: if nobody takes it, offer it once more to anyone who
  missed (never to those who said no). A second miss isn't scored again.
  Widening to neighbouring areas is not built: there's no area map here.
- Scores stored by responder ID in `SCORE_STORE_PATH` (JSON, written
  atomically), so they survive restarts and same-name responders don't
  collide. `reset()`/`restore()` now take IDs.
- **Deploy step:** run `history.import_legacy(old _scores, ids_by_name)`
  once, or every score (including the four restored on 24 Oct) falls
  back to neutral. It returns any names it couldn't match.
- `test_routing.py`: 14 checks, run with `python test_routing.py`.

## Routing fix — shipped 24 Oct 2026
Approved by the Director of Product and the staff engineer. Scores for Vesper,
Meteor Mite, Farlight and The Undertow restored to pre-4.2 values after deploy.
- Missed pings no longer score as turn-downs. A miss is free unless it is
  the 3rd or later in a row; any answer resets the run.
- Recent-acceptance scores drift back toward neutral (0.02 a day), so a
  responder who stops being asked can recover.
- `history.reset()` for a one-off reset of responders penalised by 4.2.
- Callout offer timeout 60s -> 90s (back to pre-4.2). At 60s, missed
  pings went from 1-3% to 13-22%.

## 4.2 — 12 Aug 2026
- Rebalanced ranking weights: proximity up, recent acceptance down.
- Callout offer timeout 90s -> 60s.
- Console filter persistence (not in this service).

## 4.1 — 16 Jun 2026
- Proximity now uses a travel-time estimate instead of straight-line
  distance.
- Bulk callout.
- Mobile push reliability.

## 4.0 — 7 Apr 2026
- Console navigation.
- Responder profile redesign.
- Routing override audit log.
