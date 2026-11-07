"""Ranking replay: re-run every real callout (29 Jun - 6 Sep 2026) under different routing rules.

Each rule goes live on 12 Aug (the 4.2 release date); before that, everyone runs the pre-4.2 rules,
so all rules start from the same scores. Who gets pinged is decided by the rule; how each responder
answers is drawn from how they actually answered in the database. Averaged over many random runs.

Assumptions (the database has no availability, capability tags or locations):
- Everyone is always available and has the needed tags.
- A responder can be asked about a callout in an area only if they were asked about at least one
  callout in that area in the real data (stand-in for the 45-minute travel horizon).
- Travel time: 5 minutes inside the responder's own area, 20 minutes elsewhere.
- At most 4 responders are pinged per callout (the most the real data ever shows).
- Miss chance depends on the ping wait: each responder's own miss rate at 90s (before 4.2)
  or at 60s (after 4.2), shrunk toward the average so small samples don't dominate.
- Yes/no when they do answer: each responder's own take rate over the whole period, shrunk the same way.
"""
import json, random, sys
from collections import defaultdict, Counter, deque
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')
D = json.load(open(sys.argv[1]))
RUNS = int(sys.argv[2]) if len(sys.argv) > 2 else 300
LOCAL_MIN = float(sys.argv[3]) if len(sys.argv) > 3 else 5
AWAY_MIN = float(sys.argv[4]) if len(sys.argv) > 4 else 20
CALIB = len(sys.argv) > 5 and sys.argv[5] == 'calib'
REL = datetime(2026, 8, 12)
ts = lambda s: datetime.fromisoformat(s.replace('Z', ''))

area_of = {r['name']: r['area'] for r in D['responders']}
NAMES = sorted(area_of)
c_area = {c['callout_number']: c['area'] for c in D['callouts']}
callouts = sorted((ts(c['happened_at']), c['callout_number'], c['area']) for c in D['callouts'])

elig = defaultdict(set)
for p in D['pings']:
    elig[c_area[p['callout_number']]].add(p['responder'])
for n, a in area_of.items():
    elig[a].add(n)

pre, post = defaultdict(Counter), defaultdict(Counter)
for p in D['pings']:
    (pre if ts(p['sent_at']) < REL else post)[p['responder']][p['outcome']] += 1
tot = lambda c: sum(c.values())
pool_miss90 = sum(c['missed'] for c in pre.values()) / sum(tot(c) for c in pre.values())
pool_miss60 = sum(c['missed'] for c in post.values()) / sum(tot(c) for c in post.values())
ans = {n: Counter({k: pre[n][k] + post[n][k] for k in ('taken', 'turned down')}) for n in NAMES}
pool_take = sum(a['taken'] for a in ans.values()) / sum(tot(a) for a in ans.values())
K = 10
MISS = {
    90: {n: (pre[n]['missed'] + K * pool_miss90) / (tot(pre[n]) + K) for n in NAMES},
    60: {n: (post[n]['missed'] + K * pool_miss60) / (tot(post[n]) + K) for n in NAMES},
}
TAKE = {n: (ans[n]['taken'] + K * pool_take) / (tot(ans[n]) + K) for n in NAMES}
PRE_DAYS, POST_DAYS = 44, 26
USUAL = {n: tot(pre[n]) * 7 / PRE_DAYS for n in NAMES}  # usual pings a week, before 4.2

PRE_RULE = dict(wp=0.45, wa=0.40, wait=90, score='points', second=False, load=False)
RULES = {
    'No 4.2 (old rules kept)':        dict(wp=0.45, wa=0.40, wait=90, score='points', second=False, load=False),
    '4.2 as shipped':                 dict(wp=0.60, wa=0.25, wait=60, score='points', second=False, load=False),
    '24 Oct fix':                     dict(wp=0.60, wa=0.25, wait=90, score='fix',    second=False, load=False),
    '24 Oct fix at 60s':              dict(wp=0.60, wa=0.25, wait=60, score='fix',    second=False, load=False),
    'Proposed 4.3':                   dict(wp=0.60, wa=0.25, wait=90, score='share',  second=True,  load=False),
    'Proposed 4.3 + workload':        dict(wp=0.60, wa=0.25, wait=90, score='share',  second=True,  load=True),
    'Proposed 4.3 at 60s':            dict(wp=0.60, wa=0.25, wait=60, score='share',  second=True,  load=False),
}

def prox(n, area):
    return 1 - (LOCAL_MIN if area_of[n] == area else AWAY_MIN) / 45

def run(rule, seed):
    rng = random.Random(seed)
    pts = {n: 0.5 for n in NAMES}; last = {n: None for n in NAMES}; streak = Counter()
    hist = {n: deque(maxlen=30) for n in NAMES}
    week = Counter(); wk = None
    m = dict(pings=Counter(), pre=Counter(), takes=0, misses=0, sent=0, served=0, calls=0, out=0)

    def acc(n, cfg, t):
        if cfg['score'] == 'share':
            h = hist[n]; return (sum(h) + 0.75 * 5) / (len(h) + 5)
        if cfg['score'] == 'fix' and last[n] is not None:
            step = 0.02 * (t - last[n]).total_seconds() / 86400
            pts[n] = max(0.5, pts[n] - step) if pts[n] > 0.5 else min(0.5, pts[n] + step)
        last[n] = t
        return pts[n]

    def record(n, outcome, cfg, t, second_round):
        if outcome == 'taken':
            hist[n].append(1); streak[n] = 0; pts[n] = min(1, pts[n] + 0.08)
        elif outcome == 'turned down':
            hist[n].append(0); streak[n] = 0; pts[n] = max(0, pts[n] - 0.12)
        else:
            if cfg['score'] == 'points':
                pts[n] = max(0, pts[n] - 0.12)          # 4.2 code: a miss is recorded as a turn-down
            elif cfg['score'] == 'fix' and not second_round:
                streak[n] += 1
                if streak[n] >= 3: pts[n] = max(0, pts[n] - 0.12)
            # share: misses are left out of the score

    for t, num, area in callouts:
        cfg = PRE_RULE if t < REL else rule
        live = t >= REL
        w = t.isocalendar()[:2]
        if w != wk: wk = w; week = Counter()
        def prio(n):
            p = cfg['wp'] * prox(n, area) + cfg['wa'] * acc(n, cfg, t) + 0.15
            if cfg['load']: p -= 0.10 * max(0, min(1, week[n] / (USUAL[n] / 7 * (t.weekday() + 1)) - 1))
            return p
        order = sorted(elig[area], key=prio, reverse=True)[:4]
        missed, taken = [], False
        rounds = [order]
        i = 0
        while i < len(rounds):
            for n in rounds[i]:
                week[n] += 1
                u = rng.random()
                out = 'missed' if u < MISS[cfg['wait']][n] else ('taken' if rng.random() < TAKE[n] else 'turned down')
                record(n, out, cfg, t, i > 0)
                if not live: m['pre'][n] += 1
                if live:
                    m['pings'][n] += 1; m['sent'] += 1; m['out'] += area_of[n] != area
                    m['takes'] += out == 'taken'; m['misses'] += out == 'missed'
                if out == 'missed' and i == 0: missed.append(n)
                if out == 'taken': taken = True; break
            if not taken and i == 0 and cfg['second'] and missed: rounds.append(missed)
            if taken: break
            i += 1
        if live:
            m['calls'] += 1; m['served'] += taken
    return m

QUIET = ['Vesper', 'Farlight', 'The Undertow', 'Meteor Mite']
wk = POST_DAYS / 7
actual_post = {n: tot(post[n]) / wk for n in NAMES}

if CALIB:
    # How well does the replay reproduce history? Pre-4.2 rules vs actual before 12 Aug,
    # and 4.2 as shipped vs actual after. Error = average gap in pings a week per responder.
    pre_c, post_c = Counter(), Counter()
    for s in range(RUNS):
        m = run(RULES['4.2 as shipped'], s)
        for n in NAMES:
            pre_c[n] += m['pre'][n] / RUNS / (PRE_DAYS / 7); post_c[n] += m['pings'][n] / RUNS / wk
    act_pre = {n: tot(pre[n]) * 7 / PRE_DAYS for n in NAMES}
    e_pre = sum(abs(pre_c[n] - act_pre[n]) for n in NAMES) / len(NAMES)
    e_post = sum(abs(post_c[n] - actual_post[n]) for n in NAMES) / len(NAMES)
    q = sum(post_c[n] for n in QUIET) / 4
    print(f'local {LOCAL_MIN:>4} away {AWAY_MIN:>4} | error before {e_pre:.2f} | error after {e_post:.2f} | quiet four after 4.2: replay {q:.1f} vs actual {sum(actual_post[n] for n in QUIET)/4:.1f}')
    sys.exit()
print(f'Calibration: miss rate at 90s {pool_miss90:.1%}, at 60s {pool_miss60:.1%}; take rate when answered {pool_take:.1%}; runs per rule: {RUNS}')
print()
rows = {}
for name, rule in RULES.items():
    agg = defaultdict(float); per = Counter()
    for s in range(RUNS):
        m = run(rule, s)
        for k in ('takes', 'misses', 'sent', 'served', 'calls', 'out'): agg[k] += m[k] / RUNS
        for n in NAMES: per[n] += m['pings'][n] / RUNS / wk
    rows[name] = (agg, per)

hdr = ['Rule', 'Quiet four, pings/wk each', 'Lowest responder', 'The Gale', 'Acceptance', 'Misses/wk', 'Unserved', 'Out of area', 'Pings per callout']
print(' | '.join(hdr))
act_acc = sum(post[n]['taken'] for n in NAMES) / sum(tot(post[n]) for n in NAMES)
print(' | '.join(['ACTUAL after 4.2 (database)',
    '/'.join(f'{actual_post[n]:.1f}' for n in QUIET), f'{min(actual_post.values()):.1f}', f'{actual_post["The Gale"]:.1f}',
    f'{act_acc:.0%}', f'{sum(post[n]["missed"] for n in NAMES)/wk:.0f}', '', '', '']))
for name, (agg, per) in rows.items():
    low = min(per, key=per.get)
    print(' | '.join([name, '/'.join(f'{per[n]:.1f}' for n in QUIET), f'{per[low]:.1f} ({low})', f'{per["The Gale"]:.1f}',
        f'{agg["takes"]/agg["sent"]:.0%}', f'{agg["misses"]/wk:.0f}', f'{1-agg["served"]/agg["calls"]:.1%}',
        f'{agg["out"]/agg["sent"]:.0%}', f'{agg["sent"]/agg["calls"]:.2f}']))
print()
print('Per responder, pings a week after 12 Aug (actual vs 4.2 replay vs Proposed 4.3):')
pre_wk = {n: tot(pre[n]) * 7 / PRE_DAYS for n in NAMES}
for n in sorted(NAMES, key=lambda n: actual_post[n]):
    print(f'  {n:18s} before 4.2 {pre_wk[n]:5.1f} | actual {actual_post[n]:5.1f} | 4.2 replay {rows["4.2 as shipped"][1][n]:5.1f} | 24 Oct fix {rows["24 Oct fix"][1][n]:5.1f} | proposed {rows["Proposed 4.3"][1][n]:5.1f}')
