"""Recent acceptance — a running score of how often somebody has been
taking the callouts we send them.

One of the three inputs to ranking. Sits between 0 and 1. Everyone
starts at NEUTRAL_SCORE when we take them on.

Scores are keyed by responder ID, not name, and written to
config.SCORE_STORE_PATH so they survive a restart or deploy.
"""

import json
import os
import tempfile
import time

import config
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

# responder id -> {"score", "updated_at", "miss_streak"}; loaded on first use
_records = None


def recent_acceptance(responder):
    """This responder's score right now. Read by routing.score()."""
    record = _load().get(_key(responder))
    if record is None:
        return NEUTRAL_SCORE
    return _decayed(record["score"], time.time() - record["updated_at"])


def record_accepted(responder):
    """They took the callout. Score goes up."""
    _set(responder, recent_acceptance(responder) + ACCEPTANCE_CREDIT, miss_streak=0)


def record_declined(responder):
    """They turned it down. Score goes down."""
    _set(responder, recent_acceptance(responder) - DECLINE_PENALTY, miss_streak=0)


def record_missed(responder):
    """Nobody answered before the ping wait ran out.

    Not the same as a no: they may have been reaching for the phone.
    Only a run of misses costs anything.
    """
    record = _load().get(_key(responder), {})
    streak = record.get("miss_streak", 0) + 1
    score = recent_acceptance(responder)
    if streak >= MISS_STREAK_LIMIT:
        score -= MISS_PENALTY
    _set(responder, score, miss_streak=streak)


def reset(ids=None):
    """Put responders back to NEUTRAL_SCORE, by responder ID. Everyone if
    ids is None."""
    records = _load()
    for key in list(records) if ids is None else [str(i) for i in ids]:
        records.pop(key, None)
    _save()


def restore(scores):
    """Set responders' scores directly, from a {responder id: score}
    mapping.

    For putting responders back to where they were before a defect
    pushed them down, rather than to NEUTRAL_SCORE, which can still
    leave them below everyone they compete with.
    """
    records = _load()
    for responder_id, value in scores.items():
        records[str(responder_id)] = _record(value, miss_streak=0)
    _save()


def import_legacy(legacy_scores, ids_by_name):
    """One-off move from the old in-memory scores, keyed by name, to
    this store, keyed by ID. Run once when this version is deployed, or
    everyone (including restored responders) falls back to neutral.

    legacy_scores: the old _scores dict, {name: (score, updated_at)}.
    ids_by_name: {name: responder id}. Names missing from it are
    returned so they can be checked by hand, not guessed.
    """
    records = _load()
    unmatched = []
    for name, (score, updated_at) in legacy_scores.items():
        if name not in ids_by_name:
            unmatched.append(name)
            continue
        record = _record(score, miss_streak=0)
        record["updated_at"] = updated_at
        records[str(ids_by_name[name])] = record
    _save()
    return unmatched


def _key(responder):
    return str(responder.id)


def _record(value, miss_streak):
    return {
        "score": max(SCORE_FLOOR, min(SCORE_CEILING, value)),
        "updated_at": time.time(),
        "miss_streak": miss_streak,
    }


def _set(responder, value, miss_streak):
    _load()[_key(responder)] = _record(value, miss_streak)
    _save()


def _decayed(score, seconds):
    """Ease a score back toward NEUTRAL_SCORE with time."""
    step = SCORE_DECAY_PER_DAY * seconds / SECONDS_PER_DAY
    if score > NEUTRAL_SCORE:
        return max(NEUTRAL_SCORE, score - step)
    return min(NEUTRAL_SCORE, score + step)


def _load():
    global _records
    if _records is None:
        try:
            with open(config.SCORE_STORE_PATH) as f:
                _records = json.load(f)
        except FileNotFoundError:
            _records = {}
    return _records


def _save():
    """Write all scores, replacing the file in one step so a crash
    mid-write can't leave it half-written."""
    directory = os.path.dirname(os.path.abspath(config.SCORE_STORE_PATH))
    fd, tmp_path = tempfile.mkstemp(dir=directory, suffix=".tmp")
    with os.fdopen(fd, "w") as f:
        json.dump(_records, f)
    os.replace(tmp_path, config.SCORE_STORE_PATH)
