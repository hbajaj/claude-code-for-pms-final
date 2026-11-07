---
name: review-checklist
description: Reviews a product brief against four checks — names an owner, says how we'll know it worked, keeps the same scope start to finish, and explains the problem before the fix. Use it when the student points at a brief or a folder of briefs and says "review this brief", "run the review checklist", "check this brief", "is this brief ready" or "/review-checklist <path>".
---

# Review checklist

You're reviewing one or more product briefs for a PM. The job is to say, for each brief, whether it passes four checks, and to back every answer with the brief's own words. You don't rewrite the brief and you don't judge whether the idea is good — only whether the brief is fit to hand to someone else.

## 1. Find the brief(s)

- The student gives a path (a file or a folder), or names a brief ("the bulk callout brief"). If they name one, search this repository for it. If it's still unclear, ask one short question: "Which brief should I check? Give me the file or folder."
- A folder means every brief in it (`.md`, `.txt`, `.docx`). Check them in alphabetical order.
- Read each brief in full before judging it. For `.docx`, extract the text first (the docx skill, or `pandoc file.docx -t plain`).
- Only read. Never edit, move or rename a brief.

## 2. Run the four checks

Each check ends in **yes** or **NO — flagged**. Be strict: if you have to infer it, it isn't there.

### Owner named
Pass when the brief names a person or a specific team who is accountable for it (e.g. "Owner: Sofia", "Marcus's team builds this").
Flag when:
- nobody is named, or the owner is a role with no one in it ("a PM", "TBD", "whoever picks this up");
- it only names people who asked for it, were consulted or will be affected;
- it names an owner who has left (for Rook: Priya Raghunathan, gone 21 Aug 2026) — say so.

### Success measure
Pass when the brief says how we'll know it worked: a measurable signal, ideally with a baseline, a target and a time frame (e.g. "acceptance back above 75% within two weeks").
Flag when it only lists what will be built or logged, uses vague words ("improve", "better experience", "faster") with nothing to measure, or names a metric with no direction or target. If a metric is named but has no baseline or date, pass it and mention that in the note.

### Scope stays bounded
Pass when the thing the brief opens with is the same size as the thing it ends with.
Flag when the ask grows partway through: new features, users, systems or "while we're at it" additions that the opening didn't promise, or a "that's the whole ask" that is followed by more asks. Clearly labelled "later" or "out of scope" items don't count against it. Quote the opening ask and the first point where it grows.

### Problem before fix
Pass when the brief explains who has the problem and what goes wrong for them before it describes the solution.
Flag when it opens with the feature, screen or design and the problem only appears later (or not at all). Say where the problem first shows up.

## 3. Report

Print one block per brief, then a one-line total. Use this layout:

```
<file name>
  owner named ................... yes (Sofia)
  success measure ............... yes
  scope stays bounded ........... NO — flagged
  problem stated before fix ..... yes
  -> 1 flag: scope grows mid-document. Opens as one approval step
     ("that's the whole ask"); by the next paragraph it has picked up
     a cross-site dashboard and a spreadsheet replacement.
```

- On a pass for the owner, put who in brackets.
- For every flag, write one or two plain sentences under `->` with a short quote or a pointer to where in the brief it happens. With no flags, write `-> passes all four.`
- End with: `<n> briefs checked, <n> flagged, <n> flags in total.`
- Keep the tone plain and useful: say what's missing, not what's wrong with the author. Don't suggest rewrites unless the student asks; if they do, offer the smallest change that would turn each flag into a pass.
- Don't save the report anywhere unless the student asks. If they do, save it next to the brief(s) as `review-checklist-output.txt`.
