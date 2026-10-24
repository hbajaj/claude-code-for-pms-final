"""Ranking available responders for a single callout.

Given a callout and everyone who's currently free, work out the order
we should ask them in. Top of the list gets asked first; if they don't
take it, we move down.
"""

from config import (
    WEIGHT_PROXIMITY,
    WEIGHT_RECENT_ACCEPTANCE,
    WEIGHT_CAPABILITY_MATCH,
    PROXIMITY_HORIZON_MINUTES,
    ALLOW_PARTIAL_MATCH_FALLBACK,
)
import availability
import history


def rank_for_callout(callout):
    """The responders to offer this callout to, best match first."""
    ranked, _ = candidates_for_callout(callout)
    return ranked


def candidates_for_callout(callout):
    """Who to offer this callout to, best match first, and whether
    they're only a partial match.

    Only available responders with every required capability tag are
    ranked. If there are none, fall back to those with some of the tags
    (partial match) so the handler can decide; responders with none of
    them are never offered it. An empty list means a coverage gap.

    Returns (ranked responders, partial_match).
    """
    available = availability.available_for(callout.region, callout.at)
    full = [r for r in available if capability_score(r, callout) == 1.0]
    if full:
        return _ranked(full, callout), False
    if ALLOW_PARTIAL_MATCH_FALLBACK:
        partial = [r for r in available if capability_score(r, callout) > 0.0]
        if partial:
            return _ranked(partial, callout), True
    return [], False


def _ranked(candidates, callout):
    scored = [(score(r, callout), r) for r in candidates]
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [responder for _, responder in scored]


def score(responder, callout):
    """How good a match this responder is for this callout.

    Higher is better. Three parts, each weighted:
      - how fast they can get there
      - how often they've been taking callouts lately
      - whether they can do this kind of work at all
    """
    return (
        WEIGHT_PROXIMITY * proximity_score(responder, callout)
        + WEIGHT_RECENT_ACCEPTANCE * history.recent_acceptance(responder)
        + WEIGHT_CAPABILITY_MATCH * capability_score(responder, callout)
    )


def proximity_score(responder, callout):
    """1.0 if they're practically there already, falling off with
    travel time, 0.0 past the horizon.

    Travel time, not straight-line distance. That changed in 4.1.
    """
    minutes = availability.travel_time_minutes(responder, callout.location)
    if minutes >= PROXIMITY_HORIZON_MINUTES:
        return 0.0
    return 1.0 - (minutes / PROXIMITY_HORIZON_MINUTES)


def capability_score(responder, callout):
    """1.0 if they can do everything this callout needs, 0.0 if they
    can't do any of it, somewhere in between otherwise.
    """
    needed = set(callout.required_capabilities)
    if not needed:
        return 1.0
    matched = needed & set(responder.capabilities)
    return len(matched) / len(needed)
