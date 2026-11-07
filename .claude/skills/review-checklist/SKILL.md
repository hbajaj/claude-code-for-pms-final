---
name: review-checklist
description: Reviews a product brief against four checks — names an owner, says how we'll know it worked, keeps the same scope start to finish, and explains the problem before the fix — with every verdict backed by a quote that a script verifies against the brief. Use it when the student points at a brief, a folder of briefs or pasted brief text and says "review this brief", "run the review checklist", "check this brief", "is this brief ready", "are my reviews up to date" or "/review-checklist <path>".
---

# Review checklist

You're reviewing product briefs for a PM. For each brief, say whether it passes four checks, back every answer with the brief's own words, and prove those words are really there. You don't rewrite the brief and you don't judge whether the idea is good — only whether it's fit to hand to someone else.

`<skill>` below means this skill's folder (the folder this file is in). Run Python as `python -I -X utf8`.

## 0. Start with what's out of date

Run `python -I -X utf8 <skill>/scripts/validate.py --status` first. If a brief the student has reviewed before says **CHANGED since review**, tell them in one line and offer to re-run it. If they asked "are my reviews up to date?", that line is the whole answer.

## 1. Find the brief(s)

- A path (file or folder), a name ("the canvas brief") or pasted text. If they name one, search this repository for it. Still unclear: ask "Which brief should I check? Give me the file or folder, or paste it."
- A folder means every brief in it (`.md`, `.txt`, `.docx`, `.dc.html`), alphabetical order.
- **Pasted text:** save it to a file in the scratchpad directory and treat that file as the brief. Never save someone else's brief into the course folder or log it. Use the author name the student gives you; if they correct it, use the correction.
- **Links outside this folder** (someone else's GitHub, a website): the course CLAUDE.md says read only within this directory. Ask the student to paste the text instead, or get their explicit OK to fetch it once.
- Read each brief in full before judging. For `.dc.html` canvas files, read the text with `validate.py --text <file>`. For `.docx`, `pandoc file.docx -t plain` into the scratchpad.
- Only read. Never edit, move or rename a brief unless the student asks you to fix it.

## 2. Run the four checks

Each check ends in **pass** or **flag**. Be strict: if you have to infer it, it isn't there. Before deciding a borderline case, read `<skill>/references/examples.md` and judge it the same way.

- **Owner named** — pass when a person or specific team is named as accountable for the brief. Flag a role with no name ("the Dispatch PM", "TBD"), people who only asked, were consulted or are being asked for something, an owner of only one part, or an owner who has left (Priya Raghunathan, gone 21 Aug 2026).
- **Success measure** — pass when it says how we'd know after launch that it worked: a measurable signal, ideally with baseline, target, time frame and who checks. Flag feature lists, vague words ("improve"), or validation that only looks at past data. Missing date or checker: pass, with a note.
- **Scope stays bounded** — pass when what it opens with is the same size as what it ends with. Flag when new features, users, systems or problems appear that the opening and the ask didn't mention. Items under "Later", "Not in scope" or similar don't count.
- **Problem before fix** — pass when who has the problem and what goes wrong come before the solution. Flag when it opens with the feature or screen.

## 3. Write the result as evidence, then validate it

Write the result as JSON to the scratchpad (e.g. `review-<name>.json`):

```json
{"title": "brief.md",
 "checks": {
   "owner":         {"verdict": "pass", "who": "Himanshu Bajaj",
                     "evidence": [{"quote": "Owner: Himanshu Bajaj", "where": "header"}]},
   "success":       {"verdict": "pass", "note": "No date to check by.",
                     "evidence": [{"quote": "Both back to ~11–13", "where": "How we'll know it worked"}]},
   "scope":         {"verdict": "flag", "note": "Opens as eight small changes; a new 4.3 score appears later that the ask doesn't cover.",
                     "evidence": [{"quote": "This brief proposes eight small changes", "where": "In short"},
                                  {"quote": "4.3, date to be set by Wen and Marcus", "where": "How the score works"}]},
   "problem_first": {"verdict": "pass",
                     "evidence": [{"quote": "Nobody could see why", "where": "In short, first bullet"}]}}}
```

Rules: every check has at least one quote copied **word for word** from the brief (short is fine, 4+ characters). A flag about something missing quotes the place it should have been (e.g. the byline). Every flag has a `note`.

Then run:

`python -I -X utf8 <skill>/scripts/validate.py <brief> <review.json> --log`

- Leave out `--log` for pasted or outside briefs.
- `VALID=no` lists what's wrong (usually a quote that isn't in the brief). **Fix the JSON — re-read the brief, correct the quote or change the verdict — and run it again.** Never show the student a report that hasn't come back `VALID=yes`.
- `VALID=yes` prints the report. `LOGGED=yes` means the brief's fingerprint is saved, so step 0 can spot later edits.

## 4. Check twins are in sync

Some briefs exist twice — e.g. `05-super-speed/brief.md` and its canvas version `05-super-speed/canvas-brief.dc.html`. When you review one and the other is in the same folder, review both and compare: same four verdicts, same owner, same ask, same success targets. List every difference in one line each under **Out of sync**. Don't fix them unless asked.

## 5. Report

Show the validated report block for each brief (the script's output, in a code block), then one line: `<n> briefs checked, <n> flagged, <n> flags in total.` Under it:

- For each flag, the smallest change that would turn it into a pass.
- Any **close call** (where `examples.md` didn't settle it) — say which way you went and why, in one line.
- Any **Out of sync** lines from step 4.

Keep the tone plain: say what's missing, not what's wrong with the author. Only save a report file if the student asks (then save it next to the brief as `review-checklist-output.txt`).
