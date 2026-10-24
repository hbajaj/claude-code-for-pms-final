# Dispatch routing — changelog

## Proposed for 4.3 (not yet reviewed by the staff engineer)
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
