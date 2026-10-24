"""Tuning values for callout routing.

Everything in here changes who gets asked to take a job, so don't
change anything in here without telling the engineering manager.
"""

# How long a callout offer stays on a responder's phone before we give
# up on them and move to the next person on the list.
# 4.2 cut this to 60; misses went from 1-3% of pings to 13-22%.
# Back to 90 on 24 Oct 2026, alongside the miss-scoring fix.
OFFER_TIMEOUT_SECONDS = 90

# How much each input counts when we rank who to ask first. These are
# relative to each other; they don't need to add up to anything.
WEIGHT_PROXIMITY = 0.60              # was 0.45 until 4.2
WEIGHT_RECENT_ACCEPTANCE = 0.25      # was 0.40 until 4.2
WEIGHT_CAPABILITY_MATCH = 0.15       # unchanged since 4.0

# Points on and off the recent-acceptance score.
ACCEPTANCE_CREDIT = 0.08
DECLINE_PENALTY = 0.12               # a "no" from the responder

# Missed pings (nobody answered in time) are not the same as a "no".
# Until 24 Oct 2026 they cost the same as a
# turn-down, which sank responders who
# were simply slow to the phone after the 60s cut. Now a miss is free
# unless it's part of a run: from the MISS_STREAK_LIMIT-th miss in a row,
# each further miss costs MISS_PENALTY. Any answer (yes or no) resets the run.
MISS_PENALTY = 0.12
MISS_STREAK_LIMIT = 3

# Scores drift back toward neutral on their own, this much per day, so a
# bad stretch doesn't stick forever to someone who stops being asked.
SCORE_DECAY_PER_DAY = 0.02

# The score never goes outside these.
SCORE_FLOOR = 0.0
SCORE_CEILING = 1.0

# Anyone further out than this scores zero on proximity.
PROXIMITY_HORIZON_MINUTES = 45

# Capability is a filter, not just part of the score: only responders
# with every tag a callout needs are offered it. If nobody available has
# all of them, fall back to those with some of them, and flag the callout
# to the handler as a partial match. Nobody with none of them is offered it.
ALLOW_PARTIAL_MATCH_FALLBACK = True

# When everyone on the list has missed or turned the callout down, offer
# it once more to those who missed (never to those who said no) before
# giving up on it.
SECOND_ROUND_FOR_MISSED = True

# Where recent-acceptance scores are kept, so they survive a restart.
# Keyed by responder ID, not name.
SCORE_STORE_PATH = "routing_scores.json"
