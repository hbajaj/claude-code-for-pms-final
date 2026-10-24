# Support tickets from the September interviews

Draft by the Dispatch PM for Nadia Hoffmann (Support lead).
Sofia Marino's console-redesign interviews (2–5 Sep 2026) raised 14 issues that never reached support.
Aunt Dot, Kip and Halloran have **never** filed a ticket, and Mr. Ambrose has filed one (3043).
Two of these handlers look after responders who were starved of pings after 4.2, so these issues are missing from the ticket counts.

The Rook database is read-only from here, so these are **drafts to enter**. `interview-tickets.csv` has the same 14 in the `support_tickets` column order for import.
Draft IDs (D-01…) are placeholders; support assigns real ticket numbers on entry. "Related" lists existing tickets on the same issue, for linking.

## Summary

| ID | Handler / responder | Subject | Priority | Related |
| --- | --- | --- | --- | --- |
| D-01 | Aunt Dot / Vesper | Very quiet stretches: Vesper hardly being pinged | **Urgent** | Starved-responder pattern (Farlight, The Undertow tickets) |
| D-02 | Aunt Dot / Vesper | Ping gone before Vesper can reach the phone | **High** | 3043 and other "gone before I could answer" tickets |
| D-03 | Aunt Dot / Vesper | Console text too small to read at a glance | Normal | 3013, 3142 |
| D-04 | Aunt Dot / Vesper | Tell the handler when a callout comes in for her responder | Normal | Handler Phone App brief |
| D-05 | Kip / Meteor Mite | Meteor Mite almost no callouts while The Gale is overloaded | **Urgent** | Starved-responder pattern |
| D-06 | Kip / Meteor Mite, The Gale | Dark mode for the console | Normal | 3018, 3029, 3105, 3117 |
| D-07 | Kip / Meteor Mite, The Gale | Different alert sound per responder | Normal | 3031, 3127 |
| D-08 | Mr. Ambrose / Captain Vantage | Callout moved on while Captain Vantage was suiting up (again) | **High** | 3043 (his own, 13 Aug) |
| D-09 | Mr. Ambrose / Captain Vantage | Saved filters reset to default after updates, silently | **High** | 3044, 3064, 3072, 3134 |
| D-10 | Mr. Ambrose / Captain Vantage | Larger text on the status badge | Normal | 3013, 3142 |
| D-11 | Mr. Ambrose / Captain Vantage | Capability tag legend hard to find | Low | 3037, 3087 |
| D-12 | Halloran / Sgt. Bulwark | Requisition priority field does nothing; plate waited 11 days | **High** | 3021, 3063, 3074, 3128 |
| D-13 | Halloran / Sgt. Bulwark | Field failure reports get no response | Normal | 3032, 3101 |
| D-14 | Halloran / Sgt. Bulwark | Equipment catalog search; add category filters | Normal | 3001, 3095 |

Priorities are my suggestion: **Urgent** = a responder losing work now; **High** = a callout lost, gear safety, or a handler unknowingly watching the wrong list.
Also raised but not ticketed: Halloran said maintenance scheduling has improved, and Bulwark lost an August callout before he had his boots on (covered by D-02's theme).

## Tickets

**D-01 · Very quiet stretches: Vesper hardly being pinged** — Aunt Dot / Vesper · interview 3 Sep · Urgent
Dot reports stretches, more than one, where Vesper's phone "just sits there" and he's home all week. She hadn't connected it to anything. Ping data shows Vesper went from 86 pings before 4.2 (12 Aug) to 17 after, with 5 taken. Same pattern as Farlight, The Undertow and Meteor Mite. Link to the routing fix proposal.

**D-02 · Ping gone before Vesper can reach the phone** — Aunt Dot / Vesper · interview 3 Sep · High
When a ping arrives, Vesper is often upstairs. By the time he reaches the phone it has "gone to somebody else". Dot says this happens more than it used to, and he now loses that race more often than he wins it. Consistent with the 4.2 ping wait cut from 90s to 60s.

**D-03 · Console text too small to read at a glance** — Aunt Dot / Vesper · interview 3 Sep · Normal
Dot uses the console standing up, on a kitchen counter. From normal standing distance she can't tell whether something has changed without leaning in.

**D-04 · Tell the handler when a callout comes in for her responder** — Aunt Dot / Vesper · interview 3 Sep · Normal
Dot hears Vesper's phone buzz through the ceiling and shouts up to him. She'd like her own notification when a callout comes in for him. She doesn't need to act on it, just to know. Input for the Handler Phone App brief.

**D-05 · Meteor Mite almost no callouts while The Gale is overloaded** — Kip / Meteor Mite · interview 4 Sep · Urgent
Kip handles two responders in the same area, Eastgate. Meteor Mite has been texting Kip "all week" asking if something's broken, while The Gale "hasn't stopped". Kip has nothing to tell either of them. Ping data shows Meteor Mite went from 70 pings before 4.2 to 14 after, with 3 taken, while The Gale went from 82 to 69. Same area, so distance doesn't explain it. Starved-responder pattern; link to the routing fix proposal.

**D-06 · Dark mode for the console** — Kip / Meteor Mite, The Gale · interview 4 Sep · Normal
Kip works nights on three screens, and the console is "a wall of white light". The OS colour filter makes it unreadable. This is Kip's top request.

**D-07 · Different alert sound per responder** — Kip / Meteor Mite, The Gale · interview 4 Sep · Normal
Both responders trigger the same "bing", so Kip has to look to see which one it's for. That trips him up late at night.

**D-08 · Callout moved on while Captain Vantage was suiting up (again)** — Mr. Ambrose / Captain Vantage · interview 2 Sep · High
Around 19 Aug, a callout went to someone else while Captain Vantage was "coat on, one boot on". Ambrose heard about it afterwards from Vantage, not from the console. He says it's the closest-run he's seen, that it wasn't the first this year, and that slower responses used to still win the job. Follow-up to his own ticket 3043 (13 Aug). Ambrose asks that the console's live-callout indicator be made harder to miss.

**D-09 · Saved filters reset to default after updates, silently** — Mr. Ambrose / Captain Vantage · interview 2 Sep · High
Twice, Ambrose's saved filters reverted to default after what he assumes was an update. He was looking at the wrong list for about 15 minutes before noticing. He wants a warning when filters reset. Same as 3044, 3064, 3072 and 3134. See the filter section of open-questions.md.

**D-10 · Larger text on the status badge** — Mr. Ambrose / Captain Vantage · interview 2 Sep · Normal
At a glance Ambrose sometimes can't tell "engaged" from "available" without leaning in.

**D-11 · Capability tag legend hard to find** — Mr. Ambrose / Captain Vantage · interview 2 Sep · Low
The legend sits in a drawer off the responder detail panel. Ambrose needs it when an unfamiliar tag appears, and had to look one up twice this spring.

**D-12 · Requisition priority field does nothing; plate waited 11 days** — Halloran / Sgt. Bulwark · interview 5 Sep · High (gear safety)
Halloran ordered a replacement vest plate for a real crack, not a cosmetic one. It waited 11 days for a quartermaster signature. He set the priority field, but every requisition sits in one queue, "laces or plate". Rook Supply. Relevant to the Requisition Approval Chains brief, which wouldn't fix this.

**D-13 · Field failure reports get no response** — Halloran / Sgt. Bulwark · interview 5 Sep · Normal
Filing is quick, but reports "go into a void". There's no sign anyone read them or acted on them. Rook Supply.

**D-14 · Equipment catalog search; add category filters** — Halloran / Sgt. Bulwark · interview 5 Sep · Normal
Searching "plate" returned about 40 results, half unrelated. He needs category filters. Rook Supply.

## Suggested follow-ups for support
- Contact Aunt Dot and Kip directly about D-01 and D-05, so they know it's being looked at. Their responders' quiet weeks have a cause.
- Confirm with each handler before entering. These were raised in a research call, not filed by them.
