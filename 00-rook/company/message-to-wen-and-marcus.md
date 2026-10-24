# Message to Wen and Marcus — ready to send

Draft from the Dispatch PM. **Not sent.** Send by Slack or email, with the repo link.

---

> To: Wen Li, Marcus Oyelaran
> Subject: Routing fix + score restore: approved by Helen, need your call on timing
>
> Hi Wen, hi Marcus,
>
> Helen has approved two things for Dispatch routing. I'd like your review and a decision on how we ship them.
>
> **What's wrong.** Since 4.2, a missed ping (no answer within the 60s wait) costs a responder the same as a turn-down. Scores never recover on their own, and a low score means fewer pings. Four responders have been effectively switched off since mid-August: Vesper, Meteor Mite, Farlight and The Undertow. Their pings fell from 70–86 before 4.2 to 11–17 after. This explains the "phone never goes off" tickets Nadia has been tracking, and Marcus, it answers your 14 Aug question. The acceptance-weight cut actually helped responders who turn jobs down. The harm comes from misses being scored as turn-downs.
>
> **What's approved:**
> 1. **The miss-rule fix.** A single miss costs nothing, and the 3rd or later miss in a row costs a turn-down. Scores ease back toward neutral at 0.02 a day. It's in the repo under `00-rook/code/dispatch-routing/`, and basic checks pass locally.
> 2. **Restoring the four responders' scores** to their pre-4.2 values: Vesper 0.96, Meteor Mite 1.00, Farlight 0.84, The Undertow 0.88. Neutral would still leave them below everyone else. Uses `history.restore()`.
>
> **What I need from you:**
> - Wen: a review of the code and values. Please also confirm the live scores before we restore, since mine are replayed from the ping log, and tell me whether scores survive a deploy, because that decides how the restore runs.
> - Both: hotfix or 4.3? The fix has to land before or with the restore, or one bad evening puts them back at zero.
> - One more change, which I've decided and am confirming with Helen: **ping wait back to 90s**. At 60s, misses went from 1–3% of pings to 13–22%. That's the trigger for the spiral and the other third of tickets ("gone before I could answer"). It's one value in `config.py`, and I'd like it to ship with the fix so we're back to known behaviour. Marcus, flagging per the note at the top of config.py.
>
> Details are in `00-rook/company/`: routing-fix-proposal.md, score-reset-request.md, how-routing-works.md (please check it, it's my first attempt at writing routing down) and dispatch-guardrail-metrics.md.
>
> Happy to walk through it whenever suits.
>
> [Name], Dispatch PM
