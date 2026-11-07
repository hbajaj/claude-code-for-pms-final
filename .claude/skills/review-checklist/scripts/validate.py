"""Validate a review-checklist result against the brief it reviews.

Usage:
  python -I -X utf8 validate.py <brief> <review.json> [--log]
      Checks that the review is complete and that every quote really appears
      in the brief. Prints the report. With --log, records the result (and a
      fingerprint of the brief) in review-log.json so later runs can tell
      whether the brief has changed since it was reviewed.
  python -I -X utf8 validate.py --status
      Lists every logged brief and whether it changed since its last review.
  python -I -X utf8 validate.py --text <brief>
      Prints the brief's readable text (handy for .dc.html canvas files).

review.json shape:
  {"title": "brief.md",
   "checks": {
     "owner":         {"verdict": "pass"|"flag", "who": "Sofia", "note": "...",
                       "evidence": [{"quote": "...", "where": "header"}]},
     "success":       {...}, "scope": {...}, "problem_first": {...}}}
Every check needs at least one quote copied word for word from the brief.
For a flag about something missing, quote the place where it should have been.
"""
import hashlib, html, json, os, re, sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(os.path.dirname(HERE), "review-log.json")
CHECKS = [("owner", "owner named"), ("success", "success measure"),
          ("scope", "scope stays bounded"), ("problem_first", "problem stated before fix")]


def read_text(path):
    raw = open(path, encoding="utf-8").read()
    if path.lower().endswith((".html", ".htm")):
        raw = re.sub(r"<(script|style)[\s\S]*?</\1>", " ", raw)
        # canvas files keep table/card rows in script data: keep quoted strings from it
        data = " ".join(re.findall(r"'([^'\n]{12,})'", open(path, encoding="utf-8").read()))
        raw = re.sub(r"<[^>]+>", " ", raw) + " " + data
        raw = html.unescape(raw)
    return raw


def norm(s):
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("—", "-").replace("–", "-").replace("−", "-").replace(" ", " ")
    s = re.sub(r"[*_`#|]", " ", s)  # markdown emphasis, headings, table bars
    return re.sub(r"\s+", " ", s).strip().lower()


def fingerprint(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()[:16]


def load_log():
    try:
        return json.load(open(LOG, encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def key_for(path):
    try:
        return os.path.relpath(os.path.abspath(path), os.getcwd()).replace("\\", "/")
    except ValueError:
        return os.path.abspath(path)


def validate(brief, review):
    text = norm(read_text(brief))
    problems = []
    checks = review.get("checks", {})
    for key, label in CHECKS:
        c = checks.get(key)
        if not c:
            problems.append(f"{label}: missing from the review")
            continue
        if c.get("verdict") not in ("pass", "flag"):
            problems.append(f"{label}: verdict must be 'pass' or 'flag'")
        ev = c.get("evidence") or []
        if not ev:
            problems.append(f"{label}: no evidence quoted")
        for e in ev:
            q = norm(e.get("quote", ""))
            if len(q) < 4:
                problems.append(f"{label}: quote too short to check")
            elif q not in text:
                problems.append(f'{label}: quote not found in brief: "{e.get("quote")}"')
        if c.get("verdict") == "flag" and not c.get("note"):
            problems.append(f"{label}: a flag needs a note saying what's missing")
    return problems


def render(review):
    out = [review.get("title", "brief")]
    flags = []
    for key, label in CHECKS:
        c = review["checks"][key]
        dots = "." * max(3, 31 - len(label))
        if c["verdict"] == "pass":
            extra = f" ({c['who']})" if key == "owner" and c.get("who") else ""
            out.append(f"  {label} {dots} yes{extra}")
        else:
            out.append(f"  {label} {dots} NO - flagged")
            flags.append(c)
    if flags:
        out.append(f"  -> {len(flags)} flag{'s' if len(flags) > 1 else ''}:")
        for c in flags:
            q = c["evidence"][0]
            out.append(f"     - {c['note']} (\"{q['quote']}\", {q.get('where', 'brief')})")
    else:
        out.append("  -> passes all four.")
    notes = [(l, review["checks"][k]["note"]) for k, l in CHECKS
             if review["checks"][k]["verdict"] == "pass" and review["checks"][k].get("note")]
    for l, n in notes:
        out.append(f"     note ({l}): {n}")
    return "\n".join(out), len(flags)


def status():
    log = load_log()
    if not log:
        print("No reviews logged yet.")
        return
    for path, e in sorted(log.items()):
        if not os.path.exists(path):
            state = "MISSING (file moved or deleted)"
        elif fingerprint(path) != e["fingerprint"]:
            state = "CHANGED since review - re-run"
        else:
            state = "in sync"
        print(f"{path}: {e['flags']} flag(s), reviewed {e['reviewed_at']} - {state}")


def main(argv):
    if argv[:1] == ["--status"]:
        return status()
    if argv[:1] == ["--text"]:
        print(read_text(argv[1]))
        return
    if len(argv) < 2:
        print(__doc__)
        sys.exit(2)
    brief, review_path = argv[0], argv[1]
    review = json.load(open(review_path, encoding="utf-8"))
    problems = validate(brief, review)
    if problems:
        print("VALID=no")
        for p in problems:
            print("  - " + p)
        sys.exit(1)
    report, nflags = render(review)
    print("VALID=yes")
    print(report)
    if "--log" in argv:
        log = load_log()
        log[key_for(brief)] = {
            "fingerprint": fingerprint(brief),
            "reviewed_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
            "flags": nflags,
            "verdicts": {k: review["checks"][k]["verdict"] for k, _ in CHECKS},
        }
        json.dump(log, open(LOG, "w", encoding="utf-8"), indent=2)
        print("LOGGED=yes")


if __name__ == "__main__":
    main(sys.argv[1:])
