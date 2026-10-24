"""Checks for routing, offers and the recent-acceptance score.

Run from this folder with:  python test_routing.py
Uses a temporary score file, and stands in for the phone and
availability parts, which aren't in this repo.
"""

import os
import tempfile
import time
import types

import config

_tmp = tempfile.mkdtemp()
config.SCORE_STORE_PATH = os.path.join(_tmp, "scores.json")

import availability  # noqa: E402
import history  # noqa: E402
import offer  # noqa: E402
import routing  # noqa: E402


def responder(rid, name, minutes, tags):
    return types.SimpleNamespace(id=rid, name=name, minutes=minutes, capabilities=tags)


def callout(needs):
    return types.SimpleNamespace(region="Eastgate", at=0, location=None, required_capabilities=needs)


def use_available(*people):
    availability.available_for = lambda region, at: list(people)
    availability.travel_time_minutes = lambda r, location: r.minutes


def fresh_scores():
    history._records = None
    if os.path.exists(config.SCORE_STORE_PATH):
        os.remove(config.SCORE_STORE_PATH)


def close(a, b):
    return abs(a - b) < 1e-3


# ---- capability filter -------------------------------------------------

def test_responder_missing_a_tag_is_not_offered_when_someone_has_all():
    fresh_scores()
    near = responder(1, "Near", 5, [])
    far = responder(2, "Far", 30, ["hazmat-tolerant"])
    use_available(near, far)
    ranked, partial = routing.candidates_for_callout(callout(["hazmat-tolerant"]))
    assert [r.name for r in ranked] == ["Far"], [r.name for r in ranked]
    assert partial is False


def test_falls_back_to_partial_match_and_flags_it():
    fresh_scores()
    some = responder(1, "Some", 10, ["flight"])
    none = responder(2, "None", 5, [])
    use_available(some, none)
    ranked, partial = routing.candidates_for_callout(callout(["flight", "aquatic"]))
    assert [r.name for r in ranked] == ["Some"], [r.name for r in ranked]
    assert partial is True


def test_nobody_with_any_tag_is_a_coverage_gap():
    fresh_scores()
    use_available(responder(1, "A", 5, []), responder(2, "B", 8, ["flight"]))
    ranked, partial = routing.candidates_for_callout(callout(["aquatic"]))
    assert ranked == [] and partial is False


def test_no_tags_needed_ranks_everyone_by_score():
    fresh_scores()
    use_available(responder(1, "Far", 30, []), responder(2, "Near", 5, []))
    assert [r.name for r in routing.rank_for_callout(callout([]))] == ["Near", "Far"]


# ---- second round for missed pings -------------------------------------

def run_dispatch(people, answers, needs=None):
    """answers: {name: [first-round answer, second-round answer]}"""
    use_available(*people)
    calls = []
    flagged = []

    def fake_offer(r, c):
        n = sum(1 for name in calls if name == r.name)
        calls.append(r.name)
        return answers[r.name][n]

    offer.offer_to = fake_offer
    offer.flag_partial_match = lambda c: flagged.append(c)
    taken_by = offer.dispatch(callout(needs or []))
    return taken_by, calls, flagged


def test_missed_responder_gets_a_second_chance():
    fresh_scores()
    a, b = responder(1, "A", 5, []), responder(2, "B", 10, [])
    taken_by, calls, _ = run_dispatch(
        [a, b], {"A": [offer.MISSED, offer.TAKEN], "B": [offer.TURNED_DOWN]})
    assert taken_by.name == "A"
    assert calls == ["A", "B", "A"], calls


def test_responder_who_said_no_is_not_asked_again():
    fresh_scores()
    a, b = responder(1, "A", 5, []), responder(2, "B", 10, [])
    taken_by, calls, _ = run_dispatch(
        [a, b], {"A": [offer.TURNED_DOWN], "B": [offer.MISSED, offer.MISSED]})
    assert taken_by is None
    assert calls == ["A", "B", "B"], calls


def test_second_miss_on_same_callout_is_not_scored_twice():
    fresh_scores()
    a = responder(1, "A", 5, [])
    run_dispatch([a], {"A": [offer.MISSED, offer.MISSED]})
    assert history._load()["1"]["miss_streak"] == 1


def test_partial_match_is_flagged_to_handler():
    fresh_scores()
    a = responder(1, "A", 5, ["flight"])
    _, _, flagged = run_dispatch([a], {"A": [offer.TAKEN]}, needs=["flight", "aquatic"])
    assert len(flagged) == 1


# ---- scores: miss rule, recovery, stored by ID -------------------------

def test_miss_rule():
    fresh_scores()
    a = responder(1, "A", 5, [])
    history.record_missed(a); history.record_missed(a)
    assert close(history.recent_acceptance(a), 0.5), "first two misses free"
    history.record_missed(a)
    assert close(history.recent_acceptance(a), 0.38), "third in a row costs"
    history.record_declined(a)
    assert close(history.recent_acceptance(a), 0.26)
    history.record_missed(a)
    assert close(history.recent_acceptance(a), 0.26), "an answer resets the run"
    history.record_accepted(a)
    assert close(history.recent_acceptance(a), 0.34)


def test_scores_recover_toward_neutral():
    fresh_scores()
    history.restore({1: 0.2, 2: 0.9})
    records = history._load()
    records["1"]["updated_at"] -= 5 * 86400
    records["2"]["updated_at"] -= 5 * 86400
    assert close(history.recent_acceptance(responder(1, "A", 0, [])), 0.3)
    assert close(history.recent_acceptance(responder(2, "B", 0, [])), 0.8)
    records["1"]["updated_at"] -= 60 * 86400
    assert close(history.recent_acceptance(responder(1, "A", 0, [])), 0.5), "stops at neutral"


def test_scores_survive_a_restart():
    fresh_scores()
    a = responder(7, "Vesper", 5, [])
    history.restore({7: 0.96})
    history._records = None  # as if the process restarted
    assert close(history.recent_acceptance(a), 0.96)


def test_two_responders_with_the_same_name_do_not_share_a_score():
    fresh_scores()
    one, two = responder(1, "Halfmoon", 5, []), responder(2, "Halfmoon", 5, [])
    history.record_declined(one)
    assert close(history.recent_acceptance(one), 0.38)
    assert close(history.recent_acceptance(two), 0.5)


def test_reset_and_restore_by_id():
    fresh_scores()
    history.restore({1: 0.96, 2: 1.4})
    assert close(history.recent_acceptance(responder(2, "B", 0, [])), 1.0), "clamped"
    history.reset([1])
    assert close(history.recent_acceptance(responder(1, "A", 0, [])), 0.5)
    history.reset()
    assert history._load() == {}


def test_import_from_old_name_keyed_scores():
    fresh_scores()
    now = time.time()
    legacy = {"Vesper": (0.96, now), "Meteor Mite": (1.0, now), "Unknown": (0.3, now)}
    unmatched = history.import_legacy(legacy, {"Vesper": 11, "Meteor Mite": 12})
    assert unmatched == ["Unknown"], unmatched
    assert close(history.recent_acceptance(responder(11, "Vesper", 0, [])), 0.96)
    assert close(history.recent_acceptance(responder(12, "Meteor Mite", 0, [])), 1.0)


if __name__ == "__main__":
    tests = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_")]
    failed = 0
    for name, fn in tests:
        try:
            fn()
            print("ok    ", name)
        except AssertionError as e:
            failed += 1
            print("FAILED", name, "-", e)
    print(f"\n{len(tests) - failed} passed, {failed} failed")
    raise SystemExit(1 if failed else 0)
