# dispatch-routing

The part of Dispatch that decides who gets asked to take a callout,
puts the offer on their phone, and waits for an answer.

- `config.py` — the tuning values. Timeout, weights, points.
- `routing.py` — ranks the available responders for one callout.
- `offer.py` — pushes the offer and waits; walks down the list.
- `history.py` — the recent-acceptance score: taken, turned down and
  missed each score differently (since 24 Oct 2026; see CHANGELOG).
- `availability.py` — who's free, where they are, travel time.

- `test_routing.py` — checks for all of the above. `python test_routing.py`.

**Repo ahead of production:** the capability filter, second round and
ID-keyed score store are built here but not deployed. See CHANGELOG.

Everyone available *with the required capability tags* is on the list
(partial matches only if nobody has all of them), and this code decides
the order.
But we stop at the first yes, so in practice the order also decides
*whether* somebody gets asked: people near the bottom may never be
pinged, and a low score keeps them there. A plain-language description
is in `00-rook/company/how-routing-works.md`.

Owner: the staff engineer who built it. Ask the engineering manager if
she's out.
