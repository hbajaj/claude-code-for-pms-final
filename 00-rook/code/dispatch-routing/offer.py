"""Putting the offer on somebody's phone and waiting for an answer.

We work down the ranked list one at a time. Each responder gets the
callout and a fixed window to answer. If they take it we're done. If
they don't, we move on.
"""

import time

from config import OFFER_TIMEOUT_SECONDS, SECOND_ROUND_FOR_MISSED
import history
import routing

TAKEN = "taken"
TURNED_DOWN = "turned down"
MISSED = "missed"


def dispatch(callout):
    """Offer a callout down the ranked list until somebody takes it.

    If nobody takes it, offer it once more to anyone who missed it (a
    miss isn't a no), in the same order. Returns the responder who took
    it, or None if nobody did.
    """
    ranked, partial_match = routing.candidates_for_callout(callout)
    if partial_match:
        flag_partial_match(callout)

    missed = []
    for responder in ranked:
        answer = offer_to(responder, callout)
        if answer == TAKEN:
            history.record_accepted(responder)
            return responder
        if answer == TURNED_DOWN:
            history.record_declined(responder)
        else:
            history.record_missed(responder)
            missed.append(responder)

    if SECOND_ROUND_FOR_MISSED:
        for responder in missed:
            answer = offer_to(responder, callout)
            if answer == TAKEN:
                history.record_accepted(responder)
                return responder
            if answer == TURNED_DOWN:
                history.record_declined(responder)
            # A second miss on the same callout isn't scored again.
    return None


def flag_partial_match(callout):
    """Tell the handler this callout is going to responders who don't
    have every capability tag it needs."""
    ...


def offer_to(responder, callout):
    """Push the callout to a responder's phone and wait for a tap.

    Returns TAKEN, TURNED_DOWN or MISSED. Either of the last two sends
    the callout down the list, but they score differently: a turn-down
    is a no, a miss may just be someone who didn't reach the phone.
    """
    push_to_device(responder, callout)
    deadline = time.time() + OFFER_TIMEOUT_SECONDS
    while time.time() < deadline:
        answer = poll_device(responder, callout)
        if answer is not None:
            return answer
    withdraw_from_device(responder, callout)
    return MISSED


def push_to_device(responder, callout):
    """Send the offer to whatever device they're signed in on."""
    ...


def poll_device(responder, callout):
    """Has this responder answered yet? None if they haven't."""
    ...


def withdraw_from_device(responder, callout):
    """Take the offer off their phone. It's gone to somebody else."""
    ...
