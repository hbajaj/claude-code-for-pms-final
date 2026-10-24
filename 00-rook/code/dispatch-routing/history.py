"""Recent acceptance — a running score of how often somebody has been
taking the callouts we send them.

One of the three inputs to ranking. Sits between 0 and 1. Everyone
starts at NEUTRAL_SCORE when we take them on.
"""

import time

from config import (
    ACCEPTANCE_CREDIT,
    DECLINE_PENALTY,
    MISS_PENALTY,
    MISS_STREAK_LIMIT,
    SCORE_DECAY_PER_DAY,
    SCORE_FLOOR,
    SCORE_CEILING,
)

NEUTRAL_SCORE = 0.5
SECONDS_PER_DAY = 24 * 60 * 60

# name -> (score, when it was last set)
_scores = {}
# name -> how many pings in a row they've missed
_miss_streaks = {}


def recent_acceptance(responder):
    """This responder's score right now. Read by routing.score()."""
    score, updated_at = _scores.get(responder.name, (NEUTRAL_SCORE, None))
    if updated_at is None:
        return score
    return _decayed(score, time.time() - updated_at)


def record_accepted(responder):
    """They took the callout. Score goes up."""
    _miss_streaks[responder.name] = 0
    _set(responder, recent_acceptance(responder) + ACCEPTANCE_CREDIT)


def record_declined(responder):
    """They turned it down. Score goes down."""
    _miss_streaks[responder.name] = 0
    _set(responder, recent_acceptance(responder) - DECLINE_PENALTY)


def record_missed(responder):
    """Nobody answered before the ping wait ran out.

    Not the same as a no: they may have been reaching for the phone.
    Only a run of misses costs anything.
    """
    streak = _miss_streaks.get(responder.name, 0) + 1
    _miss_streaks[responder.name] = streak
    if streak >= MISS_STREAK_LIMIT:
        _set(responder, recent_acceptance(responder) - MISS_PENALTY)


def reset(names=None):
    """Put responders back to NEUTRAL_SCORE. Everyone if names is None.

    For the one-off repair after 4.2, when misses were penalised as
    turn-downs.
    """
    for name in list(_scores) if names is None else names:
        _scores.pop(name, None)
        _miss_streaks.pop(name, None)


def _decayed(score, seconds):
    """Ease a score back toward NEUTRAL_SCORE with time."""
    step = SCORE_DECAY_PER_DAY * seconds / SECONDS_PER_DAY
    if score > NEUTRAL_SCORE:
        return max(NEUTRAL_SCORE, score - step)
    return min(NEUTRAL_SCORE, score + step)


def _set(responder, value):
    _scores[responder.name] = (
        max(SCORE_FLOOR, min(SCORE_CEILING, value)),
        time.time(),
    )
