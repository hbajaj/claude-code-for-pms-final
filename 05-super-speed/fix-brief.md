# Brief: when a responder goes quiet, nobody should have to guess why

For Helen Achebe, Director of Product. From the Dispatch PM. 7 Nov 2026. A draft, not a slide.
**Owner: Himanshu Bajaj, PM for Rook Dispatch.**
Cc Wen Li (Staff Engineer), Marcus Oyelaran (Engineering Manager), Sofia Marino (Product Designer).

## What you asked for
What we'd build instead of quietly changing a number, seen by the people it happens to. Something a handler like Kip
would notice, and something a responder who's gone quiet would feel differently about. And a proper answer to Wen's note in the code.

## Whose story this is: Meteor Mite and Kip
Kip looks after two responders in Eastgate, Meteor Mite and The Gale. They have the same city and the same handler.

| Pings a week | Before 4.2 (29 Jun–8 Aug) | Week of 31 Aug |
|---|---|---|
| Meteor Mite | 10–12 | **1** |
| The Gale | 12–14 | **21** |

After 4.2, Meteor Mite got 14 pings in four weeks and **missed** 8 of them. Each miss cost as much as **turning down** a ping.
That lowered Mite's recent-acceptance score, which lowered Mite's routing priority, which meant fewer pings. The only way back was a ping that never came.

Here's what each of them saw:
- **Mite:** a silent phone, and kept texting Kip to ask whether something was broken.
- **The Gale:** picked up the slack and, in Kip's words, was "exhausted".
- **Kip:** two coverage cards side by side telling opposite stories, with nothing on screen to explain the difference. Kip told Mite to hang in there. Kip's ask: make it "look less like a coincidence".

## What changes for Meteor Mite (phone app)
1. **The ping says who it's for.** It shows the responder, the area and the capability tags, with the ping wait counting down from the first second.
   Mite's ping gets its own sound, so it doesn't sound like The Gale's (Kip's ask).
2. **A missed ping is a missed ping, not a no.** The phone says: *"You missed a callout at 23:40. That doesn't count against you."*
   Turn-downs still come at a median of ~22s, so a miss means the ping was noticed late, not that Mite decided slowly.
3. **We ask instead of guessing.** After 3 missed pings in a row: *"Still on duty?"* with **I'm here** or **Going off duty**.
   "Going off duty" updates the Responder Availability Record, which Supply also reads. Today a 3-miss streak silently lowers the score.
4. **A quiet week comes with a reason.** *"You've had 4 pings this week. You usually get about 11. Here's why, and here's what's changed."* Mite isn't left wondering whether they've been forgotten.
5. **Still open? You can still take it.** If nobody else has taken the callout, Mite gets one more offer after missing it. (Routing v2's second round. Built and tested, not deployed.)

## What changes for Kip (console)
6. **Each coverage card shows this week's pings against the responder's usual,** with a one-line reason:
   *"Meteor Mite · 1 ping this week (usually ~11) · 3 missed in a row, asked Mite to confirm on duty."*
   *"The Gale · 21 pings (usually ~13) · covering most of Eastgate."*
7. **Live ping status on the card:** *"Pinging Meteor Mite · 64s left · next: The Gale."*
8. **A heads-up when a responder drops below half their usual pings,** so Kip hears it from Rook before hearing it from Mite.

## Wen's note, answered properly
Wen's 2019 TODO asked whether a score should ease back toward neutral on its own. The case for: a bad month shouldn't follow someone into spring. The case against: if someone has stopped taking work, that should stick.
**We keep both by asking the responder.** A slow-to-the-phone responder recovers automatically, and the recovery goes back to *their own* usual level, not just neutral.
Someone who really has stopped answering is marked off duty, which they confirm themselves, instead of being punished silently.
Today's recovery stops at neutral (0.5), which is still below everyone else's 0.72 or higher.

## What's already live, and what this changes
- Live since 24 Oct, approved by you: misses are scored separately, scores recover 0.02 a day, the ping wait is back at **90 seconds**, and the four starved responders' scores are restored.
  The ping wait stays at 90s, but that number is not the fix. Items 1–8 are, and none of them depends on the wait length.
- **New:** items 1–4 and 6–8 (Sofia designs them, Wen scopes them), item 5 (Wen reviews v2), and the recovery change above (Wen).

## How we'll know it worked
- Meteor Mite is back to ~10–12 pings a week and The Gale back to ~12–14. No available responder goes a week without a ping.
- Missed pings return to 2–6 a week. "Phone never goes off" tickets stop. Kip stops having to say "hang in there".
- Acceptance rate goes back to 75–78%, watched **alongside** the others, because on its own it rose while Mite disappeared.
  Ravi Menon confirms the numbers. Nadia Hoffmann tracks the ticket split.

## Not in this brief
- Dark mode, Kip's top ask. It's real, but it belongs to the console redesign.
- 4.2's ranking weights (proximity 0.60, acceptance 0.25). Priya's goal of favouring the nearby responder stands, but the weights need their own review.

**Next:** a clickable prototype of Meteor Mite's phone and Kip's coverage cards, so you can walk through the week before and after.
